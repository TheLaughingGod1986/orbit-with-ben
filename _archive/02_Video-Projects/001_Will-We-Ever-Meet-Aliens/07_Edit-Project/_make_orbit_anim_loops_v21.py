#!/usr/bin/env python3
"""v21 — Orbit blink + talk mouth animation loops (hard-alpha MOV).

For each emotion builds:
  loops/orbit_{emotion}_idle.mov   ~3.5s  (one natural blink, mouth closed)
  loops/orbit_{emotion}_talk.mov   ~0.8s  (mouth cycle + micro-blink)

Mouth is a small speaker LED under the visor — robotic lip-sync without a cartoon jaw.
"""
from __future__ import annotations

import importlib.util
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
BODY = ROOT / "04_Generated-Clips/03_Polished/orbit_narrator/rgba/orbit_body_master_v17.png"
OUT = ROOT / "04_Generated-Clips/03_Polished/orbit_narrator/rgba"
LOOPS = OUT / "loops"
PIP_H = 160
FPS = 30

# Import face-painting helpers from the expressive sprite builder
spec = importlib.util.spec_from_file_location("expr", EDIT / "_make_expressive_orbit_sprites.py")
expr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(expr)


def draw_mouth(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], open_amt: float):
    """Soft speaker LED under the visor. open_amt 0=closed, 1=fully open."""
    x0, y0, x1, y1 = box
    vw, vh = x1 - x0, y1 - y0
    cx = x0 + vw * 0.5
    cy = y1 + vh * 0.22
    # Closed: thin charcoal line; open: warm glowing capsule
    half_w = vw * (0.10 + 0.10 * open_amt)
    half_h = max(2.0, vh * (0.04 + 0.14 * open_amt))
    # outer glow when open
    if open_amt > 0.15:
        glow = int(90 + 110 * open_amt)
        draw.ellipse(
            [cx - half_w * 1.35, cy - half_h * 1.4, cx + half_w * 1.35, cy + half_h * 1.4],
            fill=(255, 140, 50, glow),
        )
    fill = (
        int(28 + 200 * open_amt),
        int(24 + 90 * open_amt),
        int(30 + 10 * open_amt),
        255,
    )
    draw.ellipse([cx - half_w, cy - half_h, cx + half_w, cy + half_h], fill=fill)
    if open_amt > 0.35:
        # inner bright core
        draw.ellipse(
            [cx - half_w * 0.45, cy - half_h * 0.35, cx + half_w * 0.45, cy + half_h * 0.35],
            fill=(255, 220, 140, 230),
        )


def apply_blink_lids(img: Image.Image, box: tuple[int, int, int, int], blink: float) -> Image.Image:
    """Close lids over each glowing eye only — never a full-visor charcoal slab."""
    if blink <= 0.02:
        return img
    arr = np.asarray(img.convert("RGBA")).copy()
    x0, y0, x1, y1 = box
    roi = arr[y0:y1, x0:x1]
    r = roi[:, :, 0].astype(np.int16)
    g = roi[:, :, 1].astype(np.int16)
    b = roi[:, :, 2].astype(np.int16)
    a = roi[:, :, 3]
    eye = (a > 200) & (r > 160) & (g > 120) & (b < 175) & ((r.astype(np.int32) - b) > 50)
    if int(eye.sum()) < 30:
        return img

    ys, xs = np.where(eye)
    mid = float(np.median(xs))
    out = img.copy()
    d = ImageDraw.Draw(out)
    lid = (14, 16, 24, 255)
    for side in (xs <= mid, xs > mid):
        if not np.any(side):
            continue
        sx, sy = xs[side], ys[side]
        ex0 = x0 + int(sx.min()) - 2
        ey0 = y0 + int(sy.min()) - 2
        ex1 = x0 + int(sx.max()) + 2
        ey1 = y0 + int(sy.max()) + 2
        eh = max(1, ey1 - ey0)
        # Top lid descends; at full blink also bottom lid rises
        top = int(eh * (0.15 + 0.75 * blink))
        d.ellipse([ex0, ey0, ex1, ey0 + max(2, top)], fill=lid)
        if blink > 0.55:
            bot = int(eh * 0.35 * (blink - 0.55) / 0.45)
            d.ellipse([ex0, ey1 - bot, ex1, ey1], fill=lid)
    return out


