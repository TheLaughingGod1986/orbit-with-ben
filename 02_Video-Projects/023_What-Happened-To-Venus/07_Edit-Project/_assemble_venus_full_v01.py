#!/usr/bin/env python3
"""Venus 023 full first cut v01 (J0003). Ch0-1 = Part01 rough v03 picture (Claude PASS 6048885704), held through the
0.7 s breath; Ch2-5 built row by row from SHOT_LIST_v02.md with harvest v02/v03 plates and Claude's 6049181839 calls
(row 52 DAVINCI 12.0-22.2 s; row 28 S91-50688 notch framed out, slow push on black). Internal cuts snap into the
nearest VO pause. Locked VO untouched; house bed full runtime; hold 2.5 s past the last word, then 1 s fade; -14 LUFS.
Pack: per-row frames (row_###.jpg) + per-row sheet, cut sheets, clip_check, align, ffmpeg checks."""
from pathlib import Path
import json, subprocess as sp, re, hashlib, math, sys, csv, io
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
HERE=Path(__file__).resolve().parent; EP=HERE.parent
UAT=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/OWB UAT'
WORK=Path('/private/tmp/venus023_full_work_v01'); PACK=HERE/'full_rough_v01_pack'
PART01=UAT/'023_Venus_Part01_rough_v03.mp4'; VO=EP/'02_Voiceover/venus_vo_v01.mp3'; BED=UAT/'jupiter-music.mp3'
OUT=UAT/'023_Venus_full_rough_v01.mp4'
POOL=HERE/'nasa_pool_v01'; RAW=EP/'04_Generated-Clips/01_Raw'; G2=RAW/'graphics_v02'
FPS=30; LAST_WORD=509.50; HOLD=2.5; FADE=1.0; TOTAL=round((LAST_WORD+HOLD+FADE)*FPS)/FPS
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
CLIP_CHECK=EP.parents[1]/'00_Brand/Channel-Setup/tools/clip_check.py'
words=json.loads((EP/'02_Voiceover/words.json').read_text())['words']

def run(args):
 p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-6000:])
