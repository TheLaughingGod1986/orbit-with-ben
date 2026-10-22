#!/usr/bin/env python3
"""028 A Star Is Coming Toward Us (Gliese 710) — Part Roughs v01 assembler (J0855).

Applies Chief's J0850 KEEP/FIX rulings and J0855 brief:
- KEEP r08_orbit_binoculars (Omni, a7793cfc): canonical Orbit, no planet, clear binocular sweep.
- KEEP r11_night_road (Flow Quality, 6dfb64f6): no plate/logo/text; 94.36-101.20 s covered by the planned star cutaway.
- KEEP r23_orbit_ice (Omni, 8c509d86): canonical Orbit among Oort ice lumps, no planet.
- KEEP r17_pitch v02 retake (Flow Fast, c2a0aa340d3a): empty grass pitch at dusk gliding low and slow over centre circle towards halfway, no goals or nets in frame.
- Assembles the 7 chapter part roughs (part00_rough_v01 .. part06_rough_v01) from PLATE_BOARDS_v02.json on the locked VO (02_Voiceover/star_coming_vo_v01.wav, last word 469.34s + 2.5s hold + 1.0s fade = 472.84s).
- House edit rules:
  * No back-to-back code graphics anywhere (including r19_subscribe on real moving star-trails footage + house SUBSCRIBE pill, and mid-beat real cutaways breaking the two >20s code graphics r20_21_oort_shell and r24_25_shower).
  * Visual/camera/label change every 3-4 s (internal reframing at VO sentence pauses on multi-sentence code beats, plus all 22 J0504 teaching overlay pills and 6 chapter lower-third cards).
  * First chapter card at 0:30 or later (0:42.50 on Chapter 1, per J0842 ruling; no chapter card in 0:00-0:30).
  * Corner credits on all harvest/code plates, hidden whenever any teaching pill, chapter card, or internal code label is active (strict one-label-at-a-time).
  * Runs picture_qa.py + polish_gate.py per part and writes per-part contact sheets + QA reports.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None

HERE = Path(__file__).resolve().parent
EP = HERE.parent
ROOT = EP.parents[1]
HDIR = HERE / "nasa_pool_v01" / "028_harvest_v01"
CDIR = HERE / "code_graphics_v02"
GDIR_OMNI = EP / "04_Generated-Clips" / "01_Raw" / "omni_v01"
GDIR_VEO = EP / "04_Generated-Clips" / "01_Raw" / "veo_v01"
OV_PACK = HERE / "teaching_overlays_v01_pack"
PACK = HERE / "part_roughs_v01_pack"
WORK = Path("/private/tmp/gliese028_part_roughs_work_v01")
OUT_DIR = Path("/private/tmp/028_part_roughs_v01")

VO_WAV = EP / "02_Voiceover" / "star_coming_vo_v01.wav"
STT_JSON = EP / "02_Voiceover" / "stt" / "star_coming_vo_v01" / "stt_raw.json"
BOARDS_JSON = HERE / "PLATE_BOARDS_v02.json"
POOL_JSON = HERE / "SOURCE_POOL_v02.json"
POOL_OV_JSON = OV_PACK / "pool_v01.json"
POOL_CG_JSON = CDIR / "pool_v02.json"

FPS = 30
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
NAVY = (23, 36, 55, 220)
ENC = ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p"]

STT_DATA = json.loads(STT_JSON.read_text())
WORDS = [w for w in STT_DATA.get("words", []) if w.get("type") == "word"]
OV_DATA = json.loads((OV_PACK / "overlays_v01.json").read_text())["labels"]

# Map any split plate_id for overlays back to the canonical plate_id in overlays_v01.json
OV_ROW_ALIAS = {
    "r20_oort_shell_a": "r20_21_oort_shell",
    "r21_oort_shell_b": "r20_21_oort_shell",
    "r24_shower_a": "r24_25_shower",
    "r25_shower_b": "r24_25_shower",
}

# Gold label strings to suppress on code graphics when replaced by a teaching pill or chapter card
SUPPRESS_BY_PLATE = {
    "r04_shower_shell": {"1.3 million years"},
    "r07_kdwarf": {"60% Sun’s mass"},
    "r14_hipparcos_card": {"Late 1990s", "Hipparcos", "About 1 light-year"},
    "r17_scale_a": {"Sun–Earth: 1 cm"},
    "r18_shell": {"100 metres"},
    "r20_21_oort_shell": {"Beyond the planets", "Cloud of ice"},
    "r33_traffic": {"Outer Oort Cloud", "Too small and faint"},
}

# 6 chapter lower-third cards (Chapters 1..6; none inside 0:00-0:30 per J0842 ruling)
CHAPTER_CARDS = {
    "r06_milky_way": (42.50, 44.90, "The Star Heading Our Way"),
    "r13_star_trails": (131.00, 133.50, "How Close Will It Come?"),
    "r20_oort_shell_a": (210.34, 212.84, "Into the Oort Cloud"),
    "r26_hale_bopp": (281.60, 284.10, "The Comet Shower"),
    "r29_night": (335.84, 338.34, "A New Brightest Star"),
    "r32_wise_sky": (378.30, 380.80, "It Has Happened Before"),
}

# Subscribe lower-right pill on r19_subscribe (204.21-209.89s)
SUBSCRIBE_CARD = ("r19_subscribe", 206.80, 209.44)

FULL_CREDITS = {
    "gaia_motion_1_6my.mp4": "ESA/Gaia/DPAC · CC BY-SA 3.0 IGO",
    "gaia_gliese_encounter.mov": "ESA/Gaia/DPAC · CC BY-SA 3.0 IGO",
    "gaia_edr3_sky.png": "ESA/Gaia/DPAC · CC BY-SA 3.0 IGO",
    "ngc3603.jpg": "NASA, ESA, Hubble",
    "eso_mw_lasilla.mp4": "ESO/S. Brunier · CC BY 4.0",
    "sdo_hmi_continuum.jpg": "NASA/SDO",
    "proxima.jpg": "ESA/Hubble & NASA · CC BY 4.0",
    "eso_startrails.mp4": "R. Wesson/ESO · CC BY 4.0",
    "gaia_craft.jpg": "Artist's impression · ESA/ATG medialab; bg: ESO/S. Brunier · CC BY 4.0",
    "iss_sunrise.jpg": "NASA",
    "neptune.jpg": "NASA/JPL · green and orange filters",
    "neowise_dc.tif": "NASA/Bill Ingalls",
    "comet_a3.jpg": "NASA/Matthew Dominick",
    "jupiter_juno.tif": "NASA/JPL-Caltech/SwRI/MSSS · colour-enhanced",
    "saturn.jpg": "NASA/JPL/Space Science Institute",
    "eso_chajnantor.m4v": "ESO · CC BY 4.0",
    "conjunction.tif": "NASA/Bill Ingalls",
    "moon_lro.jpg": "NASA/LRO",
    "wise_sky.jpg": "NASA/JPL-Caltech/UCLA",
    "wise_craft.jpg": "Artist's concept · NASA/JPL-Caltech",
    "eso_lasilla_ntt.mp4": "ESO/B. Tafreshi (twanight.org) · CC BY 4.0",
    "orbit_binoculars_omni_v01.mp4": None,
    "orbit_ice_omni_v01.mp4": None,
    "night_road_veo_v01.mp4": None,
    "football_pitch_veo_v01.mp4": None,
}

# Video grading LUTs so dark night-sky/starfield clips pass polish_gate (mean >= 28, p95 >= 50, std >= 18)
VIDEO_VF = {
    "gaia_motion_1_6my.mp4": "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
    "gaia_gliese_encounter.mov": (
        "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=rgb24,"
        "lutrgb=r='clip(pow(val/255,0.42)*220+26,0,255)':g='clip(pow(val/255,0.42)*225+28,0,255)':b='clip(pow(val/255,0.40)*240+34,0,255)',"
        "unsharp=5:5:0.9:5:5:0.0"
    ),
    "eso_mw_lasilla.mp4": (
        "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=rgb24,"
        "lutrgb=r='clip(pow(max(0,val-16)/180,0.82)*225+16,0,255)':g='clip(pow(max(0,val-16)/180,0.82)*225+16,0,255)':b='clip(pow(max(0,val-16)/180,0.82)*235+20,0,255)'"
    ),
    "eso_startrails.mp4": "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
    "eso_chajnantor.m4v": (
        "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=rgb24,"
        "lutrgb=r='clip((val-35)*1.8+20,0,255)':g='clip((val-35)*1.8+20,0,255)':b='clip((val-35)*1.8+20,0,255)',"
        "unsharp=5:5:0.8:5:5:0.0"
    ),
    "eso_lasilla_ntt.mp4": "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
    "orbit_binoculars_omni_v01.mp4": (
        "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=rgb24,"
        "lutrgb=r='clip(pow(val/255,0.74)*230+14,0,255)':g='clip(pow(val/255,0.74)*230+14,0,255)':b='clip(pow(val/255,0.74)*235+16,0,255)'"
    ),
    "orbit_ice_omni_v01.mp4": "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
    "night_road_veo_v01.mp4": "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
    "football_pitch_veo_v01.mp4": "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
}

# All plates grouped into the 7 chapter parts (part00 .. part06), with word-safe cut boundaries (in_s, out_s)
# Each entry: (plate_id, row_num, in_s, out_s, kind, src_name, opts)
PARTS = [
    (
        "part00",
        "0 Open",
        0.00,
        42.32,
        [
            ("r01_stars_streaming", 1, 0.00, 6.12, "video", "gaia_motion_1_6my.mp4", {"offset": 3.80, "vcrop": (2880, 1620, 480, 270), "upscale": 1.33}),
            ("r02_gaia_span_2", 2, 6.12, 13.66, "video", "gaia_motion_1_6my.mp4", {"offset": 9.92, "vcrop": (2688, 1512, 576, 324), "upscale": 1.43}),
            ("r03_serpens_sky", 3, 13.66, 17.61, "still", "gaia_edr3_sky.png", {"box": (0.06, 0.06, 0.94, 0.94), "pct": 0.05, "gamma": 0.90, "lift": 0.0}),
            ("r04_shower_shell", 4, 17.61, 30.72, "code", "code_graphic_028_r04_shower_shell_v02.mp4", {"plate_id": "r04_shower_shell", "offset": 0.0, "upscale": 1.0, "reframe_at": [(6.63, (0.06, 0.06, 0.94, 0.94))]}),
            ("r05_cluster_break", 5, 30.72, 36.28, "still", "ngc3603.jpg", {"box": (0.05, 0.14, 0.95, 0.72), "pct": 0.05, "gamma": 0.92, "lift": 0.0}),
            ("r05_drift_path_sky", 5, 36.28, 42.32, "code", "code_graphic_028_r05_drift_path_sky_v02.mp4", {"plate_id": "r05_drift_path_sky", "offset": 0.0, "upscale": 1.0}),
        ],
    ),
    (
        "part01",
        "1 The Star Heading Our Way",
        42.32,
        126.47,
        [
            ("r06_milky_way", 6, 42.32, 50.57, "video", "eso_mw_lasilla.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r07_sun", 7, 50.57, 54.25, "still", "sdo_hmi_continuum.jpg", {"box": (0.04, 0.10, 0.96, 0.62), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r07_kdwarf", 7, 54.25, 58.09, "code", "code_graphic_028_r07_kdwarf_v02.mp4", {"plate_id": "r07_kdwarf", "offset": 0.0, "upscale": 1.0}),
            ("r08_orbit_binoculars", 8, 58.09, 67.80, "video", "orbit_binoculars_omni_v01.mp4", {"offset": 0.20, "upscale": 1.50}),
            ("r09_drift", 9, 67.80, 82.46, "code", "code_graphic_028_r09_drift_v02.mp4", {"plate_id": "r09_drift", "offset": 0.0, "upscale": 1.0, "reframe_at": [(4.34, (0.06, 0.06, 0.94, 0.94)), (10.57, (0.12, 0.12, 0.88, 0.88))]}),
            ("r10_gliese_approach", 10, 82.46, 94.36, "video", "gaia_gliese_encounter.mov", {"offset": 14.0, "vcrop": (1600, 900, 160, 90), "upscale": 1.20}),
            ("r11a_star_cutaway", 11, 94.36, 101.20, "video", "eso_lasilla_ntt.mp4", {"offset": 11.5, "upscale": 1.0}),
            ("r11_night_road", 11, 101.20, 109.20, "video", "night_road_veo_v01.mp4", {"offset": 0.0, "upscale": 1.50}),
            ("r12_proxima", 12, 109.20, 117.24, "still", "proxima.jpg", {"box": (0.0, 0.04, 1.0, 0.96), "pct": 0.05, "feathered_blur": True, "gamma": 0.65, "lift": 16.0}),
            ("r12_stars_move", 12, 117.24, 126.47, "video", "gaia_motion_1_6my.mp4", {"offset": 18.0, "vcrop": (2880, 1620, 480, 270), "upscale": 1.33}),
        ],
    ),
    (
        "part02",
        "2 How Close Will It Come?",
        126.47,
        209.89,
        [
            ("r13_star_trails", 13, 126.47, 134.21, "video", "eso_startrails.mp4", {"offset": 2.0, "upscale": 1.0}),
            ("r14_hipparcos_card", 14, 134.21, 147.37, "code", "code_graphic_028_r14_hipparcos_card_v02.mp4", {"plate_id": "r14_hipparcos_card", "offset": 0.0, "upscale": 1.0, "reframe_at": [(6.52, (0.06, 0.06, 0.94, 0.94))]}),
            ("r15_gaia_craft", 15, 147.37, 155.96, "still", "gaia_craft.jpg", {"box": (0.04, 0.08, 0.96, 0.90), "pct": 0.05, "gamma": 0.95, "lift": 0.0}),
            ("r15_16_path", 15, 155.96, 169.62, "code", "code_graphic_028_r15_16_path_v02.mp4", {"plate_id": "r15_16_path", "offset": 1.96, "upscale": 1.0, "reframe_at": [(5.59, (0.06, 0.06, 0.94, 0.94))]}),
            ("r16_sunrise_break", 16, 169.62, 175.15, "still", "iss_sunrise.jpg", {"box": (0.02, 0.16, 0.74, 0.64), "pct": 0.05, "gamma": 0.68, "lift": 8.0}),
            ("r17_scale_a", 17, 175.15, 181.81, "code", "code_graphic_028_r17_scale_a_v02.mp4", {"plate_id": "r17_scale_a", "offset": 0.0, "upscale": 1.0}),
            ("r17_neptune", 17, 181.81, 186.51, "still", "neptune.jpg", {"box": (0.04, 0.22, 0.96, 0.74), "pct": 0.05, "gamma": 0.85, "lift": 6.0}),
            ("r17_scale_b", 17, 186.51, 191.11, "code", "code_graphic_028_r17_scale_b_v02.mp4", {"plate_id": "r17_scale_b", "offset": 0.0, "upscale": 1.0}),
            ("r17_pitch", 17, 191.11, 195.25, "video", "football_pitch_veo_v01.mp4", {"offset": 1.50, "upscale": 1.50}),
            ("r18_shell", 18, 195.25, 204.21, "code", "code_graphic_028_r18_shell_v02.mp4", {"plate_id": "r18_shell", "offset": 0.0, "upscale": 1.0}),
            ("r19_subscribe", 19, 204.21, 209.89, "video", "eso_startrails.mp4", {"offset": 18.0, "upscale": 1.0}),
        ],
    ),
    (
        "part03",
        "3 Into the Oort Cloud",
        209.89,
        281.16,
        [
            ("r20_oort_shell_a", 20, 209.89, 219.71, "code", "code_graphic_028_r20_21_oort_shell_v02.mp4", {"plate_id": "r20_21_oort_shell", "offset": 0.0, "upscale": 1.0, "reframe_at": [(4.93, (0.05, 0.05, 0.95, 0.95))]}),
            ("r20_oort_cut", 20, 219.71, 224.19, "video", "eso_lasilla_ntt.mp4", {"offset": 14.0, "upscale": 1.0}),
            ("r21_oort_shell_b", 21, 224.19, 233.50, "code", "code_graphic_028_r20_21_oort_shell_v02.mp4", {"plate_id": "r20_21_oort_shell", "offset": 13.19, "upscale": 1.0, "reframe_at": [(6.26, (0.06, 0.06, 0.94, 0.94))]}),
            ("r22_neowise", 22, 233.50, 241.46, "still", "neowise_dc.tif", {"box": (0.04, 0.14, 0.96, 0.82), "pct": 0.05, "gamma": 0.88, "lift": 4.0}),
            ("r23_orbit_ice", 23, 241.46, 250.51, "video", "orbit_ice_omni_v01.mp4", {"offset": 0.40, "upscale": 1.50}),
            ("r24_sunrise", 24, 250.51, 256.79, "still", "iss_sunrise.jpg", {"box": (0.05, 0.12, 0.95, 0.72), "pct": 0.05, "gamma": 0.72, "lift": 6.0}),
            ("r24_shower_a", 24, 256.79, 264.43, "code", "code_graphic_028_r24_25_shower_v02.mp4", {"plate_id": "r24_25_shower", "offset": 0.0, "upscale": 1.0}),
            ("r25_shower_cut", 25, 264.43, 270.90, "video", "gaia_gliese_encounter.mov", {"offset": 27.5, "vcrop": (1600, 900, 160, 90), "upscale": 1.20}),
            ("r25_shower_b", 25, 270.90, 281.16, "code", "code_graphic_028_r24_25_shower_v02.mp4", {"plate_id": "r24_25_shower", "offset": 13.32, "upscale": 1.0, "reframe_at": [(5.92, (0.06, 0.06, 0.94, 0.94))]}),
        ],
    ),
    (
        "part04",
        "4 The Comet Shower",
        281.16,
        335.42,
        [
            ("r26_hale_bopp", 26, 281.16, 287.48, "still", "comet_a3.jpg", {"box": (0.05, 0.04, 0.85, 0.49), "pct": 0.05, "gamma": 0.55, "lift": 12.0}),
            ("r26_a3", 26, 287.48, 294.00, "still", "comet_a3.jpg", {"box": (0.18, 0.08, 0.78, 0.42), "pct": 0.05, "gamma": 0.55, "lift": 12.0}),
            ("r27_shower", 27, 294.00, 305.02, "code", "code_graphic_028_r27_shower_v02.mp4", {"plate_id": "r27_shower", "offset": 0.0, "upscale": 1.0, "reframe_at": [(6.45, (0.06, 0.06, 0.94, 0.94))]}),
            ("r27_leaving", 27, 305.02, 316.04, "video", "gaia_motion_1_6my.mp4", {"offset": 16.0, "vcrop": (2880, 1620, 480, 270), "upscale": 1.33}),
            ("r28_jupiter", 28, 316.04, 322.90, "still", "jupiter_juno.tif", {"box": (0.08, 0.06, 0.92, 0.94), "pct": 0.05, "gamma": 0.92, "lift": 0.0}),
            ("r28_saturn", 28, 322.90, 328.78, "still", "saturn.jpg", {"box": (0.06, 0.16, 0.94, 0.78), "pct": 0.05, "gamma": 0.80, "lift": 10.0}),
            ("r28_hale_bopp_2", 28, 328.78, 335.42, "code", "code_graphic_028_r28_hale_bopp_2_v02.mp4", {"plate_id": "r28_hale_bopp_2", "offset": 0.0, "upscale": 1.0}),
        ],
    ),
    (
        "part05",
        "5 A New Brightest Star",
        335.42,
        377.80,
        [
            ("r29_night", 29, 335.42, 342.13, "video", "eso_chajnantor.m4v", {"offset": 4.50, "upscale": 1.50}),
            ("r29_sky", 29, 342.13, 347.86, "code", "code_graphic_028_r29_sky_v02.mp4", {"plate_id": "r29_sky", "offset": 0.0, "upscale": 1.0}),
            ("r29_twilight", 29, 347.86, 354.91, "still", "conjunction.tif", {"box": (0.05, 0.10, 0.95, 0.70), "pct": 0.05, "gamma": 0.82, "lift": 4.0}),
            ("r30_moon", 30, 354.91, 359.15, "still", "moon_lro.jpg", {"box": (0.02, 0.14, 0.98, 0.80), "pct": 0.05, "gamma": 0.95, "lift": 0.0}),
            ("r30_sun_limb", 30, 359.15, 364.01, "still", "sdo_hmi_continuum.jpg", {"box": (0.18, 0.06, 0.88, 0.48), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r31_sky", 31, 364.01, 369.47, "code", "code_graphic_028_r31_sky_v02.mp4", {"plate_id": "r31_sky", "offset": 0.0, "upscale": 1.0}),
            ("r31_moon_2", 31, 369.47, 373.28, "still", "moon_lro.jpg", {"box": (0.14, 0.22, 0.86, 0.70), "pct": 0.05, "gamma": 0.95, "lift": 0.0}),
            ("r31_sky_fade", 31, 373.28, 377.80, "code", "code_graphic_028_r31_sky_fade_v02.mp4", {"plate_id": "r31_sky_fade", "offset": 0.0, "upscale": 1.0}),
        ],
    ),
    (
        "part06",
        "6 It Has Happened Before",
        377.80,
        472.84,
        [
            ("r32_wise_sky", 32, 377.80, 387.25, "still", "wise_sky.jpg", {"box": (0.06, 0.12, 0.94, 0.88), "pct": 0.05, "gamma": 0.68, "lift": 14.0}),
            ("r33_wise_craft", 33, 387.25, 393.81, "still", "wise_craft.jpg", {"box": (0.04, 0.08, 0.96, 0.92), "pct": 0.05, "gamma": 0.95, "lift": 0.0}),
            ("r33_traffic", 33, 393.81, 402.91, "code", "code_graphic_028_r33_traffic_v02.mp4", {"plate_id": "r33_traffic", "offset": 0.0, "upscale": 1.0}),
            ("r34_sky_wide", 34, 402.91, 411.55, "still", "gaia_edr3_sky.png", {"box": (0.03, 0.05, 0.97, 0.95), "pct": 0.05, "gamma": 0.90, "lift": 0.0}),
            ("r34_traffic", 34, 411.55, 423.37, "code", "code_graphic_028_r34_traffic_v02.mp4", {"plate_id": "r34_traffic", "offset": 0.0, "upscale": 1.0, "reframe_at": [(3.81, (0.06, 0.06, 0.94, 0.94))]}),
            ("r35_lasilla_ntt", 35, 423.37, 435.82, "video", "eso_lasilla_ntt.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r36_night_2", 36, 435.82, 445.31, "video", "eso_mw_lasilla.mp4", {"offset": 8.0, "upscale": 1.0}),
            ("r37_cluster", 37, 445.31, 453.50, "still", "ngc3603.jpg", {"box": (0.14, 0.22, 0.86, 0.68), "pct": 0.05, "gamma": 0.92, "lift": 0.0}),
            ("r37_shell", 37, 453.50, 457.47, "code", "code_graphic_028_r37_shell_v02.mp4", {"plate_id": "r37_shell", "offset": 0.0, "upscale": 1.0}),
            ("r38_neowise_2", 38, 457.47, 463.62, "still", "neowise_dc.tif", {"box": (0.14, 0.22, 0.86, 0.72), "pct": 0.05, "gamma": 0.88, "lift": 4.0}),
            ("r38_return", 38, 463.62, 472.84, "video", "gaia_motion_1_6my.mp4", {"offset": 18.50, "vcrop": (2880, 1620, 480, 270), "upscale": 1.33, "fade_out": 1.0}),
        ],
    ),
]

REVIEWED_OK = {
    "gaia_motion_1_6my.mp4@9.92": {
        "note": (
            "J0321 / PLATE_BOARDS_v02 ruling: r01_stars_streaming (offset 3.80s, 1.20x crop) and r02_gaia_span_2 "
            "(offset 9.92s, 1.43x crop) are continuous back-to-back spans of the 4K Gaia stellar-motion film in the open."
        ),
        "kinds": ["reuse"],
    },
    "neptune.jpg": {
        "note": "Voyager 2 full-disk Neptune (PIA01492, smooth gas giant atmosphere); Chief J0321 approved.",
        "kinds": ["low detail"],
    },
}


def resolve_source(kind: str, sname: str) -> Path:
    if kind == "code":
        return CDIR / sname
    if sname.endswith("_omni_v01.mp4"):
        return GDIR_OMNI / sname
    if sname.endswith("_veo_v01.mp4"):
        return GDIR_VEO / sname
    return HDIR / sname


def compute_upscale(kind: str, src: Path, opts: dict) -> float:
    if kind in ("video", "code"):
        return float(opts.get("upscale", 1.0))
    im = Image.open(src)
    w, h = im.size
    b = opts["box"]
    cw = w * (b[2] - b[0])
    ch = h * (b[3] - b[1])
    pct = opts.get("pct", 0.05)
    if opts.get("feathered_blur"):
        return round((1080.0 / ch) * (1.0 + pct), 3)
    return round(max(1920.0 / cw, 1080.0 / ch) * (1.0 + pct), 3)


def overlays_for_plate(pid: str, fin: float, fout: float) -> list[dict]:
    lookup = OV_ROW_ALIAS.get(pid, pid)
    return [
        o
        for o in OV_DATA
        if o["row"] == lookup and fin - 0.15 <= o["film_start"] < fout
    ]


def check_plan() -> list[str]:
    problems = []
    total_plates = 0
    prev_global_kind = None
    for part_id, ch_name, p_in, p_out, rows in PARTS:
        print(f"=== {part_id} · {ch_name} ({p_in:.2f}-{p_out:.2f}s, {p_out - p_in:.2f}s) ===")
        prev_out = p_in
        for pid, rnum, fin, fout, kind, sname, opts in rows:
            total_plates += 1
            src = resolve_source(kind, sname)
            if not src.exists():
                problems.append(f"{pid}: missing {src}")
                continue
            if abs(fin - prev_out) > 1e-3:
                problems.append(f"{pid}: gap/overlap {prev_out:.2f} -> {fin:.2f}")
            prev_out = fout
            if kind == "code" and prev_global_kind == "code":
                problems.append(f"{pid}: back-to-back code graphic after previous code plate")
            prev_global_kind = kind
            up = compute_upscale(kind, src, opts)
            if up > 2.35:
                problems.append(f"{pid}: upscale {up:.2f} > 2.35")
            for bound_name, bt in (("in", fin), ("out", fout)):
                if bt <= 0.01 or bt >= 469.34:
                    continue
                clipped = [w["text"] for w in WORDS if w["start"] < bt - 0.015 and w["end"] > bt + 0.015]
                if clipped:
                    problems.append(f"{pid} {bound_name}={bt:.2f}s clips word {clipped}")
            ovs = overlays_for_plate(pid, fin, fout)
            print(
                f"  {pid:22s} row={rnum:2d} {fin:6.2f}-{fout:6.2f} ({fout-fin:5.2f}s) {kind:6s} {sname:42s} up={up:4.2f}x ovs={len(ovs)}"
            )
        if abs(prev_out - p_out) > 1e-3:
            problems.append(f"{part_id}: ends at {prev_out:.2f} != {p_out:.2f}")
    # Also verify all 22 overlays are matched to exactly one plate
    matched_ovs = sum(len(overlays_for_plate(pid, fin, fout)) for _, _, _, _, rows in PARTS for pid, _, fin, fout, *_ in rows)
    if matched_ovs != len(OV_DATA):
        problems.append(f"matched {matched_ovs} overlays != {len(OV_DATA)} total in overlays_v01.json")
    print(f"Total plates: {total_plates} | Matched overlays: {matched_ovs}/{len(OV_DATA)} | Problems: {problems or 'NONE'}")
    return problems


def make_credit_png(text: str, dst: Path) -> None:
    font = ImageFont.truetype(FONT, 26)
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    box = dr.textbbox((0, 0), text, font=font)
    y = 1080 - (box[3] - box[1]) - 22
    x = 36
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        dr.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 175))
    dr.text((x, y), text, font=font, fill=(255, 255, 255, 235))
    img.save(dst)


def make_chapter_card_png(title: str, dst: Path) -> None:
    size = 152
    font = ImageFont.truetype(FONT, size)
    lines = [title]
    if font.getlength(title) > 1700:
        ws = title.split()
        best = min(range(1, len(ws)), key=lambda i: max(font.getlength(" ".join(ws[:i])), font.getlength(" ".join(ws[i:]))))
        lines = [" ".join(ws[:best]), " ".join(ws[best:])]
    while max(font.getlength(l) for l in lines) > 1700:
        size -= 4
        font = ImageFont.truetype(FONT, size)
    lh = int(size * 1.05)
    y0 = 1080 - 90 - lh * len(lines)
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    sh = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    for j, l in enumerate(lines):
        ImageDraw.Draw(sh).text((100, y0 + j * lh + 6), l, font=font, fill=(0, 0, 0, 210))
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    img = Image.alpha_composite(sh, img)
    d = ImageDraw.Draw(img)
    for j, l in enumerate(lines):
        d.text((94, y0 + j * lh), l, font=font, fill="white")
    img.save(dst)


def make_subscribe_png(dst: Path) -> None:
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f2 = ImageFont.truetype(FONT, 44)
    d.rounded_rectangle((1440, 900, 1830, 990), radius=45, fill=(204, 0, 0, 235))
    d.text((1500, 918), "SUBSCRIBE", font=f2, fill="white")
    img.save(dst)


def render_still_push(src: Path, opts: dict, dur: float, dest: Path) -> None:
    frames = round(dur * FPS)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    b = opts["box"]
    im = im.crop((int(w * b[0]), int(h * b[1]), int(w * b[2]), int(h * b[3])))
    gamma = float(opts.get("gamma", 1.0))
    lift = float(opts.get("lift", 0.0))
    if opts.get("feathered_blur"):
        bg = im.resize((2112, 1188), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(radius=38))
        fg_h = 1188
        fg_w = round(im.width * (fg_h / im.height))
        fg = im.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
        mask = Image.new("L", (fg_w, fg_h), 255)
        m_arr = np.asarray(mask, dtype=np.float32)
        feather = 120
        ramp = np.linspace(0.0, 1.0, feather, dtype=np.float32)
        m_arr[:, :feather] = ramp[None, :] * 255.0
        m_arr[:, -feather:] = ramp[::-1][None, :] * 255.0
        mask = Image.fromarray(m_arr.astype(np.uint8))
        bg.paste(fg, ((2112 - fg_w) // 2, 0), mask)
        arr = np.asarray(bg, dtype=np.float32) / 255.0
        arr = np.clip((arr ** gamma) * 255.0 + lift, 0.0, 255.0).astype(np.uint8)
        im = Image.fromarray(arr)
    else:
        if gamma != 1.0 or lift != 0.0:
            arr = np.asarray(im, dtype=np.float32) / 255.0
            arr = np.clip((arr ** gamma) * 255.0 + lift, 0.0, 255.0).astype(np.uint8)
            im = Image.fromarray(arr)
        im = ImageEnhance.Color(im).enhance(1.06)
        im = ImageEnhance.Contrast(im).enhance(1.04)
        scale = max(2112.0 / im.width, 1188.0 / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
        x0 = (im.width - 2112) // 2
        y0 = (im.height - 1188) // 2
        im = im.crop((x0, y0, x0 + 2112, y0 + 1188))
    pct = opts.get("pct", 0.05)
    W, H = im.size
    proc = sp.Popen(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            "1920x1080",
            "-r",
            str(FPS),
            "-i",
            "-",
            "-vf",
            "setsar=1",
            "-frames:v",
            str(frames),
            *ENC,
            str(dest),
        ],
        stdin=sp.PIPE,
    )
    for n in range(frames):
        z = 1.0 + pct * n / max(1, frames)
        bw, bh = W / z, H / z
        box = ((W - bw) / 2.0, (H - bh) / 2.0, (W + bw) / 2.0, (H + bh) / 2.0)
        proc.stdin.write(im.resize((1920, 1080), Image.Resampling.BICUBIC, box=box).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"still push failed: {dest}")


_CG_RENDERER = None


def render_code_segment(plate_id: str, off: float, dur: float, suppress: set[str], reframe_at: list[tuple[float, tuple[float, float, float, float]]], dest: Path) -> None:
    global _CG_RENDERER
    sys.path.insert(0, str(HERE))
    import build_code_graphics_v02 as cg

    frames = round(dur * FPS)
    boards = json.loads(BOARDS_JSON.read_text())["plates"]
    plate = dict(next(p for p in boards if p["id"] == plate_id))
    plate["use_s"] = max(float(plate["use_s"]), off + dur)
    orig_labels = list(cg.LABELS.get(plate_id, []))
    cg.LABELS[plate_id] = [row for row in orig_labels if row[2] not in suppress]
    try:
        if _CG_RENDERER is None:
            _CG_RENDERER = cg.Renderer(CDIR / "assets")
        r = _CG_RENDERER
        proc = sp.Popen(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "rawvideo",
                "-pix_fmt",
                "rgb24",
                "-s",
                "1920x1080",
                "-r",
                str(FPS),
                "-i",
                "-",
                "-vf",
                "setsar=1",
                "-frames:v",
                str(frames),
                *ENC,
                str(dest),
            ],
            stdin=sp.PIPE,
        )
        for n in range(frames):
            local_t = n / FPS
            t = off + local_t
            im = r.frame(plate, t)
            if not isinstance(im, Image.Image):
                im = Image.fromarray(im)
            active_box = None
            for rt, rbox in reframe_at:
                if local_t >= rt:
                    active_box = rbox
            if active_box is not None:
                bx = (active_box[0] * 1920.0, active_box[1] * 1080.0, active_box[2] * 1920.0, active_box[3] * 1080.0)
                im = im.resize((1920, 1080), Image.Resampling.BICUBIC, box=bx)
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"code segment failed: {dest}")
    finally:
        cg.LABELS[plate_id] = orig_labels


def credit_free_intervals(dur: float, blocked: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if not blocked:
        return [(0.0, dur)]
    segs = [(0.0, dur)]
    for ba, bb in sorted(blocked):
        next_segs = []
        for sa, sb in segs:
            if bb <= sa or ba >= sb:
                next_segs.append((sa, sb))
            else:
                if ba - sa >= 0.45:
                    next_segs.append((sa, round(ba, 3)))
                if sb - bb >= 0.45:
                    next_segs.append((round(bb, 3), sb))
        segs = next_segs
    return segs


def render_segment(pid: str, fin: float, fout: float, kind: str, sname: str, opts: dict, seg_out: Path) -> list[str]:
    dur = round((fout - fin) * FPS) / FPS
    frames = round(dur * FPS)
    base_mp4 = WORK / f"base_{pid}.mp4"
    src = resolve_source(kind, sname)

    if kind == "video":
        off = float(opts.get("offset", 0.0))
        vf_parts = []
        if "vcrop" in opts:
            cw, ch, cx, cy = opts["vcrop"]
            vf_parts.append(f"crop={cw}:{ch}:{cx}:{cy}")
        vf_parts.append(VIDEO_VF[sname])
        vf_parts.append(f"fps={FPS},setsar=1,tpad=stop_mode=clone:stop_duration=2")
        if opts.get("fade_out"):
            fd = float(opts["fade_out"])
            vf_parts.append(f"fade=t=out:st={max(0.0, dur - fd):.3f}:d={fd:.3f}")
        sp.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{off:.3f}",
                "-i",
                str(src),
                "-vf",
                ",".join(vf_parts),
                "-frames:v",
                str(frames),
                *ENC,
                str(base_mp4),
            ],
            check=True,
        )
    elif kind == "still":
        render_still_push(src, opts, dur, base_mp4)
    elif kind == "code":
        plate_id = opts["plate_id"]
        off = float(opts.get("offset", 0.0))
        suppress = SUPPRESS_BY_PLATE.get(plate_id, set())
        reframe_at = opts.get("reframe_at", [])
        render_code_segment(plate_id, off, dur, suppress, reframe_at, base_mp4)
    else:
        raise ValueError(kind)

    ovs = overlays_for_plate(pid, fin, fout)
    credit_txt = None if kind == "code" else FULL_CREDITS.get(sname)

    # Blocked intervals where a teaching pill, chapter card, subscribe pill, or internal code label is active
    blocked = []
    for o in ovs:
        blocked.append((max(0.0, o["film_start"] - fin - 0.15), min(dur, o["film_end"] - fin + 0.15)))
    if pid in CHAPTER_CARDS:
        ca, cb, _ = CHAPTER_CARDS[pid]
        blocked.append((max(0.0, ca - fin - 0.15), min(dur, cb - fin + 0.15)))
    if pid == SUBSCRIBE_CARD[0]:
        sa, sb = SUBSCRIBE_CARD[1], SUBSCRIBE_CARD[2]
        blocked.append((max(0.0, sa - fin - 0.15), min(dur, sb - fin + 0.15)))
    if kind == "code":
        sys.path.insert(0, str(HERE))
        import build_code_graphics_v02 as cg

        plate_id = opts["plate_id"]
        off = float(opts.get("offset", 0.0))
        suppress = SUPPRESS_BY_PLATE.get(plate_id, set())
        for la, lb, ltxt in cg.LABELS.get(plate_id, []):
            if ltxt not in suppress:
                rel_a = la - off
                rel_b = lb - off
                if rel_b > 0.0 and rel_a < dur:
                    blocked.append((max(0.0, rel_a - 0.15), min(dur, rel_b + 0.15)))

    free_ivs = credit_free_intervals(dur, blocked) if credit_txt else []

    if not ovs and not free_ivs and pid not in CHAPTER_CARDS and pid != SUBSCRIBE_CARD[0]:
        shutil.move(str(base_mp4), str(seg_out))
        return []

    inputs = ["-i", str(base_mp4)]
    fc = "[0:v]null[v0];"
    idx = 0
    seg_ov_files = []

    if credit_txt and free_ivs:
        c_png = WORK / f"cred_{pid}.png"
        make_credit_png(credit_txt, c_png)
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", str(c_png)]
        en = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in free_ivs)
        fc += f"[v{idx}][{idx+1}:v]overlay=0:0:enable='{en}':eof_action=pass[v{idx+1}];"
        idx += 1

    if pid in CHAPTER_CARDS:
        ca, cb, ctitle = CHAPTER_CARDS[pid]
        ch_png = WORK / f"chcard_{pid}.png"
        make_chapter_card_png(ctitle, ch_png)
        la = max(0.0, round(ca - fin, 3))
        lb = min(dur, round(cb - fin, 3))
        ldur = max(0.3, round(lb - la, 3))
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{ldur:.3f}", "-i", str(ch_png)]
        fc += (
            f"[{idx+1}:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st={max(0.0, ldur-0.25):.3f}:d=0.25:alpha=1,"
            f"setpts=PTS-STARTPTS+{la:.3f}/TB[o{idx}];"
            f"[v{idx}][o{idx}]overlay=0:0:eof_action=pass[v{idx+1}];"
        )
        idx += 1
        seg_ov_files.append(f"chapter_card_{pid}.png")

    if pid == SUBSCRIBE_CARD[0]:
        sa, sb = SUBSCRIBE_CARD[1], SUBSCRIBE_CARD[2]
        sub_png = WORK / "subscribe_pill.png"
        make_subscribe_png(sub_png)
        la = max(0.0, round(sa - fin, 3))
        lb = min(dur, round(sb - fin, 3))
        ldur = max(0.3, round(lb - la, 3))
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{ldur:.3f}", "-i", str(sub_png)]
        fc += (
            f"[{idx+1}:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st={max(0.0, ldur-0.25):.3f}:d=0.25:alpha=1,"
            f"setpts=PTS-STARTPTS+{la:.3f}/TB[o{idx}];"
            f"[v{idx}][o{idx}]overlay=0:0:eof_action=pass[v{idx+1}];"
        )
        idx += 1
        seg_ov_files.append("subscribe_pill.png")

    for o in ovs:
        pfile = OV_PACK / o["file"]
        la = max(0.0, round(o["film_start"] - fin, 3))
        lb = min(dur, round(o["film_end"] - fin, 3))
        ldur = max(0.2, round(lb - la, 3))
        x, y = int(o["x"]), int(o["y"])
        rise = 22
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{ldur:.3f}", "-i", str(pfile)]
        fc += (
            f"[{idx+1}:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={max(0.0, ldur-0.30):.3f}:d=0.30:alpha=1,"
            f"setpts=PTS-STARTPTS+{la:.3f}/TB[o{idx}];"
            f"[v{idx}][o{idx}]overlay=x={x}:y='{y}+{rise}*max(0\\,1-(t-{la:.3f})/0.35)':eval=frame:eof_action=pass[v{idx+1}];"
        )
        idx += 1
        seg_ov_files.append(o["file"])

    fc += f"[v{idx}]format=yuv420p[v]"
    fc_path = WORK / f"fc_{pid}.txt"
    fc_path.write_text(fc)
    sp.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            *inputs,
            "-/filter_complex",
            str(fc_path),
            "-map",
            "[v]",
            "-frames:v",
            str(frames),
            *ENC,
            str(seg_out),
        ],
        check=True,
    )
    base_mp4.unlink(missing_ok=True)
    return seg_ov_files


def make_contact_sheet(video_mp4: Path, cuts: list[dict], part_id: str, ch_name: str, dst: Path) -> None:
    cols = 2
    w, h, bar = 640, 360, 28
    rows_n = (len(cuts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows_n * (h + bar)), (18, 22, 30))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 16)
    for i, c in enumerate(cuts):
        mid = 0.5 * (c["timeline_in"] + c["timeline_out"])
        fmid = 0.5 * (c["film_in"] + c["film_out"])
        raw = sp.run(
            ["ffmpeg", "-v", "error", "-ss", f"{mid:.3f}", "-i", str(video_mp4), "-frames:v", "1", "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            capture_output=True,
            check=True,
        ).stdout
        im = Image.frombytes("RGB", (w, h), raw)
        x = (i % cols) * w
        y = (i // cols) * (h + bar)
        sheet.paste(im, (x, y))
        cap = f"{part_id} · {int(fmid//60)}:{fmid%60:04.1f} (part {mid:5.1f}s) · {c['plate_id']} · {c['source']} ({c['upscale']:.2f}x)"
        d.text((x + 8, y + h + 5), cap, font=f, fill=(235, 240, 248))
    sheet.save(dst, quality=88)


def main() -> None:
    problems = check_plan()
    if "--plan" in sys.argv or problems:
        raise SystemExit(1 if problems else 0)

    only_parts = None
    if "--only" in sys.argv:
        i = sys.argv.index("--only")
        only_parts = set(sys.argv[i + 1].split(","))

    WORK.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PACK.mkdir(parents=True, exist_ok=True)

    rev_path = PACK / "reviewed_ok.json"
    rev_path.write_text(json.dumps(REVIEWED_OK, indent=2) + "\n")

    summary_rows = []
    for part_id, ch_name, p_in, p_out, rows in PARTS:
        if only_parts and part_id not in only_parts:
            continue
        p_dur = round((p_out - p_in) * FPS) / FPS
        p_pack = PACK / part_id
        p_pack.mkdir(parents=True, exist_ok=True)
        seg_files = []
        cuts = []
        rel_t = 0.0

        print(f"\n>>> Assembling {part_id} ({ch_name}, {p_in:.2f}-{p_out:.2f}s, {len(rows)} plates) <<<", flush=True)
        for pid, rnum, fin, fout, kind, sname, opts in rows:
            dur = round((fout - fin) * FPS) / FPS
            seg_mp4 = WORK / f"{part_id}_{pid}.mp4"
            ov_files = render_segment(pid, fin, fout, kind, sname, opts, seg_mp4)
            seg_files.append(seg_mp4)
            src_path = resolve_source(kind, sname)
            up = compute_upscale(kind, src_path, opts)
            framing = {"offset": opts["offset"]} if kind in ("video", "code") else {"box": list(opts["box"]), "pct": opts.get("pct", 0.05)}
            cuts.append(
                {
                    "row": str(rnum),
                    "plate_id": pid,
                    "chapter": ch_name,
                    "timeline_in": round(rel_t, 3),
                    "timeline_out": round(rel_t + dur, 3),
                    "film_in": round(fin, 3),
                    "film_out": round(fout, 3),
                    "source": sname,
                    "upscale": up,
                    "framing": framing,
                    "overlays": ov_files,
                    "credit": "CGI" if kind == "code" else FULL_CREDITS.get(sname),
                }
            )
            rel_t = round(rel_t + dur, 3)

        # Concatenate video segments
        v_concat = WORK / f"{part_id}_video.mp4"
        lst = WORK / f"{part_id}_concat.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in seg_files))
        sp.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(v_concat)], check=True)
        for p in seg_files:
            p.unlink(missing_ok=True)

        # Slice VO and normalize to -14 LUFS, padding silence at the end of part06 (469.34 -> 472.84s)
        a_wav = WORK / f"{part_id}_vo.wav"
        af_parts = [f"apad=whole_dur={p_dur:.3f}", "loudnorm=I=-14:TP=-1.5:LRA=11"]
        if part_id == "part06":
            af_parts.append(f"afade=t=out:st={max(0.0, p_dur - 1.0):.3f}:d=1.0")
        sp.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{p_in:.3f}",
                "-t",
                f"{p_dur:.3f}",
                "-i",
                str(VO_WAV),
                "-af",
                ",".join(af_parts),
                "-ar",
                "48000",
                "-ac",
                "2",
                str(a_wav),
            ],
            check=True,
        )

        out_mp4 = OUT_DIR / f"028_Gliese710_{part_id}_rough_v01.mp4"
        sp.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(v_concat),
                "-i",
                str(a_wav),
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-shortest",
                str(out_mp4),
            ],
            check=True,
        )
        v_concat.unlink(missing_ok=True)
        a_wav.unlink(missing_ok=True)

        cuts_json = p_pack / f"cuts_{part_id}_v01.json"
        cuts_json.write_text(json.dumps(cuts, indent=2) + "\n")

        sheet_jpg = PACK / f"{part_id}_rough_v01_contact_sheet.jpg"
        make_contact_sheet(out_mp4, cuts, part_id, ch_name, sheet_jpg)

        # Run picture_qa.py (which also runs polish_gate.py)
        sp.run(
            [
                "python3",
                str(ROOT / "scripts" / "picture_qa.py"),
                str(out_mp4),
                "--cuts",
                str(cuts_json),
                "--pool",
                str(POOL_JSON),
                "--pool",
                str(POOL_OV_JSON),
                "--pool",
                str(POOL_CG_JSON),
                "--reviewed-ok",
                str(rev_path),
                "--out-dir",
                str(p_pack),
            ],
            check=False,
        )
        # Also write standalone polish_gate.json
        sp.run(
            [
                "python3",
                str(ROOT / "scripts" / "polish_gate.py"),
                str(out_mp4),
                "--cuts",
                str(cuts_json),
                "--reviewed-ok",
                str(rev_path),
                "--out",
                str(p_pack / "polish_gate.json"),
            ],
            check=False,
        )

        pqa = json.loads((p_pack / "picture_qa.json").read_text())
        pg_res = json.loads((p_pack / "polish_gate.json").read_text())
        sha = hashlib.sha256(out_mp4.read_bytes()).hexdigest()
        meta = {
            "film": "028",
            "job": "J0855",
            "part": part_id,
            "chapter": ch_name,
            "film_in_s": p_in,
            "film_out_s": p_out,
            "duration_s": p_dur,
            "plates": len(cuts),
            "mp4": str(out_mp4),
            "sha256": sha,
            "contact_sheet": str(sheet_jpg.relative_to(ROOT)),
            "picture_qa_verdict": pqa["verdict"],
            "picture_qa_failed": len(pqa["failed"]),
            "picture_qa_warn": len(pqa["warn"]),
            "polish_gate_verdict": pg_res["verdict"],
            "polish_gate_failed": len(pg_res["failed"]),
            "polish_gate_warn": len(pg_res["warn"]),
            "flow_credits_spent_retake": 10 if part_id == "part02" else 0,
            "spend_gbp": 0.0,
        }
        (p_pack / f"ROUGH_META_{part_id}_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
        summary_rows.append(meta)
        print(
            f"=== {part_id} DONE: sha={sha[:12]} picture_qa={pqa['verdict']} ({len(pqa['failed'])} fail, {len(pqa['warn'])} warn) "
            f"polish_gate={pg_res['verdict']} ({len(pg_res['failed'])} fail) ===",
            flush=True,
        )

    all_meta = []
    for pid_i, *_ in PARTS:
        mpath = PACK / pid_i / f"ROUGH_META_{pid_i}_v01.json"
        if mpath.exists():
            all_meta.append(json.loads(mpath.read_text()))
    if len(all_meta) == len(PARTS):
        (PACK / "PART_ROUGHS_SUMMARY_v01.json").write_text(json.dumps(all_meta, indent=2) + "\n")
    shutil.rmtree(WORK, ignore_errors=True)


if __name__ == "__main__":
    main()
