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
        lanes = {a["agent"]: a for a in run(d, mini={"chain": [{"agent": "codex", "up": True}]})["agents"]}
        self.assertEqual((lanes["codex"]["now"], lanes["codex"]["freeAt"]), ("J0001", "2026-11-05T10:15Z"))
        self.assertEqual(run(d, mini={"chain": [{"agent": "codex", "up": True}]})["jobs"]["J0002"]["startAt"],
                         "2026-11-05T10:15Z")

    def test_down_agents_say_why_and_jobs_for_them_say_who_they_wait_for(self):
        d = queue(("mini", "for cursor", {"for_agent": "cursor"}))
        s = run(d)
        lanes = {a["agent"]: a for a in s["agents"]}
        self.assertFalse(lanes["cursor"]["up"])
        self.assertIn("out of usage", lanes["cursor"]["why"])
        self.assertIn("waiting for cursor", s["noAgent"]["J0001"])

    def test_macbook_and_cloud_lanes(self):
        d = queue(("macbook", "book job", {}), ("cloud", "cloud job", {}))
        f = run(d)["jobs"]
        self.assertEqual(f["J0001"]["agent"], "macbook")
        self.assertEqual((f["J0002"]["agent"], f["J0002"]["startAt"]), ("claude", "2026-11-05T10:50Z"))
        self.assertNotIn("J0001", run(d, book={"at": "2026-11-05T08:00:00Z"})["jobs"])  # stale MacBook

    def test_pace_comes_from_jobs_finished_in_the_last_day(self):
        d = {"jobs": [{"status": "done", "history": [{"at": f"2026-11-05T0{i}:00Z", "by": "gemini", "what": "done: ok"}]}
                      for i in range(8)]}
        self.assertEqual(q.durations(d, AT)["gemini"], 150)  # 1440/8 = 180, clamped to 150
        d["jobs"] *= 6
        self.assertEqual(q.durations(d, AT)["gemini"], 30)


if __name__ == "__main__":
    unittest.main()
