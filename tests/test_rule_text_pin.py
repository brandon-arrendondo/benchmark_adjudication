"""The rule-text pin of aurora-lint ADR-0018: scripts/rule_text_pin.py and
validate.py's check_label_pins and check_map_merged.

Run:  python3 -m unittest discover -s tests -v
"""
import hashlib
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
RULINGS_SHA = "c" * 40
OLD_SHA = "d" * 40
SHA256 = "b" * 64
OLD_SHA256 = "e" * 64
HEADER = ",".join(validate.CSV_COLUMNS) + "\n"


def entry(carried_forward=True, **extra):
    return {"commit": SHA, "path": "a.md", "sha256": SHA256,
            "carried_forward": carried_forward, "set": "2026-10-10",
            "reason": "first map", **extra}


def pins(commit=SHA, version=SHA256, basis="carried-forward", rulings_commit="",
         rulings_ids=""):
    return {"rule_text_commit": commit, "rule_text_version": version,
            "rule_text_basis": basis, "rulings_commit": rulings_commit,
            "rulings_ids": rulings_ids}


class Layout(unittest.TestCase):
    """A temporary repository: one ruled rule (SIG30-C) and a principle."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.rulings, self.data = root / "rulings", root / "data"
        (self.rulings / "rules").mkdir(parents=True)
        (self.data / "p").mkdir(parents=True)
        self.saved = (validate.RULINGS_DIR, validate.DATA_DIR)
        validate.RULINGS_DIR, validate.DATA_DIR = self.rulings, self.data
        (self.rulings / "rules" / "SIG30-C.md").write_text(
            "# SIG30-C\n\n- **Rule text:** [x](y)\n\n## Rulings\n\n"
            "- **SIG30-C/2026-10-10/3, the form.** Text.\n", encoding="utf-8")
        (self.rulings / "principles.md").write_text(
            "## P/lists: reading lists\n", encoding="utf-8")
        self.write_map({"SIG30-C": entry()})

    def tearDown(self):
        validate.RULINGS_DIR, validate.DATA_DIR = self.saved
        self.tmp.cleanup()

    def write_map(self, rules):
        (self.rulings / "rule-text-map.json").write_text(
            json.dumps({"rules": rules}), encoding="utf-8")

    def write_label(self, fields, rule="SIG30-C"):
        row = (f"p,{SHA},f.c,1,{rule},TP,a,r,s,t,p,c,"
               + ",".join(fields[c] for c in rule_text_pin.PIN_COLUMNS) + "\n")
        (self.data / "p" / "adjudication.csv").write_text(HEADER + row,
                                                          encoding="utf-8")

    def errors(self):
        errs = []
        validate.check_rulings(errs)
        return errs


class CheckLabelPins(Layout):
    def test_carried_forward_label_passes(self):
        self.write_label(pins())
        self.assertEqual(self.errors(), [])

    def test_judged_label_with_its_rulings_passes(self):
        self.write_label(pins(basis="judged", rulings_commit=RULINGS_SHA,
                              rulings_ids="SIG30-C/2026-10-10/3 P/lists"))
        self.assertEqual(self.errors(), [])

    def test_version_the_map_does_not_know_is_rejected(self):
        # The guard: a label can only cite text the map pins, and the map
        # pins merged commits only, so no label cites unmerged wording.
        self.write_label(pins(version="f" * 64))
        self.assertTrue(any("is not a pin" in e for e in self.errors()))

    def test_commit_the_map_does_not_know_is_rejected(self):
        self.write_label(pins(commit=OLD_SHA))
        self.assertTrue(any("is not a pin" in e for e in self.errors()))

    def test_carried_forward_to_a_re_judge_pin_is_rejected(self):
        self.write_map({"SIG30-C": entry(carried_forward=False)})
        self.write_label(pins())
        self.assertTrue(any("must be re-judged" in e for e in self.errors()))

    def test_judged_at_a_re_judge_pin_passes(self):
        self.write_map({"SIG30-C": entry(carried_forward=False)})
        self.write_label(pins(basis="judged", rulings_commit=RULINGS_SHA,
                              rulings_ids="SIG30-C/2026-10-10/3"))
        self.assertEqual(self.errors(), [])

    def test_label_at_a_pin_in_the_history_passes(self):
        old = {"commit": OLD_SHA, "path": "a.md", "sha256": OLD_SHA256,
               "carried_forward": True}
        self.write_map({"SIG30-C": entry(history=[old])})
        self.write_label(pins(commit=OLD_SHA, version=OLD_SHA256))
        self.assertEqual(self.errors(), [])

    def test_malformed_history_pin_is_rejected(self):
        self.write_map({"SIG30-C": entry(history=[{"commit": "abc"}])})
        self.write_label(pins())
        self.assertTrue(any("history[0]: commit is not a full SHA" in e
                            for e in self.errors()))

    def test_judged_label_without_rulings_commit_is_rejected(self):
        self.write_label(pins(basis="judged", rulings_ids="SIG30-C/2026-10-10/3"))
        self.assertTrue(any("full rulings_commit" in e for e in self.errors()))

    def test_judged_label_without_ruling_ids_is_rejected(self):
        self.write_label(pins(basis="judged", rulings_commit=RULINGS_SHA))
        self.assertTrue(any("ruling ids it applied" in e for e in self.errors()))

    def test_undefined_ruling_id_is_rejected(self):
        self.write_label(pins(basis="judged", rulings_commit=RULINGS_SHA,
                              rulings_ids="SIG30-C/2026-10-10/9"))
        self.assertTrue(any("SIG30-C/2026-10-10/9 is not defined" in e
                            for e in self.errors()))

    def test_unknown_basis_is_rejected(self):
        self.write_label(pins(basis="guessed"))
        self.assertTrue(any("rule_text_basis 'guessed'" in e for e in self.errors()))

    def test_unpinned_label_passes(self):
        self.write_label(pins(commit="", version="unpinned", basis="unpinned"))
        self.assertEqual(self.errors(), [])

    def test_unpinned_label_naming_a_commit_is_rejected(self):
        self.write_label(pins(version="unpinned", basis="unpinned"))
        self.assertTrue(any("an unpinned label names no commit" in e
                            for e in self.errors()))

    def test_map_entry_needs_carried_forward_set_and_reason(self):
        bare = {"commit": SHA, "path": "a.md", "sha256": SHA256}
        self.write_map({"SIG30-C": bare})
        self.write_label(pins(commit="", version="unpinned", basis="unpinned"))
        errs = self.errors()
        for text in ("carried_forward is not true or false", "set is not a date",
                     "no reason the pin was set"):
            self.assertTrue(any(text in e for e in errs), text)


class Backfill(Layout):
    def write_legacy(self, rules):
        old_header = ",".join(validate.CSV_COLUMNS[:12]) + "\n"
        rows = "".join(f"p,{SHA},f.c,{n},{r},TP,a,r,s,t,p,c\n"
                       for n, r in enumerate(rules, 1))
        (self.data / "p" / "adjudication.csv").write_text(old_header + rows,
                                                          encoding="utf-8")

    def backfill(self):
        return rule_text_pin.backfill(self.data, self.rulings / "rule-text-map.json")

    def test_carried_forward_rule_takes_its_first_map_version(self):
        self.write_legacy(["SIG30-C"])
        self.assertEqual(self.backfill(), {"carried-forward": 1})
        self.assertEqual(self.errors(), [])
        row = (self.data / "p" / "adjudication.csv").read_text().splitlines()[1]
        self.assertTrue(row.endswith(f",{SHA},{SHA256},carried-forward,,"))

    def test_re_judge_rule_and_unmapped_rule_are_unpinned(self):
        self.write_map({"SIG30-C": entry(carried_forward=False)})
        (self.rulings / "rules" / "MSC42-C.md").write_text(
            "# MSC42-C\n\n- **Rule text:** none.\n", encoding="utf-8")
        self.write_legacy(["SIG30-C", "MSC42-C"])
        self.assertEqual(self.backfill(), {"unpinned": 2})
        self.assertEqual(self.errors(), [])

    def test_second_run_leaves_the_file_alone(self):
        self.write_legacy(["SIG30-C"])
        self.backfill()
        path = self.data / "p" / "adjudication.csv"
        before = path.read_bytes()
        self.assertEqual(self.backfill(), {})
        self.assertEqual(path.read_bytes(), before)


class MapDigest(unittest.TestCase):
    def test_digest_ignores_key_order_and_whitespace(self):
        a = {"rules": {"A": {"x": 1, "y": 2}}, "pin_commit": SHA}
        b = json.loads(json.dumps({"pin_commit": SHA, "rules": {"A": {"y": 2, "x": 1}}},
                                  indent=2))
        self.assertEqual(rule_text_pin.map_digest(a), rule_text_pin.map_digest(b))

    def test_digest_changes_with_a_pin(self):
        a = {"rules": {"A": {"sha256": SHA256}}}
        b = {"rules": {"A": {"sha256": OLD_SHA256}}}
        self.assertNotEqual(rule_text_pin.map_digest(a), rule_text_pin.map_digest(b))


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


class CheckMapMerged(Layout):
    """check_map_merged against a throwaway git repository standing in for
    CERT's: its origin/main has one commit; a branch has an unmerged one."""

    def setUp(self):
        super().setUp()
        self.cert = Path(self.tmp.name) / "cert"
        self.cert.mkdir()
        git(self.cert, "init", "-q", "-b", "main")
        git(self.cert, "config", "user.email", "t@example.invalid")
        git(self.cert, "config", "user.name", "t")
        (self.cert / "a.md").write_text("merged text\n")
        git(self.cert, "add", "a.md")
        git(self.cert, "commit", "-q", "-m", "merged")
        self.merged = git(self.cert, "rev-parse", "HEAD")
        git(self.cert, "update-ref", "refs/remotes/origin/main", self.merged)
        git(self.cert, "switch", "-q", "-c", "proposal")
        (self.cert / "a.md").write_text("proposed text\n")
        git(self.cert, "commit", "-q", "-am", "proposed")
        self.proposed = git(self.cert, "rev-parse", "HEAD")

    def check(self, commit, text):
        self.write_map({"SIG30-C": entry(
            commit=commit, sha256=hashlib.sha256(text.encode()).hexdigest())})
        errs = []
        validate.check_map_merged(errs, self.cert)
        return errs

    def test_merged_pin_passes(self):
        self.assertEqual(self.check(self.merged, "merged text\n"), [])

    def test_pin_at_unmerged_wording_is_rejected(self):
        errs = self.check(self.proposed, "proposed text\n")
        self.assertTrue(any("not a commit on CERT's origin/main" in e for e in errs))

    def test_pin_whose_hash_is_not_the_page_is_rejected(self):
        errs = self.check(self.merged, "other text\n")
        self.assertTrue(any("SHA-256 is not the one recorded" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
