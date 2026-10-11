"""Write or check the frozen list of grandfathered manifest directory names.

The batch directory names that existed when new names started being checked
(validate.py, reason_references.manifest_name_categories) stay valid dataset
identifiers whatever their shape. They are listed, one per line and sorted, in
batch_name_allowlist.txt beside this script. The list is written once; a new
batch takes a neutral name instead of an entry here.

    python3 scripts/batch_name_allowlist.py --check   # default
    python3 scripts/batch_name_allowlist.py --write   # only to create the file

--check exits 1 when the file is missing, unsorted or duplicated, or names a
directory that has no manifest.
"""
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BATCHES_DIR = REPO_ROOT / "batches"
ALLOWLIST_PATH = Path(__file__).resolve().parent / "batch_name_allowlist.txt"
HEADER = (
    "# Manifest directory names grandfathered as dataset identifiers.\n"
    "# Written once by scripts/batch_name_allowlist.py; do not add entries.\n"
    "# A new batch takes a neutral name (README, \"Naming a batch\").\n"
)


def tree_names(batches_dir: Path = BATCHES_DIR) -> list[str]:
    """Every directory under batches/ that holds a manifest, sorted."""
    return sorted(p.parent.name for p in batches_dir.glob("*/manifest.json"))


def parse(text: str) -> list[str]:
    """The entries of an allowlist file, in file order, comments dropped."""
    return [line.strip() for line in text.splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def read_allowlist(path: Path = ALLOWLIST_PATH) -> frozenset[str]:
    """The grandfathered names; empty when the file does not exist."""
    if not path.exists():
        return frozenset()
    return frozenset(parse(path.read_text()))


def check(path: Path = ALLOWLIST_PATH, batches_dir: Path = BATCHES_DIR) -> list[str]:
    """Problems with the allowlist file against the batches tree."""
    if not path.exists():
        return [f"{path}: missing; create it once with --write"]
    entries = parse(path.read_text())
    errors = []
    if entries != sorted(set(entries)):
        errors.append(f"{path}: entries must be sorted and unique")
    present = set(tree_names(batches_dir))
    for name in sorted(set(entries) - present):
        errors.append(f"{path}: '{name}' has no batches/{name}/manifest.json")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="check the file (default)")
    mode.add_argument("--write", action="store_true", help="write the file from the tree")
    args = parser.parse_args()
    if args.write:
        if ALLOWLIST_PATH.exists():
            print(f"{ALLOWLIST_PATH} already exists; the list is frozen", file=sys.stderr)
            return 1
        ALLOWLIST_PATH.write_text(HEADER + "".join(f"{n}\n" for n in tree_names()))
        print(f"wrote {len(tree_names())} names to {ALLOWLIST_PATH}")
        return 0
    errors = check()
    for e in errors:
        print(e, file=sys.stderr)
    if not errors:
        print(f"{ALLOWLIST_PATH.name}: {len(read_allowlist())} names, all present")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
