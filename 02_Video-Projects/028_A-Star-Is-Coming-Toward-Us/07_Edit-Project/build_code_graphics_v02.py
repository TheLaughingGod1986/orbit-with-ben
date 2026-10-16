#!/usr/bin/env python3
"""J0338: per-board, silent 1080p teaching graphics. No network or generation APIs.

Use --out /path/to/028/07_Edit-Project/code_graphics_v02 --previews first.
Assets: assets/sun_sdo.jpg (GSFC_20171208_Archive_e000790), assets/earth.jpg
(NASA Blue Marble). Sources and exact VO spans are in CODE_GRAPHICS_v02.md.
Streams RGB into ffmpeg: no PNG frame scratch, no repeated source animation.
"""
import argparse
import hashlib
import json
import math
import subprocess
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

W,H,FPS=1920,1080,50  # All board boundaries are exact at 50 fps (0.02 s).
GOLD=(255,201,74); WHITE=(244,239,230); ICE=(169,216,255); ORANGE=(255,154,60)
HERE=Path(__file__).resolve().parent
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'

# Each label <=4 words, timed locally against the locked Scribe transcript.
# Number reveal only once spoken; 0.4 s in/out, <=3.2 s stationary.
LABELS={
 'r04_shower_shell':[(0.9,4.0,'1.3 million years'),(8,11.8,'Outer edge')],
 'r05_drift_path_sky':[(2.8,5.4,'Our night sky')],
 'r07_kdwarf':[(0.1,3.2,'60% Sun’s mass')],
 'r09_drift':[(4,7.8,'Drift slowly sideways'),(10,13.8,'Hardly drifts')],
 'r14_hipparcos_card':[(0.15,1.55,'Late 1990s'),(1.85,5.3,'Hipparcos'),(8.0,11.7,'About 1 light-year')],
 'r15_16_path':[(0.2,4,'Sharper focus'),(5,8.8,'Coming closer'),(9.1,12.9,'1/5 light-year')],
 'r17_scale_a':[(2.7,5.95,'Sun–Earth: 1 cm')],
 'r17_scale_b':[(0.1,3.9,'Length of a ruler')],
 'r18_shell':[(0.2,4,'Far beyond planets'),(4.3,7.9,'100 metres')],
 'r20_21_oort_shell':[(0.15,2.3,'Beyond the planets'),(2.75,5.4,'Cloud of ice'),(5.85,9.2,'Trillions of frozen bodies'),(14.4,18.2,'Oort Cloud'),(18.5,22.3,'Never seen directly')],
 'r24_25_shower':[(2.8,6.6,'Through the Oort Cloud'),(10.5,14.3,'Gravity nudges comets'),(16,19.8,'Flung out'),(19.9,23.5,'Towards the Sun')],
 'r27_shower':[(2,5.8,'Not while passing'),(6.3,10.1,'So far out')],
 'r28_hale_bopp_2':[(0.5,4.3,'More comets')],
 'r29_sky':[(1.5,5.3,'Brightest star')],
 'r31_sky':[(0.3,4.1,'Creep across the sky')],
 'r31_sky_fade':[(0.1,3.9,'Fade and drift away')],
 'r33_traffic':[(0.2,4,'Outer Oort Cloud'),(4.3,8.1,'Too small and faint')],
 'r34_traffic':[(4.05,6.05,'Cannot yet pin down'),(6.55,9.7,'How close?')],
 'r37_shell':[(0.3,4.1,'Sister stars')],
}

def ease(x):
 return (1-math.cos(math.pi*max(0,min(1,x))))/2

@lru_cache(None)
def font(n): return ImageFont.truetype(FONT,n)

def text(im,s,xy,size=66,color=WHITE,alpha=1,anchor='mm'):
 layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer)
 box=d.textbbox(xy,s,font=font(size),anchor=anchor,stroke_width=2)
 if not (95<=box[0] and box[2]<=1825 and 54<=box[1] and box[3]<=1026):
  raise ValueError(f'Unsafe text {s}: {box}')
 d.text(xy,s,font=font(size),fill=(*color,int(255*alpha)),anchor=anchor,stroke_width=2,stroke_fill=(12,23,39,int(210*alpha)))
 im.paste(layer,(0,0),layer)

