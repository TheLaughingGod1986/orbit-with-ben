#!/usr/bin/env python3
"""R30 midpoint twist card. Alpha overlay for a graded moving plate.

Timed to the locked line "Case closed? Are we overdue...". Each caption is
under four seconds and at most four words. The shot list's 0.3 s cut to black
stays an assembly cut: this file does not bake a black slab. No KEEP.
"""
from PIL import Image, ImageDraw
from mechanism_graphics import W, H, GOLD, ease
from evidence_graphics import caption, main as render

SPECS = [
    dict(row=30, mode='twist', start_s=313.82, duration_s=3.96, source_rows=[],
         alpha=True, cue='Case closed',
         geometry='Two sequential spoken questions; no new measured claim'),
]


def frame(spec, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    # Swap on the locked word "Are" (315.52 s). Neither line holds for 4 s.
    if t < 1.70:
        span, text, size, start = 1.70, 'CASE CLOSED?', 72, 0
        grow = ease(t / .4)
    else:
        span, text, size, start = 3.96, 'ARE WE OVERDUE?', 64, 1.70
        grow = ease((t - 1.70) / .35)
    width = round((560 if t < 1.70 else 760) * grow)
    dr.line((1400 - width // 2, 590, 1400 - width // 2 + width, 590), fill=GOLD, width=6)
    caption(dr, (1400, 500), text, size, GOLD, t, start, span)
    fade = max(0, min(1, t / .4, (spec['duration_s'] - t) / .4))
    im.putalpha(im.getchannel('A').point(lambda v: round(v * fade)))
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
