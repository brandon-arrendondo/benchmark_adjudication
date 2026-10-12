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
        rf"(?<![A-Za-z0-9])(?:tasks?\s*[-_#:]?\s*|(?:bmdb|benchmarking_db|"
        rf"aurora[_-]lint|tools[_-]sqc)\s+(?:tasks?\s+)?){NUMBER_LIST}(?![A-Za-z0-9])", re.I
    ),
    "numbered review": re.compile(r"\b(?:rounds?|batch(?:es)?|ledger)\s*[-_#:]?\s*\d+\b", re.I),
    "internal run number": re.compile(r"\brun(?:\s+|[-_])\d+\b", re.I),
    "internal ruling attribution": re.compile(r"\bcoordinator\b", re.I),
    "label row reference": re.compile(r"\bgt[-_]\d+\b", re.I),
    "abbreviated batch": re.compile(r"\b\d+(?:-\d+)?_b\d+(?:/(?:\d+(?:plus)?_)?b\d+)*\b", re.I),
    "numbered machine": re.compile(r"\bdev[-_]\d+\b", re.I),
    "bare tracker context": re.compile(
        r"\b(?:the\s+)?\d{3,5}\s+(?:FP\s+pattern|mechanism\s+[A-Z]\d|stores_params|reconciliation)\b"
        r"|\brelated\s+to\s+\d{3,5}\b|\bwhich\s+\d{3,5}\s+confirmed\b"
        r"|\b\d{3,5}(?:-\d{3,5}){1,4}\s+reconciliation\b"
        r"|\bbatches\s*\(\d+(?:/\d+)+\)"
        r"|\(name-shape/summary gap,\s*\d+\)", re.I
    ),
    "commit with tracker number": re.compile(r"\b[0-9a-f]{7,40}\s*\(\d{3,5}(?:[,\s]+[^)]{1,100})?\)"),
    "dated batch alias": re.compile(r"\bbmdb\s+\d{4}-\d{2}-\d{2}(?:-[a-z0-9]+)+\b", re.I),
}
RULING = re.compile(r"\b[A-Z]{3}\d{2}-C/\d{4}-\d{2}-\d{2}/[^\s,;)]+")
PUBLIC_RUN_ID = re.compile(r"\bsqc-\d+(?:\.\d+)+-[0-9a-f]{7,40}\b")
AES_ROUNDS = re.compile(r"\bAES(?:-\d+)?\s+rounds?\s+\d+\b", re.I)
TOKEN = re.compile(r"[\w.-]+")
P_TOKEN = re.compile(r"\bP\d+\b")
CODE_OPERANDS = {"P0", "P2", "P3", "P4", "P5", "P11", "P15", "P256", "P384", "P521"}
HASH_NUMBER = re.compile(r"(?<![\w/#])#\d+\b")
BARE_FINDING = re.compile(r"\b(?:the|same as|per|see)\s+(\d{3,5})\s+(?:finding|case|precedent|correction|ruling)\b", re.I)
NAMED_READ = re.compile(r"\b(?:per|matches)\s+([a-z][a-z0-9_-]*)['’]s\s+(?:original\s+)?read\b", re.I)
PUBLIC_READERS = {"adjudicator", "reviewer", "maintainer", "owner"}
PUBLIC_COLUMNS = {"reason", "provenance", "adjudicator"}
PROVENANCE_RUN = re.compile(
    r"\bruns?(?:\s+|[-_])\d+(?:[/,-]\d+)*\b(?!\.\.)", re.I)
PROVENANCE_BATCH = re.compile(
    r"^(?:\d+(?:-\d+|plus)?_)?b\d+$|\bbatch\s+b\d+\b", re.I)
HOST_ATTRIBUTION = re.compile(r"(?<![A-Za-z0-9])r\d{3,}(?![A-Za-z0-9])", re.I)
ADJUDICATOR_CAMPAIGN = re.compile(r"-\d{3,}(?=-|$)", re.I)


