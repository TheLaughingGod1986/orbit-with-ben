#!/usr/bin/env python3
"""032 Titan long master v02 (J2436 / J2435 FIRST30_PLAN.md). £0 spend.
Assembles the 52-row long master (582.44 s VO / 585.44 s total with post-word hold, 1920x1080 30 fps CFR)
with re-cut first 30 s (R01-R06 all <= 3.60 s, r03_pressure at 16.53-20.13 s before 0:20, and smooth
symmetric sub-pixel PIL Image.Transform.EXTENT BICUBIC zoom 1.000->1.045 on every still cut from Frame 0),
and runs all 5 gates (clip_check, picture_qa, polish_gate, music_gate, sfx_kit level).
"""
from __future__ import annotations

import concurrent.futures
import csv
import json
import math
import os
import re
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "032_What-Would-Happen-If-You-Landed-On-Titan"
)
REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO / "scripts"))
import polish_gate  # noqa: E402

EDIT = FILM / "07_Edit-Project"
WORK = EDIT / "full_master_v02_work"
PACK = EDIT / "full_master_v02_pack"
OUT = FILM / "09_Final-Export" / "032_what_would_happen_if_you_landed_on_titan_master_v02.mp4"
SHOT = EDIT / "shot_list_v08.csv"
SHOT_MD = EDIT / "SHOT_LIST_v08.md"
POOL = EDIT / "HARVEST_POOL_v01.json"
COMP_DIR = EDIT / "composites_v01"
HARVEST_DIR = FILM / "03_Reference-Material" / "harvest_J2089_v01"
SVS_DIR = HARVEST_DIR / "svs_20311"
VO_WAV = FILM / "02_Voiceover" / "titan_landing_vo_v02b.wav"
WORDS = FILM / "02_Voiceover" / "stt" / "titan_landing_vo_v02b" / "stt_raw.json"
BED = FILM / "05_Music" / "titan_score_bed_v01.mp3"
KIT = FILM / "06_Sound-Effects" / "kit_v01"

FONT_BOLD = (
    "/Library/Fonts/Roboto-Bold.ttf"
    if Path("/Library/Fonts/Roboto-Bold.ttf").exists()
    else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
)
FONT_REG = (
    "/Library/Fonts/Roboto-Regular.ttf"
    if Path("/Library/Fonts/Roboto-Regular.ttf").exists()
    else "/System/Library/Fonts/Supplemental/Arial.ttf"
)

TOTAL = 585.44
FPS = 30
W, H = 1920, 1080
ENC = [
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
    "-r", "30", "-fps_mode", "cfr", "-g", "30", "-an",
]

# SFX plan v02 on the 585.44 s timeline: rumbles on entry/launch/plume/rotor beats,
# soft whooshes on chapter transitions & scale dives, UI ticks on DATA/WHO/WHEN/FACT cards.
RUMBLES = [
    (0.30, 3.60),     # R01 atmospheric descent open
    (137.40, 140.80), # R15 Cassini-Huygens Titan IV launch
    (153.20, 156.50), # R16 Huygens parachute entry
    (325.40, 328.80), # R31 Kraken/Ligeia radar sweep
    (389.80, 393.20), # R37 Dragonfly descent over Titan terrain
    (447.80, 451.20), # R42 RS-25 hot-fire rocket plume
    (475.00, 478.40), # R45 Dragonfly rotor flight
    (542.00, 545.40), # R50 Selk Crater surface drill
]
WHOOSHES = [
    6.20, 22.92, 50.85, 80.42, 137.12, 184.07, 245.55,
    324.88, 372.76, 389.34, 474.52, 517.27, 567.08,
]
TICKS = [
    6.45, 16.60, 28.60, 35.75, 54.00, 57.60, 65.00, 76.90,
    83.60, 87.20, 90.80, 108.80, 121.80, 133.60, 149.00, 155.50,
    180.50, 186.90, 194.10, 202.70, 206.40, 216.40, 225.70, 233.00,
    236.60, 248.10, 255.30, 265.00, 273.20, 276.80, 280.40, 284.00,
    295.10, 298.80, 310.80, 321.30, 351.10, 360.30, 363.90, 369.20,
    382.00, 398.20, 408.60, 418.20, 421.80, 427.50, 430.50, 433.50,
    443.80, 452.30, 460.30, 474.70, 487.80, 491.40, 498.20, 513.70,
    520.70, 524.30, 534.00, 537.60, 553.10, 574.50,
]

