#!/usr/bin/env python3
"""029 Betelgeuse — weekday Shorts v06 full-frame 9:16 rebuild (J2551 / J2829).

Rebuilds the three December 029 Shorts from their untouched Ben-OK'd v04 bases
(leaving v04 and v05 completely untouched) so every single shot fills the full
1080x1920 (9:16) frame with zero blurred bands, zero mirrored bands, and zero
flat top/bottom bars:

  1. Short 2 (`SWDCZfWZVao`, Wed 9 Dec — `029_short_wed09_great_dimming_v06`):
     - `s02_dip_a` (2.69–5.12 s): rebuilt upright 1080x1920 from `r15_dip`
       (`build_code_graphics_v01.py`) with full-height celestial blueprint
       rings, starfield, and Great Dimming light-curve trough.
     - `s03_sphere_dec` (5.12–8.74 s) & `s06_visir` (8.74–12.39 s): ESO VLT
       SPHERE / VISIR Betelgeuse composited over distinct full-bleed 9:16 crops
       of NOIRLab Gemini North's Orion night sky (`gemini_night.jpg`, 0.68x
       downscale) instead of blurred padding.
     - `s07_eject` (12.39–15.20 s): full-bleed 9:16 crop of ESO's moving
       `orion_over_paranal.mp4` (`1.778x` upscale; avoids quarantined
       `mass_ejection.jpg` chart).
  2. Short 3 (`k2kEaA7ICjc`, Fri 11 Dec — `029_short_fri11_opening_testA_v06`):
     - `s01_visir` (0.00–2.23 s) & `s04_sphere` (8.56–12.14 s): ESO VLT VISIR
       and SPHERE Betelgeuse composited over distinct full-bleed 9:16 crops of
       `gemini_night.jpg` (`0.68x` downscale) with zero blur and crisp top/bottom
       starfields.
     - `s05_promise_a`, `s06_promise_b`, `s08_promise_c`, `s09_promise_d`
       (12.14–18.73 s & 21.14–26.90 s): rebuilt upright 1080x1920 from
       `r03_r04_promise` (`build_code_graphics_v01.py` — full-height J2000 sky
       Orion flare, Solar System scale with Earth/Mars/asteroid belt, Great
       Dimming curve, and fusion core shells).
  3. Short 4 (`heiGCnGKTkE`, Mon 14 Dec — `029_short_mon14_half_moon_daylight_v06`):
     - `s02_neutrino` (2.99–5.76 s): full-height 9:16 SDO Sun + polar telemetry
       + vertical neutrino burst.
     - `s03_chajnantor` (5.76–8.90 s): replaced 720p band-padded clip with
       full-bleed 9:16 crop of ESO's 1080p `lasilla_mw.mp4` (`1.778x` upscale).
     - `s05_orion_flare` (12.36–16.16 s) & `s07_daylight` (19.82–21.94 s):
       rebuilt upright 1080x1920 from `r25_orion` and `r27_orion`
       (`build_code_graphics_v01.py`).

Preserves 100% of v04's voice slices, words, durations, captions, hooks, teach
cards, SFX timing, and -14.0 LUFS / <= -1.9 dBTP calibrated AAC loudness. £0.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess as sp
import sys
import wave
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

Image.MAX_IMAGE_PIXELS = None

MAIN_REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
STUDIO_LIVE = Path("/Volumes/data/studio-live/orbit-with-ben")
FILM_REL = Path("02_Video-Projects/029_Is-Betelgeuse-About-To-Explode")
LIVE_FILM = STUDIO_LIVE / FILM_REL if (STUDIO_LIVE / FILM_REL).exists() else MAIN_REPO / FILM_REL
LOCAL_FILM = MAIN_REPO / FILM_REL

EDIT = LIVE_FILM / "07_Edit-Project"
HDIR = EDIT / "harvest_v01"
CG_ASSETS = EDIT / "code_graphics_v01" / "assets"
VO_WAV = LIVE_FILM / "02_Voiceover" / "betelgeuse_vo_v01.wav"
BED_MP3 = LIVE_FILM / "05_Music" / "betelgeuse_score_bed_v01.mp3"
KIT_DIR = LIVE_FILM / "06_Sound-Effects" / "kit_v01"
WORDS_JSON = EDIT / "full_rough_v03b_pack" / "betelgeuse_words_list.json"
REV_OK = EDIT / "full_rough_v03b_pack" / "reviewed_ok_v03b.json"

WORK_ROOT = Path("/Volumes/MiniWork/scratch/J2551/029_shorts_work_v06")
REVIEW_ROOT = Path("/Volumes/MiniWork/scratch/J2551/029_v06_review")
UAT_ICLOUD_ROOT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
UAT_NAS_ROOT = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT")

sys.path.insert(0, str(MAIN_REPO / "04_Audio/tools"))
sys.path.insert(0, str(MAIN_REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(MAIN_REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import gate_shorts_open as gso  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 30
SR = 48000
BAND_H = round(W * 9 / 16)          # 608
BAND_Y0 = (H - BAND_H) // 2         # 656
BAND_Y1 = BAND_Y0 + BAND_H          # 1264
LINE_H = round(BAND_H * 0.115)      # 70
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)
CG_GOLD = (255, 201, 74)
CG_WHITE = (244, 239, 230)
CG_ICE = (176, 214, 232)
CG_ORANGE = (255, 154, 72)
CG_DIM = (150, 168, 190)
SHELLS = [
    (255, 176, 122),
    (255, 210, 122),
    (242, 226, 160),
    (183, 217, 138),
    (143, 208, 216),
    (176, 182, 194),
]

LONG_ID = "vP1BbqZ_dnM"
LONG_TITLE = "Is Betelgeuse About to Explode?"
TITLE_ROWS = ["Is Betelgeuse", "About to", "Explode?"]
END_CARD_LINE = "Full film on the channel"
END_ROWS = [("Is Betelgeuse", WHITE), ("About to", WHITE), ("Explode?", WHITE), (END_CARD_LINE, YELLOW)]
HOOK_END = 2.20
TITLE_IN, TITLE_OUT = 9.00, 14.00
END_CARD = 2.00
VO_TAIL = 0.30
ALL_WORDS = json.loads(WORDS_JSON.read_text())

EXPECTED_V04_SHA256 = {
    "wed09_great_dimming": "e0459b017ddafdf84229784c5694507140523e92043ab2109b8f3c3",  # checked via full 64-hex below
}
EXPECTED_V04_SHA256 = {
    "wed09_great_dimming": "e0459b017ddafdf84229784c170285d4c5694507140523e92043ab2109b8f3c3",
    "fri11_opening_testA": "ff4194857a027cfc5f93551ef398125276e6bcfb9cd3ce2fd18d8ee1134e2405",
    "mon14_half_moon_daylight": "31f362f4437b4ca56ec16b8abef1dce4c65fb5a5c6c7b5b4e2ba39229a33efd5",
}

# Real J2000 coordinates (RA hours, Dec degrees) of Orion's main stars (Hipparcos / Yale Bright Star Catalog)
ORION = {
    "betelgeuse": (5.9195, 7.407, "orange"),
    "bellatrix": (5.4189, 6.350, "blue"),
    "meissa": (5.5856, 9.934, "white"),
    "alnitak": (5.6793, -1.943, "belt"),
    "alnilam": (5.6036, -1.202, "belt"),
    "mintaka": (5.5334, -0.299, "belt"),
    "saiph": (5.7959, -9.669, "white"),
    "rigel": (5.2423, -8.202, "blue"),
}

# Real J2000 cataloged field stars across vertical 9:16 winter sky (+42 deg Auriga/Taurus/Gemini down to -42 deg Lepus/Columba/Canis Major)
ORION_CATALOG_FIELD_916 = [
    # Core Orion, Sword, Shield, Club
    (5.5906, -5.910, 2.77, "blue"),    # Hatysa (iota Ori)
    (5.5881, -5.389, 3.70, "white"),   # Theta1 Ori / M42
    (5.5885, -4.838, 4.59, "blue"),    # c Ori
    (5.6450, -2.600, 3.80, "blue"),    # sigma Ori
    (5.4079, -2.397, 3.35, "blue"),    # eta Ori
    (5.2931, -6.844, 3.59, "blue"),    # tau Ori
    (5.4950, -1.092, 4.71, "orange"),  # 31 Ori
    (5.4472, 3.096, 4.59, "blue"),     # psi Ori
    (5.3881, 1.846, 4.95, "blue"),     # 25 Ori
    (5.6533, 4.065, 4.57, "blue"),     # omega Ori
    (5.5806, 9.490, 4.41, "blue"),     # phi1 Ori
    (5.6150, 9.291, 4.09, "orange"),   # phi2 Ori
    (4.8308, 6.961, 3.19, "white"),    # pi3 Ori (Tabit)
    (4.8542, 5.605, 3.69, "blue"),     # pi4 Ori
    (4.9042, 2.441, 3.72, "blue"),     # pi5 Ori
    (4.8436, 8.900, 4.36, "white"),    # pi2 Ori
    (4.9147, 10.151, 4.65, "white"),   # pi1 Ori
    (4.9761, 1.714, 4.47, "orange"),   # pi6 Ori
    (6.0397, 9.647, 4.12, "white"),    # mu Ori
    (5.8744, 1.856, 4.76, "orange"),   # 56 Ori
    (5.9797, 0.553, 5.10, "white"),    # 60 Ori
    (5.1308, -5.086, 2.79, "white"),   # Cursa (beta Eri)
    (5.1481, -8.754, 4.27, "blue"),    # lambda Eri
    (4.8831, -5.452, 4.39, "white"),   # omega Eri
    (4.7583, -3.255, 4.00, "blue"),    # mu Eri
    (5.4000, -7.808, 4.14, "orange"),  # 29 Ori
    (6.4800, -7.033, 3.76, "blue"),    # beta Mon
    (6.3953, 4.593, 4.39, "white"),    # epsilon Mon
    (6.5480, 7.330, 4.50, "white"),    # 13 Mon
    # Northern winter field (+12 deg to +42 deg: Taurus, Gemini, Auriga)
    (4.5987, 16.509, 0.86, "orange"),  # Aldebaran (alpha Tau)
    (5.4382, 28.608, 1.65, "blue"),    # Elnath (beta Tau)
    (5.6274, 21.143, 2.97, "blue"),    # Tianguan (zeta Tau)
    (4.4769, 15.871, 3.40, "white"),   # theta2 Tau (Hyades)
    (4.4294, 19.180, 3.53, "orange"),  # epsilon Tau (Ain)
    (4.3299, 15.628, 3.65, "orange"),  # gamma Tau
    (5.9921, 20.276, 4.30, "orange"),  # chi1 Ori / northern club
    (6.0792, 14.768, 4.42, "white"),   # nu Ori
    (6.1986, 14.209, 4.35, "blue"),    # xi Ori
    (6.2478, 22.507, 3.19, "orange"),  # Tejat Prior (eta Gem)
    (6.3826, 22.514, 2.87, "orange"),  # Tejat (mu Gem)
    (6.6285, 16.399, 1.93, "white"),   # Alhena (gamma Gem)
    (6.7322, 25.131, 3.06, "orange"),  # Mebsuta (epsilon Gem)
    (6.7542, 12.896, 3.35, "white"),   # xi Gem (Alzirr)
    (4.9499, 33.166, 2.69, "orange"),  # Hassaleh (iota Aur)
    (5.9951, 37.213, 2.62, "white"),   # Mahasim (theta Aur)
    (5.2782, 45.998, 0.08, "orange"),  # Capella (alpha Aur)
    (5.1086, 41.234, 3.18, "blue"),    # eta Aur
    (5.0331, 43.823, 3.03, "orange"),  # epsilon Aur
    # Southern winter field (-11 deg to -42 deg: Lepus, Canis Major, Eridanus, Columba)
    (5.5453, -17.822, 2.58, "white"),  # Arneb (alpha Lep)
    (5.4708, -20.759, 2.84, "orange"), # Nihal (beta Lep)
    (5.1908, -22.371, 3.19, "orange"), # epsilon Lep
    (5.2156, -16.205, 3.29, "blue"),   # mu Lep
    (5.7824, -14.822, 3.55, "white"),  # zeta Lep
    (5.9500, -14.168, 3.71, "white"),  # eta Lep
    (5.7408, -22.448, 3.60, "orange"), # gamma Lep
    (5.8556, -20.879, 3.81, "orange"), # delta Lep
    (5.2094, -11.868, 4.30, "blue"),   # iota Lep
    (5.1522, -13.177, 4.46, "blue"),   # kappa Lep
    (6.3783, -17.956, 1.98, "blue"),   # Mirzam (beta CMa)
    (6.7525, -16.716, -1.46, "white"), # Sirius (alpha CMa)
    (6.3375, -30.063, 3.02, "blue"),   # Furud (zeta CMa)
    (6.6292, -19.256, 4.02, "blue"),   # nu2 CMa
    (5.6608, -34.074, 2.65, "blue"),   # Phact (alpha Col)
    (5.8492, -35.768, 3.12, "orange"), # Wazn (beta Col)
    (5.9589, -35.283, 4.36, "blue"),   # gamma Col
    (6.3686, -33.436, 3.85, "orange"), # delta Col
    (4.6975, -30.563, 3.81, "blue"),   # upsilon2 Eri
    (4.5992, -30.729, 3.85, "orange"), # upsilon4 Eri
]

ORION_LINES = [
    ("betelgeuse", "bellatrix", True),
    ("betelgeuse", "alnitak", True),
    ("bellatrix", "mintaka", False),
    ("alnitak", "alnilam", False),
    ("alnilam", "mintaka", False),
    ("alnitak", "saiph", False),
    ("mintaka", "rigel", False),
    ("saiph", "rigel", False),
]


def run(cmd: list) -> None:
    sp.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 0.5 - 0.5 * math.cos(math.pi * x)


@lru_cache(None)
def cg_font(n: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD, n)


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        if w.getframerate() != SR or w.getnchannels() != 2 or w.getsampwidth() != 2:
            raise RuntimeError(f"expected 48 kHz stereo s16: {p}")
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


def font_for(line_h: float, ratio: float = 0.86) -> ImageFont.FreeTypeFont:
    size = 10
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f = ImageFont.truetype(FONT_BLACK, size + 1)
        b = probe.textbbox((0, 0), "Hg", font=f)
        if b[3] - b[1] > line_h * ratio:
            return ImageFont.truetype(FONT_BLACK, size)
        size += 1


def centred(draw, y, text, font, fill, stroke=6) -> list[int]:
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    alpha = fill[3] if len(fill) == 4 else 255
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(10, 18, 32, alpha))
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


def silence(n: int) -> np.ndarray:
    return np.zeros((max(0, n), 2), dtype=np.float32)


def span_parts(a: float, b: float, tighten: bool) -> list[tuple[float, float]]:
    ws = [w for w in ALL_WORDS if w["end"] > a + 0.01 and w["start"] < b - 0.01]
    if not ws:
        return [(a, b)]
    if not tighten:
        return [(ws[0]["start"], ws[-1]["end"])]
    segs = []
    s = ws[0]["start"]
    prev = ws[0]["end"]
    for w in ws[1:]:
        if w["start"] - prev > 0.35:
            segs.append((s, prev))
            s = w["start"]
        prev = w["end"]
    segs.append((s, prev))
    return segs


def build_voice(sentences: list[dict], lead: float, gap: float) -> tuple[list[dict], list[dict], float]:
    slices = []
    words = []
    local = lead
    for si, sent in enumerate(sentences):
        parts = span_parts(sent["a"], sent["b"], sent.get("tighten", False))
        for pi, (a, b) in enumerate(parts):
            if pi:
                local += gap
            dur_s = b - a
            slices.append({"a": a, "b": b, "local": local})
            for w in ALL_WORDS:
                if w["end"] <= a + 0.005 or w["start"] >= b - 0.005:
                    continue
                words.append({
                    "text": w["text"],
                    "w": w["text"],
                    "s": round(w["start"] - a + local, 3),
                    "e": round(min(b, w["end"]) - a + local, 3),
                    "start": round(w["start"] - a + local, 3),
                    "end": round(min(b, w["end"]) - a + local, 3),
                })
            local = round(local + dur_s, 3)
        if si < len(sentences) - 1:
            local = round(local + gap, 3)
    return slices, words, local


def word_gaps(words: list[dict]) -> list[float]:
    gaps = []
    for a, b in zip(words, words[1:]):
        if b["s"] - a["e"] >= 0.04:
            gaps.append(round((a["e"] + b["s"]) / 2, 3))
    return gaps


def nearest_gap(target: float, gaps: list[float], lo: float, hi: float) -> float | None:
    cands = [g for g in gaps if lo < g < hi]
    if not cands:
        return None
    return min(cands, key=lambda g: abs(g - target))


def clips_word(t: float, words: list[dict]) -> bool:
    return any(w["s"] < t - 0.02 and w["e"] > t + 0.02 for w in words)


def _shift_box(box):
    if not box:
        return box
    x0, y0, x1, y1 = box
    return (min(0.85, x0 + 0.08), y0, min(1.0, x1 + 0.08), y1)


def layout_plates(plates: list[dict], words: list[dict], last: float, plan_total: float) -> list[dict]:
    total = round(last + VO_TAIL + END_CARD, 2)
    end_in = round(last + VO_TAIL, 2)
    plan_body = plan_total - END_CARD
    body = end_in
    gaps = word_gaps(words)
    internal = [p for p in plates if not p.get("end_card")]
    targets = [p["prefer_out"] / plan_body * body for p in internal[:-1]]
    bounds = [0.0]
    n = len(targets)
    for i, target in enumerate(targets):
        lo = bounds[-1] + 2.08
        hi = end_in - 2.08 * (n - i)
        g = None
        locked = internal[i].get("lock_out")
        if locked is not None:
            g = round(float(locked), 2)
            if g <= bounds[-1] + 1.55 or clips_word(g, words):
                raise SystemExit(f"{internal[i]['row']} lock {g:.2f}s is not a clean cut after {bounds[-1]:.2f}s")
        elif i == 0:
            sent = [round(w["e"] + 0.03, 2) for w in words if re.search(r"[.!?]$", w["w"]) and 2.15 <= w["e"] <= 2.97]
            if sent:
                g = sent[0]
            lo = max(lo, 2.15)
            hi = min(max(hi, lo + 0.04), 2.98)
        hi = max(hi, lo + 0.04)
        if g is None:
            g = nearest_gap(target, gaps, lo, hi)
        if g is None:
            g = nearest_gap(target, gaps, bounds[-1] + 0.35, min(end_in - 0.35, 2.98 if i == 0 else end_in))
        if g is None or clips_word(g, words):
            raise SystemExit(f"no clean cut near {target:.2f}s (window {lo:.2f}-{hi:.2f})")
        if g - bounds[-1] > 4.02:
            earlier = nearest_gap(bounds[-1] + 3.1, gaps, bounds[-1] + 2.08, g - 2.08)
            if earlier and not clips_word(earlier, words):
                bounds.append(round(earlier, 2))
        bounds.append(round(g, 2))
    bounds.append(end_in)
    bounds.append(total)
    guard = 0
    while guard < 4:
        guard += 1
        split = False
        rebuilt = [bounds[0]]
        for a, b in zip(bounds, bounds[1:]):
            if b <= end_in + 0.001 and (b - a) > 4.02:
                mid = nearest_gap((a + b) / 2, gaps, a + 2.08, b - 2.05)
                if mid and not clips_word(mid, words):
                    rebuilt.append(round(mid, 2))
                    split = True
            rebuilt.append(b)
        bounds = rebuilt
        if not split:
            break
    while len(bounds) > len(plates) + 1 and bounds[-3] > end_in - 1.7:
        bounds.pop(-3)
    if len(bounds) - 1 != len(plates):
        while len(bounds) - 1 > len(plates):
            src = plates[-2]
            extra = {
                **src,
                "row": src["row"] + "b",
                "box": _shift_box(src.get("box")),
                "cx": (src.get("cx") or 400) + 240,
            }
            if src.get("src"):
                extra["file"] = src.get("file") or src["src"]
                stem, dot, ext = src["src"].rpartition(".")
                extra["src"] = f"{stem}_b.{ext}" if dot else src["src"] + "_b"
                extra["offset"] = round(src.get("offset", 0.0) + 2.6, 2)
            plates.insert(-1, extra)
        while len(bounds) - 1 < len(plates):
            plates.pop(-2)
    out = []
    for i, p in enumerate(plates):
        q = dict(p)
        q["in"] = bounds[i]
        q["out"] = bounds[i + 1]
        if q["out"] - q["in"] > 6.01:
            raise SystemExit(f"{q['row']} holds {q['out'] - q['in']:.2f}s")
        for edge in (q["in"], q["out"]):
            if 0.05 < edge < last - 0.02 and clips_word(edge, words):
                raise SystemExit(f"{q['row']} clips a word at {edge:.2f}s")
        out.append(q)
    if out[1]["in"] > 3.0:
        raise SystemExit(f"first cut at {out[1]['in']:.2f}s")
    return out


def smooth_grade(im: Image.Image) -> Image.Image:
    """Continuous navy shadow lift with zero step threshold (avoids contour banding)."""
    arr = np.asarray(im, dtype=np.float32)
    # Continuous affine floor: 0 -> (20, 32, 56), 255 -> 255
    floors = np.array([20.0, 32.0, 56.0], dtype=np.float32)
    arr = floors + arr * ((255.0 - floors) / 255.0)
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    return im


def fit_fullbleed(src: Path, box: tuple[float, float, float, float], max_up: float = 1.95) -> tuple[Image.Image, float]:
    """Crop and scale strictly full-bleed 1080x1920 with zero GaussianBlur fallback."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    x0, y0 = int(w * box[0]), int(h * box[1])
    x1, y1 = int(w * box[2]), int(h * box[3])
    im = im.crop((x0, y0, max(x0 + 2, x1), max(y0 + 2, y1)))
    im = smooth_grade(im)
    cover = max(W / im.width, H / im.height)
    if cover > max_up + 0.02:
        raise RuntimeError(f"fit_fullbleed upscale {cover:.3f} exceeds max_up {max_up} on {src.name} {box}")
    sharp = im.resize((max(W, round(im.width * cover)), max(H, round(im.height * cover))), Image.Resampling.LANCZOS)
    x = (sharp.width - W) // 2
    y = (sharp.height - H) // 2
    return sharp.crop((x, y, x + W, y + H)), round(cover, 3)


