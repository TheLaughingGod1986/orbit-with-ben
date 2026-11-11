"""Full-bleed check in gate_shorts_open.py (10 Nov 2026, J2539, LEARNINGS rule 24; real frames and the whole
Short, 11 Nov 2026, J2546)."""
import base64
import json
import zlib
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
        self.assertEqual((m["sharp_top"], m["sharp_bottom"]), (0.0, 0.0))      # the fill has no fine detail at all
        self.assertGreater(m["sharp_middle"], 4 * g.FB_MID_MIN)                # and the band between is a picture

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
        bars = {"kind": "bars", "t": 0.0, "seam_rows": [66, 126], "sharp_top": 0.0, "sharp_middle": 0.512,
                "sharp_bottom": 0.004, "why": "one flat shade above and below, with a straight edge at the picture"}
        pad = {"kind": "blur-pad", "t": 0.25, "seam_rows": None, "sharp_top": 0.02, "sharp_middle": 0.4,
               "sharp_bottom": 0.01, "why": "no fine detail above or below, yet a picture's brightness is there"}
        self.assertEqual(g.frame0_full_bleed_verdict([ok, ok, ok]), [])
        # one later frame only (a hard cut through a letterboxed insert) is not the opening
        self.assertEqual(g.frame0_full_bleed_verdict([ok, ok, dict(pad, t=0.5)]), [])
        first = g.frame0_full_bleed_verdict([bars, ok, ok])
        self.assertEqual(len(first), 1)
        self.assertIn("not full-bleed", first[0])
        self.assertIn("above/middle/below 0%/51%/0%", first[0])
        self.assertIn("one flat shade above and below", first[0])
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
            self.assertIn("sharp pixels above/middle/below", fails[0])
            self.assertIn("no fine detail above or below", fails[0])

    def test_full_frame_picture_with_caption_band_passes(self):
        with tempfile.TemporaryDirectory() as td:
            fails, frames = self._measure(self._clip(td, "caption", (
                f"{self._src(216, 384)},"
                "drawbox=x=0:y=40:w=iw:h=60:color=black:t=fill,"
                "drawbox=x=24:y=56:w=70:h=28:color=white:t=fill,"
                "drawbox=x=122:y=56:w=70:h=28:color=white:t=fill[v]")))
            self.assertEqual(fails, [], frames)

    def _long(self, td: str, name: str, padded_from: float, padded_to: float, seconds: int = 12) -> Path:
        """A full-frame clip of `seconds` in which the picture is a 16:9 band over its own blurred copy between
        padded_from and padded_to."""
        full = f"nullsrc=s=216x384:r=10:d={seconds},geq=lum='{self.LUM}':cb=128:cr=128"
        band = f"nullsrc=s=216x122:r=10:d={seconds},geq=lum='{self.LUM}':cb=128:cr=128"
        graph = (f"{full},format=yuv420p[f];{band},format=yuv420p[b];"
                 f"{band},scale=216:384,gblur=sigma=12,format=yuv420p[bg];"
                 "[bg][b]overlay=x=0:y=131:format=yuv420[pad];"
                 f"[f][pad]overlay=enable='between(t,{padded_from},{padded_to})':format=yuv420[v]")
        return self._clip(td, name, graph)

    def test_a_padded_stretch_inside_the_short_fails_the_whole_short(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._long(td, "padded_middle", 4.0, 7.9)
            self.assertEqual(g.frame0_full_bleed_verdict(g.frame0_full_bleed(p)), [])     # the opening is fine
            frames = g.clip_full_bleed(p)
            self.assertEqual([f["t"] for f in frames], [float(t) for t in range(12)])
            self.assertEqual([f["t"] for f in frames if f["kind"]], [4.0, 5.0, 6.0, 7.0], frames)
            fails, warns = g.clip_full_bleed_verdict(frames)
            self.assertEqual(len(fails), 1)
            self.assertIn("4/12 frames", fails[0])
            self.assertIn("4-8s (blur-pad)", fails[0])

    def test_one_padded_second_in_twelve_only_warns(self):
        with tempfile.TemporaryDirectory() as td:
            frames = g.clip_full_bleed(self._long(td, "padded_second", 5.0, 5.9))
            fails, warns = g.clip_full_bleed_verdict(frames)
            self.assertEqual(fails, [])
            self.assertEqual(len(warns), 1, frames)

    def test_check_fails_a_short_padded_in_the_middle_and_lists_the_stretch(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._long(td, "padded_middle_check", 4.0, 7.9)
            res = g.check(p, date(2026, 11, 10), 14, {"entries": []}, None, report_only=True, spoken="A clean line.")
            self.assertEqual(res["verdict"], "FAIL")
            self.assertTrue(any("sampled once a second" in f for f in res["fails"]), res["fails"])
            self.assertFalse(any("frame 0 is not full-bleed" in f for f in res["fails"]), res["fails"])
            self.assertEqual(res["padded_stretches_s"], [[4.0, 8.0, "blur-pad"]])
            self.assertIsNone(res["end_card_window_s"])

    def test_check_judges_a_padded_end_card_apart_when_the_meta_names_it(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._long(td, "padded_end_card", 9.0, 12.0)
            bare = g.check(p, date(2026, 11, 10), 14, {"entries": []}, None, report_only=True, spoken="A clean line.")
            self.assertTrue(any("sampled once a second" in f for f in bare["fails"]), bare["fails"])
            meta = Path(td) / "padded_end_card_meta.json"
            meta.write_text(json.dumps({"end_card": {"start_s": 9.0, "len_s": 3.0}}))
            res = g.check(p, date(2026, 11, 10), 14, {"entries": []}, None, report_only=True, spoken="A clean line.")
            self.assertFalse(any("sampled once a second" in f for f in res["fails"]), res["fails"])
            self.assertTrue(any("end card (9.0-12.0s)" in w for w in res["warns"]), res["warns"])
            self.assertEqual(res["end_card_window_s"], [9.0, 12.0])

    def test_a_cut_ok_d_before_the_rule_is_warned_not_failed_and_a_re_cut_is_not_covered(self):
        import hashlib
        from unittest import mock
        with tempfile.TemporaryDirectory() as td:
            p = self._long(td, "okd_before", 4.0, 7.9)
            other = self._long(td, "re_cut", 4.0, 8.9)
            listed = Path(td) / "okd.json"
            listed.write_text(json.dumps({"cuts": [
                {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "file": p.name, "ok": "Ben, 10 Nov 2026"},
                {"sha256": hashlib.sha256(other.read_bytes()).hexdigest(), "file": other.name},     # no OK named
            ]}))
            self.assertEqual(g.okd_before_rule(p, listed)["file"], p.name)
            self.assertIsNone(g.okd_before_rule(other, listed))                  # an entry with no OK covers nothing
            self.assertIsNone(g.okd_before_rule(p, Path(td) / "missing.json"))
            with mock.patch.object(g, "FB_OKD_BEFORE_RULE", listed):
                res = g.check(p, date(2026, 11, 10), 14, {"entries": []}, None, report_only=True, spoken="A clean line.")
                again = g.check(other, date(2026, 11, 10), 14, {"entries": []}, None, report_only=True, spoken="A clean line.")
            self.assertFalse(any("sampled once a second" in f for f in res["fails"]), res["fails"])
            warned = [w for w in res["warns"] if "sampled once a second" in w]
            self.assertEqual(len(warned), 1, res["warns"])
            self.assertIn("OK'd before the rule (Ben, 10 Nov 2026)", warned[0])
            self.assertIn("4-8s (blur-pad)", warned[0])                          # still measured and said
            self.assertTrue(any("sampled once a second" in f for f in again["fails"]), again["fails"])

    def test_the_list_of_cuts_ok_d_before_the_rule_is_short_and_exact(self):
        doc = json.loads(g.FB_OKD_BEFORE_RULE.read_text())
        self.assertLessEqual(len(doc["cuts"]), 3)                # a way out for a fallback, not a way round the rule
        for cut in doc["cuts"]:
            with self.subTest(cut=cut.get("file")):
                self.assertRegex(cut["sha256"], r"^[0-9a-f]{64}$")
                for key in ("file", "ok", "airs", "why"):
                    self.assertTrue(str(cut.get(key) or "").strip(), key)
                self.assertIn("Ben", cut["ok"])

    def test_check_reports_it_as_a_hard_fail_with_numbers(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._clip(td, "letterbox_audio",
                           f"{self._src(216, 122)},pad=216:384:0:(oh-ih)/2:black[v]", audio=True)
            res = g.check(p, date(2026, 11, 10), 14, {"entries": []}, None, report_only=True, spoken="A clean line.")
            self.assertEqual(res["verdict"], "FAIL")
            self.assertTrue(any("not full-bleed" in f for f in res["fails"]), res["fails"])
            self.assertEqual(len(res["frame0_full_bleed"]), len(g.FB_TIMES))
            self.assertEqual(res["frame0_full_bleed"][0]["kind"], "bars")


class WholeShortUnit(unittest.TestCase):
    """The whole Short, one frame a second (J2546). Made result rows; no media."""
    OK = {"kind": None}
    PAD = {"kind": "blur-pad"}

    def clip(self, kinds: str) -> list[dict]:
        return [dict(self.PAD if k == "p" else self.OK, t=float(i)) for i, k in enumerate(kinds)]

    def test_more_than_a_tenth_padded_fails_and_names_the_stretches(self):
        frames = self.clip("....ppp......pp.....")           # 5 of 20: 4-7 s and 13-15 s
        fails, warns = g.clip_full_bleed_verdict(frames)
        self.assertEqual(len(fails), 1)
        self.assertIn("5/20 frames", fails[0])
        self.assertIn("4-7s (blur-pad), 13-15s (blur-pad)", fails[0])
        self.assertEqual(warns, [])
        self.assertEqual(g.padded_stretches(frames), [(4.0, 7.0, "blur-pad"), (13.0, 15.0, "blur-pad")])

    def test_a_tenth_or_less_only_warns(self):
        fails, warns = g.clip_full_bleed_verdict(self.clip("....pp.............."))    # 2 of 20 is the limit, not over it
        self.assertEqual(fails, [])
        self.assertEqual(len(warns), 1)
        self.assertIn("2/20 sampled frames", warns[0])
        self.assertEqual(g.clip_full_bleed_verdict(self.clip("....ppp.............."))[0][0][:40],
                         "the picture does not fill 9:16 on 3/21 f")

    def test_a_clean_short_says_nothing(self):
        self.assertEqual(g.clip_full_bleed_verdict(self.clip("." * 22)), ([], []))
        self.assertEqual(g.clip_full_bleed_verdict([]), ([], []))

    def test_a_padded_end_card_named_by_the_meta_is_judged_apart(self):
        frames = self.clip("................pppp")           # the last four seconds
        fails, _ = g.clip_full_bleed_verdict(frames)
        self.assertEqual(len(fails), 1)                       # with no meta, nothing is left out
        fails, warns = g.clip_full_bleed_verdict(frames, (16.0, 20.0))
        self.assertEqual(fails, [])
        self.assertEqual(len(warns), 1)
        self.assertIn("end card (16.0-20.0s)", warns[0])
        self.assertIn("judged apart", warns[0])

    def test_the_end_card_does_not_hide_padded_shots(self):
        frames = self.clip("..ppp...........pppp")
        fails, warns = g.clip_full_bleed_verdict(frames, (16.0, 20.0))
        self.assertEqual(len(fails), 1)
        self.assertIn("3/16 frames", fails[0])               # the body only: the card's seconds are not counted
        self.assertIn("end card 16.0-20.0s left out", fails[0])
        self.assertNotIn("16-20s", fails[0])
        self.assertEqual(len(warns), 1)

    def test_only_the_meta_names_the_end_card(self):
        self.assertIsNone(g.end_card_window(None, 24.0))
        self.assertIsNone(g.end_card_window({}, 24.0))
        self.assertIsNone(g.end_card_window({"end_card": None}, 24.0))
        self.assertIsNone(g.end_card_window({"end_card": {"font_px": 56, "rows": []}}, 24.0))   # no time in it
        self.assertEqual(g.end_card_window({"end_card": {"start_s": 20.13, "len_s": 3.5}}, 24.0), (20.13, 23.63))
        self.assertEqual(g.end_card_window({"end_card": {"start_s": 19.0}}, 24.0), (19.0, 24.0))
        self.assertEqual(g.end_card_window({"end_card_window_s": [24.82, 26.82]}, 26.82), (24.82, 26.82))
        self.assertEqual(g.end_card_window({"end_card": {"start_s": 22.0, "len_s": 9.0}}, 24.0), (22.0, 24.0))
        self.assertIsNone(g.end_card_window({"end_card": {"start_s": 30.0}}, 24.0))             # past the end
        self.assertIsNone(g.end_card_window({"end_card": {"start_s": True}}, 24.0))


class LabelledRealFrames(unittest.TestCase):
    """The 56 frames an agent labelled by eye from the scheduled Shorts (J2545): 28 padded, 28 full. They sit in
    the JSON as 108x192 grey, so no media is in the repo. No full frame may be failed. Four padded frames are
    still missed; each is named here with why, and each of their Shorts is caught through its other frames."""
    PATH = Path(__file__).resolve().parents[3] / "jobs/reviews/J2545/J2545_labelled_frames.json"
    MISSED = {
        ("rvug71d7Dqk", 0.0): "a light, feathered blur under a large hook caption: a third of the upper fill still reads as sharp",
        ("rvug71d7Dqk", 2.0): "the same shot two seconds on",
        ("C8lPx5N2DwM", 6.0): "a dark-blue graphic on a dark orange backdrop: one shade in grey at this size, and no edge to find",
        ("k2kEaA7ICjc", 10.0): "the same kind: a dark graphic on a dark backdrop of another colour",
    }
    # Chief ruling 4 on J2545: seven frames the first-pass check wrongly failed. Each must pass.
    ONCE_WRONGLY_FAILED = [("xdurJQcoiGM", 14.0), ("MScK2CK2ZFg", 16.0), ("QEoYKIVvKBA", 6.0), ("f17XCtUmN-g", 22.0),
                           ("Wvjd8g0CpzE", 22.0), ("xzKoHg0E0_U", 6.0), ("bSjWiCbB7pY", 22.0)]

    @classmethod
    def setUpClass(cls):
        doc = json.loads(cls.PATH.read_text())
        assert (doc["width"], doc["height"], doc["pix_fmt"]) == (W, H, "gray")
        cls.frames = []
        for f in doc["frames"]:
            grey = zlib.decompress(base64.b64decode(f["gray_108x192_zlib_b64"]))
            assert len(grey) == W * H
            cls.frames.append((f["id"], f["t"], f["label"], g.full_bleed_frame(grey)))

    def test_the_set_is_what_the_audit_said(self):
        self.assertEqual(len(self.frames), 56)
        self.assertEqual(sum(1 for f in self.frames if f[2] == "padded"), 28)
        self.assertEqual(sum(1 for f in self.frames if f[2] == "full"), 28)

    def test_no_full_frame_is_failed(self):
        for vid, t, label, m in self.frames:
            if label == "full":
                with self.subTest(frame=f"{vid} at {t}s"):
                    self.assertIsNone(m["kind"], m)

    def test_the_seven_once_wrongly_failed_pass(self):
        got = {(vid, t): m["kind"] for vid, t, label, m in self.frames if label == "full"}
        for key in self.ONCE_WRONGLY_FAILED:
            with self.subTest(frame=key):
                self.assertIn(key, got)
                self.assertIsNone(got[key])

    def test_every_padded_frame_is_caught_but_the_four_named(self):
        for vid, t, label, m in self.frames:
            if label == "padded" and (vid, t) not in self.MISSED:
                with self.subTest(frame=f"{vid} at {t}s"):
                    self.assertIsNotNone(m["kind"], m)

    def test_the_four_named_are_still_missed(self):
        # If one of these starts to be caught, take it off the list: the list must stay true.
        for vid, t, label, m in self.frames:
            if (vid, t) in self.MISSED:
                with self.subTest(frame=f"{vid} at {t}s"):
                    self.assertEqual(label, "padded")
                    self.assertIsNone(m["kind"], self.MISSED[(vid, t)])

    def test_the_count(self):
        right = sum(1 for _, _, label, m in self.frames if (m["kind"] is not None) == (label == "padded"))
        self.assertEqual(right, 52)                         # 28 of 28 full, 24 of 28 padded

    def test_every_short_with_a_missed_frame_is_caught_by_another(self):
        caught = {vid for vid, _, label, m in self.frames if label == "padded" and m["kind"]}
        for vid, _ in self.MISSED:
            self.assertIn(vid, caught)

    def test_the_margins_the_thresholds_were_set_on(self):
        padded = [max(m["sharp_top"], m["sharp_bottom"]) for vid, t, label, m in self.frames
                  if label == "padded" and (vid, t) not in self.MISSED and m["kind"] != "mirror"]
        # A full frame with a picture in the middle; the two without one (an eclipse, a globe) pass on that.
        full = [max(m["sharp_top"], m["sharp_bottom"]) for _, _, label, m in self.frames
                if label == "full" and m["sharp_top"] is not None and m["sharp_middle"] >= g.FB_MID_MIN]
        self.assertLessEqual(max(padded), 0.07)
        self.assertGreaterEqual(min(full), 0.10)
        self.assertLess(max(padded), g.FB_OUT_MAX)
        self.assertGreater(min(full), g.FB_OUT_MAX)


if __name__ == "__main__":
    unittest.main()
