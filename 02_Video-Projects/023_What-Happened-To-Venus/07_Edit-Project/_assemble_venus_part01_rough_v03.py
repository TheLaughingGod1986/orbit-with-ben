#!/usr/bin/env python3
"""Venus Part01 rough v03: v02 with Claude's fixes (6025765289). Rows 2->3 and 13c->14a cut in the pause before the sentence;
dark edges cropped off PIA00215 (15b) and PIA00240 (16a). Picture only; v01 audio stream copied untouched."""
from pathlib import Path
import json, subprocess as sp, re, hashlib, shutil, sys
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent; EP=HERE.parent
UAT=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/OWB UAT'
WORK=Path('/private/tmp/venus023_part01_work_v03'); PACK=HERE/'part01_rough_v03_pack'
V02_WORK=Path('/private/tmp/venus023_part01_work_v02'); V02_CUTS=HERE/'part01_rough_v02_pack/cuts_v02.json'
V01=UAT/'023_Venus_Part01_rough_v01.mp4'; OUT=UAT/'023_Venus_Part01_rough_v03.mp4'; TOTAL=142.22; FPS=30
CROP_CLEAR={'PIA00215.jpg','PIA00240.jpg'}
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
CLIP_CHECK=EP.parents[1]/'00_Brand/Channel-Setup/tools/clip_check.py'
def run(args):
 p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-6000:])
