from PIL import Image,ImageDraw,ImageFont,ImageEnhance
from pathlib import Path
import shutil
ROOT=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
BASE=ROOT/'02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/09_Thumbnails'
old=BASE/'J2144_v01'; out=BASE/'J2144_v02';out.mkdir(exist_ok=True)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Black.ttf',112)
def label(im,s,x,y,color):
 d=ImageDraw.Draw(im);b=d.textbbox((0,0),s,font=font,stroke_width=5); d.text((x-b[0],y-b[1]),s,font=font,fill=color,stroke_width=5,stroke_fill='#131116')
shutil.copy2('/private/tmp/j2176-pia14909.jpg',out/'PIA14909.jpg')
a=Image.open(out/'PIA14909.jpg').convert('RGB').crop((180,270,992,727)).resize((1280,720),Image.Resampling.LANCZOS)
a=ImageEnhance.Color(a).enhance(2.0);a=ImageEnhance.Brightness(a).enhance(1.25)
layer=Image.new('RGBA',(500,110));label(layer,'THIS IS',0,0,'white');layer=layer.resize((400,110),Image.Resampling.LANCZOS);a.paste(layer,(850,55),layer);label(a,'TITAN',850,165,'#ffdf00')
a.save(out/'032_A_real_this_is_titan_v02.jpg',quality=96,subsampling=0)
c=Image.open(old/'C_plate.png').convert('RGB').resize((1280,720),Image.Resampling.LANCZOS)
label(c,'ICE IS',650,45,'white');label(c,'ROCK',650,155,'#ffdf00')
c.save(out/'032_C_scale_ice_is_rock_v03.jpg',quality=96,subsampling=0)
shutil.copy2(old/'032_B_bright_methane_shore_v02.jpg',out/'032_B_bright_methane_shore_v02.jpg')
print(out)
