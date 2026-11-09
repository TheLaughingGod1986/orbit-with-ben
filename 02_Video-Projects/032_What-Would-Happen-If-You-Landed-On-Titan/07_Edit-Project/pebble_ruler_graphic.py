#!/usr/bin/env python3
"""R18 registered pebble-width draft; no global image distance calibration.

Still reviewed under J2296; export requires that explicit review reference. The source is
never painted or enlarged beyond 1.44x. Final moving background is not supplied.
"""
import argparse
import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw
from code_graphics import W, H, GOLD, WHITE, font

SOURCE = Path('/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA07232.jpg')
SOURCE_HASH = '4221ee7a4588a6ea169a0b438b5526e26c68827cb717a31ef1f81284b39cd3e8'
CROP = (116, 32, 430, 661)
DISPLAY = (449, 900)
ORIGIN = (220, 90)
# Manually registered to the left elongated cobble identified by ESA's caption.
# Endpoints mark approximate visible width, not a photogrammetric measurement.
ENDPOINTS = ((148, 423), (269, 423))
SECONDS = 3.6
URL = 'https://www.esa.int/media/first-colour-view-of-titan-s-surface'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def point(p):
    return (ORIGIN[0] + (p[0]-CROP[0])*DISPLAY[0]/(CROP[2]-CROP[0]),
            ORIGIN[1] + (p[1]-CROP[1])*DISPLAY[1]/(CROP[3]-CROP[1]))

@lru_cache(maxsize=1)
def plate():
    assert sha(SOURCE) == SOURCE_HASH, 'Source changed; re-register before use'
    with Image.open(SOURCE) as source:
        return source.convert('RGBA').crop(CROP).resize(DISPLAY, Image.Resampling.LANCZOS)

def frame(t):
    im = Image.new('RGBA', (W,H))
    im.alpha_composite(plate(), ORIGIN)
    d = ImageDraw.Draw(im)
    a,b = map(point, ENDPOINTS)
    y = a[1]-44
    p = min(1,max(0,(t-.4)/1.6))
    # Bracket builds above the cobble, preserving the cobble itself.
    if p:
        d.line((a[0],y,a[0]+(b[0]-a[0])*p,y), fill=GOLD, width=5)
        d.line((a[0],y-12,a[0],y+12), fill=GOLD,width=5)
        if p == 1:
            d.line((b[0],y-12,b[0],y+12),fill=GOLD,width=5)
    d.text((850,365),'ABOUT 15 CENTIMETRES',font=font(62),fill=GOLD,
           stroke_width=3,stroke_fill=(20,28,42,220))
    d.text((850,465),'PEBBLES',font=font(58),fill=WHITE,
           stroke_width=3,stroke_fill=(20,28,42,220))
    d.line((b[0]+18,y,780,y,820,410),fill=WHITE,width=3)
    d.text((850,840),'ESA/NASA/JPL/University of Arizona',font=font(27),fill=WHITE)
    opacity=max(0,min(1,t/.4,(SECONDS-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda a:round(a*opacity)))
    return im

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--approved', choices=['r18_ruler'])
    ap.add_argument('--review-ref')
    args=ap.parse_args()
    if args.render and not (args.approved == 'r18_ruler' and args.review_ref == 'J2296'):
        ap.error('Render requires r18_ruler approval under J2296')
    if args.out.exists():ap.error('Use a fresh version directory')
    args.out.mkdir(parents=True)
    preview=args.out/'code_graphic_032_r18_ruler_v01.png'
    frame(2.4).save(preview)
    review=Image.new('RGBA',(W,H),(37,52,73,255))
    review.alpha_composite(frame(2.4))
    review.convert('RGB').save(args.out/'r18_ruler_review.jpg',quality=95)
    record=dict(job='J2089',id='r18_ruler',row=18,status='DRAFT_REQUIRES_INDIVIDUAL_REVIEW',
        source=str(SOURCE),source_sha256=sha(SOURCE),source_url=URL,source_rows=[8],
        credit='ESA/NASA/JPL/University of Arizona',crop=CROP,display=DISPLAY,origin=ORIGIN,
        source_bracket_endpoints=ENDPOINTS,preview=str(preview),preview_sha256=sha(preview),
        fps=30,seconds=SECONDS,max_upscale=max(DISPLAY[0]/314,DISPLAY[1]/629),
        claim='ESA identifies the left cobble as about 15 centimetres across; no scale is inferred elsewhere in the perspective image.',
        limits=['PIA07232 allocation R18+R20 only; final cut manifest must enforce cap',
          'ESA page names ESA Standard Licence; rights clearance remains unresolved',
          'Soft source inset and bracket endpoint registration need individual review',
          'Navy background is preview only; composite over approved graded moving plate',
          'No motion/audio perception, KEEP, export or final gates claimed'])
    if args.render:
        assert record['preview_sha256'] == '3c5a2f296be594fd161062a548e9e970962c8b5dbae630d542da0cc7a09c0517', 'Reviewed preview changed'
        dest = args.out/'code_graphic_032_r18_ruler_v01.mov'
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
        record.update(render=str(dest), sha256=sha(dest), review_ref=args.review_ref,
            status='RENDERED_UNDER_REFERENCED_REVIEW_NOT_COMPOSITED')
        record['limits'] = [
            'PIA07232 allocation R18+R20 only; final cut manifest must enforce cap',
            'Per-asset rights clearance remains unresolved before final cut release',
            'Composite over approved graded moving plate; contrast and timing unverified',
            'No motion/audio perception or final film gates claimed']
    (args.out/'PEBBLE_RULER_MANIFEST_v01.json').write_text(json.dumps(record,indent=2)+'\n')
    print(preview)
if __name__=='__main__':main()
