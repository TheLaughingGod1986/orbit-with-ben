#!/usr/bin/env python3
"""J2729: deterministically reframe a licensed existing NASA plate; no generation.

Pillow and numpy are required. Existing destination assets are never overwritten.
The affine recipe preserves geometry; colour work is a global blue-shadow grade.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

DEFAULT_DIR = Path('/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/019_Andromeda-Milky-Way-Collision/08_Thumbnails/repackage_2026-11')
SOURCE = Path('/Users/benjaminoats/_desk/thumb_packaging_1011/plates/andromeda_PIA15416.jpg')
BASELINE = 'thumb_packaging_v01_ojk-dfOpAmw.jpg'
STEM = '019_andromeda_package_A_v02_ojk-dfOpAmw'
FONT = '/System/Library/Fonts/Supplemental/Arial Black.ttf'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', type=Path, default=DEFAULT_DIR)
    args = ap.parse_args()
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    targets = [out / (STEM + suffix) for suffix in ['.jpg', '_phone.png', '_comparison_actual168.png', '_recipe.json']]
    if any(p.exists() for p in targets):
        raise SystemExit('Refusing to overwrite existing assets; select a new --out-dir.')
    assert sha(SOURCE) == '88ed2cf29704895a32427c02be2daea6204f113e30f11aac4ff789c0de29a87d'
    src = Image.open(SOURCE).convert('RGB')
    # Reference coordinates retain the source's 9400:7000 aspect exactly.
    refw = 1880
    src = src.resize((refw, 1400), Image.Resampling.LANCZOS)
    angle = math.radians(8)
    scale = .76
    c, s = math.cos(angle)/scale, math.sin(angle)/scale
    # Source core (940,700) maps to (640,440); clockwise 8 degrees.
    affine = (c, s, 940-c*640-s*440, -s, c, 700+s*640-c*440)
    plate = src.transform((1280,720), Image.Transform.AFFINE, affine, Image.Resampling.BICUBIC)
    # Soften the real starfield outside the galaxy, at identical alignment.
    # This suppresses catalogue mosaic seams and competing stars without adding art.
    yy, xx = np.mgrid[:720,:1280]
    sx = affine[0]*xx + affine[1]*yy + affine[2] - 940
    sy = affine[3]*xx + affine[4]*yy + affine[5] - 700
    theta = math.radians(-28)
    major = sx*math.cos(theta)+sy*math.sin(theta)
    minor = -sx*math.sin(theta)+sy*math.cos(theta)
    radius = np.sqrt((major/780)**2+(minor/300)**2)
    mask = Image.fromarray(np.uint8(np.clip((1.23-radius)/.34,0,1)*255))
    plate = Image.composite(plate,plate.filter(ImageFilter.GaussianBlur(32)),mask)
    arr = np.asarray(plate).astype(float)/255
    # Blue shadow lift; stronger chroma on the plate's existing gold and blue.
    arr = np.clip(arr**.93 * 1.08 + (1-arr)**2*np.array([.06,.11,.23]), 0, 1)
    plate = Image.fromarray(np.uint8(arr*255))
    plate = ImageEnhance.Color(plate).enhance(1.30)
    plate = plate.filter(ImageFilter.UnsharpMask(radius=1.4,percent=115,threshold=3))
    draw = ImageDraw.Draw(plate)
    font = ImageFont.truetype(FONT,108)
    words = [('STARS',(255,255,255)),('RARELY',(255,230,0)),('HIT',(255,255,255))]
    gap = 29
    widths = [draw.textlength(w,font=font) for w,_ in words]
    x = (1280-sum(widths)-2*gap)/2
    for (word,color),width in zip(words,widths):
        draw.text((x,36),word,font=font,fill=color,stroke_width=7,stroke_fill=(0,0,0),anchor='lt')
        x += width+gap
    credit = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18)
    draw.text((22,688),'NASA/JPL-Caltech',font=credit,fill=(221,230,244),stroke_width=1,stroke_fill=(10,18,37))
    plate.save(targets[0],quality=95,subsampling=0,optimize=True)
    final = Image.open(targets[0]).convert('RGB')
    phone = final.resize((168,94),Image.Resampling.LANCZOS)
    phone.save(targets[1])
    comparison = Image.new('RGB',(352,120),(240,240,240))
    d = ImageDraw.Draw(comparison)
    d.text((0,1),'Baseline',fill='black')
    d.text((184,1),'Proposed A v02',fill='black')
    comparison.paste(Image.open(DEFAULT_DIR/BASELINE).resize((168,94),Image.Resampling.LANCZOS),(0,24))
    comparison.paste(phone,(184,24))
    comparison.save(targets[2])
    manifest = {'source':str(SOURCE),'source_sha256':sha(SOURCE),'source_original_size':[9400,7000],
        'source_reference_size':[1880,1400],'affine_output_to_reference':affine,
        'clockwise_rotation_degrees':8,'reference_scale':scale,'core_output':[640,440],
        'grade':'real starfield same-alignment Gaussian32 outside source ellipse (780,300), angle -28, radius blend .89 to1.23; gamma .93; gain1.08; nonlinear shadow lift(.06,.11,.23); saturation1.30; unsharp1.4/115/3',
        'font':FONT,'font_size':108,'outline_px':7,'credit':'NASA/JPL-Caltech',
        'source_url':'https://www.jpl.nasa.gov/images/pia15416-andromeda/',
        'assets':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in targets[:3]}}
    targets[3].write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))

if __name__ == '__main__':
    main()
