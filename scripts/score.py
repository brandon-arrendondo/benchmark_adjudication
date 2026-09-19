#!/usr/bin/env python3
"""Score an aurora-lint real-world run against this dataset's labels.

Reproduces the real-world precision / recall / label-coverage figures that
aurora-lint publishes (README "Benchmark Highlights", the paper) from three
public inputs and nothing else -- no database, no credential, no network:

  1. FINDINGS  what one aurora-lint run emitted, per project. Either the
     JSON that `aurora-lint ... --export FILE.json` writes for one codebase
     (a list of {"rule_id", "file", "line", ...}; what
     `python -m bench realworld-run` in aurora-lint invokes per project and
     leaves under its results dir as `sqc-<project>-<version>-<sha>.json`),
     given as --export PROJECT=FILE -- its "file" values are the paths as
     scanned and are normalized here (see `unit` below); or a CSV with
     columns project,file_path,line,rule_id whose file_path is ALREADY
     project-relative, exactly as a label's file_path is written, given as
     --findings-csv FILE. The CSV is the key form itself, used verbatim:
     normalizing it again would strip a path like include/mosquitto/broker.h
     to broker.h (the very collision benchmarking_db task 736 removed).
  2. LABELS    data/<project>/adjudication.csv from this repo -- the working
     tree by default, or any commit with --labels-ref (read through
     `git show`, so the label set a number was scored against is the SHA
     you cite, not whatever is checked out).
  3. SCOPE     aurora-lint's data/benchmark_repos.json, which pins each
     project's codebase commit and declares which files count toward the
     oracle (scope_include / scope_exclude). Pass the copy from the
     aurora-lint commit that produced the run (`git show <sha>:data/
     benchmark_repos.json`); it is read, never copied into this repo.

Together with the aurora-lint commit and the corpus pins, the two SHAs
(aurora-lint, benchmark_adjudication) are the citation: same inputs, same
numbers, byte for byte.

DEFINITIONS (benchmarking_db bench_db/metrics.py, DEFINITION_VERSION 1,
basis "distinct/scored-projects/in_scope"; implemented here identically)

  unit      a finding is one distinct (relpath, line, rule_id) per project.
            For an --export file, relpath strips everything up to and
            including the FIRST "/<project>/" segment of the scanned path,
            so a machine-specific "/home/x/toolchain/curl/lib/doh.c" and a
            label's "lib/doh.c" are the same key; the checkout directory
            must therefore be named after the project, as aurora-lint's
            runner requires. A path with no such segment is taken as
            already project-relative.
  scored    a project is scored iff it has a codebase commit AND at least
            one label AT that commit. Labels at another commit of the same
            project are a different corpus and are ignored.
  scope     the (project, commit)'s declared scope is applied to BOTH sides:
            findings outside it are not counted, and labels outside it leave
            the recall denominator too. Globs are path-aware: `*`, `?` and
            `[...]` stop at `/`, `**` crosses it. A project that declares no
            scope_include is unrestricted; a project ABSENT from the
            declaration is refused (an in-scope figure over it would be
            indistinguishable from a run-wide one).
  verdicts  TP and FN both mark a REAL BUG. A label whose key the run
            emitted is a detection: TP/FN -> true positive, FP -> false
            positive, uncertain -> counted toward coverage only. A real-bug
            label the run did not emit is a miss.
            precision = tp / (tp + fp)          over emitted, labeled keys
            recall    = detected / real-bug labels   (recall against KNOWN
                        true positives -- not against all bugs)
            coverage  = labeled keys / emitted in-scope keys

Percentages are rounded to one decimal with Python's round(), the same call
the private scorer makes, so they compare exactly.

DETERMINISM CAVEATS, stated rather than assumed

  * One aurora-lint binary at one commit produces byte-identical findings
    on the same checkout (aurora-lint fc9164fd onward). The MESSAGE text of
    some rules (MEM31-C's allocator name, aurora_lint task 1209) can differ
    build to build, so comparisons here are on (file, line, rule) keys only
    and messages are ignored entirely.
  * The checkout must be at the pinned commit. The runner records whatever
    SHA it finds; labels are keyed on the pin. A drifted tree scores as a
    quiet drop in coverage, not as an error -- run aurora-lint's
    `python -m bench corpus-check` first.
  * Juliet (the synthetic CWE corpus) is scored by aurora-lint's own
    `python -m bench juliet`; it is not reproduced here.

Usage:
    python3 scripts/score.py --scope path/to/benchmark_repos.json \\
        --export curl=results/sqc-curl-0.4.336-f48effe3.json \\
        --export sqlite=results/sqc-sqlite-0.4.336-f48effe3.json ...
    python3 scripts/score.py --scope ... --findings-csv findings.csv \\
        --labels-ref 3ab3f41d --json > score.json

Exit status is 0 on a scored result, 1 on refused input (a project without
a declared scope, a malformed file).
"""
from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import re
import subprocess
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

