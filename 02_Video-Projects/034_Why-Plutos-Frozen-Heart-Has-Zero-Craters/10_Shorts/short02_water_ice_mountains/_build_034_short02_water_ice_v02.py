#!/usr/bin/env python3
"""034 Pluto — Short 2 (Keeper Question: Water-Ice Mountains) v02 Full-Bleed 9:16 Builder (J2867 / J2383 §5.3).

Fixes all J2383 §5.3 & J2867 requirements:
1. Exact 25.800 s (774 frames at 30/1 CFR), reusing the locked v01 audio stems byte-for-byte:
   - 034_short02_water_ice_mountains_v01_stem_vo.wav  (sha256 d93c149a70...)
   - 034_short02_water_ice_mountains_v01_stem_sfx.wav (sha256 2b8739fe2f...)
   - 034_short02_water_ice_mountains_v01_stem_bed.wav (sha256 dbd43603f3...)
2. 100% full-bleed 1080x1920 (9:16) framing across all 10 cuts (0.00-25.80 s, <= 1.922x upscale <= 2.00x,
   0% blur-pad or starfield letterbox, zero black left/right edge bar on R01, zero end loop cross-fade):
   - R01 (0.00-2.50 s, 75f): full-bleed 1080x1920 camera sweep + solar terminator highlight rendered strictly
     inside high-res PIA20732.jpg (2690x3412) bounds (0 black edge pixels, motion >= 15, f0diff >= 4).
   - R02-R10: 9 distinct high-resolution NASA Pluto/Earth plates and native LORRI flyby video cropped full-bleed
     1080x1920 with symmetric sub-pixel PIL BICUBIC zoom (1.000 -> 1.045) and <= 1.922x upscale.
3. Preserves locked v01 overlays + word-by-word spoken captions:
   - Frame 0 & 0.00-2.40 s Hook Caption: PLUTO'S ICE MOUNTAINS? (ICE in #FFE000 yellow, burned at t=0.00 s)
   - 9.50-13.50 s Promoted Long Title: Why Pluto's Frozen Heart Has Zero Craters
   - 18.00-21.60 s Single Teach Overlay inside 16:9 centre band (11.5% height): 2–3 KM WATER-ICE PEAKS
   - Spoken word-by-word captions below the 16:9 centre band (clear of 0.00-2.40 s and 9.50-13.50 s).
4. Passes gate_shorts_open.py check (--air-date 2026-12-23), picture_qa.py, polish_gate.py,
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


def _find_repo() -> Path:
    candidates = [
        Path("/Users/ben/_desk/worker/orbit-with-ben"),
        Path("/Users/benjaminoats/YouTube/orbit-with-ben"),
        Path(__file__).resolve().parents[4],
    ]
    for c in candidates:
        if (c / "scripts/picture_qa.py").exists():
            return c
    raise RuntimeError("Could not locate orbit-with-ben repository checkout")


REPO = _find_repo()
NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters"
)
EDIT_DIR = NAS_FILM / "07_Edit-Project"
POOL_JSON = EDIT_DIR / "HARVEST_POOL_v01.json"
SHORT_DIR = NAS_FILM / "10_Shorts" / "short02_water_ice_mountains"
EXP_DIR = SHORT_DIR / "06_Final-Exports"
GFX_OUT = EDIT_DIR / "graphics_v03" / "code_graphics"
BED_MP3 = NAS_FILM / "05_Music" / "pluto_score_bed_v01.mp3"

V01_VO = EXP_DIR / "034_short02_water_ice_mountains_v01_stem_vo.wav"
V01_SFX = EXP_DIR / "034_short02_water_ice_mountains_v01_stem_sfx.wav"
V01_BED = EXP_DIR / "034_short02_water_ice_mountains_v01_stem_bed.wav"
V01_WORDS = EXP_DIR / "034_short02_water_ice_mountains_v01_words.json"

EXPECTED_V01_SHAS = {
    "vo": "d93c149a704cabdf9b86e3e6a12179f8411942de50ac84b00512cbd0607104b7",
    "sfx": "2b8739fe2fd12e98296f871a3413861153a307b01bb881f35db830027b129764",
    "bed": "dbd43603f37fad5e2a5f8424a0a7c42b8caccab6dcc323b68ed7fd830cf06230",
    "words": "e049d3b203889fc8e154b577509033dfdf074b1fdf663cbf785065565a8f762e",
}

SCRATCH_BASE = Path(os.environ.get("STUDIO_SCRATCH", str(Path.home() / "_desk" / "scratch_work")))
WORK = SCRATCH_BASE / "j2867_034_short02_v02_work"

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import gate_shorts_open as gso  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 30
SR = 48000
TOTAL_FRAMES = 774
TOTAL_S = TOTAL_FRAMES / FPS  # 25.800 s exact

BAND_H = round(W * 9 / 16)          # 608 px
BAND_Y0 = (H - BAND_H) // 2         # 656 px
BAND_Y1 = BAND_Y0 + BAND_H          # 1264 px
LINE_H = round(BAND_H * 0.115)      # 70 px

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)
NAVY_FLOOR = np.array([28.0, 38.0, 58.0], dtype=np.float32)

STEM = "034_short02_water_ice_mountains_v02"
AIR_DATE = "2026-12-23"
SHORT_TITLE = "Why Can Towering Mountains Stand on Pluto at \u2212240\u00b0C?"
ALT_TITLE = "Why Can Towering Water-Ice Mountains Stand on Pluto?"
LONG_TITLE = "Why Pluto's Frozen Heart Has Zero Craters"

TITLE_ROWS = [
    "Why Pluto's",
    "Frozen Heart",
    "Has Zero Craters",
]

HOOK_END = 2.40
TITLE_IN, TITLE_OUT = 9.50, 13.50
TEACH_IN, TEACH_OUT = 18.00, 21.60
TEACH_TEXT = "2\u20133 KM WATER-ICE PEAKS"

CLEAN_CROPS: dict[str, tuple[int, int, int, int]] = {
    "PIA18033.jpg": (1600, 900, 4600, 5700),
    "PIA19952.jpg": (1350, 950, 3750, 4950),
    "PIA19936.jpg": (650, 0, 3446, 2558),
}

# 10-cut 100% full-bleed 1080x1920 (9:16) plan: sum(frames) = 774 = 25.800 s, all upscales <= 1.913x <= 2.00x
SHOT_PLAN = [
    {
        "row": "R01", "frames": 72, "kind": "r01_open_9x16",
        "source": "code_graphic_034_short2_r01_open_9x16.mp4",
        "title": "New Horizons Jagged Shores of Pluto Highlands Sweep (PIA20732, 9:16)",
        "offset": 0.0, "video": True,
        "note": "Full-bleed 1080x1920 camera sweep + solar terminator highlight inside 2690x3412 PIA20732.jpg (0 black edge bars).",
    },
    {
        "row": "R02", "frames": 63, "kind": "still_cover",
        "source": "PIA20473.jpg",
        "title": "The Frozen Canyons of Pluto North Pole",
        "video": False, "pan_x_frac": 0.50, "pan_y_frac": 0.50, "z1": 1.045, "star_dark": True,
        "note": "Sunlit Pluto canyons and ridges beneath starry sky ('beside a flowing glacier'; clean 2.40s scene cut).",
    },
    {
        "row": "R03", "frames": 48, "kind": "still_cover",
        "source": "PIA20726.jpg",
        "title": "Pluto Heart: Polygonal Nitrogen Glacier Convection Cells",
        "video": False, "pan_x_frac": 0.50, "pan_y_frac": 0.50, "z1": 1.045,
        "note": "Flowing polygonal nitrogen glacier cells beside Pluto's mountain walls ('between -226').",
    },
    {
        "row": "R04", "frames": 93, "kind": "still_cover",
        "source": "PIA20198.jpg",
        "title": "The Mountainous Shoreline of Sputnik Planum",
        "video": False, "pan_x_frac": 0.50, "pan_y_frac": 0.50, "z1": 1.045,
        "note": "Mountainous shoreline of Sputnik Planitia at -226 to -240 C.",
    },
    {
        "row": "R05", "frames": 84, "kind": "video_pan",
        "source": "File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm",
        "title": "New Horizons LORRI Pluto Flyby Sequence (14 July 2015)",
        "offset": 16.0, "video": True, "x0_start": 610.0, "x0_end": 710.0,
        "note": "New Horizons close-approach flyover over Sputnik Planitia shoreline mountains + promoted long title.",
    },
    {
        "row": "R06", "frames": 96, "kind": "still_cover",
        "source": "PIA18033.jpg",
        "title": "Blue Marble Earth (NASA)",
        "video": False, "pan_x_frac": 0.50, "pan_y_frac": 0.50, "z1": 1.045,
        "note": "Blue Marble Earth high-res continent/glacier crop ('On Earth, water ice is a soft glacier that melts').",
    },
    {
        "row": "R07", "frames": 69, "kind": "still_cover",
        "source": "File_Sputnik_Planum_floating_hills_-_unannotated.jpg.jpg",
        "title": "Sputnik Planitia Water-Ice Hills and Glacier Margin",
        "video": False, "pan_x_frac": 0.50, "pan_y_frac": 0.50, "z1": 1.045,
        "note": "Water-ice hills along Sputnik Planitia ('and rock is the solid ground beneath it').",
    },
    {
        "row": "R08", "frames": 75, "kind": "still_cover",
        "source": "PIA19842.jpg",
        "title": "A Mountain Range within Pluto Heart",
        "video": False, "pan_x_frac": 0.50, "pan_y_frac": 0.50, "z1": 1.035,
        "note": "Hillary Montes 2-3 km water-ice mountain range within Pluto's heart + single teach overlay ('2-3 KM WATER-ICE PEAKS').",
    },
    {
        "row": "R09", "frames": 60, "kind": "still_cover",
        "source": "PIA19952.jpg",
        "title": "The Rich Color Variations of Pluto (MVIC)",
        "video": False, "pan_x_frac": 0.50, "pan_y_frac": 0.50, "z1": 1.045, "star_dark": True,
        "note": "MVIC enhanced-colour view of Pluto's water-ice mountain margin ('are big blocks of water ice').",
    },
    {
        "row": "R10", "frames": 114, "kind": "still_cover",
        "source": "PIA19936.jpg",
        "title": "Surface Variety: Frosted Mountain Margin of Sputnik Planitia",
        "video": False, "pan_x_frac": 0.75, "pan_y_frac": 0.50, "z1": 1.045,
        "note": "Frosted mountain ridges coated with frozen methane/nitrogen ('sometimes coated with frozen gases like methane'), clean hold with zero loop cross-fade.",
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
        rng = np.random.default_rng(3402)
        for _ in range(2100):
            sy = int(rng.integers(4, H - 6))
            sx = int(rng.integers(4, W - 6))
            b = float(rng.uniform(85.0, 195.0))
            sz = 2 if rng.random() < 0.76 else 3
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


def render_r01_open_9x16(frames_n: int, dest: Path, pool_map: dict[str, Path], open_f0: Path) -> float:
    """Renders full-bleed 1080x1920 (9:16) opener clip from 2690x3412 PIA20732.jpg.
    All crop boxes stay strictly inside [180..2510] x [240..3240] so zero edge bars can occur."""
    src_im = Image.open(pool_map["PIA20732.jpg"]).convert("RGB")
    src_im = ImageEnhance.Contrast(src_im).enhance(1.08)
    src_im = ImageEnhance.Color(src_im).enhance(1.14)
    sw_img, sh_img = src_im.size  # 2690 x 3412

    xx = np.linspace(0.0, 1.0, W, dtype=np.float32)[None, :, None]
    yy = np.linspace(0.0, 1.0, H, dtype=np.float32)[:, None, None]
    denom = float(max(1, frames_n - 1))
    frames: list[Image.Image] = []

    # Start window: 1500x2666.7 at (200, 560) -> End window: 1120x1991.1 at (1260, 280)
    # Max upscale = 1920 / 1991.1 = 0.964x <= 2.00x; 100% inside 2690x3412!
    for f in range(frames_n):
        u = f / denom
        cw = 1500.0 - 380.0 * u
        ch = cw * (H / W)
        x0 = 200.0 + 1060.0 * u
        y0 = 560.0 - 280.0 * u
        assert 0.0 <= x0 and x0 + cw <= sw_img and 0.0 <= y0 and y0 + ch <= sh_img
        plate = src_im.transform(
            (W, H),
            Image.Transform.EXTENT,
            (x0, y0, x0 + cw, y0 + ch),
            resample=Image.Resampling.BICUBIC,
        )
        plate = plate.filter(ImageFilter.UnsharpMask(radius=1.4, percent=115, threshold=2))
        arr = np.asarray(plate, dtype=np.float32)

        sweep_x = 0.14 + 0.74 * u
        dist = (xx - sweep_x) + 0.22 * (yy - 0.5)
        glow = np.exp(-((dist / 0.28) ** 2))
        tint = (
            np.array([[[20.0, 12.0, -5.0]]], dtype=np.float32) * glow
            + np.array([[[-6.0, 5.0, 20.0]]], dtype=np.float32) * (1.0 - glow)
        )
        arr = lift_navy(np.clip(arr + tint, 0.0, 255.0))
        fr = Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8), "RGB")
        if f == 0:
            fr.save(open_f0)
        frames.append(fr)

    pipe_frames(frames, dest)
    GFX_OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dest, GFX_OUT / "code_graphic_034_short2_r01_open_9x16.mp4")
    return 0.96


def build_base_9x16_cover(shot: dict, pool_map: dict[str, Path]) -> tuple[Image.Image, float]:
    src = pool_map[shot["source"]]
    im = Image.open(src).convert("RGB")
    if shot["source"] in CLEAN_CROPS:
        im = im.crop(CLEAN_CROPS[shot["source"]])
    im = ImageEnhance.Color(im).enhance(1.16)
    im = ImageEnhance.Contrast(im).enhance(1.08)

    sw, sh = im.size
    if sw / sh >= W / H:
        ch = float(sh)
        cw = ch * (W / H)
    else:
        cw = float(sw)
        ch = cw * (H / W)
    px_frac = float(shot.get("pan_x_frac", 0.5))
    py_frac = float(shot.get("pan_y_frac", 0.5))
    x0 = max(0.0, min(sw - cw, (sw - cw) * px_frac))
    y0 = max(0.0, min(sh - ch, (sh - ch) * py_frac))
    crop = im.transform(
        (W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), resample=Image.Resampling.BICUBIC
    )
    crop = crop.filter(ImageFilter.UnsharpMask(radius=1.5, percent=122, threshold=2))
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
    return Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8), "RGB"), up


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

    if kind == "r01_open_9x16":
        assert open_f0 is not None
        return render_r01_open_9x16(frames_n, dest, pool_map, open_f0)

    if kind == "video_pan":
        src = pool_map[shot["source"]]
        raw = load_raw_video_frames(src, float(shot["offset"]), frames_n)
        cw = 1080.0 * (W / H)  # 607.5 px -> 1920/1080 = 1.778x <= 2.00x
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
            fr = Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8), "RGB")
            frames.append(fr)
        pipe_frames(frames, dest)
        return 1.78

    if kind == "still_cover":
        base, up = build_base_9x16_cover(shot, pool_map)
        render_symmetric_still_zoom(base, frames_n, float(shot["z1"]), dest)
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


def draw_two_colour_line(draw: ImageDraw.ImageDraw, y: int, segs: list[tuple[str, tuple]], font: ImageFont.FreeTypeFont, stroke: int = 7) -> list[int]:
    full = "".join(s for s, _ in segs)
    total_w = sum(draw.textlength(s, font=font) for s, _ in segs)
    x = round((W - total_w) / 2.0)
    cur_x = x
    for s, col in segs:
        draw.text((cur_x, y), s, font=font, fill=col, stroke_width=stroke, stroke_fill=(16, 26, 46, 255))
        cur_x += round(draw.textlength(s, font=font))
    return list(draw.textbbox((x, y), full, font=font, stroke_width=stroke))


def make_hook(dest: Path) -> dict:
    """Two-line >=96px hook burned from t=0.00s: PLUTO'S ICE (yellow ICE) / MOUNTAINS?"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT_BLACK, 114)
    while max(d.textlength("PLUTO'S ICE", font=f), d.textlength("MOUNTAINS?", font=f)) > W * 0.86:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y0 = 225
    b0 = draw_two_colour_line(d, y0, [("PLUTO'S ", WHITE), ("ICE", YELLOW)], f, stroke=7)
    b1 = centred(d, y0 + lh, "MOUNTAINS?", f, WHITE, stroke=7)
    im.save(dest)
    return {"text": "PLUTO'S ICE / MOUNTAINS?", "yellow_word": "ICE", "font_px": f.size, "bboxes": [b0, b1]}


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


