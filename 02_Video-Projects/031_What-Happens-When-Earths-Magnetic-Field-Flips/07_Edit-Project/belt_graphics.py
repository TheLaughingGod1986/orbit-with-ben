#!/usr/bin/env python3
"""R25 altitude ruler overlays. £0; schematic, not belt geometry or a model.

Equal vertical distances encode equal altitude increments. Use over distinct
moving real plates, with subject clearance. The 600/200/400 km values follow
locked SOURCES row 10; these are approximate reference values, not a profile.
The core patch, belt geometry and intervening real shot remain unfinished.
"""
from PIL import Image, ImageDraw
from mechanism_graphics import W, H, GOLD, WHITE, BLUE, RED, ease
from evidence_graphics import caption, main as render

SPECS = [
    dict(row=25, mode='belts_normal', start_s=248.72, duration_s=2.4,
         source_rows=[10], alpha=True,
         geometry='Shared zero altitude ruler, approximate 600 km reference; no physical belt geometry'),
    dict(row=25, mode='belts_dip', start_s=259.18, duration_s=5.56,
         source_rows=[10], alpha=True,
         geometry='Shared zero altitude ruler; 200 km is half the approximately 400 km ISS reference; transition schematic'),
]


def y_at(km):
    return 900 - km * .8


def ruler(d, t):
    x = 1210
    d.line((x, y_at(0), x, y_at(650)), fill=WHITE, width=4)
    for km in (0, 200, 400, 600):
        y = y_at(km)
        d.line((x-10, y, x+12, y), fill=WHITE, width=3)
    # Surface label is deliberately brief; ruler remains visible as labels change.
    caption(d, (1350, 960), 'SURFACE · 0 KM', 40, WHITE, t, 0, 2.4)


def marker(d, km, colour, t):
    y = y_at(km)
    d.line((1230, y, 1230+round(450*ease(t/.45)), y), fill=colour, width=6)
    d.ellipse((1200, y-10, 1220, y+10), fill=colour)


def frame(s, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ruler(d, t)
    if s['mode'] == 'belts_normal':
        marker(d, 600, GOLD, t)
        caption(d, (1450, 275), 'TRAPPED RADIATION', 48, WHITE, t, 0, 2.4)
        # 600 starts on its actual spoken cue (250.12 s).
        caption(d, (1460, 365), 'BEYOND ≈ 600 KM', 48, GOLD, t, 1.4, 2.4)
    else:
        # Motion represents the narrated sag; not a measured temporal model.
        height = 600-400*ease(t/1.84)
        marker(d, height, GOLD, t)
        caption(d, (1450, 275), 'RADIATION DIPS', 48, WHITE, t, 0, 3.54)
        caption(d, (1450, 795), '≈ 200 KM', 50, GOLD, t, 1.839, 5.56)
        # The comparison starts with 'half' at 262.72 s.
        if t >= 3.54:
            marker(d, 400, BLUE, t-3.54)
        caption(d, (1450, 510), 'ISS ≈ 400 KM', 46, BLUE, t, 3.54, 5.56)
        caption(d, (1450, 275), 'HALF THE HEIGHT', 50, GOLD, t, 3.54, 5.56)
    alpha = max(0, min(1, t/.4, (s['duration_s']-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda p: round(p*alpha)))
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