#: Bumped when a definition here changes what it counts. Mirrors
#: benchmarking_db bench_db/metrics.py DEFINITION_VERSION -- the two must
#: move together (benchmarking_db's cross-check test asserts equality of
#: output, so a one-sided bump fails there).
DEFINITION_VERSION = 1
BASIS = "distinct/scored-projects/in_scope"
REAL_BUG_VERDICTS = frozenset({"TP", "FN"})
VALID_VERDICTS = frozenset({"TP", "FP", "uncertain", "FN"})

LABEL_COLUMNS = ("project", "codebase_commit", "file_path", "line", "rule_id",
                 "verdict")
FINDINGS_CSV_COLUMNS = ("project", "file_path", "line", "rule_id")


# ── scope predicate (bench_db/corpus.py, verbatim semantics) ─────────────────

def _translate(pat: str) -> re.Pattern:
    """One glob to a full-match regex: `*`/`?`/`[...]` stop at `/`, `**`
    crosses it (`a/**` = beneath a/, `a/**/b` = b at any depth under a/,
    `**/b` = b anywhere)."""
    i, n, out = 0, len(pat), []
    while i < n:
        ch = pat[i]
        i += 1
        if ch == "*":
            if i < n and pat[i] == "*":
                i += 1
                if i < n and pat[i] == "/":
                    i += 1
                    out.append("(?:.*/)?")
                else:
                    out.append(".*")
            else:
                out.append("[^/]*")
        elif ch == "?":
            out.append("[^/]")
        elif ch == "[":
            j = i
            if j < n and pat[j] in "!^":
                j += 1
            if j < n and pat[j] == "]":
                j += 1
            while j < n and pat[j] != "]":
                j += 1
            if j >= n:
                out.append(r"\[")
            else:
                inner = pat[i:j].replace("\\", r"\\")
                i = j + 1
                if inner[:1] in ("!", "^"):
                    inner = "^" + inner[1:]
                out.append("[" + inner + "]")
        else:
            out.append(re.escape(ch))
    return re.compile("(?s:" + "".join(out) + r")\Z")


@lru_cache(maxsize=512)
def _matcher(pat: str) -> re.Pattern:
    return _translate(pat)


def in_scope(relpath: str, include: list[str] | None,
             exclude: list[str] | None) -> bool:
    """No include list means unrestricted; else a path must match one include
    and no exclude."""
    if not include:
        return True
    if not any(_matcher(p).match(relpath) for p in include):
        return False
    if exclude and any(_matcher(p).match(relpath) for p in exclude):
        return False
    return True


def project_relpath(project: str, file_path: str) -> str:
    """Strip through the FIRST '/<project>/' segment (benchmarking_db
    BenchDB.project_relpath). The first, not the last: four corpora contain
    a directory named after the project (include/mosquitto/, include/curl/,
    ext/jni/src/org/sqlite/, libsel4/include/sel4/), and stripping through
    the last would collapse distinct files onto one basename."""
    marker = f"/{project}/"
    idx = file_path.find(marker)
    if idx != -1:
        return file_path[idx + len(marker):]
    return file_path


# ── inputs ───────────────────────────────────────────────────────────────────

