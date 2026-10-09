#!/usr/bin/env python3
"""026 How Far Is the Nearest Star? rough v05 (J0085): v04 with Ben's three fixes (#6077058676) and the Chief's stills FIX
(#6090651546). Only rows 9, 11, 24 and 27 change:
- row 9: iss073e0982679 under "A light-year is a distance, not a time.", then the labelled `lightyear` graphic
  (code_out_v05) from 112.20 to the row end, so its pulse lands on "four years ago". journey and eso1031a leave row 9.
- row 11: Orbit's parallax thumb trick, orbit_thumb_omni_v01 (Vertex Omni, one take), from "Hold up your thumb";
  eso1323a and iss073e0982679 (second framing) cover the rest of the row.
- row 24: Orbit's walk, orbit_walk_omni_v01 (one take), from "Walk at a steady pace", then journey from "Take a car".
- row 27: the labelled `lightrace` graphic (code_out_v05) replaces the lighttimes bars.
The v04 docstring follows.

v03 with Claude's v04 fixes (#6075235567, claude_rulings_v03.json "v04"):
eso0932a held still on tight 16:9 crops (galactic centre at 2:54, Carina side at 7:51; no push, so no jitter), PIA04495 recropped to the
whole spacecraft, 3:42 eso1241a out (black until ~13 s, constellation labels from ~14.5 s) for the unused LRO full Moon e001982;
border-fill check is a WARN for this film.
rough v03: v02 with Claude's rulings #6074757587 (claude_rulings_v03.json): potw1343a and Bessel full frame,
KSC/PIA17462/PIA21747 swaps, third time-lapse uses dropped, parallax and lighttimes redrawn (code_out_v03), reviewed_ok from the rulings.
v02 notes:
- <=2 uses per still, the second at a new framing; reuse count per source printed and written to the pack.
- Upscale (source px -> 1080p, push included) recorded per row and asserted <= 2.35.
- Every cut snapped to a VO pause (words.json); no shot held longer than 6 s except the row 33 bookend.
- Frame 0 is the ESO time-lapse uhd_yb_paranal_01 from its first frame; row 33 ends on it again, pushing in, to the end.
- Labelled plates (eso1629g, eso1629b, eso1702a, eso1702b) are out; no insets (potw1343a, Bessel, e001586 dropped).
- Each code graphic at most 2 uses, 3 where its state moves on (offsets differ); 024's starfield 3 uses.
- Each ESO time-lapse at most 3 segments (its briefed use + 2), clean stretches only (pool_v03.json notes);
  freed slots filled from the pool v03 star-field plates. The SDO flare enters after its text card (from 8 s).
- Shot list: SHOT_LIST_v01.md (33 rows); pool: pool_v03.json (files in pool_v01/).
Locked VO untouched, 026's own bed full runtime, hold 2.5 s past the last word, then 1 s fade, -14 LUFS.
`--plan` prints the segment list, reuse counts and checks without rendering."""
from pathlib import Path
import json, subprocess as sp, re, hashlib, math, sys, csv, io
from collections import Counter
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent; EP=HERE.parent
sys.path.insert(0,str(EP.parent/'025_Could-A-Robot-Survive-On-Mars/07_Edit-Project'))
from fillbox import best_box, border_fill_fraction
Image.MAX_IMAGE_PIXELS = None
UAT=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/OWB UAT'
WORK=Path('/private/tmp/nearest026_rough_work_v05'); PACK=HERE/'rough_v05_pack'
VO=EP/'02_Voiceover/nearest_star_vo_v01.mp3'
OUT=UAT/'026_NearestStar_v05_PHONE.mp4'
BED=EP/'05_Music/nearest-star_score_bed_v01_full.mp3'
MAX_UP=2.35; MAX_HOLD=6.0
H=HERE/'pool_v01'
CG=HERE/'code_out_v01'
CG3=HERE/'code_out_v03'
CG5=HERE/'code_out_v05'
OMNI=EP/'04_Generated-Clips/01_Raw/omni_v01'
STARFIELD=EP.parent/'024_What-Happens-If-You-Travel-Near-Light-Speed/07_Edit-Project/graphics_v03/starfield.mp4'
FPS=30; LAST_WORD=490.964; HOLD=2.5; FADE=1.0; TOTAL=round((LAST_WORD+HOLD+FADE)*FPS)/FPS
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

