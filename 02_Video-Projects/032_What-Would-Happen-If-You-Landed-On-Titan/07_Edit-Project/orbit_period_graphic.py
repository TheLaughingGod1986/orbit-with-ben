#!/usr/bin/env python3
"""R08 period-counter draft: real Cassini photograph beside an elapsed-time dial.

The dial is a clock, never a reconstruction of Titan's projected orbit.
"""
import argparse
import hashlib
import json
import math
import subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw
from code_graphics import W, H, GOLD, WHITE, font

SOURCE = Path('/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA14922.jpg')
SECONDS = 3.6
PHOTO_XY = (140, 220)
PHOTO_SIZE = (715, 670)
DIAL = (1370, 520)
RADIUS = 220


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def photo():
    im = Image.open(SOURCE).convert('RGBA')
    im.thumbnail(PHOTO_SIZE, Image.Resampling.LANCZOS)
    return im


def progress(t):
    return min(1, max(0, (t-.4)/2.0))


def frame(t):
    im = Image.new('RGBA', (W,H))
    im.alpha_composite(photo(), PHOTO_XY)
    d = ImageDraw.Draw(im)
    d.text((140,130), 'TITAN AND SATURN', font=font(54), fill=GOLD)
    d.text((140,930), 'NASA/JPL-Caltech/SSI', font=font(28), fill=WHITE)
    d.text((1020,130), 'ONE FULL ORBIT', font=font(58), fill=GOLD)
    x,y=DIAL
    box=(x-RADIUS,y-RADIUS,x+RADIUS,y+RADIUS)
    d.ellipse(box, outline=(140,160,180,170), width=4)
    p=progress(t)
    if p>0:
        d.arc(box,start=-90,end=-90+360*p,fill=GOLD,width=12)
    # The hand belongs to the elapsed-time dial; no body travels on this arc.
    angle=2*math.pi*p-math.pi/2
    d.line((x,y,x+175*math.cos(angle),y+175*math.sin(angle)),fill=WHITE,width=7)
    d.ellipse((x-10,y-10,x+10,y+10),fill=GOLD)
    d.text((1040,815), 'ABOUT 16 DAYS',font=font(68),fill=WHITE)
    opacity=max(0,min(1,t/.4,(SECONDS-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda a:round(a*opacity)))
    return im


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--approved', choices=['r08_orbit_period'])
    ap.add_argument('--review-ref')
    a=ap.parse_args()
    if a.render and not (a.approved == 'r08_orbit_period' and a.review_ref == 'J2262'):
        ap.error('Render requires r08_orbit_period approval under J2262')
    if a.out.exists(): ap.error('Use a fresh version directory')
    a.out.mkdir(parents=True,exist_ok=True)
    preview=a.out/'code_graphic_032_r08_orbit_period_v01.png'
    if preview.exists(): ap.error('Use a fresh version directory')
    frame(2.4).save(preview)
    bg=Image.new('RGBA',(W,H),(37,52,73,255));bg.alpha_composite(frame(2.4))
    bg.convert('RGB').save(a.out/'r08_orbit_period_review.jpg',quality=95)
    rec=dict(job='J2089',id='r08_orbit_period',row=8,source_rows=[2],
        status='DRAFT_REQUIRES_REVIEW',preview=str(preview),preview_sha256=sha(preview),
        source=str(SOURCE),source_sha256=sha(SOURCE),source_id='PIA14922',
        source_dimensions=list(Image.open(SOURCE).size),photo_dimensions=list(photo().size),
        source_credit='NASA/JPL-Caltech/Space Science Institute',seconds=SECONDS,fps=30,
        claim='SOURCES.md governing row 2: 15 days and 22 hours, spoken as about sixteen days',
        design='Elapsed-time clock beside intact Cassini photograph; no simulated orbit or body-size scale',
        limits=['Review whether a period dial is an acceptable R08 orbit16 implementation before rendering',
          'PIA14922 already proposed for R06: allocating R08 would exhaust its two appearances; final cut count required',
          'Native photo is reduced, not upscaled; original field and body geometry preserved',
          'Composite placement, near-black, grain, contrast and moving-plate checks outstanding',
          'No motion/audio perception or film approval claimed; navy is a preview backdrop only'])
    if a.render:
        dest = a.out/'code_graphic_032_r08_orbit_period_v01.mov'
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
        rec.update(render=str(dest), sha256=sha(dest), review_ref=a.review_ref,
            status='RENDERED_UNDER_REFERENCED_REVIEW_NOT_COMPOSITED')
    (a.out/'ORBIT_PERIOD_MANIFEST_v01.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(preview)

if __name__=='__main__':main()
