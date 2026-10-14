#!/usr/bin/env python3
"""025 Could a Robot Survive on Mars? full rough v03c (J0063: Claude's v03b sheet pass: row 16 PIA12490 cropped between its green annotation
boxes, row 27 PIA25739 right half -> PIA18093 left side (clear sky over the rim, its second use, new framing), PIA19400 at 201 s
reviewed_ok against the fill gate; unchanged segments reused from the v03b work dir). v03b (J0062: Claude's v03 review, #6066558180: row 16 PIA25739 left half -> PIA19400
tight on the sun and ridge (its second use, new framing), row 27 PIA24593 cropped inside the two blue rotor discs and kept as reviewed_ok
against the polish floor, polish gate gutter/noise tweaks; unchanged segments reused from the v03 work dir). v03 (J0058: Claude's sheet review of v02d, #6066030404: swaps for unfinished-looking frames, sub-pixel pushes, polish gate). v02 (J0055: Claude on v01, every frame fills 16:9, no text plates, no static holds, rows 28/30), built on 024 _assemble_light_speed_full_v03.py with its rules:
- <=2 uses per still, the second at a new framing; reuse count per source printed and written to the pack.
- Upscale (source px -> 1080p, push included) recorded per row and asserted <= 2.35.
- Every cut snapped to a VO pause (words.json); no shot held longer than 6 s except the row 32 bookend.
- Frame 0 is the Opportunity Legacy Pan (PIA22909), already panning; row 32 returns to it at a new stretch, still panning, to the end.
- No whole-globe Mars anywhere; NASA plates from nasa_pool_v01 minus the three drops in _evidence/mars_robot_pool_check_v01.json
  (PIA26147, PIA10664, PIA06263); PIA15689 (false colour, on hold) is not used.
- Omni takes trimmed to Claude's J0050 spans: cold 4.0-9.0 s (row 13 into 14), wheel 0.5-8.5 s (row 25, cut at <=6 s); audio stripped.
- Shot list: SHOT_LIST_v02.md (32 rows). Each row's cuts are spread evenly over the row and snapped to the nearest VO pause.
Locked VO untouched, house bed full runtime, hold 2.5 s past the last word, then 1 s fade, -14 LUFS.
`--plan` prints the segment list, reuse counts and checks without rendering."""
from pathlib import Path
import json, subprocess as sp, re, hashlib, math, sys, csv, io
from collections import Counter
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fillbox import best_box, border_fill_fraction
Image.MAX_IMAGE_PIXELS = None
HERE=Path(__file__).resolve().parent; EP=HERE.parent
UAT=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/OWB UAT'
WORK=Path('/private/tmp/mars025_full_work_v03c'); PACK=HERE/'full_rough_v03c_pack'
VO=EP/'02_Voiceover/mars_robot_vo_v01.mp3'
OUT=UAT/'025_MarsRobot_full_rough_v03c.mp4'
MAX_UP=2.35; MAX_HOLD=6.0
H=HERE/'nasa_pool_v01'
OM=EP/'04_Generated-Clips/01_Raw/omni_v01'
FPS=30; LAST_WORD=486.704; HOLD=2.5; FADE=1.0; TOTAL=round((LAST_WORD+HOLD+FADE)*FPS)/FPS
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
CLIP_CHECK=EP.parents[1]/'00_Brand/Channel-Setup/tools/clip_check.py'
POLISH=EP.parents[1]/'scripts/polish_gate.py'
PLAN='--plan' in sys.argv
words=json.loads((EP/'02_Voiceover/words.json').read_text())['words']

def run(args):
 p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-6000:])
