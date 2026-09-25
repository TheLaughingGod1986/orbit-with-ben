#!/usr/bin/env python3
"""Composite yellow-highlight + white hooks onto per-id mysterious 9:16 plates.

UAT: ORBIT_HOUSE_AND_UAT_BIBLE.md — distinct plate, no Orbit, centre stack,
both lines survive Studio preview and Shorts-list 16:9 crop. Does not upload.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
W, H = 1080, 1920
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Live Studio cluster 2 Sep 2026. Do not use leftover duplicate ids.
JOBS = [
    {
        "id": "eVp9a7f4rWg",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-03T11:30:00+01:00",
        "role": "thu_upcoming_europa",
        "plate": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/plates_v02/eVp9a7f4rWg.png",
        "out_dir": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["COULD WE", "KILL IT?"],
        "yellow": {"COULD", "KILL", "IT?"},
    },
    {
        "id": "FbRFvSApfOQ",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-03T20:00:00+01:00",
        "role": "thu_launch_europa",
        "plate": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/plates_v02/FbRFvSApfOQ.png",
        "out_dir": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["MORE WATER", "THAN EARTH"],
        "yellow": {"MORE", "WATER"},
    },
    {
        "id": "8Bym-yrYhGc",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-04T11:30:00+01:00",
        "role": "europa_daily",
        "plate": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/plates_v02/8Bym-yrYhGc.png",
        "out_dir": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["THIS OCEAN", "SHOULDN'T EXIST"],
        "yellow": {"SHOULDN'T", "EXIST"},
    },
    {
        "id": "1glQuYFSaYQ",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-05T11:30:00+01:00",
        "role": "europa_daily",
        "plate": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/plates_v02/1glQuYFSaYQ.png",
        "out_dir": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["WHAT WOULD", "LIFE EAT?"],
        "yellow": {"LIFE", "EAT?"},
    },
    {
        "id": "Xza_jSHD4qw",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-06T11:30:00+01:00",
        "role": "europa_daily",
        "plate": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/plates_v02/Xza_jSHD4qw.png",
        "out_dir": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["LIFE WITHOUT", "SUNLIGHT"],
        "yellow": {"WITHOUT", "SUNLIGHT"},
    },
    {
        "id": "VE0f186WQZo",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-07T11:30:00+01:00",
        "role": "europa_daily",
        "plate": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/plates_v02/VE0f186WQZo.png",
        "out_dir": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["AN OCEAN", "IN SPACE"],
        "yellow": {"OCEAN", "SPACE"},
    },
    {
        "id": "D3KSYrqip5A",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-08T11:30:00+01:00",
        "role": "europa_daily",
        "plate": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/plates_v02/D3KSYrqip5A.png",
        "out_dir": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["ALREADY", "FLYING"],
        "yellow": {"ALREADY", "FLYING"},
    },
    {
        "id": "TE_HDKAnqms",
        "related": "NbW5G1BpPY0",
        "uk": "2026-09-09T11:30:00+01:00",
        "role": "europa_daily",
        "plate": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/plates_v02/TE_HDKAnqms.png",
        "out_dir": ROOT
        / "02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["LIFE UNDER", "ICE"],
        "yellow": {"LIFE", "UNDER"},
    },
    {
        "id": "92vmMxSNmlk",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-10T11:30:00+01:00",
        "role": "thu_upcoming_neutron",
        "plate": ROOT
        / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/plates_v02/92vmMxSNmlk.png",
        "out_dir": ROOT
        / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["CAN'T STAND", "ON IT"],
        "yellow": {"CAN'T", "STAND"},
    },
    {
        "id": "vCxXTYXSSqY",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-11T11:30:00+01:00",
        "role": "neutron_daily",
        "plate": ROOT
        / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/plates_v02/vCxXTYXSSqY.png",
        "out_dir": ROOT
        / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["A TEASPOON", "OUTWEIGHS MOUNTAINS"],
        "yellow": {"TEASPOON", "OUTWEIGHS"},
    },
    {
        "id": "va5ATScn3rs",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-12T11:30:00+01:00",
        "role": "neutron_daily",
        "plate": ROOT
        / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/plates_v02/va5ATScn3rs.png",
        "out_dir": ROOT
        / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["SKY WOULD", "LEAN"],
        "yellow": {"SKY", "LEAN"},
    },
    {
        "id": "o7ykyTDZKiE",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-13T11:30:00+01:00",
        "role": "neutron_daily",
        "plate": ROOT
        / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/plates_v02/o7ykyTDZKiE.png",
        "out_dir": ROOT
        / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["LAST CLEAR", "IMAGE"],
        "yellow": {"LAST", "CLEAR"},
    },
    {
        "id": "Rp_8J6_6IIk",
        "related": "Yk1tLh23rko",
        "uk": "2026-09-14T11:30:00+01:00",
        "role": "neutron_daily",
        "plate": ROOT
        / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/plates_v02/Rp_8J6_6IIk.png",
        "out_dir": ROOT
        / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["CRUSHES YOU", "TOO FAST"],
        "yellow": {"CRUSHES", "YOU"},
    },
    {
        "id": "0j_pgYbCe5E",
        "related": "REXYxuLOBoI",
        "uk": "2026-09-18T11:30:00+01:00",
        "role": "last_star_leftover_locked_date",
        "plate": ROOT
        / "02_Video-Projects/005_The-Last-Star-In-The-Universe/10_Shorts/08_Thumbs/plates_v02/0j_pgYbCe5E.png",
        "out_dir": ROOT
        / "02_Video-Projects/005_The-Last-Star-In-The-Universe/10_Shorts/08_Thumbs/yellow_white_v02",
        "lines": ["DOESN'T END", "WHERE YOU THINK"],
        "yellow": {"DOESN'T", "END"},
    },
]


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
    im = ImageEnhance.Color(im).enhance(1.06)
    # Darken the vertical centre so yellow/white type never sits on matching ice/water.
    overlay = Image.new("RGB", (W, H), (0, 0, 0))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle((0, int(H * 0.30), W, int(H * 0.70)), fill=150)
    mask = mask.filter(ImageFilter.GaussianBlur(72))
    return Image.composite(Image.blend(im, overlay, 0.42), im, mask)


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_w: int, start: int = 132) -> ImageFont.FreeTypeFont:
    size = start
    while size > 44:
        font = ImageFont.truetype(FONT_PATH, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_w:
            return font
        size -= 3
    return ImageFont.truetype(FONT_PATH, 44)


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
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx or dy:
                    draw.text((x + dx, y + dy), w, font=font, fill=BLACK)
        draw.text((x, y), w, font=font, fill=color)
        x += ww + space


def compose(job: dict) -> dict:
    im = cover_plate(job["plate"])
    draw = ImageDraw.Draw(im)
    lines = job["lines"]
    fonts = [fit_font(draw, line, int(W * 0.88)) for line in lines]
    heights = [
        draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]
        for line, font in zip(lines, fonts)
    ]
    gap = 26
    block = sum(heights) + gap * (len(lines) - 1)
    y = max(int(H * 0.34), min((H - block) // 2, int(H * 0.66) - block))
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
        "related": job["related"],
        "uk": job["uk"],
        "role": job["role"],
        "plate": str(job["plate"]),
    }


def main() -> None:
    if not Path(FONT_PATH).exists():
        raise SystemExit(f"Missing font: {FONT_PATH}")
    missing = [j["id"] for j in JOBS if not j["plate"].exists()]
    if missing:
        raise SystemExit(f"Missing plates: {missing}")
    manifest = [compose(j) for j in JOBS]
    by_dir: dict[str, list] = {}
    for row in manifest:
        d = str(Path(row["file"]).parent)
        by_dir.setdefault(d, []).append(row)
        print("wrote", row["file"])
    for d, rows in by_dir.items():
        Path(d, "MANIFEST.json").write_text(
            json.dumps(
                {
                    "version": "yellow_white_v02",
                    "note": "Per-id mysterious plates + yellow/white centre stack. Apply in Studio only.",
                    "shorts": rows,
                },
                indent=2,
            )
            + "\n"
        )


if __name__ == "__main__":
    main()
