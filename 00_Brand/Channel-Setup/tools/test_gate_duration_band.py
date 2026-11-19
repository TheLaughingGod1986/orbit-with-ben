"""Short duration band in gate_shorts_open.py (Ben, 19 Nov 2026; 16.0–19.0 s inclusive)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_shorts_open as g  # noqa: E402


class DurationBand(unittest.TestCase):
    def test_duration_band_edges(self):
        cases = (
            (15.99, True),
            (16.0, False),
            (19.0, False),
            (19.01, True),
        )
        for dur, expect_warn in cases:
            with self.subTest(dur=dur):
                fails, warns = g.duration_verdict(dur)
                self.assertEqual(fails, [], f"dur={dur}")
                if expect_warn:
                    self.assertEqual(len(warns), 1)
                    self.assertIn("outside 16.0–19.0s band", warns[0])
                else:
                    self.assertEqual(warns, [])


if __name__ == "__main__":
    unittest.main()