"""House typography over text-free illustration plates; no generation calls."""
import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
p=Path(sys.argv[1])
f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Black.ttf',112)
for side,parts,stem in [('B',[('METHANE ',(255,215,30)),('SHORE',(255,255,255))],'bright_methane_shore'),('C',[('ICE IS ',(255,255,255)),('ROCK',(255,215,30))],'scale_ice_is_rock')]:
 src=p/f'{side}_plate.png'
 if not src.exists(): continue
 im=ImageOps.fit(Image.open(src).convert('RGB'),(1280,720),method=Image.Resampling.LANCZOS)
 d=ImageDraw.Draw(im)
 width=sum(d.textlength(t,font=f) for t,_ in parts)
 x=(1280-width)/2
 for t,c in parts:
  d.text((x,0 if side == "C" else 20),t,font=f,fill=c,stroke_width=5,stroke_fill=(14,18,22))
  x+=d.textlength(t,font=f)
 im.save(p/f'032_{side}_{stem}_v02.jpg',quality=96,subsampling=0)
