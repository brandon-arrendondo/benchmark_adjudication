#!/usr/bin/env python3
"""Validate data/*/adjudication.csv and batches/*/manifest.json.

Pure stdlib, no dependencies — this runs in CI on every PR against
untrusted diffs, so it stays cheap and has nothing to install.

Checks:
  - CSV header matches the canonical column set exactly.
  - codebase_commit / aurora_lint_sha are full 40-char lowercase hex, never
    abbreviated (see README: two spellings of one commit already split a
    project's labels into two disagreeing sets once, in benchmarking_db).
  - verdict is one of TP/FP/uncertain/FN.
  - line is a positive integer.
  - (project, codebase_commit, file_path, line, rule_id) is unique within a
    project's CSV, matching ground_truth's own UNIQUE constraint.
  - every row's `source` names a batch_id with a manifest under batches/.
  - every manifest's declared row_count matches the number of CSV rows
    actually carrying that batch_id as their source.
  - every manifest's required fields are present and SHA-shaped.
  - every manifest submitted on or after RECHECK_REQUIRED_FROM states what it
    re-checked: a `recheck` block, or `"recheck": null` for a batch of new
    labels only; a manifest with a `corrections` block needs a real one. The
    block's fields are checked for shape and for consistency with the
    manifest's own counts (see check_recheck).
  - every data/*/adjudication.csv is LF-terminated with no CR byte anywhere
    (see check_line_terminators for why this is an error, not a warning).
  - rulings/: dated ruling ids, a rule file or an unruled entry for every
    labelled rule, and a well-formed rule-text pin for every labelled rule
    with a CERT C page (see check_rulings).
  - no free-text field (reason/provenance/confidence) contains a
    backslash-escaped quote (\") -- CSV has no backslash-escape convention,
    so this is the signature of a row built by something that assumed
    JSON/Python-style string escaping and never passed through a real CSV
    writer, silently corrupting that row's field boundaries the moment a
    real quote shows up in the text. This is a syntactic check (a fixed
    two-character sequence), not a semantic one, so it doesn't carry the
    false-positive risk of the abandoned secrets scanner below -- it
    doesn't ask CI to judge the content of a field, only the literal
    escaping. Checked on the parsed field value (not raw text), same as
    every other check here -- a field that reads oddly because it
    legitimately quotes a C string literal is still fine either way, since
    a real CSV writer never introduces a bare backslash-quote sequence in
    the first place.

ADR-0007 vocabulary (ADR-0007, clarified 699c5c8a; bmdb 1414, follow-up to 1400):
a public reason/provenance states only the verdict's label basis -- what the
flagged construct is and why it is TP/FP/FN "at the pinned commit" -- and
makes no claim about impact, severity, exploitability, reachability by an
attacker, trigger inputs, reproducibility or sanitizer results. This is a
disclosure-safety rule (stay on good terms with upstream maintainers; don't
frame a finding more aggressively than they may judge it), not a secrets
check, so it is scoped narrower than the abandoned scanner below and tuned
against the corpus rather than dropped. Two known false-positive classes,
both allowlisted rather than pattern-loosened: (1) plain CFG/dead-code
"reachable" (MSC07/13/17-C's own subject matter) vs. an attacker-reachability
claim -- ADR0007_PATTERNS['reachable_threat'] requires attacker/remote/
network/untrusted context within ~25 chars; (2) CERT-C's own advisory/
recommendation "severity" (e.g. "low-severity const opportunity" on a
DCL06-C/DCL13-C style hit) vs. a vulnerability-severity claim --
SEVERITY_TAXONOMY_CONTEXT excludes a severity_word hit when rule-taxonomy
vocabulary (advisory, recommendation, style, DCL\\d\\d-C, ...) appears in the
same clause. Warn-only on legacy rows (adjudicated before this check
landed): warn: not add to `errors`, so 172k rows already in the corpus at
tune-in-time don't retroactively break CI. Fail on any row adjudicated on or
after ADR0007_CHECK_LANDING_DATE, so a new row can't reintroduce the
vocabulary. See scripts/adr0007_vocabulary_counts.py for a per-project/rule
breakdown of the legacy warnings -- validate.py itself prints only a count,
same lesson as the secrets scanner below: a per-row dump trains reviewers to
click past it.

Deliberately NOT checked here: whether a free-text field discloses a secret
or internal address. An earlier version of this script regex-scanned
reason/provenance/confidence/notes/requested_by for that, and its first real
run (benchmarking_db's initial population, 2026-09-16) flagged 311 rows that
were all false positives -- ordinary C identifiers like `nToken`/`pToken`
matching a generic `token\\s*[:=]` pattern in adjudication reasoning text, not
credentials. Brandon's call: don't fight the false-positive fight on secrets
detection with a regex; this is a reviewer judgment call instead -- see the
PR template's checklist item and README's Accountability section. A
mechanical scanner either misses a disclosure worded in a way it didn't
anticipate, or -- as happened here -- trains reviewers to click past its
noise, both worse than not having it.

Exits 1 with all violations listed (not just the first) on failure.
"""
import csv
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
BATCHES_DIR = REPO_ROOT / "batches"
RULINGS_DIR = REPO_ROOT / "rulings"

