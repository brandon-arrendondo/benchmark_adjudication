"""New manifest directory names are held to the internal-reference policy.

Synthetic numbers only (900xx), as in test_reason_references.py.
"""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import batch_name_allowlist
import validate
from reason_references import manifest_name_categories

NUMBER = str(90000 + 1)


class ManifestNameTests(unittest.TestCase):
    def test_grandfathered_name_passes(self):
        name = f"delta-fio40c-task{NUMBER}"
        self.assertTrue(manifest_name_categories(name, frozenset()))
        self.assertEqual(manifest_name_categories(name, frozenset({name})), set())

    def test_new_internal_looking_names_are_refused(self):
        for name in (f"task-{NUMBER}-foo", f"task{NUMBER}", f"task_{NUMBER}",
                     f"run-{NUMBER}", f"run {NUMBER}", f"delta_run_{NUMBER}",
                     f"run{NUMBER}", f"delta_x_bmdb{NUMBER}", f"delta-x-bmdb{NUMBER}",
                     f"bmdb-{NUMBER}", f"aurora_lint-{NUMBER}"):
            with self.subTest(name=name):
                self.assertTrue(manifest_name_categories(name, frozenset()))
        self.assertIn("tracker reference",
                      manifest_name_categories(f"task-{NUMBER}-foo", frozenset()))
        self.assertIn("internal run number",
                      manifest_name_categories(f"run-{NUMBER}", frozenset()))

    def test_host_names_are_refused(self):
        for name in (f"dev-{NUMBER}-recheck", "r9001-pass", f"dev{NUMBER}",
                     "windev-09", "windev09"):
            with self.subTest(name=name):
                self.assertIn("numbered machine", manifest_name_categories(name, frozenset()))

    def test_neutral_new_names_pass(self):
        for name in ("delta-str30c-2026-10", "correction-fio40c-ex1-2026-10",
                     "census-exp34c-sqlite", "delta-devel-2026-10", "dry-run-str11c",
                     "rerun-int32c-2026-10"):
            with self.subTest(name=name):
                self.assertEqual(manifest_name_categories(name, frozenset()), set())

    def test_validate_reports_only_unlisted_internal_names(self):
        names = ["delta-str30c-2026-10", f"task-{NUMBER}-foo", f"run-{NUMBER}"]
        errors = validate.check_batch_names(names, frozenset({f"run-{NUMBER}"}))
        self.assertEqual(len(errors), 1)
        self.assertIn(f"batches/task-{NUMBER}-foo", errors[0])


class AllowlistFileTests(unittest.TestCase):
    # The allowlist is frozen: these pin its exact contents. Growing it lets a
    # new name escape the check, so a change here needs maintainer review;
    # a new batch takes a neutral name instead (README, "Naming a batch").
    FROZEN_COUNT = 679
    FROZEN_SHA256 = "0cac3c86dd81cc383189624aa98aeebf928f71e0a4191d42729140f8d2d56227"

    def test_allowlist_is_frozen(self):
        entries = sorted(batch_name_allowlist.read_allowlist())
        self.assertEqual(len(entries), self.FROZEN_COUNT)
        self.assertEqual(
            hashlib.sha256("\n".join(entries).encode()).hexdigest(), self.FROZEN_SHA256)

    def test_allowlist_matches_the_tree(self):
        self.assertEqual(batch_name_allowlist.check(), [])
        listed = batch_name_allowlist.read_allowlist()
        self.assertTrue(listed)
        self.assertLessEqual(listed, set(batch_name_allowlist.tree_names()))

    def test_every_current_name_passes(self):
        allowlist = batch_name_allowlist.read_allowlist()
        self.assertEqual(
            validate.check_batch_names(batch_name_allowlist.tree_names(), allowlist), [])

    def test_check_reports_stale_and_unsorted_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "batches" / "b-one").mkdir(parents=True)
            (root / "batches" / "b-one" / "manifest.json").write_text("{}")
            path = root / "allowlist.txt"
            path.write_text("# header\nb-two\nb-one\n")
            errors = batch_name_allowlist.check(path, root / "batches")
            self.assertTrue(any("sorted" in e for e in errors))
            self.assertTrue(any("'b-two' has no" in e for e in errors))
            path.write_text("b-one\n")
            self.assertEqual(batch_name_allowlist.check(path, root / "batches"), [])

    def test_missing_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            errors = batch_name_allowlist.check(Path(tmp) / "absent.txt", Path(tmp))
            self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
