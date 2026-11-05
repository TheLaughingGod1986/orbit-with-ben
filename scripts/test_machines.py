#!/usr/bin/env python3
"""Tests for scripts/machines.py: the home page's per-machine card (Ben, 4 Nov 2026)."""
import datetime as dt
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import machines as m  # noqa: E402

AT = dt.datetime(2026, 11, 4, 23, 0, tzinfo=dt.timezone.utc)


def done(i, by, at):
    return {"id": i, "status": "done", "title": i, "history": [{"at": "2026-11-01T00:00Z", "by": "claude", "what": "added"},
                                                              {"at": at, "by": by, "what": "done: ok"}]}


class Machines(unittest.TestCase):
    def test_claimed_jobs_land_on_their_machine(self):
        q = {"jobs": [{"id": "J1", "status": "claimed", "by": "codex", "title": "a"},
                      {"id": "J2", "status": "claimed", "by": "gemini", "title": "b"},
                      {"id": "J3", "status": "claimed", "by": "macbook", "title": "c"},
                      {"id": "J4", "status": "open", "by": "", "title": "d"}]}
        s = {r["id"]: r for r in m.section(q, None, None, AT)["machines"]}
        self.assertEqual([n["id"] for n in s["mini"]["now"]], ["J1", "J2"])
        self.assertEqual([n["id"] for n in s["macbook"]["now"]], ["J3"])

    def test_done_in_24h_counted_per_machine_and_agent(self):
        q = {"jobs": [done("J1", "codex", "2026-11-04T20:00Z"), done("J2", "gemini", "2026-11-04T01:00Z"),
                      done("J3", "macbook", "2026-11-04T22:00Z"), done("J4", "codex", "2026-11-03T20:00Z"),
                      done("J5", "claude", "2026-11-04T22:30Z")]}
        sec = m.section(q, None, None, AT)
        s = {r["id"]: r for r in sec["machines"]}
        self.assertEqual((s["mini"]["done24"], s["mini"]["byAgent"]), (2, {"codex": 1, "gemini": 1}))
        self.assertEqual(s["macbook"]["done24"], 1)
        self.assertEqual(s["cloud"]["done24"], 1)
        self.assertEqual(sec["doneTotal"], 4)
        self.assertNotIn("grok", s)

    def test_heartbeats_say_why_a_machine_is_idle(self):
        sec = m.section({"jobs": []}, {"at": "2026-11-04T22:55:00Z", "state": "running", "note": "woke Gemini for J2148"},
                        {"at": "2026-11-04T22:52:00Z", "state": "waiting", "why": ["in use (0 min idle, needs 10)"],
                         "job": "", "agents": ["codex", "claude"]}, AT)
        s = {r["id"]: r for r in sec["machines"]}
        self.assertIn("J2148", s["mini"]["why"])
        self.assertEqual(s["macbook"]["state"], "waiting")
        self.assertIn("in use", s["macbook"]["why"])
        self.assertEqual(s["macbook"]["agents"], ["codex", "claude"])

    def test_macbook_heartbeat_job_shows_even_before_the_queue_catches_up(self):
        q = {"jobs": [{"id": "J9", "status": "open", "title": "test"}]}
        s = {r["id"]: r for r in m.section(q, None, {"state": "working", "job": "J9", "why": []}, AT)["machines"]}
        self.assertEqual(s["macbook"]["now"][0]["id"], "J9")

    def test_relay_execution_and_fresh_heartbeat_show_the_minis_job(self):
        q = {"jobs": [{"id": "J7", "status": "open", "title": "picture"}, {"id": "J8", "status": "open", "title": "review"}]}
        hb = {"at": "2026-11-04T22:50:00Z", "state": "running", "note": "woke Gemini for J8 (cap 25 min)"}
        s = {r["id"]: r for r in m.section(q, hb, None, AT, [{"job": "J7", "worker": "codex", "startedAt": "x"}])["machines"]}
        self.assertEqual([(n["id"], n["agent"]) for n in s["mini"]["now"]], [("J7", "codex"), ("J8", "gemini")])
        self.assertEqual(s["mini"]["now"][0]["title"], "picture")

    def test_old_woke_heartbeat_is_not_a_current_job(self):
        hb = {"at": "2026-11-04T22:00:00Z", "state": "running", "note": "woke Gemini for J8 (cap 25 min)"}
        s = {r["id"]: r for r in m.section({"jobs": []}, hb, None, AT)["machines"]}
        self.assertEqual(s["mini"]["now"], [])

    def test_cloud_and_grok_last_seen_come_from_the_queue_history(self):
        q = {"jobs": [done("J1", "claude", "2026-11-04T22:30Z"), done("J2", "chief", "2026-11-04T21:00Z")]}
        s = {r["id"]: r for r in m.section(q, None, None, AT)["machines"]}
        self.assertEqual((s["cloud"]["seen"], s["grok"]["seen"]), ("2026-11-04T22:30Z", "2026-11-04T21:00Z"))

    def test_unknown_agents_are_ignored(self):
        q = {"jobs": [{"id": "J1", "status": "claimed", "by": "someone", "title": "x"}]}
        self.assertTrue(all(not r["now"] for r in m.section(q, None, None, AT)["machines"]))


if __name__ == "__main__":
    unittest.main()
