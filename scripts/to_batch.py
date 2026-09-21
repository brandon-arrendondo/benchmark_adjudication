#!/usr/bin/env python3
"""Turn Brandon's filled-in blind-sample verdicts into a benchmark_adjudication
batch: an in-place correction of the matching rows in data/*/adjudication.csv
(same key, new verdict/reason/adjudicator), plus batches/<batch_id>/manifest.json.
Nothing here pushes anything -- this only writes local files for review
before a PR (bmdb 1317, Item 2 step 3(b)).

Usage:
    python3 scripts/to_batch.py <verdict_csv> <batch_id>

<verdict_csv> is review/2026-09-21/blind_sample.csv with human_verdict
(TP/FP) and human_reason filled in -- blank human_verdict rows are
skipped, so a partial pass (label some, run later, label more) works.
human_reason must be non-empty (ADR-0007: label basis only, same as any
other row in this repo) or the row is rejected with a list at the end,
matching so nothing partial gets silently dropped.

Reassigning a row's `source` to the new batch orphans it from whatever
batch originally contributed it, so that batch's declared row_count would
otherwise go stale and fail validate.py's cross-check. Follows the
existing correction precedent (see bmdb 1281's `e2d94d6`, "Source
manifests get row_count decrements and superseded_rows records"): each
old batch's manifest.json is decremented by the number of rows it lost
and gets (or extends) a `superseded_rows` entry naming the new batch, the
count, and the keys -- an audit trail, not just a silent number change.
"""
import csv
import datetime
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
BATCHES_DIR = REPO_ROOT / "batches"


def main() -> None:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <verdict_csv> <batch_id>", file=sys.stderr)
        sys.exit(2)
    verdict_path, batch_id = Path(sys.argv[1]), sys.argv[2]

    to_apply = []
    rejected = []
    with verdict_path.open(newline="") as f:
        for row in csv.DictReader(f):
            verdict = (row.get("human_verdict") or "").strip().upper()
            reason = (row.get("human_reason") or "").strip()
            if not verdict:
                continue
            if verdict not in ("TP", "FP"):
                rejected.append((row["sample_id"], f"human_verdict '{verdict}' not TP/FP"))
                continue
            if not reason:
                rejected.append((row["sample_id"], "human_reason is empty"))
                continue
            to_apply.append((row, verdict, reason))

    if rejected:
        print(f"{len(rejected)} row(s) rejected, not applied:", file=sys.stderr)
        for sid, why in rejected:
            print(f"  {sid}: {why}", file=sys.stderr)

    if not to_apply:
        print("nothing to apply (no valid human_verdict rows)")
        return

    now = datetime.datetime.now().isoformat()
    projects_touched: dict[str, str] = {}
    applied = 0
    not_found = []
    # old_batch_id -> list of "project file:line RULE-ID" keys taken from it
    superseded: dict[str, list[str]] = {}

    by_project: dict[str, list] = {}
    for row, verdict, reason in to_apply:
        by_project.setdefault(row["project"], []).append((row, verdict, reason))

    for project, items in by_project.items():
        csv_path = DATA_DIR / project / "adjudication.csv"
        with csv_path.open(newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)

        index = {
            (r["project"], r["codebase_commit"], r["file_path"], r["line"], r["rule_id"]): i
            for i, r in enumerate(rows)
        }

        for row, verdict, reason in items:
            key = (row["project"], row["codebase_commit"], row["file_path"], row["line"], row["rule_id"])
            if key not in index:
                not_found.append(row["sample_id"])
                continue
            i = index[key]
            old_source = rows[i]["source"]
            key_label = f"{row['project']} {row['file_path']}:{row['line']} {row['rule_id']}"
            if old_source and old_source != batch_id:
                superseded.setdefault(old_source, []).append(key_label)
            rows[i]["verdict"] = verdict
            rows[i]["adjudicator"] = "human-gavel"
            rows[i]["reason"] = reason
            rows[i]["source"] = batch_id
            rows[i]["adjudicated_at"] = now
            rows[i]["confidence"] = "high"
            applied += 1
            projects_touched[row["project"]] = row["codebase_commit"]

        with csv_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    for old_batch_id, keys in superseded.items():
        old_manifest_path = BATCHES_DIR / old_batch_id / "manifest.json"
        if not old_manifest_path.exists():
            print(f"warning: {old_batch_id} has no manifest.json, can't decrement "
                  f"row_count for {len(keys)} row(s) taken from it", file=sys.stderr)
            continue
        old_manifest = json.loads(old_manifest_path.read_text())
        if "row_count" in old_manifest:
            old_manifest["row_count"] -= len(keys)
        old_manifest.setdefault("superseded_rows", []).append({
            "by": batch_id,
            "count": len(keys),
            "keys": keys,
            "note": f"verdict corrected by human review (bmdb 1317); see {batch_id}'s manifest",
        })
        old_manifest_path.write_text(json.dumps(old_manifest, indent=2) + "\n")

    if not_found:
        print(f"{len(not_found)} row(s) had no matching key in data/*/adjudication.csv "
              f"(sample stale?): {not_found}", file=sys.stderr)

    batch_dir = BATCHES_DIR / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "batch_id": batch_id,
        "work_item_ref": "benchmarking_db-1317",
        "requested_by": "brandon",
        "adjudicator": "human-gavel",
        "aurora_lint_version": "n/a",
        "aurora_lint_sha": "0" * 40,
        "projects": sorted(projects_touched),
        "codebase_commits": projects_touched,
        "submitted_at": now,
        "row_count": applied,
    }
    (batch_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"applied {applied} row(s) across {len(projects_touched)} project(s)")
    print(f"wrote {batch_dir / 'manifest.json'}")
    print("run scripts/validate.py before committing/pushing a PR branch")


if __name__ == "__main__":
    main()
