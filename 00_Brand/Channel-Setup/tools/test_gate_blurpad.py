"""Blur-pad / letterbox check in gate_shorts_open.py (Ben, 8 Nov 2026, 031 Short 2 v02; J2421)."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_shorts_open as g  # noqa: E402

SRC = "testsrc2=size=1920x1080:rate=25:duration=6"
SRC_TALL = "testsrc2=size=1080x1920:rate=25:duration=6"
BLURPAD = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
           "boxblur=20:5[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
GBLURPAD = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "gblur=sigma=30[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
BARS = "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black"
# Full-bleed with a soft top/bottom (depth of field) that is NOT a copy of the centre.
DOF = ("[0:v]split[a][b];[a]boxblur=20:5,hue=h=120[soft];[b]crop=1080:640:0:640[mid];"
       "[soft][mid]overlay=0:640")


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not installed")
class BlurPadClips(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="blurpad_"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def make(self, name: str, src: str, vf: str | None = None, complex_: bool = False) -> Path:
        out = self.tmp / f"{name}.mp4"
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", src]
        if vf:
            cmd += ["-filter_complex" if complex_ else "-vf", vf]
        cmd += ["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(out)]
        subprocess.run(cmd, check=True, capture_output=True)
        return out

    def test_boxblur_pad_fails(self):
        scan = g.pad_scan(self.make("boxblur", SRC, BLURPAD, True))
        self.assertGreaterEqual(scan["blur"], scan["samples"] - 1, scan)
        self.assertEqual(len(g.pad_verdict(scan)), 1)
        self.assertIn("full-bleed", g.pad_verdict(scan)[0])

    def test_gblur_pad_fails(self):
        scan = g.pad_scan(self.make("gblur", SRC, GBLURPAD, True))
        self.assertEqual(len(g.pad_verdict(scan)), 1, scan)

    def test_letterbox_bars_fail(self):
        scan = g.pad_scan(self.make("bars", SRC, BARS))
        self.assertGreaterEqual(scan["bars"], scan["samples"] - 1, scan)
        self.assertEqual(len(g.pad_verdict(scan)), 1)

    def test_full_bleed_passes(self):
        scan = g.pad_scan(self.make("full", SRC_TALL))
        self.assertEqual(scan["padded"], 0, scan)
        self.assertEqual(g.pad_verdict(scan), [])

    def test_full_bleed_reframed_landscape_passes(self):
        scan = g.pad_scan(self.make("crop", SRC, "scale=-2:1920,crop=1080:1920"))
        self.assertEqual(g.pad_verdict(scan), [], scan)

    def test_full_bleed_soft_edges_passes(self):
        scan = g.pad_scan(self.make("dof", SRC_TALL, DOF, True))
        self.assertEqual(g.pad_verdict(scan), [], scan)


class PadVerdictUnit(unittest.TestCase):
    def test_threshold(self):
        self.assertEqual(g.pad_verdict({"samples": 20, "padded": 2, "blur": 2, "bars": 0, "share": 0.10, "at_s": [1, 2]}), [])
        self.assertEqual(len(g.pad_verdict({"samples": 20, "padded": 3, "blur": 3, "bars": 0, "share": 0.15,
                                            "at_s": [1, 2, 3]})), 1)
        self.assertEqual(g.pad_verdict({"samples": 0, "padded": 0, "blur": 0, "bars": 0, "share": 0.0, "at_s": []}), [])


if __name__ == "__main__":
    unittest.main()
