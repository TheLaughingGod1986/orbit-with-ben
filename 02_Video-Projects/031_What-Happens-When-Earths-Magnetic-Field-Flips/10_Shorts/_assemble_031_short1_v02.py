#!/usr/bin/env python3
"""031 Magnetic Field Flip — Active Short #1 v02 Full-Frame Assembler (J2551).

Title: What Happens When Earth's Magnetic Field Flips?
Slug / Stem: testA_opening_flip / 031_short_testA_opening_flip_v02
Scheduled Video ID: C8lPx5N2DwM (airs Sat 2026-12-05 11:30Z; watch card due 2026-12-02 18:00 London)

Fixes every padded 16:9-over-blur stretch flagged in J2545 / J2551:
  - 4.72–8.40 s (R01b): Upright 1080x1920 North Magnetic Pole drift graphic rebuilt from opening_graphics.py
  - 8.40–11.40 s (R02a): Full-bleed 9:16 ISS aurora over cloud deck (plate_031_r02a_iss_aurora_v01.mp4, 1.78x)
  - 14.12–16.16 s (R02b): Upright 1080x1920 Poles Swap + Atmosphere Holds graphic rebuilt from opening_graphics.py
  - 16.16–18.44 s (R03a): Full-bleed 9:16 rotating sunlit Earth globe (plate_031_r12a_earth_limb_v01.mp4, 1.78x)
  - 18.44–20.68 s (R03b): Full-bleed 9:16 sunlit Earth blue atmospheric limb (plate_031_r21_earth_limb_v01.mp4, 1.78x)
  - 20.68–23.64 s (R04a): Full-bleed 9:16 ISS solar array over Earth (plate_031_r04a_iss_exterior_v01.mp4, 1.78x)
  - 23.64–24.96 s (R04a2): Full-bleed 9:16 Earth radiation-belt field lines (plate_031_r25_iss_orbit_cuts_v01.mp4, 1.78x)
  - 24.96–28.00 s (R04b): Upright 1080x1920 Earth's Compass Turning Upside Down graphic rebuilt from mechanism_graphics.py
  - 28.00–31.68 s (R04c): Full-bleed 9:16 4K ISS green & crimson aurora curtains (Gerst_Earth_timelapses_2017.webm, 1.00x)

Preserves R01a (0.00–2.32 s), R01a2 (2.32–4.72 s), R02a2 (11.40–14.12 s), and R01_loop (31.68–33.00 s)
plus exact voice, words, length (33.00 s), captions, banners, SFX, bed, and loudness (-14.0 LUFS).
Never touches v01, UPLOADS.json, Buffer, or YouTube Studio. £0 spend.
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
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

Image.MAX_IMAGE_PIXELS = None

HERE = Path(__file__).resolve().parent
REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "031_What-Happens-When-Earths-Magnetic-Field-Flips"
)
NAS_EDIT = NAS_FILM / "07_Edit-Project"
NAS_SHORTS = NAS_FILM / "10_Shorts"
NAS_SUB_OUT = NAS_SHORTS / "testA_opening_flip" / "06_Final-Exports"

V01_MP4 = NAS_SUB_OUT / "031_short_testA_opening_flip_v01.mp4"
EXPECTED_V01_SHA256 = "ebe11bb730ccfab8681d564d3588d17011a28629c7b6f926eba952bfc98c4bcd"

SVS_ORIG = NAS_EDIT / "svs_moving_v01" / "originals"
NAS_PLATES_V01 = NAS_EDIT / "nas_plates_v01"
HARVEST_V01 = NAS_EDIT / "harvest_v01"
GERST_4K = Path(
    "/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/"
    "02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/"
    "pool_v01/iss/Gerst_Earth_timelapses_2017.webm"
)

VO_WAV = NAS_FILM / "02_Voiceover" / "magnetic_field_flip_vo_v02a.wav"
EXPECTED_VO_SHA256 = "3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6"
STT_JSON = NAS_FILM / "02_Voiceover" / "stt" / "magnetic_field_flip_vo_v02a" / "stt_raw.json"
BED_MP3 = NAS_FILM / "05_Music" / "magnetic_field_flip_score_bed_v01.mp3"
KIT_DIR = NAS_FILM / "06_Sound-Effects" / "kit_v01"

WORK = Path("/Volumes/MiniWork/scratch/J2551/031_short1_work_v02")
REVIEW_SCRATCH = Path("/Volumes/MiniWork/scratch/J2551/031_opening_v02_review")
UAT_ICLOUD = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/J2551_031_opening_v02")
UAT_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/J2551_031_opening_v02")

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import gate_shorts_open as gso  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 25
SR = 48000
BAND_H = round(W * 9 / 16)          # 608 px (safe text band for title/end card/captions)
BAND_Y0 = (H - BAND_H) // 2         # 656 px
BAND_Y1 = BAND_Y0 + BAND_H          # 1264 px
LINE_H = round(BAND_H * 0.115)      # 70 px

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)         # #FFE000
GOLD = (242, 182, 61, 255)
BLUE = (96, 168, 255, 255)
NAVY_BG = (28, 38, 58)
GRID_COL = (40, 58, 86)
NAVY_FLOOR = np.array([28.0, 38.0, 58.0], dtype=np.float32)

STEM = "031_short_testA_opening_flip_v02"
SHORT_SLUG = "testA_opening_flip"
SHORT_TITLE = "What Happens When Earth's Magnetic Field Flips?"
AIR_DATE = "2026-12-05"
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
HOOK_ROWS = [("POLES ARE", WHITE), ("FLIPPING", YELLOW)]
COVER_ROWS = [("POLES SWAP", WHITE), ("PLACES?", YELLOW)]

HOOK_END = 2.20
TITLE_IN, TITLE_OUT = 9.00, 14.00
TEACH_IN, TEACH_OUT = 18.52, 20.56
TEACH_TEXT = "HUNDREDS OF FLIPS"

VO_SEGMENTS = [
    (0.14, 8.34),
    (9.06, 11.84),
    (12.54, 17.08),
    (18.12, 18.36),
    (19.02, 20.08),
    (20.70, 23.28),
    (23.80, 27.86),
    (28.50, 31.32),
    (31.90, 35.32),
]
VO_LEAD_S = 0.08
VO_GAPS = [0.22] * 8
TOTAL_S = 33.00
END_CARD_IN = 31.68

SHOT_PLAN = [
    {
        "row": "R01a",
        "in": 0.00,
        "out": 2.32,
        "kind": "r01a_open",
        "source": "nasa_svs_3822_magfield_left.mp4",
        "title": "Geomagnetic Field Lines in Space (NASA SVS 3822)",
        "offset": 20.2,
    },
    {
        "row": "R01a2",
        "in": 2.32,
        "out": 4.72,
        "kind": "r01a2_bowshock",
        "source": "nasa_svs_20297_magnetosphere_earth_only.mp4",
        "title": "Earth Magnetosphere and Solar Wind Stream (NASA SVS 20297)",
        "offset": 2.0,
    },
    {
        "row": "R01b",
        "in": 4.72,
        "out": 8.40,
        "kind": "r01b_poledrift_916",
        "source": "code_graphic_031_r01b_poledrift_v02.mp4",
        "title": "North Magnetic Pole Drift 1831 to Today Graphic (031 R01 Upright 9:16)",
        "offset": 0.0,
    },
    {
        "row": "R02a",
        "in": 8.40,
        "out": 11.40,
        "kind": "r02a_aurora_916",
        "source": "plate_031_r02a_iss_aurora_v01.mp4",
        "title": "Aurora Borealis over Earth Cloud Deck from the ISS (NASA)",
        "offset": 0.2,
    },
    {
        "row": "R02a2",
        "in": 11.40,
        "out": 14.12,
        "kind": "r02a2_magfield",
        "source": "nasa_svs_3822_magfield_left.mp4",
        "title": "Geomagnetic Field Lines in Space (NASA SVS 3822)",
        "offset": 46.0,
    },
    {
        "row": "R02b",
        "in": 14.12,
        "out": 16.16,
        "kind": "r02b_flip_916",
        "source": "code_graphic_031_r02b_flip_v02.mp4",
        "title": "Magnetic Poles Swap with Intact Atmosphere Graphic (031 R02 Upright 9:16)",
        "offset": 0.0,
    },
    {
        "row": "R03a",
        "in": 16.16,
        "out": 18.44,
        "kind": "r03a_earth_globe_916",
        "source": "plate_031_r12a_earth_limb_v01.mp4",
        "title": "Sunlit Earth Atmosphere and Clouds from Space (NASA)",
        "offset": 0.4,
    },
    {
        "row": "R03b",
        "in": 18.44,
        "out": 20.68,
        "kind": "r03b_earth_limb_916",
        "source": "plate_031_r21_earth_limb_v01.mp4",
        "title": "Earth Blue Atmospheric Limb from Low Orbit (NASA)",
        "offset": 0.6,
    },
    {
        "row": "R04a",
        "in": 20.68,
        "out": 23.64,
        "kind": "r04a_iss_ext_916",
        "source": "plate_031_r04a_iss_exterior_v01.mp4",
        "title": "International Space Station Orbiting over Sunlit Earth (NASA)",
        "offset": 0.4,
    },
    {
        "row": "R04a2",
        "in": 23.64,
        "out": 24.96,
        "kind": "r04a2_belts_saa_916",
        "source": "plate_031_r25_iss_orbit_cuts_v01.mp4",
        "title": "Earth Radiation Belts and Magnetosphere Field Lines (NASA SVS)",
        "offset": 11.2,
    },
    {
        "row": "R04b",
        "in": 24.96,
        "out": 28.00,
        "kind": "r04b_compass_916",
        "source": "code_graphic_031_r04b_compass_v03.mp4",
        "title": "Compass Needle Turning Upside Down Graphic (031 R04 Upright 9:16)",
        "offset": 0.0,
    },
    {
        "row": "R04c",
        "in": 28.00,
        "out": 31.68,
        "kind": "r04c_gerst_aurora_916",
        "source": "Gerst_Earth_timelapses_2017.webm",
        "title": "4K Aurora Borealis Curtains from the ISS (ESA/NASA Alexander Gerst)",
        "offset": 11.4,
    },
    {
        "row": "R01_loop",
        "in": 31.68,
        "out": 33.00,
        "kind": "match0",
        "source": "frame0_hold_testA_opening_flip.png",
        "title": "Opening frame held for seamless loop",
        "offset": 0.0,
    },
]


def ease(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * (3.0 - 2.0 * u)


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
    """Guarantee max(R,G,B) >= 54 so near_black == 0.0% and visor_frac == 0.0."""
    mx = arr.max(axis=2, keepdims=True)
    return np.where(mx < 54.0, np.maximum(arr, NAVY_FLOOR * 1.45), arr)


def draw_vertical_house_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Full-height 1080x1920 Orbit dark-navy technical canvas with 80 px grid and subtle radial glow."""
    yy, xx = np.mgrid[:H, :W].astype(np.float32)
    dist = np.sqrt(((xx - 540.0) / 540.0) ** 2 + ((yy - 760.0) / 760.0) ** 2)
    glow = np.clip(1.0 - 0.55 * dist, 0.45, 1.0)
    base = np.zeros((H, W, 3), dtype=np.float32)
    base[:, :, 0] = 28.0 + 18.0 * glow
    base[:, :, 1] = 40.0 + 26.0 * glow
    base[:, :, 2] = 62.0 + 42.0 * glow
    im = Image.fromarray(base.astype(np.uint8)).convert("RGBA")
    dr = ImageDraw.Draw(im)
    for x in range(0, W + 1, 80):
        dr.line((x, 0, x, H), fill=(46, 68, 98, 255), width=2)
    for y in range(0, H + 1, 80):
        dr.line((0, y, W, y), fill=(46, 68, 98, 255), width=2)
    return im, dr


