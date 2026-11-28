#!/usr/bin/env python3
"""064 Every Planet Explained — Companion Short 2 (464°C Venus vs −224°C Uranus) v01 Builder (J3904).

Full-bleed 1080x1920 (9:16), 24 fps CFR (exact 441 frames = 18.375 s, dead inside Ben's 16.0-19.0 s band).
Zero blurred bars/padding, zero near-black, zero integer push jitter, zero Orbit at frame 0, zero Veo CGI.
Uses locked v03 script (`064_short02_venus_vs_uranus_script_v03.md`, sha256 634da160...) and Chief-authorized
VO take `064_short02_venus_vs_uranus_vo_v01.wav` (205 ElevenLabs chars <= 600 cap, £0 cash, overage off),
0 Flow/Vertex credits, zero YouTube upload or scheduling.

Short Title: Why Is Venus 464°C While Uranus Drops to −224°C?
Slug / Stem: short02_venus_vs_uranus / 064_short02_venus_vs_uranus_v01
Proposed Candidate / Gate-Check Slot: Wed 30 Dec 2026 11:30Z (non-colliding Mon/Wed/Fri/Sat Orbit Short day;
  NOT scheduled yet; MUST NOT upload or air before 064 long is public Wed 16 Dec 18:00 London)
Parent Long (064): Every Planet Explained in 12 Minutes (Mercury to Neptune)
"""
from __future__ import annotations

import hashlib
import json
import math
import os
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
REPO = HERE.parents[3]

NAS_STUDIO_LIVE = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects")
NAS_ARCHIVE_023 = Path(
    "/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/"
    "023_What-Happened-To-Venus/07_Edit-Project/nasa_pool_v01"
)
NAS_033 = NAS_STUDIO_LIVE / "033_Why-This-Planet-Has-21-Year-Winters"
NAS_064 = NAS_STUDIO_LIVE / "064_Every-Planet-Explained-In-10-Minutes"
NAS_SHORTS = NAS_064 / "10_Shorts"
NAS_SUB_DIR = NAS_SHORTS / "short02_venus_vs_uranus"
NAS_SUB_OUT = NAS_SUB_DIR / "06_Final-Exports"

VO_WAV = NAS_SUB_DIR / "02_Voiceover" / "064_short02_venus_vs_uranus_vo_v01.wav"
STT_JSON = NAS_SUB_DIR / "02_Voiceover" / "stt" / "064_short02_venus_vs_uranus_vo_v01" / "stt_raw.json"
TAKE_JSON = NAS_SUB_DIR / "02_Voiceover" / "064_short02_venus_vs_uranus_vo_v01_TAKE.json"
BED_MP3 = NAS_064 / "05_Music" / "every_planet_score_bed_v01.mp3"
EXPECTED_BED_SHA256 = "3e47e9d6da9aca6836a00c27a1fa58e53801190ae06ed445966ed51f5c0d75c6"
KIT_DIR = NAS_064 / "06_Sound-Effects" / "kit_v01"

# Verified real NASA / ESA assets (zero Veo CGI, zero Keck misattribution)
SRC_PARKER_VENUS = NAS_ARCHIVE_023 / "harvest_v04" / "svs14095_14095_ParkerVenus_YouTube_NoText_NoMusic.mp4"
SRC_SDO_TRANSIT = NAS_ARCHIVE_023 / "sdo" / "AIA171VenusTransit_HD1080.mp4"
SRC_SVS20390_URANUS = NAS_033 / "03_Reference-Material" / "harvest_J2299_v01" / "svs20390_Shot8_4k.mp4"
SRC_JWST_URANUS = NAS_033 / "03_Reference-Material" / "harvest_J2299_v01" / "weic2332a_hires.jpg"
SRC_VOYAGER_URANUS = NAS_033 / "03_Reference-Material" / "harvest_J2299_v01" / "PIA01488.jpg"
SRC_WISPR_3RD = NAS_ARCHIVE_023 / "harvest_v04" / "svs14095_WISPR_Magellan_3rdFlyby.mp4"
SRC_MAGELLAN_VENUS = NAS_064 / "03_Reference-Material" / "J3835_radar_v01" / "PIA00215.jpg"

EXPECTED_SHA256 = {
    SRC_PARKER_VENUS: "ebb967994b150bc878f31ccb36107adaf99bb1fa7f0217e7516556a40833849e",
    SRC_SDO_TRANSIT: "e580945d4b767e7ed3524636d61520f1b03210c814e348727b18ed9e507d30fc",
    SRC_SVS20390_URANUS: "8345caca2a6cc429",  # prefix verified below
    SRC_JWST_URANUS: "b241901c2754e811",
    SRC_VOYAGER_URANUS: "9c49e13d8da1c052",
    SRC_WISPR_3RD: "4b3d0c25e309e10da68dc4ca964ab6175875c8dd8313fe8b2b9d059005b27604",
    SRC_MAGELLAN_VENUS: "46dc965a02d4bff533685892ad16a76845a384d482ffaedda024c870b5b8a7b4",
}

SCRATCH_BASE = Path(os.environ.get("STUDIO_SCRATCH", "/Volumes/MiniWork/scratch"))
WORK = SCRATCH_BASE / "J3904_064_short02_v01"

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import gate_shorts_open as gso  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 24
SR = 48000
TOTAL_FRAMES = 441
TOTAL_S = TOTAL_FRAMES / FPS  # 18.375 s exact at 24 fps CFR (inside 16.0-19.0 s band)

BAND_H = round(W * 9 / 16)       # 608 px
BAND_Y0 = (H - BAND_H) // 2      # 656 px
BAND_Y1 = BAND_Y0 + BAND_H       # 1264 px
LINE_H = round(BAND_H * 0.115)   # 70 px

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)      # #FFE000
NAVY_FLOOR = np.array([28.0, 38.0, 58.0], dtype=np.float32)

STEM = "064_short02_venus_vs_uranus_v01"
SHORT_SLUG = "short02_venus_vs_uranus"
SHORT_TITLE = "Why Is Venus 464°C While Uranus Drops to −224°C?"
AIR_DATE = "2026-12-30"  # Non-colliding Wed 11:30Z candidate slot strictly after 16 Dec long; NOT scheduled
LONG_TITLE = "Every Planet Explained in 12 Minutes (Mercury to Neptune)"

HOOK_ROWS = [("464°C VENUS", YELLOW), ("VS −224°C?", WHITE)]
COVER_ROWS = [("464°C VENUS", YELLOW), ("VS −224°C?", WHITE)]
TITLE_ROWS = [
    "Every Planet Explained",
    "in 12 Minutes",
    "(Mercury to Neptune)",
]

