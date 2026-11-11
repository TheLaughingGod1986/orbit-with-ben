#!/usr/bin/env python3
"""Tests for Claude and Gemini usage parsers in scripts/ai_spend_daily.py (J1201)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_spend  # noqa: E402
import ai_spend_daily  # noqa: E402

CLAUDE_USAGE_PAGE = """Settings
Profile
Appearance
Account
Privacy
Usage
Capabilities
Plan usage limits
Current session
Resets in 3 hr 14 min
18% used
Weekly limits
Learn more about weekly usage limits
All models
Resets Thu 29 Oct 10:00
42% used
"""

CLAUDE_USAGE_ALT_PAGE = """Plan usage limits
Current session
25% used
Resets in 4 hr 10 min
Current week (all models)
60% used
Resets Mon 02 Nov 09:00
Current week (Sonnet only)
15% used
Resets Mon 02 Nov 09:00
"""

CLAUDE_LIVE_PRO_PAGE = """Settings
Usage
Your usage
Pro
27% of your weekly limit used.
Current session
Resets at 8:50 PM
96% used
This week
Resets Wednesday 10:00 AM
27% used
Limit resets
No resets right now
When you get one, it shows up here with its expiry date.
Usage credits
Available for any task. Promotional credits are used before purchased credits.
£0
Monthly spend limit
£0.00 of £75 this month · Auto-reload off
This week’s usage by product
Claude Code
100%
Chats
0%
"""

CLAUDE_LOGIN_PAGE = """Sign in - Claude
Question what’s next
Your thinking partner for big ambitions
Continue with Google
Continue with Apple
OR
Continue with email
Continue with SSO
"""

GEMINI_USAGE_TSV = (
    "Gemini Models\tWeekly Limit Remaining\t46%\t2026-10-30T22:00:11Z\n"
    "Gemini Models\tFive Hour Limit Remaining\t97%\t2026-10-30T11:56:56Z\n"
    "Claude and GPT models\tWeekly Limit Remaining\t100%\t2026-11-06T07:38:18Z\n"
    "Claude and GPT models\tFive Hour Limit Remaining\t100%\t2026-10-30T12:38:18Z\n"
)

GEMINI_USAGE_TTY = """Quota:
Gemini Models          Weekly Limit Remaining     46%   2026-10-30 22:00 GMT
Gemini Models          Five Hour Limit Remaining  97%   2026-10-30 11:56 GMT
Claude and GPT models  Weekly Limit Remaining     100%  2026-11-06 07:37 GMT
Claude and GPT models  Five Hour Limit Remaining  100%  2026-10-30 12:37 GMT
"""


class ClaudeUsageParser(unittest.TestCase):
    def test_standard_settings_usage_page(self):
        r = ai_spend_daily.parse_claude(CLAUDE_USAGE_PAGE)
        self.assertEqual((r["left"], r["total"]), (58, 100))
        self.assertEqual(r["used"], {"session": 18, "weekly": 42})
        self.assertEqual(r["note"], "18% used (resets in 3 hr 14 min) session; weekly 42% used, resets Thu 29 Oct 10:00")
        self.assertEqual(ai_spend.POOLS["claude"], "%")

    def test_current_week_all_models_layout(self):
        r = ai_spend_daily.parse_claude(CLAUDE_USAGE_ALT_PAGE)
        self.assertEqual((r["left"], r["total"]), (40, 100))
        self.assertEqual(r["used"], {"session": 25, "weekly": 60})
        self.assertEqual(r["note"], "25% used (resets in 4 hr 10 min) session; weekly 60% used, resets Mon 02 Nov 09:00")

    def test_live_pro_this_week_layout(self):
        r = ai_spend_daily.parse_claude(CLAUDE_LIVE_PRO_PAGE)
        self.assertEqual((r["left"], r["total"]), (73, 100))
        self.assertEqual(r["used"], {"session": 96, "weekly": 27})
        self.assertEqual(r["note"], "96% used (resets 8:50 PM) session; weekly 27% used, resets Wednesday 10:00 AM")

    def test_signed_out_or_changed_page_fails_loudly(self):
        with self.assertRaises(RuntimeError):
            ai_spend_daily.parse_claude(CLAUDE_LOGIN_PAGE)

    def test_a_bare_resets_line_is_not_given_the_next_lines_figure(self):
        """Ledger notes of 6 to 8 Nov read "0% used (resets 0% used) session": no session was running, so the
        "Resets" line had no time and the reader took the next line. The page shape here is worked back from that note."""
        page = CLAUDE_LIVE_PRO_PAGE.replace("Resets at 8:50 PM\n96% used", "Resets\n0% used").replace("27% used", "100% used")
        r = ai_spend_daily.parse_claude(page)
        self.assertEqual(r["left"], 0)
        self.assertEqual(r["note"], "0% used session; weekly 100% used, resets Wednesday 10:00 AM")


class GeminiUsageParser(unittest.TestCase):
    def test_agy_usage_tsv_output(self):
        r = ai_spend_daily.parse_gemini(GEMINI_USAGE_TSV)
        self.assertEqual((r["left"], r["total"]), (46, 100))
        self.assertEqual(r["used"], {"weekly": 54, "five_hour": 3})
        self.assertEqual(r["note"], "5-hour 3% used (resets 11:56Z) session; weekly 54% used, resets Fri 30 Oct 22:00Z")
        self.assertEqual(ai_spend.POOLS["gemini"], "%")

    def test_agy_usage_tty_table_output(self):
        r = ai_spend_daily.parse_gemini(GEMINI_USAGE_TTY)
        self.assertEqual((r["left"], r["total"]), (46, 100))
        self.assertEqual(r["used"], {"weekly": 54, "five_hour": 3})
        self.assertEqual(r["note"], "5-hour 3% used (resets 11:56Z) session; weekly 54% used, resets Fri 30 Oct 22:00Z")

    def test_missing_weekly_limit_fails_loudly(self):
        with self.assertRaises(RuntimeError):
            ai_spend_daily.parse_gemini("Model credits\nRemaining credits  0\n")

    def test_both_pools_in_daily_all_and_readers(self):
        self.assertIn("claude", ai_spend_daily.ALL)
        self.assertIn("gemini", ai_spend_daily.ALL)
        self.assertIn("claude", ai_spend_daily.READERS)
        self.assertIn("gemini", ai_spend_daily.READERS)


class ExitCodeTellsTheTruth(unittest.TestCase):
    """J2564: exit 1 means a spending figure is missing. A usage page that could not be read is named, not a failure."""

    GOOD = {"left": 10, "total": 100, "note": "n"}

    def run_main(self, readers, argv, record_rc=0, ledger=()):
        import contextlib
        import io
        from unittest import mock

        def fail(msg, kind=RuntimeError):
            def reader():
                raise kind(msg)
            return reader

        table = {k: (fail(*v) if isinstance(v, tuple) else fail(v) if isinstance(v, str) else (lambda v=v: dict(v)))
                 for k, v in readers.items()}
        out = io.StringIO()
        with mock.patch.dict(ai_spend_daily.READERS, table), \
                mock.patch.object(ai_spend_daily, "last_left", lambda pool: None), \
                mock.patch.object(ai_spend_daily, "last_record",
                                  lambda pool: next((r for r in reversed(ledger) if r["pool"] == pool), None)), \
                mock.patch.object(ai_spend_daily.subprocess, "run",
                                  lambda *a, **k: mock.Mock(returncode=record_rc)), \
                contextlib.redirect_stdout(out):
            rc = ai_spend_daily.main(argv)
        return rc, out.getvalue()

    def test_three_unread_usage_pages_do_not_fail_the_run(self):
        """The three days in the J2559 report: every spending figure read, three usage pages not."""
        rc, out = self.run_main({
            "elevenlabs": self.GOOD, "flow": self.GOOD, "vertex": self.GOOD, "gemini": self.GOOD,
            "cursor": "no 'Cursor Models' or 'Other Models · N% used' line on the Cursor spending page (signed out, or the page changed)",
            "codex": ("no rate_limits reading in the Codex session logs", ValueError),
            "claude": "no 'Current session' or weekly 'N% used' line on the Claude usage page (signed out, or the page changed)",
        }, ["--dry-run"])
        self.assertEqual(rc, 0)
        for pool in ("cursor", "codex", "claude"):
            self.assertIn(f"UNREAD {pool}:", out)
        self.assertNotIn("FAIL ", out)
        self.assertIn("usage pages not read (no spending figure is missing): cursor, codex, claude", out)
        self.assertIn("every spending figure asked for was read", out)

    def test_each_spend_pool_unread_fails_the_run(self):
        for pool in ai_spend_daily.SPEND:
            readers = {p: self.GOOD for p in ai_spend_daily.ALL}
            readers[pool] = "could not read it"
            rc, out = self.run_main(readers, ["--dry-run"])
            self.assertEqual(rc, 1, pool)
            self.assertIn(f"FAIL {pool}:", out)
            self.assertIn(f"SPENDING FIGURE MISSING: {pool}", out)

    def test_spend_pools_are_the_three_that_cost_credit_or_money(self):
        self.assertEqual(set(ai_spend_daily.SPEND), {"elevenlabs", "flow", "vertex"})
        self.assertTrue(set(ai_spend_daily.SPEND) <= set(ai_spend_daily.ALL))

    def test_a_reading_that_cannot_be_written_fails_the_run_even_for_a_usage_page(self):
        rc, out = self.run_main({"gemini": self.GOOD}, ["--pools", "gemini"], record_rc=1)
        self.assertEqual(rc, 1)
        self.assertIn("FAIL gemini: the reading could not be written to the ledger", out)

    def test_readings_that_work_are_still_recorded_when_others_fail(self):
        import contextlib
        import io
        from unittest import mock
        calls = []
        table = {"elevenlabs": lambda: dict(self.GOOD), "claude": lambda: (_ for _ in ()).throw(RuntimeError("x")),
                 "gemini": lambda: dict(self.GOOD)}
        with mock.patch.dict(ai_spend_daily.READERS, table), \
                mock.patch.object(ai_spend_daily, "last_record", lambda pool: None), \
                mock.patch.object(ai_spend_daily.subprocess, "run",
                                  lambda cmd, **k: calls.append(cmd) or mock.Mock(returncode=0)), \
                contextlib.redirect_stdout(io.StringIO()):
            rc = ai_spend_daily.main(["--pools", "elevenlabs,claude,gemini"])
        self.assertEqual(rc, 0)
        self.assertEqual([c[c.index("--pool") + 1] for c in calls], ["elevenlabs", "gemini"])

    def test_an_unread_page_says_when_the_pool_was_last_recorded_and_by_whom(self):
        from datetime import datetime, timezone
        ledger = [{"pool": "codex", "kind": "record", "left": 96.0, "at": "2026-11-11T05:12:45Z", "by": "macbook"}]
        from unittest import mock
        with mock.patch.object(ai_spend_daily, "last_record", lambda pool: ledger[-1] if pool == "codex" else None):
            now = datetime(2026, 11, 11, 8, 30, tzinfo=timezone.utc)
            self.assertEqual(ai_spend_daily.last_recorded("codex", now), "last recorded 11 Nov 05:12Z by macbook (3 h ago)")
            self.assertEqual(ai_spend_daily.last_recorded("claude", now), "never recorded")
            late = datetime(2026, 11, 15, 8, 30, tzinfo=timezone.utc)
            self.assertIn("(4 days ago)", ai_spend_daily.last_recorded("codex", late))

    def test_a_codex_only_run_exits_0_when_the_log_has_no_reading(self):
        rc, out = self.run_main({"codex": ("no Codex session logs under /x", ValueError)},
                                ["--pools", "codex", "--codex-pool", "codex"])
        self.assertEqual(rc, 0)
        self.assertIn("likely cause: Codex has not run on this machine", out)
        self.assertNotIn("every spending figure", out)

    def test_strict_is_for_a_caller_that_must_know_its_one_pool_was_recorded(self):
        """The MacBook worker stamps "recorded" on exit 0; an unread page must not earn the stamp."""
        argv = ["--pools", "codex", "--codex-pool", "codex", "--strict"]
        rc, out = self.run_main({"codex": ("no Codex session logs under /x", ValueError)}, argv)
        self.assertEqual(rc, 1)
        self.assertIn("UNREAD codex:", out)
        self.assertEqual(self.run_main({"codex": self.GOOD}, argv)[0], 0)


class LikelyCause(unittest.TestCase):
    CHANGED = "RuntimeError: no 'Current session' or weekly 'N% used' line on the Claude usage page (signed out, or the page changed)"

    def test_sign_in_screen_is_bens(self):
        self.assertIn("Ben's sign-in", ai_spend_daily.likely_cause(self.CHANGED, CLAUDE_LOGIN_PAGE))
        self.assertIn("Ben's sign-in", ai_spend_daily.likely_cause("RuntimeError: claude.ai is signed out in the CDP Chrome"))

    def test_signed_in_page_with_other_wording_is_a_reader_fix(self):
        page = "Settings\nUsage\nYou have reached your weekly limit\nYour limit resets Wednesday 10:00 AM\n"
        self.assertIn("the reader needs a fix", ai_spend_daily.likely_cause(self.CHANGED, page))

    def test_empty_page(self):
        self.assertIn("came back empty", ai_spend_daily.likely_cause(self.CHANGED, "  \n"))

    def test_codex_causes(self):
        self.assertIn("wrote no limit reading", ai_spend_daily.likely_cause(
            "ValueError: no rate_limits reading in the Codex session logs (lines with rate_limits: 0; none holds a limit window)"))
        self.assertIn("for three days", ai_spend_daily.likely_cause("ValueError: newest Codex reading is 90 h old"))

    def test_browser_not_answering(self):
        self.assertIn("debugging port", ai_spend_daily.likely_cause("Error: BrowserType.connect_over_cdp: connect ECONNREFUSED"))


class PageExcerpt(unittest.TestCase):
    AT = "@"  # the test addresses are put together here so no address, even a made-up one, sits in a tracked file

    def test_no_address_and_no_payment_line_reaches_the_log(self):
        page = f"Usage\n\nsomeone.name{self.AT}example.org\nSigned in as a.b{self.AT}example.com on Pro\n" \
               "Visa ending 4242\nPayment method\n•••• 4242\nYou have reached your weekly limit\n"
        lines = ai_spend_daily.page_excerpt(page)
        self.assertEqual(lines, ["Usage", "<email>", "Signed in as <email> on Pro", "You have reached your weekly limit"])
        self.assertNotIn("@", "".join(lines))

    def test_capped(self):
        self.assertEqual(len(ai_spend_daily.page_excerpt("\n".join(f"line {i}" for i in range(80)))), 25)
        self.assertEqual(len(ai_spend_daily.page_excerpt("x" * 500)[0]), 120)

    def test_address_drops_the_query(self):
        self.assertEqual(ai_spend_daily.page_address("https://claude.ai/login?returnTo=%2Fsettings%2Fusage&x=1"),
                         "claude.ai/login")
        self.assertEqual(ai_spend_daily.page_address(""), "")

    def test_a_failed_page_reading_prints_what_the_page_showed(self):
        import contextlib
        import io
        from unittest import mock

        def reader():
            ai_spend_daily.SEEN.update(url="https://grok.com/dashboard/billing?team=1",
                                       text=f"Billing\nYou have used all of your weekly usage\nowner{self.AT}example.org\n")
            raise RuntimeError("no 'Cursor Models' or 'Other Models · N% used' line on the Cursor spending page "
                               "(signed out, or the page changed)")
        out = io.StringIO()
        with mock.patch.dict(ai_spend_daily.READERS, {"cursor": reader}), \
                mock.patch.object(ai_spend_daily, "last_record", lambda pool: None), contextlib.redirect_stdout(out):
            rc = ai_spend_daily.main(["--dry-run", "--pools", "cursor"])
        text = out.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("  page address: grok.com/dashboard/billing\n", text)
        self.assertIn("  page shows: You have used all of your weekly usage\n", text)
        self.assertIn("the reader needs a fix", text)
        self.assertNotIn("@", text)
        self.assertNotIn("team=1", text)


class FlowPageBelongsToAPictureRun(unittest.TestCase):
    """The reading and a picture run find the same Flow tab; while a run holds its lock the reading leaves it alone."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lock = Path(self.tmp.name) / "shared" / "writer.lock"

    def hold(self):
        import fcntl
        self.lock.parent.mkdir(parents=True, exist_ok=True)
        handle = self.lock.open("a+")
        self.addCleanup(handle.close)
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return handle

    def test_busy_when_a_run_holds_the_lock(self):
        self.hold()
        with self.assertRaises(ai_spend_daily.Busy):
            with ai_spend_daily.flow_page_free(self.lock):
                self.fail("the Flow page was touched while a run held it")

    def test_free_when_no_run_holds_it_and_released_afterwards(self):
        self.lock.parent.mkdir(parents=True)
        with ai_spend_daily.flow_page_free(self.lock):
            with self.assertRaises(ai_spend_daily.Busy):  # held during the reading, so a run cannot start under it
                with ai_spend_daily.flow_page_free(self.lock):
                    pass
        with ai_spend_daily.flow_page_free(self.lock):
            pass

    def test_a_machine_with_no_picture_runs_reads_as_before(self):
        with ai_spend_daily.flow_page_free(self.lock):
            pass
        self.assertFalse(self.lock.parent.exists())

    def test_read_flow_never_opens_the_page_while_a_run_holds_the_lock(self):
        from unittest import mock
        self.hold()
        with mock.patch.object(ai_spend_daily, "FLOW_LOCK", self.lock), \
                mock.patch.object(ai_spend_daily, "_page_text", side_effect=AssertionError("page opened")):
            with self.assertRaises(ai_spend_daily.Busy):
                ai_spend_daily.read_flow()

    def test_a_busy_flow_page_is_not_a_missing_spending_figure(self):
        import contextlib
        import io
        from unittest import mock

        def busy():
            raise ai_spend_daily.Busy("a picture run holds the Flow page")
        out = io.StringIO()
        good = {"left": 1, "total": 2, "note": "n"}
        with mock.patch.dict(ai_spend_daily.READERS, {"flow": busy, "elevenlabs": lambda: dict(good), "vertex": lambda: dict(good)}), \
                mock.patch.object(ai_spend_daily, "last_record", lambda pool: None), contextlib.redirect_stdout(out):
            rc = ai_spend_daily.main(["--dry-run", "--pools", "elevenlabs,flow,vertex"])
        self.assertEqual(rc, 0)
        self.assertIn("BUSY flow:", out.getvalue())
        self.assertIn("left alone for a picture run: flow", out.getvalue())


