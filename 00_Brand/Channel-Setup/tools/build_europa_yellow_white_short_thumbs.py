#!/usr/bin/env python3
"""Build Europa Short thumbs: yellow highlight + white rest, vertical-centre stack.

UAT: ORBIT_HOUSE_AND_UAT_BIBLE.md (yellow lock 1 Sep 2026 + clip gate 31 Aug).
Does not upload — Studio / YouTube OAuth required to apply.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
EP = ROOT / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts"
PLATE = EP / "08_Thumbs/plates/long_maxres.jpg"
OUT = EP / "08_Thumbs/yellow_white_v01"

RELATED = "NbW5G1BpPY0"
SHORTS = [
    ("FbRFvSApfOQ", "2026-09-03T20:00:00+01:00", ["MORE WATER", "THAN EARTH"], {"MORE", "WATER"}),
    ("EcsunqhN0jQ", "2026-09-04T11:30:00+01:00", ["THIS OCEAN", "SHOULDN'T EXIST"], {"SHOULDN'T", "EXIST"}),
    ("k0PjH2I0OxY", "2026-09-05T11:30:00+01:00", ["WHAT WOULD", "LIFE EAT?"], {"LIFE", "EAT?"}),
    ("0eqTVgrlU-s", "2026-09-06T11:30:00+01:00", ["LIFE WITHOUT", "SUNLIGHT"], {"WITHOUT", "SUNLIGHT"}),
    ("Fv-lSwB_Z-o", "2026-09-07T11:30:00+01:00", ["AN OCEAN", "IN SPACE"], {"OCEAN", "SPACE"}),
    ("KPO68c-U42E", "2026-09-08T11:30:00+01:00", ["ALREADY", "FLYING"], {"ALREADY", "FLYING"}),
    ("gN2qAv8m9Wc", "2026-09-09T11:30:00+01:00", ["COULD WE", "KILL IT?"], {"KILL", "IT?"}),
    ("TE_HDKAnqms", "2026-09-10T11:30:00+01:00", ["LIFE UNDER", "ICE"], {"LIFE", "UNDER"}),
]

W, H = 1080, 1920
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_PATH = next(
    p
    for p in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    )
    if Path(p).exists()
)


def make_plate(base: Image.Image, i: int) -> Image.Image:
    bw, bh = base.size
    crop_h = bh
    crop_w = int(crop_h * (W / H))
    if crop_w > bw:
        crop_w = bw
        crop_h = int(crop_w / (W / H))
    max_x = max(1, bw - crop_w)
    x0 = int((i / max(1, len(SHORTS) - 1)) * max_x)
    y0 = min(max(0, (bh - crop_h) // 2 + (i - 3) * 8), max(0, bh - crop_h))
    crop = base.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((W, H), Image.Resampling.LANCZOS)
    dark = ImageEnhance.Brightness(crop).enhance(0.72 - i * 0.02)
    overlay = Image.new("RGB", (W, H), (0, 0, 0))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle((0, int(H * 0.28), W, int(H * 0.72)), fill=160)
    mask = mask.filter(ImageFilter.GaussianBlur(60))
    dark = Image.composite(Image.blend(dark, overlay, 0.55), dark, mask)
    dark = ImageEnhance.Color(dark).enhance(1.05 + (i % 3) * 0.05)
    return ImageEnhance.Contrast(dark).enhance(1.15)


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_w: int, start: int = 150) -> ImageFont.FreeTypeFont:
    size = start
    while size > 48:
        font = ImageFont.truetype(FONT_PATH, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_w:
            return font
        size -= 4
    return ImageFont.truetype(FONT_PATH, 48)


def draw_line_words(draw, y, words, yellow_words, font):
    space = draw.textbbox((0, 0), " ", font=font)[2]
    widths = [
        draw.textbbox((0, 0), w, font=font)[2] - draw.textbbox((0, 0), w, font=font)[0]
        for w in words
    ]
    total = sum(widths) + space * (len(words) - 1)
    x = (W - total) // 2
    yellow_norm = {yw.upper().strip("?") for yw in yellow_words}
    for w, ww in zip(words, widths):
        color = YELLOW if w.upper().strip("?") in yellow_norm else WHITE
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx or dy:
                    draw.text((x + dx, y + dy), w, font=font, fill=BLACK)
        draw.text((x, y), w, font=font, fill=color)
        x += ww + space


def main() -> None:
    if not PLATE.exists():
        raise SystemExit(f"Missing plate: {PLATE}")
    OUT.mkdir(parents=True, exist_ok=True)
    base = Image.open(PLATE).convert("RGB")
    manifest = []
    for i, (vid, when, lines, yellow) in enumerate(SHORTS):
        im = make_plate(base, i)
        draw = ImageDraw.Draw(im)
        fonts = [fit_font(draw, line, int(W * 0.86)) for line in lines]
        heights = [
            draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]
            for line, font in zip(lines, fonts)
        ]
        gap = 28
        block = sum(heights) + gap * (len(lines) - 1)
        y = max(int(H * 0.22), min((H - block) // 2, int(H * 0.78) - block))
        for line, font, hh in zip(lines, fonts, heights):
            draw_line_words(draw, y, line.split(" "), yellow, font)
            y += hh + gap
        out = OUT / f"cover_{vid}.jpg"
        im.save(out, quality=92, optimize=True)
        manifest.append(
            {
                "id": vid,
                "schedule_uk": when,
                "hook": " / ".join(lines),
                "file": out.name,
                "yellow": sorted(yellow),
            }
        )
        print("wrote", out)
    (OUT / "MANIFEST.json").write_text(
        json.dumps(
            {
                "related": RELATED,
                "note": "Yellow+white centre-safe covers. Apply in Studio or via YouTube thumbnails.set.",
                "shorts": manifest,
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
