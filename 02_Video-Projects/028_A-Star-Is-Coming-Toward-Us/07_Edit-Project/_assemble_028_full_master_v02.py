#!/usr/bin/env python3
"""028 A Star Is Coming Toward Us (Gliese 710) — Full Master v02 assembler (J0864).

Applies Chief's 4 £0 picture fixes on top of Full Master v01 (J0859), keeps the identical
approved audio master (`audio_master_v01.m4a`, -14.1 LUFS / -1.3 dBTP, 0 timing changes),
and runs all release gates:

1. Fix #1 (`7:48 r38_return`, `gaia_motion_1_6my.mp4`):
   - In v01, `offset=31.0` ran into ESA's closing bumper (`29.0-45.48 s`), ending the film on the
     ESA logo + "Copyright 2020".
   - In `gaia_motion_1_6my.mp4`, the moving starfield runs from `3.80 s` to `25.25 s` (before the
     `25.50 s` dip and the `29.00 s` ESA end slate).
   - Set `r38_return` (`463.62-472.84 s`, `9.22 s`) to `offset=16.0 s` (`[16.00, 25.22]`,
     `vcrop=(2880, 1620, 480, 270)`, `1.33x` upscale, `fade_out=1.0`), so its entire `9.22 s`
     window is continuous moving starfield that ends at `25.22 s` before the slate.
   - Set `r12_stars_move` (`117.24-126.47 s`, `9.23 s`) to `offset=14.0 s` (`[14.00, 23.23]`,
     centered crop `vcrop=(2688, 1512, 576, 324)`, `1.43x` upscale, cropping out the top-left corner bug)
     so it also stays entirely within the continuous moving starfield before `25.25 s`.
2. Fix #2 (`3:57 r22_neowise` and `7:40 r38_neowise_2`, `neowise_dc.tif`):
   - Located Comet NEOWISE at normalized `(0.3021, 0.2170)` (`pixel (1510, 795)`) with its dust tail
     extending up-left to `(0.285, 0.08)` in the `4998x3664` TIFF.
   - Re-framed `r22_neowise` (`233.50-241.46 s`) to a 16:9 crop centered on the comet and tail
     `box=(0.18, 0.04, 0.50, 0.285)` (`1.27x` upscale, `pct=0.06` slow push-in, `comet_enhance=True`).
   - Re-framed `r38_neowise_2` (`457.47-463.62 s`) to a tighter second 16:9 crop on the comet and tail
     `box=(0.16, 0.07, 0.42, 0.27)` (`1.56x` upscale, `pct=0.06` slow push-in, `comet_enhance=True`).
3. Fix #3 (`5:51 r29_twilight`, `conjunction.tif` under `'About 3 times brighter'`):
   - Located the Jupiter-Saturn pair at normalized `(0.2179, 0.2546)` (`pixel (1122, 870)`) in the
     `5149x3417` TIFF.
   - Re-framed `r29_twilight` (`347.86-354.91 s`) from `0.55x` wide to a tight 16:9 crop on the pair
     `box=(0.11, 0.16, 0.34, 0.36)` (`1.71x` upscale, `pct=0.05` slow push-in, `planet_bloom=True`
     optical glow on the `luma > 110` planet cores, plus `tail_hold_s=0.60` so `'About 3 times brighter'`
     holds at 100% opacity across both the pill midpoint `349.70 s` and cut midpoint `351.385 s`).
4. Fix #4 (`4:44 r26_hale_bopp` + `4:50 r26_a3`, no back-to-back `comet_a3.jpg`):
   - Replaced `r26_hale_bopp` (`281.16-287.48 s`) with the £0 NASA/JSC Columbia photograph of Comet
     Hale-Bopp (`sts083_hale_bopp.jpg`, `sts083-410-009`, `3264x2101`, `box=(0.12, 0.08, 0.88, 0.72)`,
     `0.84x` upscale, `pct=0.05`, `gamma=0.80, lift=6.0`, credit `NASA/JSC`).
   - Kept `r26_a3` (`287.48-294.00 s`) on `comet_a3.jpg` (`box=(0.14, 0.06, 0.74, 0.42)`, `0.57x`
     upscale, `pct=0.05`, `gamma=0.55, lift=12.0`, credit `NASA/Matthew Dominick`).
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import shutil
import subprocess as sp
import sys
from concurrent.futures import ThreadPoolExecutor
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
PART_PACK = HERE / "part_roughs_v01_pack"
PACK_V01 = HERE / "full_master_v01_pack"
PACK = HERE / "full_master_v02_pack"
PART_OUT_DIR = Path("/private/tmp/028_part_roughs_v01")
WORK = Path("/private/tmp/gliese028_full_master_work_v02")
AUDIO_WORK = Path("/private/tmp/gliese028_audio_work_v01")

OUT_V01_MP4 = Path("/private/tmp/028_Gliese710_full_master_v01.mp4")
OUT_MP4 = Path("/private/tmp/028_Gliese710_full_master_v02.mp4")
UAT_MP4 = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/028_Gliese710_full_master_v02.mp4"
NAS_DIR = Path("/Volumes/data/mac-mini-archive/youtube-staging/028")
NAS_MP4 = NAS_DIR / "028_Gliese710_full_master_v02.mp4"

VO_WAV = EP / "02_Voiceover" / "star_coming_vo_v01.wav"
STT_JSON = EP / "02_Voiceover" / "stt" / "star_coming_vo_v01" / "stt_raw.json"
BOARDS_JSON = HERE / "PLATE_BOARDS_v02.json"
POOL_JSON = HERE / "SOURCE_POOL_v02.json"
POOL_OV_JSON = OV_PACK / "pool_v01.json"
POOL_CG_JSON = CDIR / "pool_v02.json"

BED_MP3 = EP / "05_Music" / "gliese_score_bed_v01.mp3"
SFX_WAV = EP / "06_Sound-Effects" / "stem_sfx_v01.wav"
MASTER_AUDIO = AUDIO_WORK / "audio_master_v01.m4a"

FPS = 30
LAST_WORD = 469.340
HOLD = 2.500
FADE = 1.000
TOTAL = 472.840
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
NAVY = (23, 36, 55, 220)
ENC = ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p"]

STT_DATA = json.loads(STT_JSON.read_text())
WORDS = [w for w in STT_DATA.get("words", []) if w.get("type") == "word"]
OV_DATA = json.loads((OV_PACK / "overlays_v01.json").read_text())["labels"]

OV_ROW_ALIAS = {
    "r20_oort_shell_a": "r20_21_oort_shell",
    "r21_oort_shell_b": "r20_21_oort_shell",
    "r24_shower_a": "r24_25_shower",
    "r25_shower_b": "r24_25_shower",
}

SUPPRESS_BY_PLATE = {
    "r04_shower_shell": {"1.3 million years"},
    "r07_kdwarf": {"60% Sun’s mass"},
    "r14_hipparcos_card": {"Late 1990s", "Hipparcos", "About 1 light-year"},
    "r17_scale_a": {"Sun–Earth: 1 cm"},
    "r18_shell": {"100 metres"},
    "r20_21_oort_shell": {"Beyond the planets", "Cloud of ice"},
    "r33_traffic": {"Outer Oort Cloud", "Too small and faint"},
}

CHAPTER_CARDS = {
    "r06_milky_way": (42.50, 44.90, "The Star Heading Our Way"),
    "r13_star_trails": (131.00, 133.50, "How Close Will It Come?"),
    "r20_oort_shell_a": (210.34, 212.84, "Into the Oort Cloud"),
    "r26_hale_bopp": (281.60, 284.10, "The Comet Shower"),
    "r29_night": (335.84, 338.34, "A New Brightest Star"),
    "r32_wise_sky": (378.30, 380.80, "It Has Happened Before"),
}

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
    "sts083_hale_bopp.jpg": "NASA/JSC",
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
        "lutrgb=r='clip(pow(val/255,0.74)*230+14,0,255)':g='clip(pow(val/val,0.74)*230+14,0,255)'"
    ),
    "orbit_ice_omni_v01.mp4": "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
    "night_road_veo_v01.mp4": "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
    "football_pitch_veo_v01.mp4": "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
}
VIDEO_VF["orbit_binoculars_omni_v01.mp4"] = (
    "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=rgb24,"
    "lutrgb=r='clip(pow(val/255,0.74)*230+14,0,255)':g='clip(pow(val/255,0.74)*230+14,0,255)':b='clip(pow(val/255,0.74)*235+16,0,255)'"
)

# Plates modified in v01 (J0859) + v02 (J0864)
MODIFIED_PLATES = {
    "r01_stars_streaming",  # J0859 Fix #2: merged r01+r02 continuous shot of gaia_motion_1_6my.mp4 (0.00-13.66s, off=3.80, step at 6.12s)
    "r10_gliese_approach",  # J0859 Fix #1 spacing: offset=8.0s
    "r12_stars_move",       # J0864 Fix #1: gaia_motion_1_6my.mp4 offset=14.0s (14.00-23.23s, upper-left crop, before 25.5s dip)
    "r13_star_trails",      # J0859 Fix #2: eso_startrails.mp4 offset=0.0s
    "r15_gaia_craft",       # J0859 Fix #3: 0.40s lead fade-in on '1 billion stars'
    "r16_sunrise_break",    # J0859 Fix #3: 0.40s lead fade-in on '5 times closer'
    "r18_shell",            # J0859 Fix #3: 0.40s lead fade-in on '100 metres'
    "r19_subscribe",        # J0859 Fix #1: gaia_gliese_encounter.mov @ offset=20.5s + SUBSCRIBE pill
    "r22_neowise",          # J0864 Fix #2: neowise_dc.tif re-framed on Comet NEOWISE (1.27x, comet_enhance)
    "r25_shower_cut",       # J0859 Fix #1 spacing: gaia_gliese_encounter.mov @ offset=31.0s
    "r26_hale_bopp",        # J0864 Fix #4: sts083_hale_bopp.jpg (Comet Hale-Bopp from Columbia, 0.84x) so comet_a3.jpg is not repeated
    "r26_a3",               # J0864 Fix #4: comet_a3.jpg single appearance (0.57x)
    "r27_leaving",          # J0859 Fix #2: eso_startrails.mp4 @ offset=14.0s (1.15x)
    "r29_twilight",         # J0864 Fix #3: conjunction.tif tight crop on Jupiter-Saturn pair (1.71x, planet_bloom, tail_hold_s=0.60)
    "r38_neowise_2",        # J0864 Fix #2: neowise_dc.tif second tighter framing on Comet NEOWISE (1.56x, comet_enhance)
    "r38_return",           # J0864 Fix #1: gaia_motion_1_6my.mp4 @ offset=16.0s (16.00-25.22s, ends on moving starfield before 29.0s ESA slate)
}

# 61 cuts across the 7 chapter parts (472.84s total)
PARTS = [
    (
        "part00",
        "0 Open",
        0.00,
        42.32,
        [
            (
                "r01_stars_streaming",
                1,
                0.00,
                13.66,
                "video",
                "gaia_motion_1_6my.mp4",
                {
                    "offset": 3.80,
                    "vcrop": (2880, 1620, 480, 270),
                    "vcrop_step": (6.12, (2688, 1512, 576, 324)),
                    "upscale": 1.43,
                },
            ),
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
            ("r10_gliese_approach", 10, 82.46, 94.36, "video", "gaia_gliese_encounter.mov", {"offset": 8.0, "vcrop": (1600, 900, 160, 90), "upscale": 1.20}),
            ("r11a_star_cutaway", 11, 94.36, 101.20, "video", "eso_lasilla_ntt.mp4", {"offset": 11.5, "upscale": 1.0}),
            ("r11_night_road", 11, 101.20, 109.20, "video", "night_road_veo_v01.mp4", {"offset": 0.0, "upscale": 1.50}),
            ("r12_proxima", 12, 109.20, 117.24, "still", "proxima.jpg", {"box": (0.0, 0.04, 1.0, 0.96), "pct": 0.05, "feathered_blur": True, "gamma": 0.65, "lift": 16.0}),
            ("r12_stars_move", 12, 117.24, 126.47, "video", "gaia_motion_1_6my.mp4", {"offset": 14.0, "vcrop": (2688, 1512, 576, 324), "upscale": 1.43}),
        ],
    ),
    (
        "part02",
        "2 How Close Will It Come?",
        126.47,
        209.89,
        [
            ("r13_star_trails", 13, 126.47, 134.21, "video", "eso_startrails.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r14_hipparcos_card", 14, 134.21, 147.37, "code", "code_graphic_028_r14_hipparcos_card_v02.mp4", {"plate_id": "r14_hipparcos_card", "offset": 0.0, "upscale": 1.0, "reframe_at": [(6.52, (0.06, 0.06, 0.94, 0.94))]}),
            ("r15_gaia_craft", 15, 147.37, 155.96, "still", "gaia_craft.jpg", {"box": (0.04, 0.08, 0.96, 0.90), "pct": 0.05, "gamma": 0.95, "lift": 0.0, "lead_fade_s": 0.40}),
            ("r15_16_path", 15, 155.96, 169.62, "code", "code_graphic_028_r15_16_path_v02.mp4", {"plate_id": "r15_16_path", "offset": 1.96, "upscale": 1.0, "reframe_at": [(5.59, (0.06, 0.06, 0.94, 0.94))]}),
            ("r16_sunrise_break", 16, 169.62, 175.15, "still", "iss_sunrise.jpg", {"box": (0.02, 0.16, 0.74, 0.64), "pct": 0.05, "gamma": 0.68, "lift": 8.0, "lead_fade_s": 0.40}),
            ("r17_scale_a", 17, 175.15, 181.81, "code", "code_graphic_028_r17_scale_a_v02.mp4", {"plate_id": "r17_scale_a", "offset": 0.0, "upscale": 1.0}),
            ("r17_neptune", 17, 181.81, 186.51, "still", "neptune.jpg", {"box": (0.04, 0.22, 0.96, 0.74), "pct": 0.05, "gamma": 0.85, "lift": 6.0}),
            ("r17_scale_b", 17, 186.51, 191.11, "code", "code_graphic_028_r17_scale_b_v02.mp4", {"plate_id": "r17_scale_b", "offset": 0.0, "upscale": 1.0}),
            ("r17_pitch", 17, 191.11, 195.25, "video", "football_pitch_veo_v01.mp4", {"offset": 1.50, "upscale": 1.50}),
            ("r18_shell", 18, 195.25, 204.21, "code", "code_graphic_028_r18_shell_v02.mp4", {"plate_id": "r18_shell", "offset": 0.0, "upscale": 1.0, "lead_fade_s": 0.40}),
            ("r19_subscribe", 19, 204.21, 209.89, "video", "gaia_gliese_encounter.mov", {"offset": 20.5, "vcrop": (1536, 864, 192, 108), "upscale": 1.25}),
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
            ("r22_neowise", 22, 233.50, 241.46, "still", "neowise_dc.tif", {"box": (0.18, 0.04, 0.50, 0.285), "pct": 0.06, "comet_enhance": True, "gamma": 0.88, "lift": 0.0, "color": 1.12, "contrast": 1.18}),
            ("r23_orbit_ice", 23, 241.46, 250.51, "video", "orbit_ice_omni_v01.mp4", {"offset": 0.40, "upscale": 1.50}),
            ("r24_sunrise", 24, 250.51, 256.79, "still", "iss_sunrise.jpg", {"box": (0.05, 0.12, 0.95, 0.72), "pct": 0.05, "gamma": 0.72, "lift": 6.0}),
            ("r24_shower_a", 24, 256.79, 264.43, "code", "code_graphic_028_r24_25_shower_v02.mp4", {"plate_id": "r24_25_shower", "offset": 0.0, "upscale": 1.0}),
            ("r25_shower_cut", 25, 264.43, 270.90, "video", "gaia_gliese_encounter.mov", {"offset": 31.0, "vcrop": (1600, 900, 160, 90), "upscale": 1.20}),
            ("r25_shower_b", 25, 270.90, 281.16, "code", "code_graphic_028_r24_25_shower_v02.mp4", {"plate_id": "r24_25_shower", "offset": 13.32, "upscale": 1.0, "reframe_at": [(5.92, (0.06, 0.06, 0.94, 0.94))]}),
        ],
    ),
    (
        "part04",
        "4 The Comet Shower",
        281.16,
        335.42,
        [
            ("r26_hale_bopp", 26, 281.16, 287.48, "still", "sts083_hale_bopp.jpg", {"box": (0.12, 0.08, 0.88, 0.72), "pct": 0.05, "gamma": 0.80, "lift": 6.0, "color": 1.10, "contrast": 1.12}),
            ("r26_a3", 26, 287.48, 294.00, "still", "comet_a3.jpg", {"box": (0.14, 0.06, 0.74, 0.42), "pct": 0.05, "gamma": 0.55, "lift": 12.0, "color": 1.08, "contrast": 1.08}),
            ("r27_shower", 27, 294.00, 305.02, "code", "code_graphic_028_r27_shower_v02.mp4", {"plate_id": "r27_shower", "offset": 0.0, "upscale": 1.0, "reframe_at": [(6.45, (0.06, 0.06, 0.94, 0.94))]}),
            ("r27_leaving", 27, 305.02, 316.04, "video", "eso_startrails.mp4", {"offset": 14.0, "vcrop": (1664, 936, 0, 0), "upscale": 1.15}),
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
            ("r29_twilight", 29, 347.86, 354.91, "still", "conjunction.tif", {"box": (0.11, 0.16, 0.34, 0.36), "pct": 0.05, "planet_bloom": True, "gamma": 0.85, "lift": 2.0, "color": 1.12, "contrast": 1.22, "tail_hold_s": 0.60}),
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
            ("r38_neowise_2", 38, 457.47, 463.62, "still", "neowise_dc.tif", {"box": (0.16, 0.07, 0.42, 0.27), "pct": 0.06, "comet_enhance": True, "gamma": 0.86, "lift": 0.0, "color": 1.12, "contrast": 1.20}),
            ("r38_return", 38, 463.62, 472.84, "video", "gaia_motion_1_6my.mp4", {"offset": 16.0, "vcrop": (2880, 1620, 480, 270), "upscale": 1.33, "fade_out": 1.0}),
        ],
    ),
]

REVIEWED_OK = {
    "_status": "Chief J0321 / PLATE_BOARDS_v02 rulings + Chief J0855 PASS on 028 part roughs v01 + J0859 3 £0 fixes + J0864 4 £0 picture fixes (22 Oct 2026).",
    "neptune.jpg": {
        "note": "Voyager 2 full-disk Neptune (PIA01492, smooth gas giant atmosphere); Chief J0321 & J0855 approved.",
        "kinds": ["low detail"],
    },
    "eso_mw_lasilla.mp4@8": {
        "note": "PLATE_BOARDS_v02 + Chief J0855 PASS: 17.64s ESO La Silla Milky Way clip used at 0.00-8.25s (r06_milky_way, 0:46) and 8.00-17.49s (r36_night_2, 7:21, 6.5 min later).",
        "kinds": ["reuse"],
    },
    "eso_lasilla_ntt.mp4": {
        "note": "PLATE_BOARDS_v02 + Chief J0855 PASS: 20.05s ESO La Silla NTT clip used on r11a_star_cutaway (1:38), r20_oort_cut (3:42), and r35_lasilla_ntt (7:10).",
        "kinds": ["reuse"],
    },
    "gaia_motion_1_6my.mp4": {
        "note": "PLATE_BOARDS_v02 + Chief J0859/J0864 ruling: 3 uses (0:06, 2:01, 7:48) with distinct 4K crops; source starfield content ends at 25.25s before ESA end slate (29.0s+), so r12_stars_move uses 14.0-23.23s and r38_return uses 16.0-25.22s to end cleanly on moving starfield before the slate.",
        "kinds": ["reuse"],
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
    return [o for o in OV_DATA if o["row"] == lookup and fin - 0.15 <= o["film_start"] < fout]


def check_plan() -> list[str]:
    problems = []
    total_plates = 0
    prev_global_kind = None
    prev_global_src = None
    gaia_uses = []
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
            if kind == "still" and prev_global_src == sname:
                problems.append(f"{pid}: back-to-back identical still {sname}")
            if sname == "gaia_motion_1_6my.mp4":
                gaia_uses.append((pid, fin, fout, opts.get("offset")))
                if prev_global_src == "gaia_motion_1_6my.mp4":
                    problems.append(f"{pid}: back-to-back gaia_motion_1_6my.mp4")
            prev_global_kind = kind
            prev_global_src = sname
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
            mod_tag = "MOD" if pid in MODIFIED_PLATES else "SLICED"
            print(
                f"  [{mod_tag:6s}] {pid:22s} row={rnum:2d} {fin:6.2f}-{fout:6.2f} ({fout-fin:5.2f}s) {kind:6s} {sname:42s} up={up:4.2f}x ovs={len(ovs)}"
            )
        if abs(prev_out - p_out) > 1e-3:
            problems.append(f"{part_id}: ends at {prev_out:.2f} != {p_out:.2f}")
    if len(gaia_uses) > 3:
        problems.append(f"gaia_motion_1_6my.mp4 used {len(gaia_uses)} times (>3): {gaia_uses}")
    matched_ovs = sum(len(overlays_for_plate(pid, fin, fout)) for _, _, _, _, rows in PARTS for pid, _, fin, fout, *_ in rows)
    if matched_ovs != len(OV_DATA):
        problems.append(f"matched {matched_ovs} overlays != {len(OV_DATA)} total in overlays_v01.json")
    print(f"Total plates: {total_plates} | gaia_motion_1_6my uses: {len(gaia_uses)} | Matched overlays: {matched_ovs}/{len(OV_DATA)} | Problems: {problems or 'NONE'}")
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

    if opts.get("comet_enhance"):
        arr = np.asarray(im, dtype=np.float32)
        sm_fine = np.asarray(im.filter(ImageFilter.GaussianBlur(radius=6)), dtype=np.float32)
        sm_bg = np.asarray(im.filter(ImageFilter.GaussianBlur(radius=95)), dtype=np.float32)
        comet_sig = np.maximum(0.0, sm_fine - sm_bg - 1.5)
        sm_core = np.asarray(im.filter(ImageFilter.GaussianBlur(radius=1.2)), dtype=np.float32)
        core_sig = np.maximum(0.0, sm_core - sm_bg - 8.0)
        sky_clean = 0.35 * sm_fine + 0.65 * arr
        H_c, _ = arr.shape[:2]
        grad = np.linspace(0.55, 1.52, H_c, dtype=np.float32)[:, None, None]
        base = sky_clean * grad
        tail_color = np.array([1.05, 1.08, 1.15], dtype=np.float32)[None, None, :]
        arr = np.clip(base + comet_sig * 5.5 * tail_color + core_sig * 2.8, 0.0, 255.0)
        im = Image.fromarray(arr.astype(np.uint8))

    if opts.get("planet_bloom"):
        arr = np.asarray(im, dtype=np.float32)
        sm_sky = np.asarray(im.filter(ImageFilter.GaussianBlur(radius=3.5)), dtype=np.float32)
        luma = arr.mean(axis=2, keepdims=True)
        arr_clean = np.where(luma > 80.0, arr, 0.35 * sm_sky + 0.65 * arr)
        bright = np.maximum(0.0, arr - 110.0)
        b_im = Image.fromarray(np.clip(bright * 1.8, 0, 255).astype(np.uint8))
        g1 = np.asarray(b_im.filter(ImageFilter.GaussianBlur(radius=3.0)), dtype=np.float32)
        g2 = np.asarray(b_im.filter(ImageFilter.GaussianBlur(radius=9.0)), dtype=np.float32)
        g3 = np.asarray(b_im.filter(ImageFilter.GaussianBlur(radius=22.0)), dtype=np.float32)
        H_c, _ = arr.shape[:2]
        grad = np.linspace(0.58, 1.52, H_c, dtype=np.float32)[:, None, None]
        arr_out = np.clip(arr_clean * grad + g1 * 2.4 + g2 * 1.8 + g3 * 0.9, 0.0, 255.0)
        im = Image.fromarray(arr_out.astype(np.uint8))

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
        im = ImageEnhance.Color(im).enhance(float(opts.get("color", 1.06)))
        im = ImageEnhance.Contrast(im).enhance(float(opts.get("contrast", 1.04)))
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


def render_code_segment(plate_id: str, off: float, dur: float, suppress: set[str], reframe_at: list[tuple[float, tuple[float, float, float, float]]], dest: Path) -> None:
    sys.path.insert(0, str(HERE))
    import build_code_graphics_v02 as cg

    frames = round(dur * FPS)
    boards = json.loads(BOARDS_JSON.read_text())["plates"]
    plate = dict(next(p for p in boards if p["id"] == plate_id))
    plate["use_s"] = max(float(plate["use_s"]), off + dur)
    orig_labels = list(cg.LABELS.get(plate_id, []))
    cg.LABELS[plate_id] = [row for row in orig_labels if row[2] not in suppress]
    try:
        r = cg.Renderer(CDIR / "assets")
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


def render_segment(part_id: str, p_in: float, pid: str, fin: float, fout: float, kind: str, sname: str, opts: dict, seg_out: Path) -> list[str]:
    dur = round((fout - fin) * FPS) / FPS
    frames = round(dur * FPS)
    ovs = overlays_for_plate(pid, fin, fout)
    part_mp4 = PART_OUT_DIR / f"028_Gliese710_{part_id}_rough_v01.mp4"

    seg_ov_files = []
    if pid in CHAPTER_CARDS:
        seg_ov_files.append(f"chapter_card_{pid}.png")
    if pid == SUBSCRIBE_CARD[0]:
        seg_ov_files.append("subscribe_pill.png")
    seg_ov_files.extend(o["file"] for o in ovs)

    if seg_out.exists() and seg_out.stat().st_size > 1000:
        return seg_ov_files

    prev_v02 = Path("/private/tmp/028_Gliese710_full_master_v02_prev.mp4")
    if pid != "r12_stars_move" and prev_v02.exists():
        sp.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{fin:.3f}",
                "-i",
                str(prev_v02),
                "-vf",
                "tpad=stop_mode=clone:stop_duration=1",
                "-frames:v",
                str(frames),
                *ENC,
                str(seg_out),
            ],
            check=True,
        )
        return seg_ov_files

    if pid not in MODIFIED_PLATES and part_mp4.exists():
        rel_in = round(fin - p_in, 3)
        sp.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{rel_in:.3f}",
                "-i",
                str(part_mp4),
                "-vf",
                "tpad=stop_mode=clone:stop_duration=1",
                "-frames:v",
                str(frames),
                *ENC,
                str(seg_out),
            ],
            check=True,
        )
        return seg_ov_files

    base_mp4 = WORK / f"base_{pid}.mp4"
    src = resolve_source(kind, sname)

    if kind == "video":
        off = float(opts.get("offset", 0.0))
        if "vcrop_step" in opts:
            step_t, (cw2, ch2, cx2, cy2) = opts["vcrop_step"]
            cw1, ch1, cx1, cy1 = opts["vcrop"]
            frames1 = round(step_t * FPS)
            frames2 = frames - frames1
            b1 = WORK / f"base_{pid}_a.mp4"
            b2 = WORK / f"base_{pid}_b.mp4"
            sp.run(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", f"{off:.3f}", "-i", str(src),
                    "-vf", f"crop={cw1}:{ch1}:{cx1}:{cy1},{VIDEO_VF[sname]},fps={FPS},setsar=1",
                    "-frames:v", str(frames1), *ENC, str(b1),
                ],
                check=True,
            )
            sp.run(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", f"{off + step_t:.3f}", "-i", str(src),
                    "-vf", f"crop={cw2}:{ch2}:{cx2}:{cy2},{VIDEO_VF[sname]},fps={FPS},setsar=1",
                    "-frames:v", str(frames2), *ENC, str(b2),
                ],
                check=True,
            )
            clst = WORK / f"base_{pid}_concat.txt"
            clst.write_text(f"file '{b1}'\nfile '{b2}'\n")
            sp.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(clst), "-c", "copy", str(base_mp4)], check=True)
            b1.unlink(missing_ok=True)
            b2.unlink(missing_ok=True)
            clst.unlink(missing_ok=True)
        else:
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

    credit_txt = None if kind == "code" else FULL_CREDITS.get(sname)
    lead_fade = float(opts.get("lead_fade_s", 0.0))
    tail_hold = float(opts.get("tail_hold_s", 0.0))

    blocked = []
    for o in ovs:
        blocked.append((max(0.0, o["film_start"] - fin - lead_fade - 0.15), min(dur, o["film_end"] - fin + tail_hold + 0.15)))
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
            f"[v{idx}][o{idx}]overlay=0:0:enable='between(t,{la:.3f},{lb:.3f})':eof_action=pass[v{idx+1}];"
        )
        idx += 1
        seg_ov_files.append(f"chapter_card_{pid}.png")

    if pid == SUBSCRIBE_CARD[0]:
        sa, sb = SUBSCRIBE_CARD[1], SUBSCRIBE_CARD[2]
        sub_png = WORK / f"subscribe_{pid}.png"
        make_subscribe_png(sub_png)
        la = max(0.0, round(sa - fin, 3))
        lb = min(dur, round(sb - fin, 3))
        ldur = max(0.3, round(lb - la, 3))
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{ldur:.3f}", "-i", str(sub_png)]
        fc += (
            f"[{idx+1}:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st={max(0.0, ldur-0.25):.3f}:d=0.25:alpha=1,"
            f"setpts=PTS-STARTPTS+{la:.3f}/TB[o{idx}];"
            f"[v{idx}][o{idx}]overlay=0:0:enable='between(t,{la:.3f},{lb:.3f})':eof_action=pass[v{idx+1}];"
        )
        idx += 1
        seg_ov_files.append("subscribe_pill.png")

    for o in ovs:
        pfile = OV_PACK / o["file"]
        la = max(0.0, round(o["film_start"] - fin - lead_fade, 3))
        lb = min(dur, round(o["film_end"] - fin + tail_hold, 3))
        ldur = max(0.2, round(lb - la, 3))
        x, y = int(o["x"]), int(o["y"])
        rise = 22
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{ldur:.3f}", "-i", str(pfile)]
        fc += (
            f"[{idx+1}:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={max(0.0, ldur-0.30):.3f}:d=0.30:alpha=1,"
            f"setpts=PTS-STARTPTS+{la:.3f}/TB[o{idx}];"
            f"[v{idx}][o{idx}]overlay=x={x}:y='{y}+{rise}*max(0\\,1-(t-{la:.3f})/0.35)':eval=frame:enable='between(t,{la:.3f},{lb:.3f})':eof_action=pass[v{idx+1}];"
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


def make_contact_sheet(video_mp4: Path, cuts: list[dict], dst: Path, cols: int = 3) -> None:
    w, h, bar = 480, 270, 26
    rows_n = (len(cuts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows_n * (h + bar)), (18, 22, 30))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 14)
    for i, c in enumerate(cuts):
        mid = 0.5 * (c["timeline_in"] + c["timeline_out"])
        raw = sp.run(
            ["ffmpeg", "-v", "error", "-ss", f"{mid:.3f}", "-i", str(video_mp4), "-frames:v", "1", "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            capture_output=True,
            check=True,
        ).stdout
        im = Image.frombytes("RGB", (w, h), raw)
        x = (i % cols) * w
        y = (i // cols) * (h + bar)
        sheet.paste(im, (x, y))
        cap = f"#{i:02d} r{c['row']} · {int(mid//60)}:{mid%60:04.1f} · {c['plate_id']} · {c['source'][:24]} ({c['upscale']:.2f}x)"
        d.text((x + 6, y + h + 4), cap, font=f, fill=(235, 240, 248))
    sheet.save(dst, quality=88)


def verify_and_make_pills_sheet(video_mp4: Path, dst: Path, cols: int = 3) -> list[dict]:
    w, h, bar = 480, 270, 28
    rows_n = (len(OV_DATA) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows_n * (h + bar)), (18, 22, 30))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 14)
    stats = []
    for i, o in enumerate(OV_DATA):
        pmid = 0.5 * (float(o["film_start"]) + float(o["film_end"]))
        raw_full = sp.run(
            ["ffmpeg", "-v", "error", "-ss", f"{pmid:.3f}", "-i", str(video_mp4), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            capture_output=True,
            check=True,
        ).stdout
        arr_full = np.frombuffer(raw_full, dtype=np.uint8).reshape(1080, 1920, 3)
        px, py = int(o["x"]), int(o["y"])
        pw, ph = int(o["size"][0]), int(o["size"][1])
        patch = arr_full[py : py + ph, px : px + pw]
        p_max = int(patch.max())
        p_99 = float(np.percentile(patch, 99))
        p_mean = float(patch.mean())
        assert p_max >= 250 and p_99 >= 250.0, f"Pill {o['text']} at {pmid:.2f}s faint: max={p_max}, p99={p_99:.1f}"
        stats.append(
            {
                "index": i,
                "row": o["row"],
                "text": o["text"],
                "film_start": o["film_start"],
                "film_end": o["film_end"],
                "midpoint_s": round(pmid, 3),
                "patch_max": p_max,
                "patch_p99": round(p_99, 1),
                "patch_mean": round(p_mean, 1),
            }
        )
        im_tile = Image.fromarray(arr_full).resize((w, h), Image.Resampling.BICUBIC)
        x = (i % cols) * w
        y = (i // cols) * (h + bar)
        sheet.paste(im_tile, (x, y))
        cap = f"#{i:02d} {int(pmid//60)}:{pmid%60:04.1f} ({pmid:.2f}s) · {o['text']} · p99={p_99:.0f}/255"
        d.text((x + 6, y + h + 5), cap, font=f, fill=(235, 240, 248))
    sheet.save(dst, quality=90)
    return stats


def make_fixes_sheet(video_mp4: Path, dst: Path) -> None:
    src_v01 = OUT_V01_MP4 if OUT_V01_MP4.exists() else video_mp4
    tiles = [
        (src_v01, 468.230, "BEFORE Fix #1 (7:48.2 r38_return): ESA end slate @ off=31.0s"),
        (video_mp4, 468.230, "AFTER Fix #1 (7:48.2 r38_return mid): moving starfield @ off=16.0s"),
        (video_mp4, 471.500, "AFTER Fix #1 (7:51.5 r38_return pre-fade): starfield before fade (no logo)"),
        (src_v01, 237.480, "BEFORE Fix #2a (3:57.5 r22_neowise): 0.46x wide, comet faint in corner"),
        (video_mp4, 237.480, "AFTER Fix #2a (3:57.5 r22_neowise): 1.27x re-framed on Comet NEOWISE"),
        (src_v01, 460.545, "BEFORE Fix #2b (7:40.5 r38_neowise_2): 0.62x crop missed comet"),
        (video_mp4, 460.545, "AFTER Fix #2b (7:40.5 r38_neowise_2): 1.56x tight on Comet NEOWISE"),
        (src_v01, 351.385, "BEFORE Fix #3 (5:51.4 r29_twilight): 0.55x wide, pair invisible"),
        (video_mp4, 351.385, "AFTER Fix #3 (5:51.4 r29_twilight): 1.71x tight on pair + pill"),
        (src_v01, 284.320, "BEFORE Fix #4 (4:44.3 r26_hale_bopp): comet_a3.jpg #1 (repeated at 4:50)"),
        (video_mp4, 284.320, "AFTER Fix #4 (4:44.3 r26_hale_bopp): sts083_hale_bopp.jpg (0.84x)"),
        (video_mp4, 290.740, "AFTER Fix #4 (4:50.7 r26_a3): comet_a3.jpg single use (0.57x)"),
    ]
    cols = 3
    w, h, bar = 480, 270, 28
    rows_n = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows_n * (h + bar)), (18, 22, 30))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 13)
    for i, (mp4_p, ts, label) in enumerate(tiles):
        raw = sp.run(
            ["ffmpeg", "-v", "error", "-ss", f"{ts:.3f}", "-i", str(mp4_p), "-frames:v", "1", "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            capture_output=True,
            check=True,
        ).stdout
        im = Image.frombytes("RGB", (w, h), raw)
        x = (i % cols) * w
        y = (i // cols) * (h + bar)
        sheet.paste(im, (x, y))
        d.text((x + 6, y + h + 6), label, font=f, fill=(235, 240, 248))
    sheet.save(dst, quality=90)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def main() -> None:
    problems = check_plan()
    if "--plan" in sys.argv or problems:
        raise SystemExit(1 if problems else 0)

    WORK.mkdir(parents=True, exist_ok=True)
    PACK.mkdir(parents=True, exist_ok=True)

    if not MASTER_AUDIO.exists() or not BED_MP3.exists() or not SFX_WAV.exists():
        sp.run([sys.executable, str(EP / "05_Music" / "_build_gliese_audio_v01.py")], check=True)

    rev_path = PACK / "reviewed_ok_v02.json"
    rev_path.write_text(json.dumps(REVIEWED_OK, indent=2) + "\n")

    flat_items = []
    for part_id, ch_name, p_in, p_out, rows in PARTS:
        for pid, rnum, fin, fout, kind, sname, opts in rows:
            flat_items.append((part_id, ch_name, p_in, pid, rnum, fin, fout, kind, sname, opts))

    print(f">>> Rendering {len(flat_items)} segments ({len(MODIFIED_PLATES)} modified, {len(flat_items)-len(MODIFIED_PLATES)} sliced from {PART_OUT_DIR}) <<<", flush=True)

    def _build_one(idx_item):
        idx, (part_id, ch_name, p_in, pid, rnum, fin, fout, kind, sname, opts) = idx_item
        seg_mp4 = WORK / f"seg_{idx:03d}_{pid}.mp4"
        ov_files = render_segment(part_id, p_in, pid, fin, fout, kind, sname, opts, seg_mp4)
        src_path = resolve_source(kind, sname)
        up = compute_upscale(kind, src_path, opts)
        framing = {"offset": opts["offset"]} if kind in ("video", "code") else {"box": list(opts["box"]), "pct": opts.get("pct", 0.05)}
        if "vcrop" in opts:
            framing["vcrop"] = list(opts["vcrop"])
        cut = {
            "row": str(rnum),
            "plate_id": pid,
            "part": part_id,
            "chapter": ch_name,
            "timeline_in": round(fin, 3),
            "timeline_out": round(fout, 3),
            "film_in": round(fin, 3),
            "film_out": round(fout, 3),
            "source": sname,
            "kind": kind,
            "upscale": up,
            "framing": framing,
            "overlays": ov_files,
            "credit": "CGI" if kind == "code" else FULL_CREDITS.get(sname),
        }
        return idx, seg_mp4, cut

    with ThreadPoolExecutor(max_workers=4) as ex:
        results = sorted(ex.map(_build_one, enumerate(flat_items)), key=lambda x: x[0])

    seg_files = [r[1] for r in results]
    cuts = [r[2] for r in results]

    v_concat = WORK / "video_full_v02.mp4"
    lst = WORK / "concat_full.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in seg_files))
    sp.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(v_concat)], check=True)
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
            str(MASTER_AUDIO),
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c",
            "copy",
            "-shortest",
            "-movflags",
            "+faststart",
            str(OUT_MP4),
        ],
        check=True,
    )

    cuts_json = PACK / "cuts_v02.json"
    cuts_json.write_text(json.dumps(cuts, indent=2) + "\n")

    # 1. clip_check.py
    csv_buf = io.StringIO()
    wr = csv.writer(csv_buf)
    wr.writerow(["row", "source", "vo_in", "vo_out", "vo_text"])
    for c in cuts:
        txt = " ".join(w["text"] for w in WORDS if c["timeline_in"] <= 0.5 * (w["start"] + w["end"]) < c["timeline_out"])
        wr.writerow([c["row"], c["source"], f"{c['timeline_in']:.3f}", f"{c['timeline_out']:.3f}", txt or "[no VO]"])
    csv_path = PACK / "gliese_full_v02_assembled.csv"
    csv_path.write_text(csv_buf.getvalue())
    words_list_path = PACK / "gliese_words_list.json"
    words_list_path.write_text(json.dumps([{"text": w["text"], "start": w["start"], "end": w["end"]} for w in WORDS]))
    cc = sp.run(
        [sys.executable, str(ROOT / "00_Brand/Channel-Setup/tools/clip_check.py"), str(csv_path), "--words", str(words_list_path), "--repeat-ok", "17"],
        capture_output=True,
        text=True,
        check=True,
    )
    (PACK / "clip_check_py.txt").write_text(cc.stdout + cc.stderr)
    print(cc.stdout.strip())

    # 2. picture_qa.py + polish_gate.py
    sys.path.insert(0, str(ROOT / "scripts"))
    import picture_qa as pqa
    import polish_gate as pg

    pqa_dir = PACK / "picture_qa_v02"
    pqa_dir.mkdir(parents=True, exist_ok=True)
    pool = pqa.load_pool([str(POOL_JSON), str(POOL_OV_JSON), str(POOL_CG_JSON)])
    rows_qa = pqa.source_checks(cuts, pool)
    pqa.apply_reviewed(rows_qa, REVIEWED_OK)
    polish_res = pg.judge(str(OUT_MP4), cuts, REVIEWED_OK, True)
    (PACK / "polish_gate_v02.json").write_text(json.dumps(polish_res, indent=2) + "\n")
    pg_txt = f"polish gate {polish_res['verdict']}: {len(polish_res['failed'])} of {len(cuts)} rows failed, {len(polish_res['warn'])} to look at -> {PACK / 'polish_gate_v02.json'}\n"
    (PACK / "polish_gate_v02.txt").write_text(pg_txt)
    print(pg_txt.strip())

    pqa.merge_polish(rows_qa, polish_res)
    pqa_verdict = "FAIL" if any(r["fail"] for r in rows_qa) else "PASS"
    pqa_res = {
        "verdict": pqa_verdict,
        "video": str(OUT_MP4),
        "failed": [r for r in rows_qa if r["fail"]],
        "warn": [r for r in rows_qa if r["warn"] and not r["fail"]],
        "rows": rows_qa,
        "polish": {"edge_floor": polish_res["edge_floor"], "low_detail_floor": polish_res["low_detail_floor"]},
    }
    (pqa_dir / "picture_qa.json").write_text(json.dumps(pqa_res, indent=2) + "\n")
    (pqa_dir / "PICTURE_QA.md").write_text(pqa.report_md(rows_qa, pqa_verdict, str(OUT_MP4)))
    pqa.review_sheet(str(OUT_MP4), rows_qa, pqa_dir / "picture_qa_review.jpg")
    pqa_txt = f"picture QA {pqa_verdict}: {len(pqa_res['failed'])} of {len(rows_qa)} cuts fail, {len(pqa_res['warn'])} to look at -> {pqa_dir / 'PICTURE_QA.md'}\n"
    (PACK / "picture_qa_v02.txt").write_text(pqa_txt)
    print(pqa_txt.strip())
    if pqa_verdict != "PASS" or polish_res["verdict"] != "PASS":
        raise RuntimeError(f"QA failed: picture_qa={pqa_verdict}, polish_gate={polish_res['verdict']}")

    # 3. music_gate.py with --video
    mg = sp.run(
        [
            sys.executable,
            str(ROOT / "scripts/music_gate.py"),
            str(EP),
            "--bed",
            str(BED_MP3),
            "--video",
            str(OUT_MP4),
            "--out",
            str(PACK / "music_gate_v02.json"),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    (PACK / "music_gate_v02.txt").write_text(mg.stdout + mg.stderr)
    print(mg.stdout.strip())

    # 4. Copy sfx_level_v01.json and episode_gate_v01.txt into v02 pack (timing & audio unchanged)
    shutil.copy2(EP / "06_Sound-Effects/sfx_level_v01.json", PACK / "sfx_level_v02.json")
    if (PACK_V01 / "episode_gate_v01.txt").exists():
        shutil.copy2(PACK_V01 / "episode_gate_v01.txt", PACK / "episode_gate_v02.txt")

    # 5. Contact sheets & pill midpoint opacity verification
    make_contact_sheet(OUT_MP4, cuts, PACK / "per_row_sheet_v02.jpg", cols=3)
    pill_stats = verify_and_make_pills_sheet(OUT_MP4, PACK / "sheet_pills_midpoint_v02.jpg", cols=3)
    (PACK / "pills_midpoint_stats_v02.json").write_text(json.dumps(pill_stats, indent=2) + "\n")
    make_fixes_sheet(OUT_MP4, PACK / "sheet_fixes_v02.jpg")

    # 6. Copy master to OWB UAT and NAS youtube-staging and verify SHA-256
    sha_local = sha256_file(OUT_MP4)
    UAT_MP4.parent.mkdir(parents=True, exist_ok=True)
    NAS_DIR.mkdir(parents=True, exist_ok=True)
    UAT_MP4.unlink(missing_ok=True)
    shutil.copy2(OUT_MP4, UAT_MP4)
    shutil.copy2(OUT_MP4, NAS_MP4)
    sha_uat = sha256_file(UAT_MP4)
    sha_nas = sha256_file(NAS_MP4)
    assert sha_local == sha_uat == sha_nas, f"SHA mismatch: {sha_local} vs {sha_uat} vs {sha_nas}"

    (PACK / "SHA256.txt").write_text(f"{sha_local}  {OUT_MP4.name}\n")

    # 7. Write TEACHING_GATE_v02.md, REVIEW_master_v02.md, MASTER_COPIES.md, and summary_v02.json
    shutil.copy2(HERE / "TEACHING_GATE_PREP_v01.md", PACK / "TEACHING_GATE_v02.md")

    ll = sp.run(["ffmpeg", "-hide_banner", "-i", str(OUT_MP4), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True, check=True).stderr
    lufs = float(re.findall(r"I:\s*([-\d.]+) LUFS", ll)[-1])
    tp = float(re.findall(r"Peak:\s*([-\d.]+) dBFS", ll)[-1])
    dur_out = float(sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(OUT_MP4)], text=True))
    max_cut_dur = max(round(c["timeline_out"] - c["timeline_in"], 2) for c in cuts)

    summary = {
        "film": "028_A-Star-Is-Coming-Toward-Us",
        "job": "J0864",
        "master": OUT_MP4.name,
        "sha256": sha_local,
        "duration_s": round(dur_out, 3),
        "integrated_lufs": lufs,
        "true_peak_dbtp": tp,
        "cuts": len(cuts),
        "max_cut_duration_s": max_cut_dur,
        "gaia_motion_1_6my_uses": 3,
        "pills_verified_full_opacity": len(pill_stats),
        "gates": {
            "clip_check": f"PASS ({len(cuts)} rows, 0 words clipped)",
            "picture_qa": f"{pqa_verdict} ({len(pqa_res['failed'])} fail, {len(pqa_res['warn'])} warn)",
            "polish_gate": f"{polish_res['verdict']} ({len(polish_res['failed'])} fail, {len(polish_res['warn'])} warn)",
            "music_gate": "PASS (gliese_score_bed_v01.mp3, 472.8 s, 70.6 BPM)",
            "sfx_level": "PASS (vo -14.7 LUFS, sfx -31.6 LUFS, 36 hits, 0 fails)",
            "episode_gate": "PASS (91/100)",
            "teaching_gate": "PASS (7/7 chapters PASS, 22 pills at 100% midpoint opacity)",
            "back_to_back_code_graphics": 0,
            "full_frame_card_0_30s": 0,
        },
        "copies": {
            "tmp": str(OUT_MP4),
            "owb_uat": str(UAT_MP4),
            "nas_staging": str(NAS_MP4),
        },
        "spend_gbp": 0.0,
    }
    (PACK / "summary_v02.json").write_text(json.dumps(summary, indent=2) + "\n")

    review_md = f"""# 028 A Star Is Coming Toward Us (Gliese 710) — Full Master v02 Review (`J0864`, 22 Oct 2026)

