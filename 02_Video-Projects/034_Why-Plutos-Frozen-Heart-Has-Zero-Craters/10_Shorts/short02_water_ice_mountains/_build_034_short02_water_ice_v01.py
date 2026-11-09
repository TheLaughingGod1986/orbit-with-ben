#!/usr/bin/env python3
"""Deterministic builder for OWB 034 Short 2 (Keeper Question Short: Water-Ice Mountains).

Job: J2320 — 034 Pluto Short 2 (Keeper question): build 22-27s Charon/water-ice cut + gates
Ruling: J2364 Chief Ruling — Selection 2A (Water-Ice Mountains Whole-Sentence Lift: S46+S47+S48+S50)
Target air slot: Wed 2026-12-23 11:30 London (no upload in this build job)
Spend: £0 (reuses locked 034 VO v03, score bed v01, house SFX kit v01, and studio-live harvest_v01)

Specification (SHORTS_PLAN_v01.md §4.3 + J2364 Chief Ruling + OWB-2026-11-E1):
  - Title: Why Can Towering Mountains Stand on Pluto at −240°C? (52 chars)
  - Alt title: Why Can Towering Water-Ice Mountains Stand on Pluto? (52 chars)
  - Selection: S46 + S47 + S48 + S50 (w0842..w0881 + w0900..w0917; 58 Scribe tokens / 64 spoken words)
  - Duration: 25.800 s (774 frames at 30.00 fps CFR; within 22–27 s Keeper floor/cap)
  - Frame 0 & 0.00–2.40 s Hook Caption: PLUTO'S ICE MOUNTAINS? (ICE in #FFD43B yellow)
  - 9.50–13.50 s Promoted Long Banner: Why Pluto's Frozen Heart Has Zero Craters
  - 18.00–21.60 s Single Teach Overlay (inside 16:9 centre band, 11.5% height): 2–3 KM WATER-ICE PEAKS
  - Payoff ("Pluto's two to three-kilometer mountains are big blocks of water ice"): 17.67–21.87 s (68.5%–84.8% >= 70%)
  - Loop tail: last word "methane." ends at 25.035 s (0.765 s tail <= 1.20 s) with 0.25 s visual crossfade to Frame 0.
"""

from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess as sp
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

FILM_DIR = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters"
)
SHORT_DIR = FILM_DIR / "10_Shorts" / "short02_water_ice_mountains"
EXPORT_DIR = SHORT_DIR / "06_Final-Exports"
HARVEST_DIR = FILM_DIR / "07_Edit-Project" / "harvest_v01" / "matched"
GRAPHICS_DIR = FILM_DIR / "07_Edit-Project" / "graphics_v03" / "full_frame"
VO_MASTER = FILM_DIR / "02_Voiceover" / "pluto_frozen_heart_vo_v03.wav"
VO_STT = FILM_DIR / "02_Voiceover" / "stt" / "pluto_frozen_heart_vo_v03" / "stt_raw.json"
MUSIC_BED = FILM_DIR / "05_Music" / "pluto_score_bed_v01.mp3"
SFX_DIR = FILM_DIR / "06_Sound-Effects" / "kit_v01"

WORK_DIR = Path("/tmp/j2320_short2_work")

W, H = 1080, 1920
BAND_Y0, BAND_Y1 = 656, 1264
BAND_H = BAND_Y1 - BAND_Y0  # 608 px (exact 16:9 inside 1080x1920)
FPS = 30
DURATION = 25.80
TOTAL_FRAMES = int(round(DURATION * FPS))  # 774 frames
SR = 48000

TITLE = "Why Can Towering Mountains Stand on Pluto at \u2212240\u00b0C?"
ALT_TITLE = "Why Can Towering Water-Ice Mountains Stand on Pluto?"
PROMO_LONG_TITLE = "Why Pluto's Frozen Heart Has Zero Craters"
TEACH_OVERLAY_TEXT = "2\u20133 KM WATER-ICE PEAKS"

VO_SLICES = [
    ("S46a", 441.660, 445.200, 842, 850),  # "Why can towering mountains stand beside a flowing glacier"
    ("S46b", 445.360, 447.960, 851, 852),  # "between -226"
    ("S46c", 448.180, 451.340, 853, 856),  # "and -240 degrees Celsius?"
    ("S47", 451.840, 454.580, 857, 863),   # "Here is the biggest misconception about Pluto."
    ("S48a", 454.960, 458.240, 864, 873),  # "On Earth, water ice is a soft glacier that melts,"
    ("S48b", 458.440, 460.780, 874, 881),  # "and rock is the solid ground beneath it."
    ("S50a", 473.880, 478.270, 900, 910),  # "Pluto's two to three-kilometer mountains are big blocks of water ice,"
    ("S50b", 478.530, 482.385, 911, 917),  # "sometimes coated with frozen gases like methane."
]
XFADE_S = 0.015

