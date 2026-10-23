#!/usr/bin/env python3
"""House cover typography for J0889. Usage: script.py --assets <art dir> --out <output dir>."""
from pathlib import Path
import argparse,json
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
ap=argparse.ArgumentParser();ap.add_argument('--assets',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
font='/System/Library/Fonts/Supplemental/Arial Black.ttf'
meta=[]
for key,words,hook in [('A',['STAR','VISITOR'],'VISITOR'),('B',['COMET','NUDGE'],'NUDGE'),('C',["SUN’S",'NEIGHBOUR'],'NEIGHBOUR')]:
 src=a.assets/f'gliese_art_{key}.png'
 if not src.exists():continue
 im=ImageOps.fit(Image.open(src).convert('RGB'),(1280,720),method=Image.Resampling.LANCZOS)
 # Mild whole-frame grade; no subject cropping or image painting.
 im=ImageEnhance.Brightness(im).enhance(1.08)
 d=ImageDraw.Draw(im)
 size=112
 while True:
  f=ImageFont.truetype(font,size);cap=f.getbbox('H');height=cap[3]-cap[1]
  widths=[d.textlength(w,font=f) for w in words];total=sum(widths)+28
  if height<=82 and total<=1160:break
  size-=1
 top_pad=26 if key=='C' else 40
 x=(1280-total)/2;y=top_pad-cap[1];boxes=[]
 for word,width in zip(words,widths):
  color=(255,230,0) if word==hook else 'white'
  d.text((x+3,y+4),word,font=f,fill='black',stroke_width=6,stroke_fill='black')
  d.text((x,y),word,font=f,fill=color,stroke_width=5,stroke_fill='black')
  boxes.append(list(d.textbbox((x,y),word,font=f,stroke_width=5)));x+=width+28
 dst=a.out/f'gliese_thumb_{key}.jpg';im.save(dst,quality=94,subsampling=0)
 meta.append({'variant':key,'text':' '.join(words),'yellow':hook,'font':'Arial Black','font_size':size,'cap_height':height,'cap_share':height/720,'text_boxes':boxes,'file':dst.name,'art':src.name})
(a.out/'COVER_LAYOUT.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta,indent=2))
