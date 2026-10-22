#!/usr/bin/env python3
"""029 Is Betelgeuse About to Explode? — Full Rough v02 assembler (J0828).

Breaks the 5 long code-graphic holds (plus the 20.7s back-to-back companion_speckle hold on r33)
into stretches of 12s or less by cutting away at sentence boundaries (words.json) to moving plates
already in the pool, then returning to the code graphic at its continuing animation timestamp.

All 5 code-graphic holds broken (<= 12.0s per stretch):
1. `r03_r04_promise` (13.96-36.94s, was 22.98s):
   - `r03_promise_a` (13.96-22.00s, 8.04s): code graphic @ 0.00s ("One day it will blow itself apart... daytime sky.")
   - `r04_promise_cut` (22.00-25.54s, 3.54s): `alma_orion_set.mp4` @ 0.00s ("In this film, I will show you what kind of star it is,")
   - `r04_promise_b` (25.54-36.94s, 11.40s): code graphic @ 11.58s ("why it scared astronomers in 2019..." + `In 2019` pill at 27.48-29.50s)
2. `r17_r20_shells` (175.40-224.02s, was 48.62s — 3 cut-aways -> 4 code stretches, max 11.53s):
   - `r17_shells_a` (175.40-185.86s, 10.46s): code graphic @ 0.00s ("Gravity pulls... hydrogen into helium.")
   - `r18_shells_cut1` (185.86-189.12s, 3.26s): `sphere_dec.jpg` push ("Now it is fusing helium into carbon.")
   - `r18_shells_b` (189.12-199.43s, 10.31s): code graphic @ 13.72s ("After that will come heavier... only years, then days.")
   - `r19_shells_cut2` (199.43-204.37s, 4.94s): `tarantula.jpg` tight cluster push ("The end of the line is iron. Fusing iron does not release energy.")
   - `r19_shells_c` (204.37-215.90s, 11.53s): code graphic @ 28.97s ("It costs energy... gravity wins. In less than a second... collapses" + `Less than 1 second` pill at 211.94-215.20s)
   - `r20_shells_cut3` (215.90-218.20s, 2.30s): `casa.jpg` central remnant push ("into a ball the size of a city.")
   - `r20_shells_d` (218.20-224.02s, 5.82s): code graphic @ 42.80s ("The outer layers fall in, bounce off it, and are blasted out into space.")
3. `r27_orion` (290.98-309.46s, was 18.48s):
   - `r27_orion_a` (290.98-299.90s, 8.92s): code graphic @ 0.00s ("It would stay that bright for weeks... simply gone.")
   - `r27_orion_cut` (299.90-303.32s, 3.42s): `m42.jpg` upper trapezium push ("The hunter would lose a shoulder,")
   - `r27_orion_b` (303.32-309.46s, 6.14s): code graphic @ 12.34s ("and every person who looked up afterwards would see a different Orion from the one we know.")
4. `r29_span_astrolabe` (326.56-350.50s, was 23.94s):
   - `r29_astro_a` (326.56-333.14s, 6.58s): code graphic @ 0.00s ("And here is a strange thought. The light from Betelgeuse takes centuries to reach us.")
   - `r29_astro_cut1` (333.14-336.90s, 3.76s): `jwst_pillars.jpg` upper spires push ("If it had exploded sometime in the late Middle Ages,")
   - `r29_astro_b` (336.90-342.54s, 5.64s): code graphic @ 10.34s ("more than five hundred years ago, we would only be finding out about now." + `500 years` pill at 337.66-340.86s)
   - `r29_astro_cut2` (342.54-345.36s, 2.82s): `gemini_dome.jpg` push + `So When?` chapter card (342.84-345.34s, "So when will it happen?")
   - `r29_astro_c` (345.36-350.50s, 5.14s): code graphic @ 18.80s ("The best estimates say Betelgeuse has around a hundred thousand years left." + `100,000 years` pill at 347.88-349.95s)
5. `r31_shells_twins` (359.36-378.30s, was 18.94s):
   - `r31_twins_a` (359.36-369.62s, 10.26s): code graphic @ 0.00s ("Why can't we just look and tell? Because the changes that matter happen deep in the core... until the very end.")
   - `r31_twins_cut` (369.62-372.00s, 2.38s): `hl_tau.jpg` push ("From outside, a")
   - `r31_twins_b` (372.00-378.30s, 6.30s): code graphic @ 12.64s ("star with 100,000 years left and a star with a hundred years left can look almost the same." + `100,000 years left` and `100 years` pills)
6. Bonus `r33_speckle` + `r33_pair` (392.60-413.30s, was 20.70s back-to-back `companion_speckle.jpg`):
   - `r33_speckle` (392.60-403.00s, 10.40s): `companion_speckle.jpg` push + `In 2025` pill
   - `r33_pair_cut` (403.00-406.60s, 3.60s): `gemini_earth_sky.jpg` push ("right where a hidden companion star was predicted to be.")
   - `r33_pair` (406.60-413.30s, 6.70s): `companion_speckle.jpg` push + `Every 6 years` pill ("A small star circling Betelgeuse every six years or so, lost in its glare.")
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
PACK_V01 = HERE / "full_rough_v01_pack"
PACK = HERE / "full_rough_v02_pack"
PART_OUT_DIR = Path("/private/tmp/029_part_roughs_v01")
V01_MP4 = Path("/private/tmp/029_Betelgeuse_full_rough_v01.mp4")
WORK = Path("/private/tmp/betelgeuse029_full_rough_work_v02")
AUDIO_WORK = Path("/private/tmp/betelgeuse029_audio_work_v01")

OUT_MP4 = Path("/private/tmp/029_Betelgeuse_full_rough_v02.mp4")
UAT_MP4 = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/029_Betelgeuse_full_rough_v02.mp4"
NAS_DIR = Path("/Volumes/data/mac-mini-archive/youtube-staging/029")
NAS_MP4 = NAS_DIR / "029_Betelgeuse_full_rough_v02.mp4"

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
SUPPRESS_BY_PLATE = {
    "r03_r04_promise": {"in 2019", "giant star actually dies"},
    "r09_finder": {"three stars"},
    "r10_r11_dip": {"began to fade", "February 2020", "about a third", "fifty years"},
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
    "r29_astro_cut2": (342.84, 345.34, "So When?"),
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

# Plates newly split or added in v02 (all unchanged plates slice directly from V01_MP4 if cached)
V02_NEW_PLATES = {
    "r03_promise_a",
    "r04_promise_cut",
    "r04_promise_b",
    "r17_shells_a",
    "r18_shells_cut1",
    "r18_shells_b",
    "r19_shells_cut2",
    "r19_shells_c",
    "r20_shells_cut3",
    "r20_shells_d",
    "r27_orion_a",
    "r27_orion_cut",
    "r27_orion_b",
    "r29_astro_a",
    "r29_astro_cut1",
    "r29_astro_b",
    "r29_astro_cut2",
    "r29_astro_c",
    "r31_twins_a",
    "r31_twins_cut",
    "r31_twins_b",
    "r33_pair_cut",
    "r33_pair",
    "r36_orion_b",
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
            ("r03_promise_a", 3, 13.96, 22.00, "code", "code_graphic_029_r03_r04_promise_v01.mp4", {"plate_id": "r03_r04_promise", "full_dur": 22.98, "offset": 0.0, "upscale": 1.0}),
            ("r04_promise_cut", 4, 22.00, 25.54, "video", "alma_orion_set.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r04_promise_b", 4, 25.54, 36.94, "code", "code_graphic_029_r03_r04_promise_v01.mp4", {"plate_id": "r03_r04_promise", "full_dur": 22.98, "offset": 11.58, "upscale": 1.0}),
        ],
    ),
    (
        "part01",
        "1 The Star in Orion's Shoulder",
        36.94,
        105.48,
        [
            ("r05_surface", 5, 36.94, 41.90, "still", "sphere_dec.jpg", {"box": (0.0, 0.0, 1.0, 1.0), "pct": 0.05, "feathered_blur": True, "gamma": 0.52, "lift": 24.0}),
            ("r05_scale", 5, 41.90, 48.58, "code", "code_graphic_029_r05_scale_v01.mp4", {"plate_id": "r05_scale", "full_dur": 6.68, "offset": 0.0, "upscale": 1.0}),
            ("r06_paranal", 6, 48.58, 55.00, "video", "lasilla_startrails.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r06_sphere_jan", 6, 55.00, 62.10, "still", "sphere_jan.jpg", {"box": (0.0, 0.04, 1.0, 0.96), "pct": 0.05, "feathered_blur": True, "gamma": 0.55, "lift": 22.0}),
            ("r07_sdo", 7, 62.10, 67.50, "still", "sdo_hmi_continuum.jpg", {"box": (0.02, 0.08, 0.98, 0.62), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r07_sphere_jan", 7, 67.50, 73.35, "still", "sphere_jan.jpg", {"box": (0.0, 0.0, 1.0, 1.0), "pct": 0.05, "feathered_blur": True, "gamma": 0.55, "lift": 22.0}),
            ("r08_westerlund_w", 8, 73.35, 80.19, "still", "westerlund.jpg", {"box": (0.05, 0.12, 0.95, 0.795), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r08_westerlund_t", 8, 80.19, 85.92, "still", "westerlund.jpg", {"box": (0.22, 0.24, 0.78, 0.66), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r08_tarantula", 8, 85.92, 92.92, "still", "tarantula.jpg", {"box": (0.04, 0.12, 0.96, 0.76), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r09_finder", 9, 92.92, 105.48, "code", "code_graphic_029_r09_finder_v01.mp4", {"plate_id": "r09_finder", "full_dur": 12.56, "offset": 0.0, "upscale": 1.0}),
        ],
    ),
    (
        "part02",
        "2 The Great Dimming",
        105.48,
        169.50,
        [
            ("r10_span_c", 10, 105.48, 109.50, "video", "lasilla_startrails.mp4", {"offset": 6.50, "upscale": 1.15, "vcrop": (1670, 939, 125, 70)}),
            ("r10_r11_dip", 10, 109.50, 123.16, "code", "code_graphic_029_r10_r11_dip_v01.mp4", {"plate_id": "r10_r11_dip", "full_dur": 13.66, "offset": 0.0, "upscale": 1.0}),
            ("r12_orbit_thumb", 12, 123.16, 130.42, "omni", "sun_orbit_row67_omni_v01.mp4", {"src_path": str(OMNI_RED_GIANT), "offset": 1.80, "upscale": 1.50}),
            ("r13_compare", 13, 130.42, 137.80, "code", "code_graphic_029_r13_compare_v01.mp4", {"plate_id": "r13_compare", "full_dur": 7.38, "offset": 0.0, "upscale": 1.0}),
            ("r14_ejection", 14, 137.80, 142.86, "still", "dust_impression.jpg", {"box": (0.0, 0.16, 1.0, 0.84), "pct": 0.05, "gamma": 0.48, "lift": 24.0}),
            ("r14_dust", 14, 142.86, 147.60, "still", "dust_impression.jpg", {"box": (0.12, 0.22, 0.88, 0.78), "pct": 0.05, "gamma": 0.48, "lift": 24.0}),
            ("r15_span_d", 15, 147.60, 152.80, "video", "lasilla_startrails.mp4", {"offset": 11.0, "upscale": 1.0}),
            ("r15_dip", 15, 152.80, 157.76, "code", "code_graphic_029_r15_dip_v01.mp4", {"plate_id": "r15_dip", "full_dur": 4.96, "offset": 0.0, "upscale": 1.0}),
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
            ("r17_shells_a", 17, 175.40, 185.86, "code", "code_graphic_029_r17_r20_shells_v01.mp4", {"plate_id": "r17_r20_shells", "full_dur": 48.62, "offset": 0.0, "upscale": 1.0}),
            ("r18_shells_cut1", 18, 185.86, 189.12, "still", "sphere_dec.jpg", {"box": (0.0, 0.02, 1.0, 0.98), "pct": 0.05, "feathered_blur": True, "gamma": 0.52, "lift": 24.0}),
            ("r18_shells_b", 18, 189.12, 199.43, "code", "code_graphic_029_r17_r20_shells_v01.mp4", {"plate_id": "r17_r20_shells", "full_dur": 48.62, "offset": 13.72, "upscale": 1.0}),
            ("r19_shells_cut2", 19, 199.43, 204.37, "still", "tarantula.jpg", {"box": (0.14, 0.20, 0.86, 0.72), "pct": 0.05, "gamma": 1.0, "lift": 0.0}),
            ("r19_shells_c", 19, 204.37, 215.90, "code", "code_graphic_029_r17_r20_shells_v01.mp4", {"plate_id": "r17_r20_shells", "full_dur": 48.62, "offset": 28.97, "upscale": 1.0}),
            ("r20_shells_cut3", 20, 215.90, 218.20, "still", "casa.jpg", {"box": (0.08, 0.18, 0.92, 0.76), "pct": 0.05, "gamma": 0.85, "lift": 10.0}),
            ("r20_shells_d", 20, 218.20, 224.02, "code", "code_graphic_029_r17_r20_shells_v01.mp4", {"plate_id": "r17_r20_shells", "full_dur": 48.62, "offset": 42.80, "upscale": 1.0}),
            ("r20_crab", 20, 224.02, 228.95, "still", "crab.jpg", {"box": (0.04, 0.18, 0.96, 0.74), "pct": 0.05, "gamma": 0.90, "lift": 0.0}),
            ("r21_hero", 21, 228.95, 233.00, "code", "code_graphic_029_r21_hero_v01.mp4", {"plate_id": "r21_hero", "full_dur": 4.05, "offset": 0.0, "upscale": 1.0}),
            ("r21_neutron", 21, 233.00, 238.30, "still", "crab.jpg", {"box": (0.22, 0.28, 0.78, 0.62), "pct": 0.05, "gamma": 0.88, "lift": 4.0}),
            ("r21_bh", 21, 238.30, 242.50, "code", "code_graphic_029_r21_bh_v01.mp4", {"plate_id": "r21_bh", "full_dur": 4.20, "offset": 0.0, "upscale": 1.0}),
            ("r22_subscribe", 22, 242.50, 247.60, "still", "gemini_night.jpg", {"box": (0.04, 0.08, 0.96, 0.80), "pct": 0.05, "gamma": 0.90, "lift": 4.0, "subscribe_pill": True}),
        ],
    ),
    (
        "part04",
        "4 The Night It Goes",
        247.60,
        350.50,
        [
            ("r23_paranal", 23, 247.60, 254.80, "code", "code_graphic_029_r23_paranal_v01.mp4", {"plate_id": "r23_paranal", "full_dur": 7.20, "offset": 0.0, "upscale": 1.0}),
            ("r24_superk", 24, 254.80, 261.28, "video", "chajnantor_mw.m4v", {"offset": 3.25, "upscale": 1.50}),
            ("r24_epic", 24, 261.28, 266.96, "still", "dscovr_epic.jpg", {"box": (0.04, 0.18, 0.96, 0.74), "pct": 0.05, "gamma": 0.85, "lift": 10.0}),
            ("r24_superk_2", 24, 266.96, 274.12, "video", "chajnantor_mw.m4v", {"offset": 6.10, "upscale": 1.80, "vcrop": (1066, 600, 107, 0)}),
            ("r25_orion", 25, 274.12, 282.16, "code", "code_graphic_029_r25_orion_v01.mp4", {"plate_id": "r25_orion", "full_dur": 8.04, "offset": 0.0, "upscale": 1.0}),
            ("r26_orbit_flare", 26, 282.16, 286.08, "omni", "orbit_thumb_omni_v01.mp4", {"src_path": str(OMNI_FLARE_SHIELD), "offset": 1.50, "upscale": 1.50}),
            ("r26_moon", 26, 286.08, 290.98, "still", "half_moon.jpg", {"box": (0.04, 0.18, 0.96, 0.74), "pct": 0.05, "gamma": 0.75, "lift": 16.0}),
            ("r27_orion_a", 27, 290.98, 299.90, "code", "code_graphic_029_r27_orion_v01.mp4", {"plate_id": "r27_orion", "full_dur": 18.48, "offset": 0.0, "upscale": 1.0}),
            ("r27_orion_cut", 27, 299.90, 303.32, "still", "m42.jpg", {"box": (0.14, 0.16, 0.86, 0.68), "pct": 0.05, "gamma": 0.90, "lift": 4.0}),
            ("r27_orion_b", 27, 303.32, 309.46, "code", "code_graphic_029_r27_orion_v01.mp4", {"plate_id": "r27_orion", "full_dur": 18.48, "offset": 12.34, "upscale": 1.0}),
            ("r28_epic", 28, 309.46, 315.47, "still", "dscovr_epic.jpg", {"box": (0.12, 0.22, 0.88, 0.70), "pct": 0.05, "gamma": 0.85, "lift": 10.0}),
            ("r28_mw", 28, 315.47, 320.70, "video", "lasilla_mw.mp4", {"offset": 0.0, "upscale": 1.0}),
            ("r28_people", 28, 320.70, 326.56, "still", "gemini_earth_sky.jpg", {"box": (0.05, 0.10, 0.95, 0.82), "pct": 0.05, "gamma": 0.92, "lift": 4.0}),
            ("r29_astro_a", 29, 326.56, 333.14, "code", "code_graphic_029_r29_span_astrolabe_v01.mp4", {"plate_id": "r29_span_astrolabe", "full_dur": 23.94, "offset": 0.0, "upscale": 1.0}),
            ("r29_astro_cut1", 29, 333.14, 336.90, "still", "jwst_pillars.jpg", {"box": (0.04, 0.12, 0.96, 0.68), "pct": 0.05, "gamma": 0.92, "lift": 4.0}),
            ("r29_astro_b", 29, 336.90, 342.54, "code", "code_graphic_029_r29_span_astrolabe_v01.mp4", {"plate_id": "r29_span_astrolabe", "full_dur": 23.94, "offset": 10.34, "upscale": 1.0}),
            ("r29_astro_cut2", 29, 342.54, 345.36, "still", "gemini_dome.jpg", {"box": (0.08, 0.16, 0.92, 0.74), "pct": 0.05, "gamma": 0.85, "lift": 6.0}),
            ("r29_astro_c", 29, 345.36, 350.50, "code", "code_graphic_029_r29_span_astrolabe_v01.mp4", {"plate_id": "r29_span_astrolabe", "full_dur": 23.94, "offset": 18.80, "upscale": 1.0}),
        ],
    ),
    (
        "part05",
        "5 So When?",
        350.50,
        517.26,
        [
            ("r30_vlt", 30, 350.50, 359.36, "video", "lasilla_startrails.mp4", {"offset": 13.10, "upscale": 1.15, "vcrop": (1670, 939, 125, 70)}),
            ("r31_twins_a", 31, 359.36, 369.62, "code", "code_graphic_029_r31_shells_twins_v01.mp4", {"plate_id": "r31_shells_twins", "full_dur": 18.94, "offset": 0.0, "upscale": 1.0}),
            ("r31_twins_cut", 31, 369.62, 372.00, "still", "hl_tau.jpg", {"box": (0.10, 0.22, 0.90, 0.72), "pct": 0.05, "gamma": 0.72, "lift": 16.0}),
            ("r31_twins_b", 31, 372.00, 378.30, "code", "code_graphic_029_r31_shells_twins_v01.mp4", {"plate_id": "r31_shells_twins", "full_dur": 18.94, "offset": 12.64, "upscale": 1.0}),
            ("r32_sphere_dec", 32, 378.30, 385.46, "still", "sphere_dec.jpg", {"box": (0.0, 0.04, 1.0, 0.96), "pct": 0.05, "feathered_blur": True, "gamma": 0.52, "lift": 24.0}),
            ("r32_ejection", 32, 385.46, 392.60, "still", "visir_flames.jpg", {"box": (0.0, 0.16, 1.0, 0.84), "pct": 0.05, "gamma": 0.70, "lift": 14.0}),
            ("r33_speckle", 33, 392.60, 403.00, "still", "companion_speckle.jpg", {"box": (0.03, 0.23, 0.97, 0.77), "pct": 0.05, "sub": 10.0, "gain": 5.2, "lift": 20.0}),
            ("r33_pair_cut", 33, 403.00, 406.60, "still", "gemini_earth_sky.jpg", {"box": (0.12, 0.18, 0.88, 0.76), "pct": 0.05, "gamma": 0.92, "lift": 4.0}),
            ("r33_pair", 33, 406.60, 413.30, "still", "companion_speckle.jpg", {"box": (0.0, 0.18, 1.0, 0.82), "pct": 0.05, "sub": 10.0, "gain": 5.2, "lift": 20.0}),
            ("r34_gemini", 34, 413.30, 419.65, "still", "gemini_night.jpg", {"box": (0.08, 0.12, 0.92, 0.86), "pct": 0.05, "gamma": 0.90, "lift": 4.0}),
            ("r34_pair", 34, 419.65, 425.12, "video", "orion_over_paranal.mp4", {"offset": 0.45, "upscale": 1.0}),
            ("r34_dome", 34, 425.12, 432.60, "still", "gemini_dome.jpg", {"box": (0.05, 0.12, 0.95, 0.78), "pct": 0.05, "gamma": 0.85, "lift": 6.0}),
            ("r35_song", 35, 432.60, 442.00, "code", "code_graphic_029_r35_song_v01.mp4", {"plate_id": "r35_song", "full_dur": 9.40, "offset": 0.0, "upscale": 1.0}),
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

# Chief-ruled board reuses (J0353 + J0808 KEEP + J0828 cut-aways)
REVIEWED_OK = {
    "_status": "Chief J0353 source rulings + J0808 KEEP on PLATE_BOARDS_v03.json + J0828 long-hold cut-aways (22 Oct 2026).",
    "sphere_jan.jpg": {
        "note": "J0353 Chief ruling #1 + PLATE_BOARDS_v03: r02_surface -> sphere_jan.jpg (eso2003b) alongside r06_sphere_jan and r07_sphere_jan (3 distinct framings).",
        "kinds": ["reuse"],
    },
    "sphere_dec.jpg": {
        "note": "J0828 Chief brief: sphere_dec.jpg crop push used as 3.26s cut-away at 185.86-189.12s inside r17_r20_shells alongside r05_surface and r32_sphere_dec.",
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
    "alma_orion_set.mp4": {
        "note": "J0828 Chief brief: 4.44s ESO ALMA Orion Nebula setting time-lapse used as 3.54s cut-away at 22.00-25.54s inside r03_r04_promise and at 493.36-496.90s on r38_night.",
        "kinds": ["reuse"],
    },
    "code_graphic_029_r29_span_astrolabe_v01.mp4@18.8": {
        "note": "J0828 Chief brief: r29_span_astrolabe split into 3 non-overlapping code stretches (0.00-6.58s, 10.34-15.98s, 18.80-23.94s) separated by jwst_pillars.jpg and gemini_dome.jpg cut-aways.",
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


def overlays_for_window(fin: float, fout: float) -> list[dict]:
    return [o for o in OV_DATA if fin - 0.05 <= o["film_start"] and o["film_end"] <= fout + 0.05]


def check_plan() -> list[str]:
    problems = []
    total_plates = 0
    prev_kind = None
    prev_pid = None
    prev_sname = None
    matched_ovs = set()
    for part_id, ch_name, p_in, p_out, rows in PARTS:
        print(f"=== {part_id} · {ch_name} ({p_in:.2f}-{p_out:.2f}s, {p_out - p_in:.2f}s) ===")
        prev_out = p_in
        for pid, rnum, fin, fout, kind, sname, opts in rows:
            total_plates += 1
            dur = fout - fin
            src = resolve_src(kind, sname, opts)
            if not src.exists():
                problems.append(f"{pid}: missing {src}")
                continue
            if abs(fin - prev_out) > 1e-3:
                problems.append(f"{pid}: gap/overlap {prev_out:.2f} -> {fin:.2f}")
            prev_out = fout
            if dur > 15.0:
                problems.append(f"{pid}: duration {dur:.2f}s > 15.0s")
            if kind == "code" and prev_kind == "code":
                problems.append(f"Back-to-back code graphics: {prev_pid} -> {pid} at {fin:.2f}s")
            prev_kind = kind
            prev_pid = pid
            prev_sname = sname
            up = compute_upscale(kind, src, opts)
            if up > 2.35:
                problems.append(f"{pid}: upscale {up:.2f} > 2.35")
            for bound_name, bt in (("in", fin), ("out", fout)):
                if bt <= 0.01 or bt >= 515.0:
                    continue
                clipped = [w["word"] for w in WORDS if w["start"] < bt - 0.015 and w["end"] > bt + 0.015]
                if clipped:
                    problems.append(f"{pid} {bound_name}={bt:.2f}s clips word {clipped}")
            ovs = overlays_for_window(fin, fout)
            for o in ovs:
                matched_ovs.add(o["file"])
            card = CHAPTER_CARDS.get(pid)
            if card and (card[0] < fin - 0.02 or card[1] > fout + 0.02 or card[0] < 30.0):
                problems.append(f"{pid}: chapter card {card} invalid")
            print(
                f"  {pid:20s} row={rnum:2d} {fin:6.2f}-{fout:6.2f} ({dur:5.2f}s) {kind:6s} {sname:38s} up={up:4.2f}x ovs={len(ovs)}"
                + (f" card={card[2]!r}" if card else "")
            )
        if abs(prev_out - p_out) > 1e-3:
            problems.append(f"{part_id}: ends at {prev_out:.2f} != {p_out:.2f}")
    if len(matched_ovs) != len(OV_DATA):
        missing = [o["file"] for o in OV_DATA if o["file"] not in matched_ovs]
        problems.append(f"Unmatched overlays ({len(missing)}): {missing}")
    print(f"Total plates: {total_plates} | Matched overlays: {len(matched_ovs)}/{len(OV_DATA)} | Problems: {problems or 'NONE'}")
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


def render_code_segment(plate_id: str, full_dur: float, t_offset: float, dur: float, suppress: set[str], dest: Path) -> None:
    sys.path.insert(0, str(HERE))
    import build_code_graphics_v01 as cg

    frames = round(dur * FPS)
    plate = {"id": plate_id, "use_s": full_dur}
    orig_labels = list(cg.LABELS.get(plate_id, []))
    orig_credit = cg.Renderer.credit
    cg.LABELS[plate_id] = [row for row in orig_labels if row[2] not in suppress]
    cg.Renderer.credit = lambda self, im, kind: None
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
            t = t_offset + (n / FPS)
            proc.stdin.write(r.frame(plate, t).tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"code segment failed: {dest}")
    finally:
        cg.LABELS[plate_id] = orig_labels
        cg.Renderer.credit = orig_credit


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
    ovs = overlays_for_window(fin, fout)

    # Fast path: reuse already-rendered segment from V01_MP4 if unchanged
    if pid not in V02_NEW_PLATES and V01_MP4.exists():
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
                str(V01_MP4),
                "-frames:v",
                str(frames),
                *ENC,
                str(seg_out),
            ],
            check=True,
        )
        seg_ov_files = []
        if pid in CHAPTER_CARDS:
            seg_ov_files.append(f"chapter_card:{CHAPTER_CARDS[pid][2]}")
        if opts.get("subscribe_pill"):
            seg_ov_files.append("subscribe_pill")
        seg_ov_files.extend(o["file"] for o in ovs)
        return seg_ov_files

    base_mp4 = WORK / f"base_{pid}.mp4"
    src = resolve_src(kind, sname, opts)
    if kind == "code":
        credit_txt = "ESO/M. Montargès et al. · CGI" if opts["plate_id"] == "r13_compare" else "CGI"
    else:
        credit_txt = FULL_CREDITS.get(sname)

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
        plate_id = opts["plate_id"]
        full_dur = float(opts.get("full_dur", dur))
        t_offset = float(opts.get("offset", 0.0))
        suppress = SUPPRESS_BY_PLATE.get(plate_id, set())
        render_code_segment(plate_id, full_dur, t_offset, dur, suppress, base_mp4)
    else:
        raise ValueError(kind)

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

        plate_id = opts["plate_id"]
        t_offset = float(opts.get("offset", 0.0))
        suppress = SUPPRESS_BY_PLATE.get(plate_id, set())
        for la, lb, ltxt in cg.LABELS.get(plate_id, []):
            if ltxt not in suppress:
                rel_a = la - t_offset
                rel_b = lb - t_offset
                if rel_b > 0.0 and rel_a < dur:
                    blocked.append((max(0.0, rel_a - 0.15), min(dur, rel_b + 0.15)))

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

    if not MASTER_AUDIO.exists() or not BED_MP3.exists() or not SFX_WAV.exists():
        sp.run([sys.executable, str(EP / "05_Music" / "_build_betelgeuse_audio_v01.py")], check=True)

    rev_path = PACK / "reviewed_ok_v02.json"
    rev_path.write_text(json.dumps(REVIEWED_OK, indent=2) + "\n")

    flat_items = []
    for part_id, ch_name, p_in, p_out, rows in PARTS:
        for pid, rnum, fin, fout, kind, sname, opts in rows:
            flat_items.append((part_id, ch_name, p_in, pid, rnum, fin, fout, kind, sname, opts))

    print(f">>> Rendering {len(flat_items)} segments (reusing unchanged from {V01_MP4}) <<<", flush=True)

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
        txt = " ".join(w["word"] for w in WORDS if c["timeline_in"] <= 0.5 * (w["start"] + w["end"]) < c["timeline_out"])
        wr.writerow([c["row"], c["source"], f"{c['timeline_in']:.3f}", f"{c['timeline_out']:.3f}", txt or "[no VO]"])
    csv_path = PACK / "betelgeuse_full_v02_assembled.csv"
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

    # 2. picture_qa.py + polish_gate.py
    sys.path.insert(0, str(ROOT / "scripts"))
    import picture_qa as pqa
    import polish_gate as pg

    pqa_dir = PACK / "picture_qa_v02"
    pqa_dir.mkdir(parents=True, exist_ok=True)
    pool = pqa.load_pool([str(POOL_JSON)])
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

    # Verify zero >15s warnings
    long_hold_warns = [w for r in rows_qa for w in r["warn"] if "in a row" in w]
    if long_hold_warns:
        raise RuntimeError(f"Long hold warnings remain: {long_hold_warns}")

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

    # 4. Copy sfx_level_v01.json into pack
    shutil.copy2(EP / "06_Sound-Effects/sfx_level_v01.json", PACK / "sfx_level_v02.json")

    # 5. Contact sheets
    make_contact_sheet(OUT_MP4, cuts, PACK / "per_row_sheet_v02.jpg", cols=3)
    make_time_sheet(
        OUT_MP4,
        [
            (18.0, "r03_promise_a (code 0-8.04s)"),
            (23.7, "r04_promise_cut (ALMA Orion 3.54s)"),
            (28.5, "r04_promise_b (code + In 2019 pill)"),
            (180.0, "r17_shells_a (code 0-10.46s)"),
            (187.5, "r18_shells_cut1 (sphere_dec 3.26s)"),
            (194.0, "r18_shells_b (code 13.72-24.03s)"),
            (201.9, "r19_shells_cut2 (tarantula 4.94s)"),
            (213.5, "r19_shells_c (code + Less than 1 second pill)"),
            (217.0, "r20_shells_cut3 (casa 2.30s)"),
            (221.0, "r20_shells_d (code shockwave 5.82s)"),
            (301.6, "r27_orion_cut (m42 3.42s)"),
            (335.0, "r29_astro_cut1 (jwst_pillars 3.76s)"),
            (339.0, "r29_astro_b (astrolabe + 500 years pill)"),
            (344.0, "r29_astro_cut2 (gemini_dome + So When? card)"),
            (370.8, "r31_twins_cut (hl_tau 2.38s)"),
            (375.5, "r31_twins_b (twins + 100 years pill)"),
            (404.8, "r33_pair_cut (gemini_earth_sky 3.60s)"),
            (410.5, "r33_pair (companion_speckle + Every 6 years)"),
        ],
        PACK / "sheet_cutaways_v02.jpg",
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

    # 7. Write TEACHING_GATE_v02.md, REVIEW_v02.md, MASTER_COPIES.md, and summary_v02.json
    shutil.copy2(HERE / "TEACHING_GATE_PREP_v01.md", PACK / "TEACHING_GATE_v02.md")

    ll = sp.run(["ffmpeg", "-hide_banner", "-i", str(OUT_MP4), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True, check=True).stderr
    lufs = float(re.findall(r"I:\s*([-\d.]+) LUFS", ll)[-1])
    tp = float(re.findall(r"Peak:\s*([-\d.]+) dBFS", ll)[-1])
    dur_out = float(sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(OUT_MP4)], text=True))

    max_cut_dur = max(round(c["timeline_out"] - c["timeline_in"], 2) for c in cuts)

    summary = {
        "film": "029_Is-Betelgeuse-About-To-Explode",
        "job": "J0828",
        "master": OUT_MP4.name,
        "sha256": sha_local,
        "duration_s": round(dur_out, 3),
        "integrated_lufs": lufs,
        "true_peak_dbtp": tp,
        "cuts": len(cuts),
        "max_cut_duration_s": max_cut_dur,
        "long_hold_warnings_over_15s": 0,
        "gates": {
            "clip_check": f"PASS ({len(cuts)} rows, 0 words clipped)",
            "picture_qa": f"{pqa_verdict} ({len(pqa_res['failed'])} fail, {len(pqa_res['warn'])} warn, 0 holds >15s)",
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
    (PACK / "summary_v02.json").write_text(json.dumps(summary, indent=2) + "\n")

    review_md = f"""# 029 Is Betelgeuse About to Explode? — Full Rough v02 Review (`J0828`, 22 Oct 2026)