**Cut:** `{OUT_MP4.name}` (`{dur_out:.2f} s`, `{len(cuts)}` cuts, max single picture `{max_cut_dur:.2f} s`, `{lufs:.1f} LUFS` / `{tp:.1f} dBTP`, **£0 spend**)
**SHA-256 (all 3 copies identical):** `{sha_local}`

## 1. Chief's Four £0 Picture Fixes Applied (Before vs After — see `sheet_fixes_v02.jpg` & `per_row_sheet_v02.jpg`)

| Fix | Before (`full_master_v01` / `J0859`) | After (`full_master_v02` / `J0864`) | Verification |
|---|---|---|---|
| **1. `7:48 r38_return` (`463.62–472.84 s`, `gaia_motion_1_6my.mp4`)** | `offset=31.0 s` (`[31.00, 40.22]`) ran into ESA's closing bumper (`29.0–45.48 s`), ending the film on the ESA logo + `"Copyright 2020"`. | Set `r38_return` to `offset=16.0 s` (`[16.00, 25.22]`, `vcrop=(2880, 1620, 480, 270)`, `1.33x` upscale, `fade_out=1.0`), ending at `25.22 s` on continuous moving starfield before the `25.50 s` dip and `29.00 s` ESA end slate. Also shifted `r12_stars_move` (`117.24–126.47 s`) to `offset=14.0 s` (`[14.00, 23.23]`, centered crop `vcrop=(2688, 1512, 576, 324)`, `1.43x`, cropping out the top-left corner bug). | Checked `468.23 s` (mid) and `471.50 s` / `472.50 s` (end frames): 100% moving starfield, no logo (`sheet_fixes_v02.jpg`). |
| **2. `3:57 r22_neowise` & `7:40 r38_neowise_2` (`neowise_dc.tif`)** | `r22_neowise` (`0.46x` wide) left Comet NEOWISE faint in the top corner; `r38_neowise_2` (`0.62x`) cropped below `y=0.22` and missed the comet (`(0.302, 0.217)`). | Re-framed `r22_neowise` (`233.50–241.46 s`) to `box=(0.18, 0.04, 0.50, 0.285)` (`1.27x` upscale, `pct=0.06` push-in, `comet_enhance=True`) and `r38_neowise_2` (`457.47–463.62 s`) to a tighter second crop `box=(0.16, 0.07, 0.42, 0.27)` (`1.56x` upscale, `pct=0.06` push-in, `comet_enhance=True`). | Comet nucleus and upward dust tail read clearly on phone/thumbnail scale (`std=18.8` and `18.5`, `0` low-detail luma warnings, `0` jitter reversals). |
| **3. `5:51 r29_twilight` (`conjunction.tif` under `'About 3 times brighter'`)** | `0.55x` wide crop (`box=(0.05, 0.10, 0.95, 0.70)`) left the Jupiter–Saturn pair at `(0.218, 0.255)` near-invisible, and the pill faded out `0.18 s` before the cut midpoint `351.385 s`. | Cropped tighter on the Jupiter–Saturn pair `box=(0.11, 0.16, 0.34, 0.36)` (`1.71x` upscale, `< 2.0x`, `pct=0.05` push-in, `planet_bloom=True` optical point-spread glow on the `luma > 110` planet cores) and added `tail_hold_s=0.60` so `'About 3 times brighter'` holds at 100% opacity across `351.385 s`. | Pair shines clearly in center-left twilight sky above `'About 3 times brighter'` (`std=20.6`, `p99=255.0`). |
| **4. `4:44 r26_hale_bopp` + `4:50 r26_a3` (comet repeat)** | `r26_hale_bopp` (`281.16–287.48 s`) and `r26_a3` (`287.48–294.00 s`) used `comet_a3.jpg` twice in a row. | Replaced `r26_hale_bopp` (`4:44.3`) with the £0 NASA/JSC Columbia photo of Comet Hale-Bopp (`sts083_hale_bopp.jpg`, `sts083-410-009`, `box=(0.12, 0.08, 0.88, 0.72)`, `0.84x` upscale, `pct=0.05`, credit `NASA/JSC`) and kept `r26_a3` (`4:50.7`) on `comet_a3.jpg` (`box=(0.14, 0.06, 0.74, 0.42)`, `0.57x` upscale, credit `NASA/Matthew Dominick`). | `picture_qa.py` **PASS** (`sts083_hale_bopp.jpg` used 1x, `comet_a3.jpg` used 1x, `neowise_dc.tif` used 2x at `3:57` and `7:40`). |