def probe(p):return float(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
def fr(t):return round(t*FPS)/FPS

# Graphics longer than the 12 s defaults: deuterium spans rows 31+32a, line spans 43a+43b then 44b.
GPY=Path.home()/'.venvs/orbit-code-graphics/bin/python'  # matplotlib lives here
DEUT_S=254.00-236.66; LINE_A=365.00-350.92; LINE_S=LINE_A+(389.88-381.70)
for name,secs in (('deuterium',DEUT_S),('line',LINE_S)):
 if not (G2/f'{name}.mp4').exists():
  sp.run([str(GPY),str(HERE/'code_graphics.py'),name,str(G2),'--seconds',f'{secs+0.5:.2f}'],check=True)

# (row, nominal in, source, opts). Each segment ends where the next begins; breaths ride on the row before.
S=[('1-18',0.0,PART01,dict(video=True,tpad=True)),
 ('20b',142.57,'open/PIA00104.jpg',{}),('21a',149.02,'open/PIA00240.jpg',{}),('21b',154.50,'magellan_extra/PIA00084.jpg',{}),
 ('21c',160.00,'open/PIA00087.jpg',{}),('22',165.00,'magellan_extra/PIA00103.jpg',{}),('22',171.28,'magellan_extra/PIA00200.jpg',{}),
 ('23',177.56,'earth/PIA18033.jpg',{}),('24',184.64,'harvest_v02/s129e007324.jpg',dict(crop_bottom=0.045)),
 ('24',189.82,'harvest_v02/PIA03877.jpg',{}),('25',195.00,'earth/GSFC_20171208_Archive_e001435.jpg',{}),
 ('26',202.34,'open/PIA00241.jpg',{}),('26',207.54,'magellan_extra/PIA00246.jpg',{}),('27',212.74,'open/PIA00106.jpg',{}),
 ('28',218.76,'harvest_v03/S91-50688.jpg',dict(on_black=True,pct=.04)),
 ('30b',224.15,'harvest_v02/ARC-1978-AC78-9245.jpg',dict(strip_bars=True)),('30b',230.58,'harvest_v02/ARC-1978-AC78-0238.jpg',dict(strip_bars=True)),
 ('31',236.66,G2/'deuterium.mp4',dict(video=True,offset=0.0)),('32a',247.48,G2/'deuterium.mp4',dict(video=True,offset=247.48-236.66)),
 ('32b',254.00,'magellan_extra/PIA00159.jpg',{}),('32c',261.00,'open/PIA00104.jpg',{}),('33',268.82,'open/PIA00254.jpg',{}),
 ('34a',275.70,'open/PIA00106.jpg',dict(pct=.04)),('34b',283.70,'magellan_extra/PIA00246.jpg',dict(pct=.04)),
 ('35',291.78,RAW/'plates_v01/venus_ch3_plateA_ocean_nasa_v01.mp4',dict(video=True,offset=0.0)),
 ('36',305.00,RAW/'plates_v01/venus_ch3_plateA_ocean_nasa_v01.mp4',dict(video=True,offset=13.22)),
 ('37',312.96,RAW/'plates_v02/venus_ch3_row37_plateB_steam_lid_sharp_v02.mp4',dict(video=True,tpad=True)),
 ('38',320.54,RAW/'graphics_v01/nightlid.mp4',dict(video=True,offset=0.0)),
 ('39a',331.34,RAW/'plates_v02/venus_ch3_row39a_split_ocean_vs_steamlid_v02.mp4',dict(video=True,tpad=True)),
 ('39b',335.06,RAW/'plates_v02/venus_ch3_row39b_magellan_alpha_regio_tessera_PIA00215_v02.mp4',dict(video=True,tpad=True)),
 ('40',338.98,'open/PIA00106.jpg',{}),('40',343.26,'open/PIA00087.jpg',{}),
 ('42b',347.89,'earth/as17-148-22727.jpg',{}),
 ('43a',350.92,G2/'line.mp4',dict(video=True,offset=0.0)),('43b',357.00,G2/'line.mp4',dict(video=True,offset=357.00-350.92)),
 ('43c',365.00,'open/PIA00240.jpg',{}),('43c',369.29,'earth/PIA18033.jpg',{}),
 ('44a',373.58,POOL/'sdo/HMIVenusTransit_HD1080.mp4',dict(video=True,offset=5.0)),
 ('44b',381.70,G2/'line.mp4',dict(video=True,offset=LINE_A)),
 ('45a',389.88,'earth/as17-148-22727.jpg',{}),('45b',396.50,'earth/GSFC_20171208_Archive_e001435.jpg',{}),
 ('45c',403.00,'open/PIA00104.jpg',{}),
 ('46',409.60,RAW/'omni_v01/orbit_looks_back_earth_omni_v01_t0-5s.mp4',dict(video=True,offset=0.0)),
 ('46',414.60,'magellan_extra/PIA00084.jpg',{}),
 ('48b',417.23,'open/PIA00241.jpg',{}),('49',420.88,'magellan_extra/PIA00215.jpg',{}),('49',425.75,'magellan_extra/PIA00200.jpg',{}),
 ('49',430.62,'magellan_extra/PIA00246.jpg',{}),('50',435.48,'open/PIA00240.jpg',{}),('50',440.24,'open/PIA00087.jpg',{}),
 ('51',445.00,'parker/PIA24470.jpg',{}),('51',449.91,'parker/PIA24937.jpg',{}),
 ('52',454.82,POOL/'harvest_v03/13887_DAVINCI_PEVAA.mp4',dict(video=True,offset=12.0)),
 ('53',465.00,'harvest_v03/veritas-cut7-16.jpg',{}),('53',471.00,'magellan_extra/PIA00103.jpg',{}),
 ('54',475.72,'open/PIA00254.jpg',dict(pct=.06)),('54',482.06,'open/PIA00106.jpg',{}),('55',488.40,'open/PIA00104.jpg',{}),
 ('56',495.12,'harvest_v02/NHQ202605180003.jpg',dict(band=(0.04,0.0))),('56',500.47,'harvest_v02/NHQ202605180003.jpg',dict(band=(0.08,0.12))),
 ('57',505.82,'open/PIA00254.jpg',dict(pct=.06))]
FIXED={142.57,224.15,347.89,417.23,409.60,414.60}  # breath midpoints, card rows, Omni 0-5 s cut

def snap(t):
 """Nearest VO pause (>=0.12 s) within 0.9 s; cut at its midpoint so no word is clipped."""
 best=None
 for a,b in zip(words,words[1:]):
  g0,g1=a['end'],b['start']
  if g1-g0<0.12:continue
  m=(g0+g1)/2
  if abs(m-t)<=0.9 and (best is None or abs(m-t)<abs(best-t)):best=m
 return best if best is not None else t

segs=[]
for i,(row,t,src,o) in enumerate(S):
 tin=t if (i==0 or t in FIXED) else snap(t)
 segs.append(dict(row=row,timeline_in=fr(tin),src=Path(src) if isinstance(src,Path) else POOL/src,o=o))
for a,b in zip(segs,segs[1:]):a['timeline_out']=b['timeline_in']
segs[-1]['timeline_out']=TOTAL
for s in segs:
 d=s['timeline_out']-s['timeline_in']
 assert d>=2.0,(s['row'],d)
# video sources keep their timeline offset when a snap moves the in-point
for s,(row,t,_,o) in zip(segs,S):
 if o.get('video') and 'offset' in o:o['offset']=o['offset']+(s['timeline_in']-fr(t if t in FIXED else t))

def strip_bars(im):
 a=np.array(im.convert('L')).astype(float);sd=a.std(axis=0);ok=np.flatnonzero(sd>8)
 return im.crop((int(ok[0]),0,int(ok[-1])+1,im.height))
def prep_still(s,dest):
 im=Image.open(s['src']).convert('RGB');o=s['o']
 if o.get('crop_bottom'):im=im.crop((0,0,im.width,int(im.height*(1-o['crop_bottom']))))
 if o.get('strip_bars'):im=strip_bars(im)
 if 'band' in o:
  top,inset=o['band'];w=int(im.width*(1-inset));h=int(w*9/16);x=(im.width-w)//2;y=int(im.height*top)
  im=im.crop((x,y,x+w,y+h))
 if s['src'].name=='PIA23791.jpg':im=im.crop((1145,0,2245,1096))
 im=ImageEnhance.Color(im).enhance(1.10);im=ImageEnhance.Contrast(im).enhance(1.04)
 if o.get('on_black'):
  # globe larger than the frame height so the bottom data-gap notch sits below frame; space stays black
  d=round(1188*1.12);g=im.resize((d,d),Image.Resampling.LANCZOS);c=Image.new('RGB',(2112,1188),(0,0,0))
  c.paste(g,((2112-d)//2,-round(d*0.03)));c.save(dest);return
 im=im.point([min(255,int(v*.92+28)) for v in range(256)]*3)
 scale=max(2112/im.width,1188/im.height)
 im=im.resize((round(im.width*scale*1.0),round(im.height*scale*1.0)),Image.Resampling.LANCZOS)
 x=(im.width-2112)//2;y=(im.height-1188)//2;im.crop((x,y,x+2112,y+1188)).save(dest)

WORK.mkdir(parents=True,exist_ok=True);PACK.mkdir(parents=True,exist_ok=True)
ENC=['-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4']
if '--finish-only' not in sys.argv:
 for i,s in enumerate(segs):
  pre=.2 if i else 0;post=.2 if i<len(segs)-1 else 0
  frames=round((s['timeline_out']-s['timeline_in']+pre+post)*FPS);dest=WORK/f'seg_{i:02}.mp4';s['render']=str(dest)
  if dest.exists() and (WORK/f'seg_{i:02}.ok').exists() and (WORK/f'seg_{i:02}.ok').read_text()==json.dumps([s['timeline_in'],s['timeline_out'],str(s['src']),s['o']],default=str):
   print('reuse',i,s['row'],flush=True);continue
  print('seg',i,s['row'],s['timeline_in'],s['timeline_out'],s['src'].name,flush=True)
  o=s['o']
  if o.get('video'):
   off=o.get('offset',0.0)
   vf='scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,setsar=1,tpad=stop_mode=clone:stop_duration=2'
   run(['-ss',max(0,off-pre),'-i',s['src'],'-vf',vf+',format=yuv420p','-frames:v',frames,*ENC,dest])
  else:
   plate=WORK/f'plate_{i:02}.png';prep_still(s,plate);pct=o.get('pct',.05)
   vf=f"scale=3840:2160,zoompan=z='1+{pct}*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={frames}:s=1920x1080:fps=30,setsar=1,format=yuv420p"
   run(['-i',plate,'-vf',vf,'-frames:v',frames,*ENC,dest])
  got=round(probe(dest)*FPS)
  if got<frames-1:raise RuntimeError(f'seg {i} {s["row"]}: {got} frames < {frames}')
  (WORK/f'seg_{i:02}.ok').write_text(json.dumps([s['timeline_in'],s['timeline_out'],str(s['src']),s['o']],default=str))
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

 # Lower-thirds (Ch2-5, ~2.5 s from the chapter's first word; Ch1 is baked into Part01) and the subscribe cue.
 def first_word(t):return next(w['start'] for w in words if w['start']>=t-0.01)
 cards=[('A Blanket With No Way Out',142.92),('Where Did the Water Go?',224.50),("The Line Earth Hasn't Crossed",348.24),('Going Back',417.58)]
 font=ImageFont.truetype(FONT,62);ov=[]
 for k,(title,t) in enumerate(cards):
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
 (PACK/'overlays_v01.json').write_text(json.dumps([dict(file=Path(p).name,start=round(a,3),end=round(b,3)) for p,a,b in ov],indent=2))

 # House bed, acrossfade-looped to full runtime (as Part01 v01), fading with the picture.
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
 run(['-i',WORK/'picture.mp4','-i',WORK/'audio.m4a','-map','0:v','-map','1:a','-c','copy','-t',TOTAL,'-movflags','+faststart',OUT])

# ---- checks and review pack
runtime=probe(OUT)
ll=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
lufs=float(re.findall(r'I:\s*([-\d.]+) LUFS',ll)[-1])
checks=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-vf','blackdetect=d=0.1:pix_th=0.10:pic_th=0.98,freezedetect=n=-50dB:d=1','-an','-f','null','-'],capture_output=True,text=True).stderr
(PACK/'ffmpeg_checks.txt').write_text('\n'.join(l for l in checks.splitlines() if 'black_' in l or 'freeze' in l))
p01=json.loads((HERE/'part01_rough_v03_pack/cuts_v03.json').read_text())
cuts=[dict(row=c['row'],timeline_in=c['timeline_in'],timeline_out=c['timeline_out'],source=c['source']) for c in p01]
cuts[-1]['timeline_out']=segs[1]['timeline_in']
cuts+=[dict(row=s['row'],timeline_in=s['timeline_in'],timeline_out=s['timeline_out'],source=s['src'].name) for s in segs[1:]]
(PACK/'cuts_v01.json').write_text(json.dumps(cuts,indent=2))
buf=io.StringIO();wr=csv.writer(buf);wr.writerow(['row','source','vo_in','vo_out','vo_text'])
for c in cuts:
 text=' '.join(w['text'] for w in words if c['timeline_in']<=(w['start']+w['end'])/2<c['timeline_out'])
 wr.writerow([c['row'],c['source'],f"{c['timeline_in']:.3f}",f"{c['timeline_out']:.3f}",text or '[no VO]'])
(PACK/'venus_full_v01_assembled.csv').write_text(buf.getvalue());(PACK/'venus_words_list.json').write_text(json.dumps(words))
cc=sp.run([sys.executable,str(CLIP_CHECK),str(PACK/'venus_full_v01_assembled.csv'),'--words',str(PACK/'venus_words_list.json')],capture_output=True,text=True)
(PACK/'clip_check_py.txt').write_text(cc.stdout+cc.stderr)
# align: every cut sits in a VO pause (not inside a word)
inside=[c['timeline_in'] for c in cuts[1:] if any(w['start']+0.02<c['timeline_in']<w['end']-0.02 for w in words)]
align=dict(runtime=runtime,expected=TOTAL,vo_last_word_end=LAST_WORD,hold_after_last_word=HOLD,fade=FADE,cuts=len(cuts),
 cuts_inside_a_word=inside,longest_shot=max(c['timeline_out']-c['timeline_in'] for c in cuts))
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
sheet('per_row_sheet_v01',tiles)
def tsheet(name,times):
 items=[]
 for i,t in enumerate(times):p=WORK/f'f_{name}_{i}.jpg';grab(t,p);items.append((p,f'{t:.2f}s'))
 sheet(name,items,cols=3)
tsheet('frame0_sheet',[0,.2,.4,.6,.8,1])
tsheet('sheet_rows_28_52_53',[219.5,221.5,223.5,456.0,460.0,464.0,466.0,469.0,473.0])
tsheet('sheet_cards_sub',[o['start']+1.0 for o in json.loads((PACK/'overlays_v01.json').read_text())])
tsheet('sheet_end',[LAST_WORD-1,LAST_WORD+0.5,LAST_WORD+1.5,LAST_WORD+2.5,TOTAL-0.5,TOTAL-0.05])
h=hashlib.sha256()
with OUT.open('rb') as f:
 for b in iter(lambda:f.read(1<<20),b''):h.update(b)
(PACK/'SHA256.txt').write_text(f'{h.hexdigest()}  {OUT.name}\n')
summary=dict(out=str(OUT),sha256=h.hexdigest(),runtime=runtime,lufs=lufs,clip_check_exit=cc.returncode,align=align)
(PACK/'summary_v01.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=1));print(cc.stdout+cc.stderr)