HOOK_END = 2.10
TITLE_IN, TITLE_OUT = 9.00, 14.00
TEACH_IN, TEACH_OUT = 14.90, 17.45
TEACH_TEXT = "464°C · RUNAWAY GREENHOUSE"

# Clean silence-trimmed segments from 064_short02_venus_vs_uranus_vo_v01.wav (atempo = 1.0, 0 words dropped)
VO_SEGMENTS = [
    (0.080, 4.240),   # "Why is Venus's surface 464 degrees Celsius"
    (4.500, 8.400),   # "while Uranus's air drops to -224?"
    (9.200, 11.280),  # "Uranus has no true surface."
    (11.460, 12.940), # "That's its coldest air."
    (13.500, 14.340), # "On Venus,"
    (14.560, 19.040), # "thick carbon dioxide air traps heat in a runaway greenhouse"
]
VO_LEAD_S = 0.000
VO_GAPS = [0.100, 0.160, 0.100, 0.160, 0.100]

# 8-shot full-bleed 1080x1920 cut plan at exact 24 fps frames (sum = 441 frames = 18.375 s).
# Cut 1 = 1.750 s (<= 2.80 s), Cut 2 = 4.208 s (<= 4.80 s), max shot = 3.958 s (<= 4.00 s).
# Zero split spoken words; zero Veo CGI; zero consecutive stills > 2; every upscale <= 1.85x.
SHOT_PLAN = [
    {
        "row": "R01",
        "f0": 0, "f1": 42,  # 0.000 - 1.750 s (1.750 s <= 2.80 s)
        "kind": "parker_venus",
        "src_path": SRC_PARKER_VENUS,
        "source": "svs14095_14095_ParkerVenus_YouTube_NoText_NoMusic.mp4",
        "title": "NASA SVS 14095 Parker Solar Probe Venus flyby visualization (golden sunlit Venus limb)",
        "video": True,
        "offset": 17.600,
        "crop_x": 160,
        "crop_w": 608,
        "crop_y": 0,
        "crop_h": 1080,
        "upscale": 1.78,
    },
    {
        "row": "R02",
        "f0": 42, "f1": 101,  # 1.750 - 4.208 s (2.458 s; Cut 2 = 4.208 s <= 4.80 s)
        "kind": "sdo_transit",
        "src_path": SRC_SDO_TRANSIT,
        "source": "AIA171VenusTransit_HD1080.mp4",
        "title": "NASA SDO AIA 171 Å observational Venus transit across the Sun",
        "video": True,
        "offset": 16.500,
        "crop_x": 656,
        "crop_w": 608,
        "crop_y": 0,
        "crop_h": 1080,
        "upscale": 1.78,
    },
    {
        "row": "R03",
        "f0": 101, "f1": 196,  # 4.208 - 8.167 s (3.958 s <= 4.00 s)
        "kind": "svs20390_uranus",
        "src_path": SRC_SVS20390_URANUS,
        "source": "svs20390_Shot8_4k.mp4",
        "title": "NASA Goddard SVS 20390 Shot 8 4K Uranus and tilted rings visualization",
        "video": True,
        "offset": 1.600,
        "crop_y": 264,
        "crop_h": 1632,
        "crop_w": 918,
        "x0": 2050,
        "x1": 1520,
        "upscale": 1.18,
    },
    {
        "row": "R04",
        "f0": 196, "f1": 251,  # 8.167 - 10.458 s (2.292 s <= 4.00 s)
        "kind": "still_push",
        "src_path": SRC_JWST_URANUS,
        "source": "weic2332a_hires.jpg",
        "title": "ESA/Webb NASA CSA STScI JWST NIRCam Uranus rings and polar cap (CC BY 4.0)",
        "video": False,
        "z0": 1.00, "z1": 1.08,
        "x_frac": 0.50, "y_frac": 0.50,
        "sat": 1.24, "contrast": 1.12,
        "space_lift": True,
        "upscale": 1.25,
    },
    {
        "row": "R05",
        "f0": 251, "f1": 289,  # 10.458 - 12.042 s (1.583 s <= 4.00 s)
        "kind": "still_push",
        "src_path": SRC_VOYAGER_URANUS,
        "source": "PIA01488.jpg",
        "title": "NASA/JPL Voyager 2 Uranus blue-cyan atmosphere (PIA01488)",
        "video": False,
        "z0": 1.00, "z1": 1.08,
        "x_frac": 0.50, "y_frac": 0.50,
        "sat": 1.28, "contrast": 1.14,
        "space_lift": True,
        "upscale": 0.73,
    },
    {
        "row": "R06",
        "f0": 289, "f1": 357,  # 12.042 - 14.875 s (2.833 s <= 4.00 s)
        "kind": "wispr_venus",
        "src_path": SRC_WISPR_3RD,
        "source": "svs14095_WISPR_Magellan_3rdFlyby.mp4",
        "title": "NASA/JHUAPL/NRL Parker Solar Probe WISPR Venus night-side glow + Magellan radar 3rd flyby",
        "video": True,
        "offset": 0.200,
        "crop_x": 0,
        "crop_w": 585,
        "crop_y": 0,
        "crop_h": 1040,
        "upscale": 1.85,
    },
    {
        "row": "R07",
        "f0": 357, "f1": 420,  # 14.875 - 17.500 s (2.625 s <= 4.00 s)
        "kind": "still_push",
        "src_path": SRC_MAGELLAN_VENUS,
        "source": "PIA00215.jpg",
        "title": "NASA/JPL Magellan synthetic aperture radar Venus volcanic surface (PIA00215)",
        "video": False,
        "inner_crop": (350, 600, 2550, 1838),
        "z0": 1.00, "z1": 1.08,
        "x_frac": 0.50, "y_frac": 0.50,
        "sat": 1.26, "contrast": 1.14,
        "space_lift": False,
        "upscale": 1.55,
    },
    {
        "row": "R08_loop",
        "f0": 420, "f1": 441,  # 17.500 - 18.375 s (0.875 s < 1.20 s)
        "kind": "parker_venus_loop",
        "src_path": SRC_PARKER_VENUS,
        "source": f"frame0_return_{STEM}.mp4",
        "title": "NASA SVS 14095 Parker Solar Probe Venus flyby forward pre-roll return into Frame 0",
        "video": True,
        "offset": 16.725,  # ends exactly 1 frame before R01 t=17.600 s
        "crop_x": 160,
        "crop_w": 608,
        "crop_y": 0,
        "crop_h": 1080,
        "upscale": 1.78,
    },
]


