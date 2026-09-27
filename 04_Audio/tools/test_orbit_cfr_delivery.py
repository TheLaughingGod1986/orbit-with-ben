#!/usr/bin/env python3
"""Tests for YouTube-safe CFR delivery (no VideoToolbox, no VFR)."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from shutil import which

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from orbit_cfr_delivery import (  # noqa: E402
    assess_playback_health,
    choose_delivery_fps,
    encoder_is_videotoolbox,
    is_variable_frame_rate,
    libx264_cfr_video_args,
    remaster_cfr,
    shorts_encode_args,
)


def have_ffmpeg() -> bool:
    return bool(which("ffmpeg") and which("ffprobe"))


class HealthAssessmentTests(unittest.TestCase):
    def test_vfr_when_avg_differs_from_r(self) -> None:
        self.assertTrue(is_variable_frame_rate("30/1", "24/1"))
        self.assertFalse(is_variable_frame_rate("30/1", "30/1"))
        self.assertFalse(is_variable_frame_rate("30000/1001", "30000/1001"))

    def test_missing_rates_count_as_vfr(self) -> None:
        self.assertTrue(is_variable_frame_rate("0/0", "30/1"))
        self.assertTrue(is_variable_frame_rate(None, "30/1"))

    def test_videotoolbox_tag(self) -> None:
        self.assertTrue(encoder_is_videotoolbox({"encoder": "h264_videotoolbox"}))
        self.assertTrue(encoder_is_videotoolbox({"encoder": "VideoToolbox"}))
        self.assertFalse(encoder_is_videotoolbox({"encoder": "Lavc60.31.102 libx264"}))

    def test_shorts_stay_30fps(self) -> None:
        self.assertEqual(choose_delivery_fps("24/1", "24/1", vertical=True), Fraction(30, 1))

    def test_longform_keeps_cinematic_24(self) -> None:
        self.assertEqual(choose_delivery_fps("24/1", "24/1", vertical=False), Fraction(24, 1))

    def test_unhealthy_vfr_json(self) -> None:
        data = {
            "streams": [
                {
                    "codec_type": "video",
                    "codec_name": "h264",
                    "width": 1080,
                    "height": 1920,
                    "r_frame_rate": "30/1",
                    "avg_frame_rate": "24/1",
                    "pix_fmt": "yuv420p",
                    "tags": {"encoder": "h264_videotoolbox"},
                },
                {
                    "codec_type": "audio",
                    "codec_name": "aac",
                    "sample_rate": "48000",
                    "channels": 2,
                    "duration": "12.0",
                },
            ]
        }
        health = assess_playback_health(data)
        self.assertFalse(health["ok"])
        self.assertTrue(health["variable_frame_rate"])
        self.assertTrue(health["videotoolbox"])
        self.assertTrue(any("Variable frame rate" in e for e in health["errors"]))
        self.assertTrue(any("Hardware encoder" in e for e in health["errors"]))

    def test_healthy_cfr_json(self) -> None:
        data = {
            "streams": [
                {
                    "codec_type": "video",
                    "codec_name": "h264",
                    "width": 1920,
                    "height": 1080,
                    "r_frame_rate": "30/1",
                    "avg_frame_rate": "30/1",
                    "pix_fmt": "yuv420p",
                    "tags": {"encoder": "Lavc libx264"},
                    "duration": "10.0",
                },
                {
                    "codec_type": "audio",
                    "codec_name": "aac",
                    "sample_rate": "48000",
                    "channels": 2,
                    "duration": "10.0",
                },
            ]
        }
        health = assess_playback_health(data)
        self.assertTrue(health["ok"])
        self.assertFalse(health["variable_frame_rate"])
        self.assertEqual(health["delivery_fps"], "30")


class EncodeArgsTests(unittest.TestCase):
    def test_never_videotoolbox(self) -> None:
        blob = " ".join(shorts_encode_args())
        self.assertNotIn("videotoolbox", blob)
        self.assertIn("libx264", blob)
        self.assertIn("fps_mode", blob)
        self.assertIn("force-cfr=1", blob)
        self.assertIn("yuv420p", blob)

    def test_libx264_args_include_timescale(self) -> None:
        args = libx264_cfr_video_args(Fraction(30, 1))
        self.assertIn("30000", args)


@unittest.skipUnless(have_ffmpeg(), "ffmpeg/ffprobe required")
class RemasterRoundtripTests(unittest.TestCase):
    def test_vfr_source_becomes_cfr(self) -> None:
        with tempfile.TemporaryDirectory(prefix="orbit-cfr-") as tmp_name:
            tmp = Path(tmp_name)
            src = tmp / "vfr_source.mp4"
            dest = tmp / "cfr_out.mp4"
            # Irregular timestamps: stretch 30fps testsrc onto a 24fps timebase
            # then declare 30fps at mux — classic VFR that social platforms choke on.
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-f",
                    "lavfi",
                    "-i",
                    "testsrc=duration=2:size=320x240:rate=30",
                    "-f",
                    "lavfi",
                    "-i",
                    "sine=frequency=440:duration=2",
                    "-vf",
                    "setpts=N/(24*TB)",
                    "-fps_mode",
                    "vfr",
                    "-c:v",
                    "libx264",
                    "-preset",
                    "ultrafast",
                    "-pix_fmt",
                    "yuv420p",
                    "-c:a",
                    "aac",
                    "-ar",
                    "48000",
                    "-ac",
                    "2",
                    str(src),
                ],
                check=True,
            )
            result = remaster_cfr(src, dest)
            after = result["output"]
            self.assertTrue(after["ok"], after.get("errors"))
            self.assertFalse(after["variable_frame_rate"])
            self.assertEqual(after["r_frame_rate"], after["avg_frame_rate"])
            self.assertFalse(after["videotoolbox"])
            self.assertEqual(after["pix_fmt"], "yuv420p")
            self.assertTrue(result["copied_audio"])
            # Audio duration stays within a frame of the source (no reset / trim)
            src_a = float(result["source"]["audio_duration"] or 0)
            dst_a = float(after["audio_duration"] or 0)
            self.assertGreater(dst_a, 1.5)
            self.assertLess(abs(dst_a - src_a), 0.15)


class OverlayFilterTests(unittest.TestCase):
    def test_final_overlay_forces_cfr_30(self) -> None:
        auto = TOOLS.parents[1] / "00_Brand" / "Channel-Setup" / "tools"
        sys.path.insert(0, str(auto))
        try:
            from onscreen_captions import ffmpeg_overlay_filter, vertical_base_filter
        except ImportError as exc:
            self.skipTest(f"onscreen_captions import failed: {exc}")

        beats = [{"start": 0.0, "end": 2.0, "lines": [("hello", "yellow")]}]
        tail = ffmpeg_overlay_filter(beats, cta_start=8.0)
        self.assertIn("fps=30", tail)
        self.assertTrue(tail.endswith("[v]") or "[v]" in tail)
        base = vertical_base_filter(framed=False)
        self.assertIn("fps=30", base)
        self.assertIn("[base]", base)


if __name__ == "__main__":
    unittest.main()
