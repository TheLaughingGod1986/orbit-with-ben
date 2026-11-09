#!/usr/bin/env python3
"""R13 depth ruler component, £0; requires a graded moving plate.

This is a local depth ruler, not Earth geometry or a layer-thickness model.
It complements the still-unbuilt layers scene. No Chief approval implied.
"""
from PIL import Image, ImageDraw
from mechanism_graphics import W, H, BLUE, GOLD, WHITE, ease
from evidence_graphics import caption, main as render

SPECS = [dict(row=13, mode='depth', start_s=125.9, duration_s=3.6,
              source_rows=[6], alpha=True,
              geometry='Local linear depth ruler, surface zero to about 3000 km; '
                       'no globe, layer thicknesses or measured dynamo model',
              component_only=True,
              requires='Graded moving real plate, subject clearance and Chief review; '
                       'not a replacement for the complete layers scene')]


def frame(spec, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    x, top, bottom = 1350, 320, 790
    progress = ease(t / 1.24)
    tip = top + round((bottom - top) * progress)
    # Common zero, linear scale. Unlabelled ticks divide the ruler evenly.
    dr.line((x, top, x, bottom), fill=(100, 194, 247, 100), width=4)
    for i in range(7):
        y = top + round((bottom - top) * i / 6)
        dr.line((x-16, y, x+16, y), fill=BLUE, width=3)
    dr.line((x, top, x, tip), fill=GOLD, width=7)
    dr.polygon([(x-14, tip-18), (x+14, tip-18), (x, tip)], fill=GOLD)
    caption(dr, (1530, top), 'SURFACE', 40, WHITE, t, 0, 3.6)
    caption(dr, (1530, bottom), '≈ 3,000 KM', 48, GOLD, t, 0, 3.6)
    caption(dr, (1400, 930), 'BENEATH YOUR SHOES', 48, WHITE, t, 1.32, 3.6)
    opacity = max(0, min(1, t/.4, (spec['duration_s']-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda v: round(v*opacity)))
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
