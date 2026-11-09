#!/usr/bin/env python3
"""R29 South Atlantic Anomaly strength plate. £0 schematic, not an ESA map.

The locked line is "Since 1970, that weak spot has widened and split into
two lobes." SOURCES row 12 (ESA Swarm, 20 May 2020) is the number source:
minimum strength about 24,000 nT to 22,000 nT, and westward growth of about
20 km per year, with a second centre. Those figures are drawn because
SHOT_LIST_v02 names them. They are not spoken in this sentence, so the
WORDS gate still has to be scored. Spoken labels (WEAK SPOT, WIDENED,
2 LOBES) land on the locked words.

Shapes are two illustrative blobs. They are not a traced coastline, a
copied Swarm contour, or a site. The bar is a zoomed 20,000–26,000 nT
window so the sourced drop is visible; it is not a zero-based collapse.
The upper right stays empty for the existing "1970" WHEN stamp
(301.44–305.04 s).
"""
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

from evidence_graphics import caption, main as render
from mechanism_graphics import BLUE, GOLD, H, NAVY, W, WHITE, ease

SPECS = [
    dict(row=29, mode='saa', start_s=301.20, duration_s=5.12,
         source_rows=[12], alpha=False, cue='Since',
         geometry='Schematic single blob that widens, drifts west and splits into two lobes. '
                  'Zoomed 20,000–26,000 nT bar from 24,000 to 22,000. Not an ESA/DTU contour.',
         source_url='https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Swarm/Swarm_probes_weakening_of_Earth_s_magnetic_field',
         clear='x>1080 and y<420 stays empty for the existing 1970 WHEN stamp.'),
]


def grid(dr):
    for x in range(0, W, 80):
        dr.line((x, 0, x, H), fill=(32, 52, 75))
    for y in range(0, H, 80):
        dr.line((0, y, W, y), fill=(32, 52, 75))


def ellipse(dr, cx, cy, rx, ry, fill):
    dr.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=fill)


def strength_bar(dr, t):
    # Zoomed window: 20,000 at the left, 26,000 at the right. Shared scale.
    x0, x1, y = 200, 980, 900
    drop = ease((t - 2.70) / 1.15) if t >= 2.70 else 0
    nt = 24000 - 2000 * drop

    def x_at(value):
        return x0 + (value - 20000) / 6000 * (x1 - x0)

    dr.rounded_rectangle((x0, y - 22, x1, y + 22), radius=12, outline=WHITE, width=4)
    dr.rounded_rectangle((x0 + 4, y - 16, x_at(nt), y + 16), radius=8, fill=GOLD)
    # The start mark stays so the drop still reads after the first caption leaves.
    mark = x_at(24000)
    dr.line((mark, y - 34, mark, y + 34), fill=WHITE, width=4)
    return nt


def lobes(dr, t):
    widen = ease((t - 2.70) / 0.85) if t >= 2.70 else 0
    split = ease((t - 3.54) / 0.7) if t >= 3.54 else 0
    drift = 16 * t
    cx, cy = 700 - drift, 500
    rx, ry = 130 + 70 * widen, 100
    bob = 8 * math.sin(t * 1.7)
    if split < 0.04:
        ellipse(dr, cx, cy + bob, rx, ry, GOLD)
        ellipse(dr, cx - 20, cy + bob, rx * 0.38, ry * 0.38, (255, 228, 160, 255))
        return cx, cy, rx
    sep = 36 + 170 * split
    lrx = rx * (1 - 0.15 * split)
    ellipse(dr, cx - sep, cy + bob, lrx, ry, GOLD)
    ellipse(dr, cx + sep * 0.8, cy - bob + 16 * split, lrx * 0.82, ry * 0.9, (255, 176, 72, 255))
    ellipse(dr, cx - sep - 10, cy + bob, lrx * 0.28, ry * 0.28, (255, 236, 190, 255))
    return cx - sep, cy, lrx


def west_arrow(dr, t):
    if t < 2.70 or t >= 4.50:
        return
    p = ease((t - 2.70) / 0.45)
    x2, x1, y = 150, 150 + round(210 * p), 640
    dr.line((x1, y, x2, y), fill=BLUE, width=8)
    dr.polygon([(x2, y), (x2 + 22, y - 14), (x2 + 22, y + 14)], fill=BLUE)


def frame(spec, t):
    im = Image.new('RGBA', (W, H), NAVY + (255,))
    dr = ImageDraw.Draw(im)
    grid(dr)
    lobes(dr, t)
    west_arrow(dr, t)
    strength_bar(dr, t)
    # Left side only. The 1970 stamp owns the upper right.
    caption(dr, (420, 150), '24,000 nT', 52, GOLD, t, 0.40, 2.55)
    caption(dr, (420, 230), 'WEAK SPOT', 48, WHITE, t, 1.92, 2.68)
    caption(dr, (420, 150), 'WIDENED', 52, GOLD, t, 2.70, 4.15)
    caption(dr, (420, 230), '22,000 nT', 52, GOLD, t, 3.40, 5.12)
    caption(dr, (360, 720), 'WESTWARD', 40, BLUE, t, 2.70, 4.35)
    caption(dr, (620, 720), '≈ 20 KM/YR', 40, WHITE, t, 2.70, 4.35)
    caption(dr, (420, 150), '2 LOBES', 56, GOLD, t, 4.24, 5.12)
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
        data['status'] = 'partial_saa_strength_only'
        data['spend_gbp'] = 0
        data['words_note'] = (
            '24,000 nT, 22,000 nT and about 20 km/yr are SOURCES row 12 figures named by '
            'SHOT_LIST_v02. They are not spoken on this line. WEAK SPOT, WIDENED and 2 LOBES '
            'follow the locked words. Upper right is clear for the existing 1970 stamp.'
        )
        got.manifest.write_text(json.dumps(data, indent=2) + '\n')


if __name__ == '__main__':
    main()