def pipe_frames(frames: list[Image.Image], dest: Path) -> None:
    proc = sp.Popen(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-video_track_timescale", "30000", str(dest)],
        stdin=sp.PIPE,
    )
    assert proc.stdin is not None
    for im in frames:
        proc.stdin.write(im.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"frame encode failed: {dest}")


@lru_cache(maxsize=1)
def _load_gemini_night() -> Image.Image:
    return Image.open(HDIR / "gemini_night.jpg").convert("RGB")


def render_orion_sphere_open(dur_s: float, dest: Path, save_f0: Path | None = None) -> float:
    """Wed 9 Dec opening: real NOIRLab Gemini North Orion night-sky starfield + ESO VLT SPHERE dimming."""
    frames_n = max(1, round(dur_s * FPS))
    bg_src = _load_gemini_night()
    bg_crop = bg_src.crop((4600, 1600, 4600 + 2400, 1600 + 4266))
    cw0, ch0 = bg_crop.size
    bg_crop = ImageEnhance.Contrast(ImageEnhance.Color(bg_crop).enhance(1.22)).enhance(1.18)
    bw, bh = 1620, 2880
    bg_big = bg_crop.resize((bw, bh), Image.Resampling.LANCZOS)
    up = round(max(bw / cw0, bh / ch0), 3)

    s_jan = Image.open(HDIR / "sphere_jan.jpg").convert("RGB")
    s_dec = Image.open(HDIR / "sphere_dec.jpg").convert("RGB")
    disk_sz = 760
    yy, xx = np.mgrid[:disk_sz, :disk_sz]
    rr = np.sqrt((xx - disk_sz / 2) ** 2 + (yy - disk_sz / 2) ** 2) / (disk_sz / 2)
    disk_alpha = np.clip((0.74 - rr) / 0.24, 0.0, 1.0) ** 1.4

    frames = []
    for n in range(frames_n):
        t = n / FPS
        tn = n / max(1, frames_n - 1)
        cw = 1320 - 240 * tn
        ch = 2346 - 426 * tn
        cx = (bw - cw) * (0.08 + 0.84 * tn)
        cy = (bh - ch) * (0.88 - 0.76 * tn)
        frame_bg = bg_big.resize((W, H), Image.Resampling.BICUBIC, box=(cx, cy, cx + cw, cy + ch))
        arr = np.asarray(frame_bg, dtype=np.float32)

        dim_mix = np.clip((t - 0.35) / 1.85, 0.0, 1.0)
        pad = 0.14 - 0.04 * tn
        w0, h0 = s_jan.size
        box_s = (int(w0 * pad), int(h0 * pad), int(w0 * (1 - pad)), int(h0 * (1 - pad)))
        j_im = np.asarray(s_jan.crop(box_s).resize((disk_sz, disk_sz), Image.Resampling.LANCZOS), dtype=np.float32)
        d_im = np.asarray(s_dec.crop(box_s).resize((disk_sz, disk_sz), Image.Resampling.LANCZOS), dtype=np.float32)
        star_rgb = j_im * (1.0 - dim_mix) + d_im * dim_mix
        star_lum = star_rgb.max(axis=2) / 255.0
        al = np.clip(disk_alpha * np.clip((star_lum - 0.20) / 0.35, 0.0, 1.0), 0.0, 1.0)[..., None]

        x0 = (W - disk_sz) // 2 + int(round(36 * math.sin(tn * math.pi)))
        y0 = 960 - disk_sz // 2
        patch = arr[y0:y0 + disk_sz, x0:x0 + disk_sz]
        arr[y0:y0 + disk_sz, x0:x0 + disk_sz] = np.clip(patch * (1.0 - al) + star_rgb * 1.10 * al, 0, 255)
        arr[..., 0] = np.clip(arr[..., 0] + 8, 20, 255)
        arr[..., 1] = np.clip(arr[..., 1] + 14, 28, 255)
        arr[..., 2] = np.clip(arr[..., 2] + 30, 48, 255)

        frame = Image.fromarray(arr.astype(np.uint8))
        if n == 0 and save_f0 is not None:
            frame.save(save_f0)
        frames.append(frame)
    pipe_frames(frames, dest)
    return up


