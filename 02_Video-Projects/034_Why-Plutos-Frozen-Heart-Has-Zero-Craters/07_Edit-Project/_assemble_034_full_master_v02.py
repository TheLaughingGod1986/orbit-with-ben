#!/usr/bin/env python3
"""034 Pluto long master v02 (J2438 + J2383 §5.1 finishing fixes). £0 spend.

Executes corrected FIRST30_PLAN.md (0870bcdf52) and all J2383 §5.1 fixes:
1. Splices out raw 2.000..4.800s (-2.800s, 'in distant orbit around our sun,') from
   pluto_frozen_heart_vo_v03.wav so Sentence 1 ends at 5.900s < 8.000s and Sentence 2
   payoff completes at 16.240s < 20.000s, restoring +2.800s via three verified
   inter-sentence silences (39.300s +1.000s, 54.000s +0.900s, 60.550s +0.900s) so
   R08 starts at 65.760s (frame 1,973) and R08-R74 stay 100% locked.
2. Inserts all 6 chapter-card silences (R08, R20, R33, R45, R54, R64) at
   prev_word_raw_end + 0.600s (65.760, 159.220, 261.140, 368.220, 451.660, 534.260s)
   eliminating pre-onset phoneme blips while keeping word offsets identical to v01.
3. Re-cuts R01-R07 (0.000-65.767s, frames 0..1,973) into 19 cuts <= 3.933s (11 cuts
   <= 3.533s in R01-R04, 138 cuts total across 19,408 frames = 646.933s at 30/1 CFR).
4. Upgrades render_still() to symmetric sub-pixel PIL Image.Transform.EXTENT BICUBIC
   zoom (1.000 -> z_max <= 1.045) + 2D separable min(fx, fy) 48px feather over lifted
   starry canvas (eliminating the 48x48 top-left corner glitch) with upscale <= 2.00x.
5. Word-boundary asset ID matching in row_assets() (fixing R34 ksc_011906_nh_launchchange
   -> KSC-06pd0099), offset >= 2.0s on ksc_011906_*.mp4 (skipping 0.0-0.5s black fade-ins),
   full person names on WHO cards (R10, R11, R58), and stripping duplicate Credit: pills.
"""
from __future__ import annotations

import concurrent.futures as cf
import csv
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
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters"
)
REPO = (
    Path("/Volumes/MiniWork/scratch/j2438-wt")
    if Path("/Volumes/MiniWork/scratch/j2438-wt/scripts/picture_qa.py").exists()
    else Path("/Users/benjaminoats/YouTube/orbit-with-ben")
)
EDIT = FILM / "07_Edit-Project"
SCRATCH_BASE = Path(os.environ.get("STUDIO_SCRATCH", "/Volumes/MiniWork/scratch"))
WORK = SCRATCH_BASE / "j2438_pluto_master_v02_work"
PACK = EDIT / "full_master_v02_pack"
OUT = FILM / "09_Final-Export" / "034_pluto_frozen_heart_master_v02.mp4"
SHOT = EDIT / "shot_list_v02.csv"
POOL = EDIT / "HARVEST_POOL_v01.json"
GFX = EDIT / "graphics_v03"
VO_WAV = FILM / "02_Voiceover" / "pluto_frozen_heart_vo_v03.wav"
WORDS_V01 = FILM / "02_Voiceover" / "stt" / "pluto_frozen_heart_vo_v03" / "stt_timeline_offset_v01.json"
WORDS = FILM / "02_Voiceover" / "stt" / "pluto_frozen_heart_vo_v03" / "stt_timeline_offset_v02.json"
BED = FILM / "05_Music" / "pluto_score_bed_v01.mp3"
KIT = FILM / "06_Sound-Effects" / "kit_v01"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

FPS = 30
TOTAL_FRAMES = 19408  # Exact 646.933333s at 30/1 CFR
TOTAL = TOTAL_FRAMES / FPS
SR = 48000
W, H = 1920, 1080
ENC = [
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
    "-r", "30", "-fps_mode", "cfr", "-video_track_timescale", "30000", "-g", "30", "-an",
]

LAB_RE = re.compile(r"`([^`]{1,48})`\s*\(`([0-9.]+)\s*[–-]\s*([0-9.]+)\s*s")
WHO_RE = re.compile(
    r"\*\*`WHO`\s*#\d+:\*\*\s*`([^`]+)`\s*/\s*`([^`]+)`\s*\(`([0-9.]+)\s*[–-]\s*([0-9.]+)\s*s"
)
CREDIT_MARKER_RE = re.compile(r"Credit:\s*`[^`]*`\s*\([^)]*\)")
SKIP_LAB = {"when", "who", "fact", "data", "scale", "chapter", "edit label"}

# Clean crop boxes on source plates that carry bottom/corner border bars or split comparison panels
CLEAN_CROPS: dict[str, tuple[int, int, int, int]] = {
    "PIA20155.jpg": (0, 0, 879, 760),
    "PIA19934.jpg": (0, 0, 1217, 900),
    "PIA19936.jpg": (300, 0, 3400, 1744),
    "PIA20727.jpg": (0, 350, 5000, 3850),
    "File_Charon_Discovery.jpg.jpg": (708, 0, 1416, 1072),
}

# SFX plan v02: R01-R06 updated to v02 cut/label boundaries; >= 65.76s identical to v01.
RUMBLES = [
    (3.17, 6.20), (36.50, 39.90), (268.18, 271.68), (326.88, 330.38),
    (377.43, 380.68), (427.08, 430.48), (520.58, 524.08), (620.28, 623.78),
]
WHOOSHES = [17.40, 111.92, 138.16, 197.36, 338.58, 463.04, 547.84, 562.86]
TICKS = [
    6.35, 13.30, 17.40, 23.00, 28.00, 31.90, 38.20, 46.80, 54.30,
    68.37, 71.62, 85.07, 88.87, 93.47, 112.12, 138.32,
    164.01, 197.56, 218.01, 230.26, 246.31, 268.23, 277.78, 288.53, 298.23,
    311.38, 321.13, 323.03, 326.93, 338.73, 355.93, 396.23, 436.23, 472.63,
    480.63, 495.33, 499.33, 520.73, 563.03, 580.63,
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    p = sp.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout)[-1800:])


def probe(path: Path) -> dict:
    raw = sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=width,height,codec_type,avg_frame_rate,nb_frames",
         "-of", "json", str(path)],
        text=True,
    )
    d = json.loads(raw)
    v = next(s for s in d.get("stream", d.get("streams", [])) if s.get("codec_type") == "video")
    return {
        "width": int(v["width"]),
        "height": int(v["height"]),
        "duration": float(d["format"]["duration"]),
        "avg_frame_rate": v.get("avg_frame_rate"),
        "nb_frames": int(v["nb_frames"]) if v.get("nb_frames") and str(v["nb_frames"]).isdigit() else None,
    }