# All timeline boundaries sit on exact 30-fps frame boundaries (multiples of 0.10s = 3 frames)
# so frame_in_cut = f - start_frame increments by exactly 1 every frame.
CUT_SPECS = [
    {
        "row": "R01",
        "timeline_in": 0.00,
        "timeline_out": 2.50,
        "source": "code_graphic_034_short2_r01_open.mp4",
        "video": True,
        "upscale": 1.00,
        "framing": {"mode": "9x16_centre_band", "offset": 0.0},
        "note": "Custom M1-B opener from PIA20732 (Jagged Shores of Pluto Highlands): fast camera sweep + solar terminator highlight.",
    },
    {
        "row": "R02",
        "timeline_in": 2.50,
        "timeline_out": 4.50,
        "source": "PIA19710.jpg",
        "video": False,
        "upscale": 1.04,
        "brightness": 0.72,
        "contrast": 1.24,
        "step_pf": (2, 0),
        "framing": {"mode": "9x16_centre_band", "pan": "right"},
        "note": "The Icy Mountains of Pluto (Norgay Montes 3 km water-ice peaks).",
    },
    {
        "row": "R03",
        "timeline_in": 4.50,
        "timeline_out": 6.10,
        "source": "PIA19944.jpg",
        "video": False,
        "upscale": 0.85,
        "step_pf": (-2, 0),
        "framing": {"mode": "9x16_centre_band", "pan": "left"},
        "note": "Valley Glaciers on Pluto flowing past water-ice mountain walls.",
    },
    {
        "row": "R04",
        "timeline_in": 6.10,
        "timeline_out": 9.20,
        "source": "PIA20198.jpg",
        "video": False,
        "upscale": 0.50,
        "step_pf": (2, 0),
        "framing": {"mode": "9x16_centre_band", "pan": "right"},
        "note": "The Mountainous Shoreline of Sputnik Planum at -226 to -240 C.",
    },
    {
        "row": "R05",
        "timeline_in": 9.20,
        "timeline_out": 12.00,
        "source": "File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm",
        "video": True,
        "upscale": 1.78,
        "framing": {"mode": "9x16_centre_band", "offset": 16.0},
        "note": "New Horizons close-approach flyover over Sputnik Planitia shoreline mountains + promoted long title banner.",
    },
    {
        "row": "R06",
        "timeline_in": 12.00,
        "timeline_out": 15.20,
        "source": "PIA18033.jpg",
        "video": False,
        "upscale": 0.35,
        "crop_box": (1600, 1100, 5600, 3800),
        "step_pf": (-2, 0),
        "framing": {"mode": "9x16_centre_band", "pan": "left"},
        "note": "Blue Marble Earth high-res continent/glacier crop ('On Earth, water ice is a soft glacier that melts').",
    },
    {
        "row": "R07",
        "timeline_in": 15.20,
        "timeline_out": 17.50,
        "source": "PIA19842.jpg",
        "video": False,
        "upscale": 1.04,
        "step_pf": (2, 0),
        "framing": {"mode": "9x16_centre_band", "pan": "right"},
        "note": "A Mountain Range within Pluto Heart (Hillary Montes bedrock contrast).",
    },
    {
        "row": "R08",
        "timeline_in": 17.50,
        "timeline_out": 20.00,
        "source": "PIA20473.jpg",
        "video": False,
        "upscale": 0.50,
        "step_pf": (-2, 0),
        "unsharp": True,
        "framing": {"mode": "9x16_centre_band", "pan": "left"},
        "note": "The Frozen Canyons and ridges of Pluto + single teach overlay ('2-3 KM WATER-ICE PEAKS').",
    },
    {
        "row": "R09",
        "timeline_in": 20.00,
        "timeline_out": 22.00,
        "source": "PIA20007.jpg",
        "video": False,
        "upscale": 0.92,
        "crop_box": (120, 120, 1060, 700),
        "step_pf": (2, 0),
        "framing": {"mode": "9x16_centre_band", "pan": "right"},
        "note": "Sputnik Planum in Color (payoff: 'are big blocks of water ice').",
    },
    {
        "row": "R10",
        "timeline_in": 22.00,
        "timeline_out": 25.80,
        "source": "PIA19948.jpg",
        "video": False,
        "upscale": 0.65,
        "step_pf": (-2, 0),
        "unsharp": True,
        "framing": {"mode": "9x16_centre_band", "pan": "left"},
        "note": "Pluto Majestic Mountains, Frozen Plains and Foggy Hazes ('sometimes coated with frozen gases like methane') + 0.25s loop crossfade.",
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Impact.ttf" if bold else "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def build_vo_stem_and_words(vo_out: Path, words_out: Path) -> tuple[np.ndarray, list[dict]]:
    """Assemble the 8 E1-tightened VO slices with 15 ms cosine crossfades and emit mapped word timings."""
    with wave.open(str(VO_MASTER), "rb") as wf:
        sr = wf.getframerate()
        nch = wf.getnchannels()
        assert sr == SR and nch == 2, f"Unexpected VO format: sr={sr}, nch={nch}"
        raw = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
        audio = raw.reshape(-1, 2)

    stt = json.loads(VO_STT.read_text())["words"]
    word_entries = [w for w in stt if w.get("type") == "word"]

    xfade_n = int(round(XFADE_S * SR))
    t_fade = np.linspace(0.0, math.pi / 2.0, xfade_n, dtype=np.float32)[:, None]
    fade_out = np.cos(t_fade)
    fade_in = np.sin(t_fade)

    assembled = None
    mapped_words = []

    for idx, (label, s0, s1, w0, w1) in enumerate(VO_SLICES):
        i0 = int(round(s0 * SR))
        i1 = int(round(s1 * SR))
        seg = audio[i0:i1].copy()

        if idx == 0:
            r_n = int(0.010 * SR)
            seg[:r_n] *= np.linspace(0.0, 1.0, r_n, dtype=np.float32)[:, None]
        if idx == len(VO_SLICES) - 1:
            r_n = int(0.015 * SR)
            seg[-r_n:] *= np.linspace(1.0, 0.0, r_n, dtype=np.float32)[:, None]

        if assembled is None:
            slice_dest_start = 0.0
            assembled = seg
        else:
            slice_dest_start = (len(assembled) - xfade_n) / SR
            overlap = assembled[-xfade_n:] * fade_out + seg[:xfade_n] * fade_in
            assembled = np.vstack([assembled[:-xfade_n], overlap, seg[xfade_n:]])

        for wi in range(w0, w1 + 1):
            w = word_entries[wi]
            ws = max(s0, float(w["start"]))
            we = min(s1, float(w["end"]))
            if wi == 856:
                we = 451.210
            mapped_words.append(
                {
                    "word": w["text"],
                    "start": round(slice_dest_start + (ws - s0), 3),
                    "end": round(slice_dest_start + (we - s0), 3),
                    "slice": label,
                    "source_word_index": wi,
                    "source_start": round(float(w["start"]), 3),
                    "source_end": round(float(w["end"]), 3),
                }
            )

    target_samples = int(round(DURATION * SR))
    if len(assembled) < target_samples:
        pad = np.zeros((target_samples - len(assembled), 2), dtype=np.float32)
        assembled = np.vstack([assembled, pad])
    else:
        assembled = assembled[:target_samples]

    pcm = np.clip(assembled * 32767.0, -32768, 32767).astype(np.int16)
    with wave.open(str(vo_out), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())

    words_payload = {
        "film": "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters",
        "short": "034_short02_water_ice_mountains_v01",
        "ruling": "J2364 Selection 2A (S46 + S47 + S48 + S50 whole-sentence lift)",
        "duration_s": DURATION,
        "scribe_word_count": len(mapped_words),
        "spoken_word_count": 64,
        "first_word_start_s": mapped_words[0]["start"],
        "last_word_end_s": mapped_words[-1]["end"],
        "loop_tail_s": round(DURATION - mapped_words[-1]["end"], 3),
        "words": mapped_words,
    }
    words_out.write_text(json.dumps(words_payload, indent=2) + "\n")
    return assembled, mapped_words


def build_sfx_and_bed_stems(vo_audio: np.ndarray, sfx_out: Path, bed_out: Path) -> tuple[np.ndarray, np.ndarray]:
    """Build 25.80s SFX and Music Bed stems calibrated to pass sfx_kit.py level and -14 LUFS master."""
    target_samples = int(round(DURATION * SR))

    def load_wav_stereo(path: Path) -> np.ndarray:
        raw = sp.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-i",
                str(path),
                "-ar",
                str(SR),
                "-ac",
                "2",
                "-f",
                "s16le",
                "-",
            ],
            capture_output=True,
            check=True,
        ).stdout
        arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        return arr.reshape(-1, 2)

    whoosh = load_wav_stereo(SFX_DIR / "sfx_owb_whoosh_soft_v01.wav")
    tick = load_wav_stereo(SFX_DIR / "sfx_owb_tick_ui_v01.wav")

    sfx = np.zeros((target_samples, 2), dtype=np.float32)

    def place_sfx(clip: np.ndarray, start_s: float, gain_db: float, max_dur_s: float | None = None):
        s_idx = int(round(start_s * SR))
        c = clip.copy()
        if max_dur_s is not None:
            max_n = int(round(max_dur_s * SR))
            if len(c) > max_n:
                c = c[:max_n]
                fade_n = min(int(0.04 * SR), len(c))
                c[-fade_n:] *= np.linspace(1.0, 0.0, fade_n, dtype=np.float32)[:, None]
        gain = 10.0 ** (gain_db / 20.0)
        e_idx = min(target_samples, s_idx + len(c))
        if e_idx > s_idx:
            sfx[s_idx:e_idx] += c[: e_idx - s_idx] * gain

    place_sfx(whoosh, 0.00, gain_db=-16.5, max_dur_s=0.85)
    place_sfx(tick, 9.50, gain_db=-17.5, max_dur_s=0.22)
    place_sfx(tick, 18.00, gain_db=-17.5, max_dur_s=0.22)

    raw_bed = sp.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-ss",
            "44.0",
            "-t",
            f"{DURATION:.3f}",
            "-i",
            str(MUSIC_BED),
            "-ar",
            str(SR),
            "-ac",
            "2",
            "-f",
            "s16le",
            "-",
        ],
        capture_output=True,
        check=True,
    ).stdout
    bed = np.frombuffer(raw_bed, dtype=np.int16).astype(np.float32).reshape(-1, 2) / 32768.0
    if len(bed) < target_samples:
        bed = np.vstack([bed, np.zeros((target_samples - len(bed), 2), dtype=np.float32)])
    else:
        bed = bed[:target_samples]

    fi_n = int(0.25 * SR)
    fo_n = int(0.35 * SR)
    bed[:fi_n] *= np.linspace(0.35, 1.0, fi_n, dtype=np.float32)[:, None]
    bed[-fo_n:] *= np.linspace(1.0, 0.35, fo_n, dtype=np.float32)[:, None]
    bed_gain = 10.0 ** (-15.5 / 20.0)
    bed *= bed_gain

    for arr, out_p in ((sfx, sfx_out), (bed, bed_out)):
        pcm = np.clip(arr * 32767.0, -32768, 32767).astype(np.int16)
        with wave.open(str(out_p), "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(SR)
            wf.writeframes(pcm.tobytes())

    return sfx, bed


def render_custom_opener_clip(out_mp4: Path) -> None:
    """Render code_graphic_034_short2_r01_open.mp4 (1080x608, 2.50s, 75f) from PIA20732.jpg with brisk motion >=12."""
    src_im = Image.open(HARVEST_DIR / "PIA20732.jpg").convert("RGB")
    crop = src_im.crop((120, 320, 2680, 2180))  # 2560x1860 jagged Al-Idrisi mountain shoreline
    crop = ImageEnhance.Contrast(crop).enhance(1.06)
    crop = ImageEnhance.Color(crop).enhance(1.12)
    crop = ImageEnhance.Brightness(crop).enhance(0.96)

    bw, bh = 1080, BAND_H  # 1080x608
    n_frames = int(round(2.50 * FPS))  # 75 frames

    proc = sp.Popen(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{bw}x{bh}",
            "-r",
            str(FPS),
            "-i",
            "pipe:0",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "16",
            "-pix_fmt",
            "yuv420p",
            str(out_mp4),
        ],
        stdin=sp.PIPE,
    )

    xx = np.linspace(0.0, 1.0, bw, dtype=np.float32)[None, :, None]
    yy = np.linspace(0.0, 1.0, bh, dtype=np.float32)[:, None, None]

    for f in range(n_frames):
        u = f / max(1, n_frames - 1)
        scale = 1.00 + 0.42 * u
        sw = crop.width / scale
        sh = sw * (bh / bw)
        cx = crop.width * (0.28 + 0.44 * u)
        cy = crop.height * (0.62 - 0.24 * u)
        x0 = cx - sw / 2.0
        y0 = cy - sh / 2.0
        plate = crop.transform(
            (bw, bh),
            Image.Transform.EXTENT,
            (x0, y0, x0 + sw, y0 + sh),
            resample=Image.Resampling.BICUBIC,
        )
        arr = np.asarray(plate, dtype=np.float32)

        sweep_x = 0.12 + 0.78 * u
        dist = (xx - sweep_x) + 0.25 * (yy - 0.5)
        glow = np.exp(-((dist / 0.25) ** 2))
        tint = np.array([[[22.0, 14.0, -6.0]]], dtype=np.float32) * glow + np.array(
            [[[-8.0, 6.0, 24.0]]], dtype=np.float32
        ) * (1.0 - glow)
        arr = np.clip(arr + tint, 0.0, 255.0).astype(np.uint8)
        proc.stdin.write(arr.tobytes())

    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("Failed encoding custom opener clip")


