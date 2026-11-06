#!/usr/bin/env python3
"""031 £0 opening and depth graphics. No approval implied.

poledrift and flip are full-frame explainers on a real NASA Earth disc.
The Canada-to-Siberia arc is a schematic, not a plotted pole survey.
layers and the 1905 place stamp are alpha overlays for graded moving plates.
Numbers are the locked shot-list / SOURCES figures only.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

from evidence_graphics import caption, main as render
from mechanism_graphics import BLUE, GOLD, NAVY, RED, W, H, WHITE, ease, label

EARTH = Path(
    '/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/'
    '031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/'
    'harvest_v01/GSFC_20171208_Archive_e000678.jpg'
)
EARTH_ID = 'GSFC_20171208_Archive_e000678'
_DISC = {}


SPECS = [
    dict(row=1, mode='poledrift', start_s=4.52, duration_s=3.82,
         source_rows=[1], alpha=False, cue='north',
         earth_nasa_id=EARTH_ID,
         geometry='Schematic arc on DSCOVR Earth; speed 55 km/yr from SOURCES row 1'),
    dict(row=2, mode='flip', start_s=12.54, duration_s=4.54,
         source_rows=[1], alpha=False, cue='Will',
         earth_nasa_id=EARTH_ID,
         geometry='Bar magnet turns over; atmosphere ring stays, never stripped'),
    dict(row=13, mode='layers', start_s=125.9, duration_s=5.86,
         source_rows=[6], alpha=True, cue='3,000',
         geometry='Depth counter to 3000 km; not a measured core cross-section'),
    dict(row=5, mode='when1905', start_s=36.14, duration_s=3.22,
         source_rows=[3], alpha=True, cue='1905,',
         geometry='Place and year stamp only; not the full film timeline'),
]


def disc(im, cx, cy, r):
    key = r
    if key not in _DISC:
        # Crop to the planet limb. The file has a black margin that would sit inside the circle.
        src = Image.open(EARTH).convert('RGBA').crop((220, 219, 1856, 1855))
        src = src.resize((r * 2, r * 2), Image.Resampling.LANCZOS)
        mask = Image.new('L', (r * 2, r * 2), 0)
        ImageDraw.Draw(mask).ellipse((1, 1, r * 2 - 2, r * 2 - 2), fill=255)
        src.putalpha(mask)
        _DISC[key] = src
    im.alpha_composite(_DISC[key], (cx - r, cy - r))


def grid(dr):
    for x in range(0, W, 80):
        dr.line((x, 0, x, H), fill=(32, 52, 75), width=1)
    for y in range(0, H, 80):
        dr.line((0, y, W, y), fill=(32, 52, 75), width=1)


def poledrift(im, t, spec):
    cx, cy, r = 960, 430, 300
    disc(im, cx, cy, r)
    dr = ImageDraw.Draw(im)
    dr.ellipse((cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16), outline=BLUE, width=8)
    s = ease(min(1, t / 2.8))

    def pt(u):
        # Leaves the Canadian Arctic on this Americas view and runs off the
        # top limb. Siberia is not on this plate, so its label sits past the limb.
        ang = math.radians(112 - 28 * u)
        rad = r * (0.72 + 0.42 * u)
        return (cx + rad * math.cos(ang), cy - rad * math.sin(ang))

    trail = [pt(s * i / 28) for i in range(29)]
    dr.line(trail, fill=GOLD, width=8)
    x, y = pt(s)
    dr.ellipse((x - 16, y - 16, x + 16, y + 16), fill=RED)
    label(dr, (pt(0)[0] - 20, pt(0)[1] + 40), 'CANADA', 36, WHITE)
    label(dr, (pt(1)[0] + 90, pt(1)[1]), 'SIBERIA', 36, WHITE)
    label(dr, (960, 860), '1831 → TODAY', 52, WHITE)
    label(dr, (960, 940), 'UP TO 55 KM/YR', 60, GOLD)
    label(dr, (960, 1010), '> MARATHON / YR', 44, WHITE)
    label(dr, (150, 70), 'NASA', 32, WHITE, anchor='lm')


def flip(im, t, spec):
    cx, cy, r = 960, 460, 300
    disc(im, cx, cy, r)
    dr = ImageDraw.Draw(im)
    # The air shell stays the same size for the whole shot.
    for extra, width in ((18, 10), (36, 5)):
        dr.ellipse((cx - r - extra, cy - r - extra, cx + r + extra, cy + r + extra), outline=BLUE, width=width)
    ang = math.pi * ease((t - 0.35) / 2.4)
    ux, uy = math.sin(ang), -math.cos(ang)
    half = r * 0.72
    x1, y1 = cx + half * ux, cy + half * uy
    x2, y2 = cx - half * ux, cy - half * uy
    dr.line((x1, y1, x2, y2), fill=(196, 160, 92), width=28)
    dr.ellipse((x1 - 26, y1 - 26, x1 + 26, y1 + 26), fill=RED)
    dr.ellipse((x2 - 26, y2 - 26, x2 + 26, y2 + 26), fill=WHITE)
    label(dr, (x1 + 54 * ux, y1 + 54 * uy), 'N', 48, RED)
    label(dr, (x2 - 54 * ux, y2 - 54 * uy), 'S', 48, WHITE)
    caption(dr, (960, 960), 'POLES SWAP', 64, GOLD, t, 0.45, 4.05)
    label(dr, (150, 70), 'NASA', 32, WHITE, anchor='lm')


def layers(im, t, spec):
    dr = ImageDraw.Draw(im)
    s = ease(min(1, t / 4.2))
    x, top, bot = 1420, 250, 860
    y = top + (bot - top) * s
    disc(im, x, 130, 78)
    dr.line((x, top, x, bot), fill=(180, 196, 214, 90), width=4)
    dr.line((x, top, x, y), fill=GOLD, width=10)
    dr.ellipse((x - 16, y - 16, x + 16, y + 16), fill=GOLD)
    if s > 0.82:
        grow = ease((s - 0.82) / 0.18)
        rad = 18 + 48 * grow
        dr.ellipse((x - rad, bot - rad * 0.6, x + rad, bot + rad * 0.7), fill=(212, 154, 62, 230))
    shown = round(3000 * s)
    caption(dr, (980, 430), f'{shown:,} KM', 64, GOLD, t, 0.35, 3.9)
    caption(dr, (980, 430), '3,000 KM', 64, GOLD, t, 3.9, 5.7)
    caption(dr, (980, 530), 'BENEATH YOUR FEET', 42, WHITE, t, 0.8, 4.4)
    caption(dr, (980, 640), 'LIQUID OUTER CORE', 42, WHITE, t, 4.15, 5.86)


def when1905(im, t, spec):
    dr = ImageDraw.Draw(im)
    slide = round(40 * (1 - ease(min(1, t / 0.4))))
    x = 280 - slide
    dr.line((x, 780, x + round(220 * ease(min(1, t / 0.45))), 780), fill=GOLD, width=8)
    label(dr, (x, 860), '1905', 72, GOLD, anchor='lm')
    label(dr, (x, 950), 'PONTFAREIN, FRANCE', 48, WHITE, anchor='lm')


def frame(spec, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0) if spec['alpha'] else NAVY + (255,))
    dr = ImageDraw.Draw(im)
    if not spec['alpha']:
        grid(dr)
    {'poledrift': poledrift, 'flip': flip, 'layers': layers, 'when1905': when1905}[spec['mode']](im, t, spec)
    if spec['alpha']:
        a = max(0, min(1, t / 0.4, (spec['duration_s'] - t) / 0.4))
        im.putalpha(im.getchannel('A').point(lambda p: round(p * a)))
    return im


def main(argv=None):
    if not EARTH.is_file():
        raise FileNotFoundError(EARTH)
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
