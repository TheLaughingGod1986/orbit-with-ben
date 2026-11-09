#!/usr/bin/env python3
"""034 locked chapter cards and folded transparent gauges, J2371, £0.

Pillow + ffmpeg; no API calls, no implicit downloads, no source mutation.
Full-frame CODE rows (R02/R15/R24/R29/R35/R48/R56/R69) live in full_frame_graphics.py.
Output is review material, never implicit KEEP.
"""
import argparse, csv, hashlib, json, math, subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
HERE=Path(__file__).resolve().parent
W,H,FPS=1920,1080,30
GOLD=(255,207,64,255); WHITE=(244,247,251,255); BLUE=(105,196,241,255)
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
# Exact local phase boundaries from the locked CSV, not equal-duration guesses.
PHASES={
 'R17':[(0,4.06,['39 AU (5.5 HOURS)'],'distance'),(4.06,8.16,['1/900 EARTH SUN'],'sunlight'),(8.16,12.19,['300× FULL MOON','SUNSET TWILIGHT BRIGHTNESS'],'moonlight')],
 'R38':[(0,4.83,['248-YEAR ORBIT','30 TO 49.3 AU'],'orbit'),(4.83,9.74,['4.5B YRS AGO','1930','2006'],'timeline')],
 'R43':[(0,4.71,['6.25 GB DOWNLINK','15 MONTHS'],'download'),(4.71,9.48,['4.5 LIGHT-HOURS','1–2 KBPS DOWNLINK'],'radio')],
 'R52':[(0,4.86,['2–3 KM MOUNTAINS','600 KM VALLEYS'],'elevation'),(4.86,9.76,['SOLID -> GAS'],'sublimation'),(9.76,14.57,['6% EARTH GRAVITY'],'gravity')],
 'R61':[(0,4.49,['~13 MICROBARS'],'basal'),(4.49,9.08,['BASAL LIQUID NITROGEN'],'rise')],
}
@lru_cache(None)
def font(size):return ImageFont.truetype(FONT,size)
def ease(x):return .5-.5*math.cos(math.pi*max(0,min(1,x)))
def text(d,xy,s,size=58,colour=WHITE,anchor=None):
 box=d.textbbox(xy,s,font=font(size),anchor=anchor,stroke_width=2)
 if box[0]<70 or box[2]>1850 or box[1]<50 or box[3]>1030:raise ValueError(f'Text outside safe area: {s}')
 d.text(xy,s,font=font(size),fill=colour,anchor=anchor,stroke_width=2,stroke_fill=(18,30,48,230))
def arrow(d,a,b,colour=GOLD,width=5):
 d.line((*a,*b),fill=colour,width=width);ang=math.atan2(b[1]-a[1],b[0]-a[0])
 pts=[b,(b[0]-18*math.cos(ang-.5),b[1]-18*math.sin(ang-.5)),(b[0]-18*math.cos(ang+.5),b[1]-18*math.sin(ang+.5))];d.polygon(pts,fill=colour)
@lru_cache(None)
def canvas():
 # Same radial colour endpoints and deterministic star hash as the luma artifact.
 small=Image.new('RGB',(480,270));p=small.load();cx,cy=239.875,134.875;radius=math.hypot(cx,cy)
 for y in range(270):
  for x in range(480):
   t=min(1,math.hypot(x-cx,y-cy)/radius);p[x,y]=tuple(round(a+(b-a)*t) for a,b in zip((31,49,80),(22,34,56)))
 im=small.resize((W,H),Image.Resampling.BILINEAR).convert('RGBA');d=ImageDraw.Draw(im)
 for y in range(0,H,4):
  for x in range(0,W,4):
   if ((x*73856093)^(y*19349663))&65535<524:
    c=im.getpixel((x,y));d.point((x,y),fill=tuple(min(255,k+28) for k in c[:3])+(255,))
 return im

