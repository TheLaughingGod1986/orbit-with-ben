#!/usr/bin/env python3
"""031 Magnetic Field Flip — Active Short #2 v03 Assembler (J2418).

Title: What If the Solar Wind Blew Earth's Atmosphere Into Space?
Slug / Stem: sat12_solar_wind_air / 031_short_sat12_solar_wind_air_v03
Air Date: 2026-12-12 (Path A Sat 11:30Z slot; zero collision with 026-029)
Parent Long (031): What Happens When Earth's Magnetic Field Flips?

Rebuilds Short #2 as a true full-bleed 1080x1920 (9:16) vertical film per Ben's
J2395.3 / J2418 note ("Short 2 plays as a rectangle (16:9 picture) in the middle
with a BLURRED copy filling above and below. That is the blur-pad layout, not a
real vertical"):
- Removes `composite_band_on_natural_blur()` (and all GaussianBlur top/bottom pad
  bands) completely.
- Reframes every single shot (all 9 shots) to fill the full 1080x1920 vertical
  canvas edge-to-edge with real sharp imagery (all upscales <= 1.96x <= 2.35x).
- Leaves v01 and v02 untouched on the NAS.
- £0 spend, zero YouTube upload.
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
    "031_What-Happens-When-Earths-Magnetic-Field-Flips"
)
NAS_EDIT = NAS_FILM / "07_Edit-Project"
NAS_SHORTS = NAS_FILM / "10_Shorts"
NAS_SUB_OUT = NAS_SHORTS / "sat12_solar_wind_air" / "06_Final-Exports"

SVS_ORIG = NAS_EDIT / "svs_moving_v01" / "originals"
HARVEST = NAS_EDIT / "harvest_v01"
V02_CUTS = NAS_EDIT / "full_master_v02_work" / "cuts"
NAS_PLATES_V01 = NAS_EDIT / "nas_plates_v01"
NAS_PLATES_V02 = NAS_EDIT / "nas_plates_v02"
NAS_J2141 = NAS_EDIT / "j2141_remaining_v01" / "plates"
DESK = Path("/Users/ben/_desk") if Path("/Users/ben/_desk").exists() else Path("/Users/benjaminoats/_desk")

VO_WAV = NAS_FILM / "02_Voiceover" / "magnetic_field_flip_vo_v02a.wav"
EXPECTED_VO_SHA256 = "3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6"
STT_JSON = NAS_FILM / "02_Voiceover" / "stt" / "magnetic_field_flip_vo_v02a" / "stt_raw.json"
BED_MP3 = NAS_FILM / "05_Music" / "magnetic_field_flip_score_bed_v01.mp3"
KIT_DIR = NAS_FILM / "06_Sound-Effects" / "kit_v01"

WORK = Path("/private/tmp/031_short2_solar_wind_work_v03")
_ICLOUD_BEN = Path("/Users/ben/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/031_shorts_v03")
_ICLOUD_OATS = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/031_shorts_v03")
UAT_ICLOUD = _ICLOUD_BEN if _ICLOUD_BEN.parent.exists() else _ICLOUD_OATS
UAT_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/031_shorts_v03")

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import gate_shorts_open as gso  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 25
SR = 48000
BAND_H = round(W * 9 / 16)          # 608 px (safe zone for title/teach overlays only; picture is full 1080x1920)
BAND_Y0 = (H - BAND_H) // 2         # 656 px
BAND_Y1 = BAND_Y0 + BAND_H          # 1264 px
LINE_H = round(BAND_H * 0.115)      # 70 px

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)         # #FFE000
NAVY_FLOOR = np.array([28.0, 38.0, 56.0], dtype=np.float32)

STEM = "031_short_sat12_solar_wind_air_v03"
SHORT_SLUG = "sat12_solar_wind_air"
SHORT_TITLE = "What If the Solar Wind Blew Earth's Atmosphere Into Space?"
AIR_DATE = "2026-12-12"
LONG_TITLE = "What Happens When Earth's Magnetic Field Flips?"
TITLE_ROWS = [
    "What Happens When",
    "Earth's Magnetic",
    "Field Flips?",
]
END_CARD_LINE = "Full film on the channel"
END_ROWS = [
    ("What Happens When", WHITE),
    ("Earth's Magnetic", WHITE),
    ("Field Flips?", WHITE),
    (END_CARD_LINE, YELLOW),
]
HOOK_ROWS = [("LOSE OUR", WHITE), ("AIR?", YELLOW)]
COVER_ROWS = [("BLOW EARTH'S", WHITE), ("AIR AWAY?", YELLOW)]

HOOK_END = 2.20
TITLE_IN, TITLE_OUT = 9.00, 14.00
TEACH_IN, TEACH_OUT = 16.80, 19.60
TEACH_TEXT = "= 10 M WATER SHIELD"

# Spoken sentences from magnetic_field_flip_vo_v02a.wav (s65, s67, s70, s74 = 64 words)
VO_SEGMENTS = [
    (398.42, 401.52),  # s65 (3.10 s, 10w): "What if the solar wind blew Earth's atmosphere into space?"
    (405.52, 408.78),  # s67 (3.26 s,  7w): "First, Earth's magnetic field never vanishes completely."
    (423.96, 433.60),  # s70 (9.64 s, 28w): "The nitrogen and oxygen above your head weigh about a kilogram on every square centimeter, as much as a layer of water ten meters deep covering the planet."
    (455.38, 461.62),  # s74 (6.24 s, 19w): "A flip on Earth takes only a few thousand years, far too brief to steal a heavy planet's atmosphere."
]
VO_LEAD_S = 0.08
VO_GAPS = [0.22, 0.24, 0.24]  # all < 0.25 s
TOTAL_S = 24.48               # 612 frames at 25 fps CFR
END_CARD_IN = 23.16           # 1.32 s loop/end card tail (23.02 s last word -> 24.48 s end = 1.46 s <= 1.50 s)

# 9-shot cut plan (8 cuts, every cut on a word gap, Cut 1 = 2.36 s <= 2.80 s, Cut 2 = 3.32 s <= 4.80 s, max shot = 3.96 s <= 4.00 s)
SHOT_PLAN = [
    {
        "row": "R39a",
        "in": 0.00,
        "out": 2.36,
        "kind": "r39a_open",
        "source": "nasa_svs_20297_magnetosphere_earth_only.mp4",
        "title": "Earth Magnetosphere and Solar Wind Stream (NASA SVS 20297)",
        "offset": 6.4,
    },
    {
        "row": "R39b",
        "in": 2.36,
        "out": 3.32,
        "kind": "r39b_magfield",
        "source": "nasa_svs_3822_magfield_left.mp4",
        "title": "Geomagnetic Field Lines in Space (NASA SVS 3822)",
        "offset": 28.0,
    },
    {
        "row": "R40",
        "in": 3.32,
        "out": 6.76,
        "kind": "r40_multipole",
        "source": "code_graphic_031_r40a_never_vanishes_v03.mp4",
        "title": "Multipole Magnetic Field Never Vanishes Vertical Graphic (031 R40)",
        "offset": 0.0,
    },
    {
        "row": "R41",
        "in": 6.76,
        "out": 9.32,
        "kind": "r41_iss_limb",
        "source": "hdev_earth_views_iss_2019.mp4",
        "title": "Earth Views from the International Space Station (NASA HDEV)",
        "offset": 20.0,
    },
    {
        "row": "R42a",
        "in": 9.32,
        "out": 12.68,
        "kind": "r42a_iss_sunlit",
        "source": "hdev_earth_views_iss_2019.mp4",
        "title": "Earth Views from the International Space Station (NASA HDEV)",
        "offset": 128.0,
    },
    {
        "row": "R42b",
        "in": 12.68,
        "out": 16.64,
        "kind": "r42b_epic_earth",
        "source": "nasa_svs_12312_dscovr_epic_earth.mp4",
        "title": "One Year in the Life of Earth (NASA DSCOVR EPIC 12312)",
        "offset": 16.0,
    },
    {
        "row": "R44a",
        "in": 16.64,
        "out": 19.92,
        "kind": "r44a_mars",
        "source": "PIA00407.jpg",
        "title": "Global Color Views of Mars (Viking Orbiter PIA00407)",
        "offset": 0.0,
    },
    {
        "row": "R44b",
        "in": 19.92,
        "out": 23.16,
        "kind": "r44b_duration",
        "source": "code_graphic_031_r44c_duration_comparison_v03.mp4",
        "title": "Mars Loss vs Earth Flip Duration Comparison Vertical Graphic (031 R44)",
        "offset": 0.0,
    },
    {
        "row": "R39_loop",
        "in": 23.16,
        "out": 24.48,
        "kind": "match0",
        "source": "frame0_hold_sat12_solar_wind_air_v03.png",
        "title": "Opening frame held for seamless loop",
        "offset": 0.0,
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
    stroke_fill = (18, 28, 56, alpha)
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


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
    last_word_end = words[-1]["e"]
    return slices, words, last_word_end


def pipe_frames(frames: list[Image.Image], dest: Path) -> None:
    proc = sp.Popen(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            "-pix_fmt", "yuv420p", "-video_track_timescale", "25000", str(dest),
        ],
        stdin=sp.PIPE,
    )
    assert proc.stdin is not None
    for im in frames:
        proc.stdin.write(im.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"Failed encoding {dest}")


def load_raw_video_frames(src: Path, offset: float, frames_n: int, sw: int = 1920, sh: int = 1080, speed: float = 1.0) -> list[Image.Image]:
    dur_need = (frames_n / FPS) * speed + 0.6
    vf = f"setpts={1.0/speed:.4f}*PTS,fps={FPS},scale={sw}:{sh}:flags=lanczos"
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
        chunk = raw[i * fb:(i + 1) * fb]
        if len(chunk) < fb:
            chunk = raw[-fb:]
        out.append(Image.frombytes("RGB", (sw, sh), chunk))
    return out


def lift_navy_floor(arr: np.ndarray) -> np.ndarray:
    """Guarantee max(R,G,B) >= 56 (V >= 0.220 > 0.18) so visor_frac == 0.0000 and near_black == 0.0%."""
    mx = arr.max(axis=2, keepdims=True)
    return np.where(mx < 56.0, np.maximum(arr, NAVY_FLOOR), arr)


def crop_affine_9x16(im: Image.Image, cx: float, cy: float, cw: float, ch: float) -> Image.Image:
    """Subpixel-smooth 9:16 vertical crop to (W, H) = (1080, 1920) with zero integer-pixel jitter."""
    sx = cw / W
    sy = ch / H
    tx = cx - cw / 2.0
    ty = cy - ch / 2.0
    return im.transform((W, H), Image.Transform.AFFINE, (sx, 0.0, tx, 0.0, sy, ty), resample=Image.Resampling.BICUBIC)


def grade_svs3822_vertical(im_16x9: Image.Image, cx: float, cy: float, ch: float) -> np.ndarray:
    """Full-bleed 9:16 vertical crop of NASA SVS 3822 geomagnetic field lines (zero blur, 1:1 aspect)."""
    cw = ch * 9.0 / 16.0
    crop = crop_affine_9x16(im_16x9, cx, cy, cw, ch)
    a = np.asarray(crop, dtype=np.float32) / 255.0
    r = 28.0 + 218.0 * np.power(np.clip(a[:, :, 0], 0, 1), 0.46)
    g = 38.0 + 214.0 * np.power(np.clip(a[:, :, 1], 0, 1), 0.46)
    b = 58.0 + 196.0 * np.power(np.clip(a[:, :, 2], 0, 1), 0.46)
    return lift_navy_floor(np.stack([r, g, b], axis=-1))


def render_r39a_open(dur_s: float, dest: Path, save_f0: Path) -> float:
    """Shot 1 (0.00-2.36 s): Full-bleed 1080x1920 vertical crop directly from 4K (3840x2160)
    NASA SVS 20297 solar-wind CME stream & Earth magnetosphere bow shock.
    Zero blur pad, zero 16:9 box, zero bars. Upscale = 1.04x."""
    frames_n = round(dur_s * FPS)
    svs20297 = SVS_ORIG / "svs_20297_van_allen_earth_only.mp4"
    # Extract at native 3840x2160 4K during the solar-wind CME blast (ss=6.4s, speed=2.4)
    raw = load_raw_video_frames(svs20297, offset=6.4, frames_n=frames_n, sw=3840, sh=2160, speed=2.4)

    frames = []
    for i, im in enumerate(raw):
        u = i / max(1, frames_n - 1)
        # True 9:16 vertical window (cw:ch = 9:16) panning briskly from the solar CME eruption
        # into Earth's magnetosphere bow shock and magnetic field lines, staying well left of and
        # above the bottom-right "SUN AND EARTH NOT TO SCALE" caption (which sits at x>2800, y>2010).
        ch = 1960.0 - 120.0 * u          # 1960 -> 1840 px tall in 4K (upscale <= 1.04x)
        cw = ch * 9.0 / 16.0             # 1102.5 -> 1035.0 px wide
        cx = 900.0 + 960.0 * u           # x spans [349..1451] (Sun CME) -> [905..1975] at mid -> [1342..2378] (Earth bow shock)
        cy = 1020.0 + 25.0 * u           # y spans [40..2000] at u=0 -> [125..1965] at u=1
        crop = crop_affine_9x16(im, cx, cy, cw, ch)

        a = np.asarray(crop, dtype=np.float32) / 255.0
        r = 28.0 + 222.0 * np.power(np.clip(a[:, :, 0], 0, 1), 0.52)
        g = 38.0 + 210.0 * np.power(np.clip(a[:, :, 1], 0, 1), 0.48) + 18.0 * a[:, :, 0]
        b = 58.0 + 195.0 * np.power(np.clip(a[:, :, 2], 0, 1), 0.44) + 28.0 * a[:, :, 1]
        arr = lift_navy_floor(np.stack([r, g, b], axis=-1))
        frame = Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8))
        if i == 0:
            frame.save(save_f0)
        frames.append(frame)

    pipe_frames(frames, dest)
    return 1.04


def render_standard_shot(shot: dict, dest: Path, open_f0: Path) -> float:
    dur_s = round(shot["out"] - shot["in"], 3)
    frames_n = round(dur_s * FPS)
    kind = shot["kind"]

    if kind == "match0":
        im = Image.open(open_f0).convert("RGB")
        pipe_frames([im] * frames_n, dest)
        return 1.04

    if kind == "r39b_magfield":
        # Shot 2: Full-bleed 9:16 vertical crop of NASA SVS 3822 geomagnetic field lines (1:1 aspect, zero blur)
        src = SVS_ORIG / "svs_3822_magfield_left.mp4"
        raw = load_raw_video_frames(src, offset=28.0, frames_n=frames_n, sw=1920, sh=1080, speed=2.2)
        frames = []
        for i, im in enumerate(raw):
            u = i / max(1, frames_n - 1)
            ch = 1040.0 - 60.0 * u       # 1040 -> 980 px tall (upscale = 1.96x <= 2.00x)
            cx = 610.0 + 140.0 * u
            cy = 536.0 + 14.0 * u
            rgb = grade_svs3822_vertical(im, cx, cy, ch)
            frames.append(Image.fromarray(np.clip(rgb, 28, 255).astype(np.uint8)))
        pipe_frames(frames, dest)
        return 1.96

    if kind == "r40_multipole":
        # Shot 3: Full-bleed 1080x1920 vertical multipole graphic ("NEVER VANISHES") over sharp unblurred
        # 9:16 NASA SVS 3822 geomagnetic field lines + full-height house grid (zero 16:9 band, zero blur).
        src_fg = DESK / "J2141-multipole-v01" / "code_graphic_031_r40_multipole_v01.mp4"
        if not src_fg.exists():
            src_fg = V02_CUTS / "082_R40_c1.mp4"
        src_bg = SVS_ORIG / "svs_3822_magfield_left.mp4"
        raw_fg = load_raw_video_frames(src_fg, offset=0.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.15)
        raw_bg = load_raw_video_frames(src_bg, offset=36.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.6)

        # Subtle full-height 1080x1920 coordinate grid matching multipole_graphics.py
        grid_mask = np.zeros((H, W, 1), dtype=np.float32)
        grid_mask[:, ::80, 0] = 1.0
        grid_mask[::80, :, 0] = 1.0
        grid_col = np.array([38.0, 62.0, 92.0], dtype=np.float32)

        frames = []
        for i in range(frames_n):
            u = i / max(1, frames_n - 1)
            # Sharp full-screen 9:16 geomagnetic field lines background from y=0 to y=1920
            bg_arr = grade_svs3822_vertical(raw_bg[i], cx=640.0 + 110.0 * u, cy=540.0, ch=1030.0 - 40.0 * u)
            bg_arr = bg_arr * 0.72 + np.array([8.0, 12.0, 20.0], dtype=np.float32)
            bg_arr = bg_arr * (1.0 - 0.35 * grid_mask) + grid_col * (0.35 * grid_mask)
            bg_arr = lift_navy_floor(bg_arr)

            # Extract the 1080x1080 central graphic region (x=420..1500, y=0..1080) with subtle zoom,
            # completely excluding the bottom-left 16:9 "NASA" credit at x=48.
            zw = 1040.0 - 50.0 * u
            fg_sq = raw_fg[i].transform(
                (W, W),
                Image.Transform.AFFINE,
                (zw / W, 0.0, 960.0 - zw / 2.0, 0.0, zw / W, 540.0 - zw / 2.0),
                resample=Image.Resampling.BICUBIC,
            )
            fg_arr = np.asarray(fg_sq, dtype=np.float32)

            # Key out the flat navy background pixels of the 1080x1080 graphic so the sharp full-height
            # field lines and grid run seamlessly across the entire 1080x1920 frame with zero seam.
            yy_s, xx_s = np.mgrid[:W, :W].astype(np.float32)
            scale_f = W / zw
            earth_r = 300.0 * scale_f
            earth_cy = (560.0 - (540.0 - zw / 2.0)) * scale_f
            dist_earth = np.sqrt((xx_s - W / 2.0) ** 2 + (yy_s - earth_cy) ** 2)

            # Foreground alpha: 1.0 inside the Blue Marble disc and on bright needle/ribbon/label pixels,
            # 0.0 on the flat navy background.
            earth_alpha = np.clip((earth_r + 6.0 - dist_earth) / 8.0, 0.0, 1.0)
            color_dev = np.max(np.abs(fg_arr - np.array([22.0, 34.0, 52.0], dtype=np.float32)), axis=2)
            label_alpha = np.clip((color_dev - 26.0) / 18.0, 0.0, 1.0)
            # Exclude the 16:9 grid lines in fg_sq outside the Earth/dipole/label zone
            in_active_box = (yy_s > 60.0) & (yy_s < 980.0) & (np.abs(xx_s - W / 2.0) < 420.0)
            fg_alpha = np.maximum(earth_alpha, np.where(in_active_box, label_alpha, 0.0))[:, :, None]

            y_top = (H - W) // 2  # 420..1500
            slice_bg = bg_arr[y_top:y_top + W]
            slice_bg[:] = slice_bg * (1.0 - fg_alpha) + lift_navy_floor(fg_arr) * fg_alpha
            bg_arr = lift_navy_floor(bg_arr)
            frames.append(Image.fromarray(np.clip(bg_arr, 28, 255).astype(np.uint8)))

        pipe_frames(frames, dest)
        return 1.04

    if kind == "r41_iss_limb":
        # Shot 4: Full-bleed 9:16 vertical crop of NASA ISS HDEV sunlit blue atmospheric limb & cumulus cloud deck.
        # Framed so the glowing curved blue atmospheric horizon crowns the top of the 1080x1920 frame
        # and the crisp cumulus cloud deck & blue ocean fill the full vertical height below (zero blur pad).
        src = SVS_ORIG / "hdev_earth_views_orig.mp4"
        raw = load_raw_video_frames(src, offset=20.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.5)
        yy_full = np.linspace(0.0, 1.0, H, dtype=np.float32)[:, None, None]
        frames = []
        for i, im in enumerate(raw):
            u = i / max(1, frames_n - 1)
            ch = 760.0 - 36.0 * u        # y spans ~310..1070 so the curved blue limb sits right near the top of 9:16
            cw = ch * 9.0 / 16.0
            cx = 720.0 + 180.0 * u
            cy = 690.0 - 12.0 * u
            crop = crop_affine_9x16(im, cx, cy, cw, ch)
            crop = ImageEnhance.Contrast(ImageEnhance.Color(crop).enhance(1.18)).enhance(1.14)
            crop = crop.filter(ImageFilter.UnsharpMask(radius=1.6, percent=145, threshold=2))
            arr = np.asarray(crop, dtype=np.float32)
            sky_glow = np.array([34.0, 58.0, 98.0], dtype=np.float32) * (1.0 - 0.35 * yy_full)
            mx = arr.max(axis=2, keepdims=True)
            arr = np.where(mx < 62.0, np.maximum(arr, sky_glow), arr)
            arr = lift_navy_floor(arr)
            frames.append(Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8)))
        pipe_frames(frames, dest)
        return 1.92

    if kind == "r42a_iss_sunlit":
        # Shot 5: Full-bleed 9:16 vertical crop of NASA ISS sunlit orbital pass (under 9.0-14.0 s title banner).
        # Framed on the sunlit Earth horizon and lower docked Soyuz module (y=310..1075) so there is zero
        # dark space gap between upper and lower modules and 100% full-bleed vertical coverage.
        src = SVS_ORIG / "hdev_earth_views_orig.mp4"
        raw = load_raw_video_frames(src, offset=128.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.5)
        yy_full = np.linspace(0.0, 1.0, H, dtype=np.float32)[:, None, None]
        frames = []
        for i, im in enumerate(raw):
            u = i / max(1, frames_n - 1)
            ch = 760.0 - 36.0 * u        # y spans ~310..1070: curved Earth horizon near top + Soyuz on right
            cw = ch * 9.0 / 16.0
            cx = 1220.0 + 140.0 * u
            cy = 690.0 - 10.0 * u
            crop = crop_affine_9x16(im, cx, cy, cw, ch)
            crop = ImageEnhance.Contrast(ImageEnhance.Color(crop).enhance(1.16)).enhance(1.12)
            crop = crop.filter(ImageFilter.UnsharpMask(radius=1.5, percent=135, threshold=2))
            arr = np.asarray(crop, dtype=np.float32)
            sky_glow = np.array([34.0, 56.0, 92.0], dtype=np.float32) * (1.0 - 0.35 * yy_full)
            mx = arr.max(axis=2, keepdims=True)
            arr = np.where(mx < 62.0, np.maximum(arr, sky_glow), arr)
            arr = lift_navy_floor(arr)
            frames.append(Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8)))
        pipe_frames(frames, dest)
        return 1.92

    if kind == "r42b_epic_earth":
        # Shot 6: Full-bleed 9:16 vertical DSCOVR EPIC rotating sunlit Earth ("layer of water ten meters deep
        # covering the planet") with sharp unblurred NASA SVS 3822 polar geomagnetic field lines arching from
        # Earth's North and South poles to the top and bottom of the 1080x1920 canvas (zero blur pad, zero seam).
        src_fg = SVS_ORIG / "svs_12312_epic_earth_timelapse.mp4"
        src_bg = SVS_ORIG / "svs_3822_magfield_left.mp4"
        raw_fg = load_raw_video_frames(src_fg, offset=16.0, frames_n=frames_n, sw=1920, sh=1080, speed=2.5)
        raw_bg = load_raw_video_frames(src_bg, offset=52.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.8)

        yy_f, xx_f = np.mgrid[:H, :W].astype(np.float32)
        frames = []
        for i in range(frames_n):
            u = i / max(1, frames_n - 1)
            # Sharp unblurred 9:16 geomagnetic field lines filling the polar space above & below the Earth globe
            bg_arr = grade_svs3822_vertical(raw_bg[i], cx=600.0 + 120.0 * u, cy=540.0, ch=1040.0 - 40.0 * u)

            # Scale the 760-px DSCOVR EPIC Earth disc by 1.38x -> 1.48x so it spans ~1050..1125 px across the
            # 1080x1920 vertical frame, centered at (540, 960).
            ch = 1390.0 - 95.0 * u       # cw = 782 -> 728 px around the 760-px Earth disc (upscale = 1.48x)
            cw = ch * 9.0 / 16.0
            fg_crop = crop_affine_9x16(raw_fg[i], cx=960.0, cy=540.0, cw=cw, ch=ch)
            fg_crop = ImageEnhance.Contrast(ImageEnhance.Color(fg_crop).enhance(1.16)).enhance(1.10)
            fg_arr = np.asarray(fg_crop, dtype=np.float32)

            # Radial mask around the circular Earth limb (zero horizontal seam anywhere)
            earth_r = 376.0 * (H / ch)
            dist = np.sqrt((xx_f - W / 2.0) ** 2 + (yy_f - H / 2.0) ** 2)
            # Soft atmospheric corona glow right at the limb + sharp field lines in deep space
            limb_glow = np.exp(-((dist - earth_r) / 42.0) ** 2)[:, :, None] * np.array([36.0, 68.0, 118.0], dtype=np.float32)
            earth_alpha = np.clip((earth_r + 4.0 - dist) / 14.0, 0.0, 1.0)[:, :, None]

            comp = (bg_arr + limb_glow) * (1.0 - earth_alpha) + lift_navy_floor(fg_arr) * earth_alpha
            comp = lift_navy_floor(comp)
            frames.append(Image.fromarray(np.clip(comp, 28, 255).astype(np.uint8)))
        pipe_frames(frames, dest)
        return 1.48

    if kind == "r44a_mars":
        # Shot 7: Full-bleed 9:16 vertical crop directly inside the 6787x6787 Viking Orbiter Mars mosaic
        # (PIA00407.jpg), showing the North polar cap, Tharsis, and Valles Marineris edge-to-edge across
        # the entire 1080x1920 frame (zero black corners, zero blur pad, upscale = 0.46x).
        mars_src = Image.open(HARVEST / "PIA00407.jpg").convert("RGB")
        frames = []
        for i in range(frames_n):
            u = i / max(1, frames_n - 1)
            ch = 4560.0 - 380.0 * u      # 4560 -> 4180 px tall out of 6787 px (upscale = 0.46x)
            cw = ch * 9.0 / 16.0         # 2565 -> 2351 px wide (corners at r=2616 < Mars radius 3340 px!)
            cx = 3180.0 + 180.0 * u
            cy = 3320.0 - 140.0 * u
            crop = crop_affine_9x16(mars_src, cx, cy, cw, ch)
            crop = ImageEnhance.Contrast(ImageEnhance.Color(crop).enhance(1.08)).enhance(1.06)
            crop = crop.filter(ImageFilter.UnsharpMask(radius=1.5, percent=125, threshold=2))
            arr = lift_navy_floor(np.asarray(crop, dtype=np.float32))
            frames.append(Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8)))
        pipe_frames(frames, dest)
        return 0.46

    if kind == "r44b_duration":
        # Shot 8: Full-bleed 9:16 vertical pan inside the 11500x11500 NASA VIIRS Eastern Hemisphere Blue Marble
        # (GSFC_20171208_Archive_e001788.jpg, upscale = 0.27x) with the animated R44 duration comparison
        # graphic ("EARTH FIELD FLIP" / "A FEW THOUSAND YEARS" + blue bar) centered in the 9:16 frame.
        bm_src = Image.open(HARVEST / "GSFC_20171208_Archive_e001788.jpg").convert("RGB")
        # Downscale 11500x11500 once by 2x to 5750x5750 with Lanczos for fast, razor-sharp 9:16 affine crops
        bm_5k = bm_src.resize((5750, 5750), Image.Resampling.LANCZOS)

        f_head = ImageFont.truetype(FONT_BOLD, 48)
        f_val = ImageFont.truetype(FONT_BLACK, 52)

        frames = []
        for i in range(frames_n):
            u = i / max(1, frames_n - 1)
            t_local = i / FPS
            ch = 3760.0 - 300.0 * u      # corresponds to 7520 -> 6920 px on 11500x11500 (upscale = 0.28x)
            cw = ch * 9.0 / 16.0         # corners at r=2160 < disc radius 2840 px -> 100% full-bleed Earth!
            cx = 2780.0 + 140.0 * u
            cy = 2880.0 - 110.0 * u
            crop = crop_affine_9x16(bm_5k, cx, cy, cw, ch)
            crop = ImageEnhance.Contrast(ImageEnhance.Color(crop).enhance(1.10)).enhance(1.06)
            arr = np.asarray(crop, dtype=np.float32) * 0.86 + np.array([10.0, 16.0, 28.0], dtype=np.float32)
            arr = lift_navy_floor(arr)
            im = Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8)).convert("RGBA")

            # Animated R44 duration comparison overlay (slides/fades in over 0.35 s, holds < 3.24 s;
            # house comparison_graphics.py style: no UI box/panel so polish_gate sees zero horizontal seam)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            od = ImageDraw.Draw(ov)
            fade_in = min(1.0, max(0.0, t_local / 0.35))
            fade_out = min(1.0, max(0.0, (dur_s - t_local) / 0.30))
            alpha = int(round(255 * min(fade_in, fade_out)))
            if alpha > 4:
                centred(od, BAND_Y0 + 175, "EARTH FIELD FLIP", f_head, (255, 255, 255, alpha), stroke=7)
                val_ease = min(1.0, max(0.0, (t_local - 0.18) / 0.35))
                if val_ease > 0:
                    v_a = int(round(alpha * val_ease))
                    centred(od, BAND_Y0 + 265, "A FEW THOUSAND YEARS", f_val, (255, 224, 0, v_a), stroke=7)
                bar_p = min(1.0, max(0.0, t_local / 0.55))
                bar_p = 1.0 - (1.0 - bar_p) ** 3
                bar_w = int(round(520 * bar_p))
                if bar_w > 4:
                    bx0 = (W - 520) // 2
                    by = BAND_Y0 + 375
                    od.rounded_rectangle(
                        (bx0, by - 5, bx0 + bar_w, by + 5),
                        radius=5,
                        fill=(74, 168, 255, alpha),
                    )
            im.alpha_composite(ov)
            frames.append(im.convert("RGB"))
        pipe_frames(frames, dest)
        return 0.28

    raise ValueError(f"Unknown shot kind: {kind}")


def make_hook(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(H * 0.082 / 0.72)
    if f.size > 132:
        f = ImageFont.truetype(FONT_BLACK, 132)
    while max(d.textlength(t, font=f) for t, _ in HOOK_ROWS) > W * 0.84:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = 220
    boxes = []
    for t, c in HOOK_ROWS:
        boxes.append(centred(d, y, t, f, c, stroke=7))
        y += lh
    im.save(dest)
    return {"text": " / ".join(t for t, _ in HOOK_ROWS), "font_px": f.size, "bboxes": boxes}


def make_title(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.90)
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
    f = font_for(LINE_H * 0.82)
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
    f = font_for(LINE_H * 0.92)
    while d.textlength(text, font=f) > W * 0.78:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y0 + 48, text, f, YELLOW, stroke=7)
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
    bb = centred(d, BAND_Y1 + 36, shown, f, WHITE, stroke=6)
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


def make_cover(dest: Path, f0_png: Path) -> dict:
    im = Image.open(f0_png).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    d = ImageDraw.Draw(im)
    size = 72
    while size < 128:
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
        "ffmpeg", "-y", "-v", "error", "-ss", "398.0", "-t", f"{total:.3f}",
        "-i", str(BED_MP3),
        "-af", f"afade=t=in:d=0.10,afade=t=out:st={total - 0.45:.3f}:d=0.45",
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
        ("rumble", 0.25, -10.0),
        ("tick", 3.36, -8.5),
        ("tick", TITLE_IN, -8.0),
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


def make_review_contact_sheet(mp4_path: Path, out_jpg: Path) -> None:
    """Build a 9-shot mid-frame contact sheet for visual QA."""
    cols, rows_n = 5, 2
    tw, th = 360, 640
    header_h = 28
    sheet = Image.new("RGB", (cols * tw, rows_n * (th + header_h)), (14, 18, 26))
    dr = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT_BOLD, 16)
    for idx, shot in enumerate(SHOT_PLAN):
        mid_t = round(0.5 * (shot["in"] + shot["out"]), 2)
        raw = sp.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{mid_t:.2f}", "-i", str(mp4_path),
            "-vf", f"scale={tw}:{th}:flags=lanczos", "-frames:v", "1",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ])
        im = Image.frombytes("RGB", (tw, th), raw)
        c = idx % cols
        r = idx // cols
        x0 = c * tw
        y0 = r * (th + header_h)
        dr.text((x0 + 8, y0 + 5), f"{idx+1:02d} {shot['row']} ({mid_t:.1f}s) {shot['source'][:18]}", font=f, fill=(235, 240, 250))
        sheet.paste(im, (x0, y0 + header_h))
    sheet.save(out_jpg, quality=92)


def main() -> None:
    vo_sha = sha256(VO_WAV)
    if vo_sha != EXPECTED_VO_SHA256:
        raise SystemExit(f"VO sha256 mismatch: {vo_sha} != {EXPECTED_VO_SHA256}")
    print(f"Verified locked VO SHA-256: {vo_sha}", flush=True)

    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    NAS_SUB_OUT.mkdir(parents=True, exist_ok=True)

    slices, words, last_word_end = build_voice_plan()
    joined = " ".join(w["w"] for w in words)
    print(f"Spoken words: {len(words)} | VO: {VO_LEAD_S:.2f}-{last_word_end:.2f} s | Total: {TOTAL_S:.2f} s", flush=True)

    open_f0 = WORK / "open_f0.png"
    concat_lines = []
    cuts_meta = []
    pool_meta = []
    seen_sources = set()

    for idx, shot in enumerate(SHOT_PLAN):
        piece = WORK / f"piece_{idx:02d}.mp4"
        if shot["kind"] == "r39a_open":
            up = render_r39a_open(round(shot["out"] - shot["in"], 3), piece, open_f0)
        else:
            up = render_standard_shot(shot, piece, open_f0)
        concat_lines.append(f"file '{piece.name}'")
        cuts_meta.append({
            "row": shot["row"],
            "timeline_in": shot["in"],
            "timeline_out": shot["out"],
            "source": shot["source"],
            "upscale": up,
            "framing": {"offset": shot["offset"]},
            "video": True,
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
        print(f"  rendered {shot['row']} ({shot['in']:.2f}-{shot['out']:.2f} s) upscale={up}", flush=True)

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

    final_mp4 = NAS_SUB_OUT / f"{STEM}.mp4"
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
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.30:alpha=1,fade=t=out:st={TITLE_OUT - 0.30:.2f}:d=0.30:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
        f"[3:v]format=rgba,fade=t=in:st={END_CARD_IN:.2f}:d=0.28:alpha=1[ec]",
        f"[v2][ec]overlay=0:0:enable='gte(t,{END_CARD_IN})'[v3]",
        f"[4:v]format=rgba,fade=t=in:st={TEACH_IN}:d=0.25:alpha=1,fade=t=out:st={TEACH_OUT - 0.25:.2f}:d=0.25:alpha=1[th]",
        f"[v3][th]overlay=0:0:enable='gte(t,{TEACH_IN})*lt(t,{TEACH_OUT})'[v4]",
    ]
    last_v = "v4"
    for i, c in enumerate(caps):
        fc.append(f"[{last_v}][{base_idx + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last_v = f"c{i}"
    fc.append(f"[{last_v}]noise=alls=3:allf=t,format=yuv420p[v]")

    run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", ";".join(fc),
        "-map", "[v]", "-map", "5:a",
        *shorts_encode_args(fps=FPS),
        "-t", f"{TOTAL_S:.3f}", str(final_mp4),
    ])

    # Save sidecar files next to final_mp4 BEFORE running gate_shorts_open.py
    words_path = NAS_SUB_OUT / f"{STEM}_words.json"
    transcript_path = NAS_SUB_OUT / f"{STEM}_transcript.txt"
    cuts_path = NAS_SUB_OUT / f"{STEM}_cuts.json"
    pool_path = NAS_SUB_OUT / f"{STEM}_pool.json"
    meta_path = NAS_SUB_OUT / f"{STEM}_meta.json"
    vo_stem_out = NAS_SUB_OUT / f"{STEM}_vo.wav"
    sfx_stem_out = NAS_SUB_OUT / f"{STEM}_sfx.wav"
    bed_stem_out = NAS_SUB_OUT / f"{STEM}_bed.wav"
    shutil.copy2(WORK / "stem_vo.wav", vo_stem_out)
    shutil.copy2(WORK / "stem_sfx.wav", sfx_stem_out)
    shutil.copy2(WORK / "stem_bed.wav", bed_stem_out)

    words_path.write_text(json.dumps(words, indent=2) + "\n")
    transcript_path.write_text(joined + "\n")
    cuts_path.write_text(json.dumps(cuts_meta, indent=2) + "\n")
    pool_path.write_text(json.dumps(pool_meta, indent=2) + "\n")
    meta_path.write_text(json.dumps({
        "slug": SHORT_SLUG,
        "stem": STEM,
        "title": SHORT_TITLE,
        "air_date": AIR_DATE,
        "parent_long_title": LONG_TITLE,
        "spoken": joined,
        "vo_onset_s": VO_LEAD_S,
        "last_word_end_s": last_word_end,
        "duration_s": TOTAL_S,
        "words_file": str(words_path),
        "vo": str(vo_stem_out),
        "audio": aud,
    }, indent=2) + "\n")

    # Save frame 0 JPEG (from actual encoded video at 0.30 s), cover JPEG, and 9-shot contact sheet
    frame0_jpg = NAS_SUB_OUT / f"{STEM}_frame0.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.30", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(frame0_jpg)])
    cover_jpg = NAS_SUB_OUT / f"{STEM}_cover.jpg"
    cover_info = make_cover(cover_jpg, open_f0)
    review_sheet_jpg = NAS_SUB_OUT / f"{STEM}_review_9shots.jpg"
    make_review_contact_sheet(final_mp4, review_sheet_jpg)

    # Run all gates
    def run_gate(cmd: list) -> sp.CompletedProcess:
        return sp.run([str(x) for x in cmd], capture_output=True, text=True)

    g_txt = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", final_mp4, "--air-date", AIR_DATE, "--sheet-dir", NAS_SUB_OUT])
    g_json = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", final_mp4, "--air-date", AIR_DATE, "--sheet-dir", NAS_SUB_OUT, "--json"])
    (NAS_SUB_OUT / f"{STEM}_gate.txt").write_text((g_txt.stdout or "") + (g_txt.stderr or ""))
    (NAS_SUB_OUT / f"{STEM}_gate.json").write_text(g_json.stdout or g_json.stderr)
    print(g_txt.stdout, end="", flush=True)

    tp_f0 = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py", "short", frame0_jpg, "--out", NAS_SUB_OUT / f"{STEM}_frame0_preview.jpg", "--score"])
    tp_cov = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py", "short", cover_jpg, "--out", NAS_SUB_OUT / f"{STEM}_cover_preview.jpg", "--score"])
    print(tp_f0.stdout, end="", flush=True)
    print(tp_cov.stdout, end="", flush=True)

    sfx_res = run_gate([
        sys.executable, REPO / "scripts/sfx_kit.py", "level",
        "--vo", vo_stem_out, "--sfx", sfx_stem_out, "--bed", bed_stem_out,
        "--minutes", f"{TOTAL_S / 60:.3f}",
        "--out", NAS_SUB_OUT / f"{STEM}_sfx_level.json",
    ])
    (NAS_SUB_OUT / f"{STEM}_sfx.txt").write_text((sfx_res.stdout or "") + (sfx_res.stderr or ""))
    print(sfx_res.stdout, end="", flush=True)

    mg_res = run_gate([
        sys.executable, REPO / "scripts/music_gate.py", NAS_FILM,
        "--bed", BED_MP3, "--video", final_mp4,
        "--out", NAS_SUB_OUT / f"{STEM}_music_gate.json",
    ])
    (NAS_SUB_OUT / f"{STEM}_music_gate.txt").write_text((mg_res.stdout or "") + (mg_res.stderr or ""))
    print(mg_res.stdout, end="", flush=True)

    pg_res = run_gate([
        sys.executable, REPO / "scripts/polish_gate.py", final_mp4,
        "--cuts", cuts_path,
        "--out", NAS_SUB_OUT / f"{STEM}_polish_gate.json",
    ])
    (NAS_SUB_OUT / f"{STEM}_polish_gate.txt").write_text((pg_res.stdout or "") + (pg_res.stderr or ""))
    print(pg_res.stdout, end="", flush=True)

    pqa_dir = NAS_SUB_OUT / f"{STEM}_picture_qa"
    pqa_res = run_gate([
        sys.executable, REPO / "scripts/picture_qa.py", final_mp4,
        "--cuts", cuts_path, "--pool", pool_path, "--out-dir", pqa_dir,
    ])
    (NAS_SUB_OUT / f"{STEM}_picture_qa.txt").write_text((pqa_res.stdout or "") + (pqa_res.stderr or ""))
    print(pqa_res.stdout, end="", flush=True)

    # Mirror primary export and key sidecars directly into NAS 10_Shorts/ root and UAT folders
    for f in [
        final_mp4, frame0_jpg, cover_jpg, review_sheet_jpg,
        NAS_SUB_OUT / f"{STEM}_frame0_preview.jpg",
        NAS_SUB_OUT / f"{STEM}_cover_preview.jpg",
        meta_path, words_path, transcript_path, cuts_path, pool_path,
        NAS_SUB_OUT / f"{STEM}_gate.txt", NAS_SUB_OUT / f"{STEM}_gate.json",
    ]:
        shutil.copy2(f, NAS_SHORTS / f.name)

    for uat_dir in (UAT_ICLOUD, UAT_NAS):
        uat_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(final_mp4, uat_dir / final_mp4.name)
        shutil.copy2(cover_jpg, uat_dir / cover_jpg.name)
        shutil.copy2(NAS_SUB_OUT / f"{STEM}_frame0_preview.jpg", uat_dir / f"{STEM}_frame0_preview.jpg")
        shutil.copy2(review_sheet_jpg, uat_dir / review_sheet_jpg.name)

    summary = {
        "stem": STEM,
        "mp4_path": str(final_mp4),
        "mp4_sha256": sha256(final_mp4),
        "nas_shorts_mp4_sha256": sha256(NAS_SHORTS / final_mp4.name),
        "uat_nas_mp4_sha256": sha256(UAT_NAS / final_mp4.name),
        "uat_icloud_mp4_sha256": sha256(UAT_ICLOUD / final_mp4.name),
        "frame0_jpg_sha256": sha256(frame0_jpg),
        "cover_jpg_sha256": sha256(cover_jpg),
        "review_sheet_jpg_sha256": sha256(review_sheet_jpg),
        "vo_sha256": vo_sha,
        "bed_sha256": sha256(BED_MP3),
        "duration_s": TOTAL_S,
        "words_count": len(words),
        "vo_onset_s": VO_LEAD_S,
        "last_word_end_s": last_word_end,
        "tail_gap_s": round(TOTAL_S - last_word_end, 2),
        "audio": aud,
        "hook": hook_info,
        "title": title_info,
        "teach": {"text": TEACH_TEXT, "in": TEACH_IN, "out": TEACH_OUT, "bbox": teach_bb},
        "end_card": end_info,
        "cover": cover_info,
        "gates": {
            "gate_shorts_open_rc": g_txt.returncode,
            "thumb_preview_frame0_rc": tp_f0.returncode,
            "thumb_preview_cover_rc": tp_cov.returncode,
            "sfx_level_rc": sfx_res.returncode,
            "music_gate_rc": mg_res.returncode,
            "polish_gate_rc": pg_res.returncode,
            "picture_qa_rc": pqa_res.returncode,
        },
    }
    (NAS_SUB_OUT / f"{STEM}_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("SUMMARY:", json.dumps(summary["gates"], indent=2), flush=True)
    if any(v != 0 for v in summary["gates"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
