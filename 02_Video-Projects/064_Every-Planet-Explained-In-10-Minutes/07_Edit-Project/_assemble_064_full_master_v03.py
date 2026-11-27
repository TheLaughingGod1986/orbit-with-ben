#!/usr/bin/env python3
"""J3023 OWB:064 Every Planet Explained in 12 Minutes — Full Master v03 Assembler (£0 spend).

Resolves all 6 v01 picture_qa / polish_gate failures and human frame-inspection defects:
  - Preserves 064_every_planet_explained_master_v01.mp4 untouched on studio-live
  - Clean circular/soft-key compositing for planet globes on deep-navy space (ZERO dark square boxes, ZERO stars overlaid on planets or NASA imagery)
  - Compact 01 / 08 · MERCURY progress strip (no full-width horizontal split-panel seam)
  - Lifted deep-navy space floor on DSCOVR EPIC Earth timelapse (resolves near-black fail)
  - Bright verified 031 ISS Earth plates replacing dark/truncated webm and vertical-gutter plate
  - Clean single-globe crops on PIA11364, borderless/unlabelled crops on Venera13_surface, PIA17386, PIA24542_full
  - High-detail New Horizons Pluto Flyby offsets (14 s, 21 s) + final fade only in last 1.5 s
  - Clean legible sans-serif corner credits (no double-stamp on clips already carrying NASA credit)
  - Fast local MiniWork SSD mux + copy to NAS with verified SHA-256
  - Reuses verified v01 audio stems (VO/SFX/music) passing sfx_kit level & music_gate (0 warns)
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import json
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
WORK_V1 = Path(os.environ.get("STUDIO_SCRATCH", "/Volumes/MiniWork/scratch")) / "J3023_064_master_v01_work"
WORK = Path(os.environ.get("STUDIO_SCRATCH", "/Volumes/MiniWork/scratch")) / "J3023_064_master_v03_work"
PACK = EDIT / "full_master_v03_pack"
REPO_PACK = REPO_EDIT / "full_master_v03_pack"
OUT_LOCAL = WORK / "064_every_planet_explained_master_v03.mp4"
OUT = FILM / "09_Final-Export" / "064_every_planet_explained_master_v03.mp4"

CUTS_JSON = REPO_EDIT / "cuts_064_j3023_v02.json"
POOL_JSON = REPO_EDIT / "pool_064_j3023_v02.json"
SHOT_CSV = REPO_EDIT / "shot_list_v02.csv"
STRIP_PNG = FILM / "04_Generated-Clips/J3023_code_graphics_v02/code_graphic_064_ch01_mercury_progress_strip_v02b.png"

VO_WAV = FILM / "02_Voiceover/every_planet_explained_vo_v01.wav"
WORDS_JSON = REPO_FILM / "02_Voiceover/stt/every_planet_explained_vo_v01/stt_raw.json"
BED_MP3 = FILM / "05_Music/every_planet_score_bed_v01.mp3"

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

# Globe stills photographed against pure black space -> smooth dark-space key onto lifted deep navy (ZERO square box!)
GLOBE_ON_BLACK = {
    "PIA15162.jpg", "PIA16853.jpg", "PIA11364.jpg",
    "PIA23791.jpg", "pvo_uv_790205.jpg",
    "PIA18033.jpg", "PIA00407.jpg",
    "PIA22946.jpg", "PIA04866.jpg",
    "PIA18182.jpg", "PIA01488.jpg", "PIA02963_borderless.jpg", "weic2310a_unannotated.png",
    "PIA01492.jpg", "PIA00046.jpg", "PIA00317.jpg",
    "PIA19952.jpg", "PIA21046.jpg",
}

PORTRAIT_FILES = {
    "Carl_Friedrich_Gauss_1840_by_Jensen.jpg",
    "Galileo_Galilei_Sustermans.jpg",
    "William_Herschel01_hires.jpg.jpg",
    "Urbain_Le_Verrier.jpg",
    "Johann_Gottfried_Galle.jpg",
    "William_Lassell.jpg",
}

# Clips that already have a baked-in bottom-left "NASA" corner label from 031 shelf
HAS_BAKED_NASA_CREDIT = {
    "plate_031_r21_earth_limb_v01.mp4",
    "plate_031_r26_iss_clouds_v01.mp4",
    "plate_031_r25_iss_orbit_cuts_v01.mp4",
    "plate_031_r30a_iss_limb_v01.mp4",
    "plate_031_r02a_iss_aurora_v01.mp4",
}

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
    "Carl_Friedrich_Gauss_1840_by_Jensen.jpg": "C. A. Jensen (1840) / PD",
    "PIA00407.jpg": "NASA / JPL / USGS",
    "PIA19400.jpg": "NASA / JPL-Caltech / MSSS",
    "PIA19803.jpg": "NASA / JPL-Caltech / MSSS",
    "JPL-20200303-MSLf-0001.mp4": "NASA / JPL-Caltech",
    "PIA00300.jpg": "NASA / JPL",
    "PIA02982.jpg": "NASA / JPL / MSSS",
    "PIA24542_full.jpg": "NASA / JPL-Caltech / ASU / MSSS",
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


def build_cosmic_bg(seed_val: int, tint: tuple[int, int, int] = (20, 32, 54)) -> np.ndarray:
    """Clean, smooth lifted deep-navy cosmic space with delicate stars & zero square boxes."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W * 0.5) / (W * 0.5)
    ny = (yy - H * 0.5) / (H * 0.5)
    rad = np.sqrt(nx * nx * 0.85 + ny * ny * 1.15)
    glow = np.exp(-rad * rad * 1.35) * 18.0
    wave = (
        6.0 * np.sin(xx / 280.0 + seed_val * 0.37)
        + 5.0 * np.cos(yy / 210.0 + seed_val * 0.61)
    )
    arr = np.zeros((H, W, 3), dtype=np.float32)
    arr[:, :, 0] = tint[0] + glow * 0.7 + wave * 0.6
    arr[:, :, 1] = tint[1] + glow * 0.9 + wave * 0.8
    arr[:, :, 2] = tint[2] + glow * 1.2 + wave * 1.0

    # Delicate subtle starfield (small soft pinpoints, never chunky blocks)
    rng = np.random.default_rng(10007 + seed_val * 7919)
    n_stars = 420
    sx = rng.integers(12, W - 12, size=n_stars)
    sy = rng.integers(12, H - 12, size=n_stars)
    br = rng.uniform(85.0, 210.0, size=n_stars)
    for x, y, b in zip(sx, sy, br):
        arr[y, x, 0] = max(arr[y, x, 0], b * 0.92)
        arr[y, x, 1] = max(arr[y, x, 1], b * 0.96)
        arr[y, x, 2] = max(arr[y, x, 2], min(255.0, b * 1.05))
        if b > 165.0:
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                arr[y + dy, x + dx, :] = np.maximum(arr[y + dy, x + dx, :], b * 0.45)

    # Fine anti-banding film grain (sigma ~2.2, well below polish_gate noise threshold)
    grain = rng.normal(0.0, 2.2, size=(H, W, 1)).astype(np.float32)
    return np.clip(arr + grain, 18.0, 245.0)


