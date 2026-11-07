#!/usr/bin/env python3
"""031 £0 geodynamo graphics. No approval implied.

Current loops and the dipole are a schematic of the spoken mechanism.
They are not a Glatzmaier–Roberts frame and not a measured flow field.
The Earth disc is the harvested NASA Blue Marble plate. Numbers are not drawn:
these rows do not speak a new figure.
"""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

from evidence_graphics import caption, main as render
from mechanism_graphics import BLUE, GOLD, NAVY, RED, W, H, WHITE, ease, label

HERE = Path(__file__).resolve().parent
EARTH = Path(
    '/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/'
    '031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/'
    'harvest_v01/GSFC_20171208_Archive_e000678.jpg'
)
EARTH_ID = 'GSFC_20171208_Archive_e000678'
_DISC = {}


def _span(start_text, start_near, end_text, end_near):
    path = HERE.parent / '02_Voiceover/stt/magnetic_field_flip_vo_v02a/stt_raw.json'
    words = [w for w in json.loads(path.read_text())['words'] if w.get('type') == 'word']
    start = next(w for w in words if w['text'] == start_text and abs(w['start'] - start_near) < 1)
    end = next(w for w in words if w['text'] == end_text and abs(w['start'] - end_near) < 1)
    start_s = float(start['start'])
    duration = float(end['start']) - start_s
    if duration < 1:
        raise ValueError((start_text, end_text, duration))
    return start_s, duration


_ALIGN = _span('Most', 159.32, 'However,', 168.76)
_TIP = _span('Swirling', 172.68, 'Where', 188.36)
_SETTLE = _span('settled', 544.0, 'Our', 547.7)

SPECS = [
    dict(row=16, mode='dynamo_align', variant='align', start_s=_ALIGN[0], duration_s=_ALIGN[1],
         source_rows=[6], alpha=False, cue='Most', earth_nasa_id=EARTH_ID,
         geometry='Schematic iron-current loops lining up into one dipole. Not a measured core flow.'),
    dict(row=17, mode='dynamo_tip', variant='tip', start_s=_TIP[0], duration_s=_TIP[1],
         source_rows=[6], alpha=False, cue='Swirling', earth_nasa_id=EARTH_ID,
         geometry='Schematic backwards eddies fighting the main flow until the dipole turns over. Ends at the next word, through the pause after "over".'),
    dict(row=52, mode='dynamo_settle', variant='settle', start_s=_SETTLE[0], duration_s=_SETTLE[1],
         source_rows=[18], alpha=False, cue='settled', earth_nasa_id=EARTH_ID,
         geometry='Loops slow and the compass locks south. Ends as the next row starts. Not the generations tally.'),
]


def disc(im, cx, cy, r):
    key = r
    if key not in _DISC:
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


def ellipse(dr, cx, cy, rx, ry, rot, colour, width=8):
    pts = []
    for i in range(72):
        a = math.tau * i / 72
        x, y = rx * math.cos(a), ry * math.sin(a)
        xr = x * math.cos(rot) - y * math.sin(rot)
        yr = x * math.sin(rot) + y * math.cos(rot)
        pts.append((cx + xr, cy + yr))
    dr.line(pts + [pts[0]], fill=colour, width=width)


def dipole(dr, cx, cy, length, ang, alpha=255):
    ux, uy = math.sin(ang), -math.cos(ang)
    x1, y1 = cx + length * ux, cy + length * uy
    x2, y2 = cx - length * ux, cy - length * uy
    dr.line((x1, y1, x2, y2), fill=(196, 160, 92, alpha), width=18)
    dr.ellipse((x1 - 22, y1 - 22, x1 + 22, y1 + 22), fill=RED + (alpha,))
    dr.ellipse((x2 - 22, y2 - 22, x2 + 22, y2 + 22), fill=WHITE + (alpha,))
    label(dr, (x1 + 48 * ux, y1 + 48 * uy), 'N', 40, RED)
    label(dr, (x2 - 48 * ux, y2 - 48 * uy), 'S', 40, WHITE)


