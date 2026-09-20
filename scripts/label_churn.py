#!/usr/bin/env python3
"""Label churn between two commits of this repo: what changed in
data/*/adjudication.csv from ref A to ref B, per project, per rule and
overall, so a shift in a published figure can be explained from public data
(benchmarking_db 1372) and a relabel branch can be reviewed against its own
manifest (its churn against main should equal the donor manifests'
`superseded_rows` exactly).

Stdlib only; no database, no network. Rows are read through
`git show <ref>:data/<project>/adjudication.csv`, exactly as score.py's
--labels-ref does, so the answer is a function of two SHAs and nothing else.

Key = (project, codebase_commit, file_path, line, rule_id). Four kinds of
change, each key counted in exactly one:

  added            key in B, not in A
  removed          key in A, not in B
  flipped          key in both, verdict differs (reported by from->to)
  re-keyed         a removed row and an added row with the same
                   (project, codebase_commit, file_path, line) and the same
                   verdict but a different rule_id -- a finding moved between
                   rules (e.g. task 1292's INT32-C -> INT30-C). Paired
                   deterministically and reported apart from added/removed.

A row whose key and verdict are unchanged is not churn, whatever else in it
was edited. Each change is attributed to a batch: an added, flipped or
re-keyed row to the `source` it carries at B; a removed row to the batch
whose manifest at B lists the key under `superseded_rows`, else
"unattributed". Totals (rows and verdicts) are reported at A and at B.

Output is deterministic: keys sorted, no timestamps. `--json` prints the
document; otherwise a human table. A CR byte anywhere in either ref's CSVs
is an error (validate.py's rule) unless --allow-crlf is given -- refs before
d6d1eb8 are CRLF, and the LF normalisation itself is zero churn by this
tool's definition.

Usage:
    python3 scripts/label_churn.py A B [--json] [--allow-crlf] [--keys]
    python3 scripts/label_churn.py 3ab3f41d 1911f5b --allow-crlf --json > churn.json
"""
import argparse
import csv
import io
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERDICTS = ("TP", "FP", "FN", "uncertain")


# ── reading a ref ─────────────────────────────────────────────────────────────

def _git(*args, check=True) -> bytes:
    proc = subprocess.run(["git", "-C", str(REPO_ROOT), *args], capture_output=True)
    if check and proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {proc.stderr.decode().strip()}")
    return proc.stdout


def resolve(ref: str) -> str:
    return _git("rev-parse", "--verify", f"{ref}^{{commit}}").decode().strip()


def projects_at(ref: str) -> list:
    """Projects with a data/<project>/adjudication.csv at `ref`."""
    out = []
    for line in _git("ls-tree", "-r", "--name-only", ref, "data/").decode().splitlines():
        parts = line.split("/")
        if len(parts) == 3 and parts[2] == "adjudication.csv":
            out.append(parts[1])
    return sorted(out)


def rows_at(ref: str, allow_crlf: bool):
    """{key: (verdict, source)} for every row at `ref`, plus CR byte count per project."""
    rows, cr = {}, {}
    for project in projects_at(ref):
        raw = _git("show", f"{ref}:data/{project}/adjudication.csv")
        cr[project] = raw.count(b"\r")
        if cr[project] and not allow_crlf:
            raise SystemExit(f"{ref}:data/{project}/adjudication.csv has {cr[project]} CR byte(s); "
                             "pass --allow-crlf to read a pre-normalisation ref")
        text = raw.decode("utf-8")
        for i, row in enumerate(csv.DictReader(io.StringIO(text, newline="")), start=2):
            key = (row["project"], row["codebase_commit"], row["file_path"], int(row["line"]), row["rule_id"])
            if key in rows:
                raise SystemExit(f"{ref}:data/{project}/adjudication.csv:{i}: duplicate key {key}")
            rows[key] = (row["verdict"], row.get("source", ""))
    return rows, cr


