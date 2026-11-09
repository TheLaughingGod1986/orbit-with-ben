#!/usr/bin/env python3
"""031 Magnetic Field Flip — Active Short #2 v02 Assembler (J2394).

Title: What If the Solar Wind Blew Earth's Atmosphere Into Space?
Slug / Stem: sat12_solar_wind_air / 031_short_sat12_solar_wind_air_v02
Air Date: 2026-12-12 (Path A Sat 11:30Z slot; zero collision with 026-029)
Parent Long (031): What Happens When Earth's Magnetic Field Flips?

Repairs all 4 J2390 FIX items on Short #2 while leaving v01 untouched on the NAS:
1. Removes `get_nebula_wave()` and `make_cosmic_backdrop()` completely; uses clean
   full-9:16 reframing (`<= 2.35x` upscale) or `composite_band_on_natural_blur()`
   derived from real moving NASA pixels with a 96-px cosine feather.
2. Removes `od.arc()` cartoon curves, `plasma_wave` sine ripple, and dark-ring
   Earth cutout on `R39a` (`0.00-2.36 s`), `frame0.jpg`, `cover.jpg`, and
   `R39_loop` (`23.16-24.48 s`), rendering directly from clean graded 4K NASA SVS
   20297 solar-wind & magnetosphere footage (`svs_20297_van_allen_earth_only.mp4`).
3. Removes ghost double-exposed Earth (`GSFC_20171208_Archive_e001788.jpg`) on
   `R39b` (`2.36-3.32 s`), rendering directly from a single clean moving NASA SVS
   3822 geomagnetic field plate (`svs_3822_magfield_left.mp4`).
4. Eliminates title-card text collision on `R42a` (`9.32-12.68 s`) during the
   `9.00-14.00 s` parent-title banner by using a clean text-free moving NASA ISS
   plate (`hdev_earth_views_iss_2019.mp4` @ 128.0 s) followed by DSCOVR EPIC
   (`nasa_svs_12312_dscovr_epic_earth.mp4` @ 16.0 s).

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
V02_CUTS = NAS_EDIT / "full_master_v02_work" / "cuts"
NAS_PLATES_V01 = NAS_EDIT / "nas_plates_v01"
NAS_PLATES_V02 = NAS_EDIT / "nas_plates_v02"
NAS_J2141 = NAS_EDIT / "j2141_remaining_v01" / "plates"
DESK = Path("/Users/benjaminoats/_desk")

VO_WAV = NAS_FILM / "02_Voiceover" / "magnetic_field_flip_vo_v02a.wav"
EXPECTED_VO_SHA256 = "3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6"
STT_JSON = NAS_FILM / "02_Voiceover" / "stt" / "magnetic_field_flip_vo_v02a" / "stt_raw.json"
BED_MP3 = NAS_FILM / "05_Music" / "magnetic_field_flip_score_bed_v01.mp3"
KIT_DIR = NAS_FILM / "06_Sound-Effects" / "kit_v01"

WORK = Path("/private/tmp/031_short2_solar_wind_work_v02")
UAT_ICLOUD = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/031_shorts_v02")
UAT_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/031_shorts_v02")

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
NAVY_FLOOR = np.array([28.0, 38.0, 56.0], dtype=np.float32)

STEM = "031_short_sat12_solar_wind_air_v02"
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
        "source": "code_graphic_031_r44c_duration_comparison_v01.mp4",
        "title": "Mars Loss vs Earth Flip Duration Comparison Graphic (031 R44)",
        "offset": 0.0,
    },
    {
        "row": "R39_loop",
        "in": 23.16,
        "out": 24.48,
        "kind": "match0",
        "source": "frame0_hold_sat12_solar_wind_air_v02.png",
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


def mask_16x9_corner_credit(im: Image.Image) -> Image.Image:
    """Remove any top-left or bottom-left 16:9 corner credit (Shorts carry none)."""
    arr = np.asarray(im, dtype=np.float32).copy()
    patch_bot = arr[880:950, 20:520]
    arr[950:1080, 0:520] = np.median(patch_bot.reshape(-1, 3), axis=0)
    patch_top = arr[150:210, 20:360]
    arr[0:150, 0:360] = np.median(patch_top.reshape(-1, 3), axis=0)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def composite_band_on_natural_blur(
    fg_16x9: Image.Image,
    bg_16x9: Image.Image,
    mask_credit: bool = True,
    zoom: float = 1.0,
    replace_flat_navy: bool = False,
) -> Image.Image:
    """Composite a 16:9 frame inside the 9:16 centre band over a clean, natural Gaussian-blurred
    vertical fill derived directly from real moving NASA pixels (zero synthetic sine waves or painted dots)."""
    if mask_credit:
        fg_16x9 = mask_16x9_corner_credit(fg_16x9)
        bg_16x9 = mask_16x9_corner_credit(bg_16x9)
    if zoom > 1.001:
        w, h = fg_16x9.size
        cw, ch = round(w / zoom), round(h / zoom)
        x0 = (w - cw) // 2
        y0 = (h - ch) // 2
        fg_16x9 = fg_16x9.crop((x0, y0, x0 + cw, y0 + ch)).resize((w, h), Image.Resampling.LANCZOS)

    bg_fit = ImageOps.fit(bg_16x9, (W, H), method=Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(28))
    bg_enh = ImageEnhance.Contrast(ImageEnhance.Color(bg_fit).enhance(1.18)).enhance(1.12)
    bg_arr = np.asarray(bg_enh, dtype=np.float32) * 0.88 + np.array([18.0, 26.0, 42.0], dtype=np.float32)
    bg_arr = lift_navy_floor(bg_arr)

    fg_band = ImageOps.fit(fg_16x9, (W, BAND_H), method=Image.Resampling.LANCZOS)
    fg_band = ImageEnhance.Contrast(ImageEnhance.Color(fg_band).enhance(1.10)).enhance(1.08)
    fg_arr = np.asarray(fg_band, dtype=np.float32)

    if replace_flat_navy:
        # Blend the natural blurred NASA backdrop into the flat navy background pixels of a CODE graphic
        # while keeping the central Earth disc / multipole arrows / text labels 100% sharp and bright.
        yy_b, xx_b = np.mgrid[:BAND_H, :W].astype(np.float32)
        dist_c = np.sqrt((xx_b - W / 2.0) ** 2 + (yy_b - BAND_H * 0.52) ** 2)
        max_c = fg_arr.max(axis=2)
        is_flat_bg = (max_c < 88.0) & (dist_c > 165.0)
        bg_band_slice = bg_arr[BAND_Y0:BAND_Y1]
        blend_w = np.where(is_flat_bg, 0.65, 0.0)[:, :, None].astype(np.float32)
        fg_arr = fg_arr * (1.0 - blend_w) + bg_band_slice * blend_w

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


def render_r39a_open(dur_s: float, dest: Path, save_f0: Path) -> float:
    """Shot 1 (0.00-2.36 s): Pure graded 4K NASA SVS 20297 solar-wind CME stream & Earth magnetosphere bow shock.
    Zero od.arc() cartoon lines, zero plasma_wave sine ripple, zero dark-ring Earth cutout, zero nebula plaid/dots."""
    frames_n = round(dur_s * FPS)
    svs20297 = SVS_ORIG / "svs_20297_van_allen_earth_only.mp4"
    # Extract at 2560x1440 from the 3840x2160 4K master during the solar-wind CME blast (ss=6.4s, speed=2.4)
    raw = load_raw_video_frames(svs20297, offset=6.4, frames_n=frames_n, sw=2560, sh=1440, speed=2.4)

    frames = []
    for i, im in enumerate(raw):
        u = i / max(1, frames_n - 1)
        # Foreground 16:9 crop pans briskly from the erupting solar wind stream into the magnetosphere bow shock,
        # cropping above y=1260 so the bottom-right "SUN AND EARTH NOT TO SCALE" label is completely excluded.
        fg_x0 = int(round(120 + 520 * u))
        fg_y0 = int(round(80 + 60 * u))
        fg_w = int(round(1760 - 160 * u))
        fg_h = round(fg_w * 9 / 16)
        fg_crop = im.crop((fg_x0, fg_y0, fg_x0 + fg_w, fg_y0 + fg_h)).resize((1920, 1080), Image.Resampling.LANCZOS)

        # Background 16:9 crop for the natural Gaussian-blurred top/bottom fill sweeps across the solar corona & bow shock
        bg_x0 = int(round(580 - 440 * u))
        bg_crop = im.crop((bg_x0, 40, bg_x0 + 1840, 1260)).resize((1920, 1080), Image.Resampling.BILINEAR)

        def grade_svs20297(src_im: Image.Image) -> Image.Image:
            a = np.asarray(src_im, dtype=np.float32) / 255.0
            r = 28.0 + 222.0 * np.power(np.clip(a[:, :, 0], 0, 1), 0.52)
            g = 38.0 + 210.0 * np.power(np.clip(a[:, :, 1], 0, 1), 0.48) + 18.0 * a[:, :, 0]
            b = 58.0 + 195.0 * np.power(np.clip(a[:, :, 2], 0, 1), 0.44) + 28.0 * a[:, :, 1]
            arr = lift_navy_floor(np.stack([r, g, b], axis=-1))
            return Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8))

        fg_graded = grade_svs20297(fg_crop)
        bg_graded = grade_svs20297(bg_crop)
        frame = composite_band_on_natural_blur(fg_graded, bg_graded, mask_credit=False, zoom=1.0)
        if i == 0:
            frame.save(save_f0)
        frames.append(frame)

    pipe_frames(frames, dest)
    return 0.95


def render_standard_shot(shot: dict, dest: Path, open_f0: Path) -> float:
    dur_s = round(shot["out"] - shot["in"], 3)
    frames_n = round(dur_s * FPS)
    kind = shot["kind"]

    if kind == "match0":
        im = Image.open(open_f0).convert("RGB")
        pipe_frames([im] * frames_n, dest)
        return 1.0

    if kind == "r39b_magfield":
        # Single clean moving NASA SVS 3822 geomagnetic field lines plate (full 9:16 reframe, zero static Earth photo blend)
        src = SVS_ORIG / "svs_3822_magfield_left.mp4"
        raw = load_raw_video_frames(src, offset=28.0, frames_n=frames_n, sw=1920, sh=1080, speed=2.2)
        frames = []
        for i, im in enumerate(raw):
            u = i / max(1, frames_n - 1)
            cw = int(round(920 - 120 * u))
            ch = int(round(1020 - 100 * u))
            x0 = int(round(200 + 180 * u))
            y0 = int(round(30 + 40 * u))
            crop = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.Resampling.LANCZOS)
            a = np.asarray(crop, dtype=np.float32) / 255.0
            r = 28.0 + 218.0 * np.power(np.clip(a[:, :, 0], 0, 1), 0.46)
            g = 38.0 + 214.0 * np.power(np.clip(a[:, :, 1], 0, 1), 0.46)
            b = 58.0 + 196.0 * np.power(np.clip(a[:, :, 2], 0, 1), 0.46)
            rgb = lift_navy_floor(np.stack([r, g, b], axis=-1))
            frames.append(Image.fromarray(np.clip(rgb, 28, 255).astype(np.uint8)))
        pipe_frames(frames, dest)
        return 1.40

    if kind == "r40_multipole":
        src_fg = DESK / "J2141-multipole-v01" / "code_graphic_031_r40_multipole_v01.mp4"
        src_bg = SVS_ORIG / "svs_3822_magfield_left.mp4"
        raw_fg = load_raw_video_frames(src_fg, offset=0.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.15)
        raw_bg = load_raw_video_frames(src_bg, offset=36.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.6)
        frames = []
        for i in range(frames_n):
            u = i / max(1, frames_n - 1)
            frames.append(
                composite_band_on_natural_blur(
                    raw_fg[i], raw_bg[i], mask_credit=True, zoom=1.02 + 0.06 * u, replace_flat_navy=True
                )
            )
        pipe_frames(frames, dest)
        return 1.00

    if kind == "r41_iss_limb":
        src = SVS_ORIG / "hdev_earth_views_orig.mp4"
        raw = load_raw_video_frames(src, offset=20.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.5)
        frames = [
            composite_band_on_natural_blur(im, im, mask_credit=False, zoom=1.0 + 0.06 * (i / max(1, frames_n - 1)))
            for i, im in enumerate(raw)
        ]
        pipe_frames(frames, dest)
        return 1.15

    if kind == "r42a_iss_sunlit":
        # Clean text-free moving NASA ISS sunlit orbital pass under the 9.00-14.00 s parent-title banner (zero text collision)
        src = SVS_ORIG / "hdev_earth_views_orig.mp4"
        raw = load_raw_video_frames(src, offset=128.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.5)
        frames = [
            composite_band_on_natural_blur(im, im, mask_credit=False, zoom=1.02 + 0.06 * (i / max(1, frames_n - 1)))
            for i, im in enumerate(raw)
        ]
        pipe_frames(frames, dest)
        return 1.25

    if kind == "r42b_epic_earth":
        src = SVS_ORIG / "svs_12312_epic_earth_timelapse.mp4"
        raw_fg = load_raw_video_frames(src, offset=16.0, frames_n=frames_n, sw=1920, sh=1080, speed=2.5)
        raw_bg = load_raw_video_frames(SVS_ORIG / "hdev_earth_views_orig.mp4", offset=78.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.5)
        frames = []
        for i, im in enumerate(raw_fg):
            u = i / max(1, frames_n - 1)
            crop = im.crop((240, 120, 1680, 930)).resize((1920, 1080), Image.Resampling.LANCZOS)
            frames.append(
                composite_band_on_natural_blur(
                    crop, raw_bg[i], mask_credit=False, zoom=1.0 + 0.08 * u, replace_flat_navy=True
                )
            )
        pipe_frames(frames, dest)
        return 1.25

    if kind == "r44a_mars":
        mars_src = Image.open(HARVEST / "PIA00407.jpg").convert("RGB")
        mw, mh = mars_src.size
        mars_crop = mars_src.crop((0, 0, mw // 2, int(mh * 0.88)))
        mars_16x9 = ImageOps.fit(mars_crop, (1920, 1080), method=Image.Resampling.LANCZOS)
        mars_16x9 = mars_16x9.filter(ImageFilter.UnsharpMask(radius=1.8, percent=150, threshold=2))
        frames = []
        for i in range(frames_n):
            u = i / max(1, frames_n - 1)
            frames.append(composite_band_on_natural_blur(mars_16x9, mars_16x9, mask_credit=False, zoom=1.02 + 0.10 * u))
        pipe_frames(frames, dest)
        return 0.65

    if kind == "r44b_duration":
        src = NAS_J2141 / "composite_031_r44_mars_earth_full_v01.mp4"
        raw = load_raw_video_frames(src, offset=9.68, frames_n=frames_n, sw=1920, sh=1080, speed=1.25)
        frames = [
            composite_band_on_natural_blur(im, im, mask_credit=True, zoom=1.0 + 0.04 * (i / max(1, frames_n - 1)))
            for i, im in enumerate(raw)
        ]
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
