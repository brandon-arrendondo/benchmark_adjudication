#!/usr/bin/env python3
"""Validate data/*/adjudication.csv and batches/*/manifest.json.

Pure stdlib, no dependencies — this runs in CI on every PR against
untrusted diffs, so it stays cheap and has nothing to install.

Checks:
  - CSV header matches the canonical column set exactly.
  - codebase_commit / aurora_lint_sha are full 40-char lowercase hex, never
    abbreviated (see README: two spellings of one commit already split a
    project's labels into two disagreeing sets once, in benchmarking_db).
  - verdict is one of TP/FP/uncertain.
  - line is a positive integer.
  - (project, codebase_commit, file_path, line, rule_id) is unique within a
    project's CSV, matching ground_truth's own UNIQUE constraint.
  - every row's `source` names a batch_id with a manifest under batches/.
  - every manifest's declared row_count matches the number of CSV rows
    actually carrying that batch_id as their source.
  - every manifest's required fields are present and SHA-shaped.
  - free-text fields (reason/provenance/confidence/notes/requested_by) don't
    contain an obvious secret or an internal email address. This repo is
    public, so this is a best-effort net, not a substitute for the reviewer
    actually reading the diff -- see README's Accountability section.

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
VALID_VERDICTS = {"TP", "FP", "uncertain"}
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

MANIFEST_REQUIRED_FIELDS = [
    "batch_id", "work_item_ref", "adjudicator", "aurora_lint_version",
    "aurora_lint_sha", "projects", "codebase_commits", "submitted_at",
    "row_count",
]

# Best-effort net, not a DLP tool -- this repo is public, so the intent is
# to catch an obvious accident (a pasted credential, an internal address),
# not to substitute for the reviewer actually reading the diff.
SENSITIVE_PATTERNS = [
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("generic API key/token", re.compile(r"\b(api[_-]?key|secret|token|password)\s*[:=]\s*\S{8,}", re.IGNORECASE)),
    ("bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9\-._~+/]{20,}")),
    ("internal email address", re.compile(r"[A-Za-z0-9._%+-]+@bissell\.com", re.IGNORECASE)),
]
CSV_FREE_TEXT_COLUMNS = ["reason", "provenance", "confidence"]
MANIFEST_FREE_TEXT_FIELDS = ["notes", "requested_by", "adjudicator"]


def scan_sensitive(loc: str, field: str, value: str, errors: list[str]) -> None:
    if not value:
        return
    for label, pattern in SENSITIVE_PATTERNS:
        if pattern.search(value):
            errors.append(f"{loc}: field '{field}' looks like it contains a {label} -- remove before this goes public")


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

        for field in MANIFEST_FREE_TEXT_FIELDS:
            value = manifest.get(field)
            if isinstance(value, str):
                scan_sensitive(str(manifest_path), field, value, errors)

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

                for field in CSV_FREE_TEXT_COLUMNS:
                    scan_sensitive(loc, field, row.get(field, ""), errors)

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


def main() -> None:
    errors: list[str] = []
    manifests = load_manifests(errors)
    source_row_counts = validate_csvs(errors, manifests)
    cross_check_row_counts(errors, manifests, source_row_counts)

    if errors:
        fail(errors)

    n_rows = sum(source_row_counts.values())
    print(f"validate.py: OK — {len(manifests)} batch(es), {n_rows} row(s)")


if __name__ == "__main__":
    main()
