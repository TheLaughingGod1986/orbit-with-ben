#!/usr/bin/env python3
"""Cover for the 020 Jupiter Short jupiter_no_crust_v01 (J0205). No spend.

The clean opening plate (master jupiter_film_v04.mp4 at 128.60 s, the Short's frame 0 without its caption),
reframed as the Short (centre crop 608x1080 -> 1080x1920), with the title's hook words "JUPITER HAS / NO GROUND"
(yellow NO GROUND) stacked at the centre, at least 60% of the frame width.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = Path(__file__).resolve().parent
MASTER = Path("/private/tmp/jupiter020_short_lift/jupiter_film_v04.mp4")
PIC_IN = 128.60
OUT = HERE / "08_Covers"
DEST = OUT / "cover_jupiter_no_crust_v01.jpg"
W, H = 1080, 1920
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255)
YELLOW = (255, 214, 0)
BLACK = (0, 0, 0)
ROWS = [("JUPITER HAS", WHITE), ("NO GROUND", YELLOW)]


def centred(draw, y, text, font, fill, stroke):
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=BLACK)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plate = OUT / "_plate0.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{PIC_IN:.3f}", "-i", str(MASTER), "-frames:v", "1",
                    "-vf", f"crop=608:1080:{(1920 - 608) // 2}:0,scale={W}:{H}:flags=lanczos", str(plate)],
                   check=True)
    im = ImageEnhance.Brightness(Image.open(plate).convert("RGB")).enhance(0.75)
    plate.unlink()
    d = ImageDraw.Draw(im)
    size = 60
    while max(d.textlength(r, font=ImageFont.truetype(FONT, size + 2)) for r, _ in ROWS) <= W * 0.80:
        size += 2
    f = ImageFont.truetype(FONT, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 20
    y = (H - lh * len(ROWS)) // 2
    for r, c in ROWS:
        centred(d, y, r, f, c, stroke=9)
        y += lh
    im.save(DEST, quality=92)
    print(DEST)


if __name__ == "__main__":
    main()
