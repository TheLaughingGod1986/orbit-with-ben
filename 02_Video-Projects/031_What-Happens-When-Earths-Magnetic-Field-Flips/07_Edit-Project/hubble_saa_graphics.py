#!/usr/bin/env python3
"""R27 Hubble SAA count. £0 schematic overlay, not an orbit or anomaly map.

The 7-to-9 range is the locked SOURCES row 11 quote (HST Cycle 26 primer):
seven to nine orbits in a row each day. Glyphs are a tally of that range,
not a measured ground track. Place over the moving Hubble plate, clear of
the telescope. The existing FACT card starts at "stops observing".
"""
import math
from PIL import Image, ImageDraw
from mechanism_graphics import W, H, BLUE, GOLD, WHITE, ease
from evidence_graphics import caption, main as render

SPECS = [
    dict(row=27, mode='hubble_saa', start_s=280.42, duration_s=4.64,
         source_rows=[11], alpha=True,
         cue='seven to nine orbits in a row every day',
         geometry='Schematic oval and a 7-then-9 tally. No geographic SAA contour or Hubble orbit elements.'),
]


def orbit(d, t):
    cx, cy, rx, ry = 1450, 500, 280, 150
    # The oval draws once, then the icon keeps moving. The gold arc is only the
    # part of that same oval already drawn; it is not a geographic dent.
    drawn = ease(min(1, t / 0.7))
    steps = max(2, round(drawn * 160))
    blue, gold = [], []
    for i in range(steps):
        a = -math.pi / 2 + 2 * math.pi * i / 160
        ang = a % (2 * math.pi)
        p = (cx + rx * math.cos(a), cy + ry * math.sin(a))
        on_dent = 0.25 * math.pi <= ang <= 0.80 * math.pi
        if on_dent:
            if len(blue) > 1:
                d.line(blue, fill=BLUE, width=6)
            blue = []
            gold.append(p)
        else:
            if len(gold) > 1:
                d.line(gold, fill=GOLD, width=12)
            gold = []
            blue.append(p)
    if len(blue) > 1:
        d.line(blue, fill=BLUE, width=6)
    if len(gold) > 1:
        d.line(gold, fill=GOLD, width=12)
    if drawn >= 0.999:
        a0 = -math.pi / 2
        a1 = a0 + 2 * math.pi * 159 / 160
        d.line([(cx + rx * math.cos(a1), cy + ry * math.sin(a1)),
                (cx + rx * math.cos(a0), cy + ry * math.sin(a0))], fill=BLUE, width=6)
    travel = drawn if t < 0.7 else 1 + (t - 0.7) / 3.3
    ang = -math.pi / 2 + 2 * math.pi * travel
    sx, sy = cx + rx * math.cos(ang), cy + ry * math.sin(ang)
    d.rounded_rectangle((sx - 26, sy - 16, sx + 26, sy + 16), radius=5, outline=WHITE, width=4)
    d.ellipse((sx - 6, sy - 6, sx + 6, sy + 6), fill=GOLD)
    if 0.25 * math.pi <= (ang % (2 * math.pi)) <= 0.80 * math.pi:
        d.ellipse((sx - 18, sy - 18, sx + 18, sy + 18), outline=GOLD, width=3)


def tally(d, t):
    # Seven marks build on "seven"; two more arrive with "nine" (0.48 s).
    count = round(7 * ease(t / 0.42)) if t < 0.48 else 7 + round(2 * ease((t - 0.48) / 0.42))
    for i in range(count):
        x, y = 1210 + (i % 5) * 96, 800 + (i // 5) * 72
        d.ellipse((x - 30, y - 16, x + 30, y + 16), outline=GOLD, width=4)
        d.ellipse((x + 16, y - 6, x + 28, y + 6), fill=WHITE)


def frame(s, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    orbit(d, t)
    tally(d, t)
    # Labels follow the locked words: seven to nine, then orbits, then in a row, then every day.
    caption(d, (1450, 200), '7 TO 9', 56, GOLD, t, 0, 0.86)
    caption(d, (1450, 200), '7 TO 9 ORBITS', 52, GOLD, t, 0.86, 4.24)
    caption(d, (1450, 280), 'IN A ROW', 48, WHITE, t, 1.22, 4.24)
    caption(d, (1450, 720), 'EVERY DAY', 48, WHITE, t, 2.00, 4.24)
    alpha = max(0, min(1, t / .4, (s['duration_s'] - t) / .4))
    im.putalpha(im.getchannel('A').point(lambda p: round(p * alpha)))
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
