"""60% stayed-to-watch ship gate checks in gate_shorts_open.py (Chief, 24 Oct 2026, J0918)."""
from datetime import date
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_shorts_open as g  # noqa: E402


class StayedUnit(unittest.TestCase):
    def test_meta_promise_lint(self):
        for bad in (
            "On Mercury, one day lasts two years. Stay, and I'll show you how.",
            "The wind on Neptune is supersonic. Stay and I’ll show you how fast.",
            "Did you know Venus spins backwards?",
            "Wait for it — the core collapses in a second.",
        ):
            with self.subTest(bad=bad):
                verdict = g.meta_promise_verdict(bad)
                self.assertEqual(len(verdict), 1)
                self.assertIn("meta-promise", verdict[0])

        clean = "One day on Mercury lasts two years. Mercury races round the Sun every 88 Earth days."
        self.assertEqual(g.meta_promise_verdict(clean), [])

    def test_first_cut_verdict(self):
        self.assertEqual(g.first_cut_verdict(2.2, 23.0), [])
        self.assertEqual(g.first_cut_verdict(3.0, 23.0), [])
        self.assertEqual(len(g.first_cut_verdict(5.5, 20.44)), 1)
        self.assertIn("5.50s > 3.0s", g.first_cut_verdict(5.5, 20.44)[0])
        self.assertEqual(len(g.first_cut_verdict(None, 20.44)), 1)

    def test_vo_timing_verdict(self):
        warns, gap = g.vo_timing_verdict(0.06, 22.0, 23.0)
        self.assertEqual(warns, [])
        self.assertEqual(gap, 1.0)

        warns_late, _ = g.vo_timing_verdict(0.28, 22.0, 23.0)
        self.assertEqual(len(warns_late), 1)
        self.assertIn("0.28s > 0.15s", warns_late[0])

        warns_tail, gap_tail = g.vo_timing_verdict(0.05, 17.44, 20.44)
        self.assertEqual(len(warns_tail), 1)
        self.assertEqual(gap_tail, 3.0)
        self.assertIn("3.00s > 1.5s", warns_tail[0])


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg/ffprobe required")
class StayedFfmpegIntegration(unittest.TestCase):
    def test_pushed_still_and_late_cut_fail_unless_report_only(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "still_short.mp4"
            # 4 s static dark-grey clip with a 440 Hz tone from 0.30 s to 2.00 s (onset 0.30 s, tail gap 2.00 s)
            subprocess.run([
                "ffmpeg", "-y", "-v", "error",
                "-f", "lavfi", "-i", "color=c=0x303030:s=72x128:r=30:d=4.0",
                "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=4.0",
                "-af", "volume='if(between(t,0.30,2.00),0.5,0.0)':eval=frame",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(p),
            ], check=True)

            strict = g.check(p, date(2026, 10, 24), 14, {"entries": []}, None,
                             spoken="On Mercury, one day lasts two years. Stay, and I'll show you how.")
            self.assertEqual(strict["verdict"], "FAIL")
            self.assertLess(strict["frame0_diff_0_1_5s"], g.FRAME0_DIFF_FAIL)
            self.assertTrue(any("pushed still at frame 0" in f for f in strict["fails"]))
            self.assertTrue(any("first cut" in f for f in strict["fails"]))
            self.assertTrue(any("meta-promise" in f for f in strict["fails"]))
            self.assertTrue(any("first VO word starts" in w for w in strict["warns"]))
            self.assertTrue(any("gap from last word to end" in w for w in strict["warns"]))

            rep = g.check(p, date(2026, 10, 24), 14, {"entries": []}, None, report_only=True,
                          spoken="On Mercury, one day lasts two years. Stay, and I'll show you how.")
            self.assertEqual(rep["verdict"], "PASS")
            self.assertEqual(rep["fails"], [])
            self.assertEqual(len(rep["stayed_fails"]), 3)
            self.assertTrue(all(f"[report-only] {m}" in rep["warns"] for m in rep["stayed_fails"]))

    def test_moving_open_and_early_cut_pass(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "moving_short.mp4"
            # 0-2.2 s moving testsrc2, hard cut at 2.2 s to bright gray, audio 0.0-3.2 s on 4.0 s total
            subprocess.run([
                "ffmpeg", "-y", "-v", "error",
                "-f", "lavfi", "-i", "testsrc2=s=72x128:r=30:d=2.2",
                "-f", "lavfi", "-i", "color=c=0xd0d0d0:s=72x128:r=30:d=1.8",
                "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=4.0",
                "-filter_complex", "[0:v]format=gray,format=yuv420p[v0];[1:v]format=yuv420p[v1];[v0][v1]concat=n=2:v=1:a=0[v];"
                                   "[2:a]volume='if(lt(t,3.2),0.5,0.0)':eval=frame[a]",
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(p),
            ], check=True)

            res = g.check(p, date(2026, 10, 24), 14, {"entries": []}, None,
                          spoken="The Sun is getting brighter as it burns through its core.")
            self.assertGreaterEqual(res["frame0_diff_0_1_5s"], g.FRAME0_DIFF_FAIL)
            self.assertIsNotNone(res["first_cut_s"])
            self.assertLessEqual(res["first_cut_s"], g.FIRST_CUT_MAX_S)
            self.assertEqual(res["stayed_fails"], [])
            self.assertEqual(res["vo_src"], "mix")

    def test_sibling_sidecars_do_not_bleed_into_clean_short(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            clean_mp4 = folder / "clean_short_v01.mp4"
            sibling_mp4 = folder / "sibling_short_v01.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-v", "error",
                "-f", "lavfi", "-i", "testsrc2=s=72x128:r=30:d=2.2",
                "-f", "lavfi", "-i", "color=c=0xd0d0d0:s=72x128:r=30:d=1.8",
                "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=4.0",
                "-filter_complex", "[0:v]format=gray,format=yuv420p[v0];[1:v]format=yuv420p[v1];[v0][v1]concat=n=2:v=1:a=0[v];"
                                   "[2:a]volume='if(lt(t,3.2),0.5,0.0)':eval=frame[a]",
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(clean_mp4),
            ], check=True)
            shutil.copy(clean_mp4, sibling_mp4)

            # Only the sibling's _vo.txt has the meta-promise; clean_short has its own clean _vo.txt
            (folder / "sibling_short_vo.txt").write_text("On Mercury, a day is two years. Stay, and I'll show you how.\n")
            (folder / "clean_short_vo.txt").write_text("The Sun is getting brighter as it burns through its core.\n")
            # Unscoped words.json or sibling VO stem must also be ignored by clean_short_v01
            (folder / "words.json").write_text('[{"word": "Stay, and I\'ll show you", "start": 0.4, "end": 1.0}]')
            sibling_vo = folder / "sibling_short_vo_v01.wav"
            subprocess.run([
                "ffmpeg", "-y", "-v", "error",
                "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=4.0",
                "-af", "volume='if(between(t,0.40,1.50),0.5,0.0)':eval=frame",
                str(sibling_vo),
            ], check=True)

            clean_res = g.check(clean_mp4, date(2026, 10, 24), 14, {"entries": []}, None)
            self.assertEqual(clean_res["stayed_fails"], [])
            self.assertEqual(clean_res["vo_src"], "mix")
            self.assertFalse(any("meta-promise" in f for f in clean_res["fails"]))

            sib_res = g.check(sibling_mp4, date(2026, 10, 24), 14, {"entries": []}, None)
            self.assertTrue(any("meta-promise" in f for f in sib_res["fails"]))
            self.assertEqual(sib_res["vo_src"], str(sibling_vo))

    def test_vo_s_fallback_used_only_when_onset_is_zero(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "vo_s_test_v01.mp4"
            # Audio starts at 0.30 s and ends at 3.50 s on a 4.00 s file; meta vo_s=2.0 must NOT be used as last_word_end_s
            subprocess.run([
                "ffmpeg", "-y", "-v", "error",
                "-f", "lavfi", "-i", "color=c=0x303030:s=72x128:r=30:d=4.0",
                "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=4.0",
                "-af", "volume='if(between(t,0.30,3.50),0.5,0.0)':eval=frame",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(p),
            ], check=True)
            onset_late, last_late, src_late = g.vo_timing(p, 4.0, {"vo_s": 2.0})
            self.assertGreater(onset_late, 0.15)
            self.assertGreater(last_late, 3.0)
            self.assertEqual(src_late, "mix")

            p0 = Path(td) / "vo_s_zero_v01.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-v", "error",
                "-f", "lavfi", "-i", "color=c=0x303030:s=72x128:r=30:d=4.0",
                "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=4.0",
                "-af", "volume=0.5",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(p0),
            ], check=True)
            onset_zero, last_zero, _ = g.vo_timing(p0, 4.0, {"vo_s": 2.1})
            self.assertEqual(onset_zero, 0.0)
            self.assertEqual(last_zero, 2.1)


if __name__ == "__main__":
    unittest.main()
