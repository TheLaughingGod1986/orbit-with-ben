#!/usr/bin/env python3
"""031 £0 South Atlantic batch. Schematics, not a radiation or field model.

Belts share a surface zero. Altitudes are the spoken 600 km and 200 km only.
The station mark is twice the 200 km line because the line says the sag is
half the station's height. 400 km, 24,000 nT and 20 km/yr stay off screen:
they are in SOURCES and not in these spoken lines. No traced coastline.
"""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

from evidence_graphics import arrow, caption, main as render
from mechanism_graphics import W, H, NAVY, WHITE, GOLD, BLUE, RED, label

SPECS = [
    dict(row=25, mode='belts_hold', start_s=246.5, duration_s=4.64,
         cue='holds', source_rows=[10], alpha=False),
    dict(row=25, mode='belts_sag', start_s=259.899, duration_s=4.88,
         cue='sags', source_rows=[10], alpha=False),
    dict(row=27, mode='hubble_saa', start_s=280.42, duration_s=4.32,
         cue='seven', source_rows=[11], alpha=True),
    dict(row=28, mode='sat_safe', start_s=296.96, duration_s=2.84,
         cue='shut', source_rows=[11], alpha=True),
    dict(row=29, mode='saa', start_s=301.2, duration_s=5.12,
         cue='Since', source_rows=[12], alpha=False),
]

# Shared altitude scale: surface y=860, 600 km at y=300. 200 km is one third up.
SURFACE, TOP600 = 860, 300


def belt_y(km):
    return SURFACE - (SURFACE - TOP600) * (km / 600)


def horizon(dr):
    # A limb arc, not a flat-disc planet.
    dr.chord((-280, 700, 2200, 2100), 200, 340, fill=(28, 78, 128, 255))
    dr.arc((-280, 700, 2200, 2100), 200, 340, fill=BLUE, width=8)


def scale(dr):
    # The tick meets the high belt. Surface is the shared zero.
    dr.line((180, 120, 180, SURFACE), fill=WHITE, width=6)
    dr.line((160, SURFACE, 230, SURFACE), fill=WHITE, width=6)
    dr.line((160, 120, 240, 120), fill=GOLD, width=6)


def short_caption(dr, xy, text, size, colour, t, start, end):
    # Windows under about a second stay readable; the shared 0.35s fade would eat them.
    if not start <= t < end:
        return
    fade = 0.12
    opacity = max(0, min(1, (t - start) / fade, (end - t) / fade))
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    label(ImageDraw.Draw(layer), xy, text, size, colour)
    layer.putalpha(layer.getchannel('A').point(lambda p: round(p * opacity)))
    dr._image.alpha_composite(layer)


def particles(dr, y, t, above=True):
    for i in range(28):
        x = 420 + (i * 53 + t * 80) % 1280
        yy = y - 30 - ((i * 37 + t * 50) % 180) if above else y + 24 + ((i * 29) % 70)
        dr.ellipse((x, yy, x + 10, yy + 10), fill=GOLD if i % 3 else RED)


def belts_hold(dr, spec, t):
    horizon(dr)
    scale(dr)
    grown = 600 * (0.5 - 0.5 * math.cos(math.pi * max(0, min(1, t / 3.62))))
    y = belt_y(grown if grown > 1 else 1)
    dr.arc((360, y - 220, 1680, y + 260), 200, 340, fill=GOLD, width=14)
    particles(dr, y, t, above=True)
    if t >= 2.96:
        caption(dr, (1100, 150), 'BEYOND', 64, GOLD, t, 2.96, 4.64)
    if t >= 3.62:
        short_caption(dr, (1100, 240), '600 KILOMETERS', 64, WHITE, t, 3.62, 4.64)


def belts_sag(dr, spec, t):
    horizon(dr)
    scale(dr)
    km = 600 - 400 * (0.5 - 0.5 * math.cos(math.pi * max(0, min(1, t / 1.12))))
    y = belt_y(km)
    dr.arc((360, y - 180, 1680, y + 220), 200, 340, fill=GOLD, width=14)
    particles(dr, y, t, above=False)
    if t >= 1.12:
        caption(dr, (1100, 150), '200 KILOMETERS', 64, GOLD, t, 1.12, 4.2)
    if t >= 2.821:
        station = belt_y(400)
        dr.line((400, station, 1500, station), fill=BLUE, width=4)
        dr.rectangle((980, station - 28, 1060, station + 8), outline=WHITE, width=4)
        caption(dr, (1100, 250), 'HALF THE HEIGHT', 52, WHITE, t, 2.821, 4.88)
    if t >= 4.021:
        short_caption(dr, (1280, 360), 'SPACE STATION', 44, WHITE, t, 4.021, 4.88)


