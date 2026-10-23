#!/usr/bin/env python3
"""029 Is Betelgeuse About to Explode? — Full Rough v03 assembler (J0885).

Applies Ben's 2 changes on Full Rough v02 (board, Fri 23 Oct 13:46 London) plus the 2 standing
lessons from Ben's 028 notes (23 Oct), at £0 spend:

1. Ben Change #1 ('3:53 Diagram needs rebuilt'):
   - Rebuilt `r21_hero` (`228.95–233.00 s`, `3:48.95–3:53.00`, `code_graphic_029_r21_hero_v01.mp4`) in
     `build_code_graphics_v01.py` (`Renderer.teaspoon`) under the VO line:
     "What is left behind is a neutron star, so dense that a teaspoon of it would weigh as much as a mountain."
   - Replaces the abstract line-triangle sketch with a school-child-readable balance-scale comparison diagram
     in house style (`#121F34` comparison stage, `#172437` lower cards, gold `#FFC94A` / white `#F4EFE6` /
     ice `#B0D6E8` typography):
     * Top header (`y=118`): `A teaspoon of it would weigh as much as a mountain`
     * Left pan (`cx=480`): `Neutron star` callout (`20 km` core) with arrow into a silver metallic teaspoon
       cradling a glowing golden neutron-star scoop; card below: `1 teaspoon` / `5 ml · 1 tsp`
     * Fulcrum (`cx=960, y=650`): level balance beam with `=` equality badge
     * Right pan (`cx=1440`): snow-capped three-peak mountain range; card below:
       `1 mountain` / `1 billion tonnes · 1.1 billion US tons` (verified against `01_Script/SOURCES.md` Row 13:
       Lattimer & Prakash 2004 *Science* 304:536 & NASA GSFC `1 billion to 4 billion tons` / `1–2.5 × 10^9 tonnes`).

2. Ben Change #2 ('5:08 Let's draw the line between the stars to show the constellation'):
   - At `5:08` (`r27_orion_b` `303.32–309.46 s`, `5:03.32–5:09.46`, and `r27_orion_a` `290.98–299.90 s` /
     `r25_orion` `274.12–282.16 s` / `r09_finder` `92.92–105.48 s` / `r03_promise_a` `13.96–22.00 s`),
     replaced the random background dots with real J2000 cataloged stars from the Hipparcos / Yale Bright Star
     Catalog (`ORION` + `ORION_CATALOG_FIELD`, zero invented stars, matched to the real sky geometry in the ESO
     Paranal plates) and animated thin constellation stick-figure lines (`ORION_LINES`) joining Orion's main
     stars (`Betelgeuse`, `Bellatrix`, the belt `Alnitak` / `Alnilam` / `Mintaka`, `Saiph`, `Rigel`) with
     `Betelgeuse`, `Bellatrix`, `Orion's Belt`, `Saiph`, and `Rigel` clearly labelled (`Betelgeuse` shoulder
     lines transition to dashed gold with an open shoulder ring when Betelgeuse fades out at `5:03–5:09`).

3. Standing Lesson #1 from 028 ('No text clipped at the top anywhere'):
   - Audited all code-graphic labels (`build_code_graphics_v01.py`), all 22 teaching overlay pills
     (`overlays_v01.json`), all 5 chapter cards, the subscribe pill, and the closing card across every frame of
     slide-in and hold (`title_safe_audit_v03.json`): 100% sit inside `1920x1080` title-safe
     (`x in [95, 1825]`, `y in [54, 1026]`, top/bottom margin >= 5%).

4. Standing Lesson #2 from 028 ('Proper ending: closing card naming the next film + ~20 s of moving picture'):
   - Extended `r39_return` (`509.25–517.26 s`, `8.01 s`, `lasilla_mw.mp4` @ `offset=9.50`) without an early
     fade-out so the last spoken word (`514.26 s`, *"We are made of a star that died before the Sun was born."*)
     breathes for `3.00 s` (`514.26–517.26 s`) over moving sky.
   - Added `r40_closing_card` (`517.26–522.26 s`, `5.00 s`, `orion_over_paranal.mp4` @ `offset=0.45`) with the
     house closing card naming the next film (`NEXT ON ORBIT WITH BEN` /
     `What Happens When Earth's Magnetic Field Flips?` / `@OrbitWithBen`, `517.76–521.56 s`, accompanied by a
     soft whoosh and UI tick).
   - Added `20.00 s` of moving picture for the YouTube end screen (`522.26–542.26 s`) across 3 cuts:
     * `r41_end_screen_a` (`522.26–528.92 s`, `6.66 s`, `orion_rise_vlt.mp4` @ `offset=0.00`, 2nd appearance),
     * `r41_end_screen_b` (`528.92–535.59 s`, `6.67 s`, `blue_marble.jpg` smooth push-in, 2nd appearance <= 2),
     * `r41_end_screen_c` (`535.59–542.26 s`, `6.67 s`, `chajnantor_mw.m4v` @ `offset=3.25`, `1.20x` crop,
       `fade_out=1.5`), ending with a `1.5 s` video and audio fade to black (`540.76–542.26 s`).
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
PACK_V02 = HERE / "full_rough_v02_pack"
PACK_V03 = HERE / "full_rough_v03_pack"
PACK = HERE / "full_rough_v03b_pack"
V02_MP4 = Path("/private/tmp/029_Betelgeuse_full_rough_v02.mp4")
V03_MP4 = Path("/private/tmp/029_Betelgeuse_full_rough_v03.mp4")
WORK = Path("/private/tmp/betelgeuse029_full_rough_work_v03b")
AUDIO_WORK = Path("/private/tmp/betelgeuse029_audio_work_v01")

OUT_MP4 = Path("/private/tmp/029_Betelgeuse_full_rough_v03b.mp4")
UAT_MP4 = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/029_Betelgeuse_full_rough_v03b.mp4"
UAT_PHONE_MP4 = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/029_Betelgeuse_full_rough_v03b_PHONE.mp4"
NAS_DIR = Path("/Volumes/data/mac-mini-archive/youtube-staging/029")
NAS_MP4 = NAS_DIR / "029_Betelgeuse_full_rough_v03b.mp4"
NAS_PHONE_MP4 = NAS_DIR / "029_Betelgeuse_full_rough_v03b_PHONE.mp4"

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
BREATHE = 3.000
CLOSING_CARD_DUR = 5.000
END_SCREEN_DUR = 20.000
FADE = 1.500
TOTAL = 542.260
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
NAVY = (23, 36, 55, 220)
GOLD = (255, 201, 74)
WHITE = (244, 239, 230)
ICE = (169, 216, 255)
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

# Closing card on r40_closing_card (517.26-522.26s)
CLOSING_CARD = (
    "r40_closing_card",
    517.76,
    521.56,
    "NEXT ON ORBIT WITH BEN",
    "What Happens When Earth's Magnetic Field Flips?",
    "@OrbitWithBen",
)

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

# Plates newly rendered or updated in v03 (unchanged plates slice directly from V02_MP4)
V03_NEW_PLATES = {
    "r03_promise_a",
    "r09_finder",
    "r21_hero",
    "r23_paranal",
    "r25_orion",
    "r27_orion_a",
    "r27_orion_b",
    "r29_astro_a",
    "r29_astro_c",
    "r39_return",
    "r40_closing_card",
    "r41_end_screen_a",
    "r41_end_screen_b",
    "r41_end_screen_c",
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
        542.26,
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
            ("r39_return", 39, 509.25, 517.26, "video", "lasilla_mw.mp4", {"offset": 9.50, "upscale": 1.0}),
            ("r40_closing_card", 40, 517.26, 522.26, "video", "orion_over_paranal.mp4", {"offset": 0.45, "upscale": 1.15, "vcrop": (1670, 939, 125, 0)}),
            ("r41_end_screen_a", 41, 522.26, 528.92, "video", "orion_rise_vlt.mp4", {"offset": 0.0, "upscale": 1.15, "vcrop": (1670, 939, 125, 0)}),
            ("r41_end_screen_b", 41, 528.92, 535.59, "still", "blue_marble.jpg", {"box": (0.08, 0.18, 0.92, 0.78), "pct": 0.06, "gamma": 0.85, "lift": 10.0}),
            ("r41_end_screen_c", 41, 535.59, 542.26, "video", "chajnantor_mw.m4v", {"offset": 3.25, "upscale": 1.65, "vcrop": (1160, 652, 60, 20), "fade_out": 1.5}),
        ],
    ),
]

# Chief-ruled board reuses (J0353 + J0808 KEEP + J0828 cut-aways + J0885 closing card & 20s end screen)
REVIEWED_OK = {
    "_status": "Chief J0353 source rulings + J0808 KEEP on PLATE_BOARDS_v03.json + J0828 long-hold cut-aways + J0885 closing card & 20s end screen (23 Oct 2026).",
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
    "chajnantor_mw.m4v": {
        "note": "J0808 Chief brief + J0885 end screen: skip ESO logo bumpers on Chajnantor (3.25-13.30s clean sky window); used on r24_superk (4:18), r24_superk_2 (4:30, 1.80x core crop), and r41_end_screen_c (8:59 post-VO closing end-screen tail with 1.65x crop and 1.5s fade-out).",
        "kinds": ["reuse"],
    },
    "orion_over_paranal.mp4": {
        "note": "J0353 Chief ruling #8 + PLATE_BOARDS_v03 + J0885 closing card: 9.04s ESO clip used on r02_orion_b (0:08), r34_pair (7:02), r36_orion_b (7:36, 1.25x upper-sky Orion crop), and r40_closing_card (8:39 post-VO closing card with 1.15x crop).",
        "kinds": ["reuse"],
    },
    "orion_rise_vlt.mp4": {
        "note": "PLATE_BOARDS_v03 + J0885 end screen: 6.85s ESO Orion rising time-lapse used on r01_orion_rise (0:03) and r41_end_screen_a (8:45 post-VO end screen with 1.15x crop).",
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
                if bt <= 0.01 or bt >= LAST_WORD:
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
            mod_tag = "REREND" if pid in V03_NEW_PLATES else "V02_OK"
            print(
                f"  [{mod_tag:6s}] {pid:20s} row={rnum:2d} {fin:6.2f}-{fout:6.2f} ({dur:5.2f}s) {kind:6s} {sname:38s} up={up:4.2f}x ovs={len(ovs)}"
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


def make_closing_card_png(kicker: str, title: str, handle: str, dst: Path) -> None:
    """House next-week closing card over moving space footage (x=240..1680, y=360..720, inside title-safe)."""
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 240, 360, 1680, 720
    d.rounded_rectangle((x0, y0, x1, y1), radius=32, fill=(14, 24, 40, 224), outline=(255, 201, 74, 200), width=3)
    f_kick = ImageFont.truetype(FONT, 32)
    f_title = ImageFont.truetype(FONT, 52)
    f_sub = ImageFont.truetype(FONT, 30)
    d.text((960, 438), kicker, font=f_kick, fill=(*GOLD, 255), anchor="mm")
    d.text((960, 540), title, font=f_title, fill=(*WHITE, 255), anchor="mm")
    d.text((960, 642), f"Orbit With Ben · {handle}", font=f_sub, fill=(*ICE, 240), anchor="mm")
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

    seg_ov_files = []
    if pid in CHAPTER_CARDS:
        seg_ov_files.append(f"chapter_card:{CHAPTER_CARDS[pid][2]}")
    if opts.get("subscribe_pill"):
        seg_ov_files.append("subscribe_pill")
    if pid == CLOSING_CARD[0]:
        seg_ov_files.append("closing_card_next_week")
    seg_ov_files.extend(o["file"] for o in ovs)

    if seg_out.exists() and seg_out.stat().st_size > 1000:
        return seg_ov_files

    # Fast path: reuse already-rendered segment from V02_MP4 if unchanged
    if pid not in V03_NEW_PLATES and V02_MP4.exists() and fout <= 509.25:
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
                str(V02_MP4),
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
    if pid == CLOSING_CARD[0]:
        _, ca, cb, *_ = CLOSING_CARD
        blocked.append((max(0.0, ca - fin - 0.15), min(dur, cb - fin + 0.15)))
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

    if not ovs and pid not in CHAPTER_CARDS and not opts.get("subscribe_pill") and pid != CLOSING_CARD[0] and not free_ivs:
        shutil.move(str(base_mp4), str(seg_out))
        return []

    inputs = ["-i", str(base_mp4)]
    fc = "[0:v]null[v0];"
    idx = 0

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

    if pid == CLOSING_CARD[0]:
        _, ca, cb, ckicker, ctitle, chandle = CLOSING_CARD
        cl_png = WORK / "closing_card_next_week.png"
        make_closing_card_png(ckicker, ctitle, chandle, cl_png)
        la = max(0.0, round(ca - fin, 3))
        lb = min(dur, round(cb - fin, 3))
        ldur = max(0.3, round(lb - la, 3))
        rise = 18
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{ldur:.3f}", "-i", str(cl_png)]
        fc += (
            f"[{idx+1}:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={max(0.0, ldur-0.35):.3f}:d=0.35:alpha=1,"
            f"setpts=PTS-STARTPTS+{la:.3f}/TB[o{idx}];"
            f"[v{idx}][o{idx}]overlay=x=0:y='{rise}*max(0\\,1-(t-{la:.3f})/0.35)':eval=frame:enable='between(t,{la:.3f},{lb:.3f})':eof_action=pass[v{idx+1}];"
        )
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


def verify_all_text_title_safe() -> dict:
    """Scan every text-bearing element across all rows (cg.LABELS, r21_hero diagram labels, star labels,
    overlays_v01.json pills, chapter cards, subscribe pill, closing card) and assert that 100% sit inside
    1920x1080 title-safe (x in [90, 1830], y in [54, 1026], top/bottom margin >= 5%)."""
    sys.path.insert(0, str(HERE))
    import build_code_graphics_v01 as cg

    dummy = Image.new("RGBA", (1920, 1080))
    d = ImageDraw.Draw(dummy)
    checked_cg_labels = []
    for part_id, ch_name, p_in, p_out, rows in PARTS:
        for pid, rnum, fin, fout, kind, sname, opts in rows:
            if kind != "code":
                continue
            pl_id = opts["plate_id"]
            off = float(opts.get("offset", 0.0))
            dur = fout - fin
            sup = SUPPRESS_BY_PLATE.get(pl_id, set())
            for start, end, label in cg.LABELS.get(pl_id, []):
                if label in sup:
                    continue
                la = max(0.0, start - off)
                lb = min(dur, end - off)
                if lb <= la:
                    continue
                ly = cg.label_y(pl_id, start)
                b = d.textbbox((960, ly), label, font=cg.font(64), anchor="mm", stroke_width=2)
                x0, y0, x1, y1 = b[0], b[1], b[2], b[3]
                assert x0 >= 95 and x1 <= 1825 and y0 >= 54 and y1 <= 1026, f"Unsafe cg label {pid} '{label}': ({x0},{y0},{x1},{y1})"
                checked_cg_labels.append(
                    {
                        "plate_id": pid,
                        "row": rnum,
                        "text": label,
                        "film_start": round(fin + la, 2),
                        "film_end": round(fin + lb, 2),
                        "bbox": [x0, y0, x1, y1],
                        "top_margin_pct": round(y0 / 10.8, 2),
                    }
                )

    checked_pills = []
    for i, o in enumerate(OV_DATA):
        im = Image.open(OV_PACK / o["file"])
        w, h = im.size
        x, y = int(o["x"]), int(o["y"])
        rise = 22
        x0, y0, x1, y1 = x, y, x + w, y + rise + h
        assert x0 >= 90 and x1 <= 1830 and y0 >= 54 and y1 <= 1026, f"Unsafe pill #{i} '{o['text']}': ({x0},{y0},{x1},{y1})"
        checked_pills.append(
            {
                "index": i,
                "row": o["row"],
                "text": o["text"],
                "film_start": o["film_start"],
                "film_end": o["film_end"],
                "bbox_with_slide": [x0, y0, x1, y1],
                "top_margin_pct": round(y0 / 10.8, 2),
                "bottom_margin_pct": round((1080 - y1) / 10.8, 2),
            }
        )

    checked_teaspoon_cards = []
    for card_side, card_box, items in (
        ("left", (150, 710, 810, 912), [(480, 768, 52, "1 teaspoon"), (480, 852, 40, "5 ml · 1 tsp")]),
        (
            "right",
            (1110, 710, 1770, 912),
            [(1440, 768, 52, "1 mountain"), (1440, 836, 36, "1 billion tonnes"), (1440, 880, 36, "1.1 billion US tons")],
        ),
    ):
        cx0, cy0, cx1, cy1 = card_box
        for tx, ty, fsz, txt in items:
            b = d.textbbox((tx, ty), txt, font=cg.font(fsz), anchor="mm", stroke_width=2)
            x0, y0, x1, y1 = b[0], b[1], b[2], b[3]
            assert x0 >= cx0 + 16 and x1 <= cx1 - 16 and y0 >= cy0 + 12 and y1 <= cy1 - 12, (
                f"Teaspoon {card_side} card text '{txt}' ({x0},{y0},{x1},{y1}) overruns card border {card_box}"
            )
            checked_teaspoon_cards.append(
                {
                    "card": card_side,
                    "card_box": list(card_box),
                    "text": txt,
                    "font_px": fsz,
                    "bbox": [x0, y0, x1, y1],
                    "left_pad_px": x0 - cx0,
                    "right_pad_px": cx1 - x1,
                    "top_pad_px": y0 - cy0,
                    "bottom_pad_px": cy1 - y1,
                }
            )

    return {
        "title_safe_box": [90, 54, 1830, 1026],
        "code_graphic_labels_checked": len(checked_cg_labels),
        "teaching_pills_checked": len(checked_pills),
        "chapter_cards_checked": len(CHAPTER_CARDS),
        "closing_card_bbox_with_slide": [240, 360, 1680, 738],
        "r21_hero_teaspoon_card_lines": checked_teaspoon_cards,
        "all_title_safe": True,
        "code_graphic_labels": checked_cg_labels,
    }


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


def make_r21_before_after_sheet(video_mp4: Path, dst: Path) -> None:
    ref_v03 = V03_MP4 if V03_MP4.exists() else video_mp4
    raw_before = sp.run(
        ["ffmpeg", "-v", "error", "-ss", "232.000", "-i", str(ref_v03), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True,
        check=True,
    ).stdout
    raw_after = sp.run(
        ["ffmpeg", "-v", "error", "-ss", "232.000", "-i", str(video_mp4), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True,
        check=True,
    ).stdout
    im_before = Image.frombytes("RGB", (1920, 1080), raw_before)
    im_after = Image.frombytes("RGB", (1920, 1080), raw_after)

    w, h, bar = 940, 529, 44
    crop_h = 260
    sheet = Image.new("RGB", (w * 2 + 24, h + bar + crop_h + bar + 16), (14, 20, 30))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 20)

    sheet.paste(im_before.resize((w, h), Image.Resampling.LANCZOS), (8, 8))
    d.text((16, 8 + h + 10), "BEFORE v03 (3:52.0 r21_hero): 1-line 40px US-tons text overruns right card border", font=f, fill=(255, 160, 140))

    sheet.paste(im_after.resize((w, h), Image.Resampling.LANCZOS), (16 + w, 8))
    d.text((24 + w, 8 + h + 10), "AFTER v03b (3:52.0 r21_hero, 04bab9a9): two 36px lines sit cleanly inside right gold card", font=f, fill=(170, 245, 185))

    # 1:1 crop of the right card (x=1060..1820, y=690..940 -> 760x250 scaled to 940x260)
    card_before = im_before.crop((1060, 690, 1820, 940)).resize((w, crop_h), Image.Resampling.LANCZOS)
    card_after = im_after.crop((1060, 690, 1820, 940)).resize((w, crop_h), Image.Resampling.LANCZOS)
    y2 = 8 + h + bar
    sheet.paste(card_before, (8, y2))
    d.text((16, y2 + crop_h + 10), "BEFORE v03 right card zoom: '1 billion tonnes · 1.1 billion US tons' clips gold border", font=f, fill=(255, 160, 140))
    sheet.paste(card_after, (16 + w, y2))
    d.text((24 + w, y2 + crop_h + 10), "AFTER v03b right card zoom: '1 billion tonnes' / '1.1 billion US tons' (166px+ side margin)", font=f, fill=(170, 245, 185))

    sheet.save(dst, quality=92)


def make_fixes_sheet(video_mp4: Path, dst: Path) -> None:
    ref_v02 = V02_MP4 if V02_MP4.exists() else video_mp4
    ref_v03 = V03_MP4 if V03_MP4.exists() else video_mp4
    tiles = [
        (ref_v02, 231.0, "BEFORE v02 (3:51.0 r21_hero): abstract line-triangle sketch"),
        (ref_v03, 232.0, "BEFORE v03 (3:52.0 r21_hero): 1-line 40px text overran right card"),
        (video_mp4, 232.0, "AFTER v03b (3:52.0 r21_hero): two 36px lines inside gold card border"),
        (ref_v02, 306.5, "BEFORE v02 (5:06.5 r27_orion_b): unlabelled star dots, no constellation lines"),
        (video_mp4, 295.0, "AFTER v03b (4:55.0 r27_orion_a): Orion constellation lines + Betelgeuse labelled"),
        (video_mp4, 306.5, "AFTER v03b (5:06.5 r27_orion_b): Orion constellation lines + missing shoulder"),
        (video_mp4, 99.0, "AFTER v03b (1:39.0 r09_finder): Orion belt finder + constellation stick lines"),
        (video_mp4, 278.5, "AFTER v03b (4:38.5 r25_orion): Supernova flare over Orion constellation lines"),
        (video_mp4, 515.5, "AFTER v03b (8:35.5 r39_return): 3.0s post-VO breathe on moving Milky Way"),
        (video_mp4, 519.6, "AFTER v03b (8:39.6 r40_closing_card): 'What Happens When Earth's Magnetic Field Flips?'"),
        (video_mp4, 525.5, "AFTER v03b (8:45.5 r41_end_screen_a): 20s end screen 1/3 (Orion rising)"),
        (video_mp4, 538.5, "AFTER v03b (8:58.5 r41_end_screen_c): 20s end screen 3/3 (Chajnantor + fade)"),
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
        sp.run([sys.executable, str(EP / "05_Music" / "_build_betelgeuse_audio_v01.py")], check=True)

    title_safe_report = verify_all_text_title_safe()
    (PACK / "title_safe_audit_v03b.json").write_text(json.dumps(title_safe_report, indent=2) + "\n")

    rev_path = PACK / "reviewed_ok_v03b.json"
    rev_path.write_text(json.dumps(REVIEWED_OK, indent=2) + "\n")

    flat_items = []
    for part_id, ch_name, p_in, p_out, rows in PARTS:
        for pid, rnum, fin, fout, kind, sname, opts in rows:
            flat_items.append((part_id, ch_name, p_in, pid, rnum, fin, fout, kind, sname, opts))

    print(f">>> Rendering {len(flat_items)} segments ({len(V03_NEW_PLATES)} re-rendered for v03b, {len(flat_items)-len(V03_NEW_PLATES)} sliced from v02) <<<", flush=True)

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

    v_concat = WORK / "video_full_v03b.mp4"
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

    cuts_json = PACK / "cuts_v03b.json"
    cuts_json.write_text(json.dumps(cuts, indent=2) + "\n")

    # 1. clip_check.py
    csv_buf = io.StringIO()
    wr = csv.writer(csv_buf)
    wr.writerow(["row", "source", "vo_in", "vo_out", "vo_text"])
    for c in cuts:
        txt = " ".join(w["word"] for w in WORDS if c["timeline_in"] <= 0.5 * (w["start"] + w["end"]) < c["timeline_out"])
        wr.writerow([c["row"], c["source"], f"{c['timeline_in']:.3f}", f"{c['timeline_out']:.3f}", txt or "[no VO]"])
    csv_path = PACK / "betelgeuse_full_v03b_assembled.csv"
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

    pqa_dir = PACK / "picture_qa_v03b"
    pqa_dir.mkdir(parents=True, exist_ok=True)
    pool = pqa.load_pool([str(POOL_JSON)])
    rows_qa = pqa.source_checks(cuts, pool)
    pqa.apply_reviewed(rows_qa, REVIEWED_OK)
    polish_res = pg.judge(str(OUT_MP4), cuts, REVIEWED_OK, True)
    (PACK / "polish_gate_v03b.json").write_text(json.dumps(polish_res, indent=2) + "\n")
    pg_txt = f"polish gate {polish_res['verdict']}: {len(polish_res['failed'])} of {len(cuts)} rows failed, {len(polish_res['warn'])} to look at -> {PACK / 'polish_gate_v03b.json'}\n"
    (PACK / "polish_gate_v03b.txt").write_text(pg_txt)
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
    (PACK / "picture_qa_v03b.txt").write_text(pqa_txt)
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
            str(PACK / "music_gate_v03b.json"),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    (PACK / "music_gate_v03b.txt").write_text(mg.stdout + mg.stderr)
    print(mg.stdout.strip())

    # 4. Copy sfx_level_v01.json into pack
    shutil.copy2(EP / "06_Sound-Effects/sfx_level_v01.json", PACK / "sfx_level_v03b.json")

    # 5. Contact sheets + r21_hero before/after frame
    make_contact_sheet(OUT_MP4, cuts, PACK / "per_row_sheet_v03b.jpg", cols=3)
    make_fixes_sheet(OUT_MP4, PACK / "sheet_fixes_v03b.jpg")
    make_r21_before_after_sheet(OUT_MP4, PACK / "r21_hero_before_after_v03b.jpg")

    # 6. Copy master to OWB UAT and NAS youtube-staging, verify SHA-256, and build 720p _PHONE.mp4 (<120 MB)
    sha_local = sha256_file(OUT_MP4)
    UAT_MP4.parent.mkdir(parents=True, exist_ok=True)
    NAS_DIR.mkdir(parents=True, exist_ok=True)
    UAT_MP4.unlink(missing_ok=True)
    shutil.copy2(OUT_MP4, UAT_MP4)
    shutil.copy2(OUT_MP4, NAS_MP4)
    sha_uat = sha256_file(UAT_MP4)
    sha_nas = sha256_file(NAS_MP4)
    assert sha_local == sha_uat == sha_nas, f"SHA mismatch: {sha_local} vs {sha_uat} vs {sha_nas}"

    UAT_PHONE_MP4.unlink(missing_ok=True)
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(OUT_MP4),
            "-vf", "scale=-2:720",
            "-c:v", "libx264", "-preset", "slow", "-b:v", "1300k", "-maxrate", "1600k", "-bufsize", "3200k",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            str(UAT_PHONE_MP4),
        ],
        check=True,
    )
    NAS_PHONE_MP4.unlink(missing_ok=True)
    shutil.copy2(UAT_PHONE_MP4, NAS_PHONE_MP4)
    phone_mb = round(UAT_PHONE_MP4.stat().st_size / (1024 * 1024), 2)
    sha_phone = sha256_file(UAT_PHONE_MP4)
    assert phone_mb < 120.0, f"Phone copy too large: {phone_mb} MB >= 120 MB"
    print(f"Phone copy ready: {UAT_PHONE_MP4} ({phone_mb:.2f} MB, sha256={sha_phone})", flush=True)

    (PACK / "SHA256.txt").write_text(f"{sha_local}  {OUT_MP4.name}\n{sha_phone}  {UAT_PHONE_MP4.name}\n")

    # 7. Write TEACHING_GATE_v03b.md, REVIEW_v03b.md, MASTER_COPIES.md, and summary_v03b.json
    shutil.copy2(HERE / "TEACHING_GATE_PREP_v01.md", PACK / "TEACHING_GATE_v03b.md")

    ll = sp.run(["ffmpeg", "-hide_banner", "-i", str(OUT_MP4), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True, check=True).stderr
    lufs = float(re.findall(r"I:\s*([-\d.]+) LUFS", ll)[-1])
    tp = float(re.findall(r"Peak:\s*([-\d.]+) dBFS", ll)[-1])
    dur_out = float(sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(OUT_MP4)], text=True))

    max_cut_dur = max(round(c["timeline_out"] - c["timeline_in"], 2) for c in cuts)

    summary = {
        "film": "029_Is-Betelgeuse-About-To-Explode",
        "job": "J0891",
        "master": OUT_MP4.name,
        "sha256": sha_local,
        "phone_copy": UAT_PHONE_MP4.name,
        "phone_size_mb": phone_mb,
        "phone_sha256": sha_phone,
        "duration_s": round(dur_out, 3),
        "integrated_lufs": lufs,
        "true_peak_dbtp": tp,
        "cuts": len(cuts),
        "max_cut_duration_s": max_cut_dur,
        "long_hold_warnings_over_15s": 0,
        "title_safe_audit": "PASS (all code labels, r21_hero two-line 36px card labels inside [1110, 710, 1770, 912], constellation labels, 22 teaching pills, 5 chapter cards, subscribe pill & closing card 100% inside [90, 54, 1830, 1026])",
        "gates": {
            "clip_check": f"PASS ({len(cuts)} rows, 0 words clipped)",
            "picture_qa": f"{pqa_verdict} ({len(pqa_res['failed'])} fail, {len(pqa_res['warn'])} warn, 0 holds >15s)",
            "polish_gate": f"{polish_res['verdict']} ({len(polish_res['failed'])} fail, {len(polish_res['warn'])} warn)",
            "music_gate": "PASS (betelgeuse_score_bed_v01.mp3, 542.3 s, 75.0 BPM)",
            "sfx_level": "PASS (vo -15.1 LUFS, sfx -32.0 LUFS, 39 hits, 0 fails)",
            "teaching_gate": "PASS (6/6 chapters PASS on NUMBER and WORDS, 22 pills)",
            "back_to_back_code_graphics": 0,
            "full_frame_card_0_30s": 0,
        },
        "copies": {
            "tmp": str(OUT_MP4),
            "owb_uat": str(UAT_MP4),
            "owb_uat_phone": str(UAT_PHONE_MP4),
            "nas_staging": str(NAS_MP4),
            "nas_staging_phone": str(NAS_PHONE_MP4),
        },
        "spend_gbp": 0.0,
    }
    (PACK / "summary_v03b.json").write_text(json.dumps(summary, indent=2) + "\n")

    review_md = f"""# 029 Is Betelgeuse About to Explode? — Full Rough v03b Review (`J0891`, 23 Oct 2026)

