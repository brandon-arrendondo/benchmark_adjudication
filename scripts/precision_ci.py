#!/usr/bin/env python3
"""Interval estimates for a real-world run's precision, from public inputs.

The intervals aurora-lint's paper reports beside its precision figures
(Wilson, and a percentile bootstrap that resamples whole files or whole
projects) were computed by benchmarking_db's private bench_db/precision_ci.py
against Postgres. This is that module's definition, stdlib only, fed the same
three inputs scripts/score.py takes -- findings, labels at a commit of this
repo, and aurora-lint's scope declaration -- so anyone can recompute them.
Membership comes from score.py itself (its scope, verdict and scored-project
rules), so a point estimate here and score.py's precision cannot disagree.

WHAT IS COMPUTED

  * per project: tp / fp / uncertain, precision, Wilson interval
  * pooled (the headline): precision, Wilson, bootstrap by file and by project
  * macro-average over projects: bootstrap by file and by project
  * rule-stratified: the same run without the top 1 and top 3 rules by
    labeled volume -- precision, Wilson, macro-average, bootstrap by file
  * coverage bounds: precision if every unlabeled in-scope finding were a TP,
    and if every one were an FP
  * per rule: precision with a Wilson interval, every rule, no n floor

WHY RESAMPLE CLUSTERS. Findings are not independent: one defect pattern in
one function yields a run of same-verdict findings in one file. Resampling
findings treats those as independent draws and understates the variance by
roughly the mean cluster size. `file` resamples whole files; `project`
resamples whole projects (12 here), which is the unit for a claim about C
codebases in general, and is wide and lumpy by nature.

THE ORDER OF THE CLUSTERS IS PART OF THE DEFINITION. A bootstrap with a
fixed seed is deterministic only for a fixed order of what it draws from:
the seed picks cluster INDICES, so the same clusters listed in another order
give different replicates. --order names it:

  canonical    CI definition version 2, the definition: clusters are
               resampled in code-point order of their key, (project,
               file_path) or (project,). A property of the data alone, the
               same on every machine.
  en_US.UTF-8  CI definition version 1, kept only to reproduce intervals
               published under it (the v0.5.2 paper's first print): clusters
               in first-seen order after sorting labels by (project,
               rule_id, file_path, line) under glibc's en_US.UTF-8
               collation, which is what the Postgres behind them returned.
               Needs that locale installed, and glibc has changed its
               collation between releases.

The resample count (2,000), seed (20261310), order and definition version
are recorded in every result. Percentages are rounded to one decimal with
round(), as the private module does. At 2,000 resamples an endpoint's last
decimal is at the Monte Carlo noise floor: changing only the order moves
some endpoints by 0.1, so a one-decimal endpoint is not more precise than
that.

Usage:
    python3 scripts/precision_ci.py --scope benchmark_repos.json \\
        --findings-csv tests/golden/run-269/findings.csv.gz \\
        --labels-ref e7d70148 --json
"""
from __future__ import annotations

import argparse
import json
import locale
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score  # noqa: E402

#: benchmarking_db bench_db/precision_ci.CI_DEFINITION_VERSION each --order
#: implements; canonical is the current definition.
CI_DEFINITION_VERSION = {"canonical": 2, "en_US.UTF-8": 1}
DEFAULT_CONFIDENCE = 0.95
DEFAULT_RESAMPLES = 2_000
DEFAULT_SEED = 20261310
ORDERS = ("canonical", "en_US.UTF-8")
DEFAULT_ORDER = "canonical"


# --------------------------------------------------------------------------
# Units
# --------------------------------------------------------------------------

def _order_key(order: str):
    if order == "canonical":
        return lambda lbl: (lbl[3], lbl[1], lbl[2])
    if order == "en_US.UTF-8":
        try:
            locale.setlocale(locale.LC_COLLATE, "en_US.UTF-8")
        except locale.Error as e:
            raise SystemExit(f"--order en_US.UTF-8: locale unavailable ({e})")
        x = locale.strxfrm
        return lambda lbl: (x(lbl[3]), x(lbl[1]), lbl[2])
    raise SystemExit(f"--order must be one of {ORDERS}, got {order!r}")


