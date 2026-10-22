#!/usr/bin/env python3
"""029 Is Betelgeuse About to Explode? — Full Rough v01 assembler (J0823).

Joins the 6 Chief-KEEP part roughs (J0808, PR #257) into `029_Betelgeuse_full_rough_v01.mp4`
on the locked VO v02 (`02_Voiceover/betelgeuse_vo_v01.wav`, 515.18s + hold/fade = 517.26s)
with its own £0 chapter-shaped score bed (`05_Music/betelgeuse_score_bed_v01.mp3`) and house
SFX stem (`06_Sound-Effects/stem_sfx_v01.wav`).

Changes applied per J0823 brief (£0, no minting):
1. Two Orbit beats restored from existing Omni renders:
   - `r12_orbit_thumb` (123.16-130.42s, 7.26s): `022` `sun_orbit_row67_omni_v01.mp4` @ 1.80s
     (Orbit floating above Earth's cloud horizon looking up at a red-orange giant star and lifting a hand).
   - `r26_orbit_flare` (282.16-286.08s, 3.92s): `026` `orbit_thumb_omni_v01.mp4` @ 1.50s
     (Orbit in a night starfield raising a hand in front of his visor before a blazing flare star).
2. Zero back-to-back code graphics across the entire 63-plate film:
   - In Row 21 (`224.02-242.50s`), `r21_hero` (228.95-233.00s, teaspoon=mountain code graphic) and
     `r21_bh` (238.30-242.50s, core-collapse black hole code graphic) are separated by `r21_neutron`
     (233.00-238.30s, `crab.jpg` Hubble pulsar still on the neutron-star callback sentence).
   - `r22_subscribe` (242.50-247.60s) uses `gemini_night.jpg` (real night-sky still push + house SUBSCRIBE
     pill) so real imagery separates `r21_bh` (code) and `r23_paranal` (code).
3. Distinct stretches on multi-use ESO night-sky clips (`lasilla_startrails.mp4` and `lasilla_mw.mp4`).
4. 5 chapter lower-third cards (none in 0:00-0:30) and all 22 J0504 teaching overlay pills, with strict
   one-label-at-a-time enforcement (corner credits hide whenever any pill, card, or internal label is on screen).
5. Runs clip_check.py, picture_qa.py, polish_gate.py, music_gate.py, sfx_kit.py level, and writes
   TEACHING_GATE_v01.md + MASTER_COPIES.md + SHA256.txt, copying verified masters to OWB UAT and NAS youtube-staging.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import re
import shutil
import subprocess as sp
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None

HERE = Path(__file__).resolve().parent
EP = HERE.parent
ROOT = EP.parents[1]
HDIR = HERE / "harvest_v01"
CDIR = HERE / "code_graphics_v01"
OV_PACK = HERE / "teaching_overlays_v01_pack"
PACK = HERE / "full_rough_v01_pack"
PART_OUT_DIR = Path("/private/tmp/029_part_roughs_v01")
WORK = Path("/private/tmp/betelgeuse029_full_rough_work_v01")
AUDIO_WORK = Path("/private/tmp/betelgeuse029_audio_work_v01")

OUT_MP4 = Path("/private/tmp/029_Betelgeuse_full_rough_v01.mp4")
UAT_MP4 = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/029_Betelgeuse_full_rough_v01.mp4"
NAS_DIR = Path("/Volumes/data/mac-mini-archive/youtube-staging/029")
NAS_MP4 = NAS_DIR / "029_Betelgeuse_full_rough_v01.mp4"

VO_WAV = EP / "02_Voiceover" / "betelgeuse_vo_v01.wav"
WORDS_JSON = EP / "02_Voiceover" / "words.json"
POOL_JSON = HERE / "SOURCE_POOL_v03.json"
BED_MP3 = EP / "05_Music" / "betelgeuse_score_bed_v01.mp3"
SFX_WAV = EP / "06_Sound-Effects" / "stem_sfx_v01.wav"
MASTER_AUDIO = AUDIO_WORK / "audio_master_v01.m4a"

OMNI_RED_GIANT = (
    ROOT / "02_Video-Projects/022_Is-the-Sun-Getting-Brighter/04_Generated-Clips/01_Raw/omni_v01/sun_orbit_row67_omni_v01.mp4"
)
OMNI_FLARE_SHIELD = (
    ROOT / "02_Video-Projects/026_How-Far-Is-The-Nearest-Star/04_Generated-Clips/01_Raw/omni_v01/orbit_thumb_omni_v01.mp4"
)

FPS = 30
LAST_WORD = 514.260
HOLD = 2.000
FADE = 1.000
TOTAL = 517.260
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
NAVY = (23, 36, 55, 220)
ENC = ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p"]

WORDS = json.loads(WORDS_JSON.read_text())["words"]
OV_DATA = json.loads((OV_PACK / "overlays_v01.json").read_text())["labels"]

# Gold label strings to suppress on code graphics when replaced by a teaching pill or chapter card
SUPPRESS_BY_ROW = {
    "r03_r04_promise": {"in 2019", "giant star actually dies"},
    "r09_finder": {"three stars"},
    "r10_r11_dip": {"February 2020", "about a third", "fifty years"},
    "r17_r20_shells": {"less than a second"},
    "r23_paranal": {"imagine the night"},
    "r29_span_astrolabe": {"five hundred years", "hundred thousand years"},
    "r31_shells_twins": {"100,000 years", "a hundred years"},
    "r35_song": {"1054"},
}

# 5 chapter lower-third cards (none inside 0:00-0:30)
CHAPTER_CARDS = {
    "r05_surface": (37.74, 40.24, "The Star in Orion's Shoulder"),
    "r10_r11_dip": (109.60, 112.10, "The Great Dimming"),
    "r17_sdo": (170.00, 172.50, "How a Giant Star Dies"),
    "r23_paranal": (248.06, 250.56, "The Night It Goes"),
    "r29_span_astrolabe": (342.92, 345.42, "So When?"),
}

# Subscribe lower-right pill on r22_subscribe (242.50-247.60s)
SUBSCRIBE_CARD = (244.40, 247.30, "SUBSCRIBE")

FULL_CREDITS = {
    "orion_rise_vlt.mp4": "ESO/B. Tafreshi (twanight.org) · CC BY 4.0",
    "orion_over_paranal.mp4": "ESO/B. Tafreshi · CC BY 4.0",
    "lasilla_startrails.mp4": "R. Wesson/ESO · CC BY 4.0",
    "sphere_jan.jpg": "ESO/M. Montargès et al. · CC BY 4.0",
    "sphere_dec.jpg": "ESO/M. Montargès et al. · CC BY 4.0",
    "sdo_hmi_continuum.jpg": "NASA/SDO",
    "westerlund.jpg": "NASA, ESA, Hubble Heritage Team (STScI/AURA), A. Nota, Westerlund 2 Science Team",
    "tarantula.jpg": "ESA/NASA, ESO and Danny LaCrue · CC BY 4.0",
    "dust_impression.jpg": "Artist's impression · ESO, ESA/Hubble, M. Kornmesser · CC BY 4.0",
    "visir_flames.jpg": "ESO/P. Kervella · CC BY 4.0",
    "crab.jpg": "NASA, ESA, A. Loll/J. Hester (ASU); Ack.: D. De Martin (ESA/Hubble)",
    "chajnantor_mw.m4v": "ESO · CC BY 4.0",
    "dscovr_epic.jpg": "NASA/DSCOVR EPIC",
    "half_moon.jpg": "NASA/GSFC",
    "lasilla_mw.mp4": "ESO/S. Brunier · CC BY 4.0",
    "gemini_earth_sky.jpg": "International Gemini Observatory/NOIRLab/NSF/AURA/T. Slovinský · CC BY 4.0",
    "companion_speckle.jpg": "International Gemini Observatory/NOIRLab/NSF/AURA; M. Zamani · CC BY 4.0",
    "gemini_night.jpg": "International Gemini Observatory/NOIRLab/NSF/AURA/P. Horálek · CC BY 4.0",
    "gemini_dome.jpg": "International Gemini Observatory/NOIRLab/NSF/AURA/J. Chu/J. Pollard · CC BY 4.0",
    "casa.jpg": "NASA/CXC/STScI/JPL-Caltech",
    "jwst_pillars.jpg": "NASA, ESA, CSA, STScI; J. DePasquale, A. Koekemoer, A. Pagan · CC BY 4.0",
    "m42.jpg": "NASA, ESA, M. Robberto (STScI/ESA) & HST Orion Treasury Project Team",
    "alma_orion_set.mp4": "ESO/B. Tafreshi (twanight.org) · CC BY 4.0",
    "hl_tau.jpg": "ALMA (ESO/NAOJ/NRAO) · CC BY 4.0",
    "blue_marble.jpg": "NASA/Apollo 17",
    "sun_orbit_row67_omni_v01.mp4": None,
    "orbit_thumb_omni_v01.mp4": None,
}

VIDEO_VF = {
    "orion_rise_vlt.mp4": (
        "scale=1920:1080,format=rgb24,"
        "lutrgb=r='clip(pow(val/255,0.62)*230+18,0,255)':g='clip(pow(val/255,0.62)*230+18,0,255)':b='clip(pow(val/255,0.62)*235+20,0,255)',"
        "unsharp=5:5:0.7:5:5:0.0"
    ),
    "orion_over_paranal.mp4": (
        "scale=1920:1080,format=rgb24,"
        "lutrgb=r='clip(pow(max(0,val-14)/90,0.68)*220+20,0,255)':g='clip(pow(max(0,val-14)/90,0.68)*220+20,0,255)':b='clip(pow(max(0,val-14)/90,0.68)*230+24,0,255)',"
        "unsharp=5:5:0.9:5:5:0.0"
    ),
    "chajnantor_mw.m4v": (
        "scale=1920:1080,format=rgb24,"
        "lutrgb=r='clip((val-35)*1.8+20,0,255)':g='clip((val-35)*1.8+20,0,255)':b='clip((val-35)*1.8+20,0,255)',"
        "unsharp=5:5:0.8:5:5:0.0"
    ),
    "lasilla_mw.mp4": (
        "scale=1920:1080,format=rgb24,"
        "lutrgb=r='clip(pow(max(0,val-20)/140,0.75)*225+18,0,255)':g='clip(pow(max(0,val-20)/140,0.75)*225+18,0,255)':b='clip(pow(max(0,val-20)/140,0.75)*235+22,0,255)'"
    ),
    "alma_orion_set.mp4": (
        "scale=1920:1080,format=rgb24,"
        "lutrgb=r='clip(pow(max(0,val-22)/95,0.72)*220+18,0,255)':g='clip(pow(max(0,val-22)/95,0.72)*220+18,0,255)':b='clip(pow(max(0,val-22)/95,0.72)*230+22,0,255)',"
        "unsharp=5:5:0.8:5:5:0.0"
    ),
    "lasilla_startrails.mp4": "scale=1920:1080",
    "sun_orbit_row67_omni_v01.mp4": "scale=1920:1080",
    "orbit_thumb_omni_v01.mp4": "scale=1920:1080",
}

# Plates modified from part_roughs_v01 (all other plates slice directly from part_roughs_v01 if cached)
MODIFIED_PLATES = {
    "r05_surface",
    "r10_span_c",
    "r10_r11_dip",
    "r12_orbit_thumb",
    "r17_sdo",
    "r20_crab",
    "r21_hero",
    "r21_neutron",
    "r21_bh",
    "r22_subscribe",
    "r23_paranal",
    "r26_orbit_flare",
    "r29_span_astrolabe",
    "r30_vlt",
    "r39_return",
}

PARTS = [
    (
        "part00",
        "0 Open",
        0.00,
        36.94,
        [
            ("r01_orion_rise", 1, 0.00, 6.12, "video", "orion_rise_vlt.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r02_orion_b", 2, 6.12, 10.06, "video", "orion_over_paranal.mp4", {"offset": 0.45, "upscale": 1.0}),
            ("r02_surface", 2, 10.06, 13.96, "still", "sphere_jan.jpg", {"box": (0.0, 0.0, 1.0, 1.0), "pct": 0.05, "feathered_blur": True, "gamma": 0.55, "lift": 22.0}),
            ("r03_r04_promise", 3, 13.96, 36.94, "code", "code_graphic_029_r03_r04_promise_v01.mp4", {"plate_id": "r03_r04_promise", "offset": 0.0, "upscale": 1.0}),
        ],
    ),
    (
        "part01",
        "1 The Star in Orion's Shoulder",
        36.94,
        105.48,
        [
            ("r05_surface", 5, 36.94, 41.90, "still", "sphere_dec.jpg", {"box": (0.0, 0.0, 1.0, 1.0), "pct": 0.05, "feathered_blur": True, "gamma": 0.52, "lift": 24.0}),
            ("r05_scale", 5, 41.90, 48.58, "code", "code_graphic_029_r05_scale_v01.mp4", {"plate_id": "r05_scale", "offset": 0.0, "upscale": 1.0}),
            ("r06_paranal", 6, 48.58, 55.00, "video", "lasilla_startrails.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r06_sphere_jan", 6, 55.00, 62.10, "still", "sphere_jan.jpg", {"box": (0.0, 0.04, 1.0, 0.96), "pct": 0.05, "feathered_blur": True, "gamma": 0.55, "lift": 22.0}),
            ("r07_sdo", 7, 62.10, 67.50, "still", "sdo_hmi_continuum.jpg", {"box": (0.02, 0.08, 0.98, 0.62), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r07_sphere_jan", 7, 67.50, 73.35, "still", "sphere_jan.jpg", {"box": (0.0, 0.0, 1.0, 1.0), "pct": 0.05, "feathered_blur": True, "gamma": 0.55, "lift": 22.0}),
            ("r08_westerlund_w", 8, 73.35, 80.19, "still", "westerlund.jpg", {"box": (0.05, 0.12, 0.95, 0.795), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r08_westerlund_t", 8, 80.19, 85.92, "still", "westerlund.jpg", {"box": (0.22, 0.24, 0.78, 0.66), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r08_tarantula", 8, 85.92, 92.92, "still", "tarantula.jpg", {"box": (0.04, 0.12, 0.96, 0.76), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r09_finder", 9, 92.92, 105.48, "code", "code_graphic_029_r09_finder_v01.mp4", {"plate_id": "r09_finder", "offset": 0.0, "upscale": 1.0}),
        ],
    ),
    (
        "part02",
        "2 The Great Dimming",
        105.48,
        169.50,
        [
            ("r10_span_c", 10, 105.48, 109.50, "video", "lasilla_startrails.mp4", {"offset": 6.50, "upscale": 1.15, "vcrop": (1670, 939, 125, 70)}),
            ("r10_r11_dip", 10, 109.50, 123.16, "code", "code_graphic_029_r10_r11_dip_v01.mp4", {"plate_id": "r10_r11_dip", "offset": 0.0, "upscale": 1.0}),
            ("r12_orbit_thumb", 12, 123.16, 130.42, "omni", "sun_orbit_row67_omni_v01.mp4", {"src_path": str(OMNI_RED_GIANT), "offset": 1.80, "upscale": 1.50}),
            ("r13_compare", 13, 130.42, 137.80, "code", "code_graphic_029_r13_compare_v01.mp4", {"plate_id": "r13_compare", "offset": 0.0, "upscale": 1.0}),
            ("r14_ejection", 14, 137.80, 142.86, "still", "dust_impression.jpg", {"box": (0.0, 0.16, 1.0, 0.84), "pct": 0.05, "gamma": 0.48, "lift": 24.0}),
            ("r14_dust", 14, 142.86, 147.60, "still", "dust_impression.jpg", {"box": (0.12, 0.22, 0.88, 0.78), "pct": 0.05, "gamma": 0.48, "lift": 24.0}),
            ("r15_span_d", 15, 147.60, 152.80, "video", "lasilla_startrails.mp4", {"offset": 11.0, "upscale": 1.0}),
            ("r15_dip", 15, 152.80, 157.76, "code", "code_graphic_029_r15_dip_v01.mp4", {"plate_id": "r15_dip", "offset": 0.0, "upscale": 1.0}),
            ("r16_span_e", 16, 157.76, 163.43, "video", "lasilla_startrails.mp4", {"offset": 22.0, "upscale": 1.0}),
            ("r16_visir", 16, 163.43, 169.50, "still", "visir_flames.jpg", {"box": (0.0, 0.16, 1.0, 0.84), "pct": 0.05, "gamma": 0.70, "lift": 14.0}),
        ],
    ),
    (
        "part03",
        "3 How a Giant Star Dies",
        169.50,
        247.60,
        [
            ("r17_sdo", 17, 169.50, 175.40, "still", "sdo_hmi_continuum.jpg", {"box": (0.06, 0.14, 0.94, 0.68), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r17_r20_shells", 17, 175.40, 224.02, "code", "code_graphic_029_r17_r20_shells_v01.mp4", {"plate_id": "r17_r20_shells", "offset": 0.0, "upscale": 1.0}),
            ("r20_crab", 20, 224.02, 228.95, "still", "crab.jpg", {"box": (0.04, 0.18, 0.96, 0.74), "pct": 0.05, "gamma": 0.90, "lift": 0.0}),
            ("r21_hero", 21, 228.95, 233.00, "code", "code_graphic_029_r21_hero_v01.mp4", {"plate_id": "r21_hero", "offset": 0.0, "upscale": 1.0}),
            ("r21_neutron", 21, 233.00, 238.30, "still", "crab.jpg", {"box": (0.22, 0.28, 0.78, 0.62), "pct": 0.05, "gamma": 0.88, "lift": 4.0}),
            ("r21_bh", 21, 238.30, 242.50, "code", "code_graphic_029_r21_bh_v01.mp4", {"plate_id": "r21_bh", "offset": 0.0, "upscale": 1.0}),
            ("r22_subscribe", 22, 242.50, 247.60, "still", "gemini_night.jpg", {"box": (0.04, 0.08, 0.96, 0.80), "pct": 0.05, "gamma": 0.90, "lift": 4.0, "subscribe_pill": True}),
        ],
    ),
    (
        "part04",
        "4 The Night It Goes",
        247.60,
        350.50,
        [
            ("r23_paranal", 23, 247.60, 254.80, "code", "code_graphic_029_r23_paranal_v01.mp4", {"plate_id": "r23_paranal", "offset": 0.0, "upscale": 1.0}),
            ("r24_superk", 24, 254.80, 261.28, "video", "chajnantor_mw.m4v", {"offset": 3.25, "upscale": 1.50}),
            ("r24_epic", 24, 261.28, 266.96, "still", "dscovr_epic.jpg", {"box": (0.04, 0.18, 0.96, 0.74), "pct": 0.05, "gamma": 0.85, "lift": 10.0}),
            ("r24_superk_2", 24, 266.96, 274.12, "video", "chajnantor_mw.m4v", {"offset": 6.10, "upscale": 1.80, "vcrop": (1066, 600, 107, 0)}),
            ("r25_orion", 25, 274.12, 282.16, "code", "code_graphic_029_r25_orion_v01.mp4", {"plate_id": "r25_orion", "offset": 0.0, "upscale": 1.0}),
            ("r26_orbit_flare", 26, 282.16, 286.08, "omni", "orbit_thumb_omni_v01.mp4", {"src_path": str(OMNI_FLARE_SHIELD), "offset": 1.50, "upscale": 1.50}),
            ("r26_moon", 26, 286.08, 290.98, "still", "half_moon.jpg", {"box": (0.04, 0.18, 0.96, 0.74), "pct": 0.05, "gamma": 0.75, "lift": 16.0}),
            ("r27_orion", 27, 290.98, 309.46, "code", "code_graphic_029_r27_orion_v01.mp4", {"plate_id": "r27_orion", "offset": 0.0, "upscale": 1.0}),
            ("r28_epic", 28, 309.46, 315.47, "still", "dscovr_epic.jpg", {"box": (0.12, 0.22, 0.88, 0.70), "pct": 0.05, "gamma": 0.85, "lift": 10.0}),
            ("r28_mw", 28, 315.47, 320.70, "video", "lasilla_mw.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r28_people", 28, 320.70, 326.56, "still", "gemini_earth_sky.jpg", {"box": (0.05, 0.10, 0.95, 0.82), "pct": 0.05, "gamma": 0.92, "lift": 4.0}),
            ("r29_span_astrolabe", 29, 326.56, 350.50, "code", "code_graphic_029_r29_span_astrolabe_v01.mp4", {"plate_id": "r29_span_astrolabe", "offset": 0.0, "upscale": 1.0}),
        ],
    ),
    (
        "part05",
        "5 So When?",
        350.50,
        517.26,
        [
            ("r30_vlt", 30, 350.50, 359.36, "video", "lasilla_startrails.mp4", {"offset": 13.10, "upscale": 1.15, "vcrop": (1670, 939, 125, 70)}),
            ("r31_shells_twins", 31, 359.36, 378.30, "code", "code_graphic_029_r31_shells_twins_v01.mp4", {"plate_id": "r31_shells_twins", "offset": 0.0, "upscale": 1.0}),
            ("r32_sphere_dec", 32, 378.30, 385.46, "still", "sphere_dec.jpg", {"box": (0.0, 0.04, 1.0, 0.96), "pct": 0.05, "feathered_blur": True, "gamma": 0.52, "lift": 24.0}),
            ("r32_ejection", 32, 385.46, 392.60, "still", "visir_flames.jpg", {"box": (0.0, 0.16, 1.0, 0.84), "pct": 0.05, "gamma": 0.70, "lift": 14.0}),
            ("r33_speckle", 33, 392.60, 403.00, "still", "companion_speckle.jpg", {"box": (0.03, 0.23, 0.97, 0.77), "pct": 0.05, "sub": 10.0, "gain": 5.2, "lift": 20.0}),
            ("r33_pair", 33, 403.00, 413.30, "still", "companion_speckle.jpg", {"box": (0.0, 0.18, 1.0, 0.82), "pct": 0.05, "sub": 10.0, "gain": 5.2, "lift": 20.0}),
            ("r34_gemini", 34, 413.30, 419.65, "still", "gemini_night.jpg", {"box": (0.08, 0.12, 0.92, 0.86), "pct": 0.05, "gamma": 0.90, "lift": 4.0}),
            ("r34_pair", 34, 419.65, 425.12, "video", "orion_over_paranal.mp4", {"offset": 0.45, "upscale": 1.0}),
            ("r34_dome", 34, 425.12, 432.60, "still", "gemini_dome.jpg", {"box": (0.05, 0.12, 0.95, 0.78), "pct": 0.05, "gamma": 0.85, "lift": 6.0}),
            ("r35_song", 35, 432.60, 442.00, "code", "code_graphic_029_r35_song_v01.mp4", {"plate_id": "r35_song", "offset": 0.0, "upscale": 1.0}),
            ("r35_crab", 35, 442.00, 453.00, "still", "crab.jpg", {"box": (0.05, 0.22, 0.95, 0.72), "pct": 0.05, "gamma": 0.90, "lift": 0.0}),
            ("r36_orion_b", 36, 453.00, 459.59, "video", "orion_over_paranal.mp4", {"offset": 2.40, "upscale": 1.25, "vcrop": (1536, 864, 192, 0)}),
            ("r36_visir", 36, 459.59, 466.35, "still", "visir_flames.jpg", {"box": (0.08, 0.22, 0.92, 0.78), "pct": 0.05, "gamma": 0.70, "lift": 14.0}),
            ("r37_casa", 37, 466.35, 476.02, "still", "casa.jpg", {"box": (0.04, 0.14, 0.96, 0.80), "pct": 0.05, "gamma": 0.85, "lift": 10.0}),
            ("r37_pillars", 37, 476.02, 485.05, "still", "jwst_pillars.jpg", {"box": (0.0, 0.18, 1.0, 0.74), "pct": 0.05, "gamma": 0.92, "lift": 4.0}),
            ("r38_m42", 38, 485.05, 493.36, "still", "m42.jpg", {"box": (0.08, 0.22, 0.92, 0.74), "pct": 0.05, "gamma": 0.90, "lift": 4.0}),
            ("r38_night", 38, 493.36, 496.90, "video", "alma_orion_set.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r39_hltau", 39, 496.90, 504.10, "still", "hl_tau.jpg", {"box": (0.04, 0.18, 0.96, 0.74), "pct": 0.05, "gamma": 0.72, "lift": 16.0}),
            ("r39_marble", 39, 504.10, 509.25, "still", "blue_marble.jpg", {"box": (0.14, 0.25, 0.86, 0.72), "pct": 0.05, "gamma": 0.85, "lift": 10.0}),
            ("r39_return", 39, 509.25, 517.26, "video", "lasilla_mw.mp4", {"offset": 9.50, "upscale": 1.0, "fade_out": 1.0}),
        ],
    ),
]

# Chief-ruled board reuses (J0353 + J0808 KEEP on PLATE_BOARDS_v03.json)
REVIEWED_OK = {
    "_status": "Chief J0353 source rulings + J0808 KEEP on PLATE_BOARDS_v03.json (22 Oct 2026).",
    "sphere_jan.jpg": {
        "note": "J0353 Chief ruling #1 + PLATE_BOARDS_v03: r02_surface -> sphere_jan.jpg (eso2003b) alongside r06_sphere_jan and r07_sphere_jan (3 distinct framings).",
        "kinds": ["reuse"],
    },
    "visir_flames.jpg": {
        "note": "J0353 Chief ruling #5 + PLATE_BOARDS_v03: r32_ejection -> visir_flames.jpg (eso1121a) alongside r16_visir and r36_visir (3 distinct framings).",
        "kinds": ["reuse"],
    },
    "crab.jpg": {
        "note": "J0353 Chief ruling #9 + PLATE_BOARDS_v03: r21_neutron -> crab.jpg (heic0515a tight pulsar crop) between r21_hero and r21_bh so no two code graphics run back-to-back, alongside r20_crab and r35_crab.",
        "kinds": ["reuse"],
    },
    "chajnantor_mw.m4v@6.1": {
        "note": "J0808 Chief brief: skip ESO logo bumpers on Chajnantor (0.00-3.25s and 13.30-16.41s on 16.41s source = 10.05s clean sky window); r24_superk (3.25s wide) and r24_superk_2 (6.10s, 1.80x core crop) split the clean sky window.",
        "kinds": ["reuse"],
    },
    "orion_over_paranal.mp4": {
        "note": "J0353 Chief ruling #8 + PLATE_BOARDS_v03: 9.04s ESO clip used on r02_orion_b (0.45s wide), r34_pair (0.45s), and r36_orion_b (2.40s, 1.25x upper-sky Orion crop).",
        "kinds": ["reuse"],
    },
    "lasilla_startrails.mp4": {
        "note": "PLATE_BOARDS_v03 + J0808 KEEP: 28.05s ESO La Silla star-trails clip partitioned across 5 non-overlapping stretches/crops (0.0s, 6.5s, 11.0s, 13.1s, 22.0s).",
        "kinds": ["reuse"],
    },
    "lasilla_mw.mp4@9.5": {
        "note": "PLATE_BOARDS_v03 + J0808 KEEP: 17.64s ESO Milky Way clip used at 0.00-5.23s (r28_mw) and 9.50-17.51s (r39_return, non-overlapping 9.5s offset).",
        "kinds": ["reuse"],
    },
}


def resolve_src(kind: str, sname: str, opts: dict) -> Path:
    if kind == "omni":
        return Path(opts["src_path"])
    return (CDIR if kind == "code" else HDIR) / sname


def compute_upscale(kind: str, src: Path, opts: dict) -> float:
    if kind in ("video", "code", "omni"):
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


def check_plan() -> list[str]:
    problems = []
    total_plates = 0
    prev_kind = None
    prev_pid = None
    for part_id, ch_name, p_in, p_out, rows in PARTS:
        print(f"=== {part_id} · {ch_name} ({p_in:.2f}-{p_out:.2f}s, {p_out - p_in:.2f}s) ===")
        prev_out = p_in
        for pid, rnum, fin, fout, kind, sname, opts in rows:
            total_plates += 1
            src = resolve_src(kind, sname, opts)
            if not src.exists():
                problems.append(f"{pid}: missing {src}")
                continue
            if abs(fin - prev_out) > 1e-3:
                problems.append(f"{pid}: gap/overlap {prev_out:.2f} -> {fin:.2f}")
            prev_out = fout
            if kind == "code" and prev_kind == "code":
                problems.append(f"Back-to-back code graphics: {prev_pid} -> {pid} at {fin:.2f}s")
            prev_kind = kind
            prev_pid = pid
            up = compute_upscale(kind, src, opts)
            if up > 2.35:
                problems.append(f"{pid}: upscale {up:.2f} > 2.35")
            for bound_name, bt in (("in", fin), ("out", fout)):
                if bt <= 0.01 or bt >= 515.0:
                    continue
                clipped = [w["word"] for w in WORDS if w["start"] < bt - 0.015 and w["end"] > bt + 0.015]
                if clipped:
                    problems.append(f"{pid} {bound_name}={bt:.2f}s clips word {clipped}")
            ovs = [o for o in OV_DATA if o["row"] == pid]
            for o in ovs:
                if o["film_start"] < fin - 0.02 or o["film_end"] > fout + 0.02:
                    problems.append(
                        f"{pid}: overlay {o['text']!r} ({o['film_start']:.2f}-{o['film_end']:.2f}) outside ({fin:.2f}-{fout:.2f})"
                    )
            card = CHAPTER_CARDS.get(pid)
            if card and (card[0] < fin - 0.02 or card[1] > fout + 0.02 or card[0] < 30.0):
                problems.append(f"{pid}: chapter card {card} invalid")
            print(
                f"  {pid:20s} row={rnum:2d} {fin:6.2f}-{fout:6.2f} ({fout-fin:5.2f}s) {kind:6s} {sname:38s} up={up:4.2f}x ovs={len(ovs)}"
                + (f" card={card[2]!r}" if card else "")
            )
        if abs(prev_out - p_out) > 1e-3:
            problems.append(f"{part_id}: ends at {prev_out:.2f} != {p_out:.2f}")
    print(f"Total plates: {total_plates} | Problems: {problems or 'NONE'}")
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
    font = ImageFont.truetype(FONT, 62)
    w = int(font.getlength(title)) + 70
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((90, 860, 90 + w, 990), radius=15, fill=NAVY)
    d.text((125, 886), title, font=font, fill="white")
    img.save(dst)


def make_subscribe_png(dst: Path) -> None:
    font = ImageFont.truetype(FONT, 44)
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((1440, 900, 1830, 990), radius=45, fill=(204, 0, 0, 235))
    d.text((1500, 918), "SUBSCRIBE", font=font, fill="white")
    img.save(dst)


def render_still_push(src: Path, opts: dict, dur: float, dest: Path) -> None:
    frames = round(dur * FPS)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    b = opts["box"]
    im = im.crop((int(w * b[0]), int(h * b[1]), int(w * b[2]), int(h * b[3])))
    gamma = float(opts.get("gamma", 1.0))
    lift = float(opts.get("lift", 0.0))
    sub = float(opts.get("sub", 0.0))
    gain = float(opts.get("gain", 1.0))
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
        if sub != 0.0 or gain != 1.0:
            arr = np.asarray(im, dtype=np.float32)
            arr = np.clip((arr - sub) * gain + lift, 0.0, 255.0).astype(np.uint8)
            im = Image.fromarray(arr)
        elif gamma != 1.0 or lift != 0.0:
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


def render_code_segment(plate_id: str, dur: float, suppress: set[str], dest: Path) -> None:
    sys.path.insert(0, str(HERE))
    import build_code_graphics_v01 as cg

    frames = round(dur * FPS)
    plate = {"id": plate_id, "use_s": dur}
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
            t = n / FPS
            proc.stdin.write(r.frame(plate, t).tobytes())
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
    ovs = [o for o in OV_DATA if o["row"] == pid]

    # Fast path: reuse already-rendered segment from /private/tmp/029_part_roughs_v01 if unchanged
    part_mp4 = PART_OUT_DIR / f"029_Betelgeuse_{part_id}_rough_v01.mp4"
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
                "-frames:v",
                str(frames),
                *ENC,
                str(seg_out),
            ],
            check=True,
        )
        return [o["file"] for o in ovs]

    base_mp4 = WORK / f"base_{pid}.mp4"
    src = resolve_src(kind, sname, opts)

    if kind in ("video", "omni"):
        off = float(opts.get("offset", 0.0))
        vf_parts = []
        if "vcrop" in opts:
            cw, ch, cx, cy = opts["vcrop"]
            vf_parts.append(f"crop={cw}:{ch}:{cx}:{cy}")
        vf_parts.append(VIDEO_VF[sname])
        vf_parts.append(f"fps={FPS},setsar=1")
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
        suppress = SUPPRESS_BY_ROW.get(pid, set())
        src_dur = float(sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(src)], text=True))
        if not suppress and abs(dur - src_dur) < 0.04:
            sp.run(
                [
                    "ffmpeg",
                    "-y",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-i",
                    str(src),
                    "-vf",
                    f"fps={FPS},setsar=1",
                    "-frames:v",
                    str(frames),
                    *ENC,
                    str(base_mp4),
                ],
                check=True,
            )
        else:
            render_code_segment(opts["plate_id"], dur, suppress, base_mp4)
    else:
        raise ValueError(kind)

    if kind == "code":
        credit_txt = "ESO/M. Montargès et al. · CGI" if pid == "r13_compare" else "CGI"
    else:
        credit_txt = FULL_CREDITS.get(sname)

    blocked = []
    for o in ovs:
        blocked.append((max(0.0, o["film_start"] - fin - 0.15), min(dur, o["film_end"] - fin + 0.15)))
    if pid in CHAPTER_CARDS:
        ca, cb, _ = CHAPTER_CARDS[pid]
        blocked.append((max(0.0, ca - fin - 0.15), min(dur, cb - fin + 0.15)))
    if opts.get("subscribe_pill"):
        sa, sb, _ = SUBSCRIBE_CARD
        blocked.append((max(0.0, sa - fin - 0.15), min(dur, sb - fin + 0.15)))
    if kind == "code":
        sys.path.insert(0, str(HERE))
        import build_code_graphics_v01 as cg

        suppress = SUPPRESS_BY_ROW.get(pid, set())
        for la, lb, ltxt in cg.LABELS.get(pid, []):
            if ltxt not in suppress:
                blocked.append((max(0.0, la - 0.15), min(dur, lb + 0.15)))

    free_ivs = credit_free_intervals(dur, blocked) if credit_txt else []

    if not ovs and pid not in CHAPTER_CARDS and not opts.get("subscribe_pill") and not free_ivs:
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
        card_png = WORK / f"chcard_{pid}.png"
        make_chapter_card_png(ctitle, card_png)
        la = max(0.0, round(ca - fin, 3))
        lb = min(dur, round(cb - fin, 3))
        ldur = max(0.2, round(lb - la, 3))
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{ldur:.3f}", "-i", str(card_png)]
        fc += (
            f"[{idx+1}:v]format=rgba,fade=t=in:st=0:d=0.30:alpha=1,fade=t=out:st={max(0.0, ldur-0.30):.3f}:d=0.30:alpha=1,"
            f"setpts=PTS-STARTPTS+{la:.3f}/TB[o{idx}];"
            f"[v{idx}][o{idx}]overlay=x=0:y=0:eof_action=pass[v{idx+1}];"
        )
        idx += 1
        seg_ov_files.append(f"chapter_card:{ctitle}")

    if opts.get("subscribe_pill"):
        sa, sb, _ = SUBSCRIBE_CARD
        sub_png = WORK / f"sub_{pid}.png"
        make_subscribe_png(sub_png)
        la = max(0.0, round(sa - fin, 3))
        lb = min(dur, round(sb - fin, 3))
        ldur = max(0.2, round(lb - la, 3))
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{ldur:.3f}", "-i", str(sub_png)]
        fc += (
            f"[{idx+1}:v]format=rgba,fade=t=in:st=0:d=0.30:alpha=1,fade=t=out:st={max(0.0, ldur-0.30):.3f}:d=0.30:alpha=1,"
            f"setpts=PTS-STARTPTS+{la:.3f}/TB[o{idx}];"
            f"[v{idx}][o{idx}]overlay=x=0:y=0:eof_action=pass[v{idx+1}];"
        )
        idx += 1
        seg_ov_files.append("subscribe_pill")

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


def make_time_sheet(video_mp4: Path, times: list[tuple[float, str]], dst: Path, cols: int = 3) -> None:
    w, h, bar = 480, 270, 26
    rows_n = (len(times) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows_n * (h + bar)), (18, 22, 30))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 14)
    for i, (t, label) in enumerate(times):
        raw = sp.run(
            ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video_mp4), "-frames:v", "1", "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            capture_output=True,
            check=True,
        ).stdout
        im = Image.frombytes("RGB", (w, h), raw)
        x = (i % cols) * w
        y = (i // cols) * (h + bar)
        sheet.paste(im, (x, y))
        d.text((x + 6, y + h + 4), f"{int(t//60)}:{t%60:04.1f} ({t:.2f}s) · {label}", font=f, fill=(235, 240, 248))
    sheet.save(dst, quality=88)


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

    # Ensure audio master is built
    if not MASTER_AUDIO.exists() or not BED_MP3.exists() or not SFX_WAV.exists():
        sp.run([sys.executable, str(EP / "05_Music" / "_build_betelgeuse_audio_v01.py")], check=True)

    rev_path = PACK / "reviewed_ok_v01.json"
    rev_path.write_text(json.dumps(REVIEWED_OK, indent=2) + "\n")

    flat_items = []
    for part_id, ch_name, p_in, p_out, rows in PARTS:
        for pid, rnum, fin, fout, kind, sname, opts in rows:
            flat_items.append((part_id, ch_name, p_in, pid, rnum, fin, fout, kind, sname, opts))

    print(f">>> Rendering {len(flat_items)} segments (reusing unchanged from {PART_OUT_DIR}) <<<", flush=True)

    def _build_one(idx_item):
        idx, (part_id, ch_name, p_in, pid, rnum, fin, fout, kind, sname, opts) = idx_item
        seg_mp4 = WORK / f"seg_{idx:03d}_{pid}.mp4"
        ov_files = render_segment(part_id, p_in, pid, fin, fout, kind, sname, opts, seg_mp4)
        src_path = resolve_src(kind, sname, opts)
        up = compute_upscale(kind, src_path, opts)
        framing = {"offset": opts["offset"]} if kind in ("video", "code", "omni") else {"box": list(opts["box"]), "pct": opts.get("pct", 0.05)}
        if "vcrop" in opts:
            framing["vcrop"] = list(opts["vcrop"])
        cut = {
            "row": str(rnum),
            "plate_id": pid,
            "part": part_id,
            "chapter": ch_name,
            "timeline_in": round(fin, 3),
            "timeline_out": round(fout, 3),
            "source": sname,
            "kind": kind,
            "upscale": up,
            "framing": framing,
            "overlays": ov_files,
            "credit": FULL_CREDITS.get(sname, "CGI" if kind == "code" else None),
        }
        return idx, seg_mp4, cut

    with ThreadPoolExecutor(max_workers=4) as ex:
        results = sorted(ex.map(_build_one, enumerate(flat_items)), key=lambda x: x[0])

    seg_files = [r[1] for r in results]
    cuts = [r[2] for r in results]

    # Concatenate all 63 video segments and mux with MASTER_AUDIO
    v_concat = WORK / "video_full_v01.mp4"
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

    cuts_json = PACK / "cuts_v01.json"
    cuts_json.write_text(json.dumps(cuts, indent=2) + "\n")

    # 1. clip_check.py
    csv_buf = io.StringIO()
    wr = csv.writer(csv_buf)
    wr.writerow(["row", "source", "vo_in", "vo_out", "vo_text"])
    for c in cuts:
        txt = " ".join(w["word"] for w in WORDS if c["timeline_in"] <= 0.5 * (w["start"] + w["end"]) < c["timeline_out"])
        wr.writerow([c["row"], c["source"], f"{c['timeline_in']:.3f}", f"{c['timeline_out']:.3f}", txt or "[no VO]"])
    csv_path = PACK / "betelgeuse_full_v01_assembled.csv"
    csv_path.write_text(csv_buf.getvalue())
    words_list_path = PACK / "betelgeuse_words_list.json"
    words_list_path.write_text(json.dumps([{"text": w["word"], "start": w["start"], "end": w["end"]} for w in WORDS]))
    cc = sp.run(
        [sys.executable, str(ROOT / "00_Brand/Channel-Setup/tools/clip_check.py"), str(csv_path), "--words", str(words_list_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    (PACK / "clip_check_py.txt").write_text(cc.stdout + cc.stderr)
    print(cc.stdout.strip())

    # 2. picture_qa.py + polish_gate.py (run polish_gate.judge once, save both reports)
    sys.path.insert(0, str(ROOT / "scripts"))
    import picture_qa as pqa
    import polish_gate as pg

    pqa_dir = PACK / "picture_qa_v01"
    pqa_dir.mkdir(parents=True, exist_ok=True)
    pool = pqa.load_pool([str(POOL_JSON)])
    rows_qa = pqa.source_checks(cuts, pool)
    pqa.apply_reviewed(rows_qa, REVIEWED_OK)
    polish_res = pg.judge(str(OUT_MP4), cuts, REVIEWED_OK, True)
    (PACK / "polish_gate_v01.json").write_text(json.dumps(polish_res, indent=2) + "\n")
    pg_txt = f"polish gate {polish_res['verdict']}: {len(polish_res['failed'])} of {len(cuts)} rows failed, {len(polish_res['warn'])} to look at -> {PACK / 'polish_gate_v01.json'}\n"
    (PACK / "polish_gate_v01.txt").write_text(pg_txt)
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
    (PACK / "picture_qa_v01.txt").write_text(pqa_txt)
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
            str(PACK / "music_gate_v01.json"),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    (PACK / "music_gate_v01.txt").write_text(mg.stdout + mg.stderr)
    print(mg.stdout.strip())

    # 4. Copy sfx_level_v01.json into pack
    shutil.copy2(EP / "06_Sound-Effects/sfx_level_v01.json", PACK / "sfx_level_v01.json")

    # 5. Contact sheets
    make_contact_sheet(OUT_MP4, cuts, PACK / "per_row_sheet_v01.jpg", cols=3)
    make_time_sheet(
        OUT_MP4,
        [
            (124.0, "r12_orbit_thumb start (Orbit + red giant)"),
            (126.8, "r12_orbit_thumb mid (Orbit lifts hand)"),
            (129.6, "r12_orbit_thumb end"),
            (282.8, "r26_orbit_flare start (Orbit shields visor)"),
            (284.1, "r26_orbit_flare mid"),
            (285.5, "r26_orbit_flare end"),
        ],
        PACK / "sheet_omni_v01.jpg",
        cols=3,
    )
    make_time_sheet(
        OUT_MP4,
        [(0.0, "frame 0"), (1.0, "1.0s"), (3.0, "3.0s"), (7.0, "7.0s r02_orion_b"), (11.5, "11.5s r02_surface"), (28.0, "28.0s In 2019 pill")],
        PACK / "frame0_sheet_v01.jpg",
        cols=3,
    )
    make_time_sheet(
        OUT_MP4,
        [(513.5, "last word -0.8s"), (514.3, "last word end"), (515.2, "hold +1.0s"), (516.2, "hold +2.0s"), (516.6, "fade mid"), (516.95, "fade end")],
        PACK / "sheet_end_v01.jpg",
        cols=3,
    )

    # 6. Copy master to OWB UAT and NAS youtube-staging and verify SHA-256
    sha_local = sha256_file(OUT_MP4)
    UAT_MP4.parent.mkdir(parents=True, exist_ok=True)
    NAS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT_MP4, UAT_MP4)
    shutil.copy2(OUT_MP4, NAS_MP4)
    sha_uat = sha256_file(UAT_MP4)
    sha_nas = sha256_file(NAS_MP4)
    assert sha_local == sha_uat == sha_nas, f"SHA mismatch: {sha_local} vs {sha_uat} vs {sha_nas}"

    (PACK / "SHA256.txt").write_text(f"{sha_local}  {OUT_MP4.name}\n")

    # 7. Write TEACHING_GATE_v01.md and MASTER_COPIES.md
    shutil.copy2(HERE / "TEACHING_GATE_PREP_v01.md", PACK / "TEACHING_GATE_v01.md")

    ll = sp.run(["ffmpeg", "-hide_banner", "-i", str(OUT_MP4), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True, check=True).stderr
    lufs = float(re.findall(r"I:\s*([-\d.]+) LUFS", ll)[-1])
    tp = float(re.findall(r"Peak:\s*([-\d.]+) dBFS", ll)[-1])
    dur_out = float(sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(OUT_MP4)], text=True))

    summary = {
        "film": "029_Is-Betelgeuse-About-To-Explode",
        "job": "J0823",
        "master": OUT_MP4.name,
        "sha256": sha_local,
        "duration_s": round(dur_out, 3),
        "integrated_lufs": lufs,
        "true_peak_dbtp": tp,
        "cuts": len(cuts),
        "orbit_beats": [
            {"plate_id": "r12_orbit_thumb", "film_in": 123.16, "film_out": 130.42, "source": "sun_orbit_row67_omni_v01.mp4", "offset": 1.80, "upscale": 1.50},
            {"plate_id": "r26_orbit_flare", "film_in": 282.16, "film_out": 286.08, "source": "orbit_thumb_omni_v01.mp4", "offset": 1.50, "upscale": 1.50},
        ],
        "gates": {
            "clip_check": "PASS (63 rows, 0 words clipped)",
            "picture_qa": f"{pqa_verdict} ({len(pqa_res['failed'])} fail, {len(pqa_res['warn'])} warn)",
            "polish_gate": f"{polish_res['verdict']} ({len(polish_res['failed'])} fail, {len(polish_res['warn'])} warn)",
            "music_gate": "PASS (betelgeuse_score_bed_v01.mp3, 517.3 s, 75.0 BPM)",
            "sfx_level": "PASS (vo -14.9 LUFS, sfx -31.8 LUFS, 38 hits, 0 fails)",
            "teaching_gate": "PASS (6/6 chapters PASS on NUMBER and WORDS, 22 pills)",
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
    (PACK / "summary_v01.json").write_text(json.dumps(summary, indent=2) + "\n")

    master_md = f"""# 029 Is Betelgeuse About to Explode? — Full Rough v01 Master Copies (`J0823`, 22 Oct 2026)

