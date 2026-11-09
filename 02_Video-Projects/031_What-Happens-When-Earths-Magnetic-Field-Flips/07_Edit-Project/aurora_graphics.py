#!/usr/bin/env python3
"""R51 mid-latitude aurora plate. £0. Real Earth, schematic curtains.

The disc is the harvested eastern-hemisphere Blue Marble
(GSFC_20171208_Archive_e001788), darkened so the shot reads as night.
It is a photograph, not a flat disc and not a city map.

This plate shows Africa, Arabia and a sliver of India. Cairo sits on the
Nile delta. London, Mumbai and Sydney are not on this hemisphere, so those
pins stay in the margin with a ribbon to the limb. They are the spoken
city names, not a claim that aurora was observed at a surveyed coordinate.

Curtains are our drawing. They slide from high latitude toward the middle
of the disc and keep shimmering. No KEEP or composite review.
"""
import argparse
import json
import math

from PIL import Image, ImageChops, ImageDraw

from evidence_graphics import caption, main as render
from flip_graphics import earth_disc
from mechanism_graphics import BLUE, GOLD, H, NAVY, W, WHITE, ease
from place_graphics import pin

GREEN = (90, 220, 150)
CRIMSON = (214, 64, 92)
SPECS = [
    dict(row=51, mode='aurora', start_s=522.62, duration_s=10.32,
         source_rows=[18], alpha=False, cue='Curtains',
         geometry='Darkened eastern-hemisphere Blue Marble. Cairo pin on the Nile delta. '
                  'London, Mumbai and Sydney are margin pins: those cities are off this plate. '
                  'Green and crimson curtains are a schematic, not a measurement.',
         source_url='https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/',
         plate='GSFC_20171208_Archive_e001788',
         clear='One label at a time. Pins stay after they light. Curtains keep moving.'),
]

# Disc geometry. Positions were checked against the harvested plate.
CX, CY, DIAMETER = 900, 560, 640
_NIGHT = None


def night_disc():
    global _NIGHT
    if _NIGHT is not None:
        return _NIGHT
    disc = earth_disc(DIAMETER, 0)
    r, g, b, a = disc.split()
    r = r.point(lambda v: int(v * 0.34))
    g = g.point(lambda v: int(v * 0.40))
    b = b.point(lambda v: int(v * 0.62))
    _NIGHT = Image.merge('RGBA', (r, g, b, a))
    return _NIGHT


def grid(dr):
    for x in range(0, W, 80):
        dr.line((x, 0, x, H), fill=(32, 52, 75))
    for y in range(0, H, 80):
        dr.line((0, y, W, y), fill=(32, 52, 75))


def reach(dr, a, b, t, start):
    """Same arch as the pole-map ribbon, fast enough to land while the name is up."""
    p = ease((t - start) / 0.35)
    if p <= 0:
        return
    steps = max(2, round(36 * p))
    pts = []
    for i in range(steps):
        u = i / 35
        x = a[0] + (b[0] - a[0]) * u
        y = a[1] + (b[1] - a[1]) * u - 90 * math.sin(math.pi * u)
        pts.append((x, y))
    if len(pts) > 1:
        dr.line(pts, fill=GOLD, width=5)


def curtains(base, t):
    """Bands travel from this plate's northern limb to the middle, then shimmer."""
    slide = ease(min(1.0, max(0.0, (t - 0.55) / 4.8)))
    radius = DIAMETER // 2
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    for colour, phase, lead in ((GREEN, 0.0, 0.0), (CRIMSON, 1.2, 0.06)):
        y = CY - radius * 0.86 * (1 - ease(min(1.0, slide + lead)))
        for i in range(-5, 6):
            x = CX + i * 58 + 16 * math.sin(t * 2.1 + phase + i * 0.7)
            yy = y + 14 * math.sin(t * 2.6 + phase + i)
            h = 120 + 22 * math.sin(t * 1.5 + phase + i)
            dr.ellipse((x - 22, yy - h, x + 22, yy + h), fill=colour + (150,))
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).ellipse(
        (CX - radius + 2, CY - radius + 2, CX + radius - 2, CY + radius - 2), fill=255)
    layer.putalpha(ImageChops.multiply(layer.getchannel('A'), mask))
    base.alpha_composite(layer)


def frame(spec, t):
    im = Image.new('RGBA', (W, H), NAVY + (255,))
    dr = ImageDraw.Draw(im)
    grid(dr)
    radius = DIAMETER // 2
    im.alpha_composite(night_disc(), (CX - radius, CY - radius))
    curtains(im, t)
    # Nile delta is on this plate. The other three cities are not.
    # Tip on the Nile delta, not the sea north of it.
    cairo = (835, 385)
    london = (280, 220)
    mumbai = (1540, 430)
    sydney = (1540, 820)
    pin(im, *cairo, t=t, start=6.80, colour=GOLD)
    pin(im, *london, t=t, start=5.98, colour=BLUE)
    pin(im, *mumbai, t=t, start=7.70, colour=BLUE)
    pin(im, *sydney, t=t, start=8.76, colour=BLUE)
    dr = ImageDraw.Draw(im)
    if 5.98 <= t < 6.75:
        reach(dr, london, (700, 340), t, 5.98)
    if 7.70 <= t < 8.70:
        reach(dr, mumbai, (1188, 500), t, 7.70)
    if 8.76 <= t < 10.12:
        reach(dr, sydney, (1140, 780), t, 8.76)
    # One label at a time, each under four seconds, on the locked words.
    caption(dr, (960, 120), 'GREEN AND CRIMSON', 52, GREEN, t, 0.70, 2.40)
    caption(dr, (960, 120), 'FUNNEL DOWN', 52, WHITE, t, 2.66, 3.70)
    caption(dr, (960, 120), 'THE MIDDLE', 52, GOLD, t, 3.78, 5.70)
    caption(dr, (280, 300), 'LONDON', 48, WHITE, t, 5.98, 6.75)
    caption(dr, (835, 250), 'CAIRO', 48, GOLD, t, 6.80, 7.65)
    caption(dr, (1540, 340), 'MUMBAI', 48, WHITE, t, 7.70, 8.70)
    caption(dr, (1540, 720), 'SYDNEY', 48, WHITE, t, 8.76, 10.12)
    return im


def main(argv=None):
    render(argv, specs=SPECS, render_frame=frame)
    args = argparse.ArgumentParser()
    args.add_argument('--manifest', type=Path)
    args.add_argument('--out', type=Path)
    args.add_argument('--previews', action='store_true')
    got = args.parse_args(argv)
    if got.manifest and got.manifest.exists():
        data = json.loads(got.manifest.read_text())
        data['status'] = 'partial_aurora_only'
        data['spend_gbp'] = 0
        data['words_note'] = (
            'Labels follow the locked words: green and crimson, funnel down, '
            'the middle, then London, Cairo, Mumbai and Sydney. Cairo is the '
            'only pin on this eastern-hemisphere plate.'
        )
        got.manifest.write_text(json.dumps(data, indent=2) + '\n')


if __name__ == '__main__':
    main()
