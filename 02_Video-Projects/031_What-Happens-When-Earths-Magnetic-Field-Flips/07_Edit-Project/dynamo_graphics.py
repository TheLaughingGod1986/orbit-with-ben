#!/usr/bin/env python3
"""R16, R17 and R52 dynamo plates. £0 schematics, not a geodynamo simulation.

SOURCES row 6 is the liquid outer core whose moving metal makes the field.
These drawings show that idea: current loops lining up, then red eddies
fighting them until the dipole tips. They are not the NASA SVS Glatzmaier–
Roberts clips, and they do not invent a field model. R52 only shows the
locked line that the iron settled and the compass locked south (row 18).
No KEEP, composite review or stage approval is implied by encoding.
"""
import math

from PIL import Image, ImageDraw, ImageFont

from mechanism_graphics import W, H, NAVY, WHITE, GOLD, BLUE, RED, FONT, ease, label, needle
from evidence_graphics import caption, main as render

# Full-frame cuts end in the gap after the last word they cover.
# R16 runs to "However" (168.76), not an 8 s cut inside "south pole".
# R17 includes the whole of "over." (ends 186.98) and one frame of the gap.
# R52 starts on "settled" and includes "south." (ends 546.38).
SPECS = [
    dict(row=16, mode='dynamo', variant='align', start_s=159.32, duration_s=9.44,
         source_rows=[6], alpha=False, cue='Most of the time',
         geometry='Schematic iron-current loops easing into one stack, then N and S '
                  'marks. Not a measured geodynamo and not the NASA SVS clip.'),
    dict(row=17, mode='dynamo', variant='tip', start_s=172.68, duration_s=14.32,
         source_rows=[6], alpha=False, cue='Swirling eddies',
         geometry='Schematic red eddies opposing the aligned flow, then the same '
                  'dipole weakening, wobbling and turning over. Not a simulation.'),
    dict(row=52, mode='dynamo', variant='settle', start_s=544.0, duration_s=2.4,
         source_rows=[18], alpha=False, cue='settled',
         geometry='Loops settling and a compass needle locking south. No new number. '
                  'The generations overlay already covers the earlier part of the row.'),
]


def rotp(x, y, rot, origin):
    ox, oy = origin
    dx, dy = x - ox, y - oy
    c, s = math.cos(rot), math.sin(rot)
    return ox + dx * c - dy * s, oy + dx * s + dy * c


def draw_loop(d, cx, cy, angle, phase, colour, origin, rot):
    rx, ry = 150, 46
    pts = []
    for i in range(36):
        a = 2 * math.pi * i / 36
        x = cx + rx * math.cos(a) * math.cos(angle) - ry * math.sin(a) * math.sin(angle)
        y = cy + rx * math.cos(a) * math.sin(angle) + ry * math.sin(a) * math.cos(angle)
        pts.append(rotp(x, y, rot, origin))
    d.line(pts + [pts[0]], fill=colour, width=4)
    a = phase
    x = cx + rx * math.cos(a) * math.cos(angle) - ry * math.sin(a) * math.sin(angle)
    y = cy + rx * math.cos(a) * math.sin(angle) + ry * math.sin(a) * math.cos(angle)
    bx, by = rotp(x, y, rot, origin)
    d.ellipse((bx - 7, by - 7, bx + 7, by + 7), fill=GOLD)


