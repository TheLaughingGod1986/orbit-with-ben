#!/usr/bin/env python3
"""J3378: reproducible NASA photographic composites; no API writes or generation.
Requires Pillow and numpy. All output names are exclusive (never overwrite).
Run --sources <folder> --out <new folder>; source filenames listed in SOURCES.
Solar plate is an illustrative red-dwarf proxy, not a photograph of a red dwarf.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from build_weekly_thumbs_j2834 import draw_top_band, draw_arrow, FONT_PATH
from thumb_preview import score

W,H=1280,720
SOURCES={
 'earth.jpg': ('as17-148-22727','NASA Apollo 17','https://images.nasa.gov/details/as17-148-22727'),
 'europa.jpg': ('PIA19048','NASA/JPL-Caltech/SETI Institute','https://science.nasa.gov/resource/europa-in-color/'),
 'eva.jpg': ('S84-27018','NASA','https://images.nasa.gov/details/S84-27018'),
 'sun.jpg': ('GSFC_20171208_Archive_e002069','NASA/GSFC/SDO','https://images.nasa.gov/details/GSFC_20171208_Archive_e002069'),
 'field.webp': ('NGC6638 potw2231a','ESA/Hubble & NASA, R. Cohen','https://science.nasa.gov/missions/hubble/hubble-gazes-at-a-star-studded-skyfield/'),
}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rgb(a): return Image.fromarray(np.uint8(np.clip(a,0,255)))
def load(p): return Image.open(p).convert('RGB')

def background(p, motion=False):
    # Peripheral crop avoids the bright cluster core. Real star pixels only.
    src=load(p); src=src.crop((0,0,1700,956)).resize((W,H),Image.Resampling.LANCZOS)
    a=np.asarray(src,dtype=float)/255
    lum=a.mean(axis=2)
    # Compress dense faint stars while preserving point-source texture.
    signal=np.power(lum,2.0)*0.30
    a=signal[:,:,None]*np.array([150,175,225])+np.array([17,27,54])
    im=rgb(a)
    if motion:
        # Integrate resampled photographic exposures around a vanishing point.
        # Smooth zoom kernel, no drawn ray primitives.
        acc=np.zeros((H,W,3)); total=0
        for z in np.linspace(1,1.65,64):
            scaled=im.resize((round(W*z),round(H*z)),Image.Resampling.BICUBIC)
            cx,cy=900,330
            frame=scaled.crop((round(cx*(z-1)),round(cy*(z-1)),round(cx*(z-1))+W,round(cy*(z-1))+H))
            weight=np.sin(np.pi*(z-1)/.65)**2+.15
            acc+=np.asarray(frame)*weight;total+=weight
        im=rgb(acc/total).filter(ImageFilter.GaussianBlur(.35))
    return im

def globe(p,diam):
    src=load(p); a=np.asarray(src); ys,xs=np.where(a.mean(2)>24)
    cx,cy=(xs.min()+xs.max())/2,(ys.min()+ys.max())/2
    r=min(xs.max()-xs.min(),ys.max()-ys.min())/2
    im=src.crop((int(cx-r),int(cy-r),int(cx+r),int(cy+r))).resize((diam,diam),Image.Resampling.LANCZOS)
    im=ImageEnhance.Color(im).enhance(1.4)
    y,x=np.mgrid[:diam,:diam]; mask=np.clip((diam/2-1-np.hypot(x-diam/2,y-diam/2))/1.4,0,1)
    im=im.convert('RGBA');im.putalpha(Image.fromarray(np.uint8(mask*255)));return im

def paste(im,fg,xy,glow=None):
    layer=Image.new('RGBA',im.size);layer.alpha_composite(fg,xy)
    if glow:
        halo=Image.new('RGBA',im.size,glow+(0,));halo.putalpha(layer.getchannel('A').filter(ImageFilter.GaussianBlur(15)).point(lambda v:int(v*.55)))
        im.paste(Image.alpha_composite(im.convert('RGBA'),halo).convert('RGB'))
    im.paste(Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB'))

def exterior_mask(a,threshold=25):
    dark=a.mean(2)<threshold; h,w=dark.shape; visited=np.zeros((h,w),bool)
    stack=[(y,x) for y in range(h) for x in (0,w-1)]+[(y,x) for x in range(w) for y in (0,h-1)]
    while stack:
        y,x=stack.pop()
        if not (0<=y<h and 0<=x<w) or visited[y,x] or not dark[y,x]: continue
        visited[y,x]=True;stack.extend(((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
    return Image.fromarray(np.uint8(~visited)*255)

def europa(s):
    im=background(s/'field.webp')
    earth=globe(s/'earth.jpg',850)
    paste(im,earth,(-130,180),(45,95,170))
    # PIA19048 is a crescent/terminator view, not a complete full disk.
    src=load(s/'europa.jpg'); src=ImageEnhance.Color(src).enhance(1.65)
    src=ImageEnhance.Contrast(src).enhance(1.12)
    a=np.asarray(src); mask=exterior_mask(a,13).filter(ImageFilter.GaussianBlur(1))
    src=src.convert('RGBA');src.putalpha(mask)
    src=src.resize((350,259),Image.Resampling.LANCZOS)
    paste(im,src,(850,275))
    draw_arrow(im,(790,225),(892,316),shaft_w=5,head_len=22,head_half=10)
    box=draw_top_band(im,['2×',"EARTH'S",'WATER'],'2×',tracking=-2)
    return im,box,'Earth diameter 850 px; Europa limb diameter about 327 px (38.5%). Apparent comparison, not an exact physical scale. PIA19048 terminator retained.'

def speed(s):
    im=background(s/'field.webp',True)
    src=load(s/'eva.jpg')
    earth=src.crop((0,1225,1920,1900)).resize((1280,400),Image.Resampling.LANCZOS)
    earth=ImageEnhance.Color(earth).enhance(1.65)
    a=np.asarray(earth,dtype=float)*np.array([.34,.43,.56])
    earth=rgb(a).convert('RGBA')
    # Feather source horizon into space, preserving the photographed limb.
    alpha=np.clip(np.asarray(earth.convert('RGB')).mean(2)/18,0,1)*255
    alpha[:50]*=np.linspace(0,1,50)[:,None]
    earth.putalpha(Image.fromarray(np.uint8(alpha)));paste(im,earth,(0,450))
    cut=src.crop((790,620,1070,920));mask=exterior_mask(np.asarray(cut),25)
    mask=mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.65))
    cut=ImageEnhance.Contrast(cut).enhance(1.07).convert('RGBA');cut.putalpha(mask)
    cut=cut.resize((644,690),Image.Resampling.LANCZOS)
    paste(im,cut,(160,120))
    box=draw_top_band(im,['EARTH','AGES','7×'],'7×',tracking=-2)
    return im,box,'S84-27018 EVA cutout and Earth limb; 2.3x source crop enlargement. Space travel metaphor, not actual relativistic EVA. Hubble star-pixel zoom integration (64 exposures), no vector rays.'

def stars(s):
    im=background(s/'field.webp')
    src=load(s/'sun.jpg'); a=np.asarray(src);ys,xs=np.where(a[:,:,0]>45)
    src=src.crop((int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)))
    a=np.asarray(src,dtype=float); lum=a[:,:,0]/255
    alpha=np.clip((lum-.045)/.20,0,1)
    def star(size,red):
        if red: c=np.stack((lum**.50*255,lum**2.0*65,lum**1.7*53),2)
        else: c=np.stack((lum**.48*222,lum**.48*205,lum**.48*168),2)
        out=rgb(c).convert('RGBA');out.putalpha(Image.fromarray(np.uint8(alpha*255)))
        return out.resize((size,round(size*src.height/src.width)),Image.Resampling.LANCZOS)
    paste(im,star(850,False),(-160,180),(90,65,35))
    paste(im,star(310,True),(860,280),(255,22,40))
    draw_arrow(im,(790,225),(887,315),shaft_w=5,head_len=22,head_half=10)
    box=draw_top_band(im,['OUTLIVES','OUR','SUN'],'OUTLIVES',tracking=-2)
    return im,box,'Both stars use real SDO 304-Angstrom solar texture. Smaller crimson star is an illustrative solar proxy for a red dwarf, NOT a resolved red-dwarf photograph; colours, apparent sizes and brightness are editorial comparisons, not a temperature/size measurement.'

def phone(im,duration,out):
    sheet=Image.new('RGB',(580,260),(30,30,34));d=ImageDraw.Draw(sheet)
    for x,size in [(10,(168,94)),(200,(360,202))]:
        tile=im.resize(size,Image.Resampling.LANCZOS);td=ImageDraw.Draw(tile)
        font=ImageFont.truetype(FONT_PATH,11 if size[0]==168 else 20)
        bb=td.textbbox((0,0),duration,font=font);tw=bb[2];th=bb[3]-bb[1]
        px,py=size[0]-tw-6,size[1]-th-6
        td.rectangle((px-3,py-2,size[0]-2,size[1]-2),fill=(15,15,15))
        td.text((px,py-bb[1]),duration,font=font,fill='white')
        sheet.paste(tile,(x,32));d.text((x,10),f'{size[0]} x {size[1]}',fill='white')
    sheet.save(out,quality=95)

def main():
    p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    if args.out.exists(): raise SystemExit('Refusing existing output directory')
    for f in SOURCES:
        if not (args.sources/f).is_file(): raise SystemExit('Missing source '+f)
    args.out.mkdir(parents=True)
    rows=[]
    for vid,hook,dur,build in [('NbW5G1BpPY0',"2× EARTH'S WATER",'9:19',europa),('rVqgtkBV3jc','EARTH AGES 7×','8:55',speed),('REXYxuLOBoI','OUTLIVES OUR SUN','8:38',stars)]:
        im,box,note=build(args.sources);f=args.out/f'{vid}_B_v02.jpg';im.save(f,quality=95,subsampling=0,optimize=True)
        sheet=args.out/f'{vid}_phone_badge_sheet_v02.jpg';phone(im,dur,sheet)
        row=dict(video=vid,hook=hook,file=str(f),sha256=sha(f),bytes=f.stat().st_size,score=score(f,'long'),text_box=box,phone_sheet=str(sheet),phone_sha256=sha(sheet),composition=note)
        rows.append(row);print(vid,row['score'])
    manifest=dict(job='J3378',status='proposed',spend_gbp=0,sources=[dict(file=f,id=v[0],credit=v[1],url=v[2],sha256=sha(args.sources/f)) for f,v in SOURCES.items()],candidates=rows)
    (args.out/'DESIGN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__': main()
