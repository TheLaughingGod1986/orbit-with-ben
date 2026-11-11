"""chief_relay.py: the first agent in the chain that is up acts as Chief; out of credit falls through; Grok takes back."""
import datetime as dt, os, pathlib, stat, sys, tempfile, time, unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chief_relay as cr  # noqa: E402

T0 = dt.datetime(2026, 10, 7, 12, 0, tzinfo=dt.timezone.utc)
MIN = dt.timedelta(minutes=1)


class Relay(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.old_state, self.old_home, self.old_fetch, self.old_owb = cr.STATE, cr.HOME, cr.fetch_comments, cr.STUDIO
        cr.STATE, cr.HOME = self.tmp / "state", self.tmp  # so a real CLI on this machine can't stand in for a fake
        cr.STUDIO = self.tmp / "no-owb"  # never the live queue: an addressed job there (J0071, 9 Oct) changed who ran
        self.thread = []  # fake studio thread: (created_at, body)
        cr.fetch_comments = lambda since: [{"created_at": t, "body": b} for t, b in self.thread if cr.parse(t) >= since]
        cr.STATE.mkdir()
        cr.write_json(cr.d("caches.json"), {"at": cr.iso(T0)})
        cr.write_json(cr.d("claude_beat.json"), {"fetched": cr.iso(T0), "beat": None})
        self.posts = self.tmp / "posts.txt"
        notify = self.tmp / "notify.sh"
        notify.write_text(f'#!/bin/sh\necho "$1" >> "{self.posts}"\n')
        notify.chmod(notify.stat().st_mode | stat.S_IEXEC)
        self.env = dict(os.environ)
        os.environ.update({"CHIEF_CLAUDE_BEAT_URL": "", "CHIEF_CLAUDE_BEAT_FETCH_MIN": "999999", "CHIEF_NOTIFY": str(notify), "CHIEF_HOURS": "0-24", "CHIEF_SWEEP_HOURS": "0-24", "CHIEF_CHAIN": "chief,cursor,codex",
                           "CHIEF_HEARTBEAT": "0", "CHIEF_MIN_FREE_MB": "0"})  # never push a heartbeat from a test run on the Mini
        self.cursor = self.fake("cursor", 'echo "cursor did J0001"')
        self.codex = self.fake("codex", 'echo "codex did J0001"')
        os.environ["CURSOR_AGENT_BIN"], os.environ["CODEX_BIN"] = str(self.cursor), str(self.codex)
        # Always a fake agy: on the Mini the real one is on PATH, and a test must never wake it.
        os.environ["AGY_BIN"] = str(self.fake("agy", 'echo "gemini did it"'))
        # And a fake Claude Code: the `claudecode` Mini worker (9 Nov 2026) would find the real `claude` on PATH.
        os.environ["CLAUDE_BIN"] = str(self.fake("claude", 'echo "claudecode did it"'))

    def tearDown(self):
        cr.STATE, cr.HOME, cr.fetch_comments, cr.STUDIO = self.old_state, self.old_home, self.old_fetch, self.old_owb
        cr.routing.OUT = set()
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

    def test_a_free_relay_wakes_the_queued_worker(self):
        cr.cmd_run(T0)
        self.assertTrue(self.ran("cursor"))

    def test_woken_agents_get_the_ssd_scratch_when_it_is_mounted(self):
        sd = self.tmp / "MiniWork" / "scratch"
        sd.mkdir(parents=True)
        body = f"echo \"$TMPDIR|$STUDIO_SCRATCH\" > {self.tmp}/env.txt"
        self.fake("envcli", body)
        with mock.patch.object(cr, "cli_spec", return_value=(str(self.tmp / "envcli"), [])):
            with mock.patch.object(cr, "scratch_dir", return_value=sd):
                cr.run_cli("cursor", "P", 30)
            self.assertEqual((self.tmp / "env.txt").read_text().strip(), f"{sd}/|{sd}")
            with mock.patch.object(cr, "scratch_dir", return_value=None):  # unplugged: back to /private/tmp
                cr.run_cli("cursor", "P", 30)
            self.assertTrue((self.tmp / "env.txt").read_text().strip().endswith("|/private/tmp"))

    def test_a_miniwork_folder_on_the_internal_disk_is_not_the_ssd(self):
        (self.tmp / "MiniWork" / "scratch").mkdir(parents=True)
        with mock.patch.object(cr, "MINIWORK", self.tmp / "MiniWork"), mock.patch.object(cr, "HOME", self.tmp):
            self.assertIsNone(cr.scratch_dir())  # same device as HOME: an unplugged drive's leftover folder

    def test_a_blocked_ssd_cannot_hang_the_relay(self):
        """9 Nov 2026: macOS held the relay on a permission dialog for the SSD and it went silent for hours. The check
        now runs in a child with a timeout, and the answer is kept so the wait isn't paid on every wake."""
        (self.tmp / "MiniWork" / "scratch").mkdir(parents=True)
        with mock.patch.object(cr, "MINIWORK", self.tmp / "MiniWork"), mock.patch.object(cr, "HOME", self.tmp), \
                mock.patch.object(cr, "_SSD_PROBE", "import time; time.sleep(60)"), \
                mock.patch.object(cr, "SSD_PROBE_S", 1):
            t0 = time.monotonic()
            self.assertIsNone(cr.scratch_dir())
            self.assertLess(time.monotonic() - t0, 10)
            with mock.patch.object(cr.subprocess, "run", side_effect=AssertionError("asked again")):
                self.assertIsNone(cr.scratch_dir())  # kept answer: no second wait

    def test_the_ssd_is_used_when_the_child_reports_another_device(self):
        sd = self.tmp / "MiniWork" / "scratch"
        sd.mkdir(parents=True)
        with mock.patch.object(cr, "MINIWORK", self.tmp / "MiniWork"), mock.patch.object(cr, "HOME", self.tmp), \
                mock.patch.object(cr, "_ssd_dev", return_value=os.stat(self.tmp).st_dev + 1):
            self.assertEqual(cr.scratch_dir(), sd)

    def test_claude_code_on_the_mini_runs_unattended_with_the_prompt_last(self):
        b, args = cr.cli_spec("claudecode")
        self.assertTrue(b.endswith("/claude"))
        self.assertIn("--dangerously-skip-permissions", args)
        self.assertEqual(args[-1], "-p")  # run_cli appends the prompt straight after -p

    def test_with_codex_cursor_and_gemini_out_the_job_goes_to_claude_code(self):
        q = self.routed_queue('{"next_id": 2, "jobs": [{"id": "J0901", "kind": "assembly", "status": "open", "needs": "mini", "history": []}]}')
        for a in ("cursor", "codex", "gemini"):
            cr.mark_down(a, "out of credit", T0 + 60 * MIN, T0)
        with mock.patch.object(cr, "run_cli", return_value=(0, "done")) as run:
            cr.cmd_run(T0)
        self.assertIn("claudecode", [c.args[0] for c in run.call_args_list])

    def test_grok_is_chief_while_its_heartbeat_is_fresh(self):
        cr.seen("chief", T0 - 30 * MIN)
        self.assertEqual(self.chief(), "chief")
        old = cr.queue_has_work
        cr.queue_has_work = lambda agent: False
        try:
            cr.cmd_run(T0)
        finally:
            cr.queue_has_work = old
        self.assertFalse(self.ran("cursor"))  # Grok drives itself; with no queued job no worker runs

    def post(self, at, body):
        self.thread.append((cr.iso(at), body))

    def test_a_grok_post_on_the_thread_makes_it_chief_again(self):
        cr.cmd_run(T0)
        self.assertTrue(self.ran("cursor"))
        (self.tmp / "cursor.ran").unlink()
        self.post(T0 + 10 * MIN, "[Chief] Re 123: claimed, working")  # Grok, back with credit
        old = cr.queue_has_work
        cr.queue_has_work = lambda agent: False  # nothing queued, so no worker wakes (and no sweep under Grok)
        try:
            cr.cmd_run(T0 + 30 * MIN)
        finally:
            cr.queue_has_work = old
        self.assertFalse(self.ran("cursor"))
        self.assertEqual(self.chief(T0 + 30 * MIN), "chief")
        self.assertIn("Grok Bot is Chief again", self.posts.read_text())
        self.assertIn("keep running the job queue as workers", self.posts.read_text())
        self.assertNotIn("stand down", self.posts.read_text())

    def test_cursor_codex_and_relay_posts_are_not_grok(self):
        for body in ("[Chief] [Cursor] Cursor covering. J0007 done", "[Chief] Cursor covering: J0001 started",
                     "[Chief] [Codex] Codex covering.", "[Chief] Chief relay: **Cursor is acting Chief**",
                     "[Chief] [relay] @Chief stale reviews (parked over 2 h): J0226 030 Apophis Short",   # 15 Oct 01:01Z
                     "[Chief] STALLED: 028 edit by gemini: ETA 2026-10-22T23:36Z passed ()"):   # 22 Oct 23:46Z
            self.post(T0 - 5 * MIN, body)
        cr.cmd_run(T0)
        self.assertEqual(self.chief(T0), "cursor")

    def test_gemini_and_claude_posts_are_not_grok(self):
        # 14 Oct 2026: "[Chief] Gemini covering — J0236 ..." was read as Grok and ended Ben's Claude-as-Chief order.
        for body in ("[Chief] Gemini covering — J0236 (023 Venus v05e package + upload):", "[Chief] [Gemini] J0237 done",
                     "[Chief] [Claude] acting Chief: J0228 PASS", "[Chief] notes\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_"):
            self.post(T0 - 5 * MIN, body)
        cr.cmd_run(T0)
        self.assertEqual(self.chief(T0), "cursor")

    def test_a_misread_post_time_is_dropped_once_the_thread_is_read(self):
        cr.write_json(cr.d("grok_thread.json"), {"checked": cr.iso(T0 - 10 * MIN), "last_post": cr.iso(T0 - 12 * MIN)})
        cr.note_grok_posts(T0)   # the thread reads fine and has no Grok post in the window
        self.assertIsNone(cr.grok_post_age(T0))

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

    def _chain(self, ids):
        """Patch the queue so next_job hands out `ids` in turn; return the list of jobs the relay ran."""
        ran, left = [], list(ids)
        saved = (cr.next_job, cr.queue_has_work, cr.run_cli)
        self.addCleanup(lambda: setattr(cr, "next_job", saved[0]) or setattr(cr, "queue_has_work", saved[1])
                        or setattr(cr, "run_cli", saved[2]))
        cr.next_job = lambda agent: {"id": left[0], "kind": "assembly"} if left else None
        cr.queue_has_work = lambda agent: bool(left)
        def run_cli(who, prompt, cap, model):
            ran.append(left[0])
            if left[0] != "SAME":
                left.pop(0)
            return 0, "done"
        cr.run_cli = run_cli
        return ran

    def test_when_a_job_ends_the_next_ready_job_starts_in_the_same_run(self):
        ran = self._chain(["J0001", "J0002", "J0003"])
        cr.seen("chief", T0 - 10 * MIN)
        cr.cmd_run(T0)
        self.assertEqual(ran, ["J0001", "J0002", "J0003"])  # back to back, no wait for the next tick

    def test_a_job_released_to_retry_later_is_not_rerun_in_a_tight_loop(self):
        ran = self._chain(["SAME"])
        cr.seen("chief", T0 - 10 * MIN)
        cr.cmd_run(T0)
        self.assertEqual(ran, ["SAME"])

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

    def test_a_stalled_grok_is_not_brought_back_by_a_thread_post(self):
        # Ben, 28 Oct 2026: Grok kept posting but never cleared its inbox, and each post made it Chief again.
        cr.mark_down("chief", "Chief inbox delivered but not progressed", T0 + 30 * MIN, T0, kind="stalled")
        self.post(T0 + 10 * MIN, "[Chief] looking at it")
        cr.note_grok_posts(T0 + 12 * MIN)
        self.assertEqual(self.chief(T0 + 12 * MIN), "cursor")
        cr.seen("chief", T0 + 15 * MIN)  # Grok actually ran jobs.py: it's back
        self.assertEqual(self.chief(T0 + 16 * MIN), "chief")

    def test_hourly_cloud_claude_gets_a_full_run_to_take_its_inbox(self):
        # 5 Nov 2026: a 30-min window benched Claude (runs hourly at :50) every hour, up to 12 h.
        cr.STUDIO = self.tmp / "owb"
        (cr.STUDIO / "jobs").mkdir(parents=True, exist_ok=True)
        (cr.STUDIO / "jobs" / "queue.json").write_text('{"jobs": []}')
        for agent in ("claude", "chief"):
            cr.write_json(cr.d("inbox.json"), {"agent": agent, "notified_at": cr.iso(T0),
                                               "waiting": {"J1": {"since": cr.iso(T0)}}})
            self.assertEqual(cr.chief_delivery_overdue(agent, T0 + 45 * MIN), agent == "chief")
            # 10 Nov 2026: 75 min still benched Claude nightly; it now gets two full runs (150 min).
            self.assertEqual(cr.chief_delivery_overdue(agent, T0 + 76 * MIN), agent == "chief")
            self.assertTrue(cr.chief_delivery_overdue(agent, T0 + 151 * MIN))

    def test_repeat_stalls_keep_grok_down_longer(self):
        windows = [cr.stall_window("chief", T0 + i * MIN) for i in range(6)]
        self.assertEqual([int(w.total_seconds() // 60) for w in windows], [30, 60, 120, 240, 480, 720])
        self.assertEqual(int(cr.stall_window("chief", T0 + 25 * 60 * MIN).total_seconds() // 60), 30)  # a day later

    def test_a_hard_flag_from_ben_is_not_cleared_by_a_post(self):
        (cr.STUDIO / "scripts").mkdir(parents=True, exist_ok=True)
        (cr.STUDIO / "scripts" / "credit_flags.json").write_text(
            '{"flags": {"chief": {"out_until": "2099-01-01T00:00:00Z", "reason": "Ben: Grok is down", "hard": true}}}')
        self.post(T0 + 5 * MIN, "[Chief] back")
        cr.note_grok_posts(T0 + 6 * MIN)
        self.assertEqual(self.chief(T0 + 6 * MIN), "cursor")

    def test_grok_takes_back_over_when_it_runs_jobs_again(self):
        cr.mark_down("chief", "out of credit", None, T0)
        cr.seen("chief", T0 - 10 * MIN)  # before the mark: still down
        self.assertEqual(self.chief(T0), "cursor")
        cr.seen("chief", T0 + 5 * MIN)  # Grok ran jobs.py after the mark: it's back
        self.assertEqual(self.chief(T0 + 6 * MIN), "chief")

    def test_nobody_up_posts_once_and_runs_nothing(self):
        cr.mark_down("cursor", "out of credit", None, T0)
        cr.mark_down("codex", "out of credit", None, T0)
        cr.mark_down("gemini", "out of credit", None, T0)
        cr.cmd_run(T0)
        cr.cmd_run(T0 + 30 * MIN)
        self.assertFalse(self.ran("cursor") or self.ran("codex") or self.ran("agy"))
        self.assertEqual(self.posts.read_text().count("nobody can act as Chief"), 1)

    def test_with_grok_cursor_and_codex_down_gemini_still_takes_queued_jobs(self):
        old_q = cr.queue_has_work
        cr.queue_has_work = lambda agent: True
        try:
            cr.mark_down("cursor", "out of credit", None, T0)
            cr.mark_down("codex", "out of credit", None, T0)
            cr.cmd_run(T0)
            self.assertTrue(self.ran("agy"))
        finally:
            cr.queue_has_work = old_q

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

    def test_a_failed_elected_chief_yields_to_the_next_agent(self):
        self.fake("cursor", 'echo "Traceback: KeyError"; exit 1')
        cr.cmd_run(T0)
        self.assertTrue(self.ran("codex"))
        self.assertIn("run failed (exit 1)", self.posts.read_text())

    def test_a_long_job_that_mentions_quota_is_not_out_of_credit(self):
        self.assertFalse(cr.out_of_credit(0, "checked the YouTube quota exceeded warning ... " + "x" * 800))
        self.assertTrue(cr.out_of_credit(1, "usage limit reached, try again at 5pm"))
        self.assertFalse(cr.out_of_credit(124, "rate limit"))

    def test_a_worker_quoting_a_429_mid_run_is_not_out_of_credit(self):
        # Ben, 15 Oct 2026: Cursor and Codex were marked out overnight with credit left. Only the CLI's own last lines count.
        work = "buffer: 401 Unauthorized for the HOS key\nyoutube: HTTP 429\n" + "step 3 of 5 done\n" * 80
        self.assertFalse(cr.out_of_credit(1, work + "Traceback: KeyError 'slot'"))
        said = cr.credit_phrase(1, work + "Error: You've hit your usage limit. Try again at 4am.")
        self.assertIn("usage limit", said)

    def test_cursor_out_of_its_opus_pool_runs_on_auto_and_stays_up(self):
        # 15 Oct 2026 03:40Z: "You've hit your usage limit for Opus ... Switch to a different model" benched all of Cursor.
        args = cr.cli_spec("cursor")[1]
        self.assertEqual(args[args.index("--model") + 1], "grok-4.7")   # Ben, 15 Oct 2026: Grok 4.7, not Auto, by default
        cr.write_json(cr.d("cursor_default_out.json"), {"until": cr.iso(cr.now() + dt.timedelta(hours=1))})
        args = cr.cli_spec("cursor")[1]
        self.assertEqual(args[args.index("--model") + 1], "auto")
        self.assertTrue(cr.state_of("cursor", cr.now())[0])
        cr.write_json(cr.d("cursor_default_out.json"), {"until": cr.iso(cr.now() - dt.timedelta(minutes=1))})
        args = cr.cli_spec("cursor")[1]
        self.assertEqual(args[args.index("--model") + 1], "grok-4.7")   # the mark ended: back to Grok 4.7
        self.assertTrue(cr.MODEL_LIMIT_RE.search("ActionRequiredError: You've hit your usage limit for Opus You've saved $780"))
        self.assertFalse(cr.MODEL_LIMIT_RE.search("ERROR: You've hit your usage limit. Upgrade to Pro"))

    def test_the_mark_says_what_the_cli_said(self):
        self.fake("cursor", 'echo "Error: You are out of credits. Upgrade your plan."; exit 1')
        cr.cmd_run(T0)
        self.assertIn("out of credits", cr.state_of("cursor", cr.now())[1])

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

    def test_while_grok_is_chief_cursor_still_runs_one_queued_job_as_worker(self):
        old = cr.queue_has_work
        cr.queue_has_work = lambda agent: True
        try:
            cr.seen("chief", T0 - 10 * MIN)  # Grok is Chief
            self.assertEqual(self.chief(), "chief")
            cr.cmd_run(T0)
            self.assertTrue(self.ran("cursor"))  # the Mini doesn't idle (9 Oct stall)
            self.assertFalse(self.ran("codex"))
        finally:
            cr.queue_has_work = old

    def test_while_grok_is_chief_an_empty_queue_wakes_no_worker_and_no_sweep(self):
        old = cr.queue_has_work
        cr.queue_has_work = lambda agent: False
        try:
            cr.seen("chief", T0 - 10 * MIN)
            cr.seen("cursor", T0 - 300 * MIN)  # a sweep would be due if Cursor were Chief
            cr.cmd_run(T0)
            self.assertFalse(self.ran("cursor"))
            self.assertFalse(self.ran("codex"))
        finally:
            cr.queue_has_work = old

    def test_a_job_addressed_to_codex_wakes_codex_while_cursor_is_chief(self):
        old_owb, old_q = cr.STUDIO, cr.queue_has_work
        cr.STUDIO = self.tmp / "owb"
        (cr.STUDIO / "jobs").mkdir(parents=True)
        q = cr.STUDIO / "jobs" / "queue.json"
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
            cr.STUDIO, cr.queue_has_work = old_owb, old_q

    def test_a_model_at_capacity_flags_only_that_model(self):
        old_owb, old_q = cr.STUDIO, cr.queue_has_work
        cr.STUDIO = self.tmp / "owb"
        (cr.STUDIO / "jobs").mkdir(parents=True)
        (cr.STUDIO / "jobs" / "queue.json").write_text(
            '{"jobs": [{"id": "J0072", "for": "codex", "model": "gpt-6.1-sol", "status": "open", "needs": "any"}]}')
        self.fake("codex", 'echo "ERROR: Selected model is at capacity. Please try a different model."; exit 1')
        cr.queue_has_work = lambda agent: True
        try:
            cr.cmd_run(T0)
            self.assertTrue(self.ran("codex"))
            self.assertTrue(cr.d("down_models", "gpt-6.1-sol.json").exists())  # the named model: flagged
            self.assertTrue(cr.state_of("codex", cr.now() + 16 * MIN)[0])  # its default too: a 15-min pause, not 1 h
            self.assertNotIn("run failed", self.posts.read_text() if self.posts.exists() else "")
        finally:
            cr.STUDIO, cr.queue_has_work = old_owb, old_q

    def test_a_failed_addressed_run_is_not_retried_every_tick(self):
        old_owb, old_q = cr.STUDIO, cr.queue_has_work
        cr.STUDIO = self.tmp / "owb"
        (cr.STUDIO / "jobs").mkdir(parents=True)
        (cr.STUDIO / "jobs" / "queue.json").write_text('{"jobs": [{"id": "J0071", "for": "codex", "status": "open", "needs": "any"}]}')
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
            cr.STUDIO, cr.queue_has_work = old_owb, old_q

    def test_agy_gets_the_prompt_straight_after_p(self):
        # `agy -p` takes the next argument as the prompt; with -p first it read a flag as the prompt (exit 2, 13 Oct).
        _, args = cr.cli_spec("gemini")
        self.assertEqual(args[-1], "-p")
        self.assertIn("--dangerously-skip-permissions", args)
        os.environ["AGY_FLAGS"] = "-p --dangerously-skip-permissions"  # an old env value is put right too
        _, args = cr.cli_spec("gemini")
        self.assertEqual((args.count("-p"), args[-1]), (1, "-p"))

    def test_a_failing_worker_is_backed_off_not_woken_every_minute(self):
        # 13-14 Oct: Gemini exited 2 on every 60 s relay run and posted "run failed" 88 times in 20 h.
        old_q = cr.queue_has_work
        cr.queue_has_work = lambda agent: True
        self.fake("agy", 'echo "error: unexpected argument"; exit 2')
        try:
            cr.mark_down("cursor", "out of credit", None, T0)
            cr.mark_down("codex", "out of credit", None, T0)
            cr.cmd_run(T0)
            self.assertTrue(self.ran("agy"))
            self.assertFalse(cr.state_of("gemini", T0 + MIN)[0])
            (self.tmp / "agy.ran").unlink()
            cr.cmd_run(T0 + MIN)
            self.assertFalse(self.ran("agy"))
            self.assertEqual(self.posts.read_text().count("run failed (exit 2)"), 1)
        finally:
            cr.queue_has_work = old_q

    def routed_queue(self, jobs_json):
        cr.STUDIO = self.tmp / "owb"
        (cr.STUDIO / "jobs").mkdir(parents=True, exist_ok=True)
        (cr.STUDIO / "jobs" / "queue.json").write_text(jobs_json)

    def test_a_made_up_third_channels_job_wakes_its_worker_like_any_other(self):
        # J2618: nothing in the relay names a channel, so a channel that is only in the channel files is served too.
        base = cr.channels._load()
        home = next(c for c in base if c.get("home"))
        sky = dict(home, slug="sky", label="SKY", name="Night Sky", short="Sky", home=False, order=3, title_match=r"\bSKY\b",
                   repo={"url": "https://github.com/example/night-sky.git", "env": "SKY_REPO", "checkouts": ["Night Sky"]})
        old_q, old_others = cr.queue_has_work, cr.OTHERS
        self.codex = self.fake("codex", f'echo "$@" > {self.tmp}/codex.args')
        self.routed_queue('{"jobs": [{"id": "J0201", "kind": "chart", "status": "open", "needs": "mini", "repo": "sky", '
                          '"title": "SKY 001: draw the star chart"}]}')
        cr.queue_has_work = lambda agent: True
        try:
            with mock.patch.object(cr.channels, "_load", lambda directory=None: base + (sky,)):
                cr.OTHERS = {**old_others, "sky": self.tmp / "YouTube" / "Night Sky"}
                cr.seen("chief", T0 - 10 * MIN)
                cr.cmd_run(T0)
            self.assertTrue(self.ran("codex"))
            brief = (self.tmp / "codex.args").read_text()
            self.assertIn("claim only J0201", brief)
            self.assertIn(f"2b. Night Sky ({self.tmp / 'YouTube' / 'Night Sky'}): git pull.", brief)
            self.assertIn(f'--sky "{self.tmp / "YouTube" / "Night Sky"}"', brief)
            self.assertIn("Chief for Night Sky", brief)                      # its own Chief chain, by its own name
            self.assertIn(f"--add-dir {self.tmp / 'YouTube' / 'Night Sky'}", brief)
        finally:
            cr.queue_has_work, cr.OTHERS = old_q, old_others

    def test_a_chart_job_wakes_codex_on_gpt_6_astra_while_grok_is_chief(self):
        old_q = cr.queue_has_work
        self.codex = self.fake("codex", f'echo "$@" > {self.tmp}/codex.args')
        self.routed_queue('{"jobs": [{"id": "J0200", "kind": "chart", "status": "open", "needs": "mini"}]}')
        cr.queue_has_work = lambda agent: True
        try:
            cr.seen("chief", T0 - 10 * MIN)
            cr.cmd_run(T0)
            self.assertTrue(self.ran("codex"))
            self.assertFalse(self.ran("cursor"))
            self.assertIn("exec -m gpt-6-astra --approve-for-me", (self.tmp / "codex.args").read_text())
        finally:
            cr.queue_has_work = old_q

    def test_with_codex_down_cursor_stands_in_then_hands_back(self):
        old_q = cr.queue_has_work
        self.routed_queue('{"jobs": [{"id": "J0200", "kind": "chart", "status": "open", "needs": "mini"}]}')
        cr.queue_has_work = lambda agent: True
        try:
            cr.seen("chief", T0 - 10 * MIN)
            cr.mark_down("codex", "usage limit", T0 + 60 * MIN, T0)
            cr.cmd_run(T0)
            self.assertTrue(self.ran("cursor"))  # the backup takes the chart job
            self.assertFalse(self.ran("codex"))
            (self.tmp / "cursor.ran").unlink()
            cr.seen("chief", T0 + 61 * MIN)
            cr.cmd_run(T0 + 61 * MIN)  # Codex's limit is over: the next chart job goes back to it
            self.assertTrue(self.ran("codex"))
            self.assertFalse(self.ran("cursor"))
        finally:
            cr.queue_has_work = old_q

    def test_an_assembly_job_stays_with_cursor_and_no_model_flag(self):
        old_q = cr.queue_has_work
        self.routed_queue('{"jobs": [{"id": "J0201", "kind": "assembly", "status": "open", "needs": "mini"}]}')
        cr.queue_has_work = lambda agent: True
        try:
            cr.seen("chief", T0 - 10 * MIN)
            cr.cmd_run(T0)
            self.assertTrue(self.ran("cursor"))
            self.assertFalse(self.ran("codex"))
        finally:
            cr.queue_has_work = old_q

    def test_stand_ins_are_told_to_park_protected_calls(self):
        self.assertIn("parked for Chief", cr.authority_prompt("cursor", "codex"))
        self.assertIn("No final OK or PASS, no merge", cr.authority_prompt("cursor", "codex"))

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


    # ---- Claude out of usage -> Cursor on the Claude model (Ben, 11 Oct 2026 23:40) ----

    def claude_setup(self, jobs_json):
        import json
        import jobs
        self.routed_queue(jobs_json)
        self.cursor = self.fake("cursor", f'echo "$@" >> {self.tmp}/cursor.args; echo "cursor did it"')
        self.codex = self.fake("codex", f'echo "$@" > {self.tmp}/codex.args; echo "codex did it"')
        self.old_reroute, self.old_q = cr.reroute, cr.queue_has_work
        q = cr.STUDIO / "jobs" / "queue.json"

        def fake_reroute(job, to, model, note):  # jobs.py reroute, on the test queue (never the live one)
            data = json.loads(q.read_text())
            j = next(x for x in data["jobs"] if x["id"] == job["id"])
            jobs.do_reroute(j, "relay", to, model, note, cr.now())
            q.write_text(json.dumps(data))
            return True
        cr.reroute, cr.queue_has_work = fake_reroute, (lambda agent: True)
        self.addCleanup(lambda: setattr(cr, "reroute", self.old_reroute))
        self.addCleanup(lambda: setattr(cr, "queue_has_work", self.old_q))
        return q

    def job(self, q, jid):
        import json
        return next(j for j in json.loads(q.read_text())["jobs"] if j["id"] == jid)

    def test_a_claude_job_blocked_on_a_usage_limit_is_redispatched_to_cursor_on_the_claude_model(self):
        q = self.claude_setup('{"jobs": [{"id": "J0300", "kind": "script", "status": "blocked", "needs": "cloud", '
                              '"by": "claude", "result": "Claude Code: usage limit reached, resets 04:00", "history": '
                              '[{"by": "claude", "what": "blocked: Claude Code: usage limit reached, resets 04:00"}]}]}')
        cr.seen("chief", T0 - 10 * MIN)  # Grok is Chief: Cursor is the worker
        cr.cmd_run(T0)
        j = self.job(q, "J0300")
        self.assertEqual((j["status"], j["for"], j["needs"], j["model"]), ("open", "cursor", "mini", "cursor-claude-opus-5-5"))
        self.assertEqual(j["rerouted_from"]["needs"], "cloud")
        self.assertTrue(self.ran("cursor"))  # woken in the same run, not left parked
        self.assertFalse(self.ran("codex"))
        self.assertIn("--model claude-opus-5-5", (self.tmp / "cursor.args").read_text())
        self.assertTrue(cr.claude_out(T0 + MIN)[0])  # Claude marked down for the retry time
        self.assertTrue((cr.STATE / "chief" / "down" / "claude.json").exists())
        self.assertIn("Claude is out of usage", self.posts.read_text())

    def test_claude_marked_out_reroutes_only_claude_owned_jobs(self):
        q = self.claude_setup('{"jobs": ['
                              '{"id": "J0301", "kind": "review", "status": "open", "needs": "cloud"}, '
                              '{"id": "J0302", "kind": "assembly", "status": "open", "needs": "mini"}, '
                              '{"id": "J0303", "kind": "chief", "status": "open", "needs": "cloud"}, '
                              '{"id": "J0304", "model": "claude-opus-5-5", "status": "open", "needs": "ben"}, '
                              '{"id": "J0305", "kind": "listing", "status": "open", "needs": "macbook"}]}')
        cr.mark_down("claude", "usage limit", T0 + 120 * MIN, T0)
        cr.seen("chief", T0 - 10 * MIN)
        cr.cmd_run(T0)
        self.assertEqual(self.job(q, "J0301").get("for"), "cursor")
        for jid in ("J0302", "J0303", "J0304", "J0305"):  # J0305: a MacBook job stays on the MacBook
            self.assertNotIn("rerouted_from", self.job(q, jid), jid)
        self.assertIn("--model claude-opus-5-5", (self.tmp / "cursor.args").read_text())
        # The released/open review no longer stops unrelated assembly work in
        # this run. Keep all invocations rather than inspecting only the last.
        self.assertIn("--model grok-4.7", (self.tmp / "cursor.args").read_text())
        self.assertIn("DISPATCH PRIORITY: claim only J0302", (self.tmp / "cursor.args").read_text())

    def test_with_cursor_down_the_claude_job_goes_to_gemini_before_codex(self):
        os.environ["AGY_BIN"] = str(self.fake("agy", f'echo "$@" > {self.tmp}/agy.args; echo "gemini did it"'))
        q = self.claude_setup('{"jobs": [{"id": "J0308", "kind": "listing", "status": "open", "needs": "cloud"}]}')
        cr.mark_down("claude", "usage limit", None, T0)
        cr.mark_down("cursor", "out of credit", T0 + 60 * MIN, T0)
        cr.seen("chief", T0 - 10 * MIN)
        cr.cmd_run(T0)
        j = self.job(q, "J0308")
        self.assertEqual((j["for"], j["model"]), ("gemini", "gemini-argon"))
        self.assertTrue(self.ran("agy"))
        self.assertFalse(self.ran("codex"))
        agy = (self.tmp / "agy.args").read_text()
        self.assertTrue(agy.startswith("--dangerously-skip-permissions"))
        self.assertIn(" -p You are Gemini", agy)  # the prompt comes straight after -p

    def test_a_worker_out_of_usage_mid_job_hands_it_down_the_chain_in_the_same_run_and_logs_who_ran_it(self):
        import json
        os.environ["AGY_BIN"] = str(self.fake("agy", f'echo "$@" > {self.tmp}/agy.args; echo "gemini did it"'))
        q = self.claude_setup('{"jobs": [{"id": "J0309", "kind": "review", "status": "open", "needs": "cloud"}]}')
        self.fake("cursor", f'echo "$@" > {self.tmp}/cursor.args; echo "Error: usage limit reached for this model"; exit 1')
        cr.mark_down("claude", "usage limit", None, T0)  # 1) Claude Code is out
        cr.seen("chief", T0 - 10 * MIN)
        cr.cmd_run(T0)
        self.assertIn("--model claude-opus-5-5", (self.tmp / "cursor.args").read_text())  # 2) Cursor on Claude tried
        self.assertTrue(self.ran("agy"))  # 3) Gemini took it in the same run, not parked
        self.assertFalse(self.ran("codex"))
        j = self.job(q, "J0309")
        self.assertEqual((j["for"], j["model"]), ("gemini", "gemini-argon"))
        # Ben, 14 Oct: only Claude-in-Cursor's pool is empty; Cursor stays up for its own models (Auto)
        self.assertEqual(cr.state_of("cursor", cr.now())[1], "ready")
        self.assertIn("cursor-claude-opus-5-5", cr.load_out(cr.now()))
        runs = [json.loads(l) for l in (cr.STATE / "chief" / "runs.jsonl").read_text().splitlines()]
        self.assertEqual([(r["job"], r["worker"], r["cli_model"], r["lane"], r["out_of_usage"]) for r in runs],
                         [("J0309", "cursor", "claude-opus-5-5", 2, True),
                          ("J0309", "gemini", cr.routing.AGY_ARGON_MODEL, 3, False)])

    def test_codex_out_of_usage_on_a_chart_job_moves_to_cursor(self):
        q = self.claude_setup('{"jobs": [{"id": "J0310", "kind": "chart", "status": "open", "needs": "mini"}]}')
        self.fake("codex", f'echo "$@" > {self.tmp}/codex.args; echo "ERROR: You have hit your usage limit"; exit 1')
        cr.seen("chief", T0 - 10 * MIN)
        cr.cmd_run(T0)
        self.assertIn("exec -m gpt-6-astra", (self.tmp / "codex.args").read_text())  # code and graphics: Codex first
        self.assertTrue(self.ran("cursor"))  # then the next in the chart chain
        self.assertIn("--model grok-4.7", (self.tmp / "cursor.args").read_text())  # Cursor on Grok 4.7 for a chart
        self.assertEqual(self.job(q, "J0310")["for"], "cursor")

    def test_with_cursor_and_gemini_down_the_claude_job_goes_to_codex_on_astra(self):
        q = self.claude_setup('{"jobs": [{"id": "J0305", "kind": "listing", "status": "open", "needs": "cloud"}]}')
        cr.mark_down("claude", "usage limit", None, T0)
        cr.mark_down("cursor", "out of credit", T0 + 60 * MIN, T0)
        cr.mark_down("gemini", "quota exhausted", T0 + 60 * MIN, T0)
        cr.seen("chief", T0 - 10 * MIN)
        cr.cmd_run(T0)
        j = self.job(q, "J0305")
        self.assertEqual((j["for"], j["model"]), ("codex", "gpt-6-astra"))
        self.assertTrue(self.ran("codex"))
        self.assertIn("exec -m gpt-6-astra", (self.tmp / "codex.args").read_text())

    def test_while_claude_is_up_its_jobs_stay_with_claude(self):
        q = self.claude_setup('{"jobs": [{"id": "J0306", "kind": "script", "status": "open", "needs": "cloud"}, '
                              '{"id": "J0307", "kind": "qa", "status": "blocked", "needs": "cloud", "result": "needs Ben: a sign-in", '
                              '"history": [{"by": "claude", "what": "blocked: needs Ben: a sign-in"}]}]}')
        cr.seen("chief", T0 - 10 * MIN)
        cr.cmd_run(T0)
        self.assertNotIn("for", self.job(q, "J0306"))
        self.assertNotIn("for", self.job(q, "J0307"))  # an ordinary block is not a usage limit
        self.assertFalse(cr.claude_out(cr.now())[0])

    def test_a_claude_ledger_note_about_its_limit_counts_as_out(self):
        led = self.tmp / "owb" / "05_Analytics" / "ai_spend"
        led.mkdir(parents=True)
        cr.STUDIO = self.tmp / "owb"
        (led / "ledger.jsonl").write_text('{"at": "%s", "kind": "record", "pool": "claude", "note": "hit the 5-hour limit"}\n'
                                          % cr.iso(T0 - 30 * MIN))
        self.assertTrue(cr.claude_out(T0)[0])
        self.assertFalse(cr.claude_out(T0 + 6 * 60 * MIN)[0])  # older than CHIEF_CLAUDE_OUT_H (5 h)

    def test_a_model_the_cli_does_not_know_is_flagged_and_the_job_walks_on(self):
        # Ben, 15 Oct 2026: best-fit model per job; a wrong id must never stop the queue.
        self.assertTrue(cr.UNKNOWN_MODEL_RE.search("Error: Unknown model 'grok-4.7'. Run agent --list-models"))
        self.assertTrue(cr.UNKNOWN_MODEL_RE.search("The model gemini-argon does not exist or you lack access"))
        self.assertFalse(cr.UNKNOWN_MODEL_RE.search("Traceback: KeyError 'model'"))

    def test_provider_capacity_is_a_model_blip_not_a_worker_outage(self):
        # Codex, 5 Nov 2026 09:10Z: one "model is at capacity" reply marked Codex down for an hour.
        self.assertTrue(cr.CAPACITY_RE.search("ERROR: Selected model is at capacity. Please try a different model."))
        self.assertTrue(cr.CAPACITY_RE.search('{"type": "overloaded_error", "message": "Overloaded"}'))
        self.assertFalse(cr.CAPACITY_RE.search("Disk at capacity: 97% used"))
        self.assertFalse(cr.CAPACITY_RE.search("Traceback: ValueError: capacity must be positive"))

    def test_cursor_gets_the_claude_model_flag_only_for_claude_work(self):
        _, args = cr.cli_spec("cursor", "cursor-claude-opus-5-5")
        self.assertEqual(args[-2:], ["--model", "claude-opus-5-5"])
        _, args = cr.cli_spec("cursor", "cursor-auto")
        self.assertNotIn("--model", args)
        _, args = cr.cli_spec("cursor", "gpt-6-astra")
        self.assertEqual(args[-2:], ["--model", "grok-4.7"])   # not Cursor's own model: its default lane, Grok 4.7


    def test_heartbeat_is_one_parentless_commit_on_its_own_branch(self):
        import json, subprocess
        remote, repo = self.tmp / "remote.git", self.tmp / "repo"
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        for k, v in (("user.name", "t"), ("user.email", "t@t")):
            subprocess.run(["git", "-C", str(repo), "config", k, v], check=True)
        subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(remote)], check=True)
        old_owb = cr.STUDIO
        try:
            cr.STUDIO = repo
            os.environ["CHIEF_HEARTBEAT"] = "1"
            cr.push_heartbeat(T0, "idle", "cursor", "nothing queued")
            cr.push_heartbeat(T0 + 10 * MIN, "running", "cursor", "woke Cursor")
        finally:
            cr.STUDIO = old_owb
        log = subprocess.run(["git", "-C", str(remote), "log", "--format=%P|%s", "mini-heartbeat"], capture_output=True, text=True, check=True).stdout
        self.assertEqual(len(log.strip().splitlines()), 1)  # replaced, not stacked
        self.assertTrue(log.startswith("|"))  # no parent
        doc = json.loads(subprocess.run(["git", "-C", str(remote), "show", "mini-heartbeat:heartbeat.json"], capture_output=True, text=True, check=True).stdout)
        self.assertEqual((doc["state"], doc["agent"]), ("running", "cursor"))

    # ---- Ben, 14 Oct 2026: out-of-credit flags, Claude as acting Chief, and the Mini repairing itself ----

    def flags(self, flags):
        import json
        (cr.STUDIO / "scripts").mkdir(parents=True, exist_ok=True)
        (cr.STUDIO / "scripts" / "credit_flags.json").write_text(json.dumps({"flags": flags}))

    def test_a_flagged_model_is_skipped_and_its_worker_keeps_its_other_models(self):
        q = self.claude_setup('{"jobs": [{"id": "J0401", "kind": "review", "status": "open", "needs": "cloud"},'
                              ' {"id": "J0402", "kind": "assembly", "status": "open", "needs": "mini"}]}')
        os.environ["AGY_BIN"] = str(self.fake("agy", 'echo "gemini did it"'))
        self.flags({"cursor-claude-opus-5-5": {"out_until": "2026-11-06T00:00:00Z", "reason": "Other Models used up"}})
        cr.mark_down("claude", "usage limit", None, T0)
        cr.seen("chief", T0 - 10 * MIN)
        cr.cmd_run(T0)
        self.assertEqual(self.job(q, "J0401")["for"], "gemini")  # straight past Claude-in-Cursor to Gemini
        self.assertTrue(self.ran("agy"))
        self.assertEqual(cr.state_of("cursor", T0)[1], "ready")  # Cursor itself is fine for Auto jobs
        self.assertEqual(cr.routing.model_for({"kind": "assembly"}, "cursor"), "cursor-grok-4-7")

    def test_an_agent_flag_takes_it_out_until_the_reset_and_grok_posting_clears_it(self):
        self.routed_queue('{"jobs": []}')
        self.flags({"chief": {"out_until": "2026-10-16T18:00:00Z", "reason": "out of credit until Friday"},
                    "codex": {"out_until": "2026-10-07T11:00:00Z", "reason": "already over"}})
        cr.seen("chief", T0 - 10 * MIN)  # even a fresh heartbeat: the flag wins
        self.assertIn("flagged out of credit", cr.state_of("chief", T0)[1])
        self.assertTrue(cr.state_of("codex", T0)[0])  # an expired flag is ignored
        self.thread.append(("2026-10-07T11:50:00Z", "[Chief] back: PASS on J0123"))
        cr.note_grok_posts(T0)
        self.assertTrue(cr.state_of("chief", T0)[0])  # Grok posting again is proof it's back

    def test_ben_names_claude_chief_and_the_mini_clis_run_as_workers(self):
        import json
        self.routed_queue('{"jobs": [{"id": "J0403", "kind": "assembly", "status": "open", "needs": "mini"}]}')
        (cr.STUDIO / "scripts").mkdir(parents=True, exist_ok=True)
        (cr.STUDIO / "scripts" / "chief_override.json").write_text(json.dumps(
            {"agent": "claude", "until": "2026-10-16T18:00:00Z", "reason": "Ben, 14 Oct: Grok out until Friday"}))
        self.cursor = self.fake("cursor", f'echo "$@" > {self.tmp}/cursor.args; echo "cursor did it"')
        old = cr.queue_has_work
        cr.queue_has_work = lambda agent: True
        try:
            self.assertEqual(self.chief(), "claude")
            cr.cmd_run(T0)
        finally:
            cr.queue_has_work = old
        self.assertIn("Claude is Chief (reviews, PASS, merges", (self.tmp / "cursor.args").read_text())
        posts = self.posts.read_text()
        self.assertIn("**Claude is acting Chief** until 2026-10-16T18:00:00Z", posts)
        self.assertIn("Grok out until Friday", posts)
        cr.seen("chief", T0 - 10 * MIN)
        self.assertEqual(self.chief(), "chief")  # Grok working again ends it early
        self.assertIsNone(cr.override(dt.datetime(2026, 10, 17, tzinfo=dt.timezone.utc)))  # and it expires

    def beat(self, at, **extra):
        cr.write_json(cr.d("claude_beat.json"), {"fetched": cr.iso(T0), "beat": dict({"at": cr.iso(at), "who": "claude"}, **extra)})

    def test_claude_is_out_when_its_heartbeat_goes_quiet_and_back_when_it_returns(self):
        # Ben, 14 Oct 2026: flag Claude out when it runs out of usage, switch back automatically when it's back.
        self.beat(T0 - 30 * MIN)
        self.assertFalse(cr.claude_out(T0)[0])
        self.beat(T0 - 160 * MIN)
        out, why = cr.claude_out(T0)
        self.assertTrue(out)
        self.assertIn("no Claude run for 160 min", why)
        cr.mark_down("claude", "a Claude job was blocked on a usage limit", T0 + 60 * MIN, T0)
        self.beat(T0 + 5 * MIN)   # the next run after the reset
        self.assertFalse(cr.claude_out(T0 + 6 * MIN)[0])
        self.assertFalse(cr.d("down", "claude.json").exists())   # the fresh beat cleared the mark

    def test_claude_can_say_it_is_out_until_its_reset(self):
        self.beat(T0, out=True, until=cr.iso(T0 + 3 * 60 * MIN), reason="5-hour limit")
        self.assertTrue(cr.claude_out(T0 + 60 * MIN)[0])
        self.assertFalse(cr.claude_out(T0 + 4 * 60 * MIN)[0])           # past the reset: given the usual window to beat
        self.assertTrue(cr.claude_out(T0 + 6 * 60 * MIN)[0])            # and still silent 90 min after it: out

    def test_claude_counts_out_after_one_missed_hourly_run(self):
        # Ben, 15 Oct 2026: "when your usage ran out, work stopped again": 150 min was too long to wait.
        self.beat(T0 - 80 * MIN)
        self.assertFalse(cr.claude_out(T0)[0])
        self.beat(T0 - 95 * MIN)
        self.assertTrue(cr.claude_out(T0)[0])

    def test_the_newest_beat_wins_when_git_is_stale(self):
        # 15 Oct 2026 03:40Z: the Mini's git read still showed the 01:51 beat after a 03:31 push.
        old = cr.raw_claude_beat
        cr.raw_claude_beat = lambda: {"at": cr.iso(T0 - 2 * MIN), "who": "claude"}
        try:
            cr.write_json(cr.d("claude_beat.json"), {"beat": {"at": cr.iso(T0 - 120 * MIN)}})
            cr.fetch_claude_beat(T0)
            self.assertFalse(cr.claude_out(T0)[0])
        finally:
            cr.raw_claude_beat = old

    def test_no_heartbeat_yet_changes_nothing(self):
        self.assertFalse(cr.claude_out(T0)[0])

    def test_while_claude_is_out_the_next_one_down_is_chief_then_claude_takes_it_back(self):
        import json
        (cr.STUDIO / "scripts").mkdir(parents=True, exist_ok=True)
        (cr.STUDIO / "scripts" / "chief_override.json").write_text(json.dumps(
            {"agent": "claude", "until": "2026-10-16T18:00:00Z", "reason": "Ben, 14 Oct"}))
        self.beat(T0 - 200 * MIN)
        self.assertEqual(self.chief(), "cursor")                 # Claude out: the Mini chain covers
        rows = cr.acting(T0)[0]
        self.assertTrue(any(a == "claude" and not up and "out of usage" in why for a, up, why in rows))
        self.beat(T0 - 1 * MIN)
        self.assertEqual(self.chief(), "claude")                 # back: Claude is Chief again

    # ---- Ben, 21 Oct 2026: a standing chain with Claude in it, and one alert when nobody can be Chief ----

    def test_the_default_chain_puts_claude_second(self):
        del os.environ["CHIEF_CHAIN"]
        self.assertEqual(cr.chain(), ["claude", "chief", "codex", "gemini"])

    def test_claude_is_chief_after_grok_while_its_heartbeat_is_fresh_and_hands_on_and_back(self):
        os.environ["CHIEF_CHAIN"] = "chief,claude,cursor,codex"
        cr.seen("chief", T0 - 200 * MIN)                       # Grok quiet
        self.assertEqual(self.chief(), "cursor")                # no Claude heartbeat yet: Claude isn't up
        self.assertIn("no heartbeat yet", dict((a, w) for a, _, w in cr.acting(T0)[0])["claude"])
        self.beat(T0 - 20 * MIN)
        self.assertEqual(self.chief(), "claude")
        self.beat(T0 - 100 * MIN)                               # Claude missed its hourly run: next one down
        self.assertEqual(self.chief(), "cursor")
        self.beat(T0 - 2 * MIN)                                 # back
        self.assertEqual(self.chief(), "claude")
        self.beat(T0, out=True, until=cr.iso(T0 + 120 * MIN), reason="5-hour limit")
        self.assertEqual(self.chief(T0 + 10 * MIN), "cursor")  # Claude said it's out
        self.post(T0 + 20 * MIN, "[Chief] Sweep done.")
        cr.note_grok_posts(T0 + 30 * MIN)
        self.assertEqual(self.chief(T0 + 30 * MIN), "chief")   # Grok posting takes it back from anyone

    def test_with_claude_chief_the_mini_clis_run_as_workers_and_the_post_says_so(self):
        os.environ["CHIEF_CHAIN"] = "chief,claude,cursor,codex"
        self.routed_queue('{"jobs": [{"id": "J0403", "kind": "assembly", "status": "open", "needs": "mini"}]}')
        self.beat(T0 - 5 * MIN)
        self.cursor = self.fake("cursor", f'echo "$@" > {self.tmp}/cursor.args; echo "cursor did it"')
        old = cr.queue_has_work
        cr.queue_has_work = lambda agent: True
        try:
            cr.cmd_run(T0)
        finally:
            cr.queue_has_work = old
        self.assertIn("Claude is Chief (reviews, PASS, merges", (self.tmp / "cursor.args").read_text())
        posts = self.posts.read_text()
        self.assertIn("**Claude is acting Chief**", posts)
        self.assertIn("reviews, PASS, merges and final OKs go to Claude", posts)
        self.assertIn("Next in line: Cursor, Codex", posts)

    def test_an_override_naming_a_chain_member_defers_to_the_chain(self):
        import json
        os.environ["CHIEF_CHAIN"] = "chief,claude,cursor,codex"
        (cr.STUDIO / "scripts").mkdir(parents=True, exist_ok=True)
        (cr.STUDIO / "scripts" / "chief_override.json").write_text(json.dumps(
            {"agent": "claude", "until": "2026-12-31T00:00:00Z", "reason": "Ben, 21 Oct"}))
        self.beat(T0 - 5 * MIN)
        rows, who = cr.acting(T0)
        self.assertEqual(who, "claude")
        self.assertEqual([a for a, _, _ in rows].count("claude"), 1)

    def test_nobody_chief_for_three_hours_with_reviews_waiting_pings_ben_once(self):
        cr.STUDIO.mkdir(parents=True, exist_ok=True)
        (cr.STUDIO / "jobs").mkdir(exist_ok=True)
        (cr.STUDIO / "jobs" / "queue.json").write_text(
            '{"jobs": [{"id": "J0792", "status": "blocked", "result": "parked for Chief: review before Ben\'s watch"}]}')
        os.environ["CHIEF_ALERT_HOURS"] = "0-24"
        rows = [("chief", False, "quiet"), ("cursor", False, "out of usage")]
        cr.alert_no_chief(None, rows, T0)
        cr.alert_no_chief(None, rows, T0 + 2 * 60 * MIN)
        self.assertFalse(self.posts.exists())                    # under 3 h: nothing yet
        cr.alert_no_chief(None, rows, T0 + 3 * 60 * MIN)
        cr.alert_no_chief(None, rows, T0 + 4 * 60 * MIN)
        posts = self.posts.read_text()
        self.assertEqual(posts.count("@TheLaughingGod1986 no Chief"), 1)
        self.assertIn("J0792", posts)
        self.assertIn("Cursor: out of usage", posts)
        cr.alert_no_chief("claude", rows, T0 + 5 * 60 * MIN)     # a Chief is back: the spell ends
        self.assertFalse(cr.d("no_chief.json").exists())

    def test_no_alert_without_waiting_reviews_or_at_night(self):
        cr.STUDIO.mkdir(parents=True, exist_ok=True)
        (cr.STUDIO / "jobs").mkdir(exist_ok=True)
        (cr.STUDIO / "jobs" / "queue.json").write_text('{"jobs": []}')
        os.environ["CHIEF_ALERT_HOURS"] = "0-24"
        cr.alert_no_chief(None, [], T0)
        cr.alert_no_chief(None, [], T0 + 4 * 60 * MIN)
        self.assertFalse(self.posts.exists())
        (cr.STUDIO / "jobs" / "queue.json").write_text(
            '{"jobs": [{"id": "J1", "status": "blocked", "result": "parked for Chief: x"}]}')
        os.environ["CHIEF_ALERT_HOURS"] = "0-0"                  # outside the alert hours
        cr.alert_no_chief(None, [], T0 + 5 * 60 * MIN)
        self.assertFalse(self.posts.exists())

    def test_the_heartbeat_names_the_acting_chief(self):
        cr.write_json(cr.d("current.json"), {"agent": "claude", "since": cr.iso(T0)})
        self.assertEqual(cr.heartbeat_doc(T0, "idle")["chief"], "claude")

    def test_a_run_records_who_is_up_and_out_for_the_board(self):
        os.environ["CHIEF_CHAIN"] = "chief,claude,cursor,codex"
        self.beat(T0 - 5 * MIN)
        cr.mark_down("codex", "out of usage", T0 + 60 * MIN, T0)
        cr.cmd_run(T0)
        chain = cr.heartbeat_doc(T0, "idle")["chain"]
        self.assertEqual([r["agent"] for r in chain], ["chief", "claude", "cursor", "codex"])
        self.assertEqual([r["up"] for r in chain], [False, True, True, False])
        self.assertIn("retry after", chain[3]["why"])

    def test_a_stuck_mini_repairs_itself_once_and_says_so(self):
        import json
        self.routed_queue('{"jobs": []}')
        (cr.STUDIO / "scripts").mkdir(parents=True, exist_ok=True)
        calls = self.tmp / "repair.calls"
        (cr.STUDIO / "scripts" / "mini_repair.py").write_text(
            "def repair(apply, repos=None, do_caches=True, scan=True):\n"
            f"    open({str(calls)!r}, 'a').write('x')\n"
            "    return {'before_mb': 110, 'after_mb': 25000, 'caches': [], 'worktrees': ['/private/tmp/a: remove (clean)'],\n"
            "            'checkouts': [{'repo': '/x/orbit-with-ben', 'ok': True, 'actions': ['moved 7 untracked file(s)']}],\n"
            "            'biggest': []}\n")
        os.environ["CHIEF_MIN_FREE_MB"] = str(10 ** 9)  # the disk counts as low
        self.assertTrue(cr.self_heal(T0))
        self.assertTrue(cr.self_heal(T0 + 5 * MIN))  # throttled: no second repair within 30 min
        self.assertEqual(calls.read_text(), "x")
        post = self.posts.read_text()
        self.assertIn("repaired the Mini", post)
        self.assertIn("110 MB -> 25,000 MB free", post)
        self.assertIn("moved 7 untracked file(s)", post)
        self.assertEqual(json.loads((cr.STATE / "chief" / "heal.json").read_text())["after_mb"], 25000)

    def test_a_low_disk_moves_old_scratch_to_the_nas_and_says_so(self):
        import json
        (cr.STUDIO / "scripts").mkdir(parents=True, exist_ok=True)
        calls = self.tmp / "offload.calls"
        (cr.STUDIO / "scripts" / "nas_offload.py").write_text(
            "def offload(apply, target_gb=20):\n"
            f"    open({str(calls)!r}, 'a').write('x')\n"
            "    return {'before_mb': 7000, 'after_mb': 31000, 'target_mb': 20480, 'nas': 'ok', 'would': [], 'kept': [],\n"
            "            'moved': [{'path': '/private/tmp/r', 'nas': '/Volumes/data/x', 'ok': True, 'mb': 24000, 'files': 9}]}\n"
            "def summary(rep):\n"
            "    return 'NAS offload: moved 1 scratch folder(s), 24,000 MB, to the NAS (sha256 checked). 7,000 -> 31,000 MB free.'\n"
            "if __name__ == '__main__':\n"
            "    import json\n"
            "    print(json.dumps(offload(True)))\n")
        os.environ["CHIEF_OFFLOAD_ANY_OS"] = "1"
        os.environ["CHIEF_OFFLOAD_GB"] = str(10 ** 9)  # the disk counts as under target
        try:
            cr.offload_scratch(T0)  # starts it in the background and returns at once (9 Nov 2026: it held the relay 6 h)
            st = json.loads((cr.STATE / "chief" / "offload.json").read_text())
            self.assertTrue(st["running"])
            import time
            for _ in range(200):
                if not cr._pid_alive(st["pid"]):
                    break
                try:
                    os.waitpid(st["pid"], os.WNOHANG)
                except ChildProcessError:
                    pass
                time.sleep(0.05)
            cr.offload_scratch(T0 + 30 * MIN)  # reports the finished run; throttled: no second start within 3 h
        finally:
            os.environ.pop("CHIEF_OFFLOAD_ANY_OS")
            os.environ.pop("CHIEF_OFFLOAD_GB")
        self.assertEqual(calls.read_text(), "x")
        self.assertIn("moved 1 scratch folder(s)", self.posts.read_text())
        self.assertEqual(json.loads((cr.STATE / "chief" / "offload.json").read_text())["moved"], 1)

    def test_weekly_cache_clean_starts_in_the_background_once_a_week(self):
        import json
        cr.d("caches.json").unlink(missing_ok=True)
        os.environ["CHIEF_OFFLOAD_ANY_OS"] = "1"
        started = []
        class P:
            pid = 4242
        try:
            with mock.patch.object(cr.subprocess, "Popen", side_effect=lambda cmd, **kw: started.append(cmd) or P()):
                cr.weekly_caches(T0)
                cr.weekly_caches(T0 + 3 * 24 * 60 * MIN)  # 3 days later: not yet
                cr.weekly_caches(T0 + 8 * 24 * 60 * MIN)  # 8 days later: again
        finally:
            os.environ.pop("CHIEF_OFFLOAD_ANY_OS")
        self.assertEqual(len(started), 2)
        self.assertIn("--caches-only", started[0])
        self.assertEqual(json.loads((cr.STATE / "chief" / "caches.json").read_text())["pid"], 4242)

    def test_a_disk_still_full_after_repair_wakes_nobody(self):
        self.routed_queue('{"jobs": [{"id": "J0404", "kind": "assembly", "status": "open", "needs": "mini"}]}')
        (cr.STUDIO / "scripts").mkdir(parents=True, exist_ok=True)
        (cr.STUDIO / "scripts" / "mini_repair.py").write_text(
            "def repair(apply, repos=None, do_caches=True, scan=True):\n"
            "    return {'before_mb': 110, 'after_mb': 120, 'caches': [], 'worktrees': [], 'checkouts': [],\n"
            "            'biggest': ['  29,000 MB  /private/tmp/owb_comp']}\n")
        os.environ["CHIEF_MIN_FREE_MB"] = str(10 ** 9)
        os.environ["CHIEF_HARD_MIN_FREE_MB"] = "300"
        old = cr.queue_has_work
        cr.queue_has_work = lambda agent: True
        try:
            cr.cmd_run(T0)
        finally:
            cr.queue_has_work = old
        self.assertFalse(self.ran("cursor"))  # a wake would only fail at git pull and burn credit
        self.assertIn("move the version-before-last render scratch to the NAS", self.posts.read_text())

    def test_a_claim_far_past_its_eta_is_a_dead_worker_and_walks_the_chain(self):
        # 15 Oct 2026: Gemini held J0258 for 3 h past its ETA and the board showed it running.
        data = {"jobs": [
            {"id": "J1", "status": "claimed", "by": "gemini", "eta": "2026-10-07T10:00Z", "kind": "listing"},   # 2 h past
            {"id": "J2", "status": "claimed", "by": "cursor", "eta": "2026-10-07T11:40Z", "kind": "listing"},   # 20 min past: still live
            {"id": "J3", "status": "claimed", "by": "cursor", "eta": "2026-10-07T09:00Z", "kind": "chief"},     # expired role claims use the same recovery policy; elected-role claim guards still apply
            {"id": "J4", "status": "claimed", "by": "claude", "eta": "2026-10-07T09:00Z", "kind": "listing"},   # not a Mini worker
            {"id": "J5", "status": "claimed", "by": "codex", "eta": "", "kind": "listing"},                     # no ETA: unknown, left alone
        ]}
        self.assertEqual([j["id"] for j in cr.stalled_claims(data, T0)], ["J1", "J3"])


    # ---- a job that keeps hitting the time cap on one step is parked, not started again (10 Nov 2026, J2466) ----
    def capped(self, n, worker="codex", job="J0400", start=T0 - 180 * MIN, every=30):
        return [{"at": cr.iso(start + i * every * MIN), "job": job, "worker": worker, "exit": 124} for i in range(n)]

    def test_three_capped_runs_with_no_step_finished_count_as_three(self):
        job = {"id": "J0400", "history": [{"at": "2026-10-07T08:00Z", "by": "claude", "what": "added"}]}
        self.assertEqual(cr.capped_runs_in_a_row(job, self.capped(3)), 3)
        self.assertEqual(cr.capped_runs_in_a_row(job, self.capped(2)), 2)

    def test_reporting_step_zero_again_is_not_a_finished_step(self):
        job = {"id": "J0400", "history": [{"at": "2026-10-07T08:00Z", "by": "claude", "what": "added"}] + [
            {"at": cr.iso(T0 - 180 * MIN + i * 30 * MIN)[:16] + "Z", "by": "codex", "what": "step 0 of 5 done"} for i in range(3)]}
        self.assertEqual(cr.capped_runs_in_a_row(job, self.capped(3)), 3)

    def test_a_finished_step_starts_the_count_again(self):
        job = {"id": "J0400", "history": [
            {"at": "2026-10-07T08:00Z", "by": "claude", "what": "added"},
            {"at": "2026-10-07T09:45Z", "by": "codex", "what": "step 1 of 5 done: inventory written"}]}
        # runs began 09:00, 09:30, 10:00, 10:30: the step was finished during the second, so two count
        self.assertEqual(cr.capped_runs_in_a_row(job, self.capped(4)), 2)
        job["history"].append({"at": "2026-10-07T10:40Z", "by": "codex", "what": "step 1 of 5 done: said again"})
        self.assertEqual(cr.capped_runs_in_a_row(job, self.capped(4)), 2)  # the same step again is not progress

    def test_a_run_that_began_in_the_minute_of_the_last_step_is_not_counted(self):
        job = {"id": "J0400", "history": [{"at": "2026-10-07T10:30Z", "by": "codex", "what": "step 2 of 5 done"}]}
        self.assertEqual(cr.capped_runs_in_a_row(job, self.capped(4)), 0)

    def test_a_run_that_ended_by_itself_breaks_the_row(self):
        job = {"id": "J0400", "history": [{"at": "2026-10-07T08:00Z", "by": "claude", "what": "added"}]}
        runs = self.capped(2) + [{"at": cr.iso(T0 - 100 * MIN), "job": "J0400", "worker": "codex", "exit": 0}] + \
            self.capped(2, start=T0 - 60 * MIN)
        self.assertEqual(cr.capped_runs_in_a_row(job, runs), 2)  # a release with a note is a hand-back, not a loop

    def test_other_jobs_other_workers_and_a_reopen_do_not_count(self):
        job = {"id": "J0400", "history": [{"at": "2026-10-07T08:00Z", "by": "claude", "what": "added"}]}
        runs = self.capped(3, job="J0999") + self.capped(2, worker="cursor") + self.capped(1, start=T0 - 20 * MIN)
        self.assertEqual(cr.capped_runs_in_a_row(job, runs), 1)  # only the newest, by codex, on this job
        job["history"].append({"at": "2026-10-07T11:50Z", "by": "claude", "what": "reopened: narrower first step"})
        self.assertEqual(cr.capped_runs_in_a_row(job, self.capped(3)), 0)

    def stuck_setup(self, job_json):
        import json
        import jobs
        self.routed_queue('{"jobs": [' + job_json + ']}')
        q = cr.STUDIO / "jobs" / "queue.json"
        (cr.STATE / "chief").mkdir(parents=True, exist_ok=True)
        (cr.STATE / "chief" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in self.capped(3)))
        old_park, old_q = cr.park_stuck, cr.queue_has_work

        def fake_park(job, runs):  # jobs.py stuck, on the test queue (never the live one)
            data = json.loads(q.read_text())
            jobs.do_stuck(next(x for x in data["jobs"] if x["id"] == job["id"]), "relay", runs, cr.now())
            q.write_text(json.dumps(data))
            return True
        cr.park_stuck, cr.queue_has_work = fake_park, (lambda agent: True)
        self.addCleanup(lambda: setattr(cr, "park_stuck", old_park))
        self.addCleanup(lambda: setattr(cr, "queue_has_work", old_q))
        self.codex = self.fake("codex", f'echo "$@" > {self.tmp}/codex.args')
        cr.seen("chief", T0 - 10 * MIN)
        return q

    def test_a_job_capped_three_times_running_is_parked_for_the_chief_and_not_started_again(self):
        q = self.stuck_setup('{"id": "J0400", "kind": "chart", "status": "open", "needs": "mini", "progress": '
                             '{"step": 1, "of": 6}, "history": [{"at": "2026-10-07T08:00Z", "by": "claude", "what": "added"}]}')
        cr.cmd_run(T0)
        j = self.job(q, "J0400")
        self.assertEqual(j["status"], "blocked")
        self.assertIn("parked for Chief: 3 runs in a row hit the time cap at step 1 of 6", j["result"])
        self.assertTrue(cr.workflow.is_review(j))  # so it reaches the Chief's inbox
        self.assertEqual(j["progress"], {"step": 1, "of": 6})  # kept: nothing is redone
        self.assertFalse(self.ran("codex"))
        self.assertIn("J0400 is parked for the Chief", self.posts.read_text())

    def test_two_capped_runs_are_not_enough(self):
        import json
        q = self.stuck_setup('{"id": "J0400", "kind": "chart", "status": "open", "needs": "mini", '
                             '"history": [{"at": "2026-10-07T08:00Z", "by": "claude", "what": "added"}]}')
        (cr.STATE / "chief" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in self.capped(2)))
        cr.cmd_run(T0)
        self.assertEqual(self.job(q, "J0400")["status"], "open")
        self.assertTrue(self.ran("codex"))

    def test_if_parking_fails_the_job_runs_as_before(self):
        q = self.stuck_setup('{"id": "J0400", "kind": "chart", "status": "open", "needs": "mini", '
                             '"history": [{"at": "2026-10-07T08:00Z", "by": "claude", "what": "added"}]}')
        cr.park_stuck = lambda job, runs: False
        cr.cmd_run(T0)
        self.assertEqual(self.job(q, "J0400")["status"], "open")
        self.assertTrue(self.ran("codex"))


class PromptNamesTheRuleFiles(unittest.TestCase):
    """J2577: the relay's prompt names the studio's AGENTS.md and then the channel's own studio/RULES.md, for each
    checkout that has one. A checkout that has not split its rules yet reads as it always did."""

    FILL = dict(name="Codex", agent="codex", why="a test", authority="A", priority="P", role="a specialist worker")

    def checkout(self, root, name, split):
        path = pathlib.Path(root) / name
        (path / "studio").mkdir(parents=True)
        if split:
            (path / "studio" / "RULES.md").write_text("# rules\n")
        return path

    def brief(self, checkouts):
        return cr.PROMPT.format(**self.FILL, **cr.brief_channels("codex", checkouts))

    def test_each_channel_is_told_the_files_its_checkout_has(self):
        with tempfile.TemporaryDirectory() as d:
            o, h = self.checkout(d, "o", True), self.checkout(d, "h", False)
            p = self.brief({"owb": o, "hos": h})
            self.assertIn(f'1. Orbit With Ben ({o}): git pull. Read AGENTS.md and then studio/RULES.md (the rules, the Never list, '
                          '"Stop and ask Ben", "Who does what",\n', p)
            self.assertIn(f'2. History of Science ({h}): git pull. Read its AGENTS.md ("The desk"). Run its desk inbox:\n', p)
            self.assertIn("Do them in the HOS checkout, following its AGENTS.md.", p)
            p = self.brief({"owb": self.checkout(d, "o2", True), "hos": self.checkout(d, "h2", True)})
            self.assertIn('Read its AGENTS.md and then studio/RULES.md ("The desk").', p)
            self.assertIn("Do them in the HOS checkout, following its AGENTS.md and then studio/RULES.md.", p)

    def test_with_no_channel_file_the_prompt_reads_as_it_always_did(self):
        with tempfile.TemporaryDirectory() as d:
            o = self.checkout(d, "o", False)
            p = self.brief({"owb": o, "hos": self.checkout(d, "h", False)})
        self.assertIn(f'1. Orbit With Ben ({o}): git pull. Read AGENTS.md (the rules, the Never list, "Stop and ask Ben", '
                      '"Who does what",\n', p)
        self.assertNotIn("studio/RULES.md", p)

    def test_by_default_every_channel_in_the_channel_files_is_in_the_brief(self):
        p = cr.PROMPT.format(**self.FILL, **cr.brief_channels("codex"))
        for slug in cr.channels.slugs():
            self.assertIn(f"{cr.channels.name(slug)} (", p)
        self.assertNotRegex(p, r"\{\w+\}")                       # nothing left unfilled


BRIEF_BEFORE_J2618 = '''You are {name}, {role} on the Mac mini because {why}. You run unattended: do ONE job, then stop.
Your agent id is `{agent}` everywhere (jobs.py --agent, studio.py --by, hos_desk.py --as/--from).

0. If a git pull fails (no space left, or local files in the way), run  python3 scripts/mini_repair.py --apply
   (safe: caches, clean temp worktrees; blocking files are kept in ~/_desk/rescue, local edits stashed, local commits
   pushed to a rescue branch first) and pull again. Still under 20 GB free: move render scratch to the NAS by
   AGENTS.md "Render scratch" before anything else.
1. Orbit With Ben ({owb}): git pull. Read {owb_rules} (the rules, the Never list, "Stop and ask Ben", "Who does what",
   "Chief relay"). Run: python3 scripts/owb_thread.py read   and   python3 scripts/studio.py board
2. History of Science ({hos}): git pull. Read its {hos_rules} ("The desk"). Run its desk inbox:
     python3 00_Brand/Channel-Setup/tools/hos_desk.py inbox --as {agent}   (run in the HOS checkout; there is no scripts/hos_desk.py)
3. Follow the DISPATCH PRIORITY or CHIEF REVIEW PRIORITY below first, if supplied; otherwise, which channel first (Ben, 9 Oct: 4 videos a month on each channel; credits follow):
     python3 scripts/channel_balance.py --hos "{hos}"
   If it says History of Science first: take the single oldest HOS desk task you can do now, and go to step 4. Only if
   there is none, fall through to the OWB queue below.
   Queue jobs marked `hos` (repo: hos, e.g. "HOS 007 Shorts VO") are NOT HOS desk tasks: they are normal queue jobs
   that `jobs.py next` hands out like any other. Do them in the HOS checkout, following its {hos_rules}. "HOS desk tasks"
   means only desk #180 messages that are not in the queue.
   The OWB job queue (AGENTS.md "Job queue"):  python3 scripts/jobs.py next --agent {agent} --can mini,gemini,any --git
   If it prints a job, that job is yours: do it (step 4), then  jobs.py done|block|release <id> --agent {agent} ... --git.
   Ben watches % done on the board: split the job into n steps (replace a default_plan at step 0; otherwise keep its earlier n) and run
     python3 scripts/jobs.py progress <id> --agent {agent} --step <k> --of <n> --git
   with --action "<plain-English action still unfinished>"; update that action as the remaining work changes. Use k=0 when you start and again after each finished step (k = steps done), before you release or finish.
   During a long step, repeat the current k with an honest --note at least every 5 minutes; never increase k for elapsed time.
   As soon as you choose the video(s), include --films HOS:006 (or OWB:028,OWB:029 for a shared job) on that progress
   command, and --note with the concrete outcome of each finished step. Keep the links on later progress updates.
   This connects the live job to the video's swim lane. A job parked for review is not an approved film stage.
   Inspect your actual input tools once at session start. Record demonstrated audio_input/moving_video_input only
   if this session can really perceive that medium (ffmpeg, ASR, a player window or a model name is not proof):
     python3 scripts/chief_relay.py capabilities --agent {agent} --available '<demonstrated identifiers, or empty>' --evidence '<actual tool/probe result>'
   If the assigned work cannot proceed because of an input capability, park it with a typed hold, not a generic
   six-hour input retry: jobs.py wait <id> --agent {agent} --type capability --requires audio_input
   --condition '<what input is unavailable and what was actually tested>' --check-at '<future UTC time>' --git.
   For a condition verification, update its original parent with --recheck <verification id> and finish the
   verification itself. Never claim to hear audio or review motion from text/stills/measurements.
   If it exits 10 (nothing waiting): pick the single oldest task for the Chief that isn't in the queue (on the HOS
   desk, or a Claude message on #99 asking the Chief for something with no Chief reply yet).
   If nothing is waiting anywhere, stop without posting.
4. Do that one task, following that repo's AGENTS.md exactly: claim before work (studio.py claim --git, or the HOS
   desk's own rule), commit only from a clean worktree (your own: `git worktree add --detach <dir> origin/main` or
   `-b <branch>`; never `git worktree add --force <dir> main`, which moves main under the shared checkout), never spend money or credit beyond the written rules, never
   upload, schedule, retitle or change privacy on YouTube unless the job brief or a Chief/Claude message for that task
   says to, never delete a video or anything on the NAS, and never print secrets. Chief owns AGENTS.md and the Never list
   (Ben, 9-10 Oct 2026): a job added by chief, a "[Chief]" OK, or a brief saying "Ben approved (relayed by Chief)" is
   full authorisation, including Never-list exceptions it names. Never ask Ben to re-post an OK on #99. If a step needs
   Ben (real money, a sign-in, something that can't be undone), say so in your report and stop.
   A job that needs `gemini` is a facts-and-numbers check: run it through Gemini with the `agy` CLI (AGENTS.md "Who does
   what"), claim it as {agent}/gemini, and commit Gemini's findings as the job says. You check Gemini's output is complete;
   you don't rewrite its findings or any spoken line.
5. Report: OWB by writing the report to a file and posting it with  python3 scripts/owb_thread.py post -f <file>
   (start with "{name} covering"); HOS with  hos_desk.py post --from {agent} --to claude ...  Say what you did,
   what's next, and what blocks you. Never put the report text on the command line: the shell runs any backtick
   or $(...) in it as a command and posts the output.
{authority}
{priority}
   Each job's kind selects its specialist worker. Acting-Chief authority is a separate role; a worker fallback does
   not inherit it merely because it runs Claude or GPT.
Your run is killed at 25 minutes. Anything that takes longer (a full render, a big download, a batch of picture jobs):
start it detached so it outlives you, e.g.
   tmux new -d -s <job>-render "cd <dir> && <command> > ~/_desk/logs/<job>-render.log 2>&1; echo $? > ~/_desk/logs/<job>-render.done"
then release the job with a note naming the tmux session, the log and the .done file. The next run checks that file:
missing means still running (leave it, take a quick job meanwhile); present means read the exit code and the log, and
carry on. Never start a second copy of a render that is still running.
Otherwise, if a job will take longer than about 20 minutes, stop at a clean point, release your claim with a note,
report, and stop.
'''


class TheBriefIsBuiltFromTheChannelFiles(unittest.TestCase):
    """J2618, 11 Nov 2026: chief_relay.py names no channel. The brief it gives every agent on the Mini is put together
    from the channel files. For today's two channels it must read as the hand-written one did, word for word: that
    text, as it stood on main before the change, is BRIEF_BEFORE_J2618 above. The one intended difference is the
    thread tool's file name, which moved to studio_thread.py in J2620 (the old name still runs the same tool)."""

    COMMON = dict(name="Codex", agent="codex", why="it is first in line", authority="AUTHORITY", priority="PRIORITY",
                  role="a specialist worker")
    O, H = pathlib.Path("/Users/x/YouTube/orbit-with-ben"), pathlib.Path("/Users/x/YouTube/History Of Science")

    def sky(self, **more):
        base = cr.channels._load()
        home = next(c for c in base if c.get("home"))
        sky = dict(home, slug="sky", label="SKY", name="Night Sky", short="Sky", home=False, order=3,
                   title_match=r"\bSKY\b", youtube={"studio_port": "9300"},
                   repo={"url": "https://github.com/example/night-sky.git", "env": "SKY_REPO", "checkouts": ["Night Sky"]},
                   **more)
        sky.pop("cadence", None)
        return mock.patch.object(cr.channels, "_load", lambda directory=None: base + (sky,))

    def rules(self, studio, other):
        return mock.patch.object(cr.channels, "rules_phrase", lambda path: studio if path == self.O else other)

    def test_todays_brief_is_the_old_one_word_for_word(self):
        for studio, other in (("AGENTS.md and then studio/RULES.md", "AGENTS.md and then studio/RULES.md"),
                              ("AGENTS.md and then studio/RULES.md", "AGENTS.md"), ("AGENTS.md", "AGENTS.md")):
            with self.subTest(rules=(studio, other)), self.rules(studio, other):
                now = cr.PROMPT.format(**self.COMMON, **cr.brief_channels("codex", {"owb": self.O, "hos": self.H}))
                was = BRIEF_BEFORE_J2618.format(**self.COMMON, owb=self.O, hos=self.H, owb_rules=studio, hos_rules=other)
                self.assertEqual(was.count("scripts/owb_thread.py"), 2)
                self.assertEqual(now, was.replace("scripts/owb_thread.py", "scripts/studio_thread.py"))

    def test_the_sentence_a_worker_gets_is_the_old_one(self):
        self.assertEqual(cr.worker_only_steps(),
                         "In step 3 skip the channel check and the HOS desk inbox: do only the job "
                         "`jobs.py next` gives you, and that includes `hos` queue jobs (repo: hos), which are normal "
                         "queue jobs, not desk tasks: do them in the HOS checkout. If it exits 10, stop without posting")

    def test_a_third_channel_gets_its_own_lines_and_changes_nobody_elses(self):
        sky = pathlib.Path("/Users/x/YouTube/Night Sky")
        with self.rules("AGENTS.md", "AGENTS.md"):
            two = cr.PROMPT.format(**self.COMMON, **cr.brief_channels("codex", {"owb": self.O, "hos": self.H}))
            with self.sky():
                three = cr.PROMPT.format(**self.COMMON, **cr.brief_channels("codex", {"owb": self.O, "hos": self.H, "sky": sky}))
        self.assertIn(f"2b. Night Sky ({sky}): git pull. Read its AGENTS.md.\n3. Follow the DISPATCH PRIORITY", three)
        self.assertIn(f'python3 scripts/channel_balance.py --hos "{self.H}" --sky "{sky}"\n', three)
        self.assertIn("   Queue jobs marked `sky` (repo: sky) are normal queue jobs that `jobs.py next` hands out like any other.\n"
                      "   Do them in the SKY checkout, following its AGENTS.md.\n", three)
        added = [line for line in three.splitlines() if line not in two.splitlines()]
        gone = [line for line in two.splitlines() if line not in three.splitlines()]
        self.assertEqual(len(added), 4, added)                     # its step, the balance line, its two queue lines
        self.assertEqual(gone, [f'     python3 scripts/channel_balance.py --hos "{self.H}"'])
        self.assertNotIn("SKY desk", three)                        # it has no desk, so no desk line names it

    def test_a_third_channel_with_a_desk_gets_the_desk_lines_too(self):
        sky = pathlib.Path("/Users/x/YouTube/Night Sky")
        with self.rules("AGENTS.md", "AGENTS.md"), self.sky(desk={"tool": "tools/sky_desk.py", "number": 12}):
            p = cr.PROMPT.format(**self.COMMON, **cr.brief_channels("codex", {"owb": self.O, "hos": self.H, "sky": sky}))
        self.assertIn("(jobs.py --agent, studio.py --by, hos_desk.py --as/--from, sky_desk.py --as/--from).", p)
        self.assertIn(f'2b. Night Sky ({sky}): git pull. Read its AGENTS.md ("The desk"). Run its desk inbox:\n'
                      "     python3 tools/sky_desk.py inbox --as codex   (run in the SKY checkout; there is no scripts/sky_desk.py)", p)
        self.assertIn("   If it says Night Sky first: take the single oldest SKY desk task you can do now, and go to step 4.", p)
        self.assertIn('means only desk #12 messages that are not in the queue.', p)
        self.assertIn("(on the HOS or SKY\n   desk, or a Claude message on #99", p)
        self.assertIn("; HOS with  hos_desk.py post --from codex --to claude ...; SKY with  sky_desk.py post --from codex --to claude ...", p)

    def test_the_studio_alone_still_gets_a_brief(self):
        with self.rules("AGENTS.md", "AGENTS.md"):
            p = cr.PROMPT.format(**self.COMMON, **cr.brief_channels("codex", {"owb": self.O}))
        self.assertIn("2. No other channel is plugged in.\n3. Follow", p)
        self.assertIn("(jobs.py --agent, studio.py --by).", p)
        self.assertIn("claim before work (studio.py claim --git), commit only", p)
        self.assertNotIn("desk", p.split("3. Follow")[1].split("4. Do that one task")[0].replace("HOS desk", ""))
        with mock.patch.object(cr, "OTHERS", {}):
            self.assertEqual(cr.worker_only_steps(), "In step 3 skip the channel check: do only the job `jobs.py next` "
                                                     "gives you. If it exits 10, stop without posting")

    def test_every_cli_is_allowed_each_other_channels_checkout_and_the_desk_folder(self):
        with mock.patch.object(cr, "OTHERS", {"hos": self.H}), mock.patch.object(cr, "STATE", pathlib.Path("/Users/x/_desk/state")):
            self.assertEqual(cr.add_dirs(), "--add-dir '/Users/x/YouTube/History Of Science' --add-dir /Users/x/_desk")
            for agent in ("codex", "gemini", "claudecode"):
                with self.subTest(agent=agent), mock.patch.dict(os.environ, {"CODEX_BIN": "/bin/echo", "AGY_BIN": "/bin/echo",
                                                                             "CLAUDE_BIN": "/bin/echo"}):
                    os.environ.pop("AGY_FLAGS", None), os.environ.pop("CLAUDE_CODE_FLAGS", None)
                    _bin, args = cr.cli_spec(agent, "")
                    at = args.index("--add-dir")                 # the folder with a space in its name is one argument
                    self.assertEqual(args[at:at + 4], ["--add-dir", "/Users/x/YouTube/History Of Science", "--add-dir", "/Users/x/_desk"])
        with mock.patch.object(cr, "OTHERS", {"hos": self.H, "sky": pathlib.Path("/s")}), \
                mock.patch.object(cr, "STATE", pathlib.Path("/Users/x/_desk/state")):
            self.assertEqual(cr.add_dirs(), "--add-dir '/Users/x/YouTube/History Of Science' --add-dir /s --add-dir /Users/x/_desk")

    def test_the_checkouts_are_the_ones_the_old_constants_named(self):
        home = pathlib.Path("/Users/x")
        with mock.patch.dict(os.environ, {"OWB_REPO": "", "HOS_REPO": ""}):
            self.assertEqual(cr.channels.studio_checkout(home), home / "YouTube" / "orbit-with-ben")
            self.assertEqual(cr.channels.repo_path("hos", home), home / "YouTube" / "History Of Science")
        with mock.patch.dict(os.environ, {"OWB_REPO": "/elsewhere/o", "HOS_REPO": "/elsewhere/h"}):
            self.assertEqual(cr.channels.studio_checkout(home), pathlib.Path("/elsewhere/o"))
            self.assertEqual(cr.channels.repo_path("hos", home), pathlib.Path("/elsewhere/h"))

    def test_the_studios_own_names_come_from_the_registry(self):
        src = pathlib.Path(cr.__file__).read_text()
        self.assertIn('env[channels.studio_env("AGENT")] = agent', src)
        self.assertIn('f"https://raw.githubusercontent.com/{channels.studio_github()}/"', src)
        self.assertEqual(cr.channels.studio_env("AGENT"), "OWB_AGENT")
        self.assertEqual(cr.channels.studio_github(), "TheLaughingGod1986/orbit-with-ben")

    def test_the_spend_ledger_and_the_film_folders_are_where_they_were(self):
        with mock.patch.object(cr, "STUDIO", pathlib.Path("/o")), mock.patch.object(cr, "HOME", pathlib.Path("/Users/x")), \
                mock.patch.dict(os.environ, {"OWB_REPO": ""}):
            self.assertEqual(cr.STUDIO / cr.channels.studio_records("ai_spend", "ledger.jsonl").relative_to(cr.channels.ROOT),
                             pathlib.Path("/o/05_Analytics/ai_spend/ledger.jsonl"))
            self.assertEqual(cr.board_films(), pathlib.Path("/Users/x/YouTube/orbit-with-ben/02_Video-Projects"))

    def test_the_script_names_no_channel_and_reaches_into_no_channels_folder(self):
        import test_channel_ratchet as ratchet
        src = pathlib.Path(cr.__file__).read_text()
        self.assertEqual(ratchet.channel_lines(src), {})
        self.assertEqual(ratchet.home_lines(src), {})


if __name__ == "__main__":
    unittest.main()
