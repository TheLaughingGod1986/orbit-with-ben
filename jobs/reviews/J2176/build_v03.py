"""J2212-approved single-frame crop/grade, no compositing or generation."""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import sys
source, output = map(Path, sys.argv[1:3])
im = Image.open(source).convert("RGB").crop((0,224,1024,800)).resize((1280,720),Image.Resampling.LANCZOS)
im = ImageEnhance.Color(im).enhance(1.65)
im = ImageEnhance.Brightness(im).enhance(1.2)
f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Black.ttf",112)
d = ImageDraw.Draw(im)
x = 60
for text, color in [("THIS IS ","white"),("TITAN","#ffdf00")]:
    box = d.textbbox((0,0),text,font=f)
    d.text((x,42-box[1]),text,font=f,fill=color,stroke_width=5,stroke_fill="#131116")
    x += d.textlength(text,font=f)
im.save(output,quality=96,subsampling=0)