def superseded_index(ref: str) -> dict:
    """{"project file:line rule": batch_id} from every manifest's superseded_rows at `ref`."""
    index = {}
    for line in _git("ls-tree", "-r", "--name-only", ref, "batches/").decode().splitlines():
        if not line.endswith("/manifest.json"):
            continue
        try:
            m = json.loads(_git("show", f"{ref}:{line}").decode("utf-8"))
        except (ValueError, SystemExit):
            continue
        for entry in m.get("superseded_rows", []) or []:
            for key in entry.get("keys", []) or []:
                index.setdefault(key, entry.get("by") or m.get("batch_id") or "unattributed")
    return index


def key_str(key) -> str:
    project, _commit, path, line, rule = key
    return f"{project} {path}:{line} {rule}"


# ── the diff ──────────────────────────────────────────────────────────────────

def churn(a_rows: dict, b_rows: dict, superseded: dict | None = None) -> dict:
    """The four change sets between two {key: (verdict, source)} maps."""
    superseded = superseded or {}
    a_keys, b_keys = set(a_rows), set(b_rows)
    removed = sorted(a_keys - b_keys)
    added = sorted(b_keys - a_keys)

    # re-key: pair a removed row with an added row that differs only in rule_id
    # and keeps the verdict. When several added rows share the site, prefer
    # the one whose batch is the batch that superseded the removed row (the
    # manifests record an in-place re-key that way), then one in the same
    # CERT category (INT32-C -> INT30-C), then the lowest rule_id.
    by_site_added = defaultdict(list)
    for key in added:
        by_site_added[(key[:4], b_rows[key][0])].append(key)
    rekeyed, paired = [], set()
    for key in removed:
        candidates = by_site_added.get((key[:4], a_rows[key][0]))
        if candidates:
            by = superseded.get(key_str(key))
            category = key[4].rstrip("0123456789-C")
            candidates.sort(key=lambda k: (b_rows[k][1] != by, not k[4].startswith(category), k[4]))
            to = candidates.pop(0)
            paired.update((key, to))
            rekeyed.append({"from": key_str(key), "to": key_str(to), "rule_from": key[4], "rule_to": to[4],
                            "verdict": a_rows[key][0], "batch": b_rows[to][1] or "unattributed",
                            "project": key[0]})
    added = [k for k in added if k not in paired]
    removed = [k for k in removed if k not in paired]

    flipped = []
    for key in sorted(a_keys & b_keys):
        va, vb = a_rows[key][0], b_rows[key][0]
        if va != vb:
            flipped.append({"key": key_str(key), "from": va, "to": vb, "project": key[0], "rule": key[4],
                            "batch": b_rows[key][1] or "unattributed"})

    return {
        "added": [{"key": key_str(k), "verdict": b_rows[k][0], "project": k[0], "rule": k[4],
                   "batch": b_rows[k][1] or "unattributed"} for k in added],
        "removed": [{"key": key_str(k), "verdict": a_rows[k][0], "project": k[0], "rule": k[4],
                     "batch": superseded.get(key_str(k), "unattributed")} for k in removed],
        "flipped": flipped,
        "rekeyed": rekeyed,
    }


def _bucket() -> dict:
    return {"added": 0, "removed": 0, "rekeyed": 0, "flipped": 0, "flips": Counter()}


def summarise(change: dict) -> dict:
    """Counts overall, per project, per rule and per batch."""
    overall, per_project, per_rule, per_batch = _bucket(), defaultdict(_bucket), defaultdict(_bucket), defaultdict(_bucket)

    def bump(kind, project, rules, batch, flip=None):
        for b in (overall, per_project[project], per_batch[batch], *(per_rule[r] for r in rules)):
            b[kind] += 1
            if flip:
                b["flips"][flip] += 1

    for e in change["added"]:
        bump("added", e["project"], [e["rule"]], e["batch"])
    for e in change["removed"]:
        bump("removed", e["project"], [e["rule"]], e["batch"])
    for e in change["rekeyed"]:
        bump("rekeyed", e["project"], sorted({e["rule_from"], e["rule_to"]}), e["batch"])
    for e in change["flipped"]:
        bump("flipped", e["project"], [e["rule"]], e["batch"], f"{e['from']}->{e['to']}")

    def freeze(b):
        return {"added": b["added"], "removed": b["removed"], "rekeyed": b["rekeyed"], "flipped": b["flipped"],
                "flips": dict(sorted(b["flips"].items()))}

    return {
        "overall": freeze(overall),
        "per_project": {p: freeze(b) for p, b in sorted(per_project.items())},
        "per_rule": {r: freeze(b) for r, b in sorted(per_rule.items())},
        "per_batch": {r: freeze(b) for r, b in sorted(per_batch.items())},
    }


