"""weekly_public_audit: Orbit-first labelled tests are not frame-0 breaches (Claude #99 6036942792)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import weekly_public_audit as w  # noqa: E402


class OrbitFirstTestAllowlist(unittest.TestCase):
    def test_three_labelled_test_ids(self):
        self.assertEqual(
            w.ORBIT_FIRST_TEST_IDS,
            frozenset({"Ih2zhZTbIR0", "dQlOgsDGmtA", "pL339HhjDwo"}),
        )

    def test_orbit_at_frame_0_is_not_a_breach_for_labelled_tests(self):
        flags = ["Orbit at frame 0", "mostly dark frame 0 (check the subject is visible)"]
        self.assertEqual(
            w.frame0_breach_flags("pL339HhjDwo", flags),
            ["mostly dark frame 0 (check the subject is visible)"],
        )
        self.assertEqual(w.frame0_breach_flags("Ih2zhZTbIR0", ["Orbit at frame 0"]), [])
        self.assertEqual(w.frame0_breach_flags("dQlOgsDGmtA", ["Orbit at frame 0"]), [])

    def test_orbit_at_frame_0_still_breaches_every_other_short(self):
        flags = ["Orbit at frame 0"]
        self.assertEqual(w.frame0_breach_flags("Qn56D6TOi0k", flags), flags)
        self.assertEqual(w.frame0_breach_flags("1NeQFVnzO2Q", flags), flags)

    def test_none_passthrough(self):
        self.assertIsNone(w.frame0_breach_flags("pL339HhjDwo", None))


if __name__ == "__main__":
    unittest.main()