CSV_COLUMNS = [
    "project", "codebase_commit", "file_path", "line", "rule_id", "verdict",
    "adjudicator", "reason", "source", "adjudicated_at", "provenance",
    "confidence",
]
# FN (false negative): a real bug found by reading the file, with no
# matching aurora-lint finding at that line/rule. Never affects precision;
# counts as a known real bug for recall once some future aurora-lint version
# actually flags it. Matches benchmarking_db's insert_ground_truth_labels
# convention exactly, so a merge here round-trips with no translation.
VALID_VERDICTS = {"TP", "FP", "uncertain", "FN"}
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
BACKSLASH_QUOTE_RE = re.compile(r'\\"')

# Date (not datetime) this check landed on main -- see the ADR-0007 docstring
# note above. Compared against adjudicated_at's leading YYYY-MM-DD only;
# adjudicated_at has accumulated several ISO-variant spellings over the
# corpus's history (bare date, full timestamp, with/without a UTC suffix),
# but they all share that prefix, and lexicographic comparison on it sorts
# the same as the dates themselves.
ADR0007_CHECK_LANDING_DATE = "2026-09-21"

ADR0007_PATTERNS = {
    "crafted": re.compile(r"\bcrafted\b", re.I),
    "attacker": re.compile(r"\battacker\b", re.I),
    "exploit": re.compile(r"\bexploit(?:s|ed|able|ability)?\b", re.I),
    "reachable_threat": re.compile(
        r"\b(?:attacker|remote(?:ly)?|network|external(?:ly)?|untrusted|malicious)"
        r"[\w\s-]{0,25}reachab(?:le|ility)\b"
        r"|\breachab(?:le|ility)[\w\s-]{0,25}"
        r"(?:attacker|remote(?:ly)?|network|untrusted|malicious)\b",
        re.I,
    ),
    "oob": re.compile(r"\boob\b|\bout[- ]of[- ]bounds\b", re.I),
    "heap_buffer_overflow": re.compile(r"\bheap-buffer-overflow\b", re.I),
    "overflow_asan": re.compile(r"\boverflow\s+(?:WRITE|READ)\b", re.I),
    "crash": re.compile(r"\bcrash(?:es|ed|ing)?\b", re.I),
    "dos": re.compile(r"\bDoS\b"),
    "poc": re.compile(r"\bPoC\b|\bpoc/", re.I),
    "sanitizer_tool": re.compile(r"\b(?:ASan|UBSan|valgrind|GDB|sanitizer)\b", re.I),
    "reproduced": re.compile(r"\breproduc(?:ed|ible|es)\b", re.I),
    "live_at_head": re.compile(r"\blive at HEAD\b", re.I),
    "segfault": re.compile(r"\bsegfault\b|\bSIGSEGV\b", re.I),
    "severity_word": re.compile(
        r"\b(?:low|medium|high)[- ]severity\b|\bseverity\b|\bcritical\b|\bCVSS\b", re.I
    ),
    "vulnerable": re.compile(r"\bvulnerab(?:le|ility)\b", re.I),
    "trigger_threat": re.compile(
        r"\btrigger(?:ed|ing|s)?\s+(?:by\s+)?(?:an?\s+)?"
        r"(?:attacker|remote|malicious|crafted|untrusted)\b"
        r"|\b(?:attacker|remote|malicious|crafted|untrusted)[\w\s-]{0,15}trigger",
        re.I,
    ),
    "sqli_payload": re.compile(r"UNION\s+SELECT|DROP\s+TABLE|OR\s+1\s*=\s*1", re.I),
    "remote_input": re.compile(
        r"\bremote(?:ly)?[\w\s-]{0,15}\b(?:input|controlled|data|attacker)\b", re.I
    ),
}

