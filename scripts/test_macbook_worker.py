#!/usr/bin/env python3
"""Tests for scripts/macbook_worker.py: it only runs on mains power while the MacBook is idle, the `macbook` lane is
kept apart from the Mini's, and a run never outlives its cap (Ben, 28 Oct 2026)."""
import datetime as dt
import os
import pathlib
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jobs  # noqa: E402
import macbook_worker as mw  # noqa: E402

AC = "Now drawing from 'AC Power'\n -InternalBattery-0 (id=1)\t100%; charged; 0:00 remaining present: true"
BATT = "Now drawing from 'Battery Power'\n -InternalBattery-0 (id=1)\t80%; discharging"
IDLE_20 = '    |   "HIDIdleTime" = 1200000000000\n'
IDLE_1 = '    |   "HIDIdleTime" = 60000000000\n'
T0 = dt.datetime(2026, 10, 28, 12, 0, tzinfo=dt.timezone.utc)
WED_NIGHT = dt.datetime(2026, 10, 28, 22, 0, tzinfo=dt.timezone.utc)


class Guards(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._state = mw.STATE
        mw.STATE = pathlib.Path(self.tmp.name)

    def tearDown(self):
        mw.STATE = self._state
        self.tmp.cleanup()

    def test_idle_on_mains_with_space_runs(self):
        self.assertEqual(mw.guards(AC, IDLE_20, free_gb=100, now=WED_NIGHT), [])

    def test_round_the_clock_by_default(self):
        self.assertTrue(mw.in_hours(dt.datetime.fromisoformat("2026-10-29T14:00:00+00:00")))  # Thu afternoon
        self.assertEqual(mw.guards(AC, IDLE_20, free_gb=100, now=T0), [])  # Wed noon
        self.assertTrue(any("in use" in w for w in mw.guards(AC, IDLE_1, free_gb=100, now=T0)))  # Ben at the keys

    def test_hours_are_weeknights_and_weekends_london(self):
        os.environ["MACBOOK_HOURS"] = "night"
        self.addCleanup(os.environ.pop, "MACBOOK_HOURS", None)
        at = lambda s: dt.datetime.fromisoformat(s)  # noqa: E731
        self.assertTrue(mw.in_hours(at("2026-10-28T21:30:00+00:00")))   # Wed 21:30 London
        self.assertTrue(mw.in_hours(at("2026-10-29T08:00:00+00:00")))   # Thu 08:00
        self.assertFalse(mw.in_hours(at("2026-10-29T09:00:00+00:00")))  # Thu 09:00: Ben's working day
        self.assertFalse(mw.in_hours(at("2026-10-29T14:00:00+00:00")))  # Thu afternoon
        self.assertTrue(mw.in_hours(at("2026-10-31T14:00:00+00:00")))   # Sat afternoon
        self.assertTrue(mw.in_hours(at("2026-11-01T14:00:00+00:00")))   # Sun afternoon
        self.assertTrue(mw.in_hours(at("2026-06-03T20:30:00+00:00")))   # BST: 21:30 London in summer

    def test_no_run_that_would_end_after_nine(self):
        os.environ["MACBOOK_HOURS"] = "night"
        self.addCleanup(os.environ.pop, "MACBOOK_HOURS", None)
        why = mw.guards(AC, IDLE_20, free_gb=100, now=dt.datetime.fromisoformat("2026-10-29T08:50:00+00:00"))
        self.assertTrue(any("outside its hours" in w for w in why))
        why = mw.guards(AC, IDLE_20, free_gb=100, now=dt.datetime.fromisoformat("2026-10-29T14:00:00+00:00"))
        self.assertTrue(any("outside its hours" in w for w in why))

    def test_battery_in_use_and_low_disk_each_stop_it(self):
        why = mw.guards(BATT, IDLE_1, free_gb=3, now=WED_NIGHT)
        self.assertTrue(any("battery" in w for w in why))
        self.assertTrue(any("in use" in w for w in why))
        self.assertTrue(any("disk low" in w for w in why))

    def test_pause_file_stops_it(self):
        (mw.STATE / "macbook-worker.pause").write_text("")
        self.assertTrue(any("paused" in w for w in mw.guards(AC, IDLE_20, free_gb=100, now=WED_NIGHT)))

    def test_unreadable_idle_counts_as_in_use(self):
        self.assertEqual(mw.idle_minutes("no such key"), 0.0)

    def test_claimed_job_id_is_read_from_jobs_output(self):
        self.assertEqual(mw.claimed_job("J1102 [macbook] claimed by macbook\nTitle ..."), "J1102")
        self.assertEqual(mw.claimed_job("jobs: nothing waiting for you"), "")

    def test_prompt_names_the_job_and_the_local_model_limits(self):
        p = mw.PROMPT.format(job="J1102", owb="/o", hos="/h", model="qwen3:14b", cap_min=25)
        self.assertIn("jobs.py show J1102", p)
        self.assertIn("127.0.0.1:11434", p)
        self.assertIn("Never scripts, facts or anything spoken", p)

    def test_usage_is_recorded_at_most_every_few_hours(self):
        calls = []
        real = mw.sh
        mw.sh = lambda cmd, **kw: calls.append(cmd) or mw.subprocess.CompletedProcess(cmd, 0, "READ codex", "")
        self.addCleanup(setattr, mw, "sh", real)
        self.assertTrue(mw.record_usage(now=WED_NIGHT))
        self.assertEqual(calls[0][calls[0].index("--codex-pool") + 1], "codex")  # one account on both machines
        self.assertFalse(mw.record_usage(now=WED_NIGHT + dt.timedelta(hours=1)))
        self.assertTrue(mw.record_usage(now=WED_NIGHT + dt.timedelta(hours=4)))
        self.assertEqual(len(calls), 2)


class Lane(unittest.TestCase):
    def job(self, needs):
        return {"id": "J9001", "title": "033 picture: render batch", "needs": needs, "status": "open", "by": ""}

    def test_macbook_jobs_go_only_to_the_macbook_worker(self):
        j = self.job("macbook")
        data = {"jobs": [j]}
        self.assertIn("macbook", jobs.NEEDS)
        self.assertTrue(jobs.claimable(data, j, {"macbook"}, T0, "macbook"))
        self.assertFalse(jobs.claimable(data, j, jobs.MINI_NEEDS, T0, "codex"))

    def test_the_macbook_worker_never_takes_mini_jobs(self):
        j = self.job("mini")
        self.assertFalse(jobs.claimable({"jobs": [j]}, j, {"macbook"}, T0, "macbook"))


class Cap(unittest.TestCase):
    def test_a_run_past_its_cap_is_killed_with_its_children(self):
        with tempfile.TemporaryDirectory() as t:
            marker = pathlib.Path(t) / "child_survived"
            start = time.time()
            code = mw.run_capped(["sh", "-c", f"(sleep 3; touch {marker}) & sleep 30"], t, 1)
            self.assertEqual(code, 124)
            self.assertLess(time.time() - start, 10)
            time.sleep(3.5)
            self.assertFalse(marker.exists(), "a background child outlived the cap")


if __name__ == "__main__":
    unittest.main()