def render_starfield_star_composite(
    fg_src: Path,
    dur_s: float,
    dest: Path,
    sky_origin: tuple[int, int],
    disk_sz: int = 800,
    drive: bool = False,
    bg_gain: float = 1.0,
    shimmer: bool = False,
    save_f0: Path | None = None,
) -> float:
    """Composite a square ESO telescope plate (sphere_jan, sphere_dec, visir_flames) cleanly over a
    distinct full-bleed 9:16 starfield crop of gemini_night.jpg (20736x8549, 0.675x downscale).
    Zero GaussianBlur, zero flat bands, crisp real stars across top, middle, and bottom."""
    frames_n = max(1, round(dur_s * FPS))
    bg_src = _load_gemini_night()
    sx0, sy0 = sky_origin
    sx1 = min(bg_src.width, sx0 + 2400)
    sy1 = min(bg_src.height, sy0 + 4266)
    bg_crop = bg_src.crop((sx0, sy0, sx1, sy1))
    cw0, ch0 = bg_crop.size
    bg_crop = ImageEnhance.Contrast(ImageEnhance.Color(bg_crop).enhance(1.24)).enhance(1.20)
    if abs(bg_gain - 1.0) > 1e-3:
        bg_crop = ImageEnhance.Brightness(bg_crop).enhance(bg_gain)
    bw, bh = 1620, 2880
    bg_big = bg_crop.resize((bw, bh), Image.Resampling.LANCZOS)

    fg_raw = Image.open(fg_src).convert("RGB")
    fw, fh = fg_raw.size
    fg_crop = fg_raw.crop((int(fw * 0.06), int(fh * 0.06), int(fw * 0.94), int(fh * 0.94)))
    up_fg = disk_sz / max(1, min(fg_crop.width, fg_crop.height))
    up = round(max(bw / cw0, bh / ch0, min(1.85, up_fg)), 3)

    frames = []
    for n in range(frames_n):
        tn = n / max(1, frames_n - 1)
        t_s = n / FPS
        if shimmer:
            cw = 1520 - 430 * tn
            ch = 2702 - 764 * tn
            cx = (bw - cw) * (0.95 - 0.90 * tn)
            cy = (bh - ch) * (0.08 + 0.84 * tn)
        elif drive:
            cw = 1420 - 300 * tn
            ch = 2524 - 533 * tn
            cx = (bw - cw) * (0.90 - 0.80 * tn)
            cy = (bh - ch) * (0.14 + 0.72 * tn)
        else:
            cw = 1360 - 180 * tn
            ch = 2418 - 320 * tn
            cx = (bw - cw) * (0.18 + 0.64 * tn)
            cy = (bh - ch) * (0.22 + 0.56 * tn)
        frame_bg = bg_big.resize((W, H), Image.Resampling.BICUBIC, box=(cx, cy, cx + cw, cy + ch))
        arr = np.asarray(frame_bg, dtype=np.float32)

        cur_sz = int(round(disk_sz * (0.92 + (0.20 if shimmer else (0.16 if drive else 0.09)) * tn)))
        cur_sz = min(W - 40, max(320, cur_sz))
        fg_im = np.asarray(fg_crop.resize((cur_sz, cur_sz), Image.Resampling.LANCZOS), dtype=np.float32)
        yy, xx = np.mgrid[:cur_sz, :cur_sz]
        dx = xx - cur_sz / 2
        dy = yy - cur_sz / 2
        rr = np.sqrt(dx ** 2 + dy ** 2) / (cur_sz / 2)
        radial = np.clip((0.88 - rr) / 0.28, 0.0, 1.0) ** 1.35
        lum = fg_im.max(axis=2) / 255.0
        if shimmer:
            ang = np.arctan2(dy, dx)
            wave_f = np.sin(7.0 * ang + 15.0 * rr - 14.5 * t_s) * np.cos(4.0 * ang - 11.0 * rr + 10.5 * t_s)
            plume_env = np.clip((lum - 0.16) / 0.35, 0.0, 1.0) * np.clip((rr - 0.14) / 0.10, 0.0, 1.0) * np.clip((0.80 - rr) / 0.22, 0.0, 1.0)
            fg_im = np.clip(
                fg_im + plume_env[..., None] * wave_f[..., None] * np.array([150.0, 66.0, 18.0], dtype=np.float32),
                0.0,
                255.0,
            )
            core_mask = np.clip((0.12 - rr) / 0.03, 0.0, 1.0)
            al = np.clip(np.maximum(core_mask, radial * np.clip((lum - 0.09) / 0.24, 0.0, 1.0)), 0.0, 1.0)[..., None]
        else:
            al = np.clip(radial * np.clip((lum - 0.09) / 0.24, 0.0, 1.0), 0.0, 1.0)[..., None]

        x0 = (W - cur_sz) // 2 + int(round((54 if shimmer else (44 if drive else 20)) * math.sin(tn * math.pi)))
        y0 = (980 if drive else 960) - cur_sz // 2
        patch = arr[y0:y0 + cur_sz, x0:x0 + cur_sz]
        if shimmer:
            core_w = np.clip((0.12 - rr) / 0.03, 0.0, 1.0)[..., None]
            fg_blend = np.maximum(patch * (0.55 * (1.0 - core_w)), fg_im * 1.12)
            blended = patch * (1.0 - al) + fg_blend * al
        else:
            # Screen/additive-aware blend so fiery plume illuminates starfield without dark square halo
            blended = patch * (1.0 - al) + np.maximum(patch * 0.55, fg_im * 1.12) * al
        arr[y0:y0 + cur_sz, x0:x0 + cur_sz] = np.clip(blended, 0, 255)

        floors = np.array([20.0, 30.0, 52.0], dtype=np.float32)
        arr = floors + arr * ((255.0 - floors) / 255.0)
        frame = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        if n == 0 and save_f0 is not None:
            frame.save(save_f0)
        frames.append(frame)
    pipe_frames(frames, dest)
    return up


def render_still_fullbleed(
    src: Path,
    dur_s: float,
    dest: Path,
    box: tuple[float, float, float, float],
    rings: bool = False,
    drive: bool = False,
    save_f0: Path | None = None,
) -> float:
    """Full-bleed 9:16 still move with zero GaussianBlur and smooth shadow lift."""
    frames_n = max(1, round(dur_s * FPS))
    room = 1.18 if drive else 1.025
    base, fit = fit_fullbleed(src, box, max_up=1.95)
    big = base.resize((round(W * room), round(H * room)), Image.Resampling.BICUBIC)
    bw, bh = big.size
    frames = []
    for n in range(frames_n):
        t = n / max(1, frames_n - 1)
        z = 1.0 + (room - 1.0) * t
        cw, ch = bw / z, bh / z
        if drive:
            drift = (t - 0.5) * 0.09
            cx = min(max(0.0, (bw - cw) / 2 + drift * bw), bw - cw)
            cy = min(max(0.0, (bh - ch) / 2), bh - ch)
        else:
            cx = (bw - cw) / 2.0
            cy = (bh - ch) / 2.0
        frame = big.resize((W, H), Image.Resampling.BICUBIC, box=(cx, cy, cx + cw, cy + ch))
        if rings:
            arr = np.asarray(frame, dtype=np.float32)
            yy, xx = np.mgrid[:H, :W]
            rad = 60 + (n / FPS) * 520
            dist = np.sqrt((xx - 540) ** 2 + ((yy - 980) * 0.7) ** 2)
            ring = np.exp(-((dist - rad) / 22) ** 2)
            arr += (115 * ring)[..., None] * np.array([1.0, 0.78, 0.4])
            frame = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        if n == 0 and save_f0 is not None:
            frame.save(save_f0)
        frames.append(frame)
    pipe_frames(frames, dest)
    return round(min(1.98, fit * (1.02 if not drive else 1.0)), 3)


def render_hold(src_png: Path, dur_s: float, dest: Path) -> float:
    im = Image.open(src_png).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.Resampling.LANCZOS)
    pipe_frames([im] * max(1, round(dur_s * FPS)), dest)
    return 1.0


def render_video_fullbleed(src: Path, offset: float, dur_s: float, dest: Path, mode: str, cx: int = 656) -> float:
    """Strictly full-bleed 9:16 real video crop (mode='crop' or 'sky'). Never band-padded."""
    if mode == "sky":
        up = round(max(W / 700, H / 835), 3)
        vf = (
            f"fps={FPS},crop=700:835:{cx}:0,scale={W}:{H}:flags=lanczos:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},eq=brightness=0.08:gamma=1.2:contrast=1.12:saturation=1.02,format=rgb24,"
            "geq=r='r(X,Y)':g='min(g(X,Y),max(r(X,Y),b(X,Y))+12)':b='b(X,Y)',format=yuv420p,setsar=1"
        )
    else:
        up = round(max(W / 608, H / 1080), 3)
        vf = (
            f"fps={FPS},crop=608:1080:{cx}:0,scale={W}:{H}:flags=lanczos,"
            f"eq=brightness=0.12:gamma=1.4:contrast=1.25:saturation=1.3,setsar=1"
        )
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{offset:.3f}", "-t", f"{dur_s:.3f}", "-i", str(src),
        "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-r", str(FPS),
        "-video_track_timescale", "30000", str(dest),
    ])
    return up


