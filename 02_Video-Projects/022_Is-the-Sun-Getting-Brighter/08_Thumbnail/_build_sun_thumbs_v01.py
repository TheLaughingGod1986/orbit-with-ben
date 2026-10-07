#!/usr/bin/env python3
"""022 Sun long thumbnails A/B/C v01 (J0020).

Plate: NASA SVS 11517 (SDO AIA 304, full disc with limb prominences) at 56.0 s.
Rules: THUMBNAIL_AND_TITLE_RULES.md §2 and §2.A (near-black <=30%, graded plate,
~12% line height, text off the subject and out of the bottom-right, no Orbit).

  python3 _build_sun_thumbs_v01.py
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SRC = HERE.parent / "04_Generated-Clips" / "svs" / "svs11517.mov"
SRC_T = 56.0
OUT = HERE / "abc_v01"
W, H = 1280, 720
FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/Library/Fonts/Arial Black.ttf",
]
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STROKE = 7
LINE_H = 0.12  # cap height per line as a share of frame height
DISC_D = 600
DISC_CX = W - DISC_D // 2 - 40
TEXT_X = 40
TEXT_MAX_W = DISC_CX - DISC_D // 2 - TEXT_X - 10

VARIANTS = [
    ("A", "burning-harder", ["BURNING", "HARDER"], "BURNING"),
    ("B", "its-climbing", ["IT'S", "CLIMBING"], "CLIMBING"),
    ("C", "running-down", ["RUNNING", "DOWN?"], "DOWN?"),
]


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    sys.exit("Arial Black not found")


def grab_plate() -> Image.Image:
    raw = OUT / "_plate_svs11517_56s.png"
    if not raw.exists():
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-ss", str(SRC_T), "-i", str(SRC),
             "-frames:v", "1", "-update", "1", str(raw)],
            check=True,
        )
    return Image.open(raw).convert("RGB")


def disc_crop(plate: Image.Image) -> tuple[Image.Image, int]:
    a = np.asarray(plate.convert("L"), dtype=np.float32)
    ys, xs = np.where(a > 60)
    cx, cy = int(np.median(xs)), int(np.median(ys))
    r = int(max(xs.max() - xs.min(), ys.max() - ys.min()) / 2)
    pad = int(r * 0.22)  # keep the limb prominences and inner corona
    box = (cx - r - pad, cy - r - pad, cx + r + pad, cy + r + pad)
    return plate.crop(box), r


def background() -> Image.Image:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx - DISC_CX, yy - H / 2) / (W * 0.75)
    glow = np.clip(1.0 - d, 0, 1) ** 1.6
    base = np.stack([
        18 + 120 * glow,
        8 + 46 * glow,
        22 + 10 * glow,
    ], axis=-1)
    rng = random.Random(22)
    img = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    stars = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(stars)
    for _ in range(420):
        x, y = rng.randrange(W), rng.randrange(H)
        b = rng.randint(70, 220)
        rad = 1 if rng.random() < 0.85 else 2
        sd.ellipse((x - rad, y - rad, x + rad, y + rad), fill=b)
    stars = stars.filter(ImageFilter.GaussianBlur(0.6))
    return Image.composite(Image.new("RGB", (W, H), (255, 244, 225)), img, stars)


def sun_layer(plate: Image.Image) -> Image.Image:
    crop, r = disc_crop(plate)
    scale = DISC_D / (2 * r)
    size = int(crop.width * scale)
    sun = crop.resize((size, size), Image.LANCZOS)
    sun = ImageEnhance.Color(sun).enhance(1.25)
    sun = ImageEnhance.Contrast(sun).enhance(1.15)
    sun = sun.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
    return sun


def compose(plate: Image.Image) -> Image.Image:
    bg = background()
    sun = sun_layer(plate)
    x0 = DISC_CX - sun.width // 2
    y0 = H // 2 - sun.height // 2
    canvas = np.asarray(bg, dtype=np.float32)
    layer = np.zeros_like(canvas)
    tmp = Image.new("RGB", (W, H), BLACK)
    tmp.paste(sun, (x0, y0))
    layer = np.asarray(tmp, dtype=np.float32)
    rim = np.asarray(tmp.filter(ImageFilter.GaussianBlur(38)), dtype=np.float32) * 0.9
    out = 255 - (255 - canvas) * (255 - layer) / 255  # screen the sun onto the glow
    out = 255 - (255 - out) * (255 - rim) / 255
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def fit(draw: ImageDraw.ImageDraw, lines: list[str]) -> ImageFont.FreeTypeFont:
    target_cap = int(H * LINE_H)
    size = int(target_cap / 0.72)
    while size > 40:
        f = font(size)
        if all(draw.textbbox((0, 0), ln, font=f, stroke_width=STROKE)[2] <= TEXT_MAX_W for ln in lines):
            return f
        size -= 2
    return font(size)


def draw_text(img: Image.Image, lines: list[str], hook: str) -> dict:
    d = ImageDraw.Draw(img)
    f = fit(d, lines)
    cap = d.textbbox((0, 0), "H", font=f)
    cap_h = cap[3] - cap[1]
    gap = int(cap_h * 0.32)
    block = len(lines) * cap_h + (len(lines) - 1) * gap
    y = (H - block) // 2 - cap[1] - 20
    for ln in lines:
        col = YELLOW if ln == hook else WHITE
        d.text((TEXT_X + 4, y + 5), ln, font=f, fill=BLACK, stroke_width=STROKE, stroke_fill=BLACK)
        d.text((TEXT_X, y), ln, font=f, fill=col, stroke_width=STROKE, stroke_fill=BLACK)
        y += cap_h + gap
    return {"font_size": f.size, "cap_px": cap_h, "cap_share": round(cap_h / H, 3)}


def near_black(img: Image.Image) -> float:
    a = np.asarray(img.convert("L"))
    return round(float((a < 26).mean()), 3)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    plate = grab_plate()
    base = compose(plate)
    meta = {"source": "NASA SVS 11517 (SDO AIA 304)", "source_t": SRC_T, "variants": []}
    paths = []
    for key, slug, lines, hook in VARIANTS:
        img = base.copy()
        info = draw_text(img, lines, hook)
        p = OUT / f"sun_thumb_{key}_{slug}.png"
        img.save(p, optimize=True)
        paths.append(p)
        meta["variants"].append({"key": key, "text": " ".join(lines), "yellow": hook,
                                 "file": p.name, "near_black": near_black(img), **info})
    sheet = OUT / "sun_thumbs_v01_small_size_check.jpg"
    subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
                    "long", *map(str, paths), "--out", str(sheet)], check=True)
    (OUT / "META.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
