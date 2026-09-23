"""Golden test: scripts/score.py reproduces the paper's figures exactly.

Two pinned runs: #265 (the v0.5.0 baseline, described below) and #269 (the
v0.5.2 baseline, tests/golden/run-269, same three inputs at its own SHAs --
see that directory's expected.json).

This is the correctness gate for the reference scorer (benchmarking_db task
1331, aurora-lint ADR-0004: one definition, no second thing that can
disagree). The published numbers for the v0.5.0 baseline were computed by
benchmarking_db's private scorer against Postgres; this test feeds the same
three inputs to the public scorer and asserts every per-project and overall
figure is identical -- not close, identical.

Inputs, all pinned:
  findings  tests/golden/run-265/findings.csv.gz -- run 265's distinct
            (project, file, line, rule) keys, exported from sqc_bench.
  labels    data/*/adjudication.csv at benchmark_adjudication 3ab3f41d, read
            through `git show` (so a shallow clone cannot run this: CI fetches
            full history).
  scope     aurora-lint data/benchmark_repos.json at f48effe3, the commit
            that produced the run. Read from a local checkout when
            AURORA_LINT_DIR names one, else fetched from GitHub; the file is
            never copied into this repo (bmdb 739: no third declaration).

Set BENCHMARK_ADJUDICATION_OFFLINE=1 to skip the fetch-dependent test when
working without network and without a checkout.

Run:  python3 -m unittest discover -s tests -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN = REPO_ROOT / "tests" / "golden" / "run-265"
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import score  # noqa: E402

AURORA_LINT_RAW = ("https://raw.githubusercontent.com/brandon-arrendondo/"
                   "aurora-lint/{sha}/data/benchmark_repos.json")


def _scope_json(sha: str) -> str:
    """benchmark_repos.json at `sha` of aurora-lint, as text."""
    local = os.environ.get("AURORA_LINT_DIR")
    if local:
        proc = subprocess.run(
            ["git", "-C", local, "show", f"{sha}:data/benchmark_repos.json"],
            capture_output=True, text=True)
        if proc.returncode == 0:
            return proc.stdout
        raise RuntimeError(f"AURORA_LINT_DIR={local}: cannot git show "
                           f"{sha}:data/benchmark_repos.json ({proc.stderr.strip()})")
    if os.environ.get("BENCHMARK_ADJUDICATION_OFFLINE"):
        raise unittest.SkipTest("offline and no AURORA_LINT_DIR: cannot read "
                                "the pinned scope declaration")
    with urllib.request.urlopen(AURORA_LINT_RAW.format(sha=sha), timeout=60) as r:
        return r.read().decode("utf-8")


def _labels_available(sha: str) -> bool:
    return subprocess.run(["git", "-C", str(REPO_ROOT), "cat-file", "-e",
                           f"{sha}^{{commit}}"], capture_output=True).returncode == 0


class _GoldenRun:
    """One pinned run's golden. A subclass names its directory under
    tests/golden/; the three inputs and the expected figures all come from
    that directory's expected.json, so adding a run adds no test code."""

    golden: Path

    @classmethod
    def setUpClass(cls):
        cls.expected = json.loads((cls.golden / "expected.json").read_text())
        labels_sha = cls.expected["benchmark_adjudication_commit"]
        if not _labels_available(labels_sha):
            raise AssertionError(
                f"benchmark_adjudication {labels_sha} is not in this clone's "
                f"history (shallow fetch?). The golden test scores the labels "
                f"at that commit; fetch full history.")
        scope_text = _scope_json(cls.expected["aurora_lint_commit"])
        cls.tmp = tempfile.TemporaryDirectory()
        scope_path = Path(cls.tmp.name) / "benchmark_repos.json"
        scope_path.write_text(scope_text)
        scope = score.load_scope(scope_path)
        findings = score.load_findings_csv(cls.golden / "findings.csv.gz")
        commits = {p: scope[p]["commit"] for p in findings}
        labels, n_labels = score.load_labels(sorted(findings), None, labels_sha)
        cls.n_labels = n_labels
        cls.got = score.score(findings, labels, scope, commits)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_label_set_is_the_oracle_the_paper_cites(self):
        """The label count at benchmark_adjudication_commit is the one
        release_baseline_numbers reported for the oracle it scored against
        (168,761 at 3ab3f41d for run 265; 172,189 at e7d70148 for run 269)."""
        self.assertEqual(self.n_labels, self.expected["oracle_labels_total"])

    def test_definition_version_and_basis(self):
        self.assertEqual(self.got["definition_version"],
                         self.expected["definition_version"])
        self.assertEqual(self.got["basis"], self.expected["basis"])

    def test_overall_figures_are_identical(self):
        self.assertEqual(self.got["overall"], self.expected["overall"])

    def test_every_project_is_identical(self):
        exp = self.expected["per_project"]
        self.assertEqual(sorted(self.got["per_project"]), sorted(exp))
        for project, want in exp.items():
            with self.subTest(project=project):
                have = dict(self.got["per_project"][project])
                # release_baseline_numbers abbreviates the commit for display;
                # score.py carries the full SHA the labels are keyed on.
                have["commit"] = have["commit"][:len(want["commit"])]
                self.assertEqual(have, want)


