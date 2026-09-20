"""scripts/label_churn.py: the label-churn diff between two commits.

Two layers. The synthetic cases feed `churn()` hand-built row maps, one per
change category, including task 1292's INT32-C -> INT30-C re-key and the
tie-break a re-key needs when an unrelated rule was also added at the same
site. The golden cases run the tool over this repository's own history and
pin the figures the paper cites (benchmarking_db 1372):

  3ab3f41d -> f5216b8   ordinary churn, CRLF at both ends
  f5216b8  -> 5d4e70e   the LF normalisation: zero key changes, only bytes
  5d4e70e  -> 1911f5b   additions only
  3ab3f41d -> 1911f5b   the whole span, which must equal the three windows summed
  1911f5b  -> 5f132a2   the ERR33-C strict-bar relabel: 185 FP->TP, one batch

The golden tests need the full history (CI fetches it) and skip when a ref
is not present.

Run:  python3 -m unittest discover -s tests -v
"""
import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import label_churn as lc  # noqa: E402

C = "0" * 40


def key(project, path, line, rule):
    return (project, C, path, line, rule)


class TestChurnSynthetic(unittest.TestCase):
    def test_added_removed_flipped_rekeyed_each_counted_once(self):
        a = {
            key("p", "a.c", 1, "R1-C"): ("TP", "old"),      # unchanged
            key("p", "a.c", 2, "R1-C"): ("FP", "old"),      # flipped FP->TP
            key("p", "a.c", 3, "R1-C"): ("TP", "old"),      # removed
            key("p", "b.c", 9, "INT32-C"): ("FP", "old"),   # re-keyed to INT30-C
            key("p", "c.c", 5, "R2-C"): ("TP", "old"),      # edited reason only: not churn
        }
        b = {
            key("p", "a.c", 1, "R1-C"): ("TP", "old"),
            key("p", "a.c", 2, "R1-C"): ("TP", "fix-batch"),
            key("p", "a.c", 4, "R1-C"): ("FP", "new-batch"),  # added
            key("p", "b.c", 9, "INT30-C"): ("FP", "rekey-batch"),
            key("p", "c.c", 5, "R2-C"): ("TP", "old"),
        }
        change = lc.churn(a, b, {"p a.c:3 R1-C": "cull-batch"})
        self.assertEqual([e["key"] for e in change["added"]], ["p a.c:4 R1-C"])
        self.assertEqual(change["removed"], [{"key": "p a.c:3 R1-C", "verdict": "TP", "project": "p",
                                              "rule": "R1-C", "batch": "cull-batch"}])
        self.assertEqual(change["flipped"], [{"key": "p a.c:2 R1-C", "from": "FP", "to": "TP", "project": "p",
                                              "rule": "R1-C", "batch": "fix-batch"}])
        self.assertEqual(change["rekeyed"], [{"from": "p b.c:9 INT32-C", "to": "p b.c:9 INT30-C",
                                              "rule_from": "INT32-C", "rule_to": "INT30-C", "verdict": "FP",
                                              "batch": "rekey-batch", "project": "p"}])
        s = lc.summarise(change)
        self.assertEqual(s["overall"], {"added": 1, "removed": 1, "rekeyed": 1, "flipped": 1,
                                        "flips": {"FP->TP": 1}})
        self.assertEqual(s["per_rule"]["INT30-C"]["rekeyed"], 1)
        self.assertEqual(s["per_rule"]["INT32-C"]["rekeyed"], 1)
        self.assertEqual(s["per_batch"]["cull-batch"]["removed"], 1)

    def test_rekey_requires_same_verdict(self):
        a = {key("p", "a.c", 1, "INT32-C"): ("TP", "old")}
        b = {key("p", "a.c", 1, "INT30-C"): ("FP", "new")}
        change = lc.churn(a, b)
        self.assertEqual(change["rekeyed"], [])
        self.assertEqual(len(change["added"]), 1)
        self.assertEqual(len(change["removed"]), 1)

    def test_rekey_prefers_the_superseding_batch_then_same_category(self):
        # 1292's shape: INT32-C withdrawn, INT30-C added by the re-keying batch,
        # and an unrelated ERR00-C label added at the same site by another batch.
        a = {key("p", "a.c", 7, "INT32-C"): ("FP", "old")}
        b = {key("p", "a.c", 7, "ERR00-C"): ("FP", "task-578"),
             key("p", "a.c", 7, "INT30-C"): ("FP", "task-1292")}
        change = lc.churn(a, b, {"p a.c:7 INT32-C": "task-1292"})
        self.assertEqual(change["rekeyed"][0]["to"], "p a.c:7 INT30-C")
        self.assertEqual([e["key"] for e in change["added"]], ["p a.c:7 ERR00-C"])
        # with no manifest record the CERT category still decides
        change = lc.churn(a, b)
        self.assertEqual(change["rekeyed"][0]["to"], "p a.c:7 INT30-C")
        # with neither, the lowest rule_id pairs, deterministically
        b2 = {key("p", "a.c", 7, "ERR00-C"): ("FP", "x"), key("p", "a.c", 7, "DCL00-C"): ("FP", "y")}
        self.assertEqual(lc.churn(a, b2)["rekeyed"][0]["to"], "p a.c:7 DCL00-C")

    def test_totals(self):
        rows = {key("p", "a.c", 1, "R"): ("TP", ""), key("p", "a.c", 2, "R"): ("FP", ""),
                key("q", "b.c", 1, "R"): ("FN", ""), key("q", "b.c", 2, "R"): ("uncertain", "")}
        t = lc.totals(rows)
        self.assertEqual((t["rows"], t["TP"], t["FP"], t["FN"], t["uncertain"]), (4, 1, 1, 1, 1))
        self.assertEqual(t["per_project"]["q"], {"rows": 2, "TP": 0, "FP": 0, "FN": 1, "uncertain": 1})

    def test_output_is_deterministic(self):
        a = {key("p", "z.c", 1, "R"): ("TP", ""), key("p", "a.c", 1, "R"): ("TP", "")}
        b = {key("p", "z.c", 2, "R"): ("FP", "b2"), key("p", "a.c", 2, "R"): ("FP", "b1")}
        one = lc.churn(a, b)
        two = lc.churn(dict(reversed(list(a.items()))), dict(reversed(list(b.items()))))
        self.assertEqual(one, two)
        self.assertEqual([e["key"] for e in one["added"]], ["p a.c:2 R", "p z.c:2 R"])


