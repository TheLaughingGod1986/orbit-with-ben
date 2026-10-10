#!/usr/bin/env python3
"""025 Fri 13 Nov Short cover (J0103; Chief ruling #6101571703): yellow 1% / white AIR, no Orbit, centre stack in the
v04 house look. Plate: Valinor Hills under the thin Mars sky (PIA26237), the Short's "about 1%" shot, taken clean from
the NASA still so no burned-in captions sit under the words. v04's compose caps the hero at 168 px, which leaves
a two-word stack this short at about a quarter of the frame width, so the stack is sized here to fill at least 60%
(THUMBNAIL_AND_TITLE_RULES §Shorts) and kept inside the 16:9 crop band."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
import build_yellow_white_short_thumbs_v04 as v04  # noqa: E402

SRC = FILM / "07_Edit-Project/nasa_pool_v01/ingenuity/PIA26237.jpg"
OUT = HERE / "08_Covers"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plate = OUT / "_plate_valinor.png"
    with Image.open(SRC) as im:
        im = im.convert("RGB")
        sw, sh = im.size
        cw = min(sw, int(sh * v04.W / v04.H))
        x = int(max(0, min(sw - cw, 0.45 * sw - cw / 2)))
        im.crop((x, 0, x + cw, sh)).resize((v04.W, v04.H), Image.LANCZOS).save(plate)
    im = v04.cover_plate(plate)
    draw = ImageDraw.Draw(im)
    lines, yellow = ["1%", "AIR"], {"1%"}
    hero = v04.fit_font(draw, lines[0], int(v04.W * 0.61), start=420)
    sub = v04.fit_font(draw, lines[1], int(v04.W * 0.62), start=int(v04.line_size(hero) * 0.52))
    fonts = [hero, sub]
    # advance by the glyph bottom from the draw origin: at these sizes the top bearing is large
    tops = [draw.textbbox((0, 0), ln, font=f, stroke_width=v04.STROKE)[1] for ln, f in zip(lines, fonts)]
    heights = [draw.textbbox((0, 0), ln, font=f, stroke_width=v04.STROKE)[3] for ln, f in zip(lines, fonts)]
    widths = [draw.textbbox((0, 0), ln, font=f, stroke_width=v04.STROKE)[2]
              - draw.textbbox((0, 0), ln, font=f, stroke_width=v04.STROKE)[0] for ln, f in zip(lines, fonts)]
    gap = 8
    block = sum(heights) + gap - tops[0]
    y = -tops[0] + max(int(v04.H * 0.36), min((v04.H - block) // 2, int(v04.H * 0.64) - block))
    for ln, f, hh in zip(lines, fonts, heights):
        v04.draw_line_words(draw, y, ln.split(" "), yellow, f)
        y += hh + gap
    out = OUT / "cover_fri13_ingenuity_72.jpg"
    im.save(out, quality=93, optimize=True)
    plate.unlink()
    print(out, f"stack {max(widths) / v04.W:.0%} of width, block {block}px")

if __name__ == "__main__":
    main()
