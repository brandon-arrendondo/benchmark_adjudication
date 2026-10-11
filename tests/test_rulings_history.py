"""validate.py resolves a label's rulings_ids at its rulings_commit.

A label records the commit of this repository whose rulings/ it was judged
under (aurora-lint ADR-0018, Decision 4). That commit must be in the
repository's history, and every ruling id the label applied must be defined
in that commit's rulings/: an id added later was not there to apply.

Each test builds a throwaway git repository standing in for this one.

Run:  python3 -m unittest discover -s tests -v
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import rule_text_pin  # noqa: E402
import validate  # noqa: E402

SHA = "a" * 40
SHA256 = "b" * 64
HEADER = ",".join(validate.CSV_COLUMNS) + "\n"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def rule_file(*items):
    return ("# SIG30-C\n\n- **Rule text:** [x](y)\n\n## Rulings\n\n"
            + "".join(f"- **SIG30-C/2026-10-10/{n}, item.** Text.\n" for n in items))


class RulingsHistory(unittest.TestCase):
    """History: `first` defines SIG30-C/2026-10-10/1 and P/lists; `second`,
    on main after it, adds SIG30-C/2026-10-10/2; `side` is a commit on a
    branch main never merged."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.rulings, self.data = self.repo / "rulings", self.repo / "data"
        (self.rulings / "rules").mkdir(parents=True)
        (self.data / "p").mkdir(parents=True)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.email", "t@example.invalid")
        git(self.repo, "config", "user.name", "t")
        (self.rulings / "rule-text-map.json").write_text(json.dumps({"rules": {"SIG30-C": {
            "commit": SHA, "path": "a.md", "sha256": SHA256, "carried_forward": True,
            "set": "2026-10-10", "reason": "first map"}}}))
        (self.rulings / "principles.md").write_text("## P/lists: reading lists\n")
        self.first = self.commit(rule_file(1))
        git(self.repo, "switch", "-q", "-c", "side")
        self.side = self.commit(rule_file(1, 3))
        git(self.repo, "switch", "-q", "main")
        self.second = self.commit(rule_file(1, 2))
        self.saved = (validate.RULINGS_DIR, validate.DATA_DIR, validate.GIT_REPO)
        validate.RULINGS_DIR, validate.DATA_DIR = self.rulings, self.data
        validate.GIT_REPO = self.repo

    def tearDown(self):
        validate.RULINGS_DIR, validate.DATA_DIR, validate.GIT_REPO = self.saved
        self.tmp.cleanup()

    def commit(self, text):
        (self.rulings / "rules" / "SIG30-C.md").write_text(text)
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "rulings")
        return git(self.repo, "rev-parse", "HEAD")

    def label(self, rulings_commit, rulings_ids):
        pins = {"rule_text_commit": SHA, "rule_text_version": SHA256,
                "rule_text_basis": "judged", "rulings_commit": rulings_commit,
                "rulings_ids": rulings_ids}
        row = (f"p,{SHA},f.c,1,SIG30-C,TP,a,r,s,t,p,c,"
               + ",".join(pins[c] for c in rule_text_pin.PIN_COLUMNS) + "\n")
        (self.data / "p" / "adjudication.csv").write_text(HEADER + row)

    def check(self):
        errors = []
        unchecked = validate.check_rulings(errors)
        return errors, unchecked

    def test_ids_defined_at_the_cited_commit_pass(self):
        self.label(self.first, "SIG30-C/2026-10-10/1 P/lists")
        self.assertEqual(self.check(), ([], 0))

    def test_id_added_after_the_cited_commit_is_rejected(self):
        # Today's tree defines /2, but the label says it was judged at
        # `first`, where /2 did not exist yet.
        self.label(self.first, "SIG30-C/2026-10-10/2")
        errors, _ = self.check()
        self.assertTrue(any("SIG30-C/2026-10-10/2 is not defined in rulings/ at "
                            f"rulings_commit {self.first[:12]}" in e for e in errors), errors)

    def test_the_same_id_at_a_later_commit_passes(self):
        self.label(self.second, "SIG30-C/2026-10-10/2")
        self.assertEqual(self.check(), ([], 0))

    def test_unknown_commit_is_rejected(self):
        self.label("e" * 40, "SIG30-C/2026-10-10/1")
        errors, _ = self.check()
        self.assertTrue(any("is not a commit in this repository's history" in e
                            for e in errors), errors)

    def test_commit_on_an_unmerged_branch_is_rejected(self):
        self.label(self.side, "SIG30-C/2026-10-10/1")
        errors, _ = self.check()
        self.assertTrue(any("is not a commit in this repository's history" in e
                            for e in errors), errors)

    def test_history_ref_names_the_commit_whose_history_counts(self):
        # A tree extracted at `side` from a clone whose HEAD is main: with
        # --history-ref side, `side` is in its history and `second` is not.
        self.saved_ref = validate.HISTORY_REF
        self.addCleanup(setattr, validate, "HISTORY_REF", self.saved_ref)
        validate.HISTORY_REF = self.side
        self.label(self.side, "SIG30-C/2026-10-10/3")
        self.assertEqual(self.check(), ([], 0))
        self.label(self.second, "SIG30-C/2026-10-10/2")
        errors, _ = self.check()
        self.assertTrue(any("is not a commit in this repository's history" in e
                            for e in errors), errors)

    def test_without_history_ids_are_checked_against_this_tree_and_counted(self):
        validate.GIT_REPO = None
        self.label(self.first, "SIG30-C/2026-10-10/2")
        self.assertEqual(self.check(), ([], 1))
        self.label(self.first, "SIG30-C/2026-10-10/9")
        errors, _ = self.check()
        self.assertTrue(any("SIG30-C/2026-10-10/9 is not defined under rulings/" in e
                            for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
