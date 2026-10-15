"""J0273 deterministic typography; generated artwork stays outside git."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib, urllib.request
ROOT=Path('/Users/benjaminoats/_desk/J0273-thumbnails')
FONT='/System/Library/Fonts/Supplemental/Arial Black.ttf'
JOBS=[('laststar','REXYxuLOBoI',[('ONE STAR',False),('LEFT',True)],(45,36),82),('neutron','Yk1tLh23rko',[("DON’T TOUCH",False),('THIS',True)],(45,36),82)]
manifest=[]
for slug,video,lines,pos,size in JOBS:
 art=ROOT/'art'/f'{slug}_orbit.png'
 im=Image.open(art).convert('RGB').resize((1280,720),Image.Resampling.LANCZOS)
 d=ImageDraw.Draw(im); font=ImageFont.truetype(FONT,size); x,y=pos
 for words,yellow in lines:
  d.text((x,y),words,font=font,fill='#FFD400' if yellow else 'white',stroke_width=5,stroke_fill='#071127',anchor='lt')
  y+=int(size*1.08)
 out=ROOT/f'{slug}_B_v02.jpg'; im.save(out,quality=94,optimize=True)
 assert out.stat().st_size<2_000_000
 a=ROOT/f'{slug}_A_live.jpg'
 if not a.exists():
  urllib.request.urlretrieve(f'https://i.ytimg.com/vi/{video}/maxresdefault.jpg',a)
 # Literal phone-size two-column sheet, plus larger tiles for scrutiny.
 sheet=Image.new('RGB',(760,380),'#24334a'); sd=ImageDraw.Draw(sheet)
 label=ImageFont.truetype(FONT,17)
 for i,(p,t) in enumerate([(a,'A - current public thumbnail'),(out,'B - Codex proposal')]):
  ox=15+i*380; sd.text((ox,8),t,font=label,fill='white')
  src=Image.open(p).convert('RGB')
  sheet.paste(src.resize((168,94),Image.Resampling.LANCZOS),(ox,40))
  sheet.paste(src.resize((360,202),Image.Resampling.LANCZOS),(ox,155))
 sheet.save(ROOT/f'{slug}_AB_v02.jpg',quality=94)
 manifest.append({'slug':slug,'video':video,'hook':' '.join(s for s,_ in lines),'art':str(art),'b':str(out),'a':str(a),'sheet':str(ROOT/f'{slug}_AB_v02.jpg'),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'dimensions':[1280,720],'source':'built-in image_gen (requested gpt-image-2 workflow); no API key or payment requested','status':'Chief review required'})
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