def make_teach(dest: Path, text: str) -> list[int]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.90)
    while d.textlength(text, font=f) > W * 0.72:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y1 - 88, text, f, YELLOW, stroke=7)
    pad = 16
    d.rounded_rectangle((bb[0] - pad, bb[1] - 10, bb[2] + pad, bb[3] + 10), radius=18, outline=(255, 224, 0, 230), width=4)
    im.save(dest)
    return bb


def make_caption(dest: Path, text: str) -> list[int]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.88)
    shown = text.upper()
    while d.textlength(shown, font=f) > W * 0.72:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y1 + 52, shown, f, WHITE, stroke=6)
    im.save(dest)
    return bb


def make_cover(dest: Path, f0_png: Path) -> dict:
    im = Image.open(f0_png).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    d = ImageDraw.Draw(im)
    size = 96
    while size < 124:
        trial = ImageFont.truetype(FONT_BLACK, size + 2)
        if max(d.textlength("ICE", font=trial), d.textlength("MOUNTAINS?", font=trial)) > W * 0.82:
            break
        size += 2
    f = ImageFont.truetype(FONT_BLACK, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    rows = [("ICE", YELLOW), ("MOUNTAINS?", WHITE)]
    y = BAND_Y0 + (BAND_H - lh * len(rows)) // 2
    boxes = [centred(d, y + idx * lh, r, f, col, stroke=8) for idx, (r, col) in enumerate(rows)]
    im.save(dest, quality=94, subsampling=0)
    return {"file": str(dest), "rows": [r for r, _ in rows], "font_px": size, "bboxes": boxes}


def load_v01_words() -> tuple[dict, list[dict], float]:
    raw_sha = sha256(V01_WORDS)
    if raw_sha != EXPECTED_V01_SHAS["words"]:
        raise RuntimeError(f"v01 words sha256 mismatch: {raw_sha}")
    doc = json.loads(V01_WORDS.read_text())
    words = []
    for w in doc["words"]:
        txt = (w.get("word") or w.get("text") or "").strip()
        s = round(float(w["start"]), 3)
        e = round(float(w["end"]), 3)
        words.append({
            **w,
            "word": txt,
            "text": txt,
            "w": txt,
            "start": s,
            "end": e,
            "s": s,
            "e": e,
        })
    return doc, words, words[-1]["e"]


def caption_chunks(words: list[dict], vo_end: float) -> list[dict]:
    chunks, cur = [], []
    for w in words:
        cand_len = sum(len(x["w"]) for x in cur) + len(cur) + len(w["w"])
        if cur and (len(cur) >= 3 or cand_len > 18):
            chunks.append(cur)
            cur = []
        cur.append(w)
        if re.search(r"[,.?!]$", w["w"]):
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


def prepare_locked_audio(work: Path) -> tuple[dict, Path, Path, Path, Path]:
    """Verifies locked v01 audio stems by SHA-256, mixes them, and calibrates AAC loudness to -14.0 LUFS / <= -1.85 dBTP."""
    for key, src_p in (("vo", V01_VO), ("sfx", V01_SFX), ("bed", V01_BED)):
        got = sha256(src_p)
        if got != EXPECTED_V01_SHAS[key]:
            raise RuntimeError(f"v01 {key} stem sha256 mismatch: {got} != {EXPECTED_V01_SHAS[key]}")

    vo_arr = read_wav(V01_VO)
    sfx_arr = read_wav(V01_SFX)
    bed_arr = read_wav(V01_BED)
    n = TOTAL_FRAMES * (SR // FPS)  # 1,238,400 samples = 25.800 s
    assert len(vo_arr) == n and len(sfx_arr) == n and len(bed_arr) == n

    mix_raw = work / "mix_raw.wav"
    write_wav(vo_arr + sfx_arr + bed_arr, mix_raw)

    _, vo_i = sfx_kit.ebur128(V01_VO)
    _, sfx_i = sfx_kit.ebur128(V01_SFX)
    _, bed_i = sfx_kit.ebur128(V01_BED)

    gain_db = 0.0
    limit_db = -2.25
    cal_wav = work / "mix_cal.wav"
    test_m4a = work / "mix_cal_test.m4a"
    i_lufs, tp = -14.0, -2.0
    for _ in range(6):
        af = (
            f"aresample=192000,volume={gain_db:.3f}dB,"
            f"alimiter=limit={limit_db:.2f}dB:level=disabled:attack=5:release=50,"
            "aresample=48000"
        )
        run(["ffmpeg", "-y", "-v", "error", "-i", str(mix_raw), "-af", af, "-ar", str(SR), "-ac", "2", "-t", f"{TOTAL_S:.3f}", str(cal_wav)])
        run(["ffmpeg", "-y", "-v", "error", "-i", str(cal_wav), "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2", "-t", f"{TOTAL_S:.3f}", str(test_m4a)])
        m_i, m_tp = gso.aac_loudness(test_m4a)
        if m_i is not None and m_tp is not None:
            i_lufs, tp = m_i, m_tp
        if -14.15 <= i_lufs <= -13.85 and tp <= -1.85:
            break
        gain_db += (-14.0 - i_lufs)
        if tp > -1.85:
            limit_db -= max(0.15, tp - (-2.0))

    stats = {
        "vo_lufs": round(vo_i, 2),
        "sfx_lufs": round(sfx_i, 2),
        "bed_lufs": round(bed_i, 2),
        "aac_integrated_lufs": round(i_lufs, 2),
        "aac_true_peak_dbtp": round(tp, 2),
    }
    return stats, V01_VO, V01_SFX, V01_BED, cal_wav


def main() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True, exist_ok=True)
    EXP_DIR.mkdir(parents=True, exist_ok=True)

    pool_map = load_pool_map()
    v01_words_doc, words, last_word_end = load_v01_words()
    spoken_text = " ".join(w["w"] for w in words)
    print(f"Short 2 v02 words={len(words)}, onset={words[0]['s']:.3f}s, last_end={last_word_end:.3f}s, total={TOTAL_S:.3f}s", flush=True)

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
            "framing": (
                {"offset": shot["offset"], "crop": "9:16 full-bleed", "mode": "cover"}
                if shot["video"]
                else {"crop": "9:16 full-bleed", "mode": "cover"}
            ),
            "note": shot["note"],
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
    teach_bbox = make_teach(WORK / "teach.png", TEACH_TEXT)
    caps = caption_chunks(words, last_word_end)
    for i, c in enumerate(caps):
        make_caption(WORK / f"cap_{i:02d}.png", c["text"])

    # Overlay hook (0.00-2.40s, burned from t=0.00s with fade-out only), promo title (9.50-13.50s),
    # single teach pill (18.00-21.60s), and word-by-word captions (clear of hook and promo title).
    inputs = ["-y", "-v", "error", "-i", str(pic_mp4)]
    overlays = [
        (WORK / "hook.png", 0.00, HOOK_END, "hook"),
        (WORK / "title.png", TITLE_IN, TITLE_OUT, "both"),
        (WORK / "teach.png", TEACH_IN, TEACH_OUT, "both"),
    ]
    for i, c in enumerate(caps):
        if c["e"] > HOOK_END + 0.12:
            st = max(HOOK_END, c["s"])
            if c["e"] - st >= 0.18:
                overlays.append((WORK / f"cap_{i:02d}.png", round(st, 2), c["e"], "none"))

    fc_parts = []
    cur = "0:v"
    for idx_ov, (png_p, st_s, en_s, fade_mode) in enumerate(overlays, 1):
        hold = max(0.18, en_s - st_s)
        inputs.extend(["-loop", "1", "-t", f"{hold:.3f}", "-i", str(png_p)])
        f_chain = ["format=rgba"]
        if fade_mode == "hook":
            f_chain.append(f"fade=t=out:st={max(0.10, hold - 0.25):.3f}:d=0.25:alpha=1")
        elif fade_mode == "both" and hold > 0.50:
            f_chain.append("fade=t=in:st=0:d=0.22:alpha=1")
            f_chain.append(f"fade=t=out:st={hold - 0.22:.3f}:d=0.22:alpha=1")
        f_chain.append(f"setpts=PTS+{st_s:.3f}/TB")
        fc_parts.append(f"[{idx_ov}:v]{','.join(f_chain)}[ov{idx_ov}]")
        nxt = f"v{idx_ov}"
        fc_parts.append(
            f"[{cur}][ov{idx_ov}]overlay=0:0:format=auto:eof_action=pass:"
            f"enable='gte(t,{st_s:.3f})*lt(t,{en_s - 0.001:.3f})'[{nxt}]"
        )
        cur = nxt

    audio_stats, src_vo, src_sfx, src_bed, cal_wav = prepare_locked_audio(WORK)

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

    # Export v02 stems (exact byte copies of locked v01 stems), cover, words, cuts, pool, and meta
    dst_vo = EXP_DIR / f"{STEM}_stem_vo.wav"
    dst_sfx = EXP_DIR / f"{STEM}_stem_sfx.wav"
    dst_bed = EXP_DIR / f"{STEM}_stem_bed.wav"
    dst_words = EXP_DIR / f"{STEM}_words.json"
    dst_cover = EXP_DIR / f"{STEM}_cover.jpg"
    dst_cover_prev = EXP_DIR / f"{STEM}_cover_preview.jpg"
    dst_cuts = EXP_DIR / "cuts_v02.json"
    dst_pool = EXP_DIR / "pool_v02.json"
    dst_meta = EXP_DIR / f"{STEM}_meta.json"

    shutil.copy2(src_vo, dst_vo)
    shutil.copy2(src_sfx, dst_sfx)
    shutil.copy2(src_bed, dst_bed)
    assert sha256(dst_vo) == EXPECTED_V01_SHAS["vo"]
    assert sha256(dst_sfx) == EXPECTED_V01_SHAS["sfx"]
    assert sha256(dst_bed) == EXPECTED_V01_SHAS["bed"]

    make_cover(dst_cover, open_f0)

    words_doc = {
        **v01_words_doc,
        "short": STEM,
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
        "job": "J2867",
        "ruling": "J2364 Selection 2A (S46 + S47 + S48 + S50 whole-sentence lift) + J2383 §5.3 full-bleed 9:16 v02",
        "film": "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters",
        "short_slug": "short02_water_ice_mountains",
        "short_id": STEM,
        "format": "Keeper Question Short (OWB-2026-11-E1, v02 100% full-bleed 9:16, 0 end card, 0 loop xfade)",
        "air_date": AIR_DATE,
        "air_slot": "2026-12-23T11:30:00Z",
        "title": SHORT_TITLE,
        "alt_title": ALT_TITLE,
        "long_title": LONG_TITLE,
        "promoted_long_title": LONG_TITLE,
        "promoted_long_window_s": [TITLE_IN, TITLE_OUT],
        "hook_caption": "PLUTO'S ICE MOUNTAINS?",
        "hook_yellow_word": "ICE",
        "single_teach_overlay": {
            "text": TEACH_TEXT,
            "word_count": 4,
            "window_s": [TEACH_IN, TEACH_OUT],
            "bbox": teach_bbox,
            "band_height_px": LINE_H,
            "band_height_pct": 11.51,
        },
        "duration_s": TOTAL_S,
        "frames": TOTAL_FRAMES,
        "fps": FPS,
        "resolution": f"{W}x{H}",
        "scribe_words": len(words),
        "spoken_words": 64,
        "word_count": len(words),
        "spoken": spoken_text,
        "vo": dst_vo.name,
        "words_file": dst_words.name,
        "vo_onset_s": words[0]["s"],
        "first_word_start_s": words[0]["s"],
        "last_word_end_s": last_word_end,
        "loop_tail_s": round(TOTAL_S - last_word_end, 3),
        "payoff_window_s": [17.67, 21.87],
        "payoff_pct": [68.5, 84.8],
        "cut_1_s": 2.40,
        "cut_2_s": 4.50,
        "max_shot_s": 3.80,
        "hook": hook_info,
        "title_card": title_info,
        "audio": audio_stats,
        "loudness": {
            "integrated_lufs": audio_stats["aac_integrated_lufs"],
            "true_peak_dbtp": audio_stats["aac_true_peak_dbtp"],
        },
        "spend_gbp": 0.0,
        "sha256": {
            "mp4": sha256(out_mp4),
            "cover_jpg": sha256(dst_cover),
            "stem_vo_wav": sha256(dst_vo),
            "stem_sfx_wav": sha256(dst_sfx),
            "stem_bed_wav": sha256(dst_bed),
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
    g6 = sp.run([
        sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
        "short", str(dst_cover), "--out", str(dst_cover_prev),
    ], capture_output=True, text=True)

    report = [
        f"# Gate Report — `{STEM}.mp4` (`J2867`)",
        "",
        f"- **File:** `{out_mp4}`",
        f"- **SHA-256:** `{meta_doc['sha256']['mp4']}`",
        f"- **Duration:** `{TOTAL_S:.3f} s` (`{TOTAL_FRAMES}` frames at `30/1` CFR)",
        f"- **AAC Loudness:** `{audio_stats['aac_integrated_lufs']:.2f} LUFS` integrated, `{audio_stats['aac_true_peak_dbtp']:.2f} dBTP` true peak",
        f"- **Locked v01 Stems Reused Byte-Identical:** VO `{meta_doc['sha256']['stem_vo_wav'][:12]}`, SFX `{meta_doc['sha256']['stem_sfx_wav'][:12]}`, Bed `{meta_doc['sha256']['stem_bed_wav'][:12]}`",
        "",
        f"## 1. `gate_shorts_open.py` (rc={g1.returncode})",
        "```text", (g1.stdout + "\n" + g1.stderr).strip()[-2000:], "```",
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
        "",
        f"## 6. `thumb_preview.py short` (rc={g6.returncode})",
        "```text", (g6.stdout + "\n" + g6.stderr).strip()[-600:], "```",
    ]
    (EXP_DIR / "GATE_REPORT_v02.md").write_text("\n".join(report) + "\n")
    print("\n".join(report), flush=True)

    if any(g.returncode != 0 for g in (g1, g2, g3, g4, g5, g6)):
        raise SystemExit(f"Short 2 v02 gate failed: {[g.returncode for g in (g1, g2, g3, g4, g5, g6)]}")

    # Clean intermediate build scratch once all gates PASS (AGENTS.md rule)
    shutil.rmtree(WORK, ignore_errors=True)


if __name__ == "__main__":
    main()