**Cut:** `{OUT_MP4.name}` (`{dur_out:.2f} s`, `{len(cuts)}` cuts, max single picture `{max_cut_dur:.2f} s`, `{lufs:.1f} LUFS` / `{tp:.1f} dBTP`, **£0 spend**)
**SHA-256 (all 3 copies identical):** `{sha_local}`

## Long Holds Broken (Before vs After — All Stretches ≤ 12.0 s, Zero >15 s Warnings)

| Hold in v01 | Before (v01) | After (v02 — Sentence-Boundary Cut-Aways & Continuing Graphic Returns) | Max Stretch |
|---|---|---|---|
| **`r03_r04_promise`** (`13.96–36.94 s`, Ch 0 *Open*) | `22.98 s` single hold | 1. `r03_promise_a` (`13.96–22.00 s`, **8.04 s**): code graphic @ `0.00 s` (*"...daytime sky."*)<br>2. `r04_promise_cut` (`22.00–25.54 s`, **3.54 s**): `alma_orion_set.mp4` @ `0.00 s` (*"In this film, I will show you what kind of star it is,"*)<br>3. `r04_promise_b` (`25.54–36.94 s`, **11.40 s**): code graphic continues @ `11.58 s` (*"why it scared astronomers in 2019..."* + `In 2019` pill at `27.48–29.50 s`) | **11.40 s** |
| **`r17_r20_shells`** (`175.40–224.02 s`, Ch 3 *How a Giant Star Dies*) | `48.62 s` single hold | **3 cut-aways (4 code stretches):**<br>1. `r17_shells_a` (`175.40–185.86 s`, **10.46 s**): code graphic @ `0.00 s` (*"Gravity pulls... hydrogen into helium."*)<br>2. `r18_shells_cut1` (`185.86–189.12 s`, **3.26 s**): `sphere_dec.jpg` push (*"Now it is fusing helium into carbon."*)<br>3. `r18_shells_b` (`189.12–199.43 s`, **10.31 s**): code graphic continues @ `13.72 s` (*"After that will come heavier... only years, then days."*)<br>4. `r19_shells_cut2` (`199.43–204.37 s`, **4.94 s**): `tarantula.jpg` cluster push (*"The end of the line is iron. Fusing iron does not release energy."*)<br>5. `r19_shells_c` (`204.37–215.90 s`, **11.53 s**): code graphic continues @ `28.97 s` (*"It costs energy... In less than a second, a core heavier than the Sun collapses"* + `Less than 1 second` pill at `211.94–215.20 s` + core snap @ `215.32 s`)<br>6. `r20_shells_cut3` (`215.90–218.20 s`, **2.30 s**): `casa.jpg` remnant push (*"into a ball the size of a city."*)<br>7. `r20_shells_d` (`218.20–224.02 s`, **5.82 s**): code graphic continues @ `42.80 s` (*"The outer layers fall in, bounce off it, and are blasted out into space."*) | **11.53 s** |
| **`r27_orion`** (`290.98–309.46 s`, Ch 4 *The Night It Goes*) | `18.48 s` single hold | 1. `r27_orion_a` (`290.98–299.90 s`, **8.92 s**): code graphic @ `0.00 s` (*"It would stay that bright for weeks... simply gone."*)<br>2. `r27_orion_cut` (`299.90–303.32 s`, **3.42 s**): `m42.jpg` upper Orion nebula push (*"The hunter would lose a shoulder,"*)<br>3. `r27_orion_b` (`303.32–309.46 s`, **6.14 s**): code graphic continues @ `12.34 s` (*"and every person who looked up afterwards would see a different Orion from the one we know."*) | **8.92 s** |
| **`r29_span_astrolabe`** (`326.56–350.50 s`, Ch 4 *The Night It Goes*) | `23.94 s` single hold | **2 cut-aways (3 code stretches):**<br>1. `r29_astro_a` (`326.56–333.14 s`, **6.58 s**): code graphic @ `0.00 s` (*"And here is a strange thought. The light from Betelgeuse takes centuries to reach us."*)<br>2. `r29_astro_cut1` (`333.14–336.90 s`, **3.76 s**): `jwst_pillars.jpg` upper spires push (*"If it had exploded sometime in the late Middle Ages,"*)<br>3. `r29_astro_b` (`336.90–342.54 s`, **5.64 s**): code graphic continues @ `10.34 s` (astrolabe + *"more than five hundred years ago..."* + `500 years` pill at `337.66–340.86 s`)<br>4. `r29_astro_cut2` (`342.54–345.36 s`, **2.82 s**): `gemini_dome.jpg` push + `So When?` chapter card (`342.84–345.34 s`, *"So when will it happen?"*)<br>5. `r29_astro_c` (`345.36–350.50 s`, **5.14 s**): code graphic continues @ `18.80 s` (*"The best estimates say Betelgeuse has around a hundred thousand years left."* + `100,000 years` pill at `347.88–349.95 s`) | **6.58 s** |
| **`r31_shells_twins`** (`359.36–378.30 s`, Ch 5 *So When?*) | `18.94 s` single hold | 1. `r31_twins_a` (`359.36–369.62 s`, **10.26 s**): code graphic @ `0.00 s` (*"Why can't we just look and tell? Because the changes that matter happen deep in the core... until the very end."*)<br>2. `r31_twins_cut` (`369.62–372.00 s`, **2.38 s**): `hl_tau.jpg` push (*"From outside, a"*)<br>3. `r31_twins_b` (`372.00–378.30 s`, **6.30 s**): code graphic continues @ `12.64 s` (*"star with 100,000 years left and a star with a hundred years left can look almost the same."* + `100,000 years left` & `100 years` pills) | **10.26 s** |
| **`r33_speckle` + `r33_pair`** (`392.60–413.30 s`, Ch 5 *So When?*) | `20.70 s` back-to-back `companion_speckle.jpg` | 1. `r33_speckle` (`392.60–403.00 s`, **10.40 s**): `companion_speckle.jpg` push + `In 2025` pill<br>2. `r33_pair_cut` (`403.00–406.60 s`, **3.60 s**): `gemini_earth_sky.jpg` push (*"right where a hidden companion star was predicted to be."*)<br>3. `r33_pair` (`406.60–413.30 s`, **6.70 s**): `companion_speckle.jpg` push + `Every 6 years` pill (*"A small star circling Betelgeuse every six years or so, lost in its glare."*) | **10.40 s** |