Q={'tl':(0.0,0.0),'tr':(0.5,0.0),'bl':(0.0,0.5),'br':(0.5,0.5),'c':(0.25,0.25)}
FILL_MAX=0.015
FILL_NOTE=json.loads((HERE/'claude_rulings_v03.json').read_text())['v04']['fill_gate']
CG_NOTE='code graphic, near-black space by design; reviewed_ok for near-black and low detail (Claude, #6074131477)'
REVIEWED_OK={n:CG_NOTE for n in ('triple.mp4','parallax.mp4','journey.mp4','scale.mp4','lighttimes.mp4','starfield.mp4','lightyear.mp4','lightrace.mp4')}
POLISH_OK={n:dict(note=CG_NOTE,kinds=['near-black','low detail']) for n in REVIEWED_OK}
POLISH_OK.update(json.loads((HERE/'claude_rulings_v03.json').read_text())['reviewed_ok'])
REVIEWED_OK.update({n:v['note'] for n,v in POLISH_OK.items()})
_LEN={}
def V(p,at=0.0,**k):
 """A video source from `at`, capped at what is left of the file."""
 p=p if isinstance(p,Path) else (CG3 if p in ('parallax','lighttimes') else CG)/f'{p}.mp4'
 L=_LEN.setdefault(p,probe(p))
 return (p,{**dict(video=1,at=at,max=min(MAX_HOLD,L-at-0.1)),**k})