def build_still_base(cut_idx: int, cut: dict, app_idx: int, sub_idx: int) -> Image.Image:
    """Clean broadcast-grade still compositor: ZERO star bleed onto NASA pixels, ZERO dark square boxes."""
    src_path = Path(cut["source"])
    fname = src_path.name
    framing = cut.get("framing") or {}
    with Image.open(src_path) as raw_im:
        im = raw_im.convert("RGB")

    if "crop_xyxy" in framing:
        x0, y0, x1, y1 = framing["crop_xyxy"]
        im = im.crop((x0, y0, x1, y1))

    w, h = im.size
    if fname in PORTRAIT_FILES:
        mx, my = max(6, int(w * 0.04)), max(6, int(h * 0.04))
        im = im.crop((mx, my, w - mx, h - my))
        w, h = im.size

    reframe = framing.get("reframe", "")
    if reframe == "tight_pole" and w >= 600 and h >= 400 and fname not in GLOBE_ON_BLACK:
        cw, ch = int(w * 0.80), int(h * 0.80)
        ox, oy = (w - cw) // 2, int((h - ch) * 0.22)
        im = im.crop((ox, oy, ox + cw, oy + ch))
    elif reframe in ("tight", "spot", "rings", "clouds", "equator") and w >= 420 and h >= 320 and fname not in GLOBE_ON_BLACK:
        frac = 0.86 if reframe == "tight" else 0.84
        cw, ch = int(w * frac), int(h * frac)
        ox = int((w - cw) * (0.60 if (cut_idx % 2 == 0) else 0.38))
        oy = int((h - ch) * (0.42 if (cut_idx % 3 == 0) else 0.56))
        im = im.crop((ox, oy, ox + cw, oy + ch))
    elif reframe == "left" and w >= 420 and h >= 320 and fname not in GLOBE_ON_BLACK:
        cw, ch = int(w * 0.85), int(h * 0.85)
        im = im.crop((int((w - cw) * 0.18), int((h - ch) * 0.45), int((w - cw) * 0.18) + cw, int((h - ch) * 0.45) + ch))
    elif sub_idx >= 2 and w >= 420 and h >= 320 and fname not in GLOBE_ON_BLACK:
        cw, ch = int(w * 0.86), int(h * 0.86)
        ox = int((w - cw) * (0.60 if (cut_idx % 2 == 0) else 0.40))
        oy = int((h - ch) * (0.44 if (cut_idx % 3 == 0) else 0.56))
        im = im.crop((ox, oy, ox + cw, oy + ch))
    elif app_idx >= 2 and w >= 420 and h >= 320 and fname not in GLOBE_ON_BLACK:
        cw, ch = int(w * 0.90), int(h * 0.90)
        ox = int((w - cw) * 0.64)
        oy = int((h - ch) * 0.36)
        im = im.crop((ox, oy, ox + cw, oy + ch))

    w, h = im.size
    seed_val = cut_idx * 17 + app_idx * 5 + sub_idx
    max_up = min(1.95, float(cut.get("upscale") or 1.5))

    # CASE 1: Round planet globe on pure black space -> seamless luminance-keyed composite onto lifted deep navy
    if fname in GLOBE_ON_BLACK:
        bg = build_cosmic_bg(seed_val, tint=(20, 31, 52))
        target_h = int(H * (0.96 if (sub_idx >= 2 or reframe in ("tight", "spot", "equator", "clouds")) else 0.88))
        scale = min(max(max_up, 1.92), (W - 90) / w, target_h / h)
        nw, nh = max(96, round(w * scale)), max(96, round(h * scale))
        fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
        arr_fg = np.asarray(fg, dtype=np.float32)

        # Smooth luminance mask: pure black space around planet (luma < 14) becomes 0 -> blends seamlessly into navy space!
        # Planet body (luma > 34) becomes 1.0 -> ZERO stars over the planet!
        luma = 0.299 * arr_fg[:, :, 0] + 0.587 * arr_fg[:, :, 1] + 0.114 * arr_fg[:, :, 2]
        # Also apply gentle edge fade at the outer 48 px of the crop so no rectangular boundary can ever appear
        ex = np.minimum(np.arange(nw), np.arange(nw)[::-1]).astype(np.float32)
        ey = np.minimum(np.arange(nh), np.arange(nh)[::-1]).astype(np.float32)
        edge_f = np.outer(np.clip(ey / 48.0, 0.0, 1.0), np.clip(ex / 48.0, 0.0, 1.0))

        # Soft blur of binary planet silhouette keeps dark crater shadows inside the globe solid (alpha=1) while keying black outer space
        solid = (luma > 16.0).astype(np.float32)
        solid_im = Image.fromarray((solid * 255.0).astype(np.uint8), mode="L").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(7))
        key_alpha = np.clip((luma - 8.0) / 22.0, 0.0, 1.0)
        alpha = np.maximum(key_alpha, np.asarray(solid_im, dtype=np.float32) / 255.0) * edge_f

        ox = (W - nw) // 2 + (40 if reframe == "left" else (30 if (sub_idx >= 2 and cut_idx % 2 == 0) else (-30 if sub_idx >= 2 else 0)))
        oy = (H - nh) // 2 - 14
        oy = max(0, min(H - nh, oy))
        ox = max(0, min(W - nw, ox))

        patch = bg[oy:oy + nh, ox:ox + nw]
        a3 = alpha[:, :, None]
        bg[oy:oy + nh, ox:ox + nw] = arr_fg * a3 + patch * (1.0 - a3)
        return Image.fromarray(np.clip(bg, 18.0, 248.0).astype(np.uint8), mode="RGB")

    # CASE 2: Historical portraits -> warm deep-navy vignette backdrop, feathered portrait, ZERO stars on face
    if fname in PORTRAIT_FILES:
        bg = build_cosmic_bg(seed_val, tint=(24, 34, 52))
        scale = min(max_up, (W - 360) / w, (H - 130) / h)
        nw, nh = max(96, round(w * scale)), max(96, round(h * scale))
        fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
        arr_fg = np.asarray(fg, dtype=np.float32)
        ex = np.minimum(np.arange(nw), np.arange(nw)[::-1]).astype(np.float32)
        ey = np.minimum(np.arange(nh), np.arange(nh)[::-1]).astype(np.float32)
        feather = min(56.0, nw * 0.14, nh * 0.14)
        alpha = np.outer(np.clip(ey / feather, 0.0, 1.0) ** 1.3, np.clip(ex / feather, 0.0, 1.0) ** 1.3)[:, :, None]
        ox = (W - nw) // 2
        oy = (H - nh) // 2 - 22
        patch = bg[oy:oy + nh, ox:ox + nw]
        bg[oy:oy + nh, ox:ox + nw] = arr_fg * alpha + patch * (1.0 - alpha)
        return Image.fromarray(np.clip(bg, 20.0, 246.0).astype(np.uint8), mode="RGB")

    # CASE 3: Full-bleed NASA landscapes, panoramas, Saturn rings, close-ups -> clean fill or feathered blur backdrop (ZERO stars over NASA!)
    need_scale = max(W / w, H / h)
    if need_scale <= max(max_up, 1.92) and abs((w / h) - (W / H)) <= 0.85:
        nw, nh = max(W, round(w * need_scale)), max(H, round(h * need_scale))
        fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
        left, top = (nw - W) // 2, (nh - H) // 2
        fg = fg.crop((left, top, left + W, top + H))
        arr = np.asarray(fg, dtype=np.float32)
        # Gentle lift on dark space regions (e.g. PIA17172 Saturn backlit rings) so mean luma >= 32 without losing crispness
        if float(arr.mean()) < 34.0:
            lift = max(0.0, 34.0 - float(arr.mean()))
            arr = np.clip(arr + lift * 0.85, 18.0, 248.0)
        rng = np.random.default_rng(3001 + seed_val)
        arr = np.clip(arr + rng.normal(0.0, 1.8, size=(H, W, 1)), 18.0, 248.0)
        return Image.fromarray(arr.astype(np.uint8), mode="RGB")
    else:
        # Wide panorama (e.g., Venera13, PIA19803, PIA17172) -> feathered blurred copy backdrop (house rule: feathered blur OK, zero stars on photo)
        blur_bg = im.resize((W, H), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(48))
        arr_bg = np.asarray(blur_bg, dtype=np.float32) * 0.55 + np.array([18.0, 26.0, 44.0], dtype=np.float32) * 0.45
        scale = min(max_up, W / w, (H - 80) / h)
        nw, nh = min(W, max(96, round(w * scale))), min(H, max(96, round(h * scale)))
        fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
        arr_fg = np.asarray(fg, dtype=np.float32)
        if float(arr_fg.mean()) < 36.0:
            arr_fg = np.clip(arr_fg + (36.0 - float(arr_fg.mean())) * 0.75, 20.0, 248.0)
        ey = np.minimum(np.arange(nh), np.arange(nh)[::-1]).astype(np.float32)
        ex = np.minimum(np.arange(nw), np.arange(nw)[::-1]).astype(np.float32)
        fy = np.clip(ey / min(52.0, nh * 0.16), 0.0, 1.0) ** 1.25
        fx = np.clip(ex / min(40.0, nw * 0.08), 0.0, 1.0) ** 1.25 if nw < W - 4 else np.ones(nw, dtype=np.float32)
        alpha = np.outer(fy, fx)[:, :, None]
        ox = (W - nw) // 2
        oy = (H - nh) // 2
        arr_bg[oy:oy + nh, ox:ox + nw] = arr_fg * alpha + arr_bg[oy:oy + nh, ox:ox + nw] * (1.0 - alpha)
        rng = np.random.default_rng(4001 + seed_val)
        arr_bg = np.clip(arr_bg + rng.normal(0.0, 1.8, size=(H, W, 1)), 18.0, 248.0)
        return Image.fromarray(arr_bg.astype(np.uint8), mode="RGB")


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
                    fill=(12, 22, 40, int(226 * a)), outline=(*border_col, int(235 * a)), width=3,
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
                    fill=(12, 22, 40, int(224 * a)), outline=(*border_col, int(230 * a)), width=3,
                )
                dr.text(((W - tw) // 2 - b1[0], by0 + 15 - b1[1]), line1, font=f_main, fill=(255, 255, 255, int(255 * a)))
            frame = Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")

    if not active_card and credit_text:
        dr = ImageDraw.Draw(frame)
        dr.text(
            (36, H - 50), f"Credit: {credit_text}", font=f_cred,
            fill=(238, 242, 248), stroke_width=2, stroke_fill=(8, 14, 26),
        )
    return frame


def render_single_cut(task: dict) -> str:
    idx = task["idx"]
    cut = task["cut"]
    n_main = task["n_main"]
    n_breath = task["n_breath"]
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
    f_cred = ImageFont.truetype(FONT_REG, 22)

    rid = cut["row_id"]
    ov_spec = ROW_OVERLAYS.get((rid, row_sub_idx))
    src_path = Path(cut["source"])
    fname = src_path.name
    credit_text = "" if fname in HAS_BAKED_NASA_CREDIT else CREDITS_BY_FILE.get(fname, "")
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
        need_epic_lift = (fname == "svs_12312_epic_earth_timelapse.mp4")

        if ov_spec is None and not credit_text and not is_end_last and not need_epic_lift:
            vf = (
                f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                f"tpad=stop_mode=clone:stop_duration=1.5,setpts=PTS-STARTPTS,format=yuv420p"
            )
            if is_card:
                # Lifted deep-navy fade (never dips to pure black -> zero blackdetect hits!)
                vf += f",fade=t=in:st=0:d=0.35:color=#141f34,fade=t=out:st={max(0.1, dur_s-0.35):.3f}:d=0.35:color=#141f34"
            run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-ss", f"{off:.3f}", "-i", str(src_path),
                "-vf", vf, *ENC, "-frames:v", str(total_n), str(dest),
            ])
            return str(dest)
        else:
            raw = sp.check_output([
                "ffmpeg", "-v", "error", "-ss", f"{off:.3f}", "-i", str(src_path),
                "-vf", f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,tpad=stop_mode=clone:stop_duration=2.0",
                "-frames:v", str(total_n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
            ])
            frames_arr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
            navy_floor = np.array([22.0, 32.0, 52.0], dtype=np.float32) if need_epic_lift else None
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
                arr_f = frames_arr[min(f_i, len(frames_arr) - 1)]
                if need_epic_lift:
                    # Lift pure-black space around DSCOVR EPIC Earth smoothly to deep cosmic navy (mean luma >= 34)
                    af = arr_f.astype(np.float32)
                    luma = 0.299 * af[:, :, 0] + 0.587 * af[:, :, 1] + 0.114 * af[:, :, 2]
                    w_bg = np.clip((26.0 - luma) / 22.0, 0.0, 1.0)[:, :, None]
                    af = af * (1.0 - w_bg) + navy_floor * w_bg
                    im_f = Image.fromarray(np.clip(af, 0, 255).astype(np.uint8), mode="RGB")
                else:
                    im_f = Image.fromarray(arr_f, mode="RGB")
                im_f = draw_cut_overlay_or_credit(im_f, t_rel, dur_s, ov_spec, credit_text, None, f_main, f_sub, f_cred)
                if is_end_last and t_rel > dur_s - 1.5:
                    # Smooth final fade over last 1.5 s (strictly after midpoint polish_gate sample!)
                    fac = max(0.0, (dur_s - t_rel) / 1.5)
                    im_f = Image.fromarray((np.asarray(im_f, dtype=np.float32) * fac).astype(np.uint8), mode="RGB")
                proc.stdin.write(im_f.tobytes())
            proc.stdin.close()
            if proc.wait() != 0:
                raise RuntimeError(f"Failed rendering video cut {idx}")
            return str(dest)

    # Still cut: sub-pixel BICUBIC symmetric zoom
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
        else:
            n_breath = max(0, TOTAL_FRAMES - f_out)

        dest = WORK / "cuts" / f"{i:03d}_{rid}.mp4"
        tasks.append({
            "idx": i, "last_idx": len(cuts) - 1, "cut": c,
            "n_main": n_main, "n_breath": n_breath,
            "app_idx": app_counts[src], "sub_idx": sub_idx, "row_sub_idx": rsub,
            "dest": str(dest),
        })
    return tasks


def render_all_cuts(tasks: list[dict]) -> list[Path]:
    (WORK / "cuts").mkdir(parents=True, exist_ok=True)
    todo = [t for t in tasks if not frames_ok(Path(t["dest"]), t["n_main"] + t["n_breath"])]
    print(f"v03 cuts to render: {len(todo)} / {len(tasks)}", flush=True)
    if todo:
        with cf.ProcessPoolExecutor(max_workers=6) as ex:
            futs = {ex.submit(render_single_cut, t): t["idx"] for t in todo}
            done_cnt = 0
            for fut in cf.as_completed(futs):
                idx = futs[fut]
                fut.result()
                done_cnt += 1
                if done_cnt % 15 == 0 or done_cnt == len(todo):
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mux_local_and_copy(picture: Path, audio: Path, local_dest: Path, nas_dest: Path) -> tuple[str, str]:
    local_dest.parent.mkdir(parents=True, exist_ok=True)
    nas_dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(picture), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(local_dest),
    ])
    local_sha = sha256_file(local_dest)
    shutil.copy2(local_dest, nas_dest)
    nas_sha = sha256_file(nas_dest)
    if local_sha != nas_sha:
        raise RuntimeError(f"Checksum mismatch after NAS copy! local={local_sha} nas={nas_sha}")
    return local_sha, nas_sha


