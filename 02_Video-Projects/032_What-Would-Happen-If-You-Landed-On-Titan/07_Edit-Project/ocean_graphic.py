#!/usr/bin/env python3
"""R35 photo plus magnified, qualitative ocean cross-section. Review draft only.

No invented ocean thickness or core structure. The 55–80 km is depth below
surface, not ocean thickness. This schematic is intentionally not to scale.
"""
import argparse
import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw
from code_graphics import W, H, GOLD, WHITE, font

SECONDS = 3.6
SOURCE = Path('/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA14602.jpg')
CROP = (265, 275, 775, 785)
LABELS = ['TITAN', 'ICY GROUND', '55–80 KM BELOW', 'LIQUID WATER',
          'LIKELY SALTS + AMMONIA', 'SCHEMATIC · NOT TO SCALE']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def photo():
    image = Image.open(SOURCE).convert('RGBA').crop(CROP)
    mask = Image.new('L', image.size)
    ImageDraw.Draw(mask).ellipse((0, 0, 509, 509), fill=255)
    image.putalpha(mask)
    return image.resize((480, 480), Image.Resampling.LANCZOS)


def progress(t):
    return max(0, min(1, (t-.4)/1.5))


def frame(t):
    im = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(im)
    p = progress(t)
    opacity = max(0, min(1, t/.4, (SECONDS-t)/.4))
    im.alpha_composite(photo(), (120, 265))
    def label(x, y, text, size=52, colour=WHITE):
        d.text((x, y), text, font=font(size), fill=colour,
               stroke_width=2, stroke_fill=(20, 28, 42, 255))
    label(240, 780, 'TITAN', 58, GOLD)
    # Zoom connector, deliberately not a measured planetary shell wedge.
    d.line((555, 400, 760, 285), fill=(255, 207, 64, 180), width=3)
    d.line((555, 620, 760, 815), fill=(255, 207, 64, 180), width=3)
    # The local cross-section has no ocean floor: thickness remains unspecified.
    left, right, top, boundary, bottom = 780, 1295, 285, 515, 815
    d.rectangle((left, top, right, boundary), fill=(177, 210, 223, 190))
    d.line((left, top, right, top), fill=WHITE, width=4)
    # Ocean fills horizontally while the depth bracket draws down from surface.
    if p > 0:
        d.rectangle((left, boundary, left+round((right-left)*p), bottom),
                    fill=(47, 145, 202, 200))
        y = top+round((boundary-top)*p)
        d.line((right+35, top, right+35, y), fill=GOLD, width=5)
        d.line((right+25, top, right+45, top), fill=GOLD, width=4)
        d.line((right+25, y, right+45, y), fill=GOLD, width=4)
        # Fine moving interface ripple; illustrative, not a measured wave.
        import math
        points = [(x, boundary+round(3*math.sin(x/35+t*2)))
                  for x in range(left, left+round((right-left)*p), 4)]
        if len(points)>1:
            d.line(points, fill=(198, 237, 251, 255), width=3)
    label(820, 355, 'ICY GROUND')
    label(1370, 390, '55–80 KM', 48, GOLD)
    label(1370, 452, 'BELOW', 48, GOLD)
    label(820, 585, 'LIQUID WATER', 50)
    label(820, 680, 'LIKELY SALTS', 43)
    label(820, 738, '+ AMMONIA', 43)
    label(780, 880, 'SCHEMATIC · NOT TO SCALE', 38)
    im.putalpha(im.getchannel('A').point(lambda a: round(a*opacity)))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--approved', choices=['r35_ocean'])
    ap.add_argument('--review-ref')
    a = ap.parse_args()
    if a.render and not (a.approved == 'r35_ocean' and a.review_ref == 'J2264'):
        ap.error('Render requires r35_ocean approval under J2264')
    if a.out.exists():
        ap.error('Use a fresh version directory; existing previews are immutable')
    a.out.mkdir(parents=True)
    preview = a.out/'code_graphic_032_r35_ocean_v01.png'
    frame(2).save(preview)
    bg = Image.new('RGBA', (W,H), (37, 52, 73, 255))
    bg.alpha_composite(frame(2))
    bg.convert('RGB').save(a.out/'r35_ocean_review.jpg', quality=95)
    manifest = dict(job='J2089', row=35, id='r35_ocean', source_rows=[13],
        status='DRAFT_STILL_REQUIRES_INDIVIDUAL_REVIEW', duration=SECONDS, fps=30,
        source=str(SOURCE), source_id='PIA14602', source_sha256=sha(SOURCE),
        source_credit='NASA/JPL-Caltech/Space Science Institute', crop=CROP,
        preview=str(preview), preview_sha256=sha(preview), labels=LABELS,
        evidence='SOURCES.md row 13: NASA Titan facts; 55–80 km below icy ground; liquid water likely mixed with salts and ammonia.',
        depth_semantics='55–80 km refers to below-surface depth, never ocean thickness',
        geometry='Qualitative local cross-section, not to scale; no ocean floor/core claim',
        limits=['Photo allocation must be reconciled with final source reuse manifest',
                'Reviewer must decide schematic matches the locked line',
                'No new factual claim, script/VO change, MOV, composite or motion/audio review',
                'Preview background is a review aid; use an approved graded moving plate'])
    if a.render:
        dest = a.out/'code_graphic_032_r35_ocean_v01.mov'
        proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-n', '-f', 'rawvideo',
            '-pixel_format', 'rgba', '-video_size', f'{W}x{H}', '-framerate', '30',
            '-i', 'pipe:0', '-an', '-c:v', 'qtrle', str(dest)], stdin=subprocess.PIPE)
        try:
            for i in range(108):
                proc.stdin.write(frame(i/30).tobytes())
            proc.stdin.close()
            if proc.wait():
                raise RuntimeError('ffmpeg failed')
        except BaseException:
            proc.kill()
            proc.wait()
            raise
        manifest.update(render=str(dest), sha256=sha(dest), review_ref=a.review_ref,
            status='RENDERED_UNDER_REFERENCED_REVIEW_NOT_COMPOSITED')
        (a.out/'OCEAN_RENDER_MANIFEST_v01.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (a.out/'OCEAN_MANIFEST_v01.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(preview)


if __name__ == '__main__':
    main()