def column_reference_categories(column: str, value: str,
                                batch_ids: set[str] | None = None,
                                file_path: str = "",
                                evidence_lines: set[tuple[str, str, str]] | None = None,
                                codebase_commit: str = "") -> set[str]:
    """Review public attribution text; exporter callers can supply batch IDs.

    Source identifiers and pin metadata are intentionally outside this policy.
    Exact batch citations remain valid only when supplied by the caller from
    the dataset's manifest directories. No files or database are read here.
    """
    if column not in PUBLIC_COLUMNS:
        return set()
    batches = batch_ids or set()
    categories = reference_categories(value, batches, file_path, evidence_lines,
                                      codebase_commit)
    if column == "reason":
        return categories
    # Operands, source locations and diagnostic messages in provenance use the
    # same technical exceptions as reasons; extra checks concern attribution.
    text = TOKEN.sub(lambda m: " " if m.group() in batches else m.group(), value)
    if HOST_ATTRIBUTION.search(text):
        categories.add("numbered machine")
    if column == "provenance":
        if PROVENANCE_RUN.search(text):
            categories.add("internal run number")
        if PROVENANCE_BATCH.search(text):
            categories.add("abbreviated batch")
    elif ADJUDICATOR_CAMPAIGN.search(text):
        categories.add("adjudicator campaign reference")
    return categories


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
    protected += [(m.start(), m.end()) for m in PUBLIC_RUN_ID.finditer(reason)]
    protected += [(m.start(), m.end()) for m in AES_ROUNDS.finditer(reason)]
    # Hex commit citations may be all digits; the whole token, never a digit
    # prefix of a SHA, is protected when attributed to the public tool.
    protected += [(m.start(), m.end()) for m in re.finditer(
        r"\b(?:aurora[-_]lint|tools[-_]sqc)\s+[0-9a-f]{7,40}\b", reason)]

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


# Forms a directory name takes that reason text, written in words, does not:
# a tracker or tool prefix joined to its number by `_` or `-` or nothing
# (`delta_x_bmdb90001`, `aurora_lint-90001`, `task90001`), a run number with no
# separator (`run90001`), and a numbered fleet host with or without a prefix
# (`windev-04`, `dev90001`). Names only: the reason and provenance patterns
# above stay as they are, so no existing row is judged again.
NAME_PATTERNS = {
    "tracker reference": re.compile(
        r"(?<![A-Za-z0-9])(?:tasks?|bmdb|benchmarking[_-]db|aurora[_-]lint|tools[_-]sqc)"
        r"[\s_-]*\d+(?!\d)", re.I),
    "internal run number": re.compile(r"(?<![A-Za-z0-9])run[\s_-]*\d+(?!\d)", re.I),
    "numbered machine": re.compile(r"(?<![A-Za-z0-9])(?:win)?dev[\s_-]*\d+(?!\d)", re.I),
}


def manifest_name_categories(name: str, allowlist: set[str] | frozenset[str]) -> set[str]:
    """Review a manifest directory name as a citation, without reading files.

    A batch directory name is cited verbatim by reasons and provenance, which
    therefore accept it (see `column_reference_categories`). The names that
    existed when this check was introduced stay valid as dataset identifiers
    and are passed in as `allowlist`. Any other name is held to the same
    internal-reference policy as reason text, plus the host-name form from
    provenance, so a new batch cannot make an internal reference citable by
    being named after it. Underscores and dots count as separators, as hyphens
    do. Returns the policy categories the name falls under; empty means it may
    be used.
    """
    if name in allowlist:
        return set()
    categories = set()
    for text in {name, re.sub(r"[_.]", "-", name)}:
        categories |= reference_categories(text, set())
        if HOST_ATTRIBUTION.search(text):
            categories.add("numbered machine")
        categories |= {c for c, p in NAME_PATTERNS.items() if p.search(text)}
    return categories


def batch_name_errors(names, allowlist: set[str] | frozenset[str]) -> list[str]:
    """One message per name in `names` that `manifest_name_categories`
    refuses, in the given order; pure, so validate.py and the exporter share
    it without either importing the other."""
    errors = []
    for name in names:
        categories = manifest_name_categories(name, allowlist)
        if categories:
            errors.append(
                f"batches/{name}: the directory name reads as an internal reference "
                f"({', '.join(sorted(categories))}); give the batch a neutral name"
            )
    return errors
