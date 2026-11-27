#!/usr/bin/env python3
"""032 Titan — Short #2 v03 Assembler (J3865 Chief FIX follow-up to J3856 / J3853).

Full-bleed 1080x1920 (9:16), 30 fps CFR. Zero centre-band blur pad, zero integer
star-crop push jitter, zero corner halo, zero barred RLSJm59OSzI assets.
Scratch stays on /Volumes/MiniWork (never fills /).

Fixes all Chief FIX requirements from jobs/reviews/J3856/REVIEW.md (7bcaa478f7):
  1. S03 picture-to-words accuracy (4.733-8.500 s, "but when Cassini swept its radar
     across Titan's North Pole"): removes v02 Dragonfly surface footage and replaces it
     with official NASA/GSFC SVS 12709 moving Cassini-over-Titan footage
     (GSFC_20170912_Cassini_m12709_CIRS_Short~orig.mp4, XMP ingredient
     Cassini_Saturn_Animation_Reel.mov, window 260.000-263.767 s, 1920x1080 30fps,
     audio stripped -an, native upscale 1.78x <= 2.35x, verified fixed-crop native
     motion diff min=3.60 / median=5.84 / max=6.97). Selected via bounded external
     NASA/JPL search (option A: 2 of 3 deep candidates examined; PIA17656 rejected at
     1280x720 -> 2.67x > 2.35x).
  2. S08 simplified, readable, locked-spoken-word graphic (20.400-24.000 s):
     removes unspoken "55-80 KM BELOW" range and right-side bracket; expands cutaway
     column to 636 px wide so all main teaching labels (TITAN, ICY CRUST, HIDDEN OCEAN,
     LIQUID WATER) render at 68 px (11.18% of the 608 px 16:9 safe band, within 67-73 px)
     using exact locked spoken wording timed strictly from words.json:
       - 20.400-21.000 s: real Cassini ISS Titan (PIA14602) + ICY CRUST (zero ocean spoiler)
       - 21.000 s ("second", 78.1% >= 70.0%): open-bottomed cyan subsurface layer sweeps in
       - 21.520 s ("hidden"): HIDDEN OCEAN reveals on one bold 68 px line
       - 22.960 s ("liquid"): LIQUID WATER reveals on one bold 68 px line
       - Subordinate qualitative disclaimer: NOT TO SCALE (26 px, no invented proportions)
  3. S04 clean full-frame reframing preserved (8.500-12.067 s): PIA21434.jpg interior
     9:16 crop (460, 150, 949, 1020), z1=1.02, upscale 2.25x <= 2.35x (verified
     mathematically as the largest border-free interior 9:16 crop on PIA21434.jpg),
     with crisp UnsharpMask checked full-size for softness.
  4. Reproducible evidence: writes v03 beside preserved v01 and v02 on NAS with verified
     SHA-256s, corrected full-size stills, dedicated phone-size graphic preview, 10-shot
     contact sheet, captions, full bounded external search log, provenance, E1 metrics,
     and all 7 fresh gates + canonical MP3 music uniqueness check.

Title: Is Titan Just a Dry Desert?
Alt Title: Does Saturn's Moon Titan Hide Two Oceans?
Slug / Stem: dry_desert_two_oceans / 032_short_dry_desert_two_oceans_v03
Gate Check Date (UNAPPROVED SLOT — never uploaded here): 2026-12-26
Parent Long (032): What Would Happen If You Landed on Titan? (Seas of Liquid Gas) [T3cBBss1F60]

Lifts verbatim whole sentences S44, S45, S46, S52 (65 spoken words) from locked master VO
`02_Voiceover/titan_landing_vo_v02b.wav` with tightened <0.25 s inter-sentence breaths
(26.900 s total runtime, 807 frames at 30 fps CFR, zero end card / zero CTA per OWB-2026-11-E1).
£0 spend, zero generation, zero YouTube upload, zero Buffer/UPLOADS/slot changes.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import subprocess as sp
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "032_What-Would-Happen-If-You-Landed-On-Titan"
)
NAS_HARV = NAS_FILM / "03_Reference-Material" / "harvest_J2089_v01"
NAS_HARV_J3865 = NAS_FILM / "03_Reference-Material" / "harvest_J3865_v01"
NAS_SVS = NAS_HARV / "svs_20311"
NAS_SHORTS = NAS_FILM / "10_Shorts"
SHORT_SLUG = "dry_desert_two_oceans"
STEM = "032_short_dry_desert_two_oceans_v03"
NAS_SUB_OUT = NAS_SHORTS / SHORT_SLUG / "06_Final-Exports"

MASTER_V02 = NAS_FILM / "09_Final-Export" / "032_what_would_happen_if_you_landed_on_titan_master_v02.mp4"
EXPECTED_MASTER_SHA256 = "519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073"
VO_WAV = NAS_FILM / "02_Voiceover" / "titan_landing_vo_v02b.wav"
EXPECTED_VO_SHA256 = "55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5"
STT_JSON = NAS_FILM / "02_Voiceover" / "stt" / "titan_landing_vo_v02b" / "stt_raw.json"
BED_MP3 = NAS_FILM / "05_Music" / "titan_score_bed_v01.mp3"
EXPECTED_BED_SHA256 = "02c7d95865f8b39de4f9d3dfda8aa85084ecea04fc56dbd6776268279dab8f9e"
KIT_DIR = NAS_FILM / "06_Sound-Effects" / "kit_v01"
EXPECTED_S03_SHA256 = "96749f161f522658833e9fff4f61d17170eb99d11c1fc7a82885bddaee982fa9"

WORK = Path("/Volumes/MiniWork/scratch/J3865_032_short2_v03")

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import gate_shorts_open as gso  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 30
SR = 48000
BAND_H = round(W * 9 / 16)          # 608 px (safe zone for title/teach graphics; picture is full 1080x1920)
BAND_Y0 = (H - BAND_H) // 2         # 656 px
BAND_Y1 = BAND_Y0 + BAND_H          # 1264 px
LINE_H = round(BAND_H * 0.115)      # 70 px (11.51% of 608 px safe band — target 67-73 px / 11-12%)
TEACH_FONT_PX = 68                  # 68 / 608 = 11.18% (strictly inside 67-73 px / 11-12%)

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)         # #FFE000
GOLD = (255, 207, 64, 255)
CYAN = (110, 225, 250, 255)
NAVY_FLOOR = np.array([28.0, 38.0, 58.0], dtype=np.float32)

SHORT_TITLE = "Is Titan Just a Dry Desert?"
ALT_TITLE = "Does Saturn's Moon Titan Hide Two Oceans?"
AIR_DATE = "2026-12-26"             # Non-colliding gate-check date ONLY; NOT an approved schedule slot
LONG_ID = "T3cBBss1F60"
LONG_TITLE = "What Would Happen If You Landed on Titan? (Seas of Liquid Gas)"

TITLE_ROWS = [
    "What Would Happen",
    "If You Landed on Titan?",
    "(Seas of Liquid Gas)",
]
HOOK_ROWS = [("DRY", WHITE), ("DESERT?", YELLOW)]
COVER_ROWS = [("TITAN'S", WHITE), ("2 OCEANS?", YELLOW)]

HOOK_END = 1.90
TITLE_IN, TITLE_OUT = 9.00, 14.00

# Verbatim S44, S45, S46, S52 from titan_landing_vo_v02b.wav (65 spoken words), tightened breaths < 0.25 s:
VO_SEGMENTS = [
    (322.660, 324.440),  # S44: Is Titan just a dry desert?
    (325.320, 325.700),  # S45: Wrong.
    (326.240, 337.840),  # S46: The equator may be lined with dunes, but when Cassini swept its radar across Titan's North Pole, it uncovered a drowned coastline of bays and islands filled with liquid natural gas.
    (373.104, 385.064),  # S52: And far beneath Titan's icy crust, tens of kilometers down, Cassini's gravity measurements revealed a second hidden ocean of liquid water likely mixed with salts and ammonia.
]
VO_LEAD_S = 0.060
VO_GAPS = [0.150, 0.150, 0.160]
TOTAL_S = 26.900              # 807 frames at 30 fps CFR (strictly inside 22-27 s; tail = 0.660 s < 1.20 s)

# 10-shot full-bleed 9:16 cut plan (every cut on an exact 30fps frame inside a verified word silence gap;
# Cut 1 = 1.900 s <= 2.80 s, Cut 2 = 4.733 s <= 4.80 s, max shot = 3.767 s <= 4.00 s;
# S01-S03 (0.000-8.500 s) are 100% real moving official NASA video (video=True, zero still zoom in 1.9-8.5 s);
# S03 now shows the actual Cassini orbiter sweeping past Titan (NASA SVS 12709, zero Dragonfly hardware);
# zero barred RLSJm59OSzI assets [PIA14925, PIA06230, PIA09739, PIA21625]).
SHOT_PLAN = [
    {
        "row": "S01_open",
        "in": 0.000,
        "out": 1.900,
        "kind": "svs_pan",
        "source": "SVS20311_DF_Open_1080.mp4",
        "title": "Dragonfly Unfolding on Titan Golden Dunes (SVS 20311)",
        "credit": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
        "offset": 1.800,
        "video": True,
        "x0_start": 260.0,
        "x0_end": 540.0,
    },
    {
        "row": "S02_dunes",
        "in": 1.900,
        "out": 4.733,
        "kind": "svs_pan",
        "source": "SVS20311_DF_End_Pan_1080.mp4",
        "title": "Sweeping Camera Pan Across Titan Towering Golden Dunes (SVS 20311)",
        "credit": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
        "offset": 0.100,
        "video": True,
        "x0_start": 1180.0,
        "x0_end": 1312.0,
    },
    {
        "row": "S03_cassini_titan_flyby",
        "in": 4.733,
        "out": 8.500,
        "kind": "svs_pan_soft",
        "source": "SVS12709_Cassini_Titan_Flyby_260_264_1080.mp4",
        "title": "Cassini Orbiter Flying Across Titan (NASA SVS 12709 / Cassini Saturn Animation Reel)",
        "credit": "NASA/Goddard Space Flight Center/JPL-Caltech",
        "offset": 0.033,
        "video": True,
        "x0_start": 405.0,
        "x0_end": 685.0,
    },
    {
        "row": "S04_coastline",
        "in": 8.500,
        "out": 12.067,
        "kind": "still_rect",
        "source": "PIA21434.jpg",
        "title": "Titan Kraken and Ligeia Seas in Sharper Focus (Cassini VIMS)",
        "credit": "NASA/JPL-Caltech/University of Arizona/University of Idaho/DLR",
        "video": False,
        # Verified mathematically as the largest border-free interior 9:16 crop on PIA21434 (1828x1200):
        # 489x870 interior crop -> border_min=59.0, 0 diagonal border, 0 starfield fill,
        # upscale = 1920/870 * 1.02 = 2.25x <= 2.35x (any ch >= 920 hits black space border=0.0).
        "crop_box": (460, 150, 949, 1020),
        "z1": 1.02,
        "warm_tint": True,
        "unsharp_pct": 135,
    },
    {
        "row": "S05_methane_sea",
        "in": 12.067,
        "out": 14.200,
        "kind": "still_cover",
        "source": "PIA20021_right_panel_1440x1144.jpg",
        "title": "Titan Northern Lakes and Seas (Cassini Radar Right-Panel Crop)",
        "credit": "NASA/JPL-Caltech/ASI/Cornell",
        "video": False,
        "pan_x_frac": 0.50,
        "z1": 1.045,
        "boost_sat": 1.25,
    },
    {
        "row": "S06_icy_crust",
        "in": 14.200,
        "out": 16.767,
        "kind": "svs_pan",
        "source": "SVS20311_Dragonfly_Drill_1080.mp4",
        "title": "Dragonfly Sampling Titan Icy Crust (SVS 20311)",
        "credit": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
        "offset": 7.400,
        "video": True,
        "x0_start": 560.0,
        "x0_end": 720.0,
    },
    {
        "row": "S07_cassini_gravity",
        "in": 16.767,
        "out": 20.400,
        "kind": "still_orb",
        "source": "PIA14922.jpg",
        "title": "Colorful Colossuses: Titan Beside Ringed Saturn (Cassini ISS)",
        "credit": "NASA/JPL-Caltech/Space Science Institute",
        "video": False,
        "orb_scale": 0.90,
        "z1": 1.045,
    },
    {
        "row": "S08_titan_ocean_depth",
        "in": 20.400,
        "out": 24.000,
        "kind": "titan_ocean_depth",
        "source": "code_graphic_032_s2_titan_ocean_depth_9x16_v03.mp4",
        "photo_source": "PIA14602.jpg",
        "title": "Titan Subsurface Ocean Cutaway: Icy Crust & Hidden Ocean of Liquid Water (032 S02 v03)",
        "credit": "Original graphic + NASA/JPL-Caltech/Space Science Institute (PIA14602)",
        "offset": 0.0,
        "video": True,
    },
    {
        "row": "S09_saturn_horizon",
        "in": 24.000,
        "out": 26.267,
        "kind": "svs_pan",
        "source": "SVS20311_DF_End_Pan_1080.mp4",
        "title": "Dragonfly Flight Pan Over Titan Surface Horizon (SVS 20311)",
        "credit": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
        "offset": 10.200,
        "video": True,
        "x0_start": 480.0,
        "x0_end": 640.0,
    },
    {
        "row": "S10_loop",
        "in": 26.267,
        "out": 26.900,
        "kind": "loop_return",
        "source": f"frame0_return_{STEM}.mp4",
        "raw_source": "SVS20311_DF_Open_1080.mp4",
        "title": "Opening frame return for seamless loop",
        "credit": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
        "offset": 0.0,
        "raw_offset": 1.167,
        "video": True,
        "x0_start": 170.0,
        "x0_end": 260.0,
    },
]

BARRED_ASSETS = {"PIA14925", "PIA06230", "PIA09739", "PIA21625"}

BOUNDED_EXTERNAL_SEARCH = {
    "policy": "Chief option A (J3856 REVIEW.md): official NASA/JPL/Cassini external-source search, max 20 active minutes and 3 deep candidates total; no spend, no generation, no E1 waiver.",
    "elapsed_active_minutes": 9,
    "deep_candidates_examined": 2,
    "deep_candidate_cap": 3,
    "catalogs_queried": [
        "NASA JPL Photojournal / science.nasa.gov (PIA17656, PIA17655)",
        "NASA Image and Video Library API (images-api.nasa.gov/search?media_type=video)",
        "NASA Goddard Scientific Visualization Studio API (svs.gsfc.nasa.gov/api/search?keywords=Titan|Cassini)",
    ],
    "candidates": [
        {
            "index": 1,
            "id": "PIA17656",
            "title": "Flying over an Extraterrestrial Land of Lakes (Cassini Radar North Polar Flyover)",
            "source_url": "https://assets.science.nasa.gov/content/dam/science/psd/photojournal/pia/pia17/pia17656/PIA17656_Unannotated-ProRes.mov",
            "credit": "NASA/JPL-Caltech/ASI/USGS",
            "rights": "NASA/JPL Public Domain",
            "native_resolution": "1280x720 (both ProRes master and 1280 H.264 mov)",
            "fps": "29.97 / 30",
            "duration_s": 63.66,
            "upscale_9x16_full_bleed": 2.67,
            "verdict": "REJECTED",
            "reason": "Native height 720 px requires 1920/720 = 2.67x upscale for full-bleed 1080x1920, exceeding the 2.35x picture_qa hard ceiling. (Also confirmed via XMP:Ingredients that SVS 12709's 288.27-296.80s flyover embeds this same 720p PIA17656 file.)",
        },
        {
            "index": 2,
            "id": "GSFC_20170912_Cassini_m12709_CIRS_Short (NASA SVS 12709)",
            "title": "Cassini's Infrared Saturn (Short Version) — Cassini Orbiter Flyby Across Titan",
            "source_url": "https://images-assets.nasa.gov/video/GSFC_20170912_Cassini_m12709_CIRS_Short/GSFC_20170912_Cassini_m12709_CIRS_Short~orig.mp4",
            "svs_page": "https://svs.gsfc.nasa.gov/12709",
            "xmp_ingredient": "Cassini_Saturn_Animation_Reel.mov (259.43s - 263.93s)",
            "credit": "NASA/Goddard Space Flight Center/JPL-Caltech",
            "rights": "U.S. Government / NASA GSFC Public Domain visual asset; original third-party Killer Tracks audio stripped via -an (silent picture only)",
            "native_resolution": "1920x1080",
            "fps": "30/1",
            "source_window_s": [260.000, 263.767],
            "extracted_archival_clip": "harvest_J3865_v01/SVS12709_Cassini_Titan_Flyby_260_264_1080.mp4",
            "extracted_archival_sha256": EXPECTED_S03_SHA256,
            "upscale_9x16_full_bleed": 1.78,
            "fixed_crop_native_motion_diff": {"min": 3.60, "median": 5.84, "max": 6.97, "frames": 113},
            "verdict": "ACCEPTED",
            "reason": "Native 1920x1080 30fps official NASA Cassini animation showing the Cassini spacecraft (high-gain radar dish, booms, golden foil) flying smoothly across Titan's illuminated golden globe for 3.967s (119 clean un-faded, text-free frames >= 113 frames needed for S03). 1.78x upscale <= 2.35x, strong native motion on every frame, zero Dragonfly hardware.",
        },
    ],
    "selected_s03_source": "SVS12709_Cassini_Titan_Flyby_260_264_1080.mp4",
}


def run(cmd: list) -> None:
    sp.run([str(c) for c in cmd], check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2 and w.getnchannels() == 2
        a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
        return a.reshape(-1, 2)


def write_wav(x: np.ndarray, dst: Path) -> None:
    pcm = (np.clip(x, -1.0, 1.0) * 32767.0).astype("<i2")
    z = (pcm[:, 0] == 0) & (pcm[:, 1] == 0)
    if z.any():
        idx = np.arange(z.sum())
        pcm[z, 0] = np.where(idx % 2 == 0, 1, -1)
        pcm[z, 1] = np.where(idx % 2 == 0, -1, 1)
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def silence(n: int) -> np.ndarray:
    return np.zeros((max(0, n), 2), dtype=np.float32)


def lift_navy(arr: np.ndarray) -> np.ndarray:
    mx = arr.max(axis=2, keepdims=True)
    return np.where(mx < 54.0, np.maximum(arr, NAVY_FLOOR), arr)


def soft_lift_navy(arr: np.ndarray) -> np.ndarray:
    """Smooth C-infinity navy floor lift: avoids hard contour steps on Titan's atmospheric limb."""
    return NAVY_FLOOR + arr * (1.0 - NAVY_FLOOR / 255.0)


