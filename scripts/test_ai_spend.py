#!/usr/bin/env python3
"""Tests for ai_spend.py: the board/credits document the Kanban page reads."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_spend  # noqa: E402


class BuildDoc(unittest.TestCase):
    def rows(self):
        return [
            {"at": "2026-10-10T09:00:00Z", "kind": "record", "pool": "flow", "left": 52, "by": "cursor"},  # before the month
            {"at": "2026-10-12T09:00:00Z", "kind": "record", "pool": "flow", "left": 12500, "total": 12500, "by": "cursor"},
            {"at": "2026-10-13T09:00:00Z", "kind": "spend", "pool": "flow", "amount": 100, "film": "HOS:006", "what": "q", "by": "cursor"},
            {"at": "2026-10-13T09:05:00Z", "kind": "spend", "pool": "vertex", "amount": 1.6, "film": "OWB:025", "what": "omni", "by": "cursor"},
            {"at": "2026-10-13T10:00:00Z", "kind": "record", "pool": "flow", "left": 12400, "by": "cursor"},
            {"at": "2026-10-14T10:00:00Z", "kind": "record", "pool": "claude", "note": "hit the weekly limit", "by": "claude"},
        ]

    def test_month_starts_at_the_refill(self):
        d = ai_spend.build_doc(self.rows())
        flow = d["pools"]["flow"]
        self.assertEqual(flow["first"]["left"], 12500)  # the 10 Oct reading is before the month
        self.assertEqual(flow["latest"]["left"], 12400)
        self.assertEqual(flow["spent_logged"], 100.0)
        self.assertEqual(len(flow["series"]), 2)

    def test_spend_per_film_and_claude_notes(self):
        d = ai_spend.build_doc(self.rows())
        self.assertEqual(d["byFilm"], {"HOS:006": {"flow": 100.0}, "OWB:025": {"vertex": 1.6}})
        self.assertEqual(d["pools"]["claude"]["notes"][0]["note"], "hit the weekly limit")
        self.assertNotIn("elevenlabs", d["pools"])

    def test_monthly_logs_keep_history_without_counting_balance_or_refills_as_spend(self):
        rows = self.rows() + [
            {"at": "2026-09-30T10:00:00Z", "kind": "spend", "pool": "flow", "amount": 70},
            {"at": "2026-10-15T10:00:00Z", "kind": "record", "pool": "flow", "left": 25000},
            {"at": "2026-11-01T10:00:00Z", "kind": "spend", "pool": "flow", "amount": 30},
        ]
        d = ai_spend.build_doc(rows)
        self.assertEqual(d["monthly"]["2026-09"]["flow"]["logged"], 70)
        self.assertEqual(d["monthly"]["2026-10"]["flow"]["logged"], 100)
        self.assertEqual(d["monthly"]["2026-10"]["flow"]["entries"], 1)
        self.assertEqual(d["monthly"]["2026-11"]["flow"]["logged"], 30)
        self.assertEqual(d["monthly"]["2026-10"]["flow"]["latest"]["left"], 25000)

    def test_cli_rejects_bad_film_and_missing_balance(self):
        with self.assertRaises(SystemExit):
            ai_spend.main(["spend", "--pool", "flow", "--amount", "1", "--film", "006", "--by", "t"])
        with self.assertRaises(SystemExit):
            ai_spend.main(["record", "--pool", "flow", "--by", "t"])


class FlowRefill(unittest.TestCase):
    def test_rise_is_refill_total(self):
        import ai_spend_daily
        r = {"left": 25000, "note": "n"}
        self.assertEqual(ai_spend_daily.flow_refill(r, 52)["total"], 25000)
        self.assertNotIn("total", ai_spend_daily.flow_refill(r, None))
        self.assertNotIn("total", ai_spend_daily.flow_refill({"left": 40, "note": "n"}, 52))


SPENDING_PAGE = """Spending
CURRENT PLAN
Ultra
$200/mo
Usage limits reset on 6 Nov (25 days left)
Adjust Plan
Included in Ultra
Cursor Models · Includes Cursor Grok and Composer
14% used
Additional usage beyond limits consumes Other Models quota or on-demand spend.
Other Models
30% used
Additional usage beyond limits consumes on-demand spend.
Grok Bot
Included in Ultra. Learn more
Weekly usage
80% used
Resets 16 Oct (5 days left)
On-Demand Usage
On-demand spending is currently disabled
"""


class CursorSpending(unittest.TestCase):
    def test_percent_layout(self):
        import ai_spend_daily
        r = ai_spend_daily.parse_cursor(SPENDING_PAGE)
        self.assertEqual((r["left"], r["total"]), (86, 100))   # Cursor Models: the pool the Mini's Cursor runs on
        self.assertEqual(r["used"], {"cursor models": 14, "other models": 30, "weekly usage": 80})
        self.assertIn("limits reset 6 Nov", r["note"])
        self.assertIn("weekly resets 16 Oct", r["note"])
        self.assertEqual(ai_spend.POOLS["cursor"], "%")

    def test_billing_expiring_row_is_available(self):
        import ai_spend_daily
        page = ("Free Trial\n Expiring in 30 days\nDanger\n2%\n£4.93\n£225.63 One-time\nFreeTrialUpgrade:x\n"
                "Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY\n Used\nDanger\n0%\n£0.00\n£30.09\n"
                "Free Trial\n Expired\n—\n£225.63\n£225.63 One-time\n")
        trial, note = ai_spend_daily.parse_billing(page)
        self.assertEqual(trial, 4.93)
        self.assertIn("Free Trial: £4.93 Available (expiring in 30 days)", note)
        self.assertIn("Free Trial: £225.63 Expired", note)

    def test_billing_pool_sums_every_available_credit(self):
        # Ben's screenshot, 12 Oct 2026 23:51: the new Developer Program credit plus the trial's tail.
        import ai_spend_daily
        page = ("Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY\n Available\n100%\n£75.39\n£75.39 One-time\n"
                "f8b5-CREDIT_TYPE_MONTHLY-357d\nFollowing services: All of Google Cloud Platform\n12 October 2026\n"
                "Free Trial\n Expiring in 30 days\nDanger\n0%\n£0.67\n£225.63 One-time\nFreeTrialUpgrade:x\n"
                "Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY\n Used\nDanger\n0%\n£0.00\n£30.09\n"
                "Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY\n Expired\n—\n£9.62\n£30.09\n")
        pool, note = ai_spend_daily.parse_billing(page)
        self.assertEqual(pool, 76.06)
        self.assertIn("£9.62 Expired", note)

    def test_changed_page_fails_loudly(self):
        import ai_spend_daily
        with self.assertRaises(RuntimeError):
            ai_spend_daily.parse_cursor("Usage\nTotal tokens 801.1M\nIncluded 801.1M\nOn-demand 0")


if __name__ == "__main__":
    unittest.main()
