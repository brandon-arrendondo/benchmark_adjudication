"""Tests for scripts/eval_scope_table.py, the evaluated-scope table.

Run269EvalScope is the golden: at the pinned corpus checkouts, with run 269's
findings and the labels at e7d70148, every row and the totals equal the
v0.5.2 paper's table (tests/golden/run-269/expected_eval_scope.json). The
Files/SLOC columns need the twelve codebase checkouts at their pins under
$SQC_BENCH_ROOT (default ~/toolchain), which CI does not have, so the golden
is skipped when any is absent. The small cases below run everywhere.

Run:  python3 -m unittest discover -s tests -v
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN = REPO_ROOT / "tests" / "golden" / "run-269"
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import eval_scope_table as est  # noqa: E402
import score  # noqa: E402
from test_score_golden import _labels_available, _scope_json  # noqa: E402

BENCH_ROOT = Path(os.environ.get("SQC_BENCH_ROOT", "~/toolchain")).expanduser()


class Run269EvalScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        exp = json.loads((GOLDEN / "expected.json").read_text())
        cls.want = json.loads((GOLDEN / "expected_eval_scope.json").read_text())
        missing = [r["project"] for r in cls.want["rows"]
                   if not (BENCH_ROOT / r["project"]).is_dir()]
        if missing:
            raise unittest.SkipTest(f"no pinned checkout under {BENCH_ROOT} for {missing}")
        if not _labels_available(exp["benchmark_adjudication_commit"]):
            raise AssertionError("labels commit not in this clone; fetch full history")
        cls.tmp = tempfile.TemporaryDirectory()
        scope_path = Path(cls.tmp.name) / "benchmark_repos.json"
        scope_path.write_text(_scope_json(exp["aurora_lint_commit"]))
        scope = score.load_scope(scope_path)
        findings = score.load_findings_csv(GOLDEN / "findings.csv.gz")
        commits = {p: scope[p]["commit"] for p in findings}
        labels, _ = score.load_labels(sorted(findings), None,
                                      exp["benchmark_adjudication_commit"])
        scored = score.score(findings, labels, scope, commits)["per_project"]
        cls.got = est.table(scope, BENCH_ROOT, scored)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_row_is_the_papers(self):
        got = {r["project"]: r for r in self.got["rows"]}
        for want in self.want["rows"]:
            with self.subTest(project=want["project"]):
                self.assertEqual(got[want["project"]], want)

    def test_totals_are_the_papers(self):
        self.assertEqual(self.got["total"], self.want["total"])


class Definitions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name) / "p"
        (root / "lib").mkdir(parents=True)
        (root / "lib" / "win").mkdir()
        (root / "test").mkdir()
        (root / "lib" / "a.c").write_text(
            "/* a block\n   comment */\nint x;\n\n// line comment\nint y; // trailing\n")
        (root / "lib" / "a.h").write_text("int z;\n")
        (root / "lib" / "notes.txt").write_text("int ignored;\n")
        (root / "lib" / "win" / "w.c").write_text("int w;\n")
        (root / "test" / "t.c").write_text("int t;\n")
        self.root = root

    def tearDown(self):
        self.tmp.cleanup()

    def test_sloc_drops_comments_and_blank_lines(self):
        self.assertEqual(est.sloc(self.root / "lib" / "a.c"), 2)

    def test_scope_counts_only_declared_c_and_h(self):
        """Include lib/**, exclude lib/win/**: a.c and a.h count; w.c is
        excluded, test/ is outside the include, notes.txt is not C."""
        self.assertEqual(est.count_project(self.root, ["lib/**"], ["lib/win/**"]), (2, 3))

    def test_no_include_means_the_whole_project(self):
        self.assertEqual(est.count_project(self.root, None, None), (4, 5))

    def test_status_thresholds(self):
        self.assertEqual([est.status(c) for c in (None, 49.9, 50, 89.9, 90)],
                         ["unscored", "in progress", "partial", "partial", "exhaustive"])

    def test_size_columns_alone_without_a_run(self):
        scope = {"p": {"commit": "c" * 40, "include": ["lib/**"], "exclude": None}}
        doc = est.table(scope, Path(self.tmp.name), None)
        self.assertEqual(doc["rows"][0]["files"], 3)
        self.assertIsNone(doc["rows"][0]["findings"])
        self.assertIsNone(doc["rows"][0]["status"])
        self.assertNotIn("findings", doc["total"])


if __name__ == "__main__":
    unittest.main()
