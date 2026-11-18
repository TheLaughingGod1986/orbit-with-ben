#!/usr/bin/env python3
"""Tests for scripts/queue_eta.py: who each queued job waits for, its place in line and when it starts (Ben, 5 Nov)."""
import datetime as dt
import pathlib
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jobs  # noqa: E402
import queue_eta as q  # noqa: E402

AT = dt.datetime(2026, 11, 5, 10, 0, tzinfo=dt.timezone.utc)
MINI = {"chain": [{"agent": "codex", "up": True}, {"agent": "gemini", "up": True},
                  {"agent": "cursor", "up": False, "why": "out of usage"}]}
BOOK = {"at": "2026-11-05T09:55:00Z"}


def queue(*specs):
    d = {"next_id": 1, "jobs": []}
    for needs, title, kw in specs:
        jobs.do_add(d, title=title, needs=needs, body="", by="claude", at=AT - dt.timedelta(hours=1), **kw)
    return d


def run(d, mini=MINI, book=BOOK):
    with patch.object(jobs.chief_relay, "worker_capabilities", return_value={}), \
            patch.object(jobs.chief_relay, "current_execution", return_value=None), \
            patch.object(jobs, "ordered", side_effect=lambda data, at=None: list(data["jobs"])), \
            patch.object(q, "_flags", return_value={}):
        return q.section(d, mini, book, AT)


