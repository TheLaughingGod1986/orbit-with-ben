#!/usr/bin/env python3
"""031 £0 field batch: age stack, sample map, extinction check, grid shield.

Schematics, not measured maps or datasets. Stripe counts, coast blobs and
icon positions are illustrative. The 300,000-year human comparison is not
drawn: those words are not in the locked line for row 11, so a label would
fail the WORDS match. No KEEP, motion review or stage approval.
"""
import math

from PIL import Image, ImageDraw

from evidence_graphics import caption, main as evidence_main
from mechanism_graphics import BLUE, GOLD, H, NAVY, RED, W, WHITE, ease

# Starts are locked Scribe word starts. Durations land in the following gap
# and are an exact number of frames at 25 fps.
SPECS = [
    dict(row=11, mode='strata', start_s=99.12, duration_s=12.28,
         cue='The younger rocks', source_rows=[4, 5], alpha=False,
         note='SCALE 300,000 years omitted; not spoken in this row'),
    dict(row=10, mode='matuyama_map', start_s=94.92, duration_s=3.96,
         cue='tests volcanic rocks', source_rows=[4], alpha=False,
         note='Schematic blobs, not a traced map. WHO card ends as Japan starts'),
    dict(row=45, mode='extinction_check', start_s=462.4, duration_s=6.6,
         cue='Across millions', source_rows=[2], alpha=True,
         note='Lower third left clear for the existing FACT card'),
    dict(row=46, mode='grid_shield', start_s=472.22, duration_s=7.76,
         cue='hardening', source_rows=[2], alpha=False,
         note='Starts at hardening so the SDO plate can lead the row'),
]


def grid(dr):
    for x in range(0, W, 80):
        dr.line((x, 0, x, H), fill=(32, 52, 75))
    for y in range(0, H, 80):
        dr.line((0, y, W, y), fill=(32, 52, 75))


def rock_band(dr, box, colour, t, delay):
    x0, y0, x1, y1 = box
    grow = ease((t - delay) / 0.45)
    if grow <= 0:
        return
    dr.rounded_rectangle((x0, y0, x0 + (x1 - x0) * grow, y1), radius=10, fill=colour)


def small_needle(dr, x, y, angle):
    u = (math.sin(angle), -math.cos(angle))
    dr.line((x - 22 * u[0], y - 22 * u[1], x + 22 * u[0], y + 22 * u[1]), fill=WHITE, width=5)
    dr.ellipse((x + 14 * u[0] - 5, y + 14 * u[1] - 5, x + 14 * u[0] + 5, y + 14 * u[1] + 5), fill=RED)


def strata(dr, spec, t):
    # Age stack only. Needles show the spoken north/south split, not a sample map.
    bands = [
        (230, (186, 122, 78), 'north'),
        (318, (168, 104, 68), 'north'),
        (406, (150, 92, 62), 'north'),
        (520, (122, 78, 64), 'south'),
        (608, (108, 70, 60), 'south'),
        (696, (96, 64, 58), 'south'),
        (784, (84, 58, 54), 'south'),
    ]
    for i, (y, colour, way) in enumerate(bands):
        rock_band(dr, (220, y, 1180, y + 72), colour, t, i * 0.08)
        if t < 0.7:
            continue
        target = 0 if way == 'north' else math.pi
        trigger = 1.15 if way == 'north' else 5.55
        angle = target * ease((t - trigger) / 0.45)
        wobble = 0.08 * math.sin(t * 3 + i)
        if t >= trigger:
            for x in (360, 560, 760, 960):
                small_needle(dr, x, y + 36, angle + wobble)
    if t >= 9.7:
        dr.line((200, 492, 200 + 1000 * ease((t - 9.7) / 0.35), 492), fill=GOLD, width=8)
    caption(dr, (1500, 280), 'YOUNGER → NORTH', 42, GOLD, t, 1.15, 4.7)
    caption(dr, (1500, 760), 'OLDER → SOUTH', 42, WHITE, t, 5.55, 9.3)
    caption(dr, (1500, 520), '780,000 YEARS AGO', 40, GOLD, t, 9.85, 12.28)


def blob(dr, box, colour):
    dr.ellipse(box, fill=colour, outline=GOLD, width=4)


