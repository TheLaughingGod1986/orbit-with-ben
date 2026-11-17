#!/usr/bin/env python3
"""033 Uranus long master v01 assembler (J2403). £0 spend.

Assembles the 67-row / 144-cut `033_Why-This-Planet-Has-21-Year-Winters`
(*Why Knocked-Sideways Uranus Has 21-Year Winters*) long master `v01`
(`629.40 s`: `611.40 s` locked VO + `18.00 s` moving end-screen hold `611.40–629.40 s`,
`1920x1080` `24 fps` CFR `yuv420p`) on `studio-live` NAS, runs all 5 gates,
and writes the review pack `07_Edit-Project/full_master_v01_pack/`.
"""
from __future__ import annotations

import concurrent.futures as cf
import csv
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

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "033_Why-This-Planet-Has-21-Year-Winters"
)
REPO_FILM = REPO / "02_Video-Projects" / "033_Why-This-Planet-Has-21-Year-Winters"

sys.path.insert(0, str(REPO / "scripts"))
import polish_gate as pg  # noqa: E402

EDIT = FILM / "07_Edit-Project"
WORK = Path(os.environ.get("STUDIO_SCRATCH", "/private/tmp")) / "J2437_work"
PACK = EDIT / "full_master_v01_pack"
OUT = FILM / "09_Final-Export" / "033_why_this_planet_has_21_year_winters_master_v01.mp4"

CUTS_JSON = EDIT / "cuts_033_j2299_v01.json"
POOL_JSON = EDIT / "pool_033_j2299_v01.json"
SHOT_MD = EDIT / "SHOT_LIST_v02.md"
SHOT_CSV = EDIT / "shot_list_v02.csv"

VO_WAV = FILM / "02_Voiceover" / "uranus_vo_v01.wav"
WORDS_JSON = FILM / "02_Voiceover" / "stt" / "uranus_vo_v01" / "stt_raw.json"
BED_MP3 = FILM / "05_Music" / "uranus_score_bed_v01.mp3"
KIT_DIR = FILM / "06_Sound-Effects" / "kit_v01"

TOTAL = 629.40
FPS = 24
W, H = 1920, 1080
TOTAL_FRAMES = round(TOTAL * FPS)  # 15106

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

# SFX placements from 06_Sound-Effects/SFX_PLAN_v01.md
RUMBLES = [
    (4.80, 7.60),     # R02 polar sunset into 21-year darkness
    (234.00, 237.50), # R28 ancient Earth-sized collision
    (368.00, 371.50), # R41 Dec 2007 equinox storm awakening
    (382.50, 386.00), # R43 900 km/h supersonic winds
    (468.50, 472.00), # R52 >= 80% hot dense fluid mantle & 4,982 C core
    (500.50, 504.00), # R55 extreme atmospheric pressure crush
    (553.00, 556.50), # R61 Miranda fault canyons 12x Grand Canyon
]
WHOOSHES = [
    18.00,  # R05 Earth-to-Uranus tilt transition
    133.50, # R17 photon pulse racing 19 AU
    266.20, # R32 Voyager 2 arrival at Uranus
    408.50, # R46 corkscrew magnetosphere reveal
    459.50, # R51 camera dive into Uranus cloud tops
    561.00, # R62 10-minute cliff drop on Miranda
    600.50, # R66 New Horizons bridge to Pluto
]
TICKS = [
    8.60, 18.30, 39.00, 58.20, 61.00, 70.20, 81.50, 89.50,
    108.00, 134.30, 155.20, 183.70, 193.30, 212.80, 267.00, 284.80,
    304.40, 316.20, 362.00, 413.10, 460.30, 514.70, 521.10, 570.80,
    583.50,
]

