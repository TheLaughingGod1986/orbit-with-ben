#!/usr/bin/env python3
"""024 Light Speed full rough v04 (J0089): v03's picture and the locked VO unchanged, with 024's own score bed
(05_Music/light-speed_score_bed_v01_full.mp3, J0079, music_gate PASS) in place of the shared jupiter-music.mp3, at 026's
level (volume 0.134, no ducking), fading with the picture. The picture is v03's rendered picture.mp4 (cards and subscribe
cue burned in), read from /private/tmp/light024_full_work_v03; nothing is re-cut. The master stays in /private/tmp and
OWB UAT gets the phone copy (1080p H.264 High, CRF 23, AAC 160k, +faststart).
v03 notes:
024 Light Speed full rough v03 (J0046): v02 with Claude's v02 review (thread 6058384739):
- Row 1 is one continuous starfield span from 12 s for the whole row (0-6.50 s); the second shot (14 s render from 0 s,
  which fell back to grey) is gone. Row 1 holds 6.50 s against the 6 s cap, on Claude's call. Nothing else changes.
v02 notes:
024 Light Speed full rough v02 (J0045): v01 plus Claude's v01 review (thread 6058016232):
- Frame 0 starts in the blue, rushing part of the 23 s starfield (12 s in), not the dim slow start.
- NHQ ISS video cropped below its "Earth from the Space Station" corner bug (logo ends ~y 97 of 720).
- Row 23 is iss019e018483 (crew at work), cropped above its burned-in ID caption, not the STS-33 portrait.
- Row 27's 1.82 s night-city cut is gone; row 28's DC-8 starts at the 317.05 s pause (holds 6.86 s, Claude's timing).
- Row 38 ends on the ISS dawn limb to 464.98 s (7.56 s, Claude's timing); row 39 is one continuous 27 s starfield
  with a slow push-in through the hold and fade (6 s cap waived for this bookend, as with the Venus Maat Mons bookends).
Unchanged segments are copied from the v01 work folder when their render key matches.
v01 notes:
024 Light Speed full rough v01 (J0044), built on 023 _assemble_venus_full_v04.py with the Venus review rules:
- <=2 uses per still, the second at a new framing; reuse count per source printed and written to the pack.
- Upscale (source px -> 1080p, push included) recorded per row and asserted <= 2.35.
- Every cut snapped to a VO pause (words.json); no shot held longer than 6 s; frame 0 is the moving starfield.
- Omni takes trimmed to Claude's PASS spans (6057589014): row 15 lightclock 4.5-9.5 s, row 27 returns 5-10 s; audio stripped.
- Harvest gaps (_evidence/light_speed_harvest_v01_gaps.md): no ISS night-city video, so night beats use the ISS night stills;
  the NHQ ISS video is cropped past its corner bug.
Locked VO untouched, house bed full runtime, hold 2.5 s past the last word, then 1 s fade, -14 LUFS.
`--plan` prints the segment list, reuse counts and checks without rendering."""
from pathlib import Path
import json, subprocess as sp, re, hashlib, math, sys, csv, io
from collections import Counter
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
HERE=Path(__file__).resolve().parent; EP=HERE.parent
UAT=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/OWB UAT'
WORK=Path('/private/tmp/light024_full_work_v04'); PACK=HERE/'full_rough_v04_pack'
WORK_V03=Path('/private/tmp/light024_full_work_v03'); PACK_V03=HERE/'full_rough_v03_pack'
VO=EP/'02_Voiceover/light_speed_vo_v01.mp3'
BED=EP/'05_Music/light-speed_score_bed_v01_full.mp3'
OUT=Path('/private/tmp/024_LightSpeed_full_rough_v04.mp4')  # iCloud locks the UAT copy mid-read; the phone copy goes to UAT
PHONE=UAT/'024_LightSpeed_v04_PHONE.mp4'
MAX_UP=2.35; MAX_HOLD=6.0
G1=HERE/'graphics_v01'; G2=HERE/'graphics_v02'; H=HERE/'nasa_pool_v01/024_harvest_v01'
OM=EP/'04_Generated-Clips/01_Raw/omni_v01'
FPS=30; LAST_WORD=487.544; HOLD=2.5; FADE=1.0; TOTAL=round((LAST_WORD+HOLD+FADE)*FPS)/FPS
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
CLIP_CHECK=EP.parents[1]/'00_Brand/Channel-Setup/tools/clip_check.py'
PLAN='--plan' in sys.argv
words=json.loads((EP/'02_Voiceover/words.json').read_text())['words']

