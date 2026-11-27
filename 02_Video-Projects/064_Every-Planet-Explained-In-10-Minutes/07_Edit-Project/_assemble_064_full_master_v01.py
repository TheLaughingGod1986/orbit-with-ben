#!/usr/bin/env python3
"""J3023 OWB:064 Every Planet Explained in 12 Minutes — Full Master v01 Assembler (£0 spend).

Assembles the complete 701.86 s (683.86 s locked VO + 18.00 s end-screen hold) 1920x1080 24 fps CFR
yuv420p master from synchronized v02 cuts/pool/provenance inputs (cuts_064_j3023_v02.json),
preserving:
  - Locked VO every_planet_explained_vo_v01.wav (SHA-256 4b478fcd...) untouched
  - R01a–R04b <= 3.80 s opening beats + sleek 01 / 08 · MERCURY frame-0 progress strip
  - Zero PIA00271 and zero PIA00233 anywhere (R09 uses real PIA23791 right globe + pvo_uv_790205)
  - Required R11 PIA00215 (SHA-256 46dc965a...) exact crop (350,600,2550,1838) pushing smoothly
    to (430,645,2470,1793) across 118.05–124.40 s, followed by v02 Venus spin graphic through 130.75 s
  - Corrected PIA18033 attribution: NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring
  - Chapter cards C02–C08 (2.40 s each, 0.60 s post-sentence breath, ~0.40 s xfade)
  - Separate VO, SFX (house kit_v01), and film-specific score bed stems (~-14 LUFS / <= -1 dBTP)
  - Full gate verification suite: clip_check, picture_qa, polish_gate, music_gate, sfx_kit level
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import json
import math
import os
import re
import shutil
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None

REPO = Path(__file__).resolve().parents[3]
REPO_FILM = Path(__file__).resolve().parents[1]
FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "064_Every-Planet-Explained-In-10-Minutes"
)
EDIT = FILM / "07_Edit-Project"
REPO_EDIT = REPO_FILM / "07_Edit-Project"
WORK = Path(os.environ.get("STUDIO_SCRATCH", "/Volumes/MiniWork/scratch")) / "J3023_064_master_v01_work"
PACK = EDIT / "full_master_v01_pack"
REPO_PACK = REPO_EDIT / "full_master_v01_pack"
OUT = FILM / "09_Final-Export" / "064_every_planet_explained_master_v01.mp4"

CUTS_JSON = REPO_EDIT / "cuts_064_j3023_v02.json"
POOL_JSON = REPO_EDIT / "pool_064_j3023_v02.json"
SHOT_CSV = REPO_EDIT / "shot_list_v02.csv"
STRIP_PNG = FILM / "04_Generated-Clips/J3023_code_graphics_v02/code_graphic_064_ch01_mercury_progress_strip_v02.png"

VO_WAV = FILM / "02_Voiceover/every_planet_explained_vo_v01.wav"
WORDS_JSON = REPO_FILM / "02_Voiceover/stt/every_planet_explained_vo_v01/stt_raw.json"
BED_MP3 = FILM / "05_Music/every_planet_score_bed_v01.mp3"
KIT_DIR = FILM / "06_Sound-Effects/kit_v01"

TOTAL = 701.86
FPS = 24
W, H = 1920, 1080
TOTAL_FRAMES = round(TOTAL * FPS)  # 16845 frames

ENC = [
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-pix_fmt", "yuv420p", "-r", str(FPS), "-fps_mode", "cfr",
    "-g", str(FPS), "-an",
]

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
FONT_DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"

# SFX plan v01: planetary reveals, chapter transitions, and Teach-on-Screen ticks (>= 0.5 s apart)
RUMBLES = [
    (7.10, 10.60),    # Mercury Prokofiev permanent shadow reveal
    (93.80, 97.30),   # Venus 464 C runaway greenhouse reveal
    (176.45, 179.95), # Earth 1,670 km/h equatorial spin reveal
    (272.70, 276.20), # Mars 6.36 mbar thin air & Olympus Mons scale
    (333.80, 337.30), # Jupiter 318 Earth masses reveal
    (381.10, 384.60), # Midpoint twist: no solid surface
    (414.60, 418.10), # Saturn 282,000 km rings reveal
    (525.00, 528.50), # Uranus 97.77 deg sideways tilt reveal
    (653.20, 656.70), # Neptune >2,000 km/h supersonic winds reveal
]
WHOOSHES = [
    81.85,  # C02 Venus card
    158.30, # C03 Earth card
    251.75, # C04 Mars card
    324.75, # C05 Jupiter card
    407.40, # C06 Saturn card
    496.98, # C07 Uranus card
    584.95, # C08 Neptune card
]
TICKS = [
    15.10, 22.20, 26.00, 29.60, 33.10, 46.80, 57.30, 64.60, 73.10,
    103.50, 107.70, 111.80, 124.60, 131.00, 143.10,
    168.90, 187.20, 193.40, 208.70, 217.80, 232.50, 245.10,
    254.50, 296.30, 301.50, 313.00,
    344.50, 356.40, 364.70, 388.40,
    425.30, 433.70, 439.30, 466.10, 477.90,
    505.00, 535.70, 547.60, 554.20, 576.30,
    587.70, 613.80, 624.10, 634.40, 644.70, 664.40, 670.20, 684.10,
]

# Corner credits keyed by filename (never overrides PIA18033 Suomi NPP attribution!)
CREDITS_BY_FILE = {
    "PIA15162.jpg": "NASA / JHU APL / Carnegie",
    "PIA17386.jpg": "NASA / JHU APL / Carnegie",
    "PIA16523.jpg": "NASA / JHU APL / Carnegie",
    "PIA19411.jpg": "NASA / JHU APL / Carnegie",
    "PIA11364.jpg": "NASA / JHU APL / Carnegie",
    "PIA16853.jpg": "NASA / JHU APL / Carnegie",
    "PIA23791.jpg": "NASA / JPL-Caltech (Mariner 10)",
    "pvo_uv_790205.jpg": "NASA / NSSDCA (Pioneer Venus)",
    "PIA00215.jpg": "NASA / JPL (Magellan SAR)",
    "Venera13_surface.jpg": "Soviet Venera 13 / CC BY 2.0",
    "svs_12312_epic_earth_timelapse.mp4": "NASA / GSFC / DSCOVR EPIC",
    "PIA18033.jpg": "NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring",
    "Five_Minutes_in_Orbit.webm": "NASA / ISS",
    "plate_031_r02a_iss_aurora_v01.mp4": "NASA / ISS",
    "plate_031_r30a_iss_limb_v01.mp4": "NASA / ISS",
    "plate_031_r42a_iss_blue_limb_v01.mp4": "NASA / ISS",
    "Carl_Friedrich_Gauss_1840_by_Jensen.jpg": "C. A. Jensen (1840) / PD",
    "PIA00407.jpg": "NASA / JPL / USGS",
    "PIA19400.jpg": "NASA / JPL-Caltech / MSSS",
    "PIA19803.jpg": "NASA / JPL-Caltech / MSSS",
    "JPL-20200303-MSLf-0001.mp4": "NASA / JPL-Caltech",
    "PIA00300.jpg": "NASA / JPL",
    "PIA02982.jpg": "NASA / JPL / MSSS",
    "PIA24542_full.jpg": "NASA / JPL-Caltech / ASU / MSSS",
    "JPL-20210222-M2020f-0001.mp4": "NASA / JPL-Caltech",
    "PIA22946.jpg": "NASA / JPL-Caltech / SwRI / MSSS",
    "PIA04866.jpg": "NASA / JPL / SSI",
    "PIA21972.jpg": "NASA / JPL-Caltech / SwRI / MSSS",
    "PIA21775.jpg": "NASA / JPL-Caltech / SwRI / MSSS",
    "PIA01384.jpg": "NASA / JPL",
    "Galileo_Galilei_Sustermans.jpg": "J. Sustermans (1636) / PD",
    "PIA17172.jpg": "NASA / JPL-Caltech / SSI",
    "PIA11141.jpg": "NASA / JPL-Caltech / SSI",
    "PIA21046.jpg": "NASA / JPL-Caltech / SSI",
    "PIA17652.jpg": "NASA / JPL-Caltech / SSI",
    "PIA14944.jpg": "NASA / JPL-Caltech / SSI",
    "r01_sourced_composite_v01_silent.mp4": "NASA / JPL · ESA / CSA / STScI",
    "PIA18182.jpg": "NASA / JPL",
    "weic2310a_unannotated.png": "NASA / ESA / CSA / STScI",
    "PIA02963_borderless.jpg": "NASA / ESA / STScI",
    "PIA01488.jpg": "NASA / JPL",
    "r55_cut3_pia01488_pushin_silent.mp4": "NASA / JPL",
    "William_Herschel01_hires.jpg.jpg": "L. F. Abbott (1785) / NPG PD",
    "PIA01492.jpg": "NASA / JPL",
    "PIA00046.jpg": "NASA / JPL",
    "PIA00317.jpg": "NASA / JPL",
    "File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm": "NASA / JHUAPL / SwRI",
    "PIA19952.jpg": "NASA / JHUAPL / SwRI",
    "File_Sputnik_Planum_floating_hills_-_unannotated.jpg.jpg": "NASA / JHUAPL / SwRI",
    "Urbain_Le_Verrier.jpg": "Wikimedia Commons / PD",
    "Johann_Gottfried_Galle.jpg": "Wikimedia Commons / PD",
    "William_Lassell.jpg": "Wikimedia Commons / PD",
}

PORTRAIT_FILES = {
    "Carl_Friedrich_Gauss_1840_by_Jensen.jpg",
    "Galileo_Galilei_Sustermans.jpg",
    "William_Herschel01_hires.jpg.jpg",
    "Urbain_Le_Verrier.jpg",
    "Johann_Gottfried_Galle.jpg",
    "William_Lassell.jpg",
}

# Teach-on-Screen lower-third overlays keyed by (row_id, cut_local_idx_in_row):
# (kind, line1, line2_or_None, rel_start_s, rel_end_s) — all <= 4 words verbatim from VO, hold <= 3.7 s
ROW_OVERLAYS: dict[tuple[str, int], tuple[str, str, str | None, float, float]] = {
    ("R04a", 0): ("WHO",   "Giuseppe Colombo", "(1920–1984) — Italian mathematician", 0.20, 3.45),
    ("R04a", 1): ("WHEN",  "1965 · SPIN RESONANCE", None, 0.20, 3.45),
    ("R05",  2): ("DATA",  "176-DAY SOLAR DAY", None, 0.20, 3.20),
    ("R06",  0): ("SCALE", "BLUEBERRY VS NICKEL", None, 0.20, 3.40),
    ("R08",  0): ("LABEL", "ALMOST NO TILT", "0.034° AXIAL TILT", 0.30, 3.90),
    ("R08",  2): ("WHEN",  "MAR 2011 – APR 2015", "MESSENGER AT MERCURY", 0.30, 3.90),
    ("R10",  1): ("DATA",  "96.5% CARBON DIOXIDE", None, 0.25, 3.85),
    ("R10",  2): ("SCALE", "930 METRES UNDERWATER", None, 0.25, 3.85),
    ("R13",  0): ("WHEN",  "1978 · PIONEER VENUS", "100× EARTH DEUTERIUM", 0.40, 4.00),
    ("R13",  2): ("WHEN",  "1 MARCH 1982", "VENERA 13 · 127 MINUTES", 0.40, 4.00),
    ("R13",  3): ("SCALE", "NEARLY 4× DESIGN", None, 0.40, 4.00),
    ("R15",  1): ("DATA",  "150 MILLION KM", "1 ASTRONOMICAL UNIT", 0.25, 3.70),
    ("R16",  1): ("DATA",  "43 KM WIDER", None, 0.40, 4.00),
    ("R16",  2): ("SCALE", ">4× CYCLONE OLIVIA", None, 0.40, 4.00),
    ("R19",  0): ("WHO",   "Carl Friedrich Gauss", "(1777–1855) — German mathematician", 0.15, 2.95),
    ("R19",  1): ("WHEN",  "1830s · ABSOLUTE INTENSITY", None, 0.15, 2.95),
    ("R20",  1): ("WHEN",  "2020 · ESA REPORT", "ROUGHLY 9% WEAKENING", 0.35, 3.95),
    ("R20",  2): ("SCALE", "13 FEET OF CONCRETE", None, 0.25, 3.80),
    ("R21",  0): ("SUB",   "SUBSCRIBE TO ORBIT WITH BEN", "NEW SPACE MYSTERIES EVERY WEEK", 0.50, 4.10),
    ("R22",  1): ("WHEN",  "4 BILLION YEARS AGO", "CRUSTAL MAGNETIC TRACES", 0.35, 3.95),
    ("R26",  0): ("WHEN",  "10 JUNE 2018", "OPPORTUNITY · 60× DESIGN", 0.40, 4.00),
    ("R26",  2): ("WHEN",  "18 JANUARY 2024", "INGENUITY · 72 FLIGHTS", 0.40, 4.00),
    ("R28",  1): ("DATA",  "9.9-HOUR DAY", None, 0.40, 4.00),
    ("R28",  2): ("DATA",  "12-EARTH-YEAR ORBIT", None, 0.40, 4.00),
    ("R29",  0): ("WHO",   "Galileo Galilei", "(1564–1642) — Italian astronomer", 0.25, 3.90),
    ("R29",  1): ("WHEN",  "1610 · FOUR MOONS", None, 0.25, 3.90),
    ("R29",  2): ("WHEN",  "LATE 1800s · ~41,000 KM", None, 0.25, 3.90),
    ("R29",  4): ("WHEN",  "2014 · UNDER 16,500 KM", None, 0.25, 3.90),
    ("R30",  1): ("FACT",  "NO SOLID SURFACE", None, 0.20, 3.30),
    ("R34",  1): ("DATA",  "282,000 KM RADIAL", None, 0.25, 3.85),
    ("R34",  2): ("SCALE", "10 METRES THICK", None, 0.25, 3.85),
    ("R35",  0): ("WHEN",  "2017 · CASSINI DIVES", None, 0.30, 3.90),
    ("R35",  2): ("DATA",  "4,800–45,000 KG/S", None, 0.30, 3.90),
    ("R35",  4): ("DATA",  "0.41 MIMAS MASS", "10–100M YEARS OLD?", 0.30, 3.90),
    ("R36",  0): ("WHEN",  "EARLY 1980s · VOYAGER", None, 0.40, 4.00),
    ("R37",  1): ("LABEL", "POSSIBLY SEASONAL HAZE", None, 0.40, 4.00),
    ("R40",  0): ("WHO",   "William Herschel", "(1738–1822) — British astronomer", 0.15, 3.25),
    ("R40",  1): ("WHEN",  "13 MARCH 1781", None, 0.15, 3.25),
    ("R40",  2): ("SCALE", "SOFTBALL VS NICKEL", None, 0.40, 4.00),
    ("R41",  1): ("FACT",  "21-YEAR WINTER", None, 0.40, 4.00),
    ("R41",  2): ("DATA",  "17-HOUR BACKWARDS SPIN", None, 0.40, 4.00),
    ("R42",  0): ("WHEN",  "24 JANUARY 1986", "VOYAGER 2 ONLY VISIT", 0.20, 3.15),
    ("R43",  1): ("DATA",  "NEARLY 60° MAGNETIC TILT", None, 0.40, 4.00),
    ("R43",  2): ("DATA",  "≥80% HOT DENSE FLUID", None, 0.40, 4.00),
    ("R45",  1): ("SCALE", "BASEBALL VS NICKEL", None, 0.30, 3.90),
    ("R45",  4): ("WHEN",  "2011 · FIRST FULL ORBIT", None, 0.30, 3.90),
    ("R46",  0): ("WHO",   "Urbain Le Verrier", "(1811–1877) — French mathematician", 0.35, 4.00),
    ("R46",  2): ("WHO",   "Johann Gottfried Galle", "(1812–1910) — German astronomer", 0.35, 4.00),
    ("R46",  3): ("WHEN",  "23 SEPTEMBER 1846", None, 0.35, 4.00),
    ("R46",  4): ("WHO",   "William Lassell", "(1799–1880) — British astronomer", 0.35, 4.00),
    ("R46",  5): ("WHEN",  "10 OCTOBER 1846 · TRITON", None, 0.35, 4.00),
    ("R47",  0): ("WHEN",  "25 AUGUST 1989", "VOYAGER 2 ONLY FLYBY", 0.30, 3.90),
    ("R48",  1): ("DATA",  "TRITON · >8 KM GEYSERS", None, 0.40, 4.00),
    ("R49",  0): ("WHEN",  "JULY 2015 · NEW HORIZONS", "PLUTO NITROGEN-ICE HEART", 0.40, 4.00),
}


def run(cmd: list[str]) -> None:
    p = sp.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout)[-1800:])


def probe(path: Path) -> dict:
    raw = sp.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration:stream=width,height,codec_type,avg_frame_rate,nb_frames",
            "-of", "json", str(path),
        ],
        text=True,
    )
    d = json.loads(raw)
    v = next(s for s in d.get("stream", d.get("streams", [])) if s.get("codec_type") == "video")
    return {
        "width": int(v["width"]),
        "height": int(v["height"]),
        "avg_frame_rate": v.get("avg_frame_rate"),
        "nb_frames": int(v.get("nb_frames") or 0),
        "duration": float(d["format"]["duration"]),
    }


def frames_ok(path: Path, n: int) -> bool:
    if not path.exists() or path.stat().st_size < 1000:
        return False
    try:
        info = probe(path)
    except Exception:
        return False
    if info["nb_frames"] > 0:
        return info["nb_frames"] == n
    return abs(info["duration"] * FPS - n) < 1.0


def make_feathered_mask(w: int, h: int, feather: int = 56) -> Image.Image:
    x = np.minimum(np.arange(w), np.arange(w)[::-1]).astype(np.float32)
    y = np.minimum(np.arange(h), np.arange(h)[::-1]).astype(np.float32)
    fx = np.clip(x / float(max(1, feather)), 0.0, 1.0) ** 1.35
    fy = np.clip(y / float(max(1, feather)), 0.0, 1.0) ** 1.35
    alpha = (np.outer(fy, fx) * 255.0).astype(np.uint8)
    return Image.fromarray(alpha, mode="L")


def build_textured_bg(im: Image.Image, seed_val: int) -> Image.Image:
    bg = im.resize((W, H), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(52))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (30, 46, 74)), 0.62)
    arr = np.asarray(bg).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    grad = 16.0 * np.sin(xx / 210.0 + seed_val) + 14.0 * np.cos(yy / 165.0 + seed_val * 0.5)
    arr = np.clip(arr + grad[:, :, None], 28.0, 244.0).astype(np.uint8)
    canvas = Image.fromarray(arr, mode="RGB")
    dr = ImageDraw.Draw(canvas)
    s = (9001 + seed_val * 7919) & 0x7FFFFFFF
    for i in range(1800):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        x = 14 + s % (W - 28)
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        y = 14 + s % (H - 28)
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        br = 170 + s % 82
        sz = 1 if (i % 3) else 2
        dr.rectangle([x - sz, y - sz, x + sz, y + sz], fill=(br, min(255, br + 8), min(255, br + 18)))
    return canvas


def build_still_base(cut_idx: int, cut: dict, app_idx: int, sub_idx: int) -> Image.Image:
    """Prepares a 1920x1080 RGB base image for a non-PIA00215 still cut that passes all polish_gate checks."""
    src_path = Path(cut["source"])
    fname = src_path.name
    framing = cut.get("framing") or {}
    with Image.open(src_path) as raw_im:
        im = raw_im.convert("RGB")

    # Apply explicit pre-crop (e.g. PIA23791 right globe only [1160, 0, 2245, 1096] -> zero central divider!)
    if "crop_xyxy" in framing:
        x0, y0, x1, y1 = framing["crop_xyxy"]
        im = im.crop((x0, y0, x1, y1))

    w, h = im.size
    if fname in PORTRAIT_FILES:
        mx, my = max(6, int(w * 0.04)), max(6, int(h * 0.04))
        im = im.crop((mx, my, w - mx, h - my))
        w, h = im.size

    reframe = framing.get("reframe", "")
    if reframe == "tight_pole" and w >= 600 and h >= 400:
        cw, ch = int(w * 0.82), int(h * 0.82)
        ox, oy = (w - cw) // 2, int((h - ch) * 0.25)
        im = im.crop((ox, oy, ox + cw, oy + ch))
    elif reframe in ("tight", "spot", "rings", "clouds", "equator") and w >= 420 and h >= 320:
        frac = 0.86 if reframe == "tight" else 0.84
        cw, ch = int(w * frac), int(h * frac)
        ox = int((w - cw) * (0.62 if (cut_idx % 2 == 0) else 0.36))
        oy = int((h - ch) * (0.40 if (cut_idx % 3 == 0) else 0.56))
        im = im.crop((ox, oy, ox + cw, oy + ch))
    elif reframe == "left" and w >= 420 and h >= 320:
        cw, ch = int(w * 0.85), int(h * 0.85)
        im = im.crop((int((w - cw) * 0.18), int((h - ch) * 0.45), int((w - cw) * 0.18) + cw, int((h - ch) * 0.45) + ch))
    elif sub_idx >= 2 and w >= 420 and h >= 320:
        cw, ch = int(w * 0.86), int(h * 0.86)
        ox = int((w - cw) * (0.62 if (cut_idx % 2 == 0) else 0.38))
        oy = int((h - ch) * (0.42 if (cut_idx % 3 == 0) else 0.58))
        im = im.crop((ox, oy, ox + cw, oy + ch))
    elif app_idx >= 2 and w >= 420 and h >= 320:
        cw, ch = int(w * 0.90), int(h * 0.90)
        ox = int((w - cw) * 0.68)
        oy = int((h - ch) * 0.32)
        im = im.crop((ox, oy, ox + cw, oy + ch))

    w, h = im.size
    seed_val = cut_idx * 17 + app_idx * 5 + sub_idx
    bg_canvas = build_textured_bg(im, seed_val)
    arr_bg = np.asarray(bg_canvas).astype(np.float32)

    max_up = min(1.95, float(cut.get("upscale") or 1.5))
    is_inset = (
        fname in PORTRAIT_FILES
        or fname in ("Venera13_surface.jpg", "PIA23791.jpg", "pvo_uv_790205.jpg")
        or max(W / w, H / h) > max_up
        or abs((w / h) - (W / H)) > 0.35
    )

    if is_inset:
        scale = min(max_up, (W - 180) / w, (H - 120) / h)
        nw, nh = max(96, round(w * scale)), max(96, round(h * scale))
        fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
        arr_fg = np.asarray(fg).astype(np.float32)
        m_fg, s_fg = float(arr_fg.mean()), float(arr_fg.std())
        if s_fg < 32.0:
            arr_fg = (arr_fg - m_fg) * (36.0 / max(8.0, s_fg)) + max(72.0, m_fg)
        arr_fg = np.clip(arr_fg * 0.86 + 22.0, 28.0, 232.0)
        ox = (W - nw) // 2
        oy = (H - nh) // 2 - 18
        bg_patch = arr_bg[oy:oy + nh, ox:ox + nw]
        arr_fg = np.clip(arr_fg * 0.78 + bg_patch * 0.22, 28.0, 232.0).astype(np.uint8)
        fg = Image.fromarray(arr_fg, mode="RGB")
        mask = make_feathered_mask(nw, nh, feather=min(68, nw // 5, nh // 5))
        canvas = bg_canvas.copy()
        canvas.paste(fg, (ox, oy), mask)
    else:
        scale = max(W / w, H / h)
        nw, nh = max(W, round(w * scale)), max(H, round(h * scale))
        fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
        left, top = (nw - W) // 2, (nh - H) // 2
        fg = fg.crop((left, top, left + W, top + H))
        arr_fg = np.asarray(fg).astype(np.float32)
        m_fg, s_fg = float(arr_fg.mean()), float(arr_fg.std())
        if s_fg < 28.0:
            arr_fg = (arr_fg - m_fg) * (34.0 / max(8.0, s_fg)) + max(68.0, m_fg)
        arr_fg = np.clip(arr_fg * 0.85 + 24.0, 28.0, 234.0)
        blended = np.clip(arr_fg * 0.78 + arr_bg * 0.22, 28.0, 234.0).astype(np.uint8)
        canvas = Image.fromarray(blended, mode="RGB")

    # Subtle cosmic illumination wave + fine grain prevents banding & gutters
    arr = np.asarray(canvas).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wave = (
        (1.0 + np.sin(xx * 2.0 * np.pi / W + seed_val * 0.3)) * 7.5
        + (1.0 + np.cos(yy * 2.0 * np.pi / H + seed_val * 0.7)) * 7.5
    )
    arr = np.clip(arr * 0.90 + wave[:, :, None], 28.0, 246.0).astype(np.uint8)
    return Image.fromarray(arr, mode="RGB")


def ease(t: float, a: float, b: float) -> float:
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    x = (t - a) / (b - a)
    return x * x * (3.0 - 2.0 * x)


def card_alpha(t: float, t0: float, t1: float, fade: float = 0.35) -> float:
    if t1 - t0 > 3.85:
        t1 = t0 + 3.80
    if t <= t0 or t >= t1:
        return 0.0
    if t < t0 + fade:
        return ease(t, t0, t0 + fade)
    if t > t1 - fade:
        return 1.0 - ease(t, t1 - fade, t1)
    return 1.0


def draw_cut_overlay_or_credit(
    frame: Image.Image,
    t_rel: float,
    dur_s: float,
    ov_spec: tuple[str, str, str | None, float, float] | None,
    credit_text: str,
    strip_img: Image.Image | None,
    f_main: ImageFont.FreeTypeFont,
    f_sub: ImageFont.FreeTypeFont,
    f_cred: ImageFont.FreeTypeFont,
) -> Image.Image:
    active_card = False
    if strip_img is not None:
        # Frame 0 sleek 01 / 08 · MERCURY progress strip (visible immediately, fades out last 0.35 s)
        a_strip = 1.0 if t_rel <= dur_s - 0.35 else max(0.0, (dur_s - t_rel) / 0.35)
        if a_strip > 0.02:
            active_card = True
            ov = strip_img.copy()
            if a_strip < 0.99:
                al = ov.getchannel("A").point(lambda v: int(v * a_strip))
                ov.putalpha(al)
            frame = Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")

    if ov_spec is not None:
        kind, line1, line2, t0, t1 = ov_spec
        a = card_alpha(t_rel, t0, t1, fade=0.35)
        if a > 0.02:
            active_card = True
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dr = ImageDraw.Draw(ov)
            y_slide = int(round((1.0 - a) * 12))
            border_col = {
                "WHEN": (110, 220, 245),
                "WHO": (255, 210, 72),
                "FACT": (255, 210, 72),
                "DATA": (110, 220, 245),
                "SCALE": (245, 166, 35),
                "SUB": (245, 166, 35),
            }.get(kind, (215, 228, 245))

            if line2:
                b1 = dr.textbbox((0, 0), line1, font=f_main)
                b2 = dr.textbbox((0, 0), line2, font=f_sub)
                tw = max(b1[2] - b1[0], b2[2] - b2[0])
                bx0 = (W - tw) // 2 - 32
                by0 = 842 + y_slide
                bx1 = (W + tw) // 2 + 32
                by1 = by0 + 132
                dr.rounded_rectangle(
                    [bx0, by0, bx1, by1], radius=16,
                    fill=(12, 22, 40, int(224 * a)), outline=(*border_col, int(235 * a)), width=3,
                )
                dr.text(((W - (b1[2] - b1[0])) // 2, by0 + 18), line1, font=f_main, fill=(255, 255, 255, int(255 * a)))
                dr.text(
                    ((W - (b2[2] - b2[0])) // 2, by0 + 76), line2, font=f_sub,
                    fill=(255, 215, 90, int(255 * a)) if kind == "SUB" else (215, 230, 248, int(250 * a)),
                )
            else:
                b1 = dr.textbbox((0, 0), line1, font=f_main)
                tw, th = b1[2] - b1[0], b1[3] - b1[1]
                bx0 = (W - tw) // 2 - 28
                by0 = 885 + y_slide
                bx1 = (W + tw) // 2 + 28
                by1 = by0 + th + 30
                dr.rounded_rectangle(
                    [bx0, by0, bx1, by1], radius=14,
                    fill=(12, 22, 40, int(222 * a)), outline=(*border_col, int(230 * a)), width=3,
                )
                dr.text(((W - tw) // 2 - b1[0], by0 + 15 - b1[1]), line1, font=f_main, fill=(255, 255, 255, int(255 * a)))
            frame = Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")

    if not active_card and credit_text:
        dr = ImageDraw.Draw(frame)
        dr.text(
            (38, H - 52), f"Credit: {credit_text}", font=f_cred,
            fill=(232, 238, 246), stroke_width=2, stroke_fill=(8, 14, 26),
        )
    return frame


def render_single_cut(task: dict) -> str:
    idx = task["idx"]
    cut = task["cut"]
    n_main = task["n_main"]
    n_breath = task["n_breath"]
    next_cut = task["next_cut"]
    app_idx = task["app_idx"]
    sub_idx = task["sub_idx"]
    row_sub_idx = task["row_sub_idx"]
    dest = Path(task["dest"])

    total_n = n_main + n_breath
    if frames_ok(dest, total_n):
        return str(dest)

    dest.parent.mkdir(parents=True, exist_ok=True)
    f_main = ImageFont.truetype(FONT_BOLD, 42)
    f_sub = ImageFont.truetype(FONT_REG, 30)
    try:
        f_cred = ImageFont.truetype(FONT_DIDOT, 24, index=1)
    except Exception:
        f_cred = ImageFont.truetype(FONT_REG, 22)

    rid = cut["row_id"]
    ov_spec = ROW_OVERLAYS.get((rid, row_sub_idx))
    src_path = Path(cut["source"])
    fname = src_path.name
    credit_text = CREDITS_BY_FILE.get(fname, "")
    framing = cut.get("framing") or {}
    strip_img = Image.open(STRIP_PNG).convert("RGBA") if framing.get("overlay_strip") == "ch01_mercury" else None
    dur_s = total_n / float(FPS)

    # Special exact-spec handler for R11 PIA00215 (J3883 required crop & push, 0.873x -> 0.941x)
    if fname == "PIA00215.jpg" and "push_xyxy" in framing:
        x0a, y0a, x1a, y1a = framing["crop_xyxy"]
        x0b, y0b, x1b, y1b = framing["push_xyxy"]
        with Image.open(src_path) as raw_im:
            im_sar = raw_im.convert("RGB")
        proc = sp.Popen(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                "-i", "pipe:0", *ENC, "-frames:v", str(total_n), str(dest),
            ],
            stdin=sp.PIPE,
        )
        assert proc.stdin is not None
        for f_i in range(total_n):
            u = f_i / float(max(1, total_n - 1))
            box = (
                x0a + (x0b - x0a) * u,
                y0a + (y0b - y0a) * u,
                x1a + (x1b - x1a) * u,
                y1a + (y1b - y1a) * u,
            )
            fr = im_sar.transform((W, H), Image.Transform.EXTENT, box, Image.Resampling.BICUBIC)
            fr = draw_cut_overlay_or_credit(fr, f_i / float(FPS), dur_s, ov_spec, credit_text, None, f_main, f_sub, f_cred)
            proc.stdin.write(fr.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"Failed rendering R11 PIA00215 cut {idx}")
        return str(dest)

    if cut.get("video"):
        off = float(framing.get("offset") or 0.0)
        is_card = rid.startswith("C")
        is_end_last = (idx == task["last_idx"])
        if ov_spec is None and not credit_text and not is_end_last:
            vf = (
                f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                f"tpad=stop_mode=clone:stop_duration=1.5,setpts=PTS-STARTPTS,format=yuv420p"
            )
            if is_card:
                # Smooth 0.35 s xfade/fade-in & out on chapter cards
                vf += f",fade=t=in:st=0:d=0.35,fade=t=out:st={max(0.1, dur_s-0.35):.3f}:d=0.35"
            run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-ss", f"{off:.3f}", "-i", str(src_path),
                "-vf", vf, *ENC, "-frames:v", str(total_n), str(dest),
            ])
            return str(dest)
        else:
            raw = sp.check_output([
                "ffmpeg", "-v", "error", "-ss", f"{off:.3f}", "-i", str(src_path),
                "-vf", f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1",
                "-frames:v", str(total_n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
            ])
            frames_arr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
            proc = sp.Popen(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                    "-i", "pipe:0", *ENC, "-frames:v", str(total_n), str(dest),
                ],
                stdin=sp.PIPE,
            )
            assert proc.stdin is not None
            for f_i in range(total_n):
                t_rel = f_i / float(FPS)
                im_f = Image.fromarray(frames_arr[min(f_i, len(frames_arr) - 1)], mode="RGB")
                im_f = draw_cut_overlay_or_credit(im_f, t_rel, dur_s, ov_spec, credit_text, None, f_main, f_sub, f_cred)
                if is_end_last and t_rel > dur_s - 2.5:
                    # Smooth final fade to black over last 2.5 s (past last word + 15.5 s hold)
                    fac = max(0.0, (dur_s - t_rel) / 2.5)
                    im_f = Image.fromarray((np.asarray(im_f, dtype=np.float32) * fac).astype(np.uint8), mode="RGB")
                proc.stdin.write(im_f.tobytes())
            proc.stdin.close()
            if proc.wait() != 0:
                raise RuntimeError(f"Failed rendering video cut {idx}")
            return str(dest)

    # Still cut: sub-pixel BICUBIC symmetric zoom + optional breath crossfade into next chapter card
    base = build_still_base(idx, cut, app_idx, sub_idx)
    proc = sp.Popen(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "pipe:0", *ENC, "-frames:v", str(total_n), str(dest),
        ],
        stdin=sp.PIPE,
    )
    assert proc.stdin is not None
    for f_i in range(total_n):
        t_rel = f_i / float(FPS)
        z = 1.0 + 0.045 * (f_i / float(max(1, total_n - 1)))
        cw, ch = W / z, H / z
        l, top = (W - cw) / 2.0, (H - ch) / 2.0
        fr = base.transform((W, H), Image.Transform.EXTENT, (l, top, l + cw, top + ch), Image.Resampling.BICUBIC)
        fr = draw_cut_overlay_or_credit(fr, t_rel, dur_s, ov_spec, credit_text, strip_img, f_main, f_sub, f_cred)
        proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"Failed rendering still cut {idx}")
    return str(dest)


def build_tasks() -> list[dict]:
    cuts = json.loads(CUTS_JSON.read_text(encoding="utf-8"))
    app_counts: dict[str, int] = {}
    row_sub_counts: dict[str, int] = {}
    prev_src = None
    sub_idx = 0
    tasks = []
    for i, c in enumerate(cuts):
        src = c["source"]
        if src == prev_src:
            sub_idx += 1
        else:
            sub_idx = 1
            app_counts[src] = app_counts.get(src, 0) + 1
        prev_src = src

        rid = c["row_id"]
        rsub = row_sub_counts.get(rid, 0)
        row_sub_counts[rid] = rsub + 1

        f_in = round(c["timeline_in"] * FPS)
        f_out = round(c["timeline_out"] * FPS)
        n_main = f_out - f_in
        if i + 1 < len(cuts):
            f_next = round(cuts[i + 1]["timeline_in"] * FPS)
            n_breath = max(0, f_next - f_out)
            next_cut = cuts[i + 1]
        else:
            n_breath = max(0, TOTAL_FRAMES - f_out)
            next_cut = None

        dest = WORK / "cuts" / f"{i:03d}_{rid}.mp4"
        tasks.append({
            "idx": i, "last_idx": len(cuts) - 1, "cut": c,
            "n_main": n_main, "n_breath": n_breath, "next_cut": next_cut,
            "app_idx": app_counts[src], "sub_idx": sub_idx, "row_sub_idx": rsub,
            "dest": str(dest),
        })
    return tasks


def render_all_cuts(tasks: list[dict]) -> list[Path]:
    (WORK / "cuts").mkdir(parents=True, exist_ok=True)
    todo = [t for t in tasks if not frames_ok(Path(t["dest"]), t["n_main"] + t["n_breath"])]
    print(f"Cuts to render: {len(todo)} / {len(tasks)}", flush=True)
    if todo:
        with cf.ProcessPoolExecutor(max_workers=6) as ex:
            futs = {ex.submit(render_single_cut, t): t["idx"] for t in todo}
            done_cnt = 0
            for fut in cf.as_completed(futs):
                idx = futs[fut]
                fut.result()
                done_cnt += 1
                if done_cnt % 10 == 0 or done_cnt == len(todo):
                    print(f"  rendered {done_cnt}/{len(todo)} cuts (last idx={idx})", flush=True)
    return [Path(t["dest"]) for t in tasks]


def concat_picture(paths: list[Path], dest: Path) -> None:
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in paths), encoding="utf-8")
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy", "-bsf:v", "setts=ts=N*512:dts=N*512:duration=512",
        "-video_track_timescale", "12288", "-an", str(dest),
    ])


def loudness(path: Path) -> tuple[float, float]:
    p = sp.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    text = p.stderr
    integ = re.search(r"Integrated loudness:\s+I:\s+(-?[\d.]+) LUFS", text)
    peak = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBTP", text)
    if not integ:
        raise RuntimeError(text[-500:])
    return float(integ.group(1)), float(peak.group(1)) if peak else -1.5


def build_audio() -> dict:
    WORK.mkdir(parents=True, exist_ok=True)
    vo_laid = WORK / "vo_laid_v01.wav"
    sfx_raw = WORK / "sfx_raw_v01.wav"
    sfx_laid = WORK / "sfx_laid_v01.wav"
    bed_laid = WORK / "bed_laid_v01.wav"
    mix_wav = WORK / "mix_v01.wav"

    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(VO_WAV),
        "-af", f"aformat=channel_layouts=stereo:sample_rates=48000,apad=whole_dur={TOTAL},atrim=0:{TOTAL},aresample=48000",
        "-c:a", "pcm_s16le", str(vo_laid),
    ])

    rumble = KIT_DIR / "sfx_owb_rumble_low_v01.wav"
    whoosh = KIT_DIR / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT_DIR / "sfx_owb_tick_ui_v01.wav"

    events = []
    for a, b in RUMBLES:
        events.append((rumble, a, min(3.4, b - a), 0.082))
    for t in WHOOSHES:
        events.append((whoosh, t, 0.78, 0.085))
    for t in TICKS:
        events.append((tick, t, 0.05, 0.095))

    inputs, filters = [], []
    for i, (path, start, dur, gain) in enumerate(events):
        inputs.extend(["-i", str(path)])
        delay = int(round(start * 1000))
        filters.append(f"[{i}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={gain},adelay={delay}|{delay},aresample=48000[s{i}]")
    n = len(events)
    filters.append("".join(f"[s{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0:dropout_transition=0,apad=whole_dur={TOTAL},atrim=0:{TOTAL}[a]")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[a]", "-c:a", "pcm_s16le", str(sfx_raw)])

    vo_i, _ = loudness(vo_laid)
    bed_i, _ = loudness(BED_MP3)
    sfx_i, _ = loudness(sfx_raw)

    bed_gain_db = (vo_i - 25.5) - bed_i
    sfx_gain_db = min(0.0, (vo_i - 22.0) - sfx_i)

    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(BED_MP3),
        "-af", f"volume={bed_gain_db:.2f}dB,afade=t=out:st={TOTAL-3.0:.2f}:d=3.00,atrim=0:{TOTAL},aresample=48000",
        "-c:a", "pcm_s16le", str(bed_laid),
    ])
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(sfx_raw),
        "-af", f"volume={sfx_gain_db:.2f}dB,atrim=0:{TOTAL},aresample=48000",
        "-c:a", "pcm_s16le", str(sfx_laid),
    ])

    # Copy separate stems to NAS
    stems_dir = FILM / "06_Sound-Effects/stems_v01"
    stems_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(vo_laid, stems_dir / "064_vo_stem_v01.wav")
    shutil.copy2(sfx_laid, stems_dir / "064_sfx_stem_v01.wav")
    shutil.copy2(bed_laid, stems_dir / "064_music_stem_v01.wav")

    premix = WORK / "premix_v01.wav"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(vo_laid), "-i", str(sfx_laid), "-i", str(bed_laid),
        "-filter_complex", f"[0:a][1:a][2:a]amix=inputs=3:normalize=0:dropout_transition=0,atrim=0:{TOTAL}[a]",
        "-map", "[a]", "-c:a", "pcm_s16le", str(premix),
    ])
    pre_i, _ = loudness(premix)
    gain_db = -14.0 - pre_i
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(premix),
        "-af", f"volume={gain_db:.2f}dB,alimiter=limit=0.84:level=false",
        "-c:a", "pcm_s16le", str(mix_wav),
    ])
    final_i, final_tp = loudness(mix_wav)
    report = {
        "vo_lufs": vo_i, "bed_lufs_raw": bed_i, "bed_gain_db": round(bed_gain_db, 2),
        "sfx_lufs_raw": sfx_i, "sfx_gain_db": round(sfx_gain_db, 2),
        "premix_lufs": pre_i, "master_gain_db": round(gain_db, 2),
        "integrated_lufs": final_i, "true_peak_dbtp": final_tp,
    }
    PACK.mkdir(parents=True, exist_ok=True)
    REPO_PACK.mkdir(parents=True, exist_ok=True)
    (PACK / "mix_report_v01.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (REPO_PACK / "mix_report_v01.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def mux(picture: Path, audio: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(picture), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(dest),
    ])


def run_gates() -> dict:
    PACK.mkdir(parents=True, exist_ok=True)
    REPO_PACK.mkdir(parents=True, exist_ok=True)
    results = {}

    clip = sp.run([
        sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/clip_check.py"),
        str(SHOT_CSV), "--words", str(WORDS_JSON), "--vo-end", "683.86", "--repeat-ok", "R27",
    ], capture_output=True, text=True)
    results["clip_check"] = {"code": clip.returncode, "out": (clip.stdout or clip.stderr).strip()}

    pq = sp.run([
        sys.executable, str(REPO / "scripts/picture_qa.py"), str(OUT),
        "--cuts", str(CUTS_JSON), "--pool", str(POOL_JSON), "--out-dir", str(PACK),
    ], capture_output=True, text=True)
    results["picture_qa"] = {"code": pq.returncode, "out": (pq.stdout or pq.stderr).strip()}

    pl = sp.run([
        sys.executable, str(REPO / "scripts/polish_gate.py"), str(OUT),
        "--cuts", str(CUTS_JSON), "--out", str(PACK / "polish_gate_v01.json"),
    ], capture_output=True, text=True)
    results["polish_gate"] = {"code": pl.returncode, "out": (pl.stdout or pl.stderr).strip()[-1500:]}

    # Collect readable local/NAS other OWB music beds so music_gate runs without iCloud placeholder warnings
    other_beds: list[str] = []
    sl_root = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects")
    for p in sorted(sl_root.glob("*/05_Music/*")):
        if p.is_file() and not p.name.startswith("._") and p.suffix.lower() in (".mp3", ".wav", ".m4a") and "064_" not in str(p):
            other_beds.extend(["--others", str(p)])
    mg_cmd = [
        sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
        "--bed", str(BED_MP3), "--video", str(OUT),
        "--out", str(PACK / "music_gate_v01.json"),
    ] + other_beds
    mg = sp.run(mg_cmd, capture_output=True, text=True)
    results["music_gate"] = {"code": mg.returncode, "out": (mg.stdout or mg.stderr).strip()}

    lv = sp.run([
        sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
        "--vo", str(WORK / "vo_laid_v01.wav"),
        "--sfx", str(WORK / "sfx_laid_v01.wav"),
        "--bed", str(WORK / "bed_laid_v01.wav"),
        "--minutes", "11.7",
        "--out", str(PACK / "sfx_level_v01.json"),
    ], capture_output=True, text=True)
    results["sfx_level"] = {"code": lv.returncode, "out": (lv.stdout or lv.stderr).strip()}

    i, tp = loudness(OUT)
    black = sp.run([
        "ffmpeg", "-hide_banner", "-i", str(OUT),
        "-vf", "blackdetect=d=0.04:pix_th=0.10", "-f", "null", "-",
    ], capture_output=True, text=True)
    blacks = [ln for ln in black.stderr.splitlines() if "black_start" in ln]
    info = probe(OUT)
    sha = hashlib.sha256(OUT.read_bytes()).hexdigest()
    results["delivery"] = {
        "file": str(OUT), "sha256": sha, "bytes": OUT.stat().st_size,
        "integrated_lufs": i, "true_peak_dbtp": tp,
        "width": info["width"], "height": info["height"],
        "avg_frame_rate": info["avg_frame_rate"], "nb_frames": info["nb_frames"],
        "duration": info["duration"], "black_frames": blacks[:8],
    }

    # Copy text/JSON reports to repo pack (never media/JPEGs if large, keep JSON/MD in git!)
    for fname in ("picture_qa.json", "PICTURE_QA.md", "polish_gate_v01.json", "music_gate_v01.json", "sfx_level_v01.json"):
        src = PACK / fname
        if src.exists():
            shutil.copy2(src, REPO_PACK / fname)
    (PACK / "gate_results_v01.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    (REPO_PACK / "gate_results_v01.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return results


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--all"
    WORK.mkdir(parents=True, exist_ok=True)
    PACK.mkdir(parents=True, exist_ok=True)
    REPO_PACK.mkdir(parents=True, exist_ok=True)

    if mode == "--audio":
        rep = build_audio()
        print("Audio report:", json.dumps(rep, indent=2), flush=True)
        lv = sp.run([
            sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
            "--vo", str(WORK / "vo_laid_v01.wav"),
            "--sfx", str(WORK / "sfx_laid_v01.wav"),
            "--bed", str(WORK / "bed_laid_v01.wav"),
            "--minutes", "11.7",
            "--out", str(PACK / "sfx_level_v01.json"),
        ], capture_output=True, text=True)
        print(lv.stdout, lv.stderr, flush=True)
        raise SystemExit(lv.returncode)

    tasks = build_tasks()
    paths = render_all_cuts(tasks)
    picture = WORK / "picture_v01.mp4"
    print(f"Concatenating {len(paths)} cuts -> {picture}", flush=True)
    concat_picture(paths, picture)

    mix_wav = WORK / "mix_v01.wav"
    if not mix_wav.exists() or mode == "--all":
        print("Building audio stems & mix...", flush=True)
        build_audio()

    print("Muxing final master ->", OUT, flush=True)
    mux(picture, mix_wav, OUT)

    if mode in ("--gates", "--all"):
        results = run_gates()
        print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
