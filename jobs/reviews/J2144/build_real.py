"""Deterministic rule-19 crop/grade; never synthesize mission-image pixels."""
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
p=Path(sys.argv[1])
im=Image.open(p/'PIA14922.jpg').convert('RGB')
im=im.crop((200,560,840,920)).resize((1280,720),Image.Resampling.LANCZOS)
im=ImageEnhance.Color(im).enhance(1.65)
im=ImageEnhance.Brightness(im).enhance(1.2)
im=ImageEnhance.Contrast(im).enhance(1.05)
f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Black.ttf',112)
d=ImageDraw.Draw(im)
x,y=58,38
for text,color in [('ORANGE ',(255,215,30)),('WORLD',(255,255,255))]:
 d.text((x,y),text,font=f,fill=color,stroke_width=5,stroke_fill=(14,18,22))
 x+=d.textlength(text,font=f)
im.save(p/'032_A_real_orange_world_v01.jpg',quality=96,subsampling=0)
