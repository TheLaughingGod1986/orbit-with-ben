"""Thumbnail ledger + packaging panel (Ben, 14 Oct 2026)."""
import datetime as dt, pathlib, sys, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import packaging_panel  # noqa: E402
import thumb_ledger as tl  # noqa: E402

T0 = dt.datetime(2026, 10, 14, 21, 0, tzinfo=dt.timezone.utc)


def ledger(results):
    d = {"tests": []}
    for i, (a, b, wa, wb) in enumerate(results):
        t = tl.add(d, video=f"v{i}", channel="owb", a_maker=a, b_maker=b)
        tl.result(d, t["id"], wt_a=wa, wt_b=wb)
    return d


class Ledger(unittest.TestCase):
    def test_winner_needs_a_clear_margin(self):
        self.assertEqual(tl.winner_of({"wt_a": 40, "wt_b": 60}), "b")
        self.assertEqual(tl.winner_of({"wt_a": 49, "wt_b": 51}), "draw")
        self.assertEqual(tl.winner_of({"wt_a": 49, "wt_b": 51, "winner": "b"}), "b")   # Studio's own call wins

    def test_codex_earns_the_default_only_with_enough_wins(self):
        self.assertIsNone(tl.verdict(ledger([("house", "codex", 40, 60)] * 3))[0])          # only 3 tests
        self.assertEqual(tl.verdict(ledger([("house", "codex", 40, 60)] * 4))[0], "codex")
        self.assertIsNone(tl.verdict(ledger([("house", "codex", 40, 60)] * 2 + [("house", "codex", 60, 40)] * 2))[0])

    def test_draws_dont_count_as_decided(self):
        d = ledger([("house", "codex", 50, 51)] * 5)
        self.assertEqual(tl.tally(d)["codex"], {"tests": 0, "wins": 0, "draws": 5})
        self.assertIsNone(tl.verdict(d)[0])

    def test_the_seeded_ledger_parses(self):
        d = tl.load()
        self.assertTrue(all(t["b"]["maker"] for t in d["tests"]))


class Panel(unittest.TestCase):
    def test_three_independent_critics_then_claude_decides(self):
        data = {"next_id": 1, "jobs": []}
        js = packaging_panel.queue(data, "024 package", ["a.json"], "owb-024", at=T0)
        self.assertEqual([j.get("for") for j in js[:3]], ["codex", "gemini", "cursor"])
        self.assertTrue(all(j["needs"] == "mini" and "owb-024/" in j["body"] for j in js[:3]))
        self.assertIn("Don't read the other critics", js[0]["body"])
        self.assertEqual(js[3]["needs"], "cloud")
        self.assertEqual(js[3]["after"], js[2]["id"])
        self.assertIn("DECISION.md", js[3]["body"])


if __name__ == "__main__":
    unittest.main()
