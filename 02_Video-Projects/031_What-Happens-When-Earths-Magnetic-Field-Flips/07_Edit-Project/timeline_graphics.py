#!/usr/bin/env python3
"""Progressive historical-date alpha overlays, £0; no finished composite implied.

Dates accumulate in narrative order, remain chronologically ordered on screen.
Spacing is categorical, explicitly NOT TO SCALE; no invented measured history.
Geological ages and durations belong to separate existing graphics.
"""
from PIL import Image, ImageDraw
from mechanism_graphics import W, H, GOLD, WHITE, BLUE, ease, label
from evidence_graphics import main as render

DATES = ['1830s', '1905', '1929', '1970', '2013']
EVENTS = [
    (5, '1905', 36.14, 3),
    (10, '1929', 89.94, 4),
    (20, '1830s', 209.10, 8),
    (24, '2013', 234.58, 9),
    (29, '1970', 301.44, 12),
]
SPECS = []
seen = []
for row, date, start, source in EVENTS:
    SPECS.append(dict(row=row, mode='timeline', start_s=start, duration_s=3.6,
        source_rows=[source], alpha=True, current=date, previous=list(seen),
        labels=DATES + ['NOT TO SCALE'],
        compositor_note='Replace standalone WHEN stamp in this window; moving graded plate required.'))
    seen.append(date)


def frame(s, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, x1, y = 240, 1680, 225
    # Draw-in is an entrance animation; line length conveys no elapsed interval.
    d.line((x0, y, x0 + round((x1-x0)*ease(t/.5)), y), fill=BLUE+(220,), width=5)
    label(d, (960, 90), 'NOT TO SCALE', 38, WHITE)
    for i, date in enumerate(DATES):
        x = x0 + i*(x1-x0)/4
        if date not in s['previous'] and date != s['current']:
            continue  # Future dates are not revealed early.
        active = date == s['current']
        progress = ease((t-.35)/.45) if active else 1
        drop = round(50*(1-progress)) if active else 0
        colour = GOLD if active else WHITE
        layer = Image.new('RGBA', (W,H), (0,0,0,0))
        ld = ImageDraw.Draw(layer)
        ld.ellipse((x-12,y-12-drop,x+12,y+12-drop),fill=colour)
        label(ld,(x,y+76-drop),date,58 if active else 46,colour)
        layer.putalpha(layer.getchannel('A').point(lambda a:round(a*progress)))
        im.alpha_composite(layer)
    fade = max(0,min(1,t/.4,(s['duration_s']-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda a:round(a*fade)))
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)

if __name__ == '__main__':
    main()
