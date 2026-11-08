#!/usr/bin/env python3
"""R19 distance-scale draft. Photo plus bars, never an orbital reconstruction."""
import argparse
import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw
from code_graphics import W, H, GOLD, WHITE, font

SECONDS = 3.6
SOURCE = Path('/Users/benjaminoats/_desk/cache/J2089/harvest_v01/PIA14909.jpg')
CROP = (295, 294, 703, 702)
VALUES = (1.0, 9.5)
BAR_X, BAR_WIDTH = 830, 900

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

@lru_cache(maxsize=1)
def body():
    image = Image.open(SOURCE).convert('RGBA').crop(CROP)
    mask = Image.new('L', image.size)
    ImageDraw.Draw(mask).ellipse((0, 0, image.width-1, image.height-1), fill=255)
    image.putalpha(mask)
    return image.resize((460, 460), Image.Resampling.LANCZOS)

def widths(t):
    progress = min(1, max(0, (t-.4)/2.0))
    return [BAR_WIDTH * v / 9.5 * progress for v in VALUES]

def frame(t):
    im = Image.new('RGBA', (W,H))
    d = ImageDraw.Draw(im)
    opacity = max(0, min(1, t/.4, (SECONDS-t)/.4))
    im.alpha_composite(body(), (170,250))
    d.text((170,760), 'TITAN', font=font(58), fill=GOLD)
    d.text((170,850), 'NASA/JPL-Caltech/SSI', font=font(28), fill=WHITE)
    d.text((830,150), 'DISTANCE FROM SUN', font=font(54), fill=GOLD)
    for name, value, y, width in zip(('EARTH','TITAN'), VALUES, (390,640), widths(t)):
        d.text((830,y-100), f'{name} {value:g} AU', font=font(56), fill=WHITE)
        d.line((BAR_X,y,BAR_X+BAR_WIDTH,y), fill=(140,160,180,120), width=3)
        if width > 0:
            d.rectangle((BAR_X,y-20,BAR_X+width,y+20), fill=GOLD)
    d.text((830,810), '9.5× EARTH’S DISTANCE', font=font(54), fill=WHITE)
    # Linear distance scale, not body size or positions in an actual sky.
    im.putalpha(im.getchannel('A').point(lambda a: round(a*opacity)))
    return im

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--approved', choices=['r19_distance'])
    ap.add_argument('--review-ref')
    a=ap.parse_args()
    if a.render and not (a.approved == 'r19_distance' and a.review_ref == 'J2260'):
        ap.error('Render requires r19_distance approval under J2260')
    if a.out.exists(): ap.error('Use a fresh version directory')
    a.out.mkdir(parents=True,exist_ok=True)
    preview=a.out/'code_graphic_032_r19_distance_v01.png'
    if preview.exists(): ap.error('Use a fresh version directory')
    frame(2.4).save(preview)
    review=Image.new('RGBA',(W,H),(37,52,73,255))
    review.alpha_composite(frame(2.4))
    review.convert('RGB').save(a.out/'r19_distance_review.jpg',quality=95)
    record=dict(job='J2089',id='r19_distance',row=19,source_rows=[8],
        status='DRAFT_STILL_REQUIRES_REVIEW',source=str(SOURCE),source_id='PIA14909',
        source_sha256=sha(SOURCE),crop=CROP,preview=str(preview),preview_sha256=sha(preview),
        credit='NASA/JPL-Caltech/Space Science Institute',seconds=SECONDS,fps=30,
        claim='SOURCES.md row 8: about 9.5 astronomical units; Earth distance is 1 AU by definition',
        claim_url='https://science.nasa.gov/saturn/moons/titan/facts/',
        ratio=9.5,scale='Both bars share 900/9.5 pixels per AU; common animated growth',
        limits=['Distance comparison, not an orbital or body-size diagram',
          'J2260 allocates PIA14909 to R19; PIA14602 remains R09+R35 only; final cut count required',
          'Photo is illustrative; no new texture, illumination, orbit or geometry reconstructed',
          'Final graded moving plate and sound-off contrast need review; navy is preview only',
          'No motion/audio perception or approval claimed; no MOV exported'])
    if a.render:
        dest = a.out/'code_graphic_032_r19_distance_v01.mov'
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
        record.update(render=str(dest), sha256=sha(dest), review_ref=a.review_ref,
            status='RENDERED_UNDER_REFERENCED_REVIEW_NOT_COMPOSITED')
    (a.out/'DISTANCE_MANIFEST_v01.json').write_text(json.dumps(record,indent=2)+'\n')
    print(preview)
if __name__=='__main__': main()
