#!/usr/bin/env python3
"""027 What If Earth Stopped Spinning? rough v01 (J0077), built in the SHOT_LIST_v02 order (agenda cut, first answer at ~23 s).
Base: 026's rough v04 assembler. VO = earth_spin_vo_v02order.wav (322b925; words_v02order.json); each row's VO-in is its
SHOT_LIST_v01 time mapped through the re-cut spans. No music bed until the ElevenLabs renewal on 30 Oct: VO only, -14 LUFS.
026's lessons from the start: frame 0 is the moving EPIC Earth (no fade, no title); <=2 uses per still at a new framing;
upscale <=2.35 asserted; cuts in VO pauses; no shot over 6 s except hold_ok rows; ESA/NOAA corner bugs cropped off (vcrop).
Claude's J0077 rulings: Omni row 21 from the second sample frame (1.7 s); Veo cabin pour 0-4.8 s only; phone dark open.
v01b (Claude #6086704806): row 35's back-to-back Gerst 330/340 merged into one span <=8.3 s; row 14 Omni ends on the
shrug (~8.4 s into the take), not on the idle; row 22 = Magellan PIA00271 (<=8.2 s, slow push) then PIA23791 at 1.78x.
v01d (Claude #6087573310): row 6 Five Minutes -> ISS city-lights still iss070e062746 (slow push, crop clear of the
array); row 7 La Silla from 3.4 s (past the ESO card, hard cut at 3.08 s + 0.2 s pre-roll), second cut continuous; row 22
PIA23791 box [0,0,0.46,1]; row 28 NOAA@108 dropped, its time to the clean 63 s span (<=7 s); rows 17 and 18-19 oceans
re-rendered (code_out_v05, c2b15c5 shore); Gerst@250/@316/@330 near-black ruled per stretch.
v01c (Claude #6087174848, picture_qa counts appearances and stretches): every code graphic is a row's own render, named
rowNN_<graphic>.mp4 in the cut list; a run of one graphic is cut from one continuous render (cont=1 carries the offset on);
row 21 Gerst moves to the 278.5 s night-clouds stretch (256 was within 10 s of row 6's 250); dark Gerst stretches (rows 2, 10, 13, 16) swapped for the NASA 'Sunrise To Sunset Aboard The ISS' daylight reel; row 6 =
Five Minutes from 18 s with the lower crop; row 33 leaves Five (only 31.5 s long) for the ISS reel; row 8 drops row 35's
speed (bulge carries it); row 18 drops the bulge repeat; caption 'Radar map · NASA Magellan' on PIA00271 (Claude #6086910171).
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
WORK=Path('/private/tmp/earth027_rough_work_v01d'); PACK=HERE/'rough_v01d_pack'
VO=EP/'02_Voiceover/earth_spin_vo_v02order.wav'
OUT=UAT/'027_EarthSpin_rough_v01d.mp4'
BED=None
MAX_UP=2.35; MAX_HOLD=6.0
H=HERE/'pool_v01'
CG=HERE/'code_out_v03'; CG4=HERE/'code_out_v04'; CG5=HERE/'code_out_v05'
GEN=EP/'04_Generated-Clips/01_Raw'
FPS=30
_VOJ=json.loads((EP/'02_Voiceover/words_v02order.json').read_text())
LAST_WORD=_VOJ['last_word_end']; HOLD=2.5; FADE=1.0; TOTAL=round((LAST_WORD+HOLD+FADE)*FPS)/FPS
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
CLIP_CHECK=EP.parents[1]/'00_Brand/Channel-Setup/tools/clip_check.py'
POLISH=EP.parents[1]/'scripts/polish_gate.py'
PLAN='--plan' in sys.argv
words=[dict(text=t,start=a,end=b) for t,a,b in _VOJ['words']] if isinstance(_VOJ['words'][0],list) else _VOJ['words']
SPAN=_VOJ['spans']
def nt(t):
 """SHOT_LIST_v01 time -> v02-order timeline."""
 for s in SPAN:
  if s['v01_in']<=t<s['v01_out']:return round(t-s['v01_in']+s['new_in'],3)
 raise SystemExit(f'v01 time {t} is in no span (cut?)')

def run(args):
 p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-6000:])
def probe(p):return float(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
def fr(t):return round(t*FPS)/FPS

Q={'tl':(0.0,0.0),'tr':(0.5,0.0),'bl':(0.0,0.5),'br':(0.5,0.5),'c':(0.25,0.25)}
FILL_MAX=0.015
FILL_NOTE='027 rough v01: EPIC disc and code graphics sit on near-black space; WARN for Claude to look at full size.'
REVIEWED_OK={};POLISH_OK={}
_LEN={}
def V(p,at=0.0,**k):
 """A video source from `at`, capped at what is left of the file."""
 L=_LEN.setdefault(p,probe(p))
 return (p,{**dict(video=1,at=at,max=min(MAX_HOLD,L-at-0.1)),**k})
def G(row,name,at=0.0,**k):return V(CG/row/f'{name}.mp4',at,**k)
def G4(row,name,at=0.0,**k):return V(CG4/row/f'{name}.mp4',at,**k)
def G5(row,name,at=0.0,**k):return V(CG5/row/f'{name}.mp4',at,**k)
CITY='iss/iss070e062746.jpg'
c=dict(quad='c')
EPIC=Path('/private/tmp/owb027_epic_v01/epic_spin_v01.mp4')
GERST=H/'iss/Gerst_Earth_timelapses_2017.webm'; GC=(384,216,3456,1944)  # ESA logo top-left cropped off (Claude #6085748466)
FIVE=H/'iss/Five_Minutes_in_Orbit.webm'; FC=(0,200,1920,1080)  # lower crop: city lights fill the frame (Claude #6087174848)
ISS=H/'iss/ISS_sunrise_to_sunset.ogv'
SEA=H/'sea/Kalaloch_waves_rocks_02.webm'
SILLA=H/'stars/ESO_timelapse_La_Silla.webm'
PEND=H/'foucault/Foucault_pendulum_1.webm'; PC=(0,216,1920,864)  # visitors' legs cropped off (<=1.25x)
NOAA=H/'eclipse/NOAA_sat_eclipse_2024_notext.webm'
NP=GEN/'omni_v01/orbit_northpole_omni_v01.mp4'; SUNSET=GEN/'omni_v01/orbit_sunset_omni_v01.mp4'
POUR=GEN/'veo_v01/cabin_pour_veo_v01.mp4'; PHONE=GEN/'veo_v01/phone_midnight_veo_v01.mp4'
BM,BM2='earth/GSFC_20171208_Archive_e002130.jpg','earth/GSFC_20171208_Archive_e002131.jpg'
SUN='sun/GSFC_20171208_Archive_e002035.jpg'
MOON,FAR='moon/GSFC_20171208_Archive_e000868.jpg','moon/GSFC_20171208_Archive_e001939.jpg'
AS14='moon/as14-67-09386.jpg'; VENUS='venus/PIA23791.jpg'
CORAL1,CORAL2='coral/Heliophyllum_confluens_fossil_coral_Columbus_Limestone_Middl.jpg','coral/Eridophyllum_seriale_2.jpg'
TIGHT=(240,135,1440,810)
# (row, VO in from SHOT_LIST_v01 -> nt(), [sources]) in SHOT_LIST_v02 order; v01 row 4 (the agenda) is cut.
ROWS=[
 ('1',0.0,[V(EPIC,0.0,max=6.5),V(GERST,40.0,vcrop=GC)]),
 ('2',nt(9.76),['airborne/ED07-0256-09.jpg',V(ISS,2.0)]),
 ('3',nt(17.36),[G('row03','speed',max=6.5,hold_ok=1)]),
 ('10',nt(111.92),[V(ISS,20.0),V(ISS,20.0,cont=1)]),
 ('11',nt(121.06),[G('row10','air',max=7.5,hold_ok=1),G('row11','air',8.0)]),
 ('12',nt(133.70),[V(SEA,0.0),V(SEA,9.0)]),
 ('13',nt(143.12),[V(ISS,44.0),G('row13','speed',2.0),G('row13','speed',7.0)]),
 ('14',nt(155.24),[V(NP,0.0,max=8.8,hold_ok=1),V(GERST,316.0,vcrop=GC,near=74.5)]),
 ('15',nt(167.16),[SUN,V(EPIC,8.0,vcrop=(460,180,1000,563)),'earth/GSFC_20171208_Archive_e000265.jpg']),
 ('5',nt(40.38),[V(POUR,0.0,max=4.8),'airborne/AFRC2022-0059-49.jpg',('airborne/ED07-0256-09.jpg',c)]),
 ('6',nt(51.32),[V(GERST,250.0,vcrop=GC),(CITY,dict(box=(0.0,0.30,0.80,0.75),pct=.06,hold_ok=1,max=9.0))]),
 ('7',nt(63.32),[V(SILLA,3.4),V(SILLA,3.4,cont=1)]),
 ('8',nt(72.98),[G4('row08','bulge',max=7.0,hold_ok=1),G4('row08','bulge',cont=1),BM]),
 ('9',nt(90.86),[V(PEND,0.0,vcrop=PC),V(PEND,12.0,vcrop=PC),V(PEND,24.0,vcrop=PC),('foucault/Portrait_Leon_Foucault_1860.jpg',dict(box=(0.05,0.04,0.95,0.62)))]),
 ('16',nt(182.42),[V(ISS,56.0)]),
 ('17',nt(187.84),[G5('row17','oceans',max=5.3,hold_ok=1)]),
 ('18',nt(192.84),[BM2,(BM2,c),G5('row18-19','oceans',max=10.0,hold_ok=1)]),
 ('19',nt(212.52),[G5('row18-19','oceans',cont=1),('earth/GSFC_20171208_Archive_e000265.jpg',c)]),
 ('20',nt(221.96),[G4('row20','dayyear'),G4('row20','dayyear',cont=1),G4('row20','dayyear',cont=1)]),
 ('21',nt(237.30),[V(SUNSET,1.7,max=8.2,hold_ok=1),V(GERST,278.5,vcrop=GC)]),
 ('22',nt(248.76),[('venus/PIA00271.jpg',dict(hold_ok=1,max=8.2,pct=.04)),(VENUS,dict(box=(0.0,0.0,0.46,1.0),hold_ok=1,max=10.5,pct=.04))]),
 ('23',nt(265.90),[MOON,'tide/Bay_of_Fundy_tide_in.jpg','tide/Bay_of_Fundy_tide_out.jpg']),
 ('24',nt(275.10),[G4('row24-25','tides'),G4('row24-25','tides',cont=1),G4('row24-25','tides',cont=1)]),
 ('25',nt(287.98),[G4('row24-25','tides',cont=1),G4('row24-25','tides',cont=1),AS14,(AS14,c)]),
 ('26',nt(307.52),[(MOON,c),FAR,(FAR,dict(box=(0.08,0.2,0.92,0.75)))]),
 ('27',nt(323.28),[('tablet/Cuneiform_tablet-_commentary_on_Enuma_Anu_Enlil_tablet_5_MET.jpg',dict(pct=.06)),'eclipse/NHQ201708210100.jpg']),
 ('28',nt(334.66),[V(NOAA,2.0,vcrop=(384,0,3456,1944)),V(NOAA,52.0,vcrop=(384,216,3456,1944)),V(NOAA,63.0,vcrop=(0,0,3456,1944),max=7.0,hold_ok=1)]),
 ('29',nt(352.16),[(CORAL1,dict(pct=.06)),CORAL2,(CORAL1,c),(CORAL2,c)]),
 ('30',nt(369.70),[G('row30','clock',max=4.9,hold_ok=1)]),
 ('31',nt(374.30),[V(PHONE,0.0),'nist/NIST_atomic_clock_006.jpg']),
 ('32',nt(379.14),['nist/NIST-F2_cesium_fountain_atomic_clock.jpg','nist/NIST_ytterbium_lattice_clock.jpg']),
 ('33',nt(389.62),[G('row33','clock',0.0,vcrop=TIGHT),G('row33','clock',6.0),V(ISS,68.0)]),
 ('34',nt(403.46),['kilauea/commons_Pahoeoe_fountain_original.jpg',(BM,c),'greenland/GSFC_20171208_Archive_e001753.jpg']),
 ('35',nt(416.88),[(SUN,dict(box=(0.05,0.2,0.95,0.7))),G('row35','tides',2.0,vcrop=TIGHT),G('row35','speed',6.0),V(GERST,330.0,vcrop=GC,max=8.3,hold_ok=1)]),
 ('36',nt(439.12),[V(SILLA,24.0),'stars/ESO_star_trails_VLT_Paranal.jpg']),
 ('37',nt(449.30),[('young/NASA_Bennu_journey_early_Earth.jpg',dict(box=(0.2,0.0,0.8,1.0))),
   (EPIC,dict(video=1,at=4.0,max=16.9,hold_ok=1,bookend=1))]),
]
CHAPTERS=[('The Sudden Stop',nt(111.92)),('The Speed You Cannot Feel',nt(40.38)),('A Slow Stop',nt(192.84)),('Earth Is Already Slowing',nt(265.90)),('Keeping Score',nt(374.30))]

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
 if row=='37':caps[-1]=srcs[-1][1]['max']
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
_end={}
for s in segs:
 if s['o'].get('video'):
  if s['o'].get('cont'):s['o']['at']=round(_end[s['src']],3)
  s['o']['offset']=s['o'].get('at',0.0);_end[s['src']]=s['o']['offset']+s['timeline_out']-s['timeline_in']
def cname(p):return f'{p.parent.name}_{p.name}' if p.parent.parent in (CG,CG4,CG5) else p.name
_seg=lambda n:next(s for s in segs if s['src'].name==n)
LABELS=[('Radar map · NASA Magellan',_seg('PIA00271.jpg')['timeline_in'],_seg('PIA00271.jpg')['timeline_out']),
 ("Artist's impression",_seg('NASA_Bennu_journey_early_Earth.jpg')['timeline_in'],_seg('NASA_Bennu_journey_early_Earth.jpg')['timeline_out'])]
QA_OK={'PIA00271.jpg':dict(note='Magellan radar data on a globe; real terrain, false colour; captioned (Claude #99)',kinds=['kind of picture']),
 'epic_spin_v01.mp4':dict(note='row 37 is the planned return; row 15 a later turn (Claude #99)',kinds=['reuse'])}
for s in segs:
 if s['src'].parent.parent in (CG,CG4,CG5):QA_OK[cname(s['src'])]=dict(note='our code graphic on the house background (Claude #6087174848)',kinds=['near-black'])
QA_OK.update({'Gerst_Earth_timelapses_2017.webm@316':dict(note='night pass, city lights fill (p95 58) (Claude #6087573310)',kinds=['near-black']),
 'Gerst_Earth_timelapses_2017.webm@250':dict(note='aurora and city lights (p95 66) (Claude #6087573310)',kinds=['near-black']),
 'Gerst_Earth_timelapses_2017.webm@330':dict(note='aurora limb (p95 61) (Claude #6087573310)',kinds=['near-black'])})
POLISH_OK.update(QA_OK)
def plan_cuts():return [dict(row=s['row'],timeline_in=s['timeline_in'],timeline_out=s['timeline_out'],source=cname(s['src']),
 framing={k:v for k,v in s['o'].items() if k in('quad','offset','vcrop','pan')}) for s in segs]
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
vreuse=Counter(cname(s['src']) for s in segs if s['o'].get('video'))
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
 PACK.mkdir(parents=True,exist_ok=True);(PACK/'cuts_v01d_plan.json').write_text(json.dumps(plan_cuts(),indent=2))
 (PACK/'picture_qa_reviewed_ok_v01d.json').write_text(json.dumps(QA_OK,indent=2,ensure_ascii=False))
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
for wd in ('v01b','v01c'):
 for ok in Path(f'/private/tmp/earth027_rough_work_{wd}').glob('seg_*.ok'):V01_CACHE[ok.read_text()]=ok.with_suffix('.mp4')
if '--finish-only' not in sys.argv:
 for i,s in enumerate(segs):
  pre=.2 if i else 0;post=.2 if i<len(segs)-1 else 0
  frames=round((s['timeline_out']-s['timeline_in']+pre+post)*FPS);dest=WORK/f'seg_{i:03}.mp4'
  if dest.exists() and (WORK/f'seg_{i:03}.ok').exists() and (WORK/f'seg_{i:03}.ok').read_text()==okkey(s):
   print('reuse',i,s['row'],flush=True);continue
  old=V01_CACHE.get(okkey(s)) if (i and i<len(segs)-1) else None
  if old and old.exists():
   import os;dest.unlink(missing_ok=True);os.link(old,dest);(WORK/f'seg_{i:03}.ok').write_text(okkey(s))
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
 for k,(name,t,t_end) in enumerate(LABELS):
  img=Image.new('RGBA',(1920,1080),(0,0,0,0));sh=Image.new('RGBA',(1920,1080),(0,0,0,0))
  ImageDraw.Draw(sh).text((96,958),name,font=f3,fill=(0,0,0,190));sh=sh.filter(ImageFilter.GaussianBlur(5))
  img=Image.alpha_composite(sh,img);ImageDraw.Draw(img).text((92,954),name,font=f3,fill='white')
  p=WORK/f'label_{k}.png';img.save(p);ov.append((p,t,t_end))
 inputs=['-i',WORK/'picture_raw.mp4'];fc='[0:v]null[v0];'
 for k,(p,a,b) in enumerate(ov):
  inputs+=['-loop','1','-t',TOTAL,'-i',p]
  fc+=f"[{k+1}:v]fade=t=in:st={a:.3f}:d=0.25:alpha=1,fade=t=out:st={b-0.25:.3f}:d=0.25:alpha=1[o{k}];[v{k}][o{k}]overlay=enable='between(t,{a:.3f},{b:.3f})'[v{k+1}];"
 fc+=f"[v{len(ov)}]fade=t=out:st={TOTAL-FADE:.3f}:d={FADE},format=yuv420p[v]"
 run([*inputs,'-filter_complex',fc,'-map','[v]','-t',TOTAL,*ENC,WORK/'picture.mp4'])
 (PACK/'overlays_v01d.json').write_text(json.dumps([dict(file=Path(p).name,start=round(a,3),end=round(b,3)) for p,a,b in ov],indent=2))

 # No bed until 30 Oct (J0077): VO alone, padded to the runtime, two-pass loudnorm to -14 LUFS.
 mix=f'[0:a]apad=whole_dur={TOTAL},atrim=0:{TOTAL},asetpts=PTS-STARTPTS'
 first=sp.run(['ffmpeg','-hide_banner','-i',str(VO),'-filter_complex',mix+',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]','-map','[a]','-f','null','-'],capture_output=True,text=True).stderr
 st=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',first,re.S)[-1]);(PACK/'loudnorm_first_pass.json').write_text(json.dumps(st,indent=2))
 norm=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
 run(['-i',VO,'-filter_complex',mix+','+norm+'[a]','-map','[a]','-ar','48000','-c:a','aac','-b:a','192k',WORK/'audio.m4a'])
 OUT.parent.mkdir(parents=True,exist_ok=True)
 run(['-i',WORK/'picture.mp4','-i',WORK/'audio.m4a','-map','0:v','-map','1:a','-c','copy','-t',TOTAL,'-movflags','+faststart',WORK/OUT.name])
 sp.run(['cp',str(WORK/OUT.name),str(OUT)],check=True)

# ---- checks and review pack
runtime=probe(OUT)
ll=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
lufs=float(re.findall(r'I:\s*([-\d.]+) LUFS',ll)[-1])
checks=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-vf','blackdetect=d=0.1:pix_th=0.10:pic_th=0.98,freezedetect=n=-50dB:d=0.8','-an','-f','null','-'],capture_output=True,text=True).stderr
(PACK/'ffmpeg_checks.txt').write_text('\n'.join(l for l in checks.splitlines() if 'black_' in l or 'freeze' in l))
cuts=[dict(row=s['row'],timeline_in=s['timeline_in'],timeline_out=s['timeline_out'],source=cname(s['src']),
 framing={k:v for k,v in s['o'].items() if k in('quad','offset','vcrop','pan')},src_w=s['src_w'],upscale=s['upscale']) for s in segs]
(PACK/'cuts_v01d.json').write_text(json.dumps(cuts,indent=2));(PACK/'picture_qa_reviewed_ok_v01d.json').write_text(json.dumps(QA_OK,indent=2,ensure_ascii=False))
reuse_rows={n:[s['row'] for s in stills if s['src'].name==n] for n in sorted(reuse,key=lambda n:(-reuse[n],n))}
(PACK/'reuse_v01d.json').write_text(json.dumps(dict(stills=dict(sorted(reuse.items(),key=lambda x:(-x[1],x[0]))),rows=reuse_rows,
 video=dict(sorted(vreuse.items(),key=lambda x:(-x[1],x[0])))),indent=2))
buf=io.StringIO();wr=csv.writer(buf);wr.writerow(['row','source','vo_in','vo_out','vo_text'])
for c in cuts:
 text=' '.join(w['text'] for w in words if c['timeline_in']<=(w['start']+w['end'])/2<c['timeline_out'])
 wr.writerow([c['row'],c['source'],f"{c['timeline_in']:.3f}",f"{c['timeline_out']:.3f}",text or '[no VO]'])
(PACK/'earth_spin_rough_v01d_assembled.csv').write_text(buf.getvalue());(PACK/'earth_spin_words_list.json').write_text(json.dumps(words))
cc=sp.run([sys.executable,str(CLIP_CHECK),str(PACK/'earth_spin_rough_v01d_assembled.csv'),'--words',str(PACK/'earth_spin_words_list.json')],capture_output=True,text=True)
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
sheet('per_row_sheet_v01d',tiles)
fill=[dict(row=c['row'],cut=k,source=c['source'],frac=round(border_fill_fraction(frames/f"row_{k:03}.jpg"),4)) for k,c in enumerate(cuts)]
for f in fill:
 if f['frac']>FILL_MAX and f['source'] in REVIEWED_OK:f.update(status='reviewed_ok',note=REVIEWED_OK[f['source']])
fill_fail=[f for f in fill if f['frac']>FILL_MAX and 'status' not in f]
fill_reviewed=[f for f in fill if f.get('status')=='reviewed_ok']
(PACK/'fill_gate_v01d.json').write_text(json.dumps(dict(rule='fail if near-black(<12)/near-white(>245) pixels touching the border cover > 1.5% of the row frame',verdict='WARN' if fill_fail else 'PASS',note=FILL_NOTE,fail=fill_fail,reviewed_ok=fill_reviewed,rows=fill),indent=2))
freezes=[l for l in checks.splitlines() if 'freeze_duration' in l]
def tsheet(name,times):
 items=[]
 for i,t in enumerate(times):p=WORK/f'f_{name}_{i}.jpg';grab(t,p);items.append((p,f'{t:.2f}s'))
 sheet(name,items,cols=3)
tsheet('frame0_sheet',[0,.2,.4,.6,.8,1])
tsheet('sheet_0_8s',[0,1,2,3,4,5,6,6.4,6.6,7,7.5,8])
om=[c for c in cuts if c['source'].startswith('orbit_')]
if om:tsheet('sheet_omni',[t for c in om for t in (c['timeline_in']+0.5,(c['timeline_in']+c['timeline_out'])/2,c['timeline_out']-0.5)])
tsheet('sheet_cards_sub',[o['start']+1.0 for o in json.loads((PACK/'overlays_v01d.json').read_text())])
tsheet('sheet_end',[LAST_WORD-1,LAST_WORD+0.5,LAST_WORD+1.5,LAST_WORD+2.5,TOTAL-0.5,TOTAL-0.05])
h=hashlib.sha256()
with OUT.open('rb') as f:
 for b in iter(lambda:f.read(1<<20),b''):h.update(b)
(PACK/'SHA256.txt').write_text(f'{h.hexdigest()}  {OUT.name}\n')
summary=dict(fill_gate='WARN' if fill_fail else 'PASS',fill_fail=fill_fail,fill_reviewed_ok=[(f['row'],f['source'],f['frac']) for f in fill_reviewed],freezes_over_0_8s=freezes,sentence_end_rows=SENT_NOTE,out=str(OUT),sha256=h.hexdigest(),runtime=runtime,lufs=lufs,clip_check_exit=cc.returncode,align=align,reuse_stills=dict(reuse))
(PACK/'polish_reviewed_ok_v01d.json').write_text(json.dumps(POLISH_OK,indent=2))
pg=sp.run([sys.executable,str(POLISH),str(WORK/OUT.name),'--cuts',str(PACK/'cuts_v01d.json'),'--out',str(PACK/'polish_gate_v01d.json'),'--reviewed-ok',str(PACK/'polish_reviewed_ok_v01d.json')],capture_output=True,text=True)
(PACK/'polish_gate_v01d.txt').write_text(pg.stdout+pg.stderr);summary['polish_gate']='PASS' if pg.returncode==0 else 'FAIL'
(PACK/'summary_v01d.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=1));print(cc.stdout+cc.stderr)