def load_scope(path: Path) -> dict[str, dict]:
    """{project: {"commit": sha, "include": [...] | None, "exclude": [...] | None}}
    from an aurora-lint data/benchmark_repos.json."""
    data = json.loads(Path(path).read_text())
    out = {}
    for entry in data.get("repos", []):
        name = entry.get("name")
        if not name:
            continue
        out[name] = {
            "commit": entry.get("version"),
            "include": list(entry["scope_include"]) if entry.get("scope_include") else None,
            "exclude": list(entry["scope_exclude"]) if entry.get("scope_exclude") else None,
        }
    return out


def _open_text(path: Path):
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", newline="", encoding="utf-8")
    return open(path, newline="", encoding="utf-8")


def load_findings_export(project: str, path: Path) -> set[tuple]:
    """Distinct keys from one aurora-lint --export JSON."""
    violations = json.loads(Path(path).read_text())
    if not isinstance(violations, list):
        raise SystemExit(f"{path}: expected a JSON list of violations")
    keys = set()
    for v in violations:
        keys.add((project_relpath(project, v["file"]), int(v["line"]), v["rule_id"]))
    return keys


def load_findings_csv(path: Path) -> dict[str, set[tuple]]:
    """{project: keys} from a project,file_path,line,rule_id CSV (optionally
    gzipped). file_path is project-relative and used verbatim -- it is the
    key, not a scan path (see the module docstring for why it is not passed
    through project_relpath)."""
    per: dict[str, set] = defaultdict(set)
    with _open_text(Path(path)) as f:
        reader = csv.DictReader(f)
        missing = [c for c in FINDINGS_CSV_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"{path}: findings CSV lacks column(s) {missing}")
        for row in reader:
            fp = row["file_path"]
            if fp.startswith("/"):
                raise SystemExit(
                    f"{path}: file_path {fp!r} is absolute; a findings CSV "
                    f"carries project-relative paths. Convert an aurora-lint "
                    f"export with --export PROJECT=FILE instead.")
            per[row["project"]].add((fp, int(row["line"]), row["rule_id"]))
    return dict(per)


def _label_rows(project: str, labels_dir: Path | None, labels_ref: str | None):
    """Rows of data/<project>/adjudication.csv from a directory or a git ref."""
    if labels_ref:
        rel = f"data/{project}/adjudication.csv"
        proc = subprocess.run(["git", "-C", str(REPO_ROOT), "show",
                               f"{labels_ref}:{rel}"],
                              capture_output=True, check=False)
        if proc.returncode != 0:
            return None
        text = proc.stdout.decode("utf-8")
        return list(csv.DictReader(io.StringIO(text, newline="")))
    path = (labels_dir or DATA_DIR) / project / "adjudication.csv"
    if not path.exists():
        return None
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_labels(projects, labels_dir: Path | None, labels_ref: str | None):
    """{project: [(codebase_commit, file_path, line, rule_id, verdict), ...]}
    plus the total row count read, for the basis line."""
    out, total = {}, 0
    for project in projects:
        rows = _label_rows(project, labels_dir, labels_ref)
        if rows is None:
            out[project] = []
            continue
        labels = []
        for i, row in enumerate(rows, start=2):
            missing = [c for c in LABEL_COLUMNS if c not in row]
            if missing:
                raise SystemExit(f"data/{project}/adjudication.csv:{i}: "
                                 f"missing column(s) {missing}")
            if row["verdict"] not in VALID_VERDICTS:
                raise SystemExit(f"data/{project}/adjudication.csv:{i}: "
                                 f"verdict {row['verdict']!r} not in "
                                 f"{sorted(VALID_VERDICTS)}")
            labels.append((row["codebase_commit"], row["file_path"],
                           int(row["line"]), row["rule_id"], row["verdict"]))
        out[project] = labels
        total += len(labels)
    return out, total


# ── scoring ──────────────────────────────────────────────────────────────────

def _pct(num, denom, digits=1):
    return round(num / denom * 100, digits) if denom else None