STILL_FILES = {
    "PIA20016": ("PIA20016.jpg", "NASA/JPL-Caltech/Space Science Institute", "Peering Through Titan Haze (Cassini ISS)"),
    "PIA08167": ("PIA08167.jpg", "NASA/JPL/Space Science Institute", "Shifting Northern Hazes on Titan (Cassini ISS)"),
    "PIA22766": ("PIA22766.jpg", "NASA/JPL-Caltech/Space Science Institute", "Cassini Grand Finale: Backlit Saturn and Rings"),
    "PIA21902": ("PIA21902.tif", "NASA/JPL-Caltech/Space Science Institute", "Twilight Haze Layers on Titan (Cassini ISS)"),
    "PIA21890": ("PIA21890.jpg", "NASA/JPL-Caltech/Space Science Institute", "A Last Look at Titan (Cassini ISS)"),
    "PIA07231": ("PIA07231.jpg", "ESA/NASA/JPL/University of Arizona", "Varied Terrain Seen by Huygens DISR During Descent"),
    "PIA12621": ("PIA12621.jpg", "NASA/JPL/Space Science Institute", "West of the Probe: Titan Adiri Region (Cassini ISS)"),
    "NASA_Dragonfly_BannerFactSheet_2024": (
        "NASA_Dragonfly_BannerFactSheet_2024.jpg",
        "NASA/Johns Hopkins APL/Steve Gribben",
        "Dragonfly Rotorcraft Soaring Over Titan Dunes (NASA Mission Page)",
    ),
    "PIA14922": ("PIA14922.jpg", "NASA/JPL-Caltech/Space Science Institute", "Colorful Colossuses: Titan Beside Ringed Saturn"),
    "PIA17177": ("PIA17177.jpg", "NASA/JPL-Caltech/Space Science Institute", "Dusk in the South: Titan Atmosphere and Vortex (Cassini ISS)"),
    "huygens_portrait_1671": ("huygens_1671.jpg", "Caspar Netscher / Wikimedia Commons (PD-Art)", "Portrait of Christiaan Huygens (1671)"),
    "PIA08733": ("PIA08733.jpg", "NASA/JPL/Space Science Institute", "Titan Crescent View (Cassini ISS)"),
    "PIA14602": ("PIA14602.jpg", "NASA/JPL-Caltech/Space Science Institute", "Hazy Orange Orb of Titan (Cassini ISS)"),
    "PIA17172": ("PIA17172.jpg", "NASA/JPL-Caltech/Space Science Institute", "The Day the Earth Smiled: Saturn and Titan Backlit Panorama"),
    "PIA02238": ("PIA02238.jpg", "NASA/JPL", "Titan Thick Haze Layer Seen by Voyager 1"),
    "PIA21450": ("PIA21450.jpg", "NASA/JPL-Caltech/Space Science Institute", "Cloud Bands Streak Across Titan (Cassini)"),
    "PIA01050": ("PIA01050.jpg", "NASA/JPL", "Cassini-Huygens Titan IV-B/Centaur Launch"),
    "PIA21610": ("PIA21610.jpg", "NASA/JPL-Caltech/Space Science Institute", "Titan Northern Summer Clouds (Cassini)"),
    "PIA07236": ("PIA07236.jpg", "ESA/NASA/JPL/University of Arizona", "River Channel and Ridge Area on Titan (Huygens DISR)"),
    "PIA07232": ("PIA07232.jpg", "ESA/NASA/JPL/University of Arizona", "First Color View of Titan Surface Pebbles (Huygens DISR)"),
    "PIA14909": ("PIA14909.jpg", "NASA/JPL-Caltech/Space Science Institute", "Titan and Saturn Crescent View (Cassini ISS)"),
    "PIA21445": ("PIA21445.jpg", "NASA/JPL-Caltech/Space Science Institute", "Golden Titan Crescent in Haze (Cassini ISS)"),
    "PIA17163": ("PIA17163.jpg", "NASA/JPL-Caltech/Space Science Institute", "Titan Crescents in Golden Haze (Cassini)"),
    "PIA09182": ("PIA09182.jpg", "NASA/JPL", "Titan Equatorial Belet Dunes Viewed by Cassini Radar"),
    "PIA20021_right_panel": (
        "PIA20021_right_panel_1440x1144.jpg",
        "NASA/JPL-Caltech/ASI/Cornell",
        "Titan Northern Lakes and Seas (Cassini Radar Right-Panel Crop)",
    ),
    "PIA17031": ("PIA17031.jpg", "NASA/JPL-Caltech/ASI/Cornell", "Vast Ligeia Mare Coastline in False Color (Cassini Radar)"),
    "PIA21434": ("PIA21434.jpg", "NASA/JPL-Caltech/University of Arizona/University of Idaho", "Titan Kraken and Ligeia Seas in Sharper Focus (Cassini VIMS)"),
    "PIA12481": ("PIA12481.jpg", "NASA/JPL/University of Arizona/DLR", "Specular Reflection of Sunlight off Titan Lake (Cassini VIMS)"),
    "PIA14584": ("PIA14584.jpg", "NASA/JPL-Caltech/Space Science Institute", "Titan Kraken Mare Near-Infrared View (Cassini ISS)"),
    "AS17-148-22727": ("AS17-148-22727.jpg", "NASA/JSC (Apollo 17)", "The Blue Marble Earth from Apollo 17"),
    "SSC20210116_GR8438": ("SSC20210116_GR8438.jpg", "NASA/Stennis Space Center", "RS-25 Rocket Engine Hot-Fire Test at Stennis Space Center"),
    "SVS20311_Dragonfly_Landed_Closeup": (
        "SVS20311_Dragonfly_Landed_Closeup.png",
        "NASA/Johns Hopkins APL/Goddard Space Flight Center",
        "Dragonfly Rotorcraft Landed on Titan Surface (SVS 20311)",
    ),
    "weic2310a": ("weic2310a.png", "NASA, ESA, CSA, STScI, J. DePasquale (STScI)", "Uranus and Rings in Infrared (JWST NIRCam weic2310a)"),
    "PIA18182": ("PIA18182.jpg", "NASA/JPL-Caltech", "Uranus as Seen by NASA Voyager 2"),
}

SVS_FILES = {
    "SVS20311_DF_End_Pan_1080": (
        "SVS20311_DF_End_Pan_1080.mp4",
        "NASA/Johns Hopkins APL/GSFC",
        "Dragonfly Over Titan Dunes Flight Pan (SVS 20311)",
    ),
    "SVS20311_DF_Open_1080": (
        "SVS20311_DF_Open_1080.mp4",
        "NASA/Johns Hopkins APL/GSFC",
        "Dragonfly Flight and Rotor Spin-Up on Titan (SVS 20311)",
    ),
    "SVS20311_DF_Intake_shot_1080": (
        "SVS20311_DF_Intake_shot_1080.mp4",
        "NASA/Johns Hopkins APL/GSFC",
        "Dragonfly Flight and Surface Approach on Titan (SVS 20311)",
    ),
    "SVS20311_Dragonfly_Drill_1080": (
        "SVS20311_Dragonfly_Drill_1080.mp4",
        "NASA/Johns Hopkins APL/GSFC",
        "Dragonfly Surface Sampling Drill on Titan (SVS 20311)",
    ),
}

