#!/usr/bin/env python3
"""R32 sourced ratio component, not a measured paleointensity curve. £0."""
from PIL import Image, ImageDraw
from mechanism_graphics import W, H, WHITE, GOLD, BLUE, ease
from evidence_graphics import caption, main as render

SPECS = [dict(row=32, mode='paleo_ratio', start_s=329.54, duration_s=6.56,
              source_rows=[13], alpha=True,
              geometry='Shared zero and scale: today 1, million-year average 0.5. '
                       'No invented historical samples or chronology.')]


def frame(s, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Right-side overlay requires graded moving plate and subject clearance.
    x, width = 1080, 620
    d.line((x, 460, x, 850), fill=WHITE, width=4)
    p = ease((t-2.56) / .7)
    if t >= 2.56:
        d.rounded_rectangle((x, 490, x + max(1, round(width*p)), 535),
                            radius=8, fill=BLUE)
    caption(d, (1390, 400), 'TODAY', 54, GOLD, t, 0, 2.56)
    caption(d, (1390, 400), '100,000 YEARS', 48, GOLD, t, 2.56, 4.48)
    # Exact "twice" word begins at 334.02 s, 4.48 s into this component.
    if t >= 4.48:
        q = ease((t-4.48)/.45)
        d.rounded_rectangle((x, 730, x+max(1, round(width*.5*q)), 775),
                            radius=8, fill=GOLD)
        caption(d, (1390, 400), 'TWICE ITS AVERAGE', 48, GOLD, t, 4.48, 6.56)
        caption(d, (1390, 570), 'TODAY', 44, WHITE, t, 4.48, 6.56)
        caption(d, (1390, 650), 'MILLION-YEAR AVERAGE', 44, WHITE, t, 4.48, 6.56)
    a = max(0, min(1, t/.4, (s['duration_s']-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda v: round(v*a)))
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
