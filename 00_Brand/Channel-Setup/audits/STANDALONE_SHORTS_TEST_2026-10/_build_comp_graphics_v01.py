#!/usr/bin/env python3
"""J0207: local-only 1080p30 cards and straight-alpha ProRes timelines.
Run cards, timelines, sheet, check in order. No network or generation APIs.
Timelines start at VO zero; assembly adds the segment's 0.6s lead-in.
Cards retain moving picture through edges; assembler uses 0.4s crossfades.
"""
import argparse, json, math, subprocess, io
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
PLAN=Path(__file__).resolve().parent
OUT=Path('/private/tmp/owb_comp/graphics_v01')
FONT='/System/Library/Fonts/Supplemental/Arial Black.ttf'
W,H,FPS=1920,1080,30
YELLOW=(255,216,55,255); WHITE=(246,247,250,255)
CARDS=[('021',40,'The Rings Are Leaving'),('013',300,'The Moon Lets Go'),('019',100,'Two Galaxies Meet'),('007',160,'What Dead Stars Leave'),('005',173,'The Last Light')]
TIMES=[('b1','bridge1_vo_v02',15.44,'300',1.8,6.9,1),('b3','bridge3_vo_v01',16.48,'collide,',0,4.6,2),('close','closing_vo_v01',20.08,'10',11.0,15.7,3)]
def run(a): return subprocess.check_output(a)
def smooth(x):
 x=max(0,min(1,x)); return x*x*(3-2*x)
def envelope(t,a,b): return min(smooth((t-a)/.4),smooth((b-t)/.4))
def text(d,xy,s,size=52,fill=WHITE,anchor='la'):
 d.text(xy,s,font=ImageFont.truetype(FONT,size),fill=fill,anchor=anchor,stroke_width=2,stroke_fill=(12,23,40,230))
def encoder(path,n,alpha=False):
 args=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgba' if alpha else 'rgb24','-s','1920x1080','-r','30','-i','-','-an']
 args+=['-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le','-threads','4'] if alpha else ['-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-threads','4']
 return subprocess.Popen(args+['-frames:v',str(n),str(path)],stdin=subprocess.PIPE)
def card_name(i): return f'code_graphic_owbcomp_card_{i:02d}.mp4'
def cards():
 for i,(film,start,title) in enumerate(CARDS,1):
  dec=subprocess.Popen(['ffmpeg','-v','error','-ss',str(start),'-reinit_filter','0','-i',f'/private/tmp/owb_comp/bodies_v01/body_{film}.mp4','-t','3','-vf','fps=30,scale=1920:1080,gblur=sigma=14,eq=brightness=0.12:saturation=0.65:contrast=0.8,noise=alls=2:allf=t','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
  enc=encoder(OUT/card_name(i),90)
  for k in range(90):
   data=dec.stdout.read(W*H*3)
   if len(data)!=W*H*3: raise RuntimeError('short plate')
   im=Image.frombytes('RGB',(W,H),data).convert('RGBA'); im=Image.alpha_composite(im,Image.new('RGBA',(W,H),(15,32,57,65)))
   layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer);t=k/FPS;a=envelope(t,0,3);dy=round(24*(1-smooth(t/.4)))
   title_y=350 if i==4 else 520
   text(d,(960,title_y+dy),title,86,YELLOW,'mm');d.line((760,title_y+80+dy,1160,title_y+80+dy),fill=WHITE,width=3)
   layer.putalpha(layer.getchannel('A').point(lambda v:round(v*a)))
   enc.stdin.write(Image.alpha_composite(im,layer).convert('RGB').tobytes())
  enc.stdin.close();assert enc.wait()==0;assert dec.wait()==0
  print(card_name(i),flush=True)
def cue(stem,token):
 p=PLAN/'vo_compilation_v01/stt'/f'owb_comp_{stem}'/'stt_raw.json'
 return next(w['start'] for w in json.loads(p.read_text())['words'] if w['text']==token)
def timeline_frame(t,a,b,count,hit):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im);opacity=envelope(t,a,b)
 if opacity<=0:return im
 # Log axis: 10^8 through 10^13; no extra numeric claims displayed.
 x0,x1,y=180,1740,830
 progress=smooth((t-a)/.65) if count==1 else 1
 d.line((x0,y,x0+(x1-x0)*progress,y),fill=(100,192,228,235),width=4)
 for j in range(6):
  x=x0+(x1-x0)*j/5
  if x<=x0+(x1-x0)*progress:d.line((x,y-8,x,y+8),fill=(110,168,193,160),width=2)
 # Broad qualitative band for galaxies, deliberately no precise merger date.
 points=[(x0+(math.log10(math.sqrt(1e8*3e8))-8)/5*(x1-x0),"SATURN'S RINGS",'100–300 MILLION YEARS'),(x0+.4*(x1-x0),'GALAXIES MERGE','BILLIONS OF YEARS'),(x1,'LAST STARS','~10 TRILLION YEARS')]
 for j,(x,label,value) in enumerate(points[:count]):
  drop=smooth((t-hit)/.4) if j==count-1 else 1
  if drop<=0:continue
  yy=y-round(28*(1-drop));c=(*YELLOW[:3],round(255*drop))
  if j==1:d.line((x0+.2*(x1-x0),y+14,x0+.6*(x1-x0),y+14),fill=(*YELLOW[:3],100),width=6)
  if j==0:
   end=x0+(math.log10(3e8)-8)/5*(x1-x0);d.line((x0,y+14,end,y+14),fill=c,width=6)
  d.ellipse((x-9,yy-9,x+9,yy+9),fill=c)
  anchor='la' if j==0 else ('ra' if j==2 else 'ma');tx=x0 if j==0 else x
  ty=690 if j!=1 else 905
  text(d,(tx,ty),label,44,c,anchor);text(d,(tx,ty+58),value,38,(*WHITE[:3],round(255*drop)),anchor)
  d.line((x,yy-16 if j!=1 else yy+16,x,ty+110 if j!=1 else ty-10),fill=c,width=2)
 im.putalpha(im.getchannel('A').point(lambda v:round(v*opacity)))
 return im

