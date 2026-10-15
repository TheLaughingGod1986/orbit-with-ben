"""J0328: deterministic house typography and existing EPIC plate; no generation or spend."""
from pathlib import Path
import argparse, hashlib, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
p=argparse.ArgumentParser(); p.add_argument('--source',required=True); a=p.parse_args()
here=Path(__file__).resolve().parent; out=here/'abc_v01'; out.mkdir(exist_ok=True)
repo=here.parents[2]; sys.path.insert(0,str(repo/'00_Brand/Channel-Setup/tools'))
from thumb_preview import score
W,H=1280,720
# Recover the unobscured EPIC globe from frame zero of the locked v01l master.
src=Image.open(a.source).convert('RGB').crop((460,40,1460,1040))
src=ImageEnhance.Brightness(src).enhance(1.26)
src=ImageEnhance.Color(src).enhance(2.05)
src=ImageEnhance.Contrast(src).enhance(1.10)
src=src.filter(ImageFilter.UnsharpMask(radius=1.6,percent=55,threshold=3))
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Black.ttf',110)
variants=[('A',['OCEANS','MOVE'],1,(12,35,64),(30,105,154)),('B',['ONE-YEAR','DAYS'],1,(24,29,62),(67,68,146)),('C',['AIR','RACES ON'],1,(9,41,57),(24,111,125))]
meta={'job':'J0328','status':'draft for Chief review','source':'NASA DSCOVR EPIC 2025-06-21; unobscured globe recovered from frame 0 of locked v01l master','source_sha256':hashlib.sha256(Path(a.source).read_bytes()).hexdigest(),'variants':[]}
for key,lines,hook,lo,hi in variants:
 y,x=np.mgrid[:H,:W]; g=np.exp(-((x-900)**2+(y-360)**2)/(550**2))
 bg=np.array(lo)+(np.array(hi)-np.array(lo))*g[:,:,None]
 rng=np.random.default_rng(328); bg+=rng.normal(0,0.7,(H,W,1))
 im=Image.fromarray(np.uint8(np.clip(bg,0,255)))
 d=650; globe=src.resize((d,d),Image.Resampling.LANCZOS)
 mask=Image.new('L',(d,d)); ImageDraw.Draw(mask).ellipse((2,2,d-3,d-3),fill=255)
 halo=Image.new('RGBA',(W,H)); hd=ImageDraw.Draw(halo); hd.ellipse((613,28,1271,686),fill=(75,169,255,110)); halo=halo.filter(ImageFilter.GaussianBlur(16))
 im=Image.alpha_composite(im.convert('RGBA'),halo).convert('RGB'); im.paste(globe,(617,33),mask)
 dr=ImageDraw.Draw(im)
 for j,line in enumerate(lines):
  font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Black.ttf',99 if key in ('B','C') else 110)
  box=dr.textbbox((0,0),line,font=font); width=box[2]-box[0]
  assert width<=575,(line,width)
  dr.text((30,180+j*135-box[1]),line,font=font,fill=(255,230,0) if j==hook else 'white',stroke_width=6,stroke_fill=(3,9,18))
  if key=='C' and j==1:
   offset=dr.textlength('RACES ',font=font)
   dr.text((30+offset,180+j*135-box[1]),'ON',font=font,fill='white',stroke_width=6,stroke_fill=(3,9,18))
 f=out/f'earth_spin_thumb_{key}.jpg'; im.save(f,quality=95,subsampling=0)
 s=score(f,'long'); meta['variants'].append({'key':key,'file':f.name,'text':' '.join(lines),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size,'score':s})
(out/'META.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta,indent=2))
