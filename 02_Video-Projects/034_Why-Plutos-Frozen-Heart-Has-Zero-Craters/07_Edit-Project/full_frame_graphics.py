#!/usr/bin/env python3
"""J2371 source-backed full-frame CODE builders (all 8 rows: R02, R15, R24, R29, R35, R48, R56, R69).
No downloads; never overwrites existing assets. £0 spend.
"""
import argparse,csv,json,math,subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw,ImageEnhance,ImageChops
from code_graphics import W,H,FPS,HERE,GOLD,WHITE,BLUE,canvas,text,arrow,ease,sha

PHASES={
 'R02':[(0,5.15,['1,000 KM WIDE']),(5.15,10.44,['> TEXAS + OKLAHOMA','0 CRATERS'])],
 'R15':[(0,5.65,['2,377 KM DIAMETER']),(5.65,11.35,['1/5 EARTH WIDTH',"2/3 EARTH'S MOON"]),(11.35,14.62,['HALF U.S. WIDTH','2,377 KM DIAMETER'])],
 'R24':[(0,3.47,['CHARON: 1,214 KM','1,214 KM ACROSS']),(3.47,6.94,["HALF PLUTO'S SIZE",'CHARON: 1,214 KM'])],
 'R29':[(0,5.14,['153 HOURS (6.4 DAYS)']),(5.14,10.20,['153 HOURS'])],
 'R35':[(0,5.26,['58,536 KM/H','(36,400 MPH)']),(5.26,10.53,['FASTEST EARTH LAUNCH','+14,000 KM/H BOOST'])],
 'R48':[(0,4.51,['1,000 KM (600 MI)','> TEXAS + OKLAHOMA']),(4.51,9.03,['LARGEST KNOWN GLACIER','1,000 KM (600 MI)'])],
 'R56':[(0,4.18,['0 °C FREEZING POINT','−226 TO −240 °C']),(4.18,8.38,['200 °C BELOW FREEZING']),(8.38,12.50,['WATER-ICE BEDROCK'])],
 'R69':[(0,5.87,['1 OCTOBER 2024','300M MILES/YR']),(5.87,11.76,['60 AU FROM SUN','300M MILES/YR'])],
}
SOURCES={
 'R02':['PIA20007.jpg','PIA18033.jpg'],
 'R15':['PIA20534.jpg','PIA18033.jpg','PIA00405.jpg'],
 'R24':['PIA19968.jpg','PIA00405.jpg'],
 'R29':['PIA19966.jpg'],
 'R35':['File_New_Horizons_1.jpg.jpg'],
 'R48':['PIA14458.jpg'],
 'R56':['PIA19957.jpg'],
 'R69':['PIA20362.jpg','File_Reworked_composite_image_of_Arrokoth_rotated.png.png'],
}
# USGS-derived outer perimeter (lon, lat) for Texas + Oklahoma combined & Red River divider
TX_OK_OUTER=[
 (-103.00,37.00),(-100.00,37.00),(-94.62,37.00),(-94.43,35.48),(-94.48,33.64),
 (-94.04,33.55),(-94.04,31.99),(-93.51,31.03),(-93.84,29.77),(-94.74,29.35),
 (-96.40,28.40),(-97.15,27.80),(-97.14,25.96),(-99.10,26.43),(-99.52,27.50),
 (-100.32,28.65),(-101.40,29.77),(-102.32,29.77),(-103.14,28.98),(-104.55,29.56),
 (-106.64,31.78),(-106.62,32.00),(-103.06,32.00),(-103.04,36.50),(-103.00,37.00)
]
TX_OK_RED_RIVER=[
 (-103.04,36.50),(-100.00,36.50),(-100.00,34.56),(-99.18,34.11),(-98.08,33.90),
 (-96.60,33.84),(-95.50,33.88),(-94.48,33.64)
]