_STAR_BG: np.ndarray | None = None


def get_clean_starfield() -> np.ndarray:
    global _STAR_BG
    if _STAR_BG is None:
        raw = Image.open(NAS_HARV / "weic2310a.png").convert("RGB")
        corner = raw.crop((0, 0, 360, 640)).resize((W, H), Image.Resampling.LANCZOS)
        st = np.asarray(corner, dtype=np.float32)
        st_norm = np.clip((st - 4.0) / 22.0, 0.0, 1.0)
        rgb = np.stack(
            [
                29.0 + 38.0 * st_norm[:, :, 0],
                40.0 + 42.0 * st_norm[:, :, 1],
                62.0 + 48.0 * st_norm[:, :, 2],
            ],
            axis=-1,
        )
        rng = np.random.default_rng(3202)
        for _ in range(1800):
            sy = int(rng.integers(4, H - 6))
            sx = int(rng.integers(4, W - 6))
            b = float(rng.uniform(75.0, 175.0))
            sz = 2 if rng.random() < 0.78 else 3
            rgb[sy : sy + sz, sx : sx + sz, 0] = np.maximum(rgb[sy : sy + sz, sx : sx + sz, 0], b * 0.90)
            rgb[sy : sy + sz, sx : sx + sz, 1] = np.maximum(rgb[sy : sy + sz, sx : sx + sz, 1], b * 0.96)
            rgb[sy : sy + sz, sx : sx + sz, 2] = np.maximum(rgb[sy : sy + sz, sx : sx + sz, 2], b * 1.05)
        _STAR_BG = np.clip(lift_navy(rgb), 28.0, 255.0)
    return _STAR_BG


def resolve_asset_path(name: str) -> Path:
    for base in (NAS_HARV_J3865, NAS_HARV, NAS_SVS):
        p = base / name
        if p.exists():
            return p
    raise FileNotFoundError(f"Missing asset on NAS: {name}")