def render_neutrinos_916(dur_s: float, dest: Path) -> float:
    """Full-height 1080x1920 code graphic: SDO Sun + polar telemetry rings + vertical neutrino burst."""
    y, x = np.mgrid[:H, :W]
    glow = np.exp(-(((x - 540) / 460) ** 2 + ((y - 960) / 760) ** 2))
    mw = np.exp(-((((x - 540) * 0.72 + (y - 960) * 0.42) / 380.0) ** 2))
    base_arr = np.stack([
        22 + 34 * glow + 16 * mw,
        36 + 46 * glow + 24 * mw,
        66 + 68 * glow + 38 * mw,
    ], axis=-1)
    bg = Image.fromarray(np.clip(base_arr, 0, 255).astype(np.uint8)).convert("RGBA")
    ld = ImageDraw.Draw(bg)
    rng_bg = np.random.default_rng(29014)
    for sx, sy, rad in rng_bg.uniform([24, 30, 1.3], [W - 24, H - 30, 2.8], (520, 3)):
        ld.ellipse((sx - rad, sy - rad, sx + rad, sy + rad), fill=(214, 228, 248, 175))
    for rx, ry in ((240, 340), (380, 560), (500, 780)):
        ld.ellipse((540 - rx, 960 - ry, 540 + rx, 960 + ry), outline=(150, 188, 228, 76), width=2)
    bg_rgb = bg.convert("RGB")

    sun = Image.open(HDIR / "sdo_hmi_continuum.jpg").convert("RGB")
    sun = ImageOps.fit(sun, (290, 290), method=Image.Resampling.LANCZOS)
    mask = Image.new("L", (290, 290))
    ImageDraw.Draw(mask).ellipse((2, 2, 287, 287), fill=255)
    sun.putalpha(mask)

    rng = np.random.default_rng(7)
    dots = np.column_stack([rng.uniform(0, 2 * math.pi, 110), rng.uniform(0.14, 1.0, 110)])
    frames_n = max(1, round(dur_s * FPS))
    frames = []
    for n in range(frames_n):
        t = n / FPS
        im = bg_rgb.copy()
        im.paste(sun, (W // 2 - 145, 960 - 145), sun)
        d = ImageDraw.Draw(im, "RGBA")
        grow = 65 + t * 340
        for ang, phase in dots:
            r = grow * phase
            px = 540 + math.cos(ang) * r * 0.92
            py = 960 + math.sin(ang) * r * 1.48
            if -12 <= px <= W + 12 and -12 <= py <= H + 12:
                rad = 3.2 + 2.4 * phase
                d.ellipse((px - rad, py - rad, px + rad, py + rad), fill=(192, 234, 255, 220))
        frames.append(im.convert("RGB"))
    pipe_frames(frames, dest)
    return 1.0


class UprightCodeRenderer:
    """Native 1080x1920 (9:16) rebuild of 029's `build_code_graphics_v01.py` plates."""

    def __init__(self) -> None:
        self.sun = Image.open(CG_ASSETS / "sun_sdo.jpg").convert("RGB").crop((448, 212, 3648, 3412))
        self.earth = Image.open(CG_ASSETS / "earth.jpg").convert("RGB")
        self.mars = Image.open(CG_ASSETS / "mars.jpg").convert("RGB")
        self.bodies: dict = {}
        self.blobs: dict = {}

        rng = np.random.default_rng(1054)
        y, x = np.mgrid[:H, :W]
        rad = np.sqrt(((x - 540) / 520) ** 2 + ((y - 960) / 860) ** 2)
        g1 = np.exp(-rad ** 2 * 1.25)
        band_d = ((x - 540) * 0.78 + (y - 960) * 0.62) / 310.0
        band_l = ((x - 540) * 0.62 - (y - 960) * 0.78) / 960.0
        mw = np.exp(-band_d ** 2) * np.exp(-band_l ** 2 * 0.55)
        dust = np.exp(-((band_d - 0.18) / 0.32) ** 2) * np.exp(-band_l ** 2 * 0.9)
        g_top = np.exp(-(((x - 360) / 380) ** 2 + ((y - 340) / 340) ** 2))
        g_bot = np.exp(-(((x - 740) / 390) ** 2 + ((y - 1580) / 360) ** 2))
        glow = np.clip(0.62 * g1 + 0.46 * mw - 0.18 * dust + 0.34 * g_top + 0.34 * g_bot, 0, 1.35)
        base = np.stack([18 + 60 * glow, 28 + 80 * glow, 46 + 108 * glow], axis=-1)
        bg = Image.fromarray(np.uint8(np.clip(base, 0, 255)))

        # Chart / telemetry background with full-height polar compass ellipses (y=110..1810) + stars
        chart_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(chart_layer)
        for rx, ry in ((190, 270), (310, 460), (430, 650), (520, 830)):
            ld.ellipse((540 - rx, 960 - ry, 540 + rx, 960 + ry), outline=(165, 195, 230, 82), width=2)
            for deg in range(0, 360, 6):
                ang = math.radians(deg)
                t_len = 10 if deg % 18 == 0 else 5
                ld.line((
                    540 + (rx - t_len) * math.cos(ang), 960 + (ry - t_len) * math.sin(ang),
                    540 + (rx + t_len) * math.cos(ang), 960 + (ry + t_len) * math.sin(ang),
                ), fill=(185, 212, 242, 105), width=2)
        srng = np.random.default_rng(10540)
        for n_stars, r_px, alpha in [(460, 2.1, 132), (210, 3.1, 158), (65, 4.3, 180)]:
            for sx, sy in srng.uniform([32, 48], [W - 32, H - 48], (n_stars, 2)):
                ld.ellipse((sx - r_px, sy - r_px, sx + r_px, sy + r_px), fill=(215, 232, 252, alpha))
        self.chart_bg = Image.alpha_composite(bg.convert("RGBA"), chart_layer).convert("RGB")

        # Sky background: full-height dashed celestial RA/Dec reticle + crisp starfield + compass ticks
        sky_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sld = ImageDraw.Draw(sky_layer)
        for ra_h in (4.75, 5.15, 5.55, 5.95, 6.35):
            gx, _ = self.orion_px(ra_h, 0.0)
            if 40 <= gx <= W - 40:
                for yy in range(70, H - 70, 28):
                    sld.line((gx, yy, gx, min(H - 70, yy + 14)), fill=(120, 158, 198, 56), width=1)
        for dec_d in (-35, -25, -15, -5, 5, 15, 25, 35):
            _, gy = self.orion_px(5.56, dec_d)
            if 70 <= gy <= H - 70:
                for xx in range(54, W - 54, 28):
                    sld.line((xx, gy, min(W - 54, xx + 14), gy), fill=(120, 158, 198, 56), width=1)
        for crx, cry in ((460, 740), (340, 540), (510, 840)):
            sld.ellipse((540 - crx, 960 - cry, 540 + crx, 960 + cry), outline=(160, 194, 232, 76), width=2)
            for deg in range(0, 360, 6):
                ang = math.radians(deg)
                t_len = 9 if deg % 18 == 0 else 4
                sld.line((
                    540 + (crx - t_len) * math.cos(ang), 960 + (cry - t_len) * math.sin(ang),
                    540 + (crx + t_len) * math.cos(ang), 960 + (cry + t_len) * math.sin(ang),
                ), fill=(182, 210, 242, 98), width=2)
        sky_srng = np.random.default_rng(29011)
        for n_stars, r_px, alpha in [(480, 2.2, 138), (220, 3.2, 165), (75, 4.4, 188)]:
            for sx, sy in sky_srng.uniform([28, 36], [W - 28, H - 36], (n_stars, 2)):
                sld.ellipse((sx - r_px, sy - r_px, sx + r_px, sy + r_px), fill=(215, 232, 252, alpha))
        self.sky_bg = Image.alpha_composite(bg.convert("RGBA"), sky_layer).convert("RGB")

        self.field = rng.uniform([18, 24], [W - 18, H - 24], (180, 2))
        self.belt = np.stack([rng.uniform(2.2, 3.3, 280), rng.uniform(0, 2 * math.pi, 280)], axis=1)
        self.orion = {n: (*self.orion_px(ra, dec), kind) for n, (ra, dec, kind) in ORION.items()}
        self.catalog_field = [(*self.orion_px(ra, dec), mag, kind) for ra, dec, mag, kind in ORION_CATALOG_FIELD_916]

    @staticmethod
    def orion_px(ra: float, dec: float, cy: float = 1020.0, scale: float = 21.5) -> tuple[float, float]:
        x = -(ra - 5.56) * 15.0 * scale
        y = (dec - (-1.1)) * scale
        return 540.0 + x, cy - y

    def draw_text(self, im: Image.Image, s: str, xy: tuple[float, float], size: int = 50, color=CG_WHITE, alpha: float = 1.0, anchor: str = "mm") -> None:
        if alpha <= 0.02 or not s:
            return
        for sz in (size, max(34, size - 8), max(28, size - 16)):
            layer = Image.new("RGBA", im.size)
            d = ImageDraw.Draw(layer)
            box = d.textbbox(xy, s, font=cg_font(sz), anchor=anchor, stroke_width=3)
            if 48 <= box[0] and box[2] <= W - 48 and 60 <= box[1] and box[3] <= H - 70:
                d.text(
                    xy, s, font=cg_font(sz),
                    fill=(*color, int(255 * alpha)),
                    anchor=anchor, stroke_width=3,
                    stroke_fill=(10, 18, 32, int(225 * alpha)),
                )
                im.paste(layer, (0, 0), layer)
                return

    def base(self, t: float, sky: bool = False) -> Image.Image:
        if sky:
            im = self.sky_bg.copy()
            d = ImageDraw.Draw(im)
            shift_y = (t * 10.0) % H
            for idx, (fx, fy) in enumerate(self.field[:95]):
                yy = (fy + shift_y * (0.4 if idx % 2 else 0.2)) % (H - 40) + 20
                d.ellipse((fx, yy, fx + 2.0, yy + 2.0), fill=(192, 212, 236))
            return im
        im = self.chart_bg.copy()
        d = ImageDraw.Draw(im)
        shift = (t * 16.0) % (W - 36)
        for fx, fy in self.field:
            xx = 18 + (fx - 18 + shift) % (W - 36)
            d.ellipse((xx, fy, xx + 2.2, fy + 2.2), fill=(196, 210, 228))
        return im

    def sun_dot(self, im: Image.Image, xy: tuple[float, float], r: int = 8) -> None:
        x, y = xy
        glow = Image.new("RGBA", im.size)
        gd = ImageDraw.Draw(glow)
        gd.ellipse((x - r * 3, y - r * 3, x + r * 3, y + r * 3), fill=(255, 232, 170, 85))
        gd.ellipse((x - r, y - r, x + r, y + r), fill=(255, 248, 220, 255))
        im.paste(Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB"))

    def body(self, im: Image.Image, xy: tuple[float, float], r: int, kind: str = "earth") -> None:
        r = max(4, int(r))
        key = (r, kind)
        if key not in self.bodies:
            src = {"earth": self.earth, "mars": self.mars}.get(kind, self.sun)
            sprite = ImageOps.fit(src, (2 * r, 2 * r), method=Image.Resampling.LANCZOS)
            mask = Image.new("L", (2 * r, 2 * r))
            ImageDraw.Draw(mask).ellipse((1, 1, 2 * r - 2, 2 * r - 2), fill=255)
            sprite.putalpha(mask)
            self.bodies[key] = sprite
        im.paste(self.bodies[key], (int(xy[0] - r), int(xy[1] - r)), self.bodies[key])

    def sky(
        self,
        im: Image.Image,
        t: float,
        flare: float = 0.0,
        fade: float = 0.0,
        zoom: float = 1.0,
        lines_prog: float = 1.0,
        label_betelgeuse: bool = True,
        label_constellation: bool = False,
    ) -> None:
        fx, fy = 540.0, 1020.0

        def Z(px: float, py: float) -> tuple[float, float]:
            return fx + (px - fx) * zoom, fy + (py - fy) * zoom

        d = ImageDraw.Draw(im)
        for sx, sy, mag, kind in self.catalog_field:
            px, py = Z(sx, sy)
            if not (24 <= px <= W - 24 and 36 <= py <= H - 36):
                continue
            r_s = max(2.2, min(7.2, 6.2 - 0.78 * mag))
            col = (195, 220, 255) if kind == "blue" else ((255, 205, 165) if kind == "orange" else (232, 240, 252))
            d.ellipse((px - r_s, py - r_s, px + r_s, py + r_s), fill=col)

        if lines_prog > 0.01:
            line_layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ld = ImageDraw.Draw(line_layer)
            n_seg = len(ORION_LINES)
            for idx, (s1, s2, is_shoulder) in enumerate(ORION_LINES):
                seg_u = max(0.0, min(1.0, lines_prog * n_seg - idx))
                if seg_u <= 0.01:
                    continue
                x1, y1 = Z(*self.orion[s1][:2])
                x2, y2 = Z(*self.orion[s2][:2])
                xe = x1 + (x2 - x1) * ease(seg_u)
                ye = y1 + (y2 - y1) * ease(seg_u)
                if is_shoulder and fade > 0.35:
                    dist = math.hypot(xe - x1, ye - y1)
                    steps = max(1, int(dist // 16))
                    for k in range(0, steps, 2):
                        u0 = k / steps
                        u1 = min(1.0, (k + 1.1) / steps)
                        ld.line(
                            (x1 + (xe - x1) * u0, y1 + (ye - y1) * u0,
                             x1 + (xe - x1) * u1, y1 + (ye - y1) * u1),
                            fill=(*CG_GOLD, 215), width=4,
                        )
                else:
                    col_line = (*CG_GOLD, 220) if is_shoulder else (*CG_ICE, 210)
                    ld.line((x1, y1, xe, ye), fill=col_line, width=4)
            im.paste(Image.alpha_composite(im.convert("RGBA"), line_layer).convert("RGB"))
            d = ImageDraw.Draw(im)

        star_glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sgd = ImageDraw.Draw(star_glow)
        for name, (sx, sy, kind) in self.orion.items():
            if name == "betelgeuse":
                continue
            px, py = Z(sx, sy)
            col = (210, 228, 255) if kind == "blue" else CG_WHITE
            r = 8 if kind == "belt" else (10 if name == "rigel" else 7)
            sgd.ellipse((px - r * 2.5, py - r * 2.5, px + r * 2.5, py + r * 2.5), fill=(*col, 72))
            sgd.ellipse((px - r, py - r, px + r, py + r), fill=(*col, 255))
        im.paste(Image.alpha_composite(im.convert("RGBA"), star_glow).convert("RGB"))
        d = ImageDraw.Draw(im)

        bx, by = Z(*self.orion["betelgeuse"][:2])
        a = max(0.0, 1.0 - fade)
        if a > 0.03:
            col = CG_WHITE if flare > 0.55 else CG_ORANGE
            radius = int(26 + 150 * flare * a)
            key = (radius, col)
            if key not in self.blobs:
                s = radius * 2
                yy, xx = np.mgrid[:s, :s]
                dist = np.sqrt((xx - radius) ** 2 + (yy - radius) ** 2) / max(1, radius)
                alpha = np.clip(1.0 - dist, 0.0, 1.0) ** 0.85
                arr = np.zeros((s, s, 4), np.uint8)
                arr[..., 0], arr[..., 1], arr[..., 2] = col
                arr[..., 3] = (alpha * 255).astype(np.uint8)
                self.blobs[key] = Image.fromarray(arr, "RGBA")
            glow = Image.new("RGBA", im.size)
            glow.paste(self.blobs[key], (int(bx - radius), int(by - radius)), self.blobs[key])
            if a < 0.98:
                glow.putalpha(glow.getchannel("A").point(lambda p: int(p * a)))
            im.paste(Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB"))
            d = ImageDraw.Draw(im)
            r_core = max(6, int(10 * a))
            d.ellipse((bx - r_core, by - r_core, bx + r_core, by + r_core), fill=CG_WHITE if flare > 0.4 else (255, 220, 185))

        if fade > 0.45:
            ring_r = 20
            for deg in range(0, 360, 30):
                d.arc((bx - ring_r, by - ring_r, bx + ring_r, by + ring_r), deg, deg + 16, fill=CG_GOLD, width=3)

        if label_betelgeuse:
            lx = max(250, int(bx - 30))
            ly = max(790, int(by - 6))
            d.line((bx - 16, by, lx + 8, ly), fill=CG_GOLD, width=3)
            self.draw_text(im, "Betelgeuse", (lx, ly), 38, CG_GOLD if fade > 0.4 else CG_ORANGE, 1.0, anchor="rm")

        if label_constellation and lines_prog > 0.35:
            a_lbl = ease((lines_prog - 0.35) / 0.45)
            blx, bly = Z(*self.orion["bellatrix"][:2])
            self.draw_text(im, "Bellatrix", (min(W - 70, int(blx + 22)), max(800, int(bly - 4))), 34, CG_ICE, a_lbl, anchor="lm")
            alx, aly = Z(*self.orion["alnitak"][:2])
            self.draw_text(im, "Orion's Belt", (max(240, int(alx - 22)), int(aly + 6)), 34, CG_ICE, a_lbl, anchor="rm")
            rgx, rgy = Z(*self.orion["rigel"][:2])
            self.draw_text(im, "Rigel", (min(W - 70, int(rgx + 22)), min(1245, int(rgy))), 34, CG_ICE, a_lbl, anchor="lm")
            spx, spy = Z(*self.orion["saiph"][:2])
            self.draw_text(im, "Saiph", (max(210, int(spx - 22)), min(1245, int(spy))), 34, CG_ICE, a_lbl, anchor="rm")

    def scale(self, im: Image.Image, t: float, s: float, cy: int = 1020, k: float = 82.0) -> None:
        cx = 540
        layer = Image.new("RGBA", im.size)
        ld = ImageDraw.Draw(layer)
        R = max(8.0, 3.55 * k * s)
        ld.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(*CG_ORANGE, 74))
        im.paste(Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB"))
        d = ImageDraw.Draw(im)
        for au, col in ((0.39, CG_DIM), (0.72, CG_DIM), (1.0, CG_ICE), (1.52, (214, 122, 86))):
            rr = au * k
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=col, width=2)
        for rad, ang in self.belt:
            px = cx + rad * k * math.cos(ang)
            py = cy + rad * k * math.sin(ang)
            d.ellipse((px - 1.5, py - 1.5, px + 1.5, py + 1.5), fill=CG_WHITE)
        d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=CG_ORANGE, width=4)
        ang = t * 0.55
        self.sun_dot(im, (cx, cy), r=8)
        self.body(im, (cx + k * math.cos(ang), cy + k * math.sin(ang)), 18, "earth")
        self.body(im, (cx + 1.52 * k * math.cos(ang * 0.6 + 1.0), cy + 1.52 * k * math.sin(ang * 0.6 + 1.0)), 15, "mars")

    def dip(self, im: Image.Image, t: float, pen: float, tight: bool = False) -> None:
        d = ImageDraw.Draw(im)
        cx_u = 0.687
        xs, ys = [], []
        trough = None
        # Vertical 9:16 light-curve window: x=100..980, y=420..1120 (completely clear of title/captions)
        for i in range(240):
            u = i / 239.0
            flux = 1.0 - 0.64 * math.exp(-((u - cx_u) / 0.11) ** 2)
            px = 108 + 864 * u
            py = 430 + 650 * (1.0 - (flux - 0.30) / 0.75)
            xs.append(px)
            ys.append(py)
            if trough is None or py > trough[1]:
                trough = (px, py)
        z = 1.38 if tight else 1.0
        fx, fy = trough if tight else (540.0, 760.0)

        def Z(px: float, py: float) -> tuple[float, float]:
            return fx + (px - fx) * z, fy + (py - fy) * z

        # Dashed baseline (avoids solid horizontal seam trigger)
        bx0, by0 = Z(108, ys[0])
        bx1, _ = Z(972, ys[0])
        bx0 = max(64.0, bx0)
        bx1 = min(float(W - 64), bx1)
        for xx in range(int(bx0), int(bx1), 26):
            d.line((xx, by0, min(bx1, xx + 14), by0), fill=CG_DIM, width=2)

        m = max(2, int(len(xs) * pen))
        pts = [
            (max(54.0, min(float(W - 54), Z(xs[i], ys[i])[0])),
             max(240.0, min(1220.0, Z(xs[i], ys[i])[1])))
            for i in range(m)
        ]
        if len(pts) >= 2:
            d.line(pts, fill=CG_ORANGE, width=6)
        px, py = pts[-1]
        pulse = 11 + 4 * math.sin(t * 5.0)
        glow = Image.new("RGBA", im.size)
        gd = ImageDraw.Draw(glow)
        gd.ellipse((px - pulse * 2.2, py - pulse * 2.2, px + pulse * 2.2, py + pulse * 2.2), fill=(*CG_ORANGE, 58))
        gd.ellipse((px - pulse, py - pulse, px + pulse, py + pulse), fill=(*CG_ORANGE, 235))
        im.paste(Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB"))

    def shells(self, im: Image.Image, t: float, grow: float) -> None:
        d = ImageDraw.Draw(im)
        cx, cy = 540, 820
        radii = [340, 278, 220, 168, 120]
        ang = (t * 28.0) % 360.0
        wedge = 70.0
        for r, col in zip(radii, SHELLS):
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        core = 30 + 88 * grow
        d.ellipse((cx - core, cy - core, cx + core, cy + core), fill=SHELLS[-1])
        box_r = radii[0]
        d.pieslice((cx - box_r, cy - box_r, cx + box_r, cy + box_r), ang - wedge / 2, ang + wedge / 2, fill=(20, 28, 44))
        for r, col in zip(radii, SHELLS):
            d.pieslice((cx - r, cy - r, cx + r, cy + r), ang - wedge / 2, ang + wedge / 2, fill=col)
        d.pieslice((cx - core, cy - core, cx + core, cy + core), ang - wedge / 2, ang + wedge / 2, fill=SHELLS[-1])

    def render_clip(self, mode: str, offset: float, dur_s: float, dest: Path) -> float:
        frames_n = max(1, round(dur_s * FPS))
        frames = []
        for n in range(frames_n):
            t = offset + (n / FPS)
            if mode == "wed_r15_dip":
                im = self.base(t, sky=False)
                self.dip(im, t, pen=min(1.0, 0.72 + 0.28 * ease((t - offset) / max(0.4, dur_s * 0.7))), tight=True)
                self.draw_text(im, "that point fades", (540, 270), 52, CG_GOLD, 1.0)
                self.draw_text(im, "CGI", (84, 1785), 26, CG_ICE, 0.9, anchor="lm")
            elif mode in ("fri_promise_a", "fri_promise_b", "fri_promise_c", "fri_promise_d"):
                sky_mode = t < 8.7
                im = self.base(t, sky=sky_mode)
                if t < 8.7:
                    self.sky(
                        im, t,
                        flare=ease((t - 4.2) / 2.4),
                        zoom=1.0 + 0.08 * ease(t / 8.0),
                        lines_prog=ease((t - 0.3) / 2.4),
                        label_betelgeuse=True,
                        label_constellation=(mode == "fri_promise_a"),
                    )
                    self.draw_text(im, "CGI", (84, 1785), 26, CG_ICE, 0.9, anchor="lm")
                elif t < 13.5:
                    self.scale(im, t, ease((t - 8.7) / 4.6) * 0.48, cy=1025, k=78.0)
                    if mode == "fri_promise_c":
                        self.draw_text(im, "kind of star", (540, 270), 52, CG_GOLD, 1.0)
                    self.draw_text(im, "NASA · CGI", (84, 1785), 26, CG_ICE, 0.9, anchor="lm")
                elif t < 18.3:
                    self.dip(im, t, ease((t - 13.5) / 4.2), tight=False)
                    if mode in ("fri_promise_c", "fri_promise_d"):
                        lbl = "in 2019" if t < 15.15 else "giant star actually dies"
                        self.draw_text(im, lbl, (540, 270), 48, CG_GOLD, 1.0)
                    self.draw_text(im, "CGI", (84, 1785), 26, CG_ICE, 0.9, anchor="lm")
                else:
                    u = (t - 18.3) / 4.6
                    self.shells(im, t, grow=ease(u))
                    self.draw_text(im, "giant star actually dies", (540, 270), 48, CG_GOLD, 1.0)
                    self.draw_text(im, "CGI", (84, 1785), 26, CG_ICE, 0.9, anchor="lm")
            elif mode == "mon_r25_orion":
                im = self.base(t, sky=True)
                flare = ease((t - 1.6) / 1.4)
                self.sky(
                    im, t,
                    flare=flare,
                    zoom=1.0 + 0.10 * ease((t - offset) / max(0.5, dur_s)),
                    lines_prog=ease((t - 0.15) / 1.8),
                    label_betelgeuse=True,
                    label_constellation=True,
                )
                # Note: TITLE_OUT is 14.00 s (local t ~ 2.04 s); show header cleanly in top third y=270
                lbl = "the light arrives" if (t - offset) < 1.85 else "Within days"
                self.draw_text(im, lbl, (540, 270), 50, CG_GOLD, 1.0)
                self.draw_text(im, "CGI", (84, 1785), 26, CG_ICE, 0.9, anchor="lm")
            elif mode == "mon_r27_orion":
                im = self.base(t, sky=True)
                fade = ease((t - 2.3) / 1.6)
                flare = 1.0 - ease((t - 2.0) / 1.6)
                self.sky(
                    im, t,
                    flare=flare,
                    fade=fade,
                    zoom=1.0 + 0.06 * ease((t - offset) / max(0.5, dur_s)),
                    lines_prog=1.0,
                    label_betelgeuse=True,
                    label_constellation=True,
                )
                self.draw_text(im, "bright for weeks", (540, 270), 50, CG_GOLD, 1.0)
                self.draw_text(im, "CGI", (84, 1785), 26, CG_ICE, 0.9, anchor="lm")
            else:
                raise ValueError(f"unknown upright code mode: {mode}")
            frames.append(im)
        pipe_frames(frames, dest)
        return 1.0


@lru_cache(maxsize=1)
def get_code_renderer() -> UprightCodeRenderer:
    return UprightCodeRenderer()


def make_hook(dest: Path, rows: list[tuple[str, tuple]]) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(H * 0.082 / 0.72)
    if f.size > 132:
        f = ImageFont.truetype(FONT_BLACK, 132)
    while max(d.textlength(t, font=f) for t, _ in rows) > W * 0.84:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = 220
    boxes = []
    for t, c in rows:
        boxes.append(centred(d, y, t, f, c, stroke=7))
        y += lh
    im.save(dest)
    return {"text": " / ".join(t for t, _ in rows), "font_px": f.size, "bboxes": boxes}


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
            raise SystemExit(f"title outside the 16:9 band: {r} {bb}")
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
            raise SystemExit(f"end card outside the 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed, "long_title": LONG_TITLE, "youtube_id": LONG_ID}


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
        raise SystemExit(f"teach pill outside the 16:9 band: {text} {bb}")
    im.save(dest)
    return bb


def make_cover(dest: Path, base_png: Path, rows: list[tuple[str, tuple]]) -> dict:
    """Full-bleed 9:16 cover built from the Short's full-bleed opening/key plate (zero blur)."""
    base = Image.open(base_png).convert("RGB")
    if base.size != (W, H):
        base = ImageOps.fit(base, (W, H), method=Image.Resampling.LANCZOS)
    im = ImageEnhance.Color(base).enhance(1.28)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    arr = np.asarray(im, dtype=np.float32)
    arr = np.clip(((arr / 255.0) ** 0.84) * 255.0 + 8, 0, 255)
    im = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(im)
    size = 72
    while size < 128:
        trial = ImageFont.truetype(FONT_BLACK, size + 2)
        if max(d.textlength(r, font=trial) for r, _ in rows) > W * 0.78:
            break
        size += 2
    f = ImageFont.truetype(FONT_BLACK, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = BAND_Y0 + (BAND_H - lh * len(rows)) // 2
    boxes = []
    for r, col in rows:
        bb = centred(d, y, r, f, col, stroke=8)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"cover text outside the 16:9 band: {r} {bb}")
        boxes.append(bb)
        y += lh
    im.save(dest, quality=94, subsampling=0)
    return {"file": str(dest), "rows": [r for r, _ in rows], "font_px": size, "bboxes": boxes}


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
        if end <= TITLE_IN or start >= TITLE_OUT:
            text = " ".join(x["w"] for x in c).rstrip(",.")
            if TITLE_IN < start < TITLE_OUT:
                continue
            if start < TITLE_OUT < end:
                start = TITLE_OUT
            if end - start >= 0.18 and start < vo_end:
                out.append({"text": text, "s": round(start, 2), "e": round(min(end, vo_end), 2)})
        else:
            text = " ".join(x["w"] for x in c).rstrip(",.")
            if start < TITLE_IN - 0.05 and TITLE_IN - start >= 0.18:
                out.append({"text": text, "s": round(start, 2), "e": round(min(end, TITLE_IN), 2)})
            if end > TITLE_OUT + 0.05:
                out.append({"text": text, "s": round(max(start, TITLE_OUT), 2), "e": round(min(end, vo_end), 2)})
    return [c for c in out if c["e"] - c["s"] >= 0.18]


def build_audio(work: Path, slices: list[dict], total: float, hits: list[tuple[str, float, float]]) -> dict:
    parts = []
    cursor = 0.0
    for i, sl in enumerate(slices):
        gap_n = int(round((sl["local"] - cursor) * SR))
        if gap_n > 0:
            parts.append(silence(gap_n))
        seg = sl["b"] - sl["a"]
        p = work / f"vo_{i}.wav"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(VO_WAV), "-ss", f"{sl['a']:.3f}", "-t", f"{seg:.3f}",
             "-ar", str(SR), "-ac", "2", str(p)])
        parts.append(read_wav(p))
        cursor = sl["local"] + seg
    vo = np.concatenate(parts, axis=0) if parts else silence(1)
    n = int(round(total * SR))
    if len(vo) < n:
        vo = np.concatenate([vo, silence(n - len(vo))], axis=0)
    vo = vo[:n]
    raw = work / "stem_vo_raw.wav"
    write_wav(vo, raw)
    vo_wav = work / "stem_vo.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(vo_wav)])
    vo_norm = read_wav(vo_wav)[:n]
    if len(vo_norm) < n:
        vo_norm = np.pad(vo_norm, ((0, n - len(vo_norm)), (0, 0)))
    write_wav(vo_norm, vo_wav)
    vo_m, vo_i = sfx_kit.ebur128(vo_wav)
    vo_m_arr = np.array(vo_m)
    speaking = (vo_m_arr > sfx_kit.SILENT) & (vo_m_arr >= vo_i - sfx_kit.SPEAKING_WITHIN)

    bed_raw = work / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{slices[0]['a']:.3f}", "-t", f"{total:.3f}", "-i", str(BED_MP3),
         "-af", f"afade=t=in:d=0.08,afade=t=out:st={max(0.1, total - 0.5):.3f}:d=0.5",
         "-ar", str(SR), "-ac", "2", str(bed_raw)])
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
    run(["ffmpeg", "-y", "-v", "error", "-i", str(mix_raw), "-af", "loudnorm=I=-14:TP=-2.2:LRA=11",
         "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(mix)])
    _, mix_i = sfx_kit.ebur128(mix)
    _, bed_i = sfx_kit.ebur128(bed_wav)
    _, sfx_i = sfx_kit.ebur128(sfx_wav)
    return {"vo_lufs": round(vo_i, 2), "bed_lufs": round(bed_i, 2), "sfx_lufs": round(sfx_i, 2), "mix_lufs": round(mix_i, 2)}


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
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src_wav), "-af", af,
             "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(cal_wav)])
        run(["ffmpeg", "-y", "-v", "error", "-i", str(cal_wav), "-c:a", "aac", "-b:a", "256k",
             "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(test_m4a)])
        m_i, m_tp = gso.aac_loudness(test_m4a)
        if m_i is not None and m_tp is not None:
            i_lufs, tp = m_i, m_tp
        print(f"    aac cal iter {it}: gain={gain_db:+.2f}dB limit={limit_db:.2f}dB -> I={i_lufs:.2f} LUFS, TP={tp:.2f} dBTP", flush=True)
        if -14.15 <= i_lufs <= -13.85 and tp <= -1.85:
            break
        gain_db += (-14.0 - i_lufs)
        if tp > -1.85:
            limit_db -= max(0.15, tp - (-2.0))
    return cal_wav, round(i_lufs, 2), round(tp, 2)


def teach_at(words: list[dict], needle: str, end_in: float) -> tuple[float, float]:
    hits = [w for w in words if needle in re.sub(r"[^a-z]", "", w["w"].lower())]
    start = hits[0]["s"] if hits else 16.2
    start = min(max(start, 14.15), end_in - 2.7)
    end = min(start + 3.0, end_in - 0.15)
    if end - start < 2.5:
        start = max(14.15, end - 2.6)
    return round(start, 2), round(end, 2)


SHORTS = [
    {
        "slug": "wed09_great_dimming",
        "stem": "029_short_wed09_great_dimming_v06",
        "v04_stem": "029_short_wed09_great_dimming_v04",
        "video_id": "SWDCZfWZVao",
        "day": "Wed 9 Dec",
        "air": "2026-12-09",
        "due": "2026-12-06 18:00",
        "airs": "2026-12-09 11:30",
        "title": "Why Did Betelgeuse Suddenly Lose Two-Thirds of Its Light?",
        "plan_total": 22.74,
        "lead": 0.05,
        "gap": 0.18,
        "hook": [("LOST 2/3 OF", WHITE), ("ITS LIGHT", YELLOW)],
        "cover_rows": [("LOST 2/3 OF", WHITE), ("ITS LIGHT?", YELLOW)],
        "cover_from_open_f0": True,
        "teach_text": "CLOUD OF DUST",
        "teach_needle": "cloud",
        "payoff_word": "dust",
        "sentences": [
            {"a": 109.92, "b": 114.20}, {"a": 115.00, "b": 119.14}, {"a": 127.54, "b": 129.38},
            {"a": 133.54, "b": 137.80}, {"a": 138.44, "b": 143.56},
        ],
        "plates": [
            {"row": "s01_orion_sphere", "prefer_out": 2.69, "lock_out": 2.69, "kind": "orion_sphere_open", "src": "gemini_night.jpg"},
            {"row": "s02_dip_a", "prefer_out": 5.12, "lock_out": 5.12, "kind": "upright_code", "code_mode": "wed_r15_dip", "src": "code_graphic_029_wed_r15_dip_v06.mp4", "offset": 0.3},
            {"row": "s03_sphere_dec", "prefer_out": 8.74, "lock_out": 8.74, "kind": "starfield_comp", "src": "sphere_dec.jpg", "sky_origin": (8200, 1500), "disk_sz": 760},
            {"row": "s06_visir", "prefer_out": 12.39, "lock_out": 12.39, "kind": "starfield_comp", "src": "visir_flames.jpg", "sky_origin": (12400, 1900), "disk_sz": 820},
            {"row": "s07_eject", "prefer_out": 15.20, "lock_out": 15.20, "kind": "video", "src": "orion_over_paranal.mp4", "offset": 1.2, "cx": 680},
            {"row": "s08_dust_a", "prefer_out": 17.77, "lock_out": 17.77, "kind": "still", "src": "dust_impression.jpg", "box": (0.08, 0.05, 0.78, 0.95)},
            {"row": "s09_dust_b", "prefer_out": 20.71, "kind": "still", "src": "dust_impression.jpg", "box": (0.22, 0.12, 0.92, 0.98)},
            {"row": "s10_end", "kind": "match0", "src": "gemini_night.jpg", "end_card": True},
        ],
    },
    {
        "slug": "fri11_opening_testA",
        "stem": "029_short_fri11_opening_testA_v06",
        "v04_stem": "029_short_fri11_opening_testA_v04",
        "video_id": "k2kEaA7ICjc",
        "meta_promise_lint": "waived: Test A arm (SHORTS_TESTS.md). The long's own opening says 'In this film, I will show you'.",
        "test_a": True,
        "cut_before": ["In", "s06_promise_b"],
        "teach_on_row": "s06_promise_b",
        "day": "Fri 11 Dec (Test A)",
        "air": "2026-12-11",
        "due": "2026-12-08 18:00",
        "airs": "2026-12-11 11:30",
        "title": "Is Betelgeuse Really About to Explode?",
        "plan_total": 36.08,
        "lead": 0.08,
        "gap": 0.20,
        "hook": [("VISIBLE IN", WHITE), ("DAYLIGHT", YELLOW)],
        "cover_rows": [("VISIBLE IN", WHITE), ("DAYLIGHT?", YELLOW)],
        "cover_from_open_f0": True,
        "teach_text": "DAYTIME SKY",
        "teach_needle": "daytime",
        "payoff_word": "garden",
        "sentences": [
            {"a": 0.08, "b": 3.86}, {"a": 4.58, "b": 5.70}, {"a": 6.54, "b": 8.48},
            {"a": 9.02, "b": 10.64}, {"a": 11.76, "b": 13.34}, {"a": 13.96, "b": 21.40},
            {"a": 22.58, "b": 36.94, "tighten": True},
        ],
        "plates": [
            {"row": "s01_visir", "prefer_out": 2.50, "kind": "starfield_comp", "src": "visir_flames.jpg", "sky_origin": (18200, 80), "bg_gain": 0.64, "shimmer": True, "disk_sz": 830, "drive": True},
            {"row": "s02_orion_b", "prefer_out": 5.28, "kind": "video", "src": "orion_rise_vlt.mp4", "offset": 1.2, "cx": 640},
            {"row": "s03_paranal", "prefer_out": 9.24, "kind": "video", "src": "orion_over_paranal.mp4", "offset": 0.45, "cx": 700},
            {"row": "s04_sphere", "prefer_out": 12.80, "kind": "starfield_comp", "src": "sphere_jan.jpg", "sky_origin": (15600, 1400), "disk_sz": 760},
            {"row": "s05_promise_a", "prefer_out": 15.26, "lock_out": 15.26, "kind": "upright_code", "code_mode": "fri_promise_a", "src": "code_graphic_029_fri_promise_a_v06.mp4", "offset": 0.4},
            {"row": "s06_promise_b", "prefer_out": 18.66, "kind": "upright_code", "code_mode": "fri_promise_b", "src": "code_graphic_029_fri_promise_b_v06.mp4", "offset": 6.0},
            {"row": "s07_alma", "prefer_out": 22.10, "kind": "video", "src": "alma_orion_set.mp4", "offset": 0.4, "cx": 860, "mode": "sky"},
            {"row": "s08_promise_c", "prefer_out": 25.90, "kind": "upright_code", "code_mode": "fri_promise_c", "src": "code_graphic_029_fri_promise_c_v06.mp4", "offset": 11.0},
            {"row": "s09_promise_d", "prefer_out": 29.80, "kind": "upright_code", "code_mode": "fri_promise_d", "src": "code_graphic_029_fri_promise_d_v06.mp4", "offset": 16.5},
            {"row": "s10_lasilla", "prefer_out": 34.08, "kind": "video", "src": "lasilla_mw.mp4", "offset": 1.0, "cx": 500},
            {"row": "s11_end", "kind": "match0", "src": "visir_flames.jpg", "end_card": True},
        ],
    },
    {
        "slug": "mon14_half_moon_daylight",
        "stem": "029_short_mon14_half_moon_daylight_v06",
        "v04_stem": "029_short_mon14_half_moon_daylight_v04",
        "video_id": "heiGCnGKTkE",
        "day": "Mon 14 Dec",
        "air": "2026-12-14",
        "due": "2026-12-11 18:00",
        "airs": "2026-12-14 11:30",
        "title": "How Bright Will Betelgeuse Get When It Explodes?",
        "plan_total": 23.94,
        "lead": 0.06,
        "gap": 0.20,
        "hook": [("BRIGHT AS A", WHITE), ("HALF MOON", YELLOW)],
        "cover_rows": [("BRIGHT AS A", WHITE), ("HALF MOON?", YELLOW)],
        "cover_src": HDIR / "half_moon.jpg",
        "cover_box": (0.08, 0.08, 0.92, 0.92),
        "teach_text": "HALF MOON BRIGHT",
        "teach_needle": "half",
        "payoff_word": "daylight",
        "sentences": [
            {"a": 248.06, "b": 250.96}, {"a": 251.88, "b": 254.38}, {"a": 255.30, "b": 261.70},
            {"a": 274.12, "b": 275.72}, {"a": 276.70, "b": 282.16}, {"a": 282.92, "b": 284.64},
        ],
        "plates": [
            {"row": "s01_casa", "prefer_out": 2.96, "kind": "still", "src": "casa.jpg", "box": (0.18, 0.05, 0.82, 0.95), "rings": True, "drive": True},
            {"row": "s02_neutrino", "prefer_out": 5.76, "kind": "neutrino", "src": "code_graphic_029_mon_neutrino_v06.mp4"},
            {"row": "s03_chajnantor", "prefer_out": 9.00, "kind": "video", "src": "lasilla_mw.mp4", "offset": 2.0, "cx": 520},
            {"row": "s04_epic", "prefer_out": 12.36, "kind": "still", "src": "dscovr_epic.jpg", "box": (0.12, 0.08, 0.88, 0.92)},
            {"row": "s05_orion_flare", "prefer_out": 16.00, "kind": "upright_code", "code_mode": "mon_r25_orion", "src": "code_graphic_029_mon_r25_orion_v06.mp4", "offset": 0.4},
            {"row": "s06_half_moon", "prefer_out": 19.80, "kind": "still", "src": "half_moon.jpg", "box": (0.10, 0.08, 0.90, 0.92)},
            {"row": "s07_daylight", "prefer_out": 21.94, "kind": "upright_code", "code_mode": "mon_r27_orion", "src": "code_graphic_029_mon_r27_orion_v06.mp4", "offset": 2.0},
            {"row": "s08_end", "kind": "match0", "src": "casa.jpg", "end_card": True},
        ],
    },
]

POOL = {
    "gemini_night.jpg": "NOIRLab Gemini North photograph of the Orion night-sky starfield with ESO VLT SPHERE Betelgeuse",
    "sphere_jan.jpg": "ESO VLT SPHERE photograph of Betelgeuse in January 2019 over NOIRLab Gemini North Orion starfield",
    "sphere_dec.jpg": "ESO VLT SPHERE photograph of Betelgeuse in December 2019 over NOIRLab Gemini North Orion starfield",
    "visir_flames.jpg": "ESO VLT VISIR photograph of Betelgeuse and its plume over NOIRLab Gemini North Orion starfield",
    "dust_impression.jpg": "ESO artist's concept of a dust cloud dimming a red star",
    "casa.jpg": "NASA Chandra photograph of the Cassiopeia A supernova remnant",
    "dscovr_epic.jpg": "NASA DSCOVR EPIC photograph of Earth",
    "half_moon.jpg": "NASA photograph of the Moon at half phase",
    "sdo_hmi_continuum.jpg": "NASA SDO HMI photograph of the Sun",
    "orion_rise_vlt.mp4": "ESO video of Orion rising over the VLT",
    "orion_over_paranal.mp4": "ESO video of Orion over Paranal",
    "alma_orion_set.mp4": "ESO video of Orion setting over ALMA",
    "lasilla_mw.mp4": "ESO video of the Milky Way over La Silla",
    "lasilla_mw_b.mp4": "ESO video of the Milky Way over La Silla",
}


def loop_diff(final: Path, total: float, masks: list[Path], work: Path) -> float:
    f0 = work / "loop_f0.png"
    fl = work / "loop_last.png"
    last_n = max(0, round(total * FPS) - 1)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-vf", "select=eq(n\\,0)", "-frames:v", "1", str(f0)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-vf", f"select=eq(n\\,{last_n})", "-frames:v", "1", str(fl)])
    a = np.asarray(Image.open(f0).convert("RGB").resize((W, H)), dtype=np.int16)
    b = np.asarray(Image.open(fl).convert("RGB").resize((W, H)), dtype=np.int16)
    mask = np.zeros((H, W), dtype=bool)
    for p in masks:
        if p.exists():
            al = np.asarray(Image.open(p).convert("RGBA").resize((W, H)).split()[-1])
            mask |= al > 16
    diff = np.abs(a - b).mean(axis=2)
    keep = ~mask
    return round(float(diff[keep].mean()), 2) if keep.any() else 999.0


def ocr_frames(final: Path, report: Path, work: Path) -> dict:
    frames = work / "ocr_frames"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-vf", "fps=30,scale=540:960", str(frames / "%05d.jpg")])
    swift = r'''
import Foundation
import Vision
import AppKit
let dir = CommandLine.arguments[1]
let names = (try? FileManager.default.contentsOfDirectory(atPath: dir))?.filter { $0.hasSuffix(".jpg") }.sorted() ?? []
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.usesLanguageCorrection = false
for name in names {
    let url = URL(fileURLWithPath: dir).appendingPathComponent(name)
    guard let img = NSImage(contentsOf: url),
          let tiff = img.tiffRepresentation,
          let rep = NSBitmapImageRep(data: tiff),
          let cg = rep.cgImage else { continue }
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    try? handler.perform([req])
    let text = (req.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: " ")
    if !text.isEmpty { print("\(name)\t\(text)") }
}
'''
    src_swift = WORK_ROOT / "j2551_ocr_scan.swift"
    bin_path = WORK_ROOT / "j2551_ocr_scan"
    if not bin_path.exists():
        src_swift.parent.mkdir(parents=True, exist_ok=True)
        src_swift.write_text(swift)
        run(["swiftc", "-O", "-o", str(bin_path), str(src_swift)])
    raw = sp.check_output([str(bin_path), str(frames)], text=True, stderr=sp.STDOUT)
    banned_bits = (
        "vp1bbq", "bbqzdnm", "swdczfw", "k2keaa7", "heigcng",
        "j0944", "j0929", "j0937", "j0961", "j0991", "j2551", "j2829",
        ".mp4", ".py", ".json",
    )
    hits, kept = [], []
    for line in raw.splitlines():
        if "\t" not in line:
            continue
        name, said = line.split("\t", 1)
        norm = re.sub(r"[^a-z0-9.]", "", said.lower())
        kept.append(f"{name}\t{said}")
        if any(b in norm or b in said.lower() for b in banned_bits):
            hits.append(f"{name}\t{said}")
    nframes = len(list(frames.glob("*.jpg")))
    report.write_text(f"frames {nframes}\nhits {len(hits)}\n" + "\n".join(hits) + "\n---\n" + "\n".join(kept) + "\n")
    shutil.rmtree(frames, ignore_errors=True)
    return {"verdict": "FAIL" if hits or nframes < 10 else "PASS", "frames": nframes, "hits": hits[:12]}


def build_j2829_review_pack(final_mp4: Path, stem: str, total_s: float, plates: list[dict], out_dir: Path) -> dict:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    tw, th = 270, 480
    total_frames = round(total_s * FPS)
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
    idxs_2fps = [min(total_frames - 1, round(k * 0.5 * FPS)) for k in range(int(total_s * 2) + 1)]
    cols = 9
    rows = (len(idxs_2fps) + cols - 1) // cols
    sheet_2fps = Image.new("RGB", (cols * tw, rows * th), (14, 18, 26))
    for j, fi in enumerate(idxs_2fps):
        tile = all_frames[fi].copy()
        d = ImageDraw.Draw(tile)
        d.rectangle((0, 0, 150, 26), fill=(0, 0, 0))
        d.text((6, 4), f"t={fi / FPS:05.2f}s f{fi:03d}", font=f_lbl, fill=(255, 255, 255))
        sheet_2fps.paste(tile, ((j % cols) * tw, (j // cols) * th))
    p_2fps = out_dir / f"{stem}_2fps.jpg"
    sheet_2fps.save(p_2fps, quality=86)

    # 2. Every cut boundary +-3 frames
    cut_boundaries = [round(s["out"] * FPS) for s in plates[:-1]]
    sheet_cuts = Image.new("RGB", (7 * tw, len(cut_boundaries) * th), (14, 18, 26))
    for r_idx, cf in enumerate(cut_boundaries):
        for c_idx, df in enumerate(range(-3, 4)):
            fi = max(0, min(total_frames - 1, cf + df))
            tile = all_frames[fi].copy()
            d = ImageDraw.Draw(tile)
            bg_c = (150, 30, 30) if df == 0 else (0, 0, 0)
            d.rectangle((0, 0, 220, 26), fill=bg_c)
            d.text((6, 4), f"cut{r_idx+1:02d} {df:+d} f{fi:03d} ({fi/FPS:.2f}s)", font=f_lbl, fill=(255, 255, 255))
            sheet_cuts.paste(tile, (c_idx * tw, r_idx * th))
    p_cuts = out_dir / f"{stem}_cuts_pm3.jpg"
    sheet_cuts.save(p_cuts, quality=86)

    # 3. Every frame of final 3.0 s (90 frames at 30 fps)
    n_tail = round(3.0 * FPS)
    tail_start = max(0, total_frames - n_tail)
    tail_cols = 10
    tail_rows = (n_tail + tail_cols - 1) // tail_cols
    sheet_tail = Image.new("RGB", (tail_cols * tw, tail_rows * th), (14, 18, 26))
    for j, fi in enumerate(range(tail_start, total_frames)):
        tile = all_frames[fi].copy()
        d = ImageDraw.Draw(tile)
        d.rectangle((0, 0, 150, 26), fill=(0, 0, 0))
        d.text((6, 4), f"f{fi:03d} {fi/FPS:05.2f}s", font=f_lbl, fill=(255, 255, 255))
        sheet_tail.paste(tile, ((j % tail_cols) * tw, (j // tail_cols) * th))
    p_tail = out_dir / f"{stem}_tail_3s_all_frames.jpg"
    sheet_tail.save(p_tail, quality=86)

    # 4. Extracted MP3 soundtrack for direct audio_input verification
    p_mp3 = out_dir / f"{stem}_audio.mp3"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final_mp4), "-vn", "-c:a", "libmp3lame", "-b:a", "160k", str(p_mp3)])

    # 5. Compact <=5 MB 360x640 moving video proxies (full film + final 3 s)
    p_proxy_full = out_dir / f"{stem}_proxy_full_360x640.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(final_mp4),
        "-vf", "scale=360:640:flags=lanczos",
        "-c:v", "libx264", "-preset", "fast", "-crf", "26", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(p_proxy_full),
    ])
    p_proxy_tail = out_dir / f"{stem}_proxy_tail3s_360x640.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{total_s - 3.0:.2f}", "-i", str(final_mp4),
        "-vf", "scale=360:640:flags=lanczos",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(p_proxy_tail),
    ])
    if p_proxy_full.stat().st_size > 5 * 1024 * 1024:
        raise RuntimeError(f"proxy_full exceeds 5 MB: {p_proxy_full.stat().st_size}")
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


def render_plates_and_audio(spec: dict, work: Path, s_dir: Path, plates: list[dict], teach_s: float, slices: list[dict], total: float):
    concat, cuts, pool = [], [], []
    seen = set()
    cg = get_code_renderer()
    for i, p in enumerate(plates):
        piece = work / f"piece_{i:02d}.mp4"
        pdur = round(p["out"] - p["in"], 3)
        kind = p["kind"]
        src_name = p.get("src", "code_graphic_029_mon_neutrino_v06.mp4")
        file_lookup = p.get("file") or src_name
        if kind == "orion_sphere_open":
            up = render_orion_sphere_open(pdur, piece, save_f0=(work / "open_f0.png") if i == 0 else None)
            video, offset, framing = True, 0.0, {"offset": 0.0}
        elif kind == "starfield_comp":
            up = render_starfield_star_composite(
                HDIR / file_lookup, pdur, piece,
                sky_origin=p["sky_origin"],
                disk_sz=p.get("disk_sz", 780),
                drive=p.get("drive", False),
                bg_gain=p.get("bg_gain", 1.0),
                shimmer=p.get("shimmer", False),
                save_f0=(work / "open_f0.png") if i == 0 else None,
            )
            video, offset, framing = True, 0.0, {"offset": 0.0, "sky_origin": list(p["sky_origin"])}
        elif kind == "still":
            up = render_still_fullbleed(
                HDIR / file_lookup, pdur, piece, p["box"],
                rings=p.get("rings", False),
                drive=p.get("drive", False),
                save_f0=(work / "open_f0.png") if i == 0 else None,
            )
            animated = bool(p.get("rings") or p.get("drive"))
            video = animated
            offset = 0.0 if animated else None
            framing = {"offset": 0.0} if animated else {"box": list(p["box"])}
        elif kind == "video":
            up = render_video_fullbleed(HDIR / file_lookup, p.get("offset", 0.0), pdur, piece, p.get("mode", "crop"), p.get("cx", 656))
            video, offset, framing = True, p.get("offset", 0.0), {"offset": p.get("offset", 0.0)}
        elif kind == "upright_code":
            up = cg.render_clip(p["code_mode"], p.get("offset", 0.0), pdur, piece)
            shutil.copy2(piece, s_dir / src_name)
            video, offset, framing = True, p.get("offset", 0.0), {"offset": p.get("offset", 0.0)}
        elif kind == "neutrino":
            up = render_neutrinos_916(pdur, piece)
            shutil.copy2(piece, s_dir / src_name)
            video, offset, framing = True, 0.0, {"offset": 0.0}
        elif kind == "match0":
            up = render_hold(work / "open_f0.png", pdur, piece)
            src_name = f"frame0_hold_{spec['slug']}.png"
            POOL[src_name] = "opening frame held for the loop"
            video, offset, framing = True, 0.0, {"offset": 0.0}
        else:
            raise SystemExit(f"unknown plate kind: {kind}")

        cuts.append({
            "row": p["row"],
            "timeline_in": p["in"],
            "timeline_out": p["out"],
            "source": src_name,
            "upscale": up,
            "framing": framing,
            "video": video,
        })
        if src_name not in seen:
            seen.add(src_name)
            pool.append({
                "id": Path(src_name).stem,
                "file": src_name,
                "file_id": src_name,
                "source": src_name,
                "title": POOL.get(file_lookup, POOL.get(src_name, "our own code graphic")),
            })
        concat.append(f"file '{piece.name}'")
        print(f"    plate {p['row']:16s} ({p['in']:5.2f}-{p['out']:5.2f}s) kind={kind:14s} up={up}", flush=True)

    (work / "list.txt").write_text("\n".join(concat) + "\n")
    pic = work / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt"), "-c", "copy", str(pic)])
    hits = [("whoosh", 0.0, -6.0), ("tick", TITLE_IN, -8.0), ("tick", teach_s, -8.0)]
    aud = build_audio(work, slices, total, hits)
    return pic, cuts, pool, aud


def verify_v04_untouched(slug: str) -> str:
    expected = EXPECTED_V04_SHA256[slug]
    checked = []
    for film_root in (LIVE_FILM, LOCAL_FILM):
        v04_mp4 = film_root / "10_Shorts" / slug / "06_Final-Exports" / f"029_short_{slug}_v04.mp4"
        if v04_mp4.exists():
            actual = sha256(v04_mp4)
            if actual != expected:
                raise SystemExit(f"CRITICAL: {v04_mp4} sha256 {actual} != expected {expected}")
            checked.append(actual)
    if not checked:
        raise SystemExit(f"CRITICAL: no v04 file found for {slug}")
    return expected


def build_one(spec: dict) -> dict:
    slug = spec["slug"]
    stem = spec["stem"]
    v04_sha = verify_v04_untouched(slug)
    print(f"\n=== {slug} ({spec['video_id']}) verified untouched v04 sha256={v04_sha[:16]}... ===", flush=True)

    slices, words, last = build_voice(spec["sentences"], spec["lead"], spec["gap"])
    plates_in = [dict(p) for p in spec["plates"]]
    if spec.get("cut_before"):
        token, row = spec["cut_before"]
        hit = next(
            (w for w, nxt in zip(words, words[1:])
             if w["w"].strip(".,!?") == token and nxt["w"].strip(".,!?").lower() == "this"),
            None,
        )
        if hit is None:
            raise SystemExit(f"no '{token} this' cut in {slug}")
        for p in plates_in:
            if p["row"] == row:
                p["lock_out"] = round(hit["s"] - 0.03, 2)
    plates = layout_plates(plates_in, words, last, spec["plan_total"])
    total = plates[-1]["out"]
    end_in = plates[-1]["in"]
    if spec.get("teach_on_row"):
        row = next(p for p in plates if p["row"] == spec["teach_on_row"])
        teach_e = round(row["out"] + 0.24, 2)
        teach_s = round(max(row["in"] + 0.12, teach_e - 2.9), 2)
    else:
        teach_s, teach_e = teach_at(words, spec["teach_needle"], end_in)

    joined = " ".join(w["w"] for w in words)
    print(f"  words={len(words)} last_word={last:.2f}s end_in={end_in:.2f}s total={total:.2f}s teach={teach_s:.2f}-{teach_e:.2f}s", flush=True)

    s_dir = LIVE_FILM / "10_Shorts" / slug / "06_Final-Exports"
    s_dir.mkdir(parents=True, exist_ok=True)
    work = WORK_ROOT / slug
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    hook = make_hook(work / "hook.png", spec["hook"])
    title = make_title(work / "title.png")
    end = make_end(work / "end_card.png")
    teach_bb = make_teach(work / "teach.png", spec["teach_text"])
    caps = caption_chunks(words, last)
    for i, c in enumerate(caps):
        c["bbox"] = make_caption(work / f"cap_{i:02d}.png", c["text"])

    pic, cuts, pool, aud = render_plates_and_audio(spec, work, s_dir, plates, teach_s, slices, total)
    cal_wav, aac_i, aac_tp = calibrate_aac_wav(work, work / "mix.wav", total)
    aud["mix_lufs"] = aac_i
    aud["aac_lufs"] = aac_i
    aud["aac_tp_dbtp"] = aac_tp

    final_mp4 = s_dir / f"{stem}.mp4"
    hook_im = Image.open(work / "hook.png").convert("RGBA")
    title_im = Image.open(work / "title.png").convert("RGBA")
    end_im = Image.open(work / "end_card.png").convert("RGBA")
    teach_im = Image.open(work / "teach.png").convert("RGBA")
    cap_ims = [Image.open(work / f"cap_{i:02d}.png").convert("RGBA") for i in range(len(caps))]
    blank_rgba = Image.new("RGBA", (W, H), (0, 0, 0, 0)).tobytes()

    def _scale_alpha(im: Image.Image, a: float) -> Image.Image:
        if a >= 0.999:
            return im
        r, g, b, al = im.split()
        al = al.point(lambda p, f=a: int(round(p * f)))
        return Image.merge("RGBA", (r, g, b, al))

    n_total_frames = int(round(total * FPS))
    ff_cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-t", f"{total:.3f}", "-i", str(pic),
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", str(cal_wav),
        "-filter_complex", f"[0:v]fps={FPS},setsar=1,format=yuv420p[v0];[v0][1:v]overlay=0:0,noise=alls=2:allf=t,format=yuv420p[v]",
        "-map", "[v]", "-map", "2:a", *shorts_encode_args(fps=FPS), "-t", f"{total:.3f}", str(final_mp4),
    ]
    proc = sp.Popen(ff_cmd, stdin=sp.PIPE)
    assert proc.stdin is not None
    last_state_key = None
    last_state_bytes = blank_rgba
    try:
        for fi in range(n_total_frames):
            t = fi / FPS
            hk_a = 0.0
            if 0.0 <= t < HOOK_END:
                hk_a = 1.0 if t < (HOOK_END - 0.25) else max(0.0, min(1.0, (HOOK_END - t) / 0.25))
            tt_a = 0.0
            if TITLE_IN <= t < TITLE_OUT:
                tt_a = max(0.0, min(1.0, (t - TITLE_IN) / 0.30, (TITLE_OUT - t) / 0.30))
            ec_a = 0.0
            if t >= end_in:
                ec_a = max(0.0, min(1.0, (t - end_in) / 0.28))
            th_a = 0.0
            if teach_s <= t < teach_e:
                th_a = max(0.0, min(1.0, (t - teach_s) / 0.25, (teach_e - t) / 0.25))
            cap_idx = -1
            for ci, c in enumerate(caps):
                if c["s"] <= t < c["e"]:
                    cap_idx = ci
                    break
            state_key = (round(hk_a, 3), round(tt_a, 3), round(ec_a, 3), round(th_a, 3), cap_idx)
            if state_key != last_state_key:
                if state_key == (0.0, 0.0, 0.0, 0.0, -1):
                    last_state_bytes = blank_rgba
                else:
                    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                    if hk_a > 0.0:
                        canvas.alpha_composite(_scale_alpha(hook_im, hk_a))
                    if tt_a > 0.0:
                        canvas.alpha_composite(_scale_alpha(title_im, tt_a))
                    if ec_a > 0.0:
                        canvas.alpha_composite(_scale_alpha(end_im, ec_a))
                    if th_a > 0.0:
                        canvas.alpha_composite(_scale_alpha(teach_im, th_a))
                    if cap_idx >= 0:
                        canvas.alpha_composite(cap_ims[cap_idx])
                    last_state_bytes = canvas.tobytes()
                last_state_key = state_key
            proc.stdin.write(last_state_bytes)
    finally:
        proc.stdin.close()
    rc_mux = proc.wait()
    if rc_mux != 0:
        raise SystemExit(f"final mux failed on {slug} with rc={rc_mux}")

    final_i, final_tp = gso.aac_loudness(final_mp4)
    aud["aac_lufs"] = final_i
    aud["aac_tp_dbtp"] = final_tp
    aud["mix_lufs"] = final_i
    print(f"  FINAL AAC {slug}: I={final_i} LUFS, TP={final_tp} dBTP", flush=True)

    # Cover + frame0
    frame0_jpg = s_dir / f"{stem}_frame0.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.30", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(frame0_jpg)])
    cover_jpg = s_dir / f"{stem}_cover.jpg"
    if spec.get("cover_from_open_f0"):
        cover_base = work / "open_f0.png"
    else:
        cb_im, _ = fit_fullbleed(spec["cover_src"], spec["cover_box"], max_up=1.95)
        cover_base = work / "cover_base.png"
        cb_im.save(cover_base)
    cover_info = make_cover(cover_jpg, cover_base, spec["cover_rows"])

    # Sidecars required by gate_shorts_open, polish_gate, picture_qa, sfx_kit
    words_path = s_dir / f"{stem}_words.json"
    transcript_path = s_dir / f"{stem}_transcript.txt"
    cuts_path = s_dir / f"{stem}_cuts.json"
    pool_path = s_dir / f"{stem}_pool.json"
    meta_path = s_dir / f"{stem}_meta.json"
    vo_stem_out = s_dir / f"{stem}_vo.wav"
    sfx_stem_out = s_dir / f"{stem}_sfx.wav"
    bed_stem_out = s_dir / f"{stem}_bed.wav"
    shutil.copy2(work / "stem_vo.wav", vo_stem_out)
    shutil.copy2(work / "stem_sfx.wav", sfx_stem_out)
    shutil.copy2(work / "stem_bed.wav", bed_stem_out)

    words_path.write_text(json.dumps(words, indent=2) + "\n")
    transcript_path.write_text(joined + "\n")
    cuts_path.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")
    meta_seed = {
        "job": "J2551",
        "slug": slug,
        "stem": stem,
        "video_id": spec["video_id"],
        "day": spec["day"],
        "air_date": spec["air"],
        "title": spec["title"],
        "parent_long_title": LONG_TITLE,
        "long": {"id": LONG_ID, "title": LONG_TITLE},
        "test_a": bool(spec.get("test_a", False)),
        "meta_promise_lint": spec.get("meta_promise_lint", "none"),
        "spoken": joined,
        "vo_onset_s": spec["lead"],
        "last_word_end_s": last,
        "duration_s": round(dur(final_mp4), 2),
        "end_card": {
            "start_s": end_in,
            "end_s": total,
            "text": END_CARD_LINE,
        },
        "words_file": str(words_path),
        "vo": str(vo_stem_out),
        "audio": aud,
    }
    meta_path.write_text(json.dumps(meta_seed, indent=2) + "\n")

    def run_gate(cmd: list) -> sp.CompletedProcess:
        return sp.run([str(x) for x in cmd], capture_output=True, text=True)

    g_txt = run_gate([sys.executable, MAIN_REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py",
                      "check", final_mp4, "--air-date", spec["air"], "--id", spec["video_id"], "--sheet-dir", s_dir])
    g_json = run_gate([sys.executable, MAIN_REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py",
                       "check", final_mp4, "--air-date", spec["air"], "--id", spec["video_id"], "--sheet-dir", s_dir, "--json"])
    (s_dir / f"{stem}_gate.txt").write_text((g_txt.stdout or "") + (g_txt.stderr or ""))
    (s_dir / f"{stem}_gate.json").write_text(g_json.stdout or g_json.stderr)
    print(g_txt.stdout, end="", flush=True)

    tp_f0 = run_gate([sys.executable, MAIN_REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py",
                      "short", frame0_jpg, "--out", s_dir / f"{stem}_frame0_preview.jpg", "--score"])
    tp_cov = run_gate([sys.executable, MAIN_REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py",
                       "short", cover_jpg, "--out", s_dir / f"{stem}_cover_preview.jpg", "--score"])
    print(tp_f0.stdout, end="", flush=True)
    print(tp_cov.stdout, end="", flush=True)

    sfx_res = run_gate([
        sys.executable, MAIN_REPO / "scripts/sfx_kit.py", "level",
        "--vo", vo_stem_out, "--sfx", sfx_stem_out, "--bed", bed_stem_out,
        "--minutes", f"{total / 60:.3f}",
        "--out", s_dir / f"{stem}_sfx_level.json",
    ])
    (s_dir / f"{stem}_sfx.txt").write_text((sfx_res.stdout or "") + (sfx_res.stderr or ""))
    print(sfx_res.stdout, end="", flush=True)

    mg_film = LOCAL_FILM if (LOCAL_FILM / "05_Music" / BED_MP3.name).exists() else LIVE_FILM
    mg_bed = mg_film / "05_Music" / BED_MP3.name
    mg_res = run_gate([
        sys.executable, MAIN_REPO / "scripts/music_gate.py", mg_film,
        "--bed", mg_bed, "--video", final_mp4,
        "--out", s_dir / f"{stem}_music_gate.json",
    ])
    (s_dir / f"{stem}_music_gate.txt").write_text((mg_res.stdout or "") + (mg_res.stderr or ""))
    print(mg_res.stdout, end="", flush=True)

    ocr_res = ocr_frames(final_mp4, s_dir / f"{stem}_ocr.txt", work)
    print(f"  OCR {slug}: {ocr_res['verdict']} ({ocr_res['frames']} frames, hits={len(ocr_res['hits'])})", flush=True)

    pg_res = run_gate([
        sys.executable, MAIN_REPO / "scripts/polish_gate.py", final_mp4,
        "--cuts", cuts_path, "--reviewed-ok", REV_OK,
        "--out", s_dir / f"{stem}_polish_gate.json",
    ])
    (s_dir / f"{stem}_polish_gate.txt").write_text((pg_res.stdout or "") + (pg_res.stderr or ""))
    print(pg_res.stdout, end="", flush=True)

    pqa_dir = s_dir / f"{stem}_picture_qa"
    pqa_res = run_gate([
        sys.executable, MAIN_REPO / "scripts/picture_qa.py", final_mp4,
        "--cuts", cuts_path, "--pool", pool_path, "--reviewed-ok", REV_OK, "--out-dir", pqa_dir,
    ])
    (s_dir / f"{stem}_picture_qa.txt").write_text((pqa_res.stdout or "") + (pqa_res.stderr or ""))
    print(pqa_res.stdout, end="", flush=True)

    dec_res = run_gate(["ffmpeg", "-v", "error", "-i", final_mp4, "-f", "null", "-"])
    print(f"  ffmpeg full decode rc={dec_res.returncode} stderr={dec_res.stderr.strip()!r}", flush=True)

    text_masks = [work / "hook.png", work / "end_card.png", work / "teach.png"] + [work / f"cap_{i:02d}.png" for i in range(len(caps))]
    ld = loop_diff(final_mp4, total, text_masks, work)
    print(f"  loop_diff={ld} (<= 15 required)", flush=True)

    review_dir = REVIEW_ROOT / slug
    review_pack = build_j2829_review_pack(final_mp4, stem, total, plates, review_dir)

    # Re-verify untouched v04 SHA-256 after build
    v04_after = verify_v04_untouched(slug)

    gates = {
        "gate_shorts_open_rc": g_txt.returncode,
        "thumb_preview_frame0_rc": tp_f0.returncode,
        "thumb_preview_cover_rc": tp_cov.returncode,
        "sfx_level_rc": sfx_res.returncode,
        "music_gate_rc": mg_res.returncode,
        "ocr_rc": 0 if ocr_res["verdict"] == "PASS" else 1,
        "polish_gate_rc": pg_res.returncode,
        "picture_qa_rc": pqa_res.returncode,
        "ffmpeg_decode_rc": dec_res.returncode,
        "loop_diff_rc": 0 if ld <= 15.0 else 1,
    }
    meta_full = {
        **meta_seed,
        "v04_untouched_sha256": v04_after,
        "mp4_sha256": sha256(final_mp4),
        "mp4_bytes": final_mp4.stat().st_size,
        "frame0_jpg_sha256": sha256(frame0_jpg),
        "cover_jpg_sha256": sha256(cover_jpg),
        "loop_diff": ld,
        "teach": {"text": spec["teach_text"], "s": teach_s, "e": teach_e, "bbox": teach_bb},
        "hook": hook,
        "title_banner": title,
        "end_card_layout": end,
        "cover": cover_info,
        "j2829_review_pack": review_pack,
        "gates": gates,
    }
    meta_path.write_text(json.dumps(meta_full, indent=2) + "\n")
    (review_dir / f"{stem}_summary.json").write_text(json.dumps(meta_full, indent=2) + "\n")

    if any(v != 0 for v in gates.values()):
        raise SystemExit(f"GATE FAILURE on {slug}: {json.dumps(gates)}")

    # Stage UAT folders (do not copy sidecars into MAIN_REPO local checkout; keep git status clean)
    uat_files = [
        final_mp4,
        cover_jpg,
        s_dir / f"{stem}_frame0_preview.jpg",
        Path(review_pack["sheet_2fps"]),
        Path(review_pack["sheet_cuts_pm3"]),
        Path(review_pack["sheet_tail_3s"]),
        meta_path,
    ]
    for uat_root in (UAT_NAS_ROOT, UAT_ICLOUD_ROOT):
        uat_dir = uat_root / stem
        uat_dir.mkdir(parents=True, exist_ok=True)
        sums = {}
        for f in uat_files:
            dst = uat_dir / f.name
            shutil.copy2(f, dst)
            sums[f.name] = sha256(dst)
        (uat_dir / "SHA256SUMS.json").write_text(json.dumps(sums, indent=2) + "\n")

    # Clean intermediate work folder to keep disk free
    shutil.rmtree(work, ignore_errors=True)
    return meta_full


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="Build only matching slug substring")
    args = ap.parse_args()

    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    REVIEW_ROOT.mkdir(parents=True, exist_ok=True)

    results = []
    for spec in SHORTS:
        if args.only and args.only not in spec["slug"]:
            continue
        results.append(build_one(spec))

    (REVIEW_ROOT / "ALL_029_v06_SUMMARY.json").write_text(json.dumps(results, indent=2) + "\n")
    print("\nALL REQUESTED 029 v06 SHORTS PASSED EVERY AUTOMATED GATE.", flush=True)


if __name__ == "__main__":
    main()