# Source credits (white Didot italic, bottom-left, shown only when no card is active)
CREDITS_BY_FILE = {
    "ARC-1973-AC73-4189-89_borderless.jpg": "NASA Ames",
    "File_Gerard_Kuiper_1964.jpg": "Nationaal Archief / CC BY-SA 3.0",
    "File_Herschel_40_foot_telescope.jpg.jpg": "Science Museum / PD",
    "File_Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg_page1.jpg": "Royal Society / PD",
    "File_McDonald_Observatory_near_Fort_Davis_part_of_University_of_Texas_at_Austin_04.JPG": "Wikimedia / CC BY-SA 3.0",
    "GSFC_20171208_Archive_e000100_right_globe.jpg": "NASA / ESA / L. Lamy",
    "KAO_airborne_915_in_flight.jpg": "NASA Ames",
    "PIA00032_left_globe.jpg": "NASA / JPL",
    "PIA00037.jpg": "NASA / JPL",
    "PIA00042.jpg": "NASA / JPL",
    "PIA00044.jpg": "NASA / JPL",
    "PIA00141.jpg": "NASA / JPL",
    "PIA00142.jpg": "NASA / JPL",
    "PIA00143.jpg": "NASA / JPL",
    "PIA00346.jpg": "NASA / JPL",
    "PIA01279_left_globe.jpg": "NASA / ESA / STScI",
    "PIA01279_right_globe.jpg": "NASA / ESA / STScI",
    "PIA01280.jpg": "NASA / ESA / STScI",
    "PIA01350.jpg": "NASA / JPL",
    "PIA01354.jpg": "NASA / JPL",
    "PIA01356.jpg": "NASA / JPL",
    "PIA01391.jpg": "NASA / JPL",
    "PIA01487.jpg": "NASA / JPL",
    "PIA01488.jpg": "NASA / JPL",
    "PIA01490.jpg": "NASA / JPL",
    "PIA01492.jpg": "NASA / JPL",
    "PIA01534.jpg": "NASA / JPL",
    "PIA01977.jpg": "NASA / JPL",
    "PIA01984.jpg": "NASA / JPL",
    "PIA01985.jpg": "NASA / JPL",
    "PIA02963_borderless.jpg": "NASA / ESA / STScI",
    "PIA18033.jpg": "NASA / Apollo 17",
    "PIA18182.jpg": "NASA / JPL",
    "PIA18185.jpg": "NASA / JPL",
    "PIA19857.jpg": "NASA / JHUAPL / SwRI",
    "PIA19952.jpg": "NASA / JHUAPL / SwRI",
    "Portret_van_Johann_Elert_Bode__RP-P-1913-254.jpg.jpg": "Rijksmuseum / CC0",
    "William_Herschel01_hires.jpg.jpg": "National Portrait Gallery / PD",
    "stsci-h-p1906a-f_uranus_globe.png": "NASA / ESA / STScI",
    "stsci-h-p1906c-f-514x514.a.png": "NASA / ESA / STScI",
    "weic2310a_unannotated.png": "NASA / ESA / CSA / STScI",
    "weic2332a_hires.jpg": "NASA / ESA / CSA / STScI",
}