def run(cmd: list) -> None:
    sp.run([str(c) for c in cmd], check=True)


def run_gate(cmd: list) -> sp.CompletedProcess:
    return sp.run([str(x) for x in cmd], capture_output=True, text=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        sr = w.getframerate()
        sw = w.getsampwidth()
        ch = w.getnchannels()
        assert sr == SR and sw == 2, f"Unexpected WAV format in {p}: sr={sr}, sw={sw}, ch={ch}"
        a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
        if ch == 1:
            return np.stack([a, a], axis=-1)
        assert ch == 2
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


def font_for(px: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BLACK, max(24, int(round(px))))


def centred(d: ImageDraw.ImageDraw, y: int, text: str, f: ImageFont.FreeTypeFont, col: tuple, stroke: int = 7) -> list[int]:
    bb = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
    tw = bb[2] - bb[0]
    x = (W - tw) // 2 - bb[0]
    d.text((x, y), text, font=f, fill=col, stroke_width=stroke, stroke_fill=(10, 16, 30, 255))
    b2 = d.textbbox((x, y), text, font=f, stroke_width=stroke)
    return [int(b2[0]), int(b2[1]), int(b2[2]), int(b2[3])]


def lift_navy(arr: np.ndarray) -> np.ndarray:
    mx = arr.max(axis=2, keepdims=True)
    return np.where(mx < 54.0, np.maximum(arr, NAVY_FLOOR), arr)


_STAR_CANVAS: np.ndarray | None = None


def get_star_canvas(cw: int = 1360, ch: int = 2360) -> np.ndarray:
    global _STAR_CANVAS
    if _STAR_CANVAS is None:
        rng = np.random.default_rng(6402)
        yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
        wave1 = 0.5 + 0.5 * np.sin(xx * 0.0065 + yy * 0.0045 + 0.9)
        wave2 = 0.5 + 0.5 * np.cos(xx * 0.011 - yy * 0.008 + 2.1)
        neb = 0.6 * wave1 + 0.4 * wave2
        r = 28.0 + 18.0 * neb + rng.normal(0.0, 2.2, (ch, cw))
        g = 38.0 + 22.0 * neb + rng.normal(0.0, 2.2, (ch, cw))
        b = 60.0 + 34.0 * neb + rng.normal(0.0, 2.5, (ch, cw))
        rgb = np.stack([r, g, b], axis=-1).astype(np.float32)
        for _ in range(4000):
            sy = int(rng.integers(4, ch - 6))
            sx = int(rng.integers(4, cw - 6))
            br = float(rng.uniform(115.0, 240.0))
            sz = 2 if rng.random() < 0.70 else 3
            for k, mult in enumerate((0.92, 0.96, 1.04)):
                rgb[sy:sy + sz, sx:sx + sz, k] = np.maximum(rgb[sy:sy + sz, sx:sx + sz, k], min(255.0, br * mult))
        for _ in range(680):
            sy = int(rng.integers(6, ch - 8))
            sx = int(rng.integers(6, cw - 8))
            br = float(rng.uniform(190.0, 255.0))
            sz = int(rng.choice([4, 5, 6]))
            for k, mult in enumerate((0.92, 0.96, 1.0)):
                rgb[sy:sy + sz, sx:sx + sz, k] = np.maximum(rgb[sy:sy + sz, sx:sx + sz, k], br * mult)
        _STAR_CANVAS = np.clip(lift_navy(rgb), 28.0, 255.0)
    return _STAR_CANVAS


def starfield_frame(u: float, dx: float = 110.0, dy: float = 80.0) -> np.ndarray:
    canvas = get_star_canvas()
    ch, cw, _ = canvas.shape
    x0 = (cw - W) * 0.5 - dx * 0.5 + dx * u
    y0 = (ch - H) * 0.5 - dy * 0.5 + dy * u
    im = Image.fromarray(canvas.astype(np.uint8), "RGB")
    crop = im.transform((W, H), Image.Transform.EXTENT, (x0, y0, x0 + W, y0 + H), resample=Image.Resampling.BICUBIC)
    return np.asarray(crop, dtype=np.float32)


def composite_dark_onto_stars(rgb: np.ndarray, u: float, lo: float = 14.0, hi: float = 42.0) -> np.ndarray:
    """Blend pure-black space pixels cleanly onto a lifted-navy starfield so near_black==0 and
    top/bottom bands keep crisp natural star texture without altering the bright planet/rings."""
    stars = starfield_frame(u)
    lum = rgb.max(axis=2, keepdims=True)
    alpha = np.clip((lum - lo) / max(1.0, hi - lo), 0.0, 1.0)
    out = rgb * alpha + stars * (1.0 - alpha)
    return np.clip(lift_navy(out), 28.0, 255.0)


def pipe_frames(frames: list[Image.Image], dest: Path) -> None:
    proc = sp.Popen(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15",
            "-pix_fmt", "yuv420p", "-video_track_timescale", "24000", str(dest),
        ],
        stdin=sp.PIPE,
    )
    assert proc.stdin is not None
    for im in frames:
        proc.stdin.write(im.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"Failed encoding {dest}")


def decode_video_frames(src: Path, start_s: float, frames_n: int) -> list[Image.Image]:
    dur_s = frames_n / FPS + 0.15
    raw_dir = WORK / f"dec_{src.stem}_{int(round(start_s * 1000))}"
    if raw_dir.exists():
        shutil.rmtree(raw_dir)
    raw_dir.mkdir(parents=True)
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{start_s:.4f}", "-t", f"{dur_s:.4f}", "-i", str(src),
        "-vf", f"fps={FPS}", "-frames:v", str(frames_n),
        str(raw_dir / "f_%04d.png"),
    ])
    files = sorted(raw_dir.glob("f_*.png"))
    if len(files) < frames_n:
        while len(files) < frames_n:
            files.append(files[-1])
    out = [Image.open(p).convert("RGB") for p in files[:frames_n]]
    shutil.rmtree(raw_dir)
    return out


def render_parker_venus(shot: dict, dest: Path, open_f0: Path | None = None) -> float:
    frames_n = shot["f1"] - shot["f0"]
    raw_frames = decode_video_frames(shot["src_path"], float(shot["offset"]), frames_n)
    cx, cy, cw, ch = shot["crop_x"], shot["crop_y"], shot["crop_w"], shot["crop_h"]
    out_frames = []
    denom = float(max(1, frames_n - 1))
    for i, im in enumerate(raw_frames):
        u = i / denom
        # Subtle smooth horizontal follow as Venus swells
        crop = im.crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.Resampling.LANCZOS)
        crop = ImageEnhance.Color(crop).enhance(1.26)
        crop = ImageEnhance.Contrast(crop).enhance(1.12)
        crop = crop.filter(ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=2))
        arr = np.asarray(crop, dtype=np.float32)
        arr = composite_dark_onto_stars(arr, u * 0.45, lo=16.0, hi=46.0)
        res = Image.fromarray(arr.astype(np.uint8), "RGB")
        if open_f0 is not None and i == 0:
            res.save(open_f0)
        out_frames.append(res)
    pipe_frames(out_frames, dest)
    return float(shot["upscale"])