class Forecast(unittest.TestCase):
    def test_jobs_spread_over_free_agents_in_queue_order(self):
        d = queue(*[("mini", f"job {i}", {}) for i in range(4)])
        s = run(d)
        f = s["jobs"]
        self.assertEqual({f["J0001"]["agent"], f["J0002"]["agent"]}, {"codex", "gemini"})
        self.assertEqual([f[i]["pos"] for i in ("J0001", "J0002", "J0003", "J0004")], [1, 1, 2, 2])
        self.assertEqual(f["J0001"]["startAt"], "2026-11-05T10:00Z")
        self.assertEqual(f["J0003"]["startAt"], "2026-11-05T10:45Z")  # default 45 min a job

    def test_a_busy_agent_is_free_when_its_job_should_end(self):
        d = queue(("mini", "running", {}), ("mini", "next", {}))
        j = d["jobs"][0]
        j.update(status="claimed", by="codex", since="2026-11-05T09:30Z", eta="2026-11-05T11:30Z")
        lanes = {a["agent"]: a for a in run(d, mini={"chain": [{"agent": "codex", "up": True}, {"agent": "cursor", "up": False, "why": "out"}]})["agents"]}
        self.assertEqual((lanes["codex"]["now"], lanes["codex"]["freeAt"]), ("J0001", "2026-11-05T10:15Z"))
        self.assertEqual(run(d, mini={"chain": [{"agent": "codex", "up": True}, {"agent": "cursor", "up": False, "why": "out"}]})["jobs"]["J0002"]["startAt"],
                         "2026-11-05T10:15Z")

    def test_down_agents_say_why_and_jobs_for_them_say_who_they_wait_for(self):
        d = queue(("mini", "for cursor", {"for_agent": "cursor"}))
        s = run(d)
        lanes = {a["agent"]: a for a in s["agents"]}
        self.assertFalse(lanes["cursor"]["up"])
        self.assertIn("out of usage", lanes["cursor"]["why"])
        self.assertIn("waiting for cursor", s["noAgent"]["J0001"])

    def test_a_worker_outside_the_chief_chain_is_up_unless_flagged(self):
        d = queue(("mini", "x", {"for_agent": "cursor"}))
        mini = {"chain": [{"agent": "codex", "up": True}, {"agent": "gemini", "up": True}]}
        lanes = {a["agent"]: a for a in run(d, mini=mini)["agents"]}
        self.assertTrue(lanes["cursor"]["up"])
        with patch.object(q, "_flags", return_value={"cursor": {"out_until": "2026-11-06T00:00:00Z", "reason": "weekly"}}):
            lanes = {a["agent"]: a for a in q.section(d, mini, BOOK, AT)["agents"]}
        self.assertFalse(lanes["cursor"]["up"])

    def test_macbook_and_cloud_lanes(self):
        d = queue(("macbook", "book job", {}), ("cloud", "cloud job", {}))
        f = run(d)["jobs"]
        self.assertEqual(f["J0001"]["agent"], "macbook")
        self.assertEqual((f["J0002"]["agent"], f["J0002"]["startAt"]), ("claude", "2026-11-05T10:50Z"))
        self.assertNotIn("J0001", run(d, book={"at": "2026-11-05T08:00:00Z"})["jobs"])  # stale MacBook

    def test_what_the_mini_session_found_on_5_nov(self):
        d = queue(("mini", "a", {}), ("macbook", "b", {}), ("cloud", "c", {}))
        mini = {"at": "2026-11-05T09:55:00Z", "state": "running", "note": "woke Gemini for J2147 (cap 25 min)",
                "chain": MINI["chain"] + [{"agent": "claude", "up": False, "why": "marked down: Chief inbox not progressed"}]}
        book = {"at": "2026-11-05T09:58:00Z", "state": "waiting", "why": ["in use (3 min idle, needs 10)"]}
        s = run(d, mini=mini, book=book)
        lanes = {a["agent"]: a for a in s["agents"]}
        self.assertEqual(lanes["gemini"]["now"], "J2147")  # running, not "free now"
        self.assertFalse(lanes["macbook"]["up"])
        self.assertIn("in use", lanes["macbook"]["why"])
        self.assertFalse(lanes["claude"]["up"])
        self.assertEqual(s["jobs"]["J0001"]["agent"], "codex")  # Gemini is busy, Codex is free
        self.assertNotIn("J0002", s["jobs"])

    def test_two_macbook_slots_take_two_jobs_at_once(self):
        import board_publish
        d = queue(("macbook", "a", {}), ("macbook", "b", {}), ("macbook", "c", {}))
        hb = board_publish.merge_macbook([{"at": "2026-11-05T09:55:00Z", "slot": 1, "agent": "macbook", "state": "idle"},
                                          {"at": "2026-11-05T09:56:00Z", "slot": 2, "agent": "macbook-2", "state": "idle"}])
        f = run(d, book=hb)["jobs"]
        self.assertEqual({f["J0001"]["agent"], f["J0002"]["agent"]}, {"macbook", "macbook-2"})
        self.assertEqual((f["J0001"]["startAt"], f["J0002"]["startAt"]), ("2026-11-05T10:00Z", "2026-11-05T10:00Z"))
        lanes = {a["agent"]: a for a in run(d)["agents"]}  # an old single heartbeat: slot 2 not reporting yet
        self.assertTrue(lanes["macbook"]["up"])
        self.assertIn("slot 2", lanes["macbook-2"]["why"])

    def test_pace_comes_from_jobs_finished_in_the_last_day(self):
        d = {"jobs": [{"status": "done", "history": [{"at": f"2026-11-05T0{i}:00Z", "by": "gemini", "what": "done: ok"}]}
                      for i in range(8)]}
        self.assertEqual(q.durations(d, AT)["gemini"], 150)  # 1440/8 = 180, clamped to 150
        d["jobs"] *= 6
        self.assertEqual(q.durations(d, AT)["gemini"], 30)

    def test_models_forecast_and_dispatcher_share_one_out_of_usage_source_and_reset_retry(self):
        import json
        import tempfile
        import board_publish as bp
        import chief_relay as cr

        now = dt.datetime(2026, 11, 17, 8, 40, tzinfo=dt.timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            state = root / "state" / "chief"
            (state / "down").mkdir(parents=True)
            studio_dir = root / "studio"
            (studio_dir / "scripts").mkdir(parents=True)
            flags_file = studio_dir / "scripts" / "credit_flags.json"
            flags_file.write_text('{"flags": {}}')
            ledger = studio_dir / "05_Analytics" / "ai_spend" / "ledger.jsonl"
            ledger.parent.mkdir(parents=True)

            # 1) Cursor failed out of usage in runs.jsonl with no down/cursor.json and only a stale past reset in ledger:
            #    retries after a few hours (08:27 + 3 h = 11:27), ignoring the "$0.58 used this month (resets Dec 1)" cap.
            (state / "runs.jsonl").write_text(
                json.dumps({"at": "2026-11-17T08:27:22Z", "job": "J2976", "worker": "cursor",
                            "model": "cursor-grok-4-7", "out_of_usage": True}) + "\n"
            )
            ledger.write_text(
                json.dumps({"at": "2026-11-09T08:30:46Z", "kind": "record", "pool": "cursor", "left": 1.0,
                            "total": 100.0, "note": "Weekly included usage 99% used; weekly resets 12 Nov; "
                                                    "$0.58 used this month (resets Dec 1)"}) + "\n"
            )
            (state / "down" / "codex.json").write_text(
                json.dumps({"since": "2026-11-16T10:00:00Z", "until": "2026-11-17T23:22:00Z",
                            "reason": "Codex hit usage limit until 2026-11-17T23:22:00Z"})
            )
            (state / "chain.json").write_text(json.dumps({
                "at": "2026-11-17T08:33:39Z",
                "rows": [
                    {"agent": "codex", "up": False, "why": "marked down: Codex hit usage limit"},
                    {"agent": "gemini", "up": True, "why": "ready"},
                ],
            }))

            d = {"next_id": 3, "jobs": [
                {"id": "J2979", "title": "Sweep", "needs": "mini", "status": "open", "history": []},
                {"id": "J2985", "title": "For Cursor", "needs": "mini", "for": "cursor", "status": "open", "history": []},
            ]}
            with patch.object(jobs.chief_relay, "worker_capabilities", return_value={}), \
                    patch.object(jobs.chief_relay, "current_execution", return_value=None), \
                    patch.object(jobs, "ordered", side_effect=lambda data, at=None: list(data["jobs"])), \
                    patch.dict("os.environ", {"CHIEF_USAGE_RETRY_H": "3"}, clear=False):
                models = bp.models_status(now, d["jobs"], state=state, flags_file=flags_file, studio=studio_dir)
                forecast = q.section(d, {"chain": []}, BOOK, now, models=models, state=state,
                                     studio=studio_dir, flags_file=flags_file)
                disp = cr.agent_status("cursor", now, state=state, studio=studio_dir, flags_file=flags_file)

            m_cursor = next(m for m in models["models"] if m["id"] == "cursor")
            f_cursor = next(a for a in forecast["agents"] if a["agent"] == "cursor")
            self.assertEqual(m_cursor["status"], "red")
            self.assertFalse(f_cursor["up"])
            self.assertFalse(disp["up"])
            self.assertEqual(m_cursor["why"], f_cursor["why"])
            self.assertEqual(m_cursor["until"], "2026-11-17T11:27:22Z")
            self.assertEqual(f_cursor["until"], "2026-11-17T11:27:22Z")
            self.assertEqual(disp["until"], "2026-11-17T11:27:22Z")
            self.assertEqual(forecast["jobs"]["J2979"]["agent"], "gemini")
            self.assertIn("waiting for cursor", forecast["noAgent"]["J2985"])

            # 2) Once the credit reader records a fresh future reset time, all three use that reset time.
            ledger.write_text(
                json.dumps({"at": "2026-11-17T08:39:00Z", "kind": "record", "pool": "cursor", "left": 0.0,
                            "total": 100.0, "note": "Weekly included usage 100% used; weekly resets Thu 19 Nov 19:30Z"}) + "\n"
            )
            with patch.object(jobs.chief_relay, "worker_capabilities", return_value={}), \
                    patch.object(jobs.chief_relay, "current_execution", return_value=None), \
                    patch.object(jobs, "ordered", side_effect=lambda data, at=None: list(data["jobs"])):
                models2 = bp.models_status(now, d["jobs"], state=state, flags_file=flags_file, studio=studio_dir)
                forecast2 = q.section(d, {"chain": []}, BOOK, now, models=models2, state=state,
                                      studio=studio_dir, flags_file=flags_file)
                disp2 = cr.agent_status("cursor", now, state=state, studio=studio_dir, flags_file=flags_file)
            m2 = next(m for m in models2["models"] if m["id"] == "cursor")
            f2 = next(a for a in forecast2["agents"] if a["agent"] == "cursor")
            self.assertEqual(m2["until"], "2026-11-19T19:30:00Z")
            self.assertEqual(f2["until"], "2026-11-19T19:30:00Z")
            self.assertEqual(disp2["until"], "2026-11-19T19:30:00Z")


if __name__ == "__main__":
    unittest.main()
