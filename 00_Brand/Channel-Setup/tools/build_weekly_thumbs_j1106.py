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

def last_star():
 im=background(5,(47,13,37));p=Image.open(SRC/'laststar_master_t243.png').convert('RGB')
 # Whole stellar disc from the film's own frame; it is concept art, not a new NASA claim.
 p=p.crop((375,103,893,622));m=Image.new('L',p.size,0);ImageDraw.Draw(m).ellipse((3,3,515,515),fill=255)
 p=ImageEnhance.Color(p).enhance(1.5);im.paste(p.resize((470,470)),(570,180),m.resize((470,470)).filter(ImageFilter.GaussianBlur(1)))
 # Earth is a foreground story reference, not a dimensional ratio or a claim it survives until then.
 earth(im,225,530,140)
 im=pack.grade(im,125,False);pack.band(im,['RED','DWARFS','WIN'],'WIN');return im

def andromeda():
 im=background(19,(9,26,53));p=Image.open(SRC/'andromeda_PIA15416.jpg').convert('RGB').crop((1000,1300,8500,6000))
 p=pack.grade(p,135,True);soft_rect(im,p,(225,165,1020,525));earth(im,140,575,125)
 im=pack.grade(im,125,False);pack.band(im,['STARS','MISS','STARS'],'MISS');return im

def compilation():
 im=background(21,(0,0,0));im=Image.fromarray((np.asarray(im).astype('uint16')+np.array([4,5,7])).clip(0,255).astype('uint8'));p=Image.open(OUT/'PIA06193.png').convert('RGB')
 # Preserve the complete natural shadow geometry; feather the plate sky, not the rings.
 p=p.crop((100,300,4000,1980));p=pack.grade(p,120,True)
 soft_rect(im,p,(55,165,1170,504))
 earth(im,180,635,52)
 im=pack.grade(im,120,True);pack.band(im,['SATURN','TO','STARLIGHT'],'STARLIGHT');return im

rows=[]
for vid,fn,hook,title in [('REXYxuLOBoI',last_star,'RED DWARFS WIN','Why Will Red Dwarfs Be the Last Stars?'),('ojk-dfOpAmw',andromeda,'STARS MISS STARS',"Why Do Stars Usually Miss When Galaxies Collide?"),('m09jUdwC5hk',compilation,'SATURN TO STARLIGHT','How Long Do Moons, Rings and Stars Last?')]:
 im=fn();p=OUT/f'{vid}_B_v01.jpg';im.save(p,quality=94,subsampling=0,optimize=True);assert im.size==(1280,720) and p.stat().st_size<2000000
 rows.append({'video':vid,'file':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'hook':hook,'title_B_proposal':title,'status':'draft; no test armed; Chief and panel required'})
(OUT/'MANIFEST.json').write_text(json.dumps({'job':'J1106','designs':rows,'source_notes':{'last_star':'Existing film master frame t243, illustrative star','andromeda':'NASA/JPL-Caltech PIA15416 existing plate','saturn':'NASA/JPL/Space Science Institute PIA06193, https://svs.gsfc.nasa.gov/30348/','earth':'NASA Apollo 17 as17-148-22727 existing plate; foreground story reference, not orbital geometry'}},indent=2)+'\n')
print(json.dumps(rows,indent=2))
