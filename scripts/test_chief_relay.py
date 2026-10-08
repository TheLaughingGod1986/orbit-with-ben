"""chief_relay.py: the first agent in the chain that is up acts as Chief; out of credit falls through; Grok takes back."""
import datetime as dt, os, pathlib, stat, sys, tempfile, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chief_relay as cr  # noqa: E402

T0 = dt.datetime(2026, 10, 7, 12, 0, tzinfo=dt.timezone.utc)
MIN = dt.timedelta(minutes=1)


class Relay(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.old_state, self.old_home, self.old_fetch, self.old_owb = cr.STATE, cr.HOME, cr.fetch_comments, cr.OWB
        cr.STATE, cr.HOME = self.tmp / "state", self.tmp  # so a real CLI on this machine can't stand in for a fake
        cr.OWB = self.tmp / "no-owb"  # never the live queue: an addressed job there (J0071, 9 Oct) changed who ran
        self.thread = []  # fake studio thread: (created_at, body)
        cr.fetch_comments = lambda since: [{"created_at": t, "body": b} for t, b in self.thread if cr.parse(t) >= since]
        cr.STATE.mkdir()
        self.posts = self.tmp / "posts.txt"
        notify = self.tmp / "notify.sh"
        notify.write_text(f'#!/bin/sh\necho "$1" >> "{self.posts}"\n')
        notify.chmod(notify.stat().st_mode | stat.S_IEXEC)
        self.env = dict(os.environ)
        os.environ.update({"CHIEF_NOTIFY": str(notify), "CHIEF_HOURS": "0-24", "CHIEF_SWEEP_HOURS": "0-24", "CHIEF_CHAIN": "chief,cursor,codex",
                           "CHIEF_HEARTBEAT": "0"})  # never push a heartbeat from a test run on the Mini
        self.cursor = self.fake("cursor", 'echo "cursor did J0001"')
        self.codex = self.fake("codex", 'echo "codex did J0001"')
        os.environ["CURSOR_AGENT_BIN"], os.environ["CODEX_BIN"] = str(self.cursor), str(self.codex)

    def tearDown(self):
        cr.STATE, cr.HOME, cr.fetch_comments, cr.OWB = self.old_state, self.old_home, self.old_fetch, self.old_owb
        os.environ.clear()
        os.environ.update(self.env)

    def fake(self, name, body):
        p = self.tmp / name
        p.write_text(f"#!/bin/sh\necho ran >> {self.tmp}/{name}.ran\n{body}\n")
        p.chmod(p.stat().st_mode | stat.S_IEXEC)
        return p

    def ran(self, name):
        return (self.tmp / f"{name}.ran").exists()

    def chief(self, at=T0):
        return cr.acting(at)[1]

    def test_grok_is_chief_while_its_heartbeat_is_fresh(self):
        cr.seen("chief", T0 - 30 * MIN)
        self.assertEqual(self.chief(), "chief")
        cr.cmd_run(T0)
        self.assertFalse(self.ran("cursor"))  # Grok drives itself; nobody else runs

    def post(self, at, body):
        self.thread.append((cr.iso(at), body))

    def test_a_grok_post_on_the_thread_makes_it_chief_again(self):
        cr.cmd_run(T0)
        self.assertTrue(self.ran("cursor"))
        (self.tmp / "cursor.ran").unlink()
        self.post(T0 + 10 * MIN, "[Chief] Re 123: claimed, working")  # Grok, back with credit
        cr.cmd_run(T0 + 30 * MIN)
        self.assertFalse(self.ran("cursor"))
        self.assertEqual(self.chief(T0 + 30 * MIN), "chief")
        self.assertIn("Grok Bot is Chief again", self.posts.read_text())

    def test_cursor_codex_and_relay_posts_are_not_grok(self):
        for body in ("[Chief] [Cursor] Cursor covering. J0007 done", "[Chief] Cursor covering: J0001 started",
                     "[Chief] [Codex] Codex covering.", "[Chief] Chief relay: **Cursor is acting Chief**"):
            self.post(T0 - 5 * MIN, body)
        cr.cmd_run(T0)
        self.assertEqual(self.chief(T0), "cursor")

    def test_grok_goes_quiet_three_hours_after_its_last_post(self):
        self.post(T0 - 170 * MIN, "[Chief] Done 456")
        cr.note_grok_posts(T0)
        self.assertEqual(self.chief(T0), "chief")
        cr.note_grok_posts(T0 + 20 * MIN)
        self.assertEqual(self.chief(T0 + 20 * MIN), "cursor")

    def test_an_unreadable_thread_keeps_the_last_known_post(self):
        self.post(T0 - 10 * MIN, "[Chief] Done 456")
        cr.note_grok_posts(T0)
        def boom(since):
            raise OSError("offline")
        cr.fetch_comments = boom
        cr.note_grok_posts(T0 + 30 * MIN)
        self.assertEqual(self.chief(T0 + 30 * MIN), "chief")

    def test_a_down_mark_on_grok_clears_when_it_posts_again(self):
        cr.mark_down("chief", "out of credit", None, T0)
        self.post(T0 - 5 * MIN, "[Chief] old post, before the mark")
        cr.note_grok_posts(T0 + 1 * MIN)
        self.assertEqual(self.chief(T0 + 1 * MIN), "cursor")
        self.post(T0 + 20 * MIN, "[Chief] Re 789: claimed, working")
        cr.note_grok_posts(T0 + 25 * MIN)
        self.assertEqual(self.chief(T0 + 25 * MIN), "chief")
        self.assertFalse((cr.STATE / "chief" / "down" / "chief.json").exists())

    def test_cursor_takes_over_when_grok_goes_quiet(self):
        cr.seen("chief", T0 - 200 * MIN)
        self.assertEqual(self.chief(), "cursor")
        cr.cmd_run(T0)
        self.assertTrue(self.ran("cursor"))
        self.assertFalse(self.ran("codex"))
        self.assertIn("Cursor is acting Chief", self.posts.read_text())

    def test_out_of_credit_falls_through_to_codex_in_the_same_run(self):
        self.fake("cursor", 'echo "Error: You are out of credits. Upgrade your plan."; exit 1')
        cr.cmd_run(T0)
        self.assertTrue(self.ran("cursor"))
        self.assertTrue(self.ran("codex"))
        self.assertEqual(self.chief(cr.now()), "codex")  # Cursor stays down until its retry time
        self.assertIn("retry after", cr.state_of("cursor", cr.now())[1])
        self.assertIn("Codex is acting Chief", self.posts.read_text())

    def test_a_down_mark_expires(self):
        cr.mark_down("cursor", "out of credit", T0 + 60 * MIN, T0)
        self.assertEqual(self.chief(T0), "codex")
        self.assertEqual(self.chief(T0 + 61 * MIN), "cursor")

    def test_grok_takes_back_over_when_it_runs_jobs_again(self):
        cr.mark_down("chief", "out of credit", None, T0)
        cr.seen("chief", T0 - 10 * MIN)  # before the mark: still down
        self.assertEqual(self.chief(T0), "cursor")
        cr.seen("chief", T0 + 5 * MIN)  # Grok ran jobs.py after the mark: it's back
        self.assertEqual(self.chief(T0 + 6 * MIN), "chief")

    def test_nobody_up_posts_once_and_runs_nothing(self):
        cr.mark_down("cursor", "out of credit", None, T0)
        cr.mark_down("codex", "out of credit", None, T0)
        cr.cmd_run(T0)
        cr.cmd_run(T0 + 30 * MIN)
        self.assertFalse(self.ran("cursor") or self.ran("codex"))
        self.assertEqual(self.posts.read_text().count("nobody can act as Chief"), 1)

    def test_a_failed_thread_post_is_retried_next_run(self):
        cr.seen("chief", T0 - 200 * MIN)
        os.environ["CHIEF_NOTIFY"] = "false"  # e.g. no GitHub token under launchd
        cr.cmd_run(T0)
        self.assertFalse((cr.STATE / "chief" / "current.json").exists())
        os.environ["CHIEF_NOTIFY"] = str(self.tmp / "notify.sh")
        cr.cmd_run(T0 + 30 * MIN)
        self.assertIn("Cursor is acting Chief", self.posts.read_text())

    def test_a_missing_cli_is_skipped(self):
        os.environ["CURSOR_AGENT_BIN"] = str(self.tmp / "nope")
        os.environ["PATH"] = str(self.tmp / "empty")
        self.assertEqual(self.chief(), "codex")

    def test_an_ordinary_failure_does_not_wake_the_next_agent(self):
        self.fake("cursor", 'echo "Traceback: KeyError"; exit 1')
        cr.cmd_run(T0)
        self.assertFalse(self.ran("codex"))
        self.assertIn("run failed (exit 1)", self.posts.read_text())

    def test_a_long_job_that_mentions_quota_is_not_out_of_credit(self):
        self.assertFalse(cr.out_of_credit(0, "checked the YouTube quota exceeded warning ... " + "x" * 800))
        self.assertTrue(cr.out_of_credit(1, "usage limit reached, try again at 5pm"))
        self.assertFalse(cr.out_of_credit(124, "rate limit"))

    def test_no_wake_when_nothing_is_queued_but_a_sweep_every_two_hours(self):
        old = cr.queue_has_work
        cr.queue_has_work = lambda agent: False
        try:
            cr.seen("cursor", T0 - 30 * MIN)  # woken half an hour ago, queue empty: stay asleep
            cr.cmd_run(T0)
            self.assertFalse(self.ran("cursor"))
            cr.seen("cursor", T0 - 130 * MIN)  # two hours on: one sweep for thread/desk tasks
            cr.cmd_run(T0)
            self.assertTrue(self.ran("cursor"))
        finally:
            cr.queue_has_work = old

    def test_a_job_addressed_to_codex_wakes_codex_while_cursor_is_chief(self):
        old_owb, old_q = cr.OWB, cr.queue_has_work
        cr.OWB = self.tmp / "owb"
        (cr.OWB / "jobs").mkdir(parents=True)
        q = cr.OWB / "jobs" / "queue.json"
        q.write_text('{"jobs": [{"id": "J0071", "for": "codex", "status": "open", "needs": "any"}]}')
        cr.queue_has_work = lambda agent: True
        try:
            cr.cmd_run(T0)
            self.assertTrue(self.ran("codex"))
            self.assertFalse(self.ran("cursor"))
            self.assertEqual(self.chief(), "cursor")  # Cursor is still the acting Chief
            (self.tmp / "codex.ran").unlink()
            q.write_text('{"jobs": [{"id": "J0071", "for": "codex", "status": "done", "needs": "any"}]}')
            cr.cmd_run(T0 + 11 * MIN)
            self.assertTrue(self.ran("cursor"))
            self.assertFalse(self.ran("codex"))
        finally:
            cr.OWB, cr.queue_has_work = old_owb, old_q

    def test_a_failed_addressed_run_is_not_retried_every_tick(self):
        old_owb, old_q = cr.OWB, cr.queue_has_work
        cr.OWB = self.tmp / "owb"
        (cr.OWB / "jobs").mkdir(parents=True)
        (cr.OWB / "jobs" / "queue.json").write_text('{"jobs": [{"id": "J0071", "for": "codex", "status": "open", "needs": "any"}]}')
        self.fake("codex", 'echo "error: unexpected argument"; exit 2')
        cr.queue_has_work = lambda agent: True
        try:
            cr.cmd_run(T0)
            self.assertTrue(self.ran("codex"))
            self.assertIn("run failed (exit 2)", self.posts.read_text())
            self.assertFalse(cr.state_of("codex", cr.now())[0])  # marked down for the retry time
            (self.tmp / "codex.ran").unlink()
            cr.cmd_run(T0 + 11 * MIN)
            self.assertFalse(self.ran("codex"))
            self.assertTrue(self.ran("cursor"))  # the acting Chief carries on
        finally:
            cr.OWB, cr.queue_has_work = old_owb, old_q

    def test_a_stale_codex_flags_env_is_ignored(self):
        os.environ["CODEX_FLAGS"] = "exec -s workspace-write --approve-for-me"
        b, args = cr.cli_spec("codex")
        self.assertNotIn("-s", args)
        self.assertEqual(args[:2], ["exec", "--approve-for-me"])

    def test_pause_file_stops_runs(self):
        (cr.STATE / "chief-relay.pause").write_text("")
        cr.cmd_run(T0)
        self.assertFalse(self.ran("cursor"))

    def test_status_shows_gemini_as_the_checker(self):
        os.environ["AGY_BIN"] = str(self.cursor)
        self.assertIn("Checker: Gemini (agy found)", cr.gemini_line())

    def test_default_codex_flags_parse_on_codex_0_160(self):
        os.environ.pop("CODEX_FLAGS", None)
        _, args = cr.cli_spec("codex")
        self.assertEqual(args[:2], ["exec", "--approve-for-me"])
        self.assertFalse({"-s", "--sandbox"} & set(args))  # 0.160 refuses --sandbox with --approve-for-me

    def test_chain_order_comes_from_the_env(self):
        os.environ["CHIEF_CHAIN"] = "chief,codex,cursor"
        self.assertEqual(self.chief(), "codex")


    def test_heartbeat_is_one_parentless_commit_on_its_own_branch(self):
        import json, subprocess
        remote, repo = self.tmp / "remote.git", self.tmp / "repo"
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        for k, v in (("user.name", "t"), ("user.email", "t@t")):
            subprocess.run(["git", "-C", str(repo), "config", k, v], check=True)
        subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(remote)], check=True)
        old_owb = cr.OWB
        try:
            cr.OWB = repo
            os.environ["CHIEF_HEARTBEAT"] = "1"
            cr.push_heartbeat(T0, "idle", "cursor", "nothing queued")
            cr.push_heartbeat(T0 + 10 * MIN, "running", "cursor", "woke Cursor")
        finally:
            cr.OWB = old_owb
        log = subprocess.run(["git", "-C", str(remote), "log", "--format=%P|%s", "mini-heartbeat"], capture_output=True, text=True, check=True).stdout
        self.assertEqual(len(log.strip().splitlines()), 1)  # replaced, not stacked
        self.assertTrue(log.startswith("|"))  # no parent
        doc = json.loads(subprocess.run(["git", "-C", str(remote), "show", "mini-heartbeat:heartbeat.json"], capture_output=True, text=True, check=True).stdout)
        self.assertEqual((doc["state"], doc["agent"]), ("running", "cursor"))


if __name__ == "__main__":
    unittest.main()
