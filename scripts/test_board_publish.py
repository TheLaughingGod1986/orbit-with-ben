#!/usr/bin/env python3
"""Tests for board_publish.py (self-updating Studio Kanban data) and the board_site build."""
import datetime as dt
import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import board_publish as bp  # noqa: E402


def docs(job_status="open", heartbeat="2026-10-09T20:00:00Z"):
    return {"hos": {"updatedAt": "x", "pipeline": {"films": [{"id": "005"}]}},
            "owb": {"updatedAt": "x", "films": [{"film": "027"}], "jobs": [{"id": "J1", "status": job_status}],
                    "lanes": {"mini": {"busy": 1, "heartbeat": {"at": heartbeat}}}},
            "briefs": {"updatedAt": "x", "films": {"027": "note"}},
            "credits": {"pools": {"flow": {}}}}


T0 = dt.datetime(2026, 10, 9, 20, 0, tzinfo=dt.timezone.utc)
T1 = T0 + dt.timedelta(minutes=5)


class ChangeTimes(unittest.TestCase):
    def test_first_run_stamps_every_section(self):
        board, hashes = bp.assemble(docs(), {}, {}, T0)
        self.assertEqual(set(board["changedAt"]), set(bp.SECTIONS))
        self.assertEqual(board["dataChangedAt"], "2026-10-09T20:00:00Z")
        self.assertEqual(board["owb"]["updatedAt"], "2026-10-09T20:00:00Z")

    def test_only_the_changed_section_moves(self):
        b0, h0 = bp.assemble(docs(), {}, {}, T0)
        prev = {"hashes": h0, "changedAt": b0["changedAt"]}
        b1, _ = bp.assemble(docs(job_status="claimed"), prev, {}, T1)
        self.assertEqual(b1["changedAt"]["owb"], "2026-10-09T20:05:00Z")
        self.assertEqual(b1["changedAt"]["hos"], "2026-10-09T20:00:00Z")
        self.assertEqual(b1["dataChangedAt"], "2026-10-09T20:05:00Z")

    def test_heartbeat_alone_is_not_a_data_change_but_is_published(self):
        b0, h0 = bp.assemble(docs(), {}, {}, T0)
        b1, h1 = bp.assemble(docs(heartbeat="2026-10-09T20:10:00Z"), {"hashes": h0, "changedAt": b0["changedAt"]}, {}, T1)
        self.assertEqual(h0, h1)
        self.assertEqual(b1["dataChangedAt"], "2026-10-09T20:00:00Z")
        self.assertNotEqual(bp.digest(b0), bp.digest(b1))  # so the push still happens and "Mini last seen" moves

    def test_checks_ride_along(self):
        board, _ = bp.assemble(docs(), {}, {"OWB-022": {"verdict": "ok"}}, T0)
        self.assertEqual(board["checks"]["OWB-022"]["verdict"], "ok")


class Lock(unittest.TestCase):
    def test_a_busy_publish_queues_one_more_round_and_never_fails(self):
        with tempfile.TemporaryDirectory() as d:
            old = bp.STATE
            bp.STATE = Path(d)
            try:
                import fcntl
                with open(Path(d) / "publish.lock", "w") as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self.assertEqual(bp.main(["--quiet"]), 0)
                self.assertTrue((Path(d) / "again").exists())
            finally:
                bp.STATE = old


class JobsHook(unittest.TestCase):
    def test_hook_is_off_when_disabled(self):
        import jobs
        os.environ["BOARD_PUBLISH"] = "0"
        try:
            called = []
            real = jobs.subprocess.Popen
            jobs.subprocess.Popen = lambda *a, **k: called.append(a)
            try:
                jobs.publish_board()
            finally:
                jobs.subprocess.Popen = real
            self.assertEqual(called, [])
        finally:
            os.environ.pop("BOARD_PUBLISH")


class SiteBuild(unittest.TestCase):
    def test_build_patches_the_artifact_page(self):
        spec = importlib.util.spec_from_file_location("board_build", HERE.parent / "05_Analytics/kanban/board_site/build.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as d:
            mod.build(Path(d) / "dist")
            html = (Path(d) / "dist" / "index.html").read_text()
            self.assertIn("window.claude = { use:", html)
            self.assertIn("dbApi = db.canWrite===false ? null : db;", html)
            self.assertIn("board-data/board.json", html)
            self.assertTrue((HERE.parent / "05_Analytics/kanban/board_site/api/checks.js").exists())


if __name__ == "__main__":
    unittest.main()
