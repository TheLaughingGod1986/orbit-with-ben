#!/usr/bin/env python3
"""031 £0 sky batch: paleo comparison, temporary poles, tangle, pole names, aurora.

Schematics, not measured datasets. The paleo bars share a zero and use the
sourced relationship only: today matches its 100,000-year high and is twice
the million-year average. No 8×10²² figure is drawn. Pole and city names follow
the locked line. Tahiti is named, not pinned: the harvested Blue Marble face
shows Africa, and Tahiti is on the other side. Aurora city names are cards,
not coordinates. £0. No KEEP.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from mechanism_graphics import W, H, NAVY, WHITE, GOLD, BLUE, RED, label, ease
from evidence_graphics import main as render

HERE = Path(__file__).resolve().parent
MARBLE = HERE / 'harvest_v01' / 'GSFC_20171208_Archive_e001788.jpg'
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
# Durations are exact frame multiples and end on a locked word end or in the
# following pause, never inside the next sentence.
SPECS = [
    dict(row=32, mode='paleo', start_s=326.34, duration_s=9.76, source_rows=[13], alpha=False,
         labels=['100,000-YR HIGH', '2× 1M-YR AVERAGE']),
    dict(row=40, mode='temp_poles', start_s=415.04, duration_s=2.88, source_rows=[15], alpha=True,
         labels=['TEMPORARY POLES']),
    dict(row=47, mode='tangle', start_s=488.14, duration_s=4.72, source_rows=[18], alpha=False,
         labels=['SEVERAL POLES']),
    dict(row=48, mode='poles_map', start_s=493.66, duration_s=5.64, source_rows=[18], alpha=True,
         labels=['SOUTH POLE', 'AFRICA', 'NORTH POLE', 'TAHITI']),
    dict(row=51, mode='aurora', start_s=522.62, duration_s=10.36, source_rows=[18], alpha=False,
         labels=['LONDON', 'CAIRO', 'MUMBAI', 'SYDNEY']),
]


def caption(dr, xy, text, size, colour, t, start, end, anchor='mm'):
    if not start <= t < end:
        return
    opacity = max(0, min(1, (t - start) / .35, (end - t) / .35))
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    label(ImageDraw.Draw(layer), xy, text, size, colour, anchor)
    layer.putalpha(layer.getchannel('A').point(lambda p: round(p * opacity)))
    dr._image.alpha_composite(layer)


def credit(im):
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 28)
    dr.text((36, H - 52), 'NASA', font=font, fill=(244, 239, 230, 210))


def grid(im):
    dr = ImageDraw.Draw(im)
    for x in range(0, W, 80):
        dr.line((x, 0, x, H), fill=(32, 52, 75, 255))
    for y in range(0, H, 80):
        dr.line((0, y, W, y), fill=(32, 52, 75, 255))
    return dr


def marble(size=900):
    # Loaded once. The file is a real Blue Marble photograph, not a drawn disc.
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(MARBLE).convert('RGBA')
    im.thumbnail((size, size))
    return im


_MARBLE = None


def earth():
    global _MARBLE
    if _MARBLE is None:
        im = marble()
        mask = Image.new('L', im.size, 0)
        ImageDraw.Draw(mask).ellipse((2, 2, im.size[0] - 3, im.size[1] - 3), fill=255)
        im.putalpha(mask)
        _MARBLE = im
    return _MARBLE


def paleo(im, t):
    dr = grid(im)
    # Two sourced endpoints on one scale. The curve is a bracket, not a core log.
    base, top, x0, x1 = 860, 280, 420, 1500
    grow = ease(t / 1.1)
    dr.line((x0, base, x1, base), fill=WHITE, width=4)
    dr.line((x0, top, x0, base), fill=WHITE, width=4)
    if t >= 4.52:
        h = (base - top) * ease((t - 4.52) / .7)
        dr.rounded_rectangle((620, base - h, 860, base), radius=8, fill=BLUE)
    if t >= 7.68:
        h = (base - top) * 0.5 * ease((t - 7.68) / .6)
        dr.rounded_rectangle((1060, base - h, 1300, base), radius=8, fill=GOLD)
        # The average stays at half the today bar: the spoken "twice".
        dr.line((560, base - (base - top) * 0.5, 1400, base - (base - top) * 0.5), fill=WHITE, width=2)
    caption(dr, (960, 150), "TODAY'S FIELD", 64, GOLD, t, .4, 4.2)
    caption(dr, (740, 220), '100,000-YR HIGH', 42, WHITE, t, 5.76, 9.0)
    caption(dr, (1180, 220), '2× 1M-YR AVERAGE', 42, GOLD, t, 7.68, 9.76)
    _ = grow


def temp_poles(im, t):
    dr = ImageDraw.Draw(im)
    cx, cy, r = 1460, 520, 220
    dr.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLUE, width=4)
    n = min(6, int(ease(t / 1.2) * 6))
    for i in range(n):
        a = -math.pi / 2 + i * (math.tau / 6) + 0.15 * math.sin(t * 2 + i)
        x, y = cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a)
        pulse = 16 + 4 * math.sin(t * 3 + i)
        dr.ellipse((x - pulse, y - pulse, x + pulse, y + pulse), fill=GOLD)
        dr.line((cx, cy, x, y), fill=BLUE, width=3)
    caption(dr, (cx, cy + r + 70), 'TEMPORARY POLES', 48, GOLD, t, 1.32, 2.88)


def tangle(im, t):
    dr = grid(im)
    cx, cy = 960, 560
    for i in range(8):
        phase = ease(t / 1.4) * (0.4 + 0.15 * i)
        for s in range(24):
            u = s / 23
            ang = phase * math.sin(u * 6 + i) + i * 0.7
            rad = 40 + u * (220 + 30 * math.sin(t + i))
            x = cx + rad * math.cos(ang)
            y = cy + rad * math.sin(ang) * 0.72
            if s:
                dr.line((px, py, x, y), fill=BLUE if i % 2 == 0 else RED, width=4)
            px, py = x, y
        if t >= 1.36 and i < int(1 + 5 * ease((t - 1.36) / 1.2)):
            a = i * 1.05
            x = cx + 250 * math.cos(a)
            y = cy + 180 * math.sin(a)
            dr.ellipse((x - 18, y - 18, x + 18, y + 18), fill=GOLD)
    caption(dr, (960, 140), 'SEVERAL POLES', 64, GOLD, t, 1.36, 4.4)


def poles_map(im, t):
    """Alpha pins for a 900px Blue Marble pasted at (510, 90). Tahiti is not pinned."""
    dr = ImageDraw.Draw(im)
    # Southern Africa on GSFC_20171208_Archive_e001788, measured on the square face.
    ax, ay = 510 + 0.40 * 900, 90 + 0.62 * 900
    if t >= 1.52:
        p = ease((t - 1.52) / .35)
        y = ay - 40 * (1 - p)
        pulse = 12 + 3 * math.sin(t * 4)
        dr.ellipse((ax - pulse, y - pulse, ax + pulse, y + pulse), fill=GOLD)
        dr.line((ax, y, ax, y - 70), fill=GOLD, width=4)
        caption(dr, (ax, y - 110), 'SOUTH POLE', 40, GOLD, t, 1.52, 4.72, 'mm')
        caption(dr, (ax, y - 160), 'AFRICA', 36, WHITE, t, 1.52, 4.72, 'mm')
    if t >= 3.50:
        # Name only. This photograph does not show the Pacific face.
        caption(dr, (1560, 280), 'NORTH POLE', 44, GOLD, t, 3.50, 5.64)
        caption(dr, (1560, 340), 'TAHITI', 44, WHITE, t, 3.50, 5.64)
        caption(dr, (1560, 410), 'PACIFIC', 36, WHITE, t, 5.04, 5.64)


def aurora(im, t):
    body = earth()
    # Dim the day photograph enough to read curtains, and keep the frame above near-black.
    dim = Image.merge('RGBA', (
        body.getchannel('R').point(lambda p: int(p * 0.78)),
        body.getchannel('G').point(lambda p: int(p * 0.78)),
        body.getchannel('B').point(lambda p: int(p * 0.78)),
        body.getchannel('A')))
    im.paste(dim, (510, 40), dim)
    dr = ImageDraw.Draw(im)
    for i, colour in enumerate(((80, 220, 140, 150), (220, 60, 80, 130))):
        shift = (t * 40 + i * 70) % 180
        for band in range(4):
            y = 180 + band * 70 + shift * 0.3 + i * 24
            dr.arc((560, y, 1360, y + 220), 200, 340, fill=colour, width=18)
    names = [('LONDON', 5.98), ('CAIRO', 6.80), ('MUMBAI', 7.70), ('SYDNEY', 8.76)]
    for i, (name, start) in enumerate(names):
        caption(dr, (360 + i * 400, 960), name, 48, GOLD, t, start, min(start + 3.2, 10.36))
    credit(im)


def frame(spec, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0) if spec['alpha'] else NAVY + (255,))
    globals()[spec['mode']](im, t)
    if spec['alpha']:
        a = max(0, min(1, t / .4, (spec['duration_s'] - t) / .4))
        im.putalpha(im.getchannel('A').point(lambda p: round(p * a)))
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