class FlowAccountByFingerprint(unittest.TestCase):
    """J2537: the script holds the studio Ultra account's sha256, never its address, and the ledger note names the role."""
    AT = "@"

    def addr(self, name):
        return f"{name}{self.AT}googlemail.com"

    def patched(self, page_text):
        import hashlib
        import tempfile
        from unittest import mock
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        stack = [mock.patch.object(ai_spend_daily, "FLOW_ACCOUNT_SHA256", hashlib.sha256(self.addr("studio.ultra").encode()).hexdigest()),
                 mock.patch.object(ai_spend_daily, "FLOW_LOCK", Path(tmp.name) / "none" / "writer.lock"),
                 mock.patch.object(ai_spend_daily, "_page_text", lambda *a, **k: page_text)]
        for m in stack:
            m.start()
            self.addCleanup(m.stop)

    def test_the_fingerprint_is_a_sha256_and_matches_whatever_the_case(self):
        self.assertRegex(ai_spend_daily.FLOW_ACCOUNT_SHA256, r"^[0-9a-f]{64}$")
        self.patched("")
        self.assertTrue(ai_spend_daily.is_flow_account("  " + self.addr("Studio.Ultra").upper() + " "))
        self.assertFalse(ai_spend_daily.is_flow_account(self.addr("someone.else")))

    def test_the_note_names_the_role_not_the_address(self):
        self.patched(f"Flow\n{self.addr('studio.ultra')}\nULTRA\n12,690 credits\n")
        r = ai_spend_daily.read_flow()
        self.assertEqual(r["left"], 12690)
        self.assertEqual(r["note"], "Flow account picker credits (the studio Ultra account, CDP :9222)")

    def test_another_account_is_refused_without_printing_it(self):
        self.patched(f"Flow\n{self.addr('someone.else')}\n500 credits\n")
        with self.assertRaises(RuntimeError) as cm:
            ai_spend_daily.read_flow()
        self.assertIn("another account", str(cm.exception))
        self.assertNotIn(self.AT, str(cm.exception))

    def test_no_account_shown_still_reads_the_balance(self):
        self.patched("Flow\n3,000 credits\n")
        self.assertEqual(ai_spend_daily.read_flow()["note"], "Flow account picker credits (account not shown, CDP :9222)")


