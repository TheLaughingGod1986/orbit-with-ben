"""chief_relay.py: the first agent in the chain that is up acts as Chief; out of credit falls through; Grok takes back."""
import datetime as dt, os, pathlib, stat, sys, tempfile, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chief_relay as cr  # noqa: E402

T0 = dt.datetime(2026, 10, 7, 12, 0, tzinfo=dt.timezone.utc)
MIN = dt.timedelta(minutes=1)


class Relay(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.old_state, self.old_home = cr.STATE, cr.HOME
        cr.STATE, cr.HOME = self.tmp / "state", self.tmp  # so a real CLI on this machine can't stand in for a fake
        cr.STATE.mkdir()
        self.posts = self.tmp / "posts.txt"
        notify = self.tmp / "notify.sh"
        notify.write_text(f'#!/bin/sh\necho "$1" >> "{self.posts}"\n')
        notify.chmod(notify.stat().st_mode | stat.S_IEXEC)
        self.env = dict(os.environ)
        os.environ.update({"CHIEF_NOTIFY": str(notify), "CHIEF_HOURS": "0-24", "CHIEF_CHAIN": "chief,cursor,codex"})
        self.cursor = self.fake("cursor", 'echo "cursor did J0001"')
        self.codex = self.fake("codex", 'echo "codex did J0001"')
        os.environ["CURSOR_AGENT_BIN"], os.environ["CODEX_BIN"] = str(self.cursor), str(self.codex)

    def tearDown(self):
        cr.STATE, cr.HOME = self.old_state, self.old_home
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

    def test_pause_file_stops_runs(self):
        (cr.STATE / "chief-relay.pause").write_text("")
        cr.cmd_run(T0)
        self.assertFalse(self.ran("cursor"))

    def test_status_shows_gemini_as_the_checker(self):
        os.environ["AGY_BIN"] = str(self.cursor)
        self.assertIn("Checker: Gemini (agy found)", cr.gemini_line())

    def test_chain_order_comes_from_the_env(self):
        os.environ["CHIEF_CHAIN"] = "chief,codex,cursor"
        self.assertEqual(self.chief(), "codex")


if __name__ == "__main__":
    unittest.main()
