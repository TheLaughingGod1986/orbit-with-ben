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

    def test_the_worktree_moves_when_the_one_already_there_cannot_be_read(self):
        """11 Nov 2026: the folder on the removable SSD could be made and looked writable, but launchd could not
        open the worktree's files. The run chose it, could not read it, and stopped at 'already exists'."""
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            wt = t / "worktrees" / "analytics"
            wt.mkdir(parents=True)                      # a worktree folder with no .git pointer that opens
            env = {"ANALYTICS_WORKTREE": str(wt), "ANALYTICS_SAFE_DIR": f"{t}/safe"}
            self.assertEqual(sh("pick_worktree", env=env).stdout.strip(), f"{t}/safe/worktree")
            (wt / ".git").write_text("gitdir: elsewhere\n")
            self.assertEqual(sh("pick_worktree", env=env).stdout.strip(), str(wt))

    def test_usable_leaves_no_file_behind(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(sh(f'usable "{t}"; echo rc=$?').stdout.strip(), "rc=0")
            self.assertEqual(list(pathlib.Path(t).iterdir()), [])

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
            (t / "not_a_repo/scripts").mkdir(parents=True)
            # Reach the existing Git-failure/watchdog path through the unarmed guard.
            shutil.copy2(SCRIPT.parents[2] / "scripts/engine_guard.py",
                         t / "not_a_repo/scripts/engine_guard.py")
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


@unittest.skipUnless(shutil.which("bash") and shutil.which("perl") and shutil.which("git"), "needs bash, perl and git")
class WorktreeAndPushRetry(unittest.TestCase):
    def setUp(self):
        import os
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.git_env = dict(
            os.environ,
            GIT_AUTHOR_NAME="Studio tests",
            GIT_COMMITTER_NAME="Studio tests",
            GIT_AUTHOR_EMAIL="studio-test@example.invalid",
            GIT_COMMITTER_EMAIL="studio-test@example.invalid",
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_CONFIG_NOSYSTEM="1",
            HOME=str(self.root / "home"),
        )
        (self.root / "home").mkdir()
        self.remote = self.root / "remote.git"
        self.git(self.root, "init", "--bare", str(self.remote))
        self.repo = self.root / "repo"
        self.git(self.root, "clone", str(self.remote), str(self.repo))
        self.git(self.repo, "checkout", "-b", "main")
        self.write(self.repo, "05_Analytics/owb/snapshots/seed.json", "{}\n")
        self.git(self.repo, "add", ".")
        self.git(self.repo, "commit", "-m", "seed without engine_guard")
        self.git(self.repo, "push", "origin", "main")

    def git(self, repo: pathlib.Path, *args: str) -> str:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=self.git_env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout.strip()

    def write(self, repo: pathlib.Path, rel: str, text: str) -> None:
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def test_stale_worktree_missing_engine_guard_is_rebased_before_guard_check(self):
        """Sat 21 Nov 2026 failure: fallback worktree predated scripts/engine_guard.py and failed before rebase."""
        wt = self.root / "safe" / "worktree"
        self.git(self.repo, "worktree", "add", "--detach", str(wt), "origin/main")
        self.assertFalse((wt / "scripts" / "engine_guard.py").exists())

        # Advance origin/main to add scripts/engine_guard.py (like commit 19a110d1dd).
        (self.repo / "scripts").mkdir(parents=True, exist_ok=True)
        shutil.copy2(SCRIPT.parents[2] / "scripts" / "engine_guard.py", self.repo / "scripts" / "engine_guard.py")
        self.write(self.repo, "channels/channels.json", '{"studio": {"github": "test/studio"}}\n')
        self.git(self.repo, "add", ".")
        self.git(self.repo, "commit", "-m", "add engine_guard")
        self.git(self.repo, "push", "origin", "main")

        r = sh(
            f'prepare_tracker_worktree "{self.repo}" "{wt}" && python3 "{wt}/scripts/engine_guard.py"',
            env=self.git_env,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((wt / "scripts" / "engine_guard.py").is_file())
        self.assertEqual(self.git(wt, "rev-parse", "HEAD"), self.git(self.remote, "rev-parse", "main"))

    def test_corrupted_worktree_directory_is_recreated_cleanly(self):
        wt = self.root / "safe" / "worktree"
        wt.mkdir(parents=True)
        (wt / ".git").write_text("gitdir: /nonexistent/broken/worktree\n")
        (wt / "stale.txt").write_text("junk\n")

        r = sh(f'prepare_tracker_worktree "{self.repo}" "{wt}"', env=self.git_env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertFalse((wt / "stale.txt").exists())
        self.assertEqual(self.git(wt, "rev-parse", "HEAD"), self.git(self.remote, "rev-parse", "main"))

    def test_worktree_from_foreign_repo_is_refused_without_deleting_it(self):
        foreign = self.root / "foreign"
        self.git(self.root, "init", str(foreign))
        self.write(foreign, "keep.txt", "precious\n")
        self.git(foreign, "add", ".")
        self.git(foreign, "commit", "-m", "foreign")

        r = sh(f'prepare_tracker_worktree "{self.repo}" "{foreign}"', env=self.git_env)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("does not belong", r.stderr)
        self.assertEqual((foreign / "keep.txt").read_text(), "precious\n")

    def test_push_with_rebase_retry_recovers_from_non_fast_forward(self):
        """Thu 19 Nov & Fri 20 Nov failure: main moved while the snapshot ran; retry must fetch, rebase, and push."""
        wt = self.root / "safe" / "worktree"
        self.git(self.repo, "worktree", "add", "--detach", str(wt), "origin/main")

        # Tracker commits today's snapshot in the detached worktree.
        self.write(wt, "05_Analytics/owb/snapshots/2026-11-21.json", '{"views": 100}\n')
        self.git(wt, "add", "05_Analytics")
        self.git(wt, "commit", "-m", "Channel tracker 2026-11-21")

        # Meanwhile origin/main moves ahead on an unrelated file.
        self.write(self.repo, "other.txt", "concurrent job commit\n")
        self.git(self.repo, "add", "other.txt")
        self.git(self.repo, "commit", "-m", "concurrent commit on main")
        self.git(self.repo, "push", "origin", "main")

        env = dict(self.git_env, PUSH_RETRIES="3", PUSH_RETRY_DELAY_S="0")
        r = sh(f'cd "{wt}" && push_with_rebase_retry', env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.git(self.remote, "show", "main:05_Analytics/owb/snapshots/2026-11-21.json"), '{"views": 100}')
        self.assertEqual(self.git(self.remote, "show", "main:other.txt"), "concurrent job commit")

    def test_push_with_rebase_retry_fails_after_bounded_attempts_when_remote_rejects(self):
        wt = self.root / "safe" / "worktree"
        self.git(self.repo, "worktree", "add", "--detach", str(wt), "origin/main")
        self.write(wt, "05_Analytics/owb/snapshots/2026-11-21.json", '{"views": 100}\n')
        self.git(wt, "add", "05_Analytics")
        self.git(wt, "commit", "-m", "Channel tracker 2026-11-21")

        counter = self.root / "attempts.log"
        hook = self.remote / "hooks" / "pre-receive"
        hook.write_text(f'#!/bin/sh\necho x >> "{counter}"\nexit 1\n')
        hook.chmod(0o755)

        env = dict(self.git_env, PUSH_RETRIES="3", PUSH_RETRY_DELAY_S="0")
        r = sh(f'cd "{wt}" && push_with_rebase_retry', env=env)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("failed after 3 attempts", r.stderr)
        self.assertEqual(len(counter.read_text().splitlines()), 3)

    def test_push_with_rebase_retry_aborts_rebase_cleanly_on_conflict(self):
        wt = self.root / "safe" / "worktree"
        self.git(self.repo, "worktree", "add", "--detach", str(wt), "origin/main")
        self.write(wt, "05_Analytics/owb/snapshots/seed.json", '{"side": "tracker"}\n')
        self.git(wt, "add", "05_Analytics")
        self.git(wt, "commit", "-m", "tracker edit")
        local_head = self.git(wt, "rev-parse", "HEAD")

        self.write(self.repo, "05_Analytics/owb/snapshots/seed.json", '{"side": "main"}\n')
        self.git(self.repo, "add", "05_Analytics")
        self.git(self.repo, "commit", "-m", "conflicting main edit")
        self.git(self.repo, "push", "origin", "main")

        env = dict(self.git_env, PUSH_RETRIES="3", PUSH_RETRY_DELAY_S="0")
        r = sh(f'cd "{wt}" && push_with_rebase_retry', env=env)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("rebase onto origin/main failed", r.stderr)
        self.assertEqual(self.git(wt, "rev-parse", "HEAD"), local_head)
        gitdir = pathlib.Path(self.git(wt, "rev-parse", "--git-dir"))
        self.assertFalse((gitdir / "rebase-merge").exists())


if __name__ == "__main__":
    unittest.main()
