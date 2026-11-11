#!/usr/bin/env python3
"""Tests for scripts/macbook_worker.py: it only runs on mains power while the MacBook is idle, the `macbook` lane is
kept apart from the Mini's, and a run never outlives its cap (Ben, 28 Oct 2026)."""
import datetime as dt
import os
import pathlib
import sys
import tempfile
import time
import subprocess
import unittest
from unittest import mock

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
        slot = mock.patch.object(mw, "SLOT", 1)   # these are slot 1's rules, whichever slot runs the suite (J2463)
        slot.start(); self.addCleanup(slot.stop)

    def tearDown(self):
        mw.STATE = self._state
        self.tmp.cleanup()

    def test_idle_on_mains_with_space_runs(self):
        self.assertEqual(mw.guards(AC, IDLE_20, free_gb=100, now=WED_NIGHT), [])

    def test_round_the_clock_by_default(self):
        self.assertTrue(mw.in_hours(dt.datetime.fromisoformat("2026-10-29T14:00:00+00:00")))  # Thu afternoon
        self.assertEqual(mw.guards(AC, IDLE_20, free_gb=100, now=T0), [])  # Wed noon
        self.assertEqual(mw.guards(AC, IDLE_1, free_gb=100, now=T0), [])  # Ben at the keys: slot 1 runs in the background

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
        self.assertTrue(any("disk low" in w for w in why))
        with mock.patch.dict(os.environ, {"MACBOOK_BUSY_OK": "0"}):  # the old rule: nothing while Ben is at the keys
            self.assertTrue(any("in use" in w for w in mw.guards(AC, IDLE_1, free_gb=100, now=WED_NIGHT)))
        with mock.patch.object(mw, "SLOT", 2), mock.patch.object(mw.os, "cpu_count", return_value=10):
            self.assertTrue(any("in use" in w for w in mw.guards(AC, IDLE_1, free_gb=100, now=WED_NIGHT, load=1.0)))

    def test_a_job_while_ben_is_at_the_keys_runs_at_background_priority(self):
        with mock.patch.object(mw.shutil, "which", return_value="/usr/sbin/taskpolicy"):
            self.assertEqual(mw.busy_cmd(["codex", "exec"], idle_min=1)[:2], ["taskpolicy", "-b"])
            self.assertEqual(mw.busy_cmd(["codex", "exec"], idle_min=30), ["codex", "exec"])

    def test_pause_file_stops_it(self):
        (mw.STATE / "macbook-worker.pause").write_text("")
        self.assertTrue(any("paused" in w for w in mw.guards(AC, IDLE_20, free_gb=100, now=WED_NIGHT)))

    def test_unreadable_idle_counts_as_in_use(self):
        self.assertEqual(mw.idle_minutes("no such key"), 0.0)

    def test_claimed_job_id_is_read_from_jobs_output(self):
        self.assertEqual(mw.claimed_job("J1102 [macbook] claimed by macbook\nTitle ..."), "J1102")
        self.assertEqual(mw.claimed_job("jobs: nothing waiting for you"), "")

    def test_prompt_names_the_job_and_the_local_model_limits(self):
        p = mw.PROMPT.format(job="J1102", agent="macbook-2", model="qwen3:14b", cap_min=25, **mw.prompt_channels())
        self.assertIn("jobs.py show J1102", p)
        self.assertIn("jobs.py done J1102 --agent macbook-2", p)
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

    def test_heartbeat_says_why_it_is_waiting(self):
        doc = mw.heartbeat_doc("waiting", ["on battery", "in use (2 min idle, needs 10)"], now=WED_NIGHT)
        self.assertEqual((doc["host"], doc["state"], doc["at"]), ("macbook", "waiting", "2026-10-28T22:00:00Z"))
        self.assertIn("on battery", doc["why"])

    def test_it_pulls_before_the_guards(self):
        # A stuck guard must not keep the MacBook on old code: pull_main runs first in each job's run_one().
        src = pathlib.Path(mw.__file__).read_text()
        body = src[src.index("def run_one() -> str:"):]
        self.assertLess(body.index("pull_main()"), body.index("guards()"))