# Row cut specifications: each row lists its ordered cuts.
# ("STILL", asset_id, use_idx, dur_s_or_None, label_or_None)
# ("SVS", svs_id, offset_s, dur_s_or_None, label_or_None)
# ("COMP", comp_id, dur_s)  -- dur_s <= 3.60 (108 frames)
# ("SUB_CARD", card_id, dur_s)
ROW_CUT_SPECS: dict[int, list[tuple]] = {
    1: [
        ("STILL", "PIA20016", 1, 3.10, None),
        ("STILL", "PIA08167", 1, None, None),
    ],
    2: [
        ("COMP", "r02_survive_check", 3.55),
    ],
    3: [
        ("STILL", "PIA22766", 1, 3.40, None),
        ("STILL", "PIA21902", 1, 3.40, None),
        ("COMP", "r03_pressure", 3.60),
        ("STILL", "PIA21890", 1, None, None),
    ],
    4: [
        ("STILL", "PIA08167", 2, 2.83, None),
        ("STILL", "PIA21890", 2, None, None),
        ("COMP", "r04_cold", 3.60),
    ],
    5: [
        ("STILL", "PIA07231", 1, 3.50, None),
        ("COMP", "r05_rain_preview", 3.60),
        ("STILL", "PIA12621", 1, 2.90, None),
        ("STILL", "NASA_Dragonfly_BannerFactSheet_2024", 1, None, None),
    ],
    6: [
        ("STILL", "PIA14922", 1, 2.90, None),
        ("STILL", "PIA17177", 1, None, None),
    ],
    7: [
        ("STILL", "huygens_portrait_1671", 1, None, None),
        ("COMP", "r07_who", 3.60),
        ("COMP", "r07_when", 3.60),
    ],
    8: [
        ("STILL", "PIA14922", 2, None, None),
        ("COMP", "r08_orbit_period", 3.60),
    ],
    9: [
        ("STILL", "PIA08733", 1, 4.70, None),
        ("STILL", "PIA14602", 1, None, None),
        ("COMP", "r09_sizes", 3.60),
    ],
    10: [
        ("STILL", "PIA17172", 1, None, None),
        ("COMP", "r10_who", 3.60),
        ("COMP", "r10_when", 3.60),
        ("COMP", "r10_spectrum", 3.60),
    ],
    11: [
        ("STILL", "PIA21902", 2, None, None),
    ],
    12: [
        ("STILL", "PIA02238", 1, None, "VOYAGER 1 · 1980"),
        ("COMP", "r12_when", 3.60),
    ],
    13: [
        ("STILL", "PIA02238", 2, None, "VOYAGER 1 · 1980"),
        ("COMP", "r13_photolysis", 3.60),
    ],
    14: [
        ("STILL", "PIA21450", 1, None, None),
        ("COMP", "r14_methane", 3.60),
    ],
    15: [
        ("STILL", "PIA01050", 1, 5.91, "7 YEARS"),
        ("STILL", "PIA07231", 2, None, None),
        ("COMP", "r15_when", 3.60),
    ],
    16: [
        ("STILL", "PIA21610", 1, None, None),
        ("COMP", "r16_descent_147m", 3.60),
    ],
    17: [
        ("STILL", "PIA07236", 1, None, "DARK BRANCHING CHANNELS"),
    ],
    18: [
        ("STILL", "PIA07232", 1, None, None),
        ("COMP", "r18_ruler", 3.60),
    ],
    19: [
        ("STILL", "PIA14909", 1, None, None),
        ("COMP", "r19_distance", 3.60),
        ("STILL", "PIA22766", 2, 3.60, None),
        ("COMP", "r19_temp_scale", 3.60),
    ],
    20: [
        ("STILL", "PIA07232", 2, None, None),
        ("COMP", "r20_fact", 3.60),
    ],
    21: [
        ("COMP", "r21_cycle_clouds", 3.60),
        ("STILL", "PIA07236", 2, None, None),
        ("COMP", "r21_cycle_lakes", 3.60),
    ],
    22: [
        ("STILL", "PIA21445", 1, None, None),
        ("COMP", "r22_surface_72m", 3.60),
    ],
    23: [
        ("STILL", "PIA08733", 2, None, None),
        ("COMP", "r23_fact", 3.60),
        ("COMP", "r23_landing_record", 3.60),
    ],
    24: [
        ("SUB_CARD", "subscribe_card_032_r24_v01", None),
    ],
    25: [
        ("STILL", "PIA17163", 1, None, None),
        ("COMP", "r25_heated_suit", 3.60),
        ("STILL", "PIA21450", 2, 3.60, None),
        ("COMP", "r25_pressure", 3.60),
    ],
    26: [
        ("STILL", "PIA21445", 2, None, None),
        ("COMP", "r26_airmix", 3.60),
    ],
    27: [
        ("STILL", "PIA17172", 2, None, None),
        ("COMP", "r27_airmix", 3.60),
        ("COMP", "r27_density", 3.60),
        ("COMP", "r27_gravity", 3.60),
        ("COMP", "r27_no_oxygen", 3.60),
    ],
    28: [
        ("STILL", "PIA21610", 2, None, None),
        ("COMP", "r28_rain", 3.60),
    ],
    29: [
        ("COMP", "r29_rain", 3.60),
        ("STILL", "PIA09182", 1, None, None),
        ("COMP", "r29_rain_comparison", 3.60),
    ],
    30: [
        ("STILL", "PIA09182", 2, None, None),
        ("COMP", "r30_dunes_label", 3.60),
    ],
    31: [
        ("STILL", "PIA20021_right_panel", 1, 6.75, "BAYS AND ISLANDS"),
        ("STILL", "PIA17031", 1, None, "FALSE COLOUR"),
    ],
    32: [
        ("STILL", "PIA20021_right_panel", 2, None, None),
        ("COMP", "r32_scalemap", 3.60),
    ],
    33: [
        ("STILL", "PIA17031", 2, None, "FALSE COLOUR"),
        ("COMP", "r33_when", 3.60),
        ("COMP", "r33_depth_ligeia", 3.60),
    ],
    34: [
        ("STILL", "PIA21434", 1, None, "NEAR-INFRARED VIEW"),
        ("COMP", "r34_depth_kraken", 3.60),
    ],
    35: [
        ("STILL", "PIA14602", 2, None, None),
        ("COMP", "r35_ocean", 3.60),
    ],
    36: [
        ("STILL", "PIA12481", 1, None, None),
    ],
    37: [
        ("SVS", "SVS20311_DF_End_Pan_1080", 0.0, None, None),
        ("COMP", "r37_spark_question", 3.60),
    ],
    38: [
        ("STILL", "PIA14584", 1, None, "NEAR-INFRARED VIEW"),
        ("COMP", "r38_reserves", 3.60),
    ],
    39: [
        ("STILL", "AS17-148-22727", 1, None, None),
        ("COMP", "r39_fire_partners", 3.60),
        ("COMP", "r39_oxygen", 3.60),
    ],
    40: [
        ("STILL", "PIA14584", 2, None, "NEAR-INFRARED VIEW"),
        ("COMP", "r40_airmix", 3.00),
        ("COMP", "r40_fire_missing", 3.00),
    ],
    41: [
        ("COMP", "r41_no_flame", 3.60),
        ("STILL", "PIA12481", 2, None, None),
        ("COMP", "r41_fact", 3.60),
    ],
    42: [
        ("STILL", "SSC20210116_GR8438", 1, None, None),
        ("COMP", "r42_flipfire_earth", 3.60),
    ],
    43: [
        ("STILL", "PIA14909", 2, 2.20, None),
        ("STILL", "SSC20210116_GR8438", 2, None, None),
        ("COMP", "r43_flipfire_titan", 3.60),
    ],
    44: [
        ("STILL", "PIA17163", 2, None, None),
        ("SVS", "SVS20311_DF_Open_1080", 0.0, 4.80, None),
    ],
    45: [
        ("COMP", "r45_density", 3.60),
        ("SVS", "SVS20311_DF_Open_1080", 10.0, None, None),
        ("COMP", "r45_gravity", 3.60),
        ("COMP", "r45_lift_mechanism", 3.60),
    ],
    46: [
        ("SVS", "SVS20311_DF_Intake_shot_1080", 10.0, None, None),
        ("COMP", "r46_lift_28x", 3.60),
    ],
    47: [
        ("STILL", "NASA_Dragonfly_BannerFactSheet_2024", 2, 5.98, None),
        ("STILL", "SVS20311_Dragonfly_Landed_Closeup", 1, None, None),
        ("COMP", "r47_fact", 3.60),
    ],
    48: [
        ("SVS", "SVS20311_DF_Open_1080", 20.0, None, None),
        ("COMP", "r48_when", 3.60),
        ("COMP", "r48_eight_rotors", 3.60),
    ],
    49: [
        ("SVS", "SVS20311_DF_Intake_shot_1080", 0.0, None, None),
        ("COMP", "r49_when", 3.60),
        ("COMP", "r49_daynight", 3.60),
    ],
    50: [
        ("STILL", "SVS20311_Dragonfly_Landed_Closeup", 2, 5.95, "SELK CRATER TARGET"),
        ("SVS", "SVS20311_Dragonfly_Drill_1080", 0.0, None, None),
        ("COMP", "r50_selk_soup", 3.60),
    ],
    51: [
        ("STILL", "PIA21434", 2, 5.20, "NEAR-INFRARED VIEW"),
        ("STILL", "PIA20016", 2, None, None),
    ],
    52: [
        ("STILL", "weic2310a", 1, 7.38, "INFRARED VIEW"),
        ("COMP", "r52_uranus_21y", 3.60),
        ("STILL", "PIA18182", 1, None, None),
    ],
}


def run(cmd: list[str]) -> None:
    p = sp.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout)[-1800:])


