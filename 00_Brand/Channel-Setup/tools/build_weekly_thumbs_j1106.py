#!/usr/bin/env python3
"""J1106 review drafts. House compositing only, no generation or YouTube writes.
Uses existing master/NASA plates; output remains outside git. Run with thumbs venv.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageEnhance,ImageFilter
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'00_Brand/Channel-Setup/tools'))
import build_packaging_long_thumbs_j0133 as pack
from build_back_catalogue_tc_variants_j0099 import disk,paste_disk
OUT=Path('/Users/benjaminoats/_desk/j1106/designs');OUT.mkdir(exist_ok=True)
SRC=Path('/Users/benjaminoats/_desk/thumb_packaging_1011/plates')
EARTH=Path('/Users/benjaminoats/_desk/j0152/as17-148-22727_orig.jpg')
W,H=1280,720

def background(seed,colour):
 rng=np.random.default_rng(seed);y,x=np.mgrid[0:H,0:W];g=np.exp(-((x-680)**2/700**2+(y-470)**2/450**2))
 a=np.zeros((H,W,3),float)
 for k,c in enumerate(colour):a[:,:,k]=[16,23,49][k]+g*c
 a+=rng.normal(0,1.2,(H,W,1));im=Image.fromarray(a.clip(0,255).astype('uint8'));d=ImageDraw.Draw(im)
 for _ in range(100):
  x,y=int(rng.integers(W)),int(rng.integers(170,H));v=int(rng.integers(65,150));d.ellipse((x,y,x+1,y+1),fill=(v,v,min(v+25,255)))
 return im

def earth(im,cx,cy,d):
 sq,m=disk(Image.open(EARTH).convert('RGB'));sq=ImageEnhance.Color(sq).enhance(1.5);paste_disk(im,sq,m,cx,cy,d)

def soft_rect(im,plate,box):
 x,y,w,h=box;fg=plate.resize((w,h),Image.Resampling.LANCZOS);m=Image.new('L',(w,h),0)
 ImageDraw.Draw(m).rectangle((24,24,w-24,h-24),fill=255);m=m.filter(ImageFilter.GaussianBlur(18));im.paste(fg,(x,y),m)

def stellar_disc(size):
 # Stay inside the actual stellar limb: the old crop included blue background.
 p=Image.open(SRC/'laststar_master_t243.png').convert('RGB').crop((400,125,868,593))
 p=ImageEnhance.Contrast(p).enhance(0.70)
 p=ImageEnhance.Color(p).enhance(1.15)
 p=p.resize((size,size),Image.Resampling.LANCZOS)
 m=Image.new('L',(size,size),0);ImageDraw.Draw(m).ellipse((4,4,size-5,size-5),fill=255)
 return p,m.filter(ImageFilter.GaussianBlur(2))

def last_star():
 im=background(5,(47,13,37));p,m=stellar_disc(490)
 im.paste(p,(450,180),m)
 im=pack.grade(im,120,False);pack.band(im,['RED','DWARF','END'],'END');return im

def andromeda():
 # Full-width plate, with its own blurred sky behind the title; no inset rectangle.
 p=Image.open(SRC/'andromeda_PIA15416.jpg').convert('RGB').crop((1000,1300,8500,6000))
 p=pack.grade(p,120,True)
 im=background(19,(9,26,53))
 fg=p.resize((W,535),Image.Resampling.LANCZOS)
 mask=np.ones((535,W),dtype=np.uint8)*255
 mask[:75,:]=np.linspace(0,255,75).astype('uint8')[:,None]
 im.paste(fg,(0,185),Image.fromarray(mask))
 im=pack.grade(im,115,True);pack.band(im,['MOST','STARS','MISS'],'MISS');return im

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
 # A separate endpoint vignette indicates the second story scale, not orbital geometry.
 star,mask=stellar_disc(175);im.paste(star,(65,205),mask)
 im=ImageEnhance.Color(im).enhance(1.15)
 # Lift deep shadows without a blur pass; retain the original band texture.
 im=im.point(lambda v: round(28+227*v/255))
 im=ImageEnhance.Color(im).enhance(1.35)
 pack.band(im,['FIVE','COSMIC','CLOCKS'],'CLOCKS');return im

rows=[]
for vid,fn,hook,title in [('REXYxuLOBoI',last_star,'RED DWARF END',"What Happens When the Universe's Last Star Dies?"),('ojk-dfOpAmw',andromeda,'MOST STARS MISS',"What Would Andromeda Look Like from Earth?"),('m09jUdwC5hk',compilation,'FIVE COSMIC CLOCKS','How Long Do Moons, Rings and Stars Last?')]:
 im=fn();p=OUT/f'{vid}_B_v02_worker.jpg';im.save(p,quality=94,subsampling=0,optimize=True);assert im.size==(1280,720) and p.stat().st_size<2000000
 rows.append({'video':vid,'file':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'hook':hook,'title_B_proposal':title,'status':'draft; no test armed; Chief and panel required'})
(OUT/'MANIFEST_v02_worker.json').write_text(json.dumps({'job':'J1106','designs':rows,'source_notes':{'last_star':'Existing film master frame t243, illustrative star','andromeda':'NASA/JPL-Caltech PIA15416 existing plate','saturn':'NASA/JPL/Space Science Institute PIA06193, https://svs.gsfc.nasa.gov/30348/','reference_rule':'Earth removed on unanimous panel advice. Main-character/scale-reference requirement remains unresolved; Chief decision required, no PASS claimed.'}},indent=2)+'\n')
print(json.dumps(rows,indent=2))
