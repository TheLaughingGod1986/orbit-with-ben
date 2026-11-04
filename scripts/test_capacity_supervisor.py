"""Real local harmless subprocesses; no worker/model/publishing calls."""
import copy
import datetime as dt
import os
import pathlib
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from capacity_supervisor import run, utcnow
from execution_leases import Registry


class Supervisor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.registry = Registry(self.root / "leases", "mini", 1)
        at = utcnow()
        self.claim = dict(id="J1843", status="claimed", by="codex", kind="assembly",
            execution_resources=["cpu"], no_spend=True, no_publish=True,
            dispatch_reservation=dict(job="J1843", token="token-A", host="mini", worker="codex",
                account="shared", claimant="codex", phase="claimed", head="reviewed",
                at=at.isoformat(), expiresAt=(at+dt.timedelta(minutes=2)).isoformat()))
        self.kw = dict(registry=self.registry, read_claim=lambda:copy.deepcopy(self.claim),
            guard=lambda claim:True, installed_head="reviewed", reviewed_head="reviewed",
            argv=[sys.executable, "-c", "print('local test')"], cwd=self.root,
            log_path=self.root / "execution.log", cap_seconds=2,
            preflight=lambda claim, cwd:None)

    def test_real_exit_is_receipt_and_does_not_complete_claim(self):
        before = copy.deepcopy(self.claim)
        result = run(**self.kw)
        self.assertEqual((result["phase"], result["exit_code"]), ("exited", 0))
        self.assertEqual(self.claim, before)
        self.assertEqual(self.registry.observe(utcnow()), [])
        self.assertEqual((self.root / "execution.log").read_text(), "local test\n")

    def test_nonzero_exit_retained(self):
        self.kw["argv"] = [sys.executable, "-c", "raise SystemExit(7)"]
        self.assertEqual(run(**self.kw)["exit_code"], 7)
        self.assertEqual(self.registry.observe(utcnow()), [])

    def test_completed_attempt_cannot_relaunch_same_canonical_token(self):
        run(**self.kw)
        self.kw["log_path"] = self.root / "second.log"
        with self.assertRaises(FileExistsError):
            run(**self.kw)
        self.assertEqual((self.root / "second.log").stat().st_size, 0)
        self.assertEqual(self.registry.observe(utcnow()), [])

    def test_cap_kills_real_child_and_frees_only_after_reaping(self):
        self.kw.update(argv=[sys.executable, "-c", "import time; time.sleep(30)"], cap_seconds=1)
        result = run(**self.kw)
        self.assertEqual((result["phase"], result["exit_code"]), ("timed_out", -9))
        self.assertEqual(self.registry.observe(utcnow()), [])

    def test_guard_loss_stops_running_child(self):
        checks = iter([True, True, False])
        self.kw.update(argv=[sys.executable, "-c", "import time; time.sleep(30)"],
                       guard=lambda c:next(checks))
        self.assertEqual(run(**self.kw)["phase"], "guard_stopped")

    def test_timeout_stops_descendant_in_same_session(self):
        marker = self.root / "orphan-wrote.txt"
        descendant = "import time,pathlib; time.sleep(1.6); pathlib.Path(" + repr(str(marker)) + ").write_text('orphan')"
        leader = "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c'," + repr(descendant) + "]); time.sleep(30)"
        self.kw.update(argv=[sys.executable, "-c", leader], cap_seconds=1)
        self.assertEqual(run(**self.kw)["phase"], "timed_out")
        time.sleep(0.9)
        self.assertFalse(marker.exists())

    def test_canonical_cancellation_stops_running_child(self):
        calls = 0
        def reread():
            nonlocal calls
            calls += 1
            if calls >= 3:
                self.claim["status"] = "open"
            return copy.deepcopy(self.claim)
        self.kw.update(argv=[sys.executable, "-c", "import time; time.sleep(30)"], read_claim=reread)
        self.assertEqual(run(**self.kw)["phase"], "guard_stopped")

    def test_changed_claim_after_preflight_never_launches(self):
        self.kw["preflight"] = lambda c, p:self.claim.update(status="open")
        with self.assertRaises(ValueError):
            run(**self.kw)
        self.assertFalse((self.root / "execution.log").exists())
        self.assertEqual(self.registry.observe(utcnow()), [])

    def test_preflight_hash_failure_never_occupies_slot(self):
        def bad(c, p):
            raise ValueError("changed input hash")
        self.kw["preflight"] = bad
        with self.assertRaisesRegex(ValueError, "hash"):
            run(**self.kw)
        self.assertEqual(self.registry.observe(utcnow()), [])

    def test_second_supervisor_in_same_process_cannot_replay(self):
        receipt = self.claim["dispatch_reservation"]
        self.registry.record(dict(receipt, phase="reserved"), os.getpid(), utcnow(), 60)
        with self.assertRaisesRegex(ValueError, "already has"):
            run(**self.kw)
        self.assertEqual(len(self.registry.observe(utcnow())), 1)

    def test_gate_rejections_have_no_process_side_effect(self):
        changes = [dict(status="open"), dict(by="other"), dict(no_spend=False),
                   dict(no_publish=False), dict(kind="chief"), dict(execution_resources=["browser"])]
        for change in changes:
            with self.subTest(change=change):
                original = copy.deepcopy(self.claim)
                self.claim.update(change)
                with self.assertRaises(ValueError):
                    run(**self.kw)
                self.claim = original
        self.assertFalse((self.root / "execution.log").exists())

    def test_stale_claim_and_review_change_rejected(self):
        self.kw["reviewed_head"] = "new-review"
        with self.assertRaises(ValueError):
            run(**self.kw)
        self.kw["reviewed_head"] = "reviewed"
        self.claim["dispatch_reservation"]["expiresAt"] = (utcnow()-dt.timedelta(seconds=1)).isoformat()
        with self.assertRaises(ValueError):
            run(**self.kw)

    def test_launch_failure_releases_local_lease_but_preserves_claim(self):
        self.kw["argv"] = [str(self.root / "missing-executable")]
        with self.assertRaises(FileNotFoundError):
            run(**self.kw)
        self.assertEqual(self.registry.observe(utcnow()), [])
        self.assertEqual(self.claim["status"], "claimed")

    def test_log_never_overwritten(self):
        (self.root / "execution.log").write_text("old")
        with self.assertRaises(FileExistsError):
            run(**self.kw)
        self.assertEqual((self.root / "execution.log").read_text(), "old")
        self.assertEqual(self.registry.observe(utcnow()), [])

    def test_cleanup_failure_does_not_free_slot(self):
        with patch("capacity_supervisor._stop_group", side_effect=RuntimeError("cannot reap")):
            with self.assertRaisesRegex(RuntimeError, "reap"):
                run(**self.kw)
        self.assertEqual(len(self.registry.observe(utcnow())), 1)

    def test_real_supervisor_crash_quarantines_child_capacity(self):
        claim_file = self.root / "claim.json"
        import json
        claim_file.write_text(json.dumps(self.claim))
        pid_file = self.root / "child.pid"
        child_code = "import os,pathlib,time; pathlib.Path(" + repr(str(pid_file)) + ").write_text(str(os.getpid())); time.sleep(30)"
        code = (
            "import json,pathlib,sys; sys.path.insert(0," + repr(str(pathlib.Path(__file__).parent)) + "); "
            "from execution_leases import Registry; from capacity_supervisor import run; "
            "run(registry=Registry(" + repr(str(self.root / "leases")) + ",'mini',1), "
            "read_claim=lambda:json.loads(pathlib.Path(" + repr(str(claim_file)) + ").read_text()), "
            "guard=lambda c:True,installed_head='reviewed',reviewed_head='reviewed', "
            "argv=[sys.executable,'-c'," + repr(child_code) + "],cwd=" + repr(str(self.root)) + ", "
            "log_path=" + repr(str(self.root / "crash.log")) + ",cap_seconds=20,preflight=lambda c,p:None)"
        )
        supervisor = subprocess.Popen([sys.executable, "-c", code])
        child_pid = None
        try:
            until = time.monotonic()+5
            while not pid_file.exists() and time.monotonic() < until:
                if supervisor.poll() is not None:
                    self.fail("test supervisor exited before spawning child")
                time.sleep(0.02)
            self.assertTrue(pid_file.exists())
            child_pid = int(pid_file.read_text())
            supervisor.kill()
            supervisor.wait(timeout=5)
            row = self.registry.observe(utcnow())[0]
            self.assertTrue(row["recovery_required"])
            self.assertFalse(row["process_validated"])
            self.assertEqual(row["job"], "J1843")
        finally:
            if supervisor.poll() is None:
                supervisor.kill()
                supervisor.wait(timeout=5)
            if child_pid:
                try:
                    os.killpg(child_pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass


if __name__ == "__main__":
    unittest.main()