def build_base_9x16_rect(shot: dict) -> tuple[Image.Image, float]:
    """Full-bleed 9:16 from an explicit clean interior crop box (zero diagonal borders)."""
    src = resolve_asset_path(shot["source"])
    im = Image.open(src).convert("RGB")
    if shot.get("warm_tint"):
        a = np.asarray(im, dtype=np.float32)
        g = a.mean(axis=2)
        a = np.stack([g * 1.08 + 18.0, g * 0.88 + 12.0, g * 0.66 + 16.0], axis=-1)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if shot.get("boost_sat"):
        im = ImageEnhance.Color(im).enhance(float(shot["boost_sat"]))
        im = ImageEnhance.Contrast(im).enhance(1.07)
    x0, y0, x1, y1 = shot["crop_box"]
    cw, ch = float(x1 - x0), float(y1 - y0)
    crop = im.transform(
        (W, H), Image.Transform.EXTENT, (float(x0), float(y0), float(x1), float(y1)), resample=Image.Resampling.BICUBIC
    )
    unsharp_pct = int(shot.get("unsharp_pct", 120))
    crop = crop.filter(ImageFilter.UnsharpMask(radius=1.5, percent=unsharp_pct, threshold=2))
    arr = lift_navy(np.asarray(crop, dtype=np.float32))
    z1 = float(shot.get("z1", 1.045))
    up = round((H / ch) * z1, 2)
    return Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8)), up


def build_base_9x16_cover(shot: dict) -> tuple[Image.Image, float]:
    src = resolve_asset_path(shot["source"])
    im = Image.open(src).convert("RGB")
    if shot.get("boost_sat"):
        im = ImageEnhance.Color(im).enhance(float(shot["boost_sat"]))
        im = ImageEnhance.Contrast(im).enhance(1.07)

    sw, sh = im.size
    if sw / sh >= W / H:
        ch = float(sh)
        cw = ch * (W / H)
    else:
        cw = float(sw)
        ch = cw * (H / W)
    px_frac = float(shot.get("pan_x_frac", 0.5))
    x0 = max(0.0, min(sw - cw, (sw - cw) * px_frac))
    y0 = (sh - ch) * 0.5
    crop = im.transform(
        (W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), resample=Image.Resampling.BICUBIC
    )
    crop = crop.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=2))
    arr = lift_navy(np.asarray(crop, dtype=np.float32))
    z1 = float(shot.get("z1", 1.045))
    up = round((H / ch) * z1, 2)
    return Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8)), up


def build_base_9x16_orb(shot: dict) -> tuple[Image.Image, float]:
    src = resolve_asset_path(shot["source"])
    im = Image.open(src).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.22)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    sw, sh = im.size
    orb_scale = float(shot.get("orb_scale", 0.88))
    target_w = round(W * orb_scale)
    scale = target_w / float(sw)
    nw, nh = round(sw * scale), round(sh * scale)
    fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
    fg_arr = np.asarray(fg, dtype=np.float32)

    bg_arr = get_clean_starfield().copy()
    yy, xx = np.mgrid[0:nh, 0:nw].astype(np.float32)
    rx = (xx - nw * 0.5) / max(1.0, nw * 0.47)
    ry = (yy - nh * 0.5) / max(1.0, nh * 0.47)
    r = np.sqrt(rx * rx + ry * ry)
    radial = np.clip((1.00 - r) / 0.24, 0.0, 1.0)
    radial = 0.5 - 0.5 * np.cos(np.pi * radial)

    luma_max = fg_arr.max(axis=2)
    space_key = np.clip((luma_max - 16.0) / 34.0, 0.0, 1.0)
    core = np.clip((0.68 - r) / 0.20, 0.0, 1.0)
    alpha = radial * np.maximum(core, space_key)

    x0 = (W - nw) // 2
    y0 = (H - nh) // 2
    patch = bg_arr[y0 : y0 + nh, x0 : x0 + nw]
    patch[:] = patch * (1.0 - alpha[:, :, None]) + lift_navy(fg_arr) * alpha[:, :, None]

    z1 = float(shot.get("z1", 1.045))
    up = round(scale * z1, 2)
    return Image.fromarray(np.clip(lift_navy(bg_arr), 28, 255).astype(np.uint8)), up


def pipe_frames(frames: list[Image.Image], dest: Path) -> None:
    proc = sp.Popen(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15",
            "-pix_fmt", "yuv420p", "-video_track_timescale", "30000", str(dest),
        ],
        stdin=sp.PIPE,
    )
    assert proc.stdin is not None
    for im in frames:
        proc.stdin.write(im.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"Failed encoding {dest}")


def render_symmetric_still_zoom(base: Image.Image, frames_n: int, z1: float, dest: Path) -> None:
    denom = float(max(1, frames_n - 1))
    frames = []
    for i in range(frames_n):
        z = 1.0 + (z1 - 1.0) * (i / denom)
        cw, ch = W / z, H / z
        l, top = (W - cw) * 0.5, (H - ch) * 0.5
        fr = base.transform((W, H), Image.Transform.EXTENT, (l, top, l + cw, top + ch), resample=Image.Resampling.BICUBIC)
        frames.append(fr)
    pipe_frames(frames, dest)


def load_raw_video_frames(src: Path, offset: float, frames_n: int, sw: int = 1920, sh: int = 1080) -> list[Image.Image]:
    dur_need = (frames_n / FPS) + 0.5
    vf = f"fps={FPS},scale={sw}:{sh}:flags=lanczos"
    raw = sp.check_output(
        [
            "ffmpeg", "-v", "error", "-ss", f"{offset:.3f}", "-t", f"{dur_need:.3f}",
            "-i", str(src), "-vf", vf, "-frames:v", str(frames_n),
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ]
    )
    fb = sw * sh * 3
    out = []
    for i in range(frames_n):
        chunk = raw[i * fb : (i + 1) * fb]
        if len(chunk) < fb:
            chunk = raw[-fb:]
        out.append(Image.frombytes("RGB", (sw, sh), chunk))
    return out


