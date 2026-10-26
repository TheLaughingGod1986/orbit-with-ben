"""plate_check.py pure checks (Audit rules, Orbit Auditor 26 Oct 2026). No ffmpeg needed."""
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plate_check as p  # noqa: E402

N = p.FW * p.FH


def plate(seed: int) -> bytes:
    r = random.Random(seed)
    return bytes(r.randint(40, 230) for _ in range(N))


def noisy(b: bytes, seed: int, amp: int = 3) -> bytes:
    r = random.Random(seed)
    return bytes(max(0, min(255, v + r.randint(-amp, amp))) for v in b)


BLACK = bytes(N)


class Plates(unittest.TestCase):
    def test_each_beat_own_plate_passes(self):
        frames = [plate(i) for i in range(6)]
        times = [i * 30.0 for i in range(6)]
        self.assertEqual(p.repeated_plates(times, frames), [])

    def test_held_shot_is_one_beat(self):
        a = plate(1)
        frames = [noisy(a, i) for i in range(10)]
        times = [float(i) for i in range(10)]
        self.assertEqual(p.repeated_plates(times, frames), [])

    def test_reused_plate_fails(self):
        a = plate(1)
        frames = [a, plate(2), noisy(a, 3), plate(4), noisy(a, 5)]
        times = [0.0, 30.0, 60.0, 90.0, 120.0]
        reps = p.repeated_plates(times, frames)
        self.assertEqual(len(reps), 1)
        self.assertEqual(reps[0]["occurrences"], 3)
        self.assertEqual(reps[0]["at"], [0.0, 60.0, 120.0])

    def test_callback_allowed(self):
        a = plate(1)
        frames = [a, plate(2), noisy(a, 3)]
        times = [0.0, 30.0, 60.0]
        self.assertEqual(p.repeated_plates(times, frames, callbacks=(60.0,)), [])

    def test_black_and_flat_frames_ignored(self):
        flat = bytes([120]) * N
        frames = [BLACK, plate(2), BLACK, flat, plate(3), flat]
        times = [0.0, 30.0, 60.0, 90.0, 120.0, 150.0]
        self.assertEqual(p.repeated_plates(times, frames), [])


class EndHold(unittest.TestCase):
    def test_end_on_opening_plate_fails(self):
        a = plate(1)
        times = [1.0, 2.0, 100.0, 200.0, 290.0, 299.0]
        frames = [a, noisy(a, 1), plate(5), plate(6), noisy(a, 2), BLACK]
        s, to, te = p.end_hold_match(times, frames, 300.0)
        self.assertGreaterEqual(s, p.END_SSIM)
        self.assertEqual(te, 290.0)

    def test_own_end_plate_passes(self):
        a = plate(1)
        times = [1.0, 2.0, 100.0, 290.0, 299.0]
        frames = [a, noisy(a, 1), plate(5), plate(9), BLACK]
        s, _, _ = p.end_hold_match(times, frames, 300.0)
        self.assertLess(s, p.END_SSIM)


class ShortRules(unittest.TestCase):
    def test_duration_band(self):
        self.assertEqual(p.duration_verdict(24.0), [])
        self.assertEqual(p.duration_verdict(22.0), [])
        self.assertEqual(p.duration_verdict(27.0), [])
        self.assertEqual(len(p.duration_verdict(20.5)), 1)
        self.assertEqual(len(p.duration_verdict(28.0)), 1)
        self.assertEqual(p.duration_verdict(20.5, "J0216"), [])

    def test_title_and_id_matching(self):
        ocr = "THE FULL FILM, IS THE SUN GETTING BRIGHTER? h8HGfyShEHl"
        self.assertTrue(p.text_has(ocr, "Is the Sun Getting Brighter?"))
        self.assertTrue(p.text_has(ocr, "h8HGfyShEHI", 0.85))
        self.assertFalse(p.text_has("How Long Do Saturn's Rings Have Left?", "Is the Sun Getting Brighter?"))
        self.assertFalse(p.text_has("Watch the full film", "VBaYRPp85Sw", 0.85))
        self.assertFalse(p.text_has("anything", ""))

    def test_caption_words(self):
        self.assertTrue(p.has_words("THE SUN"))
        self.assertFalse(p.has_words("~ — 4 ."))

    def test_yellow(self):
        yellow = bytes([255, 214, 0]) * 10
        grey = bytes([128, 128, 128]) * 90
        self.assertAlmostEqual(p.yellow_frac(yellow + grey), 0.1)
        self.assertEqual(p.yellow_frac(bytes([255, 255, 255]) * 10), 0.0)


if __name__ == "__main__":
    unittest.main()