def draw_label_center(dr: ImageDraw.ImageDraw, cx: int, cy: int, text: str, size: int, fill: tuple, alpha: float = 1.0) -> None:
    if alpha <= 0.02:
        return
    a = int(round(255 * max(0.0, min(1.0, alpha))))
    col = (fill[0], fill[1], fill[2], a)
    f = ImageFont.truetype(FONT_BOLD, size)
    b = dr.textbbox((0, 0), text, font=f, stroke_width=5)
    tw, th = b[2] - b[0], b[3] - b[1]
    dr.text((cx - tw // 2 - b[0], cy - th // 2 - b[1]), text, font=f, fill=col, stroke_width=5, stroke_fill=(14, 22, 38, a))


def render_r01a_open(dur_s: float, dest: Path, save_f0: Path) -> float:
    frames_n = round(dur_s * FPS)
    svs3822 = SVS_ORIG / "svs_3822_magfield_left.mp4"
    raw = load_raw_video_frames(svs3822, offset=21.2, frames_n=frames_n, sw=1920, sh=1080, speed=2.5)

    frames = []
    for i, im in enumerate(raw):
        im = ImageOps.mirror(im)
        u = i / max(1, frames_n - 1)
        cw = int(round(920 - 160 * u))
        ch = int(round(1040 - 140 * u))
        x0 = int(round(860 - 420 * u))
        y0 = int(round(20 + 60 * u))
        crop = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.Resampling.LANCZOS)
        a = np.asarray(crop, dtype=np.float32) / 255.0
        r = 28.0 + 220.0 * np.power(np.clip(a[:, :, 0], 0, 1), 0.45)
        g = 36.0 + 215.0 * np.power(np.clip(a[:, :, 1], 0, 1), 0.45)
        b = 56.0 + 198.0 * np.power(np.clip(a[:, :, 2], 0, 1), 0.45)
        rgb = np.clip(np.stack([r, g, b], axis=-1), 28, 255).astype(np.uint8)
        frame = Image.fromarray(rgb)
        if i == 0:
            frame.save(save_f0)
        frames.append(frame)

    pipe_frames(frames, dest)
    return 1.40


def render_r01b_poledrift_916(dur_s: float, dest: Path) -> float:
    """Upright 1080x1920 rebuild of opening_graphics.py 'poledrift' (4.72-8.40 s).
    All diagram elements stay within y=180..1180 so spoken captions at y=1300..1370 are 100% unobstructed."""
    frames_n = round(dur_s * FPS)
    cx, cy, r = 540, 720, 340
    p0 = (315.0, 825.0)    # 1831 Boothia Peninsula (Canada)
    p_mid = (520.0, 610.0) # Central Arctic Ocean
    p1 = (760.0, 565.0)    # Toward Siberia

    def bezier(u: float) -> tuple[float, float]:
        x = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p_mid[0] + u ** 2 * p1[0]
        y = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p_mid[1] + u ** 2 * p1[1]
        return x, y

    frames = []
    for i in range(frames_n):
        t = i / FPS
        im, dr = draw_vertical_house_canvas()

        # Polar azimuthal projection rings & meridians
        dr.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(22, 36, 58, 255), outline=(140, 185, 240, 255), width=6)
        for rr in (115, 228):
            dr.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(64, 96, 138, 255), width=3)
        for ang_deg in range(0, 180, 30):
            ang = math.radians(ang_deg)
            dx, dy = int(round(r * math.cos(ang))), int(round(r * math.sin(ang)))
            dr.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=(54, 82, 120, 255), width=2)

        # Geographicpole cross & labels
        dr.line((cx - 16, cy, cx + 16, cy), fill=(180, 210, 245, 255), width=4)
        dr.line((cx, cy - 16, cx, cy + 16), fill=(180, 210, 245, 255), width=4)
        draw_label_center(dr, cx, cy + 54, "ARCTIC", 38, (180, 215, 255, 255), 1.0)
        draw_label_center(dr, int(p0[0]), int(p0[1]) + 62, "1831", 40, WHITE, 1.0)
        draw_label_center(dr, int(p0[0]), int(p0[1]) + 112, "CANADA", 36, BLUE, 1.0)
        draw_label_center(dr, int(p1[0]), int(p1[1]) - 64, "SIBERIA", 44, GOLD, ease((t - 0.35) / 0.45))

        # Start marker (1831)
        dr.ellipse((p0[0] - 13, p0[1] - 13, p0[0] + 13, p0[1] + 13), fill=WHITE)

        # Animated gold drift track
        prog = ease(t / max(0.4, dur_s - 0.55))
        steps = max(2, int(round(70 * prog)))
        pts = [bezier(prog * k / steps) for k in range(steps + 1)]
        if len(pts) >= 2:
            dr.line(pts, fill=GOLD, width=11)
        hx, hy = pts[-1]
        # Glowing leading magnetic pole marker
        pulse = 22 + int(round(4 * math.sin(t * 6.0)))
        dr.ellipse((hx - pulse, hy - pulse, hx + pulse, hy + pulse), fill=(242, 182, 61, 95))
        dr.ellipse((hx - 14, hy - 14, hx + 14, hy + 14), fill=GOLD, outline=WHITE, width=3)

        # Upright header & bottom callout (well above y=1300 captions)
        draw_label_center(dr, 540, 235, "NORTH MAGNETIC POLE", 50, WHITE, ease(t / 0.25))
        draw_label_center(dr, 540, 308, "55 KM / YEAR DRIFT", 44, BLUE, ease((t - 0.25) / 0.35))
        draw_label_center(dr, 540, 1145, "RACING TO SIBERIA", 54, GOLD, ease((t - 0.70) / 0.40))

        frames.append(im.convert("RGB"))

    pipe_frames(frames, dest)
    return 1.00


