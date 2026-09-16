# benchmark_adjudication

A dataset: TP/FP/uncertain adjudication labels for static-analysis findings
across several open-source C codebases, adjudicated for aurora-lint but not
specific to it — a label says "line N of file F in commit C of project P is a
real bug" (or isn't), independent of which tool flagged it or who runs it.

## Using this dataset

No account, credential, database, or tooling of any kind is required — this
is plain CSV under `data/<project>/adjudication.csv`, one row per labeled
finding, columns documented below. Clone or download the repo and read the
files directly with anything that reads CSV.

- The join key is `(project, codebase_commit, file_path, line, rule_id)`.
  `codebase_commit` is a full git SHA of the exact commit the label applies
  to — check out that commit of the project to get matching file contents
  and line numbers before comparing your own tool's findings against these
  labels.
- `verdict` is the label: `TP` (real defect), `FP` (not a real defect),
  `uncertain`, or `FN` (a real bug found by reading the file that aurora-lint
  did NOT flag at that line/rule — has no matching finding, so it never
  affects precision, but counts as a known real bug for recall once some
  future aurora-lint version actually catches it).
- `rule_id` names the kind of defect (e.g. a CERT-C rule like `MEM31-C`), not
  a tool-specific code — these labels are usable by any static analyzer that
  reasons about the same defect classes, not only aurora-lint.
- `batches/*/manifest.json` is provenance metadata (who submitted a batch of
  labels, under what request, with which tool version) for auditing how the
  dataset grew over time. **You can ignore it entirely** if you just want the
  labels — nothing in `data/*.csv` requires resolving a manifest to be
  usable.

Everything past this point describes how *this maintainer* curates and adds
to the dataset. None of it is a prerequisite for using it.

## Why the review process exists

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
  "requested_by": "maintainer",
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

## How labels get added (maintainer process)

Every change to `main` goes through a PR (branch protection enforces this —
no direct pushes, no force-push). The PR template asks for the work item
reference, scope, and row count up front so a reviewer can check the PR's
actual diff against what was actually requested, before approving — that
check is the point, not a formality. `scripts/validate.py` runs in CI on
every PR and catches the mechanical class of problem (schema violations,
duplicate keys, a row whose `source` doesn't match any manifest, a
manifest's declared `row_count` not matching reality) so review time goes to
the judgment call: does this batch's content actually match what was asked
for. Nothing about this process affects how the merged data reads or is
used.

Whether a free-text field discloses a secret or an internal address is
**not** something CI checks — an earlier regex-based scanner flagged 311
rows in this repo's very first PR that turned out to be ordinary C variable
names (`nToken`, `pToken`) in adjudication reasoning, not credentials. That's
a reviewer judgment call instead: the PR template's checklist asks the
reviewer (human or AI) to actually read free-text fields in the diff for
anything that shouldn't be public, rather than leaning on a scanner that
either misses a disclosure worded unexpectedly or trains reviewers to click
past its noise.

Brandon Arrendondo is the accountable owner of aurora-lint and all its
benchmark data, including what gets merged here — per BISSELL's AI
Acceptable Use Policy, that accountability sits with a named human, not
with any agent that performs a review on his behalf.

## Relationship to Postgres (maintainer-internal, optional context)

For this maintainer's own pipeline, `ground_truth` also lives in Postgres
(`sqc_bench`, in the separate `benchmarking_db` repo), and a merged commit
here can be loaded there for use by that pipeline's own tooling — see
`benchmarking_db/docs/design/adjudication-ingest-from-benchmark_adjudication.md`.
That relationship is why labels are organized into reviewed batches with
full SHA provenance in the first place (reproducibility of a past published
number), but it is specific to this maintainer's infrastructure. **This
dataset does not depend on Postgres, a coordinator, or any other tooling to
be useful** — the CSV files are the dataset, this repo is deliberately
Postgres-blind (no DSN, no connection code, ever), and anyone else can
consume `data/*/adjudication.csv` on its own with no other system involved.