def probe(p):return float(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
def fr(t):return round(t*FPS)/FPS

if not PLAN:
 # iCloud evicts/locks OWB UAT files mid-run, so read the bed from a local copy.
 BED=WORK/'bed_jupiter-music.mp3'
 if not BED.exists():
  import shutil, time
  WORK.mkdir(parents=True,exist_ok=True)
  for _ in range(10):
   sp.run(['brctl','download',str(UAT/'jupiter-music.mp3')])
   try: shutil.copyfile(UAT/'jupiter-music.mp3',BED); break
   except OSError: time.sleep(6)

Q={'tl':(0.0,0.0),'tr':(0.5,0.0),'bl':(0.0,0.5),'br':(0.5,0.5),'c':(0.25,0.25)}
PAN='rovers_wait/PIA24765.jpg';PAN_BOX=(0.095,0.12,0.965,0.57)
FILL_MAX=0.015
SCENE='scene content, not an empty edge (Claude, thread #6064654610)'
REVIEWED_OK={'PIA17792.jpg':SCENE,'PIA20316.jpg':SCENE,'PIA26016.jpg':SCENE+'; pass unless the sheet shows a straight black/white edge','PIA23177.jpg':SCENE+'; pass unless the sheet shows a straight black/white edge',
 'PIA20328.jpg':'reviewed_ok only if the 16:9 window stays inside the tilted mosaic: no corner wedge at any point of the push (Claude, #6064654610)',
 'PIA22210.jpg':'reviewed_ok only if cropped above the stair-stepped bottom edge at <=2.35x, else drop (Claude, #6064654610)',
 'PIA24264.jpg':'reviewed_ok only if cropped above the black distorted base: sky and horizon, deck top at most (Claude, #6064654610)',
 'PIA07372.jpg':'scene content (rover deck), Claude #6066030404','PIA13804.jpg':'scene content (lander deck), Claude #6066030404',
 'PIA19400.jpg':'the dark ridge is scene (Claude, J0063 v03b sheet pass)'}
POLISH_OK={'PIA24593.jpg':dict(note="Ingenuity's shadow, cropped clear of the blue rotor disc; reviewed_ok against the floor (Claude, #6066558180)",kinds=['low detail']),
 'PIA22520.jpg':dict(note='dust haze of the storm that ended Opportunity: the haze is the point (Claude, #6066558180)',kinds=['split panel','low detail'])}
COLD=OM/'orbit_mars_cold_omni_v01.mp4'; WHEEL=OM/'orbit_mars_wheel_omni_v01.mp4'
def v(at,**k):return dict(video=1,at=at,**k)
c=dict(quad='c')
# (row, VO in from SHOT_LIST_v02, [sources]); a source is a pool path or (path, opts). One cut per source.
ROWS=[
 ('1',0.12,[(PAN,dict(pan=(0.0,0.30),box=PAN_BOX))]),
 ('2',6.08,['opp_deck/PIA07372.jpg']),
 ('3',10.48,['gale_desert/PIA22210.jpg','gale_desert/PIA21268.jpg']),
 ('4',19.08,['frost/PIA11132.jpg','opp_deck/PIA15115.jpg']),
 ('5',26.28,[('gale_desert/PIA20284.jpg',dict(box=(0.0,0.05,0.35,0.95))),'dust/PIA17759.jpg','open_pan/PIA19109.jpg','open_pan/PIA18098.jpg']),
 ('6',41.26,['gale_desert/PIA20283.jpg','gale_desert/PIA20284.jpg']),
 ('7',51.08,['viking/PIA00382.jpg','viking/PIA10738.jpg','gale_desert/PIA25413.jpg']),
 ('8',66.88,['radiation/PIA13580.jpg','gale_desert/PIA26559.jpg','gale_desert/PIA25176.jpg','rovers_wait/PIA22207.jpg']),
 ('9',82.80,['rover_work/PIA16096.jpg','rover_work/PIA20316.jpg','rover_work/PIA24543.jpg','rover_work/PIA23240.jpg']),
 ('10',98.06,['dust/PIA11798.jpg','spirit/PIA12457.jpg','wheel/PIA21486.jpg']),
 ('11',111.50,['dsn/PIA17792.jpg','dsn/PIA23214.jpg','rovers_wait/PIA25681.jpg','dsn/PIA26717.jpg']),
 ('12',133.76,['spirit/PIA09090.jpg','dusk_plain/PIA15024.jpg','dusk_plain/PIA26673.gif']),
 ('13',144.96,['spirit/PIA07882.jpg','open_pan/PIA20328.jpg',('dusk_plain/PIA19400.jpg',dict(pct=0.12)),(COLD,v(4.0,max=5.0,push=0.05))]),
 ('14',161.40,[('spirit/PIA12142.jpg',dict(box=(0.68,0.28,0.873,0.86))),('spirit/PIA12203.jpg',dict(quad='tl')),'spirit/PIA12337.jpg','spirit/PIA12203.jpg',('spirit/PIA07882.jpg',c)]),
 ('15',186.38,['spirit/PIA07371.jpg','spirit/PIA01907.jpg','tracks/PIA16933.jpg']),
 ('16',199.44,[('dusk_plain/PIA19400.jpg',dict(box=(0.05,0.36,0.70,0.815))),'phoenix/PIA13804.jpg','phoenix/PIA10665.jpg',('phoenix/PIA12490.jpg',dict(box=(0.12,0.232,0.8645,0.5653))),('phoenix/PIA13804.jpg',c)]),
 ('17',225.06,['rover_work/PIA24542.jpg','rovers_wait/PIA24264.jpg']),
 ('18',231.68,['open_pan/PIA18093.jpg','open_pan/PIA16122.jpg']),
 ('19',239.06,['dust/PIA10128.jpg','dust/PIA11799.jpg','dust/PIA20329.jpg']),
 ('20',254.80,['dust/PIA07458.jpg','dust/PIA06739.jpg',('dust/PIA18079.jpg',dict(box=(0.15,0.15,0.85,0.78))),('dust/PIA17759.jpg',c)]),
 ('21',275.08,[('power/PIA22330.jpg',dict(box=(0.505,0.0,1.0,1.0))),('dust/PIA18079.jpg',dict(quad='tl')),('storm2018/PIA22520.jpg',dict(box=(0.505,0.12,1.0,1.0))),'dsn/PIA26716.jpg',('storm2018/PIA22520.jpg',dict(box=(0.0,0.12,0.495,1.0)))]),
 ('22',299.32,[('opp_deck/PIA07372.jpg',c),'open_pan/PIA22928.jpg']),
 ('23',308.44,['insight/PIA23203.jpg','insight/PIA25286.jpg','insight/PIA23177.jpg','insight/PIA22871.jpg','insight/PIA25287.jpg']),
 ('24',331.50,['power/PIA23305.jpg','power/PIA23306.jpg','power/PIA22486.jpg',('power/PIA22486.jpg',c)]),
 ('25',351.20,['wheel/PIA17751.jpg','wheel/PIA26016.jpg',(WHEEL,v(0.5)),'wheel/PIA15693.jpg','wheel/PIA16112.jpg']),
 ('26',373.78,['launch_edl/KSC-20200730-PH-FMX01_0042.jpg','launch_edl/KSC-20200730-PH-KLS01_0001.jpg','launch_edl/PIA24333.jpg','launch_edl/PIA14839.jpg']),
 ('27',391.26,[('ingenuity/PIA24593.jpg',dict(box=(0.08,0.42,0.92,1.0))),('open_pan/PIA18093.jpg',dict(box=(0.05,0.0,0.305,0.62))),'ingenuity/PIA26236.jpg','ingenuity/PIA26237.jpg','ingenuity/PIA26243.jpg']),
 ('28',417.12,[('power/PIA23305.jpg',c),('spirit/PIA01907.jpg',c),('wheel/PIA19920.jpg',c),'rovers_wait/PIA26344.jpg',('rovers_wait/PIA24264.jpg',c)]),
 ('29',439.56,['tracks/PIA23246.jpg','tracks/PIA14129.jpg','tracks/PIA17590.jpg']),
 ('30',451.88,['power/KSC-2011-6687.jpg',('spirit/PIA09090.jpg',c),'wheel/PIA19920.jpg',('rover_work/PIA20316.jpg',c)]),
 ('31',472.66,['tracks/PIA15694.jpg',('spirit/PIA07371.jpg',c)]),
 ('32',483.80,[(PAN,dict(pan=(0.62,0.90),box=PAN_BOX,hold_ok=1,bookend=1))]),
]
CHAPTERS=[("A Desert That Isn't",41.26),('The Cold',133.76),('The Dust',231.68),('Wear and Tear',331.50),('What It Takes',417.12)]

GAPS=[((a['end']+b['start'])/2,b['start']-a['end']) for a,b in zip(words,words[1:])]
def snap(t):
 """Midpoint of the nearest VO pause (>=0.30 s, else >=0.20 s, else >=0.10 s) within 2 s, then 3.5 s; past the last word, keep t."""
 if t>LAST_WORD:return t
 for reach in (2.0,3.5):
  for need in (0.30,0.20,0.10):
   cands=[m for m,g in GAPS if g>=need and abs(m-t)<=reach]
   if cands:return min(cands,key=lambda m:abs(m-t))
 raise SystemExit(f'no VO pause near {t}')

# Row starts sit in the pause before each row's first word. Inside a row, each cut goes to the VO pause nearest an even
# split of what is left, keeping every hold between 1.8 s and 6 s (or the source's own max, e.g. an Omni span).
PAUSES=dict(sorted((m,g) for m,g in GAPS if g>=0.06))
def sentence_end(t):
 c=[((a['end']+b['start'])/2) for a,b in zip(words,words[1:]) if b['start']-a['end']>=0.25 and a['text'].rstrip().endswith(('.','?','!')) and abs((a['end']+b['start'])/2-t)<=1.5]
 return min(c,key=lambda m:abs(m-t)) if c else None
SENT_ROWS=('29','31');SENT_NOTE={}
starts=[0.0]
for r,t,_ in ROWS[1:]:
 m=sentence_end(t-0.3) if r in SENT_ROWS else None
 if r in SENT_ROWS:SENT_NOTE[r]=dict(shot_list=t,moved_to=m) if m else dict(shot_list=t,kept_between_words=snap(t-0.3))
 starts.append(m if m else snap(t-0.3))
ends=starts[1:]+[TOTAL]
segs=[]
for (row,_,srcs),a,b in zip(ROWS,starts,ends):
 srcs=[s if isinstance(s,tuple) else (s,{}) for s in srcs]
 n=len(srcs)
 caps=[min(MAX_HOLD,o.get('max',MAX_HOLD)) for _,o in srcs]
 if row=='32':caps[-1]=99
 cand=[m for m in PAUSES if a+1.8<=m<=b-1.8]
 # best[k][m]: lowest cost with cut k at pause m (cost = squared distance from the even split, small pauses penalised)
 even=[a+(b-a)*k/n for k in range(n)]
 best={0:{a:(0.0,None)}}
 for k in range(1,n):
  best[k]={}
  for m in cand:
   for prev,(cost,_) in best[k-1].items():
    if 1.8<=m-prev<=caps[k-1]:
     c=cost+(m-even[k])**2+(0.4 if PAUSES[m]<0.10 else 0)
     if m not in best[k] or c<best[k][m][0]:best[k][m]=(c,prev)
 last={m:v for m,v in best[n-1].items() if 1.8<=b-m<=caps[n-1]}
 if not last:raise SystemExit(f'row {row} ({a:.2f}-{b:.2f}): no pause plan for {n} cuts')
 m=min(last,key=lambda x:last[x][0]);cuts=[m]
 for k in range(n-1,0,-1):m=best[k][m][1];cuts.append(m)
 for (src,o),tin in zip(srcs,reversed(cuts)):
  segs.append(dict(row=row,timeline_in=fr(tin),src=src if isinstance(src,Path) else H/src,o=dict(o)))
for a,b in zip(segs,segs[1:]):a['timeline_out']=b['timeline_in']
segs[-1]['timeline_out']=TOTAL
for s in segs:
 if s['o'].get('video'):s['o']['offset']=s['o'].get('at',0.0)
SPANS={COLD.name:(4.0,9.0),WHEEL.name:(0.5,8.5)}

FILL_CACHE={}
def framed(s):
 im=Image.open(s['src']).convert('RGB');o=s['o']
 if 'box' not in o and not o.get('pan'):
  fb=FILL_CACHE.get((s['src'],framing(o)))
  if fb is None:
   fb=best_box(im,min_h_px=1) or (0,0,1,1)
   # bright-sky plates: if the filled box alone needs more than the cap (after quad halving and the push), widen it
   # around its centre to the smallest 16:9 crop the cap allows, clamped to the image
   need=1080*(1+o.get('pct',.05))/(MAX_UP-0.02)*(2 if 'quad' in o else 1)
   if (fb[3]-fb[1])*im.height<need:
    h=min(im.height,need);w=min(im.width,h*16/9);h=min(h,w*9/16)
    cx=(fb[0]+fb[2])/2*im.width;cy=(fb[1]+fb[3])/2*im.height
    x0=min(max(0,cx-w/2),im.width-w);y0=min(max(0,cy-h/2),im.height-h)
    fb=(x0/im.width,y0/im.height,(x0+w)/im.width,(y0+h)/im.height)
   FILL_CACHE[(s['src'],framing(o))]=fb
  im=im.crop((round(im.width*fb[0]),round(im.height*fb[1]),round(im.width*fb[2]),round(im.height*fb[3])))
 if 'box' in o:
  x0,y0,x1,y1=o['box'];im=im.crop((int(im.width*x0),int(im.height*y0),int(im.width*x1),int(im.height*y1)))
 if 'quad' in o:
  fx,fy=Q[o['quad']];im=im.crop((int(im.width*fx),int(im.height*fy),int(im.width*(fx+.5)),int(im.height*(fy+.5))))
 return im
def vsize(p):return tuple(map(int,sp.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0',str(p)],text=True).strip().split(',')[:2]))
def upscale(s):
 o=s['o']
 if o.get('video'):
  w,h=vsize(s['src'])
  if o.get('vcrop'):w,h=o['vcrop'][2:]
  return w,max(1920/w,1080/h)
 im=framed(s)
 if o.get('pan'):return im.width,1080/im.height
 return im.width,max(1920/im.width,1080/im.height)*(1+o.get('pct',.05))
def framing(o):return (o.get('quad'),o.get('box'),o.get('pan'))

# ---- checks: reuse <= 2 per still with a different framing, holds <= 6 s, cuts in VO pauses, upscale <= 2.35,
# Omni inside Claude's spans, video spans inside the source
stills=[s for s in segs if not s['o'].get('video')]
reuse=Counter(s['src'].name for s in stills)
vreuse=Counter(s['src'].name for s in segs if s['o'].get('video'))
problems=[]
for name,n in reuse.items():
 uses=[s for s in stills if s['src'].name==name]
 if n>2:problems.append(f'{name} used {n}x')
 if n==2 and framing(uses[0]['o'])==framing(uses[1]['o']):problems.append(f'{name} second use has the same framing')
dur_cache={}
for s in segs:
 d=s['timeline_out']-s['timeline_in']
 if d<1.8:problems.append(f"{s['row']} {s['timeline_in']} only {d:.2f}s")
 if d>MAX_HOLD+0.05 and not s['o'].get('hold_ok'):problems.append(f"{s['row']} {s['timeline_in']} {s['src'].name} held {d:.2f}s")
 if s['src'].name in SPANS and s['o']['offset']+d>SPANS[s['src'].name][1]+0.05:problems.append(f"{s['row']} {s['src'].name} runs past Claude's span to {s['o']['offset']+d:.2f}s")
 if s['o'].get('video') and s['src'].exists():
  L=dur_cache.setdefault(s['src'],probe(s['src']))
  if s['o']['offset']+d>L+0.5:problems.append(f"{s['row']} {s['src'].name} runs {s['o']['offset']+d-L:.2f}s past its end")
for s in segs[1:]:
 t=s['timeline_in']
 near=[w for w in words if w['start']+0.02<t<w['end']-0.02]
 if near:problems.append(f"cut {t:.2f} ({s['row']}) inside '{near[0]['text']}' {near[0]['start']:.2f}-{near[0]['end']:.2f}")
for s in segs:
 if not s['src'].exists():problems.append(f'missing {s["src"]}');continue
 s['src_w'],s['upscale']=upscale(s);s['upscale']=round(s['upscale'],3)
 if s['upscale']>MAX_UP:problems.append(f"{s['row']} {s['src'].name} upscale {s['upscale']:.2f} > {MAX_UP}")
assert all(s.get('upscale',0)<=MAX_UP for s in segs) or problems
print('reuse (stills):',dict(sorted(reuse.items(),key=lambda x:-x[1])))
print('reuse (video):',dict(sorted(vreuse.items(),key=lambda x:-x[1])))
if PLAN or problems:
 for s in segs:print(f"{s['row']:>4} {s['timeline_in']:8.2f} {s['timeline_out']-s['timeline_in']:5.2f}  {s['src'].name[:44]:44} up {s.get('upscale',0):4.2f} {json.dumps({k:v for k,v in s['o'].items() if k not in('fixed','video','at')})}")
 print('segments:',len(segs),'runtime',TOTAL)
 print('problems:',problems or 'none')
 raise SystemExit(1 if problems else 0)

def prep_still(s,dest):
 im=framed(s)
 im=ImageEnhance.Color(im).enhance(1.06);im=ImageEnhance.Contrast(im).enhance(1.04)
 scale=max(2112/im.width,1188/im.height)
 im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 x=(im.width-2112)//2;y=(im.height-1188)//2;im.crop((x,y,x+2112,y+1188)).save(dest)

def subpixel(im,box,frames,dest):
 # Float crop boxes resampled per frame, so a push or pan moves smoothly instead of stepping whole pixels (Ben's 'wobbly' on 023).
 p=sp.Popen(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-',
  '-vf','setsar=1,format=yuv420p','-frames:v',str(frames),*map(str,ENC),str(dest)],stdin=sp.PIPE)
 for n in range(frames):p.stdin.write(im.resize((1920,1080),Image.Resampling.BICUBIC,box=box(n)).tobytes())
 p.stdin.close()
 if p.wait():raise RuntimeError(f'subpixel render failed: {dest}')

WORK.mkdir(parents=True,exist_ok=True);PACK.mkdir(parents=True,exist_ok=True)
ENC=['-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4']
def okkey(s):return json.dumps([s['timeline_in'],s['timeline_out'],str(s['src']),s['o']],default=str,sort_keys=True)
V01_CACHE={}
for ok in Path('/private/tmp/mars025_full_work_v03b').glob('seg_*.ok'):V01_CACHE[ok.read_text()]=ok.with_suffix('.mp4')
if '--finish-only' not in sys.argv:
 for i,s in enumerate(segs):
  pre=.2 if i else 0;post=.2 if i<len(segs)-1 else 0
  frames=round((s['timeline_out']-s['timeline_in']+pre+post)*FPS);dest=WORK/f'seg_{i:03}.mp4'
  if dest.exists() and (WORK/f'seg_{i:03}.ok').exists() and (WORK/f'seg_{i:03}.ok').read_text()==okkey(s):
   print('reuse',i,s['row'],flush=True);continue
  old=V01_CACHE.get(okkey(s)) if (i and i<len(segs)-1) else None
  if old and old.exists():
   import shutil;shutil.copyfile(old,dest);(WORK/f'seg_{i:03}.ok').write_text(okkey(s))
   print('reuse cached',i,s['row'],old,flush=True);continue
  print('seg',i,s['row'],s['timeline_in'],s['timeline_out'],s['src'].name,flush=True)
  o=s['o']
  if o.get('video'):
   off=o['offset'];vc=o.get('vcrop')
   push=(f",scale=w='2*trunc(960*(1+{o['push']}*t/{frames/FPS:.3f}))':h=-2:eval=frame,crop=1920:1080" if o.get('push') else '')
   vf=(f'crop={vc[2]}:{vc[3]}:{vc[0]}:{vc[1]},' if vc else '')+'scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30'+push+',setsar=1,tpad=stop_mode=clone:stop_duration=2'
   run(['-ss',max(0,off-pre),'-i',s['src'],'-vf',vf+',format=yuv420p','-frames:v',frames,*ENC,dest])
  elif o.get('pan'):
   # Panorama at 1080 px high; the 1920 window slides across the given fraction of its width, moving from frame 0.
   im=framed(s);sc=1080/im.height;im=im.resize((round(im.width*sc),1080),Image.Resampling.LANCZOS)
   im=ImageEnhance.Color(im).enhance(1.06);im=ImageEnhance.Contrast(im).enhance(1.04)
   x0,x1=(f*(im.width-1920) for f in o['pan'])
   subpixel(im,lambda n:(x0+(x1-x0)*n/frames,0.0,x0+(x1-x0)*n/frames+1920,1080.0),frames,dest)
  else:
   plate=WORK/f'plate_{i:03}.png';prep_still(s,plate);pct=o.get('pct',.05);im=Image.open(plate).convert('RGB')
   def box(n,W=im.width,H=im.height):
    z=1+pct*n/frames;w,h=W/z,H/z;return ((W-w)/2,(H-h)/2,(W+w)/2,(H+h)/2)
   subpixel(im,box,frames,dest)
  got=round(probe(dest)*FPS)
  if got<frames-1:raise RuntimeError(f'seg {i} {s["row"]}: {got} frames < {frames}')
  (WORK/f'seg_{i:03}.ok').write_text(okkey(s))
 chunks=[]
 for i,s in enumerate(segs):
  p=WORK/f'seg_{i:03}.mp4';pre=.2 if i else 0
  center=WORK/f'center_{i:03}.mp4';cd=(s['timeline_out']-s['timeline_in'])-(.2 if i else 0)-(.2 if i<len(segs)-1 else 0)
  run(['-ss',pre+(.2 if i else 0),'-i',p,'-frames:v',round(cd*FPS),*ENC,center]);chunks.append(center)
  if i<len(segs)-1:
   nxt=WORK/f'seg_{i+1:03}.mp4';trans=WORK/f'trans_{i:03}.mp4';length=probe(p)
   run(['-ss',length-.4,'-i',p,'-i',nxt,'-filter_complex','[0:v]setpts=PTS-STARTPTS[a];[1:v]trim=duration=0.4,setpts=PTS-STARTPTS[b];[a][b]xfade=transition=fade:duration=0.4:offset=0,format=yuv420p[v]','-map','[v]','-frames:v',12,*ENC,trans]);chunks.append(trans)
 (WORK/'concat.txt').write_text(''.join(f"file '{p}'\n" for p in chunks))
 run(['-f','concat','-safe','0','-i',WORK/'concat.txt','-c','copy',WORK/'picture_raw.mp4'])

 # Chapter lower-thirds (2.5 s from the chapter's first word) and the 4 s subscribe cue under the subscribe line.
 def first_word(t):return next(w['start'] for w in words if w['start']>=t-0.5)
 font=ImageFont.truetype(FONT,62);ov=[]
 for k,(title,t) in enumerate(CHAPTERS):
  w=int(font.getlength(title))+70;img=Image.new('RGBA',(1920,1080),(0,0,0,0));d=ImageDraw.Draw(img)
  d.rounded_rectangle((90,860,90+w,990),radius=15,fill=(23,36,55,220));d.text((125,886),title,font=font,fill='white')
  p=WORK/f'card_{k}.png';img.save(p);a=first_word(t);ov.append((p,a,a+2.5))
 sub_at=next(w['start'] for w in words if w['text'].startswith('Subscribing'))
 img=Image.new('RGBA',(1920,1080),(0,0,0,0));d=ImageDraw.Draw(img);f2=ImageFont.truetype(FONT,44)
 d.rounded_rectangle((1440,900,1830,990),radius=45,fill=(204,0,0,235));d.text((1500,918),'SUBSCRIBE',font=f2,fill='white')
 p=WORK/'subscribe.png';img.save(p);ov.append((p,sub_at,sub_at+4.0))
 inputs=['-i',WORK/'picture_raw.mp4'];fc='[0:v]null[v0];'
 for k,(p,a,b) in enumerate(ov):
  inputs+=['-loop','1','-t',TOTAL,'-i',p]
  fc+=f"[{k+1}:v]fade=t=in:st={a:.3f}:d=0.25:alpha=1,fade=t=out:st={b-0.25:.3f}:d=0.25:alpha=1[o{k}];[v{k}][o{k}]overlay=enable='between(t,{a:.3f},{b:.3f})'[v{k+1}];"
 fc+=f"[v{len(ov)}]fade=t=out:st={TOTAL-FADE:.3f}:d={FADE},format=yuv420p[v]"
 run([*inputs,'-filter_complex',fc,'-map','[v]','-t',TOTAL,*ENC,WORK/'picture.mp4'])
 (PACK/'overlays_v03c.json').write_text(json.dumps([dict(file=Path(p).name,start=round(a,3),end=round(b,3)) for p,a,b in ov],indent=2))

 # House bed, acrossfade-looped to full runtime, fading with the picture.
 bdur=probe(BED)-8-6.5-2;copies=max(1,math.ceil((TOTAL-4)/(bdur-4)));inputs=[];fc=''
 for _ in range(copies):inputs+=['-ss',8,'-i',BED]
 for i in range(copies):
  fc+=f'[{i}:a]asplit=2[h{i}][t{i}];[h{i}]atrim=0:71.5,asetpts=PTS-STARTPTS[head{i}];[t{i}]atrim=start=78,asetpts=PTS-STARTPTS[tail{i}];[head{i}][tail{i}]acrossfade=d=2:c1=tri:c2=tri[bed{i}];'
 last='bed0'
 for i in range(1,copies):
  lab=f'm{i}';fc+=f'[{last}][bed{i}]acrossfade=d=4:c1=tri:c2=tri[{lab}];';last=lab
 fc+=f'[{last}]atrim=0:{TOTAL},volume=0.14,afade=t=out:st={TOTAL-FADE-1.5:.3f}:d={FADE+1.5}[m]'
 run([*inputs,'-filter_complex',fc,'-map','[m]','-c:a','pcm_s24le',WORK/'music.wav'])
 mix=f'[0:a]apad=whole_dur={TOTAL},atrim=0:{TOTAL},asetpts=PTS-STARTPTS[v];[v][1:a]amix=inputs=2:duration=first:normalize=0'
 first=sp.run(['ffmpeg','-hide_banner','-i',str(VO),'-i',str(WORK/'music.wav'),'-filter_complex',mix+',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]','-map','[a]','-f','null','-'],capture_output=True,text=True).stderr
 st=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',first,re.S)[-1]);(PACK/'loudnorm_first_pass.json').write_text(json.dumps(st,indent=2))
 norm=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
 run(['-i',VO,'-i',WORK/'music.wav','-filter_complex',mix+','+norm+'[a]','-map','[a]','-ar','48000','-c:a','aac','-b:a','192k',WORK/'audio.m4a'])
 OUT.parent.mkdir(parents=True,exist_ok=True)
 run(['-i',WORK/'picture.mp4','-i',WORK/'audio.m4a','-map','0:v','-map','1:a','-c','copy','-t',TOTAL,'-movflags','+faststart',WORK/OUT.name])
 sp.run(['cp',str(WORK/OUT.name),str(OUT)],check=True)

# ---- checks and review pack
runtime=probe(OUT)
ll=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
lufs=float(re.findall(r'I:\s*([-\d.]+) LUFS',ll)[-1])
checks=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-vf','blackdetect=d=0.1:pix_th=0.10:pic_th=0.98,freezedetect=n=-50dB:d=0.8','-an','-f','null','-'],capture_output=True,text=True).stderr
(PACK/'ffmpeg_checks.txt').write_text('\n'.join(l for l in checks.splitlines() if 'black_' in l or 'freeze' in l))
cuts=[dict(row=s['row'],timeline_in=s['timeline_in'],timeline_out=s['timeline_out'],source=s['src'].name,
 framing={k:v for k,v in s['o'].items() if k in('quad','offset','vcrop','pan')},src_w=s['src_w'],upscale=s['upscale']) for s in segs]
(PACK/'cuts_v03c.json').write_text(json.dumps(cuts,indent=2))
reuse_rows={n:[s['row'] for s in stills if s['src'].name==n] for n in sorted(reuse,key=lambda n:(-reuse[n],n))}
(PACK/'reuse_v03c.json').write_text(json.dumps(dict(stills=dict(sorted(reuse.items(),key=lambda x:(-x[1],x[0]))),rows=reuse_rows,
 video=dict(sorted(vreuse.items(),key=lambda x:(-x[1],x[0])))),indent=2))
buf=io.StringIO();wr=csv.writer(buf);wr.writerow(['row','source','vo_in','vo_out','vo_text'])
for c in cuts:
 text=' '.join(w['text'] for w in words if c['timeline_in']<=(w['start']+w['end'])/2<c['timeline_out'])
 wr.writerow([c['row'],c['source'],f"{c['timeline_in']:.3f}",f"{c['timeline_out']:.3f}",text or '[no VO]'])
(PACK/'mars_robot_full_v03c_assembled.csv').write_text(buf.getvalue());(PACK/'mars_robot_words_list.json').write_text(json.dumps(words))
cc=sp.run([sys.executable,str(CLIP_CHECK),str(PACK/'mars_robot_full_v03c_assembled.csv'),'--words',str(PACK/'mars_robot_words_list.json')],capture_output=True,text=True)
(PACK/'clip_check_py.txt').write_text(cc.stdout+cc.stderr)
inside=[c['timeline_in'] for c in cuts[1:] if any(w['start']+0.02<c['timeline_in']<w['end']-0.02 for w in words)]
align=dict(runtime=runtime,expected=TOTAL,vo_last_word_end=LAST_WORD,hold_after_last_word=HOLD,fade=FADE,cuts=len(cuts),
 cuts_inside_a_word=inside,longest_shot=max(c['timeline_out']-c['timeline_in'] for c in cuts),max_upscale=max(c['upscale'] for c in cuts))
(PACK/'align_vs_vo.json').write_text(json.dumps(align,indent=2))

frames=PACK/'frames';frames.mkdir(exist_ok=True)
def grab(t,dst,w=480):run(['-ss',f'{t:.3f}','-i',OUT,'-frames:v','1','-vf',f'scale={w}:{w*9//16}',dst])
tiles=[]
for k,c in enumerate(cuts):
 mid=(c['timeline_in']+c['timeline_out'])/2;dst=frames/f"row_{k:03}.jpg";grab(mid,dst);tiles.append((dst,f"{c['row']} {mid:.1f}s {c['source'][:22]}"))
def sheet(name,items,cols=6):
 rows_n=math.ceil(len(items)/cols);board=Image.new('RGB',(cols*320,rows_n*200),(18,18,22));d=ImageDraw.Draw(board)
 for i,(p,label) in enumerate(items):
  x=i%cols*320;y=i//cols*200;board.paste(Image.open(p).resize((320,180)),(x,y));d.text((x+6,y+182),label,fill='white')
 board.save(PACK/(name+'.jpg'),quality=90)
sheet('per_row_sheet_v03c',tiles)
fill=[dict(row=c['row'],cut=k,source=c['source'],frac=round(border_fill_fraction(frames/f"row_{k:03}.jpg"),4)) for k,c in enumerate(cuts)]
for f in fill:
 if f['frac']>FILL_MAX and f['source'] in REVIEWED_OK:f.update(status='reviewed_ok',note=REVIEWED_OK[f['source']])
fill_fail=[f for f in fill if f['frac']>FILL_MAX and 'status' not in f]
fill_reviewed=[f for f in fill if f.get('status')=='reviewed_ok']
(PACK/'fill_gate_v03c.json').write_text(json.dumps(dict(rule='fail if near-black(<12)/near-white(>245) pixels touching the border cover > 1.5% of the row frame',verdict='FAIL' if fill_fail else 'PASS',fail=fill_fail,reviewed_ok=fill_reviewed,rows=fill),indent=2))
freezes=[l for l in checks.splitlines() if 'freeze_duration' in l]
def tsheet(name,times):
 items=[]
 for i,t in enumerate(times):p=WORK/f'f_{name}_{i}.jpg';grab(t,p);items.append((p,f'{t:.2f}s'))
 sheet(name,items,cols=3)
tsheet('frame0_sheet',[0,.2,.4,.6,.8,1])
tsheet('sheet_0_8s',[0,1,2,3,4,5,6,6.4,6.6,7,7.5,8])
om=[c for c in cuts if c['source'].startswith('orbit_')]
tsheet('sheet_omni',[t for c in om for t in (c['timeline_in']+0.5,(c['timeline_in']+c['timeline_out'])/2,c['timeline_out']-0.5)])
tsheet('sheet_cards_sub',[o['start']+1.0 for o in json.loads((PACK/'overlays_v03c.json').read_text())])
tsheet('sheet_end',[LAST_WORD-1,LAST_WORD+0.5,LAST_WORD+1.5,LAST_WORD+2.5,TOTAL-0.5,TOTAL-0.05])
h=hashlib.sha256()
with OUT.open('rb') as f:
 for b in iter(lambda:f.read(1<<20),b''):h.update(b)
(PACK/'SHA256.txt').write_text(f'{h.hexdigest()}  {OUT.name}\n')
summary=dict(fill_gate='FAIL' if fill_fail else 'PASS',fill_fail=fill_fail,fill_reviewed_ok=[(f['row'],f['source'],f['frac']) for f in fill_reviewed],freezes_over_0_8s=freezes,sentence_end_rows=SENT_NOTE,out=str(OUT),sha256=h.hexdigest(),runtime=runtime,lufs=lufs,clip_check_exit=cc.returncode,align=align,reuse_stills=dict(reuse))
(PACK/'polish_reviewed_ok_v03c.json').write_text(json.dumps(POLISH_OK,indent=2))
pg=sp.run([sys.executable,str(POLISH),str(WORK/OUT.name),'--cuts',str(PACK/'cuts_v03c.json'),'--out',str(PACK/'polish_gate_v03c.json'),'--reviewed-ok',str(PACK/'polish_reviewed_ok_v03c.json')],capture_output=True,text=True)
(PACK/'polish_gate_v03c.txt').write_text(pg.stdout+pg.stderr);summary['polish_gate']='PASS' if pg.returncode==0 else 'FAIL'
(PACK/'summary_v03c.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=1));print(cc.stdout+cc.stderr)