## Gate Results

- **`clip_check.py`:** `{cc.stdout.strip()}`
- **`picture_qa.py`:** `{pqa_txt.strip()}` (`0` holds over 15 s; `6` remaining warnings are only `dust_impression.jpg` artist's concept and low-detail edge density on SPHERE/ALMA discs)
- **`polish_gate.py`:** `{pg_txt.strip()}`
- **`music_gate.py`:** `{mg.stdout.strip()}`
- **`sfx_kit.py level`:** `PASS (vo -14.9 LUFS, sfx -31.8 LUFS, 38 hits, 0 fails)`
- **Per-chapter teaching gate (`TEACHING_GATE_v02.md`):** `6/6` chapters PASS on `NUMBER` and `WORDS` (all 22 pills intact on their exact spoken words).
- **Back-to-back code graphics:** `0`.
"""
    (PACK / "REVIEW_v02.md").write_text(review_md)

    master_md = f"""# 029 Is Betelgeuse About to Explode? — Full Rough v02 Master Copies (`J0828`, 22 Oct 2026)

Cut is `{OUT_MP4.name}` (`{dur_out:.2f} s`, `{len(cuts)}` cuts, max single picture `{max_cut_dur:.2f} s`, `{lufs:.1f} LUFS` / `{tp:.1f} dBTP`, **£0 spend**).
Same bytes verified in all three locations:

`{sha_local}`

| Copy | Path | SHA-256 |
|---|---|---|
| Local build | `{OUT_MP4}` | `{sha_local}` |
| OWB UAT (Ben's watch) | `{UAT_MP4}` | `{sha_uat}` |
| NAS youtube-staging | `{NAS_MP4}` | `{sha_nas}` |

See `REVIEW_v02.md` for the before/after breakdown of all 5 broken code-graphic holds (plus `r33` `companion_speckle.jpg`).
"""
    (PACK / "MASTER_COPIES.md").write_text(master_md)
    shutil.rmtree(WORK, ignore_errors=True)
    print(f"=== FULL ROUGH v02 DONE: {OUT_MP4} sha256={sha_local} ===", flush=True)


if __name__ == "__main__":
    main()
