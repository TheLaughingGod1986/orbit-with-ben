#!/usr/bin/env python3
"""The daily channel tracker (07_Content-Ops/launchd/analytics-snapshot.sh) must not hang on a folder that never
answers. 10 Nov 2026: ~/_desk/worktrees had moved to the removable SSD the day before; launchd cannot open a
removable volume without a macOS permission click, the first git call sat there, and no snapshot was made."""
import pathlib
import shutil
import subprocess
import tempfile
import time
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "07_Content-Ops" / "launchd" / "analytics-snapshot.sh"


def sh(body: str, env: dict | None = None, timeout: int = 30) -> subprocess.CompletedProcess:
    """Source the script (which must not run the tracker when sourced), then run `body`."""
    import os
    full = dict(os.environ, **(env or {}))
    return subprocess.run(["bash", "-c", f'source "{SCRIPT}"; {body}'], capture_output=True, text=True,
                          timeout=timeout, env=full)


@unittest.skipUnless(shutil.which("bash") and shutil.which("perl"), "needs bash and perl")
class Helpers(unittest.TestCase):
    def test_sourcing_the_script_does_not_run_the_tracker(self):
        r = sh("type -t main; type -t within; type -t usable; type -t pick_worktree; type -t gate_with_limit")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.split(), ["function"] * 5)
        self.assertNotIn("---", r.stdout)   # main prints '--- <date>' first thing

    def test_a_command_that_never_returns_is_stopped(self):
        t0 = time.time()
        r = sh("within 1 sleep 20; echo rc=$?")
        self.assertLess(time.time() - t0, 10)
        self.assertNotEqual(r.stdout.strip(), "rc=0")

    def test_a_command_inside_its_time_keeps_its_own_result(self):
        self.assertEqual(sh("within 5 true; echo rc=$?").stdout.strip(), "rc=0")
        self.assertEqual(sh("within 5 false; echo rc=$?").stdout.strip(), "rc=1")

    def test_a_gate_that_hangs_is_stopped_and_says_so(self):
        """10 Nov 2026: the hand run's gate step hung until a worker stopped it. It sits before the commit."""
        t0 = time.time()
        r = sh("gate_with_limit 1 sleep 20; echo rc=$?")
        self.assertLess(time.time() - t0, 10)
        self.assertIn("rc=142", r.stdout)
        self.assertIn("did not finish inside 1s and was stopped", r.stdout)
        self.assertIn("snapshot and reports still go out", r.stdout)

    def test_a_gate_that_finishes_keeps_its_own_result_and_says_nothing(self):
        self.assertEqual(sh("gate_with_limit 5 true; echo rc=$?").stdout.strip(), "rc=0")
        self.assertEqual(sh("gate_with_limit 5 sh -c 'exit 3'; echo rc=$?").stdout.strip(), "rc=3")

    def test_usable_makes_a_missing_folder_and_refuses_one_it_cannot_make(self):
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            self.assertEqual(sh(f'usable "{t}/new/deeper"; echo rc=$?').stdout.strip(), "rc=0")
            self.assertTrue((t / "new" / "deeper").is_dir())
            (t / "a_file").write_text("x")
            self.assertNotEqual(sh(f'usable "{t}/a_file/under"; echo rc=$?').stdout.strip(), "rc=0")

    def test_the_worktree_stays_where_it_is_when_its_folder_answers(self):
        with tempfile.TemporaryDirectory() as t:
            r = sh("pick_worktree", env={"ANALYTICS_WORKTREE": f"{t}/worktrees/analytics", "ANALYTICS_SAFE_DIR": f"{t}/safe"})
            self.assertEqual(r.stdout.strip(), f"{t}/worktrees/analytics")
            self.assertEqual(r.stderr.strip(), "")

    def test_the_worktree_moves_to_the_internal_disk_when_its_folder_cannot_be_used(self):
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            (t / "blocked").write_text("not a folder")   # stands in for a volume that refuses or never answers
            r = sh("pick_worktree", env={"ANALYTICS_WORKTREE": f"{t}/blocked/worktrees/analytics",
                                         "ANALYTICS_SAFE_DIR": f"{t}/safe"})
            self.assertEqual(r.stdout.strip(), f"{t}/safe/worktree")
            self.assertIn("did not answer or cannot be written", r.stderr)

    def test_a_folder_check_that_hangs_counts_as_not_usable(self):
        # Stand in for the hang: a `mkdir` that never returns, first on PATH for the check's own shell.
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            fake = t / "bin"; fake.mkdir()
            (fake / "mkdir").write_text("#!/bin/sh\nsleep 60\n"); (fake / "mkdir").chmod(0o755)
            import os
            t0 = time.time()
            r = sh(f'usable "{t}/x"; echo rc=$?', env={"PATH": f"{fake}:{os.environ['PATH']}"})
            self.assertLess(time.time() - t0, 20)
            self.assertNotEqual(r.stdout.strip(), "rc=0")


@unittest.skipUnless(shutil.which("bash") and shutil.which("perl") and shutil.which("git"), "needs bash, perl and git")
class WholeRun(unittest.TestCase):
    def test_a_run_that_ends_early_exits_with_its_own_code_and_the_watchdog_stays_quiet(self):
        """A first draft of the watchdog fired the moment the run ended: stopping its sleep let the lines after it
        run, and the script was killed with 143 and logged 'still going after 45 minutes'."""
        import os
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            (t / "not_a_repo").mkdir()
            env = dict(os.environ, HOME=str(t / "home"), ORBIT_REPO=str(t / "not_a_repo"),
                       ANALYTICS_WORKTREE=str(t / "worktrees" / "analytics"), ANALYTICS_SAFE_DIR=str(t / "safe"),
                       BOARD_PUBLISH="0")
            (t / "home").mkdir()
            r = subprocess.run(["bash", str(SCRIPT)], capture_output=True, text=True, timeout=120, env=env)
            out = r.stdout + r.stderr
            self.assertEqual(r.returncode, 1, out)
            self.assertIn("could not make the tracker worktree", out)
            self.assertNotIn("still going after 45 minutes", out)
            time.sleep(0.5)
            left = subprocess.run(["pgrep", "-f", "^perl -e sleep 2700; print"], capture_output=True, text=True).stdout.split()
            self.assertEqual(left, [], "the watchdog was left running")


if __name__ == "__main__":
    unittest.main()
