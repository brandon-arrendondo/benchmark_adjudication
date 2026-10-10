"""scripts/to_batch.py: an applied verdict becomes a label judged at its
rule's current pin, under the rulings it names (aurora-lint ADR-0018).

Run:  python3 -m unittest discover -s tests -v
"""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import rule_text_pin  # noqa: E402
import to_batch  # noqa: E402
import validate  # noqa: E402

SHA = "a" * 40
RULINGS_SHA = "c" * 40
SHA256 = "b" * 64


class ToBatch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "data" / "p").mkdir(parents=True)
        (root / "batches" / "old").mkdir(parents=True)
        (root / "rulings").mkdir()
        self.map_path = root / "rulings" / "rule-text-map.json"
        self.map_path.write_text(json.dumps({"rules": {"SIG30-C": {
            "commit": SHA, "path": "a.md", "sha256": SHA256,
            "carried_forward": False, "set": "2026-10-10", "reason": "first map"}}}))
        legacy = rule_text_pin.backfill_fields("SIG30-C", {})
        self.csv_path = root / "data" / "p" / "adjudication.csv"
        with self.csv_path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=validate.CSV_COLUMNS, lineterminator="\n")
            w.writeheader()
            w.writerow({"project": "p", "codebase_commit": SHA, "file_path": "f.c",
                        "line": "1", "rule_id": "SIG30-C", "verdict": "FP",
                        "adjudicator": "claude", "reason": "r", "source": "old",
                        "adjudicated_at": "2026-06-01", "provenance": "",
                        "confidence": "", **legacy})
        (root / "batches" / "old" / "manifest.json").write_text(
            json.dumps({"row_count": 1}))
        self.verdicts = root / "verdicts.csv"
        self.patches = [mock.patch.object(to_batch, "DATA_DIR", root / "data"),
                        mock.patch.object(to_batch, "BATCHES_DIR", root / "batches"),
                        mock.patch.object(rule_text_pin, "MAP_PATH", self.map_path)]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def run_batch(self, rulings):
        with self.verdicts.open("w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["sample_id", "project", "codebase_commit", "file_path", "line",
                        "rule_id", "human_verdict", "human_reason", "human_rulings"])
            w.writerow(["s1", "p", SHA, "f.c", "1", "SIG30-C", "TP", "basis", rulings])
        argv = ["to_batch.py", str(self.verdicts), "new", "--rulings-commit", RULINGS_SHA]
        with mock.patch.object(sys, "argv", argv):
            to_batch.main()
        with self.csv_path.open(newline="") as f:
            return next(csv.DictReader(f))

    def test_applied_row_is_judged_at_the_current_pin(self):
        row = self.run_batch("SIG30-C/2026-10-10/3  P/lists")
        self.assertEqual((row["verdict"], row["rule_text_commit"], row["rule_text_version"],
                          row["rule_text_basis"], row["rulings_commit"], row["rulings_ids"]),
                         ("TP", SHA, SHA256, "judged", RULINGS_SHA,
                          "SIG30-C/2026-10-10/3 P/lists"))

    def test_row_without_rulings_is_rejected(self):
        row = self.run_batch("")
        self.assertEqual((row["verdict"], row["rule_text_basis"]), ("FP", "unpinned"))

    def test_rulings_commit_must_be_full(self):
        argv = ["to_batch.py", str(self.verdicts), "new", "--rulings-commit", "abc"]
        with mock.patch.object(sys, "argv", argv), self.assertRaises(SystemExit):
            to_batch.main()


if __name__ == "__main__":
    unittest.main()
