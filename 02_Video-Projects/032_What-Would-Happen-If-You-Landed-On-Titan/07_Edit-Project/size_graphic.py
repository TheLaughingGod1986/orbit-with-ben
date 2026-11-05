#!/usr/bin/env python3
"""R09 real-photo diameter comparison. Draft preview; no approval implied.

Photographic globes retain their pixels; circular limb masks remove black
surrounds. All three grow by the same factor, preserving diameter ratios at
every frame. No independent Ken Burns or invented planetary textures.
"""
import argparse
import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw
from code_graphics import W, H, GOLD, WHITE, font

CACHE = Path('/Users/benjaminoats/_desk/cache/J2089')
SECONDS = 3.6
SPECS = [
    dict(name='MOON', km=3475, id='PIA00405', x=380,
         path=str(CACHE/'size_sources_v01/PIA00405.jpg'),
         crop=[0, 0, 1986, 1986], credit='NASA/JPL/USGS'),
    dict(name='MERCURY', km=4879, id='PIA15162', x=950,
         path=str(CACHE/'size_sources_v01/PIA15162.jpg'),
         crop=[95, 95, 2052, 2052],
         credit='NASA/JHUAPL/Carnegie Institution of Washington'),
    dict(name='TITAN', km=5150, id='PIA14602', x=1520,
         path=str(CACHE/'harvest_v03/PIA14602.jpg'),
         crop=[265, 275, 775, 785], credit='NASA/JPL-Caltech/Space Science Institute'),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@lru_cache(maxsize=3)
def globe(asset_id):
    spec = next(s for s in SPECS if s['id'] == asset_id)
    image = Image.open(spec['path']).convert('RGBA').crop(spec['crop'])
    # An inscribed disc only masks the source surround; it never fills a body.
    mask = Image.new('L', image.size)
    ImageDraw.Draw(mask).ellipse((0, 0, image.width-1, image.height-1), fill=255)
    image.putalpha(mask)
    return image


def diameters(t):
    growth = .72 + .28 * min(1, max(0, t/1.6))
    return [round(470 * s['km']/5150 * growth) for s in SPECS]


def frame(t):
    im = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(im)
    alpha = max(0, min(1, t/.4, (SECONDS-t)/.4))
    d.text((120, 100), 'DIAMETER', font=font(54), fill=WHITE,
           stroke_width=2, stroke_fill=(20, 28, 42, 255))
    for s, diameter in zip(SPECS, diameters(t)):
        body = globe(s['id']).resize((diameter, diameter), Image.Resampling.LANCZOS)
        im.alpha_composite(body, (s['x']-diameter//2, 510-diameter//2))
        for text, y, size, colour in [(s['name'], 800, 58, GOLD),
                                     (f"{s['km']:,} KM", 875, 54, WHITE)]:
            f = font(size)
            width = d.textlength(text, font=f)
            d.text((s['x']-width/2, y), text, font=f, fill=colour,
                   stroke_width=2, stroke_fill=(20, 28, 42, 255))
        # Bracket shares the exact diameter scale of the corresponding body.
        left, right = s['x']-diameter//2, s['x']-diameter//2+diameter
        d.line((left, 765, right, 765), fill=WHITE, width=3)
        for x in (left, right):
            d.line((x, 755, x, 775), fill=WHITE, width=3)
    im.putalpha(im.getchannel('A').point(lambda a: round(a*alpha)))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--approved', choices=['r09_sizes'])
    ap.add_argument('--review-ref')
    ap.add_argument('--rights-ref')
    args = ap.parse_args()
    if args.render and not (args.approved and args.review_ref and args.rights_ref):
        ap.error('Render needs named approval, still-review reference and source-rights reference')
    args.out.mkdir(parents=True, exist_ok=True)
    preview = args.out/'code_graphic_032_r09_sizes_v01.png'
    if preview.exists():
        ap.error('Use a fresh version directory; previews are immutable')
    frame(1.8).save(preview)
    review = Image.new('RGBA', (W, H), (37, 52, 73, 255))
    review.alpha_composite(frame(1.8))
    review.convert('RGB').save(args.out/'r09_sizes_review.jpg', quality=95)
    result = dict(job='J2089', row=9, id='r09_sizes', source_rows=[3],
                  status='DRAFT_STILL_REQUIRES_REVIEW_AND_RIGHTS_CLEARANCE',
                  duration=SECONDS, fps=30, preview=str(preview),
                  preview_sha256=sha(preview), assets=[{**s, 'sha256':sha(s['path'])}
                                                        for s in SPECS],
                  diameter_pixels=diameters(1.8),
                  ratio_method='linear diameter, common 470/5150 pixels per km',
                  limits=['Photographic limb crops are representative, not measurements',
                          'Titan visible haze limb stands for nominal surface diameter',
                          'PIA15162 APL/Carnegie terms require reviewer clearance',
                          'Final moving plate, contrast, timing and reuse not verified',
                          'No motion perception; no MOV render until still review'])
    if args.render:
        dest = args.out/'code_graphic_032_r09_sizes_v01.mov'
        proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-n', '-f', 'rawvideo',
                                 '-pixel_format', 'rgba', '-video_size', f'{W}x{H}',
                                 '-framerate', '30', '-i', 'pipe:0', '-an', '-c:v',
                                 'qtrle', str(dest)], stdin=subprocess.PIPE)
        try:
            for i in range(round(SECONDS*30)):
                proc.stdin.write(frame(i/30).tobytes())
            proc.stdin.close()
            if proc.wait():
                raise RuntimeError('ffmpeg failed')
        except BaseException:
            proc.kill()
            raise
        result.update(render=str(dest), sha256=sha(dest), review_ref=args.review_ref,
                      rights_ref=args.rights_ref,
                      status='RENDERED_UNDER_REFERENCED_REVIEW_NOT_COMPOSITED')
    (args.out/'SIZE_MANIFEST_v01.json').write_text(json.dumps(result, indent=2)+'\n')
    print(preview)


if __name__ == '__main__':
    main()