class CodexReadsEveryRunInTheWindow(unittest.TestCase):
    def test_a_reading_older_than_the_newest_five_logs_is_found(self):
        import json
        import os
        import tempfile
        import time
        with tempfile.TemporaryDirectory() as d:
            sess = Path(d) / "sessions" / "2026" / "11" / "11"
            sess.mkdir(parents=True)
            now = time.time()
            stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 3600))
            reading = {"timestamp": stamp, "payload": {"rate_limits": {"secondary": {"used_percent": 12, "resets_at": now + 86400}}}}
            f = sess / "old.jsonl"
            f.write_text(json.dumps(reading) + "\n")
            os.utime(f, (now - 3600, now - 3600))
            for i in range(8):  # eight newer runs that ended without a limit reading
                g = sess / f"new{i}.jsonl"
                g.write_text(json.dumps({"timestamp": stamp, "payload": {"type": "message", "rate_limits": None}}) + "\n")
                os.utime(g, (now - 60 * i, now - 60 * i))
            self.assertEqual(ai_spend_daily.read_codex(Path(d))["left"], 88.0)

    def test_the_error_says_what_the_logs_held(self):
        with self.assertRaises(ValueError) as cm:
            ai_spend_daily.parse_codex(['{"timestamp":"2026-11-11T00:00:00Z","payload":{"rate_limits":null}}', "{}"])
        self.assertIn("lines with rate_limits: 1; none holds a limit window", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
