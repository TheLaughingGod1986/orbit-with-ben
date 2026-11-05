#!/usr/bin/env python3
"""R52 draft: real Voyager Uranus and a sourced winter-duration counter.

No invented surface texture, terminator, illumination or collision depiction.
"""
import argparse
import hashlib
import json
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw
from code_graphics import W, H, GOLD, WHITE, font

SECONDS = 3.6
SOURCE = Path('/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA18182.jpg')
CROP = (140, 160, 1560, 1580)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def body():
    im = Image.open(SOURCE).convert('RGBA').crop(CROP)
    mask = Image.new('L', im.size)
    ImageDraw.Draw(mask).ellipse((0, 0, im.width-1, im.height-1), fill=255)
    im.putalpha(mask)
    return im.resize((620, 620), Image.Resampling.LANCZOS)


def frame(t):
    im = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(im)
    alpha = max(0, min(1, t/.4, (SECONDS-t)/.4))
    progress = min(1, max(0, (t-.4)/2.2))
    im.alpha_composite(body(), (180, 220))
    # This is a time bar, never a fabricated orbital/illumination simulation.
    d.text((1000, 350), 'DARK WINTER', font=font(57), fill=GOLD)
    d.text((1000, 445), f'{round(21*progress)} YEARS', font=font(86), fill=WHITE)
    d.line((1010, 650, 1690, 650), fill=(130, 150, 180, 180), width=8)
    d.line((1010, 650, 1010+680*progress, 650), fill=GOLD, width=8)
    for x, text in ((1010, '0'), (1690, '21')):
        d.line((x, 633, x, 667), fill=WHITE, width=3)
        d.text((x-15, 685), text, font=font(40), fill=WHITE)
    d.text((180, 900), 'URANUS', font=font(58), fill=GOLD)
    d.text((180, 980), 'NASA/JPL-Caltech', font=font(28), fill=WHITE)
    im.putalpha(im.getchannel('A').point(lambda a: round(a*alpha)))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--approved', choices=['r52_uranus_21y'])
    ap.add_argument('--review-ref')
    args = ap.parse_args()
    if args.render and not (args.approved and args.review_ref):
        ap.error('Render requires named still approval and its actual review reference')
    if args.render:
        ap.error('Draft only: implement export after the still decision')
    args.out.mkdir(parents=True, exist_ok=True)
    preview = args.out/'code_graphic_032_r52_uranus_21y_v01.png'
    if preview.exists():
        ap.error('Use a fresh version directory; do not overwrite previews')
    frame(2.6).save(preview)
    review = Image.new('RGBA', (W, H), (37, 52, 73, 255))
    review.alpha_composite(frame(2.6))
    review.convert('RGB').save(args.out/'r52_uranus_review.jpg', quality=95)
    record = dict(job='J2089', row=52, id='r52_uranus_21y', source_rows=[18],
                  status='DRAFT_STILL_REQUIRES_REVIEW', duration=SECONDS, fps=30,
                  preview=str(preview), preview_sha256=sha(preview),
                  source=str(SOURCE), source_sha256=sha(SOURCE), crop=CROP,
                  source_id='PIA18182', credit='NASA/JPL-Caltech',
                  claim_source='SOURCES.md row 18; https://science.nasa.gov/uranus/facts/',
                  source_record='HARVEST_POOL_v01.json: PIA18182',
                  limits=['Duration-only variant; planned tilt-axis explanation remains outstanding',
                          'No exact tilt angle, terminator, orbit or collision reconstructed',
                          'Still review, plate compositing, reuse and motion QA pending',
                          'Film background must be graded moving imagery; review navy is illustrative',
                          'Counts as R52 use of PIA18182, not an additional source appearance'])
    (args.out/'URANUS_MANIFEST_v01.json').write_text(json.dumps(record, indent=2)+'\n')
    print(preview)


if __name__ == '__main__':
    main()
