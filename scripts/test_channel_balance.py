#!/usr/bin/env python3
"""Tests for channel_balance.py: python3 scripts/test_channel_balance.py"""
import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channel_balance as cb  # noqa: E402

T = dt.date(2026, 10, 9)


def f(i, air, done):
    return dict(id=i, title="", air=air, complete=done)


class Balance(unittest.TestCase):
    def test_a_channel_with_its_four_done_yields_to_the_other(self):
        owb = [f(str(i), f"2026-11-0{i}", True) for i in range(1, 5)] + [f("9", "2026-12-06", True)] * 4
        hos = [f("a", "2026-11-05", True), f("b", "2026-11-12", False)] + [f("z", "2026-12-03", True)] * 4
        r = cb.priority(owb, hos, T)
        self.assertEqual(r["first"], "hos")
        self.assertIn("History of Science has 1 of 4 complete for 2026-11", r["why"])

    def test_the_earlier_short_month_wins_then_the_bigger_gap(self):
        owb = [f("1", "2026-11-01", False)] + [f(str(i), f"2026-11-1{i}", True) for i in range(3)]
        hos = [f("a", "2026-11-05", False), f("b", "2026-11-12", False)] + [f("c", "2026-11-19", True)] * 2
        self.assertEqual(cb.priority(owb, hos, T)["first"], "hos")  # same month: HOS is 2 short, OWB 1

    def test_a_month_with_too_few_films_planned_is_short(self):
        owb = [f(str(i), f"2026-11-0{i}", True) for i in range(1, 5)] + [f("9", "2026-12-06", True)]
        hos = [f(str(i), f"2026-11-0{i}", True) for i in range(1, 5)] + [f("z", f"2026-12-0{i}", True) for i in range(1, 5)]
        r = cb.priority(owb, hos, T)
        self.assertEqual(r["first"], "owb")
        self.assertEqual(r["channels"]["owb"]["2026-12"]["unplanned"], 3)

    def test_this_months_aired_films_missing_from_the_records_dont_count_as_short(self):
        owb = [f("21", "2026-10-11", True)] + [f(str(i), f"2026-11-0{i}", False) for i in range(1, 5)]
        hos = [f("5", "2026-10-29", True)] + [f(str(i), f"2026-11-0{i}", True) for i in range(1, 5)]
        r = cb.priority(owb, hos, T)
        self.assertEqual(r["channels"]["hos"]["2026-10"]["short"], 0)
        self.assertEqual(r["first"], "owb")

    def test_all_done(self):
        fs = [f(str(i), f"2026-{m}-0{i}", True) for m in ("10", "11", "12") for i in range(1, 5)]
        self.assertIn("Both channels", cb.priority(fs, fs, T)["why"])


if __name__ == "__main__":
    unittest.main()
