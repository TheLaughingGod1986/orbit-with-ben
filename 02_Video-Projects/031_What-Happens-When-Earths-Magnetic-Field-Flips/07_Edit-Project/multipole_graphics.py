#!/usr/bin/env python3
"""R40 and R47 multipole plates. £0. Real Earth, schematic poles.

The disc is the harvested eastern-hemisphere Blue Marble. It is a photograph,
not a flat disc. The magnets and ribbons are our drawing. They are not a
geodynamo model and not the NASA SVS clip.

R40 shows the locked line: the field never vanishes, the main magnet weakens
to about a tenth, and smaller temporary poles appear. It does not name a city.
R47 starts on "tangling" and shows several poles in unexpected places. Africa
and Tahiti stay on the later R48 plate.

Do not stack the older dipole_strength bar on R40. That bar was the strength
stand-in. This plate is the geometry. No KEEP or composite review.
"""
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from evidence_graphics import caption, main as render
from flip_graphics import earth_disc
from mechanism_graphics import BLUE, GOLD, H, NAVY, RED, W, WHITE, ease, needle

FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
CX, CY, RADIUS = 960, 560, 300

SPECS = [
    dict(row=40, mode='multipole', start_s=405.52, duration_s=12.40,
         source_rows=[15], alpha=False, cue='First',
         geometry='Real Blue Marble. Main dipole shrinks to about a tenth and '
                  'a stub remains. Four schematic temporary poles appear. '
                  'Not a city map and not a field model.',
         source_url='https://science.nasa.gov/science-research/earth-science/flip-flop-why-variations-in-earths-magnetic-field-arent-causing-todays-climate-change/',
         plate='GSFC_20171208_Archive_e001788',
         clear='One label at a time. Do not composite the dipole_strength bar on this plate.'),
    dict(row=47, mode='multipole_tangle', start_s=488.14, duration_s=4.72,
         source_rows=[18], alpha=False, cue='tangling',
         geometry='Real Blue Marble with several short schematic poles and '
                  'crossing ribbons. Not Africa or Tahiti, and not the SVS clip.',
         source_url='https://web.archive.org/web/20230512145930id_/https://science.nasa.gov/science-news/science-at-nasa/2003/29dec_magneticfield/',
         plate='GSFC_20171208_Archive_e001788',
         clear='Owns the row from tangling through places. The SVS clip still owns 480.80–488.14.'),
]


def grid(dr):
    for x in range(0, W, 80):
        dr.line((x, 0, x, H), fill=(32, 52, 75))
    for y in range(0, H, 80):
        dr.line((0, y, W, y), fill=(32, 52, 75))


def ribbon(dr, a, b, bow, colour, width, phase):
    pts = []
    for i in range(28):
        u = i / 27
        x = a[0] + (b[0] - a[0]) * u
        y = a[1] + (b[1] - a[1]) * u - bow * math.sin(math.pi * u)
        x += 10 * math.sin(phase + u * 5)
        pts.append((x, y))
    dr.line(pts, fill=colour, width=width)


def mark(im, xy, text, colour):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.text(xy, text, font=ImageFont.truetype(FONT, 36), anchor='mm', fill=colour)
    im.alpha_composite(layer)


def body(im, t):
    disc = earth_disc(RADIUS * 2, t * 6)
    im.paste(disc, (CX - RADIUS, CY - RADIUS), disc)


def main_dipole(im, t, reach):
    """A stub always remains, so the drawing matches 'never vanishes'."""
    d = ImageDraw.Draw(im)
    wobble = 0.06 * math.sin(t * 2.2)
    needle(d, CX, CY, wobble, length=max(36, reach), width=16)
    # Letters only while they sit off the disc. A short magnet stays unmarked.
    if reach > RADIUS * 0.75:
        ux, uy = math.sin(wobble), -math.cos(wobble)
        mark(im, (CX + ux * (reach + 46), CY + uy * (reach + 46)), 'N', RED)
        mark(im, (CX - ux * (reach + 46), CY - uy * (reach + 46)), 'S', WHITE)


def pop_pole(im, angle, t, start, length=70):
    p = ease((t - start) / 0.35)
    if p <= 0:
        return
    # Outside the limb, so the needles are not painted onto the continents.
    x = CX + math.cos(angle) * (RADIUS + 86)
    y = CY + math.sin(angle) * (RADIUS + 86)
    jx = 8 * math.sin(t * 2.4 + angle)
    needle(ImageDraw.Draw(im), x + jx, y, angle, length=length * p, width=8)


def frame(spec, t):
    im = Image.new('RGBA', (W, H), NAVY + (255,))
    dr = ImageDraw.Draw(im)
    grid(dr)
    body(im, t)
    dr = ImageDraw.Draw(im)
    if spec['mode'] == 'multipole':
        shrink = ease((t - 6.48) / 2.30)
        reach = RADIUS * (1 - 0.90 * shrink)
        main_dipole(im, t, reach)
        dr = ImageDraw.Draw(im)
        wobble = 0.06 * math.sin(t * 2.2)
        ux, uy = math.sin(wobble), -math.cos(wobble)
        ribbon(dr, (CX + ux * reach, CY + uy * reach),
               (CX - ux * reach, CY - uy * reach), 80, BLUE, 4, t * 2)
        for angle, start in ((-0.9, 10.40), (0.45, 10.72), (2.2, 11.08), (2.8, 11.40)):
            pop_pole(im, angle, t, start)
        dr = ImageDraw.Draw(im)
        caption(dr, (960, 120), 'NEVER VANISHES', 52, GOLD, t, 1.80, 3.50)
        caption(dr, (960, 120), 'MAIN MAGNET', 52, WHITE, t, 4.16, 6.40)
        caption(dr, (960, 120), 'ABOUT A TENTH', 52, GOLD, t, 7.06, 8.94)
        caption(dr, (960, 120), 'TEMPORARY POLES', 48, WHITE, t, 10.40, 12.20)
    else:
        knots = []
        for i, angle in enumerate((-1.1, -0.2, 0.7, 1.6, 2.5)):
            knots.append((CX + math.cos(angle) * (RADIUS + 86),
                          CY + math.sin(angle) * (RADIUS + 86)))
            pop_pole(im, angle, t, 0.15 + i * 0.16, length=64)
        dr = ImageDraw.Draw(im)
        drift = 18 * ease((t - 2.66) / 0.8)
        for i in range(len(knots)):
            a = knots[i]
            b = knots[(i + 2) % len(knots)]
            b = (b[0] + drift, b[1] - drift * 0.4)
            ribbon(dr, a, b, 90, BLUE if i % 2 == 0 else RED, 4, t * 2.5 + i)
        caption(dr, (960, 120), 'SEVERAL POLES', 52, GOLD, t, 0.98, 2.18)
        caption(dr, (960, 120), 'UNEXPECTED PLACES', 48, WHITE, t, 3.56, 4.50)
    credit = ImageDraw.Draw(im)
    credit.text((48, 1024), 'NASA', font=ImageFont.truetype(FONT, 28), fill=(210, 214, 220))
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
        data['status'] = 'partial_multipole_only'
        data['spend_gbp'] = 0
        data['words_note'] = (
            'R40 labels follow never vanishes, the main magnet, about a tenth, '
            'and temporary poles. R47 labels follow several poles and unexpected '
            'places. No city is named on either plate.'
        )
        got.manifest.write_text(json.dumps(data, indent=2) + '\n')


if __name__ == '__main__':
    main()