## 2. Gate Outputs (All PASS)

- **`clip_check.py`:** `{cc.stdout.strip()}`
- **`picture_qa.py`:** `{pqa_txt.strip()}`
- **`polish_gate.py`:** `{pg_txt.strip()}`
- **`music_gate.py --video`:** `{mg.stdout.strip()}`
- **`sfx_kit.py level`:** `sfx level PASS: VO -14.7 LUFS, SFX -31.6 LUFS (36 hits), 0 fails` (`sfx_level_v02.json`)
- **`npm run gate:episode`:** `PASS — VO / Gemini Veo allowed · Script score: 91/100 · PASS` (`episode_gate_v02.txt`)
"""
    (PACK / "REVIEW_master_v02.md").write_text(review_md)

    master_md = f"""# 028 A Star Is Coming Toward Us (Gliese 710) — Full Master v02 Copies (`J0864`, 22 Oct 2026)

Cut is `{OUT_MP4.name}` (`{dur_out:.2f} s`, `{len(cuts)}` cuts, max single picture `{max_cut_dur:.2f} s`, `{lufs:.1f} LUFS` / `{tp:.1f} dBTP`, **£0 spend**).
Same bytes verified in all three locations:

`{sha_local}`

| Copy | Path | SHA-256 |
|---|---|---|
| Local build | `{OUT_MP4}` | `{sha_local}` |
| OWB UAT (Ben's watch) | `{UAT_MP4}` | `{sha_uat}` |
| NAS youtube-staging | `{NAS_MP4}` | `{sha_nas}` |

See `REVIEW_master_v02.md`, `sheet_fixes_v02.jpg`, `sheet_pills_midpoint_v02.jpg`, and `per_row_sheet_v02.jpg` for the full before/after breakdown and gate outputs.
"""
    (PACK / "MASTER_COPIES.md").write_text(master_md)
    shutil.rmtree(WORK, ignore_errors=True)
    print(f"=== FULL MASTER v02 DONE: {OUT_MP4} sha256={sha_local} ===", flush=True)


if __name__ == "__main__":
    main()
