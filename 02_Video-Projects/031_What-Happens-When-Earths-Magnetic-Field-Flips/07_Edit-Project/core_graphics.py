#!/usr/bin/env python3
"""031 £0 core batch: tight flip, outer-core churn, Laschamp dip.

These are our own schematics. The Earth disc is the harvested Blue Marble.
The magnet, swirls and strength bar are not a field model or a measured curve.
The dip follows the spoken "nearly to zero" / "snapped back". It does not
replace the sourced 6% rings graphic. No KEEP or composite approval.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from evidence_graphics import caption, main as render
from mechanism_graphics import BLUE, GOLD, NAVY, RED, W, H, WHITE, ease

EARTH = Path(
    '/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/'
    '031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/'
    'harvest_v01/GSFC_20171208_Archive_e000678.jpg'
)
EARTH_ID = 'GSFC_20171208_Archive_e000678'
_DISC = {}

SPECS = [
    dict(row=12, mode='flip_tight', start_s=112.98, duration_s=9.0,
         source_rows=[4, 5], alpha=False, cue='turned',
         earth_nasa_id=EARTH_ID,
         geometry='Second flip: tight dipole turns over, air ring stays, then a dive to the core'),
    dict(row=14, mode='layers_core', start_s=132.70, duration_s=6.0,
         source_rows=[6], alpha=False, cue='Down',
         geometry='Tight churning outer core only; no temperature number'),
    dict(row=33, mode='paleo_dip', start_s=345.0, duration_s=4.16,
         source_rows=[14], alpha=False, cue='shield',
         geometry='Qualitative dip and rebound for the spoken line; not the 6% record'),
]


def disc(radius):
    if radius not in _DISC:
        src = Image.open(EARTH).convert('RGBA').crop((220, 219, 1856, 1855))
        src = src.resize((radius * 2, radius * 2), Image.Resampling.LANCZOS)
        mask = Image.new('L', (radius * 2, radius * 2), 0)
        ImageDraw.Draw(mask).ellipse((1, 1, radius * 2 - 2, radius * 2 - 2), fill=255)
        src.putalpha(mask)
        _DISC[radius] = src
    return _DISC[radius]


def paste_disc(im, cx, cy, radius):
    body = disc(radius)
    im.alpha_composite(body, (int(cx - radius), int(cy - radius)))


def credit(im):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 28)
    ImageDraw.Draw(layer).text((48, 1008), 'CGI', font=font, fill=(244, 239, 230, 210))
    im.alpha_composite(layer)


def grid(im):
    dr = ImageDraw.Draw(im)
    for x in range(0, W, 80):
        dr.line((x, 0, x, H), fill=(36, 58, 84))
    for y in range(0, H, 80):
        dr.line((0, y, W, y), fill=(36, 58, 84))


def magnet(angle):
    tile = Image.new('RGBA', (280, 90), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.rounded_rectangle((6, 18, 140, 72), radius=12, fill=RED)
    d.rounded_rectangle((136, 18, 274, 72), radius=12, fill=BLUE)
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 36)
    d.text((58, 28), 'N', font=font, fill=WHITE)
    d.text((188, 28), 'S', font=font, fill=WHITE)
    return tile.rotate(math.degrees(-angle), resample=Image.Resampling.BICUBIC, expand=True)


def flip_tight(im, t):
    # Turn during "upside down" (t 1.52–2.38), then dive from "secret" (t 5.60).
    turn = ease((t - 1.52) / 0.86)
    dive = ease((t - 5.60) / 2.4)
    radius = int(250 + 170 * dive)
    cy = int(560 + 40 * dive)
    paste_disc(im, 960, cy, radius)
    ring = ImageDraw.Draw(im)
    pad = 18
    ring.ellipse((960 - radius - pad, cy - radius - pad, 960 + radius + pad, cy + radius + pad),
                 outline=BLUE + (255,), width=10)
    bar = magnet(math.pi * turn)
    im.alpha_composite(bar, (960 - bar.width // 2, cy - bar.height // 2))
    # Golden core grows only on the dive, so the air ring is never stripped.
    if dive > 0:
        core = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        r = int(28 + 70 * dive)
        ImageDraw.Draw(core).ellipse((960 - r, cy - r, 960 + r, cy + r), fill=GOLD + (int(210 * dive),))
        im.alpha_composite(core)
    dr = ImageDraw.Draw(im)
    caption(dr, (960, 120), 'UPSIDE DOWN', 64, GOLD, t, 1.52, 5.2)
    caption(dr, (960, 120), 'SECRET ENGINE', 64, WHITE, t, 5.6, 8.6)


def layers_core(im, t):
    bowl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(bowl)
    dr.ellipse((510, 210, 1410, 1010), fill=(18, 32, 52, 255))
    for i in range(18):
        phase = t * 1.1 + i * 0.55
        x = 960 + math.sin(phase) * (90 + (i % 5) * 28)
        y = 610 + math.cos(phase * 0.85) * (50 + (i % 4) * 18)
        rw = 64 + (i % 4) * 26
        rh = 26 + (i % 3) * 12
        colour = GOLD if i % 2 == 0 else (214, 140, 52, 255)
        dr.ellipse((x - rw, y - rh, x + rw, y + rh), fill=colour)
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).ellipse((518, 218, 1402, 1002), fill=255)
    bowl.putalpha(mask)
    im.alpha_composite(bowl)
    ring = ImageDraw.Draw(im)
    ring.ellipse((510, 210, 1410, 1010), outline=BLUE + (255,), width=8)
    caption(ring, (960, 120), 'OUTER CORE', 64, WHITE, t, 0.4, 3.2)
    caption(ring, (960, 120), 'LIQUID IRON', 64, GOLD, t, 3.2, 5.6)


def paleo_dip(im, t):
    # Fall on "dropped nearly to zero", rebound on "snapped back". Not a 6% chart.
    dr = ImageDraw.Draw(im)
    if t < 1.58:
        level = 0.92
    elif t < 3.44:
        level = 0.92 - 0.84 * ease((t - 1.58) / 1.3)
    else:
        level = 0.08 + 0.84 * ease((t - 3.44) / 0.5)
    x, y, width = 460, 620, 1000
    dr.line((x, y, x + width, y), fill=(140, 160, 180, 255), width=6)
    dr.rounded_rectangle((x, y - 36, x + max(8, int(width * level)), y + 36), radius=16, fill=BLUE)
    # Marker keeps moving along the bar.
    mx = x + int(width * level)
    dr.ellipse((mx - 16, y - 16, mx + 16, y + 16), fill=GOLD)
    caption(dr, (960, 280), 'TRIED TO FLIP', 56, WHITE, t, 0.2, 1.58)
    caption(dr, (960, 280), 'NEARLY TO ZERO', 60, GOLD, t, 1.58, 3.44)
    caption(dr, (960, 280), 'SNAPPED BACK', 60, WHITE, t, 3.44, 4.16)
    caption(dr, (960, 820), 'LASCHAMP DIP', 48, WHITE, t, 0.3, 4.0)


def frame(spec, t):
    im = Image.new('RGBA', (W, H), NAVY + (255,))
    grid(im)
    {'flip_tight': flip_tight, 'layers_core': layers_core, 'paleo_dip': paleo_dip}[spec['mode']](im, t)
    credit(im)
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
