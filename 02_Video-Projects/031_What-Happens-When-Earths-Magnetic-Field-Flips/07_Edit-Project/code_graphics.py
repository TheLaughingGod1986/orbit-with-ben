#!/usr/bin/env python3
"""031 J2141: row-specific transparent WHO/FACT edit overlays. £0.

Cards ride over moving/blurred real plates in assembly. These are alpha overlays,
not full-frame black cards. Timing follows the locked v02a Scribe words. No KEEP
or motion review is implied by successful encoding. Remaining mechanisms are
listed in BUILD_HANDOFF_J2141.md; unsupported modes fail explicitly.
"""
import argparse, hashlib, io, json, math, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1920,1080,25
HERE=Path(__file__).resolve().parent
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
# row, kind, trigger, labels, source row, end of allowed shot-list row
CARDS=[
 (5,'WHO','Bernard Brunhes',['Bernard Brunhes','(1867–1910) — French geophysicist'],19,45.76),
 (10,'WHO','Motonori Matuyama',['Motonori Matuyama','(1884–1958) — Japanese geophysicist'],19,98.22),
 (20,'WHO','Carl Friedrich Gauss',['Carl Friedrich Gauss','(1777–1855) — German mathematician'],19,225.48),
 (6,'FACT','baking the mud',['BAKED INTO RED BRICK'],3,53.32),
 (14,'FACT','hot as the surface',['HOT AS THE SUN'],6,141.12),
 (19,'FACT','183 times',['183 MAGNETIC FLIPS'],7,202.38),
 (27,'FACT','stops observing',['HUBBLE STOPS OBSERVING'],11,289.02),
 (35,'FACT','recorded like a diary',['RECORDED LIKE A DIARY'],14,373.06),
 (45,'FACT','no link',['NO MASS EXTINCTIONS'],2,468.98),
]
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def schedule(words):
 words=[w for w in words if w.get('type')=='word'];tokens=[norm(w['text']) for w in words];out=[]
 for row,kind,trigger,labels,source,end in CARDS:
  q=[norm(s) for s in trigger.split()]; hits=[i for i in range(len(tokens)-len(q)+1) if tokens[i:i+len(q)]==q and words[i]['start']<end and end-words[i]['start']<25]
  if len(hits)!=1:raise ValueError(f'Expected unique cue for r{row}: {trigger}: {hits}')
  start=float(words[hits[0]]['start']);duration=min(3.6,end-start)
  if duration<0.8:raise ValueError(f'Insufficient card window r{row}')
  out.append(dict(id=f'code_graphic_031_r{row:02d}_{kind.lower()}_v01',row=row,kind=kind,labels=labels,source_rows=[source],start_s=start,duration_s=round(math.floor(duration*FPS)/FPS,2),cue=trigger))
 return out

def frame(card,t):
 # 0.4s animation in/out; no flat slab, no still hold longer than 4s.
 d=card['duration_s'];alpha=max(0,min(1,t/.4,(d-t)/.4));ease=.5-.5*math.cos(math.pi*alpha)
 im=Image.new('RGBA',(W,H),(0,0,0,0));dr=ImageDraw.Draw(im);x=140+round(30*(1-ease));y=800
 dr.line((x,778,x+round(150*ease),778),fill=(255,201,74,round(255*alpha)),width=6)
 for n,label in enumerate(card['labels']):
  f=ImageFont.truetype(FONT,62 if n==0 else 42);pos=(x,y+n*82)
  box=dr.textbbox(pos,label,font=f,stroke_width=2)
  if box[2]>1780 or box[3]>1010:raise ValueError(f'Unsafe text: {label}')
  dr.text(pos,label,font=f,fill=((255,201,74) if n==0 else (244,239,230))+(round(255*alpha),),stroke_width=2,stroke_fill=(12,23,39,round(220*alpha)))
 return im

def main():
 if len(sys.argv)>1 and sys.argv[1]=='mechanisms':
  from mechanism_graphics import main as mechanisms
  return mechanisms(sys.argv[2:])
 ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['cards']);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--words',type=Path,default=HERE.parent/'02_Voiceover/stt/magnetic_field_flip_vo_v02a/stt_raw.json');ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--previews',action='store_true');a=ap.parse_args()
 cards=schedule(json.loads(a.words.read_text())['words']);a.out.mkdir(parents=True,exist_ok=True)
 for c in cards:
  preview=a.out/(c['id']+'.png');frame(c,min(1,c['duration_s']/2)).save(preview)
  if a.previews:continue
  dest=a.out/(c['id']+'.mov')
  cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','qtrle','-pix_fmt','argb',str(dest)]
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
  try:
   for i in range(round(c['duration_s']*FPS)):proc.stdin.write(frame(c,i/FPS).tobytes())
   proc.stdin.close();rc=proc.wait()
  except BaseException:proc.kill();proc.wait();raise
  if rc:raise RuntimeError(f'ffmpeg exited {rc}')
  c.update(path=str(dest),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size,fps=FPS,width=W,height=H,alpha=True,review_status='pending_composite_and_Chief_review')
  print(c['id'],flush=True)
 a.manifest.write_text(json.dumps(dict(job='J2141',status='partial_cards_only',spend_gbp=0,locked_words_sha256=hashlib.sha256(a.words.read_bytes()).hexdigest(),cards=cards),indent=2)+'\n')
if __name__=='__main__':main()