def project_tx_ok(pts,cx,cy,scale):
 # Equirectangular cos(31.5 deg) aspect-corrected projection centered at (-100.0, 31.5)
 cos_lat=math.cos(math.radians(31.5))
 return [(round(cx+(lon+100.0)*cos_lat*scale),round(cy-(lat-31.5)*scale)) for lon,lat in pts]

@lru_cache(None)
def source(root,name):return Image.open(Path(root)/name).convert('RGBA')

def plate(im,root,name,box,crop=None,cutout=False,rotate_deg=0.0):
 pic=source(root,name).copy()
 if crop:pic=pic.crop(crop)
 x,y,w,h=box;factor=min(w/pic.width,h/pic.height)
 if factor>2.35:raise ValueError(f'Upscale above house cap: {factor:.2f}x for {name}')
 pic.thumbnail((w,h),Image.Resampling.LANCZOS)
 if cutout:
  # Only remove the existing near-black surround; do not fabricate planet geometry.
  lum=pic.convert('L');alpha=lum.point(lambda v:min(255,max(0,(v-3)*20)))
  if crop:
   mask=Image.new('L',pic.size);ImageDraw.Draw(mask).ellipse((2,2,pic.width-3,pic.height-3),fill=255);alpha=ImageChops.multiply(alpha,mask)
  pic.putalpha(alpha)
 else:pic=ImageEnhance.Color(pic).enhance(1.12)
 if rotate_deg:
  pic=pic.rotate(rotate_deg,resample=Image.Resampling.BICUBIC,expand=False)
 im.alpha_composite(pic,(round(x+(w-pic.width)/2),round(y+(h-pic.height)/2)))

def caliper(d,x0,x1,y,colour=GOLD,tick_h=24,width=5):
 d.line((x0,y-tick_h,x0,y+tick_h),fill=WHITE,width=4)
 if abs(x1-x0)>24:
  arrow(d,(x0,y),(x1,y),colour=colour,width=width)
  d.line((x1,y-tick_h,x1,y+tick_h),fill=WHITE,width=4)

