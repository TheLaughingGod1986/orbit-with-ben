#!/usr/bin/env python3
"""R23 proposed qualitative landing record; review before any export.

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
    x = 200 + 980*p
    if p:
        d.line((200, 560, x, 560), fill=GOLD, width=6)
        d.polygon([(x, 560), (x-22, 547), (x-22, 573)], fill=GOLD)
    text((600, 640), 'NOT TO SCALE', 38)
    text((160, 940), 'NASA/JPL-Caltech/Space Science Institute', 28)
    opacity = max(0, min(1, t/.4, (SECONDS-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda a: round(a*opacity)))
    return im

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--approved', choices=['r23_landing_record'])
    ap.add_argument('--review-ref')
    a = ap.parse_args()
    if a.render and not (a.approved == 'r23_landing_record' and a.review_ref == 'J2304'):
        ap.error('Render requires r23_landing_record approval under J2304')
    if a.out.exists():
        ap.error('Use a fresh version directory')
    a.out.mkdir(parents=True)
    preview = a.out/'code_graphic_032_r23_landing_record_v01.png'
    frame(2.4).save(preview)
    review = Image.new('RGBA', (W,H), (37,52,73,255))
    review.alpha_composite(frame(2.4))
    review.convert('RGB').save(a.out/'r23_landing_record_review.jpg', quality=95)
    record = dict(job='J2089', id='r23_landing_record', row=23, source_rows=[7],
        status='PROPOSED_ALTERNATIVE_REQUIRES_REVIEW_NOT_RENDERED',
        source=str(SOURCE), source_id='PIA14909', source_sha256=sha(SOURCE),
        crop=CROP, display=[408,408], upscale=1.0,
        preview=str(preview), preview_sha256=sha(preview), seconds=SECONDS, fps=30,
        claim_url=URL, claim='Huygens made the most distant landing from Earth.',
        proposal='Replace unsupported quantitative landings_chart with qualitative record graphic; retain locked VO.',
        allocation_proposal='PIA14909 second appearance R23, following approved R19; needs reviewer confirmation against full cut list.',
        labels=['MOST DISTANT LANDING','HUYGENS','FROM EARTH','TITAN','NOT TO SCALE'],
        limits=['9.5 AU is not used as Earth-to-Titan landing distance',
          'No Moon/Venus/Mars bar lengths or landing-distance ranking inferred',
          'No actual trajectory, landing-site location or body size comparison',
          'PIA14909 per-asset rights and final <=2 appearances check remain required',
          'Preview navy only; final graded moving plate, placement, timing and contrast unverified',
          'Separate from existing R23 FACT card; do not place full-frame code graphics back to back',
          'No motion/audio perception, KEEP, export or film approval claimed'])
    if a.render:
        assert record['preview_sha256'] == '8a2de4177dff150ecb24e70d2e64422241f729fde5537ca5deedb540a51a9d2c', 'Reviewed preview changed'
        dest = a.out/'code_graphic_032_r23_landing_record_v01.mov'
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
            status='RENDERED_UNDER_REFERENCED_REVIEW_NOT_COMPOSITED',
            allocation='PIA14909 R19 and R23 only; second appearance',
            alternative='J2304 qualitative record replaces landings_chart and duplicate r23_fact')
        record['limits'] = [
            'PIA14909 per-asset rights and final <=2 appearances check remain required',
            'Composite over approved graded moving plate; contrast and timing unverified',
            'Separate from R22 CODE with real moving picture; omit duplicate r23_fact',
            'No motion/audio perception or final film gates claimed']
    (a.out/'LANDING_RECORD_MANIFEST_v01.json').write_text(json.dumps(record,indent=2)+'\n')
    print(preview)

if __name__ == '__main__':
    main()
