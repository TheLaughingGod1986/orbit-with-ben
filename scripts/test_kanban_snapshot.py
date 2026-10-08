#!/usr/bin/env python3
"""Tests for kanban_snapshot.py: stage 'since' times and the film notes (board/briefs)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kanban_snapshot as ks  # noqa: E402


class Since(unittest.TestCase):
    snaps = [("2026-10-05T10:00:00Z", {"picture": "todo", "edit": "todo"}),
             ("2026-10-06T10:00:00Z", {"picture": "doing", "edit": "todo"}),
             ("2026-10-07T10:00:00Z", {"picture": "doing", "edit": "todo"}),
             ("2026-10-08T10:00:00Z", {"picture": "done", "edit": "review"})]

    def test_since_is_when_the_current_state_began(self):
        s = ks.since_from_history(self.snaps[:3], truncated=False)
        self.assertEqual(s["picture"], "2026-10-06T10:00:00Z")  # not the 7 Oct commit that left it unchanged
        self.assertEqual(ks.since_from_history(self.snaps, truncated=False)["edit"], "2026-10-08T10:00:00Z")

    def test_cut_short_history_gives_no_time_for_a_state_older_than_it(self):
        s = ks.since_from_history(self.snaps[:3], truncated=True)
        self.assertNotIn("edit", s)  # 'todo' since before the oldest commit we can see
        self.assertEqual(s["picture"], "2026-10-06T10:00:00Z")
        self.assertEqual(ks.since_from_history([], truncated=True), {})


class MiniWork(unittest.TestCase):
    def test_claim_to_release_is_work_and_overnight_is_capped(self):
        jobs = [{"id": "J1", "needs": "mini", "film": "025", "history": [
                    {"at": "2026-10-08T10:00Z", "by": "claude", "what": "added"},
                    {"at": "2026-10-08T10:10Z", "by": "cursor", "what": "claimed"},
                    {"at": "2026-10-08T10:40Z", "by": "cursor", "what": "released: step 1"},
                    {"at": "2026-10-08T11:00Z", "by": "cursor", "what": "claimed"},
                    {"at": "2026-10-08T11:15Z", "by": "cursor", "what": "done: ok"}]},
                {"id": "J2", "needs": "mini", "history": [
                    {"at": "2026-10-07T20:00Z", "by": "cursor", "what": "claimed"},
                    {"at": "2026-10-08T09:00Z", "by": "cursor", "what": "done: ok"}]},
                {"id": "J3", "needs": "cloud", "history": [
                    {"at": "2026-10-08T10:00Z", "by": "claude", "what": "claimed"},
                    {"at": "2026-10-08T11:00Z", "by": "claude", "what": "done: ok"}]}]
        w = ks.mini_work(jobs, "2026-10-08")
        self.assertEqual(w["byFilm"], {"OWB:025": 45, "admin": 480})  # J2's 13 h claim counts as 8 h
        self.assertEqual((w["jobs"], w["minutes"]), (2, 525))
        self.assertNotIn("claude", w["byAgent"])


class Briefs(unittest.TestCase):
    def test_real_file_loads_and_every_step_says_when(self):
        films = ks.load_briefs()
        self.assertTrue(films)
        for key, b in films.items():
            for k in ("updated", "mood", "line", "done", "holdup", "steps"):
                self.assertIn(k, b, key)
            self.assertIn(b["mood"], ("good", "waiting", "held", "finished", "watched", "ready"), key)
            for st in b["steps"]:
                self.assertTrue(st.get("who") and st.get("what"), key)
                self.assertTrue(st.get("done") or st.get("job") or st.get("afterJob") or st.get("when") or st.get("whenText"), f"{key}: {st}")

    def test_bad_key_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "b.json"
            p.write_text(json.dumps({"films": {"022": {}}}))
            old, ks.BRIEFS = ks.BRIEFS, p
            try:
                with self.assertRaises(SystemExit):
                    ks.load_briefs()
            finally:
                ks.BRIEFS = old


if __name__ == "__main__":
    unittest.main()
