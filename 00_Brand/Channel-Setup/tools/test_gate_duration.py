"""Duration rule in gate_shorts_open.py, incl. the one-off Short length test (Chief OK, 11 Oct 2026)."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_shorts_open as g  # noqa: E402


class Duration(unittest.TestCase):
    def test_house_band(self):
        self.assertEqual(g.duration_verdict(24.0), ([], []))
        self.assertEqual(len(g.duration_verdict(33.0)[1]), 1)   # warn only
        self.assertEqual(len(g.duration_verdict(40.0)[0]), 1)   # FAIL
        self.assertEqual(len(g.duration_verdict(55.0)[0]), 1)   # a long Short still FAILs without the flag

    def test_length_test(self):
        self.assertEqual(g.duration_verdict(55.0, True), ([], []))
        self.assertEqual(len(g.duration_verdict(45.0, True)[1]), 1)
        self.assertEqual(len(g.duration_verdict(61.0, True)[0]), 1)


if __name__ == "__main__":
    unittest.main()
