"""Background-match check in gate_shorts_open.py (6 Oct 2026, dQlOgsDGmtA vs Ih2zhZTbIR0 on one Jupiter plate)."""
import random, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_shorts_open as g  # noqa: E402

W, H = g.THUMB_W, g.THUMB_H


def plate(seed: int, smooth: int = 3) -> bytearray:
    """A textured background: random blobs, lightly smoothed, like a planet or nebula plate."""
    rnd = random.Random(seed)
    px = [[rnd.randint(0, 255) for _ in range(W)] for _ in range(H)]
    for _ in range(smooth):
        px = [[(px[y][x] + px[y][max(x - 1, 0)] + px[max(y - 1, 0)][x]) // 3 for x in range(W)] for y in range(H)]
    return bytearray(v for row in px for v in row)


def overlay(img: bytearray, x0: int, y0: int, w: int, h: int, value: int) -> bytearray:
    out = bytearray(img)
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            out[y * W + x] = value
    return out


def space(seed: int) -> bytearray:
    rnd = random.Random(seed)
    img = bytearray(rnd.randint(0, 6) for _ in range(W * H))
    img[rnd.randrange(W * H)] = 255   # a star
    return img


class BackgroundMatch(unittest.TestCase):
    def test_same_plate_under_different_overlays_matches(self):
        bg = plate(1)
        orbit = overlay(bg, 8, 14, 11, 16, 200)       # Orbit, centred
        caption = overlay(bg, 2, 36, 23, 5, 255)       # a caption bar low down
        self.assertGreaterEqual(g.background_match(orbit, caption), g.BG_FAIL)
        self.assertGreaterEqual(g.background_match(bg, orbit), g.BG_FAIL)

    def test_different_plates_do_not_match(self):
        self.assertLess(g.background_match(plate(1), plate(2)), g.BG_WARN)
        self.assertLess(g.background_match(overlay(plate(3), 8, 14, 11, 16, 200), plate(4)), g.BG_WARN)

    def test_two_black_space_opens_give_no_verdict(self):
        self.assertEqual(g.background_match(space(1), space(2)), 0.0)

    def test_hex_round_trip_and_bad_sizes(self):
        bg = plate(5)
        self.assertEqual(g.background_match(bytes(bg).hex(), bytes(bg).hex()), 1.0)
        self.assertEqual(g.background_match(b"\x00" * 10, bytes(bg)), 0.0)


if __name__ == "__main__":
    unittest.main()
