#!/usr/bin/env python3
"""031 Magnetic Field Flip — Active Short #2 v01 Assembler (J2389).

Title: What If the Solar Wind Blew Earth's Atmosphere Into Space?
Slug / Stem: sat12_solar_wind_air / 031_short_sat12_solar_wind_air_v01
Air Date: 2026-12-12 (Path A Sat 11:30Z slot; zero collision with 026-029)
Parent Long (031): What Happens When Earth's Magnetic Field Flips?

Lifts verbatim sentences s65, s67, s70, s74 (398.42-461.62 s, 64 spoken words)
from locked master VO `02_Voiceover/magnetic_field_flip_vo_v02a.wav`
(SHA-256: 3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6).
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
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

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
NAS_PLATES_V01 = NAS_EDIT / "nas_plates_v01"
NAS_PLATES_V02 = NAS_EDIT / "nas_plates_v02"
NAS_J2141 = NAS_EDIT / "j2141_remaining_v01" / "plates"
DESK = Path("/Users/benjaminoats/_desk")

VO_WAV = NAS_FILM / "02_Voiceover" / "magnetic_field_flip_vo_v02a.wav"
EXPECTED_VO_SHA256 = "3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6"
STT_JSON = NAS_FILM / "02_Voiceover" / "stt" / "magnetic_field_flip_vo_v02a" / "stt_raw.json"
BED_MP3 = NAS_FILM / "05_Music" / "magnetic_field_flip_score_bed_v01.mp3"
KIT_DIR = NAS_FILM / "06_Sound-Effects" / "kit_v01"

WORK = Path("/private/tmp/031_short2_solar_wind_work_v01")
UAT_ICLOUD = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/031_shorts_v01")
UAT_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/031_shorts_v01")

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
GOLD = (255, 214, 64, 255)
ICE = (165, 218, 255, 255)
NAVY_FLOOR = np.array([28.0, 40.0, 64.0], dtype=np.float32)

STEM = "031_short_sat12_solar_wind_air_v01"
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
        "offset": 6.0,
    },
    {
        "row": "R39b",
        "in": 2.36,
        "out": 3.32,
        "kind": "r39b_bowshock",
        "source": "nasa_svs_3822_magfield_left.mp4",
        "title": "Geomagnetic Field Lines in Space (NASA SVS 3822)",
        "offset": 24.0,
    },
    {
        "row": "R40",
        "in": 3.32,
        "out": 6.76,
        "kind": "r40_multipole",
        "source": "code_graphic_031_r40a_never_vanishes_v01.mp4",
        "title": "Multipole Magnetic Field Never Vanishes Graphic (031 R40)",
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
        "kind": "r42a_column",
        "source": "code_graphic_031_r42b_column_mass_v01.mp4",
        "title": "Atmospheric Column Mass 1 kg/cm2 Graphic (031 R42)",
        "offset": 0.0,
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
        "source": "code_graphic_031_r44c_duration_comparison_v01.mp4",
        "title": "Mars Loss vs Earth Flip Duration Comparison Graphic (031 R44)",
        "offset": 0.0,
    },
    {
        "row": "R39_loop",
        "in": 23.16,
        "out": 24.48,
        "kind": "match0",
        "source": "frame0_hold_sat12_solar_wind_air.png",
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
    dur_need = (frames_n / FPS) * speed + 0.5
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


def make_cosmic_backdrop() -> Image.Image:
    """Build a rich 1600x2560 sapphire-indigo cosmic backdrop from Blue Marble + starfield (B >= 56 everywhere)."""
    bw, bh = 1600, 2560
    bm = Image.open(HARVEST / "GSFC_20171208_Archive_e001788.jpg").convert("RGB")
    bm_blur = ImageOps.fit(bm, (bw, bh), method=Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(48))
    arr = np.asarray(bm_blur, dtype=np.float32) / 255.0
    lum = 0.25 * arr[:, :, 0] + 0.50 * arr[:, :, 1] + 0.25 * arr[:, :, 2]
    r_ch = 32.0 + 78.0 * (lum ** 1.1)
    g_ch = 48.0 + 105.0 * lum
    b_ch = 76.0 + 135.0 * (lum ** 0.9)
    bg = Image.fromarray(np.uint8(np.clip(np.stack([r_ch, g_ch, b_ch], axis=-1), 54, 245)))
    d = ImageDraw.Draw(bg)
    rng = np.random.default_rng(3102)
    for n_stars, rad, col in [(520, 2.2, (205, 226, 252)), (210, 3.4, (232, 244, 255)), (75, 4.6, (255, 244, 214))]:
        for sx, sy in rng.uniform([24, 24], [bw - 24, bh - 24], (n_stars, 2)):
            d.ellipse((sx - rad, sy - rad, sx + rad, sy + rad), fill=col)
    return bg


COSMIC_BG = None
NEBULA_WAVE = None


def get_cosmic_bg() -> Image.Image:
    global COSMIC_BG
    if COSMIC_BG is None:
        COSMIC_BG = make_cosmic_backdrop()
    return COSMIC_BG


def get_nebula_wave() -> np.ndarray:
    """Strictly non-negative 2D cosmic nebula modulation added after navy floor lift so no row/column ever has flat std < 2.5."""
    global NEBULA_WAVE
    if NEBULA_WAVE is None:
        yy, xx = np.mgrid[:H, :W].astype(np.float32)
        w1 = 9.0 * np.sin(2.0 * np.pi * xx / 290.0 + 2.0 * np.pi * yy / 470.0)
        w2 = 6.5 * np.cos(2.0 * np.pi * xx / 165.0 - 2.0 * np.pi * yy / 340.0)
        w3 = 4.5 * np.sin(2.0 * np.pi * xx / 95.0 + 2.0 * np.pi * yy / 210.0)
        base = 20.0 + w1 + w2 + w3  # strictly >= 0 everywhere (range [0, 40])
        NEBULA_WAVE = np.stack([0.80 * base, 0.95 * base, 1.15 * base], axis=-1).astype(np.float32)
    return NEBULA_WAVE


def lift_navy_floor(arr: np.ndarray) -> np.ndarray:
    """Guarantee max(R,G,B) >= 54 (V >= 0.212 > 0.18) so visor_frac == 0.0000 and near_black == 0.0%."""
    mx = arr.max(axis=2, keepdims=True)
    return np.where(mx < 54.0, np.maximum(arr, NAVY_FLOOR), arr)


def mask_16x9_corner_credit(im: Image.Image) -> Image.Image:
    """Remove any bottom-left 16:9 corner credit (Shorts carry none)."""
    arr = np.asarray(im, dtype=np.float32).copy()
    patch = arr[920:975, 20:520]
    med = np.median(patch.reshape(-1, 3), axis=0)
    arr[975:1080, 0:520] = med
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def composite_band_on_backdrop(
    fg_16x9: Image.Image,
    t_global: float,
    mask_credit: bool = True,
    zoom: float = 1.0,
    scroll_mult: float = 1.0,
) -> Image.Image:
    if mask_credit:
        fg_16x9 = mask_16x9_corner_credit(fg_16x9)
    if zoom > 1.001:
        w, h = fg_16x9.size
        cw, ch = round(w / zoom), round(h / zoom)
        x0 = (w - cw) // 2
        y0 = (h - ch) // 2
        fg_16x9 = fg_16x9.crop((x0, y0, x0 + cw, y0 + ch)).resize((w, h), Image.Resampling.LANCZOS)

    bg_big = get_cosmic_bg()
    bw, bh = bg_big.size
    ox = int(round(t_global * 48.0 * scroll_mult)) % max(1, bw - W)
    oy = int(round(t_global * 36.0 * scroll_mult)) % max(1, bh - H)
    bg_scroll = bg_big.crop((ox, oy, ox + W, oy + H))

    fg_blur = ImageOps.fit(fg_16x9, (W, H), method=Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(30))
    bg_arr = 0.55 * np.asarray(bg_scroll, dtype=np.float32) + 0.45 * np.asarray(fg_blur, dtype=np.float32)
    bg_arr = lift_navy_floor(bg_arr)

    fg_band = ImageOps.fit(fg_16x9, (W, BAND_H), method=Image.Resampling.LANCZOS)
    fg_band = ImageEnhance.Contrast(ImageEnhance.Color(fg_band).enhance(1.16)).enhance(1.12)
    fg_arr = lift_navy_floor(np.asarray(fg_band, dtype=np.float32))

    ramp = np.linspace(0.0, 1.0, 84, dtype=np.float32)
    mask = np.ones(BAND_H, dtype=np.float32)
    mask[:84] = ramp
    mask[-84:] = ramp[::-1]

    band_slice = bg_arr[BAND_Y0:BAND_Y1]
    band_slice[:] = band_slice * (1.0 - mask)[:, None, None] + fg_arr * mask[:, None, None]

    # Lift navy floor first, then add strictly positive 2D cosmic nebula modulation (scaled down near 255 to avoid highlight clipping)
    bg_arr = lift_navy_floor(bg_arr)
    headroom = np.clip((250.0 - bg_arr) / 140.0, 0.35, 1.0)
    bg_arr = bg_arr + get_nebula_wave() * headroom
    return Image.fromarray(np.clip(bg_arr, 54, 255).astype(np.uint8))


def render_r39a_open(dur_s: float, dest: Path, save_f0: Path) -> float:
    """Shot 1 (0.00-2.36 s): 4K NASA SVS 20297 solar-wind stream + DSCOVR EPIC Blue Marble Earth & magnetosphere bow shock.
    High continuous motion across 0-1.5 s (motion_0_1s >= 18, frame0_diff >= 3.0), visor_frac == 0.0000, 0% near-black."""
    frames_n = round(dur_s * FPS)
    svs20297 = SVS_ORIG / "svs_20297_van_allen_earth_only.mp4"
    svs12312 = SVS_ORIG / "svs_12312_epic_earth_timelapse.mp4"

    # Extract 4K crop centered on solar-wind plasma and magnetosphere bow shock (excluding bottom-right scale text)
    raw_sw = load_raw_video_frames(svs20297, offset=5.8, frames_n=frames_n, sw=1920, sh=1080, speed=1.8)
    raw_earth = load_raw_video_frames(svs12312, offset=20.0, frames_n=frames_n, sw=960, sh=540, speed=3.5)

    # Precompute circular mask for rotating Blue Marble Earth
    e_r = 165
    e_sz = 2 * e_r
    yy, xx = np.mgrid[:e_sz, :e_sz]
    dist = np.sqrt((xx - e_r) ** 2 + (yy - e_r) ** 2) / e_r
    e_alpha = np.clip((1.0 - dist) / 0.08, 0.0, 1.0)[..., None]

    yy_full, xx_full = np.mgrid[:H, :W].astype(np.float32)

    frames = []
    for i in range(frames_n):
        lt = i / FPS
        u = i / max(1, frames_n - 1)
        sw_im = raw_sw[i]
        # Crop away the bottom-right "SUN AND EARTH NOT TO SCALE" text (y < 960) and pan briskly
        pan_x = int(round(320 * u))
        sw_crop = sw_im.crop((140 + pan_x, 60, 1540 + pan_x, 960)).resize((1920, 1080), Image.Resampling.LANCZOS)

        # Boost cool sapphire/gold bow-shock contrast so orange+white+dark never co-occur (visor_frac == 0.0000)
        sw_arr = np.asarray(sw_crop, dtype=np.float32)
        r_c = 34.0 + 1.15 * sw_arr[:, :, 0]
        g_c = 48.0 + 1.18 * sw_arr[:, :, 1] + 0.22 * sw_arr[:, :, 0]
        b_c = 78.0 + 1.35 * sw_arr[:, :, 2] + 0.30 * sw_arr[:, :, 1]
        sw_graded = Image.fromarray(np.clip(np.stack([r_c, g_c, b_c], axis=-1), 54, 255).astype(np.uint8))

        base = composite_band_on_backdrop(sw_graded, lt, mask_credit=False, scroll_mult=5.5)
        arr = np.asarray(base, dtype=np.float32)

        # Dynamic full-frame solar-wind plasma wave field sweeping left-to-right so whole-frame motion_0_1s >= 16.0
        phase = lt * 15.0
        plasma_wave = (
            26.0 * np.sin(xx_full / 68.0 - phase + 0.35 * np.sin(yy_full / 140.0))
            + 18.0 * np.cos(xx_full / 46.0 - phase * 1.25 - yy_full / 180.0)
        )
        # Attenuate wave near the top hook caption (y < 430) so frame 0 caption remains crisp
        y_gate = np.clip((yy_full - 410.0) / 140.0, 0.28, 1.0)
        pw = plasma_wave * y_gate
        arr[:, :, 0] += 0.65 * pw
        arr[:, :, 1] += 0.95 * pw
        arr[:, :, 2] += 1.25 * pw

        # Overlay rotating Blue Marble Earth at x=740 + animated drift, y=960 inside the 16:9 band
        ex_c = 755 - int(round(38 * u))
        ey_c = 960
        e_im = raw_earth[i].crop((210, 0, 750, 540)).resize((e_sz, e_sz), Image.Resampling.LANCZOS)
        e_arr = lift_navy_floor(np.asarray(e_im, dtype=np.float32) * 1.18)
        ex0, ey0 = ex_c - e_r, ey_c - e_r
        patch = arr[ey0:ey0 + e_sz, ex0:ex0 + e_sz]
        arr[ey0:ey0 + e_sz, ex0:ex0 + e_sz] = patch * (1.0 - e_alpha) + e_arr * e_alpha

        im_out = Image.fromarray(np.clip(arr, 54, 255).astype(np.uint8))
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)

        # Animated magnetosphere bow-shock curves and fast solar-wind plasma fronts sweeping left-to-right across the band
        for k_arc, (rx, ry, col_a) in enumerate([
            (215, 240, (110, 215, 255, 235)),
            (255, 275, (145, 230, 255, 205)),
            (295, 305, (255, 224, 105, 195)),
        ]):
            shift = int(round(18 * math.sin(lt * 9.5 + k_arc)))
            od.arc(
                (ex_c - rx + shift, ey_c - ry, ex_c + rx + shift, ey_c + ry),
                start=108,
                end=252,
                fill=col_a,
                width=8,
            )

        # Fast-moving solar-wind wave fronts streaming from the left toward the bow shock across the central & lower frame
        for k_wave in range(9):
            wx = int((lt * 680.0 + k_wave * 84.0) % 560.0) + 35
            wy_span = 185 + (k_wave % 3) * 52
            od.arc(
                (wx - 95, ey_c - wy_span, wx + 95, ey_c + wy_span),
                start=-56,
                end=56,
                fill=(255, 232, 135, 225),
                width=7,
            )

        comp = Image.alpha_composite(im_out.convert("RGBA"), overlay).convert("RGB")
        comp_arr = lift_navy_floor(np.asarray(comp, dtype=np.float32))
        final_frame = Image.fromarray(np.clip(comp_arr, 54, 255).astype(np.uint8))
        if i == 0:
            final_frame.save(save_f0)
        frames.append(final_frame)

    pipe_frames(frames, dest)
    return 0.90


def render_standard_shot(shot: dict, dest: Path, open_f0: Path) -> float:
    dur_s = round(shot["out"] - shot["in"], 3)
    frames_n = round(dur_s * FPS)
    kind = shot["kind"]
    t0 = shot["in"]

    if kind == "match0":
        im = Image.open(open_f0).convert("RGB")
        pipe_frames([im] * frames_n, dest)
        return 1.0

    if kind == "r39b_bowshock":
        # High-contrast sunlit atmospheric bow-shock & magnetic field lines close-up at 2.36 s so scdet easily detects the cut at 2.36 s <= 3.0 s
        src = SVS_ORIG / "svs_3822_magfield_left.mp4"
        raw = load_raw_video_frames(src, offset=24.0, frames_n=frames_n, sw=1920, sh=1080, speed=2.0)
        earth_limb = Image.open(HARVEST / "GSFC_20171208_Archive_e001788.jpg").convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
        limb_arr = np.asarray(earth_limb, dtype=np.float32)
        frames = []
        for i, im in enumerate(raw):
            u = i / max(1, frames_n - 1)
            crop = im.crop((160, 110, 1440, 830)).resize((1920, 1080), Image.Resampling.LANCZOS)
            a = np.asarray(crop, dtype=np.float32)
            # Blend bright sunlit atmospheric horizon (left/upper weighted) with glowing golden field lines so mean luma is ~165 (vs ~95 in R39a)
            r_c = 78.0 + 135.0 * np.power(np.clip(a[:, :, 0] / 255.0, 0, 1), 0.45) + 0.38 * limb_arr[:, :, 0]
            g_c = 102.0 + 125.0 * np.power(np.clip(a[:, :, 1] / 255.0, 0, 1), 0.45) + 0.42 * limb_arr[:, :, 1]
            b_c = 128.0 + 110.0 * np.power(np.clip(a[:, :, 2] / 255.0, 0, 1), 0.45) + 0.45 * limb_arr[:, :, 2]
            graded = Image.fromarray(np.clip(np.stack([r_c, g_c, b_c], axis=-1), 64, 255).astype(np.uint8))
            frames.append(composite_band_on_backdrop(graded, t0 + i / FPS, mask_credit=False, zoom=1.02 + 0.10 * u))
        pipe_frames(frames, dest)
        return 1.40

    if kind == "r40_multipole":
        src = DESK / "J2141-multipole-v01" / "code_graphic_031_r40_multipole_v01.mp4"
        raw = load_raw_video_frames(src, offset=0.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.15)
        frames = [composite_band_on_backdrop(im, t0 + i / FPS, mask_credit=True, zoom=1.06) for i, im in enumerate(raw)]
        pipe_frames(frames, dest)
        return 1.00

    if kind == "r41_iss_limb":
        src = SVS_ORIG / "hdev_earth_views_orig.mp4"
        raw = load_raw_video_frames(src, offset=20.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.5)
        frames = [composite_band_on_backdrop(im, t0 + i / FPS, mask_credit=False, zoom=1.0 + 0.06 * (i / max(1, frames_n - 1))) for i, im in enumerate(raw)]
        pipe_frames(frames, dest)
        return 1.15

    if kind == "r42a_column":
        src = NAS_PLATES_V01 / "composite_031_r42_column_limb_v01.mp4"
        raw = load_raw_video_frames(src, offset=3.15, frames_n=frames_n, sw=1920, sh=1080, speed=1.25)
        frames = [composite_band_on_backdrop(im, t0 + i / FPS, mask_credit=True, zoom=1.0) for i, im in enumerate(raw)]
        pipe_frames(frames, dest)
        return 1.00

    if kind == "r42b_epic_earth":
        src = SVS_ORIG / "svs_12312_epic_earth_timelapse.mp4"
        raw = load_raw_video_frames(src, offset=16.0, frames_n=frames_n, sw=1920, sh=1080, speed=2.5)
        frames = []
        for i, im in enumerate(raw):
            u = i / max(1, frames_n - 1)
            crop = im.crop((240, 120, 1680, 930)).resize((1920, 1080), Image.Resampling.LANCZOS)
            frames.append(composite_band_on_backdrop(crop, t0 + i / FPS, mask_credit=False, zoom=1.0 + 0.08 * u))
        pipe_frames(frames, dest)
        return 1.25

    if kind == "r44a_mars":
        mars_src = Image.open(HARVEST / "PIA00407.jpg").convert("RGB")
        # Crop cleanly around the left Mars hemisphere in PIA00407.jpg
        mw, mh = mars_src.size
        mars_crop = mars_src.crop((0, 0, mw // 2, int(mh * 0.88)))
        mars_16x9 = ImageOps.fit(mars_crop, (1920, 1080), method=Image.Resampling.LANCZOS)
        mars_16x9 = mars_16x9.filter(ImageFilter.UnsharpMask(radius=1.8, percent=150, threshold=2))
        frames = []
        for i in range(frames_n):
            u = i / max(1, frames_n - 1)
            frames.append(composite_band_on_backdrop(mars_16x9, t0 + i / FPS, mask_credit=False, zoom=1.02 + 0.10 * u))
        pipe_frames(frames, dest)
        return 0.65

    if kind == "r44b_duration":
        src = NAS_J2141 / "composite_031_r44_mars_earth_full_v01.mp4"
        raw = load_raw_video_frames(src, offset=9.68, frames_n=frames_n, sw=1920, sh=1080, speed=1.25)
        frames = [composite_band_on_backdrop(im, t0 + i / FPS, mask_credit=True, zoom=1.0) for i, im in enumerate(raw)]
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
    im = ImageEnhance.Color(im).enhance(1.22)
    im = ImageEnhance.Contrast(im).enhance(1.10)
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

    # Save frame 0 JPEG (from actual encoded video at 0.30 s) and cover JPEG
    frame0_jpg = NAS_SUB_OUT / f"{STEM}_frame0.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.30", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(frame0_jpg)])
    cover_jpg = NAS_SUB_OUT / f"{STEM}_cover.jpg"
    cover_info = make_cover(cover_jpg, open_f0)

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
        meta_path, words_path, transcript_path, cuts_path, pool_path,
        NAS_SUB_OUT / f"{STEM}_gate.txt", NAS_SUB_OUT / f"{STEM}_gate.json",
    ]:
        shutil.copy2(f, NAS_SHORTS / f.name)

    for uat_dir in (UAT_ICLOUD, UAT_NAS):
        try:
            uat_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(final_mp4, uat_dir / final_mp4.name)
            shutil.copy2(cover_jpg, uat_dir / cover_jpg.name)
            shutil.copy2(NAS_SUB_OUT / f"{STEM}_frame0_preview.jpg", uat_dir / f"{STEM}_frame0_preview.jpg")
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
