#!/usr/bin/env python3
"""J2371 source-backed full-frame builders. No downloads; never overwrites assets.

R15/R48 remain unsupported: R15's panorama is not a globe; R48 needs a
verified Texas/Oklahoma vector outline. Keep the locked shot plan unchanged.
"""
import argparse,csv,json,math,subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw,ImageEnhance,ImageChops
from code_graphics import W,H,FPS,HERE,GOLD,WHITE,BLUE,canvas,text,arrow,ease,sha
PHASES={
 'R02':[(0,5.15,['1,000 KM WIDE']),(5.15,10.44,['> TEXAS + OKLAHOMA','0 CRATERS'])],
 'R24':[(0,3.47,['1,214 KM ACROSS']),(3.47,6.94,["HALF PLUTO'S SIZE"])],
 'R29':[(0,5.14,['153 HOURS (6.4 DAYS)']),(5.14,10.20,['153 HOURS'])],
 'R35':[(0,5.26,['58,536 KM/H','(36,400 MPH)']),(5.26,10.53,['FASTEST EARTH LAUNCH','+14,000 KM/H BOOST'])],
 'R56':[(0,4.18,['0 °C FREEZING POINT','−226 TO −240 °C']),(4.18,8.38,['200 °C BELOW FREEZING']),(8.38,12.50,['WATER-ICE BEDROCK'])],
 'R69':[(0,5.87,['1 OCTOBER 2024','300M MILES/YR']),(5.87,11.76,['60 AU FROM SUN'])],
}
SOURCES={
 'R02':['PIA20007.jpg','PIA18033.jpg'],
 'R24':['PIA19968.jpg','PIA00405.jpg'],
 'R29':['PIA19966.jpg'],
 'R35':['File_New_Horizons_1.jpg.jpg'],
 'R56':['PIA19957.jpg'],
 'R69':['PIA20362.jpg','File_Reworked_composite_image_of_Arrokoth_rotated.png.png'],
}
@lru_cache(None)
def source(root,name):return Image.open(Path(root)/name).convert('RGBA')
def plate(im,root,name,box,crop=None,cutout=False):
 pic=source(root,name).copy()
 if crop:pic=pic.crop(crop)
 x,y,w,h=box;factor=min(w/pic.width,h/pic.height)
 if factor>2.35:raise ValueError('Upscale above house cap')
 pic.thumbnail((w,h),Image.Resampling.LANCZOS)
 if cutout:
  # Only remove the existing near-black surround; do not fabricate planet geometry.
  lum=pic.convert('L');alpha=lum.point(lambda v:min(255,max(0,(v-3)*20)))
  if crop:
   mask=Image.new('L',pic.size);ImageDraw.Draw(mask).ellipse((2,2,pic.width-3,pic.height-3),fill=255);alpha=ImageChops.multiply(alpha,mask)
  pic.putalpha(alpha)
 else:pic=ImageEnhance.Color(pic).enhance(1.12)
 im.alpha_composite(pic,(round(x+(w-pic.width)/2),round(y+(h-pic.height)/2)))