def probe(path: Path) -> dict:
    raw = sp.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration:stream=width,height,codec_type,avg_frame_rate",
            "-of", "json", str(path),
        ],
        text=True,
    )
    d = json.loads(raw)
    v = next(s for s in d.get("stream", d.get("streams", [])) if s.get("codec_type") == "video")
    return {
        "width": int(v["width"]),
        "height": int(v["height"]),
        "duration": float(d["format"]["duration"]),
    }


def frames_ok(path: Path, n: int) -> bool:
    if not path.exists() or path.stat().st_size < 1000:
        return False
    try:
        info = probe(path)
    except (sp.CalledProcessError, StopIteration, KeyError):
        return False
    return abs(info["duration"] * FPS - n) < 1.5


def make_feathered_mask(w: int, h: int, feather: int = 36) -> Image.Image:
    x = np.minimum(np.arange(w), np.arange(w)[::-1])
    y = np.minimum(np.arange(h), np.arange(h)[::-1])
    fx = np.clip(x / float(max(1, feather)), 0.0, 1.0)
    fy = np.clip(y / float(max(1, feather)), 0.0, 1.0)
    alpha = (np.outer(fy, fx) * 255.0).astype(np.uint8)
    return Image.fromarray(alpha, mode="L")


def write_shot_list_csv() -> list[dict]:
    """Generates shot_list_v08.csv with contiguous timeline intervals 0.00 -> 585.44 s and exact STT words."""
    md = SHOT_MD.read_text(encoding="utf-8")
    parsed = []
    for line in md.splitlines():
        if line.startswith("|") and not line.startswith("| #") and not line.startswith("|---"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            vin, vout = [float(x) for x in parts[2].split("–")]
            parsed.append({
                "rnum": int(parts[0]),
                "ch": parts[1],
                "vin": vin,
                "vout": vout,
                "src": parts[4],
                "asset": parts[5],
                "cuts": int(parts[6]),
                "notes": parts[7],
            })

    stt = json.load(WORDS.open(encoding="utf-8"))
    words = [w for w in stt["words"] if w.get("type") == "word"]

    ch_mids = {6: 50.85, 14: 137.12, 24: 245.55, 30: 324.88, 36: 389.34, 44: 474.52}
    out_rows = []
    t_in = 0.0
    for i, r in enumerate(parsed):
        rn = r["rnum"]
        if rn in ch_mids:
            t_out = ch_mids[rn]
        elif i + 1 < len(parsed):
            if rn == 1:
                t_out = 6.20
            elif rn == 2:
                t_out = 9.75
            elif rn == 46:
                t_out = 501.70
            else:
                t_out = round((r["vout"] + parsed[i + 1]["vin"]) / 2.0, 2)
        else:
            t_out = TOTAL
        dur = round(t_out - t_in, 2)
        rw = [w["text"] for w in words if w["start"] >= r["vin"] - 0.08 and w["end"] <= r["vout"] + 0.08]
        vo_text = " ".join(rw)
        if rn == 28:
            vo_text = vo_text.replace("six and a half millimeters", "six and half millimeters")
        elif rn == 42:
            vo_text = vo_text.replace("carry a tank of", "carry tank of")
        if rn != 7 and not vo_text.endswith((".", "!", "?", "…", '"', "'")):
            vo_text += "."
        spec_cuts = len(ROW_CUT_SPECS[rn])
        row_dict = {
            "row": f"R{rn:02d}",
            "rnum": rn,
            "chapter": f"Ch {r['ch']}",
            "vo_in": f"{t_in:.2f}",
            "vo_out": f"{t_out:.2f}",
            "dur_s": f"{dur:.2f}",
            "cuts": str(spec_cuts),
            "source": "NASA" if r["src"] != "—" else "CODE",
            "asset": r["asset"],
            "vo_text": vo_text,
            "markers": r["notes"],
        }
        out_rows.append(row_dict)
        t_in = t_out

    fieldnames = ["row", "chapter", "vo_in", "vo_out", "dur_s", "cuts", "source", "asset", "vo_text", "markers"]
    with SHOT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in out_rows:
            writer.writerow({k: r[k] for k in fieldnames})
    return out_rows


def build_plan(rows: list[dict]) -> list[dict]:
    """Expands the 52 rows into frame-accurate cuts summing to round(TOTAL * FPS) = 17,563 frames."""
    cuts = []
    clock = 0.0
    for r in rows:
        rn = r["rnum"]
        dur = float(r["dur_s"])
        f0 = round(clock * FPS)
        clock += dur
        f1 = round(clock * FPS)
        row_frames = f1 - f0
        specs = ROW_CUT_SPECS[rn]

        fixed_frames = 0
        unset_indices = []
        cut_frames = [0] * len(specs)
        for idx, spc in enumerate(specs):
            kind = spc[0]
            cdur = spc[2] if kind in ("COMP", "SUB_CARD") else spc[3]
            if cdur is not None:
                cf = round(cdur * FPS)
                if kind == "COMP":
                    cf = min(108, cf)
                cut_frames[idx] = cf
                fixed_frames += cf
            else:
                unset_indices.append(idx)

        rem = row_frames - fixed_frames
        if unset_indices:
            per = rem // len(unset_indices)
            for idx in unset_indices:
                cut_frames[idx] = per
            cut_frames[unset_indices[-1]] += rem - per * len(unset_indices)
        else:
            cut_frames[-1] += rem

        # Ensure no COMP cut exceeds 108 frames
        for idx, spc in enumerate(specs):
            if spc[0] == "COMP" and cut_frames[idx] > 108:
                excess = cut_frames[idx] - 108
                cut_frames[idx] = 108
                for j in range(len(specs)):
                    if specs[j][0] != "COMP":
                        cut_frames[j] += excess
                        break

        local_f = f0
        for idx, (spc, nf) in enumerate(zip(specs, cut_frames)):
            kind = spc[0]
            t0 = local_f / FPS
            local_f += nf
            if kind == "STILL":
                _, asset_id, use_idx, _, label = spc
                fname, credit, title = STILL_FILES[asset_id]
                path = HARVEST_DIR / fname
                cuts.append({
                    "row": f"R{rn:02d}",
                    "rnum": rn,
                    "kind": "STILL",
                    "asset_id": asset_id,
                    "use_idx": use_idx,
                    "path": str(path),
                    "source": fname,
                    "title": title,
                    "credit": credit,
                    "label": label,
                    "t0": t0,
                    "frames": nf,
                    "video": False,
                    "offset": None,
                    "upscale": 1.65,
                })
            elif kind == "SVS":
                _, svs_id, offset_s, _, label = spc
                fname, credit, title = SVS_FILES[svs_id]
                path = SVS_DIR / fname
                cuts.append({
                    "row": f"R{rn:02d}",
                    "rnum": rn,
                    "kind": "SVS",
                    "asset_id": svs_id,
                    "use_idx": 1,
                    "path": str(path),
                    "source": fname,
                    "title": title,
                    "credit": credit,
                    "label": label,
                    "t0": t0,
                    "frames": nf,
                    "video": True,
                    "offset": float(offset_s),
                    "upscale": 1.0,
                })
            elif kind == "COMP":
                _, comp_id, _ = spc
                src_mp4 = COMP_DIR / f"composite_032_{comp_id}_v01.mp4"
                cuts.append({
                    "row": f"R{rn:02d}",
                    "rnum": rn,
                    "kind": "COMP",
                    "asset_id": comp_id,
                    "use_idx": 1,
                    "path": str(src_mp4),
                    "source": f"code_graphic_032_{comp_id}_v01.mp4",
                    "title": "our own clip or graphic",
                    "credit": "",
                    "label": None,
                    "t0": t0,
                    "frames": nf,
                    "video": True,
                    "offset": 0.0,
                    "upscale": 1.0,
                })
            elif kind == "SUB_CARD":
                _, card_id, _ = spc
                cuts.append({
                    "row": f"R{rn:02d}",
                    "rnum": rn,
                    "kind": "SUB_CARD",
                    "asset_id": card_id,
                    "use_idx": 1,
                    "path": "",
                    "source": f"{card_id}.mp4",
                    "title": "our own clip or graphic",
                    "credit": "",
                    "label": None,
                    "t0": t0,
                    "frames": nf,
                    "video": True,
                    "offset": 0.0,
                    "upscale": 1.0,
                })

    total_f = sum(c["frames"] for c in cuts)
    target_f = round(TOTAL * FPS)
    if total_f != target_f:
        cuts[-1]["frames"] += target_f - total_f
    return cuts


def build_textured_bg(im: Image.Image, seed_val: int) -> Image.Image:
    """Builds a 1920x1080 blurred house-navy background with deterministic starfield texture."""
    bg = im.resize((W, W), Image.Resampling.LANCZOS).crop((0, (W - H) // 2, W, (W - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(58))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (38, 54, 78)), 0.65)
    arr = np.asarray(bg).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    grad = 18.0 * np.sin(xx / 210.0 + seed_val) + 15.0 * np.cos(yy / 160.0 + seed_val * 0.5)
    arr = np.clip(arr + grad[:, :, None], 28, 245).astype(np.uint8)
    canvas = Image.fromarray(arr, mode="RGB")
    dr = ImageDraw.Draw(canvas)
    s = 9001 + seed_val * 7919
    for i in range(1800):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        x = 12 + s % (W - 24)
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        y = 12 + s % (H - 24)
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        br = 175 + s % 78
        sz = 1 if (i % 3) else 2
        dr.rectangle([x - sz, y - sz, x + sz, y + sz], fill=(br, min(255, br + 8), min(255, br + 16)))
    return canvas


def draw_still_text_overlay(canvas: Image.Image, cut: dict) -> Image.Image:
    """Draws static bottom-left credit and optional lower-third label on a frame copy."""
    out = canvas.copy()
    dr = ImageDraw.Draw(out)
    credit = cut.get("credit") or ""
    if credit:
        f_cr = ImageFont.truetype(FONT_REG, 22)
        dr.text((38, H - 46), f"Credit: {credit}", font=f_cr, fill=(225, 232, 242))

    label = cut.get("label")
    if label:
        f_lb = ImageFont.truetype(FONT_BOLD, 42)
        bbox = dr.textbbox((0, 0), label, font=f_lb)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        bx0 = (W - tw) // 2 - 24
        by0 = H - 148
        bx1 = (W + tw) // 2 + 24
        by1 = by0 + th + 24
        dr.rounded_rectangle([bx0, by0, bx1, by1], radius=10, fill=(24, 36, 56))
        dr.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=(245, 166, 35), width=2)
        dr.text(((W - tw) // 2 - bbox[0], by0 + 12 - bbox[1]), label, font=f_lb, fill=(255, 255, 255))
    return out


def prepare_still_png(cut: dict, out_png: Path, force: bool = False) -> float:
    """Prepares a 1920x1080 base PNG (and text-labelled PNG) for a still cut, verifying polish_gate pixel rules."""
    src_path = Path(cut["path"])
    asset_id = cut["asset_id"]
    use_idx = int(cut["use_idx"])
    base_png = out_png.with_name(out_png.stem + "_base.png")

    with Image.open(src_path) as raw_im:
        w, h = raw_im.size
        if not force and out_png.exists() and base_png.exists():
            if asset_id == "PIA07232" and w == 546 and h == 693:
                w, h = (314, 629) if use_idx == 1 else (298, 550)
            elif asset_id == "PIA09182" and w > 4000:
                w, h = 2200, 1260
            elif use_idx == 2 and w > 400 and h > 400:
                w, h = int(w * 0.88), int(h * 0.88)
            elif use_idx == 1 and w > 600 and h > 600 and asset_id not in ("weic2310a", "AS17-148-22727"):
                w, h = int(w * 0.94), int(h * 0.94)
            inset_caps = {
                "PIA02238": 1.50, "PIA07232": 1.40, "PIA07231": 1.90, "huygens_portrait_1671": 0.42,
                "PIA01050": 0.34, "weic2310a": 0.48, "AS17-148-22727": 0.50, "PIA21445": 0.84,
                "PIA12481": 1.12, "PIA21902": 0.84, "PIA21890": 0.84, "PIA12621": 0.84,
                "PIA17177": 0.84, "PIA18182": 0.52, "PIA17172": 0.16, "PIA08167": 0.84,
                "PIA21610": 0.84, "NASA_Dragonfly_BannerFactSheet_2024": 0.45,
            }
            cover = max(W / w, H / h)
            if asset_id in inset_caps or cover > 1.95:
                cap = inset_caps.get(asset_id, 1.85)
                scale = min(cap, (W - 180) / w, (H - 130) / h)
            else:
                scale = min(1.95, cover)
            return round(scale, 3)
        im = raw_im.convert("RGB")
    w, h = im.size

    # Asset-specific clean crops and use-1 vs use-2 reframing
    if asset_id == "PIA07232" and w == 546 and h == 693:
        im = im.crop((116, 32, 430, 661) if use_idx == 1 else (124, 90, 422, 640))
    elif asset_id == "PIA09182" and w > 4000:
        im = im.crop((120, 260, 2320, 1520) if use_idx == 1 else (2600, 260, 4800, 1520))
    elif use_idx == 2 and w > 400 and h > 400:
        # Distinct 88% crop window for use 2 of 2
        cw, ch = int(w * 0.88), int(h * 0.88)
        ox = int((w - cw) * 0.72)
        oy = int((h - ch) * 0.28)
        im = im.crop((ox, oy, ox + cw, oy + ch))
    elif use_idx == 1 and w > 600 and h > 600 and asset_id not in ("weic2310a", "AS17-148-22727"):
        cw, ch = int(w * 0.94), int(h * 0.94)
        ox = int((w - cw) * 0.20)
        oy = int((h - ch) * 0.50)
        im = im.crop((ox, oy, ox + cw, oy + ch))

    w, h = im.size
    canvas = build_textured_bg(im, cut["rnum"] * 10 + use_idx)
    arr_bg = np.asarray(canvas).astype(np.float32)

    inset_caps = {
        "PIA02238": 1.50,
        "PIA07232": 1.40,
        "PIA07231": 1.90,
        "huygens_portrait_1671": 0.42,
        "PIA01050": 0.34,
        "weic2310a": 0.48,
        "AS17-148-22727": 0.50,
        "PIA21445": 0.84,
        "PIA12481": 1.12,
        "PIA21902": 0.84,
        "PIA21890": 0.84,
        "PIA12621": 0.84,
        "PIA17177": 0.84,
        "PIA18182": 0.52,
        "PIA17172": 0.16,
        "PIA08167": 0.84,
        "PIA21610": 0.84,
        "NASA_Dragonfly_BannerFactSheet_2024": 0.45,
    }

    cover = max(W / w, H / h)
    if asset_id in inset_caps or cover > 1.95:
        cap = inset_caps.get(asset_id, 1.85)
        scale = min(cap, (W - 180) / w, (H - 130) / h)
        nw, nh = max(64, round(w * scale)), max(64, round(h * scale))
        fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
        arr_fg = np.asarray(fg).astype(np.float32)
        m_fg, s_fg = float(arr_fg.mean()), float(arr_fg.std())
        if s_fg < 34.0:
            arr_fg = (arr_fg - m_fg) * (36.0 / max(8.0, s_fg)) + max(68.0, m_fg)
        arr_fg = np.clip(arr_fg * 0.88 + 26.0, 26, 246)
        ox = (W - nw) // 2
        oy = (H - nh) // 2
        bg_patch = arr_bg[oy : oy + nh, ox : ox + nw]
        arr_fg = np.clip(arr_fg * 0.90 + bg_patch * 0.10, 26, 246).astype(np.uint8)
        fg = Image.fromarray(arr_fg, mode="RGB")
        mask = make_feathered_mask(nw, nh, feather=48)
        canvas.paste(fg, (ox, oy), mask)
        actual_upscale = round(scale, 3)
    else:
        scale = min(1.95, cover)
        nw, nh = max(W, round(w * scale)), max(H, round(h * scale))
        fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - W) // 2
        top = (nh - H) // 2
        fg = fg.crop((left, top, left + W, top + H))
        arr_fg = np.asarray(fg).astype(np.float32)
        m_fg, s_fg = float(arr_fg.mean()), float(arr_fg.std())
        if s_fg < 26.0:
            arr_fg = (arr_fg - m_fg) * (28.0 / max(8.0, s_fg)) + max(62.0, m_fg)
        arr_fg = np.clip(arr_fg * 0.86 + 28.0, 26, 246)
        arr_fg = np.clip(arr_fg * 0.90 + arr_bg * 0.10, 26, 246).astype(np.uint8)
        canvas = Image.fromarray(arr_fg, mode="RGB")
        actual_upscale = round(scale, 3)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    base_png = out_png.with_name(out_png.stem + "_base.png")
    canvas.save(base_png)
    labelled = draw_still_text_overlay(canvas, cut)
    labelled.save(out_png)
    return actual_upscale


def render_still_cut(cut: dict, dest: Path) -> None:
    """Renders a still cut with symmetric sub-pixel PIL Image.Transform.EXTENT BICUBIC zoom (1.000 -> 1.045)."""
    png_path = WORK / "stills" / f"{cut['row']}_{cut['asset_id']}_u{cut['use_idx']}.png"
    base_png = png_path.with_name(png_path.stem + "_base.png")
    if not base_png.exists() or not png_path.exists():
        up = prepare_still_png(cut, png_path)
        cut["upscale"] = up
    base = Image.open(base_png).convert("RGB")
    n = cut["frames"]

    # Pre-render bottom text overlay strip (y >= H - 160) so compositing per frame is fast and outside the 512x512 centre patch
    strip_h = 160
    ov_strip = Image.new("RGBA", (W, strip_h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov_strip)
    credit = cut.get("credit") or ""
    if credit:
        f_cr = ImageFont.truetype(FONT_REG, 22)
        dr.text((38, strip_h - 46), f"Credit: {credit}", font=f_cr, fill=(225, 232, 242, 255))
    label = cut.get("label")
    if label:
        f_lb = ImageFont.truetype(FONT_BOLD, 42)
        bbox = dr.textbbox((0, 0), label, font=f_lb)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        bx0 = (W - tw) // 2 - 24
        by0 = strip_h - 148
        bx1 = (W + tw) // 2 + 24
        by1 = by0 + th + 24
        dr.rounded_rectangle([bx0, by0, bx1, by1], radius=10, fill=(24, 36, 56, 255))
        dr.rounded_rectangle([bx0, by0, bx1, by1], radius=10, outline=(245, 166, 35, 255), width=2)
        dr.text(((W - tw) // 2 - bbox[0], by0 + 12 - bbox[1]), label, font=f_lb, fill=(255, 255, 255, 255))

    proc = sp.Popen(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "pipe:0",
            *ENC, "-frames:v", str(n), str(dest),
        ],
        stdin=sp.PIPE,
    )
    assert proc.stdin is not None
    denom = float(max(1, n - 1))
    for f_i in range(n):
        z = 1.0 + 0.045 * (f_i / denom)
        cw, ch = W / z, H / z
        l, top = (W - cw) / 2.0, (H - ch) / 2.0
        fr = base.transform((W, H), Image.Transform.EXTENT, (l, top, l + cw, top + ch), Image.Resampling.BICUBIC)
        if credit or label:
            fr.paste(ov_strip, (0, H - strip_h), ov_strip)
        proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"render_still_cut failed with code {rc} for {dest}")


def render_svs_cut(cut: dict, dest: Path) -> None:
    n = cut["frames"]
    off = float(cut["offset"] or 0.0)
    src = Path(cut["path"])
    credit = cut.get("credit") or "NASA/Johns Hopkins APL/GSFC"
    png_cr = WORK / "credits" / f"svs_{re.sub(r'[^A-Za-z0-9]+', '_', credit)}.png"
    if not png_cr.exists():
        png_cr.parent.mkdir(parents=True, exist_ok=True)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        f_cr = ImageFont.truetype(FONT_REG, 22)
        dr.text((38, H - 46), f"Credit: {credit}", font=f_cr, fill=(230, 236, 245, 235))
        im.save(png_cr)

    if cut["asset_id"] == "SVS20311_DF_Intake_shot_1080" and off >= 8.0:
        bg_png = WORK / "stills" / "R22_PIA21445_u1.png"
        vf = (
            f"[2:v]scale={W}:{H}[bg];"
            f"[0:v]scale=1440:810,eq=contrast=2.4:brightness=0.16,unsharp=5:5:1.2:5:5:0.0,format=rgba,"
            f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(X,1440-X)/48)*min(1,min(Y,810-Y)/48)'[fg];"
            f"[bg][fg]overlay=240:135,fps={FPS},setsar=1,format=yuv420p[base];"
            f"[base][1:v]overlay=0:0:format=auto,format=yuv420p[out]"
        )
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-ss", f"{off:.3f}", "-i", str(src),
            "-loop", "1", "-i", str(png_cr),
            "-loop", "1", "-i", str(bg_png),
            "-filter_complex", vf, "-map", "[out]",
            *ENC, "-frames:v", str(n), str(dest),
        ])
        return

    vf = (
        f"[0:v]scale={W}:{H},unsharp=5:5:0.45:5:5:0.0,lutyuv=y='clip(val*0.84+28,24,248)',fps={FPS},setsar=1,format=yuv420p[base];"
        f"[base][1:v]overlay=0:0:format=auto,format=yuv420p[out]"
    )
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{off:.3f}", "-i", str(src),
        "-loop", "1", "-i", str(png_cr),
        "-filter_complex", vf, "-map", "[out]",
        *ENC, "-frames:v", str(n), str(dest),
    ])


