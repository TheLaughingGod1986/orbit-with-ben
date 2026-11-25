#!/usr/bin/env python3
"""J3112-directed revision of the existing plate compositor; no generated pixels."""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
from build_j3105 import text, FONT, W, H

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def label(im,xy,s,size=48):
 ImageDraw.Draw(im).text(xy,s,font=ImageFont.truetype(FONT,size),fill='white',stroke_width=2,stroke_fill='#102b4b')
def bar(im,width,label_text):
 d=ImageDraw.Draw(im);x,y=55,595
 d.line((x,y,x+width,y),fill='white',width=8)
 for xx in (x,x+width):d.line((xx,y-12,xx,y+12),fill='white',width=8)
 label(im,(x,y+17),label_text,48)
def vignette(im):
 a=np.asarray(im).astype(float); yy,xx=np.indices((H,W)); top=np.clip((220-yy)/220,0,1)**1.2
 pad=.78*np.exp(-((xx-160)/280)**4-((yy-660)/120)**4)
 w=np.maximum(top,pad)[...,None]; navy=np.array([13,34,56]);return Image.fromarray(np.uint8(a*(1-w)+navy*w))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sources',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 old=json.loads(Path(__file__).with_name('MANIFEST_J3105_v01.json').read_text());rows=[]
 def save(im,v,note,recipe):
  prev=next(r for r in old['candidates'] if r['variant']==v);source=a.sources/(prev['source']+'.jpg'); assert sha(source)==prev['source_sha256']
  name=f'034_pluto_{v}_j3105_v02.jpg';p=a.out/name;im.save(p,quality=96,subsampling=0)
  row={**prev,'file':name,'sha256':sha(p),'processing':note,'recipe':recipe,'durable_path':str(Path(prev['durable_path']).parent.parent/'J3105_v02'/name)};rows.append(row)
 # The disc fits BELOW the title: a full 650 px disc cannot fit in a 720 px frame
 # with a 140 px text band. Chief J3112 explicitly prioritises the whole limb.
 src=Image.open(a.sources/'PIA19952.jpg').convert('RGB')
 # Source limb centre/radius measured on the verified 5000-square plate.
 box=(300,300,4650,4650);src=src.crop(box).resize((560,560),Image.Resampling.LANCZOS)
 src=ImageEnhance.Color(src).enhance(1.55);src=ImageEnhance.Contrast(src).enhance(1.08)
 yy,xx=np.indices((560,560));r=np.sqrt((xx-279.5)**2+(yy-279.5)**2)
 mask=Image.fromarray(np.uint8(np.clip((279.5-r)/3.5,0,1)*255))
 im=Image.new('RGB',(W,H),'#102b4b');im.paste(src,(430,145),mask);text(im,['NITROGEN','GLACIER'])
 label(im,(50,510),'PLUTO',52);label(im,(50,575),'2,377 km',48)
 save(im,'A','Whole globe with 3.5 px circular limb feather, no rectangular paste seam. 560 px diameter prioritises whole limb and text clearance under J3112. Planet diameter explicitly labelled; no glacier caliper.',{'source_crop':box,'disc_size':560,'paste':[430,145],'limb_feather_px':3.5})
 # Tighten horizontal field by 18%, keeping all vertical haze and relief.
 src=Image.open(a.sources/'PIA19948.jpg').convert('RGB');box=(308,0,3112,1461)
 src=src.crop(box).resize((1280,667),Image.Resampling.LANCZOS)
 lum=ImageOps.autocontrast(src.convert('L'),cutoff=.5)
 src=ImageOps.colorize(lum,'#0d2948','#e6f6ff',mid='#4288b1')
 im=Image.new('RGB',(W,H),'#0d2948');im.paste(src,(0,110));im=vignette(im);text(im,['ICE','MOUNTAINS'])
 width=round(250/(1250*(box[2]-box[0])/3420)*1280);bar(im,width,'~250 km')
 save(im,'B','Cold blue/silver editorial grade, not true colour. 18% horizontal crop retains haze and mountain/plain boundary. Approximate scene-width scale, not a local foreshortened terrain measurement.',{'source_crop':box,'source_scene_width_km':1250,'crop_scene_width_km':1250*2804/3420,'scale_km':250,'scale_px':width})
 src=Image.open(a.sources/'PIA20726.jpg').convert('RGB');box=(0,520,2736,2059)
 src=src.crop(box).resize((W,H),Image.Resampling.LANCZOS)
 # Cream highlights and dark rust/charcoal valleys retain the actual terrain.
 lum=ImageOps.autocontrast(src.convert('L'),cutoff=.5)
 im=ImageOps.colorize(lum,'#292325','#fff0cc',mid='#a77d55');im=ImageEnhance.Color(im).enhance(1.35);im=vignette(im);text(im,['FLOWING','ICE']);bar(im,320,'~100 km')
 save(im,'C','Warm cream/rust/charcoal editorial grade, not natural colour; actual cellular plain and shoreline. Smooth navy top vignette and lower-left scale pad. Full 400 km source width retained; approximate scene reference.',{'source_crop':box,'source_scene_width_km':400,'scale_km':100,'scale_px':320})
 manifest={**old,'job':'J3114','chief_review_job':'J3115','candidates':rows,'phone_review':'phone_review_v02.jpg','title_pairing_draft':'Why Does Pluto Have a Heart? (And Why It Has Zero Craters)','title_status':'Panel wording applied; exact arms remain subject to J3115.'}
 (a.out/'MANIFEST_J3105_v02.json').write_text(json.dumps(manifest,indent=2)+'\n')
 sheet=Image.new('RGB',(950,780),'#e8edf3')
 for i,row in enumerate(rows):
  im=Image.open(a.out/row['file']);y=i*260;d=ImageDraw.Draw(sheet);d.text((20,y+10),row['variant']+'  |  168 x 94 and 360 x 202',font=ImageFont.truetype(FONT,20),fill='#102b4b')
  sheet.paste(im.resize((168,94),Image.Resampling.LANCZOS),(20,y+55));sheet.paste(im.resize((360,202),Image.Resampling.LANCZOS),(230,y+45))
 sheet.save(a.out/'phone_review_v02.jpg',quality=96)
if __name__=='__main__':main()