c=dict(quad='c')
NS='nightsky/';PX='proxima/';AC='alphacen/';SUN='sun/';EM='earth_moon/';VG='voyager/';SL='sail/';DSN='dsn/';PB='proxima_b/'
TL=H/'timelapse'
def T(name,at=0.0,**k):return V(TL/f'{name}.mp4',at,**k)
YB1,YB2,BT1,BT6,BT7,CRUX,VISTA='uhd_yb_paranal_01','uhd_yb_paranal_02','uhd_bt_paranal_01','uhd_bt_paranal_06','uhd_bt_paranal_07','bt_lasilla_crux','vltfromvistatimelapse'
CRUX_C=(300,0,3240,1822)
# star-field plates from pool v04 (no labels)
OMC1,OMC2,TUC,N6752,CAR1,CAR2,CAR3,MYST='eso0844a.jpg','heic0809a.jpg','eso1302a.jpg','eso1323a.jpg','eso1250a_8k.jpg','eso0905a.jpg','eso1031a.jpg','heic1007a.jpg'
SDO=H/SUN/'GSFC_20160426_SDO_m12224_SolarFlare.mp4'
# (row, VO in from SHOT_LIST_v01, [sources]); a source is a pool path or (path, opts). One cut per source.
ROWS=[
 ('1',0.08,[T(YB1),NS+'iss073e0982261.jpg']),
 ('2',8.54,[T(BT1)]),
 ('3',13.90,[T(BT6),PX+'potw1343a.jpg']),
 ('4',20.88,[V('triple'),V('parallax'),V('journey')]),
 ('5',33.54,[(PX+'potw1343a.jpg',dict(box=(0.15,0.15,0.85,0.85))),TUC,N6752,OMC2]),
 ('6',50.14,[SUN+'GSFC_20171208_Archive_e002035.jpg',SUN+'GSFC_20171208_Archive_e000790.jpg',AC+'eso1629i.jpg']),
 ('7',64.30,[(AC+'eso1629i.jpg',c),T(CRUX,vcrop=CRUX_C),PX+'GSFC_20171208_Archive_e000214.jpg',T('eso1241a',8.0,max=5.5),CAR2]),
 ('8',88.88,[V('triple',6),OMC1,T(BT7,2.0),CAR1]),
 ('9',108.90,[NS+'iss073e0982679.jpg',(CG5/'lightyear.mp4',dict(video=1,at=0.0,max=9.7,hold_ok=1,near=112.19))]),
 ('10',122.14,[NS+'GSFC_20171208_Archive_e000256.jpg',(NS+'iss073e0982261.jpg',c)]),
 ('11',128.10,[(OMNI/'orbit_thumb_omni_v01.mp4',dict(video=1,at=0.0,max=9.9,hold_ok=1)),(N6752,dict(quad='c',near=137.3)),(NS+'iss073e0982679.jpg',dict(quad='c',near=140.7))]),
 ('12',144.36,[V('parallax',3),NS+'eso0934a.jpg',T(VISTA,3.5),(NS+'GSFC_20171208_Archive_e000256.jpg',dict(box=(0.15,0.15,0.85,0.85))),(PX+'GSFC_20171208_Archive_e000214.jpg',dict(box=(0.12,0.12,0.88,0.88)))]),
 ('13',167.18,['portraits/Tycho_Brahe.jpg',(NS+'eso0932a.jpg',dict(box=(2150/6000,1012/3000,3850/6000,1968/3000),pct=0)),(CAR3,c)]),
 ('14',182.32,[V('parallax',6),(NS+'eso0934a.jpg',c),('portraits/Bessel_Herterich_1825.jpg',dict(box=(0.08,0.12,0.92,0.62))),(CAR1,c),T(BT1,2.0,vcrop=(640,360,2560,1440))]),
 ('15',205.78,['gaia/gaia_sky_in_colour.jpg',(OMC1,c),('gaia/gaia_sky_in_colour.jpg',c),(EM+'GSFC_20171208_Archive_e001982.jpg',dict(box=(0,0,1,1)))]),
 ('16',224.94,[V(STARFIELD),MYST]),
 ('17',232.96,[V(STARFIELD,6),(TUC,c)]),
 ('18',239.90,[V('scale'),V('scale',4),(MYST,c)]),
 ('19',250.48,[EM+'GSFC_20171208_Archive_e002130.jpg',EM+'GSFC_20171208_Archive_e000868.jpg',EM+'GSFC_20171208_Archive_e001788.jpg']),
 ('20',263.86,[(EM+'GSFC_20171208_Archive_e002130.jpg',c),(EM+'GSFC_20171208_Archive_e001788.jpg',c),EM+'iss025e015176.jpg']),
 ('21',277.80,[T(CRUX,4.0,vcrop=(600,150,2560,1440)),V(STARFIELD,12),(CAR2,c),(OMC2,c)]),
 ('22',296.40,[VG+'PIA17049.jpg',VG+'PIA21739.jpg',VG+'PIA21746.jpg']),
 ('23',312.28,[VG+'PIA17464.jpg']),
 ('24',315.26,[(OMNI/'orbit_walk_omni_v01.mp4',dict(video=1,at=0.0,max=9.9,hold_ok=1)),V('journey',6,near=323.4),(VG+'PIA04495.jpg',dict(box=(0.02,0.16,0.98,0.16+0.96*3017*9/16/2494),near=329.0)),(VG+'PIA21739.jpg',dict(quad='c',near=332.2))]),
 ('25',336.98,[VG+'PIA14111.jpg',(VG+'PIA21746.jpg',c),T(BT7,2.0,vcrop=(1280,720,2560,1440)),(VG+'PIA17464.jpg',c)]),
 ('26',355.22,[(VG+'PIA21839.jpg',dict(hold_ok=1,max=8.0,pct=.04))]),
 ('27',362.16,[(CG5/'lightrace.mp4',dict(video=1,at=0.0,max=17.8,hold_ok=1))]),
 ('28',378.98,[PB+'eso1629a.jpg',V(H/PB/'eso1629d_video.mp4'),(PB+'eso1629a.jpg',c),V(H/PB/'eso1629e_video.mp4',12)]),
 ('29',396.84,[PB+'eso1629e.jpg',V(H/PB/'eso1629e_video.mp4')]),
 ('30',403.98,[(PB+'eso1629e.jpg',c),V(SDO,8),V(SDO,16),SUN+'GSFC_20171208_Archive_e000759.jpg']),
 ('31',421.90,[SL+'ACD24-0020-061.jpg',SL+'ACS3_SolarPanels_001.jpg',SL+'CamA_Seq109_2024-08-28_17-17-11Z_V2_S560161.jpg',SL+'CamC_Seq109_2024-08-28_17-17-13Z_V2_S595171.jpg']),
 ('32',442.70,[DSN+'PIA23214.jpg',DSN+'PIA24163.jpg',DSN+'PIA25136.jpg']),
 ('33',457.86,[DSN+'PIA26147.jpg',DSN+'PIA25137.jpg',(NS+'eso0932a.jpg',dict(box=(3500/6000,1086/3000,4900/6000,1873/3000),pct=0)),T(BT6,7.0,vcrop=(1280,720,2560,1440)),T(VISTA,8.5,vcrop=(64,36,1152,648)),T(YB2,0.0,vcrop=(1280,0,2560,1440)),
   (TL/f'{YB1}.mp4',dict(video=1,at=0.3,max=7.2,push=0.05,hold_ok=1,bookend=1))]),
]
LABELS=[]
CHAPTERS=[('The Star You Cannot See',33.54),('Measuring the Gap',122.14),('Shrink It Down',232.96),('The Walk',312.28),('Is Anyone There?',378.98)]

