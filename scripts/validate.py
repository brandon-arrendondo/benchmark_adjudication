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

Deliberately NOT checked here: whether a free-text field discloses a secret
or internal address. An earlier version of this script regex-scanned
reason/provenance/confidence/notes/requested_by for that, and its first real
run (benchmarking_db's initial population, 2026-09-16) flagged 311 rows that
were all false positives -- ordinary C identifiers like `nToken`/`pToken`
matching a generic `token\s*[:=]` pattern in adjudication reasoning text, not
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

MANIFEST_REQUIRED_FIELDS = [
    "batch_id", "work_item_ref", "adjudicator", "aurora_lint_version",
    "aurora_lint_sha", "projects", "codebase_commits", "submitted_at",
    "row_count",
]


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


def validate_csvs(errors: list[str], manifests: dict[str, dict]) -> dict[str, int]:
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


def check_line_terminators(warnings: list[str]) -> None:
    """Report a CSV whose line terminators are not all the same.

    A batch generator that rewrites a file instead of appending to it -- or
    that uses Python's csv module without passing lineterminator -- silently
    converts every line to CRLF, turning a small addition into a whole-file
    diff and manufacturing conflicts with any batch in flight. That has
    happened twice (the task-1292 merge commit's "CRLF-normalization false
    conflict with 1291", and task-1303).

    This is a WARNING, not an error: `data/` is currently mixed by project,
    and at least one file is mixed internally, so failing here would fail CI
    on already-merged data. It flags the file so a reviewer sees the cause
    rather than a 75k-line diff with no explanation.
    """
    if not DATA_DIR.exists():
        return

    for csv_path in sorted(DATA_DIR.glob("*/adjudication.csv")):
        data = csv_path.read_bytes()
        if not data:
            continue
        crlf = data.count(b"\r\n")
        lf = data.count(b"\n") - crlf
        if crlf and lf:
            warnings.append(
                f"{csv_path}: mixed line terminators ({crlf} CRLF, {lf} LF). "
                f"Append with the file's existing terminator "
                f"(csv writers default to lineterminator='\\r\\n')."
            )


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    manifests = load_manifests(errors)
    source_row_counts = validate_csvs(errors, manifests)
    cross_check_row_counts(errors, manifests, source_row_counts)
    check_line_terminators(warnings)

    if errors:
        fail(errors)

    for w in warnings:
        print(f"validate.py: warning: {w}", file=sys.stderr)

    n_rows = sum(source_row_counts.values())
    print(f"validate.py: OK — {len(manifests)} batch(es), {n_rows} row(s)")


if __name__ == "__main__":
    main()
