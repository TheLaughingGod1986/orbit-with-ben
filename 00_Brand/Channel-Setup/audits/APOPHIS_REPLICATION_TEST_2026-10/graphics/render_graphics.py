#!/usr/bin/env python3
"""J1307: deterministic alpha graphics, no generation APIs. Pillow required.
PNG sequences are straight RGBA, 1080x1920, content inside y=656..1264.
Every duration is provisional; assembly must fit the measured VO.
"""
import argparse, hashlib, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
W,H=1080,1920
Y0,Y1=656,1264
WHITE=(245,248,255,255); YELLOW=(255,213,64,255); BLUE=(91,202,241,255)
FONT='/System/Library/Fonts/Supplemental/Arial Black.ttf'
CARDS={
 'ar1_date':['22 DEC 2032'],
 'ar1_odds':['4.3%\n(JUNE 2025)','→ 0%\n(WEBB, FEB 2026)'],
 'ar2_dates':['RETIRES 2030','DEORBIT BURN\n~2031','DECISION 2027'],
 'ar3_dates':['2 AUG 2027','258 KM PATH','LONGEST: 6M23S,\nEGYPT'],
}
NAMES=list(CARDS)+['ar1_size','ar1_miss','ar2_station','ar2_nemo','ar3_path','ar3_duration']

def ease(v):
 v=max(0.,min(1.,v)); return v*v*(3-2*v)

def label(im,text,y=720,opacity=1):
 # 96px Arial Black gives 69px capitals: 11.35% of the centre band.
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer);f=ImageFont.truetype(FONT,96)
 for i,line in enumerate(text.split('\n')):
  b=d.textbbox((0,0),line,font=f); width=b[2]-b[0]
  if width>980: raise ValueError('Label too wide: '+line)
  d.text(((W-width)/2,y+i*100-b[1]),line,font=f,fill=WHITE,stroke_width=4,stroke_fill=(12,24,42,255))
 layer.putalpha(layer.getchannel('A').point(lambda a:round(a*opacity)))
 im.alpha_composite(layer)

def ruler(d,x0,x1,y):
 d.line((x0,y,x1,y),fill=YELLOW,width=5)
 for x in [x0,x1]:d.line((x,y-13,x,y+13),fill=YELLOW,width=5)

def map_base(bounds):
 # Geographic data only: our own equirectangular render, no sourced map image.
 lo,hi,bot,top=bounds
 def xy(lon,lat):return ((lon-lo)/(hi-lo)*W,Y0+(top-lat)/(top-bot)*(Y1-Y0))
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 for y in range(Y0,Y1):
  k=(y-Y0)/(Y1-Y0);d.line((0,y,W,y),fill=(22+int(7*k),68+int(11*k),98+int(15*k),255))
 land=Image.new('RGBA',(W,H));dl=ImageDraw.Draw(land)
 for f in json.loads((HERE/'countries.json').read_text())['features']:
  g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
  for poly in polys:
   ring=poly[0]
   # Shift entire rings, not individual vertices, to avoid a dateline seam.
   for shift in [-360,0,360]:
    pts=[xy(lon+shift,lat) for lon,lat in ring]
    if max(x for x,y in pts)<0 or min(x for x,y in pts)>W:continue
    dl.polygon(pts,fill=(99,135,128,255),outline=(152,178,156,255))
 # Clip drawn geography to exact centre band.
 im.alpha_composite(land.crop((0,Y0,W,Y1)),(0,Y0))
 return im,xy

def moon_disc(path,size):
 im=Image.open(path).convert('RGB')
 # This NASA file is a full Moon on black; crop detected luminous disc.
 import numpy as np
 a=np.asarray(im); mask=a.max(axis=2)>38
 yy,xx=np.where(mask)
 im=im.crop((int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1))).resize((size,size),Image.Resampling.LANCZOS).convert('RGBA')
 m=Image.new('L',(size,size));ImageDraw.Draw(m).ellipse((1,1,size-2,size-2),fill=255);im.putalpha(m)
 return im