def labeled_units(findings, labels, scope, commits, order=DEFAULT_ORDER):
    """[(project, file_path, rule_id, verdict)] for every labeled key the run
    emitted, in scored projects, inside scope -- score.score's membership,
    listed in `order` (projects by name, then labels by rule, file, line)."""
    key = _order_key(order)
    units = []
    for project in sorted(findings):
        commit = commits.get(project)
        include, exclude = scope[project]["include"], scope[project]["exclude"]
        present = {k for k in findings[project] if score.in_scope(k[0], include, exclude)}
        at_commit = sorted((lbl for lbl in labels.get(project, [])
                            if commit and lbl[0] == commit), key=key)
        for _, file_path, line, rule_id, verdict in at_commit:
            if (score.in_scope(file_path, include, exclude)
                    and (file_path, line, rule_id) in present):
                units.append((project, file_path, rule_id, verdict))
    return units


def _is_tp(verdict):
    return verdict in score.REAL_BUG_VERDICTS


# --------------------------------------------------------------------------
# Single proportion
# --------------------------------------------------------------------------

_Z = {0.80: 1.2815515655446004, 0.90: 1.6448536269514722,
      0.95: 1.959963984540054, 0.98: 2.3263478740408408,
      0.99: 2.5758293035489004}


def wilson(successes, total, confidence=DEFAULT_CONFIDENCE):
    """Wilson score interval as percentages; None when there is nothing to
    bound. Chosen over the normal approximation because 0/n and n/n occur."""
    if total <= 0:
        return None
    if confidence not in _Z:
        raise SystemExit(f"--confidence must be one of {sorted(_Z)}")
    z = _Z[confidence]
    p = successes / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total))
    return max(0.0, centre - half) * 100, min(1.0, centre + half) * 100


def _fmt_ci(ci):
    if ci is None:
        return {"lo_pct": None, "hi_pct": None}
    return {"lo_pct": round(ci[0], 1), "hi_pct": round(ci[1], 1)}


def _tally(units):
    tp = fp = unc = 0
    for u in units:
        if _is_tp(u[3]):
            tp += 1
        elif u[3] == "FP":
            fp += 1
        else:
            unc += 1
    return tp, fp, unc


def _pct(tp, fp):
    return tp / (tp + fp) * 100 if (tp + fp) else None


def _r1(v):
    return None if v is None else round(v, 1)


def _by(units, idx):
    out = {}
    for u in units:
        out.setdefault(u[idx], []).append(u)
    return out


def macro_average_pct(units):
    """Unweighted mean of per-project precisions; a project with nothing
    scored contributes nothing rather than a 0."""
    vals = [p for p in (_pct(*_tally(us)[:2]) for us in _by(units, 0).values())
            if p is not None]
    return sum(vals) / len(vals) if vals else None


def top_rules_by_volume(units, k):
    counts = {}
    for u in units:
        counts[u[2]] = counts.get(u[2], 0) + 1
    return [r for r, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]]


# --------------------------------------------------------------------------
# Bootstrap
# --------------------------------------------------------------------------

def _cluster_tallies(units, cluster, order=DEFAULT_ORDER):
    """Collapse each cluster to (project, tp, fp) before resampling: precision
    depends on a cluster only through its two counts. Listed in code-point
    order of the cluster key under `canonical` (v2), first-seen order of the
    units under `en_US.UTF-8` (v1)."""
    if cluster == "file":
        key = lambda u: (u[0], u[1])  # noqa: E731
    elif cluster == "project":
        key = lambda u: (u[0],)  # noqa: E731
    else:
        raise ValueError(f"cluster must be file|project, got {cluster!r}")
    acc = {}
    for u in units:
        k = key(u)
        tp, fp = acc.get(k, (0, 0))
        if _is_tp(u[3]):
            tp += 1
        elif u[3] == "FP":
            fp += 1
        acc[k] = (tp, fp)
    items = sorted(acc.items()) if order == "canonical" else acc.items()
    return [(k[0], tp, fp) for k, (tp, fp) in items]


def pooled_from_tallies(tallies):
    tp = sum(t for _, t, _ in tallies)
    fp = sum(f for _, _, f in tallies)
    return _pct(tp, fp)