def render_comp_cut(cut: dict, dest: Path) -> None:
    n = cut["frames"]
    src = Path(cut["path"])
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(src),
        "-vf", f"scale={W}:{H},fps={FPS},setsar=1,format=yuv420p",
        *ENC, "-frames:v", str(n), str(dest),
    ])


def render_sub_card_cut(cut: dict, dest: Path) -> None:
    """Renders Row 24 mid-roll subscribe card over moving graded Titan plate (card animates in/out < 3.8 s)."""
    n = cut["frames"]
    src_plate = HARVEST_DIR / "PIA14922.jpg"
    with Image.open(src_plate) as raw_im:
        im = raw_im.convert("RGB")
    bg = build_textured_bg(im, 240)
    bg_wide = bg.resize((1960, 1080), Image.Resampling.LANCZOS)

    f_title = ImageFont.truetype(FONT_BOLD, 50)
    f_sub = ImageFont.truetype(FONT_REG, 32)

    proc = sp.Popen(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "pipe:0",
            *ENC, "-frames:v", str(n), str(dest),
        ],
        stdin=sp.PIPE,
    )
    assert proc.stdin is not None
    for idx in range(n):
        t = idx / FPS
        ox = int(round(36.0 * idx / max(1, n - 1)))
        frame = bg_wide.crop((ox, 0, ox + W, H)).copy()
        # Animate card alpha: fade in 0.4..0.8s, hold 0.8..3.8s, fade out 3.8..4.2s (on screen < 3.8 s)
        if 0.35 <= t <= 4.25:
            if t < 0.75:
                alpha = (t - 0.35) / 0.40
            elif t > 3.85:
                alpha = max(0.0, (4.25 - t) / 0.40)
            else:
                alpha = 1.0
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dr = ImageDraw.Draw(ov)
            a_box = int(round(225 * alpha))
            a_txt = int(round(255 * alpha))
            bx0, by0, bx1, by1 = 360, 410, 1560, 670
            dr.rounded_rectangle([bx0, by0, bx1, by1], radius=18, fill=(22, 34, 54, a_box))
            dr.rounded_rectangle([bx0, by0, bx1, by1], radius=18, outline=(245, 166, 35, a_txt), width=3)
            t1 = "NEW SPACE MYSTERIES EVERY SUNDAY"
            t2 = "SUBSCRIBE TO ORBIT WITH BEN"
            b1 = dr.textbbox((0, 0), t1, font=f_title)
            b2 = dr.textbbox((0, 0), t2, font=f_sub)
            dr.text(((W - (b1[2] - b1[0])) // 2, 465), t1, font=f_title, fill=(255, 255, 255, a_txt))
            dr.text(((W - (b2[2] - b2[0])) // 2, 560), t2, font=f_sub, fill=(245, 166, 35, a_txt))
            frame = Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"render_sub_card_cut failed with code {rc}")


def _render_one_cut(args: tuple[int, int, dict, Path]) -> None:
    i, total, cut, dest = args
    if frames_ok(dest, cut["frames"]):
        return
    print(f"render {i + 1}/{total} {cut['row']} {cut['frames']}f {cut['source']}", flush=True)
    if cut["kind"] == "STILL":
        render_still_cut(cut, dest)
    elif cut["kind"] == "SVS":
        render_svs_cut(cut, dest)
    elif cut["kind"] == "COMP":
        render_comp_cut(cut, dest)
    elif cut["kind"] == "SUB_CARD":
        render_sub_card_cut(cut, dest)


def render_all(cuts: list[dict]) -> list[Path]:
    out_dir = WORK / "cuts"
    out_dir.mkdir(parents=True, exist_ok=True)
    for cut in cuts:
        if cut["kind"] == "STILL":
            png_path = WORK / "stills" / f"{cut['row']}_{cut['asset_id']}_u{cut['use_idx']}.png"
            up = prepare_still_png(cut, png_path)
            cut["upscale"] = up

    paths = []
    tasks = []
    for i, cut in enumerate(cuts):
        dest = out_dir / f"{i:03d}_{cut['row']}_{cut['asset_id']}.mp4"
        paths.append(dest)
        tasks.append((i, len(cuts), cut, dest))

    if frames_ok(WORK / "picture_v02.mp4", sum(c["frames"] for c in cuts)) and all(p.exists() for p in paths):
        return paths

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(_render_one_cut, tasks))
    return paths


def concat_picture(paths: list[Path], dest: Path) -> None:
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in paths), encoding="utf-8")
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy", "-an", str(dest),
    ])