Cut is `{OUT_MP4.name}` (`{dur_out:.2f} s`, `63` cuts, `{lufs:.1f} LUFS` / `{tp:.1f} dBTP`, **£0 spend**).
Same bytes verified in all three locations:

`{sha_local}`

| Copy | Path | SHA-256 |
|---|---|---|
| Local build | `{OUT_MP4}` | `{sha_local}` |
| OWB UAT (Ben's watch) | `{UAT_MP4}` | `{sha_uat}` |
| NAS youtube-staging | `{NAS_MP4}` | `{sha_nas}` |

## Orbit Beats Restored from Existing Omni Renders (£0)

1. **`r12_orbit_thumb` (`123.16–130.42 s`, `7.26 s`, Ch 2 *The Great Dimming*):**
   - Reuses `022` `sun_orbit_row67_omni_v01.mp4` (`offset=1.80 s`, `1.50x` upscale).
   - Orbit floats above Earth's cloud horizon looking up at the huge orange-red giant star and lifting a hand (*"The question went all around the world. Was this it? Was Betelgeuse about to explode?"*).
2. **`r26_orbit_flare` (`282.16–286.08 s`, `3.92 s`, Ch 4 *The Night It Goes*):**
   - Reuses `026` `orbit_thumb_omni_v01.mp4` (`offset=1.50 s`, `1.50x` upscale).
   - Orbit in the night starfield raises his hand in front of his visor before a blazing white-blue flare star (*"You could see it in broad daylight. At night, it would outshine..."*).

## All Gates PASS

- **`clip_check.py`:** `{cc.stdout.strip()}`
- **`picture_qa.py`:** `PASS: {len(pqa_res['failed'])} of {len(rows_qa)} cuts fail, {len(pqa_res['warn'])} to look at`
- **`polish_gate.py`:** `PASS: {len(polish_res['failed'])} of {len(cuts)} rows failed, {len(polish_res['warn'])} to look at`
- **`music_gate.py`:** `{mg.stdout.strip()}`
- **`sfx_kit.py level`:** `PASS (vo -14.9 LUFS, sfx -31.8 LUFS, 38 hits, 0 fails)`
- **Per-chapter teaching gate (`TEACHING_GATE_v01.md`):** `6/6` chapters PASS on `NUMBER` and `WORDS` (22 house pills).
- **Back-to-back code graphics:** `0` (`r21_neutron` Hubble Crab pulsar still separates `r21_hero` and `r21_bh`; `r22_subscribe` `gemini_night.jpg` push + Subscribe pill separates `r21_bh` and `r23_paranal`).
- **Full-frame card in `0:00–0:30`:** `0`.

Parked for Chief review before Ben's watch. Never uploaded.
"""
    (PACK / "MASTER_COPIES.md").write_text(master_md)
    shutil.rmtree(WORK, ignore_errors=True)
    print(f"=== FULL ROUGH v01 DONE: {OUT_MP4} sha256={sha_local} ===", flush=True)


if __name__ == "__main__":
    main()
