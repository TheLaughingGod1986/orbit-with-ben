#!/usr/bin/env python3
"""025 Mon 9 Nov Short cover (J0103; Chief ruling #6101571703): yellow TOO COLD / white FOR BATTERIES, no Orbit,
centre stack in the v04 house look, kept off "minus 90" (thumb C on the long uses it). Plate: frost on the Martian
ground (PIA11132), the Short's opening shot, taken clean from the NASA still. Sized like the Fri 13 cover."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
import build_yellow_white_short_thumbs_v04 as v04  # noqa: E402

SRC = FILM / "07_Edit-Project/nasa_pool_v01/frost/PIA11132.jpg"
OUT = HERE / "08_Covers"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plate = OUT / "_plate_frost.png"
    with Image.open(SRC) as im:
        im = im.convert("RGB")
        sw, sh = im.size
        cw = min(sw, int(sh * v04.W / v04.H))
        x = int(max(0, min(sw - cw, 0.5 * sw - cw / 2)))
        im.crop((x, 0, x + cw, sh)).resize((v04.W, v04.H), Image.LANCZOS).save(plate)
    im = v04.cover_plate(plate)
    draw = ImageDraw.Draw(im)
    lines, yellow = ["TOO COLD", "FOR BATTERIES"], {"TOO", "COLD"}
    hero = v04.fit_font(draw, lines[0], int(v04.W * 0.80), start=420)
    sub = v04.fit_font(draw, lines[1], int(v04.W * 0.80), start=int(v04.line_size(hero) * 0.60))
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
    out = OUT / "cover_mon09_night_cold.jpg"
    im.save(out, quality=93, optimize=True)
    plate.unlink()
    print(out, f"stack {max(widths) / v04.W:.0%} of width, block {block}px")


if __name__ == "__main__":
    main()