def hubble_saa(dr, spec, t):
    cx, cy, rx, ry = 1280, 460, 340, 150
    dr.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=BLUE, width=6)
    # The dent is a wedge on the orbit, not a map of the Atlantic.
    dr.pieslice((cx + 40, cy - 80, cx + 280, cy + 160), 20, 160, fill=(246, 121, 98, 90))
    ang = t * 1.7
    x = cx + rx * math.cos(ang)
    y = cy + ry * math.sin(ang)
    dr.ellipse((x - 16, y - 16, x + 16, y + 16), fill=GOLD)
    caption(dr, (1280, 180), 'SEVEN TO NINE', 56, GOLD, t, 0.05, 3.5)
    caption(dr, (1280, 260), 'ORBITS', 52, WHITE, t, 0.86, 4.1)
    caption(dr, (1280, 700), 'EVERY DAY', 52, WHITE, t, 2.0, 4.32)


def sat_safe(dr, spec, t):
    x, y = 1320, 420
    dr.rectangle((x - 70, y - 28, x + 70, y + 28), outline=WHITE, width=6)
    dr.rectangle((x - 150, y - 16, x - 78, y + 16), fill=BLUE)
    dr.rectangle((x + 78, y - 16, x + 150, y + 16), fill=BLUE)
    alive = 5 - int(min(4, t / 2.2 * 4))
    for i in range(5):
        colour = GOLD if i < alive else (80, 80, 90, 180)
        dr.ellipse((x - 50 + i * 22, y - 8, x - 34 + i * 22, y + 8), fill=colour)
    caption(dr, (1320, 250), 'SHUT DOWN', 60, GOLD, t, 0.05, 2.84)
    caption(dr, (1320, 620), 'NON-ESSENTIAL', 48, WHITE, t, 1.16, 2.84)


def saa(dr, spec, t):
    grow = 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, (t - 0.4) / 2.4)))
    if t < 3.54:
        r = 70 + 150 * grow
        dr.ellipse((960 - r, 560 - r * 0.65, 960 + r, 560 + r * 0.65), fill=(246, 121, 98, 210))
    else:
        split = max(0, min(1, (t - 3.54) / 1.2))
        gap = 280 * split
        for side in (-1, 1):
            cx = 960 + side * gap
            dr.ellipse((cx - 100, 490, cx + 100, 670), fill=(246, 121, 98, 220))
            arrow(dr, 960, 400, cx, 480, GOLD, 5)
    caption(dr, (960, 160), 'SINCE 1970', 64, GOLD, t, 0.24, 3.9)
    caption(dr, (960, 260), 'WIDENED', 56, WHITE, t, 2.7, 4.9)
    short_caption(dr, (960, 860), 'TWO LOBES', 64, GOLD, t, 4.24, 5.12)


def frame(spec, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0) if spec['alpha'] else NAVY + (255,))
    dr = ImageDraw.Draw(im)
    if not spec['alpha']:
        for x in range(0, W, 80):
            dr.line((x, 0, x, H), fill=(32, 52, 75))
        for y in range(0, H, 80):
            dr.line((0, y, W, y), fill=(32, 52, 75))
    globals()[spec['mode']](dr, spec, t)
    if spec['alpha']:
        a = max(0, min(1, t / 0.4, (spec['duration_s'] - t) / 0.4))
        im.putalpha(im.getchannel('A').point(lambda p: round(p * a)))
    return im


def main(argv=None):
    # evidence.main stamps a mechanisms status. This batch rewrites that line.
    render(argv, specs=SPECS, render_frame=frame)
    argv = list(argv or [])
    if '--manifest' not in argv:
        return
    manifest = Path(argv[argv.index('--manifest') + 1])
    data = json.loads(manifest.read_text())
    data['status'] = 'partial_saa_only'
    data['batch'] = 'South Atlantic belts, Hubble dent, satellite shutdown, two lobes'
    data['unspoken_kept_off_screen'] = [
        '400 km ISS height is the geometry of half, not a label (SOURCES row 10)',
        '24,000 to 22,000 nT and 20 km/yr stay off this line (SOURCES row 12)',
    ]
    manifest.write_text(json.dumps(data, indent=2) + '\n')


if __name__ == '__main__':
    main()
