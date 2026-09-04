#!/usr/bin/env python3
"""Astrum-inspired Short covers: ALL-CAPS heavy sans, size hierarchy, black dead space.

Steal from Astrum: caps punch, one highlight colour, kicker line bigger, picture on black.
Keep Orbit house: yellow (not cyan) + white, vertical-centre stack, both lines survive
Studio preview + Shorts-list 16:9 crop, no Orbit, 3–6 words.

UAT: ORBIT_HOUSE_AND_UAT_BIBLE.md. Does not upload. Does not change dates.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
W, H = 1080, 1920
YELLOW = (255, 230, 0)  # house yellow — Astrum uses cyan; we do not
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STROKE = 4
BAR = int(H * 0.09)

EU = ROOT / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs"
NS = ROOT / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs"
LS = ROOT / "02_Video-Projects/005_The-Last-Star-In-The-Universe/10_Shorts/08_Thumbs"

# hero = which line is the bigger Astrum-style subject (ANDROMEDA / MOON / WHAT?)
JOBS = [
    {
        "id": "FbRFvSApfOQ",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-03T11:30:00+01:00",
        "role": "thu_upcoming_europa",
        "plate": EU / "plates_v02/FbRFvSApfOQ.png",
        "out_dir": EU / "yellow_white_v04",
        "lines": ["MORE WATER", "THAN EARTH"],
        "yellow": {"MORE", "WATER"},
        "hero": 0,
    },
    {
        "id": "eVp9a7f4rWg",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-03T20:00:00+01:00",
        "role": "thu_launch_europa",
        "plate": EU / "plates_v02/eVp9a7f4rWg.png",
        "out_dir": EU / "yellow_white_v04",
        "lines": ["COULD WE", "KILL IT?"],
        "yellow": {"KILL", "IT?"},
        "hero": 1,
    },
    {
        "id": "8Bym-yrYhGc",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-04T11:30:00+01:00",
        "role": "europa_daily",
        "plate": EU / "plates_v02/8Bym-yrYhGc.png",
        "out_dir": EU / "yellow_white_v04",
        "lines": ["THIS OCEAN", "SHOULDN'T EXIST"],
        "yellow": {"SHOULDN'T", "EXIST"},
        "hero": 1,
    },
    {
        "id": "1glQuYFSaYQ",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-05T11:30:00+01:00",
        "role": "europa_daily",
        "plate": EU / "plates_v02/1glQuYFSaYQ.png",
        "out_dir": EU / "yellow_white_v04",
        "lines": ["WHAT WOULD", "LIFE EAT?"],
        "yellow": {"LIFE", "EAT?"},
        "hero": 1,
    },
    {
        "id": "Xza_jSHD4qw",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-06T11:30:00+01:00",
        "role": "europa_daily",
        "plate": EU / "plates_v02/Xza_jSHD4qw.png",
        "out_dir": EU / "yellow_white_v04",
        "lines": ["LIFE WITHOUT", "SUNLIGHT"],
        "yellow": {"SUNLIGHT"},
        "hero": 1,
    },
    {
        "id": "VE0f186WQZo",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-07T11:30:00+01:00",
        "role": "europa_daily",
        "plate": EU / "plates_v02/VE0f186WQZo.png",
        "out_dir": EU / "yellow_white_v04",
        "lines": ["AN OCEAN", "IN SPACE"],
        "yellow": {"IN", "SPACE"},
        "hero": 1,
    },
    {
        "id": "D3KSYrqip5A",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-08T11:30:00+01:00",
        "role": "europa_daily",
        "plate": EU / "plates_v02/D3KSYrqip5A.png",
        "out_dir": EU / "yellow_white_v04",
        "lines": ["ALREADY", "FLYING"],
        "yellow": {"ALREADY"},
        "hero": 0,
    },
    {
        "id": "TE_HDKAnqms",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-09T11:30:00+01:00",
        "role": "europa_daily",
        "plate": EU / "plates_v02/TE_HDKAnqms.png",
        "out_dir": EU / "yellow_white_v04",
        "lines": ["LIFE UNDER", "ICE"],
        "yellow": {"ICE"},
        "hero": 1,
    },
    {
        "id": "92vmMxSNmlk",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-10T11:30:00+01:00",
        "role": "thu_upcoming_neutron",
        "plate": NS / "plates_v02/92vmMxSNmlk.png",
        "out_dir": NS / "yellow_white_v04",
        "lines": ["CAN'T STAND", "ON IT"],
        "yellow": {"CAN'T", "STAND"},
        "hero": 0,
    },
    {
        "id": "vCxXTYXSSqY",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-11T11:30:00+01:00",
        "role": "neutron_daily",
        "plate": NS / "plates_v02/vCxXTYXSSqY.png",
        "out_dir": NS / "yellow_white_v04",
        "lines": ["A TEASPOON", "OF MOUNTAINS"],
        "yellow": {"OF", "MOUNTAINS"},
        "hero": 1,
    },
    {
        "id": "va5ATScn3rs",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-12T11:30:00+01:00",
        "role": "neutron_daily",
        "plate": NS / "plates_v02/va5ATScn3rs.png",
        "out_dir": NS / "yellow_white_v04",
        "lines": ["THE SKY", "WOULD LEAN"],
        "yellow": {"WOULD", "LEAN"},
        "hero": 1,
    },
    {
        "id": "o7ykyTDZKiE",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-13T11:30:00+01:00",
        "role": "neutron_daily",
        "plate": NS / "plates_v02/o7ykyTDZKiE.png",
        "out_dir": NS / "yellow_white_v04",
        "lines": ["LAST CLEAR", "IMAGE"],
        "yellow": {"IMAGE"},
        "hero": 1,
    },
    {
        "id": "Rp_8J6_6IIk",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-14T11:30:00+01:00",
        "role": "neutron_daily",
        "plate": NS / "plates_v02/Rp_8J6_6IIk.png",
        "out_dir": NS / "yellow_white_v04",
        "lines": ["CRUSHES YOU", "TOO FAST"],
        "yellow": {"CRUSHES", "YOU"},
        "hero": 0,
    },
    {
        "id": "3QrICn9Kp00",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-15T11:30:00+01:00",
        "role": "neutron_mystery",
        "plate": NS / "plates_v02/3QrICn9Kp00.png",
        "out_dir": NS / "yellow_white_v04",
        "lines": ["LIGHT LEAVES", "EXHAUSTED"],
        "yellow": {"EXHAUSTED"},
        "hero": 1,
    },
    {
        "id": "mAAMsbhm88w",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-16T11:30:00+01:00",
        "role": "neutron_mystery",
        "plate": NS / "plates_v02/mAAMsbhm88w.png",
        "out_dir": NS / "yellow_white_v04",
        "lines": ["COULD A PROBE", "GET CLOSER?"],
        "yellow": {"GET", "CLOSER?"},
        "hero": 1,
    },
    {
        "id": "0j_pgYbCe5E",
        "related": "REXYxuLOBoI",
        "uk": "2026-09-18T11:30:00+01:00",
        "role": "last_star_leftover_locked_date",
        "plate": LS / "plates_v02/0j_pgYbCe5E.png",
        "out_dir": LS / "yellow_white_v04",
        "lines": ["DOESN'T END", "WHERE YOU THINK"],
        "yellow": {"DOESN'T", "END"},
        "hero": 0,
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
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = ImageEnhance.Color(im).enhance(1.08)
    overlay = Image.new("RGB", (W, H), (0, 0, 0))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle((0, int(H * 0.28), W, int(H * 0.72)), fill=175)
    mask = mask.filter(ImageFilter.GaussianBlur(80))
    im = Image.composite(Image.blend(im, overlay, 0.50), im, mask)
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, W, BAR), fill=BLACK)
    draw.rectangle((0, H - BAR, W, H), fill=BLACK)
    return im


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_w: int, start: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > 44:
        font = ImageFont.truetype(FONT_PATH, size)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=STROKE)
        if bbox[2] - bbox[0] <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT_PATH, 44)


def line_size(font: ImageFont.FreeTypeFont) -> int:
    return int(getattr(font, "size", 44))


def draw_line_words(draw, y, words, yellow_words, font):
    space = draw.textbbox((0, 0), " ", font=font, stroke_width=STROKE)[2]
    widths = [
        draw.textbbox((0, 0), w, font=font, stroke_width=STROKE)[2]
        - draw.textbbox((0, 0), w, font=font, stroke_width=STROKE)[0]
        for w in words
    ]
    total = sum(widths) + space * (len(words) - 1)
    x = (W - total) // 2
    yellow_norm = {yellow_key(yw) for yw in yellow_words}
    for w, ww in zip(words, widths):
        color = YELLOW if yellow_key(w) in yellow_norm else WHITE
        draw.text((x + 3, y + 5), w, font=font, fill=BLACK, stroke_width=STROKE, stroke_fill=BLACK)
        draw.text((x, y), w, font=font, fill=color, stroke_width=STROKE, stroke_fill=BLACK)
        x += ww + space


def compose(job: dict) -> dict:
    im = cover_plate(job["plate"])
    draw = ImageDraw.Draw(im)
    lines = job["lines"]
    hero = int(job.get("hero", 1))
    max_w = int(W * 0.90)
    starts = [168 if i == hero else 102 for i in range(len(lines))]
    fonts = [fit_font(draw, line, max_w, start=s) for line, s in zip(lines, starts)]
    # Keep setup clearly smaller than the Astrum hero line.
    hero_px = line_size(fonts[hero])
    fonts = [
        font if i == hero else fit_font(draw, line, max_w, start=min(line_size(font), int(hero_px * 0.62)))
        for i, (line, font) in enumerate(zip(lines, fonts))
    ]
    heights = [
        draw.textbbox((0, 0), line, font=font, stroke_width=STROKE)[3]
        - draw.textbbox((0, 0), line, font=font, stroke_width=STROKE)[1]
        for line, font in zip(lines, fonts)
    ]
    gap = 14
    block = sum(heights) + gap * (len(lines) - 1)
    # Vertical centre, inside 16:9 crop band (~y 656–1264 on 1920).
    y = max(int(H * 0.36), min((H - block) // 2, int(H * 0.64) - block))
    for line, font, hh in zip(lines, fonts, heights):
        draw_line_words(draw, y, line.split(" "), job["yellow"], font)
        y += hh + gap
    out_dir: Path = job["out_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"cover_{job['id']}.jpg"
    im.save(out, quality=93, optimize=True)
    return {
        "id": job["id"],
        "file": str(out),
        "hook": " / ".join(lines),
        "yellow": sorted(job["yellow"]),
        "hero": hero,
        "related": job["related"],
        "uk": job["uk"],
        "role": job["role"],
        "plate": str(job["plate"]),
    }


def main() -> None:
    import os

    if not Path(FONT_PATH).exists():
        raise SystemExit(f"Missing font: {FONT_PATH}")
    only = {x.strip() for x in os.environ.get("ONLY_IDS", "").split(",") if x.strip()}
    jobs = [j for j in JOBS if not only or j["id"] in only]
    if not jobs:
        raise SystemExit("No jobs matched ONLY_IDS")
    missing = [j["id"] for j in jobs if not j["plate"].exists()]
    if missing:
        raise SystemExit(f"Missing plates: {missing}")
    manifest = [compose(j) for j in jobs]
    by_dir: dict[str, list] = {}
    for row in manifest:
        d = str(Path(row["file"]).parent)
        by_dir.setdefault(d, []).append(row)
        print("wrote", row["file"])
    for d, rows in by_dir.items():
        Path(d, "MANIFEST.json").write_text(
            json.dumps(
                {
                    "version": "yellow_white_v04",
                    "note": "Astrum-inspired ALL-CAPS Arial Black, hero line bigger, black letterbox, yellow kicker (not cyan). Centre stack. Apply in Studio only — do not change dates.",
                    "shorts": rows,
                },
                indent=2,
            )
            + "\n"
        )


if __name__ == "__main__":
    main()
