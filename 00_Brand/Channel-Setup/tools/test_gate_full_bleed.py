"""Frame-0 full-bleed check in gate_shorts_open.py (10 Nov 2026, J2539, LEARNINGS rule 24)."""
from datetime import date
import math
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_shorts_open as g  # noqa: E402

W, H = g.FB_W, g.FB_H
BAND_H = round(W * 9 / 16)          # a 16:9 picture band across the full width
BAND_Y0 = (H - BAND_H) // 2
BAND_Y1 = BAND_Y0 + BAND_H


def picture(x: int, y: int) -> int:
    """A detailed picture with no flat rows, no straight edges and no mirror line."""
    v = 128 + 50 * math.sin(x / 2.5) + 40 * math.sin(y / 3.5) + 25 * math.sin((x + 2 * y) / 1.7)
    return max(0, min(255, int(v)))


def frame(px) -> bytes:
    return bytes(px(x, y) for y in range(H) for x in range(W))


def banded(fill) -> bytes:
    """The picture in the centred 16:9 band, fill(x, y) above and below it."""
    return frame(lambda x, y: picture(x, y) if BAND_Y0 <= y < BAND_Y1 else fill(x, y))


class FullBleedUnit(unittest.TestCase):
    def test_full_frame_picture_passes(self):
        m = g.full_bleed_frame(frame(picture))
        self.assertIsNone(m["kind"], m)
        self.assertGreater(m["detail_top"], g.FB_DETAIL_FLOOR)
        self.assertGreater(m["detail_bottom"], g.FB_DETAIL_FLOOR)

    def test_black_bars_fail(self):
        m = g.full_bleed_frame(banded(lambda x, y: 0))
        self.assertEqual(m["kind"], "bars", m)
        self.assertAlmostEqual(m["seam_rows"][0], BAND_Y0, delta=2)
        self.assertAlmostEqual(m["seam_rows"][1], BAND_Y1, delta=2)
        self.assertEqual(m["std_top"], 0.0)

    def test_flat_colour_band_fails(self):
        self.assertEqual(g.full_bleed_frame(banded(lambda x, y: 90))["kind"], "bars")

    def test_soft_fill_fails_as_blur_pad(self):
        # a smooth ramp stands in for a heavily blurred copy: it has brightness but almost no row detail
        m = g.full_bleed_frame(banded(lambda x, y: 100 + x // 4))
        self.assertEqual(m["kind"], "blur-pad", m)
        self.assertLess(m["detail_outside"], g.FB_SOFT_RATIO * m["detail_picture"])

    def test_mirrored_fill_fails(self):
        def mirrored(x, y):
            yy = 2 * BAND_Y0 - 1 - y if y < BAND_Y0 else 2 * BAND_Y1 - 1 - y
            return picture(x, min(max(yy, BAND_Y0), BAND_Y1 - 1))
        self.assertEqual(g.full_bleed_frame(banded(mirrored))["kind"], "mirror")

    def test_caption_strip_over_full_frame_picture_passes(self):
        y0, y1 = int(H * 0.10), int(H * 0.26)

        def captioned(x, y):
            if y0 <= y < y1:
                return 255 if (x // 6) % 2 and y0 + 6 <= y < y1 - 6 else 0   # white glyph blocks on a black strip
            return picture(x, y)
        self.assertIsNone(g.full_bleed_frame(frame(captioned))["kind"])

    def test_centred_caption_over_full_frame_picture_passes(self):
        def centred_caption(x, y):
            if BAND_Y0 <= y < BAND_Y1 and (y - BAND_Y0) % 14 < 8 and 14 <= x < W - 14:
                return 255 if (x // 4) % 2 else 0
            return picture(x, y)
        self.assertIsNone(g.full_bleed_frame(frame(centred_caption))["kind"])

    def test_black_bars_with_hook_caption_fail(self):
        def bars_with_caption(x, y):
            if BAND_Y0 <= y < BAND_Y1:
                return picture(x, y)
            if 14 <= y < 34 and 12 <= x < W - 12:
                return 255 if (x // 5) % 2 else 0
            return 0
        m = g.full_bleed_frame(frame(bars_with_caption))
        self.assertEqual(m["kind"], "bars", m)

    def test_blur_pad_with_hook_caption_fails(self):
        def pad_with_caption(x, y):
            if BAND_Y0 <= y < BAND_Y1:
                return picture(x, y)
            if 14 <= y < 34 and 12 <= x < W - 12:
                return 255 if (x // 5) % 2 else 0
            return 100 + x // 4
        m = g.full_bleed_frame(frame(pad_with_caption))
        self.assertEqual(m["kind"], "blur-pad", m)

    def test_subject_on_black_space_passes(self):
        # a planet on black: flat top and bottom, detail in the centre, but no straight full-width seam
        def planet(x, y):
            return picture(x, y) if (x - W / 2) ** 2 + (y - H / 2) ** 2 < 40 ** 2 else 0
        self.assertIsNone(g.full_bleed_frame(frame(planet))["kind"])

    def test_flat_frame_passes(self):
        self.assertIsNone(g.full_bleed_frame(frame(lambda x, y: 48))["kind"])

    def test_verdict(self):
        ok = {"kind": None}
        bars = {"kind": "bars", "t": 0.0, "seam_rows": [66, 126], "std_outside": 0.4, "std_picture": 51.2}
        pad = {"kind": "blur-pad", "t": 0.25, "seam_rows": [66, 126], "detail_outside": 0.6, "detail_picture": 14.0}
        self.assertEqual(g.frame0_full_bleed_verdict([ok, ok, ok]), [])
        # one later frame only (a hard cut through a letterboxed insert) is not the opening
        self.assertEqual(g.frame0_full_bleed_verdict([ok, ok, dict(pad, t=0.5)]), [])
        first = g.frame0_full_bleed_verdict([bars, ok, ok])
        self.assertEqual(len(first), 1)
        self.assertIn("not full-bleed", first[0])
        self.assertIn("0.4 vs picture 51.2", first[0])
        most = g.frame0_full_bleed_verdict([ok, pad, dict(pad, t=0.5)])
        self.assertEqual(len(most), 1)
        self.assertIn("blur-pad", most[0])
        self.assertIn("2/3 frames", most[0])


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg/ffprobe required")
class FullBleedFfmpeg(unittest.TestCase):
    """Made clips, 216x384, 1.5 s each."""
    LUM = "128+50*sin(X/5)+40*sin(Y/7)+25*sin((X+2*Y+40*T)/3.4)"

    def _src(self, w: int, h: int) -> str:
        return f"nullsrc=s={w}x{h}:r=10:d=1.5,geq=lum='{self.LUM}':cb=128:cr=128"

    def _clip(self, td: str, name: str, graph: str, audio: bool = False) -> Path:
        p = Path(td) / f"{name}.mp4"
        cmd = ["ffmpeg", "-y", "-v", "error"]
        if audio:
            cmd += ["-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=1.5"]
        cmd += ["-filter_complex", graph, "-map", "[v]"]
        if audio:
            cmd += ["-map", "0:a", "-c:a", "aac"]
        cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", str(p)]
        subprocess.run(cmd, check=True)
        return p

    def _measure(self, p: Path):
        frames = g.frame0_full_bleed(p)
        self.assertEqual([f["t"] for f in frames], list(g.FB_TIMES))
        return g.frame0_full_bleed_verdict(frames), frames

    def test_full_frame_picture_passes(self):
        with tempfile.TemporaryDirectory() as td:
            fails, frames = self._measure(self._clip(td, "full", f"{self._src(216, 384)}[v]"))
            self.assertEqual(fails, [], frames)
            self.assertTrue(all(f["kind"] is None for f in frames), frames)

    def test_black_bar_letterbox_fails(self):
        with tempfile.TemporaryDirectory() as td:
            fails, frames = self._measure(
                self._clip(td, "letterbox", f"{self._src(216, 122)},pad=216:384:0:(oh-ih)/2:black[v]"))
            self.assertEqual(len(fails), 1, frames)
            self.assertEqual({f["kind"] for f in frames}, {"bars"}, frames)

    def test_blur_pad_fails(self):
        with tempfile.TemporaryDirectory() as td:
            fails, frames = self._measure(self._clip(td, "blur_pad", (
                f"{self._src(216, 122)},format=yuv420p[b];"
                f"{self._src(216, 122)},scale=216:384,gblur=sigma=12,format=yuv420p[bg];"
                "[bg][b]overlay=x=0:y=131:format=yuv420[v]")))
            self.assertEqual(len(fails), 1, frames)
            self.assertEqual({f["kind"] for f in frames}, {"blur-pad"}, frames)
            self.assertIn("row detail outside", fails[0])

    def test_full_frame_picture_with_caption_band_passes(self):
        with tempfile.TemporaryDirectory() as td:
            fails, frames = self._measure(self._clip(td, "caption", (
                f"{self._src(216, 384)},"
                "drawbox=x=0:y=40:w=iw:h=60:color=black:t=fill,"
                "drawbox=x=24:y=56:w=70:h=28:color=white:t=fill,"
                "drawbox=x=122:y=56:w=70:h=28:color=white:t=fill[v]")))
            self.assertEqual(fails, [], frames)

    def test_check_reports_it_as_a_hard_fail_with_numbers(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._clip(td, "letterbox_audio",
                           f"{self._src(216, 122)},pad=216:384:0:(oh-ih)/2:black[v]", audio=True)
            res = g.check(p, date(2026, 11, 10), 14, {"entries": []}, None, report_only=True, spoken="A clean line.")
            self.assertEqual(res["verdict"], "FAIL")
            self.assertTrue(any("not full-bleed" in f for f in res["fails"]), res["fails"])
            self.assertEqual(len(res["frame0_full_bleed"]), len(g.FB_TIMES))
            self.assertEqual(res["frame0_full_bleed"][0]["kind"], "bars")


if __name__ == "__main__":
    unittest.main()
