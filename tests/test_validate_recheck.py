"""scripts/validate.py's check_recheck: the re-check block a correction batch
carries so that a flip rate is flipped / reviewed from the manifest alone
(benchmarking_db 1889).

Pure-function tests on hand-built manifests; nothing reads the repository.

Run:  python3 -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate  # noqa: E402

DUE = validate.RECHECK_REQUIRED_FROM + "T12:00:00Z"
BEFORE = "2026-09-20T12:00:00Z"


def recheck(**overrides):
    block = {"basis": "merit", "selection": "census", "reviewed": 120, "flipped": 7,
             "blind_to_prior_verdict": False, "blind_to_diagnostic": False}
    block.update(overrides)
    return block


def manifest(block=..., **fields):
    m = {"submitted_at": DUE, "row_count": 7}
    if block is not ...:
        m["recheck"] = block
    m.update(fields)
    return m


def errors(m):
    return validate.check_recheck(m, "m")


class Required(unittest.TestCase):
    def test_a_new_manifest_must_say_whether_it_rechecked(self):
        self.assertIn("missing 'recheck'", errors(manifest())[0])

    def test_a_batch_of_new_labels_says_null(self):
        self.assertEqual(errors(manifest(None)), [])

    def test_an_older_manifest_is_left_alone(self):
        self.assertEqual(errors(manifest(submitted_at=BEFORE)), [])

    def test_a_correction_batch_cannot_say_null(self):
        e = errors(manifest(None, corrections={"FP_to_TP": 3}))
        self.assertIn("has 'corrections' but 'recheck' is null", e[0])

    def test_an_older_manifest_that_has_a_block_is_still_checked(self):
        e = errors(manifest(recheck(basis="vibes"), submitted_at=BEFORE))
        self.assertTrue(any("recheck.basis 'vibes'" in x for x in e))


class Shape(unittest.TestCase):
    def test_a_complete_block_passes(self):
        self.assertEqual(errors(manifest(recheck())), [])

    def test_every_field_is_required(self):
        block = recheck()
        del block["blind_to_diagnostic"]
        self.assertEqual(errors(manifest(block)), ["m: recheck is missing 'blind_to_diagnostic'"])

    def test_basis_and_selection_come_from_the_lists(self):
        e = errors(manifest(recheck(basis="policy", selection="all")))
        self.assertEqual(len(e), 2)

    def test_a_ruling_names_the_decision(self):
        self.assertIn("needs 'ruling'", errors(manifest(recheck(basis="ruling")))[0])
        self.assertEqual(errors(manifest(recheck(basis="ruling", ruling="ADR-0011"))), [])
        self.assertIn("needs 'ruling'", errors(manifest(recheck(basis="standard")))[0])

    def test_a_sample_names_its_seed(self):
        self.assertIn("needs its 'seed'", errors(manifest(recheck(selection="sample")))[0])
        self.assertEqual(errors(manifest(recheck(selection="sample", seed=20260930))), [])

    def test_counts_are_non_negative_integers_and_flags_are_booleans(self):
        e = errors(manifest(recheck(reviewed="120", flipped=True, blind_to_prior_verdict=1)))
        self.assertEqual(len(e), 3)


class Consistency(unittest.TestCase):
    def test_flipped_cannot_exceed_reviewed(self):
        e = errors(manifest(recheck(reviewed=5, flipped=7)))
        self.assertIn("flipped 7 exceeds reviewed 5", e[0])

    def test_flipped_cannot_exceed_the_rows_the_batch_owns(self):
        e = errors(manifest(recheck(), row_count=3))
        self.assertIn("exceeds row_count 3", e[0])

    def test_flipped_equals_the_corrections_total(self):
        self.assertEqual(errors(manifest(recheck(), corrections={"FP_to_TP": 7})), [])
        e = errors(manifest(recheck(), corrections={"FP_to_TP": 5, "TP_to_FP": 1}))
        self.assertIn("does not equal the corrections total 6", e[0])


class BlindSlice(unittest.TestCase):
    def slice(self, **overrides):
        s = {"seed": 7, "reviewed": 20, "disagreed": 1,
             "blind_to_prior_verdict": True, "blind_to_diagnostic": False}
        s.update(overrides)
        return s

    def test_a_blind_slice_is_optional_and_checked_when_present(self):
        self.assertEqual(errors(manifest(recheck(blind_slice=self.slice()))), [])

    def test_a_blind_slice_needs_every_field(self):
        s = self.slice()
        del s["seed"]
        self.assertIn("blind_slice is missing 'seed'",
                      errors(manifest(recheck(blind_slice=s)))[0])

    def test_disagreements_cannot_exceed_the_slice(self):
        e = errors(manifest(recheck(blind_slice=self.slice(disagreed=21))))
        self.assertIn("disagreed exceeds its reviewed", e[0])


if __name__ == "__main__":
    unittest.main()
