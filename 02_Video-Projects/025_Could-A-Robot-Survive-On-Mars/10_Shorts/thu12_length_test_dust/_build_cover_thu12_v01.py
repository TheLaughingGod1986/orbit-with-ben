#!/usr/bin/env python3
"""025 Thu 12 Nov length-test Short cover (J0134): white SAVED BY / yellow WIND, no Orbit, centre stack in the v04
house look. Plate: the Short's own opening shot (PIA22909) as the locked master shows it at 256.5 s, centre-cropped
608x1080 like the Short (1.78x). The NASA panorama itself has black mosaic edges at 9:16. Stack sized to fill at least
60% of the width (THUMBNAIL_AND_TITLE_RULES §Shorts) and kept inside the 16:9 crop band."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import ImageDraw

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
import build_yellow_white_short_thumbs_v04 as v04  # noqa: E402

MASTER = FILM / "09_Final-Export/025_MarsRobot_full_rough_v03f.mp4"
PLATE_T = 256.5
OUT = HERE / "08_Covers"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plate = OUT / "_plate_pia22909.png"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(PLATE_T), "-i", str(MASTER),
                    "-frames:v", "1", "-vf", f"crop=608:1080:656:0,scale={v04.W}:{v04.H}:flags=lanczos", str(plate)],
                   check=True)
    im = v04.cover_plate(plate)
    draw = ImageDraw.Draw(im)
    lines, yellow = ["SAVED BY", "WIND"], {"WIND"}
    hero = v04.fit_font(draw, lines[0], int(v04.W * 0.80), start=300)
    sub = v04.fit_font(draw, lines[1], int(v04.W * 0.80), start=int(v04.line_size(hero) * 1.4))
    fonts = [hero, sub]
    # advance by the glyph bottom from the draw origin: at these sizes the top bearing is large
    boxes = [draw.textbbox((0, 0), ln, font=f, stroke_width=v04.STROKE) for ln, f in zip(lines, fonts)]
    tops = [b[1] for b in boxes]
    heights = [b[3] for b in boxes]
    widths = [b[2] - b[0] for b in boxes]
    gap = 8
    block = sum(heights) + gap - tops[0]
    y = -tops[0] + max(int(v04.H * 0.36), min((v04.H - block) // 2, int(v04.H * 0.64) - block))
    for ln, f, hh in zip(lines, fonts, heights):
        v04.draw_line_words(draw, y, ln.split(" "), yellow, f)
        y += hh + gap
    out = OUT / "cover_thu12_length_test_dust.jpg"
    im.save(out, quality=93, optimize=True)
    plate.unlink()
    print(out, f"stack {max(widths) / v04.W:.0%} of width, block {block}px")


if __name__ == "__main__":
    main()