def matuyama_map(dr, spec, t):
    # Two labelled regions and sample dots. Outlines are not a coastline trace.
    appear = ease(t / 0.4)
    if appear <= 0:
        return
    blob(dr, (260, 300, 860, 820), (78, 108, 96))
    for box in ((1040, 240, 1280, 460), (1160, 430, 1460, 700), (1080, 680, 1340, 920)):
        blob(dr, box, (92, 122, 108))
    japan = t >= 1.88
    manchuria = t >= 2.62
    if japan:
        for x, y in ((1120, 340), (1240, 520), (1180, 780), (1360, 600)):
            dr.ellipse((x - 14, y - 14, x + 14, y + 14), fill=GOLD)
    if manchuria:
        for x, y in ((400, 420), (560, 500), (480, 660), (680, 700)):
            dr.ellipse((x - 14, y - 14, x + 14, y + 14), fill=GOLD)
    caption(dr, (560, 200), 'MANCHURIA', 54, WHITE, t, 2.5, 3.96)
    caption(dr, (1240, 180), 'JAPAN', 54, GOLD, t, 1.75, 3.96)
    caption(dr, (960, 990), 'VOLCANIC ROCKS', 48, WHITE, t, 0.35, 3.5)


def extinction_check(dr, spec, t):
    # Two rows that do not line up. Not an extinction chronology.
    n = round(14 * ease(t / 1.2))
    for i in range(n):
        x = 280 + i * 90
        dr.rectangle((x, 180, x + 70, 280), fill=BLUE if i % 2 else RED)
    marks = [(420, 430), (780, 470), (1280, 440)]
    shown = round(len(marks) * ease((t - 1.2) / 0.8))
    for x, y in marks[:shown]:
        dr.regular_polygon((x, y, 18), 3, rotation=0, fill=WHITE)
    if t >= 3.3:
        span = 900 * ease((t - 3.3) / 0.4)
        # Break the rule around the words so the line does not strike the label.
        dr.line((360, 360, min(760, 360 + span), 360), fill=GOLD, width=8)
        if span > 520:
            dr.line((1160, 360, min(1260, 360 + span), 360), fill=GOLD, width=8)
    caption(dr, (960, 120), 'REVERSALS', 48, GOLD, t, 4.4, 6.6)
    caption(dr, (960, 560), 'EXTINCTIONS', 48, WHITE, t, 5.6, 6.6)
    caption(dr, (960, 360), 'NO LINK', 64, GOLD, t, 3.35, 6.4)


def satellite(dr, x, y, scale):
    dr.rounded_rectangle((x - 28, y - 18, x + 28, y + 18), radius=6, fill=WHITE)
    dr.rectangle((x - 90, y - 12, x - 34, y + 12), fill=BLUE)
    dr.rectangle((x + 34, y - 12, x + 90, y + 12), fill=BLUE)
    dr.line((x, y - 18, x, y - 48), fill=GOLD, width=4)


def pylon(dr, x, y):
    dr.line((x, y + 40, x, y + 170), fill=WHITE, width=6)
    dr.line((x - 46, y + 70, x + 46, y + 70), fill=WHITE, width=5)
    dr.line((x - 30, y + 102, x + 30, y + 102), fill=WHITE, width=4)
    dr.line((x - 18, y + 170, x, y + 40), fill=WHITE, width=3)
    dr.line((x + 18, y + 170, x, y + 40), fill=WHITE, width=3)


def grid_shield(dr, spec, t):
    satellite(dr, 620, 430, 1)
    pylon(dr, 1180, 390)
    pylon(dr, 1360, 390)
    pylon(dr, 1540, 390)
    dr.line((1180, 500, 1540, 500), fill=GOLD, width=4)
    shield = ease((t - 0.15) / 0.7)
    if shield > 0:
        bbox = (430, 220, 1710, 860)
        dr.arc(bbox, start=200, end=200 + 140 * shield, fill=GOLD, width=10)
    if t >= 2.2:
        for i in range(8):
            y = 200 + i * 70
            # Stop left of the shield. These are not a particle model.
            x2 = 300 + 24 * math.sin(t * 2 + i)
            dr.line((40, y, x2, y + 12), fill=RED, width=5)
    caption(dr, (620, 150), 'SATELLITES', 48, GOLD, t, 0.55, 3.4)
    caption(dr, (1360, 150), 'POWER GRIDS', 48, WHITE, t, 1.35, 4.3)
    caption(dr, (960, 960), 'SOLAR STORMS', 48, GOLD, t, 2.35, 5.5)
    # After the labels leave, the shield keeps a slow pulse so the frame is not a still.
    if t >= 5.5:
        pulse = 6 + 4 * math.sin(t * 3)
        dr.arc((430 - pulse, 220 - pulse, 1710 + pulse, 860 + pulse), start=200, end=340, fill=BLUE, width=6)


def frame(spec, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0) if spec['alpha'] else NAVY + (255,))
    dr = ImageDraw.Draw(im)
    if not spec['alpha']:
        grid(dr)
    globals()[spec['mode']](dr, spec, t)
    if spec['alpha']:
        fade = max(0, min(1, t / 0.4, (spec['duration_s'] - t) / 0.4))
        im.putalpha(im.getchannel('A').point(lambda p: round(p * fade)))
    return im


def main(argv=None):
    return evidence_main(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