GAPS=[((a['end']+b['start'])/2,b['start']-a['end']) for a,b in zip(words,words[1:])]
def snap(t):
 """Midpoint of the nearest VO pause (>=0.30 s, else >=0.20 s, else >=0.10 s) within 2 s, then 3.5 s; past the last word, keep t."""
 if t>LAST_WORD:return t
 for reach in (2.0,3.5):
  for need in (0.30,0.20,0.10):
   cands=[m for m,g in GAPS if g>=need and abs(m-t)<=reach]
   if cands:return min(cands,key=lambda m:abs(m-t))
 raise SystemExit(f'no VO pause near {t}')

PAUSES=dict(sorted((m,g) for m,g in GAPS if g>=0.06))
SENT_NOTE={}
starts=[0.0]
for r,t,_ in ROWS[1:]:starts.append(snap(t-0.3))
ends=starts[1:]+[TOTAL]
segs=[]
for (row,_,srcs),a,b in zip(ROWS,starts,ends):
 srcs=[s if isinstance(s,tuple) else (s,{}) for s in srcs]
 n=len(srcs)
 caps=[o['max'] if o.get('hold_ok') else min(MAX_HOLD,o.get('max',MAX_HOLD)) for _,o in srcs]
 if row=='33':caps[-1]=srcs[-1][1]['max']
 cand=[m for m in PAUSES if a+1.8<=m<=b-1.8]
 even=[a+(b-a)*k/n for k in range(n)]
 best={0:{a:(0.0,None)}}
 for k in range(1,n):
  best[k]={}
  for m in cand:
   for prev,(cost,_) in best[k-1].items():
    if 1.8<=m-prev<=caps[k-1]:
     tgt=srcs[k][1].get('near');c_=cost+((m-tgt)**2*50 if tgt else (m-even[k])**2)+(0.4 if PAUSES[m]<0.10 else 0)
     if m not in best[k] or c_<best[k][m][0]:best[k][m]=(c_,prev)
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
SPANS={}

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
for wd in ('v01','v02','v03','v04'):
 for ok in Path(f'/private/tmp/nearest026_rough_work_{wd}').glob('seg_*.ok'):V01_CACHE[ok.read_text()]=ok.with_suffix('.mp4')
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
 from PIL import ImageFilter
 f3=ImageFont.truetype(FONT,46)
 for k,(name,t) in enumerate(LABELS):
  img=Image.new('RGBA',(1920,1080),(0,0,0,0));sh=Image.new('RGBA',(1920,1080),(0,0,0,0))
  ImageDraw.Draw(sh).text((96,958),name,font=f3,fill=(0,0,0,190));sh=sh.filter(ImageFilter.GaussianBlur(5))
  img=Image.alpha_composite(sh,img);ImageDraw.Draw(img).text((92,954),name,font=f3,fill='white')
  p=WORK/f'label_{k}.png';img.save(p);ov.append((p,t,t+2.5))
 inputs=['-i',WORK/'picture_raw.mp4'];fc='[0:v]null[v0];'
 for k,(p,a,b) in enumerate(ov):
  inputs+=['-loop','1','-t',TOTAL,'-i',p]
  fc+=f"[{k+1}:v]fade=t=in:st={a:.3f}:d=0.25:alpha=1,fade=t=out:st={b-0.25:.3f}:d=0.25:alpha=1[o{k}];[v{k}][o{k}]overlay=enable='between(t,{a:.3f},{b:.3f})'[v{k+1}];"
 fc+=f"[v{len(ov)}]fade=t=out:st={TOTAL-FADE:.3f}:d={FADE},format=yuv420p[v]"
 run([*inputs,'-filter_complex',fc,'-map','[v]','-t',TOTAL,*ENC,WORK/'picture.mp4'])
 (PACK/'overlays_v05.json').write_text(json.dumps([dict(file=Path(p).name,start=round(a,3),end=round(b,3)) for p,a,b in ov],indent=2))

 # 026's own bed under the whole cut at 025's level, fading with the picture.
 run(['-i',BED,'-af',f'atrim=0:{TOTAL},asetpts=PTS-STARTPTS,volume=0.134,afade=t=out:st={TOTAL-FADE-1.5:.3f}:d={FADE+1.5}','-c:a','pcm_s24le',WORK/'music.wav'])
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
(PACK/'cuts_v05.json').write_text(json.dumps(cuts,indent=2))
reuse_rows={n:[s['row'] for s in stills if s['src'].name==n] for n in sorted(reuse,key=lambda n:(-reuse[n],n))}
(PACK/'reuse_v05.json').write_text(json.dumps(dict(stills=dict(sorted(reuse.items(),key=lambda x:(-x[1],x[0]))),rows=reuse_rows,
 video=dict(sorted(vreuse.items(),key=lambda x:(-x[1],x[0])))),indent=2))
