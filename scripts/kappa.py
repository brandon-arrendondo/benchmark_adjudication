#!/usr/bin/env python3
"""Cohen's kappa + per-rule error rate + a label-noise interval for pooled
precision, from Brandon's blind-sample verdicts against the local answer
key (bmdb 1317, Item 2).

Usage:
    python3 scripts/kappa.py <verdict_csv> <answer_key_csv>

<verdict_csv> is review/2026-09-21/blind_sample.csv after human_verdict
(TP/FP) has been filled in for some or all rows -- blank human_verdict
rows are skipped. <answer_key_csv> is the local-only file this repo never
commits (~/security-disclosures/adjudication-review-2026-09-21/
answer_key.csv on r720 today).

The label-noise interval uses the Rogan-Gladen misclassification
correction: sensitivity Se = P(human=TP | model=TP) and specificity
Sp = P(human=FP | model=FP), estimated from the sample, correct the
corpus's observed TP rate p_obs via
    p_true = (p_obs - (1 - Sp)) / (Se - (1 - Sp))
and a percentile bootstrap (resampling the *sample*, not the corpus)
gives the interval. This assumes the sample's Se/Sp generalize to the
full labeled corpus -- true insofar as the sample is the stratified
random draw scripts/build in build_blind_sample.py actually produced;
if judgment work post-processed the sample (e.g. dropped rows), that
assumption should be re-checked before trusting the interval.
"""
import csv
import random
import sys
from pathlib import Path


def load_verdicts(path: Path) -> dict[str, tuple[str, str]]:
    out = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            v = (row.get("human_verdict") or "").strip().upper()
            if v not in ("TP", "FP"):
                continue
            out[row["sample_id"]] = (v, row.get("rule_id", ""))
    return out


def load_answers(path: Path) -> dict[str, tuple[str, str]]:
    out = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            out[row["sample_id"]] = (row["model_verdict"], row["rule_id"])
    return out


def cohens_kappa(pairs: list[tuple[str, str]]) -> float:
    n = len(pairs)
    if n == 0:
        return float("nan")
    po = sum(1 for h, m in pairs if h == m) / n
    cats = ("TP", "FP")
    pe = 0.0
    for c in cats:
        p_h = sum(1 for h, _ in pairs if h == c) / n
        p_m = sum(1 for _, m in pairs if m == c) / n
        pe += p_h * p_m
    if pe == 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1 - pe)


def rogan_gladen(pairs: list[tuple[str, str]], p_obs: float) -> float | None:
    model_tp = [h for h, m in pairs if m == "TP"]
    model_fp = [h for h, m in pairs if m == "FP"]
    if not model_tp or not model_fp:
        return None
    se = sum(1 for h in model_tp if h == "TP") / len(model_tp)
    sp = sum(1 for h in model_fp if h == "FP") / len(model_fp)
    denom = se - (1 - sp)
    if abs(denom) < 1e-9:
        return None
    return (p_obs - (1 - sp)) / denom


def bootstrap_ci(pairs: list[tuple[str, str]], p_obs: float, n_boot: int = 2000, seed: int = 20260921):
    rng = random.Random(seed)
    n = len(pairs)
    estimates = []
    for _ in range(n_boot):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        est = rogan_gladen(sample, p_obs)
        if est is not None:
            estimates.append(max(0.0, min(1.0, est)))
    if not estimates:
        return None
    estimates.sort()
    lo = estimates[int(0.025 * len(estimates))]
    hi = estimates[min(len(estimates) - 1, int(0.975 * len(estimates)))]
    return lo, hi


def main() -> None:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <verdict_csv> <answer_key_csv>", file=sys.stderr)
        sys.exit(2)
    verdict_path, answer_path = Path(sys.argv[1]), Path(sys.argv[2])

    verdicts = load_verdicts(verdict_path)
    answers = load_answers(answer_path)

    pairs = []
    per_rule_pairs: dict[str, list[tuple[str, str]]] = {}
    for sample_id, (human, rule) in verdicts.items():
        if sample_id not in answers:
            print(f"warning: {sample_id} not in answer key, skipped", file=sys.stderr)
            continue
        model_verdict, _ = answers[sample_id]
        pairs.append((human, model_verdict))
        per_rule_pairs.setdefault(rule, []).append((human, model_verdict))

    n = len(pairs)
    if n == 0:
        print("no human_verdict rows found -- nothing to compute yet")
        return

    agree = sum(1 for h, m in pairs if h == m)
    kappa = cohens_kappa(pairs)
    print(f"{n} labeled row(s) (of {len(answers)} in the sample)")
    print(f"raw agreement: {agree}/{n} ({100*agree/n:.1f}%)")
    print(f"Cohen's kappa: {kappa:.4f}")
    print()

    print("per-rule error rate (human != model):")
    for rule, rp in sorted(per_rule_pairs.items(), key=lambda kv: -len(kv[1])):
        errs = sum(1 for h, m in rp if h != m)
        print(f"  {rule:12s} n={len(rp):3d}  errors={errs:3d}  ({100*errs/len(rp):.1f}%)")
    print()

    # corpus-wide observed TP rate among model TP/FP verdicts (excluding
    # human-gavel and uncertain, matching the sample's own eligible pool)
    data_dir = Path(__file__).resolve().parent.parent / "data"
    n_tp = n_fp = 0
    for csv_path in sorted(data_dir.glob("*/adjudication.csv")):
        with csv_path.open(newline="") as f:
            for row in csv.DictReader(f):
                if row["adjudicator"] == "human-gavel":
                    continue
                if row["verdict"] == "TP":
                    n_tp += 1
                elif row["verdict"] == "FP":
                    n_fp += 1
    p_obs = n_tp / (n_tp + n_fp)
    print(f"corpus observed TP rate (model-labeled pool): {p_obs:.4f} ({n_tp} TP / {n_fp} FP)")

    p_true = rogan_gladen(pairs, p_obs)
    if p_true is None:
        print("label-noise correction: not computable (need both model-TP and model-FP rows labeled)")
    else:
        ci = bootstrap_ci(pairs, p_obs)
        print(f"Rogan-Gladen corrected TP rate: {p_true:.4f}", end="")
        if ci:
            print(f"  (95% bootstrap CI: [{ci[0]:.4f}, {ci[1]:.4f}], n_boot=2000, seed=20260921)")
        else:
            print()


if __name__ == "__main__":
    main()