class Run265Golden(_GoldenRun, unittest.TestCase):
    """v0.5.0 paper baseline: aurora-lint f48effe3, labels 3ab3f41d."""
    golden = GOLDEN


class Run269Golden(_GoldenRun, unittest.TestCase):
    """v0.5.2 paper baseline: aurora-lint 92eae76c (the v0.5.2 tag), labels
    e7d70148."""
    golden = REPO_ROOT / "tests" / "golden" / "run-269"


class ScorerDefinitions(unittest.TestCase):
    """Small, hand-checkable cases for each definition score.py implements."""

    SCOPE = {"p": {"commit": "c" * 40, "include": ["lib/**"], "exclude": ["lib/win.c"]}}

    def _score(self, findings, labels):
        return score.score({"p": findings}, {"p": labels}, self.SCOPE,
                           {"p": "c" * 40})

    def test_fn_that_the_run_emits_is_a_detection_and_a_true_positive(self):
        """REAL_BUG_VERDICTS is {TP, FN}, not {TP}: a matched FN was a real
        bug the scanner used to miss and now catches."""
        got = self._score({("lib/a.c", 1, "R")},
                          [("c" * 40, "lib/a.c", 1, "R", "FN")])
        p = got["per_project"]["p"]
        self.assertEqual((p["labeled_tp"], p["tp_detected"], p["tp_labels"]), (1, 1, 1))
        self.assertEqual(p["precision_pct"], 100.0)
        self.assertEqual(p["recall_pct"], 100.0)

    def test_scope_applies_to_labels_as_well_as_findings(self):
        """An out-of-scope real-bug label leaves the recall denominator; an
        out-of-scope finding is not counted at all."""
        got = self._score({("lib/a.c", 1, "R"), ("src/x.c", 1, "R"), ("lib/win.c", 1, "R")},
                          [("c" * 40, "lib/a.c", 1, "R", "TP"),
                           ("c" * 40, "src/x.c", 1, "R", "TP"),
                           ("c" * 40, "lib/win.c", 1, "R", "FP")])
        p = got["per_project"]["p"]
        self.assertEqual(p["run_findings"], 1)
        self.assertEqual((p["tp_labels"], p["tp_detected"], p["labeled_fp"]), (1, 1, 0))
        self.assertEqual(p["label_coverage_pct"], 100.0)

    def test_uncertain_counts_toward_coverage_only(self):
        got = self._score({("lib/a.c", 1, "R"), ("lib/a.c", 2, "R")},
                          [("c" * 40, "lib/a.c", 1, "R", "uncertain")])
        p = got["per_project"]["p"]
        self.assertEqual(p["labeled_total"], 1)
        self.assertIsNone(p["precision_pct"])
        self.assertEqual(p["label_coverage_pct"], 50.0)

    def test_labels_at_another_commit_do_not_score_the_project(self):
        got = self._score({("lib/a.c", 1, "R")},
                          [("d" * 40, "lib/a.c", 1, "R", "TP")])
        self.assertFalse(got["per_project"]["p"]["scored"])
        self.assertEqual(got["overall"]["run_findings"], 0)

    def test_an_undeclared_project_is_refused(self):
        with self.assertRaises(SystemExit):
            score.score({"q": {("a.c", 1, "R")}}, {"q": []}, self.SCOPE, {"q": "c" * 40})

    def test_export_paths_normalize_through_the_first_project_segment(self):
        self.assertEqual(
            score.project_relpath("mosquitto",
                                  "/home/x/toolchain/mosquitto/include/mosquitto/broker.h"),
            "include/mosquitto/broker.h")
        self.assertEqual(score.project_relpath("curl", "lib/doh.c"), "lib/doh.c")

    def test_an_export_file_yields_the_same_keys_as_the_relative_csv(self):
        """The --export path (absolute as-scanned paths, normalized) and the
        --findings-csv path (relative keys, verbatim) must agree -- checked on
        mosquitto, whose include/mosquitto/ directory is the case a second
        normalization would corrupt."""
        csv_keys = score.load_findings_csv(GOLDEN / "findings.csv.gz")["mosquitto"]
        export = [{"rule_id": r, "file": f"/home/tester/toolchain/mosquitto/{f}",
                   "line": l, "column": 1, "severity": "warning", "message": "",
                   "suggestion": None, "requires_manual_review": False}
                  for f, l, r in csv_keys]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(export, fh)
        try:
            self.assertEqual(score.load_findings_export("mosquitto", Path(fh.name)),
                             csv_keys)
        finally:
            os.unlink(fh.name)

    def test_globs_are_path_aware(self):
        self.assertTrue(score.in_scope("src/a.c", ["src/*.c"], None))
        self.assertFalse(score.in_scope("src/external/glfw/a.c", ["src/*.c"], None))
        self.assertTrue(score.in_scope("src/external/glfw/a.c", ["src/**"], None))
        self.assertTrue(score.in_scope("anything/at/all.c", None, None))


if __name__ == "__main__":
    unittest.main()
