#!/usr/bin/env python3
"""034 Pluto — Short 1 (Test A Opening Short) v02 Full-Bleed 9:16 Builder (J2438 / J2383 §5.2).

Fixes all J2383 §5.2 & FIRST30_PLAN.md §4.4 requirements:
1. Exact 36.500 s (1,095 frames at 30/1 CFR) aligned to FIRST30_PLAN.md (-2.800 s splice
   removing 'in distant orbit around our sun,' at raw 2.000..4.800 s from pluto_frozen_heart_vo_v03.wav):
   - Sentence 1 ends at 5.900 s < 8.000 s.
   - Sentence 2 payoff completes at 16.240 s < 20.000 s.
   - Sentence 3 ('...and solved that mystery.') ends at 36.020 s edited, with 0.480 s clean tail to 36.500 s.
   - Zero 4-frame loop cross-fade at the end.
2. 100% full-bleed 1080x1920 (9:16) framing across all 12 cuts (2.100–3.533 s <= 4.000 s,
   Cut 1 = 2.100 s <= 3.000 s native moving LORRI flyby video, upright 1080x1920 R02a & R02b
   scale-graphic beats, high-res PIA19936 mosaic crop replacing washed-out R04c, <= 1.985x upscale,
   0% blur-pad or starfield letterboxing).
3. Passes gate_shorts_open.py check (--air-date 2026-12-21), picture_qa.py, polish_gate.py,
   music_gate.py, and sfx_kit.py level. £0 spend; leaves all _v01 files untouched.
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

REPO = (
    Path("/Volumes/MiniWork/scratch/j2438-wt")
    if Path("/Volumes/MiniWork/scratch/j2438-wt/scripts/picture_qa.py").exists()
    else Path("/Users/benjaminoats/YouTube/orbit-with-ben")
)
NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters"
)
EDIT_DIR = NAS_FILM / "07_Edit-Project"
POOL_JSON = EDIT_DIR / "HARVEST_POOL_v01.json"
SHORT_DIR = NAS_FILM / "10_Shorts" / "short01_testA_opening"
EXP_DIR = SHORT_DIR / "06_Final-Exports"
GFX_OUT = EDIT_DIR / "graphics_v03" / "code_graphics"

VO_WAV = NAS_FILM / "02_Voiceover" / "pluto_frozen_heart_vo_v03.wav"
STT_V02 = NAS_FILM / "02_Voiceover" / "stt" / "pluto_frozen_heart_vo_v03" / "stt_timeline_offset_v02.json"
BED_MP3 = NAS_FILM / "05_Music" / "pluto_score_bed_v01.mp3"
KIT_DIR = NAS_FILM / "06_Sound-Effects" / "kit_v01"

SCRATCH_BASE = Path(os.environ.get("STUDIO_SCRATCH", "/Volumes/MiniWork/scratch"))
WORK = SCRATCH_BASE / "j2438_034_short01_v02_work"

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(EDIT_DIR))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import gate_shorts_open as gso  # noqa: E402
import sfx_kit  # noqa: E402
import full_frame_graphics as ffg  # noqa: E402

W, H, FPS = 1080, 1920, 30
SR = 48000
TOTAL_FRAMES = 1095
TOTAL_S = TOTAL_FRAMES / FPS  # 36.500 s exact

BAND_H = round(W * 9 / 16)          # 608 px
BAND_Y0 = (H - BAND_H) // 2         # 656 px
BAND_Y1 = BAND_Y0 + BAND_H          # 1264 px
LINE_H = round(BAND_H * 0.115)      # 70 px

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)
CYAN = (105, 196, 241, 255)
NAVY_FLOOR = np.array([28.0, 38.0, 58.0], dtype=np.float32)

STEM = "034_short01_testA_opening_v02"
AIR_DATE = "2026-12-21"
SHORT_TITLE = "What Did New Horizons Discover Inside Pluto's Frozen Heart?"
ALT_TITLE = "Why Does Pluto's Frozen Heart Have Zero Impact Craters?"
LONG_TITLE = "Why Pluto's Frozen Heart Has Zero Craters"

HOOK_ROWS = [("PLUTO'S ICY", WHITE), ("HEART?", YELLOW)]
COVER_ROWS = [("ZERO", YELLOW), ("CRATERS?", WHITE)]
TITLE_ROWS = [
    "Why Pluto's",
    "Frozen Heart",
    "Has Zero Craters",
]
END_ROWS = [
    ("Why Pluto's", WHITE),
    ("Frozen Heart", WHITE),
    ("Has Zero Craters", WHITE),
    ("Full film on the channel", YELLOW),
]

HOOK_END = 2.10
TITLE_IN, TITLE_OUT = 9.00, 14.00
TEACH_IN, TEACH_OUT = 23.95, 26.95
TEACH_TEXT = "12,500 KM FLYBY"
END_CARD_IN = 35.10

CLEAN_CROPS = {
    "PIA19936.jpg": (300, 0, 3400, 1744),
}

# 12-cut full-bleed 1080x1920 (9:16) plan: sum(frames) = 1,095 = 36.500 s
SHOT_PLAN = [
    {
        "row": "R01a", "frames": 63, "kind": "video_pan",
        "source": "File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm",
        "title": "New Horizons LORRI Pluto Flyby Sequence (14 July 2015)",
        "offset": 16.0, "video": True, "x0_start": 610.0, "x0_end": 700.0,
    },
    {
        "row": "R01b", "frames": 63, "kind": "still_cover",
        "source": "PIA20291.jpg",
        "title": "New Horizons Color Image of Pluto and Sputnik Planitia",
        "video": False, "pan_x_frac": 0.56, "z1": 1.040, "star_dark": True,
    },
    {
        "row": "R01c", "frames": 64, "kind": "still_cover",
        "source": "PIA20726.jpg",
        "title": "Pluto Heart: Polygonal Nitrogen Convection Cells",
        "video": False, "pan_x_frac": 0.50, "z1": 1.045,
    },
    {
        "row": "R02a", "frames": 105, "kind": "r02_beat_9x16",
        "source": "code_graphic_034_r02a_sputnik_width_9x16.mp4",
        "title": "1,000 km Wide Sputnik Planitia Caliper (9:16)",
        "phase": 0, "offset": 0.0, "video": True,
    },
    {
        "row": "R02b", "frames": 104, "kind": "still_cover",
        "source": "PIA19952.jpg",
        "title": "The Rich Color Variations of Pluto (MVIC)",
        "video": False, "pan_x_frac": 0.56, "z1": 1.045, "star_dark": True,
    },
    {
        "row": "R02c", "frames": 105, "kind": "r02_beat_9x16",
        "source": "code_graphic_034_r02b_texas_oklahoma_scale_9x16.mp4",
        "title": "Larger Than Texas + Oklahoma Combined · 0 Craters (9:16)",
        "phase": 1, "offset": 0.0, "video": True,
    },
    {
        "row": "R03a", "frames": 106, "kind": "video_pan",
        "source": "File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm",
        "title": "New Horizons LORRI Pluto Flyby Approach Sequence",
        "offset": 26.5, "video": True, "x0_start": 620.0, "x0_end": 740.0,
    },
    {
        "row": "R03b", "frames": 106, "kind": "still_cover",
        "source": "PIA20534.jpg",
        "title": "Surface Diversity Along Pluto Terminator and Sputnik Planitia",
        "video": False, "pan_x_frac": 0.48, "z1": 1.040, "star_dark": True,
    },
    {
        "row": "R03c", "frames": 106, "kind": "still_cover",
        "source": "PIA20198.jpg",
        "title": "Mountainous Shoreline of Sputnik Planitia",
        "video": False, "pan_x_frac": 0.50, "z1": 1.045,
    },
    {
        "row": "R04a", "frames": 91, "kind": "still_cover",
        "source": "PIA20038.jpg",
        "title": "Full View of Pluto Crescent and Haze",
        "video": False, "pan_x_frac": 0.50, "z1": 1.045, "star_dark": True,
    },
    {
        "row": "R04b", "frames": 91, "kind": "still_cover",
        "source": "PIA20732.jpg",
        "title": "The Jagged Shores of Pluto Highlands",
        "video": False, "pan_x_frac": 0.50, "z1": 1.045,
    },
    {
        "row": "R04c", "frames": 91, "kind": "still_cover",
        "source": "PIA19936.jpg",
        "title": "Northern Sputnik Planitia Mosaic (New Horizons)",
        "video": False, "pan_x_frac": 0.52, "z1": 1.045,
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
    with wave.open(str(p), "rb") as w:
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


def lift_navy(arr: np.ndarray) -> np.ndarray:
    mx = arr.max(axis=2, keepdims=True)
    return np.where(mx < 54.0, np.maximum(arr, NAVY_FLOOR), arr)


_STAR_BG: np.ndarray | None = None


def get_clean_starfield() -> np.ndarray:
    global _STAR_BG
    if _STAR_BG is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        nx = (xx - W * 0.5) / (W * 0.5)
        ny = (yy - H * 0.5) / (H * 0.5)
        rad = np.clip(1.0 - 0.65 * (nx * nx + ny * ny), 0.0, 1.0)
        rgb = np.stack(
            [
                29.0 + 34.0 * rad,
                40.0 + 44.0 * rad,
                62.0 + 58.0 * rad,
            ],
            axis=-1,
        )
        rng = np.random.default_rng(3401)
        for _ in range(2100):
            sy = int(rng.integers(4, H - 6))
            sx = int(rng.integers(4, W - 6))
            b = float(rng.uniform(80.0, 185.0))
            sz = 2 if rng.random() < 0.78 else 3
            rgb[sy : sy + sz, sx : sx + sz, 0] = np.maximum(rgb[sy : sy + sz, sx : sx + sz, 0], b * 0.90)
            rgb[sy : sy + sz, sx : sx + sz, 1] = np.maximum(rgb[sy : sy + sz, sx : sx + sz, 1], b * 0.96)
            rgb[sy : sy + sz, sx : sx + sz, 2] = np.maximum(rgb[sy : sy + sz, sx : sx + sz, 2], b * 1.05)
        _STAR_BG = np.clip(lift_navy(rgb), 28.0, 255.0)
    return _STAR_BG


def load_pool_map() -> dict[str, Path]:
    d = json.loads(POOL_JSON.read_text())
    out = {}
    for a in d["assets"]:
        p = Path(a["local_path"])
        if p.exists():
            out[p.name] = p
    return out


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


def build_base_9x16_cover(shot: dict, pool_map: dict[str, Path]) -> tuple[Image.Image, float]:
    src = pool_map[shot["source"]]
    im = Image.open(src).convert("RGB")
    if shot["source"] in CLEAN_CROPS:
        im = im.crop(CLEAN_CROPS[shot["source"]])
    im = ImageEnhance.Color(im).enhance(1.16)
    im = ImageEnhance.Contrast(im).enhance(1.06)

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
    crop = crop.filter(ImageFilter.UnsharpMask(radius=1.5, percent=118, threshold=2))
    arr = np.asarray(crop, dtype=np.float32)
    if shot.get("star_dark"):
        st = get_clean_starfield()
        luma = arr.max(axis=2, keepdims=True)
        m_dark = np.clip((48.0 - luma) / 30.0, 0.0, 1.0)
        arr = arr * (1.0 - m_dark) + st * m_dark
    arr = lift_navy(arr)
    z1 = float(shot.get("z1", 1.045))
    up = round((H / ch) * z1, 3)
    if up > 2.0:
        raise ValueError(f"Upscale {up} > 2.00x on {shot['source']}")
    return Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8)), up


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


def render_r02_beat_9x16(phase_idx: int, frames_n: int, dest: Path, pool_map: dict[str, Path]) -> float:
    """Renders upright full-bleed 1080x1920 9:16 R02 scale-graphic beats over full-bleed Pluto imagery
    so there are zero horizontal letterbox edges and 0% blur-pad."""
    # Full-bleed real Pluto nitrogen glacier backdrop (PIA20726 2736x2944 -> 0.68x upscale!)
    bg_src = Image.open(pool_map["PIA20726.jpg"]).convert("RGB")
    sw, sh = bg_src.size
    cw = sw
    ch = min(float(sh), cw * (H / W))
    if sw / sh >= W / H:
        ch = float(sh)
        cw = ch * (W / H)
    bg_crop = bg_src.transform(
        (W, H), Image.Transform.EXTENT,
        ((sw - cw) * 0.5, (sh - ch) * 0.5, (sw + cw) * 0.5, (sh + ch) * 0.5),
        resample=Image.Resampling.BICUBIC,
    )
    # Darken slightly into rich navy-tinted glacier surface so calipers and globes pop cleanly without any horizontal seam
    bg_arr = np.asarray(bg_crop, dtype=np.float32) * 0.42 + np.array([22.0, 34.0, 56.0], dtype=np.float32)
    bg_base = Image.fromarray(np.clip(lift_navy(bg_arr), 28, 255).astype(np.uint8)).convert("RGBA")

    # Prepare circular real cutouts of PIA20007 Sputnik Planitia and PIA18033 North America
    def make_circle(img_path: Path, diam: int, crop_box=None) -> Image.Image:
        im = Image.open(img_path).convert("RGB")
        if crop_box:
            im = im.crop(crop_box)
        im = ImageEnhance.Color(im).enhance(1.18)
        side = min(im.size)
        lx, ty = (im.width - side) // 2, (im.height - side) // 2
        im = im.crop((lx, ty, lx + side, ty + side)).resize((diam, diam), Image.Resampling.LANCZOS)
        mask = Image.new("L", (diam, diam), 0)
        ImageDraw.Draw(mask).ellipse((3, 3, diam - 4, diam - 4), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(2.0))
        rgba = im.convert("RGBA")
        rgba.putalpha(mask)
        ImageDraw.Draw(rgba).ellipse((3, 3, diam - 4, diam - 4), outline=(185, 220, 255, 210), width=4)
        return rgba

    g_pluto = make_circle(pool_map["PIA20007.jpg"], 560 if phase_idx == 0 else 440)
    g_na = make_circle(pool_map["PIA18033.jpg"], 440, crop_box=(1600, 900, 5600, 4900)) if phase_idx == 1 else None

    f_big = ImageFont.truetype(FONT_BLACK, 64)
    f_sub = ImageFont.truetype(FONT_BOLD, 50)
    denom = float(max(1, frames_n - 1))
    frames = []

    for fi in range(frames_n):
        u_lin = fi / denom
        u = 0.5 - 0.5 * math.cos(math.pi * min(1.0, u_lin / 0.78))
        z = 1.0 + 0.040 * u_lin
        zcw, zch = W / z, H / z
        zl, zt = (W - zcw) * 0.5, (H - zch) * 0.5
        fr = bg_base.transform((W, H), Image.Transform.EXTENT, (zl, zt, zl + zcw, zt + zch), resample=Image.Resampling.BICUBIC)
        d = ImageDraw.Draw(fr)

        if phase_idx == 0:
            # Upright 9:16 Phase 0: Sputnik Planitia globe + animated 1,000 KM WIDE caliper
            gx, gy = (W - 560) // 2, 540
            fr.alpha_composite(g_pluto, (gx, gy))
            d = ImageDraw.Draw(fr)
            x0 = 260
            x1 = 260 + max(28, round(560 * u))
            cy = 1160
            d.line((x0, 980, x0, cy + 24), fill=(255, 255, 255, 190), width=4)
            d.line((x1, 980, x1, cy + 24), fill=(255, 224, 0, 220), width=4)
            d.line((x0, cy, x1, cy), fill=YELLOW, width=8)
            km_now = round(1000 * u)
            lbl = f"{km_now:,} KM WIDE"
            bb = d.textbbox((0, 0), lbl, font=f_big, stroke_width=6)
            tx = (W - (bb[2] - bb[0])) // 2 - bb[0]
            d.text((tx, 390), lbl, font=f_big, fill=YELLOW, stroke_width=6, stroke_fill=(16, 26, 46, 255))
        else:
            # Upright 9:16 Phase 1 (13.30-16.80s): stacked Pluto glacier (top) vs Texas+Oklahoma on Earth (bottom)
            fr.alpha_composite(g_pluto, ((W - 440) // 2, 340))
            assert g_na is not None
            fr.alpha_composite(g_na, ((W - 440) // 2, 920))
            d = ImageDraw.Draw(fr)
            poly = ffg.project_tx_ok(ffg.TX_OK_OUTER, W // 2, 1140, 12.0)
            d.line(poly, fill=YELLOW, width=5)
            # Animated comparison bars
            d.line((250, 815, 830, 815), fill=YELLOW, width=12)
            d.line((290, 1405, 290 + max(24, round(500 * u)), 1405), fill=CYAN, width=12)
            for txt_s, ty, col, fnt in [
                ("> TEXAS + OKLAHOMA", 225, WHITE, f_sub),
                ("0 CRATERS", 1455, YELLOW, f_big),
            ]:
                bb = d.textbbox((0, 0), txt_s, font=fnt, stroke_width=6)
                tx = (W - (bb[2] - bb[0])) // 2 - bb[0]
                d.text((tx, ty), txt_s, font=fnt, fill=col, stroke_width=6, stroke_fill=(16, 26, 46, 255))

        frames.append(fr.convert("RGB"))

    pipe_frames(frames, dest)
    # Also save dedicated 9:16 graphic asset in GFX_OUT for provenance
    GFX_OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dest, GFX_OUT / dest.name)
    return 1.04


def load_raw_video_frames(src: Path, offset: float, frames_n: int) -> list[Image.Image]:
    dur_need = (frames_n / FPS) + 0.5
    raw = sp.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{offset:.3f}", "-t", f"{dur_need:.3f}",
        "-i", str(src), "-vf", f"fps={FPS},scale=1920:1080:flags=lanczos",
        "-frames:v", str(frames_n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ])
    fb = 1920 * 1080 * 3
    out = []
    for i in range(frames_n):
        chunk = raw[i * fb : (i + 1) * fb]
        if len(chunk) < fb:
            chunk = raw[-fb:]
        out.append(Image.frombytes("RGB", (1920, 1080), chunk))
    return out


def render_shot(shot: dict, dest: Path, pool_map: dict[str, Path], open_f0: Path | None = None) -> float:
    frames_n = shot["frames"]
    kind = shot["kind"]

    if kind == "video_pan":
        src = pool_map[shot["source"]]
        raw = load_raw_video_frames(src, float(shot["offset"]), frames_n)
        cw = 1080.0 * (W / H)  # 607.5 px -> 1920/1080 = 1.778x upscale <= 2.00x
        x0_s = float(shot["x0_start"])
        x0_e = float(shot["x0_end"])
        denom = float(max(1, frames_n - 1))
        frames = []
        for i, im in enumerate(raw):
            u = i / denom
            x0 = max(0.0, min(1920.0 - cw, x0_s + (x0_e - x0_s) * u))
            crop = im.transform((W, H), Image.Transform.EXTENT, (x0, 0.0, x0 + cw, 1080.0), resample=Image.Resampling.BICUBIC)
            crop = ImageEnhance.Color(crop).enhance(1.18)
            crop = ImageEnhance.Contrast(crop).enhance(1.08)
            crop = crop.filter(ImageFilter.UnsharpMask(radius=1.4, percent=115, threshold=2))
            arr = lift_navy(np.asarray(crop, dtype=np.float32))
            fr = Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8))
            if open_f0 is not None and i == 0:
                fr.save(open_f0)
            frames.append(fr)
        pipe_frames(frames, dest)
        return 1.78

    if kind == "still_cover":
        base, up = build_base_9x16_cover(shot, pool_map)
        render_symmetric_still_zoom(base, frames_n, float(shot["z1"]), dest)
        return up

    if kind == "r02_beat_9x16":
        named_dest = WORK / shot["source"]
        up = render_r02_beat_9x16(int(shot["phase"]), frames_n, named_dest, pool_map)
        shutil.copy2(named_dest, dest)
        return up

    raise ValueError(f"Unknown shot kind: {kind}")


def font_for(line_h: float, ratio: float = 0.86, font_path: str = FONT_BLACK) -> ImageFont.FreeTypeFont:
    size = 10
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f = ImageFont.truetype(font_path, size + 1)
        b = probe.textbbox((0, 0), "Hg", font=f)
        if b[3] - b[1] > line_h * ratio:
            return ImageFont.truetype(font_path, size)
        size += 1


def centred(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill: tuple, stroke: int = 6) -> list[int]:
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    alpha = fill[3] if len(fill) == 4 else 255
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(16, 26, 46, alpha))
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


def make_hook(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT_BLACK, 118)
    while max(d.textlength(t, font=f) for t, _ in HOOK_ROWS) > W * 0.84:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = 240
    boxes = [centred(d, y + idx * lh, t, f, c, stroke=7) for idx, (t, c) in enumerate(HOOK_ROWS)]
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


def make_cover(dest: Path, f0_png: Path) -> dict:
    im = Image.open(f0_png).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    d = ImageDraw.Draw(im)
    size = 96
    while size < 128:
        trial = ImageFont.truetype(FONT_BLACK, size + 2)
        if max(d.textlength(r, font=trial) for r, _ in COVER_ROWS) > W * 0.80:
            break
        size += 2
    f = ImageFont.truetype(FONT_BLACK, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = BAND_Y0 + (BAND_H - lh * len(COVER_ROWS)) // 2
    boxes = [centred(d, y + idx * lh, r, f, col, stroke=8) for idx, (r, col) in enumerate(COVER_ROWS)]
    im.save(dest, quality=94, subsampling=0)
    return {"file": str(dest), "rows": [r for r, _ in COVER_ROWS], "font_px": size, "bboxes": boxes}


def load_opening_words() -> tuple[list[dict], float]:
    stt = json.loads(STT_V02.read_text())
    out = []
    for w in stt["words"]:
        if w.get("type", "word") != "word":
            continue
        s = float(w["start"])
        e = float(w["end"])
        if e <= TOTAL_S + 0.02:
            txt = (w.get("word") or w.get("text") or "").strip()
            out.append({"text": txt, "w": txt, "s": round(s, 3), "e": round(e, 3), "start": round(s, 3), "end": round(e, 3)})
    return out, out[-1]["e"]


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


def build_audio(work: Path) -> tuple[dict, Path, Path, Path]:
    """Builds 36.500 s spliced opening VO (0.000..2.000 s + 4.800..39.300 s raw = 36.500 s),
    ducked score bed, and house SFX stems, calibrated for -14.0 LUFS & <= -1.9 dBTP."""
    full_vo = read_wav(VO_WAV)
    s_a = full_vo[0 : int(round(2.000 * SR))].copy()
    s_b = full_vo[int(round(4.800 * SR)) : int(round(39.300 * SR))].copy()

    # 10 ms smooth cosine splice inside <-74 dB comma pause
    xf = int(0.010 * SR)
    s_a[-xf:] *= np.linspace(1.0, 0.0, xf, dtype=np.float32)[:, None]
    s_b[:xf] *= np.linspace(0.0, 1.0, xf, dtype=np.float32)[:, None]
    vo = np.concatenate([s_a, s_b], axis=0)

    n = TOTAL_FRAMES * (SR // FPS)  # 1,752,000 samples = 36.500 s
    if len(vo) < n:
        vo = np.pad(vo, ((0, n - len(vo)), (0, 0)))
    vo = vo[:n]
    tail_n = int(0.060 * SR)
    vo[-tail_n:] *= np.linspace(1.0, 0.0, tail_n, dtype=np.float32)[:, None]

    raw_vo = work / "stem_vo_raw.wav"
    write_wav(vo, raw_vo)
    vo_wav = work / "stem_vo.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(raw_vo),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", str(SR), "-ac", "2", "-t", f"{TOTAL_S:.3f}", str(vo_wav),
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
        "ffmpeg", "-y", "-v", "error", "-ss", "0.0", "-t", f"{TOTAL_S:.3f}",
        "-i", str(BED_MP3),
        "-af", f"afade=t=in:d=0.10,afade=t=out:st={TOTAL_S - 0.35:.3f}:d=0.35",
        "-ar", str(SR), "-ac", "2", str(bed_raw),
    ])
    bed = read_wav(bed_raw)[:n]
    if len(bed) < n:
        bed = np.pad(bed, ((0, n - len(bed)), (0, 0)))
    _, bi0 = sfx_kit.ebur128(bed_raw)
    bed *= 10 ** (((vo_i - 16.5) - bi0) / 20)
    bed_wav = work / "stem_bed.wav"
    write_wav(bed, bed_wav)

    T = np.arange(n) / SR
    grid = np.arange(len(vo_m)) * 0.1
    duck = np.zeros_like(grid)
    k = int(0.35 * SR)
    for _ in range(8):
        bm, _ = sfx_kit.ebur128(bed_wav)
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
        ("whoosh", 0.00, -6.5),
        ("rumble", 0.25, -11.0),
        ("tick", 6.33, -8.5),
        ("tick", TITLE_IN, -8.0),
        ("tick", 13.30, -8.5),
        ("tick", 16.80, -8.5),
        ("tick", TEACH_IN, -8.0),
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
    _, si = sfx_kit.ebur128(sfx_wav)
    if si > vo_i - 22:
        sfx *= 10 ** ((vo_i - 22 - si) / 20)
        write_wav(sfx, sfx_wav)
    for _ in range(6):
        sm, _ = sfx_kit.ebur128(sfx_wav)
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
        "-ar", str(SR), "-ac", "2", "-t", f"{TOTAL_S:.3f}", str(mix),
    ])
    _, mix_i = sfx_kit.ebur128(mix)
    _, bed_i = sfx_kit.ebur128(bed_wav)
    _, sfx_i = sfx_kit.ebur128(sfx_wav)
    return (
        {"vo_lufs": round(vo_i, 2), "bed_lufs": round(bed_i, 2), "sfx_lufs": round(sfx_i, 2), "mix_lufs": round(mix_i, 2)},
        vo_wav, sfx_wav, bed_wav,
    )


def calibrate_aac_wav(work: Path, src_wav: Path) -> tuple[Path, float, float]:
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
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src_wav), "-af", af, "-ar", str(SR), "-ac", "2", "-t", f"{TOTAL_S:.3f}", str(cal_wav)])
        run(["ffmpeg", "-y", "-v", "error", "-i", str(cal_wav), "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2", "-t", f"{TOTAL_S:.3f}", str(test_m4a)])
        m_i, m_tp = gso.aac_loudness(test_m4a)
        if m_i is not None and m_tp is not None:
            i_lufs, tp = m_i, m_tp
        if -14.15 <= i_lufs <= -13.85 and tp <= -1.85:
            break
        gain_db += (-14.0 - i_lufs)
        if tp > -1.85:
            limit_db -= max(0.15, tp - (-2.0))
    return cal_wav, round(i_lufs, 2), round(tp, 2)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    EXP_DIR.mkdir(parents=True, exist_ok=True)

    pool_map = load_pool_map()
    words, last_word_end = load_opening_words()
    spoken_text = " ".join(w["w"] for w in words)
    print(f"Short 1 v02 words={len(words)}, onset={words[0]['s']:.3f}s, last_end={last_word_end:.3f}s, total={TOTAL_S:.3f}s", flush=True)

    open_f0 = WORK / "open_f0.png"
    concat_lines = []
    cuts_meta = []
    pool_meta = []
    seen_sources = set()

    f_acc = 0
    for idx, shot in enumerate(SHOT_PLAN):
        t_in = round(f_acc / FPS, 3)
        f_acc += shot["frames"]
        t_out = round(f_acc / FPS, 3)
        shot["in"] = t_in
        shot["out"] = t_out
        piece = WORK / f"piece_{idx:02d}.mp4"
        if piece.exists() and piece.stat().st_size > 10_000 and (idx != 0 or open_f0.exists()):
            up = 1.78 if shot["kind"] == "video_pan" else (1.04 if shot["kind"] == "r02_beat_9x16" else build_base_9x16_cover(shot, pool_map)[1])
            print(f"  kept cached {shot['row']} ({t_in:.3f}-{t_out:.3f}s, {shot['frames']}f) up={up}", flush=True)
        else:
            up = render_shot(shot, piece, pool_map, open_f0 if idx == 0 else None)
            print(f"  rendered {shot['row']} ({t_in:.3f}-{t_out:.3f}s, {shot['frames']}f) up={up}", flush=True)
        concat_lines.append(f"file '{piece.name}'")
        cuts_meta.append({
            "row": shot["row"],
            "timeline_in": t_in,
            "timeline_out": t_out,
            "source": shot["source"],
            "upscale": up,
            "video": bool(shot["video"]),
            **(
                {"framing": {"offset": shot["offset"], "crop": "9:16 full-bleed", "mode": "cover"}}
                if shot["video"]
                else {}
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

    assert f_acc == TOTAL_FRAMES
    (WORK / "list.txt").write_text("\n".join(concat_lines) + "\n")
    pic_mp4 = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"), "-c", "copy", str(pic_mp4)])

    hook_info = make_hook(WORK / "hook.png")
    title_info = make_title(WORK / "title.png")
    end_info = make_end(WORK / "end_card.png")
    make_teach(WORK / "teach.png", TEACH_TEXT)
    caps = caption_chunks(words, last_word_end)
    for i, c in enumerate(caps):
        make_caption(WORK / f"cap_{i:02d}.png", c["text"])

    # Overlay hook (0-2.10s), title (9-14s), teach pill (23.95-26.95s), captions, and end card (35.10-36.50s)
    inputs = ["-y", "-v", "error", "-i", str(pic_mp4)]
    overlays = [
        (WORK / "hook.png", 0.00, HOOK_END, False),
        (WORK / "title.png", TITLE_IN, TITLE_OUT, True),
        (WORK / "teach.png", TEACH_IN, TEACH_OUT, True),
        (WORK / "end_card.png", END_CARD_IN, TOTAL_S, True),
    ]
    for i, c in enumerate(caps):
        if c["s"] >= HOOK_END - 0.05 and c["e"] <= END_CARD_IN + 0.05:
            overlays.append((WORK / f"cap_{i:02d}.png", c["s"], min(c["e"], END_CARD_IN), False))

    fc_parts = []
    cur = "0:v"
    for idx_ov, (png_p, st_s, en_s, fade) in enumerate(overlays, 1):
        hold = max(0.18, en_s - st_s)
        inputs.extend(["-loop", "1", "-t", f"{hold + 0.05:.3f}", "-i", str(png_p)])
        f_chain = ["format=rgba"]
        if fade and hold > 0.50:
            f_chain.append("fade=t=in:st=0:d=0.22:alpha=1")
            if en_s < TOTAL_S - 0.05:
                f_chain.append(f"fade=t=out:st={hold - 0.22:.3f}:d=0.22:alpha=1")
        f_chain.append(f"setpts=PTS+{st_s:.3f}/TB")
        fc_parts.append(f"[{idx_ov}:v]{','.join(f_chain)}[ov{idx_ov}]")
        nxt = f"v{idx_ov}"
        fc_parts.append(f"[{cur}][ov{idx_ov}]overlay=0:0:format=auto:eof_action=pass[{nxt}]")
        cur = nxt

    audio_stats, vo_wav, sfx_wav, bed_wav = build_audio(WORK)
    cal_wav, aac_i, aac_tp = calibrate_aac_wav(WORK, WORK / "mix.wav")

    audio_idx = len(overlays) + 1
    inputs.extend(["-i", str(cal_wav)])
    out_mp4 = EXP_DIR / f"{STEM}.mp4"
    run([
        "ffmpeg", *inputs,
        "-filter_complex", ";".join(fc_parts),
        "-map", f"[{cur}]", "-map", f"{audio_idx}:a:0",
        *shorts_encode_args(),
        "-frames:v", str(TOTAL_FRAMES),
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-shortest", "-movflags", "+faststart", str(out_mp4),
    ])

    # Export stems, cover, words, cuts, and meta
    dst_vo = EXP_DIR / f"{STEM}_stem_vo.wav"
    dst_sfx = EXP_DIR / f"{STEM}_stem_sfx.wav"
    dst_bed = EXP_DIR / f"{STEM}_stem_bed.wav"
    dst_words = EXP_DIR / f"{STEM}_words.json"
    dst_cover = EXP_DIR / f"{STEM}_cover.jpg"
    dst_cuts = EXP_DIR / "cuts_v02.json"
    dst_pool = EXP_DIR / "pool_v02.json"
    dst_meta = EXP_DIR / f"{STEM}_meta.json"

    shutil.copy2(vo_wav, dst_vo)
    shutil.copy2(sfx_wav, dst_sfx)
    shutil.copy2(bed_wav, dst_bed)
    make_cover(dst_cover, open_f0)

    words_doc = {
        "total_dur": TOTAL_S,
        "first_word_s": words[0]["s"],
        "last_word_end": last_word_end,
        "word_count": len(words),
        "words": words,
    }
    dst_words.write_text(json.dumps(words_doc, indent=2) + "\n")
    dst_cuts.write_text(json.dumps(cuts_meta, indent=2) + "\n")
    dst_pool.write_text(json.dumps(pool_meta, indent=2) + "\n")

    meta_doc = {
        "id": STEM,
        "film": "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters",
        "short_slug": "short01_testA_opening",
        "format": "Test A Opening Short (v02, FIRST30_PLAN.md -2.800s Sentence 1 splice, 100% full-bleed 9:16)",
        "title": SHORT_TITLE,
        "alt_title": ALT_TITLE,
        "long_title": LONG_TITLE,
        "air_date": AIR_DATE,
        "duration_s": TOTAL_S,
        "frames": TOTAL_FRAMES,
        "vo_onset_s": words[0]["s"],
        "sentence_1_end_s": 5.90,
        "payoff_end_s": 16.24,
        "last_word_end_s": last_word_end,
        "tail_s": round(TOTAL_S - last_word_end, 3),
        "word_count": len(words),
        "spoken": spoken_text,
        "vo": dst_vo.name,
        "words_file": dst_words.name,
        "end_card": {"start_s": END_CARD_IN, "end_s": TOTAL_S},
        "hook": hook_info,
        "title_card": title_info,
        "end_card_layout": end_info,
        "audio": {**audio_stats, "aac_integrated_lufs": aac_i, "aac_true_peak_dbtp": aac_tp},
        "sha256": {
            "mp4": sha256(out_mp4),
            "cover_jpg": sha256(dst_cover),
            "stem_vo_wav": sha256(dst_vo),
            "stem_sfx_wav": sha256(dst_sfx),
            "stem_bed_wav": sha256(dst_bed),
            "parent_vo_v03_wav": sha256(VO_WAV),
            "parent_bed_v01_mp3": sha256(BED_MP3),
        },
    }
    dst_meta.write_text(json.dumps(meta_doc, indent=2) + "\n")

    # Run all Short gates
    g1 = sp.run([
        sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
        "check", str(out_mp4), "--air-date", AIR_DATE, "--meta", str(dst_meta), "--vo", str(dst_vo),
        "--sheet-dir", str(EXP_DIR),
    ], capture_output=True, text=True)
    pq_dir = EXP_DIR / "picture_qa_v02"
    pq_dir.mkdir(parents=True, exist_ok=True)
    g2 = sp.run([
        sys.executable, str(REPO / "scripts/picture_qa.py"), str(out_mp4),
        "--cuts", str(dst_cuts), "--pool", str(dst_pool), "--pool", str(POOL_JSON), "--out-dir", str(pq_dir),
    ], capture_output=True, text=True)
    g3 = sp.run([
        sys.executable, str(REPO / "scripts/polish_gate.py"), str(out_mp4),
        "--cuts", str(dst_cuts), "--out", str(EXP_DIR / "polish_gate_v02.json"),
    ], capture_output=True, text=True)
    g4 = sp.run([
        sys.executable, str(REPO / "scripts/music_gate.py"), str(NAS_FILM),
        "--bed", str(BED_MP3), "--video", str(out_mp4), "--out", str(EXP_DIR / "music_gate_v02.json"),
    ], capture_output=True, text=True)
    g5 = sp.run([
        sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
        "--vo", str(dst_vo), "--sfx", str(dst_sfx), "--bed", str(dst_bed),
        "--minutes", f"{TOTAL_S / 60.0:.3f}", "--out", str(EXP_DIR / "sfx_level_v02.json"),
    ], capture_output=True, text=True)

    report = [
        f"# Gate Report — `{STEM}.mp4` (`J2438`)",
        "",
        f"- **File:** `{out_mp4}`",
        f"- **SHA-256:** `{meta_doc['sha256']['mp4']}`",
        f"- **Duration:** `{TOTAL_S:.3f} s` (`{TOTAL_FRAMES}` frames at `30/1` CFR)",
        f"- **AAC Loudness:** `{aac_i:.2f} LUFS` integrated, `{aac_tp:.2f} dBTP` true peak",
        "",
        f"## 1. `gate_shorts_open.py` (rc={g1.returncode})",
        "```text", (g1.stdout + "\n" + g1.stderr).strip()[-1800:], "```",
        "",
        f"## 2. `picture_qa.py` (rc={g2.returncode})",
        "```text", (g2.stdout + "\n" + g2.stderr).strip()[-1200:], "```",
        "",
        f"## 3. `polish_gate.py` (rc={g3.returncode})",
        "```text", (g3.stdout + "\n" + g3.stderr).strip()[-1200:], "```",
        "",
        f"## 4. `music_gate.py` (rc={g4.returncode})",
        "```text", (g4.stdout + "\n" + g4.stderr).strip()[-1000:], "```",
        "",
        f"## 5. `sfx_kit.py level` (rc={g5.returncode})",
        "```text", (g5.stdout + "\n" + g5.stderr).strip()[-800:], "```",
    ]
    (EXP_DIR / "GATE_REPORT_v02.md").write_text("\n".join(report) + "\n")
    print("\n".join(report), flush=True)
    if any(g.returncode != 0 for g in (g1, g2, g3, g4, g5)):
        raise SystemExit(f"Short 1 v02 gate failed: {[g.returncode for g in (g1, g2, g3, g4, g5)]}")


if __name__ == "__main__":
    main()