def make_titan_disc_rgba(path: Path, crop_box: tuple[int, int, int, int], diameter: int) -> Image.Image:
    """Real Cassini ISS Titan globe (PIA14602, exact approved crop from ocean_graphic.py)."""
    im = Image.open(path).convert("RGB").crop(crop_box)
    im = ImageEnhance.Color(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = im.resize((diameter, diameter), Image.Resampling.LANCZOS)
    circle = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(circle).ellipse((3, 3, diameter - 4, diameter - 4), fill=255)
    circle = circle.filter(ImageFilter.GaussianBlur(1.5))
    out = im.convert("RGBA")
    out.putalpha(circle)
    ImageDraw.Draw(out).ellipse(
        (3, 3, diameter - 4, diameter - 4), outline=(255, 214, 110, 195), width=max(2, diameter // 80)
    )
    return out


def font_for(line_h: float, ratio: float = 0.86, font_path: str = FONT_BLACK) -> ImageFont.FreeTypeFont:
    size = 10
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f = ImageFont.truetype(font_path, size + 1)
        b = probe.textbbox((0, 0), "Hg", font=f)
        if b[3] - b[1] > line_h * ratio:
            return ImageFont.truetype(font_path, size)
        size += 1


def centred(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple,
    stroke: int = 6,
) -> list[int]:
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    alpha = fill[3] if len(fill) == 4 else 255
    stroke_fill = (16, 26, 46, alpha)
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


def centred_in_box(
    draw: ImageDraw.ImageDraw,
    x0: int,
    x1: int,
    y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple,
    stroke: int = 6,
) -> list[int]:
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = x0 + ((x1 - x0) - (b[2] - b[0])) // 2 - b[0]
    alpha = fill[3] if len(fill) == 4 else 255
    stroke_fill = (14, 24, 42, alpha)
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


def render_titan_ocean_depth(
    frames_n: int,
    shot_in: float,
    dest: Path,
    second_s: float,
    hidden_s: float,
    liquid_s: float,
) -> tuple[float, dict]:
    """Simplified single Titan-specific Teach-on-Screen graphic (S08, 20.400-24.000 s).

    Fixes every S08 item in J3856 REVIEW.md:
      - Zero unspoken text: removes 55-80 KM BELOW completely.
      - Uses ONLY exact locked spoken words from S52, timed strictly from words.json:
          * 20.400-21.000 s: real Cassini ISS Titan (PIA14602) + TITAN + ICY CRUST (zero ocean spoiler)
          * second_s (21.000 s, "second", 78.1% >= 70%): open-bottomed cyan subsurface ocean sweeps in
          * hidden_s (21.520 s, "hidden"): HIDDEN OCEAN reveals on one bold 68 px line
          * liquid_s (22.960 s, "liquid"): LIQUID WATER reveals on one bold 68 px line
      - Every main teaching label uses 68 px Arial Black (11.18% of 608 px 16:9 safe band,
        inside the 11-12% / 67-73 px house Short teaching-label rule).
      - Subordinate qualitative disclaimer NOT TO SCALE (26 px), no ocean floor / no invented proportions.
      - Strictly inside 16:9 safe band y = 656..1264, single overlay, retains Titan.
    """
    # Exact approved PIA14602 disc crop from 032/07_Edit-Project/ocean_graphic.py
    titan_disc = make_titan_disc_rgba(resolve_asset_path("PIA14602.jpg"), (265, 275, 775, 785), 296)
    f_teach = ImageFont.truetype(FONT_BLACK, TEACH_FONT_PX)   # 68 px = 11.18% of 608 px safe band
    f_note = ImageFont.truetype(FONT_BOLD, 26)
    bg_base = Image.fromarray(get_clean_starfield().astype(np.uint8)).convert("RGBA")

    # Simplified, spacious layout strictly inside 16:9 safe band y = 656..1264:
    #   Left: real Cassini Titan globe (x = 42..338, y = 718..1014) + TITAN (68 px, y = 1040..1106)
    #   Right: gently arched planetary cutaway (x = 398..1034, width = 636 px) so 68 px labels fit
    #          on single crisp lines while the curved top surface avoids a flat letterbox seam.
    titan_x, titan_y, titan_d = 42, 718, 296
    col_x0, col_x1 = 398, 1034
    crust_y0, boundary_y = 700, 836
    ocean_y1 = 1178
    arch_lift = 24  # subtle planetary curvature at centre of cutaway top (highest y = 676 >= 656)

    def crust_top_y(x: int) -> int:
        u_x = (x - (col_x0 + col_x1) * 0.5) / max(1.0, (col_x1 - col_x0) * 0.5)
        return round(crust_y0 - arch_lift * (1.0 - u_x * u_x))

    # Precompute open-bottom ocean gradient column (no floor line, fades softly over bottom 84 px)
    ocean_w = col_x1 - col_x0
    ocean_h = ocean_y1 - boundary_y
    ocean_rgba = np.zeros((ocean_h, ocean_w, 4), dtype=np.uint8)
    ocean_rgba[:, :, 0] = 32
    ocean_rgba[:, :, 1] = 146
    ocean_rgba[:, :, 2] = 212
    fade_rows = 88
    alpha_col = np.full(ocean_h, 218.0, dtype=np.float32)
    alpha_col[-fade_rows:] = np.linspace(218.0, 12.0, fade_rows)
    ocean_rgba[:, :, 3] = alpha_col[:, None].astype(np.uint8)
    ocean_grad_im = Image.fromarray(ocean_rgba, mode="RGBA")

    frames = []
    denom = float(max(1, frames_n - 1))
    second_loc = second_s - shot_in      # 0.600 s ("second")
    hidden_loc = hidden_s - shot_in      # 1.120 s ("hidden")
    liquid_loc = liquid_s - shot_in      # 2.560 s ("liquid")

    label_bboxes: dict[str, list[int]] = {}
    top_curve_pts = [(x, crust_top_y(x)) for x in range(col_x0, col_x1 + 1, 6)]
    if top_curve_pts[-1][0] != col_x1:
        top_curve_pts.append((col_x1, crust_top_y(col_x1)))
    crust_poly = top_curve_pts + [(col_x1, boundary_y), (col_x0, boundary_y)]

    for i in range(frames_n):
        t_loc = i / FPS
        u = i / denom

        # Subtle smooth starfield push (zero integer jitter)
        z = 1.0 + 0.028 * u
        cw, ch = W / z, H / z
        l, top = (W - cw) * 0.5, (H - ch) * 0.5
        fg = bg_base.transform((W, H), Image.Transform.EXTENT, (l, top, l + cw, top + ch), resample=Image.Resampling.BICUBIC)

        entry_a = min(1.0, t_loc / 0.18)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.alpha_composite(titan_disc, (titan_x, titan_y))
        d = ImageDraw.Draw(layer)

        # TITAN label (68 px yellow) directly under real Cassini Titan globe
        bb_titan = centred_in_box(d, titan_x, titan_x + titan_d, 1040, "TITAN", f_teach, YELLOW, stroke=6)

        # Ocean reveal progress: STRICTLY starts at second_s (21.000 s, exact word start of "second")
        p_ocean = 0.0
        if t_loc >= second_loc:
            p_ocean = max(0.0, min(1.0, (t_loc - second_loc) / 0.65))
            p_ocean = 0.5 - 0.5 * math.cos(math.pi * p_ocean)

        # Qualitative zoom connector lines from Titan's limb to local cross-section
        # (lower connector hugs crust bottom until 21.000 s so there is zero early ocean cue)
        lower_conn_y = round(boundary_y + (ocean_y1 - 16 - boundary_y) * p_ocean)
        d.line((titan_x + titan_d - 12, 804, col_x0 - 10, crust_y0), fill=(255, 207, 64, 195), width=4)
        d.line((titan_x + titan_d - 12, 932, col_x0 - 10, lower_conn_y), fill=(255, 207, 64, 195), width=4)

        # Upper icy crust slab with subtle curved planetary top (exact locked spoken words "icy crust" from S52)
        d.polygon(crust_poly, fill=(172, 210, 228, 214))
        d.line(top_curve_pts, fill=WHITE, width=5)
        d.line((col_x0, crust_y0, col_x0, boundary_y), fill=(220, 240, 250, 185), width=3)
        d.line((col_x1, crust_y0, col_x1, boundary_y), fill=(220, 240, 250, 185), width=3)
        bb_crust = centred_in_box(d, col_x0, col_x1, 728, "ICY CRUST", f_teach, WHITE, stroke=6)

        # Subsurface ocean layer sweeps in at 21.000 s ("second")
        if t_loc >= second_loc:
            fill_w = max(1, round(ocean_w * p_ocean))
            layer.alpha_composite(ocean_grad_im.crop((0, 0, fill_w, ocean_h)), (col_x0, boundary_y))
            d = ImageDraw.Draw(layer)
            pts = [
                (col_x0 + dx, boundary_y + round(3.0 * math.sin(dx / 34.0 + t_loc * 3.2)))
                for dx in range(0, fill_w, 4)
            ]
            if len(pts) > 1:
                d.line(pts, fill=(208, 244, 255, 245), width=4)

        # HIDDEN OCEAN (68 px yellow): reveals at exact words.json onset of "hidden" (21.520 s)
        bb_hidden = None
        if t_loc >= hidden_loc:
            ho_a = int(round(255 * max(0.0, min(1.0, (t_loc - hidden_loc) / 0.25))))
            if ho_a > 5:
                bb_hidden = centred_in_box(d, col_x0, col_x1, 876, "HIDDEN OCEAN", f_teach, (255, 224, 0, ho_a), stroke=6)

        # LIQUID WATER (68 px white): reveals at exact words.json onset of "liquid" (22.960 s)
        bb_liquid = None
        if t_loc >= liquid_loc:
            lw_a = int(round(255 * max(0.0, min(1.0, (t_loc - liquid_loc) / 0.25))))
            if lw_a > 5:
                bb_liquid = centred_in_box(d, col_x0, col_x1, 992, "LIQUID WATER", f_teach, (255, 255, 255, lw_a), stroke=6)

        # Subordinate qualitative scale disclaimer (strictly inside safe band y = 656..1264)
        bb_note = centred(d, 1212, "NOT TO SCALE", f_note, (208, 224, 242, 220), stroke=3)

        if i == frames_n - 1:
            label_bboxes = {
                "TITAN": bb_titan,
                "ICY CRUST": bb_crust,
                "HIDDEN OCEAN": bb_hidden or [],
                "LIQUID WATER": bb_liquid or [],
                "NOT TO SCALE": bb_note,
            }
            for lbl, bb in label_bboxes.items():
                if bb and (bb[1] < BAND_Y0 or bb[3] > BAND_Y1):
                    raise SystemExit(f"S08 label {lbl!r} outside 16:9 safe band [{BAND_Y0}, {BAND_Y1}]: {bb}")

        if entry_a < 0.999:
            a_ch = layer.getchannel("A").point(lambda v: int(round(v * entry_a)))
            layer.putalpha(a_ch)
        fg.alpha_composite(layer)
        frames.append(fg.convert("RGB"))

    pipe_frames(frames, dest)
    info = {
        "row": "S08_titan_ocean_depth",
        "source": dest.name,
        "titan_photo": "PIA14602.jpg",
        "earth_proxy_used": False,
        "extra_pill_used": False,
        "unspoken_text_removed": True,
        "start_s": shot_in,
        "end_s": round(shot_in + frames_n / FPS, 3),
        "ocean_sweep_start_s": second_s,
        "hidden_ocean_reveal_s": hidden_s,
        "liquid_water_reveal_s": liquid_s,
        "teaching_font_px": TEACH_FONT_PX,
        "teaching_font_pct_of_608_safe_band": round(TEACH_FONT_PX / BAND_H * 100.0, 2),
        "subordinate_note_font_px": 26,
        "labels": ["TITAN", "ICY CRUST", "HIDDEN OCEAN", "LIQUID WATER", "NOT TO SCALE"],
        "label_bboxes": label_bboxes,
        "safe_band_y": [BAND_Y0, BAND_Y1],
    }
    return 1.00, info


def render_shot(
    shot: dict,
    dest: Path,
    open_f0: Path | None = None,
    s08_timings: tuple[float, float, float] | None = None,
) -> tuple[float, dict | None]:
    frames_n = round((shot["out"] - shot["in"]) * FPS)
    kind = shot["kind"]

    if kind in ("svs_pan", "svs_pan_soft", "loop_return"):
        src_name = shot["raw_source"] if kind == "loop_return" else shot["source"]
        src_off = float(shot["raw_offset"] if kind == "loop_return" else shot["offset"])
        src = resolve_asset_path(src_name)
        raw = load_raw_video_frames(src, offset=src_off, frames_n=frames_n, sw=1920, sh=1080)
        cw = 1080.0 * (W / H)  # 607.5 px -> upscale 1920/1080 = 1.78x
        x0_s = float(shot["x0_start"])
        x0_e = float(shot["x0_end"])
        denom = float(max(1, frames_n - 1))
        use_soft = (kind == "svs_pan_soft")
        frames = []
        for i, im in enumerate(raw):
            u = i / denom
            x0 = x0_s + (x0_e - x0_s) * u
            x0 = max(0.0, min(1920.0 - cw, x0))
            crop = im.transform((W, H), Image.Transform.EXTENT, (x0, 0.0, x0 + cw, 1080.0), resample=Image.Resampling.BICUBIC)
            if use_soft:
                crop = ImageEnhance.Color(crop).enhance(1.18)
                crop = ImageEnhance.Contrast(crop).enhance(1.08)
                crop = crop.filter(ImageFilter.UnsharpMask(radius=1.4, percent=115, threshold=2))
                arr = soft_lift_navy(np.asarray(crop, dtype=np.float32))
            else:
                crop = ImageEnhance.Color(crop).enhance(1.30)
                crop = ImageEnhance.Contrast(crop).enhance(1.10)
                crop = crop.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=2))
                arr = lift_navy(np.asarray(crop, dtype=np.float32))
            fr = Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8))
            if open_f0 is not None and i == 0:
                fr.save(open_f0)
            frames.append(fr)
        pipe_frames(frames, dest)
        if kind == "loop_return":
            shutil.copy2(dest, WORK / "exports" / shot["source"])
        return 1.78, None

    if kind == "still_rect":
        base, up = build_base_9x16_rect(shot)
        render_symmetric_still_zoom(base, frames_n, float(shot["z1"]), dest)
        return up, None

    if kind == "still_cover":
        base, up = build_base_9x16_cover(shot)
        render_symmetric_still_zoom(base, frames_n, float(shot["z1"]), dest)
        return up, None

    if kind == "still_orb":
        base, up = build_base_9x16_orb(shot)
        render_symmetric_still_zoom(base, frames_n, float(shot["z1"]), dest)
        return up, None

    if kind == "titan_ocean_depth":
        assert s08_timings is not None
        up, info = render_titan_ocean_depth(frames_n, float(shot["in"]), dest, *s08_timings)
        info["source"] = shot["source"]
        return up, info

    raise ValueError(f"Unknown shot kind: {kind}")