def dynamo_align(im, t, spec):
    cx, cy, r = 760, 500, 250 + round(18 * ease(t / spec['duration_s']))
    disc(im, cx, cy, r)
    dr = ImageDraw.Draw(im)
    s = ease(min(1, t / 6.2))
    for i, tilt0 in enumerate((-1.1, 0.7, 1.6)):
        tilt = tilt0 * (1 - s) + (i - 1) * 0.22 * s
        spin = t * 0.35
        ellipse(dr, cx, cy, r + 36, 78 + i * 10, tilt + spin * 0.15, GOLD, 8)
    if s > 0.55:
        dipole(dr, cx, cy, r * 0.78, 0)
    caption(dr, (1480, 280), 'IRON CURRENTS', 48, GOLD, t, 0.4, 3.9)
    caption(dr, (1480, 380), 'LINED UP', 48, WHITE, t, 4.1, 7.6)
    caption(dr, (1480, 480), 'STEADY POLES', 48, WHITE, t, 7.8, spec['duration_s'] - 0.2)
    label(dr, (150, 70), 'NASA', 32, WHITE, anchor='lm')


def dynamo_tip(im, t, spec):
    cx, cy, r = 760, 500, 240 + round(12 * math.sin(t * 0.7))
    disc(im, cx, cy, r)
    dr = ImageDraw.Draw(im)
    fight = ease(min(1, t / 8.0))
    for i in range(4):
        ang = t * (0.45 + 0.12 * i) + i
        ox = math.cos(ang) * (40 + 70 * fight)
        oy = math.sin(ang * 1.3) * (24 + 40 * fight)
        ellipse(dr, cx + ox, cy + oy, 70 + 20 * fight, 46, ang, RED if i % 2 else GOLD, 7)
    tip = ease(max(0, (t - 8.2) / 5.4))
    dipole(dr, cx, cy, r * (0.82 - 0.18 * fight), math.pi * tip)
    caption(dr, (1480, 260), 'EDDIES FIGHT', 48, RED, t, 0.4, 4.0)
    caption(dr, (1480, 360), 'BACKWARDS FLOW', 48, WHITE, t, 4.2, 8.0)
    caption(dr, (1480, 460), 'FIELD WEAKENS', 48, GOLD, t, 8.2, 12.0)
    caption(dr, (1480, 560), 'TIPS OVER', 48, GOLD, t, 12.2, spec['duration_s'] - 0.2)
    label(dr, (150, 70), 'NASA', 32, WHITE, anchor='lm')


def dynamo_settle(im, t, spec):
    cx, cy, r = 760, 520, 230
    disc(im, cx, cy, r)
    dr = ImageDraw.Draw(im)
    settle = ease(min(1, t / 2.2))
    wobble = (1 - settle) * math.sin(t * 5) * 0.35
    for i in range(3):
        ellipse(dr, cx, cy, r + 28, 64, wobble + (i - 1) * 0.18, GOLD, 7)
    dipole(dr, cx, cy, r * 0.75, math.pi + wobble)
    # Compass rose locks with its marked end toward the bottom of the frame.
    nx, ny = 1500, 470
    dr.ellipse((nx - 90, ny - 90, nx + 90, ny + 90), outline=GOLD, width=6)
    ang = math.pi * settle + (1 - settle) * 0.8
    ux, uy = math.sin(ang), -math.cos(ang)
    # Red is the north-seeking end. Settled, it points to the bottom of the frame.
    dr.line((nx, ny, nx - 64 * ux, ny - 64 * uy), fill=WHITE, width=12)
    dr.polygon([
        (nx + 74 * ux, ny + 74 * uy),
        (nx + 18 * uy, ny - 18 * ux),
        (nx - 18 * uy, ny + 18 * ux),
    ], fill=RED)
    caption(dr, (1500, 640), 'IRON SETTLES', 44, WHITE, t, 0.25, 2.0)
    caption(dr, (1500, 720), 'COMPASS SOUTH', 44, GOLD, t, 2.05, spec['duration_s'] - 0.15)
    label(dr, (150, 70), 'NASA', 32, WHITE, anchor='lm')


def frame(spec, t):
    im = Image.new('RGBA', (W, H), NAVY + (255,))
    dr = ImageDraw.Draw(im)
    grid(dr)
    {'align': dynamo_align, 'tip': dynamo_tip, 'settle': dynamo_settle}[spec['variant']](im, t, spec)
    return im


def main(argv=None):
    if not EARTH.is_file():
        raise FileNotFoundError(EARTH)
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
