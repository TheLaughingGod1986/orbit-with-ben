#!/usr/bin/env python3
"""064 Every Planet Explained — Companion Short 1 (Test A Opening Short) v02 Builder (J3903).

Full-bleed 1080x1920 (9:16), 24 fps CFR (exact 738 frames = 30.750 s).
Zero blurred bars/padding, zero near-black, zero integer push jitter, zero Orbit at frame 0.
£0 cash, 0 ElevenLabs chars, 0 Flow/Vertex credits, zero YouTube upload or scheduling.

Short Title: Why Does Water Ice Survive 430°C Heat on Mercury?
Alt Title:   How Does Mercury Hide Water Ice at 430°C?
Slug / Stem: short01_testA_opening / 064_short01_testA_opening_v02
Proposed Candidate / Gate-Check Slot: Mon 28 Dec 2026 11:30Z (non-colliding Mon/Wed/Fri/Sat Orbit Short day; NOT scheduled yet; MUST NOT upload or air before 064 long is public Wed 16 Dec 18:00 London)
Parent Long (064): Every Planet Explained in 12 Minutes (Mercury to Neptune)

Lifts verbatim opening sentences S1-S4 (raw 0.060-32.600 s, 71 spoken words, Mercury 430°C polar
water ice opening through Colombo 1965) from locked master VO `02_Voiceover/every_planet_explained_vo_v01.wav`
(SHA-256 4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa) with tightened <0.25 s
inter-sentence breaths, paired with 064's own score bed `every_planet_score_bed_v01.mp3` and house SFX kit.
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
NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "064_Every-Planet-Explained-In-10-Minutes"
)
NAS_HARV = NAS_FILM / "03_Reference-Material" / "harvest_J3022_v01"
NAS_SHORTS = NAS_FILM / "10_Shorts"
NAS_SUB_OUT = NAS_SHORTS / "short01_testA_opening" / "06_Final-Exports"

MASTER_V03 = NAS_FILM / "09_Final-Export" / "064_every_planet_explained_master_v03.mp4"
EXPECTED_MASTER_SHA256 = "d59057aed1590e7f6ef097513256a0548c4f9b1d7e544c4bade28aa83fef647a"
VO_WAV = NAS_FILM / "02_Voiceover" / "every_planet_explained_vo_v01.wav"
EXPECTED_VO_SHA256 = "4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa"
STT_JSON = NAS_FILM / "02_Voiceover" / "stt" / "every_planet_explained_vo_v01" / "stt_raw.json"
BED_MP3 = NAS_FILM / "05_Music" / "every_planet_score_bed_v01.mp3"
EXPECTED_BED_SHA256 = "3e47e9d6da9aca6836a00c27a1fa58e53801190ae06ed445966ed51f5c0d75c6"
KIT_DIR = NAS_FILM / "06_Sound-Effects" / "kit_v01"

SCRATCH_BASE = Path(os.environ.get("STUDIO_SCRATCH", "/Volumes/MiniWork/scratch"))
WORK = SCRATCH_BASE / "J3903_064_short01_v02"

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import gate_shorts_open as gso  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 24
SR = 48000
TOTAL_FRAMES = 738
TOTAL_S = TOTAL_FRAMES / FPS  # 30.750 s exact at 24 fps CFR

BAND_H = round(W * 9 / 16)          # 608 px (safe zone for title/teach/end overlays; picture is full 1080x1920)
BAND_Y0 = (H - BAND_H) // 2         # 656 px
BAND_Y1 = BAND_Y0 + BAND_H          # 1264 px
LINE_H = round(BAND_H * 0.115)      # 70 px

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)         # #FFE000
CYAN = (105, 225, 250, 255)
CORAL = (255, 118, 72, 255)
NAVY_FLOOR = np.array([28.0, 38.0, 58.0], dtype=np.float32)

STEM = "064_short01_testA_opening_v02"
SHORT_SLUG = "short01_testA_opening"
SHORT_TITLE = "Why Does Water Ice Survive 430°C Heat on Mercury?"
ALT_TITLE = "How Does Mercury Hide Water Ice at 430°C?"
AIR_DATE = "2026-12-28"             # Non-colliding candidate Mon/Wed/Fri/Sat Orbit Short slot (gate-check date ONLY; NOT scheduled)
LONG_TITLE = "Every Planet Explained in 12 Minutes (Mercury to Neptune)"

HOOK_ROWS = [("ICE AT", WHITE), ("430°C?", YELLOW)]
COVER_ROWS = [("ICE AT", WHITE), ("430°C?", YELLOW)]
TITLE_ROWS = [
    "Every Planet Explained",
    "in 12 Minutes",
    "(Mercury to Neptune)",
]
END_CARD_LINE = "Full film on the channel"
END_ROWS = [
    ("Every Planet Explained", WHITE),
    ("in 12 Minutes", WHITE),
    ("(Mercury to Neptune)", WHITE),
    (END_CARD_LINE, YELLOW),
]

HOOK_END = 2.10
TITLE_IN, TITLE_OUT = 9.00, 14.00
TEACH_IN, TEACH_OUT = 23.75, 27.70
TEACH_TEXT = "1965 · GIUSEPPE COLOMBO"
END_CARD_IN = 714 / FPS  # 29.750 s exact (24 frames loop/end card tail)

# Verbatim S1-S4 from every_planet_explained_vo_v01.wav (71 spoken words), tightened breaths <0.25 s
VO_SEGMENTS = [
    (0.060, 6.600),   # S1: "On Mercury, the Sun's closest planet, why does water ice survive 430-degree heat?"
    (7.560, 11.050),  # S2: "The ice hides in polar craters that never see sunlight."
    (11.890, 25.140), # S3: "At 58 million km out, sunlight shines up to 7x brighter than on Earth, yet ... -180 °C."
    (26.280, 32.600), # S4: "In 1965, Italian mathematician Giuseppe Colombo solved its spin mystery."
]
VO_LEAD_S = 0.000
VO_GAPS = [0.060, 0.080, 0.020]

# 12-shot full-bleed 1080x1920 cut plan at exact 24 fps frames (sum = 738 frames = 30.750 s).
# Cut 1 = 2.500 s (<= 2.80 s), Cut 2 = 4.458 s (<= 4.80 s), max shot = 3.625 s (<= 4.00 s).
# Every still appears <= 2 times; zero consecutive code graphics; zero upscale > 1.50x.
SHOT_PLAN = [
    {
        "row": "R01a",
        "f0": 0, "f1": 60,  # 0.000 - 2.500 s (2.500 s)
        "kind": "mercury_spin",
        "source": "code_graphic_064_short1_r01a_mercury_spin_v02.mp4",
        "title": "Rotating Mercury globe from NASA MESSENGER enhanced-color global imagery",
        "video": True,
        "offset": 0.0,
        "lon_start_deg": 40.0,
        "lon_rate_deg_s": 42.0,
    },
    {
        "row": "R01b",
        "f0": 60, "f1": 107,  # 2.500 - 4.458 s (1.958 s)
        "kind": "surface_pan",
        "source": "PIA17386.jpg",
        "title": "Enhanced Color Mercury Map (MESSENGER global surface)",
        "video": False,
        "crop_box": (220, 250, 3860, 1798),
        "x_frac_0": 0.14, "x_frac_1": 0.30,
        "z0": 1.04, "z1": 1.14,
        "sat": 1.26, "contrast": 1.12,
    },
    {
        "row": "R01c",
        "f0": 107, "f1": 157,  # 4.458 - 6.542 s (2.083 s)
        "kind": "still_orb",
        "source": "PIA16853.jpg",
        "title": "Colors of the Innermost Planet: View 1 (MESSENGER)",
        "video": False,
        "orb_scale": 0.90,
        "z0": 1.00, "z1": 1.07,
        "sat": 1.24, "y_offset": 0,
    },
    {
        "row": "R02a",
        "f0": 157, "f1": 195,  # 6.542 - 8.125 s (1.583 s)
        "kind": "polar_cover",
        "source": "PIA19411.jpg",
        "title": "Water Ice on Mercury (MESSENGER north polar mosaic)",
        "video": False,
        "x_frac_0": 0.44, "x_frac_1": 0.50,
        "z0": 1.00, "z1": 1.08,
        "sat": 1.28, "contrast": 1.14,
    },
    {
        "row": "R02b",
        "f0": 195, "f1": 243,  # 8.125 - 10.125 s (2.000 s) — back-to-back with R02a = 1 appearance
        "kind": "polar_cover",
        "source": "PIA19411.jpg",
        "title": "Water Ice on Mercury (MESSENGER north polar mosaic)",
        "video": False,
        "x_frac_0": 0.50, "x_frac_1": 0.53,
        "z0": 1.28, "z1": 1.44,
        "sat": 1.32, "contrast": 1.16,
    },
    {
        "row": "R03a",
        "f0": 243, "f1": 338,  # 10.125 - 14.083 s (3.958 s <= 4.00 s; clears 9-14 s title banner completely)
        "kind": "still_orb",
        "source": "PIA15162.jpg",
        "title": "Mercury Globe: 0°N, 180°E (MESSENGER)",
        "video": False,
        "orb_scale": 0.90,
        "z0": 1.00, "z1": 1.06,
        "warm_sun": True, "y_offset": 0,
    },
    {
        "row": "R03b",
        "f0": 338, "f1": 394,  # 14.083 - 16.417 s (2.333 s; strictly after TITLE_OUT=14.00 s)
        "kind": "cg_sunlight",
        "source": "code_graphic_064_short1_r03b_sunlight_9x16_v02.mp4",
        "title": "Mercury 7x sunlight intensity explainer",
        "video": True,
        "offset": 0.0,
    },
    {
        "row": "R03c",
        "f0": 394, "f1": 481,  # 16.417 - 20.042 s (3.625 s) — real Mercury surface separating graphics
        "kind": "surface_pan",
        "source": "PIA17386.jpg",
        "title": "Enhanced Color Mercury Map (MESSENGER global surface)",
        "video": False,
        "crop_box": (220, 250, 3860, 1798),
        "x_frac_0": 0.54, "x_frac_1": 0.72,
        "z0": 1.06, "z1": 1.16,
        "sat": 1.22, "contrast": 1.12, "cool_night": True,
    },
    {
        "row": "R03d",
        "f0": 481, "f1": 563,  # 20.042 - 23.458 s (3.417 s)
        "kind": "cg_night",
        "source": "code_graphic_064_short1_r03d_night_9x16_v02.mp4",
        "title": "Mercury 430 C day versus -180 C night contrast explainer",
        "video": True,
        "offset": 0.0,
    },
    {
        "row": "R04a",
        "f0": 563, "f1": 635,  # 23.458 - 26.458 s (3.000 s)
        "kind": "still_orb",
        "source": "PIA11364.jpg",
        "title": "Mercury True Color is in the Eye of the Beholder (MESSENGER)",
        "video": False,
        "sub_crop": (960, 40, 1890, 970),  # Single top-right globe only (no 2x2 quad)
        "orb_scale": 0.88,
        "z0": 1.00, "z1": 1.06,
        "sat": 1.24, "y_offset": -90,
    },
    {
        "row": "R04b",
        "f0": 635, "f1": 714,  # 26.458 - 29.750 s (3.292 s)
        "kind": "still_orb",
        "source": "PIA16853.jpg",
        "title": "Colors of the Innermost Planet: View 1 (MESSENGER)",
        "video": False,
        "orb_scale": 0.94,
        "z0": 1.03, "z1": 1.10,
        "sat": 1.30, "y_offset": -90,
    },
    {
        "row": "R01_loop",
        "f0": 714, "f1": 738,  # 29.750 - 30.750 s (1.000 s) — seamless return into Frame 0
        "kind": "mercury_loop",
        "source": "frame0_return_064_short01_testA_opening_v02.mp4",
        "title": "Opening frame return for seamless loop",
        "video": True,
        "offset": 0.0,
        "lon_target_deg": 40.0,
        "lon_rate_deg_s": 42.0,
    },
]


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
    """Ensure max(R,G,B) >= 54 (V >= 0.212 > 0.18) so visor_frac == 0.0000 and near_black == 0.0%."""
    mx = arr.max(axis=2, keepdims=True)
    return np.where(mx < 54.0, np.maximum(arr, NAVY_FLOOR), arr)


_STAR_CANVAS: np.ndarray | None = None


def get_star_canvas(cw: int = 1360, ch: int = 2360) -> np.ndarray:
    """Rich lifted-navy deep-space starfield with multi-scale pinpoint stars and subtle cosmic dust.
    Provides crisp fine detail across top and bottom outer bands so full_bleed passes 100%."""
    global _STAR_CANVAS
    if _STAR_CANVAS is None:
        rng = np.random.default_rng(6401)
        yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
        wave1 = 0.5 + 0.5 * np.sin(xx * 0.0065 + yy * 0.0045 + 0.7)
        wave2 = 0.5 + 0.5 * np.cos(xx * 0.011 - yy * 0.008 + 1.9)
        neb = 0.6 * wave1 + 0.4 * wave2
        r = 28.0 + 18.0 * neb + rng.normal(0.0, 2.2, (ch, cw))
        g = 38.0 + 22.0 * neb + rng.normal(0.0, 2.2, (ch, cw))
        b = 60.0 + 34.0 * neb + rng.normal(0.0, 2.5, (ch, cw))
        rgb = np.stack([r, g, b], axis=-1).astype(np.float32)

        # Fine pinpoint background stars (2-3 px)
        for _ in range(3800):
            sy = int(rng.integers(4, ch - 6))
            sx = int(rng.integers(4, cw - 6))
            br = float(rng.uniform(110.0, 235.0))
            sz = 2 if rng.random() < 0.70 else 3
            tint = rng.choice([0, 1, 2])
            if tint == 0:
                col = (br * 0.90, br * 0.96, min(255.0, br * 1.06))
            elif tint == 1:
                col = (min(255.0, br * 1.05), br * 0.97, br * 0.85)
            else:
                col = (br, br, br)
            for k in range(3):
                rgb[sy:sy + sz, sx:sx + sz, k] = np.maximum(rgb[sy:sy + sz, sx:sx + sz, k], col[k])

        # Brighter foreground stars (4-6 px) so 108x192 downscale keeps crisp texture in top/bottom bands
        for _ in range(620):
            sy = int(rng.integers(6, ch - 8))
            sx = int(rng.integers(6, cw - 8))
            br = float(rng.uniform(185.0, 255.0))
            sz = int(rng.choice([4, 5, 6]))
            for k, mult in enumerate((0.92, 0.96, 1.0)):
                rgb[sy:sy + sz, sx:sx + sz, k] = np.maximum(rgb[sy:sy + sz, sx:sx + sz, k], br * mult)
                # Tiny bright core
                rgb[sy + 1:sy + sz - 1, sx + 1:sx + sz - 1, k] = np.maximum(
                    rgb[sy + 1:sy + sz - 1, sx + 1:sx + sz - 1, k], min(255.0, br * 1.1)
                )

        _STAR_CANVAS = np.clip(lift_navy(rgb), 28.0, 255.0)
    return _STAR_CANVAS


def starfield_frame(u: float, dx: float = 120.0, dy: float = 90.0) -> np.ndarray:
    canvas = get_star_canvas()
    ch, cw, _ = canvas.shape
    x0 = (cw - W) * 0.5 - dx * 0.5 + dx * u
    y0 = (ch - H) * 0.5 - dy * 0.5 + dy * u
    im = Image.fromarray(canvas.astype(np.uint8), "RGB")
    crop = im.transform((W, H), Image.Transform.EXTENT, (x0, y0, x0 + W, y0 + H), resample=Image.Resampling.BICUBIC)
    return np.asarray(crop, dtype=np.float32)


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


_MERCURY_TEX: np.ndarray | None = None


def get_mercury_equirect() -> np.ndarray:
    """Load cropped, vibrant NASA MESSENGER enhanced-color Mercury global texture (PIA17386)."""
    global _MERCURY_TEX
    if _MERCURY_TEX is None:
        im = Image.open(NAS_HARV / "PIA17386.jpg").convert("RGB")
        # Crop strictly inside the black north/south polar margins of PIA17386
        im = im.crop((180, 255, 3916, 1793))
        im = ImageEnhance.Color(im).enhance(1.32)
        im = ImageEnhance.Contrast(im).enhance(1.16)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=135, threshold=2))
        _MERCURY_TEX = np.asarray(im, dtype=np.float32)
    return _MERCURY_TEX


def render_mercury_spin(
    frames_n: int,
    lon_start_deg: float,
    lon_rate_deg_s: float,
    dest: Path,
    zoom0: float = 1.00,
    zoom1: float = 1.07,
    open_f0: Path | None = None,
    star_u0: float = 0.0,
    star_u1: float = 1.0,
) -> float:
    """Render a real 3D orthographic rotating Mercury globe directly mapped from NASA MESSENGER
    PIA17386.jpg over a drifting deep-space starfield, with realistic sunlit shading & corona rim."""
    tex = get_mercury_equirect()
    th, tw, _ = tex.shape

    # Sphere disk size (large, unmistakably Mercury on phone; centered below upper hook band)
    base_d = 980
    cx0, cy0 = W * 0.5, 1080.0

    # Precompute sphere grid at 1040x1040 for smooth zoom
    G = 1040
    yy, xx = np.mgrid[0:G, 0:G].astype(np.float32)
    nx = (xx - (G - 1) * 0.5) / (G * 0.485)
    ny = (yy - (G - 1) * 0.5) / (G * 0.485)
    r2 = nx * nx + ny * ny
    inside = r2 <= 1.0
    nz = np.sqrt(np.clip(1.0 - r2, 0.0, 1.0))

    # Crisp anti-aliased sphere alpha
    r = np.sqrt(r2)
    alpha = np.clip((1.002 - r) / 0.012, 0.0, 1.0)

    # Solar lighting from upper-left-front so sunlit golden craters & dramatic terminator stand out
    lx, ly, lz = -0.52, -0.34, 0.78
    ndotl = np.clip(nx * lx + ny * ly + nz * lz, 0.0, 1.0)
    # Lommel-Seeliger-like planetary shading (Mercury regolith stays crisp to the limb) + subtle nightside lift
    shade = 0.24 + 0.96 * np.power(ndotl, 0.62)
    # Warm sunlit rim highlight
    rim = np.clip((1.0 - nz) * ndotl, 0.0, 1.0) ** 2.2

    lat = np.arcsin(np.clip(-ny, -1.0, 1.0))  # [-pi/2, +pi/2]
    ty_f = ((0.5 - lat / math.pi) * (th - 1)).astype(np.float32)
    ty0 = np.clip(np.floor(ty_f).astype(np.int32), 0, th - 2)
    wy = (ty_f - ty0)[:, :, None]

    lon_base = np.arctan2(nx, np.maximum(nz, 1e-6))  # [-pi/2, +pi/2]

    frames = []
    denom = float(max(1, frames_n - 1))
    for i in range(frames_n):
        u = i / denom
        t_s = i / FPS
        lon_deg = lon_start_deg + lon_rate_deg_s * t_s
        lon_rad = lon_base + math.radians(lon_deg)
        # Map longitude smoothly across [0, tw) with horizontal mirror wrap so seam is invisible
        u_wrap = (lon_rad / (2.0 * math.pi)) % 1.0
        tx_f = (u_wrap * (tw - 1)).astype(np.float32)
        tx0 = np.clip(np.floor(tx_f).astype(np.int32), 0, tw - 2)
        wx = (tx_f - tx0)[:, :, None]

        # Bilinear sample from PIA17386
        c00 = tex[ty0, tx0]
        c01 = tex[ty0, tx0 + 1]
        c10 = tex[ty0 + 1, tx0]
        c11 = tex[ty0 + 1, tx0 + 1]
        col = (c00 * (1.0 - wx) + c01 * wx) * (1.0 - wy) + (c10 * (1.0 - wx) + c11 * wx) * wy

        lit = col * shade[:, :, None]
        lit[:, :, 0] += 55.0 * rim
        lit[:, :, 1] += 36.0 * rim
        lit[:, :, 2] += 14.0 * rim
        lit = np.clip(lit, 0.0, 255.0)

        # Build drifting starfield background + warm solar glow behind upper-left limb
        su = star_u0 + (star_u1 - star_u0) * u
        bg = starfield_frame(su, dx=190.0, dy=110.0)

        # Resize/place spinning globe at smooth zoom z
        z = zoom0 + (zoom1 - zoom0) * u
        diam = int(round(base_d * z))
        # Ensure even size
        diam += diam % 2
        globe_rgba = np.zeros((G, G, 4), dtype=np.uint8)
        globe_rgba[:, :, :3] = lit.astype(np.uint8)
        globe_rgba[:, :, 3] = (alpha * 255.0).astype(np.uint8)
        g_im = Image.fromarray(globe_rgba, "RGBA").resize((diam, diam), Image.Resampling.BICUBIC)

        # Gentle vertical orbital drift + rotation makes frame0_diff strong across central band
        if star_u1 == 0.0:
            # Loop return approaches exact Frame 0 position (cx0 - 13, cy0)
            cy = cy0 + 28.0 * (1.0 - u)
            cx = cx0 - 13.0 - 18.0 * (1.0 - u)
        else:
            cy = cy0 - 38.0 * u
            cx = cx0 - 13.0 + 26.0 * u
        gx0 = int(round(cx - diam * 0.5))
        gy0 = int(round(cy - diam * 0.5))

        canvas = Image.fromarray(bg.astype(np.uint8), "RGB").convert("RGBA")
        # Soft sunlit halo on upper-left behind Mercury
        canvas.alpha_composite(g_im, (gx0, gy0))
        arr = lift_navy(np.asarray(canvas.convert("RGB"), dtype=np.float32))
        fr = Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8), "RGB")
        if open_f0 is not None and i == 0:
            fr.save(open_f0)
        frames.append(fr)

    pipe_frames(frames, dest)
    return 1.0


def render_surface_pan(shot: dict, dest: Path) -> float:
    """Full-bleed 1080x1920 symmetric push-in across a high-res NASA MESSENGER surface plate.
    Uses symmetric sub-pixel center zoom (1.00 -> z1) for 0.000 px off-trend in polish_gate.jitter()."""
    frames_n = shot["f1"] - shot["f0"]
    im = Image.open(NAS_HARV / shot["source"]).convert("RGB")
    if "crop_box" in shot:
        im = im.crop(shot["crop_box"])
    im = ImageEnhance.Color(im).enhance(float(shot.get("sat", 1.24)))
    im = ImageEnhance.Contrast(im).enhance(float(shot.get("contrast", 1.12)))
    if shot.get("cool_night"):
        arr = np.asarray(im, dtype=np.float32)
        arr[:, :, 0] *= 0.78
        arr[:, :, 1] *= 0.90
        arr[:, :, 2] = np.clip(arr[:, :, 2] * 1.18 + 14.0, 0, 255)
        im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    im = im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=125, threshold=2))

    sw, sh = im.size
    ch = float(sh)
    cw = ch * (W / H)
    xf = 0.5 * (float(shot["x_frac_0"]) + float(shot["x_frac_1"]))
    x0 = max(0.0, min(sw - cw, (sw - cw) * xf))
    y0 = 0.0
    base = im.transform((W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), resample=Image.Resampling.BICUBIC)
    base = Image.fromarray(np.clip(lift_navy(np.asarray(base, dtype=np.float32)), 28, 255).astype(np.uint8), "RGB")
    z1 = 1.06
    render_symmetric_zoom(base, frames_n, 1.00, z1, dest)
    return round((H / ch) * z1, 2)


def render_polar_cover(shot: dict, dest: Path) -> float:
    """Full-bleed 1080x1920 framing of MESSENGER north polar mosaic PIA19411 (4000x2179).
    Blends dark sky above the curved polar horizon seamlessly into our lifted-navy crisp starfield
    so top/bottom bands are 100% full-bleed textured with zero black bars or padding."""
    frames_n = shot["f1"] - shot["f0"]
    im = Image.open(NAS_HARV / shot["source"]).convert("RGB")
    im = ImageEnhance.Color(im).enhance(float(shot.get("sat", 1.28)))
    im = ImageEnhance.Contrast(im).enhance(float(shot.get("contrast", 1.14)))
    im = im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=125, threshold=2))

    # Pre-blend the black sky in PIA19411 with rich starfield texture at native 4000x2179
    sw, sh = im.size
    arr_src = np.asarray(im, dtype=np.float32)
    st_tile = Image.fromarray(get_star_canvas().astype(np.uint8), "RGB").resize((sw, sh), Image.Resampling.BICUBIC)
    st_arr = np.asarray(st_tile, dtype=np.float32)
    luma_max = arr_src.max(axis=2, keepdims=True)
    m_sky = np.clip((38.0 - luma_max) / 28.0, 0.0, 1.0)
    merged = arr_src * (1.0 - m_sky) + st_arr * m_sky
    base_im = Image.fromarray(np.clip(lift_navy(merged), 28, 255).astype(np.uint8), "RGB")

    z0, z1 = float(shot["z0"]), float(shot["z1"])
    xf0, xf1 = float(shot["x_frac_0"]), float(shot["x_frac_1"])
    denom = float(max(1, frames_n - 1))
    frames = []
    max_up = 1.0
    for i in range(frames_n):
        u = i / denom
        z = z0 + (z1 - z0) * u
        ch = sh / z
        cw = ch * (W / H)
        xf = xf0 + (xf1 - xf0) * u
        x0 = max(0.0, min(sw - cw, (sw - cw) * xf))
        y0 = (sh - ch) * 0.56  # Keep Prokofiev yellow polar ice craters centered
        y0 = max(0.0, min(sh - ch, y0))
        fr = base_im.transform((W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), resample=Image.Resampling.BICUBIC)
        arr = lift_navy(np.asarray(fr, dtype=np.float32))
        frames.append(Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8), "RGB"))
        max_up = max(max_up, H / ch)
    pipe_frames(frames, dest)
    return round(max_up, 2)


def build_orb_base(shot: dict) -> tuple[Image.Image, float]:
    """Composite a NASA Mercury globe plate seamlessly onto the crisp lifted-navy starfield
    with circular + dark-space feathering so zero box edges or near-black exist."""
    im = Image.open(NAS_HARV / shot["source"]).convert("RGB")
    if "sub_crop" in shot:
        im = im.crop(shot["sub_crop"])
    # Tight square bounding box around the lit Mercury globe
    L = np.asarray(im.convert("L"))
    ys, xs = np.where(L > 18)
    if len(xs) > 100:
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
        side = max(x1 - x0, y1 - y0)
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        half = int(side * 0.53)
        im = im.crop((max(0, cx - half), max(0, cy - half), min(im.width, cx + half), min(im.height, cy + half)))

    if shot.get("warm_sun"):
        a = np.asarray(im, dtype=np.float32)
        g = a.mean(axis=2)
        a = np.stack([g * 1.12 + 16.0, g * 1.04 + 12.0, g * 0.90 + 10.0], axis=-1)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    else:
        im = ImageEnhance.Color(im).enhance(float(shot.get("sat", 1.22)))
        im = ImageEnhance.Contrast(im).enhance(1.10)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=120, threshold=2))

    sw, sh = im.size
    orb_scale = float(shot.get("orb_scale", 0.90))
    target_w = round(W * orb_scale)
    scale = target_w / float(sw)
    nw, nh = round(sw * scale), round(sh * scale)
    fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
    fg_arr = np.asarray(fg, dtype=np.float32)

    bg_arr = starfield_frame(0.5, dx=0.0, dy=0.0).copy()
    yy, xx = np.mgrid[0:nh, 0:nw].astype(np.float32)
    rx = (xx - nw * 0.5) / max(1.0, nw * 0.47)
    ry = (yy - nh * 0.5) / max(1.0, nh * 0.47)
    r = np.sqrt(rx * rx + ry * ry)
    radial = np.clip((1.00 - r) / 0.16, 0.0, 1.0)
    radial = 0.5 - 0.5 * np.cos(np.pi * radial)

    luma_max = fg_arr.max(axis=2)
    space_key = np.clip((luma_max - 14.0) / 30.0, 0.0, 1.0)
    core = np.clip((0.80 - r) / 0.14, 0.0, 1.0)
    alpha = radial * np.maximum(core, space_key)

    x0 = (W - nw) // 2
    y0 = (H - nh) // 2 + int(shot.get("y_offset", 0))
    y0 = max(20, min(H - nh - 20, y0))
    patch = bg_arr[y0:y0 + nh, x0:x0 + nw]
    patch[:] = patch * (1.0 - alpha[:, :, None]) + lift_navy(fg_arr) * alpha[:, :, None]

    z1 = float(shot.get("z1", 1.06))
    up = round(scale * z1, 2)
    return Image.fromarray(np.clip(lift_navy(bg_arr), 28, 255).astype(np.uint8), "RGB"), up


def render_symmetric_zoom(base: Image.Image, frames_n: int, z0: float, z1: float, dest: Path) -> None:
    """Symmetric sub-pixel center zoom (z0 -> z1) on a unified 1080x1920 image: 0.000 px jitter."""
    denom = float(max(1, frames_n - 1))
    frames = []
    for i in range(frames_n):
        z = z0 + (z1 - z0) * (i / denom)
        cw, ch = W / z, H / z
        l, t = (W - cw) * 0.5, (H - ch) * 0.5
        fr = base.transform((W, H), Image.Transform.EXTENT, (l, t, l + cw, t + ch), resample=Image.Resampling.BICUBIC)
        frames.append(fr)
    pipe_frames(frames, dest)


def make_globe_rgba(path: Path, diameter: int, sat: float = 1.25) -> Image.Image:
    im = Image.open(path).convert("RGB")
    L = np.asarray(im.convert("L"))
    ys, xs = np.where(L > 18)
    if len(xs) > 100:
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
        side = max(x1 - x0, y1 - y0)
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        half = side // 2 + int(side * 0.02)
        im = im.crop((max(0, cx - half), max(0, cy - half), min(im.width, cx + half), min(im.height, cy + half)))
    im = im.resize((diameter, diameter), Image.Resampling.LANCZOS)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    circle = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(circle).ellipse((2, 2, diameter - 3, diameter - 3), fill=255)
    circle = circle.filter(ImageFilter.GaussianBlur(1.5))
    out = im.convert("RGBA")
    out.putalpha(circle)
    ImageDraw.Draw(out).ellipse(
        (2, 2, diameter - 3, diameter - 3), outline=(215, 232, 255, 185), width=max(2, diameter // 85)
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


def render_cg_sunlight(frames_n: int, dest: Path) -> float:
    """Native 1080x1920 vertical animated explainer #1 (R03b, 14.083-16.417 s):
    Starts strictly after 9-14 s title banner exits (zero text overlap).
    Word-matched strictly to 'seven times brighter than on Earth': real MESSENGER Mercury globe
    + single animated 7.0x SUNLIGHT scale bar in 68 px house type (11.2% of 608 px 16:9 band)."""
    g_merc = make_globe_rgba(NAS_HARV / "PIA15162.jpg", 380, sat=1.14)
    g_merc = g_merc.filter(ImageFilter.UnsharpMask(radius=1.3, percent=135, threshold=2))
    f_tag = ImageFont.truetype(FONT_BLACK, 48)
    f_big = ImageFont.truetype(FONT_BLACK, 68)
    f_sub = ImageFont.truetype(FONT_BOLD, 48)

    bar_x0, bar_x1 = 110, 970
    bar_max_w = bar_x1 - bar_x0

    frames = []
    denom = float(max(1, frames_n - 1))
    for i in range(frames_n):
        u = i / denom
        prog = max(0.0, min(1.0, u / 0.72))
        ease = 0.5 - 0.5 * math.cos(math.pi * prog)

        bg = starfield_frame(u, dx=80.0, dy=60.0)
        fg = Image.fromarray(bg.astype(np.uint8), "RGB").convert("RGBA")
        d = ImageDraw.Draw(fg)

        for rr in (290, 440, 610):
            d.arc((W // 2 - rr, 500 - rr, W // 2 + rr, 500 + rr), 18, 162, fill=(105, 168, 240, 82), width=3)
            d.arc((W // 2 - rr, 500 - rr, W // 2 + rr, 500 + rr), 198, 342, fill=(105, 168, 240, 82), width=3)

        centred(d, 185, "58 MILLION KM", f_tag, WHITE, stroke=6)
        fg.alpha_composite(g_merc, ((W - 380) // 2, 265))

        # Single word-matched animated sunlight scale inside the 16:9 safe band (y=656..1264)
        sun_mult = 1.0 + 6.0 * ease
        w_sun = max(24, round(bar_max_w * (sun_mult / 7.2)))
        w_earth = round(bar_max_w * (1.0 / 7.2))

        centred(d, 745, f"UP TO {sun_mult:.1f}× SUNLIGHT", f_big, YELLOW, stroke=7)
        d.rounded_rectangle((bar_x0, 855, bar_x1, 920), radius=18, outline=(170, 200, 235, 220), width=4)
        d.rounded_rectangle((bar_x0, 855, bar_x0 + w_sun, 920), radius=18, fill=YELLOW)
        # Earth 1x reference marker
        d.rounded_rectangle((bar_x0, 855, bar_x0 + w_earth, 920), radius=18, fill=(90, 195, 255, 255))
        for k_tick in range(1, 7):
            tx = bar_x0 + round(bar_max_w * (k_tick / 7.2))
            d.line((tx, 855, tx, 920), fill=(16, 26, 46, 175), width=3)

        centred(d, 975, "BRIGHTER THAN EARTH", f_sub, (210, 228, 252, 255), stroke=5)

        arr = lift_navy(np.asarray(fg.convert("RGB"), dtype=np.float32))
        frames.append(Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8), "RGB"))

    pipe_frames(frames, dest)
    return 1.0


def render_cg_night(frames_n: int, dest: Path) -> float:
    """Native 1080x1920 vertical animated explainer #2 (R03d, 20.042-23.458 s):
    Real MESSENGER Mercury globe + animated +430 °C HEAT vs -180 °C NIGHT plunge contrast
    in 68 px house type inside the 16:9 safe band (y=656..1264)."""
    g_merc = make_globe_rgba(NAS_HARV / "PIA16853.jpg", 330, sat=1.24)
    f_tag = ImageFont.truetype(FONT_BLACK, 48)
    f_big = ImageFont.truetype(FONT_BLACK, 68)
    f_sub = ImageFont.truetype(FONT_BOLD, 46)

    bar_x0, bar_x1 = 110, 970
    bar_max_w = bar_x1 - bar_x0

    frames = []
    denom = float(max(1, frames_n - 1))
    for i in range(frames_n):
        u = i / denom
        ease = 0.5 - 0.5 * math.cos(math.pi * min(1.0, u / 0.72))
        night_c = int(round(-180.0 * ease))
        w_day = round(bar_max_w * 0.92)
        w_night = max(24, round(bar_max_w * (0.10 + 0.62 * ease)))

        bg = starfield_frame(1.0 - u * 0.8, dx=90.0, dy=65.0)
        fg = Image.fromarray(bg.astype(np.uint8), "RGB").convert("RGBA")
        d = ImageDraw.Draw(fg)

        for rr in (290, 440, 610):
            d.arc((W // 2 - rr, 500 - rr, W // 2 + rr, 500 + rr), 18, 162, fill=(105, 195, 245, 72), width=3)
            d.arc((W // 2 - rr, 500 - rr, W // 2 + rr, 500 + rr), 198, 342, fill=(105, 195, 245, 72), width=3)

        centred(d, 185, "WITHOUT AN ATMOSPHERE", f_tag, CYAN, stroke=6)
        fg.alpha_composite(g_merc, ((W - 330) // 2, 270))

        d.text((bar_x0, 685), "+430 °C HEAT", font=f_big, fill=CORAL, stroke_width=6, stroke_fill=(16, 26, 46, 255))
        d.rounded_rectangle((bar_x0, 775, bar_x1, 825), radius=16, outline=(170, 200, 235, 210), width=3)
        d.rounded_rectangle((bar_x0, 775, bar_x0 + w_day, 825), radius=16, fill=CORAL)

        d.text((bar_x0, 900), f"{night_c} °C NIGHT", font=f_big, fill=CYAN, stroke_width=6, stroke_fill=(16, 26, 46, 255))
        d.rounded_rectangle((bar_x0, 990, bar_x1, 1040), radius=16, outline=(170, 200, 235, 210), width=3)
        d.rounded_rectangle((bar_x0, 990, bar_x0 + w_night, 1040), radius=16, fill=CYAN)

        d.text((bar_x0, 1095), "NIGHT PLUNGE", font=f_sub, fill=YELLOW, stroke_width=5, stroke_fill=(16, 26, 46, 255))

        arr = lift_navy(np.asarray(fg.convert("RGB"), dtype=np.float32))
        frames.append(Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8), "RGB"))

    pipe_frames(frames, dest)
    return 1.0


def render_shot(shot: dict, dest: Path, open_f0: Path | None = None) -> float:
    frames_n = shot["f1"] - shot["f0"]
    kind = shot["kind"]
    if kind == "mercury_spin":
        up = render_mercury_spin(
            frames_n,
            lon_start_deg=float(shot["lon_start_deg"]),
            lon_rate_deg_s=float(shot["lon_rate_deg_s"]),
            dest=dest,
            zoom0=1.00, zoom1=1.07,
            open_f0=open_f0,
            star_u0=0.0, star_u1=0.65,
        )
        shutil.copy2(dest, WORK / "exports" / shot["source"])
        return up
    if kind == "mercury_loop":
        dur_s = frames_n / FPS
        lon_rate = float(shot["lon_rate_deg_s"])
        lon_target = float(shot["lon_target_deg"])
        # End exactly 1 frame before Frame 0 angle so loop into t=0.00s is seamless!
        lon_start = lon_target - lon_rate * dur_s
        up = render_mercury_spin(
            frames_n,
            lon_start_deg=lon_start,
            lon_rate_deg_s=lon_rate,
            dest=dest,
            zoom0=0.97, zoom1=1.00,
            open_f0=None,
            star_u0=-0.20, star_u1=0.0,
        )
        shutil.copy2(dest, WORK / "exports" / shot["source"])
        return up
    if kind == "surface_pan":
        return render_surface_pan(shot, dest)
    if kind == "polar_cover":
        return render_polar_cover(shot, dest)
    if kind == "still_orb":
        base, up = build_orb_base(shot)
        render_symmetric_zoom(base, frames_n, float(shot["z0"]), float(shot["z1"]), dest)
        return up
    if kind == "cg_sunlight":
        up = render_cg_sunlight(frames_n, dest)
        shutil.copy2(dest, WORK / "exports" / shot["source"])
        return up
    if kind == "cg_night":
        up = render_cg_night(frames_n, dest)
        shutil.copy2(dest, WORK / "exports" / shot["source"])
        return up
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
            # Keep British spelling "kilometres" matching locked script v04
            if txt.lower() == "kilometers":
                txt = "kilometres"
            words.append({"text": txt, "w": txt, "s": s, "e": e, "start": s, "end": e})
        local = round(local + dur_s, 3)
        if si < len(VO_GAPS):
            local = round(local + VO_GAPS[si], 3)
    return slices, words, words[-1]["e"]


def make_hook(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(H * 0.082 / 0.72)
    if f.size > 134:
        f = ImageFont.truetype(FONT_BLACK, 134)
    while max(d.textlength(t, font=f) for t, _ in HOOK_ROWS) > W * 0.84:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
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
    f = font_for(LINE_H * 0.86)
    while d.textlength(text, font=f) > W * 0.82:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y1 - 92, text, f, YELLOW, stroke=7)
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
    """Full spoken-word SRT cues covering 100% of VO including 9-14 s (never drop YouTube CC lines)."""
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
    im = ImageEnhance.Color(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    d = ImageDraw.Draw(im)
    size = 76
    while size < 134:
        trial = ImageFont.truetype(FONT_BLACK, size + 2)
        if max(d.textlength(r, font=trial) for r, _ in COVER_ROWS) > W * 0.78:
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
            "-af", f"afade=t=in:d=0.008,afade=t=out:st={max(0.0, seg - 0.008):.3f}:d=0.008",
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
        held = np.array([need[max(0, i - 3):min(m, i + 4)].max() for i in range(m)])
        duck[:m] = np.minimum(duck[:m] + held, 18)
        env = np.convolve(np.interp(T, grid, duck, left=0, right=0), np.ones(k) / k, mode="same")
        write_wav(bed * (10 ** (-env / 20))[:, None], bed_wav)

    hits = [
        ("whoosh", 0.00, -6.0),
        ("rumble", 0.20, -10.5),
        ("tick", TITLE_IN, -8.5),
        ("tick", 14.08, -8.5),
        ("tick", 20.04, -8.5),
        ("tick", TEACH_IN, -8.5),
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


def copy_verified(src: Path, dst: Path) -> None:
    if dst.exists():
        raise SystemExit(f"Refusing to overwrite existing NAS file: {dst}")
    shutil.copy2(src, dst)
    if sha256(src) != sha256(dst):
        raise SystemExit(f"SHA-256 mismatch copying {src} -> {dst}")


def main() -> None:
    if (NAS_SUB_OUT / f"{STEM}.mp4").exists() or (NAS_SHORTS / f"{STEM}.mp4").exists():
        raise SystemExit(f"Target {STEM}.mp4 already exists on NAS; bump version.")

    vo_sha = sha256(VO_WAV)
    if vo_sha != EXPECTED_VO_SHA256:
        raise SystemExit(f"VO sha256 mismatch: {vo_sha} != {EXPECTED_VO_SHA256}")
    bed_sha = sha256(BED_MP3)
    if bed_sha != EXPECTED_BED_SHA256:
        raise SystemExit(f"Bed sha256 mismatch: {bed_sha} != {EXPECTED_BED_SHA256}")
    master_sha = sha256(MASTER_V03)
    if master_sha != EXPECTED_MASTER_SHA256:
        raise SystemExit(f"Master v03 sha256 mismatch: {master_sha} != {EXPECTED_MASTER_SHA256}")
    print(f"Verified SHA-256s: VO={vo_sha[:12]}... Bed={bed_sha[:12]}... Master_v03={master_sha[:12]}...", flush=True)

    # Verify shot frame continuity
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
        f"[3:v]format=rgba,fade=t=in:st={END_CARD_IN:.3f}:d=0.22:alpha=1[ec]",
        f"[v2][ec]overlay=0:0:enable='gte(t,{END_CARD_IN:.3f})'[v3]",
        f"[4:v]format=rgba,fade=t=in:st={TEACH_IN}:d=0.22:alpha=1,fade=t=out:st={TEACH_OUT - 0.22:.2f}:d=0.22:alpha=1[th]",
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
    write_srt(srt_chunks_full(words, last_word_end), srt_path)
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
        "relatedVideoId": None,
        "parent_long_film": "OWB:064",
        "parent_long_title": LONG_TITLE,
        "parent_master_v03_sha256": master_sha,
        "spoken": joined,
        "vo_onset_s": words[0]["s"],
        "last_word_end_s": last_word_end,
        "duration_s": TOTAL_S,
        "fps": FPS,
        "hook": {"text": hook_info["text"], "start_s": 0.0, "end_s": HOOK_END},
        "hook_caption": {"text": hook_info["text"], "start_s": 0.0, "end_s": HOOK_END},
        "title_banner": {"text": LONG_TITLE, "start_s": TITLE_IN, "end_s": TITLE_OUT},
        "teach_overlay": {"text": TEACH_TEXT, "start_s": TEACH_IN, "end_s": TEACH_OUT, "bbox": teach_bb},
        "end_card": {"start_s": round(END_CARD_IN, 3), "len_s": round(TOTAL_S - END_CARD_IN, 3)},
        "words_file": str(words_path),
        "vo": str(vo_stem_out),
        "audio": aud,
    }
    meta_path.write_text(json.dumps(meta_obj, indent=2) + "\n")

    frame0_jpg = OUT_WORK / f"{STEM}_frame0.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.00", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(frame0_jpg)])
    cover_jpg = OUT_WORK / f"{STEM}_cover.jpg"
    cover_info = make_cover(cover_jpg, open_f0)

    # Build 12-shot inspection contact sheet (every cut midpoint)
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
        d_t.text((8, 8), f"{idx + 1:02d} {shot['row']} ({mid_t:.1f}s)", fill=(255, 255, 255))
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
        "master_v03_sha256": master_sha,
        "vo_sha256": vo_sha,
        "bed_sha256": bed_sha,
        "duration_s": TOTAL_S,
        "fps": FPS,
        "frames": TOTAL_FRAMES,
        "words_count": len(words),
        "vo_onset_s": words[0]["s"],
        "s01_s02_breath_s": round(words[16]["s"] - words[15]["e"], 3),
        "last_word_end_s": last_word_end,
        "tail_gap_s": round(TOTAL_S - last_word_end, 3),
        "cut1_s": round(SHOT_PLAN[0]["f1"] / FPS, 3),
        "cut2_s": round(SHOT_PLAN[1]["f1"] / FPS, 3),
        "max_shot_s": max(round((s["f1"] - s["f0"]) / FPS, 3) for s in SHOT_PLAN),
        "audio": aud,
        "hook": hook_info,
        "title": title_info,
        "teach": {"text": TEACH_TEXT, "in": TEACH_IN, "out": TEACH_OUT, "bbox": teach_bb},
        "end_card": {"start_s": round(END_CARD_IN, 3), "len_s": round(TOTAL_S - END_CARD_IN, 3)},
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

    # Re-run gate_shorts_open, polish_gate, and picture_qa on canonical NAS copy so all reports record NAS paths
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