def build_voice_plan() -> tuple[list[dict], list[dict], float]:
    stt = json.loads(STT_JSON.read_text())
    raw_words = [w for w in stt["words"] if w.get("text", "").strip()]
    slices = []
    words = []
    local = VO_LEAD_S
    for si, (a, b) in enumerate(VO_SEGMENTS):
        dur_s = round(b - a, 3)
        slices.append({"a": a, "b": b, "local": round(local, 3)})
        for w in raw_words:
            if w["end"] <= a + 0.005 or w["start"] >= b - 0.005:
                continue
            s = round(w["start"] - a + local, 3)
            e = round(min(b, w["end"]) - a + local, 3)
            txt = w["text"].strip()
            words.append({"text": txt, "w": txt, "s": s, "e": e, "start": s, "end": e})
        local = round(local + dur_s, 3)
        if si < len(VO_GAPS):
            local = round(local + VO_GAPS[si], 3)
    return slices, words, words[-1]["e"]


def make_hook(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(H * 0.082 / 0.72)
    if f.size > 130:
        f = ImageFont.truetype(FONT_BLACK, 130)
    while max(d.textlength(t, font=f) for t, _ in HOOK_ROWS) > W * 0.84:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = 240
    boxes = []
    for t, c in HOOK_ROWS:
        boxes.append(centred(d, y, t, f, c, stroke=7))
        y += lh
    im.save(dest)
    return {"text": " / ".join(t for t, _ in HOOK_ROWS), "font_px": f.size, "bboxes": boxes}


def make_title(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.88)
    while max(d.textlength(r, font=f) for r in TITLE_ROWS) > W * 0.88:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 14
    y = BAND_Y0 + (BAND_H - gap * len(TITLE_ROWS)) // 2
    placed = []
    for r in TITLE_ROWS:
        bb = centred(d, y, r, f, WHITE, stroke=6)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"title outside 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed, "joined": LONG_TITLE}


def make_caption(dest: Path, text: str) -> list[int]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.90)
    shown = text.upper()
    while d.textlength(shown, font=f) > W * 0.88:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y1 + 42, shown, f, WHITE, stroke=6)
    im.save(dest)
    return bb


def caption_chunks(words: list[dict], vo_end: float) -> list[dict]:
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[,.?!]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else vo_end
        end = min(nxt, c[-1]["e"] + 0.35, vo_end)
        text = " ".join(x["w"] for x in c).rstrip(",.")
        if end <= TITLE_IN or start >= TITLE_OUT:
            if TITLE_IN < start < TITLE_OUT:
                continue
            if start < TITLE_OUT < end:
                start = TITLE_OUT
            if end - start >= 0.18 and start < vo_end:
                out.append({"text": text, "s": round(start, 2), "e": round(min(end, vo_end), 2)})
        else:
            if start < TITLE_IN - 0.05 and TITLE_IN - start >= 0.18:
                out.append({"text": text, "s": round(start, 2), "e": round(min(end, TITLE_IN), 2)})
            if end > TITLE_OUT + 0.05:
                out.append({"text": text, "s": round(max(start, TITLE_OUT), 2), "e": round(min(end, vo_end), 2)})
    return [c for c in out if c["e"] - c["s"] >= 0.18]


def srt_chunks_full(words: list[dict], vo_end: float) -> list[dict]:
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[,.?!]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else vo_end
        end = min(nxt, c[-1]["e"] + 0.35, vo_end)
        text = " ".join(x["w"] for x in c)
        if end - start >= 0.12:
            out.append({"text": text, "s": round(start, 3), "e": round(min(end, vo_end), 3)})
    return out


def write_srt(caps: list[dict], dst: Path) -> None:
    def fmt(t: float) -> str:
        ms = int(round(t * 1000))
        hh, rem = divmod(ms, 3600_000)
        mm, rem = divmod(rem, 60_000)
        ss, mmm = divmod(rem, 1000)
        return f"{hh:02d}:{mm:02d}:{ss:02d},{mmm:03d}"

    lines = []
    for idx, c in enumerate(caps, 1):
        lines.append(f"{idx}\n{fmt(c['s'])} --> {fmt(c['e'])}\n{c['text']}\n")
    dst.write_text("\n".join(lines))


def make_cover(dest: Path, f0_png: Path) -> dict:
    im = Image.open(f0_png).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.22)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    d = ImageDraw.Draw(im)
    size = 72
    while size < 126:
        trial = ImageFont.truetype(FONT_BLACK, size + 2)
        if max(d.textlength(r, font=trial) for r, _ in COVER_ROWS) > W * 0.80:
            break
        size += 2
    f = ImageFont.truetype(FONT_BLACK, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = BAND_Y0 + (BAND_H - lh * len(COVER_ROWS)) // 2
    boxes = []
    for r, col in COVER_ROWS:
        bb = centred(d, y, r, f, col, stroke=8)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"cover text outside 16:9 band: {r} {bb}")
        boxes.append(bb)
        y += lh
    im.save(dest, quality=94, subsampling=0)
    return {"file": str(dest), "rows": [r for r, _ in COVER_ROWS], "font_px": size, "bboxes": boxes}


def make_phone_graphic_preview(dest: Path, stills: list[tuple[str, Path]]) -> None:
    """Phone-scale legibility sheet for S08 (top row: 360x640 standard phone; bottom: 240x427 compact phone)."""
    pad = 24
    hdr_h = 44
    w_big, h_big = 360, 640
    w_sm, h_sm = 240, 427
    n = len(stills)
    canvas_w = pad + n * (w_big + pad)
    canvas_h = pad + hdr_h + h_big + pad + hdr_h + h_sm + pad
    sheet = Image.new("RGB", (canvas_w, canvas_h), (18, 22, 32))
    d = ImageDraw.Draw(sheet)
    f_hdr = ImageFont.truetype(FONT_BOLD, 20)
    f_sub = ImageFont.truetype(FONT_BOLD, 16)

    for idx, (label, path) in enumerate(stills):
        im = Image.open(path).convert("RGB")
        # Row 1: 360x640 (typical 1x logical phone viewport)
        x1 = pad + idx * (w_big + pad)
        y1 = pad + hdr_h
        d.text((x1, pad + 10), f"{label} (360x640 phone)", font=f_hdr, fill=(255, 224, 0))
        sheet.paste(im.resize((w_big, h_big), Image.Resampling.LANCZOS), (x1, y1))

        # Row 2: 240x427 (compact mobile feed / thumbnail-scale check)
        x2 = x1 + (w_big - w_sm) // 2
        y2 = y1 + h_big + pad + hdr_h
        d.text((x2, y2 - 28), f"240x427 compact", font=f_sub, fill=(208, 224, 242))
        sheet.paste(im.resize((w_sm, h_sm), Image.Resampling.LANCZOS), (x2, y2))

    sheet.save(dest, quality=94, subsampling=0)


def build_audio(work: Path, slices: list[dict], total: float, second_s: float, hidden_s: float, liquid_s: float) -> dict:
    parts = []
    cursor = 0.0
    for i, sl in enumerate(slices):
        gap_n = int(round((sl["local"] - cursor) * SR))
        if gap_n > 0:
            parts.append(silence(gap_n))
        seg = sl["b"] - sl["a"]
        p = work / f"vo_{i}.wav"
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(VO_WAV),
            "-ss", f"{sl['a']:.3f}", "-t", f"{seg:.3f}",
            "-ar", str(SR), "-ac", "2", str(p),
        ])
        parts.append(read_wav(p))
        cursor = sl["local"] + seg
    vo = np.concatenate(parts, axis=0)
    n = int(round(total * SR))
    if len(vo) < n:
        vo = np.concatenate([vo, silence(n - len(vo))], axis=0)
    vo = vo[:n]
    raw = work / "stem_vo_raw.wav"
    write_wav(vo, raw)
    vo_wav = work / "stem_vo.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(raw),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(vo_wav),
    ])
    vo_norm = read_wav(vo_wav)[:n]
    if len(vo_norm) < n:
        vo_norm = np.pad(vo_norm, ((0, n - len(vo_norm)), (0, 0)))
    write_wav(vo_norm, vo_wav)
    vo_m, vo_i = sfx_kit.ebur128(vo_wav)
    vo_m_arr = np.array(vo_m)
    speaking = (vo_m_arr > sfx_kit.SILENT) & (vo_m_arr >= vo_i - sfx_kit.SPEAKING_WITHIN)

    bed_raw = work / "stem_bed_raw.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", "90.0", "-t", f"{total:.3f}",
        "-i", str(BED_MP3),
        "-af", f"afade=t=in:d=0.10,afade=t=out:st={total - 0.30:.3f}:d=0.30",
        "-ar", str(SR), "-ac", "2", str(bed_raw),
    ])
    bed = read_wav(bed_raw)[:n]
    if len(bed) < n:
        bed = np.pad(bed, ((0, n - len(bed)), (0, 0)))
    _, bi0 = sfx_kit.ebur128(bed_raw)
    bed *= 10 ** (((vo_i - 16.0) - bi0) / 20)
    bed_wav = work / "stem_bed.wav"
    write_wav(bed, bed_wav)
    T = np.arange(n) / SR
    grid = np.arange(len(vo_m)) * 0.1
    duck = np.zeros_like(grid)
    k = int(0.35 * SR)
    for _ in range(8):
        bm, _bi = sfx_kit.ebur128(bed_wav)
        m = min(len(vo_m), len(bm))
        bm_arr = np.array(bm[:m])
        delta = vo_m_arr[:m] - bm_arr
        short = np.where(speaking[:m], np.clip(12.5 - delta, 0, None), 0)
        pause = np.where(~speaking[:m], np.clip(bm_arr - (vo_i - 12.5), 0, None), 0)
        need = np.maximum(short, pause)
        if not (delta[speaking[:m]] < 10.5).any() and not (bm_arr[~speaking[:m]] > vo_i - 11).any():
            break
        held = np.array([need[max(0, i - 3) : min(m, i + 4)].max() for i in range(m)])
        duck[:m] = np.minimum(duck[:m] + held, 18)
        env = np.convolve(np.interp(T, grid, duck, left=0, right=0), np.ones(k) / k, mode="same")
        write_wav(bed * (10 ** (-env / 20))[:, None], bed_wav)

    # Restrained house SFX aligned to v03 picture & locked word payoff beats (>= 0.5 s tick spacing):
    hits = [
        ("whoosh", 0.00, -6.0),
        ("rumble", 1.90, -10.5),
        ("tick", TITLE_IN, -8.0),
        ("rumble", 14.20, -10.5),
        ("tick", 20.40, -8.5),
        ("tick", second_s, -8.0),
        ("tick", hidden_s, -8.5),
        ("tick", liquid_s, -9.0),
    ]
    sfx = np.zeros((n, 2), dtype=np.float32)
    kit = {
        "whoosh": KIT_DIR / "sfx_owb_whoosh_soft_v01.wav",
        "tick": KIT_DIR / "sfx_owb_tick_ui_v01.wav",
        "rumble": KIT_DIR / "sfx_owb_rumble_low_v01.wav",
    }
    for kind, at, gain in hits:
        sample = read_wav(kit[kind]) * (10 ** (gain / 20))
        i0 = int(round(at * SR))
        i1 = min(n, i0 + len(sample))
        if i1 > i0:
            sfx[i0:i1] += sample[: i1 - i0]
    sfx_wav = work / "stem_sfx.wav"
    write_wav(sfx, sfx_wav)
    _sm, si = sfx_kit.ebur128(sfx_wav)
    if si > vo_i - 22:
        sfx *= 10 ** ((vo_i - 22 - si) / 20)
        write_wav(sfx, sfx_wav)
    for _ in range(6):
        sm, _si = sfx_kit.ebur128(sfx_wav)
        m = min(len(vo_m), len(sm))
        sm_arr = np.array(sm[:m])
        over = np.where(~speaking[:m], sm_arr - (vo_i - 8), 0)
        under = np.where(speaking[:m], 12.5 - (vo_m_arr[:m] - sm_arr), 0)
        worst = max(float(over.max()), float(under.max()))
        if worst <= 0:
            break
        sfx *= 10 ** (-(worst + 1) / 20)
        write_wav(sfx, sfx_wav)

    mix_raw = work / "mix_raw.wav"
    write_wav(read_wav(vo_wav)[:n] + read_wav(bed_wav)[:n] + sfx[:n], mix_raw)
    mix = work / "mix.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(mix_raw),
        "-af", "loudnorm=I=-14:TP=-2.2:LRA=11",
        "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(mix),
    ])
    _, mix_i = sfx_kit.ebur128(mix)
    _, bed_i = sfx_kit.ebur128(bed_wav)
    _, sfx_i = sfx_kit.ebur128(sfx_wav)
    return {
        "vo_lufs": round(vo_i, 2),
        "bed_lufs": round(bed_i, 2),
        "sfx_lufs": round(sfx_i, 2),
        "mix_lufs": round(mix_i, 2),
    }