class BackToMain(unittest.TestCase):
    # These clones have no remote: bringing main up to date is stubbed, every other git call is real.
    OK_FF = staticmethod(lambda repo, own=True: subprocess.CompletedProcess([], 0, "", ""))

    def repo(self, root, name):
        r = pathlib.Path(root) / name
        r.mkdir(parents=True)
        for cmd in (["init", "-q", "-b", "main"], ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "x"],
                    ["checkout", "-q", "-b", "macbook/j1194-work"]):
            subprocess.run(["git", "-C", str(r)] + cmd, check=True)
        return r

    def test_its_own_clone_left_on_a_work_branch_goes_back_to_main(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.object(mw, "WORKER_DIR", pathlib.Path(t)), \
                mock.patch.object(mw, "OTHERS", [pathlib.Path(t) / "none"]), mock.patch.object(mw, "log"):
            r = self.repo(t, "orbit-with-ben")
            real = mw.sh  # no remote to pull from here: the pull itself is stubbed, every other git call is real
            fake = lambda cmd, **k: subprocess.CompletedProcess(cmd, 0, "", "") if "pull" in cmd else real(cmd, **k)
            with mock.patch.object(mw, "STUDIO", r), mock.patch.object(mw, "sh", fake), mock.patch.object(mw, "ff_main", self.OK_FF):
                self.assertEqual(mw.pull_main(), "")
            self.assertEqual(subprocess.run(["git", "-C", str(r), "branch", "--show-current"], capture_output=True, text=True).stdout.strip(), "main")

    def test_its_own_clone_left_dirty_on_a_work_branch_stashes_and_goes_back_to_main(self):
        # 5 Nov 2026: J2165 left macbook/J2165 dirty and every later MacBook run errored.
        with tempfile.TemporaryDirectory() as t, mock.patch.object(mw, "WORKER_DIR", pathlib.Path(t)), \
                mock.patch.object(mw, "OTHERS", [pathlib.Path(t) / "none"]), mock.patch.object(mw, "log"):
            r = self.repo(t, "orbit-with-ben")
            (r / "half_done.md").write_text("unfinished\n")
            real = mw.sh
            fake = lambda cmd, **k: subprocess.CompletedProcess(cmd, 0, "", "") if "pull" in cmd else real(cmd, **k)
            with mock.patch.object(mw, "STUDIO", r), mock.patch.object(mw, "sh", fake), mock.patch.object(mw, "ff_main", self.OK_FF):
                self.assertEqual(mw.pull_main(), "")
            run = lambda *a: subprocess.run(["git", "-C", str(r), *a], capture_output=True, text=True).stdout.strip()
            self.assertEqual(run("branch", "--show-current"), "main")
            self.assertIn("macbook-worker autostash macbook/j1194-work", run("stash", "list"))  # kept, not lost

    def test_its_own_clone_left_dirty_on_main_stashes_so_the_next_claim_works(self):
        # 8 Nov 2026: a job left the slot's main dirty and `jobs.py next --git` refused every later claim.
        with tempfile.TemporaryDirectory() as t, mock.patch.object(mw, "WORKER_DIR", pathlib.Path(t)), \
                mock.patch.object(mw, "OTHERS", [pathlib.Path(t) / "none"]), mock.patch.object(mw, "log"):
            r = self.repo(t, "orbit-with-ben")
            subprocess.run(["git", "-C", str(r), "checkout", "-q", "main"], check=True)
            (r / "half_done.md").write_text("unfinished\n")
            real = mw.sh
            fake = lambda cmd, **k: subprocess.CompletedProcess(cmd, 0, "", "") if "pull" in cmd else real(cmd, **k)
            with mock.patch.object(mw, "STUDIO", r), mock.patch.object(mw, "sh", fake), mock.patch.object(mw, "ff_main", self.OK_FF):
                self.assertEqual(mw.pull_main(), "")
            run = lambda *a: subprocess.run(["git", "-C", str(r), *a], capture_output=True, text=True).stdout.strip()
            self.assertEqual(run("status", "--porcelain"), "")
            self.assertIn("macbook-worker autostash main", run("stash", "list"))  # kept, not lost

    def test_bens_dirty_checkout_is_never_stashed(self):
        with tempfile.TemporaryDirectory() as t, tempfile.TemporaryDirectory() as w, \
                mock.patch.object(mw, "WORKER_DIR", pathlib.Path(w)), mock.patch.object(mw, "OTHERS", [pathlib.Path(t) / "none"]):
            r = self.repo(t, "orbit-with-ben")
            subprocess.run(["git", "-C", str(r), "checkout", "-q", "main"], check=True)
            (r / "bens_work.md").write_text("mine\n")
            real = mw.sh
            fake = lambda cmd, **k: subprocess.CompletedProcess(cmd, 0, "", "") if "pull" in cmd else real(cmd, **k)
            with mock.patch.object(mw, "STUDIO", r), mock.patch.object(mw, "sh", fake), mock.patch.object(mw, "ff_main", self.OK_FF):
                mw.pull_main()
            self.assertTrue((r / "bens_work.md").exists())
            self.assertEqual(subprocess.run(["git", "-C", str(r), "stash", "list"], capture_output=True, text=True).stdout.strip(), "")

    def test_it_pulls_origin_main_by_name(self):
        # 8 Nov 2026: slot 2's clone had two branch.main.merge entries and a bare `git pull` failed with
        # "Cannot fast-forward to multiple branches"; every pull names origin main.
        src = pathlib.Path(mw.__file__).read_text()
        self.assertNotIn('"pull", "-q", "--ff-only"]', src)
        self.assertIn('"pull", "-q", "--ff-only", "origin", "main"]', src)

    def test_a_quick_clean_exit_with_the_job_still_open_pauses_the_agent(self):
        # 9 Nov 2026: claude (out of usage) exited 0 in about a minute, and J2421 was claimed and released every minute.
        self.assertTrue(mw.failed_run(0, 45, True))
        self.assertFalse(mw.failed_run(0, 45, False), "finished the job quickly: fine")
        self.assertFalse(mw.failed_run(0, 900, True), "worked a while and left it open: picked up again, not paused")
        self.assertFalse(mw.failed_run(124, 1500, True), "hit the cap: slow, not broken")
        self.assertTrue(mw.failed_run(1, 900, True))

    def test_its_own_clone_ahead_of_github_after_a_good_pull_is_rescued(self):
        # 9 Nov 2026: the pull succeeded but main kept an unpublished queue commit, and every claim refused.
        with tempfile.TemporaryDirectory() as t, mock.patch.object(mw, "WORKER_DIR", pathlib.Path(t)), \
                mock.patch.object(mw, "OTHERS", [pathlib.Path(t) / "none"]), mock.patch.object(mw, "log"):
            r = self.repo(t, "orbit-with-ben")
            subprocess.run(["git", "-C", str(r), "checkout", "-q", "main"], check=True)
            calls = []
            real = mw.sh
            fake = lambda cmd, **k: subprocess.CompletedProcess(cmd, 0, "", "") if "pull" in cmd else real(cmd, **k)
            with mock.patch.object(mw, "STUDIO", r), mock.patch.object(mw, "sh", fake), mock.patch.object(mw, "ff_main", self.OK_FF), \
                    mock.patch.object(mw, "rescue_diverged", lambda repo: calls.append(repo) or False):
                self.assertEqual(mw.pull_main(), "")
            self.assertEqual(calls, [r])

    def test_bens_own_checkout_is_never_switched(self):
        with tempfile.TemporaryDirectory() as t, tempfile.TemporaryDirectory() as w, \
                mock.patch.object(mw, "WORKER_DIR", pathlib.Path(w)), mock.patch.object(mw, "OTHERS", [pathlib.Path(t) / "none"]):
            r = self.repo(t, "orbit-with-ben")
            with mock.patch.object(mw, "STUDIO", r):
                self.assertIn("not main", mw.pull_main())
            self.assertEqual(subprocess.run(["git", "-C", str(r), "branch", "--show-current"], capture_output=True, text=True).stdout.strip(), "macbook/j1194-work")


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


class AllAgents(unittest.TestCase):
    """Ben, 4 Nov 2026: "get all the agents working on the MacBook Pro, the Gemini agents, the Cursor agents, the
    Claude agents, and the Codex agents"."""
    def setUp(self):
        os.environ.pop("MACBOOK_AGENT", None)

    def test_the_job_chain_picks_the_first_installed_agent(self):
        review = {"kind": "review"}       # Claude -> Cursor-on-Claude -> Gemini Argon -> Codex
        self.assertEqual(mw.pick_agent(review, ["codex", "gemini", "claude", "cursor"])[0], "claude")
        self.assertEqual(mw.pick_agent(review, ["codex", "gemini"]), ("gemini", "gemini-argon"))
        self.assertEqual(mw.pick_agent({"kind": "thumb"}, ["gemini", "codex"]), ("codex", "gpt-6-astra"))

    def test_credit_flagged_agent_is_skipped(self):
        import routing
        old = set(routing.OUT)
        try:
            routing.OUT = {"claude"}
            self.assertEqual(mw.pick_agent({"kind": "review"}, ["claude", "gemini"]), ("gemini", "gemini-argon"))
        finally:
            routing.OUT = old

    def test_no_cli_installed_means_no_agent(self):
        self.assertEqual(mw.pick_agent({"kind": "review"}, []), ("", ""))

    def test_a_kind_with_no_installed_lane_falls_back_to_any_installed_cli(self):
        self.assertEqual(mw.pick_agent({"kind": "vo"}, ["claude"]), ("claude", ""))

    def test_a_job_for_the_minis_claude_code_runs_on_the_macbooks_claude(self):
        self.assertEqual(mw.pick_agent({"kind": "review", "for": "claudecode"}, ["codex", "claude"])[0], "claude")

    def test_a_studio_job_is_not_run_on_the_macbooks_claude(self):
        # 9 Nov this picked Claude; on 10 Nov Claude handed two Studio jobs straight back (see StudioJobs below).
        self.assertEqual(mw.pick_agent({"kind": "studio"}, ["claude"]), ("", ""))
        self.assertEqual(mw.pick_agent({"kind": "studio"}, ["claude", "gemini"])[0], "gemini")

    def test_pin_keeps_the_old_single_agent_setting(self):
        with mock.patch.dict(os.environ, {"MACBOOK_AGENT": "codex"}):
            self.assertEqual(mw.pick_agent({"kind": "review"}, ["codex", "claude"])[0], "codex")
            self.assertEqual(mw.pick_agent({"kind": "review"}, ["claude"]), ("", ""))

    def test_each_cli_gets_its_one_shot_form(self):
        with mock.patch.object(mw, "find_bin", side_effect=lambda a: "/bin/" + a):
            g = mw.agent_cmd("gemini", "P", "gemini-argon")
            self.assertEqual(g[-2:], ["-p", "P"])
            self.assertIn("--model", g)
            self.assertEqual(mw.agent_cmd("cursor", "P", "cursor-grok-4-7")[:3], ["/bin/cursor", "-p", "--force"])
            self.assertIn("-m", mw.agent_cmd("codex", "P", "gpt-6-astra"))
            c = mw.agent_cmd("claude", "P")
            self.assertEqual(c[:3], ["/bin/claude", "-p", "P"])  # prompt before the variadic --add-dir lists
            self.assertNotEqual(c[-1], "P")
            self.assertIsNone(mw.agent_cmd("grok", "P"))

    def test_unattended_claude_may_run_tests_and_open_a_pr_but_not_merge(self):
        # J2427 bounced ~40 times on 9 Nov: unittest and gh pr create needed approval with nobody at the Mac.
        with mock.patch.object(mw, "find_bin", side_effect=lambda a: "/bin/" + a):
            c = mw.agent_cmd("claude", "P")
        allowed = c[c.index("--allowedTools") + 1].split(",")
        for rule in ("Bash(python3 -m unittest:*)", "Bash(gh pr create:*)", "Bash(git push:*)", "Bash(git fetch:*)"):
            self.assertIn(rule, allowed)   # git fetch: Ben, 10 Nov 2026, after J2495 could not read the PR heads
        self.assertFalse(any("merge" in r or "pull" in r for r in allowed))   # fetch reads; nothing here changes a branch
        self.assertLess(c.index("--allowedTools"), c.index("--add-dir"))

    def test_a_failed_cli_is_paused_and_skipped(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d, mock.patch.object(mw, "DOWN", pathlib.Path(d) / "down.json"), \
                mock.patch.object(mw, "STATE", pathlib.Path(d)):
            until = mw.mark_down("cursor", now=T0)
            self.assertEqual(mw.usable(["codex", "cursor"], now=T0), ["codex"])
            self.assertEqual(mw.usable(["codex", "cursor"], now=T0 + dt.timedelta(hours=3)), ["codex", "cursor"])
            self.assertIn("cursor", mw.down_agents(T0))
            self.assertTrue(until.startswith("2026-10-28T14:00"))

    def test_run_keeps_taking_jobs_until_idle(self):
        import tempfile
        seq = iter(["ran", "ran", "idle"])
        with tempfile.TemporaryDirectory() as d, mock.patch.object(mw, "STATE", pathlib.Path(d)), \
                mock.patch.object(mw, "run_one", side_effect=lambda: next(seq)) as one:
            self.assertEqual(mw.run(), 0)
            self.assertEqual(one.call_count, 3)

    def test_run_stops_at_its_loop_budget(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d, mock.patch.object(mw, "STATE", pathlib.Path(d)), \
                mock.patch.dict(os.environ, {"MACBOOK_LOOP_MIN": "0"}), \
                mock.patch.object(mw, "run_one", return_value="ran") as one:
            self.assertEqual(mw.run(), 0)
            self.assertEqual(one.call_count, 1)

    def test_checkouts_are_the_workers_own_never_bens(self):
        # Whichever slot runs this test (J2235 F-01c: it failed inside slot 2), the checkout is that slot's own folder.
        for slot in (1, 2):
            with mock.patch.object(mw, "SLOT", slot):
                own = mw.slot_dir(slot) / "history-of-science"
                with mock.patch.dict(os.environ, {"HOS_REPO": str(mw.HOME / "YouTube" / "History Of Science")}):
                    self.assertEqual(mw.own_checkout("HOS_REPO", "history-of-science"), own)
                with mock.patch.dict(os.environ, {"HOS_REPO": str(own)}):
                    self.assertEqual(mw.own_checkout("HOS_REPO", "history-of-science"), own)
        self.assertEqual(mw.slot_dir(1), mw.WORKER_DIR)

    def test_installed_honours_macbook_agents_and_what_exists(self):
        with mock.patch.object(mw, "find_bin", side_effect=lambda a: "/x" if a in ("codex", "claude") else None):
            self.assertEqual(mw.installed(), ["codex", "claude"])
            self.assertEqual(mw.installed("claude,gemini"), ["claude"])


class StudioJobs(unittest.TestCase):
    """10 Nov 2026: the MacBook's Claude Code handed J2460 and J2461 straight back. Its unattended allowlist cannot
    reach the Studio browser, and its launch rule still said never to change anything on YouTube."""

    JOB = {"id": "J9", "needs": "mini", "kind": "studio", "repo": "owb", "title": "Studio: set the end screen on a long",
           "body": "In Orbit Studio, set the end screen."}

    def test_a_studio_job_runs_on_gemini_and_never_on_claude(self):
        with mock.patch.dict(os.environ, {"MACBOOK_CDP": "9223,9222"}):
            self.assertTrue(mw.is_studio_job(self.JOB))
            self.assertEqual(mw.pick_agent(self.JOB, ["claude", "codex", "gemini"])[0], "gemini")
            self.assertEqual(mw.pick_agent(self.JOB, ["claude", "codex"])[0], "codex")
            self.assertEqual(mw.pick_agent(self.JOB, ["claude"]), ("", ""))
            self.assertFalse(mw.is_studio_job(dict(self.JOB, needs="any", kind="review")))
            self.assertTrue(mw.is_studio_job(dict(self.JOB, needs="macbook")))  # sent to this Mac's own window

    def test_studio_jobs_are_not_offered_when_only_claude_is_here(self):
        seen = {}

        def fake_sh(args, cwd=None, timeout=300):
            if "next" in args:
                seen["cdp"] = os.environ.get("MACBOOK_CDP")
                return subprocess.CompletedProcess(args, 10, "", "")
            return subprocess.CompletedProcess(args, 0, "", "")
        for have, want in ((["claude"], ""), (["claude", "gemini"], "9223,9222")):
            with mock.patch.dict(os.environ), \
                    mock.patch.object(mw, "sh", side_effect=fake_sh), mock.patch.object(mw, "push_heartbeat"), \
                    mock.patch.object(mw, "cdp_ports_up", return_value=["9223", "9222"]), \
                    mock.patch.object(mw, "installed", return_value=have), mock.patch.object(mw, "usable", side_effect=lambda h: h):
                self.assertEqual(mw.run_ordinary(), "idle")
                self.assertEqual(seen["cdp"], want, have)

    def test_the_launch_rule_allows_a_routed_studio_job_but_never_an_upload(self):
        self.assertNotIn("change anything on YouTube", mw.PROMPT)
        self.assertIn("never upload a video, change a video's privacy or schedule, or delete a video", mw.PROMPT)
        self.assertIn("YouTube Studio job the Chief routed to this Mac", mw.PROMPT)


class AddressedJobs(unittest.TestCase):
    def test_a_job_for_one_agent_runs_that_agents_cli(self):
        self.assertEqual(mw.pick_agent({"kind": "script", "for": "gemini"}, ["codex", "gemini", "claude"])[0], "gemini")
        self.assertEqual(mw.pick_agent({"kind": "script", "for": "cursor"}, ["codex"])[0], "codex")  # not installed: chain



class Diverged(unittest.TestCase):
    def test_a_diverged_own_main_is_kept_on_a_branch_and_reset(self):
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            g = lambda *a, cwd: subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout  # noqa: E731
            g("init", "-q", "--bare", "-b", "main", str(t / "origin.git"), cwd=t)
            g("clone", "-q", str(t / "origin.git"), str(t / "a"), cwd=t)
            for c in ("a",):
                g("config", "user.email", "x@y", cwd=t / c); g("config", "user.name", "x", cwd=t / c)
            (t / "a" / "f").write_text("1"); g("add", "f", cwd=t / "a"); g("commit", "-qm", "one", cwd=t / "a")
            g("push", "-q", "origin", "main", cwd=t / "a")
            g("clone", "-q", str(t / "origin.git"), str(t / "b"), cwd=t)
            g("config", "user.email", "x@y", cwd=t / "b"); g("config", "user.name", "x", cwd=t / "b")
            (t / "a" / "f").write_text("2"); g("commit", "-qam", "upstream", cwd=t / "a"); g("push", "-q", "origin", "main", cwd=t / "a")
            (t / "b" / "g").write_text("mine"); g("add", "g", cwd=t / "b"); g("commit", "-qm", "local only", cwd=t / "b")
            self.assertTrue(mw.rescue_diverged(t / "b"))
            self.assertEqual(g("rev-parse", "main", cwd=t / "b"), g("rev-parse", "origin/main", cwd=t / "b"))
            kept = g("branch", "-r", cwd=t / "b") + g("branch", cwd=t / "b")
            self.assertIn("macbook-worker/rescue-", kept)
            self.assertFalse(mw.rescue_diverged(t / "b"))  # nothing left to rescue

    def _diverged_clone(self, t):
        g = lambda *a, cwd: subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout  # noqa: E731
        g("init", "-q", "--bare", "-b", "main", str(t / "origin.git"), cwd=t)
        for c in ("a", "b"):
            g("clone", "-q", str(t / "origin.git"), str(t / c), cwd=t)
            g("config", "user.email", "x@y", cwd=t / c); g("config", "user.name", "x", cwd=t / c)
        (t / "a" / "f").write_text("1"); g("add", "f", cwd=t / "a"); g("commit", "-qm", "one", cwd=t / "a")
        g("push", "-q", "origin", "main", cwd=t / "a")
        g("pull", "-q", "origin", "main", cwd=t / "b")
        (t / "a" / "f").write_text("2"); g("commit", "-qam", "upstream", cwd=t / "a"); g("push", "-q", "origin", "main", cwd=t / "a")
        (t / "b" / "g").write_text("mine"); g("add", "g", cwd=t / "b"); g("commit", "-qm", "local only", cwd=t / "b")
        return g

    def test_a_clone_with_broken_branch_settings_still_follows_main(self):
        """8 and 10 Nov 2026, slot 2: `git pull origin main` died with "Cannot fast-forward to multiple branches"."""
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            g = lambda *a, cwd: subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout  # noqa: E731
            g("init", "-q", "--bare", "-b", "main", str(t / "origin.git"), cwd=t)
            for c in ("a", "b"):
                g("clone", "-q", str(t / "origin.git"), str(t / c), cwd=t)
                g("config", "user.email", "x@y", cwd=t / c); g("config", "user.name", "x", cwd=t / c)
            (t / "a" / "f").write_text("1"); g("add", "f", cwd=t / "a"); g("commit", "-qm", "one", cwd=t / "a")
            g("push", "-q", "origin", "main", cwd=t / "a")
            g("pull", "-q", "origin", "main", cwd=t / "b")
            g("push", "-q", "origin", "main:other", cwd=t / "a")
            # the damage: two merge targets for main, and no fetch refspec at all
            g("config", "--add", "branch.main.merge", "refs/heads/other", cwd=t / "b")
            g("config", "--unset-all", "remote.origin.fetch", cwd=t / "b")
            (t / "a" / "f").write_text("2"); g("commit", "-qam", "upstream", cwd=t / "a"); g("push", "-q", "origin", "main", cwd=t / "a")
            r = mw.ff_main(t / "b")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(g("rev-parse", "main", cwd=t / "b"), g("rev-parse", "main", cwd=t / "a"))
            self.assertEqual((t / "b" / "f").read_text(), "2")

    def test_a_stale_index_lock_is_moved_aside_and_the_rescue_goes_through(self):
        """10 Nov 2026: slot 2 sat in error for an hour. A git killed mid-write leaves .git/index.lock, and reset fails."""
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            g = self._diverged_clone(t)
            lock = t / "b" / ".git" / "index.lock"
            lock.write_text("")
            old = time.time() - mw.STALE_LOCK_S - 60
            os.utime(lock, (old, old))
            self.assertTrue(mw.rescue_diverged(t / "b"))
            self.assertFalse(lock.exists())
            self.assertTrue(list((t / "b" / ".git").glob("index.lock.stale-*")))  # moved aside, not deleted
            self.assertEqual(g("rev-parse", "main", cwd=t / "b"), g("rev-parse", "origin/main", cwd=t / "b"))

    def _behind_clone(self, t):
        g = lambda *a, cwd: subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout  # noqa: E731
        g("init", "-q", "--bare", "-b", "main", str(t / "origin.git"), cwd=t)
        for c in ("a", "b"):
            g("clone", "-q", str(t / "origin.git"), str(t / c), cwd=t)
            g("config", "user.email", "x@y", cwd=t / c); g("config", "user.name", "x", cwd=t / c)
        (t / "a" / "f").write_text("1"); g("add", "f", cwd=t / "a"); g("commit", "-qm", "one", cwd=t / "a")
        g("push", "-q", "origin", "main", cwd=t / "a")
        g("pull", "-q", "origin", "main", cwd=t / "b")
        (t / "a" / "f").write_text("2"); g("commit", "-qam", "upstream", cwd=t / "a"); g("push", "-q", "origin", "main", cwd=t / "a")
        return g

    def test_a_stale_index_lock_in_a_clone_that_is_only_behind_does_not_stop_the_pull(self):
        """10 Nov 2026, slot 1: 'pull failed ... Another git process seems to be running ... remove the file manually'.
        The clone had nothing of its own to rescue, so the lock was never looked at and every run errored."""
        with tempfile.TemporaryDirectory() as t, mock.patch.object(mw, "log"):
            t = pathlib.Path(t)
            g = self._behind_clone(t)
            lock = t / "b" / ".git" / "index.lock"
            lock.write_text("")
            old = time.time() - mw.STALE_LOCK_S - 60
            os.utime(lock, (old, old))
            with mock.patch.object(mw, "WORKER_DIR", t), mock.patch.object(mw, "STUDIO", t / "b"), \
                    mock.patch.object(mw, "OTHERS", [t / "none"]):
                self.assertEqual(mw.pull_main(), "")
            self.assertFalse(lock.exists())
            self.assertTrue(list((t / "b" / ".git").glob("index.lock.stale-*")))  # moved aside, not deleted
            self.assertEqual(g("rev-parse", "main", cwd=t / "b"), g("rev-parse", "main", cwd=t / "a"))
            self.assertEqual((t / "b" / "f").read_text(), "2")

    def test_a_fresh_index_lock_is_left_alone_and_the_pull_says_why(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.object(mw, "log"):
            t = pathlib.Path(t)
            self._behind_clone(t)
            lock = t / "b" / ".git" / "index.lock"
            lock.write_text("")   # a git may really be running: never touched inside STALE_LOCK_S
            with mock.patch.object(mw, "WORKER_DIR", t), mock.patch.object(mw, "STUDIO", t / "b"), \
                    mock.patch.object(mw, "OTHERS", [t / "none"]):
                self.assertIn("pull failed in b", mw.pull_main())
            self.assertTrue(lock.exists())
            self.assertEqual((t / "b" / "f").read_text(), "1")

    def test_a_failed_reset_says_why_and_the_same_commit_gets_one_rescue_branch(self):
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            g = self._diverged_clone(t)
            lock = t / "b" / ".git" / "index.lock"
            lock.write_text("")   # a fresh lock: a git may really be running, so it is left alone
            self.assertFalse(mw.rescue_diverged(t / "b"))
            self.assertIn("git reset failed", mw.RESCUE_WHY)
            self.assertIn("kept on macbook-worker/rescue-", mw.RESCUE_WHY)
            self.assertFalse(mw.rescue_diverged(t / "b"))
            self.assertEqual(len(g("branch", "--list", "macbook-worker/rescue-*", cwd=t / "b").split()), 1)
            lock.unlink()
            self.assertTrue(mw.rescue_diverged(t / "b"))
            self.assertEqual(len(g("branch", "--list", "macbook-worker/rescue-*", cwd=t / "b").split()), 1)
            self.assertEqual(mw.RESCUE_WHY, "")


class TwoSlots(unittest.TestCase):
    """Ben, 5 Nov 2026: two jobs at once on the MacBook Pro, one on the Mini, one in the cloud."""

    def test_slot_one_starts_slot_two_in_its_own_clones(self):
        calls = []
        with mock.patch.object(mw, "SLOT", 1), mock.patch.object(mw, "SLOTS", 2), \
                mock.patch.object(mw, "HOME", pathlib.Path(tempfile.mkdtemp())):
            self.assertEqual(mw.start_other_slots(popen=lambda cmd, **kw: calls.append(kw["env"]), system="Darwin"), [2])
        env = calls[0]
        self.assertEqual(env["MACBOOK_SLOT"], "2")
        self.assertTrue(env["OWB_REPO"].endswith("worker/slot2/orbit-with-ben"))
        self.assertTrue(env["HOS_REPO"].endswith("worker/slot2/history-of-science"))

    def test_no_second_slot_off_the_mac_or_from_slot_two(self):
        never = lambda *a, **k: self.fail("started a slot")  # noqa: E731
        with mock.patch.object(mw, "SLOT", 1), mock.patch.object(mw, "SLOTS", 2):
            self.assertEqual(mw.start_other_slots(popen=never, system="Linux"), [])
        with mock.patch.object(mw, "SLOT", 1), mock.patch.object(mw, "SLOTS", 1):
            self.assertEqual(mw.start_other_slots(popen=never, system="Darwin"), [])
        with mock.patch.object(mw, "SLOT", 2):
            self.assertEqual(mw.start_other_slots(popen=never, system="Darwin"), [])

    def test_each_slot_has_its_own_id_lock_heartbeat_and_clone(self):
        self.assertEqual((mw.slot_name(1, "macbook"), mw.slot_name(2, "macbook")), ("macbook", "macbook-2"))
        self.assertEqual(mw.slot_name(2, "macbook-heartbeat"), "macbook-heartbeat-2")
        self.assertEqual(mw.slot_dir(2), mw.WORKER_DIR / "slot2")
        self.assertEqual(mw.slot_dir(1), mw.WORKER_DIR)

    def test_slot_two_waits_while_the_machine_is_busy(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.object(mw, "STATE", pathlib.Path(t)), \
                mock.patch.object(mw, "SLOT", 2), mock.patch.object(mw.os, "cpu_count", return_value=10):
            self.assertEqual(mw.guards(AC, IDLE_20, free_gb=100, now=WED_NIGHT, load=3.0), [])
            self.assertIn("slot 2 waits", " ".join(mw.guards(AC, IDLE_20, free_gb=100, now=WED_NIGHT, load=7.0)))
        with tempfile.TemporaryDirectory() as t, mock.patch.object(mw, "STATE", pathlib.Path(t)), \
                mock.patch.object(mw, "SLOT", 1):
            self.assertEqual(mw.guards(AC, IDLE_20, free_gb=100, now=WED_NIGHT, load=50.0), [])  # slot 1 never

    def test_slot_two_claims_macbook_jobs_like_slot_one(self):
        j = {"id": "J0001", "title": "t", "needs": "macbook", "status": "open", "history": []}
        self.assertTrue(jobs.is_macbook("macbook-2") and jobs.is_macbook("macbook"))
        self.assertFalse(jobs.is_macbook("macbookish") or jobs.is_macbook("codex"))
        self.assertTrue(jobs.claimable({"jobs": [j]}, j, {"macbook", "any"}, T0, "macbook-2"))


class OnePublisher(unittest.TestCase):
    """J2541, 10 Nov 2026: the board is published by the Mini only. The MacBook has ~/_desk/state/chief, so every
    jobs.py call here also force-pushed board-data."""

    def test_a_run_turns_the_board_publish_off_for_everything_it_starts(self):
        slot_envs = []
        with tempfile.TemporaryDirectory() as t, mock.patch.dict(os.environ, {"BOARD_PUBLISH": "1"}), \
                mock.patch.object(mw, "STATE", pathlib.Path(t)), mock.patch.object(mw, "run_one", return_value="idle"), \
                mock.patch.object(mw, "start_other_slots", side_effect=lambda: slot_envs.append(dict(os.environ))):
            self.assertEqual(mw.run(), 0)
            self.assertEqual(slot_envs[0]["BOARD_PUBLISH"], "0")      # slot 2 is started with it
            out = pathlib.Path(t) / "seen"
            mw.run_capped(["sh", "-c", f'printf %s "$BOARD_PUBLISH" > {out}'], t, 10)   # the woken agent
            self.assertEqual(out.read_text(), "0")
            self.assertEqual(mw.sh(["sh", "-c", 'printf %s "$BOARD_PUBLISH"']).stdout, "0")   # its own jobs.py calls

    def test_jobs_py_does_not_start_the_publisher_when_it_is_off(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.object(jobs.chief_relay, "STATE", pathlib.Path(t)), \
                mock.patch.object(jobs.subprocess, "Popen") as popen:
            with mock.patch.dict(os.environ, {"BOARD_PUBLISH": "0"}):
                jobs.publish_board()
            popen.assert_not_called()
            with mock.patch.dict(os.environ, {"BOARD_PUBLISH": "1"}):
                jobs.publish_board()      # the Mini: state folder there, hook on
            self.assertEqual(popen.call_count, 1)


class LaunchAgent(unittest.TestCase):
    def test_worker_looks_every_three_minutes(self):
        # 6 Nov 2026: 900 s left a free MacBook idle while portable reviews waited.
        plist = (pathlib.Path(__file__).resolve().parent / "macbook" / "com.owb.macbook-worker.plist").read_text()
        self.assertIn("<key>StartInterval</key>\n  <integer>180</integer>", plist)
        self.assertNotIn("<integer>900</integer>", plist)


ALLOWED_BEFORE_J2526 = 11   # len(CLAUDE_ALLOWED_TOOLS) on main before the worker stopped naming channels


class AsksTheChannelLoader(unittest.TestCase):
    """J2526: the worker names no channel. Its clones, its brief and its Studio ports come from the channel files,
    so today's two channels behave exactly as before and a third needs no edit here."""

    def sky(self):
        import channels
        base = channels._load()
        home = next(c for c in base if c.get("home"))
        sky = dict(home, slug="sky", label="SKY", name="Night Sky", short="Sky", home=False, order=3,
                   title_match=r"\bSKY\b", youtube={"studio_port": "9300"},
                   repo={"url": "https://github.com/example/night-sky.git", "env": "SKY_REPO", "checkouts": ["Night Sky"]})
        return mock.patch.object(channels, "_load", lambda directory=None: base + (sky,))

    def test_the_brief_reads_as_it_always_did_for_todays_channels(self):
        with mock.patch.object(mw, "STUDIO", "/o"), mock.patch.object(mw, "OTHERS", ["/h"]), \
                mock.patch.object(mw, "AGENT_ID", "macbook-2"):
            p = mw.brief("J1102", "qwen3:14b", 25)
        for line in (
            '1. Orbit With Ben (/o) is pulled. Read AGENTS.md (the rules, the Never list, "Stop and ask Ben") and then',
            "   For a HOS job, work in the HOS checkout (/h) and follow its AGENTS.md.",
            "   History of Science folder must always be left on main.",
            "  window on CDP port 9223 (Orbit With Ben) or 9222 (History of Science), check the channel name first, and touch",
            "- keep files inside the two checkouts and ~/_desk; leave nothing running when you stop.",
            "     python3 scripts/jobs.py show J1102",
            "Your run is killed at 25 minutes:",
        ):
            self.assertIn(line + ("\n" if not line.endswith(":") else ""), p)
        self.assertNotIn("{", p)                                   # every placeholder was filled

    def test_clones_urls_and_ports_come_from_the_channel_files(self):
        self.assertEqual(mw.URLS, {"orbit-with-ben": "https://github.com/TheLaughingGod1986/orbit-with-ben.git",
                                   "history-of-science": "https://github.com/TheLaughingGod1986/history-of-science.git"})
        self.assertEqual(mw.STUDIO.name, "orbit-with-ben")
        self.assertEqual([p.name for p in mw.OTHERS], ["history-of-science"])
        self.assertEqual(mw.CDP_PORTS, ("9223", "9222"))
        # the clone's folder is the repo's name on GitHub, not the name of Ben's own folder for it
        self.assertEqual(mw.clone_name("hos"), "history-of-science")

    def test_a_third_channel_gets_its_own_clone_its_line_in_the_brief_and_its_port(self):
        with self.sky():
            self.assertEqual(mw.other_slugs(), ["hos", "sky"])
            self.assertEqual(mw.clone_name("sky"), "night-sky")
            with mock.patch.dict(os.environ, {"SKY_REPO": str(mw.HOME / "YouTube" / "Night Sky")}):
                self.assertEqual(mw.channel_clone("sky"), mw.slot_dir(mw.SLOT) / "night-sky")   # never Ben's folder
            with mock.patch.object(mw, "STUDIO", "/o"), mock.patch.object(mw, "OTHERS", ["/h", "/s"]):
                p = mw.brief("J1", "m", 25)
            self.assertIn("   For a HOS job, work in the HOS checkout (/h) and follow its AGENTS.md.\n"
                          "   For a SKY job, work in the SKY checkout (/s) and follow its AGENTS.md.\n", p)
            self.assertIn("History of Science and Night Sky folders must always be left on main", p)
            self.assertIn("9223 (Orbit With Ben) or 9222 (History of Science) or 9300 (Night Sky)", p)
            self.assertIn("inside the three checkouts", p)

    def test_a_third_channel_reaches_the_agent_and_the_second_slot(self):
        with self.sky():
            with mock.patch.object(mw, "OTHERS", [pathlib.Path("/h"), pathlib.Path("/s")]), \
                    mock.patch.object(mw, "find_bin", side_effect=lambda a: "/bin/" + a):
                c = mw.agent_cmd("claude", "P")
            dirs = [c[i + 1] for i, x in enumerate(c) if x == "--add-dir"]
            self.assertEqual(dirs, ["/h", "/s", str(mw.HOME / "_desk")])
            calls = []
            with mock.patch.object(mw, "SLOT", 1), mock.patch.object(mw, "SLOTS", 2), \
                    mock.patch.object(mw, "HOME", pathlib.Path(tempfile.mkdtemp())):
                mw.start_other_slots(popen=lambda cmd, **kw: calls.append(kw["env"]), system="Darwin")
            self.assertTrue(calls[0]["SKY_REPO"].endswith("worker/slot2/night-sky"))
            self.assertTrue(calls[0]["HOS_REPO"].endswith("worker/slot2/history-of-science"))

    def test_a_channel_with_no_repo_url_yet_does_not_stop_the_worker(self):
        import channels
        base = channels._load()
        bare = dict(next(c for c in base if c.get("home")), slug="new", label="NEW", name="New One", home=False,
                    order=9, title_match=r"\bNEW\b", youtube={}, repo={"env": "NEW_REPO", "checkouts": ["new-one"]})
        with mock.patch.object(channels, "_load", lambda directory=None: base + (bare,)):
            self.assertEqual(mw.clone_name("new"), "new")
            self.assertEqual(mw.channel_clone("new"), mw.slot_dir(mw.SLOT) / "new")
            with mock.patch.object(mw, "STUDIO", "/o"), mock.patch.object(mw, "OTHERS", ["/h", "/n"]):
                self.assertIn("9223 (Orbit With Ben) or 9222 (History of Science), check", mw.brief("J1", "m", 25))

    def test_the_unattended_tool_list_is_not_widened(self):
        # the list an unattended Claude may use without asking, as it stood before this change
        self.assertEqual(len(mw.CLAUDE_ALLOWED_TOOLS), ALLOWED_BEFORE_J2526)
        self.assertFalse(any("merge" in r or "pull" in r for r in mw.CLAUDE_ALLOWED_TOOLS))


if __name__ == "__main__":
    unittest.main()
