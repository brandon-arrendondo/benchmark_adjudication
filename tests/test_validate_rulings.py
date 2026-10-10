"""scripts/validate.py's check_rulings: rulings/ is consistent with itself
and with the labels.

Each test builds a small repository layout in a temporary directory and
points validate's RULINGS_DIR and DATA_DIR at it.

Run:  python3 -m unittest discover -s tests -v
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate  # noqa: E402

SHA = "a" * 40
SHA256 = "b" * 64
HEADER = ",".join(validate.CSV_COLUMNS) + "\n"


def rule_file(rule, body=""):
    return (f"# {rule}\n\n- **Rule text:** [x](y)\n\n## Rulings\n\n"
            f"- **{rule}/2026-10-07/1, the form.** Text.\n{body}")


class CheckRulings(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.rulings = root / "rulings"
        self.data = root / "data"
        (self.rulings / "rules").mkdir(parents=True)
        (self.data / "p").mkdir(parents=True)
        self.saved = (validate.RULINGS_DIR, validate.DATA_DIR)
        validate.RULINGS_DIR, validate.DATA_DIR = self.rulings, self.data
        self.write_rule("SIG30-C")
        self.write_map({"SIG30-C": {"commit": SHA, "path": "a/sig30-c.md",
                                    "sha256": SHA256}})
        self.write_labels(["SIG30-C"])

    def tearDown(self):
        validate.RULINGS_DIR, validate.DATA_DIR = self.saved
        self.tmp.cleanup()

    def write_rule(self, rule, text=None):
        (self.rulings / "rules" / f"{rule}.md").write_text(
            text if text is not None else rule_file(rule), encoding="utf-8")

    def write_map(self, rules):
        (self.rulings / "rule-text-map.json").write_text(
            json.dumps({"rules": rules}), encoding="utf-8")

    def write_labels(self, rules):
        rows = "".join(f"p,{SHA},f.c,1,{r},TP,a,r,s,t,p,c\n" for r in rules)
        (self.data / "p" / "adjudication.csv").write_text(HEADER + rows,
                                                          encoding="utf-8")

    def errors(self):
        errs = []
        validate.check_rulings(errs)
        return errs

    def test_consistent_layout_passes(self):
        self.assertEqual(self.errors(), [])

    def test_task_numbered_id_is_rejected(self):
        self.write_rule("SIG30-C", rule_file("SIG30-C", "- See SIG30-C/2358/3.\n"))
        self.assertTrue(any("not dated" in e for e in self.errors()))

    def test_batch_id_in_principles_is_rejected(self):
        (self.rulings / "principles.md").write_text(
            "Ruled 2026-10-09 (from P84 on).\n", encoding="utf-8")
        self.assertTrue(any("'P84'" in e for e in self.errors()))

    def test_task_id_in_readme_is_rejected(self):
        (self.rulings / "README.md").write_text(
            "Ruled under aurora_lint 2358.\n", encoding="utf-8")
        self.assertTrue(any("aurora_lint 2358" in e for e in self.errors()))

    def test_bare_item_reference_is_rejected(self):
        self.write_rule("SIG30-C", rule_file("SIG30-C",
                                             "- As ERR33-C ruling 10.\n"))
        self.assertTrue(any("internal reference" in e for e in self.errors()))

    def test_principle_ids_are_not_batch_ids(self):
        (self.rulings / "principles.md").write_text(
            "## P/lists: reading lists\n", encoding="utf-8")
        self.assertEqual(self.errors(), [])

    def test_id_for_another_rule_is_rejected(self):
        self.write_rule("SIG30-C", rule_file("SIG30-C",
                                             "- **SIG31-C/2026-10-07/1, x.**\n"))
        self.assertTrue(any("defines a ruling id for SIG31-C" in e
                            for e in self.errors()))

    def test_duplicate_id_is_rejected(self):
        self.write_rule("SIG30-C", rule_file("SIG30-C",
                                             "- **SIG30-C/2026-10-07/1, again.**\n"))
        self.assertTrue(any("defined twice" in e for e in self.errors()))

    def test_labelled_rule_without_ruling_is_rejected(self):
        self.write_labels(["SIG30-C", "SIG31-C"])
        errs = self.errors()
        self.assertTrue(any("SIG31-C has no rulings/rules" in e for e in errs))

    def test_unruled_list_covers_a_labelled_rule(self):
        self.write_labels(["SIG30-C", "SIG31-C"])
        self.write_map({"SIG30-C": {"commit": SHA, "path": "a.md", "sha256": SHA256},
                        "SIG31-C": {"commit": SHA, "path": "b.md", "sha256": SHA256}})
        (self.rulings / "unruled.md").write_text("- **SIG31-C**: open\n",
                                                 encoding="utf-8")
        self.assertEqual(self.errors(), [])

    def test_labelled_rule_without_pin_is_rejected(self):
        self.write_map({})
        self.assertTrue(any("has no pin" in e for e in self.errors()))

    def test_rule_without_cert_page_needs_no_pin(self):
        self.write_rule("MSC42-C", "# MSC42-C\n\n- **Rule text:** none.\n")
        self.write_labels(["SIG30-C", "MSC42-C"])
        self.assertEqual(self.errors(), [])

    def test_malformed_pin_is_rejected(self):
        self.write_map({"SIG30-C": {"commit": "abc", "path": "a.md",
                                    "sha256": SHA256}})
        self.assertTrue(any("not a full SHA" in e for e in self.errors()))


if __name__ == "__main__":
    unittest.main()
