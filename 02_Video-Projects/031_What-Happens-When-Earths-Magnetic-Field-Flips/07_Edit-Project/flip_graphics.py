#!/usr/bin/env python3
"""R2 and R12 flip plates. £0. Schematic magnet on a real Earth photograph.

The disc is the already-harvested NASA Blue Marble eastern hemisphere
(GSFC_20171208_Archive_e001788). It is a real body, not a flat colour disc
and not a pole-path map. The bar magnet and the blue air ring are our drawing.
The ring stays outside the disc for the whole shot: the air is not stripped.
N and S are the pole marks from the shot list. No KEEP or composite review.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from mechanism_graphics import W, H, FPS, NAVY, WHITE, GOLD, BLUE, RED, ease
from evidence_graphics import caption, main as render

EARTH_NAME = 'GSFC_20171208_Archive_e001788.jpg'
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
_EARTH = None

SPECS = [
    dict(row=2, mode='flip', variant='question', start_s=12.54, duration_s=4.56,
         source_rows=[1], alpha=False, cue='Will',
         geometry='Real Blue Marble disc, schematic bar magnet rotating half a turn, '
                  'air ring held outside the disc. Not a geographic pole map.',
         requires='Motion review and Chief acceptance. Does not replace the R1 pole-speed overlay.'),
    dict(row=12, mode='flip', variant='upside', start_s=112.98, duration_s=3.32,
         source_rows=[4], alpha=False, cue='turned',
         geometry='Tighter real Blue Marble disc and the same schematic half-turn. '
                  'Not the later core dive.',
         requires='Motion review and Chief acceptance. Real Blue Marble limb plate still separates this from R11.'),
]


def earth_source():
    global _EARTH
    if _EARTH is not None:
        return _EARTH
    roots = [
        Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/'
             '031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/harvest_v01'),
        Path(__file__).resolve().parent / 'harvest_v01',
    ]
    for root in roots:
        path = root / EARTH_NAME
        if path.is_file():
            im = Image.open(path).convert('RGB')
            im.thumbnail((900, 900), Image.Resampling.LANCZOS)
            _EARTH = im
            return _EARTH
    raise FileNotFoundError(EARTH_NAME)


def earth_disc(diameter, spin):
    rot = earth_source().rotate(-spin, resample=Image.Resampling.BICUBIC, expand=False)
    inset = int(rot.width * 0.14)
    src = rot.crop((inset, inset, rot.width - inset, rot.height - inset))
    disc = src.resize((diameter, diameter), Image.Resampling.LANCZOS).convert('RGBA')
    mask = Image.new('L', (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((1, 1, diameter - 2, diameter - 2), fill=255)
    disc.putalpha(mask)
    return disc


def pole_mark(base, xy, text, colour):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype(FONT, 54)
    draw.text(xy, text, font=font, anchor='mm', fill=colour)
    base.alpha_composite(layer)


def frame(spec, t):
    im = Image.new('RGBA', (W, H), NAVY + (255,))
    dr = ImageDraw.Draw(im)
    for x in range(0, W, 80):
        dr.line((x, 0, x, H), fill=(32, 52, 75))
    for y in range(0, H, 80):
        dr.line((0, y, W, y), fill=(32, 52, 75))
    tight = spec['variant'] == 'upside'
    cx, cy = (960, 540)
    radius = 340 if tight else 280
    # Air ring sits just outside the body and never collapses.
    for i, extra in enumerate((10, 24, 38)):
        r = radius + extra
        tone = (120, 196, 255, 170 - i * 40)
        dr.ellipse((cx - r, cy - r, cx + r, cy + r), outline=tone, width=8)
    disc = earth_disc(radius * 2, t * 10)
    im.paste(disc, (cx - radius, cy - radius), disc)
    dr = ImageDraw.Draw(im)
    # Half turn only: the red end starts at the top of the frame and finishes at the bottom.
    angle = math.pi * ease((t - 0.35) / (1.7 if tight else 2.1))
    reach = radius + 78
    ux, uy = math.sin(angle), -math.cos(angle)
    vx, vy = math.cos(angle), math.sin(angle)
    half = 22

    def end(along, side):
        return (cx + along * ux + side * vx, cy + along * uy + side * vy)

    dr.polygon([end(reach, half), end(reach, -half), end(0, -half), end(0, half)], fill=RED)
    dr.polygon([end(0, half), end(0, -half), end(-reach, -half), end(-reach, half)], fill=WHITE)
    dr.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=GOLD)
    pole_mark(im, end(reach + 48, 0), 'N', RED)
    pole_mark(im, end(-reach - 48, 0), 'S', WHITE)
    credit = ImageDraw.Draw(im)
    credit.text((48, 1008), 'NASA', font=ImageFont.truetype(FONT, 28), fill=(210, 214, 220))
    # Upper left stays clear of the pole letters, which pass through the top and bottom.
    if tight:
        caption(credit, (300, 150), 'UPSIDE DOWN', 52, GOLD, t, 1.45, 3.05)
    else:
        caption(credit, (300, 150), 'OUR AIR', 56, WHITE, t, 2.7, 3.55)
        caption(credit, (300, 150), 'INTO SPACE', 52, GOLD, t, 3.7, 4.4)
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
