#!/usr/bin/env python3
"""R11 qualitative polarity stack, not a measured stratigraphic section. £0.

Alpha overlay: composite over graded moving volcanic imagery. Equal layer
thicknesses encode no elapsed time, rock thickness or sample locations.
"""
from PIL import Image, ImageDraw
from mechanism_graphics import W, H, BLUE, GOLD, WHITE, ease
from evidence_graphics import arrow, caption, main as render

SPECS = [dict(
    row=11, mode='strata', start_s=99.12, duration_s=6.20,
    source_rows=[4], alpha=True,
    geometry='Qualitative younger/older polarity groups; not measured strata',
    source_url='https://doi.org/10.2183/pjab1912.5.203',
    required_plate='Graded moving volcanic plate; no flat background',
    remaining='Later 780,000-year WHEN component and SCALE comparison are separate',
)]


def frame(spec, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Arrows are magnetisation directions relative to today's north, not flow.
    for y, start, end, direction, colour, text in [
        (350, 0.14, 2.10, -1, BLUE, 'YOUNGER ROCKS'),
        (700, 2.54, 6.20, 1, GOLD, 'OLDER')]:
        if not start <= t < end:
            continue
        p = ease((t-start)/0.45)
        opacity = max(0, min(1, (t-start)/0.35, (end-t)/0.35))
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle((1070, y-90, 1070+round(650*p), y+90),
                             radius=12, fill=colour+(70,), outline=colour, width=4)
        arrow(ld, 1170, y-direction*55*p, 1170, y+direction*55*p,
              colour=WHITE, width=7)
        caption(ld, (1450, y-25), text, 45, WHITE, t, start, end)
        # NORTH/SOUTH appear only when their exact locked words are spoken.
        cue = 1.30 if direction == -1 else 5.70
        caption(ld, (1450, y+40), 'NORTH' if direction == -1 else 'SOUTH',
                48, colour, t, cue, end)
        layer.putalpha(layer.getchannel('A').point(lambda v: round(v*opacity)))
        im.alpha_composite(layer)
    a = max(0, min(1, t/0.4, (spec['duration_s']-t)/0.4))
    im.putalpha(im.getchannel('A').point(lambda v: round(v*a)))
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