def card_frame(row,t):
 im=canvas().copy();layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 title=row['label'].removeprefix('CHAPTER CARD: ')
 # Balanced lines, no paraphrasing of locked chapter titles.
 words=title.split();best=min(range(1,len(words)),key=lambda k:abs(len(' '.join(words[:k]))-len(' '.join(words[k:]))))
 lines=[' '.join(words[:best]),' '.join(words[best:])]
 a=min(1,t/.4,(2.5-t)/.4);shift=round(22*(1-ease(a)))
 text(d,(960,350+shift),row['chapter'].upper(),42,GOLD,'mm')
 for i,line in enumerate(lines):text(d,(960,475+i*115+shift),line,86,WHITE,'mm')
 d.line((760,710,760+round(400*ease(min(1,t/.4))),710),fill=GOLD,width=5)
 layer.putalpha(layer.getchannel('A').point(lambda v:round(v*max(0,a))))
 im.alpha_composite(layer);return im

def overlay_frame(row,t):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 start,end,labels,kind=next(p for p in PHASES[row['row']] if p[0]<=t<p[1])
 local=t-start;dur=end-start;u=ease(local/max(.4,dur-.5));fade=min(1,local/.4,(min(dur,4.6)-local)/.4)
 # Teaching graphics occupy lower third; no slab. Plate placement stays assembly-owned.
 x0,x1,y=160,1760,935
 if kind in ('distance','download'):
  d.line((x0,y,x1,y),fill=(150,180,210,150),width=4)
  arrow(d,(x0,y),(x0+(x1-x0)*u,y));d.line((x0,915,x0,955),fill=WHITE,width=3)
 elif kind=='sunlight':
  # Unit square grid: one gold cell out of 900, a literal brightness fraction.
  for i in range(900):
   x=1000+(i%45)*16;yy=675+(i//45)*12
   d.rectangle((x,yy,x+10,yy+7),fill=GOLD if i==0 else (132,166,198,100))
 elif kind=='moonlight':
  # 300 small luminous units, revealed progressively. No invented Moon disc.
  for i in range(round(300*u)):
   x=1040+(i%30)*21;yy=710+(i//30)*20;d.rectangle((x,yy,x+11,yy+10),fill=BLUE)
 elif kind=='orbit':
  # q=30,Q=49.3 -> a=39.65,e=(Q-q)/(Q+q). Ellipse is a path, not a body.
  a=190;b=a*math.sqrt(1-((49.3-30)/(49.3+30))**2);cx,cy=1370,800
  pts=[(cx+a*math.cos(v*2*math.pi/160),cy+b*math.sin(v*2*math.pi/160)) for v in range(max(2,round(161*u)))]
  d.line(pts,fill=BLUE,width=5)
 elif kind=='timeline':
  # Discrete milestones, explicitly not proportional chronology.
  d.line((200,940,1720,940),fill=BLUE,width=3)
  for i,lab in enumerate(labels):
   if u>=i*.22:
    x=340+i*620;d.line((x,920,x,960),fill=GOLD,width=6);text(d,(x,865),lab,42,GOLD,'mm')
  labels=[]
 elif kind=='radio':
  for i in range(6):
   x=250+((i/6+local*.16)%1)*1400
   d.arc((x-40,850,x+40,980),-65,65,fill=BLUE,width=4)
 elif kind=='elevation':
  arrow(d,(1460,960),(1460,960-210*u));d.line((1300,960,1660,960),fill=BLUE,width=4)
 elif kind=='sublimation':
  for i in range(24):
   x=1170+(i%8)*65;yy=960-((i/24+local*.2)%1)*240
   d.ellipse((x,yy,x+7,yy+7),fill=BLUE)
  d.line((1100,970,1700,970),fill=WHITE,width=3)
 elif kind=='gravity':
  d.line((1000,935,1720,935),fill=(155,190,215,150),width=18)
  d.line((1000,935,1000+720*.06*u,935),fill=GOLD,width=18)
 elif kind in ('basal','rise'):
  # Schematic layer boundary and cracks, with flow only from the base upward.
  d.line((1050,740,1720,740),fill=WHITE,width=5);d.line((1050,960,1720,960),fill=BLUE,width=6)
  for x in (1190,1450,1640):
   d.line((x,960,x-30,880,x+12,810,x-8,740),fill=(135,200,230,180),width=4)
   if kind=='rise':arrow(d,(x-4,955),(x-4,955-195*u),BLUE,6)
 for i,lab in enumerate(labels):text(d,(160,745+i*78),lab,58 if len(lab)<25 else 48,GOLD if i==0 else WHITE)
 if row['row']=='R43' and .43<=t<4.03:
  date_layer=Image.new('RGBA',(W,H));dd=ImageDraw.Draw(date_layer)
  text(dd,(160,635),'25 OCTOBER 2016',50,WHITE)
  da=min(1,(t-.43)/.4,(4.03-t)/.4);date_layer.putalpha(date_layer.getchannel('A').point(lambda v:round(v*da)));im.alpha_composite(date_layer)
 # Phase fade prevents static labels staying up for >4 seconds.
 im.putalpha(im.getchannel('A').point(lambda v:round(v*max(0,fade))))
 return im

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def render(row,out):
 card=row['source']=='CARD';name=row['asset'].split(' ')[0] if card else row['asset'].split('(overlay_')[1].split(')')[0]
 if not card:name='overlay_'+name+'.mov'
 dest=out/name
 if dest.exists():raise FileExistsError(f'Refusing overwrite: {dest}')
 duration=float(row['dur_s']);frames=round(duration*FPS);fn=card_frame if card else overlay_frame
 cmd=['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an']
 cmd+=['-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart'] if card else ['-c:v','qtrle','-pix_fmt','argb']
 p=subprocess.Popen(cmd+[str(dest)],stdin=subprocess.PIPE)
 try:
  for i in range(frames):p.stdin.write(fn(row,i/FPS).tobytes())
  p.stdin.close()
  if p.wait():raise RuntimeError(f'encode failed: {dest}')
 except BaseException:
  p.kill();p.wait();raise
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]))
 stream=probe['streams'][0];actual=float(probe['format']['duration'])
 assert abs(actual-duration)<=1/FPS+.001
 assert (stream['width'],stream['height'])==(W,H)
 if not card:assert stream['pix_fmt']=='argb'
 subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
 return dict(row=row['row'],file=str(dest),sha256=sha(dest),bytes=dest.stat().st_size,requested_duration=duration,encoded_duration=actual,frames=frames,fps=FPS,alpha=not card,decode='PASS',phases=PHASES.get(row['row']),status='RENDERED_PENDING_COMPOSITE_REVIEW')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--manifest',required=True,type=Path);ap.add_argument('--preview',action='store_true');ap.add_argument('--rows',nargs='*');args=ap.parse_args()
 rows=list(csv.DictReader((HERE/'shot_list_v01.csv').open()))
 selected=[r for r in rows if (r['source']=='CARD' or r['row'] in PHASES) and (not args.rows or r['row'] in args.rows)]
 args.out.mkdir(parents=True,exist_ok=True)
 manifest=dict(job='J2371',status='CARDS_AND_OVERLAYS_11_OF_11',spend_gbp=0,shot_list_sha256=sha(HERE/'shot_list_v01.csv'),font=FONT,canvas_artifact_sha256=sha(HERE/'LIFTED_NAVY_LUMA_ARTIFACT_v01.json'),full_frame_companion='full_frame_graphics.py',assets=[])
 for row in selected:
  times=[1.25] if row['source']=='CARD' else [(a+b)/2 for a,b,_,_ in PHASES[row['row']]]
  for j,t in enumerate(times):
   im=card_frame(row,t) if row['source']=='CARD' else overlay_frame(row,t)
   if row['source']!='CARD':bg=canvas().copy();bg.alpha_composite(im);im=bg
   im.convert('RGB').save(args.out/f'{row["row"]}_phase{j+1}.jpg',quality=92)
  if not args.preview:
   manifest['assets'].append(render(row,args.out));args.manifest.write_text(json.dumps(manifest,indent=2)+'\n');print(row['row'],'rendered + decoded',flush=True)
 if args.preview:print('Previews only')
if __name__=='__main__':main()
