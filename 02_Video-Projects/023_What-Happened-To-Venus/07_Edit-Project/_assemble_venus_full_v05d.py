#!/usr/bin/env python3
"""Venus 023 full cut v05d (J0096): Ben's v05c notes (board 9 Oct 13:36Z), Claude's J0095 graphics; only these rows change.
- Rows 13c+14a+14b (78.20-96.27): one graphics_v03 `albedo` clip (18.1 s) from offset 0 across the three rows
  (14b's PIA00104 is out). Row 31: graphics_v03 `heavyh` (10.9 s). Rows 32a+32b: one `deuterium` (13.3 s), 32b's PIA00257 out.
- Round 3 (Chief #6093640970): albedo and heavyh from graphics_v05 (4% linear pull-back, no hold over 1.5 s); deuterium stays graphics_v04.
- Row 30b: both AC78-9245 spans (all four Multiprobe probes) -> the NSSDCA/NASA Ames painting of the Large Probe alone
  (pv_probe.jpg, 800x1051), on a feathered blur fill: whole painting first, then the probe and heat shield (lower 58%).
- Rows 39a/39b: plates_v04 (round 2: 100 px two-line labels, graded backdrop under black; 39b PIA00257 globe, Alpha Regio ringed, push into PIA00147 ridged upland).
- A video segment that starts at offset 0 clones its first frame for the 0.2 s lead under the crossfade, so the
  clip's beats stay on the voice (v05c clamped that lead and ran the graphic 0.2 s early).
v05c notes:
Venus 023 full cut v05c (J0059): Claude #6080054846 on v05b, only these rows change.
- Rows 13a, 13b: AIA171 transit cropped to the top 1626x915 (x 147), 1.18x, so the burnt-in timestamp
  (bottom left, y 919-956) is out of frame; Venus and the Sun stay in frame through the zoom-out.
- Row 30b second cut: the 1978 painting ARC-1978-AC78-0238 (banded, Jupiter-like) -> the real Pioneer Venus Orbiter
  ultraviolet cloud image of 5 Feb 1979 (NSSDCA pvo_uv_790205, NASA), disc cut from the scanned page onto black.
  Claude's examples PIA00072/PIA00073 are Galileo 1990 images, not Pioneer Venus, so they were not used.
v05b notes:
Venus 023 full cut v05b (J0059): Claude #6079629063 on v05, only these rows change.
- Row 51 splits on "sun, | looked": the flyby animation (svs 181 s) stays on "a probe on its way to the sun", then the real
  WISPR night side (svs 171.1 s; the shot runs 170.5-177.2 s, so 171.3 would cut into the next shot) cropped clear of the
  right-edge gutter (vcrop 1824x1026, 1.05x) on "looked at the night side of Venus ... through the clouds".
- Row 56: Venus (the dot left of the Moon) and the Moon both in frame, ~1.1x, slow sideways drift.
- Rows 37, 38, 43a, 43b: every frame (the plate's clone-held tail included) goes through a float-box push (`move`=(z0,z1)),
  so no hold sits still; 43b carries on 43a's zoom.
v05 notes:
Venus 023 full cut v05 (J0059): Ben's v04 watch ('wobbly', 'unfinished', 'not polished'), Claude's rulings #6079012304.
- Every still push/drift goes through scripts/still_motion.py (float crop boxes); no zoompan anywhere.
- svs14095 kept at row 22 and the first row-51 cut only; rows 34a, 34b (second half) and 50 are Magellan 3D views
  with a different crop from their first use. AIA171 at 45b -> Magellan global PIA00271 on black.
- Row 44a HMI transit reframed so the burnt-in timestamp (bottom left) is out of frame; 44b (was line.mp4) is a later,
  differently framed part of the same real SDO transit (every Earth plate is already at two uses).
- Row 56: tight crops on the Moon and Venus (<=2x) with a slow sideways drift, not a push.
- Music: 023's own score bed (05_Music/venus_score_bed_v01_full.mp3, music_gate PASS), as 025 lays its bed.
v04 notes:
Venus 023 full first cut v04 (J0003): v03 with row 43c only changed (Claude 6050575895).
- Row 43c: S91-50688 as a top-left limb crop filling the frame (box=(0.05,0.0833,0.60) of the 6000 px still),
  slow 4% push; row 28 keeps the same still as the full disc on black, so the second use is a different framing.
v03 notes (6050173783), unchanged:
- Row 52: the PEVAA descent from 12 s carries on through "DAVINCI,"; the second half is the text-free highland
  descent at 62.8-67.5 s of SVS 13887 (between "SNAP!" and the next thought bubble), cut into row 53 on "Regio, | and".
- Upscale: every row records src_w and upscale (source px -> 1080p output, push included); assert upscale <= 2.35.
  The 1250 px Magellan stills are full-frame only.
- Rainbow hemisphere globes (PIA00007/008/157/158/159/160): at most 4, never adjacent, only on mapping lines
  (16b, 49a). The rest are surface 3D views, the grey Magellan globe PIA00478, and SVS 14095 spans
  (cloud globe 124 s, surface 130 s, Venera 13 at 153 s with the credit line cropped off, cloud-to-radar globe 161 s).
Everything else as v02: <=2 uses per still with a different framing, holds <=7 s, cuts in VO pauses,
locked VO untouched, house bed full runtime, hold 2.5 s past the last word, then 1 s fade, -14 LUFS.
`--plan` prints the segment list, reuse counts and checks without rendering."""
from pathlib import Path
import json, subprocess as sp, re, hashlib, math, sys, csv, io
from collections import Counter
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS = None
HERE=Path(__file__).resolve().parent; EP=HERE.parent
UAT=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/OWB UAT'
WORK=Path('/private/tmp/venus023_full_work_v05d'); PACK=HERE/'full_rough_v05d_pack'
VO=EP/'02_Voiceover/venus_vo_v01.mp3'
OUT=Path('/private/tmp/023_Venus_full_rough_v05d.mp4')  # iCloud locks the UAT copy mid-read; the phone copy goes to UAT
MAX_UP=2.35; RAINBOW={'PIA00007.jpg','PIA00008.jpg','PIA00157.jpg','PIA00158.jpg','PIA00159.jpg','PIA00160.jpg'}
POOL=HERE/'nasa_pool_v01'; RAW=EP/'04_Generated-Clips/01_Raw'; G1=RAW/'graphics_v01'; G2=RAW/'graphics_v02'; G3=RAW/'graphics_v04'; G5=RAW/'graphics_v05'
PL3=RAW/'plates_v04'; PROBE='pioneer/pv_probe.jpg'
H4=POOL/'harvest_v04'; SVS=H4/'svs14095_14095_ParkerVenus_YouTube_NoText_NoMusic.mp4'
FPS=30; LAST_WORD=509.50; HOLD=2.5; FADE=1.0; TOTAL=round((LAST_WORD+HOLD+FADE)*FPS)/FPS
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
CLIP_CHECK=EP.parents[1]/'00_Brand/Channel-Setup/tools/clip_check.py'
PLAN='--plan' in sys.argv
words=json.loads((EP/'02_Voiceover/words.json').read_text())['words']
P=[c['timeline_in'] for c in json.loads((HERE/'part01_rough_v03_pack/cuts_v03.json').read_text())]

