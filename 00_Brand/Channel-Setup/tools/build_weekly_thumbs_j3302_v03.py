#!/usr/bin/env python3
"""J3381: reproducible NASA photographic composites; no API writes or generation.
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
 'eva_new.jpg': ('s84-27017','NASA','https://images.nasa.gov/details/s84-27017'),
 'sun.jpg': ('GSFC_20171208_Archive_e002069','NASA/GSFC/SDO','https://images.nasa.gov/details/GSFC_20171208_Archive_e002069'),
 'field.jpg': ('GSFC_20171208_Archive_e002064','NASA, ESA, M. Livio and the Hubble 20th Anniversary Team (STScI)','https://images.nasa.gov/details/GSFC_20171208_Archive_e002064'),
}

EXPECTED_SHA256={'earth.jpg': 'cb4c3d2da98ee72130ebfd2ea472fc84ede6726002c2a8c9cabd86e4deea9f0f', 'europa.jpg': 'f020c034750675cb0ace6c3164b18151746bfa28405e888d810312cd563d650d', 'eva_new.jpg': '220b4ef88dd4c98f4dd5b62c18372e7c3151d9a206aa299c274874683569972a', 'sun.jpg': 'e13524641873a6ec38798932ff3823f2f9fa33e27caf6c309d0f0fbe3eb4af34', 'field.jpg': 'd90c54b8a809cd43beb9a630bd846b0c7328d45afa32b26d03fb67041b6e517e'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rgb(a): return Image.fromarray(np.uint8(np.clip(a,0,255)))
def load(p): return Image.open(p).convert('RGB')

def background(p, motion=False):
    # Remove low-frequency nebula signal; retain real Hubble point-source pixels.
    # Select compact star cores from known locations in the photographic plate.
    # No full-frame high-pass residual: that retains bright nebula contours.
    src=load(p).resize((W,H),Image.Resampling.LANCZOS)
    a=np.asarray(src,dtype=float)/255
    lum=a.mean(axis=2)
    smooth=np.asarray(src.filter(ImageFilter.GaussianBlur(8)),dtype=float).mean(2)/255
    yy,xx=np.mgrid[:H,:W];mask=np.zeros((H,W),bool)
    for x,y in [(.14,.025),(.48,.04),(.11,.7),(.42,.51),(.59,.47),(.93,.94),(.7,.15),(.95,.13),(.59,.105),(.28,.09),(.005,.39),(.02,.30)]:
        mask |= ((xx-x*W)**2+(yy-y*H)**2)<225
    signal=np.clip(lum-smooth-.04,0,1)*mask*3
    a=signal[:,:,None]*np.array([150,175,225])+np.array([17,27,54])
    im=rgb(a)
    if motion:
        # Redistribute the same photographic point-source texture for a legible
        # travel metaphor; these are composited stars, not a sky map.
        sy,sx=np.unravel_index(np.argmax(signal),signal.shape)
        patch=im.crop((sx-8,sy-8,sx+9,sy+9))
        for x,y in [(120,220),(420,210),(680,190),(1100,220),(180,480),(900,550),(570,630),(1080,480),(100,650)]:
            im.paste(patch,(x,y))
        # Integrate resampled photographic exposures around a vanishing point.
        # Smooth zoom kernel, no drawn ray primitives.
        acc=np.zeros((H,W,3)); total=0
        for z in np.linspace(1,1.65,256):
            scaled=im.resize((round(W*z),round(H*z)),Image.Resampling.BICUBIC)
            cx,cy=900,330
            frame=scaled.crop((round(cx*(z-1)),round(cy*(z-1)),round(cx*(z-1))+W,round(cy*(z-1))+H))
            weight=np.sin(np.pi*(z-1)/.65)**2+.15
            acc+=np.asarray(frame)*weight;total+=weight
        im=rgb((acc/total-np.array([17,27,54]))*12+np.array([17,27,54])).filter(ImageFilter.GaussianBlur(.35))
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
    im=background(s/'field.jpg')
    earth=globe(s/'earth.jpg',1800)
    paste(im,earth,(-1450,165),(45,95,170))
    # PIA19048 is a crescent/terminator view, not a complete full disk.
    src=load(s/'europa.jpg'); src=ImageEnhance.Color(src).enhance(1.65)
    src=ImageEnhance.Contrast(src).enhance(1.12)
    a=np.asarray(src); mask=exterior_mask(a,13).filter(ImageFilter.GaussianBlur(1))
    src=src.convert('RGBA');src.putalpha(mask)
    src=src.resize((760,563),Image.Resampling.LANCZOS)
    paste(im,src,(470,145))
    box=draw_top_band(im,['2×',"EARTH'S",'WATER'],'2×',tracking=-2)
    return im,box,'Earth diameter 1800 px partial reference; Europa limb diameter about 710 px (39.4%), whole source silhouette retained. Apparent comparison, not an exact physical scale. PIA19048 terminator retained.'

def speed(s):
    im=background(s/'field.jpg',True)
    original=load(s/'eva_new.jpg')
    # Downsample the much closer original exposure; no enlarged distant crop.
    src=original.resize((1280,1290),Image.Resampling.LANCZOS)
    # Whole astronaut with original photographed Earth below; isolate by a
    # luminance mask only above the limb, retaining suit blacks internally.
    cut=src.crop((350,55,1000,745))
    mask=exterior_mask(np.asarray(cut),25)
    # Original horizon reaches the bottom of the crop; exclude it below boots.
    aa=np.asarray(mask).copy(); aa[675:]=0
    ca=np.asarray(cut,dtype=float)
    yy=np.arange(cut.height)[:,None]
    aa[(yy>590)&(ca[:,:,2]>ca[:,:,0]*1.15)&(ca[:,:,2]>ca[:,:,1]*1.04)]=0
    mask=Image.fromarray(aa).filter(ImageFilter.GaussianBlur(.55))
    cut=cut.convert('RGBA');cut.putalpha(mask)
    cut=cut.resize((490,520),Image.Resampling.LANCZOS)
    paste(im,cut,(330,166))
    earth=globe(s/'earth.jpg',1000)
    earth=ImageEnhance.Brightness(earth).enhance(.65)
    paste(im,earth,(1050,260))
    box=draw_top_band(im,['EARTH','AGES','7×'],'7×',tracking=-2)
    return im,box,'s84-27017 closer EVA exposure, full astronaut silhouette downsampled from 6852px original; partial Apollo Earth reference. Space travel metaphor, not actual relativistic EVA. Redistributed photographic Hubble star-core texture with zoom integration (256 exposures), no vector rays.'

def stars(s):
    im=background(s/'field.jpg')
    src=load(s/'sun.jpg'); a=np.asarray(src);ys,xs=np.where(a[:,:,0]>45)
    src=src.crop((int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)))
    a=np.asarray(src,dtype=float); lum=a[:,:,0]/255
    alpha=np.clip((lum-.045)/.20,0,1)
    def star(size,red):
        if red: c=np.stack((lum**.50*255,lum**2.0*65,lum**1.7*53),2)
        else: c=np.stack((lum**.48*222,lum**.48*205,lum**.48*168),2)
        out=rgb(c).convert('RGBA');out.putalpha(Image.fromarray(np.uint8(alpha*255)))
        return out.resize((size,round(size*src.height/src.width)),Image.Resampling.LANCZOS)
    paste(im,star(1500,False).transpose(Image.Transpose.FLIP_LEFT_RIGHT),(1000,175),(90,65,35))
    paste(im,star(530,True),(190,165),(255,22,40))
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
        if sha(args.sources/f)!=EXPECTED_SHA256[f]: raise SystemExit('Source hash mismatch '+f)
    args.out.mkdir(parents=True)
    rows=[]
    for vid,hook,dur,build in [('NbW5G1BpPY0',"2× EARTH'S WATER",'9:19',europa),('rVqgtkBV3jc','EARTH AGES 7×','8:55',speed),('REXYxuLOBoI','OUTLIVES OUR SUN','8:38',stars)]:
        im,box,note=build(args.sources);f=args.out/f'{vid}_B_v03.jpg';im.save(f,quality=95,subsampling=0,optimize=True)
        sheet=args.out/f'{vid}_phone_badge_sheet_v03.jpg';phone(im,dur,sheet)
        row=dict(video=vid,hook=hook,file=str(f),sha256=sha(f),bytes=f.stat().st_size,score=score(f,'long'),text_box=box,phone_sheet=str(sheet),phone_sha256=sha(sheet),composition=note)
        rows.append(row);print(vid,row['score'])
    manifest=dict(job='J3381',status='proposed',spend_gbp=0,sources=[dict(file=f,id=v[0],credit=v[1],url=v[2],asset_url=f'https://images-assets.nasa.gov/image/{v[0]}/{v[0]}~orig.jpg',sha256=sha(args.sources/f)) for f,v in SOURCES.items()],candidates=rows)
    (args.out/'DESIGN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__': main()