def render_r02b_flip_916(dur_s: float, dest: Path) -> float:
    """Upright 1080x1920 rebuild of opening_graphics.py 'flip' (14.12-16.16 s).
    Uses NASA DSCOVR Earth GSFC_20171208_Archive_e000678.jpg + dipolar field loops + rotating N/S bar magnet."""
    frames_n = round(dur_s * FPS)
    earth_src = Image.open(HARVEST_V01 / "GSFC_20171208_Archive_e000678.jpg").convert("RGB")
    # Crop Earth disc cleanly
    ew, eh = earth_src.size
    er = int(min(ew, eh) * 0.42)
    earth_crop = earth_src.crop((ew // 2 - er, eh // 2 - er, ew // 2 + er, eh // 2 + er)).resize((400, 400), Image.Resampling.LANCZOS)
    yy_m, xx_m = np.mgrid[:400, :400].astype(np.float32)
    mask_disc = np.clip((196.0 - np.sqrt((xx_m - 200.0) ** 2 + (yy_m - 200.0) ** 2)) / 3.0, 0.0, 1.0)
    mask_im = Image.fromarray((mask_disc * 255).astype(np.uint8))

    cx, cy = 540, 740
    frames = []
    for i in range(frames_n):
        t = i / FPS
        im, dr = draw_vertical_house_canvas()

        # Dipolar magnetic field loops around Earth (upright vertical layout)
        flip_p = ease((t - 0.15) / 1.15)
        loop_col = (
            int(round(96 + (242 - 96) * flip_p)),
            int(round(168 + (182 - 168) * flip_p)),
            int(round(255 + (61 - 255) * flip_p)),
            220,
        )
        for rx, ry in ((430, 320), (335, 255)):
            dr.arc((cx - rx, cy - ry, cx + rx, cy + ry), start=130, end=230, fill=loop_col, width=7)
            dr.arc((cx - rx, cy - ry, cx + rx, cy + ry), start=-50, end=50, fill=loop_col, width=7)
            dr.arc((cx - rx // 2 - 190, cy - ry, cx + rx // 2 - 190, cy + ry), start=95, end=265, fill=loop_col, width=6)
            dr.arc((cx - rx // 2 + 190, cy - ry, cx + rx // 2 + 190, cy + ry), start=-85, end=85, fill=loop_col, width=6)

        # Intact blue atmospheric halo
        for hr, alpha in ((228, 70), (214, 130), (204, 220)):
            dr.ellipse((cx - hr, cy - hr, cx + hr, cy + hr), outline=(96, 178, 255, alpha), width=6)

        # Real NASA DSCOVR Earth globe
        rot_deg = t * 4.5
        e_rot = earth_crop.rotate(rot_deg, resample=Image.Resampling.BICUBIC)
        im.paste(e_rot, (cx - 200, cy - 200), mask_im)

        # Rotating N/S bar magnet across centre (swapping places 180 deg)
        ang = math.pi * flip_p
        ux, uy = math.sin(ang), -math.cos(ang)  # at ang=0 points UP; at ang=pi points DOWN
        px, py = -uy, ux
        half_len, half_w = 135.0, 34.0

        def quad(s0: float, s1: float) -> list[tuple[float, float]]:
            return [
                (cx + ux * s0 - px * half_w, cy + uy * s0 - py * half_w),
                (cx + ux * s0 + px * half_w, cy + uy * s0 + py * half_w),
                (cx + ux * s1 + px * half_w, cy + uy * s1 + py * half_w),
                (cx + ux * s1 - px * half_w, cy + uy * s1 - py * half_w),
            ]

        dr.polygon(quad(0.0, half_len), fill=GOLD, outline=WHITE)
        dr.polygon(quad(-half_len, 0.0), fill=(52, 118, 212, 255), outline=WHITE)
        draw_label_center(dr, int(round(cx + ux * 82)), int(round(cy + uy * 82)), "N", 42, WHITE, 1.0)
        draw_label_center(dr, int(round(cx - ux * 82)), int(round(cy - uy * 82)), "S", 42, WHITE, 1.0)

        # Crisp upright labels clear of captions (y=1300)
        draw_label_center(dr, 540, 245, "POLES SWAP PLACES", 56, GOLD, ease(t / 0.25))
        draw_label_center(dr, 540, 1135, "ATMOSPHERE HOLDS", 48, BLUE, ease((t - 0.35) / 0.35))

        frames.append(im.convert("RGB"))

    pipe_frames(frames, dest)
    return 1.00


def render_r04b_compass_916(dur_s: float, dest: Path) -> float:
    """Upright 1080x1920 rebuild of mechanism_graphics.py 'compass' + _build_v02_fixes.py 'UPSIDE DOWN' (24.96-28.00 s)."""
    frames_n = round(dur_s * FPS)
    cx, cy, r = 540, 720, 310
    frames = []
    for i in range(frames_n):
        t = i / FPS
        im, dr = draw_vertical_house_canvas()

        # Compass bezel and degree ticks
        dr.ellipse((cx - r - 18, cy - r - 18, cx + r + 18, cy + r + 18), fill=(20, 32, 52, 255), outline=(120, 165, 225, 255), width=5)
        dr.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(26, 40, 64, 255), outline=WHITE, width=8)
        for deg in range(0, 360, 15):
            rad = math.radians(deg)
            inner = r - (34 if deg % 90 == 0 else (24 if deg % 30 == 0 else 14))
            w_tick = 6 if deg % 90 == 0 else 3
            col_tick = WHITE if deg % 30 == 0 else (96, 130, 175, 255)
            dr.line(
                (
                    cx + inner * math.sin(rad),
                    cy - inner * math.cos(rad),
                    cx + (r - 4) * math.sin(rad),
                    cy - (r - 4) * math.cos(rad),
                ),
                fill=col_tick,
                width=w_tick,
            )

        # Cardinal letters outside bezel
        draw_label_center(dr, cx, cy - r - 64, "N", 56, GOLD, 1.0)
        draw_label_center(dr, cx, cy + r + 64, "S", 52, BLUE, 1.0)
        draw_label_center(dr, cx - r - 62, cy, "W", 44, (190, 215, 245, 255), 1.0)
        draw_label_center(dr, cx + r + 62, cy, "E", 44, (190, 215, 245, 255), 1.0)

        # Needle angle: slight tremor upright, then 180 deg swing with damped settle
        if t < 0.45:
            ang = 0.06 * math.sin(t * 14.0)
        else:
            p = ease((t - 0.45) / 1.45)
            settle = math.exp(-3.2 * max(0.0, t - 1.55)) * 0.14 * math.sin(11.0 * max(0.0, t - 1.55)) if t > 1.55 else 0.0
            ang = math.pi * p + settle

        ux, uy = math.sin(ang), -math.cos(ang)
        px, py = -uy, ux
        tip_len, half_w = 248.0, 28.0
        # Gold North pointer
        dr.polygon(
            [
                (cx + ux * tip_len, cy + uy * tip_len),
                (cx + px * half_w, cy + py * half_w),
                (cx - px * half_w, cy - py * half_w),
            ],
            fill=GOLD,
            outline=WHITE,
        )
        # Blue South pointer
        dr.polygon(
            [
                (cx - ux * tip_len, cy - uy * tip_len),
                (cx + px * half_w, cy + py * half_w),
                (cx - px * half_w, cy - py * half_w),
            ],
            fill=(68, 138, 232, 255),
            outline=WHITE,
        )
        dr.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=WHITE, outline=(28, 40, 62, 255), width=4)

        draw_label_center(dr, 540, 215, "EARTH'S COMPASS", 52, WHITE, ease(t / 0.25))
        draw_label_center(dr, 540, 1175, "UPSIDE DOWN", 60, GOLD, ease((t - 1.05) / 0.35))

        frames.append(im.convert("RGB"))

    pipe_frames(frames, dest)
    return 1.00


def render_fullbleed_plate(
    src: Path,
    offset: float,
    dur_s: float,
    dest: Path,
    sw: int,
    sh: int,
    cw: int,
    ch: int,
    x0_start: int,
    x0_end: int,
    y0_start: int,
    y0_end: int,
    speed: float = 1.0,
    gamma: float = 0.88,
) -> float:
    """Full-bleed 9:16 crop from real high-resolution NASA/ESA footage (zero blur bands, zero flat bars)."""
    frames_n = round(dur_s * FPS)
    raw = load_raw_video_frames(src, offset=offset, frames_n=frames_n, sw=sw, sh=sh, speed=speed)
    frames = []
    for i, im in enumerate(raw):
        u = i / max(1, frames_n - 1)
        x0 = int(round(x0_start + (x0_end - x0_start) * u))
        y0 = int(round(y0_start + (y0_end - y0_start) * u))
        crop = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.Resampling.LANCZOS)
        crop = ImageEnhance.Contrast(ImageEnhance.Color(crop).enhance(1.12)).enhance(1.06)
        arr = np.asarray(crop, dtype=np.float32) / 255.0
        arr = np.power(np.clip(arr, 0.0, 1.0), gamma) * 255.0
        arr = lift_navy_floor(arr)
        frames.append(Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8)))
    pipe_frames(frames, dest)
    return round(max(W / cw, H / ch), 2)


def render_standard_shot(shot: dict, dest: Path, open_f0: Path) -> float:
    dur_s = round(shot["out"] - shot["in"], 3)
    frames_n = round(dur_s * FPS)
    kind = shot["kind"]

    if kind == "match0":
        im = Image.open(open_f0).convert("RGB")
        pipe_frames([im] * frames_n, dest)
        return 1.0

    if kind == "r01a2_bowshock":
        src = SVS_ORIG / "svs_20297_van_allen_earth_only.mp4"
        raw = load_raw_video_frames(src, offset=2.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.6)
        frames = []
        for i, im in enumerate(raw):
            u = i / max(1, frames_n - 1)
            pan_x = int(round(180 * u))
            crop = im.crop((140 + pan_x, 40, 1180 + pan_x, 960)).resize((W, H), Image.Resampling.LANCZOS)
            a = np.asarray(crop, dtype=np.float32) / 255.0
            r = 48.0 + 207.0 * np.power(np.clip(a[:, :, 0], 0, 1), 0.38)
            g = 58.0 + 197.0 * np.power(np.clip(a[:, :, 1], 0, 1), 0.38)
            b = 82.0 + 173.0 * np.power(np.clip(a[:, :, 2], 0, 1), 0.38)
            frames.append(Image.fromarray(np.clip(np.stack([r, g, b], axis=-1), 48, 255).astype(np.uint8)))
        pipe_frames(frames, dest)
        return 0.90

    if kind == "r01b_poledrift_916":
        return render_r01b_poledrift_916(dur_s, dest)

    if kind == "r02a_aurora_916":
        return render_fullbleed_plate(
            NAS_PLATES_V01 / "plate_031_r02a_iss_aurora_v01.mp4",
            offset=0.2, dur_s=dur_s, dest=dest,
            sw=1920, sh=1080, cw=608, ch=1080,
            x0_start=610, x0_end=700, y0_start=0, y0_end=0, speed=1.0, gamma=0.86,
        )

    if kind == "r02a2_magfield":
        src = SVS_ORIG / "svs_3822_magfield_left.mp4"
        raw = load_raw_video_frames(src, offset=46.0, frames_n=frames_n, sw=1920, sh=1080, speed=1.8)
        frames = []
        for i, im in enumerate(raw):
            u = i / max(1, frames_n - 1)
            crop = im.crop((240 + int(160 * u), 90, 1280 + int(160 * u), 990)).resize((W, H), Image.Resampling.LANCZOS)
            a = np.asarray(crop, dtype=np.float32) / 255.0
            r = 28.0 + 218.0 * np.power(np.clip(a[:, :, 0], 0, 1), 0.48)
            g = 36.0 + 212.0 * np.power(np.clip(a[:, :, 1], 0, 1), 0.48)
            b = 56.0 + 198.0 * np.power(np.clip(a[:, :, 2], 0, 1), 0.48)
            frames.append(Image.fromarray(np.clip(np.stack([r, g, b], axis=-1), 28, 255).astype(np.uint8)))
        pipe_frames(frames, dest)
        return 1.35

    if kind == "r02b_flip_916":
        return render_r02b_flip_916(dur_s, dest)

    if kind == "r03a_earth_globe_916":
        return render_fullbleed_plate(
            NAS_PLATES_V01 / "plate_031_r12a_earth_limb_v01.mp4",
            offset=0.4, dur_s=dur_s, dest=dest,
            sw=1920, sh=1080, cw=608, ch=1080,
            x0_start=636, x0_end=686, y0_start=0, y0_end=0, speed=1.05, gamma=0.90,
        )

    if kind == "r03b_earth_limb_916":
        return render_fullbleed_plate(
            NAS_PLATES_V01 / "plate_031_r21_earth_limb_v01.mp4",
            offset=0.6, dur_s=dur_s, dest=dest,
            sw=1920, sh=1080, cw=608, ch=1080,
            x0_start=620, x0_end=700, y0_start=0, y0_end=0, speed=1.10, gamma=0.88,
        )

    if kind == "r04a_iss_ext_916":
        return render_fullbleed_plate(
            NAS_PLATES_V01 / "plate_031_r04a_iss_exterior_v01.mp4",
            offset=0.4, dur_s=dur_s, dest=dest,
            sw=1920, sh=1080, cw=608, ch=1080,
            x0_start=620, x0_end=692, y0_start=0, y0_end=0, speed=1.05, gamma=0.90,
        )

    if kind == "r04a2_belts_saa_916":
        return render_fullbleed_plate(
            NAS_PLATES_V01 / "plate_031_r25_iss_orbit_cuts_v01.mp4",
            offset=11.2, dur_s=dur_s, dest=dest,
            sw=1920, sh=1080, cw=608, ch=1080,
            x0_start=640, x0_end=676, y0_start=0, y0_end=0, speed=1.35, gamma=0.72,
        )

    if kind == "r04b_compass_916":
        return render_r04b_compass_916(dur_s, dest)

    if kind == "r04c_gerst_aurora_916":
        return render_fullbleed_plate(
            GERST_4K,
            offset=11.4, dur_s=dur_s, dest=dest,
            sw=3840, sh=2160, cw=1080, ch=1920,
            x0_start=1340, x0_end=1460, y0_start=180, y0_end=140, speed=1.15, gamma=0.82,
        )

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
    bb = centred(d, BAND_Y1 - 92, text, f, YELLOW, stroke=7)
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
    im = ImageEnhance.Color(im).enhance(1.20)
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
        ("tick", 4.74, -8.5),
        ("tick", TITLE_IN, -8.0),
        ("tick", TEACH_IN, -8.0),
        ("tick", 25.00, -8.5),
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


def build_j2829_review_pack(final_mp4: Path, out_dir: Path) -> dict:
    """Build all J2829 5-part review artifacts: 2fps sheet, +-3 cut splice strips, 3s tail all-frames, .mp3 audio, <=5MB 360x640 proxies."""
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    # Decode all 825 frames at 270x480 once in memory (~300 MB) for instant contact sheets
    tw, th = 270, 480
    total_frames = round(TOTAL_S * FPS)
    raw = sp.check_output([
        "ffmpeg", "-v", "error", "-i", str(final_mp4),
        "-vf", f"fps={FPS},scale={tw}:{th}",
        "-frames:v", str(total_frames),
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ])
    fb = tw * th * 3
    all_frames = [Image.frombytes("RGB", (tw, th), raw[i * fb:(i + 1) * fb]) for i in range(total_frames)]
    f_lbl = ImageFont.truetype(FONT_BOLD, 18)

    # 1. Full-film 0.5 s (2 fps) grid
    idxs_2fps = [min(total_frames - 1, round(k * 0.5 * FPS)) for k in range(int(TOTAL_S * 2) + 1)]
    cols = 9
    rows = (len(idxs_2fps) + cols - 1) // cols
    sheet_2fps = Image.new("RGB", (cols * tw, rows * th), (14, 18, 26))
    for j, fi in enumerate(idxs_2fps):
        tile = all_frames[fi].copy()
        d = ImageDraw.Draw(tile)
        d.rectangle((0, 0, 145, 26), fill=(0, 0, 0))
        d.text((6, 4), f"t={fi / FPS:05.2f}s f{fi:03d}", font=f_lbl, fill=(255, 255, 255))
        sheet_2fps.paste(tile, ((j % cols) * tw, (j // cols) * th))
    p_2fps = out_dir / f"{STEM}_2fps.jpg"
    sheet_2fps.save(p_2fps, quality=86)

    # 2. Cut boundaries +-3 frames (7 frames per cut across all 12 cuts)
    cut_boundaries = [round(s["out"] * FPS) for s in SHOT_PLAN[:-1]]
    sheet_cuts = Image.new("RGB", (7 * tw, len(cut_boundaries) * th), (14, 18, 26))
    for r_idx, cf in enumerate(cut_boundaries):
        for c_idx, df in enumerate(range(-3, 4)):
            fi = max(0, min(total_frames - 1, cf + df))
            tile = all_frames[fi].copy()
            d = ImageDraw.Draw(tile)
            bg_c = (150, 30, 30) if df == 0 else (0, 0, 0)
            d.rectangle((0, 0, 215, 26), fill=bg_c)
            d.text((6, 4), f"cut{r_idx+1:02d} {df:+d} f{fi:03d} ({fi/FPS:.2f}s)", font=f_lbl, fill=(255, 255, 255))
            sheet_cuts.paste(tile, (c_idx * tw, r_idx * th))
    p_cuts = out_dir / f"{STEM}_cuts_pm3.jpg"
    sheet_cuts.save(p_cuts, quality=86)

    # 3. Every frame of final 3.0 s (frames 750..824 = 75 frames)
    tail_start = total_frames - round(3.0 * FPS)
    tail_cols = 10
    tail_rows = (75 + tail_cols - 1) // tail_cols
    sheet_tail = Image.new("RGB", (tail_cols * tw, tail_rows * th), (14, 18, 26))
    for j, fi in enumerate(range(tail_start, total_frames)):
        tile = all_frames[fi].copy()
        d = ImageDraw.Draw(tile)
        d.rectangle((0, 0, 145, 26), fill=(0, 0, 0))
        d.text((6, 4), f"f{fi:03d} {fi/FPS:05.2f}s", font=f_lbl, fill=(255, 255, 255))
        sheet_tail.paste(tile, ((j % tail_cols) * tw, (j // tail_cols) * th))
    p_tail = out_dir / f"{STEM}_tail_3s_all_frames.jpg"
    sheet_tail.save(p_tail, quality=86)

    # 4. Extracted MP3 soundtrack for direct audio_input verification
    p_mp3 = out_dir / f"{STEM}_audio.mp3"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final_mp4), "-vn", "-c:a", "libmp3lame", "-b:a", "160k", str(p_mp3)])

    # 5. Compact <=5 MB 360x640 moving video proxies (full 33s + final 3s)
    p_proxy_full = out_dir / f"{STEM}_proxy_full_360x640.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(final_mp4),
        "-vf", "scale=360:640:flags=lanczos",
        "-c:v", "libx264", "-preset", "fast", "-crf", "26", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(p_proxy_full),
    ])
    p_proxy_tail = out_dir / f"{STEM}_proxy_tail3s_360x640.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{TOTAL_S - 3.0:.2f}", "-i", str(final_mp4),
        "-vf", "scale=360:640:flags=lanczos",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(p_proxy_tail),
    ])
    return {
        "sheet_2fps": str(p_2fps),
        "sheet_cuts_pm3": str(p_cuts),
        "sheet_tail_3s": str(p_tail),
        "audio_mp3": str(p_mp3),
        "proxy_full_mp4": str(p_proxy_full),
        "proxy_full_bytes": p_proxy_full.stat().st_size,
        "proxy_tail_mp4": str(p_proxy_tail),
        "proxy_tail_bytes": p_proxy_tail.stat().st_size,
    }