def _figures(t: dict, n_findings: int) -> dict:
    """The publication figure set, keyed exactly as benchmarking_db's
    release_baseline_numbers.py / metrics.publication_figures name them."""
    labeled = t["tp"] + t["fp"] + t["unc"]
    unlabeled = max(n_findings - labeled, 0)
    return {
        "labeled_tp": t["tp"],
        "labeled_fp": t["fp"],
        "labeled_uncertain": t["unc"],
        "labeled_total": labeled,
        "precision_pct": _pct(t["tp"], t["tp"] + t["fp"]),
        "tp_labels": t["real"],
        "tp_detected": t["det"],
        "recall_pct": _pct(t["det"], t["real"]),
        "run_findings": n_findings,
        "unlabeled_count": unlabeled,
        "unlabeled_fraction": round(unlabeled / n_findings, 3) if n_findings else None,
        "label_coverage_pct": _pct(labeled, n_findings),
        "basis": BASIS,
    }


def score(findings: dict[str, set], labels: dict[str, list], scope: dict[str, dict],
          commits: dict[str, str]) -> dict:
    """findings: {project: {(relpath, line, rule_id)}}; labels as load_labels;
    scope as load_scope; commits: {project: codebase_commit} for the run."""
    per_project = {}
    total = dict(tp=0, fp=0, unc=0, real=0, det=0)
    total_findings = 0
    for project in sorted(findings):
        if project not in scope:
            raise SystemExit(
                f"{project}: not in the scope declaration -- an in-scope "
                f"figure over an undeclared project would be indistinguishable "
                f"from a run-wide one. Pass the benchmark_repos.json that "
                f"names it.")
        commit = commits.get(project)
        include, exclude = scope[project]["include"], scope[project]["exclude"]
        keys = findings[project]
        present = {k for k in keys if in_scope(k[0], include, exclude)}
        at_commit = [lbl for lbl in labels.get(project, [])
                     if commit and lbl[0] == commit]
        if not commit or not at_commit:
            per_project[project] = {"scored": False, "commit": commit,
                                    "in_scope_findings": len(present)}
            continue
        t = dict(tp=0, fp=0, unc=0, real=0, det=0)
        for _, file_path, line, rule_id, verdict in at_commit:
            if not in_scope(file_path, include, exclude):
                continue
            in_run = (file_path, line, rule_id) in present
            real = verdict in REAL_BUG_VERDICTS
            if real:
                t["real"] += 1
                if in_run:
                    t["det"] += 1
            if not in_run:
                continue
            if real:
                t["tp"] += 1
            elif verdict == "FP":
                t["fp"] += 1
            else:
                t["unc"] += 1
        for k in total:
            total[k] += t[k]
        total_findings += len(present)
        f = _figures(t, len(present))
        f.update({"scored": True, "commit": commit})
        per_project[project] = f
    return {
        "definition_version": DEFINITION_VERSION,
        "basis": BASIS,
        "overall": _figures(total, total_findings),
        "per_project": per_project,
    }


# ── presentation ─────────────────────────────────────────────────────────────

def _fmt(v):
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.1f}"
    return str(v)


def print_human(doc: dict) -> None:
    o = doc["overall"]
    print(f"basis: {doc['basis']} (definition_version {doc['definition_version']})")
    for k, v in doc["inputs"].items():
        print(f"  {k}: {v}")
    print()
    hdr = ("project", "commit", "findings", "labeled", "TP", "FP", "unc",
           "prec%", "known TP", "detected", "recall%", "cover%")
    rows = []
    for p, f in sorted(doc["per_project"].items()):
        if not f.get("scored"):
            rows.append((p, (f.get("commit") or "")[:8], f["in_scope_findings"],
                         "-", "-", "-", "-", "-", "-", "-", "-", "unscored"))
            continue
        rows.append((p, f["commit"][:8], f["run_findings"], f["labeled_total"],
                     f["labeled_tp"], f["labeled_fp"], f["labeled_uncertain"],
                     _fmt(f["precision_pct"]), f["tp_labels"], f["tp_detected"],
                     _fmt(f["recall_pct"]), _fmt(f["label_coverage_pct"])))
    rows.append(("OVERALL", "", o["run_findings"], o["labeled_total"],
                 o["labeled_tp"], o["labeled_fp"], o["labeled_uncertain"],
                 _fmt(o["precision_pct"]), o["tp_labels"], o["tp_detected"],
                 _fmt(o["recall_pct"]), _fmt(o["label_coverage_pct"])))
    widths = [max(len(str(r[i])) for r in [hdr, *rows]) for i in range(len(hdr))]
    for r in [hdr, *rows]:
        print("  ".join(str(c).ljust(w) if i == 0 else str(c).rjust(w)
                        for i, (c, w) in enumerate(zip(r, widths))))