def run(args):
 p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-6000:])
def probe(p):return float(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
def fr(t):return round(t*FPS)/FPS

sys.path.insert(0,str(EP.parents[1]/'scripts'))
from still_motion import render as sm_render
BED=EP/'05_Music/venus_score_bed_v01_full.mp3'
if not PLAN:
 GPY=Path.home()/'.venvs/orbit-code-graphics/bin/python'
 LINE_A=365.00-350.92; LINE_S=LINE_A+(389.88-381.70)
 for name,secs in (('line',LINE_S),):
  if not (G2/f'{name}.mp4').exists():
   sp.run([str(GPY),str(HERE/'code_graphics.py'),name,str(G2),'--seconds',f'{secs+0.5:.2f}'],check=True)

Q={'tl':(0.0,0.0),'tr':(0.5,0.0),'bl':(0.0,0.5),'br':(0.5,0.5),'c':(0.25,0.25)}
O,M,L,E,V='open/','magellan_extra/','harvest_v04/','earth/','harvest_v02/'
PLA=RAW/'plates_v01/venus_ch3_plateA_ocean_nasa_v01.mp4'
# (row, nominal in, source, opts). fixed=True keeps the time exactly (Part01 v03 PASS cuts, card breaths, Omni 0-5 s).
# Video opts: at = source time at this segment's in-point; base = timeline time where a continuing clip's `at` applies.
S=[('1',P[0],O+'PIA00254.jpg',dict(fixed=1)),('2',P[1],O+'PIA00106.jpg',dict(fixed=1)),
 ('3',P[2],L+'PIA13001.jpg',dict(fixed=1)),('4',P[3],O+'PIA00241.jpg',dict(fixed=1)),
 ('5',P[4],L+'PIA00108.jpg',dict(fixed=1)),('6',P[5],O+'PIA23791.jpg',dict(fixed=1,disc='right')),
 ('7',P[6],O+'PIA00104.jpg',dict(fixed=1)),('8',P[7],L+'PIA00257.jpg',dict(fixed=1)),('8',P[8],L+'PIA00107.jpg',dict(fixed=1,quad='bl')),
 ('11a',P[9],O+'PIA23791.jpg',dict(fixed=1,disc='left')),('11b',P[10],L+'PIA00270.jpg',dict(fixed=1)),
 ('12a',P[11],L+'S91-50686.jpg',dict(fixed=1)),('12b',P[12],L+'PIA00252.jpg',dict(fixed=1)),
 ('13a',P[13],POOL/'sdo/AIA171VenusTransit_HD1080.mp4',dict(fixed=1,video=1,at=8.0,vcrop=(147,0,1626,915))),
 ('13b',P[14],POOL/'sdo/AIA171VenusTransit_HD1080.mp4',dict(fixed=1,video=1,at=8.0,base=P[13],vcrop=(147,0,1626,915))),
 ('13c',P[15],G5/'albedo.mp4',dict(fixed=1,video=1,at=0.0)),('14a',P[16],G5/'albedo.mp4',dict(fixed=1,video=1,at=0.0,base='13c')),
 ('14b',P[17],G5/'albedo.mp4',dict(fixed=1,video=1,at=0.0,base='13c')),('15a',P[18],L+'PIA00272.jpg',dict(fixed=1)),
 ('15b',P[19],M+'PIA00215.jpg',dict(fixed=1,clear=1)),('16a',P[20],O+'PIA00240.jpg',dict(fixed=1,clear=1)),
 ('16b',P[21],M+'PIA00159.jpg',dict(fixed=1)),('17',P[22],M+'PIA00246.jpg',dict(fixed=1)),('17',124.97,L+'PIA00107.jpg',{}),
 ('18',P[24],L+'PIA00102.jpg',dict(fixed=1)),('18',134.07,L+'PIA00233.jpg',{}),('18',138.13,L+'PIA00268.jpg',{}),
 ('20b',142.57,L+'PIA00481.jpg',dict(fixed=1,quad='tl')),('21a',148.63,L+'PIA00272.jpg',dict(quad='tl')),('21b',153.97,E+'as17-148-22727.jpg',{}),
 ('21c',160.33,L+'PIA00271.jpg',{}),('22',165.00,M+'PIA00103.jpg',{}),('22',171.0,SVS,dict(video=1,at=130.0)),
 ('23',176.97,E+'PIA18033.jpg',{}),('23',180.9,E+'GSFC_20171208_Archive_e001435.jpg',{}),
 ('24',185.82,V+'s129e007324.jpg',dict(crop_bottom=0.045)),('24',189.30,V+'PIA03877.jpg',{}),
 ('25',194.37,E+'GSFC_20171208_Archive_e001435.jpg',dict(quad='tr')),('25',198.3,V+'PIA03877.jpg',dict(quad='bl')),
 ('26',201.97,L+'PIA00234.jpg',{}),('26',207.70,M+'PIA00200.jpg',{}),('27',212.17,O+'PIA00106.jpg',dict(quad='br')),
 ('28',218.13,'harvest_v03/S91-50688.jpg',dict(on_black=1,pct=.04)),
 ('30b',224.15,PROBE,dict(fixed=1,blur='full')),('30b',229.0,'pioneer/pvo_uv_790205.jpg',dict(on_black=1)),('30b',233.61,PROBE,dict(blur='low')),
 ('31',236.17,G5/'heavyh.mp4',dict(video=1,at=0.0)),('32a',247.10,G3/'deuterium.mp4',dict(video=1,at=0.0)),
 ('32b',253.1,G3/'deuterium.mp4',dict(video=1,at=0.0,base='32a')),('32c',260.43,M+'PIA00084.jpg',dict(quad='tl')),('32c',264.3,M+'PIA00200.jpg',dict(quad='tl')),
 ('33',268.43,L+'PIA00102.jpg',dict(quad='bl')),('34a',274.90,L+'PIA00108.jpg',dict(box=(0.08,0.08,0.84))),
 ('34a',280.0,L+'PIA00233.jpg',dict(box=(0.08,0.10,0.84))),
 ('34b',283.77,O+'PIA00240.jpg',dict(quad='tl')),('34b',287.6,L+'PIA00266.jpg',dict(box=(0.06,0.10,0.88))),
 ('35',291.27,PLA,dict(video=1,at=0.0)),('35',296.5,L+'S91-50687.jpg',{}),('35',301.0,L+'S91-50686.jpg',dict(quad='br')),
 ('36',305.33,PLA,dict(video=1,at=0.0,base='35')),
 ('37',312.43,RAW/'plates_v02/venus_ch3_row37_plateB_steam_lid_sharp_v02.mp4',dict(video=1,tpad=1,move=(1.0,1.08))),
 ('38',320.33,G1/'nightlid.mp4',dict(video=1,at=0.0,move=(1.0,1.10))),
 ('39a',330.90,PL3/'venus_row39a_split_labelled_v04.mp4',dict(video=1,tpad=1)),
 ('39b',334.60,PL3/'venus_row39b_alpha_regio_v04.mp4',dict(video=1,tpad=1)),
 ('40',338.47,L+'PIA00109.jpg',{}),('40',343.10,L+'PIA00209.jpg',{}),
 ('42b',347.89,E+'PIA18033.jpg',dict(fixed=1,quad='c')),
 ('43a',350.53,G2/'line.mp4',dict(video=1,at=0.0,move=(1.0,1.06))),('43b',356.33,G2/'line.mp4',dict(video=1,at=0.0,base='43a',move=(1.06,1.12))),
 ('43c',365.83,'harvest_v03/S91-50688.jpg',dict(box=(0.05,0.0833,0.60),pct=.04)),
 ('44a',373.23,POOL/'sdo/HMIVenusTransit_HD1080.mp4',dict(video=1,at=5.0,vcrop=(480,0,1440,810))),
 ('44b',382.07,POOL/'sdo/HMIVenusTransit_HD1080.mp4',dict(video=1,at=45.0,vcrop=(560,40,1280,720))),
 ('45a',389.50,V+'s129e007324.jpg',dict(quad='tl')),('45a',393.3,E+'as17-148-22727.jpg',dict(quad='c')),
 ('45b',398.9,L+'PIA00271.jpg',dict(on_black=1)),('45c',403.00,L+'PIA00266.jpg',{}),
 ('46',409.60,RAW/'omni_v01/orbit_looks_back_earth_omni_v01_t0-5s.mp4',dict(fixed=1,video=1,at=0.0)),
 ('46',414.60,M+'PIA00084.jpg',dict(before=1)),
 ('48b',417.23,O+'PIA00241.jpg',dict(fixed=1,quad='bl')),('49',420.27,L+'PIA00157.jpg',dict(on_black=1)),
 ('49',425.43,L+'PIA00481.jpg',{}),('49',429.77,M+'PIA00215.jpg',dict(clear=1,quad='c')),
 ('50',434.93,L+'PIA00109.jpg',dict(box=(0.06,0.06,0.88))),('50',440.23,L+'PIA00268.jpg',dict(quad='tr')),
 ('51',445.10,SVS,dict(video=1,at=181.0)),('51',448.48,SVS,dict(video=1,at=171.1,vcrop=(0,27,1824,1026))),
 ('52',454.27,POOL/'harvest_v03/13887_DAVINCI_PEVAA.mp4',dict(video=1,at=12.0)),
 ('52',461.79,POOL/'harvest_v03/13887_DAVINCI_PEVAA.mp4',dict(video=1,at=62.8)),
 ('53',466.46,'harvest_v03/veritas-cut7-16.jpg',{}),('53',471.73,M+'PIA00103.jpg',dict(quad='tl')),
 ('54',475.13,L+'PIA00252.jpg',dict(on_black=1)),('54',481.60,L+'S91-50687.jpg',dict(quad='bl')),
 ('55',487.60,L+'PIA00270.jpg',dict(on_black=1)),
 ('56',494.53,V+'NHQ202605180003.jpg',dict(box=(0.245,0.147,0.34),pct=.03,drift=1)),
 ('56',499.97,V+'NHQ202605180003.jpg',dict(box=(0.232,0.138,0.36),pct=.03,drift=-1)),
 ('57',505.13,O+'PIA00254.jpg',dict(pct=.06,bookend=1))]
CARDS=[('The Twin Next Door',43.74,'abs'),('A Blanket With No Way Out',142.92,''),('Where Did the Water Go?',224.50,''),
 ("The Line Earth Hasn't Crossed",348.24,''),('Going Back',417.58,'')]

GAPS=[((a['end']+b['start'])/2,b['start']-a['end']) for a,b in zip(words,words[1:])]
def snap(t,before=False):
 """Midpoint of the nearest VO pause (>=0.30 s, else >=0.20 s) within 2 s; before=True only looks earlier."""
 for need in (0.30,0.20):
  c=[m for m,g in GAPS if g>=need and abs(m-t)<=2.0 and (not before or m<=t-0.2)]
  if c:return min(c,key=lambda m:abs(m-t))
 raise SystemExit(f'no VO pause near {t}')

segs=[]
for i,(row,t,src,o) in enumerate(S):
 tin=t if (i==0 or o.get('fixed')) else snap(t,o.get('before'))
 segs.append(dict(row=row,timeline_in=fr(tin),src=Path(src) if isinstance(src,Path) else POOL/src,o=dict(o)))
for a,b in zip(segs,segs[1:]):a['timeline_out']=b['timeline_in']
segs[-1]['timeline_out']=TOTAL
first_in={}
for s in segs:first_in.setdefault(s['row'],s['timeline_in'])
for s in segs:
 o=s['o']
 if o.get('video'):
  base=o.get('base');base=first_in[base] if isinstance(base,str) else base
  o['offset']=o.get('at',0.0)+((s['timeline_in']-base) if base is not None else 0.0)

def strip_bars(im):
 a=np.array(im.convert('L')).astype(float);sd=a.std(axis=0);ok=np.flatnonzero(sd>8)
 return im.crop((int(ok[0]),0,int(ok[-1])+1,im.height))
def clear_box(im,thresh=14,run_=20,margin=8):
 """Smallest centred 16:9 crop of a greyscale still whose edges hold no Magellan no-data black (Part01 v03)."""
 a=np.array(im.convert('L')).astype(int);h,w=a.shape;nd=a>=thresh
 def edge(r):
  k=np.convolve(r.astype(int),np.ones(run_,int),'valid')
  hit=np.flatnonzero(k==run_);return int(hit[0]) if len(hit) else len(r)
 left=np.array([edge(nd[y]) for y in range(h)]);right=np.array([edge(nd[y][::-1]) for y in range(h)])
 cx,cy=w/2,h/2
 for hw in range(int(min(cx,cy*16/9)),100,-2):
  hh=hw*9/16;y0,y1=int(cy-hh),int(cy+hh);x0,x1=int(cx-hw),int(cx+hw)
  if x0>=left[y0:y1].max()+margin and w-x1>=right[y0:y1].max()+margin:return (x0,y0,x1,y1)
 raise RuntimeError('no clear box')
def framed(s):
 """The still cropped to its framing (for on_black globes: the disc only, outside masked)."""
 im=Image.open(s['src']).convert('RGB');o=s['o']
 if o.get('crop_bottom'):im=im.crop((0,0,im.width,int(im.height*(1-o['crop_bottom']))))
 if o.get('strip_bars'):im=strip_bars(im)
 if o.get('blur')=='low':im=im.crop((0,int(im.height*0.42),im.width,im.height))
 if o.get('disc')=='right':im=im.crop((1145,0,2245,1096))
 if o.get('disc')=='left':im=im.crop((0,0,1075,1096))
 if o.get('clear'):im=im.crop(clear_box(im))
 if 'band' in o:
  top,inset=o['band'];w=int(im.width*(1-inset));h=int(w*9/16);x=(im.width-w)//2;y=int(im.height*top)
  im=im.crop((x,y,x+w,y+h))
 if 'box' in o:
  x0,y0,bw=o['box'];w=int(im.width*bw);h=int(w*9/16);x=int(im.width*x0);y=int(im.height*y0)
  im=im.crop((x,y,x+w,y+h))
 if 'quad' in o:
  fx,fy=Q[o['quad']];im=im.crop((int(im.width*fx),int(im.height*fy),int(im.width*(fx+.5)),int(im.height*(fy+.5))))
 if o.get('on_black') and s['src'].name!='S91-50688.jpg':
  # hemispheric views: whole disc on black; everything outside the disc (incl. the colour scale) blacked out
  a=np.array(im);h,w=a.shape[:2];yy,xx=np.ogrid[:h,:w];a[(yy-h/2)**2+(xx-w/2)**2>(0.488*min(h,w))**2]=0;im=Image.fromarray(a)
  im=im.crop(im.convert('L').point(lambda v:255 if v>20 else 0).getbbox())
 return im
def upscale(s,im=None):
 """Source px -> 1080p output px for this shot, the still push included."""
 o=s['o']
 if o.get('video'):
  w,h=map(int,sp.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0',str(s['src'])],text=True).split(',')[:2])
  if o.get('vcrop'):w,h=o['vcrop'][2:]
  return w,max(1920/w,1080/h)
 im=im or framed(s);push=1+o.get('pct',.05)
 if o.get('blur'):return im.width,1080/im.height*push
 if o.get('on_black'):
  if s['src'].name=='S91-50688.jpg':return im.width,1080*1.12/im.height*push
  return im.width,1080*0.94/max(im.size)*push
 return im.width,max(1920/im.width,1080/im.height)*push

# ---- checks Claude asked for: reuse <= 2 per still with a different framing, holds <= 7 s, cuts in VO pauses,
# upscale <= 2.35, rainbow globes <= 4 and never adjacent
stills=[s for s in segs if not s['o'].get('video')]
reuse=Counter(s['src'].name for s in stills)
problems=[]
for name,n in reuse.items():
 uses=[s for s in stills if s['src'].name==name]
 if name=='PIA00254.jpg':
  if [s['row'] for s in uses]!=['1','57']:problems.append(f'{name} only as bookends 1/57')
  continue
 if n>2:problems.append(f'{name} used {n}x')
 if n==2:
  fa,fb=[{k:v for k,v in s['o'].items() if k in('quad','on_black','disc','band','clear','crop_bottom','box','blur')} for s in uses]
  if fa==fb:problems.append(f'{name} second use has the same framing')
if 'PIA00087.jpg' in reuse:problems.append('PIA00087 still in the cut')
for s in segs:
 d=s['timeline_out']-s['timeline_in']
 if d<2.0:problems.append(f"{s['row']} {s['timeline_in']} only {d:.2f}s")
 if not s['o'].get('video') and not s['o'].get('bookend') and d>7.05:problems.append(f"still {s['row']} {s['src'].name} held {d:.2f}s")
 if s['o'].get('video') and d>11.0+1e-6:problems.append(f"video {s['row']} held {d:.2f}s")
for s in segs[1:]:
 c=s['timeline_in']
 near=[w for w in words if w['start']+0.02<c<w['end']-0.02]
 if near:problems.append(f"cut {c:.2f} ({s['row']}) inside '{near[0]['text']}' {near[0]['start']:.2f}-{near[0]['end']:.2f}")
for s in segs:
 if not s['src'].exists():problems.append(f'missing {s["src"]}');continue
 s['src_w'],s['upscale']=upscale(s);s['upscale']=round(s['upscale'],3)
 if s['upscale']>MAX_UP:problems.append(f"{s['row']} {s['src'].name} upscale {s['upscale']:.2f} > {MAX_UP}")
globes=[i for i,s in enumerate(segs) if s['src'].name in RAINBOW]
if len(globes)>4:problems.append(f'{len(globes)} rainbow globes > 4')
for a_,b_ in zip(globes,globes[1:]):
 if b_==a_+1:problems.append(f"rainbow globes adjacent at {segs[a_]['row']}/{segs[b_]['row']}")
if PLAN or problems:
 for s in segs:print(f"{s['row']:>4} {s['timeline_in']:8.2f} {s['timeline_out']-s['timeline_in']:5.2f}  {s['src'].name[:44]:44} up {s.get('upscale',0):4.2f} {json.dumps({k:v for k,v in s['o'].items() if k not in('fixed',)})}")
 print('reuse:',dict(sorted(reuse.items(),key=lambda x:-x[1])))
 print('rainbow globes:',[segs[i]['row'] for i in globes])
 print('problems:',problems or 'none')
 if problems:raise SystemExit(1)
 raise SystemExit(0)

def prep_still(s,dest):
 im=framed(s);o=s['o']
 im=ImageEnhance.Color(im).enhance(1.10);im=ImageEnhance.Contrast(im).enhance(1.04)
 if o.get('blur'):
  # portrait art at full height over a dark blurred copy of itself, sides feathered into the blur
  k=1188/im.height;fg=im.resize((round(im.width*k),1188),Image.Resampling.LANCZOS)
  kb=max(2112/im.width,1188/im.height);bg=im.resize((round(im.width*kb),round(im.height*kb)),Image.Resampling.LANCZOS)
  bx,by=(bg.width-2112)//2,(bg.height-1188)//2;bg=bg.crop((bx,by,bx+2112,by+1188)).filter(ImageFilter.GaussianBlur(40))
  bg=ImageEnhance.Brightness(bg).enhance(0.80)
  # the fill's dark side goes onto a warm grade, so the frame isn't mostly near-black (Chief, 10 Oct: 30b 31-35%)
  yy,xx=np.mgrid[0:1188,0:2112].astype(np.float32);rg=np.clip(np.hypot((xx-1056)/1300,(yy-594)/900),0,1)[...,None]
  warm=np.array([110,48,30],np.float32)*(1-rg)+np.array([62,30,26],np.float32)*rg
  f=np.asarray(bg,np.float32);w=np.clip(1-f.max(axis=2,keepdims=True)/90.0,0,1)
  bg=Image.fromarray(np.clip(f*(1-w)+warm*w+f*w*0.5,0,255).astype(np.uint8))
  feather=60;m=np.ones(fg.width,float);r=np.linspace(0,1,feather);m[:feather]=r;m[-feather:]=r[::-1]
  mask=Image.fromarray((np.tile(m,(1188,1))*255).astype(np.uint8))
  bg.paste(fg,((2112-fg.width)//2,0),mask);bg.save(dest);return
 if o.get('on_black'):
  if s['src'].name=='S91-50688.jpg':
   # globe larger than the frame height so the bottom data-gap notch sits below frame; space stays black
   d=round(1188*1.12);g=im.resize((d,d),Image.Resampling.LANCZOS);c=Image.new('RGB',(2112,1188),(0,0,0))
   c.paste(g,((2112-d)//2,-round(d*0.03)));c.save(dest);return
  d=round(1188*0.94);k=d/max(im.size);g=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.LANCZOS);c=Image.new('RGB',(2112,1188),(0,0,0))
  c.paste(g,((2112-g.width)//2,(1188-g.height)//2));c.save(dest);return
 im=im.point([min(255,int(v*.92+28)) for v in range(256)]*3)
 scale=max(2112/im.width,1188/im.height)
 im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 x=(im.width-2112)//2;y=(im.height-1188)//2;im.crop((x,y,x+2112,y+1188)).save(dest)

WORK.mkdir(parents=True,exist_ok=True);PACK.mkdir(parents=True,exist_ok=True)
ENC=['-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4']
def move_video(src,frames,dest,z0,z1):
 """Float-box push over a rendered 1920x1080 clip (still_motion's method, per frame), so a held frame never sits still."""
 n_px=1920*1080*3
 dec=sp.Popen(['ffmpeg','-v','error','-i',str(src),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=sp.PIPE)
 enc=sp.Popen(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r',str(FPS),'-i','-',
  '-vf','setsar=1,format=yuv420p','-frames:v',str(frames),*ENC,str(dest)],stdin=sp.PIPE)
 last=None
 for n in range(frames):
  b=dec.stdout.read(n_px)
  if len(b)==n_px:last=Image.frombytes('RGB',(1920,1080),b)
  z=z0+(z1-z0)*n/frames;w,h=1920/z,1080/z
  enc.stdin.write(last.resize((1920,1080),Image.Resampling.BICUBIC,box=((1920-w)/2,(1080-h)/2,(1920+w)/2,(1080+h)/2)).tobytes())
 enc.stdin.close();dec.stdout.close();dec.wait()
 if enc.wait():raise RuntimeError(f'move_video failed: {dest}')
def okkey(s):return json.dumps([s['timeline_in'],s['timeline_out'],str(s['src']),s['o']],default=str,sort_keys=True)
if '--finish-only' not in sys.argv:
 for i,s in enumerate(segs):
  pre=.2 if i else 0;post=.2 if i<len(segs)-1 else 0
  frames=round((s['timeline_out']-s['timeline_in']+pre+post)*FPS);dest=WORK/f'seg_{i:02}.mp4';s['render']=str(dest)
  if dest.exists() and (WORK/f'seg_{i:02}.ok').exists() and (WORK/f'seg_{i:02}.ok').read_text()==okkey(s):
   print('reuse',i,s['row'],flush=True);continue
  print('seg',i,s['row'],s['timeline_in'],s['timeline_out'],s['src'].name,flush=True)
  o=s['o']
  if o.get('video'):
   off=o.get('offset',0.0)
   lead=max(0.0,pre-off)
   vc=o.get('vcrop');vf=(f'crop={vc[2]}:{vc[3]}:{vc[0]}:{vc[1]},' if vc else '')+'scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,setsar=1,tpad=stop_mode=clone:stop_duration=2'+(f':start_mode=clone:start_duration={lead:.3f}' if lead else '')
   if o.get('move'):
    raw=WORK/f'raw_{i:02}.mp4';run(['-ss',max(0,off-pre),'-i',s['src'],'-vf',vf+',format=yuv420p','-frames:v',frames,*ENC,raw])
    move_video(raw,frames,dest,*o['move'])
   else:
    run(['-ss',max(0,off-pre),'-i',s['src'],'-vf',vf+',format=yuv420p','-frames:v',frames,*ENC,dest])
  else:
   plate=WORK/f'plate_{i:02}.png';prep_still(s,plate);pct=o.get('pct',.05);im=Image.open(plate);pw,ph=im.size
   if o.get('drift'):
    # slow sideways drift: fixed crop of 1/(1+pct), slid across the spare width (left->right for +1)
    w,h=pw/(1+pct),ph/(1+pct);y0=(ph-h)/2
    def box(n,w=w,h=h,y0=y0,d=o['drift']):
     f=n/frames if d>0 else 1-n/frames;x=(pw-w)*f;return (x,y0,x+w,y0+h)
   else:
    def box(n,pct=pct):
     z=1+pct*n/frames;w,h=pw/z,ph/z;return ((pw-w)/2,(ph-h)/2,(pw+w)/2,(ph+h)/2)
   sm_render(im,box,frames,dest,enc=ENC)
  got=round(probe(dest)*FPS)
  if got<frames-1:raise RuntimeError(f'seg {i} {s["row"]}: {got} frames < {frames}')
  (WORK/f'seg_{i:02}.ok').write_text(okkey(s))
 chunks=[]
 for i,s in enumerate(segs):
  p=WORK/f'seg_{i:02}.mp4';pre=.2 if i else 0
  center=WORK/f'center_{i:02}.mp4';cd=(s['timeline_out']-s['timeline_in'])-(.2 if i else 0)-(.2 if i<len(segs)-1 else 0)
  run(['-ss',pre+(.2 if i else 0),'-i',p,'-frames:v',round(cd*FPS),*ENC,center]);chunks.append(center)
  if i<len(segs)-1:
   nxt=WORK/f'seg_{i+1:02}.mp4';trans=WORK/f'trans_{i:02}.mp4';length=probe(p)
   run(['-ss',length-.4,'-i',p,'-i',nxt,'-filter_complex','[0:v]setpts=PTS-STARTPTS[a];[1:v]trim=duration=0.4,setpts=PTS-STARTPTS[b];[a][b]xfade=transition=fade:duration=0.4:offset=0,format=yuv420p[v]','-map','[v]','-frames:v',12,*ENC,trans]);chunks.append(trans)
 (WORK/'concat.txt').write_text(''.join(f"file '{p}'\n" for p in chunks))
 run(['-f','concat','-safe','0','-i',WORK/'concat.txt','-c','copy',WORK/'picture_raw.mp4'])

 # Chapter lower-thirds (~2.5 s from the chapter's first word; Ch1 at Part01's 43.74 s) and the subscribe cue.
 def first_word(t):return next(w['start'] for w in words if w['start']>=t-0.01)
 font=ImageFont.truetype(FONT,62);ov=[]
 for k,(title,t,mode) in enumerate(CARDS):
  w=int(font.getlength(title))+70;img=Image.new('RGBA',(1920,1080),(0,0,0,0));d=ImageDraw.Draw(img)
  d.rounded_rectangle((90,860,90+w,990),radius=15,fill=(23,36,55,220));d.text((125,886),title,font=font,fill='white')
  p=WORK/f'card_{k}.png';img.save(p);a=t if mode=='abs' else first_word(t);ov.append((p,a,a+2.5))
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
 (PACK/'overlays_v05d.json').write_text(json.dumps([dict(file=Path(p).name,start=round(a,3),end=round(b,3)) for p,a,b in ov],indent=2))

 # 023's own bed, full runtime (no loop), fading with the picture.
 if probe(BED)<TOTAL:raise SystemExit(f'bed {probe(BED):.1f}s shorter than the cut {TOTAL:.1f}s')
 run(['-i',BED,'-af',f'atrim=0:{TOTAL},asetpts=PTS-STARTPTS,volume=0.134,afade=t=out:st={TOTAL-FADE-1.5:.3f}:d={FADE+1.5}','-c:a','pcm_s24le',WORK/'music.wav'])
 mix=f'[0:a]apad=whole_dur={TOTAL},atrim=0:{TOTAL},asetpts=PTS-STARTPTS[v];[v][1:a]amix=inputs=2:duration=first:normalize=0'
 first=sp.run(['ffmpeg','-hide_banner','-i',str(VO),'-i',str(WORK/'music.wav'),'-filter_complex',mix+',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]','-map','[a]','-f','null','-'],capture_output=True,text=True).stderr
 st=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',first,re.S)[-1]);(PACK/'loudnorm_first_pass.json').write_text(json.dumps(st,indent=2))
 norm=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
 run(['-i',VO,'-i',WORK/'music.wav','-filter_complex',mix+','+norm+'[a]','-map','[a]','-ar','48000','-c:a','aac','-b:a','192k',WORK/'audio.m4a'])
 run(['-i',WORK/'picture.mp4','-i',WORK/'audio.m4a','-map','0:v','-map','1:a','-c','copy','-t',TOTAL,'-movflags','+faststart',OUT])

# ---- checks and review pack
runtime=probe(OUT)
ll=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
lufs=float(re.findall(r'I:\s*([-\d.]+) LUFS',ll)[-1])
checks=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-vf','blackdetect=d=0.1:pix_th=0.10:pic_th=0.98,freezedetect=n=-50dB:d=1','-an','-f','null','-'],capture_output=True,text=True).stderr
(PACK/'ffmpeg_checks.txt').write_text('\n'.join(l for l in checks.splitlines() if 'black_' in l or 'freeze' in l))
fs=[float(x) for x in re.findall(r'freeze_start: ([\d.]+)',checks)];fd=[float(x) for x in re.findall(r'freeze_duration: ([\d.]+)',checks)]
long_holds=[dict(start=round(a,2),dur=round(d,2)) for a,d in zip(fs,fd) if d>1.5 and a<LAST_WORD]
cuts=[dict(row=s['row'],timeline_in=s['timeline_in'],timeline_out=s['timeline_out'],source=s['src'].name,
 framing={k:v for k,v in s['o'].items() if k in('quad','on_black','disc','band','clear','crop_bottom','box','offset','vcrop','blur')},
 src_w=s['src_w'],upscale=s['upscale']) for s in segs]
(PACK/'cuts_v05d.json').write_text(json.dumps(cuts,indent=2))
reuse_rows={n:[s['row'] for s in stills if s['src'].name==n] for n in sorted(reuse,key=lambda n:(-reuse[n],n))}
(PACK/'reuse_v05d.json').write_text(json.dumps(dict(counts=dict(sorted(reuse.items(),key=lambda x:(-x[1],x[0]))),rows=reuse_rows),indent=2))
buf=io.StringIO();wr=csv.writer(buf);wr.writerow(['row','source','vo_in','vo_out','vo_text'])
for c in cuts:
 text=' '.join(w['text'] for w in words if c['timeline_in']<=(w['start']+w['end'])/2<c['timeline_out'])
 wr.writerow([c['row'],c['source'],f"{c['timeline_in']:.3f}",f"{c['timeline_out']:.3f}",text or '[no VO]'])
(PACK/'venus_full_v05d_assembled.csv').write_text(buf.getvalue());(PACK/'venus_words_list.json').write_text(json.dumps(words))
cc=sp.run([sys.executable,str(CLIP_CHECK),str(PACK/'venus_full_v05d_assembled.csv'),'--words',str(PACK/'venus_words_list.json')],capture_output=True,text=True)
(PACK/'clip_check_py.txt').write_text(cc.stdout+cc.stderr)
inside=[c['timeline_in'] for c in cuts[1:] if any(w['start']+0.02<c['timeline_in']<w['end']-0.02 for w in words)]
still_holds=[c['timeline_out']-c['timeline_in'] for c,s in zip(cuts,segs) if not s['o'].get('video')]
align=dict(runtime=runtime,expected=TOTAL,vo_last_word_end=LAST_WORD,hold_after_last_word=HOLD,fade=FADE,cuts=len(cuts),
 cuts_inside_a_word=inside,longest_shot=max(c['timeline_out']-c['timeline_in'] for c in cuts),longest_still=max(still_holds))
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
sheet('per_row_sheet_v05d',tiles)
def tsheet(name,times):
 items=[]
 for i,t in enumerate(times):p=WORK/f'f_{name}_{i}.jpg';grab(t,p);items.append((p,f'{t:.2f}s'))
 sheet(name,items,cols=3)
tsheet('frame0_sheet',[0,.2,.4,.6,.8,1])
r51=[c for c in cuts if c['row']=='51'];r56=[c for c in cuts if c['row']=='56']
r13=[c for c in cuts if c['row'] in('13a','13b')];r30=[c for c in cuts if c['row']=='30b']
def mids(rows):return [(c['timeline_in']+c['timeline_out'])/2 for c in cuts if c['row'] in rows]
tsheet('sheet_v05d_changed_rows',[78.2+3.0,78.2+9.5,78.2+16.5,r30[0]['timeline_in']+1,r30[2]['timeline_in']+1,236.17+3.0,236.17+9.5,247.10+4.5,247.10+11.5,*mids(('39a','39b'))])
tsheet('sheet_rows_51_56',[r51[0]['timeline_in']+1,r51[0]['timeline_in']+3,r51[0]['timeline_in']+5.5,r51[0]['timeline_out']-1,
 r56[0]['timeline_in']+2,r56[1]['timeline_in']+1,r56[1]['timeline_in']+3,r56[1]['timeline_out']-0.5,TOTAL-0.5])
tsheet('sheet_cards_sub',[o['start']+1.0 for o in json.loads((PACK/'overlays_v05d.json').read_text())])
tsheet('sheet_end',[LAST_WORD-1,LAST_WORD+0.5,LAST_WORD+1.5,LAST_WORD+2.5,TOTAL-0.5,TOTAL-0.05])
h=hashlib.sha256()
with OUT.open('rb') as f:
 for b in iter(lambda:f.read(1<<20),b''):h.update(b)
(PACK/'SHA256.txt').write_text(f'{h.hexdigest()}  {OUT.name}\n')
summary=dict(freeze_over_1_5s_before_end_hold=long_holds,out=str(OUT),sha256=h.hexdigest(),runtime=runtime,lufs=lufs,clip_check_exit=cc.returncode,align=align,reuse=dict(reuse))
(PACK/'summary_v05d.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=1));print(cc.stdout+cc.stderr)