def probe(p):return float(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
def fr(t):return round(t*FPS)/FPS
def clear_box(im,thresh=14,run=20,margin=8):
 """Smallest centred 16:9 crop of a greyscale still whose edges hold no Magellan no-data black."""
 a=np.array(im.convert('L')).astype(int);h,w=a.shape;nd=a>=thresh
 def edge(r):
  k=np.convolve(r.astype(int),np.ones(run,int),'valid')
  hit=np.flatnonzero(k==run);return int(hit[0]) if len(hit) else len(r)
 left=np.array([edge(nd[y]) for y in range(h)]);right=np.array([edge(nd[y][::-1]) for y in range(h)])
 cx,cy=w/2,h/2
 for hw in range(int(min(cx,cy*16/9)),100,-2):
  hh=hw*9/16;y0,y1=int(cy-hh),int(cy+hh);x0,x1=int(cx-hw),int(cx+hw)
  if x0>=left[y0:y1].max()+margin and w-x1>=right[y0:y1].max()+margin:return (x0,y0,x1,y1)
 raise RuntimeError('no clear box')

rows=[]
for line in (HERE/'SHOT_LIST_v02.md').read_text().splitlines():
 c=[x.strip() for x in line.split('|')[1:-1]]
 if len(c)!=8 or not re.fullmatch(r'\d+[abc]?',c[0]):continue
 if int(re.match(r'\d+',c[0])[0])>18:continue
 rows.append(dict(row=c[0],vo_in=float(c[1]),vo_out=float(c[2]),type=c[3],requested=c[4],move=c[5],beat=c[6],notes=c[7]))
assets={'1':'open/PIA00254.jpg','2':'open/PIA00106.jpg','3':'open/PIA00240.jpg','4':'open/PIA00241.jpg','5':'open/PIA00087.jpg','6':'open/PIA23791.jpg','7':'open/PIA00104.jpg','8':'open/PIA00104.jpg','11a':'open/PIA23791.jpg','11b':'open/PIA00240.jpg','12a':'earth/as17-148-22727.jpg','12b':'open/PIA00104.jpg','13a':'sdo/AIA171VenusTransit_HD1080.mp4','13b':'sdo/AIA171VenusTransit_HD1080.mp4','14b':'open/PIA00104.jpg','15a':'open/PIA00106.jpg','15b':'magellan_extra/PIA00215.jpg','16a':'open/PIA00240.jpg','16b':'magellan_extra/PIA00159.jpg','17':'magellan_extra/PIA00246.jpg','18':'open/PIA00087.jpg'}
words=json.loads((EP/'02_Voiceover/words.json').read_text())['words']

visual=[]
for r in rows:
 if r['row'] in ['9','10']:continue
 r['source_file']=str(EP/'04_Generated-Clips/01_Raw/graphics_v01/albedo.mp4') if r['row'] in ['13c','14a'] else str(HERE/'nasa_pool_v01'/assets[r['row']])
 end=43.58 if r['row']=='8' else r['vo_out']
 n=2 if r['row']=='17' else 3 if r['row']=='18' else 1
 for k in range(n):
  q=dict(r);q.update(timeline_in=r['vo_in']+(end-r['vo_in'])*k/n,timeline_out=r['vo_in']+(end-r['vo_in'])*(k+1)/n,part=k+1);visual.append(q)

# v01 picture boundaries that stand.
KEEP={('4','5'):20.54,('6','7'):29.58,('7','8'):35.58,('12b','13a'):66.80,('14a','15a'):None}
# v02 fixes: cut on the first frame after the clipped word ends, inside the gap before the next word.
# v03: 2->3 and 13c->14a sit in the pause before the sentence, placed so the 0.4 s xfade ends before
# "Because" (10.76) and "Venus" (83.84); "radar?" ends 10.18 and "number." ends 82.84.
FIX={('2','3'):316/FPS,('11a','11b'):fr(49.40),('13a','13b'):fr(72.567),('13c','14a'):2509/FPS,('14b','15a'):fr(96.267),('15a','15b'):102.80,('16a','16b'):fr(115.10)}
new=[]
for v in visual:
 r=v['row']
 if r=='8':
  v.update(timeline_in=35.58,timeline_out=39.58);new.append(dict(v));v=dict(v);v.update(timeline_in=39.58,timeline_out=43.58,part=2)
 if r=='14a':v['timeline_out']=90.00
 new.append(v)
visual=new
for (a,b),t in list(KEEP.items())+list(FIX.items()):
 if t is None:continue
 for v in visual:
  if v['row']==a and v is [x for x in visual if x['row']==a][-1]:v['timeline_out']=t
  if v['row']==b and v is [x for x in visual if x['row']==b][0]:v['timeline_in']=t
for v in visual:
 v['timeline_in']=fr(v['timeline_in']);v['timeline_out']=fr(v['timeline_out'])
for a,b in zip(visual,visual[1:]):assert abs(a['timeline_out']-b['timeline_in'])<1e-6,(a['row'],b['row'])
row_in={v['row']:v['timeline_in'] for v in visual if v['part']==1}
OFFSET={'13a':8.0,'13b':8.0+(row_in['13b']-row_in['13a']),'14a':row_in['14a']-row_in['13c']}

WORK.mkdir(parents=True,exist_ok=True);PACK.mkdir(parents=True,exist_ok=True)
card=Image.new('RGBA',(1920,1080),(0,0,0,0));draw=ImageDraw.Draw(card);draw.rounded_rectangle((90,860,1000,990),radius=15,fill=(23,36,55,220));draw.text((125,886),'The Twin Next Door',font=ImageFont.truetype(FONT,62),fill='white');card.save(WORK/'chapter.png')
v02_cuts=json.loads(V02_CUTS.read_text())
crops={}
if '--finish-only' not in sys.argv:
 for i,r in enumerate(visual):
  start=r['timeline_in'];end=r['timeline_out']; pre=.2 if i else 0;post=.2 if i<len(visual)-1 else 0
  dur=end-start+pre+post; frames=round(dur*FPS); dest=WORK/f'row_{i:02}.mp4';r['render']=str(dest)
  src=Path(r['source_file']);print('row',r['row'],r['part'],start,end,flush=True)
  old=v02_cuts[i] if i<len(v02_cuts) else {}
  if (src.name not in CROP_CLEAR and (V02_WORK/f'row_{i:02}.mp4').exists() and old.get('row')==r['row'] and old.get('part')==r['part']
      and abs(old['timeline_in']-start)<1e-6 and abs(old['timeline_out']-end)<1e-6):
   shutil.copy2(V02_WORK/f'row_{i:02}.mp4',dest);print('  reuse v02 render',flush=True);continue
  if src.suffix.lower()=='.jpg':
   im=Image.open(src).convert('RGB')
   if src.name=='PIA23791.jpg':im=im.crop((1145,0,2245,1096))
   zoom=1.1
   if src.name in CROP_CLEAR:
    box=clear_box(im);im=im.crop(box);zoom=1.0
    crops[src.name]=dict(box=box,width=box[2]-box[0],upscale_end=round(1920*1.06/(box[2]-box[0]),3))
   scale=max(1920/im.width,1080/im.height)
   im=ImageEnhance.Color(im).enhance(1.10);im=ImageEnhance.Contrast(im).enhance(1.04)
   im=im.point([min(255,int(v*.92+28)) for v in range(256)]*3)
   if zoom==1.0:im=im.resize((2112,1188),Image.Resampling.LANCZOS)
   else:im=im.resize((round(im.width*scale*zoom),round(im.height*scale*zoom)),Image.Resampling.LANCZOS)
   x=(im.width-2112)//2;y=(im.height-1188)//2;im=im.crop((max(0,x),max(0,y),max(0,x)+2112,max(0,y)+1188))
   plate=WORK/f'plate_{i:02}.png';im.save(plate)
   pct=.06 if '6%' in r['move'] else .05
   if r['part']>1:pct=.06
   vf=f"scale=3840:2160,zoompan=z='1+{pct}*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={frames}:s=1920x1080:fps=30,setsar=1,format=yuv420p"
   inp=['-i',plate]
  else:
   offset=OFFSET.get(r['row'],0)
   inp=['-ss',max(0,offset-pre),'-i',src]
   vf='scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,setsar=1,format=yuv420p'
  if r['row']=='11a':
   a=43.74-start+pre;b=a+2.5
   run([*inp,'-loop','1','-i',WORK/'chapter.png','-filter_complex',f"[0:v]{vf}[base];[base][1:v]overlay=enable='between(t,{a},{b})',format=yuv420p[v]",'-map','[v]','-t',f'{frames/FPS:.6f}','-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4',dest])
  else:run([*inp,'-vf',vf,'-t',f'{frames/FPS:.6f}','-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4',dest])
 chunks=[]
 for i,r in enumerate(visual):
  p=Path(r['render']);length=probe(p); pre=.2 if i else 0
  center=WORK/f'center_{i:02}.mp4';cd=(r['timeline_out']-r['timeline_in'])-(.2 if i else 0)-(.2 if i<len(visual)-1 else 0)
  run(['-ss',pre+(.2 if i else 0),'-i',p,'-frames:v',round(cd*FPS),'-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4',center]);chunks.append(center)
  if i<len(visual)-1:
   nxt=Path(visual[i+1]['render']); trans=WORK/f'trans_{i:02}.mp4'
   run(['-ss',length-.4,'-i',p,'-i',nxt,'-filter_complex','[0:v]setpts=PTS-STARTPTS[a];[1:v]trim=duration=0.4,setpts=PTS-STARTPTS[b];[a][b]xfade=transition=fade:duration=0.4:offset=0,format=yuv420p[v]','-map','[v]','-frames:v',12,'-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4',trans]);chunks.append(trans)
 (WORK/'concat.txt').write_text(''.join(f"file '{p}'\n" for p in chunks))
 run(['-f','concat','-safe','0','-i',WORK/'concat.txt','-c','copy',WORK/'picture.mp4'])
 run(['-i',WORK/'picture.mp4','-i',V01,'-map','0:v','-map','1:a','-c','copy','-t',TOTAL,'-movflags','+faststart',OUT])

runtime=probe(OUT)
def audio_md5(p):
 return sp.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(p),'-map','0:a','-c','copy','-f','md5','-'],text=True).strip()
