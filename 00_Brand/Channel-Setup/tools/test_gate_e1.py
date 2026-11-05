"""HOS-2026-11-E1 anomaly-first gate (Chief h47, 5 Nov 2026). Films 008–010 only."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_shorts_open as g  # noqa: E402


def words(pairs):
    return [{"word": text, "start": start, "end": end} for text, start, end in pairs]


OPEN = words([
    ("This", 0.05, 0.25),
    ("thin", 0.28, 0.50),
    ("line", 0.53, 0.80),
    ("of", 0.84, 1.00),
    ("clay", 1.05, 1.40),
])


class E1Unit(unittest.TestCase):
    def test_open_accepts_a_physical_claim_and_the_j1004_scale_line(self):
        self.assertEqual(g.e1_open_verdict("This thin line of clay marks the end", OPEN), [])
        self.assertEqual(g.e1_open_verdict("Franklin's kite was never hit by lightning.", OPEN), [])
        scale = words([
            ("In", 0.04, 0.16),
            ("one", 0.20, 0.40),
            ("minute", 0.44, 0.80),
            ("the", 0.84, 1.00),
        ])
        self.assertEqual(g.e1_open_verdict("In one minute, the Moon falls about as far", scale), [])

    def test_open_rejects_a_year_dateline_and_a_bare_name(self):
        year = g.e1_open_verdict("In 1854, a killer was hiding in a water pump.", OPEN)
        self.assertTrue(any("In <year>" in f for f in year))
        spelled = g.e1_open_verdict("In seventeen fifty-two he flew it into a storm.", OPEN)
        self.assertTrue(any("In <year>" in f for f in spelled))
        name = g.e1_open_verdict("Benjamin Franklin flew a kite into a storm.", OPEN)
        self.assertTrue(any("biographer" in f for f in name))

    def test_word_4_must_end_by_2s(self):
        late = words([
            ("This", 0.10, 0.40),
            ("thin", 0.50, 0.90),
            ("line", 1.00, 1.50),
            ("of", 1.60, 2.20),
        ])
        self.assertTrue(any("word 4 ends at 2.20s" in f for f in g.e1_open_verdict("This thin line of", late)))
        self.assertTrue(any("need timestamps" in f for f in g.e1_open_verdict("This thin line of clay", [])))

    def test_cuts_and_holds(self):
        self.assertEqual(g.e1_cut_verdict([2.1, 4.2, 7.0], 23.0), [])
        early = g.e1_cut_verdict([1.2, 4.0, 7.0], 23.0)
        self.assertTrue(any("shot1→shot2" in f for f in early))
        late = g.e1_cut_verdict([3.0, 4.4, 7.5], 23.0)
        self.assertTrue(any("shot1→shot2" in f for f in late))
        no_second = g.e1_cut_verdict([2.2], 23.0)
        self.assertTrue(any("shot2→shot3" in f for f in no_second))
        held = g.e1_cut_verdict([2.1, 4.4], 23.0)
        self.assertTrue(any("plate held" in f for f in held))

    def test_pauses_payoff_tail_duration(self):
        self.assertEqual(g.e1_pause_verdict([(1.0, 1.20)], True), [])
        paused = g.e1_pause_verdict([(1.0, 1.40)], True)
        self.assertEqual(len(paused), 1)
        self.assertEqual(g.e1_pause_verdict([(5.1, 5.6)], True), [])
        self.assertTrue(g.e1_pause_verdict([], False))

        self.assertEqual(g.e1_payoff_verdict({"payoff_start_s": 16.1}, 23.0), [])
        self.assertTrue(g.e1_payoff_verdict({"payoff_start_s": 15.0}, 23.0))
        self.assertTrue(g.e1_payoff_verdict({}, 23.0))

        self.assertEqual(g.e1_tail_verdict(1.19), [])
        self.assertTrue(g.e1_tail_verdict(1.2))
        self.assertTrue(g.e1_tail_verdict(None))

        self.assertEqual(g.e1_duration_verdict(23.0), [])
        self.assertEqual(g.e1_duration_verdict(25.1), [])
        self.assertTrue(g.e1_duration_verdict(25.2))
        self.assertTrue(g.e1_duration_verdict(21.5))

    def test_auto_applies_only_on_hos_008_to_010(self):
        hos = Path("/tmp/history-of-science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/a.mp4")
        other = Path("/tmp/history-of-science/02_Video-Projects/007_The-First-Vaccine/10_Shorts/a.mp4")
        saved = g.channel.SLUG
        try:
            g.channel.SLUG = "hos"
            self.assertTrue(g.e1_applies(hos, None))
            self.assertFalse(g.e1_applies(other, None))
            self.assertFalse(g.e1_applies(hos, "off"))
            g.channel.SLUG = "orbit"
            self.assertFalse(g.e1_applies(hos, None))
            self.assertTrue(g.e1_applies(other, "hos-2026-11-e1"))
        finally:
            g.channel.SLUG = saved
        self.assertEqual(g.e1_flag("nope"), "bad")


if __name__ == "__main__":
    unittest.main()
