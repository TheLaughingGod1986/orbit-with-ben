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

    def test_a_file_only_one_machine_can_open_is_refused_and_nothing_is_queued(self):
        """9 Nov 2026: the weekly panel named drafts in the MacBook's home folder; the critics run on the Mini and in
        the cloud, and it sat for 32 hours without a critique."""
        for bad in ("/Users/someone/_desk/j2374/designs/B_v01.jpg", "~/_desk/B_v01.jpg", "/home/someone/B.jpg", "/tmp/B.jpg"):
            data = {"next_id": 1, "jobs": []}
            with self.assertRaises(ValueError) as cm:
                packaging_panel.queue(data, "weekly drafts", ["a.json", bad], "owb-weekly", at=T0)
            self.assertIn(bad, str(cm.exception))
            self.assertNotIn("a.json", str(cm.exception))
            self.assertEqual(data, {"next_id": 1, "jobs": []})

    def test_repo_paths_and_the_shared_drive_are_fine(self):
        files = ["05_Analytics/weekly_thumb_audit/x/B_v01.jpg", "/Volumes/data/studio-live/UAT/B_v01.jpg"]
        self.assertEqual(packaging_panel.unreachable(files), [])
        data = {"next_id": 1, "jobs": []}
        js = packaging_panel.queue(data, "weekly drafts", files, "owb-weekly", at=T0)
        self.assertEqual(len(js), 4)
        self.assertIn("/Volumes/data/studio-live/UAT/B_v01.jpg", js[0]["body"])

    def test_the_command_says_so_and_exits_1_before_touching_the_queue(self):
        import contextlib
        import io
        from unittest import mock
        out = io.StringIO()
        with mock.patch.object(packaging_panel.jobs, "with_git", side_effect=AssertionError("queue touched")), \
                mock.patch.object(packaging_panel.jobs, "load", side_effect=AssertionError("queue read")), \
                contextlib.redirect_stdout(out):
            rc = packaging_panel.main(["--slug", "owb-weekly", "--what", "weekly drafts", "--git",
                                       "--files", "/Users/someone/_desk/B_v01.jpg"])
        self.assertEqual(rc, 1)
        self.assertIn("not queued", out.getvalue())
        self.assertIn("/Users/someone/_desk/B_v01.jpg", out.getvalue())


if __name__ == "__main__":
    unittest.main()
