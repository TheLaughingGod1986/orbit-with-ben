#!/usr/bin/env python3
"""MelodySheep-inspired 16:9 long thumbs.

Steal: cinematic plate, huge ALL-CAPS title + smaller subtitle, no mascot.
Keep house: yellow kicker / white rest, no Orbit, no generic CTA, no pill card.
Does not upload. Does not change dates.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
ASSETS = Path("/Users/ben/.cursor/projects/Users-ben-YouTube-orbit-with-ben/assets")
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
W, H = 1280, 720
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STROKE_TITLE = 5
STROKE_SUB = 3

EU_OUT = ROOT / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/08_Thumbnail/melodysheep_v01"
NS_OUT = ROOT / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/08_Thumbnail/melodysheep_v01"

JOBS = [
    {
        "id": "NbW5G1BpPY0",
        "variant": "A",
        "apply": True,
        "plate": ASSETS / "europa_long_plate_a_underice.png",
        "out_dir": EU_OUT,
        "title": ["LIFE UNDER", "THE ICE"],
        "title_yellow": {"LIFE", "ICE"},
        "sub": "MORE WATER THAN EARTH",
        "sub_yellow": set(),
        "align": "center",
        "y_frac": 0.52,
    },
    {
        "id": "NbW5G1BpPY0",
        "variant": "B",
        "apply": False,
        "plate": ASSETS / "europa_long_plate_b_jupiter.png",
        "out_dir": EU_OUT,
        "title": ["LIFE UNDER", "THE ICE"],
        "title_yellow": {"ICE"},
        "sub": "MORE WATER THAN EARTH",
        "sub_yellow": set(),
        "align": "center",
        "y_frac": 0.62,
    },
    {
        "id": "Yk1tLh23rko",
        "variant": "A",
        "apply": True,
        "plate": ASSETS / "neutron_long_plate_b_teaspoon.png",
        "out_dir": NS_OUT,
        "title": ["A TEASPOON", "OF MOUNTAINS"],
        "title_yellow": {"MOUNTAINS"},
        "sub": "NEAR A NEUTRON STAR",
        "sub_yellow": set(),
        "align": "left",
        "y_frac": 0.42,
    },
    {
        "id": "Yk1tLh23rko",
        "variant": "B",
        "apply": False,
        "plate": ASSETS / "neutron_long_plate_a_mountains.png",
        "out_dir": NS_OUT,
        "title": ["YOU CAN'T", "STAND ON IT"],
        "title_yellow": {"CAN'T", "STAND"},
        "sub": "NEAR A NEUTRON STAR",
        "sub_yellow": set(),
        "align": "left",
        "y_frac": 0.28,
    },
]


def yellow_key(word: str) -> str:
    return word.upper().strip("?")


def cover_plate(path: Path) -> Image.Image:
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    target_ratio = W / H
    src_ratio = sw / sh
    if src_ratio > target_ratio:
        new_w = int(sh * target_ratio)
        x0 = (sw - new_w) // 2
        src = src.crop((x0, 0, x0 + new_w, sh))
    else:
        new_h = int(sw / target_ratio)
        y0 = (sh - new_h) // 2
        src = src.crop((0, y0, sw, y0 + new_h))
    im = src.resize((W, H), Image.Resampling.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.05)
    overlay = Image.new("RGB", (W, H), (0, 0, 0))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle((0, int(H * 0.22), W, int(H * 0.82)), fill=120)
    mask = mask.filter(ImageFilter.GaussianBlur(48))
    return Image.composite(Image.blend(im, overlay, 0.28), im, mask)


def fit_font(draw, text: str, max_w: int, start: int, stroke: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > 28:
        font = ImageFont.truetype(FONT_PATH, size)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if bbox[2] - bbox[0] <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT_PATH, 28)


def line_wh(draw, text, font, stroke):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_words(draw, x, y, words, yellow_words, font, stroke, align_left_x=None):
    space = draw.textbbox((0, 0), " ", font=font, stroke_width=stroke)[2]
    widths = [line_wh(draw, w, font, stroke)[0] for w in words]
    total = sum(widths) + space * (len(words) - 1)
    if align_left_x is None:
        x = (W - total) // 2
    else:
        x = align_left_x
    yellow_norm = {yellow_key(yw) for yw in yellow_words}
    for w, ww in zip(words, widths):
        color = YELLOW if yellow_key(w) in yellow_norm else WHITE
        draw.text((x + 2, y + 3), w, font=font, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK)
        draw.text((x, y), w, font=font, fill=color, stroke_width=stroke, stroke_fill=BLACK)
        x += ww + space
    return total


def compose(job: dict) -> dict:
    im = cover_plate(job["plate"])
    draw = ImageDraw.Draw(im)
    title_lines = job["title"]
    max_w = int(W * 0.90) if job["align"] == "center" else int(W * 0.56)
    left_x = 56 if job["align"] == "left" else None
    fonts = [fit_font(draw, line, max_w, start=96 if i == 1 else 78, stroke=STROKE_TITLE) for i, line in enumerate(title_lines)]
    # Second title line is the MelodySheep hero (ANDROMEDA / UNIVERSE).
    hero = fonts[-1]
    fonts = [
        font if i == len(fonts) - 1 else fit_font(draw, line, max_w, start=min(int(getattr(hero, "size", 72) * 0.72), 78), stroke=STROKE_TITLE)
        for i, (line, font) in enumerate(zip(title_lines, fonts))
    ]
    heights = [line_wh(draw, line, font, STROKE_TITLE)[1] for line, font in zip(title_lines, fonts)]
    sub_font = fit_font(draw, job["sub"], max_w, start=34, stroke=STROKE_SUB)
    sub_h = line_wh(draw, job["sub"], sub_font, STROKE_SUB)[1]
    gap = 8
    sub_gap = 16
    block = sum(heights) + gap * (len(title_lines) - 1) + sub_gap + sub_h
    y = int(H * job["y_frac"] - block / 2)
    y = max(int(H * 0.12), min(y, int(H * 0.82) - block))
    for line, font, hh in zip(title_lines, fonts, heights):
        draw_words(draw, 0, y, line.split(" "), job["title_yellow"], font, STROKE_TITLE, left_x)
        y += hh + gap
    y += sub_gap - gap
    draw_words(draw, 0, y, job["sub"].split(" "), job["sub_yellow"], sub_font, STROKE_SUB, left_x)
    out_dir: Path = job["out_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    plate_dest = out_dir / f"plate_{job['variant'].lower()}_{job['id']}.png"
    if job["plate"].exists() and not plate_dest.exists():
        shutil.copy2(job["plate"], plate_dest)
    out = out_dir / f"cover_{job['variant']}_{job['id']}.jpg"
    im.save(out, quality=93, optimize=True)
    return {
        "id": job["id"],
        "variant": job["variant"],
        "apply": job["apply"],
        "file": str(out),
        "title": " / ".join(title_lines),
        "sub": job["sub"],
        "align": job["align"],
    }


def main() -> None:
    if not Path(FONT_PATH).exists():
        raise SystemExit(f"Missing font: {FONT_PATH}")
    missing = [j["variant"] + j["id"] for j in JOBS if not j["plate"].exists()]
    if missing:
        raise SystemExit(f"Missing plates: {missing}")
    rows = [compose(j) for j in JOBS]
    for row in rows:
        print("wrote", row["file"])
    EU_OUT.mkdir(parents=True, exist_ok=True)
    NS_OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "version": "melodysheep_v01",
        "note": "MelodySheep two-line ALL-CAPS on cinematic 16:9 plates. Yellow kicker, no Orbit, no pill. Apply A in Studio only.",
        "shorts": rows,
    }
    (EU_OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (NS_OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
