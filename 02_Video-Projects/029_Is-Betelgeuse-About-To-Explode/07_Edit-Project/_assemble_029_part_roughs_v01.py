#!/usr/bin/env python3
"""029 Is Betelgeuse About to Explode? — Part Roughs v01 assembler (J0808).

Applies Chief's J0353 source rulings (PLATE_BOARDS_v03.json, 9 rows modified) and assembles
the 6 chapter part roughs (part00_rough_v01 .. part05_rough_v01) on the locked VO v02 take
(02_Voiceover/betelgeuse_vo_v01.wav, 515.18s, last word 514.26s + 3.0s hold/fade = 517.26s).

Rules enforced:
- £0 spend, no Flow/Vertex/Omni/Veo/ElevenLabs (generation_authorized: false).
- No full-frame chapter card inside 0:00-0:30 (J0804 change 2, Chief approved).
- Full source credits per HARVEST_REVIEW_v01.md (including 'Artist's impression · ESO, ESA/Hubble, M. Kornmesser'
  on dust_impression), hidden while any teaching overlay pill is on screen so one label at a time holds.
- Skip ESO logo bumpers on chajnantor_mw.m4v (0.00-3.25s and 13.30-16.41s; uses 3.25-13.25s clean sky window).
- All 22 J0504 teaching overlay pills included at exact VO word timestamps, suppressing duplicate gold labels.
- Every cut boundary is snapped to an inter-word VO pause (0 words clipped).
- Runs picture_qa.py + polish_gate.py on each part rough and writes per-part contact sheets + QA reports.
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
HDIR = HERE / "harvest_v01"
CDIR = HERE / "code_graphics_v01"
OV_PACK = HERE / "teaching_overlays_v01_pack"
PACK = HERE / "part_roughs_v01_pack"
WORK = Path("/private/tmp/betelgeuse029_part_roughs_work_v01")
OUT_DIR = Path("/private/tmp/029_part_roughs_v01")

VO_WAV = EP / "02_Voiceover" / "betelgeuse_vo_v01.wav"
WORDS_JSON = EP / "02_Voiceover" / "words.json"
BOARDS_JSON = HERE / "PLATE_BOARDS_v03.json"
POOL_JSON = HERE / "SOURCE_POOL_v03.json"

FPS = 30
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
NAVY = (23, 36, 55, 220)
ENC = ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p"]

# Load VO words and teaching overlays
WORDS = json.loads(WORDS_JSON.read_text())["words"]
OV_DATA = json.loads((OV_PACK / "overlays_v01.json").read_text())["labels"]

# Gold label strings to suppress on code graphics when replaced by a teaching pill
SUPPRESS_BY_ROW = {
    "r03_r04_promise": {"in 2019", "giant star actually dies"},
    "r09_finder": {"three stars"},
    "r10_r11_dip": {"February 2020", "about a third", "fifty years"},
    "r17_r20_shells": {"less than a second"},
    "r29_span_astrolabe": {"five hundred years", "hundred thousand years"},
    "r31_shells_twins": {"100,000 years", "a hundred years"},
    "r35_song": {"1054"},
}

# Full source credits per HARVEST_REVIEW_v01.md
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
}

# Video grading LUTs so dark night-sky clips pass polish_gate (mean >= 28, p95 >= 50, std >= 18)
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
}

# All 63 plates grouped into the 6 parts (Part 00 .. Part 05), with word-safe cut boundaries (in_s, out_s)
# Each entry: (plate_id, row_num, in_s, out_s, kind, src_name, opts)
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
            ("r10_span_c", 10, 105.48, 109.50, "video", "lasilla_startrails.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r10_r11_dip", 10, 109.50, 123.16, "code", "code_graphic_029_r10_r11_dip_v01.mp4", {"plate_id": "r10_r11_dip", "offset": 0.0, "upscale": 1.0}),
            # r12_orbit_thumb: Omni not minted (generation_authorized: false, £0); SHOT_LIST_v01 fallback = real night sky footage
            # separating r10_r11_dip (code) and r13_compare (code).
            ("r12_orbit_thumb", 12, 123.16, 130.42, "video", "orion_over_paranal.mp4", {"offset": 1.20, "upscale": 1.0, "omni_fallback": True}),
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
            ("r20_crab", 20, 224.02, 226.10, "still", "crab.jpg", {"box": (0.04, 0.18, 0.96, 0.74), "pct": 0.05, "gamma": 0.90, "lift": 0.0}),
            ("r21_neutron", 21, 226.10, 231.95, "still", "crab.jpg", {"box": (0.22, 0.28, 0.78, 0.62), "pct": 0.05, "gamma": 0.88, "lift": 4.0}),
            ("r21_hero", 21, 231.95, 236.95, "code", "code_graphic_029_r21_hero_v01.mp4", {"plate_id": "r21_hero", "offset": 0.0, "upscale": 1.0}),
            ("r21_bh", 21, 236.95, 242.50, "code", "code_graphic_029_r21_bh_v01.mp4", {"plate_id": "r21_bh", "offset": 0.0, "upscale": 1.0}),
            ("r22_subscribe", 22, 242.50, 247.60, "code", "code_graphic_029_r22_subscribe_v01.mp4", {"plate_id": "r22_subscribe", "offset": 0.0, "upscale": 1.0}),
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
            # r26_orbit_flare: Omni not minted (generation_authorized: false, £0); real night-sky footage separates r25_orion (code) and r27_orion (code).
            ("r26_orbit_flare", 26, 282.16, 286.08, "video", "orion_over_paranal.mp4", {"offset": 2.40, "upscale": 1.0, "omni_fallback": True}),
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
            ("r30_vlt", 30, 350.50, 359.36, "video", "lasilla_startrails.mp4", {"offset": 18.5, "upscale": 1.0}),
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
            ("r39_return", 39, 509.25, 517.26, "video", "lasilla_mw.mp4", {"offset": 5.5, "upscale": 1.0, "fade_out": 1.0}),
        ],
    ),
]

# Chief-ruled stretches where source clip length (<10s) makes the two Chief-assigned uses <10s apart
REVIEWED_OK = {
    "chajnantor_mw.m4v@6.1": {
        "note": (
            "J0808 Chief brief: skip ESO logo bumpers on Chajnantor (0.00-3.25s and 13.30-16.41s on 16.41s source = "
            "10.05s clean sky window); r24_superk (3.25s wide) and r24_superk_2 (6.10s, 1.20x core crop) split the clean sky window."
        ),
        "kinds": ["reuse"],
    },
    "orion_over_paranal.mp4@2.4": {
        "note": (
            "J0353 Chief ruling #8: r34_pair -> orion_over_paranal (9.04s source clip); "
            "r34_pair uses wide 0.45s and r36_orion_b uses 1.25x upper-sky Orion crop at 2.40s."
        ),
        "kinds": ["reuse"],
    },
}


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


def check_plan() -> list[str]:
    problems = []
    total_plates = 0
    for part_id, ch_name, p_in, p_out, rows in PARTS:
        print(f"=== {part_id} · {ch_name} ({p_in:.2f}-{p_out:.2f}s, {p_out - p_in:.2f}s) ===")
        prev_out = p_in
        for pid, rnum, fin, fout, kind, sname, opts in rows:
            total_plates += 1
            src = (CDIR if kind == "code" else HDIR) / sname
            if not src.exists():
                problems.append(f"{pid}: missing {src}")
                continue
            if abs(fin - prev_out) > 1e-3:
                problems.append(f"{pid}: gap/overlap {prev_out:.2f} -> {fin:.2f}")
            prev_out = fout
            up = compute_upscale(kind, src, opts)
            if up > 2.35:
                problems.append(f"{pid}: upscale {up:.2f} > 2.35")
            # Check word boundaries (except end of film)
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
            print(
                f"  {pid:20s} row={rnum:2d} {fin:6.2f}-{fout:6.2f} ({fout-fin:5.2f}s) {kind:6s} {sname:38s} up={up:4.2f}x ovs={len(ovs)}"
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


def render_segment(pid: str, fin: float, fout: float, kind: str, sname: str, opts: dict, seg_out: Path) -> list[str]:
    dur = round((fout - fin) * FPS) / FPS
    frames = round(dur * FPS)
    base_mp4 = WORK / f"base_{pid}.mp4"
    src = (CDIR if kind == "code" else HDIR) / sname

    if kind == "video":
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
        if not suppress and abs(dur - float(sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(src)], text=True))) < 0.04:
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

    # Check teaching overlays and corner credit for this segment
    ovs = [o for o in OV_DATA if o["row"] == pid]
    if kind == "code":
        if pid == "r13_compare":
            credit_txt = "ESO/M. Montargès et al. · CGI"
        elif pid == "r22_subscribe":
            credit_txt = None
        else:
            credit_txt = "CGI"
    else:
        credit_txt = FULL_CREDITS.get(sname)

    # Compute blocked intervals where a teaching pill or internal code graphic label is active
    blocked = []
    for o in ovs:
        blocked.append((max(0.0, o["film_start"] - fin - 0.15), min(dur, o["film_end"] - fin + 0.15)))
    if kind == "code":
        sys.path.insert(0, str(HERE))
        import build_code_graphics_v01 as cg

        suppress = SUPPRESS_BY_ROW.get(pid, set())
        for la, lb, ltxt in cg.LABELS.get(pid, []):
            if ltxt not in suppress:
                blocked.append((max(0.0, la - 0.15), min(dur, lb + 0.15)))

    free_ivs = credit_free_intervals(dur, blocked) if credit_txt else []

    if not ovs and not free_ivs:
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
            src_path = (CDIR if kind == "code" else HDIR) / sname
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
                    "credit": FULL_CREDITS.get(sname, "CGI" if kind == "code" and pid != "r22_subscribe" else None),
                    "omni_fallback": bool(opts.get("omni_fallback", False)),
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

        # Slice VO and normalize to -14 LUFS, padding silence at the end of part05 (515.18 -> 517.26s)
        a_wav = WORK / f"{part_id}_vo.wav"
        af_parts = [f"apad=whole_dur={p_dur:.3f}", "loudnorm=I=-14:TP=-1.5:LRA=11"]
        if part_id == "part05":
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

        out_mp4 = OUT_DIR / f"029_Betelgeuse_{part_id}_rough_v01.mp4"
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
                "--reviewed-ok",
                str(rev_path),
                "--out-dir",
                str(p_pack),
            ],
            check=True,
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
            check=True,
        )

        pqa = json.loads((p_pack / "picture_qa.json").read_text())
        pg_res = json.loads((p_pack / "polish_gate.json").read_text())
        sha = hashlib.sha256(out_mp4.read_bytes()).hexdigest()
        meta = {
            "film": "029",
            "job": "J0808",
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
            "spend_gbp": 0.0,
        }
        (p_pack / f"ROUGH_META_{part_id}_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
        summary_rows.append(meta)
        print(
            f"=== {part_id} DONE: sha={sha[:12]} picture_qa={pqa['verdict']} ({len(pqa['failed'])} fail, {len(pqa['warn'])} warn) "
            f"polish_gate={pg_res['verdict']} ({len(pg_res['failed'])} fail) ===",
            flush=True,
        )

    if summary_rows and not only_parts:
        (PACK / "PART_ROUGHS_SUMMARY_v01.json").write_text(json.dumps(summary_rows, indent=2) + "\n")
    shutil.rmtree(WORK, ignore_errors=True)


if __name__ == "__main__":
    main()