def frame(row,t,root):
 im=canvas().copy();d=ImageDraw.Draw(im);rid=row['row']
 p=next(p for p in PHASES[rid] if p[0]<=t<p[1]);start,end,labels=p;local=t-start;dur=end-start;u=ease(local/max(.5,dur-.4));phase=PHASES[rid].index(p)
 # Thin navy-grid explainer language, with genuine photographic bodies/plates.
 for x in range(120,1840,80):d.line((x,240,x,940),fill=(70,103,142,80),width=1)
 for y in range(260,950,80):d.line((120,y,1800,y),fill=(70,103,142,80),width=1)
 if rid=='R02':
  plate(im,root,'PIA20007.jpg',(180,260,1000,620),cutout=True)
  if phase==0:
   # Width object is separate from the perspective image: no false map calibration.
   arrow(d,(1150,730),(1150+500*u,730));d.line((1150,700,1150,760),fill=WHITE,width=4)
  else:plate(im,root,'PIA18033.jpg',(1180,330,520,520),cutout=True)
 elif rid=='R24':
  # Photographic comparison only; locked labels carry the numeric claims.
  plate(im,root,'PIA19968.jpg',(240,410,280,280),cutout=True)
  if phase==0:plate(im,root,'PIA00405.jpg',(770,220,800,800),cutout=True)
  if phase==0:
   arrow(d,(240,760),(240+280*u,760));d.line((240,740,240,780),fill=WHITE,width=3)
  else:
   d.line((210,860,650,860),fill=(155,180,205,200),width=12);d.line((210,860,210+220*u,860),fill=GOLD,width=12)
 elif rid=='R29':
  # Dial/sightline schematic, not a simulated telescope observation.
  cx,cy,r=960,610,290;angle=-math.pi/2+u*2*math.pi
  d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=BLUE,width=4)
  plate(im,root,'PIA19966.jpg',(cx-140,cy-140,280,280),crop=(1010,990,2700,2730),cutout=True)
  xx=cx+r*math.cos(angle);yy=cy+r*math.sin(angle)
  plate(im,root,'PIA19966.jpg',(xx-70,yy-70,140,140),crop=(365,365,1240,1250),cutout=True)
  d.line((cx,cy,xx,yy),fill=GOLD,width=3)
  for k in range(24):
   a=k*math.pi/12;d.line((cx+(r+15)*math.cos(a),cy+(r+15)*math.sin(a),cx+(r+24)*math.cos(a),cy+(r+24)*math.sin(a)),fill=WHITE,width=2)
 elif rid=='R35':
  plate(im,root,'File_New_Horizons_1.jpg.jpg',(130,290,840,640))
  cx,cy,r=1400,760,300
  d.arc((cx-r,cy-r,cx+r,cy+r),180,360,fill=BLUE,width=7)
  for i in range(11):
   a=math.pi+i*math.pi/10;d.line((cx+(r-18)*math.cos(a),cy+(r-18)*math.sin(a),cx+r*math.cos(a),cy+r*math.sin(a)),fill=WHITE,width=3)
  a=math.pi+(u if phase==0 else 1)*math.pi
  arrow(d,(cx,cy),(cx+(r-35)*math.cos(a),cy+(r-35)*math.sin(a)))
  d.line((1100,870,1100+600*u,870),fill=GOLD,width=10)
 elif rid=='R56':
  plate(im,root,'PIA19957.jpg',(100,300,1050,650))
  if phase<2:
   # Linear thermometer: freezing point at top, -240 C at bottom.
   x,y0,y1=1390,360,900;d.rounded_rectangle((x-25,y0,x+25,y1),radius=24,outline=WHITE,width=5)
   temp=(233*u if phase==0 else 233);yy=y0+(y1-y0)*temp/240
   d.line((x,y0+10,x,yy),fill=BLUE,width=24)
   for i in range(9):
    y=y0+i*(y1-y0)/8;d.line((x+40,y,x+65,y),fill=WHITE,width=3)
   if phase==1:arrow(d,(1510,y0),(1510,y0+(y1-y0)*200/240))
  else:
   # Interlocking blocks express rigidity; no claim of measured material stiffness.
   for j in range(3):
    for i in range(3):
     x=1200+i*150;y=450+j*110-25*(1-u);d.rounded_rectangle((x,y,x+130,y+90),radius=6,outline=BLUE,width=5)
 elif rid=='R69':
  plate(im,root,'PIA20362.jpg',(170,300,640,400),cutout=True)
  plate(im,root,'File_Reworked_composite_image_of_Arrokoth_rotated.png.png',(960,350,440,380),cutout=True)
  # Outbound progress path, not a calibrated orbital map.
  arrow(d,(250,850),(250+1400*u,850));d.line((250,825,250,875),fill=WHITE,width=4)
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
 manifest=dict(job='J2371',status='PARTIAL_6_OF_8_FULL_FRAME',remaining=['R15','R48'],source_root=a.sources,shot_list_sha256=sha(HERE/'shot_list_v01.csv'),assets=[])
 for r in rows:
  for i,(st,en,_) in enumerate(PHASES[r['row']]):frame(r,(st+en)/2,a.sources).convert('RGB').save(a.out/f'{r["row"]}_phase{i+1}.jpg',quality=94)
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
  manifest['assets'].append(dict(row=r['row'],file=str(dest),sha256=sha(dest),frames=frames,fps=FPS,requested_duration=float(r['dur_s']),encoded_duration=frames/FPS,decode='PASS',sources=[dict(file=n,sha256=sha(Path(a.sources)/n)) for n in SOURCES[r['row']]],phases=PHASES[r['row']],status='DRAFT_PENDING_REVIEW'))
  a.manifest.write_text(json.dumps(manifest,indent=2)+'\n');print(r['row'],'rendered + decoded',flush=True)
if __name__=='__main__':main()