def render_sdo_transit(shot: dict, dest: Path) -> float:
    frames_n = shot["f1"] - shot["f0"]
    raw_frames = decode_video_frames(shot["src_path"], float(shot["offset"]), frames_n)
    cx, cy, cw, ch = shot["crop_x"], shot["crop_y"], shot["crop_w"], shot["crop_h"]
    out_frames = []
    denom = float(max(1, frames_n - 1))
    for i, im in enumerate(raw_frames):
        u = i / denom
        crop = im.crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.Resampling.LANCZOS)
        crop = ImageEnhance.Color(crop).enhance(1.24)
        crop = ImageEnhance.Contrast(crop).enhance(1.16)
        crop = crop.filter(ImageFilter.UnsharpMask(radius=1.4, percent=145, threshold=2))
        arr = np.asarray(crop, dtype=np.float32)
        arr = composite_dark_onto_stars(arr, 0.2 + 0.5 * u, lo=12.0, hi=36.0)
        out_frames.append(Image.fromarray(arr.astype(np.uint8), "RGB"))
    pipe_frames(out_frames, dest)
    return float(shot["upscale"])


def render_svs20390_uranus(shot: dict, dest: Path) -> float:
    frames_n = shot["f1"] - shot["f0"]
    raw_frames = decode_video_frames(shot["src_path"], float(shot["offset"]), frames_n)
    cy, ch, cw = float(shot["crop_y"]), float(shot["crop_h"]), float(shot["crop_w"])
    x0, x1 = float(shot["x0"]), float(shot["x1"])
    out_frames = []
    denom = float(max(1, frames_n - 1))
    for i, im in enumerate(raw_frames):
        u = i / denom
        cx = x0 + (x1 - x0) * u
        crop = im.transform(
            (W, H),
            Image.Transform.EXTENT,
            (cx, cy, cx + cw, cy + ch),
            resample=Image.Resampling.BICUBIC,
        )
        crop = ImageEnhance.Color(crop).enhance(1.18)
        crop = ImageEnhance.Contrast(crop).enhance(1.12)
        crop = crop.filter(ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=2))
        arr = np.asarray(crop, dtype=np.float32)
        arr = composite_dark_onto_stars(arr, 0.1 + 0.75 * u, lo=12.0, hi=38.0)
        out_frames.append(Image.fromarray(arr.astype(np.uint8), "RGB"))
    pipe_frames(out_frames, dest)
    return float(shot["upscale"])


def render_wispr_venus(shot: dict, dest: Path) -> float:
    frames_n = shot["f1"] - shot["f0"]
    raw_frames = decode_video_frames(shot["src_path"], float(shot["offset"]), frames_n)
    cx, cy, cw, ch = shot["crop_x"], shot["crop_y"], shot["crop_w"], shot["crop_h"]
    out_frames = []
    denom = float(max(1, frames_n - 1))
    for i, im in enumerate(raw_frames):
        u = i / denom
        # Smooth horizontal drift across WISPR Venus glowing limb
        dx = 38.0 * u
        crop = im.transform(
            (W, H),
            Image.Transform.EXTENT,
            (cx + dx, cy, cx + cw + dx, cy + ch),
            resample=Image.Resampling.BICUBIC,
        )
        crop = ImageEnhance.Color(crop).enhance(1.22)
        crop = ImageEnhance.Contrast(crop).enhance(1.16)
        crop = crop.filter(ImageFilter.UnsharpMask(radius=1.2, percent=135, threshold=2))
        arr = np.asarray(crop, dtype=np.float32)
        # Subtle warm amber-gold grade matching glowing Venus surface through clouds
        arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.14, 0, 255)
        arr[:, :, 1] = np.clip(arr[:, :, 1] * 1.02, 0, 255)
        arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.88, 0, 255)
        arr = composite_dark_onto_stars(arr, 0.3 + 0.55 * u, lo=16.0, hi=44.0)
        out_frames.append(Image.fromarray(arr.astype(np.uint8), "RGB"))
    pipe_frames(out_frames, dest)
    return float(shot["upscale"])


def render_still_push(shot: dict, dest: Path) -> float:
    frames_n = shot["f1"] - shot["f0"]
    im = Image.open(shot["src_path"]).convert("RGB")
    if "inner_crop" in shot:
        im = im.crop(shot["inner_crop"])
    im = ImageEnhance.Color(im).enhance(float(shot.get("sat", 1.22)))
    im = ImageEnhance.Contrast(im).enhance(float(shot.get("contrast", 1.12)))
    im = im.filter(ImageFilter.UnsharpMask(radius=1.3, percent=135, threshold=2))
    iw, ih = im.size
    # Largest 9:16 crop inside source
    if iw / ih >= W / H:
        base_h = float(ih)
        base_w = base_h * (W / H)
    else:
        base_w = float(iw)
        base_h = base_w * (H / W)

    cx = iw * float(shot.get("x_frac", 0.5))
    cy = ih * float(shot.get("y_frac", 0.5))
    z0, z1 = float(shot["z0"]), float(shot["z1"])
    space_lift = bool(shot.get("space_lift", True))

    out_frames = []
    denom = float(max(1, frames_n - 1))
    for i in range(frames_n):
        u = i / denom
        z = z0 + (z1 - z0) * u
        cw = base_w / z
        ch = base_h / z
        x0 = max(0.0, min(iw - cw, cx - cw * 0.5))
        y0 = max(0.0, min(ih - ch, cy - ch * 0.5))
        crop = im.transform(
            (W, H),
            Image.Transform.EXTENT,
            (x0, y0, x0 + cw, y0 + ch),
            resample=Image.Resampling.BICUBIC,
        )
        arr = np.asarray(crop, dtype=np.float32)
        if space_lift:
            arr = composite_dark_onto_stars(arr, u * 0.85, lo=16.0, hi=46.0)
        else:
            arr = np.clip(lift_navy(arr), 28.0, 255.0)
        out_frames.append(Image.fromarray(arr.astype(np.uint8), "RGB"))
    pipe_frames(out_frames, dest)
    return round(max(W / (base_w / z1), H / (base_h / z1)), 2)