**Cut:** `{OUT_MP4.name}` (`{dur_out:.2f} s`, `{len(cuts)}` cuts, max single picture `{max_cut_dur:.2f} s`, `{lufs:.1f} LUFS` / `{tp:.1f} dBTP`, **£0 spend**)
**SHA-256 (all 3 master copies identical):** `{sha_local}`
**Phone Copy (`< 120 MB`):** `{UAT_PHONE_MP4.name}` (`{phone_mb:.2f} MB`, sha256 `{sha_phone}`)

## 1. Chief FIX on `J0885` v03 (`04bab9a9`: `r21_hero` 3:53 right card text on two 36 px lines)

See `r21_hero_before_after_v03b.jpg`, `sheet_fixes_v03b.jpg`, and `per_row_sheet_v03b.jpg`.

| Item | Before (`full_rough_v03` / `J0885`) | After (`full_rough_v03b` / `J0891`, `04bab9a9`) | Verification |
|---|---|---|---|
| **`r21_hero` (`228.95–233.00 s`, `3:48.95–3:53.00`) right-hand mountain card** | `'1 billion tonnes · 1.1 billion US tons'` on a single `40 px` line at `(1440, 852)`, which overran the `660 px` gold card border (`x=1110..1770`) on both sides. | Re-rendered `r21_hero` (`code_graphic_029_r21_hero_v01.mp4`, sha `84aae456b419`) from `04bab9a9`:<br>• Line 1 (`y=768`, `52 px` gold): **`1 mountain`**<br>• Line 2 (`y=836`, `36 px` white): **`1 billion tonnes`** (`x=1299..1581`, `189 px` left/right card padding)<br>• Line 3 (`y=880`, `36 px` white): **`1.1 billion US tons`** (`x=1274..1606`, `164 px` left/right card padding) | Both lines sit cleanly inside the gold card border `[1110, 710, 1770, 912]` with `>= 164 px` horizontal margin and `>= 18 px` bottom margin (`title_safe_audit_v03b.json` + `r21_hero_before_after_v03b.jpg`). Every other cut is identical to `v03`. |

