"""Reason review boundaries use synthetic references, never live tracker IDs."""
import csv
import sys
import tempfile
from unittest.mock import patch
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from reason_references import reference_categories
import validate


class ReasonReferenceTests(unittest.TestCase):
    def check(self, text, batches=None, file="", lines=None):
        return reference_categories(text, batches or set(), file, lines)

    def test_tracker_forms_need_review(self):
        number = str(90000 + 1)
        for prefix in ("task ", "tasks ", "task-", "bmdb ", "benchmarking_db ",
                       "aurora_lint ", "aurora-lint task ", "tools_sqc "):
            with self.subTest(prefix=prefix):
                self.assertIn("tracker reference", self.check(prefix + number))

    def test_exact_current_batch_and_dated_ruling_are_protected(self):
        batch = "task-" + str(90000 + 2) + "-source-review"
        self.assertFalse(self.check("Previously reviewed in " + batch, {batch}))
        self.assertTrue(self.check("Previously reviewed in " + batch))
        self.assertFalse(self.check("API00-C/2026-10-01/1"))
        self.assertTrue(self.check(batch + "; task " + str(90000 + 3), {batch}))

    def test_machine_shape_in_batch_is_protected(self):
        machine = "r" + str(700 + 1)
        batch = "review-" + machine + "-source"
        self.assertFalse(self.check(batch, {batch}))
        self.assertIn("numbered machine", self.check(machine))
        self.assertTrue(self.check("dev-" + str(90000 + 4)))

    def test_ledger_and_abbreviations_need_review(self):
        number = str(90000 + 5)
        for text in ("round " + number, "rounds " + number, "batch" + number,
                     "gt-" + number, "16-40_b" + number + "/b2",
                     "bmdb 2026-01-01-obsolete-labels"):
            self.assertTrue(self.check(text), text)

    def test_known_code_tokens_and_unknown_tokens(self):
        self.assertFalse(self.check("P0 P2 P3 P4 P5 P11 P15 P521"))
        self.assertIn("ambiguous numbered token", self.check("P" + str(90000 + 6)))
        self.assertFalse(self.check("BRULE-058 MSC04-C CWE-89 nToken pToken"))
        self.assertFalse(self.check("ROUND8(sizeof(*pX)); ROUND8 yields a value"))

    def test_public_compiler_issue_and_token_paste(self):
        reference = "#" + str(90000 + 7)
        self.assertFalse(self.check("GCC version-bug threshold (issue " + reference + ")"))
        self.assertTrue(self.check("GCC version-bug threshold; same as " + reference))
        self.assertTrue(self.check("Same as " + reference))
        self.assertFalse(self.check("d##0; f.c:42; API00-C/2026-01-01/2"))

    def test_bare_finding_requires_same_file_source_evidence(self):
        line = str(90000 + 8)
        text = "Duplicate of the " + line + " finding"
        self.assertFalse(self.check(text, file="f.c", lines={("", "f.c", line)}))
        self.assertTrue(self.check(text, file="g.c", lines={("", "f.c", line)}))
        self.assertTrue(self.check(text))
        self.assertTrue(reference_categories(text, set(), "f.c",
                                            {("other-commit", "f.c", line)}, "this-commit"))

    def test_commit_numbers_and_named_reads_need_review(self):
        text = "abcdef123 (" + str(90000 + 9) + " mechanism)"
        self.assertTrue(self.check(text))
        self.assertFalse(self.check("abcdef123 (stores_params)"))
        self.assertTrue(self.check("per worker's read"))
        self.assertFalse(self.check("per the initial adjudicator's read"))
        self.assertFalse(self.check("it's read; iteration's read; sscanf's read-only input"))

    def test_validator_checks_reason_only(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            (data / "project").mkdir()
            path = data / "project" / "adjudication.csv"
            tracker = "task " + str(90000 + 10)
            row = dict.fromkeys(validate.CSV_COLUMNS, "")
            row.update(project="project", codebase_commit="a" * 40,
                       file_path="f.c", line="1", rule_id="MEM31-C", verdict="FP",
                       source="public-batch", reason="Ownership is transferred to the caller.",
                       provenance=tracker, confidence=tracker, adjudicated_at="2026-01-01")
            def write():
                with path.open("w", newline="") as stream:
                    writer = csv.DictWriter(stream, fieldnames=validate.CSV_COLUMNS,
                                            lineterminator="\n")
                    writer.writeheader()
                    writer.writerow(row)
            with patch.object(validate, "DATA_DIR", data):
                write()
                errors = []
                validate.validate_csvs(errors, {"public-batch": {}}, {})
                self.assertFalse(errors)
                row["reason"] = tracker
                write()
                errors = []
                validate.validate_csvs(errors, {"public-batch": {}}, {})
                self.assertTrue(any("public-reference review" in e for e in errors))

    def test_bare_tracker_context_needs_review(self):
        number = str(9000 + 1)
        for text in (number + " FP pattern", "which " + number + " confirmed",
                     number + " stores_params", "related to " + number):
            self.assertTrue(self.check(text), text)


if __name__ == "__main__":
    unittest.main()