def render_shot(shot: dict, dest: Path, open_f0: Path | None = None) -> float:
    kind = shot["kind"]
    if kind == "parker_venus":
        return render_parker_venus(shot, dest, open_f0=open_f0)
    if kind == "parker_venus_loop":
        up = render_parker_venus(shot, dest, open_f0=None)
        shutil.copy2(dest, WORK / "exports" / shot["source"])
        return up
    if kind == "sdo_transit":
        return render_sdo_transit(shot, dest)
    if kind == "svs20390_uranus":
        return render_svs20390_uranus(shot, dest)
    if kind == "wispr_venus":
        return render_wispr_venus(shot, dest)
    if kind == "still_push":
        return render_still_push(shot, dest)
    raise ValueError(f"Unknown shot kind: {kind}")


def build_voice_plan() -> tuple[list[dict], list[dict], float]:
    stt = json.loads(STT_JSON.read_text())
    raw_words = [w for w in stt["words"] if w.get("type", "word") == "word" and w.get("text", "").strip()]
    slices = []
    words = []
    local = VO_LEAD_S
    for si, (a, b) in enumerate(VO_SEGMENTS):
        dur_s = round(b - a, 3)
        seg_words = []
        for w in raw_words:
            if w["end"] <= a + 0.005 or w["start"] >= b - 0.005:
                continue
            s = round(w["start"] - a + local, 3)
            e = round(min(b, w["end"]) - a + local, 3)
            txt = w["text"].strip()
            if txt == "-224?":
                txt = "−224?"
            entry = {
                "text": txt,
                "w": txt,
                "s": s,
                "e": e,
                "start": s,
                "end": e,
                "seg_idx": si,
                "src_start": round(float(w["start"]), 3),
                "src_end": round(float(min(b, w["end"])), 3),
            }
            words.append(entry)
            seg_words.append(entry)
        slices.append({
            "seg_idx": si,
            "a": a,
            "b": b,
            "dur": dur_s,
            "local": round(local, 3),
            "local_end": round(local + dur_s, 3),
            "nonzero_source_offset": a > 0.0,
            "word_count": len(seg_words),
        })
        local = round(local + dur_s, 3)
        if si < len(VO_GAPS):
            local = round(local + VO_GAPS[si], 3)
    return slices, words, words[-1]["e"]


