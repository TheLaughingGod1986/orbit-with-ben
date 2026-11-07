#!/usr/bin/env python3
"""R23 fixed-position connector DRAFT. No approved export is changed.

9.5 AU is heliocentric, not Huygens's landing distance from Earth. No
quantitative bar, trajectory, planetary ordering or new distance is invented.
"""
import argparse
import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw
from code_graphics import W, H, GOLD, WHITE, font

SOURCE = Path('/Users/benjaminoats/_desk/cache/J2089/harvest_v01/PIA14909.jpg')
SOURCE_HASH = 'b72f5371622b0197f91a70a62b729e1e854dd91c511639f8055cf3d93f70ce74'
CROP = (295, 294, 703, 702)
SECONDS = 3.6
URL = 'https://science.nasa.gov/mission/cassini-huygens/'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

@lru_cache(maxsize=1)
def body():
    assert sha(SOURCE) == SOURCE_HASH, 'Source changed'
    with Image.open(SOURCE) as source:
        image = source.convert('RGBA').crop(CROP)
    mask = Image.new('L', image.size)
    ImageDraw.Draw(mask).ellipse((0, 0, 407, 407), fill=255)
    image.putalpha(mask)
    return image  # Native pixels: no upscale, no new surface texture.

def frame(t):
    im = Image.new('RGBA', (W, H))
    im.alpha_composite(body(), (1290, 350))
    d = ImageDraw.Draw(im)
    def text(xy, value, size, colour=WHITE):
        d.text(xy, value, font=font(size), fill=colour,
               stroke_width=3, stroke_fill=(20, 28, 42, 220))
    text((160, 140), 'MOST DISTANT LANDING', 78, GOLD)
    text((160, 330), 'HUYGENS', 62)
    text((160, 750), 'FROM EARTH', 54)
    text((1330, 790), 'TITAN', 62, GOLD)
    # A qualitative connector, explicitly not a scale or flight trajectory.
    p = min(1, max(0, (t-.4)/1.8))
    x = 1180
    connector = Image.new("RGBA", (W,H))
    cd = ImageDraw.Draw(connector)
    if p:
        cd.line((200, 560, x, 560), fill=GOLD, width=6)
        cd.polygon([(x, 560), (x-22, 547), (x-22, 573)], fill=GOLD)
        connector.putalpha(connector.getchannel("A").point(lambda a: round(a*p)))
        im.alpha_composite(connector)
    text((600, 640), 'NOT TO SCALE', 38)
    text((160, 940), 'NASA/JPL-Caltech/Space Science Institute', 28)
    opacity = max(0, min(1, t/.4, (SECONDS-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda a: round(a*opacity)))
    return im