def calibrate_aac_wav(work: Path, src_wav: Path, total: float) -> tuple[Path, float, float]:
    gain_db = 0.0
    limit_db = -2.25
    cal_wav = work / "mix_cal.wav"
    test_m4a = work / "mix_cal_test.m4a"
    i_lufs, tp = -14.0, -2.0
    for it in range(6):
        af = (
            f"aresample=192000,volume={gain_db:.3f}dB,"
            f"alimiter=limit={limit_db:.2f}dB:level=disabled:attack=5:release=50,"
            "aresample=48000"
        )
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src_wav), "-af", af, "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(cal_wav)])
        run(["ffmpeg", "-y", "-v", "error", "-i", str(cal_wav), "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(test_m4a)])
        m_i, m_tp = gso.aac_loudness(test_m4a)
        if m_i is not None and m_tp is not None:
            i_lufs, tp = m_i, m_tp
        print(f"  aac cal iter {it}: gain={gain_db:+.2f}dB limit={limit_db:.2f}dB -> I={i_lufs:.2f} LUFS, TP={tp:.2f} dBTP", flush=True)
        if -14.15 <= i_lufs <= -13.85 and tp <= -1.85:
            break
        gain_db += (-14.0 - i_lufs)
        if tp > -1.85:
            limit_db -= max(0.15, tp - (-2.0))
    return cal_wav, round(i_lufs, 2), round(tp, 2)


def copy_verified(src: Path, dst: Path) -> None:
    if dst.exists():
        raise SystemExit(f"Refusing to overwrite existing NAS file: {dst}")
    shutil.copy2(src, dst)
    if sha256(src) != sha256(dst):
        raise SystemExit(f"SHA-256 mismatch copying {src} -> {dst}")


def collect_canonical_owb_mp3_beds() -> list[Path]:
    """Readable canonical OWB MP3 beds across NAS studio-live (excluding 032's own bed & AppleDouble)."""
    root = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects")
    beds = []
    for p in sorted(root.glob("*/05_Music/*.mp3")):
        if not p.is_file() or p.name.startswith("._"):
            continue
        if p.resolve() == BED_MP3.resolve():
            continue
        if "vo" in p.stem.lower() or "listen" in p.stem.lower():
            continue
        beds.append(p)
    return beds


def main() -> None:
    if "--no-nas" not in sys.argv:
        if (NAS_SUB_OUT / f"{STEM}.mp4").exists() or (NAS_SHORTS / f"{STEM}.mp4").exists():
            raise SystemExit(f"Target {STEM}.mp4 already exists on NAS; bump version.")

    for shot in SHOT_PLAN:
        stem_id = Path(shot["source"]).stem
        if stem_id in BARRED_ASSETS:
            raise SystemExit(f"Barred RLSJm59OSzI asset in SHOT_PLAN: {stem_id}")

    vo_sha = sha256(VO_WAV)
    if vo_sha != EXPECTED_VO_SHA256:
        raise SystemExit(f"VO sha256 mismatch: {vo_sha} != {EXPECTED_VO_SHA256}")
    bed_sha = sha256(BED_MP3)
    if bed_sha != EXPECTED_BED_SHA256:
        raise SystemExit(f"Bed sha256 mismatch: {bed_sha} != {EXPECTED_BED_SHA256}")
    master_sha = sha256(MASTER_V02)
    if master_sha != EXPECTED_MASTER_SHA256:
        raise SystemExit(f"Master v02 sha256 mismatch: {master_sha} != {EXPECTED_MASTER_SHA256}")
    s03_path = resolve_asset_path("SVS12709_Cassini_Titan_Flyby_260_264_1080.mp4")
    s03_sha = sha256(s03_path)
    if s03_sha != EXPECTED_S03_SHA256:
        raise SystemExit(f"S03 sha256 mismatch: {s03_sha} != {EXPECTED_S03_SHA256}")
    print(f"Verified SHA-256s: VO={vo_sha[:12]}... Bed={bed_sha[:12]}... Master_v02={master_sha[:12]}... S03={s03_sha[:12]}...", flush=True)

    # Record SHA-256 provenance of every input still and video clip used in v03
    source_provenance: dict[str, dict] = {
        "parent_master_v02": {"path": str(MASTER_V02), "sha256": master_sha},
        "locked_vo_v02b": {"path": str(VO_WAV), "sha256": vo_sha},
        "score_bed_v01": {"path": str(BED_MP3), "sha256": bed_sha},
        "starfield_source": {"path": str(NAS_HARV / "weic2310a.png"), "sha256": sha256(NAS_HARV / "weic2310a.png")},
    }
    for shot in SHOT_PLAN:
        for key in ("source", "raw_source", "photo_source"):
            fname = shot.get(key)
            if not fname or fname.startswith("code_graphic_") or fname.startswith("frame0_return_"):
                continue
            if fname not in source_provenance:
                p = resolve_asset_path(fname)
                entry = {
                    "path": str(p),
                    "sha256": sha256(p),
                    "credit": shot.get("credit", ""),
                    "title": shot.get("title", ""),
                }
                if fname == "SVS12709_Cassini_Titan_Flyby_260_264_1080.mp4":
                    entry["provenance_json"] = str(NAS_HARV_J3865 / "SVS12709_PROVENANCE.json")
                    entry["nasa_id"] = "GSFC_20170912_Cassini_m12709_CIRS_Short"
                    entry["svs_id"] = 12709
                    entry["xmp_ingredient"] = "Cassini_Saturn_Animation_Reel.mov"
                    entry["source_window_s"] = [260.000, 263.767]
                    entry["rights"] = "NASA GSFC Public Domain visual asset (audio stripped via -an)"
                source_provenance[fname] = entry

    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    OUT_WORK = WORK / "exports"
    OUT_WORK.mkdir(parents=True)

    slices, words, last_word_end = build_voice_plan()
    joined = " ".join(w["w"] for w in words)
    print(f"Spoken words: {len(words)} | VO: {words[0]['s']:.3f}-{last_word_end:.3f} s | Total: {TOTAL_S:.3f} s", flush=True)

    # Read S08 reveal timestamps STRICTLY from locked words.json (zero arbitrary offsets)
    payoff_w = next(w for w in words if w["w"].lower() == "second")
    hidden_w = next(w for w in words if w["w"].lower() == "hidden")
    liquid_w = next(w for w in words if w["w"].lower() == "liquid" and w["s"] > 20.0)
    second_s = float(payoff_w["s"])   # 21.000 s
    hidden_s = float(hidden_w["s"])   # 21.520 s
    liquid_s = float(liquid_w["s"])   # 22.960 s
    print(f"S08 locked-word reveals: second={second_s:.3f}s, hidden={hidden_s:.3f}s, liquid={liquid_s:.3f}s", flush=True)

    for shot in SHOT_PLAN[:-1]:
        cut_t = shot["out"]
        for w in words:
            if w["s"] + 0.005 < cut_t < w["e"] - 0.005:
                raise SystemExit(f"Cut at {cut_t:.3f}s splits word {w['w']!r} ({w['s']:.3f}-{w['e']:.3f}s)")
    print(f"Verified 0 spoken words split across all {len(SHOT_PLAN)-1} cut boundaries.", flush=True)

    open_f0 = WORK / "open_f0.png"
    concat_lines = []
    cuts_meta = []
    pool_meta = []
    seen_sources = set()
    teach_info: dict = {}

    for idx, shot in enumerate(SHOT_PLAN):
        piece = WORK / f"piece_{idx:02d}.mp4"
        up, extra = render_shot(
            shot,
            piece,
            open_f0 if idx == 0 else None,
            s08_timings=(second_s, hidden_s, liquid_s) if shot["kind"] == "titan_ocean_depth" else None,
        )
        if extra is not None:
            teach_info = extra
        concat_lines.append(f"file '{piece.name}'")
        framing = (
            {"offset": shot["offset"], "crop": "9:16 full-bleed", "mode": "cover"}
            if shot["video"]
            else {"crop": "9:16 full-bleed", "mode": "cover"}
        )
        if "crop_box" in shot:
            framing["crop_box"] = list(shot["crop_box"])
        if "x0_start" in shot:
            framing["x0_pan"] = [shot["x0_start"], shot["x0_end"]]
        c_entry = {
            "row": shot["row"],
            "timeline_in": shot["in"],
            "timeline_out": shot["out"],
            "source": shot["source"],
            "upscale": up,
            "video": bool(shot["video"]),
            "framing": framing,
        }
        cuts_meta.append(c_entry)
        if shot["source"] not in seen_sources:
            seen_sources.add(shot["source"])
            pool_meta.append({
                "id": Path(shot["source"]).stem,
                "file": shot["source"],
                "file_id": shot["source"],
                "source": shot["source"],
                "title": shot["title"],
                "credit": shot.get("credit", ""),
            })
        print(f"  rendered {shot['row']} ({shot['in']:.3f}-{shot['out']:.3f} s) video={shot['video']} upscale={up}", flush=True)

    (WORK / "list.txt").write_text("\n".join(concat_lines) + "\n")
    pic_mp4 = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"), "-c", "copy", str(pic_mp4)])

    hook_info = make_hook(WORK / "hook.png")
    title_info = make_title(WORK / "title.png")
    caps = caption_chunks(words, last_word_end)
    for i, c in enumerate(caps):
        c["bbox"] = make_caption(WORK / f"cap_{i:02d}.png", c["text"])

    aud = build_audio(WORK, slices, TOTAL_S, second_s, hidden_s, liquid_s)
    cal_wav, aac_i, aac_tp = calibrate_aac_wav(WORK, WORK / "mix.wav", TOTAL_S)
    aud["aac_lufs"] = aac_i
    aud["aac_tp_dbtp"] = aac_tp

    final_mp4 = OUT_WORK / f"{STEM}.mp4"
    inputs = ["-t", f"{TOTAL_S:.3f}", "-i", str(pic_mp4)]
    for name in ("hook.png", "title.png"):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL_S:.3f}", "-i", str(WORK / name)]
    inputs += ["-i", str(cal_wav)]
    base_idx = 4
    for i in range(len(caps)):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL_S:.3f}", "-i", str(WORK / f"cap_{i:02d}.png")]

    fc = [
        f"[0:v]fps={FPS},setsar=1,format=yuv420p[v0]",
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='gte(t,0)*lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.28:alpha=1,fade=t=out:st={TITLE_OUT - 0.28:.2f}:d=0.28:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
    ]
    last_v = "v2"
    for i, c in enumerate(caps):
        fc.append(f"[{last_v}][{base_idx + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last_v = f"c{i}"
    fc.append(f"[{last_v}]noise=alls=2:allf=t,format=yuv420p[v]")

    run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", ";".join(fc),
        "-map", "[v]", "-map", "3:a",
        *shorts_encode_args(fps=FPS),
        "-t", f"{TOTAL_S:.3f}", str(final_mp4),
    ])

    words_path = OUT_WORK / f"{STEM}_words.json"
    transcript_path = OUT_WORK / f"{STEM}_transcript.txt"
    srt_path = OUT_WORK / f"{STEM}_en-GB.srt"
    cuts_path = OUT_WORK / f"{STEM}_cuts.json"
    pool_path = OUT_WORK / f"{STEM}_pool.json"
    meta_path = OUT_WORK / f"{STEM}_meta.json"
    vo_stem_out = OUT_WORK / f"{STEM}_vo.wav"
    sfx_stem_out = OUT_WORK / f"{STEM}_sfx.wav"
    bed_stem_out = OUT_WORK / f"{STEM}_bed.wav"
    shutil.copy2(WORK / "stem_vo.wav", vo_stem_out)
    shutil.copy2(WORK / "stem_sfx.wav", sfx_stem_out)
    shutil.copy2(WORK / "stem_bed.wav", bed_stem_out)

    words_path.write_text(json.dumps(words, indent=2) + "\n")
    transcript_path.write_text(joined + "\n")
    write_srt(srt_chunks_full(words, last_word_end), srt_path)
    cuts_path.write_text(json.dumps(cuts_meta, indent=2) + "\n")
    pool_path.write_text(json.dumps(pool_meta, indent=2) + "\n")

    surprise_dry = next(w for w in words if w["w"].lower() == "dry")
    surprise_wrong = next(w for w in words if w["w"].lower() == "wrong.")
    s44_s45_breath = round(words[6]["s"] - words[5]["e"], 3)
    s45_s46_breath = round(words[7]["s"] - words[6]["e"], 3)
    s46_end_idx = next(i for i, w in enumerate(words) if w["w"].lower() == "gas.")
    s46_s52_breath = round(words[s46_end_idx + 1]["s"] - words[s46_end_idx]["e"], 3)

    e1_metrics = {
        "frame0_source": "SVS20311_DF_Open_1080.mp4 @ offset=1.800s (video=True, full-bleed 9:16)",
        "vo_onset_s": words[0]["s"],
        "surprise_dry_start_s": surprise_dry["s"],
        "surprise_desert_end_s": words[5]["e"],
        "surprise_wrong_start_s": surprise_wrong["s"],
        "cut1_s": SHOT_PLAN[0]["out"],
        "cut2_s": SHOT_PLAN[1]["out"],
        "all_cuts_s": [s["out"] for s in SHOT_PLAN[:-1]],
        "max_shot_s": max(round(s["out"] - s["in"], 3) for s in SHOT_PLAN),
        "bridge_1_9_to_8_5_all_video": all(s["video"] for s in SHOT_PLAN if 1.900 <= s["in"] < 8.500),
        "s03_source": "SVS12709_Cassini_Titan_Flyby_260_264_1080.mp4 (NASA SVS 12709, Cassini orbiter over Titan)",
        "s44_s45_breath_s": s44_s45_breath,
        "s45_s46_breath_s": s45_s46_breath,
        "s46_s52_breath_s": s46_s52_breath,
        "spoken_payoff_word": payoff_w["w"],
        "spoken_payoff_start_s": second_s,
        "spoken_payoff_pct": round(second_s / TOTAL_S * 100.0, 1),
        "visual_ocean_sweep_start_s": second_s,
        "visual_ocean_sweep_pct": round(second_s / TOTAL_S * 100.0, 1),
        "visual_hidden_ocean_reveal_s": hidden_s,
        "visual_liquid_water_reveal_s": liquid_s,
        "last_word": words[-1]["w"],
        "last_word_end_s": last_word_end,
        "loop_point_s": TOTAL_S,
        "tail_gap_s": round(TOTAL_S - last_word_end, 3),
        "loop_connection": "...likely mixed with salts and ammonia. -> Is Titan just a dry desert?",
        "meta_promise_or_cta": False,
        "end_card": None,
        "extra_teach_pill_removed": True,
    }

    nas_vo_future = NAS_SUB_OUT / f"{STEM}_vo.wav"
    nas_words_future = NAS_SUB_OUT / f"{STEM}_words.json"
    meta_obj = {
        "slug": SHORT_SLUG,
        "stem": STEM,
        "version": "v03",
        "replaces_for_review": "032_short_dry_desert_two_oceans_v02 (v01 & v02 preserved untouched on NAS)",
        "title": SHORT_TITLE,
        "alt_title": ALT_TITLE,
        "air_date": AIR_DATE,
        "air_date_status": "UNAPPROVED_GATE_CHECK_DATE_ONLY",
        "test_a": False,
        "relatedVideoId": LONG_ID,
        "parent_long_id": LONG_ID,
        "parent_long_title": LONG_TITLE,
        "parent_long_title_verified_snapshot": "2026-11-27.json",
        "parent_master_v02_sha256": master_sha,
        "spoken": joined,
        "vo_onset_s": words[0]["s"],
        "last_word_end_s": last_word_end,
        "duration_s": TOTAL_S,
        "hook": {"text": hook_info["text"], "start_s": 0.0, "end_s": HOOK_END},
        "title_banner": {"text": LONG_TITLE, "start_s": TITLE_IN, "end_s": TITLE_OUT},
        "teach_graphic": teach_info,
        "end_card": None,
        "e1_metrics": e1_metrics,
        "source_provenance": source_provenance,
        "bounded_external_search": BOUNDED_EXTERNAL_SEARCH,
        "words_file": str(words_path),
        "vo": str(vo_stem_out),
        "audio": aud,
    }
    meta_path.write_text(json.dumps(meta_obj, indent=2) + "\n")

    # Full-size (1080x1920) stills: frame0, cover, and EVERY corrected shot & graphic state
    frame0_jpg = OUT_WORK / f"{STEM}_frame0.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.30", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(frame0_jpg)])
    cover_jpg = OUT_WORK / f"{STEM}_cover.jpg"
    cover_info = make_cover(cover_jpg, open_f0)

    corrected_stills_spec = [
        ("S02_dunes_3.3s", 3.30),
        ("S03_cassini_titan_5.2s", 5.20),
        ("S03_cassini_titan_6.6s", 6.60),
        ("S03_cassini_titan_8.1s", 8.10),
        ("S04_coastline_10.3s", 10.30),
        ("S07_cassini_gravity_18.6s", 18.60),
        ("S08_graphic_20.8s_pre_payoff", 20.80),
        ("S08_graphic_22.0s_hidden_ocean", 22.00),
        ("S08_graphic_23.4s_liquid_water", 23.40),
    ]
    corrected_stills: dict[str, dict] = {}
    for tag, ts in corrected_stills_spec:
        sp_jpg = OUT_WORK / f"{STEM}_still_{tag}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ts:.2f}", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(sp_jpg)])
        corrected_stills[tag] = {"file": sp_jpg.name, "time_s": ts, "sha256": sha256(sp_jpg)}

    # Dedicated phone-size graphic preview sheet (360x640 + 240x427)
    phone_preview_path = OUT_WORK / f"{STEM}_phone_graphic_preview.jpg"
    make_phone_graphic_preview(
        phone_preview_path,
        [
            ("20.8s Pre-Payoff", OUT_WORK / f"{STEM}_still_S08_graphic_20.8s_pre_payoff.jpg"),
            ("22.0s Hidden Ocean", OUT_WORK / f"{STEM}_still_S08_graphic_22.0s_hidden_ocean.jpg"),
            ("23.4s Liquid Water", OUT_WORK / f"{STEM}_still_S08_graphic_23.4s_liquid_water.jpg"),
        ],
    )

    # 10-shot review contact sheet
    shot_tiles = []
    for idx, shot in enumerate(SHOT_PLAN):
        mid_t = round((shot["in"] + shot["out"]) / 2.0, 2)
        if shot["row"] == "S08_titan_ocean_depth":
            mid_t = 23.40
        raw_t = sp.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{mid_t:.2f}", "-i", str(final_mp4),
            "-frames:v", "1", "-vf", "scale=360:640", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
        ])
        im_t = Image.frombytes("RGB", (360, 640), raw_t)
        d_t = ImageDraw.Draw(im_t)
        d_t.rectangle((0, 0, 360, 32), fill=(0, 0, 0))
        d_t.text((8, 8), f"{idx+1:02d} {shot['row']} ({mid_t:.1f}s)", fill=(255, 255, 255))
        shot_tiles.append(im_t)
    cols_s = 5
    rows_s = (len(shot_tiles) + cols_s - 1) // cols_s
    sheet_10 = Image.new("RGB", (360 * cols_s, 640 * rows_s), (18, 22, 30))
    for idx, im_t in enumerate(shot_tiles):
        sheet_10.paste(im_t, ((idx % cols_s) * 360, (idx // cols_s) * 640))
    sheet_10_path = OUT_WORK / f"{STEM}_review_10shots.jpg"
    sheet_10.save(sheet_10_path, quality=92)

    def run_gate(cmd: list) -> sp.CompletedProcess:
        return sp.run([str(x) for x in cmd], capture_output=True, text=True)

    g_txt = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", final_mp4, "--air-date", AIR_DATE, "--sheet-dir", OUT_WORK])
    g_json = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", final_mp4, "--air-date", AIR_DATE, "--sheet-dir", OUT_WORK, "--json"])
    (OUT_WORK / f"{STEM}_gate.txt").write_text((g_txt.stdout or "") + (g_txt.stderr or ""))
    (OUT_WORK / f"{STEM}_gate.json").write_text(g_json.stdout or g_json.stderr)
    print(g_txt.stdout, end="", flush=True)

    tp_f0 = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py", "short", frame0_jpg, "--out", OUT_WORK / f"{STEM}_frame0_preview.jpg", "--score"])
    tp_cov = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py", "short", cover_jpg, "--out", OUT_WORK / f"{STEM}_cover_preview.jpg", "--score"])
    print(tp_f0.stdout, end="", flush=True)
    print(tp_cov.stdout, end="", flush=True)

    sfx_res = run_gate([
        sys.executable, REPO / "scripts/sfx_kit.py", "level",
        "--vo", vo_stem_out, "--sfx", sfx_stem_out, "--bed", bed_stem_out,
        "--minutes", f"{TOTAL_S / 60:.3f}",
        "--out", OUT_WORK / f"{STEM}_sfx_level.json",
    ])
    (OUT_WORK / f"{STEM}_sfx.txt").write_text((sfx_res.stdout or "") + (sfx_res.stderr or ""))
    print(sfx_res.stdout, end="", flush=True)

    mg_res = run_gate([
        sys.executable, REPO / "scripts/music_gate.py", NAS_FILM,
        "--bed", BED_MP3, "--video", final_mp4,
        "--out", OUT_WORK / f"{STEM}_music_gate.json",
    ])
    (OUT_WORK / f"{STEM}_music_gate.txt").write_text((mg_res.stdout or "") + (mg_res.stderr or ""))
    print(mg_res.stdout, end="", flush=True)

    canonical_mp3_beds = collect_canonical_owb_mp3_beds()
    mg_canon = run_gate([
        sys.executable, REPO / "scripts/music_gate.py", NAS_FILM,
        "--bed", BED_MP3, "--video", final_mp4,
        "--others", *canonical_mp3_beds,
        "--out", OUT_WORK / f"{STEM}_music_gate_canonical_mp3.json",
    ])
    (OUT_WORK / f"{STEM}_music_gate_canonical_mp3.txt").write_text((mg_canon.stdout or "") + (mg_canon.stderr or ""))
    print(f"Canonical NAS MP3 beds checked ({len(canonical_mp3_beds)}): rc={mg_canon.returncode}", flush=True)
    print(mg_canon.stdout, end="", flush=True)

    pg_res = run_gate([
        sys.executable, REPO / "scripts/polish_gate.py", final_mp4,
        "--cuts", cuts_path,
        "--out", OUT_WORK / f"{STEM}_polish_gate.json",
    ])
    (OUT_WORK / f"{STEM}_polish_gate.txt").write_text((pg_res.stdout or "") + (pg_res.stderr or ""))
    print(pg_res.stdout, end="", flush=True)

    pqa_dir = OUT_WORK / f"{STEM}_picture_qa"
    pqa_res = run_gate([
        sys.executable, REPO / "scripts/picture_qa.py", final_mp4,
        "--cuts", cuts_path, "--pool", pool_path, "--out-dir", pqa_dir,
    ])
    (OUT_WORK / f"{STEM}_picture_qa.txt").write_text((pqa_res.stdout or "") + (pqa_res.stderr or ""))
    print(pqa_res.stdout, end="", flush=True)

    gates = {
        "gate_shorts_open_rc": g_txt.returncode,
        "thumb_preview_frame0_rc": tp_f0.returncode,
        "thumb_preview_cover_rc": tp_cov.returncode,
        "sfx_level_rc": sfx_res.returncode,
        "music_gate_rc": mg_res.returncode,
        "music_gate_canonical_mp3_rc": mg_canon.returncode,
        "music_gate_canonical_mp3_count": len(canonical_mp3_beds),
        "polish_gate_rc": pg_res.returncode,
        "picture_qa_rc": pqa_res.returncode,
    }
    print("GATES:", json.dumps(gates, indent=2), flush=True)
    if any(v != 0 for k, v in gates.items() if k.endswith("_rc")):
        raise SystemExit(1)

    if "--no-nas" in sys.argv:
        print("DRY BUILD PASS (--no-nas); skipping NAS copy.", flush=True)
        return

    NAS_SUB_OUT.mkdir(parents=True, exist_ok=True)
    meta_obj["words_file"] = str(nas_words_future)
    meta_obj["vo"] = str(nas_vo_future)
    meta_path.write_text(json.dumps(meta_obj, indent=2) + "\n")
    cover_info["file"] = str(NAS_SUB_OUT / f"{STEM}_cover.jpg")

    open_sheet_path = OUT_WORK / f"{STEM}_open_sheet.jpg"
    summary = {
        "stem": STEM,
        "version": "v03",
        "mp4_path": str(NAS_SUB_OUT / f"{STEM}.mp4"),
        "mp4_sha256": sha256(final_mp4),
        "frame0_jpg_sha256": sha256(frame0_jpg),
        "cover_jpg_sha256": sha256(cover_jpg),
        "open_sheet_sha256": sha256(open_sheet_path),
        "review_10shots_sha256": sha256(sheet_10_path),
        "phone_graphic_preview_sha256": sha256(phone_preview_path),
        "corrected_stills": corrected_stills,
        "master_v02_sha256": master_sha,
        "vo_sha256": vo_sha,
        "bed_sha256": bed_sha,
        "s03_source_sha256": s03_sha,
        "duration_s": TOTAL_S,
        "fps": FPS,
        "frames": round(TOTAL_S * FPS),
        "words_count": len(words),
        "e1_metrics": e1_metrics,
        "source_provenance": source_provenance,
        "bounded_external_search": BOUNDED_EXTERNAL_SEARCH,
        "audio": aud,
        "hook": hook_info,
        "title": title_info,
        "teach_graphic": meta_obj["teach_graphic"],
        "end_card": None,
        "cover": cover_info,
        "gates": gates,
    }
    summary_path = OUT_WORK / f"{STEM}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")

    for item in sorted(OUT_WORK.iterdir()):
        if item.is_dir():
            dst_dir = NAS_SUB_OUT / item.name
            dst_dir.mkdir(parents=True, exist_ok=True)
            for sub in sorted(item.iterdir()):
                if sub.is_file():
                    copy_verified(sub, dst_dir / sub.name)
        elif item.is_file():
            copy_verified(item, NAS_SUB_OUT / item.name)

    g_nas_txt = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", NAS_SUB_OUT / f"{STEM}.mp4", "--air-date", AIR_DATE, "--sheet-dir", NAS_SUB_OUT])
    g_nas_json = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", NAS_SUB_OUT / f"{STEM}.mp4", "--air-date", AIR_DATE, "--sheet-dir", NAS_SUB_OUT, "--json"])
    if g_nas_txt.returncode != 0:
        raise SystemExit(f"NAS gate_shorts_open failed: {g_nas_txt.stdout}\n{g_nas_txt.stderr}")
    (NAS_SUB_OUT / f"{STEM}_gate.txt").write_text((g_nas_txt.stdout or "") + (g_nas_txt.stderr or ""))
    (NAS_SUB_OUT / f"{STEM}_gate.json").write_text(g_nas_json.stdout or g_nas_json.stderr)

    mirror_names = [
        f"{STEM}.mp4",
        f"{STEM}_frame0.jpg",
        f"{STEM}_cover.jpg",
        f"{STEM}_frame0_preview.jpg",
        f"{STEM}_cover_preview.jpg",
        f"{STEM}_open_sheet.jpg",
        f"{STEM}_review_10shots.jpg",
        f"{STEM}_phone_graphic_preview.jpg",
        f"{STEM}_meta.json",
        f"{STEM}_words.json",
        f"{STEM}_transcript.txt",
        f"{STEM}_en-GB.srt",
        f"{STEM}_cuts.json",
        f"{STEM}_pool.json",
        f"{STEM}_gate.txt",
        f"{STEM}_gate.json",
        f"{STEM}_music_gate_canonical_mp3.txt",
        f"{STEM}_music_gate_canonical_mp3.json",
        f"{STEM}_summary.json",
    ] + [v["file"] for v in corrected_stills.values()]
    for name in mirror_names:
        copy_verified(NAS_SUB_OUT / name, NAS_SHORTS / name)

    print(f"NAS copies verified by SHA-256: {NAS_SUB_OUT / (STEM + '.mp4')} ({summary['mp4_sha256']})", flush=True)


if __name__ == "__main__":
    main()
