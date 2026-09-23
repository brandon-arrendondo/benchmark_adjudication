#!/usr/bin/env python3
"""The evaluated-scope table: every project's pinned scope, its size, and how
far it is adjudicated for one run -- all from public inputs.

aurora-lint's overview paper states each real-world project's evaluated scope
in one table (Files, SLOC, Findings, Labeled, Coverage, adjudication status).
This script regenerates every column of it:

  Files / SLOC  every *.c / *.h inside the project's declared scope
                (aurora-lint data/benchmark_repos.json scope_include /
                scope_exclude, matched with score.py's in_scope -- the same
                path-aware glob rule the oracle is scored with) in the pinned
                checkout under --bench-root. SLOC is non-blank lines after
                stripping /* */ and // comments; comment markers inside string
                literals are not special-cased, which on these corpora is
                noise, not a figure. Run `python -m bench corpus-check` in
                aurora-lint first: a drifted checkout silently changes these.
  Findings / Labeled / Coverage
                score.py's run_findings / labeled_total / label_coverage_pct
                for the run's findings against the labels at --labels-ref.
                Omit --findings-csv to print the size columns alone.
  Status        exhaustive (>= 90% coverage), partial (>= 50%), in progress,
                or unscored.

Output is the LaTeX rows the paper's table carries, then a totals row;
--json emits the same as a document.

Usage:
    python3 scripts/eval_scope_table.py \\
        --scope <aurora-lint data/benchmark_repos.json at the run's commit> \\
        --bench-root ~/toolchain \\
        --findings-csv tests/golden/run-269/findings.csv.gz --labels-ref e7d70148
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score  # noqa: E402


def sloc(path: Path) -> int:
    try:
        txt = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    txt = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), txt, flags=re.S)
    txt = re.sub(r"//[^\n]*", "", txt)
    return sum(1 for line in txt.splitlines() if line.strip())


def count_project(checkout: Path, include, exclude) -> tuple[int, int]:
    files = [p for p in checkout.rglob("*")
             if p.suffix in (".c", ".h") and ".git" not in p.parts and p.is_file()
             and score.in_scope(p.relative_to(checkout).as_posix(), include, exclude)]
    return len(files), sum(sloc(p) for p in files)


def status(cov) -> str:
    if cov is None:
        return "unscored"
    if cov >= 90:
        return "exhaustive"
    if cov >= 50:
        return "partial"
    return "in progress"


def table(scope: dict, bench_root: Path, scored: dict | None) -> dict:
    rows, missing = [], []
    for name, decl in scope.items():
        checkout = bench_root / name
        if not checkout.is_dir():
            missing.append(name)
            continue
        nf, ns = count_project(checkout, decl["include"], decl["exclude"])
        pp = (scored or {}).get(name, {})
        cov = pp.get("label_coverage_pct")
        rows.append({"project": name, "commit": (decl["commit"] or "")[:8],
                     "files": nf, "sloc": ns,
                     "findings": pp.get("run_findings", pp.get("in_scope_findings")),
                     "labeled": pp.get("labeled_total"),
                     "coverage_pct": cov,
                     "status": status(cov) if scored is not None else None})
    tot_n = sum(r["findings"] or 0 for r in rows)
    tot_l = sum(r["labeled"] or 0 for r in rows)
    total = {"projects": len(rows), "files": sum(r["files"] for r in rows),
             "sloc": sum(r["sloc"] for r in rows)}
    if scored is not None:
        total.update(findings=tot_n, labeled=tot_l,
                     coverage_pct=round(tot_l / tot_n * 100, 1) if tot_n else None)
    return {"rows": rows, "total": total, "missing_checkouts": missing}


def print_latex(doc: dict) -> None:
    fmt = lambda v: f"{v:,}" if isinstance(v, int) else "---"  # noqa: E731
    for r in doc["rows"]:
        cov = r["coverage_pct"] if r["coverage_pct"] is not None else "---"
        print(f"{r['project']:10} & \\texttt{{{r['commit']}}} & {r['files']:>4,} & "
              f"{r['sloc']:>8,} & {fmt(r['findings']):>8} & {fmt(r['labeled']):>8} & "
              f"{cov:>5} & {r['status'] or '---'} \\\\")
    t = doc["total"]
    cells = [f"\\textbf{{{t['files']:,}}}", f"\\textbf{{{t['sloc']:,}}}"]
    if "findings" in t:
        cells += [f"\\textbf{{{t['findings']:,}}}", f"\\textbf{{{t['labeled']:,}}}",
                  f"\\textbf{{{t['coverage_pct']}}}"]
    else:
        cells += ["---"] * 3
    print(f"\\textbf{{Total, all {t['projects']}}} & & " + " & ".join(cells) + " & \\\\")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scope", required=True, type=Path,
                    help="aurora-lint data/benchmark_repos.json at the run's commit")
    ap.add_argument("--bench-root", type=Path,
                    default=Path(os.environ.get("SQC_BENCH_ROOT", "~/toolchain")).expanduser(),
                    help="directory holding one pinned checkout per project, named "
                         "after it (default $SQC_BENCH_ROOT, else ~/toolchain)")
    ap.add_argument("--findings-csv", type=Path,
                    help="the run's project,file_path,line,rule_id CSV (.gz ok); "
                         "omit for the size columns only")
    ap.add_argument("--labels-dir", type=Path)
    ap.add_argument("--labels-ref", help="read data/ from this commit via git show")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.labels_dir and args.labels_ref:
        ap.error("--labels-dir and --labels-ref are exclusive")

    scope = score.load_scope(args.scope)
    scored = None
    if args.findings_csv:
        findings = score.load_findings_csv(args.findings_csv)
        commits = {p: scope[p]["commit"] for p in findings if p in scope}
        labels, _ = score.load_labels(sorted(findings), args.labels_dir, args.labels_ref)
        scored = score.score(findings, labels, scope, commits)["per_project"]
    doc = table(scope, args.bench_root.expanduser(), scored)
    for name in doc["missing_checkouts"]:
        print(f"% {name}: no checkout under {args.bench_root}", file=sys.stderr)
    if args.json:
        json.dump(doc, sys.stdout, indent=1)
        print()
    else:
        print_latex(doc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
