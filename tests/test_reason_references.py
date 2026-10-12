"""Reason review boundaries use synthetic references, never live tracker IDs."""
import csv
import sys
import tempfile
from unittest.mock import patch
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from reason_references import reference_categories, column_reference_categories
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
        machine = "dev-" + str(90000 + 4)
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
        self.assertFalse(self.check("P0 P2 P3 P4 P5 P11 P15 P256 P384 P521"))
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
        self.assertTrue(self.check("abcdef123 (" + str(90000 + 9) + ", mechanism)"))
        self.assertTrue(self.check("per worker's read"))
        self.assertFalse(self.check("per the initial adjudicator's read"))
        self.assertFalse(self.check("it's read; iteration's read; sscanf's read-only input"))

    def test_internal_run_numbers_require_public_ids(self):
        number = str(90000 + 11)
        public_id = "sqc-1.2.3-abcdef123"
        self.assertFalse(self.check("Verified at " + public_id))
        for separator in (" ", "-", "_"):
            self.assertIn("internal run number", self.check("run" + separator + number))
        self.assertTrue(self.check("run " + number + " (" + public_id + ")"))
        batch = "review-run-" + number
        self.assertFalse(self.check(batch, {batch}))
        self.assertFalse(self.check("offset runs 0..limit; iteration runs 1..size"))

    def test_ruling_attribution_uses_project_language(self):
        self.assertIn("internal ruling attribution", self.check("coordinator ruling"))
        self.assertIn("internal ruling attribution", self.check("to the coordinator"))
        self.assertFalse(self.check("project ruling; for project review"))

    def test_aes_round_counts_are_code_evidence(self):
        self.assertFalse(self.check("AES rounds 12; AES-256 rounds 14"))
        self.assertIn("numbered review", self.check("AES rounds 12; review round 12"))
        self.assertIn("numbered review", self.check("rounds 12 while reviewing AES"))

    def test_validator_checks_public_attribution_columns(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            (data / "project").mkdir()
            path = data / "project" / "adjudication.csv"
            tracker = "task " + str(90000 + 10)
            row = dict.fromkeys(validate.CSV_COLUMNS, "")
            row.update(project="project", codebase_commit="a" * 40,
                       file_path="f.c", line="1", rule_id="MEM31-C", verdict="FP",
                       source="public-batch", reason="Ownership is transferred to the caller.",
                       provenance="source review", confidence=tracker, adjudicated_at="2026-01-01")
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
                for column in ("reason", "provenance", "adjudicator"):
                    with self.subTest(column=column):
                        previous = row[column]
                        row[column] = tracker
                        write()
                        errors = []
                        validate.validate_csvs(errors, {"public-batch": {}}, {})
                        self.assertTrue(any(column + " needs public-reference review" in e
                                            for e in errors))
                        row[column] = previous

    def test_embedded_task_tokens_and_exact_batch_exception(self):
        number = str(90000 + 12)
        for text in ("delta_err33_task" + number, "delta_msc13_task_" + number):
            for column in ("reason", "provenance", "adjudicator"):
                with self.subTest(text=text, column=column):
                    self.assertIn("tracker reference",
                                  column_reference_categories(column, text))
                    self.assertFalse(column_reference_categories(column, text, {text}))
        self.assertFalse(column_reference_categories("source", "task" + number))

    def test_attribution_policy_keeps_model_versions_and_public_builds(self):
        for model in ("claude", "claude-reverify", "claude-audit",
                      "claude-sonnet-5", "claude-sonnet-5-revert", "claude-opus-4.8"):
            self.assertFalse(column_reference_categories("adjudicator", model))
        self.assertTrue(column_reference_categories("adjudicator", "claude-r" + str(90000 + 13)))
        self.assertTrue(column_reference_categories("adjudicator", "claude-sonnet-5-" + str(90000 + 14)))
        self.assertTrue(column_reference_categories("provenance", "runs " + str(90000 + 15)))
        self.assertFalse(column_reference_categories("provenance", "build sqc-1.2.3-abcdef123"))
        self.assertFalse(column_reference_categories("provenance", "aurora-lint 12345678"))
        self.assertFalse(column_reference_categories("provenance", "aurora-lint 12345abc"))
        self.assertTrue(column_reference_categories("provenance", "aurora-lint " + str(90000 + 16)))
        self.assertFalse(column_reference_categories("adjudicator", "claude-opus-5-5"))
        self.assertFalse(column_reference_categories("provenance", "offset runs 0..limit; index runs 1..size"))
        self.assertFalse(column_reference_categories("provenance", "message: array index b64; ROUND8; AES rounds 12; P256"))

    def test_campaign_segment_at_any_position_requires_review(self):
        for number in (str(900 + 1), str(90000 + 1)):
            for name in ("claude-" + number, "codex-" + number,
                         "claude-sonnet-5-" + number + "-reverify",
                         "claude-sonnet-5-" + number + "-revert",
                         "claude-" + number + "-review-model-5"):
                with self.subTest(name=name):
                    self.assertIn("adjudicator campaign reference",
                                  column_reference_categories("adjudicator", name))
        for name in ("claude-opus-5-5", "claude-sonnet-5", "claude-sonnet-5-reverify"):
            with self.subTest(name=name):
                self.assertFalse(column_reference_categories("adjudicator", name))

    def test_oracle_tag_and_resolving_batch_citations(self):
        tag = "oracle-tag: interface-fixed signature: fn-pointer slot"
        self.assertFalse(column_reference_categories("provenance", tag + "; source verified"))
        batch = "review-task" + str(90000 + 17) + "-r" + str(90000 + 18)
        self.assertFalse(column_reference_categories("provenance", tag + "; prior " + batch, {batch}))
        self.assertTrue(column_reference_categories("provenance", tag + "; prior " + batch))

    def test_bare_tracker_context_needs_review(self):
        number = str(9000 + 1)
        for text in (number + " FP pattern", "which " + number + " confirmed",
                     number + " stores_params", "related to " + number):
            self.assertTrue(self.check(text), text)


if __name__ == "__main__":
    unittest.main()
