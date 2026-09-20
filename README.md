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

## Scoring a run

`scripts/score.py` is the reference scorer: the exact definition behind the
real-world precision / recall / label-coverage figures aurora-lint publishes
(README "Benchmark Highlights", the paper), as one stdlib-only Python script
that needs no database, credential or network. It exists so a published
number is reproducible from three public inputs and two SHAs — the
aurora-lint commit that produced the run and the commit of this repo whose
labels scored it — rather than from a private database.

Inputs:

1. **Findings** — what one aurora-lint run emitted. Either the per-codebase
   JSON that `aurora-lint ... --export FILE.json` writes (a list of
   `{"rule_id", "file", "line", ...}`; aurora-lint's `python -m bench
   realworld-run` invokes exactly that per project and leaves the files under
   its results directory as `sqc-<project>-<version>-<sha>.json`), passed as
   `--export PROJECT=FILE`; or a `project,file_path,line,rule_id` CSV of
   project-relative keys, passed as `--findings-csv FILE`. The scan must be of
   the pinned checkout (`python -m bench corpus-check` in aurora-lint says
   whether it still is), with the checkout directory named after the project.
2. **Labels** — `data/<project>/adjudication.csv`, from the working tree or,
   with `--labels-ref SHA`, from any commit of this repo via `git show`. Cite
   that SHA: it names the label set the number was scored against.
3. **Scope** — aurora-lint's `data/benchmark_repos.json`, which pins each
   project's codebase commit and declares which files count toward the oracle
   (`scope_include` / `scope_exclude`). Take it from the aurora-lint commit
   that produced the run (`git show <sha>:data/benchmark_repos.json`); it is
   read where it lives and deliberately not copied into this repo.

```bash
# score a fresh run of every project, labels as checked out here
python3 scripts/score.py --scope ~/aurora-lint/data/benchmark_repos.json \
    --export curl=results/sqc-curl-0.5.0-abc12345.json \
    --export sqlite=results/sqc-sqlite-0.5.0-abc12345.json  # ... one per project

# reproduce a published figure: findings of that run, labels at the cited SHA
python3 scripts/score.py --scope <benchmark_repos.json at the run's aurora-lint commit> \
    --findings-csv tests/golden/run-265/findings.csv.gz \
    --labels-ref 3ab3f41db84355a1c72542104f79e2c9d1fa4a25 --json
```

Output is a per-project table and an overall row (`--json` for the same as a
document), each figure keyed as `benchmarking_db`'s scorer keys it, with a
basis line naming the definition version and every input.

**Definitions** (`DEFINITION_VERSION` 1, basis
`distinct/scored-projects/in_scope`; the script's docstring is the full
statement):

- a *finding* is one distinct `(file, line, rule_id)` per project, the scan
  path normalized by stripping through the first `/<project>/` segment;
- a project is *scored* only if it has a codebase commit and at least one
  label at that commit — labels at another commit are a different corpus;
- the declared *scope* applies to both sides: out-of-scope findings are not
  counted, and out-of-scope labels leave the recall denominator;
- `TP` and `FN` both mark a real bug. Precision = TP / (TP + FP) over the
  run's labeled findings; recall = real-bug labels the run emitted / all
  real-bug labels (recall against *known* true positives, not all bugs);
  coverage = labeled findings / in-scope findings; `uncertain` counts toward
  coverage only.

**Correctness gate.** `tests/test_score_golden.py` (run in CI, and by
`python3 -m unittest discover -s tests`) feeds the scorer the findings of
aurora-lint real-world run #265 — the v0.5.0 paper baseline, pinned at
`tests/golden/run-265/` — the labels at `3ab3f41d` and the scope at
aurora-lint `f48effe3`, and asserts every per-project and overall figure is
identical to what `benchmarking_db`'s Postgres-backed scorer published
(52.5% precision, 96.9% recall against known TPs, 76.1% coverage over 12
projects). `benchmarking_db` runs the reverse check against its own scorer,
so the two definitions cannot drift apart unnoticed. Postgres via
`benchmarking_db` remains the source of published numbers; this script is
how anyone else checks them.

**Determinism, stated plainly.** One aurora-lint binary at one commit gives
byte-identical findings on the same checkout, but the message text of some
rules can differ between builds (MEM31-C's allocator name), so everything
here compares `(file, line, rule)` keys and ignores messages. A checkout that
drifted from its pin scores as a quiet drop in coverage, not an error. Juliet
(the synthetic CWE corpus) is scored by aurora-lint's own `python -m bench
juliet` and is not reproduced here.


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

## Labeling standards

These are the rules a verdict is judged against, so a label means the same
thing in every project. They are decisions of the project owner, recorded
here so a reviewer can check a batch against them.

**Labels are data, including true positives.** Every TP, FP and FN row belongs
in this repo whatever the defect, because it is the output of a public tool on
public code. A row's `reason` and `provenance` state the *basis of the verdict*
(what the flagged construct is, why it is TP or FP at that line). They do not
carry reproduction steps, sanitizer output, a proposed patch, an impact
narrative or report text; write-ups of a defect stay out of public repos until
the fix has landed upstream (aurora-lint ADR-0007).

**ERR33-C follows the strict reading (aurora-lint ADR-0001), in every project.**
A call whose result ERR33-C covers is a violation as written when the result
is bare-ignored, or assigned to a variable that is never tested in the
enclosing function; `ERR33-C-EX1` does not exempt it. A finding is FP only
where the error indicator *is* tested. Whether a project would want to act on
it is a suppression question, not a labeling one. Two consequences:

- A result **returned to the caller** for it to check is *propagated*, not
  ignored, and is labeled FP.
- A partial or indirect check (a value derived from the result, or a test on
  only some paths) keeps the verdict it already had until a batch decides it
  explicitly.

(benchmarking_db 1352 applied this reading across the older projects: 185 rows
were corrected FP to TP in one reviewed commit, each listed under
`superseded_rows` in the manifest of the batch that first labeled it. Task 1281
had already parked the "returned to the caller" shape on the same ground.)

## Layout

```
data/<project>/adjudication.csv   -- cumulative labels for one project
batches/<batch_id>/manifest.json  -- one immutable record per submission batch
scripts/validate.py               -- schema/consistency checks, run in CI
scripts/score.py                  -- reference scorer: precision/recall/coverage
                                     of an aurora-lint run against these labels
tests/                            -- golden test pinning score.py to a published run
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
manifest's declared `row_count` not matching reality, a backslash-escaped
quote in a free-text field, a CR byte in a CSV) so review time goes to the judgment call: does
this batch's content actually match what was asked for. Nothing about this
process affects how the merged data reads or is used.