def run(args):
 p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-6000:])
def probe(p):return float(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
def fr(t):return round(t*FPS)/FPS

Q={'tl':(0.0,0.0),'tr':(0.5,0.0),'bl':(0.0,0.5),'br':(0.5,0.5),'c':(0.25,0.25)}
SF2,SF1=G2/'starfield.mp4',G1/'starfield.mp4'; LC2,LC1=G2/'lightclock.mp4',G1/'lightclock.mp4'
EN2,EN1=G2/'energy.mp4',G1/'energy.mp4'; TW=G1/'twinclocks.mp4'; MU=G1/'muons.mp4'; GC=G1/'gpsclocks.mp4'
MD=G2/'mapdrift.mp4'; GM=G2/'gammaclocks.mp4'; CT=G2/'contraction.mp4'; SF3=HERE/'graphics_v03/starfield.mp4'
EV=H/'Earth_Views_from_the_International_Space_Station.mp4'; ART=H/'KSC-20221116-MH-AJN01-0001-Artemis_I_Isolated_Launch_Views-3314595.mp4'
NHQ=H/'NHQ_2019_0626_Earth_Views_from_the_ISS.mp4'; NHQC=(88,104,1096,616)
WORK_V01=Path('/private/tmp/light024_full_work_v01'); WORK_V02=Path('/private/tmp/light024_full_work_v02')
GPS='GPS_Block_IIIA.jpg'; GAIA='Gaia’s_sky_in_colour_ESA393127.jpg'
def v(at,**k):return dict(video=1,at=at,**k)
# (row, nominal in, source, opts). Stills are names in the harvest pool; video opts: at = source time at the in-point.
def f(at,**k):return dict(video=1,at=at,fixed=1,**k)
X=dict(fixed=1)
S=[('1',0.0,SF2,v(12.0,hold_ok=1)),('2',6.5,EV,v(14.0)),('2',9.65,EV,f(122.0)),('3',13.03,LC2,f(0.0)),('4',18.9,SF2,v(6.0)),('5',23.2,GPS,{}),
 ('6',28.3,LC2,v(6.0)),('6',32.5,SF2,v(10.0)),('6',36.8,EN2,v(0.0)),
 ('7',41.5,GPS,dict(quad='c')),('7',45.8,GC,v(0.0)),
 ('8',49.78,'PIA24573.jpg',X),('8',53.31,GC,f(4.0)),('8',59.1,'PIA24573.jpg',dict(quad='c',fixed=1)),('8',62.13,GC,f(7.0)),
 ('9',67.09,MD,f(0.0)),('9',71.68,MD,f(5.0)),('9',75.6,MD,v(9.0)),
 ('10',79.77,'iss035e017673.jpg',X),
 ('11',84.72,'EC00-0050-001.jpg',X),('11',88.04,'EC98-44444-004.jpg',X),('11',93.98,'ED07-0256-09.jpg',X),('11',98.74,'EC00-0050-001.jpg',dict(quad='c',fixed=1)),
 ('12',103.85,LC2,f(12.0)),('12',107.16,LC2,f(17.0)),
 ('13',110.29,LC2,f(0.0,vcrop=(0,270,960,540))),('13',113.97,LC1,f(3.0,vcrop=(0,270,960,540))),
 ('14',118.68,LC2,f(0.0)),('14',121.61,LC2,f(3.0)),('14',126.82,LC2,f(8.0)),('14',131.14,LC2,f(12.5)),('14',135.23,LC2,f(16.6)),('14',138.3,LC1,f(9.0)),
 ('15',141.37,OM/'orbit_lightclock_omni_v01.mp4',f(4.5)),('15',145.13,LC1,f(0.0)),('15',150.22,LC1,f(5.0)),('15',153.9,LC1,f(9.0,vcrop=(0,270,960,540))),
 ('16',156.67,GM,f(0.0)),('16',161.6,GM,f(5.0)),('16',167.15,GM,f(10.0)),('16',170.97,GM,f(14.0)),
 ('17',176.02,MU,f(0.0)),('17',179.34,MU,f(3.3)),('17',184.64,'iss071e439624.jpg',X),('17',188.7,MU,f(7.0)),
 ('17',192.86,EV,f(50.0)),('17',195.09,MU,f(8.0)),
 ('18',199.05,'iss071e439624.jpg',dict(quad='c',fixed=1)),('18',204.43,MU,f(2.0)),('18',209.3,EV,f(26.0)),
 ('19',213.06,SF1,f(0.0)),('19',215.99,SF1,f(6.0)),('20',219.57,SF2,f(14.0)),
 ('21',224.01,ART,f(260.0)),('21',228.24,ART,f(380.0)),('21',233.07,SF1,f(8.0)),
 ('22',235.8,TW,f(0.0)),('22',240.75,'iss040e085126.jpg',X),('22',245.95,NHQ,f(1740.0,vcrop=NHQC)),('22',248.75,TW,f(5.0)),
 ('23',253.66,'iss019e018483.jpg',dict(box=(0,0,1,0.92),fixed=1)),
 ('24',259.44,SF2,f(16.0)),('24',263.3,SF1,f(8.0)),
 ('25',269.1,CT,f(0.0)),('25',274.06,CT,f(5.0)),('25',280.03,CT,f(11.0)),('25',283.93,G1/'contraction.mp4',f(7.0)),
 ('26',286.9,TW,f(8.0)),('26',291.73,SF2,f(17.5)),('26',297.27,TW,f(12.0)),('26',301.72,SF1,f(4.0)),('26',306.87,EV,f(110.0)),
 ('27',312.71,OM/'orbit_returns_omni_v01.mp4',f(5.0)),
 ('28',317.05,'ED07-0256-09.jpg',dict(quad='c',fixed=1,hold_ok=1)),
 ('29',323.91,'SSC-20240229-s00309.tif',X),
 ('30',329.49,EN2,f(0.0)),('30',333.09,'SSC-2015-00064.jpg',X),('30',337.22,'GSFC_20171208_Archive_e001593.jpg',X),('30',342.04,EN2,f(4.0)),('30',346.28,EN1,f(0.0)),
 ('31',351.35,EN2,f(9.0)),('31',356.29,'SSC-20240229-s00309.tif',dict(quad='c',fixed=1)),('31',359.17,EN1,f(6.0)),('31',363.27,EN2,f(12.0)),
 ('32',368.51,'sts080-326-010.jpg',X),('32',373.6,'sts080-326-010.jpg',dict(quad='c',fixed=1)),
 ('33',378.91,'NHQ201808120013.tif',X),('33',384.77,'NHQ201808120013.tif',dict(quad='c',fixed=1)),
 ('34',389.28,'ACS3_SolarSailSunrise.png',X),('34',393.25,'ACS3_LookingDown.png',X),
 ('35',398.77,SF2,f(2.0)),('35',402.06,SF1,f(2.0)),('35',406.67,GAIA,X),('35',412.49,GAIA,dict(quad='c',fixed=1)),('35',416.09,SF2,f(12.0)),
 ('36',420.54,NHQ,f(570.0,vcrop=NHQC)),('36',425.2,'iss040e085126.jpg',dict(quad='c',fixed=1)),('36',428.95,NHQ,f(1830.0,vcrop=NHQC)),('36',432.0,'iss040e091231.jpg',X),('36',435.0,NHQ,f(2100.0,vcrop=NHQC)),
 ('37',438.57,TW,f(2.0)),('37',442.42,TW,f(9.0)),('37',446.0,GM,f(15.0)),
 ('38',448.61,GC,f(2.0)),('38',453.98,MU,f(3.0)),('38',457.42,EV,f(176.0,hold_ok=1)),
 ('39',464.98,SF3,f(0.0,push=0.06,hold_ok=1,bookend=1))]
CHAPTERS=[('Your Clock Is Already Slow',42.0),('Why Light Sets the Limit',110.7),('The Trip',224.4),
 ('The Price of Every Nine',324.5),('A One-Way Ticket to the Future',399.2)]

GAPS=[((a['end']+b['start'])/2,b['start']-a['end']) for a,b in zip(words,words[1:])]
def snap(t):
 """Midpoint of the nearest VO pause (>=0.30 s, else >=0.20 s, else >=0.10 s) within 2 s; past the last word, keep t."""
 if t>LAST_WORD:return t
 for need in (0.30,0.20,0.10):
  c=[m for m,g in GAPS if g>=need and abs(m-t)<=2.0]
  if c:return min(c,key=lambda m:abs(m-t))
 raise SystemExit(f'no VO pause near {t}')

segs=[]
for i,(row,t,src,o) in enumerate(S):
 tin=t if (i==0 or o.get('fixed')) else snap(t)
 segs.append(dict(row=row,timeline_in=fr(tin),src=src if isinstance(src,Path) else H/src,o=dict(o)))
for a,b in zip(segs,segs[1:]):a['timeline_out']=b['timeline_in']
segs[-1]['timeline_out']=TOTAL
for s in segs:
 if s['o'].get('video'):s['o']['offset']=s['o'].get('at',0.0)

def framed(s):
 im=Image.open(s['src']).convert('RGB');o=s['o']
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
 im=framed(s);return im.width,max(1920/im.width,1080/im.height)*(1+o.get('pct',.05))

# ---- checks: reuse <= 2 per still with a different framing, holds <= 6 s, cuts in VO pauses, upscale <= 2.35,
# video spans inside the source (a 2 s clone pad is the most allowed)
stills=[s for s in segs if not s['o'].get('video')]
reuse=Counter(s['src'].name for s in stills)
vreuse=Counter(s['src'].name for s in segs if s['o'].get('video'))
problems=[]
for name,n in reuse.items():
 uses=[s for s in stills if s['src'].name==name]
 if n>2:problems.append(f'{name} used {n}x')
 if n==2 and uses[0]['o'].get('quad')==uses[1]['o'].get('quad'):problems.append(f'{name} second use has the same framing')
dur_cache={}
for s in segs:
 d=s['timeline_out']-s['timeline_in']
 if d<1.8:problems.append(f"{s['row']} {s['timeline_in']} only {d:.2f}s")
 if d>MAX_HOLD+0.05 and not s['o'].get('hold_ok'):problems.append(f"{s['row']} {s['timeline_in']} {s['src'].name} held {d:.2f}s")
 if s['o'].get('video') and s['src'].exists():
  L=dur_cache.setdefault(s['src'],probe(s['src']))
  if s['o']['offset']+d>L+0.5:problems.append(f"{s['row']} {s['src'].name} runs {s['o']['offset']+d-L:.2f}s past its end")
for s in segs[1:]:
 c=s['timeline_in']
 near=[w for w in words if w['start']+0.02<c<w['end']-0.02]
 if near:problems.append(f"cut {c:.2f} ({s['row']}) inside '{near[0]['text']}' {near[0]['start']:.2f}-{near[0]['end']:.2f}")
for s in segs:
 if not s['src'].exists():problems.append(f'missing {s["src"]}');continue
 s['src_w'],s['upscale']=upscale(s);s['upscale']=round(s['upscale'],3)
 if s['upscale']>MAX_UP:problems.append(f"{s['row']} {s['src'].name} upscale {s['upscale']:.2f} > {MAX_UP}")
assert all(s.get('upscale',0)<=MAX_UP for s in segs) or problems
print('reuse (stills):',dict(sorted(reuse.items(),key=lambda x:-x[1])))
print('reuse (video/graphics):',dict(sorted(vreuse.items(),key=lambda x:-x[1])))
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

WORK.mkdir(parents=True,exist_ok=True);PACK.mkdir(parents=True,exist_ok=True)
PIC=WORK_V03/'picture.mp4'
if not PIC.exists():raise SystemExit(f'missing {PIC}: v03 picture scratch is gone, rebuild it with the v03 script first')
if abs(probe(PIC)-TOTAL)>0.1:raise SystemExit(f'{PIC} runs {probe(PIC):.3f}s, expected {TOTAL}')
import shutil;shutil.copyfile(PACK_V03/'overlays_v03.json',PACK/'overlays_v04.json')
if '--finish-only' not in sys.argv:
 # 024's own bed under the whole cut at 026's level, fading with the picture.
 if probe(BED)<TOTAL:raise SystemExit(f'bed {probe(BED):.1f}s is shorter than the cut {TOTAL}s')
 run(['-i',BED,'-af',f'atrim=0:{TOTAL},asetpts=PTS-STARTPTS,volume=0.134,afade=t=out:st={TOTAL-FADE-1.5:.3f}:d={FADE+1.5}','-c:a','pcm_s24le',WORK/'music.wav'])
 mix=f'[0:a]apad=whole_dur={TOTAL},atrim=0:{TOTAL},asetpts=PTS-STARTPTS[v];[v][1:a]amix=inputs=2:duration=first:normalize=0'
 first=sp.run(['ffmpeg','-hide_banner','-i',str(VO),'-i',str(WORK/'music.wav'),'-filter_complex',mix+',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]','-map','[a]','-f','null','-'],capture_output=True,text=True).stderr
 st=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',first,re.S)[-1]);(PACK/'loudnorm_first_pass.json').write_text(json.dumps(st,indent=2))
 norm=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
 run(['-i',VO,'-i',WORK/'music.wav','-filter_complex',mix+','+norm+'[a]','-map','[a]','-ar','48000','-c:a','aac','-b:a','192k',WORK/'audio.m4a'])
 run(['-i',PIC,'-i',WORK/'audio.m4a','-map','0:v','-map','1:a','-c','copy','-t',TOTAL,'-movflags','+faststart',OUT])
 PHONE.parent.mkdir(parents=True,exist_ok=True)
 run(['-i',OUT,'-c:v','libx264','-profile:v','high','-preset','medium','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',WORK/PHONE.name])
 shutil.copyfile(WORK/PHONE.name,PHONE)

# ---- checks and review pack
runtime=probe(OUT)
ll=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
lufs=float(re.findall(r'I:\s*([-\d.]+) LUFS',ll)[-1])
checks=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-vf','blackdetect=d=0.1:pix_th=0.10:pic_th=0.98,freezedetect=n=-50dB:d=1','-an','-f','null','-'],capture_output=True,text=True).stderr
(PACK/'ffmpeg_checks.txt').write_text('\n'.join(l for l in checks.splitlines() if 'black_' in l or 'freeze' in l))
cuts=[dict(row=s['row'],timeline_in=s['timeline_in'],timeline_out=s['timeline_out'],source=s['src'].name,
 framing={k:v for k,v in s['o'].items() if k in('quad','offset','vcrop')},src_w=s['src_w'],upscale=s['upscale']) for s in segs]
(PACK/'cuts_v04.json').write_text(json.dumps(cuts,indent=2))
reuse_rows={n:[s['row'] for s in stills if s['src'].name==n] for n in sorted(reuse,key=lambda n:(-reuse[n],n))}
(PACK/'reuse_v04.json').write_text(json.dumps(dict(stills=dict(sorted(reuse.items(),key=lambda x:(-x[1],x[0]))),rows=reuse_rows,
 video=dict(sorted(vreuse.items(),key=lambda x:(-x[1],x[0])))),indent=2))
buf=io.StringIO();wr=csv.writer(buf);wr.writerow(['row','source','vo_in','vo_out','vo_text'])
for c in cuts:
 text=' '.join(w['text'] for w in words if c['timeline_in']<=(w['start']+w['end'])/2<c['timeline_out'])
 wr.writerow([c['row'],c['source'],f"{c['timeline_in']:.3f}",f"{c['timeline_out']:.3f}",text or '[no VO]'])
(PACK/'light_speed_full_v04_assembled.csv').write_text(buf.getvalue());(PACK/'light_speed_words_list.json').write_text(json.dumps(words))
cc=sp.run([sys.executable,str(CLIP_CHECK),str(PACK/'light_speed_full_v04_assembled.csv'),'--words',str(PACK/'light_speed_words_list.json')],capture_output=True,text=True)
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
sheet('per_row_sheet_v04',tiles)
def tsheet(name,times):
 items=[]
 for i,t in enumerate(times):p=WORK/f'f_{name}_{i}.jpg';grab(t,p);items.append((p,f'{t:.2f}s'))
 sheet(name,items,cols=3)
tsheet('frame0_sheet',[0,.2,.4,.6,.8,1])
tsheet('sheet_0_8s',[0,1,2,3,4,5,6,6.4,6.6,7,7.5,8])
om=[c for c in cuts if c['source'].startswith('orbit_')]
tsheet('sheet_omni',[t for c in om for t in (c['timeline_in']+0.5,(c['timeline_in']+c['timeline_out'])/2,c['timeline_out']-0.5)])
tsheet('sheet_cards_sub',[o['start']+1.0 for o in json.loads((PACK/'overlays_v04.json').read_text())])
tsheet('sheet_end',[LAST_WORD-1,LAST_WORD+0.5,LAST_WORD+1.5,LAST_WORD+2.5,TOTAL-0.5,TOTAL-0.05])
h=hashlib.sha256()
with OUT.open('rb') as f:
 for b in iter(lambda:f.read(1<<20),b''):h.update(b)
(PACK/'SHA256.txt').write_text(f'{h.hexdigest()}  {OUT.name}\n')
summary=dict(out=str(OUT),phone=str(PHONE),phone_mb=round(PHONE.stat().st_size/1e6,1),bed=BED.name,bed_volume=0.134,picture=str(PIC),sha256=h.hexdigest(),runtime=runtime,lufs=lufs,clip_check_exit=cc.returncode,align=align,reuse_stills=dict(reuse))
(PACK/'summary_v04.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=1));print(cc.stdout+cc.stderr)