def timelines():
 manifest={'timebase':'seconds from VO start; add 0.6s for segment-local placement','fps':30,'alpha':'straight','assembly':'Place at VO zero over graded moving footage; no black background. Cards: 0.4s crossfade after sentence plus 0.5–0.8s breath.','log_axis':'10^8–10^13, equally spaced decades. Saturn interval 100–300 million. Galaxies qualitative billions band (10^9–10^11), central marker is categorical, not a numeric estimate.','cards':[{'file':card_name(i),'film':f,'source_start':s,'duration':3} for i,(f,s,_) in enumerate(CARDS,1)],'timelines':[]}
 for key,stem,duration,token,a,b,count in TIMES:
  hit=cue(stem,token);n=math.ceil(duration*FPS);name=f'code_graphic_owbcomp_timeline_{key}.mov';enc=encoder(OUT/name,n,True)
  for k in range(n):enc.stdin.write(timeline_frame(k/FPS,a,b,count,hit).tobytes())
  enc.stdin.close();assert enc.wait()==0
  manifest['timelines'].append({'file':name,'vo':f'owb_comp_{stem}.wav','vo_duration':duration,'render_duration':n/FPS,'frames':n,'visible':[a,b],'tick_vo_seconds':hit,'tick_segment_seconds':hit+.6,'tick_frame':math.ceil(hit*FPS),'word':token,'scribe':f'vo_compilation_v01/stt/owb_comp_{stem}/stt_raw.json'})
  print(name,flush=True)
 (OUT/'ticks.json').write_text(json.dumps(manifest,indent=2)+'\n')
def grab(p,t):
 return Image.open(io.BytesIO(run(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-f','image2pipe','-vcodec','png','-']))).convert('RGBA')
def sheet():
 s=Image.new('RGB',(1280,4*410),(25,38,57));d=ImageDraw.Draw(s)
 samples=[(card_name(i),1.5) for i in range(1,6)]+[(f'code_graphic_owbcomp_timeline_{k}.mov',cue(stem,tok)+.8) for k,stem,_,tok,*_ in TIMES]
 for j,(name,t) in enumerate(samples):
  im=grab(OUT/name,t)
  if name.endswith('.mov'):
   bg=grab(Path('/private/tmp/owb_comp/bodies_v01/body_019.mp4'),105).convert('RGBA');bg=Image.blend(bg,Image.new('RGBA',(W,H),(30,45,65,255)),.55);im=Image.alpha_composite(bg,im)
  x=j%2*640;y=j//2*410;s.paste(im.convert('RGB').resize((640,360)),(x,y));d.text((x+12,y+367),name,fill='white')
 s.save(PLAN/'graphics_v01_sheet.jpg',quality=92);s.save(OUT/'graphics_v01_sheet.jpg',quality=92)
def check():
 report=[]
 for p in sorted(OUT.glob('code_graphic*')):
  probe=json.loads(run(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(p)]))['streams'][0]
  assert (probe['width'],probe['height'],probe['r_frame_rate'])==(1920,1080,'30/1')
  expected=90 if '_card_' in p.name else next(math.ceil(d*FPS) for k,_,d,*_ in TIMES if p.stem.endswith('_'+k))
  assert int(probe['nb_frames'])==expected
  row={'file':p.name,'frames':expected,'duration':float(probe['duration']),'pixel_format':probe['pix_fmt']}
  if '_card_' in p.name:
   raw=run(['ffmpeg','-v','error','-i',str(p),'-vf','scale=480:270,format=gray','-f','rawvideo','-']);frames=np.frombuffer(raw,np.uint8).reshape(-1,270,480)
   means=frames.mean(axis=(1,2));p95=np.percentile(frames,95,axis=(1,2));assert np.all((means>=28)|(p95>=50))
   row.update(min_mean_luma=round(float(means.min()),2),min_p95_luma=round(float(p95.min()),2),near_black_frames_measured=len(frames))
  else:assert 'a' in probe['pix_fmt']
  report.append(row)
 (OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('step',choices=['cards','timelines','sheet','check']);args=p.parse_args();OUT.mkdir(parents=True,exist_ok=True);globals()[args.step]()