def macro_from_tallies(tallies):
    per = {}
    for project, t, f in tallies:
        tp, fp = per.get(project, (0, 0))
        per[project] = (tp + t, fp + f)
    vals = [_pct(tp, fp) for tp, fp in per.values() if (tp + fp)]
    return sum(vals) / len(vals) if vals else None


def bootstrap_ci(units, statistic, *, cluster="file", resamples=DEFAULT_RESAMPLES,
                 confidence=DEFAULT_CONFIDENCE, seed=DEFAULT_SEED, order=DEFAULT_ORDER):
    """Percentile bootstrap, resampling whole clusters with replacement."""
    tallies = _cluster_tallies(units, cluster, order)
    n = len(tallies)
    point = statistic(tallies)
    base = {"clusters": n, "cluster_unit": cluster, "resamples": resamples, "seed": seed}
    if n == 0 or point is None:
        return {**base, "point": point, "lo_pct": None, "hi_pct": None,
                "resamples": 0, "degenerate": True}
    pick = random.Random(seed).choices
    population = range(n)
    vals = []
    for _ in range(resamples):
        v = statistic([tallies[i] for i in pick(population, k=n)])
        if v is not None:
            vals.append(v)
    if not vals:
        return {**base, "point": point, "lo_pct": None, "hi_pct": None,
                "degenerate": True}
    vals.sort()
    alpha = (1 - confidence) / 2
    lo = vals[max(0, int(math.floor(alpha * len(vals))) - 1)]
    hi = vals[min(len(vals) - 1, int(math.ceil((1 - alpha) * len(vals))) - 1)]
    return {**base, "point": round(point, 1), "lo_pct": round(lo, 1),
            "hi_pct": round(hi, 1), "effective_replicates": len(vals),
            "degenerate": False}


def coverage_bounds(tp, fp, unlabeled):
    scored = tp + fp
    total = scored + unlabeled
    if total <= 0:
        return {"lower_pct": None, "upper_pct": None, "point_pct": None,
                "unlabeled": unlabeled, "coverage_pct": None}
    return {"point_pct": round(tp / scored * 100, 1) if scored else None,
            "lower_pct": round(tp / total * 100, 1),
            "upper_pct": round((tp + unlabeled) / total * 100, 1),
            "unlabeled": unlabeled,
            "coverage_pct": round(scored / total * 100, 1)}


# --------------------------------------------------------------------------
# The report
# --------------------------------------------------------------------------

