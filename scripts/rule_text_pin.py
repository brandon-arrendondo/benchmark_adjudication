#!/usr/bin/env python3
"""The rule-text pin of aurora-lint ADR-0018: the map, its digest, and the
pin fields every label carries.

Pure stdlib, like validate.py, which imports this module.

The map is rulings/rule-text-map.json. Each guideline maps to a merged commit
of cmu-sei/secure-coding-standards, the path of its page source in that commit
and the SHA-256 of that file (the guideline's rule_text_version). An entry may
also list the pins it replaced under "history", newest last, each with the
same commit/path/sha256/carried_forward fields, so a label judged against an
earlier text still names a version the map knows.

Every label carries five fields (PIN_COLUMNS):

  rule_text_commit   the CERT commit its text was pinned at; empty when unpinned
  rule_text_version  the SHA-256 of the rule's page at that commit, or
                     "unpinned"
  rule_text_basis    how the label relates to that text:
                       judged           judged against it
                       carried-forward  judged against an earlier text and
                                        carried forward to this one by the
                                        recorded review in the map entry
                       unpinned         no text this label can be tied to:
                                        the rule has no map entry, or its entry
                                        says the labels must be re-judged
  rulings_commit     the commit of this repository whose rulings/ the label
                     was judged under; empty for a label that predates the
                     rulings record
  rulings_ids        the ruling ids it applied, space-separated
                     (`<RULE>/<YYYY-MM-DD>/<item>` or `P/<name>`); empty as
                     for rulings_commit

The key of a label is (project, codebase_commit, file_path, line, rule_id,
rule_text_version).

Usage:
  python3 scripts/rule_text_pin.py digest      # the map's SHA-256 (the sixth pin)
  python3 scripts/rule_text_pin.py backfill    # add the pin columns to every CSV
"""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
MAP_PATH = REPO_ROOT / "rulings" / "rule-text-map.json"

PIN_COLUMNS = [
    "rule_text_commit", "rule_text_version", "rule_text_basis",
    "rulings_commit", "rulings_ids",
]
UNPINNED = "unpinned"
BASES = {"judged", "carried-forward", UNPINNED}


def load_map(path: Path | None = None) -> dict:
    return json.loads((path or MAP_PATH).read_text(encoding="utf-8"))


def map_digest(rule_map: dict) -> str:
    """SHA-256 of the map's canonical serialisation: sorted keys, no
    whitespace, UTF-8. This is the pin a run records (ADR-0018 Decision 1)."""
    canonical = json.dumps(rule_map, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def known_pins(entry: dict) -> list[dict]:
    """Every pin a map entry knows: its history, oldest first, then itself."""
    return [*entry.get("history", []), entry]


def backfill_fields(rule_id: str, rules: dict) -> dict:
    """The pin fields of a label that predates the pin (ADR-0018 ruling c).

    It takes its rule's first-map version as carried forward only where the
    map says the rule's reading carried forward to that text. Otherwise it is
    unpinned: never a guessed version.
    """
    entry = rules.get(rule_id)
    if entry is None or not entry.get("carried_forward"):
        return {"rule_text_commit": "", "rule_text_version": UNPINNED,
                "rule_text_basis": UNPINNED, "rulings_commit": "",
                "rulings_ids": ""}
    return {"rule_text_commit": entry["commit"],
            "rule_text_version": entry["sha256"],
            "rule_text_basis": "carried-forward", "rulings_commit": "",
            "rulings_ids": ""}


def backfill(data_dir: Path = DATA_DIR, map_path: Path = MAP_PATH) -> dict:
    """Add PIN_COLUMNS to every data/*/adjudication.csv that lacks them.

    A file that already has them is left byte-for-byte alone. Returns
    {basis: rows} over the files it rewrote.
    """
    rules = load_map(map_path)["rules"]
    counts: dict[str, int] = {}
    for csv_path in sorted(data_dir.glob("*/adjudication.csv")):
        text = csv_path.read_text(encoding="utf-8")
        reader = csv.DictReader(io.StringIO(text, newline=""))
        fields = list(reader.fieldnames or [])
        if set(PIN_COLUMNS) <= set(fields):
            continue
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=fields + PIN_COLUMNS,
                                lineterminator="\n")
        writer.writeheader()
        for row in reader:
            row.update(backfill_fields(row["rule_id"], rules))
            counts[row["rule_text_basis"]] = counts.get(row["rule_text_basis"], 0) + 1
            writer.writerow(row)
        csv_path.write_text(out.getvalue(), encoding="utf-8", newline="")
    return counts


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "digest":
        print(map_digest(load_map()))
    elif command == "backfill":
        counts = backfill()
        print(" ".join(f"{basis}={n}" for basis, n in sorted(counts.items()))
              or "nothing to backfill")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