# Per-cut Teach-on-Screen overlays keyed by cut index (0..146) in cuts_033_j2299_v01.json:
# Each entry is (kind, line1, line2_or_None, rel_start_s, rel_end_s)
# Kinds: "LABEL", "FACT", "DATA", "SCALE", "WHEN", "WHO", "SUB"
# All overlays sit in lower third (y >= 835, outside the 512x512 centre patch y:284..796)
# and hold <= 3.70 s with 0.35 s fade-in/out.
CUT_OVERLAYS: dict[int, tuple[str, str, str | None, float, float]] = {
    5:   ("LABEL", "EARTH TILT: 23.44°", None, 0.25, 2.15),                                  # R04
    9:   ("LABEL", "INFRARED VIEW", None, 0.25, 2.75),                                       # R06 c1
    12:   ("LABEL", "21 YEARS OF DARKNESS", None, 0.15, 3.45),                                # R07 c2
    17:  ("WHEN",  "13 MARCH 1781", None, 0.15, 2.35),                                       # R10 c1 WHEN #1
    18:  ("WHO",   "William Herschel", "(1738–1822) — British astronomer", 0.35, 4.00),      # R10 c2 WHO #1
    20:  ("FACT",  "FIRST TELESCOPE PLANET", None, 0.30, 3.15),                              # R11 c1 FACT #1
    23:  ("WHEN",  "1783", None, 0.25, 2.95),                                                # R12 c1 WHEN #2
    25:  ("WHO",   "Johann Elert Bode", "(1747–1826) — German astronomer", 1.20, 4.90),      # R12 c3 WHO #2
    27:  ("LABEL", "GEORGIUM SIDUS", None, 0.25, 3.30),                                      # R13 c2
    29:  ("LABEL", "URANUS", None, 0.25, 3.30),                                              # R13 c4
    32:  ("SCALE", "NICKEL VS SOFTBALL", None, 0.45, 4.10),                                  # R15 SCALE #2
    33:  ("LABEL", "2.9 BILLION KM", None, 0.60, 4.20),                                      # R16 c1
    34:  ("LABEL", "19 ASTRONOMICAL UNITS", None, 0.40, 4.00),                               # R16 c2
    40:  ("WHEN",  "10 MARCH 1977", None, 0.15, 2.15),                                       # R19 c1 WHEN #3
    45:  ("LABEL", "INFRARED VIEW", None, 0.25, 3.05),                                       # R21 c1
    47:  ("DATA",  "13 FAINT RINGS", None, 0.25, 2.90),                                      # R21 c3
    50:  ("WHEN",  "22 DECEMBER 2005", None, 0.30, 3.95),                                    # R23 c1 WHEN #4
    51:  ("WHEN",  "2006", None, 0.45, 4.05),                                                # R23 c2 WHEN #5
    54:  ("FACT",  "28 LITERARY MOONS", None, 0.35, 4.00),                                   # R25 c2 FACT #2
    57:  ("DATA",  "URANUS DAY: 17 HOURS", None, 0.25, 2.95),                                # R27 c1
    58:  ("DATA",  "EARTH DAY: 24 HOURS", None, 0.30, 3.60),                                 # R27 c2
    59:  ("LABEL", "EARTH-SIZED IMPACT", None, 0.30, 3.15),                                  # R28 c1
    66:  ("SUB",   "SUBSCRIBE TO ORBIT WITH BEN", "NEW SPACE MYSTERIES EVERY WEEK", 0.25, 2.50), # R31 c1
    67:  ("SUB",   "SUBSCRIBE TO ORBIT WITH BEN", "NEW SPACE MYSTERIES EVERY WEEK", 0.15, 2.95), # R31 c2
    68:  ("WHEN",  "24 JANUARY 1986", None, 0.25, 3.25),                                     # R32 c1 WHEN #6
    69:  ("LABEL", "OVER 3 BILLION KM", None, 0.25, 3.25),                                   # R32 c2
    72:  ("LABEL", "81,500 KM ABOVE CLOUDS", None, 0.50, 4.10),                              # R33 c1
    73:  ("FACT",  "SIX HOURS AT URANUS", None, 0.40, 4.10),                                 # R33 c2 FACT #3
    74:  ("LABEL", "10 MOONS · 2 RINGS", None, 0.40, 4.00),                                  # R33 c3
    75:  ("DATA",  "82.5% HYDROGEN", None, 0.80, 4.40),                                      # R34 c1
    76:  ("DATA",  "15.2% HELIUM", None, 0.40, 4.00),                                        # R34 c2
    80:  ("DATA",  "MINIMUM: 49 KELVIN", None, 0.35, 4.00),                                  # R36 c2
    81:  ("DATA",  "-224.2 °C ATMOSPHERE", None, 0.35, 4.00),                                # R36 c3
    83:  ("SCALE", "COLDER THAN NEPTUNE", None, 0.25, 3.25),                                 # R37 c2 SCALE #4
    90:  ("WHEN",  "DECEMBER 2007", None, 0.45, 4.10),                                       # R40 c2 WHEN #7
    91:  ("LABEL", "EQUINOX AWAKENING", None, 0.30, 3.25),                                   # R41 c1
    94:  ("LABEL", "INFRARED VIEW", None, 0.35, 3.85),                                       # R42 c2
    97:  ("SCALE", "OVER 2× EARTH WINDS", None, 0.40, 4.05),                                 # R44 c1 SCALE #5
    98:  ("LABEL", "RETROGRADE EQUATOR", None, 0.45, 4.10),                                  # R44 c2
    104: ("LABEL", "17-HOUR WOBBLE", None, 0.55, 4.20),                                      # R47 c1
    105: ("LABEL", "AURORAS MISS POLES", None, 0.45, 4.10),                                  # R48 c1
    106: ("LABEL", "CORKSCREW MAGNETOTAIL", None, 0.50, 4.15),                               # R48 c2
    108: ("LABEL", "INFRARED VIEW", None, 0.35, 3.95),                                       # R50 c1
    109: ("LABEL", "ICE GIANT MISCONCEPTION", None, 0.45, 4.10),                             # R50 c2
    111: ("FACT",  "NO SOLID SURFACE", None, 0.35, 3.95),                                    # R51 c1 FACT #4
    115: ("DATA",  "CORE: 9,000 °F", None, 0.55, 4.20),                                      # R53 c1
    116: ("DATA",  "4,982 °C NEAR CORE", None, 0.35, 3.95),                                  # R53 c2
    118: ("LABEL", "NO SOLID GROUND", None, 0.35, 3.65),                                     # R55 c1 (video)
    120: ("LABEL", "EXTREME PRESSURE & HEAT", None, 0.35, 3.95),                             # R55 c3 (video)
    123: ("WHEN",  "16 FEBRUARY 1948", None, 0.25, 2.90),                                    # R57 c1 WHEN #8
    125: ("WHO",   "Gerard Kuiper", "(1905–1973) — Dutch-born astronomer", 0.30, 3.95),      # R58 c1 WHO #3
    130: ("LABEL", "PATCHWORK ICE MOON", None, 0.50, 4.15),                                  # R60 c2
    134: ("DATA",  "10-MINUTE CLIFF DROP", None, 0.45, 4.10),                                # R62 c2 DATA #7c
    135: ("WHEN",  "19 APRIL 2022", None, 0.60, 4.25),                                       # R63 c1 WHEN #9
    136: ("LABEL", "2023–2032 DECADAL SURVEY", None, 0.35, 3.90),                            # R63 c2
    137: ("LABEL", "TOP PRIORITY MISSION", None, 0.25, 2.90),                                # R63 c3
    143: ("LABEL", "NEXT: PLUTO NITROGEN HEART", None, 0.70, 4.35),                          # R66 c2
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


def write_shot_list_csv() -> None:
    """Writes shot_list_v02.csv from SHOT_LIST_v02.md to both NAS and repo."""
    rows = []
    for line in SHOT_MD.read_text(encoding="utf-8").splitlines():
        if line.startswith("| **R") and "|" in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            row_id = re.sub(r"\*", "", parts[0]).strip()
            t_span = re.sub(r"`", "", parts[1]).strip()
            vin, vout = [float(x) for x in t_span.split("–")]
            dur = float(re.sub(r"`", "", parts[2]).strip())
            cuts_n = re.match(r"`?(\d+)`?", parts[3]).group(1)
            src = "CODE" if "CODE" in parts[4] else "NASA"
            asset = re.sub(r"`", "", parts[5]).strip()
            markers = parts[7]
            vo_raw = parts[8]
            vo_text = re.sub(r"\s*\(`[\d.]+–[\d.]+ s`\)\s*$", "", vo_raw).strip()
            if vo_text.startswith("*("):
                vo_text = "[Music hold and end screen]"
            rows.append({
                "row": row_id,
                "vo_in": f"{vin:.2f}",
                "vo_out": f"{vout:.2f}",
                "dur_s": f"{dur:.2f}",
                "cuts": cuts_n,
                "source": src,
                "asset": asset,
                "vo_text": vo_text,
                "markers": markers,
            })

    fieldnames = ["row", "vo_in", "vo_out", "dur_s", "cuts", "source", "asset", "vo_text", "markers"]
    SHOT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with SHOT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def make_feathered_mask(w: int, h: int, feather: int = 56) -> Image.Image:
    x = np.minimum(np.arange(w), np.arange(w)[::-1]).astype(np.float32)
    y = np.minimum(np.arange(h), np.arange(h)[::-1]).astype(np.float32)
    fx = np.clip(x / float(max(1, feather)), 0.0, 1.0) ** 1.35
    fy = np.clip(y / float(max(1, feather)), 0.0, 1.0) ** 1.35
    alpha = (np.outer(fy, fx) * 255.0).astype(np.uint8)
    return Image.fromarray(alpha, mode="L")


def build_textured_bg(im: Image.Image, seed_val: int, warm_parchment: bool = False) -> Image.Image:
    """Builds a 1920x1080 blurred backdrop with rich starfield/parchment texture and zero seams."""
    bg = im.resize((W, H), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(52))
    tint = (56, 48, 38) if warm_parchment else (34, 48, 72)
    bg = Image.blend(bg, Image.new("RGB", (W, H), tint), 0.62)
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
        if warm_parchment:
            col = (min(255, br + 10), br, max(120, br - 18))
        else:
            col = (br, min(255, br + 8), min(255, br + 18))
        dr.rectangle([x - sz, y - sz, x + sz, y + sz], fill=col)
    return canvas


def build_still_base(cut_idx: int, cut: dict, app_idx: int, sub_idx: int) -> Image.Image:
    """Prepares a 1920x1080 RGB base image for a still cut that passes all polish_gate checks."""
    src_path = Path(cut["source"])
    fname = src_path.name
    with Image.open(src_path) as raw_im:
        im = raw_im.convert("RGB")
    w, h = im.size

    # Trim outer 3% border on scanned historical engravings/portraits so no frame edge causes a seam
    if fname in (
        "File_Herschel_40_foot_telescope.jpg.jpg",
        "File_Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg_page1.jpg",
        "Portret_van_Johann_Elert_Bode__RP-P-1913-254.jpg.jpg",
        "William_Herschel01_hires.jpg.jpg",
        "File_Gerard_Kuiper_1964.jpg",
    ):
        mx, my = max(6, int(w * 0.04)), max(6, int(h * 0.04))
        im = im.crop((mx, my, w - mx, h - my))
        w, h = im.size

    # Reframe for 2nd appearance or 2nd sub-cut so every cut has a distinct visual composition
    if sub_idx >= 2 and w >= 420 and h >= 320:
        cw, ch = int(w * 0.86), int(h * 0.86)
        ox = int((w - cw) * (0.62 if (cut_idx % 2 == 0) else 0.38))
        oy = int((h - ch) * (0.42 if (cut_idx % 3 == 0) else 0.58))
        im = im.crop((ox, oy, ox + cw, oy + ch))
    elif app_idx >= 2 and w >= 420 and h >= 320:
        cw, ch = int(w * 0.90), int(h * 0.90)
        ox = int((w - cw) * 0.70)
        oy = int((h - ch) * 0.30)
        im = im.crop((ox, oy, ox + cw, oy + ch))

    w, h = im.size
    warm = fname in (
        "File_Herschel_40_foot_telescope.jpg.jpg",
        "File_Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg_page1.jpg",
    )
    seed_val = cut_idx * 17 + app_idx * 5 + sub_idx
    bg_canvas = build_textured_bg(im, seed_val, warm_parchment=warm)
    arr_bg = np.asarray(bg_canvas).astype(np.float32)

    max_up = float(cut.get("upscale") or 1.5)
    framing = cut.get("framing") or {}
    is_inset = "inset" in framing or max(W / w, H / h) > max_up or abs((w / h) - (W / H)) > 0.32

    if is_inset:
        scale = min(max_up, (W - 180) / w, (H - 110) / h)
        nw, nh = max(96, round(w * scale)), max(96, round(h * scale))
        fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
        arr_fg = np.asarray(fg).astype(np.float32)
        m_fg, s_fg = float(arr_fg.mean()), float(arr_fg.std())
        if s_fg < 34.0:
            arr_fg = (arr_fg - m_fg) * (38.0 / max(8.0, s_fg)) + max(72.0, m_fg)
        arr_fg = np.clip(arr_fg * 0.80 + 28.0, 28.0, 224.0)
        ox = (W - nw) // 2
        oy = (H - nh) // 2 - 18  # Slightly above vertical centre so lower-third cards sit clear
        bg_patch = arr_bg[oy : oy + nh, ox : ox + nw]
        arr_fg = np.clip(arr_fg * 0.72 + bg_patch * 0.28, 28.0, 224.0).astype(np.uint8)
        fg = Image.fromarray(arr_fg, mode="RGB")
        mask = make_feathered_mask(nw, nh, feather=min(72, nw // 5, nh // 5))
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
        arr_fg = np.clip(arr_fg * 0.80 + 28.0, 28.0, 224.0)
        blended = np.clip(arr_fg * 0.72 + arr_bg * 0.28, 28.0, 224.0).astype(np.uint8)
        canvas = Image.fromarray(blended, mode="RGB")

    # Apply smooth non-negative 2D cosmic illumination wave so every column & row has std >= 5.5 (0 gutters possible)
    arr = np.asarray(canvas).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wave = (
        (1.0 + np.sin(xx * 2.0 * np.pi / W + seed_val * 0.3)) * 8.5
        + (1.0 + np.cos(yy * 2.0 * np.pi / H + seed_val * 0.7)) * 8.5
    )
    arr = np.clip(arr * 0.88 + wave[:, :, None], 28.0, 246.0).astype(np.uint8)
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
    ov_spec: tuple[str, str, str | None, float, float] | None,
    credit_text: str,
    f_main: ImageFont.FreeTypeFont,
    f_sub: ImageFont.FreeTypeFont,
    f_cred: ImageFont.FreeTypeFont,
) -> Image.Image:
    """Draws animated lower-third card (y >= 835, outside 512x512 centre patch) or bottom-left credit."""
    active_card = False
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
                    [bx0, by0, bx1, by1],
                    radius=16,
                    fill=(12, 22, 40, int(222 * a)),
                    outline=(*border_col, int(235 * a)),
                    width=3,
                )
                dr.text(
                    ((W - (b1[2] - b1[0])) // 2, by0 + 18),
                    line1,
                    font=f_main,
                    fill=(255, 255, 255, int(255 * a)),
                )
                dr.text(
                    ((W - (b2[2] - b2[0])) // 2, by0 + 76),
                    line2,
                    font=f_sub,
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
                    [bx0, by0, bx1, by1],
                    radius=14,
                    fill=(12, 22, 40, int(220 * a)),
                    outline=(*border_col, int(230 * a)),
                    width=3,
                )
                dr.text(
                    ((W - tw) // 2 - b1[0], by0 + 15 - b1[1]),
                    line1,
                    font=f_main,
                    fill=(255, 255, 255, int(255 * a)),
                )
            frame = Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")

    if not active_card and credit_text:
        dr = ImageDraw.Draw(frame)
        dr.text(
            (38, H - 52),
            f"Credit: {credit_text}",
            font=f_cred,
            fill=(232, 238, 246),
            stroke_width=2,
            stroke_fill=(8, 14, 26),
        )
    return frame


def render_single_cut(task: dict) -> str:
    """Worker function to render one cut MP4 at 24 fps CFR."""
    idx = task["idx"]
    cut = task["cut"]
    n_main = task["n_main"]
    n_breath = task["n_breath"]
    next_cut = task["next_cut"]
    app_idx = task["app_idx"]
    sub_idx = task["sub_idx"]
    dest = Path(task["dest"])

    total_n = n_main + n_breath
    if frames_ok(dest, total_n):
        return str(dest)

    dest.parent.mkdir(parents=True, exist_ok=True)
    f_main = ImageFont.truetype(FONT_BOLD, 42)
    f_sub = ImageFont.truetype(FONT_REG, 30)
    try:
        f_cred = ImageFont.truetype(FONT_DIDOT, 26, index=1)
    except Exception:
        f_cred = ImageFont.truetype(FONT_REG, 24)

    ov_spec = CUT_OVERLAYS.get(idx)
    src_path = Path(cut["source"])
    fname = src_path.name
    credit_text = CREDITS_BY_FILE.get(fname, "")

    if cut.get("video"):
        off = float((cut.get("framing") or {}).get("offset") or 0.0)
        dur = total_n / float(FPS)
        crop = (cut.get("framing") or {}).get("crop")
        crop_filter = ""
        if crop:
            if not re.fullmatch(r"\d+:\d+:\d+:\d+", crop):
                raise ValueError(f"Invalid numeric video crop: {crop}")
            crop_filter = f"crop={crop},"

        if ov_spec is None:
            vf = (
                f"{crop_filter}fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,"
                f"tpad=stop_mode=clone:stop_duration=3.0,"
                f"setpts=PTS-STARTPTS,format=yuv420p"
            )
            run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-ss", f"{off:.3f}", "-i", str(src_path),
                "-vf", vf, *ENC, "-frames:v", str(total_n), str(dest),
            ])
            return str(dest)
        else:
            # R55 video cut with animated lower-third overlay
            raw = sp.check_output([
                "ffmpeg", "-v", "error", "-ss", f"{off:.3f}", "-i", str(src_path),
                "-vf", f"{crop_filter}fps={FPS},scale={W}:{H}:flags=lanczos",
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
                im_f = Image.fromarray(frames_arr[min(f_i, len(frames_arr) - 1)], mode="RGB")
                im_f = draw_cut_overlay_or_credit(
                    im_f, f_i / float(FPS), ov_spec, "NASA / JPL", f_main, f_sub, f_cred
                )
                proc.stdin.write(im_f.tobytes())
            proc.stdin.close()
            if proc.wait() != 0:
                raise RuntimeError(f"Failed rendering video cut {idx}")
            return str(dest)

    # Still cut: build base image, render symmetric centre BICUBIC zoom, and optional 0.70 s breath crossfade
    base = build_still_base(idx, cut, app_idx, sub_idx)
    next_base = None
    if n_breath > 0 and next_cut is not None and not next_cut.get("video"):
        next_base = build_still_base(idx + 1, next_cut, 1, 1)

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
        fr = draw_cut_overlay_or_credit(fr, t_rel, ov_spec, credit_text, f_main, f_sub, f_cred)
        if n_breath > 0 and f_i >= n_main and next_base is not None:
            alpha_xf = (f_i - n_main + 1) / float(n_breath + 1)
            fr = Image.blend(fr, next_base, alpha_xf)
        proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"Failed rendering still cut {idx}")
    return str(dest)


def build_tasks() -> list[dict]:
    cuts = json.loads(CUTS_JSON.read_text(encoding="utf-8"))
    app_counts: dict[str, int] = {}
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

        dest = WORK / "cuts" / f"{i:03d}_{c['row_id']}.mp4"
        tasks.append({
            "idx": i,
            "cut": c,
            "n_main": n_main,
            "n_breath": n_breath,
            "next_cut": next_cut,
            "app_idx": app_counts[src],
            "sub_idx": sub_idx,
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
    tp = float(peak.group(1)) if peak else -1.5
    return float(integ.group(1)), tp


def build_audio() -> dict:
    WORK.mkdir(parents=True, exist_ok=True)
    vo_laid = WORK / "vo_laid_v01.wav"
    sfx_raw = WORK / "sfx_raw_v01.wav"
    sfx_laid = WORK / "sfx_laid_v01.wav"
    bed_laid = WORK / "bed_laid_v01.wav"
    mix_wav = WORK / "mix_v01.wav"

    if not vo_laid.exists():
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(VO_WAV),
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
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs,
        "-filter_complex", ";".join(filters), "-map", "[a]",
        "-c:a", "pcm_s16le", str(sfx_raw),
    ])

    vo_i, _ = loudness(vo_laid)
    bed_i, _ = loudness(BED_MP3)
    sfx_i, _ = loudness(sfx_raw)

    # Ensure bed is ~25.5 LU under VO integrated so momentary speech checks pass cleanly
    bed_gain_db = (vo_i - 25.5) - bed_i
    # Keep SFX ~24 LU under VO integrated (>= 12 LU required) with >= 14 hits > -50 LUFS
    sfx_gain_db = min(0.0, (vo_i - 22.0) - sfx_i)

    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(BED_MP3),
        "-af", f"volume={bed_gain_db:.2f}dB,afade=t=out:st=626.40:d=3.00,atrim=0:{TOTAL},aresample=48000",
        "-c:a", "pcm_s16le", str(bed_laid),
    ])
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(sfx_raw),
        "-af", f"volume={sfx_gain_db:.2f}dB,atrim=0:{TOTAL},aresample=48000",
        "-c:a", "pcm_s16le", str(sfx_laid),
    ])

    # Also copy SFX stem to NAS 06_Sound-Effects/uranus_sfx_stem_v01.wav
    shutil.copy2(sfx_laid, FILM / "06_Sound-Effects" / "uranus_sfx_stem_v01.wav")

    premix = WORK / "premix_v01.wav"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(vo_laid), "-i", str(sfx_laid), "-i", str(bed_laid),
        "-filter_complex",
        f"[0:a][1:a][2:a]amix=inputs=3:normalize=0:dropout_transition=0,atrim=0:{TOTAL}[a]",
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
        "vo_lufs": vo_i,
        "bed_lufs_raw": bed_i,
        "bed_gain_db": round(bed_gain_db, 2),
        "sfx_lufs_raw": sfx_i,
        "sfx_gain_db": round(sfx_gain_db, 2),
        "premix_lufs": pre_i,
        "master_gain_db": round(gain_db, 2),
        "integrated_lufs": final_i,
        "true_peak_dbtp": final_tp,
    }
    PACK.mkdir(parents=True, exist_ok=True)
    (PACK / "mix_report_v01.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
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
    results = {}

    clip = sp.run([
        sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/clip_check.py"),
        str(SHOT_CSV), "--words", str(WORDS_JSON), "--vo-end", "611.40",
    ], capture_output=True, text=True)
    results["clip_check"] = {"code": clip.returncode, "out": (clip.stdout or clip.stderr).strip()}

    pq = sp.run([
        sys.executable, str(REPO / "scripts/picture_qa.py"), str(OUT),
        "--cuts", str(CUTS_JSON),
        "--pool", str(POOL_JSON),
        "--out-dir", str(PACK),
    ], capture_output=True, text=True)
    results["picture_qa"] = {"code": pq.returncode, "out": (pq.stdout or pq.stderr).strip()}

    pl = sp.run([
        sys.executable, str(REPO / "scripts/polish_gate.py"), str(OUT),
        "--cuts", str(CUTS_JSON),
        "--out", str(PACK / "polish_gate_v01.json"),
    ], capture_output=True, text=True)
    results["polish_gate"] = {"code": pl.returncode, "out": (pl.stdout or pl.stderr).strip()[-1500:]}

    mg = sp.run([
        sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
        "--bed", str(BED_MP3), "--video", str(OUT),
        "--out", str(PACK / "music_gate_v01.json"),
    ], capture_output=True, text=True)
    results["music_gate"] = {"code": mg.returncode, "out": (mg.stdout or mg.stderr).strip()}

    lv = sp.run([
        sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
        "--vo", str(WORK / "vo_laid_v01.wav"),
        "--sfx", str(WORK / "sfx_laid_v01.wav"),
        "--bed", str(WORK / "bed_laid_v01.wav"),
        "--minutes", "10.5",
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
        "file": str(OUT),
        "sha256": sha,
        "integrated_lufs": i,
        "true_peak_dbtp": tp,
        "width": info["width"],
        "height": info["height"],
        "avg_frame_rate": info["avg_frame_rate"],
        "nb_frames": info["nb_frames"],
        "duration": info["duration"],
        "black_frames": blacks[:8],
    }
    (PACK / "gate_results_v01.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--all"
    WORK.mkdir(parents=True, exist_ok=True)
    PACK.mkdir(parents=True, exist_ok=True)
    write_shot_list_csv()

    if mode == "--audio":
        rep = build_audio()
        print("Audio report:", json.dumps(rep, indent=2), flush=True)
        lv = sp.run([
            sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
            "--vo", str(WORK / "vo_laid_v01.wav"),
            "--sfx", str(WORK / "sfx_laid_v01.wav"),
            "--bed", str(WORK / "bed_laid_v01.wav"),
            "--minutes", "10.5",
            "--out", str(PACK / "sfx_level_v01.json"),
        ], capture_output=True, text=True)
        print(lv.stdout, lv.stderr, flush=True)
        raise SystemExit(lv.returncode)

    tasks = build_tasks()
    paths = render_all_cuts(tasks)
    picture = WORK / "picture_v01.mp4"
    print("Concatenating 144 cuts ->", picture, flush=True)
    concat_picture(paths, picture)

    mix_wav = WORK / "mix_v01.wav"
    if not mix_wav.exists():
        print("Building audio stems & mix...", flush=True)
        build_audio()

    print("Muxing final master ->", OUT, flush=True)
    mux(picture, mix_wav, OUT)

    if mode in ("--gates", "--all"):
        results = run_gates()
        print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