def main() -> None:
    v01_sha_before = sha256(V01_MP4)
    if v01_sha_before != EXPECTED_V01_SHA256:
        raise SystemExit(f"v01 sha256 mismatch before build: {v01_sha_before} != {EXPECTED_V01_SHA256}")
    vo_sha = sha256(VO_WAV)
    if vo_sha != EXPECTED_VO_SHA256:
        raise SystemExit(f"VO sha256 mismatch: {vo_sha} != {EXPECTED_VO_SHA256}")
    print(f"Verified untouched v01 SHA-256: {v01_sha_before}", flush=True)
    print(f"Verified locked VO SHA-256:     {vo_sha}", flush=True)

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
        if shot["kind"] == "r01a_open":
            up = render_r01a_open(round(shot["out"] - shot["in"], 3), piece, open_f0)
        else:
            up = render_standard_shot(shot, piece, open_f0)
        # Also copy upright code graphics beside NAS plates for provenance
        if shot["source"].startswith("code_graphic_"):
            shutil.copy2(piece, NAS_SUB_OUT / shot["source"])
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
    fc.append(f"[{last_v}]noise=alls=2:allf=t,format=yuv420p[v]")

    run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", ";".join(fc),
        "-map", "[v]", "-map", "5:a",
        *shorts_encode_args(fps=FPS),
        "-t", f"{TOTAL_S:.3f}", str(final_mp4),
    ])

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
        "test_a": True,
        "parent_long_title": LONG_TITLE,
        "spoken": joined,
        "vo_onset_s": VO_LEAD_S,
        "last_word_end_s": last_word_end,
        "duration_s": TOTAL_S,
        "end_card": {
            "start_s": END_CARD_IN,
            "end_s": TOTAL_S,
            "text": END_CARD_LINE,
        },
        "words_file": str(words_path),
        "vo": str(vo_stem_out),
        "audio": aud,
    }, indent=2) + "\n")

    frame0_jpg = NAS_SUB_OUT / f"{STEM}_frame0.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.30", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(frame0_jpg)])
    cover_jpg = NAS_SUB_OUT / f"{STEM}_cover.jpg"
    cover_info = make_cover(cover_jpg, open_f0)

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

    dec_res = run_gate(["ffmpeg", "-v", "error", "-i", final_mp4, "-f", "null", "-"])
    print(f"ffmpeg full decode rc={dec_res.returncode} stderr={dec_res.stderr.strip()!r}", flush=True)

    review_pack = build_j2829_review_pack(final_mp4, REVIEW_SCRATCH)

    v01_sha_after = sha256(V01_MP4)
    if v01_sha_after != EXPECTED_V01_SHA256:
        raise SystemExit(f"CRITICAL: v01 sha256 changed! {v01_sha_after}")

    # Stage UAT folders with SHA256SUMS.json
    uat_files = [
        final_mp4,
        cover_jpg,
        NAS_SUB_OUT / f"{STEM}_frame0_preview.jpg",
        Path(review_pack["sheet_2fps"]),
        Path(review_pack["sheet_cuts_pm3"]),
        Path(review_pack["sheet_tail_3s"]),
        meta_path,
    ]
    for uat_dir in (UAT_NAS, UAT_ICLOUD):
        uat_dir.mkdir(parents=True, exist_ok=True)
        sums = {}
        for f in uat_files:
            dst = uat_dir / f.name
            shutil.copy2(f, dst)
            sums[f.name] = sha256(dst)
        (uat_dir / "SHA256SUMS.json").write_text(json.dumps(sums, indent=2) + "\n")

    summary = {
        "stem": STEM,
        "video_id": "C8lPx5N2DwM",
        "air_date": AIR_DATE,
        "v01_untouched_sha256": v01_sha_after,
        "mp4_path": str(final_mp4),
        "mp4_sha256": sha256(final_mp4),
        "mp4_bytes": final_mp4.stat().st_size,
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
        "j2829_review_pack": review_pack,
        "gates": {
            "gate_shorts_open_rc": g_txt.returncode,
            "thumb_preview_frame0_rc": tp_f0.returncode,
            "thumb_preview_cover_rc": tp_cov.returncode,
            "sfx_level_rc": sfx_res.returncode,
            "music_gate_rc": mg_res.returncode,
            "polish_gate_rc": pg_res.returncode,
            "picture_qa_rc": pqa_res.returncode,
            "ffmpeg_decode_rc": dec_res.returncode,
        },
    }
    (NAS_SUB_OUT / f"{STEM}_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (REVIEW_SCRATCH / f"{STEM}_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("SUMMARY:", json.dumps(summary["gates"], indent=2), flush=True)
    if any(v != 0 for v in summary["gates"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
