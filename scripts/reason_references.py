"""Review internal references in reason text without rewriting any data.

Exact current batch directory names and dated ruling IDs are public citations.
Code operands and corroborated source-line references also remain valid. Other
matching or ambiguous forms need a reviewer to supply a public explanation.
This check is deliberately independent of the network and of Git history.
"""
import re

NUMBER_LIST = r"\d+(?:\s*[/,&+\-]\s*\d+)*"
PATTERNS = {
    "tracker reference": re.compile(
        rf"\b(?:tasks?\s*[-_#:]?\s*|(?:bmdb|benchmarking_db|"
        rf"aurora[_-]lint|tools[_-]sqc)\s+(?:tasks?\s+)?){NUMBER_LIST}\b", re.I
    ),
    "numbered review": re.compile(r"\b(?:rounds?|batch(?:es)?|ledger)\s*[-_#:]?\s*\d+\b", re.I),
    "label row reference": re.compile(r"\bgt[-_]\d+\b", re.I),
    "abbreviated batch": re.compile(r"\b\d+(?:-\d+)?_b\d+(?:/(?:\d+(?:plus)?_)?b\d+)*\b", re.I),
    "numbered machine": re.compile(r"\b(?:dev|windev)[-_]\d+\b|\br\d{3,4}\b", re.I),
    "bare tracker context": re.compile(
        r"\b(?:the\s+)?\d{3,5}\s+(?:FP\s+pattern|mechanism\s+[A-Z]\d|stores_params|reconciliation)\b"
        r"|\brelated\s+to\s+\d{3,5}\b|\bwhich\s+\d{3,5}\s+confirmed\b"
        r"|\b\d{3,5}(?:-\d{3,5}){1,4}\s+reconciliation\b"
        r"|\bbatches\s*\(\d+(?:/\d+)+\)"
        r"|\(name-shape/summary gap,\s*\d+\)", re.I
    ),
    "commit with tracker number": re.compile(r"\b[0-9a-f]{7,40}\s*\(\d{3,5}(?:\s+[^)]{1,100})?\)"),
    "dated batch alias": re.compile(r"\bbmdb\s+\d{4}-\d{2}-\d{2}(?:-[a-z0-9]+)+\b", re.I),
}
RULING = re.compile(r"\b[A-Z]{3}\d{2}-C/\d{4}-\d{2}-\d{2}/[^\s,;)]+")
TOKEN = re.compile(r"[\w.-]+")
P_TOKEN = re.compile(r"\bP\d+\b")
CODE_OPERANDS = {"P0", "P2", "P3", "P4", "P5", "P11", "P15", "P521"}
HASH_NUMBER = re.compile(r"(?<![\w/#])#\d+\b")
BARE_FINDING = re.compile(r"\b(?:the|same as|per|see)\s+(\d{3,5})\s+(?:finding|case|precedent|correction|ruling)\b", re.I)
NAMED_READ = re.compile(r"\b(?:per|matches)\s+([a-z][a-z0-9_-]*)['’]s\s+(?:original\s+)?read\b", re.I)
PUBLIC_READERS = {"adjudicator", "reviewer", "maintainer", "owner"}


def reference_categories(reason: str, batch_ids: set[str], file_path: str = "",
                         evidence_lines: set[tuple[str, str, str]] | None = None,
                         codebase_commit: str = "") -> set[str]:
    """Return review failures, scanning only the supplied reason.

    Batch names come from existing directories, never from arbitrary text that
    happens to resemble one. Bare finding numbers are accepted only when they
    resolve to a labeled source line in the same file and pinned commit;
    unresolved forms fail.
    Unknown P tokens require review instead of being assumed to be code.
    """
    protected = [(m.start(), m.end()) for m in TOKEN.finditer(reason)
                 if m.group() in batch_ids]
    protected += [(m.start(), m.end()) for m in RULING.finditer(reason)]

    def is_protected(match):
        for start, end in protected:
            if start <= match.start() and match.end() <= end:
                return True
            digits = list(re.finditer(r"\d+", match.group()))
            if digits and all(start <= match.start() + d.start()
                              and match.start() + d.end() <= end for d in digits):
                return True
        return False

    categories = set()
    for category, pattern in PATTERNS.items():
        if any(not is_protected(m) and not
               (category == "numbered review" and m.group() == "ROUND8")
               for m in pattern.finditer(reason)):
            categories.add(category)
    for m in P_TOKEN.finditer(reason):
        if not is_protected(m) and m.group() not in CODE_OPERANDS:
            categories.add("ambiguous numbered token")
    for m in HASH_NUMBER.finditer(reason):
        if is_protected(m):
            continue
        # A public compiler issue in the existing reasons is explicitly
        # identified by this evidence context. Other shorthand needs review.
        prefix = reason[max(0, m.start() - 65):m.start()]
        if not re.search(r"GCC version-bug threshold\s*\(issue\s*$", prefix):
            categories.add("ambiguous numbered reference")
    for m in BARE_FINDING.finditer(reason):
        evidence_key = (codebase_commit, file_path, m.group(1))
        if not is_protected(m) and evidence_key not in (evidence_lines or set()):
            categories.add("unresolved source-line reference")
    for m in NAMED_READ.finditer(reason):
        if not is_protected(m) and m.group(1).lower() not in PUBLIC_READERS:
            categories.add("named read attribution")
    return categories
