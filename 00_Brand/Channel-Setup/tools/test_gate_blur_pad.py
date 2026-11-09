"""Blur-pad / letterbox check in gate_shorts_open.py (Ben, 8 Nov 2026, J2421)."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_shorts_open as g  # noqa: E402

W, H = g.PAD_W, g.PAD_H
PLATE_Y0 = int((H - W * 9 / 16) / 2)
PLATE_Y1 = int(PLATE_Y0 + W * 9 / 16)


def texture(x: int, y: int) -> int:
    return (x * 37 + y * 91 + ((x * y) % 13) * 17) % 256


def frame(band_px) -> bytes:
    """A PAD_W x PAD_H frame: textured plate rows in the centred 16:9 window, band_px(x, y) outside it."""
    out = bytearray(W * H)
    for y in range(H):
        for x in range(W):
            out[y * W + x] = texture(x, y) if PLATE_Y0 <= y < PLATE_Y1 else band_px(x, y)
    return bytes(out)


class BlurPadUnit(unittest.TestCase):
    def test_full_bleed_passes(self):
        self.assertIsNone(g.pad_frame_kind(frame(texture)))

    def test_flat_bars_fail(self):
        self.assertEqual(g.pad_frame_kind(frame(lambda x, y: 0)), "bars")

    def test_soft_band_with_seam_is_blur_pad(self):
        self.assertEqual(g.pad_frame_kind(frame(lambda x, y: 100 + x // 4)), "blur-pad")

    def test_verdict_share(self):
        fails, info = g.blur_pad_verdict([None] * 9 + ["blur-pad"])
        self.assertEqual(fails, [])           # 10% is not more than 10%
        self.assertEqual(info["padded"], 1)
        fails, info = g.blur_pad_verdict([None] * 8 + ["blur-pad", "bars"])
        self.assertEqual(len(fails), 1)
        self.assertIn("full-bleed", fails[0])
        self.assertEqual(info["kinds"], ["bars", "blur-pad"])
        self.assertEqual(g.blur_pad_verdict([])[0], [])


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg/ffprobe required")
class BlurPadFfmpeg(unittest.TestCase):
    SRC = "testsrc2=s=216x122:r=10:d=4"

    def _clip(self, td: str, name: str, graph: str) -> Path:
        p = Path(td) / f"{name}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-filter_complex", graph, "-map", "[v]",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(p)], check=True)
        return p

    def _verdict(self, p: Path):
        return g.blur_pad_verdict([g.pad_frame_kind(f) for f in g.pad_frames(p)])

    def test_synthetic_clips(self):
        with tempfile.TemporaryDirectory() as td:
            pad = self._clip(td, "blur_pad", (
                f"{self.SRC},split[a][b];"
                "[a]scale=-2:384,crop=216:384,boxblur=12[bg];"
                "[bg][b]overlay=(W-w)/2:(H-h)/2[v]"))
            bars = self._clip(td, "letterbox", f"{self.SRC},pad=216:384:0:(oh-ih)/2:black[v]")
            full = self._clip(td, "full_bleed", "testsrc2=s=216x384:r=10:d=4,noise=alls=30:allf=t[v]")

            fails, info = self._verdict(pad)
            self.assertEqual(len(fails), 1, info)
            self.assertIn("blur-pad", info["kinds"])
            fails, info = self._verdict(bars)
            self.assertEqual(len(fails), 1, info)
            self.assertIn("bars", info["kinds"])
            fails, info = self._verdict(full)
            self.assertEqual(fails, [], info)


if __name__ == "__main__":
    unittest.main()