def totals(rows: dict) -> dict:
    c = Counter(v for v, _ in rows.values())
    per_project = defaultdict(Counter)
    for key, (verdict, _) in rows.items():
        per_project[key[0]][verdict] += 1
    return {
        "rows": len(rows),
        **{v: c.get(v, 0) for v in VERDICTS},
        "per_project": {p: {"rows": sum(cc.values()), **{v: cc.get(v, 0) for v in VERDICTS}}
                        for p, cc in sorted(per_project.items())},
    }


def build(ref_a: str, ref_b: str, allow_crlf: bool, with_keys: bool) -> dict:
    sha_a, sha_b = resolve(ref_a), resolve(ref_b)
    a_rows, cr_a = rows_at(sha_a, allow_crlf)
    b_rows, cr_b = rows_at(sha_b, allow_crlf)
    change = churn(a_rows, b_rows, superseded_index(sha_b))
    doc = {
        "a": {"ref": ref_a, "sha": sha_a, "cr_bytes": cr_a},
        "b": {"ref": ref_b, "sha": sha_b, "cr_bytes": cr_b},
        "totals": {"a": totals(a_rows), "b": totals(b_rows)},
        **summarise(change),
    }
    if with_keys:
        doc["keys"] = change
    return doc


# ── human output ──────────────────────────────────────────────────────────────

def print_human(doc: dict) -> None:
    a, b = doc["a"], doc["b"]
    print(f"label churn  {a['ref']} ({a['sha'][:8]})  ->  {b['ref']} ({b['sha'][:8]})")
    ta, tb = doc["totals"]["a"], doc["totals"]["b"]
    print(f"  rows {ta['rows']} -> {tb['rows']}   " + "   ".join(f"{v} {ta[v]} -> {tb[v]}" for v in VERDICTS))
    o = doc["overall"]
    print(f"  added {o['added']}  removed {o['removed']}  re-keyed {o['rekeyed']}  flipped {o['flipped']}"
          + (("  [" + ", ".join(f"{k} {n}" for k, n in o["flips"].items()) + "]") if o["flips"] else ""))

    def table(title, section):
        if not section:
            return
        print(f"\n  {title:<44} {'added':>6} {'removed':>8} {'rekeyed':>8} {'flipped':>8}  flips")
        for name, bkt in section.items():
            flips = ", ".join(f"{k} {n}" for k, n in bkt["flips"].items())
            print(f"  {name:<44} {bkt['added']:>6} {bkt['removed']:>8} {bkt['rekeyed']:>8} {bkt['flipped']:>8}  {flips}")

    table("per project", doc["per_project"])
    table("per rule", doc["per_rule"])
    table("per batch", doc["per_batch"])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref_a", help="the older commit (SHA, tag or branch)")
    ap.add_argument("ref_b", help="the newer commit")
    ap.add_argument("--json", action="store_true", help="print the JSON document instead of the table")
    ap.add_argument("--keys", action="store_true", help="include every changed key in the JSON (default: counts only)")
    ap.add_argument("--allow-crlf", action="store_true", help="accept CR bytes in a pre-normalisation ref's CSVs")
    args = ap.parse_args(argv)
    doc = build(args.ref_a, args.ref_b, args.allow_crlf, args.keys or not args.json)
    if args.json:
        print(json.dumps(doc, indent=2, sort_keys=True))
    else:
        print_human(doc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