def interval_figures(findings, labels, scope, commits, *, order=DEFAULT_ORDER,
                     exclude_top_k=(1, 3), confidence=DEFAULT_CONFIDENCE,
                     resamples=DEFAULT_RESAMPLES, seed=DEFAULT_SEED):
    units = labeled_units(findings, labels, scope, commits, order)
    tp, fp, unc = _tally(units)
    findings_total = score.score(findings, labels, scope, commits)["overall"]["run_findings"]
    ci = dict(resamples=resamples, confidence=confidence, seed=seed, order=order)

    def per_group(idx, with_uncertain):
        out = {}
        for name, us in sorted(_by(units, idx).items()):
            t, f, u = _tally(us)
            row = {"tp": t, "fp": f}
            if with_uncertain:
                row["uncertain"] = u
            row.update(labeled_scored=t + f, precision_pct=_r1(_pct(t, f)))
            w = wilson(t, t + f, confidence)
            if with_uncertain:
                row.update(wilson_lo_pct=_fmt_ci(w)["lo_pct"], wilson_hi_pct=_fmt_ci(w)["hi_pct"])
            else:
                row["wilson"] = _fmt_ci(w)
            out[name] = row
        return out

    report = {
        "basis": score.BASIS,
        "confidence": confidence,
        "ci_definition_version": CI_DEFINITION_VERSION[order],
        "order": order,
        "labeled_scored": tp + fp,
        "labeled_tp": tp,
        "labeled_fp": fp,
        "labeled_uncertain": unc,
        "findings_total": findings_total,
        "headline_pooled": {
            "precision_pct": _r1(_pct(tp, fp)),
            "wilson": _fmt_ci(wilson(tp, tp + fp, confidence)),
            "bootstrap_by_file": bootstrap_ci(units, pooled_from_tallies, cluster="file", **ci),
            "bootstrap_by_project": bootstrap_ci(units, pooled_from_tallies, cluster="project", **ci),
        },
        "macro_average": {
            "precision_pct": _r1(macro_average_pct(units)),
            "bootstrap_by_file": bootstrap_ci(units, macro_from_tallies, cluster="file", **ci),
            "bootstrap_by_project": bootstrap_ci(units, macro_from_tallies, cluster="project", **ci),
        },
        "per_project": per_group(0, True),
        "coverage_bounds": coverage_bounds(tp, fp, max(findings_total - (tp + fp + unc), 0)),
        "rule_stratified": {},
        "per_rule": per_group(2, False),
    }
    for k in exclude_top_k:
        dropped = top_rules_by_volume(units, k)
        kept = [u for u in units if u[2] not in set(dropped)]
        kt, kf, _ = _tally(kept)
        report["rule_stratified"][f"excluding_top_{k}"] = {
            "excluded_rules": dropped,
            "labeled_scored": kt + kf,
            "precision_pct": _r1(_pct(kt, kf)),
            "wilson": _fmt_ci(wilson(kt, kt + kf, confidence)),
            "macro_average_pct": _r1(macro_average_pct(kept)),
            "bootstrap_by_file": bootstrap_ci(kept, pooled_from_tallies, cluster="file", **ci),
        }
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scope", required=True, type=Path,
                    help="aurora-lint data/benchmark_repos.json at the run's commit")
    ap.add_argument("--findings-csv", required=True, type=Path,
                    help="project,file_path,line,rule_id CSV (.gz ok)")
    ap.add_argument("--labels-dir", type=Path)
    ap.add_argument("--labels-ref", help="read data/ from this commit via git show")
    ap.add_argument("--order", choices=ORDERS, default=DEFAULT_ORDER)
    ap.add_argument("--resamples", type=int, default=DEFAULT_RESAMPLES)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--confidence", type=float, default=DEFAULT_CONFIDENCE)
    ap.add_argument("--json", action="store_true", help="emit the JSON document")
    args = ap.parse_args(argv)
    if args.labels_dir and args.labels_ref:
        ap.error("--labels-dir and --labels-ref are exclusive")

    scope = score.load_scope(args.scope)
    findings = score.load_findings_csv(args.findings_csv)
    commits = {p: scope[p]["commit"] for p in findings if p in scope}
    labels, _ = score.load_labels(sorted(findings), args.labels_dir, args.labels_ref)
    doc = interval_figures(findings, labels, scope, commits, order=args.order,
                           confidence=args.confidence, resamples=args.resamples,
                           seed=args.seed)
    if args.json:
        json.dump(doc, sys.stdout, indent=1)
        print()
        return 0
    h = doc["headline_pooled"]
    m = doc["macro_average"]
    print(f"order {doc['order']}, {args.resamples} resamples, seed {args.seed}, "
          f"{doc['confidence']:.0%} intervals")
    print(f"pooled   {h['precision_pct']}%  Wilson {h['wilson']['lo_pct']}-{h['wilson']['hi_pct']}  "
          f"file {h['bootstrap_by_file']['lo_pct']}-{h['bootstrap_by_file']['hi_pct']}  "
          f"project {h['bootstrap_by_project']['lo_pct']}-{h['bootstrap_by_project']['hi_pct']}")
    print(f"macro    {m['precision_pct']}%  "
          f"file {m['bootstrap_by_file']['lo_pct']}-{m['bootstrap_by_file']['hi_pct']}  "
          f"project {m['bootstrap_by_project']['lo_pct']}-{m['bootstrap_by_project']['hi_pct']}")
    for name, r in doc["rule_stratified"].items():
        print(f"{name}  {r['precision_pct']}%  file {r['bootstrap_by_file']['lo_pct']}-"
              f"{r['bootstrap_by_file']['hi_pct']}  (without {', '.join(r['excluded_rules'])})")
    cb = doc["coverage_bounds"]
    print(f"coverage {cb['coverage_pct']}%  bracket {cb['lower_pct']}-{cb['upper_pct']}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