# CERT-C rule taxonomy uses "severity" for its own advisory/recommendation/rule
# strength (e.g. "genuine low-severity const opportunity" on a DCL06-C/DCL13-C
# style hit) -- a rule-classification statement, not a vulnerability-severity
# claim. A severity_word hit in this context is allowlisted. Measured on the
# 172k-row corpus at tune-in-time: this excludes ~97% of raw severity_word
# hits, all confirmed rule-taxonomy usage on advisory-level style/const rules.
SEVERITY_TAXONOMY_CONTEXT = re.compile(
    r"advisory|recommendation|readability|style|const\b|magic number"
    r"|DCL\d{2}-C|checked-return|conformance|intent|opportunity",
    re.I,
)


def adr0007_hit_categories(text: str) -> set[str]:
    """ADR-0007-restricted vocabulary categories present in `text`, if any."""
    hits: set[str] = set()
    for name, pat in ADR0007_PATTERNS.items():
        m = pat.search(text)
        if not m:
            continue
        if name == "severity_word":
            window = text[max(0, m.start() - 70) : m.end() + 70]
            if SEVERITY_TAXONOMY_CONTEXT.search(window):
                continue
        hits.add(name)
    return hits

MANIFEST_REQUIRED_FIELDS = [
    "batch_id", "work_item_ref", "adjudicator", "aurora_lint_version",
    "aurora_lint_sha", "projects", "codebase_commits", "submitted_at",
    "row_count",
]


# Re-check metadata (benchmarking_db 1889). Before this, what a correction
# batch re-checked lived only in free-text notes, so a flip rate needed a hand
# reading of every manifest, and about 300 flips have no rate because no note
# says how many labels were looked at. Manifests submitted before the cutoff
# are left as they are.
RECHECK_REQUIRED_FROM = "2026-10-01"
RECHECK_BASES = ("ruling", "standard", "merit", "tool", "conflict")
RECHECK_SELECTIONS = ("census", "sample", "tool-prompted", "targeted")
RECHECK_FIELDS = ("basis", "selection", "reviewed", "flipped",
                  "blind_to_prior_verdict", "blind_to_diagnostic")
BLIND_SLICE_FIELDS = ("seed", "reviewed", "disagreed",
                      "blind_to_prior_verdict", "blind_to_diagnostic")
# A `corrections` key that changes a verdict ("FP_to_TP"); any other key
# ("TP_restated") records a row rewritten with its verdict kept.
VERDICT_CHANGE_KEY = re.compile(r"^(TP|FP|FN)_to_(TP|FP|FN)$")


def verdict_changes(corrections: dict) -> int:
    return sum(v for k, v in corrections.items()
               if (m := VERDICT_CHANGE_KEY.match(k)) and m.group(1) != m.group(2))