def _have(ref):
    return subprocess.run(["git", "-C", str(REPO_ROOT), "rev-parse", "--verify", f"{ref}^{{commit}}"],
                          capture_output=True).returncode == 0


def _doc(a, b, allow_crlf=True):
    if not (_have(a) and _have(b)):
        raise unittest.SkipTest(f"{a} or {b} not in this clone (shallow?)")
    return lc.build(a, b, allow_crlf=allow_crlf, with_keys=True)


def _flat(doc):
    o = doc["overall"]
    return (o["added"], o["removed"], o["rekeyed"], o["flipped"], o["flips"])


class TestGoldenHistory(unittest.TestCase):
    def test_lf_normalisation_is_zero_churn(self):
        doc = _doc("f5216b8", "5d4e70e")
        self.assertEqual(_flat(doc), (0, 0, 0, 0, {}))
        self.assertEqual(doc["totals"]["a"]["rows"], 171599)
        self.assertEqual(doc["totals"]["a"], doc["totals"]["b"])
        # the only difference between the two refs is terminator bytes
        self.assertGreater(sum(doc["a"]["cr_bytes"].values()), 0)
        self.assertEqual(sum(doc["b"]["cr_bytes"].values()), 0)

    def test_crlf_ref_is_refused_without_the_flag(self):
        if not _have("3ab3f41d"):
            raise unittest.SkipTest("3ab3f41d not in this clone")
        with self.assertRaises(SystemExit):
            lc.rows_at("3ab3f41d", allow_crlf=False)

    def test_first_window(self):
        doc = _doc("3ab3f41d", "f5216b8")
        self.assertEqual(_flat(doc), (2838, 0, 32, 65, {"FP->TP": 61, "TP->FP": 4}))
        rk = doc["keys"]["rekeyed"]
        self.assertEqual({(r["rule_from"], r["rule_to"], r["batch"]) for r in rk},
                         {("INT32-C", "INT30-C", "task-1292-int30c-int32c-delta-b1")})
        self.assertEqual(doc["per_batch"]["task-1281-err33c-fclose-gavel-review"]["flips"], {"FP->TP": 57})

    def test_second_window(self):
        doc = _doc("5d4e70e", "1911f5b")
        self.assertEqual(_flat(doc), (591, 0, 0, 0, {}))
        self.assertEqual(doc["totals"]["b"], {**doc["totals"]["b"], "rows": 172190, "TP": 64341, "FP": 107590})

    def test_whole_span_equals_the_windows_summed(self):
        doc = _doc("3ab3f41d", "1911f5b")
        self.assertEqual(_flat(doc), (2838 + 591, 0, 32, 65, {"FP->TP": 61, "TP->FP": 4}))
        self.assertEqual((doc["totals"]["a"]["rows"], doc["totals"]["b"]["rows"]), (168761, 172190))

    def test_err33c_strict_bar_relabel(self):
        doc = _doc("1911f5b", "5f132a2", allow_crlf=False)
        self.assertEqual(_flat(doc), (0, 0, 0, 185, {"FP->TP": 185}))
        self.assertEqual(list(doc["per_batch"]), ["task-1352-err33c-strict-bar"])
        self.assertEqual({f["rule"] for f in doc["keys"]["flipped"]}, {"ERR33-C"})
        self.assertEqual(doc["per_project"]["raylib"]["flipped"], 54)

    def test_human_table_runs(self):
        if not (_have("1911f5b") and _have("5f132a2")):
            raise unittest.SkipTest("refs not in this clone")
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(lc.main(["1911f5b", "5f132a2"]), 0)
        self.assertIn("flipped 185", out.getvalue())
        self.assertIn("task-1352-err33c-strict-bar", out.getvalue())


if __name__ == "__main__":
    unittest.main()
