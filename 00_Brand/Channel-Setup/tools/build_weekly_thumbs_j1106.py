#!/usr/bin/env python3
"""J1106 review drafts. House compositing only, no generation or YouTube writes.
Uses existing master/NASA plates; output remains outside git. Run with thumbs venv.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageEnhance,ImageFilter,ImageFont,ImageStat
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'00_Brand/Channel-Setup/tools'))
import build_packaging_long_thumbs_j0133 as pack
OUT=Path('/Users/benjaminoats/_desk/j1106/designs');OUT.mkdir(exist_ok=True)
SRC=Path('/Users/benjaminoats/_desk/thumb_packaging_1011/plates')
W,H=1280,720

def background(seed,colour):
 rng=np.random.default_rng(seed);y,x=np.mgrid[0:H,0:W];g=np.exp(-((x-680)**2/700**2+(y-470)**2/450**2))
 a=np.zeros((H,W,3),float)
 for k,c in enumerate(colour):a[:,:,k]=[16,23,49][k]+g*c
 a+=rng.normal(0,1.2,(H,W,1));im=Image.fromarray(a.clip(0,255).astype('uint8'));d=ImageDraw.Draw(im)
 for _ in range(100):
  x,y=int(rng.integers(W)),int(rng.integers(170,H));v=int(rng.integers(65,150));d.ellipse((x,y,x+1,y+1),fill=(v,v,min(v+25,255)))
 return im

def stellar_disc(size):
 # Inset the mask inside the actual limb (centre 640,370, radius ~245).
 # Compress highlights and warm-grade the existing texture, removing blue flare colour.
 p=Image.open(SRC/'laststar_master_t243.png').convert('RGB').crop((410,140,870,600))
 a=np.asarray(p).astype(float)/255
 t=a[:,:,0]**0.65
 rgb=np.stack((45+135*t, 12+49*t, 13+34*t),axis=2)
 p=Image.fromarray(rgb.clip(0,255).astype('uint8')).resize((size,size),Image.Resampling.LANCZOS)
 m=Image.new('L',(size,size),0);ImageDraw.Draw(m).ellipse((4,4,size-5,size-5),fill=255)
 return p,m.filter(ImageFilter.GaussianBlur(2))

def last_star():
 im=background(5,(47,13,37));p,m=stellar_disc(490)
 im.paste(p,(450,180),m)
 im=pack.grade(im,120,False);pack.band(im,['10','TRILLION','YEARS'],'TRILLION');return im

def andromeda():
 # Full-width plate, with its own blurred sky behind the title; no inset rectangle.
 p=Image.open(SRC/'andromeda_PIA15416.jpg').convert('RGB').crop((1000,1300,8500,6000))
 p=p.filter(ImageFilter.MedianFilter(5))
 p=pack.grade(p,120,True)
 im=background(19,(9,26,53))
 fg=p.resize((W,535),Image.Resampling.LANCZOS)
 mask=np.ones((535,W),dtype=np.uint8)*255
 mask[:75,:]=np.linspace(0,255,75).astype('uint8')[:,None]
 im.paste(fg,(0,185),Image.fromarray(mask))
 im=pack.grade(im,115,True);pack.band(im,['STARS',"DON'T",'CRASH'],'CRASH' );return im

def compilation():
 im=background(21,(5,8,10));p=Image.open(OUT/'PIA06193.png').convert('RGB')
 p=p.crop((100,300,4000,1980))
 # Preserve cloud-band detail; no whole-plate blur/glow or repeated colour boosts.
 p=ImageEnhance.Color(p).enhance(1.15)
 p=p.resize((980,422),Image.Resampling.LANCZOS)
 # Key only the near-black plate sky into the house background; no rectangular slab.
 lum=np.asarray(p).max(axis=2).astype(float)
 alpha=Image.fromarray(np.clip((lum-5)/24*255,0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))
 im.paste(p,(275,255),alpha)
 # No optional vignette: Saturn remains the single hero.
 im=im.point(lambda v: round(28+227*v/255))
 # Naturally pale Saturn: grade to 105 mean HSV saturation, without clipping bands.
 base=im
 low,high=0.1,2.5
 for _ in range(16):
  factor=(low+high)/2
  im=ImageEnhance.Color(base).enhance(factor)
  if ImageStat.Stat(im.convert('HSV').getchannel('S')).mean[0]<105:low=factor
  else:high=factor
 pack.band(im,['FIVE','COSMIC','CLOCKS'],'CLOCKS');return im

rows=[]
for vid,fn,hook in [('REXYxuLOBoI',last_star,'10 TRILLION YEARS'),('ojk-dfOpAmw',andromeda,"STARS DON'T CRASH"),('m09jUdwC5hk',compilation,'FIVE COSMIC CLOCKS')]:
 im=fn();p=OUT/f'{vid}_B_v02.jpg';im.save(p,quality=94,subsampling=0,optimize=True);assert im.size==(1280,720) and p.stat().st_size<2000000
 rows.append({'video':vid,'file':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'hook':hook,'status':'worker build; Chief review required; no test armed'})
# Exact-size phone tiles, with live A beside each proposed B; larger pairs below.
sheet=Image.new('RGB',(1100,1050),'white');d=ImageDraw.Draw(sheet)
f=ImageFont.truetype(pack.FONT,18)
for i,row in enumerate(rows):
 y=20+i*340;d.text((20,y),row['video']+' — live A / proposed B v02',font=f,fill='black')
 for j,path in enumerate([OUT.parent/'live'/f"{row['video']}.jpg",Path(row['file'])]):
  im=Image.open(path).convert('RGB')
  sheet.paste(im.resize((168,94),Image.Resampling.LANCZOS),(20+j*550,y+35))
  sheet.paste(im.resize((352,198),Image.Resampling.LANCZOS),(20+j*550,y+135))
sheet.save(OUT/'PHONE_SHEET_v02.jpg',quality=95)
(OUT/'MANIFEST_v02.json').write_text(json.dumps({'job':'J1118','designs':rows,'source_notes':{'last_star':'Existing illustrated master t243; inset limb mask and compressed warm grade','andromeda':'NASA/JPL-Caltech PIA15416 existing plate; median reduction of pinpoints, full-width feathered sky','saturn':'NASA/JPL/Space Science Institute PIA06193; pale grade; no vignette','authority':'J1117 DECISION section 1 / Chief-added J1118; no Earth, no title changes'}},indent=2)+'\n')
print(json.dumps(rows,indent=2))