def frames_ok(path: Path, n: int) -> bool:
    if not path.exists() or path.stat().st_size < 1000:
        return False
    try:
        info = probe(path)
    except (sp.CalledProcessError, StopIteration, KeyError):
        return False
    if info.get("nb_frames") is not None:
        return info["nb_frames"] == n
    return abs(info["duration"] * FPS - n) < 0.6


def starfield(path: Path) -> None:
    if path.exists():
        return
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W / 2) / (W / 2)
    ny = (yy - H / 2) / (H / 2)
    rad = np.clip(1.0 - 0.72 * (nx ** 2 + ny ** 2), 0.0, 1.0)
    r = (16 + 56 * rad + 10 * (yy / H)).clip(0, 255).astype(np.uint8)
    g = (26 + 74 * rad + 12 * (yy / H)).clip(0, 255).astype(np.uint8)
    b = (44 + 98 * rad + 16 * (yy / H)).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(np.stack([r, g, b], axis=-1), "RGB")
    dr = ImageDraw.Draw(im)
    seed = 34034
    for i in range(1800):
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        x = 16 + seed % (W - 32)
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        y = 16 + seed % (H - 32)
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        br = 195 + seed % 60
        sz = 1 if (i % 2) else 2
        dr.ellipse([x - sz, y - sz, x + sz, y + sz], fill=(br, br, min(255, br + 15)))
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, quality=95)