def _count(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def check_recheck(manifest: dict, where: str) -> list[str]:
    """Errors in a manifest's `recheck` block, or in its absence.

    The block says what a correction or re-check batch looked at, so a flip
    rate is flipped / reviewed with nothing read out of the notes:

      basis      ruling | standard | merit | tool | conflict -- one per batch,
                 because a ruling relabel and a merit re-read measure
                 different things and a pooled rate reads as neither
      ruling     for basis ruling or standard: the decision it applies
      selection  census | sample | tool-prompted | targeted; a sample
                 also names its `seed`
      reviewed   labels re-checked, the ones kept as well as the ones changed
      flipped    labels whose verdict changed; equal to the verdict-changing
                 `corrections` keys when there are any
      blind_to_prior_verdict, blind_to_diagnostic   what the reader could see
      blind_slice  optional: {seed, reviewed, disagreed,
                 blind_to_prior_verdict, blind_to_diagnostic} for the small
                 blind re-label the batch carried alongside

    Whether `flipped` matches the rows the batch actually changed needs the
    history, which this script does not read; benchmarking_db's
    oracle_flip_rates.py checks it and refuses a mismatch.
    """
    errors: list[str] = []
    submitted = str(manifest.get("submitted_at") or "")
    due = submitted[:10] >= RECHECK_REQUIRED_FROM
    if "recheck" not in manifest:
        if due:
            errors.append(f"{where}: missing 'recheck' (a re-check block, or null for a "
                          f"batch of new labels only; required from {RECHECK_REQUIRED_FROM})")
        return errors
    block = manifest["recheck"]
    if block is None:
        if "corrections" in manifest:
            errors.append(f"{where}: has 'corrections' but 'recheck' is null; a correction "
                          f"batch states what it re-checked")
        return errors
    if not isinstance(block, dict):
        return [f"{where}: 'recheck' must be an object or null"]

    for field in RECHECK_FIELDS:
        if field not in block:
            errors.append(f"{where}: recheck is missing '{field}'")
    basis, selection = block.get("basis"), block.get("selection")
    if "basis" in block and basis not in RECHECK_BASES:
        errors.append(f"{where}: recheck.basis {basis!r} is not one of {', '.join(RECHECK_BASES)}")
    if basis in ("ruling", "standard") and not str(block.get("ruling") or "").strip():
        errors.append(f"{where}: recheck.basis {basis} needs 'ruling' naming the decision "
                      f"it applies")
    if "selection" in block and selection not in RECHECK_SELECTIONS:
        errors.append(f"{where}: recheck.selection {selection!r} is not one of "
                      f"{', '.join(RECHECK_SELECTIONS)}")
    if selection == "sample" and block.get("seed") is None:
        errors.append(f"{where}: recheck.selection sample needs its 'seed'")
    for field in ("reviewed", "flipped"):
        if field in block and not _count(block[field]):
            errors.append(f"{where}: recheck.{field} must be a non-negative integer")
    for field in ("blind_to_prior_verdict", "blind_to_diagnostic"):
        if field in block and not isinstance(block[field], bool):
            errors.append(f"{where}: recheck.{field} must be true or false")

    reviewed, flipped = block.get("reviewed"), block.get("flipped")
    if _count(reviewed) and _count(flipped):
        if flipped > reviewed:
            errors.append(f"{where}: recheck.flipped {flipped} exceeds reviewed {reviewed}")
        # Not checked against row_count: that counts the rows that carry this
        # batch as their source now, and drops when a later correction
        # supersedes some of them.
        corrections = manifest.get("corrections")
        if isinstance(corrections, dict) and all(_count(v) for v in corrections.values()):
            changed = verdict_changes(corrections)
            if changed != flipped:
                errors.append(f"{where}: recheck.flipped {flipped} does not equal the "
                              f"verdict-changing corrections total {changed}")

    blind = block.get("blind_slice")
    if blind is not None:
        if not isinstance(blind, dict):
            errors.append(f"{where}: recheck.blind_slice must be an object")
        else:
            for field in BLIND_SLICE_FIELDS:
                if blind.get(field) is None:
                    errors.append(f"{where}: recheck.blind_slice is missing '{field}'")
            for field in ("reviewed", "disagreed"):
                if field in blind and not _count(blind[field]):
                    errors.append(f"{where}: recheck.blind_slice.{field} must be a "
                                  f"non-negative integer")
            for field in ("blind_to_prior_verdict", "blind_to_diagnostic"):
                if field in blind and not isinstance(blind[field], bool):
                    errors.append(f"{where}: recheck.blind_slice.{field} must be true or false")
            if (_count(blind.get("reviewed")) and _count(blind.get("disagreed"))
                    and blind["disagreed"] > blind["reviewed"]):
                errors.append(f"{where}: recheck.blind_slice.disagreed exceeds its reviewed")
    return errors


def fail(errors: list[str]) -> None:
    print(f"validate.py: {len(errors)} error(s):", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)


def load_manifests(errors: list[str]) -> dict[str, dict]:
    manifests: dict[str, dict] = {}
    if not BATCHES_DIR.exists():
        return manifests
    for manifest_path in sorted(BATCHES_DIR.glob("*/manifest.json")):
        batch_dir_name = manifest_path.parent.name
        try:
            manifest = json.loads(manifest_path.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"{manifest_path}: invalid JSON ({e})")
            continue

        for field in MANIFEST_REQUIRED_FIELDS:
            if field not in manifest:
                errors.append(f"{manifest_path}: missing required field '{field}'")
        errors.extend(check_recheck(manifest, str(manifest_path)))

        batch_id = manifest.get("batch_id")
        if batch_id and batch_id != batch_dir_name:
            errors.append(
                f"{manifest_path}: batch_id '{batch_id}' does not match "
                f"directory name '{batch_dir_name}'"
            )

        sha = manifest.get("aurora_lint_sha", "")
        if sha and not FULL_SHA_RE.match(sha):
            errors.append(
                f"{manifest_path}: aurora_lint_sha '{sha}' is not a full "
                f"40-char lowercase hex SHA"
            )

        for project, commit in manifest.get("codebase_commits", {}).items():
            if not FULL_SHA_RE.match(commit):
                errors.append(
                    f"{manifest_path}: codebase_commits['{project}']='{commit}' "
                    f"is not a full 40-char lowercase hex SHA"
                )

        manifests[batch_dir_name] = manifest
    return manifests


def validate_csvs(
    errors: list[str], manifests: dict[str, dict], adr0007_warnings: dict[tuple[str, str], int]
) -> dict[str, int]:
    source_row_counts: dict[str, int] = {}
    if not DATA_DIR.exists():
        return source_row_counts

    for csv_path in sorted(DATA_DIR.glob("*/adjudication.csv")):
        project_dir_name = csv_path.parent.name
        seen_keys: set[tuple] = set()

        with csv_path.open(newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != CSV_COLUMNS:
                errors.append(
                    f"{csv_path}: header {reader.fieldnames} does not match "
                    f"expected {CSV_COLUMNS}"
                )
                continue

            for i, row in enumerate(reader, start=2):  # header is line 1
                loc = f"{csv_path}:{i}"

                if row["project"] != project_dir_name:
                    errors.append(
                        f"{loc}: project '{row['project']}' does not match "
                        f"directory '{project_dir_name}'"
                    )

                if not FULL_SHA_RE.match(row["codebase_commit"]):
                    errors.append(
                        f"{loc}: codebase_commit '{row['codebase_commit']}' is "
                        f"not a full 40-char lowercase hex SHA"
                    )

                if row["verdict"] not in VALID_VERDICTS:
                    errors.append(
                        f"{loc}: verdict '{row['verdict']}' not in "
                        f"{sorted(VALID_VERDICTS)}"
                    )

                try:
                    line_no = int(row["line"])
                    if line_no <= 0:
                        raise ValueError
                except ValueError:
                    errors.append(f"{loc}: line '{row['line']}' is not a positive integer")

                if not row["rule_id"]:
                    errors.append(f"{loc}: rule_id is empty")

                for field in ("reason", "provenance", "confidence"):
                    if BACKSLASH_QUOTE_RE.search(row[field]):
                        errors.append(
                            f'{loc}: {field} contains a backslash-escaped quote (\\") '
                            f'-- CSV has no backslash-escape convention; a literal '
                            f'quote in a field must be doubled ("") by a real CSV '
                            f"writer, never hand-escaped (see README, "
                            f'"How labels get added")'
                        )

                hit_categories = adr0007_hit_categories(
                    f"{row['reason']} {row['provenance']}"
                )
                if hit_categories:
                    msg = (
                        f"{loc}: reason/provenance carries ADR-0007-restricted "
                        f"vocabulary ({', '.join(sorted(hit_categories))}) -- state "
                        f"only the verdict's label basis (docs/adr/0007)"
                    )
                    adjudicated_at = row.get("adjudicated_at", "") or ""
                    if adjudicated_at[:10] >= ADR0007_CHECK_LANDING_DATE:
                        errors.append(msg)
                    else:
                        adr0007_warnings[(row["project"], row["rule_id"])] = (
                            adr0007_warnings.get((row["project"], row["rule_id"]), 0) + 1
                        )

                source = row["source"]
                if not source:
                    errors.append(f"{loc}: source is empty")
                elif source not in manifests:
                    errors.append(
                        f"{loc}: source '{source}' has no "
                        f"batches/{source}/manifest.json"
                    )
                source_row_counts[source] = source_row_counts.get(source, 0) + 1

                key = (
                    row["project"], row["codebase_commit"], row["file_path"],
                    row["line"], row["rule_id"],
                )
                if key in seen_keys:
                    errors.append(
                        f"{loc}: duplicate key {key} within {csv_path} "
                        f"(matches ground_truth's UNIQUE constraint)"
                    )
                seen_keys.add(key)

    return source_row_counts


def cross_check_row_counts(
    errors: list[str], manifests: dict[str, dict], source_row_counts: dict[str, int]
) -> None:
    for batch_id, manifest in manifests.items():
        declared = manifest.get("row_count")
        actual = source_row_counts.get(batch_id, 0)
        if declared is not None and declared != actual:
            errors.append(
                f"batches/{batch_id}/manifest.json: declared row_count "
                f"{declared} does not match {actual} actual CSV row(s) "
                f"with source='{batch_id}'"
            )


def check_line_terminators(errors: list[str]) -> None:
    """Reject any CR byte in a data CSV: every file is LF, everywhere.

    A batch generator that rewrites a file instead of appending to it -- or
    that uses Python's csv module without passing lineterminator -- silently
    converts every line to CRLF, turning a small addition into a whole-file
    diff and manufacturing conflicts with any batch in flight. That happened
    twice (the task-1292 merge commit's "CRLF-normalization false conflict
    with 1291", and task-1303) while data/ was mixed by project, and the
    mixed-within-file warning this used to be could not have caught either:
    a uniformly flipped file is not mixed.

    Since benchmarking_db task 1338 every data/*/adjudication.csv is LF and
    .gitattributes (`*.csv text eol=lf`) keeps it so, which makes this a
    plain ERROR with nothing to exempt. It counts every CR, not only CRLF
    record terminators: a CRLF inside a quoted multi-line field would be
    normalized by git's `text` conversion at the next commit anyway, so the
    committed bytes must already be free of it.
    """
    if not DATA_DIR.exists():
        return

    for csv_path in sorted(DATA_DIR.glob("*/adjudication.csv")):
        data = csv_path.read_bytes()
        cr = data.count(b"\r")
        if cr:
            errors.append(
                f"{csv_path}: {cr} CR byte(s) -- every adjudication.csv is LF "
                f"(.gitattributes `*.csv text eol=lf`). Write with "
                f"lineterminator='\\n' (csv writers default to '\\r\\n') and "
                f"append rather than rewrite; see README, "
                f'"How labels get added".'
            )


RULE_ID_RE = re.compile(r"^[A-Z]{3}\d{2}-C$")
RULING_REF_RE = re.compile(r"\b([A-Z]{3}\d{2}-C)/([^/\s`]+)/([0-9A-Za-z_-]+)")
RULING_DEF_RE = re.compile(r"^- \*\*([A-Z]{3}\d{2}-C)/([^/\s`]+)/([0-9A-Za-z_-]+)\b", re.M)
RULING_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def check_rulings(errors: list[str]) -> None:
    """Check rulings/ against itself and against the labels.

    - Every ruling id is `<rule>/<YYYY-MM-DD>/<item>`: dated, so a public
      file never carries an internal task id; a rule file defines only its
      own rule's ids, each once.
    - Every rule_id in data/*/adjudication.csv has rulings/rules/<id>.md or
      is listed in rulings/unruled.md (whose labels cite the principles).
    - rulings/rule-text-map.json parses, each entry is pinned to a full
      commit, a path and a SHA-256, and every labelled rule with a CERT C
      page has an entry (aurora-lint ADR-0018).
    """
    if not RULINGS_DIR.exists():
        return
    rules_dir = RULINGS_DIR / "rules"
    have = {}
    for path in sorted(rules_dir.glob("*.md")):
        rule = path.stem
        text = path.read_text(encoding="utf-8")
        have[rule] = text
        if not RULE_ID_RE.match(rule):
            errors.append(f"{path}: file name is not a CERT C rule id")
        if not text.startswith(f"# {rule}\n"):
            errors.append(f"{path}: first line must be '# {rule}'")
        for m in RULING_REF_RE.finditer(text):
            if not RULING_DATE_RE.match(m.group(2)):
                errors.append(f"{path}: ruling id {m.group(0)} is not dated "
                              f"(<rule>/<YYYY-MM-DD>/<item>)")
        defined = [m.groups() for m in RULING_DEF_RE.finditer(text)]
        for r, _date, _item in defined:
            if r != rule:
                errors.append(f"{path}: defines a ruling id for {r}")
        seen = set()
        for d in defined:
            if d in seen:
                errors.append(f"{path}: ruling id {'/'.join(d)} defined twice")
            seen.add(d)

    unruled_path = RULINGS_DIR / "unruled.md"
    unruled = set()
    if unruled_path.exists():
        unruled = set(re.findall(r"\b([A-Z]{3}\d{2}-C)\b",
                                 unruled_path.read_text(encoding="utf-8")))

    labelled = set()
    for csv_path in sorted(DATA_DIR.glob("*/adjudication.csv")):
        with csv_path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                labelled.add(row["rule_id"])
    for rule in sorted(labelled - set(have) - unruled):
        errors.append(f"rulings: label rule_id {rule} has no rulings/rules/"
                      f"{rule}.md and is not in rulings/unruled.md")

    map_path = RULINGS_DIR / "rule-text-map.json"
    try:
        rule_map = json.loads(map_path.read_text(encoding="utf-8"))["rules"]
    except (OSError, ValueError, KeyError) as exc:
        errors.append(f"{map_path}: unreadable rule-text map ({exc})")
        return
    for rule, entry in sorted(rule_map.items()):
        where = f"{map_path}: {rule}"
        if not FULL_SHA_RE.match(str(entry.get("commit", ""))):
            errors.append(f"{where}: commit is not a full SHA")
        if not str(entry.get("path", "")).endswith(".md"):
            errors.append(f"{where}: path is not a page source")
        if not SHA256_RE.match(str(entry.get("sha256", ""))):
            errors.append(f"{where}: sha256 is not a SHA-256")
    for rule in sorted(labelled - set(rule_map)):
        text = have.get(rule, "")
        if "**Rule text:** none" not in text:
            errors.append(f"{map_path}: labelled rule {rule} has no pin")


def main() -> None:
    errors: list[str] = []
    adr0007_warnings: dict[tuple[str, str], int] = {}
    manifests = load_manifests(errors)
    source_row_counts = validate_csvs(errors, manifests, adr0007_warnings)
    cross_check_row_counts(errors, manifests, source_row_counts)
    check_line_terminators(errors)
    check_rulings(errors)

    if errors:
        fail(errors)

    n_rows = sum(source_row_counts.values())
    print(f"validate.py: OK — {len(manifests)} batch(es), {n_rows} row(s)")
    if adr0007_warnings:
        n_warn = sum(adr0007_warnings.values())
        n_pairs = len(adr0007_warnings)
        print(
            f"validate.py: {n_warn} legacy row(s) across {n_pairs} (project, rule) "
            f"pair(s) carry ADR-0007-restricted vocabulary (warn-only; run "
            f"scripts/adr0007_vocabulary_counts.py for the breakdown)",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
