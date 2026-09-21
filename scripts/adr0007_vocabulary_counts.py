#!/usr/bin/env python3
"""Per-(project, rule) breakdown of ADR-0007-restricted vocabulary hits.

validate.py enforces the check (fail on new rows, warn-only on legacy ones)
but deliberately prints only a total count, not a per-row dump -- see its
ADR-0007 docstring note. This script is the counts-only report for bmdb 1414
step 2: no site detail (no file/line), just how much exists per project and
rule, to size the sweep.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import DATA_DIR, adr0007_hit_categories  # noqa: E402


def main() -> None:
    counts: dict[tuple[str, str], int] = {}
    category_totals: dict[str, int] = {}
    total_rows = 0
    hit_rows = 0

    for csv_path in sorted(DATA_DIR.glob("*/adjudication.csv")):
        with csv_path.open(newline="") as f:
            for row in csv.DictReader(f):
                total_rows += 1
                hits = adr0007_hit_categories(f"{row['reason']} {row['provenance']}")
                if not hits:
                    continue
                hit_rows += 1
                key = (row["project"], row["rule_id"])
                counts[key] = counts.get(key, 0) + 1
                for name in hits:
                    category_totals[name] = category_totals.get(name, 0) + 1

    print(f"{hit_rows} / {total_rows} row(s) flagged\n")
    print(f"{'project':12s} {'rule':10s} count")
    for (project, rule), n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{project:12s} {rule:10s} {n}")
    print()
    print("by category (a row may hit more than one):")
    for name, n in sorted(category_totals.items(), key=lambda kv: -kv[1]):
        print(f"  {name:20s} {n}")


if __name__ == "__main__":
    main()