def frame(row,t,root):
 im=canvas().copy();d=ImageDraw.Draw(im);rid=row['row']
 p=next(p for p in PHASES[rid] if p[0]<=t<p[1]);start,end,labels=p;local=t-start;dur=end-start;u=ease(local/max(.5,dur-.4));phase=PHASES[rid].index(p)
 # Thin navy-grid explainer language, with genuine photographic bodies/plates.
 for x in range(120,1840,80):d.line((x,240,x,940),fill=(70,103,142,80),width=1)
 for y in range(260,950,80):d.line((120,y,1800,y),fill=(70,103,142,80),width=1)
 if rid=='R02':
  if phase==0:
   plate(im,root,'PIA20007.jpg',(220,250,1040,620),cutout=True)
   # Caliper anchored across the Sputnik Planitia bright nitrogen basin on PIA20007
   x0,x1,y=535,535+round(440*u),875
   d.line((535,660,535,895),fill=(244,247,251,160),width=3)
   d.line((x1,660,x1,895),fill=(255,207,64,190),width=3)
   caliper(d,x0,x1,y)
  else:
   plate(im,root,'PIA20007.jpg',(140,250,940,580),cutout=True)
   caliper(d,445,845,865,colour=GOLD)
   plate(im,root,'PIA18033.jpg',(1160,290,540,540),cutout=True)
   # Highlight Texas+Oklahoma region on North America and animated comparison bar below
   poly=project_tx_ok(TX_OK_OUTER,1410,490,7.5)
   d.line(poly,fill=GOLD,width=3)
   caliper(d,1235,1235+round(390*u),865,colour=BLUE)
 elif rid=='R15':
  if phase==0:
   plate(im,root,'PIA20534.jpg',(391,275,1138,560))
   d.rounded_rectangle((389,273,1531,837),radius=8,outline=BLUE,width=3)
   caliper(d,391,391+round(1138*u),875,colour=GOLD)
  elif phase==1:
   # Earth (12,742 km), Moon (3,475 km), and Pluto panorama inset with proportional 5:1 / 3:2 bars
   plate(im,root,'PIA18033.jpg',(140,255,600,600),cutout=True)
   plate(im,root,'PIA00405.jpg',(855,470,220,220),cutout=True)
   plate(im,root,'PIA20534.jpg',(1205,495,365,180))
   d.rounded_rectangle((1203,493,1572,677),radius=6,outline=GOLD,width=3)
   # Proportional width bars below: Earth 600 px, Moon 180 px, Pluto 120 px (1/5 Earth, 2/3 Moon)
   d.line((140,895,740,895),fill=(155,185,215,210),width=12)
   d.line((855,895,1035,895),fill=WHITE,width=12)
   caliper(d,1205,1205+round(120*u),895,colour=GOLD)
  else:
   # High-res crop of North America / Continental U.S. from 8000x8000 PIA18033 (0.35x downscale)
   plate(im,root,'PIA18033.jpg',(393,260,1134,590),crop=(1750,1150,5350,3650))
   d.rounded_rectangle((440,260,1480,850),radius=10,outline=BLUE,width=3)
   # Full Continental U.S. width reference bar (880 px) vs Pluto 2,377 km half-U.S. caliper (440 px)
   d.line((520,895,1400,895),fill=(155,185,215,200),width=10)
   d.line((520,875,520,915),fill=WHITE,width=4);d.line((1400,875,1400,915),fill=WHITE,width=4)
   plate(im,root,'PIA20534.jpg',(520,515,355,175))
   d.rounded_rectangle((518,513,962,692),radius=6,outline=GOLD,width=4)
   caliper(d,520,520+round(440*u),745,colour=GOLD)
 elif rid=='R24':
  plate(im,root,'PIA19968.jpg',(260,390,300,300),cutout=True)
  if phase==0:
   plate(im,root,'PIA00405.jpg',(840,220,660,660),cutout=True)
   caliper(d,260,260+round(300*u),750,colour=GOLD)
   d.line((840,910,1500,910),fill=(155,185,215,190),width=8)
  else:
   # Moon omitted in phase 2 so it cannot be misidentified as Pluto; explicit 2x Pluto reference ring + ratio bar
   cx,cy,r=1170,540,294
   d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=BLUE,width=4)
   d.line((cx-r,cy,cx+r,cy),fill=(105,196,241,140),width=3)
   d.line((260,860,848,860),fill=(155,180,205,210),width=14)
   d.line((260,860,260+round(300*u),860),fill=GOLD,width=14)
   caliper(d,260,260+round(300*u),750,colour=GOLD)
 elif rid=='R29':
  # Mutual tidal-lock & barycentric revolution using real PIA19966 Pluto and Charon cutouts
  cx,cy,r_c,r_p=960,610,290,34;angle=-math.pi/2+u*2*math.pi;rot=-math.degrees(u*2*math.pi)
  d.ellipse((cx-r_c,cy-r_c,cx+r_c,cy+r_c),outline=BLUE,width=4)
  d.line((cx-10,cy,cx+10,cy),fill=WHITE,width=2);d.line((cx,cy-10,cx,cy+10),fill=WHITE,width=2)
  px=cx-r_p*math.cos(angle);py=cy-r_p*math.sin(angle)
  qx=cx+r_c*math.cos(angle);qy=cy+r_c*math.sin(angle)
  plate(im,root,'PIA19966.jpg',(px-135,py-135,270,270),crop=(1010,990,2700,2730),cutout=True,rotate_deg=rot)
  plate(im,root,'PIA19966.jpg',(qx-68,qy-68,136,136),crop=(365,365,1240,1250),cutout=True,rotate_deg=rot)
  # Locked sightline between facing hemispheres + progress arc
  d.line((px,py,qx,qy),fill=GOLD,width=4)
  arc_r=160 if phase==0 else r_c
  d.arc((cx-arc_r,cy-arc_r,cx+arc_r,cy+arc_r),-90,-90+round(360*u),fill=GOLD,width=6)
  for k in range(24):
   a=k*math.pi/12;d.line((cx+(r_c+15)*math.cos(a),cy+(r_c+15)*math.sin(a),cx+(r_c+24)*math.cos(a),cy+(r_c+24)*math.sin(a)),fill=WHITE,width=2)
 elif rid=='R35':
  plate(im,root,'File_New_Horizons_1.jpg.jpg',(130,290,840,640))
  cx,cy,r=1400,740,290
  d.arc((cx-r,cy-r,cx+r,cy+r),180,360,fill=BLUE,width=7)
  for i in range(11):
   a=math.pi+i*math.pi/10;d.line((cx+(r-18)*math.cos(a),cy+(r-18)*math.sin(a),cx+r*math.cos(a),cy+r*math.sin(a)),fill=WHITE,width=3)
  a=math.pi+(u if phase==0 else 1)*math.pi
  arrow(d,(cx,cy),(cx+(r-35)*math.cos(a),cy+(r-35)*math.sin(a)))
  if phase==0:
   d.line((1110,860,1110+round(460*u),860),fill=GOLD,width=12)
  else:
   d.line((1110,860,1570,860),fill=GOLD,width=12)
   arrow(d,(1570,860),(1570+round(130*u),860),colour=BLUE,width=10)
 elif rid=='R48':
  plate(im,root,'PIA14458.jpg',(130,275,980,620))
  caliper(d,255,255+round(730*(u if phase==0 else 1.0)),855,colour=GOLD)
  if phase==0:
   # Sourced USGS Texas + Oklahoma outer perimeter and Red River border at matching scale
   outer=project_tx_ok(TX_OK_OUTER,1485,565,34.0)
   red=project_tx_ok(TX_OK_RED_RIVER,1485,565,34.0)
   u_poly=ease(local/1.8)
   n_pts=max(2,round(len(outer)*u_poly))
   d.line(outer[:n_pts],fill=BLUE,width=5)
   if u_poly>0.6:d.line(red,fill=(155,205,245,190),width=3)
   caliper(d,1285,1285+round(400*u),855,colour=GOLD)
  else:
   # Solar-system glacier width comparison bars locking #1 rank
   bars=[(520,GOLD),(250,BLUE),(165,BLUE),(110,BLUE)]
   for idx,(bw,col) in enumerate(bars):
    yy=420+idx*105
    d.rounded_rectangle((1210,yy,1210+round(bw*(u if idx==0 else 1.0)),yy+52),radius=8,fill=col if idx==0 else (75,130,175,210),outline=WHITE if idx==0 else BLUE,width=3)
 elif rid=='R56':
  plate(im,root,'PIA19957.jpg',(100,300,1050,650))
  if phase<2:
   # Linear thermometer with explicit 0 °C top and −240 °C bottom scale labels
   x,y0,y1=1350,360,900;d.rounded_rectangle((x-25,y0,x+25,y1),radius=24,outline=WHITE,width=5)
   temp=(233*u if phase==0 else 233);yy=y0+(y1-y0)*temp/240
   d.line((x,y0+10,x,yy),fill=BLUE,width=24)
   for i in range(9):
    y=y0+i*(y1-y0)/8;d.line((x+40,y,x+65,y),fill=WHITE,width=3)
   text(d,(x+85,y0),'0 °C',40,WHITE,'lm')
   text(d,(x+85,y1),'−240 °C',40,BLUE,'lm')
   if phase==1:arrow(d,(1265,y0),(1265,y0+(y1-y0)*200/240),colour=GOLD,width=6)
  else:
   for j in range(3):
    for i in range(3):
     x=1200+i*150;y=450+j*110-25*(1-u);d.rounded_rectangle((x,y,x+130,y+90),radius=6,outline=BLUE,width=5)
 elif rid=='R69':
  plate(im,root,'PIA20362.jpg',(170,290,620,390),cutout=True)
  plate(im,root,'File_Reworked_composite_image_of_Arrokoth_rotated.png.png',(830,330,420,350),cutout=True)
  # Calibrated outbound AU scale axis (39 AU Pluto -> 43 AU Arrokoth -> 60 AU)
  d.line((250,835,1650,835),fill=(140,175,210,160),width=4)
  for tx,tlab in ((480,'39 AU'),(840,'43 AU'),(1650,'60 AU')):
   d.line((tx,812,tx,858),fill=WHITE if tx<1650 else GOLD,width=4)
   text(d,(tx,895),tlab,38,WHITE if tx<1650 else GOLD,'mm')
  u_lock=ease(local/1.8)
  x_end=480+round(720*u) if phase==0 else 1200+round(450*u_lock)
  arrow(d,(480,835),(x_end,835),colour=GOLD,width=6)
  if phase==1:
   au_val=48+round(12*u_lock)
   d.ellipse((1650-24,835-24,1650+24,835+24),outline=GOLD,width=4)
   text(d,(1480,520),f'{au_val} AU',76,GOLD,'mm')
 # Rebuild drawing context after composites; labels remain off photographic subjects.
 layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer)
 for i,label in enumerate(labels):text(ld,(960,115+i*80),label,66 if len(label)<25 else 58,GOLD if i==0 else WHITE,'mm')
 # No static text card >4 seconds even in 5.88-second phases.
 window=min(dur,4.6);a=max(0,min(1,local/.4,(window-local)/.4));layer.putalpha(layer.getchannel('A').point(lambda v:round(v*a)));im.alpha_composite(layer)
 text(ImageDraw.Draw(im),(110,980),('NASA/KSC' if rid=='R35' else 'NASA/JHUAPL/SwRI'),28,WHITE)
 return im

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sources',required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--preview',action='store_true');ap.add_argument('--rows',nargs='*');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 rows=[r for r in csv.DictReader((HERE/'shot_list_v01.csv').open()) if r['row'] in PHASES and (not a.rows or r['row'] in a.rows)]
 manifest=dict(job='J2371',status='FULL_FRAME_8_OF_8',remaining=[],source_root=a.sources,shot_list_sha256=sha(HERE/'shot_list_v01.csv'),assets=[])
 for r in rows:
  for i,(st,en,_) in enumerate(PHASES[r['row']]):
   t_sample=st+min(dur:=en-st,4.6)*0.55
   frame(r,t_sample,a.sources).convert('RGB').save(a.out/f'{r["row"]}_phase{i+1}.jpg',quality=94)
  if a.preview:continue
  dest=a.out/r['asset'].split()[0]
  if dest.exists():raise FileExistsError(dest)
  frames=round(float(r['dur_s'])*FPS)
  proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],stdin=subprocess.PIPE)
  try:
   for j in range(frames):proc.stdin.write(frame(r,j/FPS,a.sources).tobytes())
   proc.stdin.close()
   if proc.wait():raise RuntimeError('encode failed')
  except BaseException:proc.kill();proc.wait();raise
  subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
  manifest['assets'].append(dict(row=r['row'],file=str(dest),sha256=sha(dest),bytes=dest.stat().st_size,frames=frames,fps=FPS,requested_duration=float(r['dur_s']),encoded_duration=frames/FPS,decode='PASS',sources=[dict(file=n,sha256=sha(Path(a.sources)/n)) for n in SOURCES[r['row']]],phases=PHASES[r['row']],status='RENDERED_PENDING_REVIEW'))
  a.manifest.write_text(json.dumps(manifest,indent=2)+'\n');print(r['row'],'rendered + decoded',flush=True)
if __name__=='__main__':main()
