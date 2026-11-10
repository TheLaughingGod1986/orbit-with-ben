#!/usr/bin/env python3
"""R1 pole-speed label component; no invented route or time series. £0."""
from PIL import Image, ImageDraw
from mechanism_graphics import W, H, WHITE, GOLD, BLUE, ease
from evidence_graphics import caption, main as render

SPECS = [dict(row=1, mode='pole_speed', start_s=4.52, duration_s=3.8,
              source_rows=[1], alpha=True, component_only=True,
              source_url='https://www.ncei.noaa.gov/products/wandering-geomagnetic-poles',
              source_checked='2026-11-07',
              geometry='Qualitative animated accent and sourced upper speed label. '
                       'No map, geographic path, measured time series or present-day speed claim.',
              requires='Graded moving real imagery, subject clearance, complete poledrift scene and composite review')]


def frame(s, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # The line is a reveal accent, deliberately no axis, ticks or moving pole dot.
    p = ease(t / .6)
    d.line((1100, 420, 1100 + round(600*p), 420), fill=BLUE, width=5)
    caption(d, (1400, 520), 'NORTH MAGNETIC POLE', 46, WHITE, t, 0, 3.8)
    caption(d, (1400, 640), 'UP TO 55 KM/YR', 54, GOLD, t, 1.48, 3.8)
    a = max(0, min(1, t/.4, (s['duration_s']-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda v: round(v*a)))
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