def pole_letter(im, text, pt):
    if not (100 < pt[0] < W - 100 and 80 < pt[1] < H - 80):
        return
    layer = Image.new('RGBA', (80, 64), (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    font = ImageFont.truetype(FONT, 42)
    dr.text((40, 32), text, font=font, anchor='mm', fill=GOLD)
    im.alpha_composite(layer, (int(pt[0] - 40), int(pt[1] - 56)))


def draw_core(im, t, cx, align, red, weaken, rot, wobble):
    d = ImageDraw.Draw(im)
    origin = (cx, 540)
    seeds = [1.1, -0.8, 1.6, -1.3, 0.7]
    for i, y in enumerate((380, 460, 540, 620, 700)):
        angle = seeds[i] * (1 - align) + wobble
        draw_loop(d, cx, y, angle, (t * 1.7 + i) % (2 * math.pi), BLUE, origin, rot)
    pulse = 1 + 0.045 * math.sin(t * 2.2)
    north = rotp(cx, 300, rot, origin)
    south = rotp(cx, 780, rot, origin)
    if weaken > 0.08:
        for sign in (-1, 1):
            pts = []
            for i in range(28):
                p = i / 27
                x = cx + sign * 210 * weaken * pulse * math.sin(math.pi * p)
                y = 300 + 480 * p
                pts.append(rotp(x, y, rot, origin))
            d.line(pts, fill=BLUE, width=max(2, round(6 * weaken)))
    for pt, col in ((north, RED), (south, BLUE)):
        r = 14 * weaken + 8
        d.ellipse((pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r), fill=col)
    if red > 0.04:
        for i in range(4):
            ang = -t * 1.35 + i * math.pi / 2
            rad = (150 + 36 * math.sin(t * 1.4 + i)) * red
            ex = cx + rad * math.cos(ang)
            ey = 540 + rad * 0.62 * math.sin(ang)
            ex, ey = rotp(ex, ey, rot * 0.15, origin)
            d.ellipse((ex - 34, ey - 22, ex + 34, ey + 22), outline=RED, width=4)
            bead = (-t * 3.1 + i) % (2 * math.pi)
            bx, by = ex + 24 * math.cos(bead), ey + 14 * math.sin(bead)
            d.ellipse((bx - 6, by - 6, bx + 6, by + 6), fill=RED)
    if align > 0.45:
        pole_letter(im, 'N', north)
        pole_letter(im, 'S', south)


def compass(d, t, lock):
    x, y, r = 1500, 560, 148
    d.ellipse((x - r - 8, y - r - 8, x + r + 8, y + r + 8), fill=(119, 88, 42, 255), outline=GOLD, width=4)
    d.ellipse((x - r, y - r, x + r, y + r), fill=NAVY + (255,), outline=(196, 160, 92), width=4)
    label(d, (x, y - r + 36), 'N', 32, RED)
    label(d, (x, y + r - 36), 'S', 32, WHITE)
    angle = (0.55 * math.sin(t * 5)) * (1 - lock) + math.pi * lock
    needle(d, x, y, angle, r * 0.62, r * 0.09)


def frame(spec, t):
    im = Image.new('RGBA', (W, H), NAVY + (255,))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 80):
        d.line((x, 0, x, H), fill=(32, 52, 75, 255))
    for y in range(0, H, 80):
        d.line((0, y, W, y), fill=(32, 52, 75, 255))
    kind = spec['variant']
    if kind == 'align':
        align = ease((t - 0.8) / 2.8)
        draw_core(im, t, 960, align, 0, 1, 0, 0.05 * math.sin(t * 1.6) * align)
        caption(d, (960, 150), 'IRON CURRENTS', 56, GOLD, t, 2.7, 3.74)
        caption(d, (960, 150), 'LINED UP', 56, GOLD, t, 3.74, 6.2)
        caption(d, (960, 150), 'NORTH POLE', 56, GOLD, t, 6.26, 8.05)
        caption(d, (960, 960), 'SOUTH POLE', 56, WHITE, t, 8.1, 9.44)
    elif kind == 'tip':
        red = ease(t / 2.6)
        weaken = 1 if t < 10.5 else 1 - 0.62 * ease((t - 10.5) / 1.6)
        wobble = 0.22 * math.sin(t * 2.4) * ease((t - 11.52) / 0.45) if t > 11.2 else 0.04 * math.sin(t)
        rot = math.pi * ease((t - 13.26) / 0.9) if t > 13.26 else 0
        draw_core(im, t, 960, 1, red, weaken, rot, wobble)
        caption(d, (960, 150), 'SWIRLING EDDIES', 52, GOLD, t, 0.15, 2.9)
        caption(d, (960, 150), 'MAIN FLOW', 56, GOLD, t, 3.5, 4.7)
        caption(d, (960, 150), 'BACKWARDS EDDIES', 48, RED, t, 6.18, 8.4)
        caption(d, (960, 150), 'FIELD WEAKENS', 52, GOLD, t, 10.5, 11.45)
        caption(d, (960, 150), 'WOBBLES', 56, GOLD, t, 11.52, 13.2)
        caption(d, (960, 150), 'ALL THE WAY OVER', 48, GOLD, t, 13.48, 14.32)
    else:
        align = ease(t / 1.1)
        lock = ease((t - 0.84) / 0.85)
        draw_core(im, t, 700, align, 0.35 * (1 - align), 1, math.pi * align, 0.08 * math.sin(t * 3) * (1 - lock))
        compass(d, t, lock)
        caption(d, (700, 160), 'SETTLED', 56, GOLD, t, 0.08, 1.35)
        caption(d, (1500, 180), 'COMPASS SOUTH', 44, WHITE, t, 1.42, 2.4)
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
