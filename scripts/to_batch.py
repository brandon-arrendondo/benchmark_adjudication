#!/usr/bin/env python3
"""Turn Brandon's filled-in blind-sample verdicts into a benchmark_adjudication
batch: an in-place correction of the matching rows in data/*/adjudication.csv
(same key, new verdict/reason/adjudicator), plus batches/<batch_id>/manifest.json.
Nothing here pushes anything -- this only writes local files for review
before a PR (bmdb 1317, Item 2 step 3(b)).

Usage:
    python3 scripts/to_batch.py <verdict_csv> <batch_id> [--adjudicator TAG]
        [--answer-key PATH]

<verdict_csv> is review/2026-09-21/blind_sample.csv or priority_queue.csv
with human_verdict (TP/FP) and human_reason filled in -- blank
human_verdict rows are skipped, so a partial pass (label some, run
later, label more) works. human_reason must be non-empty (ADR-0007:
label basis only, same as any other row in this repo) or the row is
rejected with a list at the end, matching so nothing partial gets
silently dropped.

Coordinator, 2026-09-21 (worker/adjudication.md's Tuesday redistribution
will carry this forward): the priority queue (bmdb 1341, the biased
tie-break channel) and the blind sample (bmdb 1317/1337, the unbiased
measurement) must keep distinct adjudicator tags, not share
`human-gavel`. Pass `--adjudicator human-gavel` for the priority queue
(the established convention) and `--adjudicator human-blind-sample` for
the blind sample. For the blind sample specifically, pass
`--answer-key <path to the local, never-committed answer_key.csv>`:
rows where the human verdict AGREES with the model's are kappa data, not
label changes, and are skipped rather than written as a "correction" --
only a disagreement is a real ground_truth correction. `--answer-key` is
a no-op (and unnecessary) for the priority queue, which has no paired
model verdict to compare against and is itself the source of human
rulings, agreeing with the model or not.

Reassigning a row's `source` to the new batch orphans it from whatever
batch originally contributed it, so that batch's declared row_count would
otherwise go stale and fail validate.py's cross-check. Follows the
existing correction precedent (see bmdb 1281's `e2d94d6`, "Source
manifests get row_count decrements and superseded_rows records"): each
old batch's manifest.json is decremented by the number of rows it lost
and gets (or extends) a `superseded_rows` entry naming the new batch, the
count, and the keys -- an audit trail, not just a silent number change.
"""
import argparse
import csv
import datetime
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
BATCHES_DIR = REPO_ROOT / "batches"


def load_answer_key(path: Path) -> dict[str, str]:
    """sample_id -> model_verdict, from the local (never-committed) answer key."""
    with path.open(newline="") as f:
        return {row["sample_id"]: row["model_verdict"] for row in csv.DictReader(f)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("verdict_csv", type=Path)
    parser.add_argument("batch_id")
    parser.add_argument(
        "--adjudicator", default="human-gavel",
        help="adjudicator tag to write (default human-gavel; use "
             "human-blind-sample for the blind sample, per the coordinator's "
             "2026-09-21 note -- keep the two exercises' tags distinct)",
    )
    parser.add_argument(
        "--answer-key", type=Path, default=None,
        help="local answer_key.csv (blind sample only): skip rows where the "
             "human verdict agrees with the model's -- those are kappa data, "
             "not corrections",
    )
    args = parser.parse_args()
    verdict_path, batch_id = args.verdict_csv, args.batch_id

    answer_key = load_answer_key(args.answer_key) if args.answer_key else None

    to_apply = []
    rejected = []
    skipped_agreements = 0
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
            if answer_key is not None:
                model_verdict = answer_key.get(row["sample_id"])
                if model_verdict == verdict:
                    skipped_agreements += 1
                    continue
            to_apply.append((row, verdict, reason))

    if rejected:
        print(f"{len(rejected)} row(s) rejected, not applied:", file=sys.stderr)
        for sid, why in rejected:
            print(f"  {sid}: {why}", file=sys.stderr)

    if skipped_agreements:
        print(f"{skipped_agreements} row(s) where the human verdict agreed with "
              f"the model -- kappa data, not written as corrections", file=sys.stderr)

    if not to_apply:
        print("nothing to apply (no valid human_verdict rows needing correction)")
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
            rows[i]["adjudicator"] = args.adjudicator
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
            "note": f"verdict corrected by human review ({args.adjudicator}); see {batch_id}'s manifest",
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
        "adjudicator": args.adjudicator,
        "aurora_lint_version": "n/a",
        "aurora_lint_sha": "0" * 40,
        "projects": sorted(projects_touched),
        "codebase_commits": projects_touched,
        "submitted_at": now,
        "row_count": applied,
    }
    (batch_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"applied {applied} row(s) across {len(projects_touched)} project(s), "
          f"adjudicator={args.adjudicator}")
    print(f"wrote {batch_dir / 'manifest.json'}")
    print("run scripts/validate.py before committing/pushing a PR branch")


if __name__ == "__main__":
    main()
