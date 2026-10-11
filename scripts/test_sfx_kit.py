#!/usr/bin/env python3
"""Tests for sfx_kit.py (stdlib; the ffmpeg round trip is skipped without ffmpeg): python3 scripts/test_sfx_kit.py"""
import json, shutil, subprocess as sp, sys, tempfile, unittest, wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sfx_kit as sk

FFMPEG = shutil.which("ffmpeg") is not None


def series(*parts):
    """[(value, seconds), ...] -> momentary loudness every 100 ms."""
    out = []
    for v, secs in parts:
        out += [v] * round(secs / sk.STEP)
    return out


class Make(unittest.TestCase):
    def test_kits_are_ours_deterministic_and_at_peak(self):
        with tempfile.TemporaryDirectory() as d:
            for house, names in (("owb", {"rumble_low", "whoosh_soft", "tick_ui"}),
                                 ("hos", {"rumble_low", "whoosh_soft", "tick_ink"})):
                a = sk.make(Path(d) / house / "a", house, seed=3)
                b = sk.make(Path(d) / house / "b", house, seed=3)
                self.assertEqual([f["sha256"] for f in a["files"]], [f["sha256"] for f in b["files"]])
                self.assertEqual({f["file"].split("_", 2)[2].rsplit("_v01", 1)[0] for f in a["files"]}, names)
                self.assertIn("own synthesis", a["source"])
                self.assertEqual(a["spend"], "none")
                man = json.loads((Path(d) / house / "a" / "sfx_kit_manifest.json").read_text())
                self.assertEqual(len(man["files"]), 3)
                for f in a["files"]:
                    with wave.open(str(Path(d) / house / "a" / f["file"])) as w:
                        self.assertEqual((w.getframerate(), w.getnchannels()), (48000, 2))
                        raw = w.readframes(w.getnframes())
                    peak = max(abs(int.from_bytes(raw[i:i + 2], "little", signed=True)) for i in range(0, len(raw), 2))
                    self.assertAlmostEqual(peak / 32767, 10 ** (-12 / 20), delta=0.01)


class Parse(unittest.TestCase):
    def test_reads_momentary_and_summary(self):
        err = ("[Parsed_ebur128_0 @ 0x1] t: 0.1  TARGET:-23 LUFS  M: -70.0 S:-120.7  I: -70.0 LUFS  LRA: 0.0 LU\n"
               "[Parsed_ebur128_0 @ 0x1] t: 0.2  TARGET:-23 LUFS  M: -18.5 S: -19.0  I: -18.7 LUFS  LRA: 0.4 LU\n"
               "[Parsed_ebur128_0 @ 0x1] Summary:\n\n  Integrated loudness:\n    I:         -16.9 LUFS\n")
        m, i = sk.parse_ebur128(err)
        self.assertEqual(m, [-70.0, -18.5])
        self.assertEqual(i, -16.9)


class Judge(unittest.TestCase):
    VO = series((-16, 3), (-70, 1), (-16, 3))          # talk, pause, talk; integrated -16

    def test_quiet_hits_pass(self):
        sfx = series((-70, 1), (-32, 0.6), (-70, 1.9), (-26, 0.8), (-70, 2.7))
        r = sk.judge(self.VO, -16, sfx, -30)
        self.assertEqual(r["verdict"], "PASS", r["fails"])
        self.assertEqual(r["hits"], 2)

    def test_no_sfx_fails_present(self):
        r = sk.judge(self.VO, -16, series((-70, 7)), -70)
        self.assertTrue(any(f.startswith("present") for f in r["fails"]))

    def test_hit_on_top_of_speech_fails(self):
        sfx = series((-70, 1), (-22, 0.5), (-70, 5.5))
        r = sk.judge(self.VO, -16, sfx, -29)
        self.assertTrue(any(f.startswith("speech") and "0:01.0" in f for f in r["fails"]), r["fails"])

    def test_short_blip_under_run_length_is_ignored(self):
        sfx = series((-70, 1), (-22, 0.2), (-70, 1.8), (-32, 0.5), (-70, 3.5))
        r = sk.judge(self.VO, -16, sfx, -29)
        self.assertFalse([f for f in r["fails"] if f.startswith("speech")], r["fails"])

    def test_pause_swell_to_speech_level_fails(self):
        sfx = series((-70, 3), (-19, 1), (-70, 3))
        r = sk.judge(self.VO, -16, sfx, -29)
        self.assertTrue(any(f.startswith("gaps") for f in r["fails"]), r["fails"])

    def test_loud_sfx_stem_fails_under(self):
        sfx = series((-70, 3), (-25, 1), (-70, 3))
        r = sk.judge(self.VO, -16, sfx, -25)
        self.assertTrue(any(f.startswith("under") for f in r["fails"]), r["fails"])

    def test_bed_rule(self):
        sfx = series((-70, 3), (-30, 0.5), (-70, 3.5))
        bed = series((-24, 7))
        r = sk.judge(self.VO, -16, sfx, -30, bed_m=bed)
        self.assertTrue(any(f.startswith("bed") for f in r["fails"]), r["fails"])
        r = sk.judge(self.VO, -16, sfx, -30, bed_m=series((-28, 7)))
        self.assertEqual(r["verdict"], "PASS", r["fails"])

    def test_sparse_hits_warn_on_a_long(self):
        sfx = series((-70, 3), (-30, 0.5), (-70, 3.5))
        r = sk.judge(self.VO, -16, sfx, -30, minutes=8)
        self.assertEqual(r["verdict"], "PASS")
        self.assertTrue(r["warns"])


@unittest.skipUnless(FFMPEG, "needs ffmpeg")
class RoundTrip(unittest.TestCase):
    def test_level_on_real_files(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            kit = sk.make(d / "kit", "owb")
            vo = d / "vo.wav"
            sp.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                    "anoisesrc=color=pink:duration=12:sample_rate=48000:amplitude=0.5", "-af",
                    "lowpass=3000,volume='if(lt(mod(t,4),3),1,0)':eval=frame", "-ac", "2", str(vo)], check=True)
            whoosh = d / "kit" / kit["files"][1]["file"]
            for gain, want in (("-24dB", 0), ("+6dB", 1)):
                sfx = d / f"sfx{want}.wav"
                sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(whoosh), "-af",
                        f"adelay=1000|1000,volume={gain},apad=whole_dur=12", "-ac", "2", str(sfx)], check=True)
                self.assertEqual(sk.main(["level", "--vo", str(vo), "--sfx", str(sfx)]), want)


if __name__ == "__main__":
    unittest.main()
