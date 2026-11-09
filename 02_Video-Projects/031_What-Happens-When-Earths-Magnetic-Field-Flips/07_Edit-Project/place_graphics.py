#!/usr/bin/env python3
"""R10 sample map and R48 pole pins. £0. Not surveyed geography.

R10 draws two schematic land shapes and lights dots while Japan and
Manchuria are spoken. The shapes are not a traced coastline and the dots
are not Matuyama's sample list. The lower third stays empty for the
existing WHO card.

R48 puts schematic pins on the harvested eastern-hemisphere Blue Marble.
Africa is on that plate. Tahiti is not: the Pacific pin sits in the margin,
with a ribbon to the limb, rather than a false coordinate on Africa's side.
"""
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None

from evidence_graphics import caption, main as render
from flip_graphics import earth_disc
from mechanism_graphics import BLUE, GOLD, H, NAVY, RED, W, WHITE, ease

SPECS = [
    dict(row=10, mode='matuyama_map', start_s=94.92, duration_s=3.32,
         source_rows=[4], alpha=False, cue='tests',
         geometry='Schematic Japan and Manchuria shapes. Dots are not a site catalogue.',
         source_url='https://doi.org/10.2183/pjab1912.5.203',
         clear='y>760 stays empty so the WHO card can sit there until 96.80 s.'),
    dict(row=48, mode='poles_map', start_s=493.66, duration_s=5.64,
         source_rows=[18], alpha=False, cue='You',
         geometry='Real eastern-hemisphere Blue Marble. Africa pin on the visible continent. '
                  'Tahiti pin is a margin marker because this plate does not show the Pacific.',
         source_url='https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/',
         plate='GSFC_20171208_Archive_e001788'),
]


def grid(dr):
    for x in range(0, W, 80):
        dr.line((x, 0, x, H), fill=(32, 52, 75))
    for y in range(0, H, 80):
        dr.line((0, y, W, y), fill=(32, 52, 75))


def dots(dr, centres, t, start):
    for i, (x, y) in enumerate(centres):
        p = ease((t - start - i * 0.08) / 0.28)
        if p <= 0:
            continue
        r = 7 + 9 * p
        dr.ellipse((x - r, y - r, x + r, y + r), fill=GOLD)
        dr.ellipse((x - 3, y - 3, x + 3, y + 3), fill=WHITE)


def matuyama_frame(spec, t):
    im = Image.new('RGBA', (W, H), NAVY + (255,))
    dr = ImageDraw.Draw(im)
    grid(dr)
    grow = ease(t / 0.5)
    # West shape and an island chain. Spacing only: not a coastline.
    box = (260, 340, 260 + round(520 * grow), 340 + round(340 * grow))
    dr.rounded_rectangle(box, radius=80, fill=(46, 78, 64, 255), outline=BLUE, width=4)
    for i, y in enumerate((300, 450, 600)):
        if grow < 0.25 * (i + 1):
            continue
        dr.ellipse((1240, y, 1500, y + 110), fill=(46, 78, 64, 255), outline=BLUE, width=4)
    dots(dr, [(1320, 355), (1380, 500), (1340, 650)], t, 1.88)
    dots(dr, [(420, 470), (560, 560), (480, 400)], t, 2.62)
    caption(dr, (960, 150), 'VOLCANIC ROCKS', 48, WHITE, t, 0.46, 1.82)
    caption(dr, (1370, 230), 'JAPAN', 52, GOLD, t, 1.88, 2.70)
    caption(dr, (520, 250), 'MANCHURIA', 52, GOLD, t, 2.62, 3.70)
    return im


def pin(base, x, y, t, start, colour):
    p = ease((t - start) / 0.35)
    if p <= 0:
        return
    tip = y + round(46 * (1 - p))
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line((x, tip - 54, x, tip), fill=colour + (255,), width=6)
    d.ellipse((x - 16, tip - 78, x + 16, tip - 46), fill=colour + (255,))
    d.ellipse((x - 5, tip - 2, x + 5, tip + 8), fill=WHITE + (255,))
    base.alpha_composite(layer)


def ribbon(dr, a, b, t, start):
    p = ease((t - start) / 0.7)
    if p <= 0:
        return
    steps = max(2, round(48 * p))
    pts = []
    for i in range(steps):
        u = i / 47
        x = a[0] + (b[0] - a[0]) * u
        y = a[1] + (b[1] - a[1]) * u - 180 * math.sin(math.pi * u)
        pts.append((x, y))
    if len(pts) > 1:
        dr.line(pts, fill=GOLD, width=5)


def poles_frame(spec, t):
    im = Image.new('RGBA', (W, H), NAVY + (255,))
    dr = ImageDraw.Draw(im)
    grid(dr)
    diameter = 620
    disc = earth_disc(diameter, spin=t * 3)
    im.alpha_composite(disc, (960 - diameter // 2, 600 - diameter // 2))
    # Eastern hemisphere: Africa sits left of centre on this plate.
    africa = (800, 620)
    # Tahiti is not on this hemisphere. The pin stays in the margin.
    tahiti = (1580, 520)
    pin(im, *africa, t=t, start=1.52, colour=RED)
    pin(im, *tahiti, t=t, start=3.50, colour=BLUE)
    if t >= 3.85:
        ribbon(ImageDraw.Draw(im), africa, tahiti, t, 3.85)
    caption(dr, (420, 150), 'SOUTH POLE', 48, RED, t, 0.90, 4.50)
    caption(dr, (420, 220), 'AFRICA', 48, WHITE, t, 1.52, 5.24)
    caption(dr, (1500, 150), 'NORTH POLE', 48, BLUE, t, 2.52, 6.10)
    caption(dr, (1500, 220), 'TAHITI', 48, WHITE, t, 3.50, 6.10)
    caption(dr, (1580, 640), 'PACIFIC', 40, GOLD, t, 4.42, 6.10)
    return im


def frame(spec, t):
    if spec['mode'] == 'matuyama_map':
        return matuyama_frame(spec, t)
    if spec['mode'] == 'poles_map':
        return poles_frame(spec, t)
    raise KeyError(spec['mode'])


def main(argv=None):
    render(argv, specs=SPECS, render_frame=frame)
    args = argparse.ArgumentParser()
    args.add_argument('--manifest', type=Path)
    args.add_argument('--out', type=Path)
    args.add_argument('--previews', action='store_true')
    got = args.parse_args(argv)
    if got.manifest and got.manifest.exists():
        data = json.loads(got.manifest.read_text())
        data['status'] = 'partial_place_maps_only'
        data['spend_gbp'] = 0
        got.manifest.write_text(json.dumps(data, indent=2) + '\n')


if __name__ == '__main__':
    main()
