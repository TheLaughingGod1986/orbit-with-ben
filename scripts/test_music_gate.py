#!/usr/bin/env python3
"""Tests for music_gate.py on synthetic music (needs numpy and ffmpeg; skipped without them): python3 scripts/test_music_gate.py"""
import json
import shutil
import subprocess as sp
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import numpy as np
    import music_gate as mg
except ImportError:  # CI has no numpy
    np = mg = None

SR = 22050
OK = np is not None and shutil.which("ffmpeg") is not None


def piece(seed, secs=90, bpm=None):
    """A slow synth bed: a new note every 4 s with a fifth and an octave, a little noise, optional soft clicks."""
    r = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    y = np.zeros_like(t)
    for i in range(int(secs / 4)):
        f = 110 * 2 ** (r.integers(0, 24) / 12)
        a = slice(int(i * 4 * SR), int((i + 1) * 4 * SR))
        env = np.minimum(1, (t[a] - i * 4) * 4) * np.exp(-(t[a] - i * 4) * 0.3)
        y[a] += env * (np.sin(2 * np.pi * f * t[a]) + 0.5 * np.sin(3 * np.pi * f * t[a]) + 0.3 * np.sin(4.02 * np.pi * f * t[a]))
    y += 0.05 * r.standard_normal(len(t))
    for k in np.arange(0, secs, 60 / bpm) if bpm else []:
        y[int(k * SR):int(k * SR) + 400] += np.hanning(400) * 1.5
    return (y / np.abs(y).max() * 0.5).astype(np.float32)


def save(y, path, br="192k"):
    sp.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-b:a", br, str(path)],
           input=y.tobytes(), check=True)


PROMPT = "Instrumental underscore for the Mars robot film. Pace: 60-80 BPM. NOT Jupiter music."


@unittest.skipUnless(OK, "needs numpy and ffmpeg")
class MusicGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        d = cls.d = Path(cls.tmp.name)
        film = cls.film = d / "025_Mars"
        (film / "05_Music").mkdir(parents=True)
        cls.a = piece(1, bpm=72)
        save(cls.a, film / "05_Music/mars_score_bed_v01.mp3")
        (film / "05_Music/mars_score_bed_v01_plan.json").write_text(json.dumps({"prompt": PROMPT}))
        (d / "other").mkdir()
        save(cls.a[13 * SR:], d / "other/jupiter-music.mp3", "96k")  # the same track, trimmed and re-encoded
        save(piece(2), d / "other/sun_score_bed_v01.mp3")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_a_reused_track_fails_even_trimmed_and_re_encoded(self):
        res = mg.judge(self.film, self.film / "05_Music/mars_score_bed_v01.mp3", others=[self.d / "other/jupiter-music.mp3"])
        self.assertEqual(res["verdict"], "FAIL")
        self.assertTrue(res["fail"][0].startswith("reused: sounds like jupiter-music.mp3"))

    def test_its_own_bed_passes_against_different_music(self):
        res = mg.judge(self.film, self.film / "05_Music/mars_score_bed_v01.mp3", others=[self.d / "other/sun_score_bed_v01.mp3"])
        self.assertEqual(res["verdict"], "PASS", res["fail"])
        self.assertLess(mg.similarity(mg.frames(self.a), mg.frames(piece(2))), 0.5)
        self.assertEqual(res["warn"], [])  # 72 BPM is inside 60-80

    def test_a_shared_file_outside_05_music_and_a_brief_without_pace_fail(self):
        shared = self.d / "other/jupiter-music.mp3"
        res = mg.judge(self.film, shared, others=[])
        self.assertTrue(any(f.startswith("own: the bed is") for f in res["fail"]))
        self.assertTrue(any(f.startswith("own: no plan") for f in res["fail"]))
        bed = self.film / "05_Music/nopace_score_bed_v01.mp3"
        save(piece(3), bed)
        bed.with_name(bed.stem + "_plan.json").write_text(json.dumps({"prompt": "Calm strings."}))
        res = mg.judge(self.film, bed, others=[])
        self.assertTrue(any("Pace" in f for f in res["fail"]) and any("NOT" in f for f in res["fail"]))

    def test_a_hole_in_the_music_fails_but_a_breath_does_not(self):
        y = piece(5, secs=80).copy()
        breath = y.copy(); breath[30 * SR:34 * SR] *= 0.01   # 4 s breath
        hole = y.copy(); hole[30 * SR:42 * SR] *= 0.01       # 12 s near silence
        to8k = lambda a: np.interp(np.arange(0, len(a) / SR, 1 / mg.SR), np.arange(len(a)) / SR, a).astype(np.float32)
        self.assertLessEqual(mg.longest_gap(to8k(breath))[0], mg.GAP_S)
        s, at = mg.longest_gap(to8k(hole))
        self.assertGreater(s, mg.GAP_S)
        self.assertAlmostEqual(at, 31, delta=3)

    def test_an_unreadable_other_track_is_a_warning_not_a_crash(self):
        res = mg.judge(self.film, self.film / "05_Music/mars_score_bed_v01.mp3", others=[self.d / "other/missing.mp3"])
        self.assertEqual(res["verdict"], "PASS")
        self.assertTrue(any("couldn't read missing.mp3" in w for w in res["warn"]))

    def test_a_bed_shorter_than_the_cut_fails(self):
        cut = self.d / "cut.mp4"
        sp.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=64x36:d=100", str(cut)], check=True)
        res = mg.judge(self.film, self.film / "05_Music/mars_score_bed_v01.mp3", video=cut, others=[])
        self.assertTrue(any(f.startswith("length:") for f in res["fail"]))


if __name__ == "__main__":
    unittest.main()
