#!/usr/bin/env python3
"""023 Venus long thumbnails A/B/C v01 (J0003, concepts due with the first cut).

Plate: NASA S91-50688 (Magellan radar global mosaic, 270 E), the disc lowered so its
bottom data-gap notch sits below frame. Words from the locked script v02: lead melts at
327 C vs the ~464 C surface (line 10), "The Twin Next Door" (ch. 1), "Where Did the Water Go?" (ch. 3).
Rules: THUMBNAIL_AND_TITLE_RULES.md §2 (near-black <=30%, ~12% line height, text off the
subject and out of the bottom-right, no Orbit). Title it sits under: "What Happened to Venus?".

  python3 _build_venus_thumbs_v01.py
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SRC = HERE.parent / "07_Edit-Project" / "nasa_pool_v01" / "harvest_v03" / "S91-50688.jpg"
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
LINE_H = 0.12
DISC_D = 740
DISC_CX = W - DISC_D // 2 - 20
DISC_TOP = 720 - int(DISC_D * 0.885)  # the notch (lowest ~11% of the disc) falls below frame
TEXT_X = 40
TEXT_MAX_W = DISC_CX - DISC_D // 2 - TEXT_X + 30

VARIANTS = [
    ("A", "melts-lead", ["MELTS", "LEAD"], "LEAD"),
    ("B", "earths-twin", ["EARTH'S", "TWIN"], "TWIN"),
    ("C", "wheres-the-water", ["WHERE'S", "THE", "WATER?"], "WATER?"),
]


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    sys.exit("Arial Black not found")


def disc() -> Image.Image:
    im = Image.open(SRC).convert("RGB")
    box = im.convert("L").point(lambda v: 255 if v > 20 else 0).getbbox()
    side = box[2] - box[0]  # the vertical bbox runs the full frame (scan edge), so the width is the disc
    cx, cy = (box[0] + box[2]) // 2, im.height // 2
    im = im.crop((cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2))
    im = im.resize((DISC_D, DISC_D), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.15)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))


def background() -> Image.Image:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx - DISC_CX, yy - (DISC_TOP + DISC_D / 2)) / (W * 0.8)
    glow = np.clip(1.0 - d, 0, 1) ** 1.6
    base = np.stack([20 + 110 * glow, 10 + 40 * glow, 18 + 8 * glow], axis=-1)
    rng = random.Random(23)
    img = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    stars = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(stars)
    for _ in range(380):
        x, y = rng.randrange(W), rng.randrange(H)
        r = 1 if rng.random() < 0.85 else 2
        sd.ellipse((x - r, y - r, x + r, y + r), fill=rng.randint(70, 210))
    stars = stars.filter(ImageFilter.GaussianBlur(0.6))
    return Image.composite(Image.new("RGB", (W, H), (255, 244, 225)), img, stars)


def compose() -> Image.Image:
    bg = background()
    tmp = Image.new("RGB", (W, H), BLACK)
    g = disc()
    mask = Image.new("L", g.size, 0)
    ImageDraw.Draw(mask).ellipse((2, 2, DISC_D - 3, DISC_D - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.5))
    tmp.paste(g, (DISC_CX - DISC_D // 2, DISC_TOP), mask)
    planet = Image.new("L", (W, H), 0)
    planet.paste(mask, (DISC_CX - DISC_D // 2, DISC_TOP))
    rim = np.asarray(tmp.filter(ImageFilter.GaussianBlur(36)), dtype=np.float32) * 0.7
    out = 255 - (255 - np.asarray(bg, dtype=np.float32)) * (255 - rim) / 255
    out = Image.fromarray(out.clip(0, 255).astype(np.uint8))
    return Image.composite(tmp, out, planet)


def fit(draw: ImageDraw.ImageDraw, lines: list[str]) -> ImageFont.FreeTypeFont:
    size = int(H * LINE_H / 0.72)
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
    y = (H - block) // 2 - cap[1] - 30
    for ln in lines:
        col = YELLOW if ln == hook else WHITE
        d.text((TEXT_X + 4, y + 5), ln, font=f, fill=BLACK, stroke_width=STROKE, stroke_fill=BLACK)
        d.text((TEXT_X, y), ln, font=f, fill=col, stroke_width=STROKE, stroke_fill=BLACK)
        y += cap_h + gap
    return {"font_size": f.size, "cap_px": cap_h, "cap_share": round(cap_h / H, 3)}


def near_black(img: Image.Image) -> float:
    return round(float((np.asarray(img.convert("L")) < 26).mean()), 3)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    base = compose()
    meta = {"source": "NASA S91-50688 (Magellan radar global mosaic)", "title": "What Happened to Venus?", "variants": []}
    paths = []
    for key, slug, lines, hook in VARIANTS:
        img = base.copy()
        info = draw_text(img, lines, hook)
        p = OUT / f"venus_thumb_{key}_{slug}.png"
        img.save(p, optimize=True)
        paths.append(p)
        meta["variants"].append({"key": key, "text": " ".join(lines), "yellow": hook,
                                 "file": p.name, "near_black": near_black(img), **info})
    sheet = OUT / "venus_thumbs_v01_small_size_check.jpg"
    subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
                    "long", *map(str, paths), "--out", str(sheet)], check=True)
    (OUT / "META.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
