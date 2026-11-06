#!/usr/bin/env python3
"""R44 gravity comparison with real NASA bodies; equal-size icons aren't a size scale.

Reuses the sourced, locked-cue gravity bars. This is a complete short graphic,
not an extra consecutive cut to stack beside the original alpha component.
"""
import hashlib
import json
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from evidence_graphics import HERE, main as render
from mechanism_graphics import W, H, NAVY, WHITE, ease
from scale_graphics import frame as bars

POOL = json.loads((HERE/'HARVEST_POOL_v01.json').read_text())
ASSETS = {a['asset_id']: a for a in POOL['assets']}
EARTH = 'as17-148-22727'
MARS = 'PIA00407'
SPECS = [dict(row=44, mode='gravity_bodies', start_s=449.92,
    duration_s=2.28, source_rows=[17], alpha=False,
    cue='with just over a third',
    asset_ids=[EARTH, MARS],
    geometry='Equal-display-diameter body icons identify the bars; no planet-size comparison. Bars share zero: Earth 1.00, Mars 0.38.',
    replaces_component='CODE_SCALES_v01.json R44 gravity; do not add as a consecutive graphic',
    planned_mars_use=2, maximum_mars_appearances=2)]

@lru_cache(maxsize=2)
def body(ident):
    a = ASSETS[ident]
    p = Path(a['local_path'])
    if hashlib.sha256(p.read_bytes()).hexdigest() != a['sha256']:
        raise ValueError('NASA input hash mismatch: '+ident)
    src = Image.open(p).convert('RGBA')
    # Apollo globe crop excludes the original black surround; Mars is full-frame.
    if ident == EARTH:
        src = src.crop(tuple(a['crop_box']))
    src = src.resize((210, 210), Image.Resampling.LANCZOS)
    mask = Image.new('L', src.size)
    ImageDraw.Draw(mask).ellipse((1, 1, 208, 208), fill=255)
    src.putalpha(mask)
    return src

def frame(spec, t):
    im = Image.new('RGBA', (W,H), NAVY+(255,))
    d = ImageDraw.Draw(im)
    for x in range(0,W,80): d.line((x,0,x,H),fill=(36,58,84))
    for y in range(0,H,80): d.line((0,y,W,y),fill=(36,58,84))
    # Body icons align with their bars. A gentle slide animates the entrance;
    # the entire shot is shorter than the four-second static-hold ceiling.
    x = 780-round(25*(1-ease(t/.4)))
    for ident,y in [(EARTH,510),(MARS,730)]:
        icon=body(ident).copy()
        a=max(0,min(1,t/.4,(spec['duration_s']-t)/.4))
        icon.putalpha(icon.getchannel('A').point(lambda v:round(v*a)))
        im.alpha_composite(icon,(x,y-105))
    im.alpha_composite(bars(dict(duration_s=spec['duration_s'],mode='gravity'),t))
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',28)
    ImageDraw.Draw(im).text((48,1008),'NASA · NASA/JPL/USGS · CGI',font=font,fill=WHITE)
    return im

def main(argv=None):
    return render(argv,specs=SPECS,render_frame=frame)

if __name__=='__main__': main()