def paint_anim_frame(body: Image.Image, emotion: str, cfg: dict, blink: float, mouth: float) -> Image.Image:
    """Base expressive face + blink lids + talk mouth."""
    face = expr.paint_face(body, emotion, cfg)
    box2 = expr.find_visor(np.asarray(face))
    face = apply_blink_lids(face, box2, blink)
    d = ImageDraw.Draw(face)
    draw_mouth(d, box2, mouth)
    face = expr.harden(face)
    face = expr.crop_tight(face, pad=10)
    h = PIP_H
    w = max(1, int(round(face.width * (h / face.height))))
    scaled = face.resize((w, h), Image.Resampling.LANCZOS)
    # Re-harden AFTER resize — lanczos soft alpha was leaving a faint rectangular veil
    return expr.harden(scaled)


def blink_envelope(i: int, n: int, center: float = 0.62, width: float = 0.08) -> float:
    """Single blink pulse in a loop (triangular open→closed→open)."""
    t = i / max(1, n - 1)
    if abs(t - center) > width:
        return 0.0
    # 0 at edges of window, 1 at center
    return 1.0 - abs(t - center) / width


def mouth_cycle(i: int, period: int = 6) -> float:
    """Talk mouth open amount 0..1 over a short period."""
    phase = (i % period) / period
    # asymmetric: open faster, close softer
    return 0.15 + 0.85 * (0.5 - 0.5 * math.cos(2 * math.pi * phase))


def encode_loop(frames: list[Image.Image], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="orbit_loop_") as td:
        td = Path(td)
        for i, fr in enumerate(frames):
            fr.save(td / f"f_{i:04d}.png")
        # PNG codec MOV preserves straight alpha for overlay
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(FPS),
            "-i", str(td / "f_%04d.png"),
            "-c:v", "png", "-pix_fmt", "rgba",
            "-an", str(out),
        ], check=True)


def build_idle(body: Image.Image, emotion: str, cfg: dict) -> list[Image.Image]:
    n = int(FPS * 3.5)  # 3.5s
    frames = []
    for i in range(n):
        blink = blink_envelope(i, n, center=0.58, width=0.07)
        # tiny idle mouth breath
        mouth = 0.04 + 0.03 * math.sin(2 * math.pi * i / (FPS * 2.4))
        frames.append(paint_anim_frame(body, emotion, cfg, blink, mouth))
    return frames


def build_talk(body: Image.Image, emotion: str, cfg: dict) -> list[Image.Image]:
    n = int(FPS * 0.8)  # 0.8s
    frames = []
    for i in range(n):
        blink = blink_envelope(i, n, center=0.82, width=0.06) * 0.7  # softer/faster
        mouth = mouth_cycle(i, period=5)
        frames.append(paint_anim_frame(body, emotion, cfg, blink, mouth))
    return frames


def main() -> None:
    assert BODY.exists(), BODY
    body = expr.harden(Image.open(BODY))
    LOOPS.mkdir(parents=True, exist_ok=True)

    emotions = list(expr.EMOTIONS.keys())
    print(f"Building blink/talk loops for {len(emotions)} emotions…")
    for name, cfg in expr.EMOTIONS.items():
        idle_path = LOOPS / f"orbit_{name}_idle.mov"
        talk_path = LOOPS / f"orbit_{name}_talk.mov"
        print(f"  {name}…", end=" ", flush=True)
        encode_loop(build_idle(body, name, cfg), idle_path)
        encode_loop(build_talk(body, name, cfg), talk_path)
        print("ok")

    # alias
    for dst, src in (("surprised", "surprise"),):
        for mode in ("idle", "talk"):
            s = LOOPS / f"orbit_{src}_{mode}.mov"
            d = LOOPS / f"orbit_{dst}_{mode}.mov"
            if s.exists():
                shutil.copy2(s, d)

    # QC contact: first frame of each idle
    thumbs = []
    for name in emotions:
        # extract frame 0
        tmp = LOOPS / f"_qc_{name}.png"
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(LOOPS / f"orbit_{name}_idle.mov"),
            "-frames:v", "1", str(tmp),
        ], check=True)
        im = Image.open(tmp).convert("RGBA")
        bg = Image.new("RGBA", (160, 160), (12, 16, 28, 255))
        bg.paste(im, ((160 - im.width) // 2, (160 - im.height) // 2), im)
        thumbs.append(bg.convert("RGB"))
        tmp.unlink(missing_ok=True)
    sheet = Image.new("RGB", (160 * len(thumbs), 160), (12, 16, 28))
    for i, t in enumerate(thumbs):
        sheet.paste(t, (i * 160, 0))
    qc = LOOPS / "orbit_anim_contact_v21.png"
    sheet.save(qc)
    print(f"QC → {qc}")
    print(f"Loops → {LOOPS}")


if __name__ == "__main__":
    main()