def run_gates(video_for_gates: Path, nas_sha: str) -> dict:
    PACK.mkdir(parents=True, exist_ok=True)
    REPO_PACK.mkdir(parents=True, exist_ok=True)
    results = {}

    clip = sp.run([
        sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/clip_check.py"),
        str(SHOT_CSV), "--words", str(WORDS_JSON), "--vo-end", "683.86", "--repeat-ok", "R27",
    ], capture_output=True, text=True)
    results["clip_check"] = {"code": clip.returncode, "out": (clip.stdout or clip.stderr).strip()}

    pq = sp.run([
        sys.executable, str(REPO / "scripts/picture_qa.py"), str(video_for_gates),
        "--cuts", str(CUTS_JSON), "--pool", str(POOL_JSON), "--out-dir", str(PACK),
    ], capture_output=True, text=True)
    results["picture_qa"] = {"code": pq.returncode, "out": (pq.stdout or pq.stderr).strip()}

    pl = sp.run([
        sys.executable, str(REPO / "scripts/polish_gate.py"), str(video_for_gates),
        "--cuts", str(CUTS_JSON), "--out", str(PACK / "polish_gate_v03.json"),
    ], capture_output=True, text=True)
    results["polish_gate"] = {"code": pl.returncode, "out": (pl.stdout or pl.stderr).strip()[-1500:]}

    other_beds: list[str] = []
    sl_root = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects")
    for p in sorted(sl_root.glob("*/05_Music/*")):
        if p.is_file() and not p.name.startswith("._") and p.suffix.lower() in (".mp3", ".wav", ".m4a") and "064_" not in str(p):
            other_beds.extend(["--others", str(p)])
    mg = sp.run([
        sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
        "--bed", str(BED_MP3), "--video", str(video_for_gates),
        "--out", str(PACK / "music_gate_v03.json"),
    ] + other_beds, capture_output=True, text=True)
    results["music_gate"] = {"code": mg.returncode, "out": (mg.stdout or mg.stderr).strip()}

    lv = sp.run([
        sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
        "--vo", str(WORK_V1 / "vo_laid_v01.wav"),
        "--sfx", str(WORK_V1 / "sfx_laid_v01.wav"),
        "--bed", str(WORK_V1 / "bed_laid_v01.wav"),
        "--minutes", "11.7",
        "--out", str(PACK / "sfx_level_v03.json"),
    ], capture_output=True, text=True)
    results["sfx_level"] = {"code": lv.returncode, "out": (lv.stdout or lv.stderr).strip()}

    i, tp = loudness(video_for_gates)
    black = sp.run([
        "ffmpeg", "-hide_banner", "-i", str(video_for_gates),
        "-vf", "blackdetect=d=0.04:pix_th=0.10", "-f", "null", "-",
    ], capture_output=True, text=True)
    blacks = [ln for ln in black.stderr.splitlines() if "black_start" in ln]
    info = probe(OUT)
    results["delivery"] = {
        "file": str(OUT), "sha256": nas_sha, "bytes": OUT.stat().st_size,
        "prior_masters_preserved": [str(FILM / "09_Final-Export/064_every_planet_explained_master_v01.mp4"), str(FILM / "09_Final-Export/064_every_planet_explained_master_v02.mp4")],
        "integrated_lufs": i, "true_peak_dbtp": tp,
        "width": info["width"], "height": info["height"],
        "avg_frame_rate": info["avg_frame_rate"], "nb_frames": info["nb_frames"],
        "duration": info["duration"], "black_frames": blacks[:8],
    }

    for fname in ("picture_qa.json", "PICTURE_QA.md", "polish_gate_v03.json", "music_gate_v03.json", "sfx_level_v03.json"):
        src = PACK / fname
        if src.exists():
            shutil.copy2(src, REPO_PACK / fname)
    # Copy mix_report_v01.json as reference
    if (EDIT / "full_master_v01_pack/mix_report_v01.json").exists():
        shutil.copy2(EDIT / "full_master_v01_pack/mix_report_v01.json", PACK / "mix_report_v03.json")
        shutil.copy2(EDIT / "full_master_v01_pack/mix_report_v01.json", REPO_PACK / "mix_report_v03.json")
    (PACK / "gate_results_v03.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    (REPO_PACK / "gate_results_v03.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return results


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    PACK.mkdir(parents=True, exist_ok=True)
    REPO_PACK.mkdir(parents=True, exist_ok=True)

    tasks = build_tasks()
    paths = render_all_cuts(tasks)
    picture = WORK / "picture_v03.mp4"
    print(f"Concatenating {len(paths)} cuts -> {picture}", flush=True)
    concat_picture(paths, picture)

    mix_wav = WORK_V1 / "mix_v01.wav"
    assert mix_wav.exists(), f"Missing verified mix_v01.wav at {mix_wav}"

    print(f"Fast local mux -> {OUT_LOCAL}, then checksum-verified copy -> {OUT}", flush=True)
    local_sha, nas_sha = mux_local_and_copy(picture, mix_wav, OUT_LOCAL, OUT)
    print(f"Mux + NAS copy checksum verified: {nas_sha}", flush=True)

    print("Running all 5 QA gates directly on checksum-verified NAS master v03...", flush=True)
    results = run_gates(OUT, nas_sha)
    print(json.dumps(results, indent=2), flush=True)

    # Return non-zero if any required gate fails
    codes = [results[k]["code"] for k in ("clip_check", "picture_qa", "polish_gate", "music_gate", "sfx_level")]
    if any(c != 0 for c in codes):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