class Renderer:
 def __init__(self,moon):
  self.moon=moon_disc(moon,60)
  self.eclipse,self.exy=map_base((-48,45,12,55))
  self.pacific,self.pxy=map_base((-205,-65,-72,7))
  self.data=json.loads((HERE/'eclipse_path.json').read_text())
 def frame(self,name,t,duration):
  q=t/duration; im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
  if name in CARDS:
   cards=CARDS[name];pos=min(len(cards)-1,int(q*len(cards)));local=q*len(cards)-pos
   opacity=min(ease(local/.18),ease((1-local)/.18))
   label(im,cards[pos],910,opacity)
  elif name=='ar1_size':
   # 60m rock width and 60m illustrative 15x4m building height: analogy only.
   p=ease(q/.55);cx,cy=325,1030;r=150*p
   pts=[(cx+r*(1+.09*math.sin(i*2.1))*math.cos(i*math.pi/10),cy+r*(1+.09*math.sin(i*2.1))*math.sin(i*math.pi/10)) for i in range(20)]
   # Normalize silhouette to exactly 300px width at full reveal.
   if p>0:
    left=min(x for x,y in pts);right=max(x for x,y in pts)
    pts=[(cx+(x-(left+right)/2)*300*p/(right-left),y) for x,y in pts]
    d.polygon(pts,fill=(111,127,145),outline=WHITE)
   bottom=1180;top=bottom-300*p
   d.rectangle((710,top,850,bottom),fill=(47,80,111),outline=WHITE,width=4)
   for i in range(1,15):
    y=bottom-i*20*p;d.line((712,y,848,y),fill=BLUE,width=2)
   ruler(d,175,475,1210)
   label(im,'60 M' if q<.48 else '15-STOREY\nBUILDING',685)
  elif name=='ar1_miss':
   # One common isotropic scale: Moon r=30px; altitude=366.1485px.
   cx,cy,r=540,1190,30; scale=r/1737;alt=21200*scale
   im.alpha_composite(self.moon,(cx-r,cy-r))
   # Explanatory flyby arc, not an ephemeris/orbit; minimum is at x=cx.
   p=ease(q/.72);pts=[]
   for i in range(max(2,int(181*p))):
    x=90+i*5;y=cy-r-alt-.00029*(x-cx)**2;pts.append((x,y))
   d.line(pts,fill=YELLOW,width=5)
   x,y=pts[-1];d.ellipse((x-5,y-5,x+5,y+5),fill=WHITE)
   if q>.35:
    d.line((cx,cy-r,cx,cy-r-alt),fill=BLUE,width=3)
    for y in [cy-r,cy-r-alt]:d.line((cx-12,y,cx+12,y),fill=BLUE,width=4)
   label(im,'21,200 KM',925)
  elif name=='ar2_station':
   p=ease(q/.6);left,right=110,970;y=1030
   # Schematic ISS silhouette, exact overall 109m bracket; not a NASA 3D model.
   d.line((left,y,left+(right-left)*p,y),fill=WHITE,width=12)
   for x in [130,330,650,850]:
    for yy in [895,1060]:
     if x<left+(right-left)*p:
      d.rectangle((x,yy,x+100,yy+95),fill=(36,89,138),outline=BLUE,width=3)
      for j in range(1,5):d.line((x+j*20,yy,x+j*20,yy+95),fill=(114,161,193),width=1)
   d.rounded_rectangle((490,970,590,1115),radius=15,fill=(198,212,223),outline=WHITE,width=3)
   ruler(d,left,right,1225)
   label(im,'109 M' if q<.48 else '(FOOTBALL\nFIELD)',680)
  elif name=='ar2_nemo':
   im=self.pacific.copy();d=ImageDraw.Draw(im)
   x,y=self.pxy(-123-24/60,-48-53/60)
   r=18+10*math.sin(q*math.pi*4)**2
   d.ellipse((x-r,y-r,x+r,y+r),outline=YELLOW,width=4)
   d.ellipse((x-5,y-5,x+5,y+5),fill=YELLOW)
   label(im,'EMPTY SOUTH\nPACIFIC',690)
  elif name=='ar3_path':
   im=self.eclipse.copy();d=ImageDraw.Draw(im)
   rows=[r for r in self.data['rows'] if r['centre'][0]<44]
   count=max(2,int(len(rows)*ease(q/.85)));active=rows[:count]
   north=[self.exy(*r['north']) for r in active];south=[self.exy(*r['south']) for r in active]
   d.polygon(north+south[::-1],fill=(17,28,57,255))
   d.line(north,fill=BLUE,width=2);d.line(south,fill=BLUE,width=2)
   d.line([self.exy(*r['centre']) for r in active],fill=YELLOW,width=3)
   countries=['SPAIN','MOROCCO','ALGERIA','TUNISIA','LIBYA','EGYPT']
   ci=min(5,int(q*6))
   label(im,countries[ci],690)
   locations=[(-4,40),(-6,32),(3,28),(9,34),(17,27),(30,27)]
   mx,my=self.exy(*locations[ci])
   d.ellipse((mx-6,my-6,mx+6,my+6),outline=WHITE,width=2)
   x,y=self.exy(*self.data['greatest_duration'])
   if q>.78:
    d.ellipse((x-9,y-9,x+9,y+9),fill=YELLOW,outline=WHITE,width=2)
    # Marker has no extra simultaneous label; metadata identifies greatest duration.
  elif name=='ar3_duration':
   # Both bars have a common zero and scale: 383/138 = 2.77536.
   p=ease(q/.75)
   d.rounded_rectangle((100,985,100+880*138/383*p,1035),radius=10,fill=BLUE)
   d.rounded_rectangle((100,1120,100+880*p,1170),radius=10,fill=YELLOW)
   d.line((100,955,100,1200),fill=WHITE,width=3)
   label(im,'2026 ECLIPSE:\n2M 18S' if q<.48 else '2027 EGYPT:\n6M 23S',700)
  # Smooth in/out; no empty-black slab, alpha composited over moving picture.
  fade=min(ease(t/.35),ease((duration-t)/.35))
  im.putalpha(im.getchannel('A').point(lambda a:round(a*fade)))
  box=im.getchannel('A').getbbox()
  assert box is None or (box[1]>=Y0 and box[3]<=Y1),(name,box)
  return im

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--out',type=Path,required=True);p.add_argument('--moon',type=Path,required=True)
 p.add_argument('--duration',type=float,default=3.6);p.add_argument('--fps',type=int,default=30)
 p.add_argument('--only',choices=NAMES);p.add_argument('--stills-only',action='store_true')
 a=p.parse_args()
 if a.duration<1 or a.fps<1: p.error('duration >=1 and fps >=1 required')
 a.out.mkdir(parents=True,exist_ok=True);r=Renderer(a.moon);manifest=[]
 for name in [a.only] if a.only else NAMES:
  stem='code_graphic_'+name+'_v02';dest=a.out/stem;dest.mkdir(exist_ok=True)
  if not a.stills_only:
   if any(dest.glob('frame_*.png')):raise RuntimeError('Refusing to overwrite a sequence: '+str(dest))
   for i in range(round(a.duration*a.fps)):
    r.frame(name,i/a.fps,a.duration).save(dest/f'frame_{i:05}.png',compress_level=1)
  samples=[]
  for j,q in enumerate([.2,.6,.85]):
   path=dest/f'preview_{j}.png';r.frame(name,a.duration*q,a.duration).save(path)
   samples.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
  manifest.append({'name':name,'sequence':str(dest/'frame_%05d.png'),'frames':round(a.duration*a.fps),'fps':a.fps,'duration':a.duration,'previews':samples})
  print(name,flush=True)
 meta={'job':'J1307','size':[W,H],'alpha':'straight RGBA','centre_band':[Y0,Y1], 'provisional_timing':True,'moon':{'path':str(a.moon),'sha256':hashlib.sha256(a.moon.read_bytes()).hexdigest()},'items':manifest}
 (a.out/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
if __name__=='__main__':main()
