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

    def test_signed_out_or_changed_page_fails_loudly(self):
        with self.assertRaises(RuntimeError):
            ai_spend_daily.parse_claude(CLAUDE_LOGIN_PAGE)


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


if __name__ == "__main__":
    unittest.main()
