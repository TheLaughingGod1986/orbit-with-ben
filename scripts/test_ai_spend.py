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


if __name__ == "__main__":
    unittest.main()