def make_label_rgba(text: str) -> Image.Image:
    """Renders a single-line pill or a two-line WHO card ('Name\\n(years) — role') in RGBA."""
    if "\n" in text:
        line1, line2 = text.split("\n", 1)
        f1 = ImageFont.truetype(FONT, 46)
        f2 = ImageFont.truetype(FONT_REG, 34)
        tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        b1 = tmp.textbbox((0, 0), line1, font=f1)
        b2 = tmp.textbbox((0, 0), line2, font=f2)
        w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
        w2, h2 = b2[2] - b2[0], b2[3] - b2[1]
        pad_x, pad_y, gap = 26, 16, 10
        bw = max(w1, w2) + pad_x * 2
        bh = h1 + h2 + gap + pad_y * 2
        im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        dr.rounded_rectangle([0, 0, bw - 1, bh - 1], 14, fill=(22, 34, 56, 236), outline=(255, 207, 64, 220), width=2)
        dr.text(((bw - w1) // 2 - b1[0], pad_y - b1[1]), line1, font=f1, fill=(255, 207, 64, 255))
        dr.text(((bw - w2) // 2 - b2[0], pad_y + h1 + gap - b2[1]), line2, font=f2, fill=(244, 247, 251, 255))
        return im

    font = ImageFont.truetype(FONT, 52)
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    box_l, box_t, box_r, box_b = tmp.textbbox((0, 0), text, font=font)
    tw, th = box_r - box_l, box_b - box_t
    pad_x, pad_y = 22, 14
    im = Image.new("RGBA", (tw + pad_x * 2, th + pad_y * 2), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([0, 0, im.width - 1, im.height - 1], 12, fill=(22, 34, 56, 232), outline=(105, 196, 241, 180), width=2)
    dr.text((pad_x - box_l, pad_y - box_t), text, font=font, fill=(255, 255, 255, 255))
    return im


def text_png(text: str, path: Path, size: int, box: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if box:
        make_label_rgba(text).save(path)
        return
    font = ImageFont.truetype(FONT, size)
    tmp = Image.new("RGBA", (8, 8))
    d = ImageDraw.Draw(tmp)
    box_l, box_t, box_r, box_b = d.textbbox((0, 0), text, font=font)
    tw, th = box_r - box_l, box_b - box_t
    pad = 8
    im = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.text((pad - box_l, pad - box_t), text, font=font, fill=(255, 255, 255, 255))
    im.save(path)


def load_rows() -> list[dict]:
    with SHOT.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_pool() -> list[dict]:
    d = json.loads(POOL.read_text())
    assets = []
    for a in d["assets"]:
        p = Path(a["local_path"])
        if p.exists() and "contact" not in p.name:
            assets.append(a)
    return assets


def gfx_file(name: str) -> Path | None:
    hits = [p for p in GFX.rglob(name) if p.is_file() and not p.name.startswith("._")]
    return hits[0] if hits else None


def row_assets(row: dict, pool: list[dict]) -> list[dict]:
    """Word-boundary asset ID matching (fixes R34 ksc_011906_nh_launchchange vs ksc_011906_nh_launch)."""
    text = row["asset"]
    found = []
    for a in pool:
        aid = a["id"]
        pat = r"(?<![A-Za-z0-9_.-])" + re.escape(aid) + r"(?![A-Za-z0-9_.-])"
        m = re.search(pat, text)
        if m:
            found.append((m.start(), a))
    found.sort(key=lambda x: x[0])
    return [a for _, a in found]


def labels_for(row: dict) -> list[tuple[str, float, float]]:
    """Extracts WHO two-line cards and 1-4 word labels while stripping Credit: pills."""
    raw_markers = row.get("markers") or ""
    cleaned = CREDIT_MARKER_RE.sub("", raw_markers)
    out: list[tuple[str, float, float]] = []
    who_spans: list[tuple[int, int]] = []

    for wm in WHO_RE.finditer(cleaned):
        who_spans.append(wm.span())
        name = wm.group(1).strip()
        role = wm.group(2).strip()
        if "principal investigator" in role.lower():
            role = role.replace("born ", "b. ").replace("principal investigator", "PI")
        a, b = float(wm.group(3)), float(wm.group(4))
        if b - a > 4.0:
            b = a + 4.0
        if b > a:
            out.append((f"{name}\n{role}", a, b))

    for m in LAB_RE.finditer(cleaned):
        if any(s <= m.start() < e for s, e in who_spans):
            continue
        text = m.group(1).strip()
        if text.lower() in SKIP_LAB:
            continue
        words = text.split()
        if len(words) > 4:
            text = " ".join(words[:4])
        a, b = float(m.group(2)), float(m.group(3))
        if b - a > 4.0:
            b = a + 4.0
        if b > a:
            out.append((text, a, b))

    if "subscri" in (row.get("vo_text") or "").lower():
        t0 = float(row["vo_in"]) + 0.3
        out.append(("SUBSCRIBE", t0, min(t0 + 4.0, float(row["vo_out"]) - 0.1)))

    out.sort(key=lambda x: x[1])
    return out


def credit_for(asset: dict | None, source: str) -> str:
    if asset is None or source in {"CODE", "CARD"}:
        return ""
    lic = (asset.get("license") or "") + " " + asset.get("id", "")
    if asset["id"].startswith("PIA") or "NASA" in lic:
        return "NASA"
    if asset["id"].startswith("KSC") or asset["id"].startswith("ksc") or asset["id"].startswith("NHQ"):
        return "NASA"
    if "Wikimedia" in lic or asset["id"].startswith("File:"):
        return "Wikimedia"
    return "NASA"


def _still_effective_size(asset: dict, crop_frac: float = 1.0) -> tuple[int, int, float, float]:
    """Returns (eff_w, eff_h, z_max, recorded_upscale) with strict <= 2.000x cap."""
    p = Path(asset["local_path"])
    if p.name in CLEAN_CROPS:
        x0, y0, x1, y1 = CLEAN_CROPS[p.name]
        sw, sh = x1 - x0, y1 - y0
    else:
        sw = int(asset.get("width") or 0)
        sh = int(asset.get("height") or 0)
        if not sw or not sh:
            with Image.open(p) as im:
                sw, sh = im.size
    eff_w = max(2, int(round(sw * crop_frac)))
    eff_h = max(2, int(round(sh * crop_frac)))
    cover = max(W / eff_w, H / eff_h)
    z_max = 1.045
    if cover <= 2.0:
        if cover * z_max <= 2.0:
            up = round(cover * z_max, 3)
        else:
            # Keep full-frame where cover <= 2.0 by capping z_max so cover * z_max <= 2.000
            # unless z_max would be < 1.020, in which case frame over starry canvas at <= 2.000x
            if 2.0 / cover >= 1.020:
                z_max = round(1.998 / cover, 4)
                up = round(cover * z_max, 3)
            else:
                fit = min(1.998 / z_max, (W - 120) / eff_w, (H - 120) / eff_h)
                up = round(fit * z_max, 3)
    else:
        fit = min(1.998 / z_max, (W - 120) / eff_w, (H - 120) / eff_h)
        up = round(fit * z_max, 3)
    return eff_w, eff_h, z_max, min(2.0, up)


def build_opening_cuts(rows_by_id: dict[str, dict], pool_by_name: dict[str, dict], video_used: dict) -> list[dict]:
    """Exact 19-cut, 1,973-frame opening plan (R01-R07, 0.000-65.767s) from FIRST30_PLAN.md §3."""
    spec = [
        # (row, frames, kind, filename, crop_frac, video_offset)
        ("R01", 95, "NASA", "PIA20291.jpg", 1.00, None),
        ("R01", 95, "NASA", "PIA19944.jpg", 1.00, None),
        ("R02", 105, "CODE", "code_graphic_034_r02a_sputnik_width.mp4", 1.00, None),
        ("R02", 104, "NASA", "PIA20007.jpg", 1.00, None),
        ("R02", 105, "CODE", "code_graphic_034_r02b_texas_oklahoma_scale.mp4", 1.00, None),
        ("R03", 106, "NASA", "File_The_Pluto_System_As_Seen_By_New_Horizons_Spacecraft.webm.webm", 1.00, 0.0),
        ("R03", 106, "NASA", "PIA20534.jpg", 1.00, None),
        ("R03", 106, "NASA", "PIA20534.jpg", 0.86, None),
        ("R04", 91, "NASA", "PIA20038.jpg", 1.00, None),
        ("R04", 91, "NASA", "PIA20286.jpg", 1.00, None),
        ("R04", 91, "NASA", "PIA14458.jpg", 1.00, None),
        ("R05", 118, "NASA", "File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm", 1.00, 0.0),
        ("R05", 118, "NASA", "File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm", 1.00, 20.0),
        ("R05", 117, "NASA", "PIA20726.jpg", 1.00, None),
        ("R05", 118, "NASA", "PIA20726.jpg", 0.86, None),
        ("R06", 112, "NASA", "PIA20155.jpg", 1.00, None),
        ("R06", 112, "NASA", "PIA20155.jpg", 0.86, None),
        ("R07", 92, "NASA", "PIA21965.jpg", 1.00, None),
        ("R07", 91, "NASA", "PIA21965.jpg", 0.86, None),
    ]
    cuts = []
    f_cur = 0
    for rid, nf, kind, fname, cfrac, voff in spec:
        row = rows_by_id[rid]
        labs = labels_for(row)
        t0 = f_cur / FPS
        if kind == "CODE":
            p = gfx_file(fname)
            if p is None:
                raise SystemExit(f"{rid}: missing {fname}")
            info = probe(p)
            cuts.append({
                "row": rid, "kind": "CODE", "path": str(p), "source": p.name,
                "t0": t0, "frames": nf, "overlay": None, "overlay_ss": 0.0,
                "labels": [], "credit": "", "offset": 0.0, "upscale": 1.0,
                "video": True, "src_w": info["width"], "src_h": info["height"],
                "crop_frac": 1.0, "z_max": 1.0,
            })
        elif voff is not None:
            asset = pool_by_name[fname]
            p = Path(asset["local_path"])
            info = probe(p)
            need = nf / FPS
            video_used.setdefault(str(p), []).append((voff, voff + need))
            up = max(W / info["width"], H / info["height"])
            cuts.append({
                "row": rid, "kind": "NASA", "path": str(p), "source": p.name,
                "t0": t0, "frames": nf, "overlay": None, "overlay_ss": 0.0,
                "labels": labs, "credit": credit_for(asset, "NASA"),
                "offset": voff, "upscale": round(up, 3), "video": True,
                "src_w": info["width"], "src_h": info["height"],
                "crop_frac": 1.0, "z_max": 1.0,
            })
        else:
            asset = pool_by_name[fname]
            p = Path(asset["local_path"])
            sw, sh, z_max, up = _still_effective_size(asset, cfrac)
            cuts.append({
                "row": rid, "kind": "NASA", "path": str(p), "source": p.name,
                "t0": t0, "frames": nf, "overlay": None, "overlay_ss": 0.0,
                "labels": labs, "credit": credit_for(asset, "NASA"),
                "offset": None, "upscale": up, "video": False,
                "src_w": sw, "src_h": sh, "crop_frac": cfrac, "z_max": z_max,
            })
        f_cur += nf
    assert f_cur == 1973, f"Expected 1973 opening frames, got {f_cur}"
    return cuts


def build_plan(rows: list[dict], pool: list[dict]) -> list[dict]:
    """Allocates exact 30fps cuts across R01-R74 (138 cuts, 19,408 frames)."""
    rows_by_id = {r["row"]: r for r in rows}
    pool_by_name = {Path(a["local_path"]).name: a for a in pool}
    video_used: dict[str, list[tuple[float, float]]] = {}
    cuts = build_opening_cuts(rows_by_id, pool_by_name, video_used)

    clock = 65.76
    problems = []
    for row in rows:
        if row["row"] in {"R01", "R02", "R03", "R04", "R05", "R06", "R07"}:
            continue
        dur = float(row["dur_s"])
        f0 = round(clock * FPS)
        clock += dur
        f1 = round(clock * FPS)
        nframes = f1 - f0
        t0 = f0 / FPS
        kind = row["source"]
        labs = labels_for(row)
        if kind in {"CODE", "CARD"}:
            m = re.search(r"((?:code_graphic|chapter_card|overlay)_\S+?\.(?:mp4|mov))", row["asset"])
            if not m:
                problems.append(f"{row['row']}: no graphic filename")
                continue
            path = gfx_file(m.group(1))
            if path is None:
                problems.append(f"{row['row']}: missing {m.group(1)}")
                continue
            info = probe(path)
            need = nframes / FPS
            if info["duration"] + 0.15 < need:
                problems.append(f"{row['row']}: {path.name} is {info['duration']:.2f}s, row needs {need:.2f}s")
            cuts.append({
                "row": row["row"], "kind": kind, "path": str(path),
                "source": path.name, "t0": t0, "frames": nframes,
                "overlay": None, "overlay_ss": 0.0,
                "labels": [] if kind == "CARD" else labs,
                "credit": "", "offset": 0.0, "upscale": 1.0, "video": True,
                "src_w": info["width"], "src_h": info["height"],
                "crop_frac": 1.0, "z_max": 1.0,
            })
            continue

        assets = row_assets(row, pool)
        if not assets:
            problems.append(f"{row['row']}: no pool asset in {row['asset'][:80]}")
            continue
        ncuts = max(1, int(float(row["cuts"])))
        pieces = []
        for i in range(ncuts):
            asset = assets[min(len(assets) - 1, int(i * len(assets) / ncuts))]
            pieces.append(asset)
        merged = []
        for asset in pieces:
            if merged and merged[-1][0]["local_path"] == asset["local_path"] and asset.get("kind") == "native_video":
                merged[-1][1] += 1
            else:
                merged.append([asset, 1])
        weights = [c for _, c in merged]
        acc = 0
        bounds = [0]
        for wgt in weights:
            acc += wgt
            bounds.append(round(nframes * acc / ncuts))
        bounds[-1] = nframes

        local_frame = 0
        seen_still_in_row: dict[str, int] = {}
        for (asset, _), a, b in zip(merged, bounds, bounds[1:]):
            nf = b - a
            if nf <= 0:
                continue
            path = Path(asset["local_path"])
            is_video = asset.get("kind") == "native_video"
            off = 0.0
            up = 1.0
            cfrac = 1.0
            z_max = 1.045
            if is_video:
                info = probe(path)
                need = nf / FPS
                spans = video_used.setdefault(str(path), [])
                # Skip 0.0-0.5s black fade-in on KSC launch/separation videos (J2383 §5.1 #4)
                off = 2.0 if path.name.startswith("ksc_011906_") else 0.0
                while True:
                    end = off + need
                    legal = end <= info["duration"] + 0.08 and all(
                        abs(off - s) >= 10.0 and (off >= e - 0.05 or end <= s + 0.05)
                        for s, e in spans
                    )
                    if legal:
                        break
                    off += 10.0
                    if off + 0.5 > info["duration"]:
                        problems.append(
                            f"{row['row']}: {path.name} is {info['duration']:.2f}s, "
                            f"no legal {need:.2f}s stretch (used {spans})"
                        )
                        off = 2.0 if path.name.startswith("ksc_011906_") else 0.0
                        break
                spans.append((off, off + need))
                up = min(2.0, max(W / info["width"], H / info["height"]))
                src_w, src_h = info["width"], info["height"]
            else:
                use_n = seen_still_in_row.get(path.name, 0) + 1
                seen_still_in_row[path.name] = use_n
                cfrac = 0.88 if use_n >= 2 else 1.00
                src_w, src_h, z_max, up = _still_effective_size(asset, cfrac)

            ov = None
            ov_name = re.search(r"(overlay_034_r\d+_[a-z0-9_]+)", row["asset"])
            if ov_name:
                hits = list(GFX.rglob(ov_name.group(1) + ".mov"))
                ov = str(hits[0]) if hits else None
                if ov is None:
                    problems.append(f"{row['row']}: missing overlay {ov_name.group(1)}")

            cut_t0 = t0 + local_frame / FPS
            cuts.append({
                "row": row["row"], "kind": "NASA", "path": str(path),
                "source": path.name, "t0": cut_t0, "frames": nf,
                "overlay": ov, "overlay_ss": local_frame / FPS,
                "labels": labs, "credit": credit_for(asset, "NASA"),
                "offset": off if is_video else None,
                "upscale": round(up, 3),
                "video": is_video, "src_w": src_w, "src_h": src_h,
                "crop_frac": cfrac, "z_max": z_max,
            })
            local_frame += nf

    if problems:
        raise SystemExit("plan problems:\n" + "\n".join(problems))
    total_f = sum(c["frames"] for c in cuts)
    if total_f != TOTAL_FRAMES:
        drift = TOTAL_FRAMES - total_f
        cuts[-1]["frames"] += drift
        if cuts[-1]["frames"] <= 0:
            raise SystemExit(f"frame drift {drift} emptied the last cut")
    return cuts


def _lift_ycbcr(im: Image.Image) -> Image.Image:
    """Matches ffmpeg lutyuv=y='clip(val*0.78+58,0,255)' cleanly in RGB."""
    ycbcr = np.asarray(im.convert("YCbCr"), dtype=np.float32).copy()
    ycbcr[:, :, 0] = np.clip(ycbcr[:, :, 0] * 0.78 + 58.0, 0.0, 255.0)
    return Image.fromarray(ycbcr.astype(np.uint8), "YCbCr").convert("RGB")


def _apply_fine_grain(im: Image.Image) -> Image.Image:
    """Bakes subtle 2x2 spatial film grain onto dark backgrounds (studio/RULES.md Finishing §5)
    so dark nightside discs do not band under H.264 or confuse polish_gate's centre-patch FFT."""
    arr = np.asarray(im, dtype=np.float32).copy()
    rng = np.random.default_rng(34034)
    g_small = rng.normal(0.0, 3.2, (H // 2, W // 2)).astype(np.float32)
    grain = np.repeat(np.repeat(g_small, 2, axis=0), 2, axis=1)
    luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    weight = np.clip((115.0 - luma) / 55.0, 0.25, 1.0)
    arr += (grain * weight)[:, :, None]
    return Image.fromarray(np.clip(np.round(arr), 0, 255).astype(np.uint8), "RGB")


def _prepare_still_base(cut: dict, stars_im: Image.Image) -> Image.Image:
    """Builds a 1920x1080 RGB base image with 2D separable min(fx, fy) 48px feather when inset."""
    src = Path(cut["path"])
    im = Image.open(src).convert("RGB")
    if src.name in CLEAN_CROPS:
        im = im.crop(CLEAN_CROPS[src.name])
    cfrac = float(cut.get("crop_frac") or 1.0)
    if cfrac < 0.999:
        cw = max(2, int(round(im.width * cfrac)))
        ch = max(2, int(round(im.height * cfrac)))
        x0 = (im.width - cw) // 2
        y0 = (im.height - ch) // 2
        im = im.crop((x0, y0, x0 + cw, y0 + ch))

    im = _lift_ycbcr(im)
    sw, sh = im.size
    cover = max(W / sw, H / sh)
    z_max = float(cut.get("z_max") or 1.045)

    if cover <= 2.0 and cover * z_max <= 2.002:
        tw = max(W, int(round(sw * cover)))
        th = max(H, int(round(sh * cover)))
        scaled = im.resize((tw, th), Image.Resampling.LANCZOS)
        x0 = (tw - W) // 2
        y0 = (th - H) // 2
        return _apply_fine_grain(scaled.crop((x0, y0, x0 + W, y0 + H)))

    # Starfield-framed inset with true 2D separable 48px edge feather (fixes J2383 48x48 corner glitch)
    fit = min(1.998 / z_max, (W - 120) / sw, (H - 120) / sh)
    tw = max(4, int(round(sw * fit)) // 2 * 2)
    th = max(4, int(round(sh * fit)) // 2 * 2)
    fg = np.asarray(im.resize((tw, th), Image.Resampling.LANCZOS), dtype=np.float32)
    bg = np.asarray(stars_im, dtype=np.float32).copy()

    feather = min(48.0, tw / 4.0, th / 4.0)
    fx = np.minimum(np.arange(tw, dtype=np.float32) / feather, (tw - 1 - np.arange(tw, dtype=np.float32)) / feather)
    fy = np.minimum(np.arange(th, dtype=np.float32) / feather, (th - 1 - np.arange(th, dtype=np.float32)) / feather)
    fx = np.clip(fx, 0.0, 1.0)
    fy = np.clip(fy, 0.0, 1.0)
    # Smooth cosine ramp on separable min(fx, fy): 0 along all 4 outer borders, zero corner step
    alpha = np.minimum(fx[None, :], fy[:, None])
    alpha = (0.5 - 0.5 * np.cos(np.pi * alpha))[:, :, None]

    ox = (W - tw) // 2
    oy = (H - th) // 2
    patch = bg[oy : oy + th, ox : ox + tw]
    patch[:] = patch * (1.0 - alpha) + fg * alpha
    return _apply_fine_grain(Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB"))


def _decorate_ffmpeg(cut: dict, inputs: list[str], base: str, n: int) -> tuple[str, str]:
    """Overlays transparent .mov graphic, bottom-left credit, and lower-third labels (y >= 800)."""
    parts = []
    cur = base
    idx = sum(1 for tok in inputs if tok == "-i")

    if cut.get("overlay"):
        ss = float(cut.get("overlay_ss") or 0.0)
        ov_y = 55 if cut.get("row") == "R17" else 0
        inputs.extend(["-ss", f"{ss:.3f}", "-i", cut["overlay"]])
        parts.append(f"[{cur}][{idx}:v]overlay=0:{ov_y}:format=auto:eof_action=pass[ov{idx}]")
        cur = f"ov{idx}"
        idx += 1

    credit = cut.get("credit") or ""
    if credit:
        png = WORK / "credits" / f"{credit}.png"
        if not png.exists():
            text_png(credit, png, 28, False)
        inputs.extend(["-loop", "1", "-i", str(png)])
        parts.append(f"[{cur}][{idx}:v]overlay=36:H-h-28:format=auto:shortest=1[cr{idx}]")
        cur = f"cr{idx}"
        idx += 1

    t0 = cut["t0"]
    t1 = t0 + n / FPS
    placed_intervals: list[tuple[float, float]] = []
    seen = set()
    for text, a, b in cut.get("labels") or []:
        if b <= t0 + 0.04 or a >= t1 - 0.04 or text in seen:
            continue
        seen.add(text)
        slug = hashlib.md5(text.encode("utf-8")).hexdigest()[:12]
        png = WORK / "labels" / f"lbl_{slug}.png"
        if not png.exists():
            text_png(text, png, 52, True)
        local_a = max(0.0, a - t0)
        local_b = min(n / FPS, b - t0)
        hold = max(0.25, local_b - local_a)
        # Only fade in if label begins inside this cut; only fade out if label ends inside this cut
        fade_ops = ["format=rgba"]
        if a >= t0 - 0.02:
            fade_ops.append("fade=t=in:st=0:d=0.30:alpha=1")
        if b <= t1 + 0.02 and hold > 0.32:
            fade_ops.append(f"fade=t=out:st={max(0.05, hold - 0.30):.3f}:d=0.30:alpha=1")
        fade_ops.append(f"setpts=PTS+{local_a:.3f}/TB")

        inputs.extend(["-loop", "1", "-t", f"{hold + 0.05:.3f}", "-i", str(png)])
        parts.append(f"[{idx}:v]{','.join(fade_ops)}[lb{idx}]")
        # Keep lower-third pills at H-h-112 (y >= 800 > 796 centre patch, and >= 40px above H-h-28 credit)
        overlaps_prev = any(not (b <= pa + 0.05 or a >= pb - 0.05) for pa, pb in placed_intervals)
        placed_intervals.append((a, b))
        y_expr = "H-h-204" if overlaps_prev else "H-h-112"
        parts.append(f"[{cur}][lb{idx}]overlay=x=(main_w-overlay_w)/2:y={y_expr}:format=auto:eof_action=pass[lbx{idx}]")
        cur = f"lbx{idx}"
        idx += 1

    if not parts:
        return "", f"[{cur}]"
    return ";" + ";".join(parts), f"[{cur}]"


def render_still(cut: dict, dest: Path, stars: Path) -> None:
    """Symmetric sub-pixel PIL Image.Transform.EXTENT BICUBIC zoom piped into ffmpeg."""
    n = cut["frames"]
    stars_im = Image.open(stars).convert("RGB")
    base_im = _prepare_still_base(cut, stars_im)
    z_max = float(cut.get("z_max") or 1.045)

    # First encode clean sub-pixel zoomed base video, or pipe directly into decorate filtergraph
    inputs = ["-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0"]
    vf = "[0:v]format=yuv420p[base]"
    extra_vf, out_pad = _decorate_ffmpeg(cut, inputs, "base", n)

    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", *inputs,
        "-filter_complex", vf + extra_vf, "-map", out_pad,
        *ENC, "-frames:v", str(n), str(dest),
    ]
    proc = sp.Popen(cmd, stdin=sp.PIPE, stderr=sp.PIPE)
    assert proc.stdin is not None
    denom = float(max(1, n - 1))
    try:
        for fi in range(n):
            z = 1.0 + (z_max - 1.0) * (fi / denom)
            cw, ch = W / z, H / z
            left, top = (W - cw) * 0.5, (H - ch) * 0.5
            fr = base_im.transform((W, H), Image.Transform.EXTENT, (left, top, left + cw, top + ch), Image.Resampling.BICUBIC)
            proc.stdin.write(fr.tobytes())
        proc.stdin.close()
        err = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
        rc = proc.wait()
        if rc != 0:
            raise RuntimeError(f"render_still failed ({rc}) on {dest.name}: {err[-1200:]}")
    except BaseException:
        proc.kill()
        proc.wait()
        raise


def _video_plate_fix(name: str, sw: int, sh: int, off: float = 0.0) -> tuple[str, str, int, int]:
    """Per-clip crop and luma lift ported from verified v01 master (J2376), with offset-aware flyby curve."""
    crop = ""
    lift = "lutyuv=y='clip(val*0.78+58,0,255)'"
    if name == "ksc_011906_nh_launch.mp4":
        crop = "crop=590:448:106:0,"
        sw, sh = 590, 448
    elif "Approach_to_Arrokoth" in name:
        crop = "crop=500:476:150:0,"
        sw, sh = 500, 476
    elif "Pluto_System_As_Seen" in name:
        lift = "lutyuv=y='clip(val*4+32,0,255)'"
    elif "Pluto_Flyby" in name:
        if off >= 18.0:
            # At 20.0-24.0s raw luma is 132..151 (p95 164..167); stretch contrast cleanly without black-crush
            lift = "lutyuv=y='clip((val-140)*2.4+120,0,255)'"
        else:
            lift = "lutyuv=y='clip((val-210)*4+160,0,255)'"
    elif "Charon_orbiting" in name:
        lift = "lutyuv=y='clip(val*4+32,0,255)',noise=alls=12:allf=t"
    return crop, lift, sw, sh


def render_video(cut: dict, dest: Path, stars: Path) -> None:
    n = cut["frames"]
    src = Path(cut["path"])
    info = probe(src)
    sw, sh = info["width"], info["height"]
    off = float(cut["offset"] or 0.0)
    if "51712771431" in src.name:
        inputs = ["-y", "-ss", f"{off:.3f}", "-i", str(src), "-loop", "1", "-i", str(stars)]
        vf = (
            f"[1:v]scale={W}:{H},fps={FPS},format=gbrp[bg];"
            f"[0:v]tpad=stop_mode=clone:stop_duration=0.25,crop=1028:840:0:0,scale=1320:1080:flags=lanczos,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,fps={FPS},format=gbrp[fg];"
            f"[bg][fg]blend=all_mode=screen:shortest=1,format=yuv420p[base]"
        )
    else:
        crop, lift, sw, sh = _video_plate_fix(src.name, sw, sh, off)
        cover = max(W / sw, H / sh)
        inputs = ["-y", "-ss", f"{off:.3f}", "-i", str(src)]
        src_chain = f"[0:v]tpad=stop_mode=clone:stop_duration=0.25,{crop}"
        if cover <= 2.0:
            vf = (
                f"{src_chain}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                f"{lift},fps={FPS},setsar=1,format=yuv420p[base]"
            )
        else:
            fit = min(2.0, (W - 80) / sw, (H - 80) / sh)
            tw, th = max(2, int(sw * fit) // 2 * 2), max(2, int(sh * fit) // 2 * 2)
            feather = max(120, int(min(tw, th) * 0.14))
            vf = (
                f"{src_chain}split=2[vbg][vfg];"
                f"[vbg]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{lift},"
                f"gblur=sigma=28,eq=saturation=0.9,fps={FPS},format=yuv444p[bg];"
                f"[vfg]scale={tw}:{th}:flags=lanczos,{lift},fps={FPS},format=rgba,"
                f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
                f"a='clip(min(min(X,{tw}-X),min(Y,{th}-Y))*255/{feather},0,255)'[fg];"
                f"[bg][fg]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:format=auto,setsar=1,format=yuv420p[base]"
            )
    extra_vf, out_pad = _decorate_ffmpeg(cut, inputs, "base", n)
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", *inputs,
        "-filter_complex", vf + extra_vf, "-map", out_pad,
        *ENC, "-frames:v", str(n), str(dest),
    ]
    run(cmd)


def render_graphic(cut: dict, dest: Path, stars: Path | None = None) -> None:
    n = cut["frames"]
    if stars is not None and cut["kind"] == "CODE":
        inputs = ["-y", "-i", cut["path"], "-loop", "1", "-i", str(stars)]
        vf = (
            f"[0:v]tpad=stop_mode=clone:stop_duration=0.25,scale={W}:{H},fps={FPS},setsar=1,format=gbrp[fg];"
            f"[1:v]scale={W}:{H},fps={FPS},format=gbrp[bg];"
            f"[fg][bg]blend=all_expr='if(gt(Y,920),max(A,B*0.85),A)':shortest=1,format=yuv420p[base]"
        )
        cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", *inputs,
            "-filter_complex", vf, "-map", "[base]",
            *ENC, "-frames:v", str(n), str(dest),
        ]
        run(cmd)
        return
    lift_card = ",lutyuv=y='clip(val+10,0,255)'" if cut["kind"] == "CARD" else ""
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", cut["path"],
        "-vf", f"tpad=stop_mode=clone:stop_duration=0.25,scale={W}:{H},fps={FPS},setsar=1{lift_card},format=yuv420p",
        *ENC, "-frames:v", str(n), str(dest),
    ]
    run(cmd)


def _render_one_cut(args: tuple[int, dict, Path, Path]) -> tuple[int, str]:
    i, cut, dest, stars = args
    if frames_ok(dest, cut["frames"]):
        return i, f"keep {dest.name}"
    if cut["kind"] in {"CODE", "CARD"}:
        render_graphic(cut, dest, stars)
    elif cut["video"]:
        render_video(cut, dest, stars)
    else:
        render_still(cut, dest, stars)
    return i, f"done {i + 1} {cut['row']} {cut['frames']}f {cut['source']}"


def render_all(cuts: list[dict], workers: int = 6) -> list[Path]:
    stars = WORK / "starfield.jpg"
    starfield(stars)
    # Pre-build all label and credit PNGs sequentially to avoid worker race conditions
    for c in cuts:
        cr = c.get("credit") or ""
        if cr:
            p = WORK / "credits" / f"{cr}.png"
            if not p.exists():
                text_png(cr, p, 28, False)
        for text, _, _ in c.get("labels") or []:
            slug = hashlib.md5(text.encode("utf-8")).hexdigest()[:12]
            p = WORK / "labels" / f"lbl_{slug}.png"
            if not p.exists():
                text_png(text, p, 52, True)

    out_dir = WORK / "cuts"
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = [out_dir / f"{i:03d}_{c['row']}.mp4" for i, c in enumerate(cuts)]
    tasks = [(i, c, paths[i], stars) for i, c in enumerate(cuts)]

    with cf.ProcessPoolExecutor(max_workers=workers) as ex:
        for idx_done, (_, msg) in enumerate(ex.map(_render_one_cut, tasks), 1):
            if idx_done % 15 == 0 or idx_done == len(tasks):
                print(f"[{idx_done}/{len(tasks)}] {msg}", flush=True)
    return paths


def concat_picture(paths: list[Path], dest: Path) -> None:
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in paths))
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy", "-an", str(dest),
    ])


def lay_vo(dest: Path) -> None:
    """Splices out 2.000..4.800s, inserts +1.000/+0.900/+0.900s in R04-R07, and places
    all 6 chapter-card silences at prev_word_raw_end + 0.600s in pure 48kHz stereo PCM."""
    v01_data = json.loads(WORDS_V01.read_text())
    words = [w for w in v01_data["words"] if w.get("type") == "word"]

    chapter_gaps: list[tuple[float, float]] = []
    prev_shift = float(words[0]["start"]) - float(words[0]["raw_start"])
    for w_prev, w_cur in zip(words, words[1:]):
        shift = float(w_cur["start"]) - float(w_cur["raw_start"])
        if shift - prev_shift > 0.4:
            at_raw = round(float(w_prev["raw_end"]) + 0.600, 3)
            chapter_gaps.append((at_raw, round(shift - prev_shift, 6)))
            prev_shift = shift

    assert len(chapter_gaps) == 6, f"Expected 6 chapter gaps, found {len(chapter_gaps)}: {chapter_gaps}"

    with wave.open(str(VO_WAV), "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        sw = w.getsampwidth()
        assert sr == SR and ch == 2 and sw == 2
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").reshape(-1, 2).astype(np.float32)

    # Smooth 8 ms fade helper at slice edges (all inside <-74 dB silence)
    fade_n = int(0.008 * SR)
    ramp_in = np.linspace(0.0, 1.0, fade_n, dtype=np.float32)[:, None]
    ramp_out = np.linspace(1.0, 0.0, fade_n, dtype=np.float32)[:, None]

    def grab(t_a: float, t_b: float) -> np.ndarray:
        s0 = int(round(t_a * SR))
        s1 = int(round(t_b * SR))
        seg = pcm[s0:s1].copy()
        if len(seg) > fade_n * 2:
            seg[:fade_n] *= ramp_in
            seg[-fade_n:] *= ramp_out
        return seg

    def sil(dur_s: float) -> np.ndarray:
        return np.zeros((int(round(dur_s * SR)), 2), dtype=np.float32)

    # Ordered raw-time insertion events after 4.800s:
    # 3 opening inter-sentence restorations (+1.000s, +0.900s, +0.900s = +2.800s) + 6 chapter silences
    insertions = [
        (39.300, 1.000),
        (54.000, 0.900),
        (60.550, 0.900),
        *chapter_gaps,
    ]
    insertions.sort(key=lambda x: x[0])

    pieces: list[np.ndarray] = [
        grab(0.000, 2.000),  # "Across Pluto's horizon," (removing 2.000..4.800s "in distant orbit around our sun,")
    ]
    cur_raw = 4.800
    raw_end_s = len(pcm) / SR
    for ins_at, ins_dur in insertions:
        pieces.append(grab(cur_raw, ins_at))
        pieces.append(sil(ins_dur))
        cur_raw = ins_at
    pieces.append(grab(cur_raw, raw_end_s))

    out = np.concatenate(pieces, axis=0)
    target_samples = TOTAL_FRAMES * (SR // FPS)  # 19,408 * 1,600 = 31,052,800 samples
    if len(out) < target_samples:
        out = np.concatenate([out, np.zeros((target_samples - len(out), 2), dtype=np.float32)], axis=0)
    else:
        out = out[:target_samples]

    dest.parent.mkdir(parents=True, exist_ok=True)
    out_i16 = np.clip(np.round(out), -32768, 32767).astype("<i2")
    with wave.open(str(dest), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(out_i16.tobytes())


def build_sfx(dest: Path) -> None:
    rumble = KIT / "sfx_owb_rumble_low_v01.wav"
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"

    def read_s(p: Path) -> np.ndarray:
        with wave.open(str(p), "rb") as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32)
            ch = w.getnchannels()
            a = a.reshape(-1, ch)
            if ch == 1:
                a = np.repeat(a, 2, axis=1)
            return a

    r_pcm = read_s(rumble)
    w_pcm = read_s(whoosh)
    t_pcm = read_s(tick)

    target_samples = TOTAL_FRAMES * (SR // FPS)
    buf = np.zeros((target_samples, 2), dtype=np.float32)

    def place(sample: np.ndarray, start_s: float, max_dur_s: float, gain: float) -> None:
        i0 = int(round(start_s * SR))
        take = min(len(sample), int(round(max_dur_s * SR)), target_samples - i0)
        if i0 >= 0 and take > 0:
            buf[i0 : i0 + take] += sample[:take] * gain

    for a, b in RUMBLES:
        place(r_pcm, a, min(3.4, b - a), 0.045)
    for t in WHOOSHES:
        place(w_pcm, t, 0.75, 0.10)
    for t in TICKS:
        place(t_pcm, t, 0.12, 0.07)

    dest.parent.mkdir(parents=True, exist_ok=True)
    out_i16 = np.clip(np.round(buf), -32768, 32767).astype("<i2")
    with wave.open(str(dest), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(out_i16.tobytes())


def loudness(path: Path) -> tuple[float, float]:
    p = sp.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-af", "ebur128=framelog=verbose:peak=true", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    text = p.stderr
    integ = re.search(r"Integrated loudness:\s+I:\s+(-?[\d.]+) LUFS", text)
    peak = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBTP", text)
    if not integ:
        raise RuntimeError(text[-500:])
    tp = float(peak.group(1)) if peak else -1.0
    return float(integ.group(1)), tp


def mix(vo: Path, sfx: Path, dest: Path) -> dict:
    """Mixes VO + ducked score bed + house SFX to ~-14.2 LUFS and <= -1.2 dBTP."""
    vo_i, _ = loudness(vo)
    bed_i, _ = loudness(BED)
    bed_gain_db = (vo_i - 22.0) - bed_i
    sfx_i, _ = loudness(sfx)
    sfx_gain_db = min(0.0, (vo_i - 16.0) - sfx_i)

    bed_laid = WORK / "bed_laid_v02.wav"
    sfx_laid = WORK / "sfx_laid_v02.wav"
    dur_str = f"{TOTAL:.6f}"

    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(BED),
        "-af", f"volume={bed_gain_db:.2f}dB,apad=whole_dur={dur_str},atrim=0:{dur_str}",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(bed_laid),
    ])
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(sfx),
        "-af", f"volume={sfx_gain_db:.2f}dB,atrim=0:{dur_str}",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(sfx_laid),
    ])
    premix = WORK / "premix_v02.wav"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(vo), "-i", str(sfx_laid), "-i", str(bed_laid),
        "-filter_complex",
        f"[0:a][1:a][2:a]amix=inputs=3:normalize=0:dropout_transition=0,atrim=0:{dur_str}[a]",
        "-map", "[a]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(premix),
    ])
    mix_i, _ = loudness(premix)
    gain = -14.0 - mix_i
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(premix),
        "-af", f"aresample=192000,volume={gain:.2f}dB,alimiter=limit=0.78:level=false,aresample=48000,atrim=0:{dur_str}",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dest),
    ])
    final_i, final_tp = loudness(dest)

    # Preserve stems in PACK on studio-live so sfx_kit level can always be re-run
    PACK.mkdir(parents=True, exist_ok=True)
    shutil.copy2(vo, PACK / "vo_laid_v02.wav")
    shutil.copy2(sfx_laid, PACK / "sfx_laid_v02.wav")
    shutil.copy2(bed_laid, PACK / "bed_laid_v02.wav")

    return {
        "vo_lufs": vo_i, "bed_gain_db": round(bed_gain_db, 2),
        "sfx_gain_db": round(sfx_gain_db, 2), "premix_lufs": mix_i,
        "gain_db": round(gain, 2), "integrated_lufs": final_i, "true_peak_dbtp": final_tp,
    }