**Whatever generates a batch's CSV must serialize it through a real CSV
writer** (Python's `csv` module or equivalent) — never by concatenating
strings by hand. CSV has exactly one way to put a literal quote inside a
quoted field (double it, `""`); a backslash-escaped quote (`\"`, the
JSON/Python string-literal convention) is not valid CSV escaping and will
eventually corrupt that row's field boundaries the moment a real quote
shows up in a `reason` (a 181-row cleanup across 8 projects was needed for
exactly this, 2026-09-16 — see that commit's message for the recovery
mechanism and its limits, in particular why some rows' `provenance`/
`confidence` were left blank rather than guessed). `scripts/validate.py`
catches the raw pattern in CI, but the fix is upstream: generate valid CSV
in the first place.

**Every CSV is LF-terminated, and a batch appends rather than rewriting the
file.** `.gitattributes` pins `*.csv text eol=lf`, and `scripts/validate.py`
fails on any CR byte in a `data/*/adjudication.csv` (a record terminator or a
CRLF inside a quoted multi-line field alike — git's `text` conversion would
normalize either at the next commit, so the committed bytes must already be
clean). Python's `csv` module defaults to `lineterminator='\r\n'`, so using a
real CSV writer as above without that argument — and then rewriting the file
with it — converts every existing line to CRLF. Before this rule, when
`data/` was mixed by project, a 150-row addition landed that way twice as a
whole-file diff of tens of thousands of lines, which buried the rows a
reviewer was supposed to be checking and manufactured conflicts against any
other batch in flight (the task-1292 merge commit's "CRLF-normalization false
conflict with 1291", and again on task-1303). `data/` was normalized to LF in
one pass afterwards (benchmarking_db task 1338) so that "match what the file
already has" could become the one rule it is now:

```python
with open(path, "a", newline="", encoding="utf-8") as fh:
    csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n").writerows(new_rows)
```

Appending (`"a"`) rather than rewriting is what keeps the diff to the added
rows. A reviewer who sees a whole-file diff anyway can confirm nothing but
terminators moved with `git diff --ignore-cr-at-eol`; a batch that fails
`validate.py` on a CR was written by something that needs the
`lineterminator` fix, not a file-side workaround.

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
