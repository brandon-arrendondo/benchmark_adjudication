# benchmark_adjudication

Git-versioned, PR-reviewed record of the TP/FP/uncertain adjudication
(`ground_truth`) labels used to produce aurora-lint's citable precision/recall
numbers, plus the exact aurora-lint and codebase SHAs each batch of labels
was adjudicated against.

## Why this exists

`ground_truth` lives in Postgres (`sqc_bench`, owned by `benchmarking_db`) and
that does not change — this repo is not a second copy of the live oracle and
must never be treated as one. What Postgres alone cannot give you is an
answer to "which exact label set produced the number we published for commit
X" once the oracle has since been corrected, relabeled, or extended: rows get
fixed in place (`bin/gavel_review.py`, `relabel_ground_truth_rule.py`, etc. in
`benchmarking_db`), which is correct behavior for the live oracle but means a
later query is *no longer* the label set a past number was scored against.
`oracle_versions`/`freeze_oracle_version` in `benchmarking_db` anticipated
this need but only ever snapshotted a derived score, not the underlying rows
— so today there is no way to reproduce which labels backed a past number.

This repo closes that gap. Every batch of adjudication work lands here as a
reviewed PR before it reaches Postgres at all, and the merge commit SHA that
results is the citable answer to "which labels."

**This repo is not the write path of convenience for the oracle.** It is a
staging and audit layer in front of it. See `benchmarking_db/docs/design/`
for how a merged commit here gets loaded into Postgres.

## Layout

```
data/<project>/adjudication.csv   -- cumulative labels for one project
batches/<batch_id>/manifest.json  -- one immutable record per submission batch
scripts/validate.py               -- schema/consistency checks, run in CI
```

### `data/<project>/adjudication.csv`

One row per adjudicated finding, columns matching `benchmarking_db`'s
`ground_truth` table exactly so a merge round-trips with no translation:

| column | meaning |
|---|---|
| `project` | matches the `<project>` directory name |
| `codebase_commit` | full 40-char SHA of the codebase that was scanned — never abbreviated (see `benchmarking_db/schema/18_codebase_commit_full_sha.sql` for why: two spellings of one commit silently split a project's labels into two disagreeing sets before this was enforced) |
| `file_path` | project-relative path |
| `line` | 1-indexed line number |
| `rule_id` | e.g. `MEM31-C` |
| `verdict` | `TP`, `FP`, or `uncertain` |
| `adjudicator` | e.g. `manual`, `claude-opus-4.8` |
| `reason` | free text |
| `source` | the `batch_id` of the `batches/<batch_id>/manifest.json` this row came from — every row must trace to a manifest |
| `adjudicated_at` | ISO 8601 timestamp |
| `provenance` | free text |
| `confidence` | free text |

`(project, codebase_commit, file_path, line, rule_id)` must be unique within
a project's CSV, matching `ground_truth`'s own `UNIQUE` constraint — a
collision here is a defect to fix before merge, not something Postgres
should discover first.

### `batches/<batch_id>/manifest.json`

One immutable file per submission, written once and never edited after
merge (a correction is a new batch, not an edit to an old one):

```json
{
  "batch_id": "TASK-1245",
  "work_item_ref": "TASK-1245",
  "requested_by": "coordinator",
  "adjudicator": "claude-opus-4.8",
  "aurora_lint_version": "0.4.336",
  "aurora_lint_sha": "27785c4a1234567890abcdef1234567890abcdef",
  "projects": ["mosquitto"],
  "codebase_commits": {"mosquitto": "a1b2c3...40 hex chars"},
  "submitted_at": "2026-09-16T12:00:00Z",
  "row_count": 137,
  "rules": ["MEM31-C"],
  "notes": "delta-adjudication for MEM31-C structural fix"
}
```

`aurora_lint_sha` and every value in `codebase_commits` must be a full
40-char SHA for the same reason `codebase_commit` is: an abbreviation is a
display concern, not a join/citation key.

## Review protocol

Every change to `main` goes through a PR (branch protection enforces this —
no direct pushes, no force-push). The PR template asks for the work item
reference, scope, and row count up front so the coordinator (or whoever is
reviewing) can check the PR's actual diff against what was actually
dispatched, before approving — that check is the point, not a formality.
`scripts/validate.py` runs in CI on every PR and catches the mechanical
class of problem (schema violations, duplicate keys, a row whose `source`
doesn't match any manifest, a manifest's declared `row_count` not matching
reality) so review time goes to the judgment call: does this batch's content
actually match what was asked for.

## Accountability

Per BISSELL's AI Acceptable Use Policy, a human Associate is the accountable
owner of what gets merged here, even when a coordinator agent performs the
review — the agent's approval is not itself the accountable decision.
Brandon Arrendondo is that Associate for this repo.

## Populating from Postgres

The initial dump of existing `ground_truth` rows into this format, and the
tool that loads a merged batch from here back into Postgres, live in
`benchmarking_db` (it owns the DSN) — see
`benchmarking_db/docs/design/adjudication-ingest-from-benchmark_adjudication.md`.
This repo is deliberately Postgres-blind: no DSN, no connection code, ever.
