#!/usr/bin/env python3
"""Three editorial New Horizons thumbnail drafts; no generated imagery.
Usage: python3 build_j3105.py --sources <matched> --out <directory>
"""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
FONT='/System/Library/Fonts/Supplemental/Arial Black.ttf'
W,H=1280,720

def text(im,words,y=32):
 d=ImageDraw.Draw(im); f=ImageFont.truetype(FONT,82)
 widths=[d.textlength(t,font=f) for t in words]; gap=26
 x=(W-sum(widths)-gap*(len(words)-1))/2
 for i,t in enumerate(words):
  d.text((x,y),t,font=f,fill='#FFE000' if i==len(words)-1 else 'white',stroke_width=4,stroke_fill='#101b29');x+=widths[i]+gap

def scale(im,x,y,width,label):
 d=ImageDraw.Draw(im); d.line((x,y,x+width,y),fill='white',width=4)
 for xx in (x,x+width):d.line((xx,y-8,xx,y+8),fill='white',width=4)
 d.text((x,y+12),label,font=ImageFont.truetype(FONT,38),fill='white',stroke_width=2,stroke_fill='#102038')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sources',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 manifest=[]
 # A: retain the full enhanced-colour globe, one photographic source, no other objects.
 src=Image.open(a.sources/'PIA19952.jpg').convert('RGB');src=ImageEnhance.Color(src).enhance(1.65)
 # Crop black margin only; retain the globe, then grade the black point to blue.
 arr=np.array(src); mask=arr.max(2)>40; yy,xx=np.where(mask);src=src.crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1));src.thumbnail((580,550))
 im=Image.new('RGB',(W,H),(16,43,75)); arr=np.array(src).astype(float); weight=np.clip(arr.max(2)/38,0,1)[...,None]; arr=arr*weight+np.array([16,43,75])*(1-weight);src=Image.fromarray(np.uint8(np.clip(arr,0,255)))
 im.paste(src,((W-src.width)//2,155));text(im,['NITROGEN','GLACIER']);d=ImageDraw.Draw(im);d.text((45,540),'2,377 km',font=ImageFont.truetype(FONT,40),fill='white');d.text((45,590),'PLUTO DIAMETER',font=ImageFont.truetype(FONT,19),fill='white')
 manifest.append(save(im,a,'A','PIA19952','NITROGEN GLACIER','Full globe; black point lifted to navy; enhanced colour, no added objects. Diameter label is Pluto diameter, not glacier width.'))
 # B: full horizontal panorama retains true horizon and mountains. Warm editorial duotone.
 src=Image.open(a.sources/'PIA19948.jpg').convert('RGB').resize((1280,547),Image.Resampling.LANCZOS)
 lum=ImageOps.autocontrast(src.convert('L'),cutoff=0.4)
 src=ImageOps.colorize(lum,'#123349','#ffce8b')
 im=Image.new('RGB',(W,H),'#123349'); im.paste(src,(0,150));text(im,['ICE','MOUNTAINS']);scale(im,55,596,256,'250 km')
 manifest.append(save(im,a,'B','PIA19948','ICE MOUNTAINS','Entire 1250-km scene width retained; 256/1280 width scale = 250 km. Warm duotone of monochrome MVIC image; not natural colour.'))
 # C: bright ice plain; crop keeps complete source width and its mountains/plain boundary.
 src=Image.open(a.sources/'PIA20726.jpg').convert('RGB');src=src.crop((0,520,2736,1730)).resize((1280,566),Image.Resampling.LANCZOS)
 src=ImageEnhance.Contrast(src).enhance(1.25)
 src=ImageOps.colorize(src.convert('L'),'#075d80','#fff2c9');src=ImageEnhance.Color(src).enhance(2.7)
 im=Image.new('RGB',(W,H),'#438fa8');im.paste(src,(0,154));text(im,['FLOWING','ICE']);scale(im,55,596,320,'100 km')
 manifest.append(save(im,a,'C','PIA20726','FLOWING ICE','Bright cyan/cream editorial grade; full 400-km source width retained; 320/1280 scale = 100 km. Crop y=520:1730; no terrain invented.'))
 (a.out/'MANIFEST.json').write_text(json.dumps({'status':'DRAFT_REVIEW_NOT_APPROVED','job':'J3105','spend':0,'candidates':manifest},indent=2)+'\n')

def save(im,a,variant,source,hook,note):
 name=f'034_pluto_{variant}_j3105_v01.jpg';p=a.out/name;im.save(p,quality=96,subsampling=0)
 return {'variant':variant,'file':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':source,'source_sha256':hashlib.sha256((a.sources/(source+'.jpg')).read_bytes()).hexdigest(),'hook':hook,'processing':note,'size':[W,H]}
if __name__=='__main__':main()