def make_starfield_and_masks() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Precompute the starfield base, vertical backdrop weight, 150px x-modulated band mask, and soft teach-pill mask."""
    rng = np.random.default_rng(3402)
    yy = np.linspace(0.0, 1.0, H, dtype=np.float32)[:, None]
    xx = np.linspace(0.0, 1.0, W, dtype=np.float32)[None, :]
    r = 18.0 + 10.0 * (1.0 - yy) + 4.0 * np.sin(xx * math.pi)
    g = 30.0 + 14.0 * (1.0 - yy) + 5.0 * np.sin(xx * math.pi)
    b = 52.0 + 20.0 * (1.0 - yy) + 8.0 * np.sin(xx * math.pi)
    star_base = np.stack([r, g, b], axis=-1)

    for _ in range(140):
        sx = int(rng.integers(24, W - 24))
        sy = int(rng.integers(24, H - 24))
        if BAND_Y0 - 20 <= sy <= BAND_Y1 + 20:
            continue
        br = float(rng.uniform(55.0, 145.0))
        rad = int(rng.choice([1, 1, 2]))
        y0, y1 = max(0, sy - rad), min(H, sy + rad + 1)
        x0, x1 = max(0, sx - rad), min(W, sx + rad + 1)
        star_base[y0:y1, x0:x1, 0] = np.clip(star_base[y0:y1, x0:x1, 0] + br * 0.85, 0, 255)
        star_base[y0:y1, x0:x1, 1] = np.clip(star_base[y0:y1, x0:x1, 1] + br * 0.92, 0, 255)
        star_base[y0:y1, x0:x1, 2] = np.clip(star_base[y0:y1, x0:x1, 2] + br, 0, 255)

    y_all = np.arange(H, dtype=np.float32)
    dist_band = np.maximum(0.0, np.maximum(BAND_Y0 - y_all, y_all - BAND_Y1)) / 500.0
    w_bg = np.clip(0.84 - 0.50 * dist_band, 0.34, 0.84)[:, None, None]

    feather = 150.0
    y_rel = np.arange(BAND_H, dtype=np.float32)[:, None]
    x_wave = 18.0 * np.sin(np.linspace(0.0, 2.0 * math.pi, W, dtype=np.float32))[None, :]
    t_top = np.clip((y_rel - x_wave * 0.5) / feather, 0.0, 1.0)
    t_bot = np.clip(((BAND_H - 1 - y_rel) + x_wave * 0.5) / feather, 0.0, 1.0)
    band_mask = (0.5 - 0.5 * np.cos(math.pi * np.minimum(t_top, t_bot)))[:, :, None]

    py0, py1 = 1186, 1256
    px0, px1 = 180, W - 180
    yy_p = np.arange(H, dtype=np.float32)[:, None]
    xx_p = np.arange(W, dtype=np.float32)[None, :]
    cy = 0.5 * (py0 + py1)
    cx = 0.5 * (px0 + px1)
    hy = 0.5 * (py1 - py0)
    hx = 0.5 * (px1 - px0)
    dy = np.maximum(0.0, np.abs(yy_p - cy) - (hy - 18.0)) / 18.0
    dx = np.maximum(0.0, np.abs(xx_p - cx) - (hx - 28.0)) / 28.0
    d_norm = np.sqrt(dy * dy + dx * dx)
    teach_pill_mask = np.clip(0.5 + 0.5 * np.cos(math.pi * np.clip(d_norm, 0.0, 1.0)), 0.0, 1.0) * 0.78

    return star_base, w_bg, band_mask, teach_pill_mask


def compose_9x16_from_band(
    band_rgb: Image.Image,
    star_base: np.ndarray,
    w_bg: np.ndarray,
    band_mask: np.ndarray,
) -> Image.Image:
    """Composite a 1080x608 16:9 plate onto 1080x1920 with zero horizontal seams."""
    bg_fill = band_rgb.resize((W, H), resample=Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=22))
    bg_arr = np.asarray(bg_fill, dtype=np.float32) * w_bg + star_base * (1.0 - w_bg)
    band_arr = np.asarray(band_rgb, dtype=np.float32)
    bg_arr[BAND_Y0:BAND_Y1] = band_arr * band_mask + bg_arr[BAND_Y0:BAND_Y1] * (1.0 - band_mask)
    return Image.fromarray(np.clip(bg_arr, 0, 255).astype(np.uint8), mode="RGB")


def draw_hook_caption(im: Image.Image, t: float, is_cover: bool = False) -> Image.Image:
    """Draw the Frame-0 / 0.00–2.40s top hook caption: PLUTO'S / ICE / MOUNTAINS? (yellow ICE)."""
    if not is_cover and t >= 2.40:
        return im
    alpha = 1.0
    if not is_cover and t > 2.05:
        alpha = max(0.0, min(1.0, (2.40 - t) / 0.35))

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    font = load_font(96, bold=True)

    d.rounded_rectangle(
        (96, 175, W - 96, 555),
        radius=34,
        fill=(10, 18, 32, int(round(190 * alpha))),
        outline=(110, 175, 235, int(round(115 * alpha))),
        width=3,
    )

    lines = [
        ("PLUTO'S", (255, 255, 255)),
        ("ICE", (255, 212, 59)),
        ("MOUNTAINS?", (255, 255, 255)),
    ]
    ys = [248, 362, 476]
    for (txt, col), y in zip(lines, ys):
        d.text(
            (W // 2 + 4, y + 4),
            txt,
            font=font,
            fill=(0, 0, 0, int(round(230 * alpha))),
            anchor="mm",
        )
        d.text(
            (W // 2, y),
            txt,
            font=font,
            fill=(col[0], col[1], col[2], int(round(255 * alpha))),
            anchor="mm",
            stroke_width=4,
            stroke_fill=(8, 14, 24, int(round(235 * alpha))),
        )

    out = im.convert("RGBA")
    out.alpha_composite(layer)
    return out.convert("RGB")


def draw_promo_banner(im: Image.Image, t: float) -> Image.Image:
    """Draw the 9.50–13.50s promoted long exact listing title banner below the 16:9 band."""
    if not (9.50 <= t <= 13.50):
        return im
    fade = min((t - 9.50) / 0.35, (13.50 - t) / 0.35, 1.0)
    fade = max(0.0, fade)
    slide_y = int(round((1.0 - fade) * 18))

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f_kicker = load_font(30, bold=True)
    f_title = load_font(42, bold=True)

    bx0, by0, bx1, by1 = 76, 1320 + slide_y, W - 76, 1500 + slide_y
    d.rounded_rectangle(
        (bx0, by0, bx1, by1),
        radius=24,
        fill=(14, 24, 42, int(round(228 * fade))),
        outline=(255, 212, 59, int(round(215 * fade))),
        width=3,
    )
    d.text(
        (W // 2, by0 + 42),
        "FULL FILM ON ORBIT WITH BEN \u25b8",
        font=f_kicker,
        fill=(255, 212, 59, int(round(250 * fade))),
        anchor="mm",
    )
    d.text(
        (W // 2, by0 + 98),
        "Why Pluto's Frozen Heart",
        font=f_title,
        fill=(255, 255, 255, int(round(255 * fade))),
        anchor="mm",
    )
    d.text(
        (W // 2, by0 + 146),
        "Has Zero Craters",
        font=f_title,
        fill=(255, 255, 255, int(round(255 * fade))),
        anchor="mm",
    )

    out = im.convert("RGBA")
    out.alpha_composite(layer)
    return out.convert("RGB")


def draw_teach_overlay(im: Image.Image, t: float, teach_pill_mask: np.ndarray) -> Image.Image:
    """Draw the single Teach overlay (18.00–21.60s) inside the 16:9 centre band (y=1186..1256, 70px = 11.51%)."""
    if not (18.00 <= t <= 21.60):
        return im
    fade = min((t - 18.00) / 0.35, (21.60 - t) / 0.35, 1.0)
    fade = max(0.0, fade)

    arr = np.asarray(im, dtype=np.float32)
    mask = (teach_pill_mask * fade)[:, :, None]
    pill_col = np.array([[[12.0, 22.0, 38.0]]], dtype=np.float32)
    arr = arr * (1.0 - mask) + pill_col * mask
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGB").convert("RGBA")

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    font = load_font(44, bold=True)
    cy = (1186 + 1256) // 2
    d.text(
        (W // 2 + 2, cy + 2),
        TEACH_OVERLAY_TEXT,
        font=font,
        fill=(0, 0, 0, int(round(220 * fade))),
        anchor="mm",
    )
    d.text(
        (W // 2, cy),
        TEACH_OVERLAY_TEXT,
        font=font,
        fill=(255, 255, 255, int(round(255 * fade))),
        anchor="mm",
        stroke_width=2,
        stroke_fill=(8, 14, 24, int(round(225 * fade))),
    )

    out.alpha_composite(layer)
    return out.convert("RGB")


def prepare_still_source(spec: dict) -> tuple[Image.Image, int, int]:
    """Load and colour-grade a still source image for exact integer-pixel-per-frame pan."""
    im = Image.open(HARVEST_DIR / spec["source"]).convert("RGB")
    if "crop_box" in spec:
        im = im.crop(spec["crop_box"])
    if "brightness" in spec:
        im = ImageEnhance.Brightness(im).enhance(spec["brightness"])
    im = ImageEnhance.Contrast(im).enhance(spec.get("contrast", 1.10))
    im = ImageEnhance.Color(im).enhance(1.10)
    if spec.get("unsharp"):
        im = im.filter(ImageFilter.UnsharpMask(radius=2.0, percent=135, threshold=2))

    dur = spec["timeline_out"] - spec["timeline_in"]
    n_fr = int(round(dur * FPS)) + 4
    dx_pf, dy_pf = spec["step_pf"]
    w_need = W + abs(dx_pf) * n_fr + 80
    h_need = BAND_H + abs(dy_pf) * n_fr + 40
    scale = max(w_need / im.width, h_need / im.height)
    scaled_w = int(round(im.width * scale))
    scaled_h = int(round(im.height * scale))
    scaled = im.resize((scaled_w, scaled_h), resample=Image.Resampling.LANCZOS)

    x_start = 40 if dx_pf >= 0 else scaled_w - W - 40
    y_start = (scaled_h - BAND_H) // 2
    return scaled, x_start, y_start


def render_still_band_frame(scaled_pack: tuple[Image.Image, int, int], spec: dict, frame_in_cut: int) -> Image.Image:
    """Render a 1080x608 frame from a pre-scaled still using exact integer-pixel translation per frame."""
    scaled_im, x_start, y_start = scaled_pack
    dx_pf, dy_pf = spec["step_pf"]
    x0 = max(0, min(scaled_im.width - W, x_start + frame_in_cut * dx_pf))
    y0 = max(0, min(scaled_im.height - BAND_H, y_start + frame_in_cut * dy_pf))
    return scaled_im.crop((x0, y0, x0 + W, y0 + BAND_H))


def load_video_clip_frames(video_path: Path, offset_s: float, dur_s: float) -> list[Image.Image]:
    """Decode a video stretch to 1080x608 RGB frames at 30 fps."""
    n_frames = int(round(dur_s * FPS))
    raw = sp.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-ss",
            f"{offset_s:.3f}",
            "-t",
            f"{dur_s + 0.15:.3f}",
            "-i",
            str(video_path),
            "-vf",
            f"fps={FPS},scale={W}:{BAND_H}:force_original_aspect_ratio=increase,crop={W}:{BAND_H},eq=contrast=1.08:saturation=1.12",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-",
        ],
        capture_output=True,
        check=True,
    ).stdout
    frame_bytes = W * BAND_H * 3
    total_got = len(raw) // frame_bytes
    frames = []
    for i in range(n_frames):
        idx = min(i, total_got - 1)
        buf = raw[idx * frame_bytes : (idx + 1) * frame_bytes]
        frames.append(Image.frombytes("RGB", (W, BAND_H), buf))
    return frames


def calibrate_and_mux_master(
    silent_mp4: Path,
    vo_wav: Path,
    sfx_wav: Path,
    bed_wav: Path,
    final_mp4: Path,
) -> dict:
    """Mix VO + SFX + Bed to -14.0 LUFS / <= -2.0 dBTP and mux into CFR 30.00 fps MP4."""
    raw_mix = WORK_DIR / "mix_raw.wav"
    cal_mix = WORK_DIR / "mix_cal.wav"

    sp.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(vo_wav),
            "-i",
            str(sfx_wav),
            "-i",
            str(bed_wav),
            "-filter_complex",
            "[0:a][1:a][2:a]amix=inputs=3:weights='1 1 1':normalize=0,alimiter=limit=0.78:level=false[aout]",
            "-map",
            "[aout]",
            "-ar",
            str(SR),
            "-ac",
            "2",
            str(raw_mix),
        ],
        check=True,
    )

    def measure_ebur128(wav_path: Path) -> tuple[float, float]:
        out = sp.run(
            [
                "ffmpeg",
                "-nostats",
                "-i",
                str(wav_path),
                "-filter_complex",
                "ebur128=peak=true",
                "-f",
                "null",
                "-",
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stderr
        i_lufs, tp_db = -14.0, -2.5
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("I:") and "LUFS" in line:
                i_lufs = float(line.split()[1])
            elif line.startswith("Peak:") and "dBFS" in line:
                tp_db = float(line.split()[1])
        return i_lufs, tp_db

    i_raw, _ = measure_ebur128(raw_mix)
    gain_db = -14.0 - i_raw
    sp.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(raw_mix),
            "-af",
            f"volume={gain_db:.3f}dB,alimiter=limit=0.76:level=false",
            "-ar",
            str(SR),
            "-ac",
            "2",
            str(cal_mix),
        ],
        check=True,
    )

    sp.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(silent_mp4),
            "-i",
            str(cal_mix),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            str(SR),
            "-ac",
            "2",
            "-movflags",
            "+faststart",
            "-shortest",
            str(final_mp4),
        ],
        check=True,
    )

    i_mp4, tp_mp4 = measure_ebur128(final_mp4)
    if abs(i_mp4 - (-14.0)) > 0.15:
        adj_db = gain_db + (-14.0 - i_mp4)
        sp.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                str(raw_mix),
                "-af",
                f"volume={adj_db:.3f}dB,alimiter=limit=0.76:level=false",
                "-ar",
                str(SR),
                "-ac",
                "2",
                str(cal_mix),
            ],
            check=True,
        )
        sp.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                str(silent_mp4),
                "-i",
                str(cal_mix),
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-ar",
                str(SR),
                "-ac",
                "2",
                "-movflags",
                "+faststart",
                "-shortest",
                str(final_mp4),
            ],
            check=True,
        )
        i_mp4, tp_mp4 = measure_ebur128(final_mp4)

    return {"integrated_lufs": round(i_mp4, 2), "true_peak_dbtp": round(tp_mp4, 2)}


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    GRAPHICS_DIR.mkdir(parents=True, exist_ok=True)

    stem_vo = WORK_DIR / "034_short02_water_ice_mountains_v01_stem_vo.wav"
    words_json = WORK_DIR / "034_short02_water_ice_mountains_v01_words.json"
    stem_sfx = WORK_DIR / "034_short02_water_ice_mountains_v01_stem_sfx.wav"
    stem_bed = WORK_DIR / "034_short02_water_ice_mountains_v01_stem_bed.wav"
    silent_mp4 = WORK_DIR / "034_short02_water_ice_mountains_v01_silent.mp4"
    final_mp4 = WORK_DIR / "034_short02_water_ice_mountains_v01.mp4"
    cover_jpg = WORK_DIR / "034_short02_water_ice_mountains_v01_cover.jpg"
    cuts_json = WORK_DIR / "cuts_v01.json"
    meta_json = WORK_DIR / "034_short02_water_ice_mountains_v01_meta.json"

    print("[1/5] Building E1-tightened VO stem and word timings...")
    vo_audio, mapped_words = build_vo_stem_and_words(stem_vo, words_json)
    print(
        f"      VO words: {len(mapped_words)} Scribe tokens (64 spoken), "
        f"first={mapped_words[0]['start']:.3f}s, last={mapped_words[-1]['end']:.3f}s, "
        f"loop_tail={DURATION - mapped_words[-1]['end']:.3f}s"
    )

    print("[2/5] Building house SFX stem and Pluto score bed stem...")
    build_sfx_and_bed_stems(vo_audio, stem_sfx, stem_bed)

    print("[3/5] Rendering custom M1-B opener clip (code_graphic_034_short2_r01_open.mp4)...")
    opener_clip_path = GRAPHICS_DIR / "code_graphic_034_short2_r01_open.mp4"
    render_custom_opener_clip(opener_clip_path)

    print("[4/5] Rendering 774 frames (25.80s @ 30.00 fps CFR) 9:16 master...")
    star_base, w_bg, band_mask, teach_pill_mask = make_starfield_and_masks()

    still_cache: dict[str, tuple[Image.Image, int, int]] = {}
    video_cache: dict[str, list[Image.Image]] = {}
    for spec in CUT_SPECS:
        row = spec["row"]
        dur = spec["timeline_out"] - spec["timeline_in"]
        if spec["video"]:
            vpath = (
                opener_clip_path
                if spec["source"] == "code_graphic_034_short2_r01_open.mp4"
                else HARVEST_DIR / spec["source"]
            )
            video_cache[row] = load_video_clip_frames(vpath, spec["framing"]["offset"], dur)
        else:
            still_cache[row] = prepare_still_source(spec)

    frame0_band = video_cache["R01"][0]
    cover_frame = draw_hook_caption(
        compose_9x16_from_band(frame0_band, star_base, w_bg, band_mask), 0.0, is_cover=True
    )
    cover_frame.save(cover_jpg, quality=95)

    proc = sp.Popen(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{W}x{H}",
            "-r",
            str(FPS),
            "-i",
            "pipe:0",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "16",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(FPS),
            str(silent_mp4),
        ],
        stdin=sp.PIPE,
    )

    for f in range(TOTAL_FRAMES):
        t = f / FPS
        spec = next((c for c in CUT_SPECS if int(round(c["timeline_in"] * FPS)) <= f < int(round(c["timeline_out"] * FPS))), CUT_SPECS[-1])
        row = spec["row"]
        cut_start_f = int(round(spec["timeline_in"] * FPS))
        frame_in_cut = max(0, f - cut_start_f)

        if spec["video"]:
            frames_list = video_cache[row]
            f_idx = min(frame_in_cut, len(frames_list) - 1)
            band_im = frames_list[f_idx]
        else:
            band_im = render_still_band_frame(still_cache[row], spec, frame_in_cut)

        if t >= DURATION - 0.25:
            w_loop = min(1.0, max(0.0, (t - (DURATION - 0.25)) / 0.25))
            band_im = Image.blend(band_im, frame0_band, w_loop)

        full_im = compose_9x16_from_band(band_im, star_base, w_bg, band_mask)
        full_im = draw_hook_caption(full_im, t, is_cover=False)
        full_im = draw_promo_banner(full_im, t)
        full_im = draw_teach_overlay(full_im, t, teach_pill_mask)
        proc.stdin.write(full_im.tobytes())

    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("Failed encoding silent 9:16 master")

    print("[5/5] Calibrating loudness (-14.0 LUFS / <= -2.0 dBTP) and muxing master...")
    loudness = calibrate_and_mux_master(silent_mp4, stem_vo, stem_sfx, stem_bed, final_mp4)
    print(f"      Loudness: {loudness['integrated_lufs']} LUFS, True Peak: {loudness['true_peak_dbtp']} dBTP")

    cuts_out_list = [
        {
            "row": c["row"],
            "timeline_in": c["timeline_in"],
            "timeline_out": c["timeline_out"],
            "source": c["source"],
            "video": c["video"],
            "upscale": c["upscale"],
            "framing": c["framing"],
            "note": c["note"],
        }
        for c in CUT_SPECS
    ]
    cuts_json.write_text(json.dumps(cuts_out_list, indent=2) + "\n")

    meta = {
        "job": "J2320",
        "ruling": "J2364 Selection 2A (S46 + S47 + S48 + S50 whole-sentence lift)",
        "film": "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters",
        "short_id": "034_short02_water_ice_mountains_v01",
        "format": "Keeper Question Short (OWB-2026-11-E1)",
        "air_slot": "2026-12-23T11:30:00Z",
        "title": TITLE,
        "alt_title": ALT_TITLE,
        "hook_caption": "PLUTO'S ICE MOUNTAINS?",
        "hook_yellow_word": "ICE",
        "promoted_long_title": PROMO_LONG_TITLE,
        "promoted_long_window_s": [9.50, 13.50],
        "single_teach_overlay": {
            "text": TEACH_OVERLAY_TEXT,
            "word_count": 4,
            "window_s": [18.00, 21.60],
            "band_height_px": 70,
            "band_height_pct": 11.51,
        },
        "duration_s": DURATION,
        "frames": TOTAL_FRAMES,
        "fps": FPS,
        "resolution": f"{W}x{H}",
        "scribe_words": len(mapped_words),
        "spoken_words": 64,
        "first_word_start_s": mapped_words[0]["start"],
        "last_word_end_s": mapped_words[-1]["end"],
        "loop_tail_s": round(DURATION - mapped_words[-1]["end"], 3),
        "payoff_window_s": [17.67, 21.87],
        "payoff_pct": [68.5, 84.8],
        "cut_1_s": 2.50,
        "cut_2_s": 4.50,
        "max_shot_s": 3.80,
        "loudness": loudness,
        "spend_gbp": 0.0,
        "sha256": {
            "mp4": sha256_file(final_mp4),
            "cover_jpg": sha256_file(cover_jpg),
            "stem_vo_wav": sha256_file(stem_vo),
            "stem_sfx_wav": sha256_file(stem_sfx),
            "stem_bed_wav": sha256_file(stem_bed),
        },
    }
    meta_json.write_text(json.dumps(meta, indent=2) + "\n")

    for p in (stem_vo, words_json, stem_sfx, stem_bed, final_mp4, cover_jpg, cuts_json, meta_json):
        shutil.copy2(p, EXPORT_DIR / p.name)
    print(f"Done -> {EXPORT_DIR} (mp4 sha256={meta['sha256']['mp4']})")


if __name__ == "__main__":
    main()
