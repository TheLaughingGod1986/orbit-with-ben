#!/usr/bin/env python3
"""Tests for missed_runs.py (pure logic; no git or network)."""
import datetime as dt, os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import missed_runs as m

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 11, 4, 12, 0, tzinfo=UTC)


def fresh():
    return {"tracker": NOW - dt.timedelta(hours=5), "buffer": NOW - dt.timedelta(hours=5),
            "claude": NOW - dt.timedelta(minutes=20), "mini": NOW - dt.timedelta(minutes=2)}


class Misses(unittest.TestCase):
    def test_all_fresh(self):
        self.assertEqual(m.misses(NOW, fresh()), [])

    def test_buffer_silent_two_days(self):
        s = fresh(); s["buffer"] = NOW - dt.timedelta(hours=50)
        self.assertEqual([x[0] for x in m.misses(NOW, s)], ["buffer"])

    def test_claude_down_three_days(self):
        s = fresh(); s["claude"] = NOW - dt.timedelta(days=3)
        self.assertEqual([x[0] for x in m.misses(NOW, s)], ["claude"])

    def test_claude_one_missed_hour_is_fine(self):
        s = fresh(); s["claude"] = NOW - dt.timedelta(minutes=80)
        self.assertEqual(m.misses(NOW, s), [])

    def test_no_record(self):
        s = fresh(); s["tracker"] = None
        miss = m.misses(NOW, s)
        self.assertEqual(miss[0][0], "tracker")
        self.assertIn("no record", m.line(*miss[0]))

    def test_line_has_marker_and_fix(self):
        l = m.line("buffer", 50.0, 26)
        self.assertTrue(l.startswith("[alarm buffer]"))
        self.assertIn("50.0 h", l)
        self.assertIn("dev.orbit.buffer-check", l)

    def test_dedupe(self):
        self.assertTrue(m.already_posted("buffer", NOW, ["x", "[alarm buffer] buffer missed: ..."]))
        self.assertFalse(m.already_posted("claude", NOW, ["[alarm buffer] buffer missed"]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