class Renderer:
 def __init__(self,assets):
  self.sun=Image.open(assets/'sun_sdo.jpg').convert('RGB').crop((140,15,1560,1435))
  self.earth=Image.open(assets/'earth.jpg').convert('RGB')
  self.rng=np.random.default_rng(710)
  self.stars=self.rng.uniform([100,190],[1820,910],(90,2))
  # Spherical shell, projected in perspective. Ice points encode Oort geometry.
  v=self.rng.normal(size=(420,3));v/=np.linalg.norm(v,axis=1)[:,None]
  self.cloud=v*self.rng.uniform(.72,1,(420,1))
  y,x=np.mgrid[:H,:W];rad=np.sqrt(((x-960)/840)**2+((y-540)/540)**2)
  g1=np.exp(-rad**2*1.4)
  band_d=((x-960)*.42+(y-540)*.91)/340.0
  band_l=((x-960)*.91-(y-540)*.42)/780.0
  mw=np.exp(-band_d**2)*np.exp(-band_l**2*.7)
  dust=np.exp(-((band_d-.18)/.32)**2)*np.exp(-band_l**2*1.1)
  g2=np.exp(-(((x-520)/400)**2+((y-340)/280)**2))
  g3=np.exp(-(((x-1400)/420)**2+((y-720)/300)**2))
  glow=np.clip(.68*g1+.45*mw-.22*dust+.32*g2+.28*g3,0,1.35)
  base=np.stack([14+64*glow,22+84*glow,36+112*glow],axis=-1)
  bg=Image.fromarray(np.uint8(np.clip(base,0,255)))
  layer=Image.new('RGBA',(W,H),(0,0,0,0));ld=ImageDraw.Draw(layer)
  for cr in (220,350,480,620,760,900):
   ld.ellipse((960-cr,540-int(cr*.62),960+cr,540+int(cr*.62)),outline=(165,195,230,88),width=2)
   for deg in range(0,360,3):
    ang=math.radians(deg);r1=cr-(10 if deg%12==0 else 6);r2=cr+(10 if deg%12==0 else 6)
    ld.line((960+r1*math.cos(ang),540+r1*.62*math.sin(ang),960+r2*math.cos(ang),540+r2*.62*math.sin(ang)),fill=(185,212,242,115),width=2)
  srng=np.random.default_rng(7100)
  for n_stars,r_px,alpha in [(420,2.2,130),(190,3.2,155),(55,4.5,175)]:
   for sx,sy in srng.uniform([70,100],[1850,980],(n_stars,2)):
    ld.ellipse((sx-r_px,sy-r_px,sx+r_px,sy+r_px),fill=(215,232,252,alpha))
  self.background=Image.alpha_composite(bg.convert('RGBA'),layer).convert('RGB')
  self.bodies={}

 def body(self,im,xy,r,kind='sun',tint=False):
  r=max(3,int(r));key=(r,kind,tint)
  if key not in self.bodies:
   src=self.earth if kind=='earth' else self.sun
   body=ImageOps.fit(src,(2*r,2*r),method=Image.Resampling.LANCZOS)
   if kind!='earth':
    grey=ImageOps.grayscale(body)
    body=ImageOps.colorize(grey,(80,29,12) if tint else (99,61,17),ORANGE if tint else (255,237,168))
   mask=Image.new('L',(2*r,2*r));ImageDraw.Draw(mask).ellipse((1,1,2*r-2,2*r-2),fill=255)
   body.putalpha(mask);self.bodies[key]=body
  im.paste(self.bodies[key],(int(xy[0]-r),int(xy[1]-r)),self.bodies[key])

 def base(self,t,grid=True):
  im=self.background.copy();d=ImageDraw.Draw(im)
  if grid:
   shift=int(t*4)%100
   for x in range(-100,2020,100):d.line((x+shift,170,x+shift,920),fill=(42,59,82),width=1)
   for y in range(190,921,100):d.line((96,y,1824,y),fill=(42,59,82),width=1)
  for k,(x,y) in enumerate(self.stars):
   x=96+(x-96+t*(1+k%3))%1728
   d.ellipse((x,y,x+2,y+2),fill=(109,133,160))
  return im

 def cloud_draw(self,im,t,scale=1,cx=960,cy=550):
  a=t*.045;v=self.cloud.copy();x=v[:,0]*math.cos(a)-v[:,2]*math.sin(a);z=v[:,0]*math.sin(a)+v[:,2]*math.cos(a)
  d=ImageDraw.Draw(im)
  for xx,yy,zz in zip(x,v[:,1],z):
   px=cx+xx*580*scale;py=cy+yy*280*scale;rr=1.7+(zz+1)*1.4
   if 100<px<1820 and 190<py<900:
    c=tuple(int(n*(.45+.25*(zz+1))) for n in ICE);d.ellipse((px-rr,py-rr,px+rr,py+rr),fill=c)
  self.body(im,(cx,cy),max(14,36*scale))

 def frame(self,p,t):
  ident=p['id'];dur=p['use_s'];u=min(1,t/dur);asset=p['asset_id']
  im=self.base(t,asset not in ('sky','comet_tail','subscribe_card'));d=ImageDraw.Draw(im)
  if asset=='kdwarf_vs_sun':
   self.body(im,(560,480),174);self.body(im,(1340,480),135,tint=True)
   text(im,'Sun',(560,250),52);text(im,'Gliese 710',(1340,250),52,GOLD)
   # Radius is illustrative, mass is encoded separately as a calibrated bar.
   f=ease(t/.7)
   d.rounded_rectangle((360,725,760,765),radius=12,fill=(68,83,103))
   d.rounded_rectangle((1140,725,1540,765),radius=12,fill=(68,83,103))
   d.rounded_rectangle((360,725,360+max(1,400*f),765),radius=12,fill=WHITE)
   d.rounded_rectangle((1140,725,1140+max(1,240*f),765),radius=12,fill=GOLD)
   text(im,'Mass',(960,745),42)
  elif asset in ('drift','drift_path_sky'):
   # Deliberately schematic star motions, not a claimed real star chart.
   for k,(x,y) in enumerate(self.stars[::3]):
    xx=140+(x-140+t*(13+k%7))%1640;yy=y
    d.line((xx-45,yy,xx,yy),fill=(105,149,185),width=2)
    d.ellipse((xx-3,yy-3,xx+3,yy+3),fill=WHITE)
   cx=1000;cy=550
   self.body(im,(cx,cy),24+u*16,tint=True)
   d.arc((cx-90,cy-90,cx+90,cy+90),int(t*8),int(t*8)+280,fill=GOLD,width=2)
   if asset=='drift_path_sky':
    d.line([(cx,cy),(cx+180*ease(u),cy+90*ease(u))],fill=GOLD,width=3)
  elif asset in ('path','hipparcos_card'):
   sx,sy=440,700;self.body(im,(sx,sy),66)
   end=.2 if asset=='path' else 1
   f=ease(u) if asset=='path' else .1*ease(u)
   distance=1-(1-end)*f;yy=sy-365*distance;wide=90*(1-f)+16*f
   d.ellipse((sx-365,sy-365,sx+365,sy+365),outline=(79,113,146),width=2)
   layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer)
   ld.polygon([(290,yy-wide),(1740,yy-wide),(1740,yy+wide),(290,yy+wide)],fill=(*ORANGE,43))
   im.paste(layer,(0,0),layer);d=ImageDraw.Draw(im)
   d.line((290,yy,1740,yy),fill=GOLD,width=4)
   self.body(im,(1600-200*u,yy),36,tint=True)
   d.line((sx+85,sy,sx+85,yy),fill=ICE,width=3)
   for y in [sy,yy]:d.line((sx+73,y,sx+97,y),fill=ICE,width=3)
   text(im,'Sun',(440,810),48)
  elif asset=='scale':
   # Physical model units; no flat discs. First span teaches the 1-cm premise.
   if ident.endswith('_a'):
    self.body(im,(430,500),92);self.body(im,(1420,500),66,'earth')
    end=430+990*ease(u*2);d.line((430,700,end,700),fill=GOLD,width=6)
    for xx in (430,end):d.line((xx,680,xx,720),fill=GOLD,width=4)
    text(im,'Sun',(430,340),50);text(im,'Earth',(1420,340),50)
   else:
    self.body(im,(290,540),50)
    # 30 cm ruler morphs into a long model distance; board cuts before '100 metres'.
    end=600+1000*ease(u);d.line((290,650,end,650),fill=GOLD,width=5)
    for xx in np.linspace(290,end,31):d.line((xx,650,xx,670),fill=ICE,width=2)
    self.body(im,(end,540),40,tint=True)
    text(im,'Gliese 710',(min(end,1580),425),48,GOLD)
  elif asset in ('shell','oort_shell','shower_shell','shower','traffic','subscribe_card'):
   scale=1
   if ident=='r18_shell':
    # Planetary orbits only: withhold the shell until the following chapter.
    self.body(im,(960,550),48)
    for n,rr in enumerate((130,220,340,460)):
     d.ellipse((960-rr,550-rr*.52,960+rr,550+rr*.52),outline=(92,132,163),width=2)
    a=t*.16;self.body(im,(960+220*math.cos(a),550+114*math.sin(a)),25,'earth')
   else:
    if asset=='oort_shell':scale=1.2-.3*ease(u)
    if ident=='r37_shell':scale=.9+.1*u
    self.cloud_draw(im,t,scale)
   if asset in ('shower_shell','shower'):
    late=ident=='r27_shower'
    sx=1450+200*u if late else 230+1460*ease(u)
    self.body(im,(sx,360),33,tint=True)
    d=ImageDraw.Draw(im)
    d.line((180,360,1740,360),fill=(129,102,69),width=2)
    fall=ease((u-.45)/.55) if not late else .3+.55*u
    # Bezier comet orbits: displaced only after stellar passage; no collisions.
    for k in range(9):
     start=np.array([650+k*70,350+25*math.sin(k)])
     control=np.array([1700-75*k,650+18*k]);end=np.array([1070+15*k,650])
     ts=np.linspace(0,fall,35);pts=[tuple((1-v)**2*start+2*(1-v)*v*control+v*v*end) for v in ts]
     if fall>0:d.line(pts,fill=ICE,width=2)
     x,y=pts[-1];d.ellipse((x-4,y-4,x+4,y+4),fill=WHITE)
    # A few outward trajectories, only in the explicit outward/inward beat.
    if ident=='r24_25_shower' and u>.65:
     for k in range(3):
      x=1260+k*65;y=390-(u-.65)*450
      d.line((1260+k*65,390,x,y),fill=GOLD,width=3)
      d.ellipse((x-4,y-4,x+4,y+4),fill=GOLD)
   if asset=='traffic' or ident=='r37_shell':
    if ident=='r33_traffic':
     x=270+1250*u;self.body(im,(x,340),18,tint=True);self.body(im,(x+43,352),9,tint=True)
    elif ident=='r34_traffic':
     layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer)
     ld.polygon([(190,260),(1730,400),(1730,630),(190,390)],fill=(*ORANGE,38));im.paste(layer,(0,0),layer)
     self.body(im,(300+1300*u,400),27,tint=True)
    else:
     for k in range(3):self.body(im,(350+k*570+35*math.sin(t*.3+k),330+65*k),24,tint=True)
   if asset=='subscribe_card':
    a=min(ease((t-.3)/.4),ease((4.3-t)/.4))
    if a>0:text(im,'Subscribe',(1500,865-int(18*(1-a))),58,GOLD,a)
  elif asset=='comet_tail':
   x=1150-130*u;y=560+20*math.sin(t*.4)
   # Tapered tail follows an animated nucleus; an illustration, not an observation.
   layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer)
   for k in range(15,0,-1):
    spread=k*4;ld.polygon([(x,y),(1650,400-spread),(1740,500+spread)],fill=(*ICE,7))
   im.paste(layer,(0,0),layer);d=ImageDraw.Draw(im)
   for k in range(24):
    v=k/24;xx=x+600*v;yy=y-110*v+12*math.sin(t+v*4)
    d.ellipse((xx-2,yy-2,xx+2,yy+2),fill=tuple(int(c*(1-v*.7)) for c in ICE))
   d.ellipse((x-10,y-10,x+10,y+10),fill=WHITE)
  elif asset=='sky':
   fade=ident.endswith('fade');tight=ident=='r31_sky'
   x=1150+(60*u if tight or fade else 0);y=530-20*u
   r=(18-12*u) if fade else (10+20*u if not tight else 28)
   self.body(im,(x,y),r,tint=True)
   # Stars remain unresolved points; apparent discs are illustrative emphasis.
   d=ImageDraw.Draw(im);d.ellipse((585,580,599,594),fill=WHITE)
   if tight:d.line((1100,580,1100+160*u,580),fill=GOLD,width=2)
  else:raise ValueError(asset)
  for start,end,label in LABELS.get(ident,[]):
   if start<=t<=end:
    alpha=min(ease((t-start)/.4),ease((end-t)/.4))
    text(im,label,(960,125+int(14*(1-alpha))),66,GOLD,alpha)
  credit='NASA/SDO · CGI' if asset!='scale' else 'NASA · CGI'
  text(im,credit,(100,986),28,ICE,anchor='lm')
  text(im,'Illustration · not to scale',(1818,986),28,ICE,anchor='rm')
  return im

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--previews',action='store_true');ap.add_argument('--only');a=ap.parse_args()
 boards=HERE/'PLATE_BOARDS_v02.json';plates=[p for p in json.loads(boards.read_text())['plates'] if p['route'] in ('code','card')]
 if a.only:plates=[p for p in plates if p['id']==a.only]
 a.out.mkdir(parents=True,exist_ok=True);r=Renderer(a.out/'assets');records=[];thumbs=[]
 for p in plates:
  ident=p['id'];stem='code_graphic_028_'+ident+'_v02';frames=round(p['use_s']*FPS)
  assert abs(frames/FPS-p['use_s'])<1e-6
  for frac in (.18,.52,.82):
   preview=r.frame(p,p['use_s']*frac);preview.save(a.out/f'{stem}_{int(frac*100):02}.jpg',quality=94)
   thumbs.append((p,frac,preview.resize((480,270))))
  if not a.previews:
   dest=a.out/f'{stem}.mp4';tmp=a.out/f'{stem}.partial.mp4'
   cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-movflags','+faststart',str(tmp)]
   proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
   try:
    for i in range(frames):proc.stdin.write(r.frame(p,i/FPS).tobytes())
    proc.stdin.close()
    if proc.wait()!=0:raise RuntimeError(f'ffmpeg failed: {ident}')
   except BaseException:
    proc.kill();proc.wait();raise
   tmp.replace(dest)
   probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]))
   v=probe['streams'][0]
   assert (v['width'],v['height'])==(W,H)
   assert abs(float(probe['format']['duration'])-p['use_s'])<.011
   assert int(v['nb_frames'])==frames
   records.append(dict(id=ident,file=str(dest),sha256=digest(dest),t_in_s=p['t_in_s'],t_out_s=p['t_out_s'],use_s=p['use_s'],frames=frames,fps=FPS,width=W,height=H,kind='chart',source='own_code',review='pending Chief'))
   (a.out/'RENDER_MANIFEST.partial.json').write_text(json.dumps(records,indent=2)+'\n')
   print(f'{ident}: {frames} frames / {p["use_s"]}s verified',flush=True)
  r.bodies.clear()
 sheet=Image.new('RGB',(1440,len(plates)*310),(25,37,55));d=ImageDraw.Draw(sheet)
 for i,(p,frac,thumb) in enumerate(thumbs):
  x=i%3*480;y=i//3*310;sheet.paste(thumb,(x,y));d.text((x+8,y+275),f'{p["id"]}  {frac:.0%}  {p["t_in_s"]:.2f}s',font=font(19),fill=WHITE)
 sheet.save(a.out/'CONTACT_SHEET.jpg',quality=92)
 if not a.previews:
  manifest=dict(job='J0338',board_sha256=digest(boards),renderer_sha256=digest(Path(__file__)),assets={p.name:digest(p) for p in (a.out/'assets').glob('*.jpg')},review='pending Chief',renders=records)
  (a.out/'RENDER_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Wrote contact sheet; Chief review remains required.',flush=True)
if __name__=='__main__':main()
