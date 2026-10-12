#!/usr/bin/env python3
"""J0143: no-spend code composites, using the existing NASA/JPL spacecraft asset.
Usage: python3 this.py --source /path/PIA17049.jpg --out /path/j0143_v01
Media stays local; manifest records source and output hashes. Chief reviews the art.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import _build_light_speed_thumbs_v01 as house

W, H = 1280, 720

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def background():
    yy, xx = np.mgrid[:H, :W].astype(float)
    glow = np.exp(-(((xx-780)/660)**2 + ((yy-460)/380)**2))
    a = np.array([9, 25, 62]) + glow[..., None]*np.array([9, 51, 91])
    base = house.img(a)
    stars = Image.new('RGB', (W,H))
    d = ImageDraw.Draw(stars)
    rng = random.Random(143)
    # Blue, converging starlight: a conceptual motion treatment, not a simulation.
    for _ in range(180):
        x, y = rng.randrange(W), rng.randrange(265,H)
        dx, dy = x-810, y-455
        length = rng.uniform(.025,.14)
        colour = (rng.randint(55,115),rng.randint(125,195),255)
        d.line((x,y,x+dx*length,y+dy*length),fill=colour,width=rng.choice([1,1,2]))
    return house.img(house.screen(house.arr(base),house.arr(stars.filter(ImageFilter.GaussianBlur(.5)))*.65))

def plate(source):
    src = Image.open(source).convert('RGB')
    # The same whole spacecraft used in abc_v03; retain its antenna and booms.
    src = src.crop((370,35,1010,719)).resize((430,450),Image.Resampling.LANCZOS)
    a = house.arr(src)
    l = a.mean(-1)
    keep = np.clip((l-12)/32,0,1)
    a = a*keep[...,None]
    a = a*np.array([.67,1.04,1.30])
    craft = house.img(a)
    layer = Image.new('RGB',(W,H))
    # Entire craft below the two-line text band, with breathing room on all edges.
    layer.paste(craft,(425,260))
    broad = house.arr(layer.filter(ImageFilter.GaussianBlur(26)))*.35
    tight = house.arr(layer.filter(ImageFilter.GaussianBlur(5)))*.35
    base = house.arr(background())
    return house.img(house.screen(house.screen(house.screen(base,broad),tight),house.arr(layer)*1.04))

def words(im, lines, yellow):
    d=ImageDraw.Draw(im)
    f=house.font(115)
    cap=d.textbbox((0,0),'H',font=f)
    boxes=[]
    for i,line in enumerate(lines):
        width=house.line_w(d,line,f)
        x=(W-width)/2
        y=39+i*108-cap[1]
        assert width < W-70
        colour=house.YELLOW if i==yellow else house.WHITE
        house.draw_line(d,x+3,y+4,line,f,house.BLACK)
        if line.startswith('EARTH:'):
            house.draw_line(d,x,y,line,f,house.WHITE)
            prefix='EARTH: 7 '
            offset=sum(d.textlength(c,font=f)+house.TRACK for c in prefix)
            house.draw_line(d,x+offset,y,'YEARS',f,house.YELLOW)
        else:
            house.draw_line(d,x,y,line,f,colour)
        boxes.append([round(x),39+i*108-7,round(x+width),39+i*108+82+7])
    assert max(b[3] for b in boxes)<=260-24
    return boxes

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    variants=[('answer',['YOU: 1 YEAR','EARTH: 7 YEARS'],1),('tease',['OUTRUN','EARTH’S CLOCK'],0)]
    meta={'job':'J0143','approval':'pending Chief review','source':str(args.source),'source_sha256':sha(args.source),'source_credit':'NASA/JPL-Caltech, PIA17049, existing abc_v03 asset','treatment':'Illustrative Voyager spacecraft in code-rendered blue starlight; not a claim that Voyager carries people or travels at 0.99c.','script':'light_speed_script_master_v02.md, opening paragraph and TEACH at 0.99c','answer_quote':'You are gone for one year by your own watch. You land, and seven years have passed at home.','brief_exception':'Answer uses the Chief-requested two-line age comparison (six tokens), exceeding the generic 2–3-word limit. Tease has three words.','variants':[]}
    paths=[]
    for name,lines,yellow in variants:
        im=plate(args.source)
        boxes=words(im,lines,yellow)
        path=args.out/f'024_{name}_j0143_v01.jpg'
        im.save(path,quality=95,subsampling=0)
        paths.append(path)
        meta['variants'].append({'file':str(path),'text':lines,'sha256':sha(path),'text_boxes':boxes,'cap_height':82,'subject_box':[425,260,855,710]})
    gate=Path(__file__).resolve().parents[3]/'00_Brand/Channel-Setup/tools/thumb_preview.py'
    result=subprocess.run([sys.executable,str(gate),'long',*map(str,paths),'--out',str(args.out/'024_j0143_phone_sheet.jpg'),'--score'],capture_output=True,text=True)
    (args.out/'SCORE.txt').write_text(result.stdout+result.stderr)
    (args.out/'META.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
    print(result.stdout)
    return result.returncode
if __name__=='__main__':
    raise SystemExit(main())
