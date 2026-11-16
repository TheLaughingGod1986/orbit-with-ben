#!/usr/bin/env python3
"""032 Titan — Active Short #2 v02 Assembler (J0979, Test A Opening Short).

Full-bleed 1080x1920 (9:16), 30 fps CFR. Zero centre-band blur pad, zero integer
star-crop push jitter, zero corner halo, zero barred RLSJm59OSzI assets.
Leaves all _v01 files on the NAS untouched.

Title: Could You Survive Stepping Onto Saturn's Moon Titan?
Slug / Stem: fri27_opening_testA / 032_short_fri27_opening_testA_v02
Target Reserve Slot: Fri 27 Nov 2026 11:30Z (after 032 long T3cBBss1F60 goes public Wed 25 Nov 18:00Z)
Parent Long (032): What Would Happen If You Landed on Titan? (Seas of Liquid Gas) [T3cBBss1F60]

Lifts verbatim opening sentences s01-s05 (0.140-31.600 s, 91 spoken words) from locked
master VO `02_Voiceover/titan_landing_vo_v02b.wav` with tightened <0.25 s inter-sentence
breaths (30.000 s total runtime, 900 frames at 30 fps CFR).
£0 spend, zero YouTube upload.
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
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "032_What-Would-Happen-If-You-Landed-On-Titan"
)
NAS_HARV = NAS_FILM / "03_Reference-Material" / "harvest_J2089_v01"
NAS_SVS = NAS_HARV / "svs_20311"
NAS_SHORTS = NAS_FILM / "10_Shorts"
NAS_SUB_OUT = NAS_SHORTS / "fri27_opening_testA" / "06_Final-Exports"

MASTER_V02 = NAS_FILM / "09_Final-Export" / "032_what_would_happen_if_you_landed_on_titan_master_v02.mp4"
EXPECTED_MASTER_SHA256 = "519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073"
VO_WAV = NAS_FILM / "02_Voiceover" / "titan_landing_vo_v02b.wav"
EXPECTED_VO_SHA256 = "55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5"
STT_JSON = NAS_FILM / "02_Voiceover" / "stt" / "titan_landing_vo_v02b" / "stt_raw.json"
BED_MP3 = NAS_FILM / "05_Music" / "titan_score_bed_v01.mp3"
EXPECTED_BED_SHA256 = "02c7d95865f8b39de4f9d3dfda8aa85084ecea04fc56dbd6776268279dab8f9e"
KIT_DIR = NAS_FILM / "06_Sound-Effects" / "kit_v01"

DESK = Path("/Users/ben/_desk") if Path("/Users/ben/_desk").exists() else Path("/Users/benjaminoats/_desk")
WORK = DESK / "scratch" / "J0979_032_short_v02"

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import gate_shorts_open as gso  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 30
SR = 48000
BAND_H = round(W * 9 / 16)          # 608 px (safe zone for title/teach overlays only; picture is full 1080x1920)
BAND_Y0 = (H - BAND_H) // 2         # 656 px
BAND_Y1 = BAND_Y0 + BAND_H          # 1264 px
LINE_H = round(BAND_H * 0.115)      # 70 px

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)         # #FFE000
CYAN = (110, 225, 250, 255)
NAVY_FLOOR = np.array([28.0, 38.0, 58.0], dtype=np.float32)

STEM = "032_short_fri27_opening_testA_v02"
SHORT_SLUG = "fri27_opening_testA"
SHORT_TITLE = "Could You Survive Stepping Onto Saturn's Moon Titan?"
ALT_TITLE = "What Would Happen If You Landed on Titan?"
AIR_DATE = "2026-11-27"
LONG_ID = "T3cBBss1F60"
LONG_TITLE = "What Would Happen If You Landed on Titan? (Seas of Liquid Gas)"

TITLE_ROWS = [
    "What Would Happen",
    "If You Landed on Titan?",
    "(Seas of Liquid Gas)",
]
END_CARD_LINE = "Full film on the channel"
END_ROWS = [
    ("What Would Happen", WHITE),
    ("If You Landed on Titan?", WHITE),
    ("(Seas of Liquid Gas)", WHITE),
    (END_CARD_LINE, YELLOW),
]
HOOK_ROWS = [("STEP OUT", WHITE), ("ON TITAN?", YELLOW)]
COVER_ROWS = [("SURVIVE ON", WHITE), ("TITAN?", YELLOW)]

HOOK_END = 2.10
TITLE_IN, TITLE_OUT = 9.00, 14.00
TEACH_IN, TEACH_OUT = 16.55, 19.55
TEACH_TEXT = "1.47 BAR (1.5× EARTH)"

# Verbatim s01-s05 from titan_landing_vo_v02b.wav (91 spoken words), tightened breaths < 0.25 s:
# s01: 0.160 - 5.240
# s02: 6.380 - 9.360
# s03: 10.060 - 22.500
# s04: 23.340 - 25.220
# s05: 26.300 - 31.580
VO_SEGMENTS = [
    (0.140, 5.260),
    (6.360, 9.380),
    (10.040, 22.520),
    (23.320, 25.240),
    (26.280, 31.600),
]
VO_LEAD_S = 0.11
VO_GAPS = [0.19, 0.22, 0.22, 0.23]
TOTAL_S = 30.000              # 900 frames at 30 fps CFR
END_CARD_IN = 28.933          # 1.067 s loop/end card tail after last word (~28.81 s)

# 12-shot full-bleed 9:16 cut plan (every cut on an exact 30fps frame inside a verified word silence gap;
# Cut 1 = 2.467 s <= 2.80 s, Cut 2 = 4.100 s <= 4.80 s, max shot = 3.700 s <= 4.00 s;
# zero barred RLSJm59OSzI assets [PIA14925, PIA06230, PIA09739, PIA21625]).
SHOT_PLAN = [
    {
        "row": "R01a",
        "in": 0.000,
        "out": 2.467,
        "kind": "svs_pan",
        "source": "SVS20311_DF_End_Pan_1080.mp4",
        "title": "Dragonfly Over Titan Dunes Flight Pan (SVS 20311)",
        "offset": 2.20,
        "video": True,
        "x0_start": 620.0,
        "x0_end": 780.0,
    },
    {
        "row": "R01b",
        "in": 2.467,
        "out": 4.100,
        "kind": "still_orb",
        "source": "PIA14922.jpg",
        "title": "Colorful Colossuses: Titan Beside Ringed Saturn",
        "video": False,
        "orb_scale": 0.90,
        "z1": 1.045,
    },
    {
        "row": "R01c",
        "in": 4.100,
        "out": 6.900,
        "kind": "still_cover",
        "source": "SVS20311_Dragonfly_Landed_Closeup.png",
        "title": "Dragonfly Rotorcraft Landed on Titan Surface (SVS 20311)",
        "video": False,
        "pan_x_frac": 0.50,
        "z1": 1.048,
        "boost_sat": 1.22,
    },
    {
        "row": "R02b",
        "in": 6.900,
        "out": 8.533,
        "kind": "svs_pan",
        "source": "SVS20311_DF_Intake_shot_1080.mp4",
        "title": "Dragonfly Sample Intake on Titan Surface (SVS 20311)",
        "offset": 0.50,
        "video": True,
        "x0_start": 560.0,
        "x0_end": 700.0,
    },
    {
        "row": "R03a",
        "in": 8.533,
        "out": 11.633,
        "kind": "still_cover",
        "source": "PIA22766.jpg",
        "title": "Cassini Grand Finale: Backlit Saturn and Rings",
        "video": False,
        "pan_x_frac": 0.56,
        "z1": 1.048,
        "star_dark": True,
    },
    {
        "row": "R03b",
        "in": 11.633,
        "out": 14.733,
        "kind": "still_orb",
        "source": "PIA20016.jpg",
        "title": "Peering Through Titan Haze (Cassini ISS)",
        "video": False,
        "orb_scale": 0.84,
        "z1": 1.048,
    },
    {
        "row": "R03c",
        "in": 14.733,
        "out": 16.433,
        "kind": "svs_pan",
        "source": "SVS20311_DF_Open_1080.mp4",
        "title": "Dragonfly Flight and Rotor Spin-Up on Titan (SVS 20311)",
        "offset": 19.60,
        "video": True,
        "x0_start": 520.0,
        "x0_end": 660.0,
    },
    {
        "row": "R03d",
        "in": 16.433,
        "out": 19.700,
        "kind": "pressure_gauge",
        "source": "code_graphic_032_r03_pressure_9x16_v02.mp4",
        "title": "Earth 1.0 bar vs Titan 1.47 bar Atmospheric Pressure Gauge (032 R03)",
        "offset": 0.0,
        "video": True,
    },
    {
        "row": "R04a",
        "in": 19.700,
        "out": 23.400,
        "kind": "still_cover",
        "source": "PIA21434.jpg",
        "title": "Titan Kraken and Ligeia Seas in Sharper Focus (Cassini VIMS)",
        "video": False,
        "pan_x_frac": 0.50,
        "z1": 1.048,
        "star_dark": True,
        "warm_tint": True,
    },
    {
        "row": "R04b",
        "in": 23.400,
        "out": 25.833,
        "kind": "still_cover",
        "source": "PIA12621.jpg",
        "title": "West of the Probe: Cassini ISS View of Adiri on Titan",
        "video": False,
        "pan_x_frac": 0.50,
        "z1": 1.032,
        "warm_tint": True,
    },
    {
        "row": "R04c",
        "in": 25.833,
        "out": 28.933,
        "kind": "svs_pan",
        "source": "SVS20311_Dragonfly_Drill_1080.mp4",
        "title": "Dragonfly Surface Sampling Drill on Titan (SVS 20311)",
        "offset": 2.00,
        "video": True,
        "x0_start": 540.0,
        "x0_end": 720.0,
    },
    {
        "row": "R01_loop",
        "in": 28.933,
        "out": 30.000,
        "kind": "loop_return",
        "source": "frame0_return_032_short_fri27_opening_testA_v02.mp4",
        "raw_source": "SVS20311_DF_End_Pan_1080.mp4",
        "title": "Opening frame return for seamless loop",
        "offset": 0.0,
        "raw_offset": 1.133,
        "video": True,
        "x0_start": 546.0,
        "x0_end": 620.0,
    },
]

BARRED_ASSETS = {"PIA14925", "PIA06230", "PIA09739", "PIA21625"}


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


_STAR_BG: np.ndarray | None = None


def get_clean_starfield() -> np.ndarray:
    """Build a uniform, halo-free 1080x1920 deep-field starfield from the pure outer
    top-left (0, 0, 360, 640) corner of weic2310a.png plus crisp pinpoint stars."""
    global _STAR_BG
    if _STAR_BG is None:
        raw = Image.open(NAS_HARV / "weic2310a.png").convert("RGB")
        # Pure outer corner (max pixel = 25, zero Uranus ring glow)
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
    p = NAS_HARV / name
    if p.exists():
        return p
    p2 = NAS_SVS / name
    if p2.exists():
        return p2
    raise FileNotFoundError(f"Missing asset on NAS: {name}")


def build_base_9x16_cover(shot: dict) -> tuple[Image.Image, float]:
    src = resolve_asset_path(shot["source"])
    im = Image.open(src).convert("RGB")
    if shot.get("warm_tint"):
        a = np.asarray(im, dtype=np.float32)
        g = a.mean(axis=2)
        a = np.stack([g * 1.08 + 18.0, g * 0.88 + 12.0, g * 0.66 + 16.0], axis=-1)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if shot.get("boost_sat"):
        im = ImageEnhance.Color(im).enhance(float(shot["boost_sat"]))
        im = ImageEnhance.Contrast(im).enhance(1.08)

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
    crop = crop.filter(ImageFilter.UnsharpMask(radius=1.6, percent=125, threshold=2))
    arr = np.asarray(crop, dtype=np.float32)
    if shot.get("star_dark"):
        st = get_clean_starfield()
        luma = arr.max(axis=2, keepdims=True)
        m_dark = np.clip((52.0 - luma) / 32.0, 0.0, 1.0)
        arr = arr * (1.0 - m_dark) + st * m_dark
    arr = lift_navy(arr)
    z1 = float(shot.get("z1", 1.045))
    up = round((H / ch) * z1, 2)
    return Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8)), up


def build_base_9x16_orb(shot: dict) -> tuple[Image.Image, float]:
    """Composite a square NASA planet/moon plate seamlessly over the clean deep-field
    starfield with soft circular/dark-space feathering so zero rectangular edges exist."""
    src = resolve_asset_path(shot["source"])
    im = Image.open(src).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.18)
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
    """Symmetric sub-pixel centre zoom (1.000 -> z1) on a single unified 1080x1920 image:
    produces 0.000 px off-trend in polish_gate.jitter() and 0% padded frames."""
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


def make_globe_rgba(path: Path, diameter: int) -> Image.Image:
    im = Image.open(path).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.18)
    side = min(im.size)
    left, top = (im.width - side) // 2, (im.height - side) // 2
    im = im.crop((left, top, left + side, top + side)).resize((diameter, diameter), Image.Resampling.LANCZOS)
    circle = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(circle).ellipse((2, 2, diameter - 3, diameter - 3), fill=255)
    circle = circle.filter(ImageFilter.GaussianBlur(1.5))
    out = im.convert("RGBA")
    out.putalpha(circle)
    ImageDraw.Draw(out).ellipse(
        (2, 2, diameter - 3, diameter - 3), outline=(200, 225, 255, 175), width=max(2, diameter // 85)
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


def render_pressure_gauge(frames_n: int, dest: Path) -> float:
    """Native 1080x1920 single Teach-on-Screen number object: real Apollo 17 Blue Marble
    Earth (1.00 bar) vs real Cassini Titan (building to 1.47 bar = 1.5x Earth), over clean
    halo-free starfield."""
    g_earth = make_globe_rgba(resolve_asset_path("AS17-148-22727.jpg"), 310)
    g_titan = make_globe_rgba(resolve_asset_path("PIA20016.jpg"), 310)
    f_head = ImageFont.truetype(FONT_BLACK, 46)
    f_val = ImageFont.truetype(FONT_BOLD, 42)
    bg_base = Image.fromarray(get_clean_starfield().astype(np.uint8)).convert("RGBA")

    bar_x0, bar_x1 = 150, 930
    bar_max_w = bar_x1 - bar_x0  # corresponds to 1.80 bar full scale
    earth_fill_w = round(bar_max_w * (1.00 / 1.80))

    frames = []
    denom = float(max(1, frames_n - 1))
    for i in range(frames_n):
        u = i / denom
        ease = 0.5 - 0.5 * math.cos(math.pi * min(1.0, u / 0.72))
        titan_bar = 1.47 * ease
        titan_fill_w = max(8, round(bar_max_w * (titan_bar / 1.80)))

        # Subtle slow zoom on starfield so video clip moves smoothly
        z = 1.0 + 0.03 * u
        cw, ch = W / z, H / z
        l, t = (W - cw) * 0.5, (H - ch) * 0.5
        fg = bg_base.transform((W, H), Image.Transform.EXTENT, (l, t, l + cw, t + ch), resample=Image.Resampling.BICUBIC)
        fg.alpha_composite(g_earth, (150, 210))
        fg.alpha_composite(g_titan, (150, 690))

        d = ImageDraw.Draw(fg)
        d.text((500, 295), "EARTH AIR", font=f_head, fill=CYAN, stroke_width=5, stroke_fill=(16, 26, 46, 255))
        d.text((500, 360), "1.00 BAR", font=f_val, fill=WHITE, stroke_width=4, stroke_fill=(16, 26, 46, 255))
        d.rounded_rectangle((bar_x0, 555, bar_x1, 595), radius=14, outline=(160, 190, 225, 190), width=3)
        d.rounded_rectangle((bar_x0, 555, bar_x0 + earth_fill_w, 595), radius=14, fill=CYAN)

        d.text((500, 775), "TITAN SKY", font=f_head, fill=YELLOW, stroke_width=5, stroke_fill=(16, 26, 46, 255))
        d.text((500, 840), f"{titan_bar:.2f} BAR", font=f_val, fill=WHITE, stroke_width=4, stroke_fill=(16, 26, 46, 255))
        d.rounded_rectangle((bar_x0, 1035, bar_x1, 1075), radius=14, outline=(160, 190, 225, 190), width=3)
        d.rounded_rectangle((bar_x0, 1035, bar_x0 + titan_fill_w, 1075), radius=14, fill=YELLOW)

        frames.append(fg.convert("RGB"))
    pipe_frames(frames, dest)
    return 1.03


def render_shot(shot: dict, dest: Path, open_f0: Path | None = None) -> float:
    frames_n = round((shot["out"] - shot["in"]) * FPS)
    kind = shot["kind"]

    if kind in ("svs_pan", "loop_return"):
        src_name = shot["raw_source"] if kind == "loop_return" else shot["source"]
        src_off = float(shot["raw_offset"] if kind == "loop_return" else shot["offset"])
        src = resolve_asset_path(src_name)
        raw = load_raw_video_frames(src, offset=src_off, frames_n=frames_n, sw=1920, sh=1080)
        cw = 1080.0 * (W / H)  # 607.5 px -> upscale 1920/1080 = 1.78x
        x0_s = float(shot["x0_start"])
        x0_e = float(shot["x0_end"])
        denom = float(max(1, frames_n - 1))
        frames = []
        for i, im in enumerate(raw):
            u = i / denom
            x0 = x0_s + (x0_e - x0_s) * u
            x0 = max(0.0, min(1920.0 - cw, x0))
            crop = im.transform((W, H), Image.Transform.EXTENT, (x0, 0.0, x0 + cw, 1080.0), resample=Image.Resampling.BICUBIC)
            crop = ImageEnhance.Color(crop).enhance(1.28)
            crop = ImageEnhance.Contrast(crop).enhance(1.09)
            crop = crop.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=2))
            arr = lift_navy(np.asarray(crop, dtype=np.float32))
            fr = Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8))
            if open_f0 is not None and i == 0:
                fr.save(open_f0)
            frames.append(fr)
        pipe_frames(frames, dest)
        if kind == "loop_return":
            shutil.copy2(dest, WORK / "exports" / shot["source"])
        return 1.78

    if kind == "still_cover":
        base, up = build_base_9x16_cover(shot)
        render_symmetric_still_zoom(base, frames_n, float(shot["z1"]), dest)
        return up

    if kind == "still_orb":
        base, up = build_base_9x16_orb(shot)
        render_symmetric_still_zoom(base, frames_n, float(shot["z1"]), dest)
        return up

    if kind == "pressure_gauge":
        return render_pressure_gauge(frames_n, dest)

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


def make_end(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.80)
    while max(d.textlength(r, font=f) for r, _ in END_ROWS) > W * 0.88:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 10
    y = BAND_Y0 + (BAND_H - gap * len(END_ROWS)) // 2
    placed = []
    for r, col in END_ROWS:
        bb = centred(d, y, r, f, col, stroke=6)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"end card outside 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed, "long_title": LONG_TITLE}


def make_teach(dest: Path, text: str) -> list[int]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.90)
    while d.textlength(text, font=f) > W * 0.82:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y1 - 88, text, f, YELLOW, stroke=7)
    pad = 18
    d.rounded_rectangle((bb[0] - pad, bb[1] - 10, bb[2] + pad, bb[3] + 10), radius=18, outline=(255, 224, 0, 230), width=4)
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
    im = ImageEnhance.Color(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.10)
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


def build_audio(work: Path, slices: list[dict], total: float) -> dict:
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
        "ffmpeg", "-y", "-v", "error", "-ss", "0.0", "-t", f"{total:.3f}",
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

    hits = [
        ("whoosh", 0.00, -6.0),
        ("rumble", 0.20, -10.5),
        ("tick", 4.08, -8.5),
        ("tick", TITLE_IN, -8.0),
        ("tick", TEACH_IN, -8.0),
        ("tick", 23.40, -8.5),
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


def main() -> None:
    # Verify no _v02 media already exists on NAS (never overwrite finished NAS media)
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
    print(f"Verified SHA-256s: VO={vo_sha[:12]}... Bed={bed_sha[:12]}... Master_v02={master_sha[:12]}...", flush=True)

    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    OUT_WORK = WORK / "exports"
    OUT_WORK.mkdir(parents=True)
    NAS_SUB_OUT.mkdir(parents=True, exist_ok=True)

    slices, words, last_word_end = build_voice_plan()
    joined = " ".join(w["w"] for w in words)
    print(f"Spoken words: {len(words)} | VO: {words[0]['s']:.3f}-{last_word_end:.3f} s | Total: {TOTAL_S:.3f} s", flush=True)

    for shot in SHOT_PLAN[:-1]:
        cut_t = shot["out"]
        for w in words:
            if w["s"] + 0.005 < cut_t < w["e"] - 0.005:
                raise SystemExit(f"Cut at {cut_t:.3f}s splits word {w['w']!r} ({w['s']:.3f}-{w['e']:.3f}s)")
    print("Verified 0 spoken words split across all 11 cut boundaries.", flush=True)

    open_f0 = WORK / "open_f0.png"
    concat_lines = []
    cuts_meta = []
    pool_meta = []
    seen_sources = set()

    for idx, shot in enumerate(SHOT_PLAN):
        piece = WORK / f"piece_{idx:02d}.mp4"
        up = render_shot(shot, piece, open_f0 if idx == 0 else None)
        concat_lines.append(f"file '{piece.name}'")
        c_entry = {
            "row": shot["row"],
            "timeline_in": shot["in"],
            "timeline_out": shot["out"],
            "source": shot["source"],
            "upscale": up,
            "video": bool(shot["video"]),
            "framing": (
                {"offset": shot["offset"], "crop": "9:16 full-bleed", "mode": "cover"}
                if shot["video"]
                else {"crop": "9:16 full-bleed", "mode": "cover"}
            ),
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
            })
        print(f"  rendered {shot['row']} ({shot['in']:.3f}-{shot['out']:.3f} s) upscale={up}", flush=True)

    (WORK / "list.txt").write_text("\n".join(concat_lines) + "\n")
    pic_mp4 = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"), "-c", "copy", str(pic_mp4)])

    hook_info = make_hook(WORK / "hook.png")
    title_info = make_title(WORK / "title.png")
    end_info = make_end(WORK / "end_card.png")
    teach_bb = make_teach(WORK / "teach.png", TEACH_TEXT)
    caps = caption_chunks(words, last_word_end)
    for i, c in enumerate(caps):
        c["bbox"] = make_caption(WORK / f"cap_{i:02d}.png", c["text"])

    aud = build_audio(WORK, slices, TOTAL_S)
    cal_wav, aac_i, aac_tp = calibrate_aac_wav(WORK, WORK / "mix.wav", TOTAL_S)
    aud["aac_lufs"] = aac_i
    aud["aac_tp_dbtp"] = aac_tp

    final_mp4 = OUT_WORK / f"{STEM}.mp4"
    inputs = ["-t", f"{TOTAL_S:.3f}", "-i", str(pic_mp4)]
    for name in ("hook.png", "title.png", "end_card.png", "teach.png"):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL_S:.3f}", "-i", str(WORK / name)]
    inputs += ["-i", str(cal_wav)]
    base_idx = 6
    for i in range(len(caps)):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL_S:.3f}", "-i", str(WORK / f"cap_{i:02d}.png")]

    fc = [
        f"[0:v]fps={FPS},setsar=1,format=yuv420p[v0]",
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='gte(t,0)*lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.28:alpha=1,fade=t=out:st={TITLE_OUT - 0.28:.2f}:d=0.28:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
        f"[3:v]format=rgba,fade=t=in:st={END_CARD_IN:.3f}:d=0.25:alpha=1[ec]",
        f"[v2][ec]overlay=0:0:enable='gte(t,{END_CARD_IN})'[v3]",
        f"[4:v]format=rgba,fade=t=in:st={TEACH_IN}:d=0.25:alpha=1,fade=t=out:st={TEACH_OUT - 0.25:.2f}:d=0.25:alpha=1[th]",
        f"[v3][th]overlay=0:0:enable='gte(t,{TEACH_IN})*lt(t,{TEACH_OUT})'[v4]",
    ]
    last_v = "v4"
    for i, c in enumerate(caps):
        fc.append(f"[{last_v}][{base_idx + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last_v = f"c{i}"
    fc.append(f"[{last_v}]noise=alls=2:allf=t,format=yuv420p[v]")

    run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", ";".join(fc),
        "-map", "[v]", "-map", "5:a",
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
    write_srt(caps, srt_path)
    cuts_path.write_text(json.dumps(cuts_meta, indent=2) + "\n")
    pool_path.write_text(json.dumps(pool_meta, indent=2) + "\n")

    nas_vo_future = NAS_SUB_OUT / f"{STEM}_vo.wav"
    nas_words_future = NAS_SUB_OUT / f"{STEM}_words.json"
    meta_obj = {
        "slug": SHORT_SLUG,
        "stem": STEM,
        "title": SHORT_TITLE,
        "alt_title": ALT_TITLE,
        "air_date": AIR_DATE,
        "test_a": True,
        "relatedVideoId": LONG_ID,
        "parent_long_id": LONG_ID,
        "parent_long_title": LONG_TITLE,
        "parent_master_v02_sha256": master_sha,
        "spoken": joined,
        "vo_onset_s": words[0]["s"],
        "last_word_end_s": last_word_end,
        "duration_s": TOTAL_S,
        "hook": {"text": hook_info["text"], "start_s": 0.0, "end_s": HOOK_END},
        "title_banner": {"text": LONG_TITLE, "start_s": TITLE_IN, "end_s": TITLE_OUT},
        "teach_overlay": {"text": TEACH_TEXT, "start_s": TEACH_IN, "end_s": TEACH_OUT, "bbox": teach_bb},
        "end_card": {"start_s": END_CARD_IN, "len_s": round(TOTAL_S - END_CARD_IN, 3)},
        "words_file": str(words_path),
        "vo": str(vo_stem_out),
        "audio": aud,
    }
    meta_path.write_text(json.dumps(meta_obj, indent=2) + "\n")

    frame0_jpg = OUT_WORK / f"{STEM}_frame0.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.30", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(frame0_jpg)])
    cover_jpg = OUT_WORK / f"{STEM}_cover.jpg"
    cover_info = make_cover(cover_jpg, open_f0)

    shot_tiles = []
    for idx, shot in enumerate(SHOT_PLAN):
        mid_t = round((shot["in"] + shot["out"]) / 2.0, 2)
        raw_t = sp.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{mid_t:.2f}", "-i", str(final_mp4),
            "-frames:v", "1", "-vf", "scale=360:640", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
        ])
        im_t = Image.frombytes("RGB", (360, 640), raw_t)
        d_t = ImageDraw.Draw(im_t)
        d_t.rectangle((0, 0, 360, 32), fill=(0, 0, 0))
        d_t.text((8, 8), f"{idx+1:02d} {shot['row']} ({mid_t:.1f}s)", fill=(255, 255, 255))
        shot_tiles.append(im_t)
    cols_s = 4
    rows_s = (len(shot_tiles) + cols_s - 1) // cols_s
    sheet_12 = Image.new("RGB", (360 * cols_s, 640 * rows_s), (18, 22, 30))
    for idx, im_t in enumerate(shot_tiles):
        sheet_12.paste(im_t, ((idx % cols_s) * 360, (idx // cols_s) * 640))
    sheet_12_path = OUT_WORK / f"{STEM}_review_12shots.jpg"
    sheet_12.save(sheet_12_path, quality=92)

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

    # Update meta_obj paths to canonical NAS paths before copying to NAS
    meta_obj["words_file"] = str(nas_words_future)
    meta_obj["vo"] = str(nas_vo_future)
    meta_path.write_text(json.dumps(meta_obj, indent=2) + "\n")
    cover_info["file"] = str(NAS_SUB_OUT / f"{STEM}_cover.jpg")

    open_sheet_path = OUT_WORK / f"{STEM}_open_sheet.jpg"
    summary = {
        "stem": STEM,
        "mp4_path": str(NAS_SUB_OUT / f"{STEM}.mp4"),
        "mp4_sha256": sha256(final_mp4),
        "frame0_jpg_sha256": sha256(frame0_jpg),
        "cover_jpg_sha256": sha256(cover_jpg),
        "open_sheet_sha256": sha256(open_sheet_path),
        "review_12shots_sha256": sha256(sheet_12_path),
        "master_v02_sha256": master_sha,
        "vo_sha256": vo_sha,
        "bed_sha256": bed_sha,
        "duration_s": TOTAL_S,
        "fps": FPS,
        "frames": round(TOTAL_S * FPS),
        "words_count": len(words),
        "vo_onset_s": words[0]["s"],
        "s01_s02_breath_s": round(words[15]["s"] - words[14]["e"], 3),
        "payoff_start_s": words[73]["s"],
        "payoff_pct": round(words[73]["s"] / TOTAL_S * 100.0, 1),
        "last_word_end_s": last_word_end,
        "tail_gap_s": round(TOTAL_S - last_word_end, 3),
        "cut1_s": SHOT_PLAN[0]["out"],
        "cut2_s": SHOT_PLAN[1]["out"],
        "max_shot_s": max(round(s["out"] - s["in"], 3) for s in SHOT_PLAN),
        "audio": aud,
        "hook": hook_info,
        "title": title_info,
        "teach": {"text": TEACH_TEXT, "in": TEACH_IN, "out": TEACH_OUT, "bbox": teach_bb},
        "end_card": {"start_s": END_CARD_IN, "len_s": round(TOTAL_S - END_CARD_IN, 3)},
        "cover": cover_info,
        "gates": gates,
    }
    summary_path = OUT_WORK / f"{STEM}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")

    # Copy all verified _v02 outputs to NAS_SUB_OUT (checking SHA-256 on every file)
    for item in sorted(OUT_WORK.iterdir()):
        if item.is_dir():
            dst_dir = NAS_SUB_OUT / item.name
            dst_dir.mkdir(parents=True, exist_ok=True)
            for sub in sorted(item.iterdir()):
                if sub.is_file():
                    copy_verified(sub, dst_dir / sub.name)
        elif item.is_file():
            copy_verified(item, NAS_SUB_OUT / item.name)

    # Re-run gate_shorts_open on the NAS copy so gate.txt/gate.json record canonical NAS paths
    g_nas_txt = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", NAS_SUB_OUT / f"{STEM}.mp4", "--air-date", AIR_DATE, "--sheet-dir", NAS_SUB_OUT])
    g_nas_json = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", NAS_SUB_OUT / f"{STEM}.mp4", "--air-date", AIR_DATE, "--sheet-dir", NAS_SUB_OUT, "--json"])
    if g_nas_txt.returncode != 0:
        raise SystemExit(f"NAS gate_shorts_open failed: {g_nas_txt.stdout}\n{g_nas_txt.stderr}")
    (NAS_SUB_OUT / f"{STEM}_gate.txt").write_text((g_nas_txt.stdout or "") + (g_nas_txt.stderr or ""))
    (NAS_SUB_OUT / f"{STEM}_gate.json").write_text(g_nas_json.stdout or g_nas_json.stderr)

    # Mirror primary export and key sidecars into NAS 10_Shorts/ root with SHA-256 verification
    for name in (
        f"{STEM}.mp4",
        f"{STEM}_frame0.jpg",
        f"{STEM}_cover.jpg",
        f"{STEM}_frame0_preview.jpg",
        f"{STEM}_cover_preview.jpg",
        f"{STEM}_open_sheet.jpg",
        f"{STEM}_review_12shots.jpg",
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
