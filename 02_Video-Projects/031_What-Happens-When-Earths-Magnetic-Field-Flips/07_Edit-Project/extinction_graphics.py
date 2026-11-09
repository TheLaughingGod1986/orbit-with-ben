#!/usr/bin/env python3
"""R45 qualitative comparison overlay; no invented chronology or measurements."""
from PIL import Image, ImageDraw
from mechanism_graphics import W, H, GOLD, WHITE, BLUE, ease
from evidence_graphics import caption, main as render

SPECS = [dict(row=45, mode='extinction_check', start_s=465.56,
              duration_s=3.42, source_rows=[2], alpha=True,
              source_url='https://geomag.bgs.ac.uk/education/reversals.html',
              labels=['MAGNETIC REVERSALS', 'MASS EXTINCTIONS', 'NO LINK'],
              interpretation='Qualitative relationship only; no event positions, counts, time axis or correlation coefficient.')]


def frame(spec, t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Upper-right area avoids the existing lower-left FACT card. The actual
    # plate subject must still be checked in composite. The separated brackets
    # are a relationship symbol, never a plotted extinction/reversal dataset.
    p = ease(t / .5)
    d.line((1080, 250, 1080 + round(640*p), 250), fill=BLUE, width=5)
    caption(d, (1400, 320), 'MAGNETIC REVERSALS', 46, WHITE, t, .12, 3.42)
    caption(d, (1400, 570), 'MASS EXTINCTIONS', 46, WHITE, t, .24, 3.42)
    gap = 25 + round(55*ease(t/.7))
    d.line((1400, 370, 1400, 435-gap), fill=BLUE, width=5)
    d.line((1400, 455+gap, 1400, 520), fill=BLUE, width=5)
    caption(d, (1400, 445), 'NO LINK', 68, GOLD, t, .26, 3.42)
    a = max(0, min(1, t/.4, (spec['duration_s']-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda v: round(v*a)))
    return im


def main(argv=None):
    return render(argv, specs=SPECS, render_frame=frame)


if __name__ == '__main__':
    main()