def _git_rev(ref: str) -> str | None:
    proc = subprocess.run(["git", "-C", str(REPO_ROOT), "rev-parse", "--verify",
                           f"{ref}^{{commit}}"], capture_output=True, text=True)
    return proc.stdout.strip() if proc.returncode == 0 else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scope", required=True, type=Path,
                    help="aurora-lint data/benchmark_repos.json at the run's "
                         "aurora-lint commit (pins + scope_include/exclude)")
    ap.add_argument("--export", action="append", default=[], metavar="PROJECT=FILE",
                    help="aurora-lint --export JSON for one project (repeatable)")
    ap.add_argument("--findings-csv", type=Path,
                    help="project,file_path,line,rule_id CSV (.gz ok) for any "
                         "number of projects")
    ap.add_argument("--commit", action="append", default=[], metavar="PROJECT=SHA",
                    help="codebase commit the project was scanned at; default: "
                         "the pin in --scope. Must be the full 40-char SHA the "
                         "labels are keyed on.")
    ap.add_argument("--labels-dir", type=Path,
                    help="directory holding <project>/adjudication.csv "
                         "(default: this repo's data/)")
    ap.add_argument("--labels-ref",
                    help="read data/ from this commit of this repo via git show, "
                         "instead of the working tree")
    ap.add_argument("--scope-ref", help="informational: the aurora-lint commit "
                                        "--scope was taken from (recorded in output)")
    ap.add_argument("--json", action="store_true", help="emit the JSON document")
    args = ap.parse_args(argv)

    if args.labels_dir and args.labels_ref:
        ap.error("--labels-dir and --labels-ref are exclusive")
    if not args.export and not args.findings_csv:
        ap.error("give at least one --export PROJECT=FILE or --findings-csv FILE")

    scope = load_scope(args.scope)

    findings: dict[str, set] = {}
    if args.findings_csv:
        findings.update(load_findings_csv(args.findings_csv))
    for spec in args.export:
        if "=" not in spec:
            ap.error(f"--export expects PROJECT=FILE, got {spec!r}")
        project, path = spec.split("=", 1)
        findings.setdefault(project, set()).update(
            load_findings_export(project, Path(path)))

    commits = {p: scope[p]["commit"] for p in findings if p in scope}
    for spec in args.commit:
        if "=" not in spec:
            ap.error(f"--commit expects PROJECT=SHA, got {spec!r}")
        project, sha = spec.split("=", 1)
        commits[project] = sha

    labels, n_labels = load_labels(sorted(findings), args.labels_dir, args.labels_ref)
    doc = score(findings, labels, scope, commits)

    labels_src = (f"{args.labels_ref} ({_git_rev(args.labels_ref) or 'unresolved'})"
                  if args.labels_ref else str(args.labels_dir or DATA_DIR))
    doc["inputs"] = {
        "labels": f"{labels_src}, {n_labels} row(s) across "
                  f"{len(findings)} project(s)",
        "scope": f"{args.scope}" + (f" @ {args.scope_ref}" if args.scope_ref else ""),
        "findings": f"{sum(len(k) for k in findings.values())} distinct "
                    f"(file, line, rule) key(s) across {len(findings)} project(s)",
    }
    if args.json:
        json.dump(doc, sys.stdout, indent=1)
        print()
    else:
        print_human(doc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
