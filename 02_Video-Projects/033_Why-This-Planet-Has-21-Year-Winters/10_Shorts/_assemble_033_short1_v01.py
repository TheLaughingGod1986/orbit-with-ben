#!/usr/bin/env python3
"""033 Uranus — Active Short #1 v01 Assembler (J2317, Test A Opening Short).

Title: Why Does Knocked-Sideways Uranus Have 21-Year Winters?
Slug / Stem: 033_short01_testA_opening / 033_short01_testA_opening_v01
Air Date: 2026-12-18 (Path A Fri 18 Dec 11:30Z slot; Path B Sat 12 Dec / Wed 9 Dec 11:30Z slot)
Parent Long (033): Why Knocked-Sideways Uranus Has 21-Year Winters

Lifts verbatim cold-open sentences R01-R06 (0.100-30.980 s, 79 words) + R09 central question
(49.320-53.500 s, 11 words = 90 spoken words total) from locked master VO
`02_Voiceover/uranus_vo_v01.wav` (SHA-256: 3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460),
ending cleanly on the central question 033 answers (LEARNINGS 17).
Reframes the J2300/J2299 reconciled 033 cold-open assets to 9:16 (1080x1920, 25 fps CFR).
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
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

Image.MAX_IMAGE_PIXELS = None

HERE = Path(__file__).resolve().parent
REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "033_Why-This-Planet-Has-21-Year-Winters"
)
NAS_HARV = NAS_FILM / "03_Reference-Material" / "harvest_J2299_v01"
NAS_CLIPS = NAS_FILM / "04_Generated-Clips"
NAS_SHORTS = NAS_FILM / "10_Shorts"
NAS_SUB_OUT = NAS_SHORTS / "033_short01_testA_opening" / "06_Final-Exports"

VO_WAV = NAS_FILM / "02_Voiceover" / "uranus_vo_v01.wav"
EXPECTED_VO_SHA256 = "3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460"
STT_JSON = NAS_FILM / "02_Voiceover" / "stt" / "uranus_vo_v01" / "stt_raw.json"
BED_MP3 = NAS_FILM / "05_Music" / "uranus_score_bed_v01.mp3"
KIT_DIR = NAS_FILM / "06_Sound-Effects" / "kit_v01"

WORK = Path("/private/tmp/033_short1_testA_opening_work_v01")
UAT_ICLOUD = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/033_shorts_v01")
UAT_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/033_shorts_v01")

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import gate_shorts_open as gso  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 25
SR = 48000
BAND_H = round(W * 9 / 16)          # 608 px
BAND_Y0 = (H - BAND_H) // 2         # 656 px
BAND_Y1 = BAND_Y0 + BAND_H          # 1264 px
LINE_H = round(BAND_H * 0.115)      # 70 px

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)         # #FFE000
CYAN = (110, 225, 250, 255)
NAVY_FLOOR = np.array([28.0, 38.0, 58.0], dtype=np.float32)

STEM = "033_short01_testA_opening_v01"
SHORT_SLUG = "033_short01_testA_opening"
SHORT_TITLE = "Why Does Knocked-Sideways Uranus Have 21-Year Winters?"
ALT_TITLE = "What Would You See at the North Pole of Knocked-Sideways Uranus?"
AIR_DATE = "2026-12-18"
LONG_TITLE = "Why Knocked-Sideways Uranus Has 21-Year Winters"

TITLE_ROWS = [
    "Why Does Knocked-Sideways",
    "Uranus Have",
    "21-Year Winters?",
]
END_CARD_LINE = "Full film on the channel"
END_ROWS = [
    ("Why Knocked-Sideways", WHITE),
    ("Uranus Has", WHITE),
    ("21-Year Winters", WHITE),
    (END_CARD_LINE, YELLOW),
]
HOOK_ROWS = [("21-YEAR", WHITE), ("NIGHT", YELLOW)]
COVER_ROWS = [("21-YEAR", WHITE), ("WINTERS?", YELLOW)]

HOOK_END = 2.00
TITLE_IN, TITLE_OUT = 9.00, 13.50
TEACH_IN, TEACH_OUT = 18.20, 22.00
TEACH_TEXT = "URANUS TILT: 97.77° (> 4× EARTH)"

# Spoken VO segments from uranus_vo_v01.wav:
# Segment 0: contiguous R01-R06 (0.100-30.980 s, 30.880 s, 79 words)
# Segment 1: R09 central question (49.320-53.500 s, 4.180 s, 11 words)
VO_SEGMENTS = [
    (0.100, 30.980),
    (49.320, 53.500),
]
VO_LEAD_S = 0.08
VO_GAPS = [0.24]              # 0.24 s breath before R09 question; last word ends at 35.38 s
TOTAL_S = 36.48               # 912 frames at 25 fps CFR (tail_gap = 36.48 - 35.38 = 1.10 s < 1.20 s)
END_CARD_IN = 35.44           # 1.04 s loop/end card tail (< 1.20 s lock)

# 14-shot cut plan (13 cuts, every cut on an exact 25fps frame inside a verified Scribe silence gap,
# Cut 1 = 2.36 s <= 2.80 s, Cut 2 = 4.36 s <= 4.80 s, max shot = 4.00 s <= 4.00 s)
SHOT_PLAN = [
    {
        "row": "R01a",
        "in": 0.00,
        "out": 2.36,
        "kind": "r01a_open",
        "source": "r01_sourced_composite_v01_silent.mp4",
        "title": "Voyager 2 PIA18182 and JWST NIRCam weic2310a 97.77-deg sideways Uranus opener",
        "offset": 0.4,
        "video": True,
    },
    {
        "row": "R01b",
        "in": 2.36,
        "out": 4.36,
        "kind": "still_pan",
        "source": "PIA01280.jpg",
        "title": "Hubble Space Telescope view of Uranus clouds and vertical rings",
        "offset": 0.0,
        "video": True,
        "zoom0": 1.04,
        "zoom1": 1.18,
        "dx": 28,
        "dy": -18,
    },
    {
        "row": "R02",
        "in": 4.36,
        "out": 8.16,
        "kind": "still_pan",
        "source": "PIA01391.jpg",
        "title": "Voyager 2 Uranus turquoise crescent terminator in natural colour",
        "offset": 0.0,
        "video": True,
        "zoom0": 1.02,
        "zoom1": 1.16,
        "dx": -32,
        "dy": 20,
    },
    {
        "row": "R03a",
        "in": 8.16,
        "out": 11.88,
        "kind": "r03a_winter_sweep",
        "source": "PIA00032_left_globe.jpg",
        "title": "Voyager 2 Uranus true-colour single globe (left crop of PIA00032)",
        "offset": 0.0,
        "video": True,
    },
    {
        "row": "R03b",
        "in": 11.88,
        "out": 13.88,
        "kind": "still_pan",
        "source": "PIA00346.jpg",
        "title": "Voyager 2 parting view of Uranus dark winter hemisphere crescent",
        "offset": 0.0,
        "video": True,
        "zoom0": 1.04,
        "zoom1": 1.16,
        "dx": 24,
        "dy": -16,
    },
    {
        "row": "R04a",
        "in": 13.88,
        "out": 15.84,
        "kind": "still_pan",
        "source": "PIA18033.jpg",
        "title": "Earth Blue Marble from Apollo 17",
        "offset": 0.0,
        "video": True,
        "zoom0": 1.00,
        "zoom1": 1.10,
        "dx": -18,
        "dy": 12,
    },
    {
        "row": "R04b",
        "in": 15.84,
        "out": 18.20,
        "kind": "still_pan",
        "source": "PIA18033.jpg",
        "title": "Earth Blue Marble from Apollo 17",
        "offset": 12.0,
        "video": True,
        "zoom0": 1.14,
        "zoom1": 1.26,
        "dx": 22,
        "dy": -14,
    },
    {
        "row": "R05a",
        "in": 18.20,
        "out": 22.20,
        "kind": "r05a_tilt_gauge",
        "source": "code_graphic_033_r05_tilt_gauge.mp4",
        "title": "Earth 23.44-deg vs Uranus 97.77-deg Axial Tilt Protractor Gauge (033 R05)",
        "offset": 0.0,
        "video": True,
    },
    {
        "row": "R05b",
        "in": 22.20,
        "out": 25.00,
        "kind": "still_pan",
        "source": "PIA00143.jpg",
        "title": "Voyager 2 Uranus ring system back-lit",
        "offset": 0.0,
        "video": True,
        "zoom0": 1.03,
        "zoom1": 1.16,
        "dx": -26,
        "dy": 16,
    },
    {
        "row": "R06a",
        "in": 25.00,
        "out": 28.00,
        "kind": "still_pan",
        "source": "weic2310a_unannotated.png",
        "title": "JWST NIRCam Uranus rings and polar cap (weic2310a unannotated)",
        "offset": 0.0,
        "video": True,
        "zoom0": 1.00,
        "zoom1": 1.12,
        "dx": 24,
        "dy": -14,
    },
    {
        "row": "R06b",
        "in": 28.00,
        "out": 31.08,
        "kind": "still_pan",
        "source": "weic2310a_unannotated.png",
        "title": "JWST NIRCam Uranus rings and polar cap (weic2310a unannotated)",
        "offset": 12.0,
        "video": True,
        "zoom0": 1.14,
        "zoom1": 1.26,
        "dx": -24,
        "dy": 16,
    },
    {
        "row": "R09a",
        "in": 31.08,
        "out": 33.56,
        "kind": "still_pan",
        "source": "PIA02963_borderless.jpg",
        "title": "Hubble Space Telescope Uranus outer rings and moons (borderless crop)",
        "offset": 0.0,
        "video": True,
        "zoom0": 1.02,
        "zoom1": 1.14,
        "dx": 22,
        "dy": -14,
    },
    {
        "row": "R09b",
        "in": 33.56,
        "out": 35.44,
        "kind": "still_pan",
        "source": "PIA18182.jpg",
        "title": "Voyager 2 Uranus full globe in natural colour",
        "offset": 0.0,
        "video": True,
        "zoom0": 1.04,
        "zoom1": 1.16,
        "dx": -20,
        "dy": 12,
    },
    {
        "row": "R01_loop",
        "in": 35.44,
        "out": 36.48,
        "kind": "match0",
        "source": "frame0_hold_033_short01_testA_opening.png",
        "title": "Opening frame held for seamless loop",
        "offset": 0.0,
        "video": True,
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
    stroke_fill = (16, 26, 46, alpha)
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
    """Guarantee max(R,G,B) >= 54 (V >= 0.212 > 0.18) so visor_frac == 0.0000 and near_black == 0.0%."""
    mx = arr.max(axis=2, keepdims=True)
    return np.where(mx < 54.0, np.maximum(arr, NAVY_FLOOR), arr)


def mask_16x9_corner_credit(im: Image.Image) -> Image.Image:
    """Remove any bottom-left 16:9 corner credit (Shorts carry none)."""
    arr = np.asarray(im, dtype=np.float32).copy()
    patch_bot = arr[880:950, 20:620]
    arr[950:1080, 0:620] = np.median(patch_bot.reshape(-1, 3), axis=0)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


_STAR_PLATE_16X9: Image.Image | None = None
_STAR_PLATE_9X16: Image.Image | None = None


def get_star_plates() -> tuple[Image.Image, Image.Image]:
    global _STAR_PLATE_16X9, _STAR_PLATE_9X16
    if _STAR_PLATE_16X9 is None or _STAR_PLATE_9X16 is None:
        raw = Image.open(NAS_HARV / "weic2332a_hires.jpg").convert("RGB")
        # Use pure outer deep-field starfield corners (away from central Uranus rings) so zero ring halo appears in surround
        s16 = raw.crop((0, 0, 768, 432)).resize((1920, 1080), Image.Resampling.LANCZOS)
        a16 = (np.asarray(s16, dtype=np.float32) - 12.0) * 1.35 + np.array([28.0, 38.0, 58.0], dtype=np.float32)
        _STAR_PLATE_16X9 = Image.fromarray(np.clip(lift_navy_floor(a16), 28, 255).astype(np.uint8))

        s9 = raw.crop((0, 0, 480, 854)).resize((W, H), Image.Resampling.LANCZOS)
        a9 = (np.asarray(s9, dtype=np.float32) - 12.0) * 1.35 + np.array([28.0, 38.0, 58.0], dtype=np.float32)
        _STAR_PLATE_9X16 = Image.fromarray(np.clip(lift_navy_floor(a9), 28, 255).astype(np.uint8))
    return _STAR_PLATE_16X9, _STAR_PLATE_9X16


def composite_band_on_natural_blur(
    fg_16x9: Image.Image,
    bg_16x9: Image.Image,
    mask_credit: bool = True,
    zoom: float = 1.0,
    pan_x: float = 0.0,
    pan_y: float = 0.0,
) -> Image.Image:
    """Composite a 16:9 frame inside the 9:16 centre band over a clean, natural Gaussian-blurred
    vertical fill derived directly from real NASA pixels (zero synthetic sine waves, arcs, or painted dots)."""
    if mask_credit:
        fg_16x9 = mask_16x9_corner_credit(fg_16x9)
        bg_16x9 = mask_16x9_corner_credit(bg_16x9)
    if zoom > 1.001 or abs(pan_x) > 0.05 or abs(pan_y) > 0.05:
        w, h = fg_16x9.size
        cw, ch = w / max(zoom, 1.0), h / max(zoom, 1.0)
        x0 = max(0.0, min(w - cw, (w - cw) / 2.0 + pan_x))
        y0 = max(0.0, min(h - ch, (h - ch) / 2.0 + pan_y))
        fg_16x9 = fg_16x9.transform((w, h), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), resample=Image.Resampling.BICUBIC)

    _, star_9x16 = get_star_plates()
    bg_fit = ImageOps.fit(bg_16x9, (W, H), method=Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(110))
    bg_arr = (
        np.asarray(bg_fit, dtype=np.float32) * 0.22
        + np.asarray(star_9x16, dtype=np.float32) * 0.78
    )
    bg_arr = lift_navy_floor(bg_arr)

    fg_band = ImageOps.fit(fg_16x9, (W, BAND_H), method=Image.Resampling.LANCZOS)
    fg_band = ImageEnhance.Contrast(ImageEnhance.Color(fg_band).enhance(1.12)).enhance(1.08)
    fg_arr = np.asarray(fg_band, dtype=np.float32)
    fg_arr = lift_navy_floor(fg_arr)

    # Smooth cosine feather over 96 px at top and bottom of the 16:9 band so polish_gate sees zero horizontal seam
    feather = 96
    u = np.linspace(0.0, 1.0, feather, dtype=np.float32)
    ramp = 0.5 - 0.5 * np.cos(np.pi * u)
    mask = np.ones(BAND_H, dtype=np.float32)
    mask[:feather] = ramp
    mask[-feather:] = ramp[::-1]

    band_slice = bg_arr[BAND_Y0:BAND_Y1]
    band_slice[:] = band_slice * (1.0 - mask)[:, None, None] + fg_arr * mask[:, None, None]
    bg_arr = lift_navy_floor(bg_arr)
    return Image.fromarray(np.clip(bg_arr, 28, 255).astype(np.uint8))


def prepare_16x9_from_still(src_path: Path) -> Image.Image:
    """Prepare a rich 1920x1080 plate from a high-res NASA still over a seamless deep-space starfield surround
    with elliptical + dark-space feathering so square NASA plates leave zero rectangular box edges."""
    im = Image.open(src_path).convert("RGB")
    star_16x9, _ = get_star_plates()
    soft_glow = ImageOps.fit(im, (1920, 1080), method=Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(110))
    bg_arr = (
        np.asarray(star_16x9, dtype=np.float32) * 0.82
        + np.asarray(soft_glow, dtype=np.float32) * 0.18
    )
    bg_arr = lift_navy_floor(bg_arr)

    # Fit subject cleanly so full planet globe + rings are preserved with crisp detail
    scale = min(1760.0 / im.width, 980.0 / im.height)
    nw, nh = round(im.width * scale), round(im.height * scale)
    fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
    fg_arr = lift_navy_floor(np.asarray(fg, dtype=np.float32))

    # Smooth elliptical feather + dark-space blend so square image borders vanish completely
    yy, xx = np.mgrid[0:nh, 0:nw].astype(np.float32)
    rx = (xx - nw * 0.5) / max(1.0, nw * 0.48)
    ry = (yy - nh * 0.5) / max(1.0, nh * 0.48)
    r = np.sqrt(rx * rx + ry * ry)
    radial = np.clip((1.02 - r) / 0.28, 0.0, 1.0)
    radial = 0.5 - 0.5 * np.cos(np.pi * radial)

    luma_max = np.asarray(fg, dtype=np.float32).max(axis=2)
    space_key = np.clip((luma_max - 14.0) / 38.0, 0.0, 1.0)
    # Keep inner core solid while outer corners key out dark space smoothly
    core = np.clip((0.72 - r) / 0.22, 0.0, 1.0)
    alpha = radial * np.maximum(core, space_key)

    x0 = (1920 - nw) // 2
    y0 = (1080 - nh) // 2
    patch = bg_arr[y0:y0 + nh, x0:x0 + nw]
    patch[:] = patch * (1.0 - alpha[:, :, None]) + fg_arr * alpha[:, :, None]
    return Image.fromarray(np.clip(lift_navy_floor(bg_arr), 28, 255).astype(np.uint8))


def make_globe_rgba(path: Path, diameter: int) -> Image.Image:
    im = Image.open(path).convert("RGB")
    side = min(im.size)
    left, top = (im.width - side) // 2, (im.height - side) // 2
    im = im.crop((left, top, left + side, top + side)).resize((diameter, diameter), Image.Resampling.LANCZOS)
    circle = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(circle).ellipse((2, 2, diameter - 3, diameter - 3), fill=255)
    sky = im.convert("L").point(lambda p: 0 if p < 10 else 255)
    alpha = ImageChops.multiply(circle, sky)
    out = im.convert("RGBA")
    out.putalpha(alpha)
    ImageDraw.Draw(out).ellipse((2, 2, diameter - 3, diameter - 3), outline=(180, 225, 255, 170), width=max(2, diameter // 85))
    return out


def render_r01a_open(dur_s: float, dest: Path, save_f0: Path) -> float:
    """Shot 1 (0.00-2.36 s): Full 9:16 reframe of R01 sideways 97.77-deg Uranus rotation time-lapse
    (r01_sourced_composite_v01_silent.mp4 + Hubble PIA01280 cloud rotation across the globe),
    with brisk orbital push/pan so motion_0_1s >= 18, f0diff >= 3.5, visor_frac == 0.0."""
    frames_n = round(dur_s * FPS)
    r01_src = NAS_CLIPS / "J2334_fix" / "r01_sourced_composite_v01_silent.mp4"
    raw = load_raw_video_frames(r01_src, offset=0.10, frames_n=frames_n, sw=1920, sh=1080, speed=2.3)

    # Also load real Hubble PIA01280 cloud band texture to animate visible rotation across the sideways globe
    hubble = Image.open(NAS_HARV / "PIA01280.jpg").convert("RGB").resize((900, 900), Image.Resampling.LANCZOS)
    star_bg = (
        Image.open(NAS_HARV / "weic2332a_hires.jpg")
        .convert("RGB")
        .crop((0, 0, 480, 854))
        .resize((1800, 2400), Image.Resampling.LANCZOS)
    )

    frames = []
    for i, im in enumerate(raw):
        im = mask_16x9_corner_credit(im)
        u = i / max(1, frames_n - 1)
        # Dynamic 9:16 vertical crop with exact 9:16 aspect ratio (cw = ch * 9 / 16) so Uranus stays circular
        # and brisk pan/zoom + parallax starfield so motion_0_1s >= 12.0 and f0diff >= 3.5
        ch = 1040.0 - 220.0 * u
        cw = ch * (W / H)
        cx = 840.0 + 260.0 * u
        cy = 480.0 + 120.0 * u
        x0 = max(0.0, min(1920.0 - cw, cx - cw * 0.5))
        y0 = max(0.0, min(1080.0 - ch, cy - ch * 0.5))
        crop = im.transform((W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), resample=Image.Resampling.BICUBIC)

        # Blend real moving JWST wide-field starfield + Hubble cloud rotation so frame-to-frame motion is rich
        sx0 = 80.0 + 540.0 * u
        sy0 = 120.0 + 380.0 * u
        star_crop = star_bg.transform((W, H), Image.Transform.EXTENT, (sx0, sy0, sx0 + W, sy0 + H), resample=Image.Resampling.BICUBIC)

        hx0 = 60.0 + 340.0 * u
        hy0 = 40.0 + 260.0 * u
        hub_crop = hubble.transform((W, H), Image.Transform.EXTENT, (hx0, hy0, hx0 + 540.0, hy0 + 540.0), resample=Image.Resampling.BICUBIC)

        a_c = np.asarray(crop, dtype=np.float32)
        a_s = np.asarray(star_crop, dtype=np.float32)
        a_h = np.asarray(hub_crop, dtype=np.float32)

        # Combine main sideways ringed Uranus composite with moving starfield in dark surround and Hubble cloud bands on globe
        luma = a_c.mean(axis=2, keepdims=True)
        w_globe = np.clip((luma - 45.0) / 85.0, 0.0, 1.0)
        blended = a_c * 0.78 + a_s * (1.0 - w_globe) * 0.48 + a_h * w_globe * 0.34

        norm = np.clip(blended / 255.0, 0.0, 1.0)
        r = 30.0 + 215.0 * np.power(norm[:, :, 0], 0.55)
        g = 42.0 + 210.0 * np.power(norm[:, :, 1], 0.52)
        b = 64.0 + 190.0 * np.power(norm[:, :, 2], 0.50)
        rgb = lift_navy_floor(np.stack([r, g, b], axis=-1))
        frame = Image.fromarray(np.clip(rgb, 30, 255).astype(np.uint8))
        if i == 0:
            frame.save(save_f0)
        frames.append(frame)

    pipe_frames(frames, dest)
    return 1.25


def render_standard_shot(shot: dict, dest: Path, open_f0: Path) -> float:
    dur_s = round(shot["out"] - shot["in"], 3)
    frames_n = round(dur_s * FPS)
    kind = shot["kind"]

    if kind == "match0":
        im = Image.open(open_f0).convert("RGB")
        pipe_frames([im] * frames_n, dest)
        return 1.0

    if kind == "still_pan":
        src_path = NAS_HARV / shot["source"]
        base_16x9 = prepare_16x9_from_still(src_path)
        z0, z1 = shot["zoom0"], shot["zoom1"]
        dx, dy = shot["dx"], shot["dy"]
        frames = []
        for i in range(frames_n):
            u = i / max(1, frames_n - 1)
            z = z0 + (z1 - z0) * u
            px = -dx * 0.5 + dx * u
            py = -dy * 0.5 + dy * u
            frames.append(
                composite_band_on_natural_blur(
                    base_16x9, base_16x9, mask_credit=False, zoom=z, pan_x=px, pan_y=py
                )
            )
        pipe_frames(frames, dest)
        return round(max(z0, z1), 2)

    if kind == "r03a_winter_sweep":
        # Clean text-free 21-year polar winter night shadow sweep across Voyager 2 cyan Uranus globe (PIA00032_left_globe.jpg)
        # under the first half of the 9.0-13.5 s parent-title banner (zero background text collision!)
        bg_16x9 = get_star_plates()[0].copy()
        g_u = make_globe_rgba(NAS_HARV / "PIA00032_left_globe.jpg", 640)
        frames = []
        for i in range(frames_n):
            u = i / max(1, frames_n - 1)
            fg = bg_16x9.copy().convert("RGBA")
            gx = int(round(640 + 28 * u))
            gy = int(round(220 - 16 * u))
            fg.alpha_composite(g_u, (gx, gy))
            shade = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
            sd = ImageDraw.Draw(shade)
            sd.pieslice((gx, gy, gx + 640, gy + 640), 85, 85 + int(round(185 * u)), fill=(14, 24, 44, 175))
            fg.alpha_composite(shade)
            fg_rgb = fg.convert("RGB")
            frames.append(
                composite_band_on_natural_blur(
                    fg_rgb, fg_rgb, mask_credit=False, zoom=1.02 + 0.08 * u, pan_x=18 * u, pan_y=-10 * u
                )
            )
        pipe_frames(frames, dest)
        return 1.20

    if kind == "r05a_tilt_gauge":
        # Clean 9:16-framed Earth 23.44 deg vs Uranus 97.77 deg axial tilt gauge over real JWST starfield (weic2332a_hires.jpg)
        # with real Blue Marble Earth (PIA18033.jpg) and real Voyager 2 Uranus (PIA18182.jpg), free of duplicate 16:9 text
        # so the single 9:16 Teach overlay ("URANUS TILT: 97.77° (> 4× EARTH)") is the sole text card on screen!
        bg_16x9 = get_star_plates()[0].copy()
        g_e = make_globe_rgba(NAS_HARV / "PIA18033.jpg", 440)
        g_u = make_globe_rgba(NAS_HARV / "PIA18182.jpg", 480)
        frames = []
        for i in range(frames_n):
            u = i / max(1, frames_n - 1)
            ease_u = 0.5 - 0.5 * math.cos(math.pi * min(1.0, u / 0.82))
            fg = bg_16x9.copy().convert("RGBA")
            ex, ey = 250, 260
            ux, uy = 1170, 240
            fg.alpha_composite(g_e, (ex, ey))
            fg.alpha_composite(g_u, (ux, uy))
            d = ImageDraw.Draw(fg)
            e_ang = 23.44 * ease_u
            u_ang = 97.77 * ease_u
            ecx, ecy = ex + 220, ey + 220
            ucx, ucy = ux + 240, uy + 240
            d.arc((ecx - 250, ecy - 250, ecx + 250, ecy + 250), -90, -90 + e_ang, fill=CYAN, width=12)
            d.arc((ucx - 270, ucy - 270, ucx + 270, ucy + 270), -90, -90 + u_ang, fill=YELLOW, width=14)
            re_rad = math.radians(-90 + e_ang)
            ru_rad = math.radians(-90 + u_ang)
            d.line(
                (ecx - 265 * math.cos(re_rad), ecy - 265 * math.sin(re_rad), ecx + 265 * math.cos(re_rad), ecy + 265 * math.sin(re_rad)),
                fill=CYAN, width=6,
            )
            d.line(
                (ucx - 285 * math.cos(ru_rad), ucy - 285 * math.sin(ru_rad), ucx + 285 * math.cos(ru_rad), ucy + 285 * math.sin(ru_rad)),
                fill=YELLOW, width=8,
            )
            fg_rgb = fg.convert("RGB")
            frames.append(
                composite_band_on_natural_blur(
                    fg_rgb, bg_16x9, mask_credit=False, zoom=1.01 + 0.05 * u, pan_x=14 * u, pan_y=-8 * u
                )
            )
        pipe_frames(frames, dest)
        return 1.00

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
    return {"font_px": f.size, "rows": placed, "joined": SHORT_TITLE}


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
    while d.textlength(text, font=f) > W * 0.82:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y1 - 90, text, f, YELLOW, stroke=7)
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
    im = ImageEnhance.Color(im).enhance(1.22)
    im = ImageEnhance.Contrast(im).enhance(1.12)
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
        "ffmpeg", "-y", "-v", "error", "-ss", "0.0", "-t", f"{total:.3f}",
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
        ("tick", 4.38, -8.5),
        ("tick", TITLE_IN, -8.0),
        ("tick", TEACH_IN, -8.0),
        ("tick", 31.10, -8.5),
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

    # Verify zero word splits across all shot boundaries
    for shot in SHOT_PLAN[:-1]:
        cut_t = shot["out"]
        for w in words:
            if w["s"] + 0.005 < cut_t < w["e"] - 0.005:
                raise SystemExit(f"Cut at {cut_t:.2f}s splits word {w['w']!r} ({w['s']:.3f}-{w['e']:.3f}s)")
    print("Verified 0 spoken words split across all 13 cut boundaries.", flush=True)

    open_f0 = WORK / "open_f0.png"
    concat_lines = []
    cuts_meta = []
    pool_meta = []
    seen_sources = set()

    for idx, shot in enumerate(SHOT_PLAN):
        piece = WORK / f"piece_{idx:02d}.mp4"
        if shot["kind"] == "r01a_open":
            up = render_r01a_open(round(shot["out"] - shot["in"], 3), piece, open_f0)
        else:
            up = render_standard_shot(shot, piece, open_f0)
        concat_lines.append(f"file '{piece.name}'")
        c_entry = {
            "row": shot["row"],
            "timeline_in": shot["in"],
            "timeline_out": shot["out"],
            "source": shot["source"],
            "upscale": up,
            "video": bool(shot.get("video", False)),
            "framing": {"offset": shot["offset"]} if shot.get("offset") is not None else {"crop": "9:16 band"},
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
    fc.append(f"[{last_v}]noise=alls=2:allf=t,format=yuv420p[v]")

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
        "alt_title": ALT_TITLE,
        "air_date": AIR_DATE,
        "test_a": True,
        "parent_long_title": LONG_TITLE,
        "spoken": joined,
        "vo_onset_s": VO_LEAD_S,
        "last_word_end_s": last_word_end,
        "duration_s": TOTAL_S,
        "words_file": str(words_path),
        "vo": str(vo_stem_out),
        "audio": aud,
    }, indent=2) + "\n")

    # Save frame 0 JPEG (from actual encoded video at 0.30 s) and cover JPEG
    frame0_jpg = NAS_SUB_OUT / f"{STEM}_frame0.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.30", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(frame0_jpg)])
    cover_jpg = NAS_SUB_OUT / f"{STEM}_cover.jpg"
    cover_info = make_cover(cover_jpg, open_f0)

    # Build a 14-shot mid-frame contact sheet for visual QA
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
    cols_s = 5
    rows_s = (len(shot_tiles) + cols_s - 1) // cols_s
    sheet_14 = Image.new("RGB", (360 * cols_s, 640 * rows_s), (18, 22, 30))
    for idx, im_t in enumerate(shot_tiles):
        sheet_14.paste(im_t, ((idx % cols_s) * 360, (idx // cols_s) * 640))
    sheet_14_path = NAS_SUB_OUT / f"{STEM}_review_14shots.jpg"
    sheet_14.save(sheet_14_path, quality=92)

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
        final_mp4, frame0_jpg, cover_jpg,
        NAS_SUB_OUT / f"{STEM}_frame0_preview.jpg",
        NAS_SUB_OUT / f"{STEM}_cover_preview.jpg",
        sheet_14_path,
        meta_path, words_path, transcript_path, cuts_path, pool_path,
        NAS_SUB_OUT / f"{STEM}_gate.txt", NAS_SUB_OUT / f"{STEM}_gate.json",
    ]:
        shutil.copy2(f, NAS_SHORTS / f.name)

    for uat_dir in (UAT_NAS, UAT_ICLOUD):
        try:
            uat_dir.mkdir(parents=True, exist_ok=True)
            for src in (final_mp4, cover_jpg, NAS_SUB_OUT / f"{STEM}_frame0_preview.jpg"):
                dst = uat_dir / src.name
                if dst.exists():
                    dst.unlink()
                shutil.copy2(src, dst)
        except OSError as exc:
            print(f"Note: UAT copy skipped for {uat_dir}: {exc}", flush=True)

    summary = {
        "stem": STEM,
        "mp4_path": str(final_mp4),
        "mp4_sha256": sha256(final_mp4),
        "frame0_jpg_sha256": sha256(frame0_jpg),
        "cover_jpg_sha256": sha256(cover_jpg),
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