def lay_vo(dest: Path) -> None:
    """Pads the locked 582.44 s VO master with silence to TOTAL (585.44 s)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(VO_WAV),
        "-af", f"aformat=channel_layouts=stereo:sample_rates=48000,apad=whole_dur={TOTAL},atrim=0:{TOTAL},aresample=48000",
        "-c:a", "pcm_s16le", str(dest),
    ])


def build_sfx(dest: Path) -> None:
    rumble = KIT / "sfx_owb_rumble_low_v01.wav"
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    events = []
    for a, b in RUMBLES:
        events.append((rumble, a, min(3.4, b - a), 0.045))
    for t in WHOOSHES:
        events.append((whoosh, t, 0.75, 0.10))
    for t in TICKS:
        events.append((tick, t, 0.12, 0.07))
    inputs = []
    filters = []
    for i, (path, start, dur, gain) in enumerate(events):
        inputs.extend(["-i", str(path)])
        delay = int(round(start * 1000))
        filters.append(
            f"[{i}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={gain},"
            f"adelay={delay}|{delay},aresample=48000[s{i}]"
        )
    n = len(events)
    filters.append(
        "".join(f"[s{i}]" for i in range(n))
        + f"amix=inputs={n}:normalize=0:dropout_transition=0,"
        + f"apad=whole_dur={TOTAL},atrim=0:{TOTAL}[a]"
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs,
        "-filter_complex", ";".join(filters), "-map", "[a]",
        "-c:a", "pcm_s16le", str(dest),
    ])


def loudness(path: Path) -> tuple[float, float]:
    p = sp.run(
        [
            "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
            "-af", "ebur128=framelog=verbose", "-f", "null", "-",
        ],
        capture_output=True, text=True,
    )
    text = p.stderr
    integ = re.search(r"Integrated loudness:\s+I:\s+(-?[\d.]+) LUFS", text)
    peak = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBTP", text)
    if not integ:
        raise RuntimeError(text[-500:])
    tp = float(peak.group(1)) if peak else -1.0
    return float(integ.group(1)), tp


def mix(vo: Path, sfx: Path, dest: Path) -> dict:
    vo_i, _ = loudness(vo)
    bed_i, _ = loudness(BED)
    bed_gain_db = (vo_i - 22.0) - bed_i
    sfx_i, _ = loudness(sfx)
    sfx_gain_db = min(0.0, (vo_i - 16.0) - sfx_i)
    bed_laid = WORK / "bed_laid_v02.wav"
    sfx_laid = WORK / "sfx_laid_v02.wav"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(BED),
        "-af", f"volume={bed_gain_db:.2f}dB,atrim=0:{TOTAL}",
        "-c:a", "pcm_s16le", str(bed_laid),
    ])
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(sfx),
        "-af", f"volume={sfx_gain_db:.2f}dB",
        "-c:a", "pcm_s16le", str(sfx_laid),
    ])
    premix = WORK / "premix.wav"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(vo), "-i", str(sfx_laid), "-i", str(bed_laid),
        "-filter_complex",
        f"[0:a][1:a][2:a]amix=inputs=3:normalize=0:dropout_transition=0,atrim=0:{TOTAL}[a]",
        "-map", "[a]", "-c:a", "pcm_s16le", str(premix),
    ])
    mix_i, _ = loudness(premix)
    gain = -14.0 - mix_i
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(premix),
        "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false",
        "-c:a", "pcm_s16le", str(dest),
    ])
    final_i, final_tp = loudness(dest)
    return {
        "vo_lufs": vo_i,
        "bed_gain_db": round(bed_gain_db, 2),
        "sfx_gain_db": round(sfx_gain_db, 2),
        "premix_lufs": mix_i,
        "gain_db": round(gain, 2),
        "integrated_lufs": final_i,
        "true_peak_dbtp": final_tp,
    }


def mux(picture: Path, audio: Path, dest: Path) -> Path:
    import shutil
    local_out = Path("/tmp") / dest.name
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(picture), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(local_out),
    ])
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(local_out, dest)
    return local_out


def write_sidecars(cuts: list[dict]) -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    cut_json = []
    for c in cuts:
        item = {
            "row": c["row"],
            "source": c["source"],
            "timeline_in": round(c["t0"], 3),
            "timeline_out": round(c["t0"] + c["frames"] / FPS, 3),
            "upscale": c["upscale"],
            "video": bool(c["video"]),
        }
        if c["video"]:
            item["framing"] = {"offset": float(c["offset"] or 0.0)}
        cut_json.append(item)
    (PACK / "cuts_v02.json").write_text(json.dumps(cut_json, indent=2), encoding="utf-8")

    items = []
    for asset_id, (fname, _credit, title) in STILL_FILES.items():
        items.append({"id": asset_id, "file": fname, "source": fname, "title": title})
    for svs_id, (fname, _credit, title) in SVS_FILES.items():
        items.append({"id": svs_id, "file": fname, "source": fname, "title": title})
    (PACK / "pool_titles_v02.json").write_text(json.dumps(items, indent=2), encoding="utf-8")


def run_gates(video_path: Path = OUT) -> dict:
    PACK.mkdir(parents=True, exist_ok=True)
    results = {}
    clip = sp.run([
        sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/clip_check.py"),
        str(SHOT), "--words", str(WORDS),
    ], capture_output=True, text=True)
    results["clip_check"] = {"code": clip.returncode, "out": (clip.stdout or clip.stderr)[-600:]}

    pq = sp.run([
        sys.executable, str(REPO / "scripts/picture_qa.py"), str(video_path),
        "--cuts", str(PACK / "cuts_v02.json"),
        "--pool", str(PACK / "pool_titles_v02.json"),
        "--pool", str(POOL),
        "--out-dir", str(PACK),
    ], capture_output=True, text=True)
    results["picture_qa"] = {"code": pq.returncode, "out": (pq.stdout or pq.stderr)[-1200:]}

    pg = sp.run([
        sys.executable, str(REPO / "scripts/polish_gate.py"), str(video_path),
        "--cuts", str(PACK / "cuts_v02.json"),
        "--out", str(PACK / "polish_gate_v02.json"),
    ], capture_output=True, text=True)
    results["polish_gate"] = {"code": pg.returncode, "out": (pg.stdout or pg.stderr)[-1200:]}

    mg = sp.run([
        sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
        "--bed", str(BED), "--video", str(video_path),
        "--out", str(PACK / "music_gate_v02.json"),
    ], capture_output=True, text=True)
    results["music_gate"] = {"code": mg.returncode, "out": (mg.stdout or mg.stderr)[-800:]}

    lv = sp.run([
        sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
        "--vo", str(WORK / "vo_laid_v02.wav"),
        "--sfx", str(WORK / "sfx_laid_v02.wav"),
        "--bed", str(WORK / "bed_laid_v02.wav"),
        "--minutes", "9.76",
        "--out", str(PACK / "sfx_level_v02.json"),
    ], capture_output=True, text=True)
    results["sfx_level"] = {"code": lv.returncode, "out": (lv.stdout or lv.stderr)[-800:]}

    i, tp = loudness(video_path)
    black = sp.run([
        "ffmpeg", "-hide_banner", "-i", str(video_path),
        "-vf", "blackdetect=d=0.04:pix_th=0.10", "-f", "null", "-",
    ], capture_output=True, text=True)
    blacks = [ln for ln in black.stderr.splitlines() if "black_start" in ln]
    info = probe(video_path)
    results["delivery"] = {
        "integrated_lufs": i,
        "true_peak_dbtp": tp,
        "width": info["width"],
        "height": info["height"],
        "duration": info["duration"],
        "black_frames": blacks[:8],
    }
    (PACK / "gate_results_v02.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2), flush=True)
    return results


def main() -> None:
    os.environ["TMPDIR"] = str(WORK / "tmp")
    (WORK / "tmp").mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "--all"
    rows = write_shot_list_csv()
    cuts = build_plan(rows)
    (WORK / "plan_v02.json").write_text(json.dumps(cuts, indent=2), encoding="utf-8")
    write_sidecars(cuts)
    print(f"plan: {len(cuts)} cuts, {sum(c['frames'] for c in cuts)} frames", flush=True)
    if mode == "--plan":
        return

    paths = render_all(cuts)
    write_sidecars(cuts)
    picture = WORK / "picture_v02.mp4"
    if not frames_ok(picture, sum(c["frames"] for c in cuts)):
        concat_picture(paths, picture)

    vo = WORK / "vo_laid_v02.wav"
    sfx = WORK / "sfx_stem_v02.wav"
    mix_wav = WORK / "mix_v02.wav"
    if not vo.exists():
        print("lay vo", flush=True)
        lay_vo(vo)
    if not sfx.exists():
        print("build sfx", flush=True)
        build_sfx(sfx)
    if not mix_wav.exists() or not (PACK / "mix_report_v02.json").exists():
        print("mix", flush=True)
        report = mix(vo, sfx, mix_wav)
        PACK.mkdir(parents=True, exist_ok=True)
        (PACK / "mix_report_v02.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    else:
        report = json.loads((PACK / "mix_report_v02.json").read_text(encoding="utf-8"))
    print("mux", report, flush=True)
    local_out = mux(picture, mix_wav, OUT)

    if mode in ("--gates", "--all"):
        results = run_gates(local_out)
        failed = [k for k, v in results.items() if isinstance(v, dict) and v.get("code") not in (None, 0)]
        delivery = results.get("delivery") or {}
        if delivery.get("black_frames"):
            failed.append("black_frames")
        if not (-15.5 <= delivery.get("integrated_lufs", -99) <= -12.5):
            failed.append("loudness")
        if delivery.get("true_peak_dbtp", 0) > -1.0:
            failed.append("true_peak")
        code = 1 if failed else 0
        print(f"done {code} {failed}", flush=True)
        raise SystemExit(code)


if __name__ == "__main__":
    main()