same_audio=audio_md5(OUT)==audio_md5(V01)
ll=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
lufs=float(re.findall(r'I:\s*([-\d.]+) LUFS',ll)[-1])
checks=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-vf','blackdetect=d=0.1:pix_th=0.10:pic_th=0.98,freezedetect=n=-50dB:d=1','-an','-f','null','-'],capture_output=True,text=True).stderr
(PACK/'ffmpeg_checks.txt').write_text(checks)

# clip_check CSV: each row's words are the VO words whose midpoint falls inside its picture span.
csv_rows=[]
spans=[]
for r in rows:
 rel=[v for v in visual if v['row']==r['row']]
 if r['row']=='9':spans.append((r['row'],'BREATH',42.88,43.58,'[breath]'));continue
 if r['row']=='10':spans.append((r['row'],'CARD',43.74,46.24,'[card] The Twin Next Door'));continue
 spans.append((r['row'],'CODE' if r['row'] in ['13c','14a'] else 'NASA',rel[0]['timeline_in'],rel[-1]['timeline_out'],None))
import csv,io
buf=io.StringIO();wr=csv.writer(buf);wr.writerow(['row','source','vo_in','vo_out','vo_text'])
for row,src,a,b,text in spans:
 if text is None:text=' '.join(w['text'] for w in words if a<=(w['start']+w['end'])/2<b)
 wr.writerow([row,src,f'{a:.3f}',f'{b:.3f}',text])
(PACK/'venus_part01_v03_assembled.csv').write_text(buf.getvalue())
(PACK/'venus_words_list.json').write_text(json.dumps(words))
cc=sp.run([sys.executable,str(CLIP_CHECK),str(PACK/'venus_part01_v03_assembled.csv'),'--words',str(PACK/'venus_words_list.json')],capture_output=True,text=True)
(PACK/'clip_check_py.txt').write_text(cc.stdout+cc.stderr)

def sheet(name,times):
 board=Image.new('RGB',(1440,600),(18,18,22));d=ImageDraw.Draw(board)
 for i,t in enumerate(times):
  p=WORK/f'frame_{name}_{i}.jpg';run(['-ss',t,'-i',OUT,'-frames:v','1','-vf','scale=480:270',p]);x=i%3*480;y=i//3*300;board.paste(Image.open(p),(x,y));d.text((x+8,y+275),f'{t:.2f}s',fill='white')
 board.save(PACK/(name+'.jpg'),quality=92)
sheet('frame0_sheet',[0,.2,.4,.6,.8,1])
sheet('sheet_095_120',[95+25*i/5 for i in range(6)])
sheet('sheet_plates_v03',[13.0,52.0,104.0,108.5,110.5,113.5])
sheet('sheet_cuts_v03',[10.25,10.80,11.20,83.40,83.90,84.30])
h=hashlib.sha256()
with OUT.open('rb') as f:
 for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
(PACK/'SHA256.txt').write_text(f'{h.hexdigest()}  {OUT.name}\n')
(PACK/'cuts_v03.json').write_text(json.dumps([dict(row=v['row'],part=v['part'],timeline_in=v['timeline_in'],timeline_out=v['timeline_out'],duration=round(v['timeline_out']-v['timeline_in'],3),source=Path(v['source_file']).name) for v in visual],indent=2))
(PACK/'crops_v03.json').write_text(json.dumps(crops,indent=2))
print(json.dumps(dict(out=str(OUT),sha256=h.hexdigest(),runtime=runtime,lufs=lufs,audio_identical_to_v01=same_audio,clip_check_exit=cc.returncode,crops=crops),indent=1))
print(cc.stdout+cc.stderr)