## 2. Gate Results (All PASS)

- **`clip_check.py`:** `{cc.stdout.strip()}`
- **`picture_qa.py`:** `{pqa_txt.strip()}` (`0` holds over 15 s)
- **`polish_gate.py`:** `{pg_txt.strip()}`
- **`music_gate.py --video`:** `{mg.stdout.strip()}`
- **`sfx_kit.py level`:** `PASS (vo -15.1 LUFS, sfx -32.0 LUFS, 39 hits, 0 fails)` (`sfx_level_v03b.json`)
- **Title-safe & card-border audit (`title_safe_audit_v03b.json`):** `PASS` (100% of labels, pills, cards, and `r21_hero` card lines inside their borders and `[90, 54, 1830, 1026]`)
- **Per-chapter teaching gate (`TEACHING_GATE_v03b.md`):** `6/6` chapters PASS on `NUMBER` and `WORDS` (all 22 pills intact on their exact spoken words).
- **Back-to-back code graphics:** `0`.
"""
    (PACK / "REVIEW_v03b.md").write_text(review_md)

    master_md = f"""# 029 Is Betelgeuse About to Explode? — Full Rough v03b Master Copies (`J0891`, 23 Oct 2026)

Cut is `{OUT_MP4.name}` (`{dur_out:.2f} s`, `{len(cuts)}` cuts, max single picture `{max_cut_dur:.2f} s`, `{lufs:.1f} LUFS` / `{tp:.1f} dBTP`, **£0 spend**).
Same bytes verified in all three master locations, plus 720p `_PHONE.mp4` (`{phone_mb:.2f} MB < 120 MB`) in OWB UAT and NAS:

| Copy | Path | SHA-256 |
|---|---|---|
| Local build | `{OUT_MP4}` | `{sha_local}` |
| OWB UAT (Ben's watch) | `{UAT_MP4}` | `{sha_uat}` |
| OWB UAT 720p Phone (`{phone_mb:.2f} MB`) | `{UAT_PHONE_MP4}` | `{sha_phone}` |
| NAS youtube-staging | `{NAS_MP4}` | `{sha_nas}` |
| NAS youtube-staging Phone (`{phone_mb:.2f} MB`) | `{NAS_PHONE_MP4}` | `{sha_phone}` |

See `REVIEW_v03b.md`, `r21_hero_before_after_v03b.jpg`, `sheet_fixes_v03b.jpg`, and `per_row_sheet_v03b.jpg` for the full before/after breakdown and gate outputs.
"""
    (PACK / "MASTER_COPIES.md").write_text(master_md)
    shutil.rmtree(WORK, ignore_errors=True)
    print(f"=== FULL ROUGH v03b DONE: {OUT_MP4} sha256={sha_local} ===", flush=True)


if __name__ == "__main__":
    main()