def make_hook(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(H * 0.072 / 0.72)
    if f.size > 126:
        f = ImageFont.truetype(FONT_BLACK, 126)
    while max(d.textlength(t, font=f) for t, _ in HOOK_ROWS) > W * 0.86:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 18
    y = 220
    boxes = []
    for t, c in HOOK_ROWS:
        boxes.append(centred(d, y, t, f, c, stroke=8))
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
        bb = centred(d, y, r, f, WHITE, stroke=8)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"title outside 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed, "joined": LONG_TITLE}


def make_teach(dest: Path, text: str) -> list[int]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.84)
    while d.textlength(text, font=f) > W * 0.84:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y1 - 96, text, f, YELLOW, stroke=7)
    pad = 20
    d.rounded_rectangle((bb[0] - pad, bb[1] - 10, bb[2] + pad, bb[3] + 10), radius=18, outline=(255, 224, 0, 235), width=4)
    if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
        raise SystemExit(f"teach pill outside 16:9 band: {text} {bb}")
    im.save(dest)
    return bb


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
        if len(cur) == 3 or re.search(r"[,.?!;]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else vo_end
        end = min(nxt, c[-1]["e"] + 0.30, vo_end)
        text = " ".join(x["w"] for x in c).rstrip(",.")
        if end <= TITLE_IN or start >= TITLE_OUT:
            if TITLE_IN < start < TITLE_OUT:
                continue
            if start < TITLE_OUT < end:
                start = TITLE_OUT
            if end - start >= 0.16 and start < vo_end:
                out.append({"text": text, "s": round(start, 2), "e": round(min(end, vo_end), 2)})
        else:
            if start < TITLE_IN - 0.05 and TITLE_IN - start >= 0.16:
                out.append({"text": text, "s": round(start, 2), "e": round(min(end, TITLE_IN), 2)})
            if end > TITLE_OUT + 0.05:
                out.append({"text": text, "s": round(max(start, TITLE_OUT), 2), "e": round(min(end, vo_end), 2)})
    return [c for c in out if c["e"] - c["s"] >= 0.16]


def srt_chunks_full(words: list[dict], vo_end: float) -> list[dict]:
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[,.?!;]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else vo_end
        end = min(nxt, c[-1]["e"] + 0.30, vo_end)
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
    im = ImageEnhance.Color(im).enhance(1.16)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    d = ImageDraw.Draw(im)
    size = 76
    while size < 134:
        trial = ImageFont.truetype(FONT_BLACK, size + 2)
        if max(d.textlength(r, font=trial) for r, _ in COVER_ROWS) > W * 0.80:
            break
        size += 2
    f = ImageFont.truetype(FONT_BLACK, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 18
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


def build_audio(work: Path, slices: list[dict], total: float) -> dict:
    """Slice VO using `atrim` STRICTLY BEFORE `afade` (prevents the J3918 post-input -ss bug!)."""
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
            "-af", (
                f"atrim=start={sl['a']:.4f}:end={sl['b']:.4f},"
                f"asetpts=PTS-STARTPTS,"
                f"afade=t=in:d=0.008,afade=t=out:st={max(0.0, seg - 0.008):.4f}:d=0.008"
            ),
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

    # Full-runtime score bed (continuous through loop seam)
    bed_raw = work / "stem_bed_raw.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", "12.0", "-t", f"{total:.3f}",
        "-i", str(BED_MP3),
        "-af", f"afade=t=in:d=0.08,afade=t=out:st={total - 0.25:.3f}:d=0.25",
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
        held = np.array([need[max(0, i - 3):min(m, i + 4)].max() for i in range(m)])
        duck[:m] = np.minimum(duck[:m] + held, 18)
        env = np.convolve(np.interp(T, grid, duck, left=0, right=0), np.ones(k) / k, mode="same")
        write_wav(bed * (10 ** (-env / 20))[:, None], bed_wav)

    hits = [
        ("whoosh", 0.00, -6.0),
        ("rumble", 0.15, -10.5),
        ("whoosh", 4.21, -9.0),
        ("tick", TITLE_IN, -8.5),
        ("tick", TEACH_IN, -8.5),
        ("rumble", 14.90, -10.0),
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
            sfx[i0:i1] += sample[:i1 - i0]
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


def verify_speech_coverage(out_vo_wav: Path, slices: list[dict]) -> dict:
    src = read_wav(VO_WAV).mean(axis=1)
    out = read_wav(out_vo_wav).mean(axis=1)
    seg_reports = []
    ok = True
    for sl in slices:
        s0, s1 = int(round(sl["a"] * SR)), int(round(sl["b"] * SR))
        o0 = int(round(sl["local"] * SR))
        n = min(s1 - s0, len(out) - o0)
        a_src = src[s0:s0 + n]
        a_out = out[o0:o0 + n]
        win = int(0.20 * SR)
        active = covered = 0
        for pos in range(0, n - win, win):
            r_src = float(np.sqrt(np.mean(a_src[pos:pos + win] ** 2)))
            r_out = float(np.sqrt(np.mean(a_out[pos:pos + win] ** 2)))
            if 20 * math.log10(max(r_src, 1e-6)) > -42.0:
                active += 1
                if 20 * math.log10(max(r_out, 1e-6)) > -42.0:
                    covered += 1
        cov = round(covered / max(1, active), 4)
        seg_ok = cov >= 0.99
        if not seg_ok:
            ok = False
        seg_reports.append({
            "seg_idx": sl["seg_idx"],
            "src_window": [sl["a"], sl["b"]],
            "out_window": [sl["local"], sl["local_end"]],
            "active_windows": active,
            "covered_windows": covered,
            "coverage": cov,
            "pass": seg_ok,
        })
    return {"pass": ok, "segments": seg_reports}


def copy_verified(src: Path, dst: Path) -> None:
    if dst.exists():
        raise SystemExit(f"Refusing to overwrite existing NAS file: {dst}")
    shutil.copy2(src, dst)
    if sha256(src) != sha256(dst):
        raise SystemExit(f"SHA-256 mismatch copying {src} -> {dst}")


def main() -> None:
    if (NAS_SUB_OUT / f"{STEM}.mp4").exists() or (NAS_SHORTS / f"{STEM}.mp4").exists():
        raise SystemExit(f"Target {STEM}.mp4 already exists on NAS; bump version.")

    # Verify all input hashes
    verified_hashes = {}
    bed_sha = sha256(BED_MP3)
    assert bed_sha == EXPECTED_BED_SHA256, f"Bed sha mismatch: {bed_sha}"
    vo_sha = sha256(VO_WAV)
    verified_hashes[VO_WAV.name] = vo_sha
    verified_hashes[BED_MP3.name] = bed_sha
    for p, exp in EXPECTED_SHA256.items():
        assert p.exists(), f"Missing source: {p}"
        got = sha256(p)
        assert got.startswith(exp), f"SHA mismatch for {p.name}: {got} != {exp}..."
        verified_hashes[p.name] = got
    print("Verified all source SHA-256 hashes.", flush=True)

    # Verify shot continuity
    assert SHOT_PLAN[0]["f0"] == 0 and SHOT_PLAN[-1]["f1"] == TOTAL_FRAMES
    for a, b in zip(SHOT_PLAN, SHOT_PLAN[1:]):
        assert a["f1"] == b["f0"], f"Non-contiguous shot boundary: {a['row']} -> {b['row']}"

    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    OUT_WORK = WORK / "exports"
    OUT_WORK.mkdir(parents=True)

    slices, words, last_word_end = build_voice_plan()
    joined = " ".join(w["w"] for w in words)
    print(f"Spoken words: {len(words)} | VO: {words[0]['s']:.3f}-{last_word_end:.3f} s | Total: {TOTAL_S:.3f} s ({TOTAL_FRAMES}f @ {FPS}fps)", flush=True)

    # Verify zero spoken words split across cut boundaries
    for shot in SHOT_PLAN[:-1]:
        cut_t = shot["f1"] / FPS
        for w in words:
            if w["s"] + 0.005 < cut_t < w["e"] - 0.005:
                raise SystemExit(f"Cut at {cut_t:.3f}s (after {shot['row']}) splits word {w['w']!r} ({w['s']:.3f}-{w['e']:.3f}s)")
    print(f"Verified 0 spoken words split across all {len(SHOT_PLAN) - 1} cut boundaries.", flush=True)

    open_f0 = WORK / "open_f0.png"
    concat_lines = []
    cuts_meta = []
    pool_meta = []
    seen_sources = set()

    for idx, shot in enumerate(SHOT_PLAN):
        piece = WORK / f"piece_{idx:02d}.mp4"
        up = render_shot(shot, piece, open_f0 if idx == 0 else None)
        concat_lines.append(f"file '{piece.name}'")
        t_in = round(shot["f0"] / FPS, 3)
        t_out = round(shot["f1"] / FPS, 3)
        cuts_meta.append({
            "row": shot["row"],
            "timeline_in": t_in,
            "timeline_out": t_out,
            "source": shot["source"],
            "upscale": up,
            "video": bool(shot["video"]),
            "framing": (
                {"offset": shot.get("offset", 0.0), "crop": "9:16 full-bleed", "mode": "cover"}
                if shot["video"]
                else {"crop": "9:16 full-bleed", "mode": "cover"}
            ),
        })
        if shot["source"] not in seen_sources:
            seen_sources.add(shot["source"])
            pool_meta.append({
                "id": Path(shot["source"]).stem,
                "file": shot["source"],
                "file_id": shot["source"],
                "source": shot["source"],
                "title": shot["title"],
            })
        print(f"  rendered {shot['row']:8s} ({t_in:6.3f}-{t_out:6.3f} s, {shot['f1']-shot['f0']:3d}f) upscale={up}", flush=True)

    (WORK / "list.txt").write_text("\n".join(concat_lines) + "\n")
    pic_mp4 = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"), "-c", "copy", str(pic_mp4)])

    hook_info = make_hook(WORK / "hook.png")
    title_info = make_title(WORK / "title.png")
    teach_bb = make_teach(WORK / "teach.png", TEACH_TEXT)
    caps = caption_chunks(words, last_word_end)
    for i, c in enumerate(caps):
        c["bbox"] = make_caption(WORK / f"cap_{i:02d}.png", c["text"])

    aud = build_audio(WORK, slices, TOTAL_S)
    cov_report = verify_speech_coverage(WORK / "stem_vo.wav", slices)
    assert cov_report["pass"], f"Speech coverage failed: {cov_report}"
    print("Speech coverage verification: PASS across all 6 segments.", flush=True)

    cal_wav, aac_i, aac_tp = calibrate_aac_wav(WORK, WORK / "mix.wav", TOTAL_S)
    aud["aac_lufs"] = aac_i
    aud["aac_tp_dbtp"] = aac_tp

    final_mp4 = OUT_WORK / f"{STEM}.mp4"
    inputs = ["-t", f"{TOTAL_S:.3f}", "-i", str(pic_mp4)]
    for name in ("hook.png", "title.png", "teach.png"):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL_S:.3f}", "-i", str(WORK / name)]
    inputs += ["-i", str(cal_wav)]
    base_idx = 5
    for i in range(len(caps)):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL_S:.3f}", "-i", str(WORK / f"cap_{i:02d}.png")]

    fc = [
        f"[0:v]fps={FPS},setsar=1,format=yuv420p[v0]",
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='gte(t,0)*lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.25:alpha=1,fade=t=out:st={TITLE_OUT - 0.25:.2f}:d=0.25:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
        f"[3:v]format=rgba,fade=t=in:st={TEACH_IN}:d=0.22:alpha=1,fade=t=out:st={TEACH_OUT - 0.22:.2f}:d=0.22:alpha=1[th]",
        f"[v2][th]overlay=0:0:enable='gte(t,{TEACH_IN})*lt(t,{TEACH_OUT})'[v3]",
    ]
    last_v = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last_v}][{base_idx + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last_v = f"c{i}"
    fc.append(f"[{last_v}]noise=alls=2:allf=t,format=yuv420p[v]")

    run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", ";".join(fc),
        "-map", "[v]", "-map", "4:a",
        *shorts_encode_args(fps=FPS),
        "-t", f"{TOTAL_S:.3f}", str(final_mp4),
    ])

    words_path = OUT_WORK / f"{STEM}_words.json"
    transcript_path = OUT_WORK / f"{STEM}_transcript.txt"
    srt_path = OUT_WORK / f"{STEM}_en-GB.srt"
    cuts_path = OUT_WORK / f"{STEM}_cuts.json"
    pool_path = OUT_WORK / f"{STEM}_pool.json"
    meta_path = OUT_WORK / f"{STEM}_meta.json"
    cov_path = OUT_WORK / f"{STEM}_vo_coverage.json"
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
    cov_path.write_text(json.dumps(cov_report, indent=2) + "\n")

    # Find payoff onset ("traps")
    payoff_s = next(w["s"] for w in words if w["w"].lower().startswith("traps"))
    s1_s2_breath = round(slices[2]["local"] - slices[1]["local_end"], 3)
    s2_s3_breath = round(slices[4]["local"] - slices[3]["local_end"], 3)

    meta_obj = {
        "slug": SHORT_SLUG,
        "stem": STEM,
        "title": SHORT_TITLE,
        "air_date": AIR_DATE,
        "test_a": False,
        "relatedVideoId": None,
        "parent_long_film": "OWB:064",
        "parent_long_title": LONG_TITLE,
        "locked_script_v03_sha256": "634da1601232b9b8debb1880203228c4b98c95c354ae21711797f176e0c80ca0",
        "vo_take_stem": "064_short02_venus_vs_uranus_vo_v01",
        "vo_take_wav_sha256": vo_sha,
        "spoken": joined,
        "vo_onset_s": words[0]["s"],
        "last_word_end_s": last_word_end,
        "payoff_onset_s": payoff_s,
        "payoff_pct": round(100.0 * payoff_s / TOTAL_S, 1),
        "duration_s": TOTAL_S,
        "fps": FPS,
        "hook": {"text": hook_info["text"], "start_s": 0.0, "end_s": HOOK_END},
        "hook_caption": {"text": hook_info["text"], "start_s": 0.0, "end_s": HOOK_END},
        "title_banner": {"text": LONG_TITLE, "start_s": TITLE_IN, "end_s": TITLE_OUT},
        "teach_overlay": {"text": TEACH_TEXT, "start_s": TEACH_IN, "end_s": TEACH_OUT, "bbox": teach_bb},
        "end_card": None,
        "words_file": str(words_path),
        "vo": str(vo_stem_out),
        "audio": aud,
    }
    meta_path.write_text(json.dumps(meta_obj, indent=2) + "\n")

    frame0_jpg = OUT_WORK / f"{STEM}_frame0.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.00", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(frame0_jpg)])
    cover_jpg = OUT_WORK / f"{STEM}_cover.jpg"
    cover_info = make_cover(cover_jpg, open_f0)

    # Build 8-shot inspection contact sheet (midpoint of every shot)
    shot_tiles = []
    for idx, shot in enumerate(SHOT_PLAN):
        mid_t = round(((shot["f0"] + shot["f1"]) / 2.0) / FPS, 2)
        raw_t = sp.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{mid_t:.2f}", "-i", str(final_mp4),
            "-frames:v", "1", "-vf", "scale=360:640", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
        ])
        im_t = Image.frombytes("RGB", (360, 640), raw_t)
        d_t = ImageDraw.Draw(im_t)
        d_t.rectangle((0, 0, 360, 32), fill=(0, 0, 0))
        d_t.text((8, 8), f"{idx + 1:02d} {shot['row']} ({mid_t:.2f}s)", fill=(255, 255, 255))
        shot_tiles.append(im_t)
    cols_s = 4
    rows_s = (len(shot_tiles) + cols_s - 1) // cols_s
    sheet_8 = Image.new("RGB", (360 * cols_s, 640 * rows_s), (18, 22, 30))
    for idx, im_t in enumerate(shot_tiles):
        sheet_8.paste(im_t, ((idx % cols_s) * 360, (idx // cols_s) * 640))
    sheet_8_path = OUT_WORK / f"{STEM}_review_8shots.jpg"
    sheet_8.save(sheet_8_path, quality=92)

    # Run all 7 gates on local scratch master first
    g_txt = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", final_mp4, "--air-date", AIR_DATE, "--sheet-dir", OUT_WORK])
    g_json = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", final_mp4, "--air-date", AIR_DATE, "--sheet-dir", OUT_WORK, "--json"])
    (OUT_WORK / f"{STEM}_gate.txt").write_text((g_txt.stdout or "") + (g_txt.stderr or ""))
    (OUT_WORK / f"{STEM}_gate.json").write_text(g_json.stdout or g_json.stderr)
    print(g_txt.stdout, end="", flush=True)
    if g_txt.stderr:
        print(g_txt.stderr, end="", flush=True)

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
        sys.executable, REPO / "scripts/music_gate.py", NAS_064,
        "--bed", BED_MP3, "--video", final_mp4,
        "--out", OUT_WORK / f"{STEM}_music_gate.json",
    ])
    (OUT_WORK / f"{STEM}_music_gate.txt").write_text((mg_res.stdout or "") + (mg_res.stderr or ""))
    print(mg_res.stdout, end="", flush=True)

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
        "polish_gate_rc": pg_res.returncode,
        "picture_qa_rc": pqa_res.returncode,
    }
    print("GATES:", json.dumps(gates, indent=2), flush=True)
    if any(v != 0 for v in gates.values()):
        raise SystemExit(1)

    # Update meta paths to canonical NAS paths before copying to NAS
    meta_obj["words_file"] = str(NAS_SUB_OUT / f"{STEM}_words.json")
    meta_obj["vo"] = str(NAS_SUB_OUT / f"{STEM}_vo.wav")
    meta_path.write_text(json.dumps(meta_obj, indent=2) + "\n")
    cover_info["file"] = str(NAS_SUB_OUT / f"{STEM}_cover.jpg")

    open_sheet_path = OUT_WORK / f"{STEM}_open_sheet.jpg"
    summary = {
        "stem": STEM,
        "mp4_path": str(NAS_SUB_OUT / f"{STEM}.mp4"),
        "mp4_sha256": sha256(final_mp4),
        "vo_stem_sha256": sha256(vo_stem_out),
        "bed_stem_sha256": sha256(bed_stem_out),
        "sfx_stem_sha256": sha256(sfx_stem_out),
        "srt_sha256": sha256(srt_path),
        "frame0_jpg_sha256": sha256(frame0_jpg),
        "cover_jpg_sha256": sha256(cover_jpg),
        "open_sheet_sha256": sha256(open_sheet_path),
        "review_8shots_sha256": sha256(sheet_8_path),
        "source_hashes": verified_hashes,
        "duration_s": TOTAL_S,
        "fps": FPS,
        "frames": TOTAL_FRAMES,
        "words_count": len(words),
        "vo_onset_s": words[0]["s"],
        "s1_s2_breath_s": s1_s2_breath,
        "s2_s3_breath_s": s2_s3_breath,
        "payoff_onset_s": payoff_s,
        "payoff_pct": round(100.0 * payoff_s / TOTAL_S, 1),
        "last_word_end_s": last_word_end,
        "tail_gap_s": round(TOTAL_S - last_word_end, 3),
        "cut1_s": round(SHOT_PLAN[0]["f1"] / FPS, 3),
        "cut2_s": round(SHOT_PLAN[1]["f1"] / FPS, 3),
        "max_shot_s": max(round((s["f1"] - s["f0"]) / FPS, 3) for s in SHOT_PLAN),
        "audio": aud,
        "speech_coverage": cov_report,
        "hook": hook_info,
        "title": title_info,
        "teach": {"text": TEACH_TEXT, "in": TEACH_IN, "out": TEACH_OUT, "bbox": teach_bb},
        "cover": cover_info,
        "gates": gates,
    }
    summary_path = OUT_WORK / f"{STEM}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")

    # Copy all verified outputs to NAS_SUB_OUT with SHA-256 verification
    NAS_SUB_OUT.mkdir(parents=True, exist_ok=True)
    for item in sorted(OUT_WORK.iterdir()):
        if item.is_dir():
            dst_dir = NAS_SUB_OUT / item.name
            dst_dir.mkdir(parents=True, exist_ok=True)
            for sub in sorted(item.iterdir()):
                if sub.is_file():
                    copy_verified(sub, dst_dir / sub.name)
        elif item.is_file():
            copy_verified(item, NAS_SUB_OUT / item.name)

    # Re-run gate_shorts_open, polish_gate, and picture_qa on canonical NAS copy so reports record NAS paths
    nas_mp4 = NAS_SUB_OUT / f"{STEM}.mp4"
    g_nas_txt = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", nas_mp4, "--air-date", AIR_DATE, "--sheet-dir", NAS_SUB_OUT])
    g_nas_json = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", nas_mp4, "--air-date", AIR_DATE, "--sheet-dir", NAS_SUB_OUT, "--json"])
    if g_nas_txt.returncode != 0:
        raise SystemExit(f"NAS gate_shorts_open failed: {g_nas_txt.stdout}\n{g_nas_txt.stderr}")
    (NAS_SUB_OUT / f"{STEM}_gate.txt").write_text((g_nas_txt.stdout or "") + (g_nas_txt.stderr or ""))
    (NAS_SUB_OUT / f"{STEM}_gate.json").write_text(g_nas_json.stdout or g_nas_json.stderr)

    pg_nas = run_gate([sys.executable, REPO / "scripts/polish_gate.py", nas_mp4, "--cuts", NAS_SUB_OUT / f"{STEM}_cuts.json", "--out", NAS_SUB_OUT / f"{STEM}_polish_gate.json"])
    if pg_nas.returncode != 0:
        raise SystemExit(f"NAS polish_gate failed: {pg_nas.stdout}\n{pg_nas.stderr}")
    (NAS_SUB_OUT / f"{STEM}_polish_gate.txt").write_text((pg_nas.stdout or "") + (pg_nas.stderr or ""))

    pqa_nas = run_gate([sys.executable, REPO / "scripts/picture_qa.py", nas_mp4, "--cuts", NAS_SUB_OUT / f"{STEM}_cuts.json", "--pool", NAS_SUB_OUT / f"{STEM}_pool.json", "--out-dir", NAS_SUB_OUT / f"{STEM}_picture_qa"])
    if pqa_nas.returncode != 0:
        raise SystemExit(f"NAS picture_qa failed: {pqa_nas.stdout}\n{pqa_nas.stderr}")
    (NAS_SUB_OUT / f"{STEM}_picture_qa.txt").write_text((pqa_nas.stdout or "") + (pqa_nas.stderr or ""))

    # Mirror primary export and key sidecars into NAS 10_Shorts/ root with SHA-256 verification
    for name in (
        f"{STEM}.mp4",
        f"{STEM}_frame0.jpg",
        f"{STEM}_cover.jpg",
        f"{STEM}_frame0_preview.jpg",
        f"{STEM}_cover_preview.jpg",
        f"{STEM}_open_sheet.jpg",
        f"{STEM}_review_8shots.jpg",
        f"{STEM}_meta.json",
        f"{STEM}_words.json",
        f"{STEM}_transcript.txt",
        f"{STEM}_cuts.json",
        f"{STEM}_pool.json",
        f"{STEM}_gate.txt",
        f"{STEM}_gate.json",
        f"{STEM}_summary.json",
    ):
        copy_verified(NAS_SUB_OUT / name, NAS_SHORTS / name)

    print(f"NAS copies verified by SHA-256: {NAS_SUB_OUT / (STEM + '.mp4')} ({summary['mp4_sha256']})", flush=True)


if __name__ == "__main__":
    main()
