"""Tests for scripts/precision_ci.py, the public interval estimates.

Run269Intervals is the golden: fed run 269's pinned inputs (the same three
test_score_golden.Run269Golden uses) and --order en_US.UTF-8, the script
reproduces the interval block the v0.5.2 paper was typeset from --
every field, not close. That order is the one benchmarking_db's Postgres
produced, so the test is skipped on a machine without the locale.

The rest are small hand-checkable cases for each definition.

Run:  python3 -m unittest discover -s tests -v
"""
import json
import locale
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN = REPO_ROOT / "tests" / "golden" / "run-269"
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import precision_ci as pc  # noqa: E402
import score  # noqa: E402
from test_score_golden import _labels_available, _scope_json  # noqa: E402


def _has_locale(name):
    try:
        old = locale.setlocale(locale.LC_COLLATE)
        locale.setlocale(locale.LC_COLLATE, name)
        locale.setlocale(locale.LC_COLLATE, old)
        return True
    except locale.Error:
        return False


class Run269Intervals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        exp = json.loads((GOLDEN / "expected.json").read_text())
        cls.want = json.loads((GOLDEN / "expected_intervals.json").read_text())
        if not _labels_available(exp["benchmark_adjudication_commit"]):
            raise AssertionError("labels commit not in this clone; fetch full history")
        cls.tmp = tempfile.TemporaryDirectory()
        scope_path = Path(cls.tmp.name) / "benchmark_repos.json"
        scope_path.write_text(_scope_json(exp["aurora_lint_commit"]))
        cls.scope = score.load_scope(scope_path)
        cls.findings = score.load_findings_csv(GOLDEN / "findings.csv.gz")
        cls.commits = {p: cls.scope[p]["commit"] for p in cls.findings}
        cls.labels, _ = score.load_labels(sorted(cls.findings), None,
                                          exp["benchmark_adjudication_commit"])

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def _run(self, order):
        return pc.interval_figures(self.findings, self.labels, self.scope,
                                   self.commits, order=order)

    @unittest.skipUnless(_has_locale("en_US.UTF-8"), "en_US.UTF-8 not installed")
    def test_published_intervals_are_reproduced_exactly(self):
        got = self._run("en_US.UTF-8")
        for key, want in self.want.items():
            if key in ("_note", "run_id"):
                continue
            with self.subTest(field=key):
                self.assertEqual(got[key], want)

    def test_canonical_order_is_deterministic_and_order_matters(self):
        """Canonical order gives the same result twice; its point estimates
        equal the published ones (order cannot move a point estimate), while
        at least one bootstrap endpoint differs -- which is why the order is
        part of the definition, not an implementation detail."""
        a, b = self._run("canonical"), self._run("canonical")
        self.assertEqual(a, b)
        self.assertEqual(a["headline_pooled"]["precision_pct"],
                         self.want["headline_pooled"]["precision_pct"])
        self.assertEqual(a["per_project"], self.want["per_project"])
        self.assertNotEqual(a["headline_pooled"]["bootstrap_by_file"],
                            self.want["headline_pooled"]["bootstrap_by_file"])

    def test_point_estimate_agrees_with_score_py(self):
        got = self._run("canonical")
        overall = score.score(self.findings, self.labels, self.scope,
                              self.commits)["overall"]
        self.assertEqual(got["headline_pooled"]["precision_pct"], overall["precision_pct"])
        self.assertEqual(got["labeled_tp"], overall["labeled_tp"])
        self.assertEqual(got["findings_total"], overall["run_findings"])


class Definitions(unittest.TestCase):
    def test_wilson_is_not_degenerate_at_the_ends(self):
        lo, hi = pc.wilson(4, 4)
        self.assertLess(lo, 100.0)
        self.assertEqual(round(hi, 6), 100.0)
        lo, hi = pc.wilson(0, 4)
        self.assertEqual(lo, 0.0)
        self.assertGreater(hi, 0.0)
        self.assertIsNone(pc.wilson(0, 0))

    def test_wilson_known_value(self):
        """50/100 at 95%: the textbook 40.4-59.6."""
        lo, hi = pc.wilson(50, 100)
        self.assertEqual((round(lo, 1), round(hi, 1)), (40.4, 59.6))

    def test_clusters_collapse_to_their_counts(self):
        units = [("p", "a.c", "R", "TP"), ("p", "a.c", "R", "FP"),
                 ("p", "b.c", "R", "FN"), ("p", "b.c", "R", "uncertain")]
        self.assertEqual(pc._cluster_tallies(units, "file"),
                         [("p", 1, 1), ("p", 1, 0)])
        self.assertEqual(pc._cluster_tallies(units, "project"), [("p", 2, 1)])

    def test_macro_average_weights_projects_equally(self):
        units = [("big", "a.c", "R", "TP")] * 9 + [("big", "a.c", "R", "FP")] \
            + [("small", "b.c", "R", "FP")]
        self.assertAlmostEqual(pc.macro_average_pct(units), (90.0 + 0.0) / 2)

    def test_same_seed_same_interval(self):
        units = [("p", f"{i}.c", "R", "TP" if i % 3 else "FP") for i in range(60)]
        a = pc.bootstrap_ci(units, pc.pooled_from_tallies, resamples=200)
        b = pc.bootstrap_ci(units, pc.pooled_from_tallies, resamples=200)
        self.assertEqual(a, b)
        self.assertFalse(a["degenerate"])

    def test_nothing_scored_is_degenerate_not_zero(self):
        got = pc.bootstrap_ci([("p", "a.c", "R", "uncertain")], pc.pooled_from_tallies)
        self.assertTrue(got["degenerate"])
        self.assertIsNone(got["lo_pct"])


if __name__ == "__main__":
    unittest.main()