def mux(picture: Path, audio: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(picture), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(dest),
    ])


def write_sidecars(cuts: list[dict]) -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    cut_json = []
    for c in cuts:
        item = {
            "row": c["row"],
            "source": c["source"],
            "timeline_in": round(c["t0"], 3),
            "timeline_out": round(c["t0"] + c["frames"] / FPS, 3),
            "upscale": c["upscale"] if c["kind"] == "NASA" else 1.0,
            "video": bool(c["video"]),
        }
        if c["video"]:
            item["framing"] = {"offset": float(c["offset"] or 0.0)}
        cut_json.append(item)
    (PACK / "cuts_v02.json").write_text(json.dumps(cut_json, indent=2) + "\n")

    items = []
    for a in json.loads(POOL.read_text())["assets"]:
        title = a.get("title") or a["id"]
        items.append({"id": Path(a["local_path"]).name, "file": Path(a["local_path"]).name, "title": title})
    (PACK / "pool_titles_v02.json").write_text(json.dumps(items, indent=2) + "\n")


def run_gates() -> dict:
    PACK.mkdir(parents=True, exist_ok=True)
    results: dict = {}

    clip = sp.run([
        sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/clip_check.py"),
        str(SHOT), "--words", str(WORDS),
    ], capture_output=True, text=True)
    results["clip_check"] = {"code": clip.returncode, "out": (clip.stdout or clip.stderr)[-600:]}

    pq = sp.run([
        sys.executable, str(REPO / "scripts/picture_qa.py"), str(OUT),
        "--cuts", str(PACK / "cuts_v02.json"),
        "--pool", str(PACK / "pool_titles_v02.json"),
        "--pool", str(POOL),
        "--out-dir", str(PACK),
    ], capture_output=True, text=True)
    results["picture_qa"] = {"code": pq.returncode, "out": (pq.stdout or pq.stderr)[-1000:]}

    pg = sp.run([
        sys.executable, str(REPO / "scripts/polish_gate.py"), str(OUT),
        "--cuts", str(PACK / "cuts_v02.json"),
        "--out", str(PACK / "polish_gate_v02.json"),
    ], capture_output=True, text=True)
    results["polish_gate"] = {"code": pg.returncode, "out": (pg.stdout or pg.stderr)[-1000:]}

    others = [
        str(d) for d in sorted((REPO / "02_Video-Projects").glob("*/05_Music"))
        if not d.parent.name.startswith("034")
    ]
    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
    if uat.is_dir():
        others.append(str(uat))
    mg = sp.run([
        sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
        "--bed", str(BED), "--video", str(OUT),
        *(["--others", *others] if others else []),
        "--out", str(PACK / "music_gate_v02.json"),
    ], capture_output=True, text=True)
    results["music_gate"] = {"code": mg.returncode, "out": (mg.stdout or mg.stderr)[-1000:]}

    lv = sp.run([
        sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
        "--vo", str(PACK / "vo_laid_v02.wav"),
        "--sfx", str(PACK / "sfx_laid_v02.wav"),
        "--bed", str(PACK / "bed_laid_v02.wav"),
        "--minutes", "10.78",
        "--out", str(PACK / "sfx_level_v02.json"),
    ], capture_output=True, text=True)
    results["sfx_level"] = {"code": lv.returncode, "out": (lv.stdout or lv.stderr)[-800:]}

    i, tp = loudness(OUT)
    black = sp.run([
        "ffmpeg", "-hide_banner", "-i", str(OUT),
        "-vf", "blackdetect=d=0.04:pix_th=0.10", "-f", "null", "-",
    ], capture_output=True, text=True)
    blacks = [ln for ln in black.stderr.splitlines() if "black_start" in ln]
    info = probe(OUT)
    results["delivery"] = {
        "integrated_lufs": i,
        "true_peak_dbtp": tp,
        "width": info["width"],
        "height": info["height"],
        "duration": info["duration"],
        "nb_frames": info.get("nb_frames"),
        "avg_frame_rate": info.get("avg_frame_rate"),
        "black_frames": blacks[:8],
        "sha256": sha256_file(OUT),
        "bytes": OUT.stat().st_size,
    }
    (PACK / "gate_results_v02.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2), flush=True)
    return results


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    os.environ["TMPDIR"] = str(WORK / "tmp")
    (WORK / "tmp").mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "--all"

    rows = load_rows()
    pool = load_pool()
    cuts = build_plan(rows, pool)
    (WORK / "plan_v02.json").write_text(json.dumps(cuts, indent=2) + "\n")
    write_sidecars(cuts)
    print(f"plan: {len(cuts)} cuts, {sum(c['frames'] for c in cuts)} frames", flush=True)
    if mode == "--plan":
        return

    paths = render_all(cuts, workers=8)
    picture = WORK / "picture_v02.mp4"
    concat_picture(paths, picture)

    vo = WORK / "vo_laid_v02.wav"
    sfx = WORK / "sfx_stem_v02.wav"
    mix_wav = WORK / "mix_v02.wav"
    print("lay vo", flush=True)
    lay_vo(vo)
    print("build sfx", flush=True)
    build_sfx(sfx)
    print("mix", flush=True)
    report = mix(vo, sfx, mix_wav)
    PACK.mkdir(parents=True, exist_ok=True)
    (PACK / "mix_report_v02.json").write_text(json.dumps(report, indent=2) + "\n")
    print("mux", report, flush=True)
    mux(picture, mix_wav, OUT)

    if mode in ("--gates", "--all"):
        results = run_gates()
        failed = [k for k, v in results.items() if isinstance(v, dict) and v.get("code") not in (None, 0)]
        delivery = results.get("delivery") or {}
        if delivery.get("black_frames"):
            failed.append("black_frames")
        if not (-15.5 <= delivery.get("integrated_lufs", -99) <= -12.5):
            failed.append("loudness")
        if delivery.get("true_peak_dbtp", 0) > -1.0:
            failed.append("true_peak")
        code = 1 if failed else 0
        print(f"done {code} failed={failed}", flush=True)
        raise SystemExit(code)


if __name__ == "__main__":
    main()