buf=io.StringIO();wr=csv.writer(buf);wr.writerow(['row','source','vo_in','vo_out','vo_text'])
for c in cuts:
 text=' '.join(w['text'] for w in words if c['timeline_in']<=(w['start']+w['end'])/2<c['timeline_out'])
 wr.writerow([c['row'],c['source'],f"{c['timeline_in']:.3f}",f"{c['timeline_out']:.3f}",text or '[no VO]'])
(PACK/'nearest_star_rough_v05_assembled.csv').write_text(buf.getvalue());(PACK/'nearest_star_words_list.json').write_text(json.dumps(words))
cc=sp.run([sys.executable,str(CLIP_CHECK),str(PACK/'nearest_star_rough_v05_assembled.csv'),'--words',str(PACK/'nearest_star_words_list.json')],capture_output=True,text=True)
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
sheet('per_row_sheet_v05',tiles)
fill=[dict(row=c['row'],cut=k,source=c['source'],frac=round(border_fill_fraction(frames/f"row_{k:03}.jpg"),4)) for k,c in enumerate(cuts)]
for f in fill:
 if f['frac']>FILL_MAX and f['source'] in REVIEWED_OK:f.update(status='reviewed_ok',note=REVIEWED_OK[f['source']])
fill_fail=[f for f in fill if f['frac']>FILL_MAX and 'status' not in f]
fill_reviewed=[f for f in fill if f.get('status')=='reviewed_ok']
(PACK/'fill_gate_v05.json').write_text(json.dumps(dict(rule='fail if near-black(<12)/near-white(>245) pixels touching the border cover > 1.5% of the row frame',verdict='WARN' if fill_fail else 'PASS',note=FILL_NOTE,fail=fill_fail,reviewed_ok=fill_reviewed,rows=fill),indent=2))
freezes=[l for l in checks.splitlines() if 'freeze_duration' in l]
def tsheet(name,times):
 items=[]
 for i,t in enumerate(times):p=WORK/f'f_{name}_{i}.jpg';grab(t,p);items.append((p,f'{t:.2f}s'))
 sheet(name,items,cols=3)
tsheet('frame0_sheet',[0,.2,.4,.6,.8,1])
tsheet('sheet_0_8s',[0,1,2,3,4,5,6,6.4,6.6,7,7.5,8])
om=[c for c in cuts if c['source'].startswith('orbit_')]
if om:tsheet('sheet_omni',[t for c in om for t in (c['timeline_in']+0.5,(c['timeline_in']+c['timeline_out'])/2,c['timeline_out']-0.5)])
tsheet('sheet_cards_sub',[o['start']+1.0 for o in json.loads((PACK/'overlays_v05.json').read_text())])
tsheet('sheet_end',[LAST_WORD-1,LAST_WORD+0.5,LAST_WORD+1.5,LAST_WORD+2.5,TOTAL-0.5,TOTAL-0.05])
h=hashlib.sha256()
with OUT.open('rb') as f:
 for b in iter(lambda:f.read(1<<20),b''):h.update(b)
(PACK/'SHA256.txt').write_text(f'{h.hexdigest()}  {OUT.name}\n')
summary=dict(fill_gate='WARN' if fill_fail else 'PASS',fill_fail=fill_fail,fill_reviewed_ok=[(f['row'],f['source'],f['frac']) for f in fill_reviewed],freezes_over_0_8s=freezes,sentence_end_rows=SENT_NOTE,out=str(OUT),sha256=h.hexdigest(),runtime=runtime,lufs=lufs,clip_check_exit=cc.returncode,align=align,reuse_stills=dict(reuse))
(PACK/'polish_reviewed_ok_v05.json').write_text(json.dumps(POLISH_OK,indent=2))
pg=sp.run([sys.executable,str(POLISH),str(WORK/OUT.name),'--cuts',str(PACK/'cuts_v05.json'),'--out',str(PACK/'polish_gate_v05.json'),'--reviewed-ok',str(PACK/'polish_reviewed_ok_v05.json')],capture_output=True,text=True)
(PACK/'polish_gate_v05.txt').write_text(pg.stdout+pg.stderr);summary['polish_gate']='PASS' if pg.returncode==0 else 'FAIL'
(PACK/'summary_v05.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=1));print(cc.stdout+cc.stderr)
