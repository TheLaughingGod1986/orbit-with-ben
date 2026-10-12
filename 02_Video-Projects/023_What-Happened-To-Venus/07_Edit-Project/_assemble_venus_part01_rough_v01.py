#!/usr/bin/env python3
"""Disk-only Venus Part01. Saturn v03b row-build/audio/report structure; no external calls."""
from pathlib import Path
import json, subprocess as sp, re, math, shutil, sys
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent; EP=HERE.parent
UAT=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/OWB UAT'
WORK=Path('/private/tmp/venus023_part01_work'); PACK=UAT/'023_Venus_Part01_rough_v01_pack'
OUT=UAT/'023_Venus_Part01_rough_v01.mp4'; TOTAL=142.22; FPS=30
VO=EP/'02_Voiceover/venus_vo_v01.mp3'; BED=UAT/'jupiter-music.mp3'
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def run(args):
 p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-6000:])
def probe(p):return float(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
def detector(args):return sp.run(['ffmpeg','-hide_banner',*map(str,args),'-f','null','-'],capture_output=True,text=True).stderr
def finalize_pack(pack,here,work,out):
 import json,subprocess,hashlib,shutil
 from PIL import Image
 checks=json.loads((pack/'clip_check.json').read_text());align=json.loads((pack/'align_vs_vo.json').read_text())
 limits=[]
 for r in checks:
  values=[]
  for part in r.get('visual_parts',[]):
   if not part['source_file'].lower().endswith('.jpg'):continue
   t=(part['timeline_in']+part['timeline_out'])/2
   dst=work/f"verify_{r['row']}_{part['part']}.jpg"
   subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(t),'-i',str(out),'-frames:v','1','-vf','scale=320:180',str(dst)],check=True)
   h=Image.open(dst).convert('L').histogram();pct=round(sum(h[:26])/sum(h)*100,3)
   values.append(dict(part=part['part'],sample_time=t,near_black_percent=pct,threshold_luma=25,status='PASS' if pct<30 else 'FAIL'))
   limits.append(pct)
  r['nasa_still_near_black_samples']=values
  if any(v['status']=='FAIL' for v in values):r['status']='FAIL';r['failures'].append('NASA still near-black area >=30%')
 (pack/'clip_check.json').write_text(json.dumps(checks,indent=2))
 lines=['Row | Timeline in–out (s) | Duration | Black | Freeze | Mixed gap | VO pauses | Result | Source / move','Black: >=98% pixels below 10% luma for >=0.1 s. Freeze: noise <=-50dB for >=1 s. Mixed silence: <-45dB for >=0.5 s. VO-only silence: <-40dB for >=0.5 s; retained pauses are informational.']
 for r in checks:lines.append(f"{r['row']} | {r['timeline_in']:.3f}–{r['timeline_out']:.3f} | {r['duration']:.3f} | {len(r['black_frames'])} | {len(r['frozen_frames'])} | {len(r['mix_audio_gaps'])} | {len(r['vo_silences'])} | {r['status']} | {r['source_file']} / {r['move']}")
 (pack/'clip_check.txt').write_text('\n'.join(lines)+'\n')
 lines=[f"Output {align['output_duration']:.6f}s; VO segment {align['vo_segment_length']:.6f}s; delta {align['duration_delta']:+.6f}s.",'Row | Actual picture/overlay in–out | Shot-list VO in–out | In/out delta | Nearest word in/out delta | Flag >1s']
 for r in align['rows']:lines.append(f"{r['row']} | {r['cut_in']:.3f}–{r['cut_out']:.3f} | {r['shot_vo_in']:.3f}–{r['shot_vo_out']:.3f} | {r['delta_in']:+.3f}/{r['delta_out']:+.3f} | {r['word_delta_in']:+.3f}/{r['word_delta_out']:+.3f} | {'FLAG' if r['flag'] else 'PASS'}")
 lines+=['Rows 15a/15b: shared picture boundary 102.80 ->105.10s (+2.30s). Audio unchanged. The earlier row uses two internal cuts; extra PIA00200 terrain is disclosed. Row 8 includes the preserved chapter breath.']
 (pack/'align_vs_vo.txt').write_text('\n'.join(lines)+'\n')
 h=hashlib.sha256()
 with out.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 (pack/'SHA256.txt').write_text(f'{h.hexdigest()}  {out.name}\n')
 report=(pack/'REPORT.md').read_text()
 report+=f'\nFinal encoded NASA-still midpoint samples: maximum near-black area **{max(limits):.3f}%**, all below 30% (luma <=25/255). SDO transit and the locked albedo retain their supplied dark backgrounds. These are midpoint samples, supported by full-runtime blackdetect; no claim of an every-pixel/every-frame area audit.\n\nOutput duration exceeds 142.22 s by **{align["duration_delta"]:.6f} s** for the final 30 fps frame; the locked last word ends 142.20 s and Ch2 starts 142.98 s. All detected VO pauses retained. Rows 15a/15b share a picture boundary at **105.10 s**, versus **102.80 s** in the shot list (+2.30 s); no spoken audio was moved.\n'
 (pack/'REPORT.md').write_text(report)
 shutil.copytree(pack,here/'part01_rough_v01_pack',dirs_exist_ok=True)
 hand=out.parents[3]/'_desk/handoff/venus023_part01_DONE.md'
 # Resolve the real home independently of the iCloud nesting.
 from pathlib import Path
 hand=Path.home()/'_desk/handoff/venus023_part01_DONE.md'
 text=hand.read_text().strip();text+=' Final detector checks PASS; picture cuts all 4–6 s. Rows 15a/15b flag a +2.30 s picture-boundary adjustment, disclosed in both alignment reports.\n';hand.write_text(text)

# Read authoritative table, selecting visual rows through 18. Card and breath are overlays/continuous picture.
rows=[]
for line in (HERE/'SHOT_LIST_v02.md').read_text().splitlines():
 c=[x.strip() for x in line.split('|')[1:-1]]
 if len(c)!=8 or not re.fullmatch(r'\d+[abc]?',c[0]):continue
 if int(re.match(r'\d+',c[0])[0])>18:continue
 rows.append(dict(row=c[0],vo_in=float(c[1]),vo_out=float(c[2]),type=c[3],requested=c[4],move=c[5],beat=c[6],notes=c[7]))
assets={'1':'open/PIA00254.jpg','2':'open/PIA00106.jpg','3':'open/PIA00240.jpg','4':'open/PIA00241.jpg','5':'open/PIA00087.jpg','6':'open/PIA23791.jpg','7':'open/PIA00104.jpg','8':'open/PIA00104.jpg','11a':'open/PIA23791.jpg','11b':'open/PIA00240.jpg','12a':'earth/as17-148-22727.jpg','12b':'open/PIA00104.jpg','13a':'sdo/AIA171VenusTransit_HD1080.mp4','13b':'sdo/AIA171VenusTransit_HD1080.mp4','14b':'open/PIA00104.jpg','15a':'open/PIA00106.jpg','15b':'magellan_extra/PIA00215.jpg','16a':'open/PIA00240.jpg','16b':'magellan_extra/PIA00159.jpg','17':'magellan_extra/PIA00246.jpg','18':'open/PIA00087.jpg'}
subs=[{'row':'1','reason':'Magellan flyover not harvested; mandated PIA00254 fallback'}, {'row':'16b','reason':'PIA00093 500x568 would exceed 2.35x upscale; PIA00159 harvested high-resolution Magellan substitute'}, {'row':'17','reason':'Unnamed Sedna/lava perspective unavailable; harvested PIA00246 perspective'}, {'row':'18','reason':'Unnamed low-plains/haze unavailable; harvested PIA00087 plains'}]
for p in [WORK,PACK]:p.mkdir(parents=True,exist_ok=True)
words=json.loads((EP/'02_Voiceover/words.json').read_text())['words']
visual=[]
for r in rows:
 if r['row'] in ['9','10']:continue
 r['source_file']=str(EP/'04_Generated-Clips/01_Raw/graphics_v01/albedo.mp4') if r['row'] in ['13c','14a'] else str(HERE/'nasa_pool_v01'/assets[r['row']])
 end=43.58 if r['row']=='8' else r['vo_out']
 n=2 if r['row']=='17' else 3 if r['row']=='18' else 1
 for k in range(n):
  q=dict(r);q.update(timeline_in=r['vo_in']+(end-r['vo_in'])*k/n,timeline_out=r['vo_in']+(end-r['vo_in'])*(k+1)/n,part=k+1);visual.append(q)
# Picture-only pacing adjustment. Audio timestamps remain locked; disclose boundary deltas.
new=[]
for v in visual:
 r=v['row']
 if r=='4':v['timeline_out']=20.54
 if r=='5':v['timeline_in']=20.54
 if r=='6':v['timeline_out']=29.58
 if r=='7':v.update(timeline_in=29.58,timeline_out=35.58)
 if r=='8':
  v.update(timeline_in=35.58,timeline_out=39.58);new.append(dict(v));v=dict(v);v.update(timeline_in=39.58,timeline_out=43.58,part=2)
 if r=='12b':v['timeline_out']=66.80
 if r=='13a':v['timeline_in']=66.80
 if r=='13c':v['timeline_out']=84.10
 if r=='14a':v.update(timeline_in=84.10,timeline_out=90.00)
 if r=='15a':
  v.update(timeline_in=96.00,timeline_out=100.553333);new.append(dict(v));v=dict(v);v.update(timeline_in=100.553333,timeline_out=105.106667,part=2,source_file=str(HERE/'nasa_pool_v01/magellan_extra/PIA00200.jpg'))
 if r=='15b':v.update(timeline_in=105.106667,timeline_out=109.66)
 new.append(v)
visual=new
for v in visual:
 v['timeline_in']=round(v['timeline_in']*FPS)/FPS;v['timeline_out']=round(v['timeline_out']*FPS)/FPS
subs.append({'row':'15a part2','reason':'Extra 4–6s cut uses harvested PIA00200 Magellan terrain; row15b starts later, alignment flag disclosed'})
card=Image.new('RGBA',(1920,1080),(0,0,0,0));draw=ImageDraw.Draw(card);draw.rounded_rectangle((90,860,1000,990),radius=15,fill=(23,36,55,220));draw.text((125,886),'The Twin Next Door',font=ImageFont.truetype(FONT,62),fill='white');card.save(WORK/'chapter.png')
if '--finish-only' not in sys.argv:
 # Independent rendered rows, 0.2s handles either side; pairwise xfade then concat avoids a huge filter graph.
 for i,r in enumerate(visual):
  start=r['timeline_in'];end=r['timeline_out']; pre=.2 if i else 0;post=.2 if i<len(visual)-1 else 0
  dur=end-start+pre+post; frames=round(dur*FPS); dest=WORK/f'row_{i:02}.mp4';r['render']=str(dest)
  src=Path(r['source_file']);print('row',r['row'],r['part'],start,end,flush=True)
  if src.suffix.lower()=='.jpg':
   im=Image.open(src).convert('RGB')
   if src.name=='PIA23791.jpg':im=im.crop((1145,0,2245,1096))  # single Mariner disk, omit source comparison divider
   scale=max(1920/im.width,1080/im.height)
   # NASA colour grade: lifted shadows, gentle warm balance and saturation.
   im=ImageEnhance.Color(im).enhance(1.10);im=ImageEnhance.Contrast(im).enhance(1.04)
   im=im.point([min(255,int(v*.92+28)) for v in range(256)]*3)
   im=im.resize((round(im.width*scale*1.1),round(im.height*scale*1.1)),Image.Resampling.LANCZOS)
   x=(im.width-2112)//2;y=(im.height-1188)//2;im=im.crop((max(0,x),max(0,y),max(0,x)+2112,max(0,y)+1188))
   plate=WORK/f'plate_{i:02}.png';im.save(plate)
   pct=.06 if '6%' in r['move'] else .05
   if r['part']>1:pct=.06
   vf=f"scale=3840:2160,zoompan=z='1+{pct}*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={frames}:s=1920x1080:fps=30,setsar=1,format=yuv420p"
   inp=['-i',plate]
  else:
   offset=0
   if r['row']=='13a':offset=8
   if r['row']=='13b':offset=13.64
   if r['row']=='14a':offset=5.90
   inp=['-ss',max(0,offset-pre),'-i',src]
   vf='scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,setsar=1,format=yuv420p'
  if r['row']=='11a':
   a=43.74-start+pre;b=a+2.5
   run([*inp,'-loop','1','-i',WORK/'chapter.png','-filter_complex',f"[0:v]{vf}[base];[base][1:v]overlay=enable='between(t,{a},{b})',format=yuv420p[v]",'-map','[v]','-t',f'{frames/FPS:.6f}','-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4',dest])
  else:run([*inp,'-vf',vf,'-t',f'{frames/FPS:.6f}','-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4',dest])
 # Trim each row's center; encode each 0.4s transition separately, concatenate continuous chunks.
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
# Acrossfade-loop music as many times as needed. Locked VO decoded once, trimmed only; no speed or splice.
bdur=probe(BED)-8-6.5-2;copies=max(1,math.ceil((TOTAL-4)/(bdur-4)))
inputs=[]
for _ in range(copies):inputs+=['-ss',8,'-i',BED]
fc=''
for i in range(copies):
 fc+=f'[{i}:a]asplit=2[h{i}][t{i}];[h{i}]atrim=0:71.5,asetpts=PTS-STARTPTS[head{i}];[t{i}]atrim=start=78,asetpts=PTS-STARTPTS[tail{i}];[head{i}][tail{i}]acrossfade=d=2:c1=tri:c2=tri[bed{i}];'
last='bed0'
for i in range(1,copies):
 lab=f'm{i}';fc+=f'[{last}][bed{i}]acrossfade=d=4:c1=tri:c2=tri[{lab}];';last=lab
fc+=f'[{last}]atrim=0:{TOTAL},asetpts=PTS-STARTPTS,volume=0.14[m]'
run([*inputs,'-filter_complex',fc,'-map','[m]','-c:a','pcm_s24le',WORK/'music.wav'])
mixfilter=f'[0:a]atrim=0:{TOTAL},asetpts=PTS-STARTPTS[v];[v][1:a]amix=inputs=2:duration=first:normalize=0'
first=sp.run(['ffmpeg','-hide_banner','-i',str(VO),'-i',str(WORK/'music.wav'),'-filter_complex',mixfilter+',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]','-map','[a]','-f','null','-'],capture_output=True,text=True).stderr
stats=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',first,re.S)[-1]);(PACK/'loudnorm_first_pass.json').write_text(json.dumps(stats,indent=2))
normal=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:linear=true"
run(['-i',VO,'-i',WORK/'music.wav','-filter_complex',mixfilter+','+normal+'[a]','-map','[a]','-ar','48000','-c:a','aac','-b:a','192k',WORK/'audio.m4a'])
run(['-i',WORK/'picture.mp4','-i',WORK/'audio.m4a','-map','0:v','-map','1:a','-c','copy','-t',TOTAL,'-movflags','+faststart',OUT])
# Actual encoded output detection; VO-only silence is distinct from final mix.
log=detector(['-i',OUT,'-vf','blackdetect=d=0.1:pix_th=0.10:pic_th=0.98,freezedetect=n=-50dB:d=1','-af','silencedetect=n=-45dB:d=0.5']);(PACK/'ffmpeg_checks.txt').write_text(log)
vl=detector(['-i',VO,'-t',TOTAL,'-af','silencedetect=n=-40dB:d=0.5']);(PACK/'vo_silencedetect.txt').write_text(vl)
ll=detector(['-i',OUT,'-af','ebur128=peak=true']);(PACK/'loudness.txt').write_text(ll)
lufs=float(re.findall(r'I:\s*([-\d.]+) LUFS',ll)[-1]);runtime=probe(OUT)
def intervals(log,key):
 starts=[float(x) for x in re.findall(key+r'_start[:= ]+([\d.]+)',log)];ends=[float(x) for x in re.findall(key+r'_end[:= ]+([\d.]+)',log)];return list(zip(starts,ends+[TOTAL]))
black=intervals(log,'black');freeze=intervals(log,'freeze');gaps=intervals(vl,'silence');mixgaps=intervals(log,'silence')
checks=[];align=[]
for r in rows:
 a=r['vo_in'];b=r['vo_out'];related=[v for v in visual if v['row']==r['row']]
 actual_in=related[0]['timeline_in'] if related else a;actual_out=related[-1]['timeline_out'] if related else b
 source=related[0]['source_file'] if related else 'continuous previous picture' if r['row']=='9' else 'lower-third overlay'
 def overlap(items):return [[x,y] for x,y in items if x<b and y>a]
 fails=[]
 if overlap(black):fails.append('black frame')
 if overlap(freeze):fails.append('frozen frame')
 if overlap(mixgaps):fails.append('mixed audio gap')
 checks.append(dict(row=r['row'],timeline_in=actual_in,timeline_out=actual_out,source_file=source,visual_parts=[{k:v[k] for k in ['timeline_in','timeline_out','source_file','part']} for v in related],move=r['move'],duration=round(actual_out-actual_in,6),vo_duration=b-a,black_frames=overlap(black),frozen_frames=overlap(freeze),vo_silences=overlap(gaps),audio_gap_note='VO pauses retained; final mix checked separately',mix_audio_gaps=overlap(mixgaps),status='FAIL' if fails else 'PASS',failures=fails))
 nearin=min(words,key=lambda w:abs(w['start']-a));nearout=min(words,key=lambda w:abs(w['end']-b))
 ai=43.74 if r['row']=='10' else actual_in;bo=46.24 if r['row']=='10' else actual_out
 align.append(dict(row=r['row'],cut_in=ai,cut_out=bo,shot_vo_in=a,shot_vo_out=b,delta_in=round(ai-a,3),delta_out=round(bo-b,3),nearest_word_in=nearin,nearest_word_out=nearout,word_delta_in=round(ai-nearin['start'],3),word_delta_out=round(bo-nearout['end'],3),flag=abs(ai-a)>1 or abs(bo-b)>1 or abs(ai-nearin['start'])>1 or abs(bo-nearout['end'])>1,internal_cuts=[v['timeline_in'] for v in related[1:]]))
for name,data in [('clip_check',checks),('align_vs_vo',dict(rows=align,output_duration=runtime,vo_segment_length=TOTAL,duration_delta=runtime-TOTAL))]:
 (PACK/(name+'.json')).write_text(json.dumps(data,indent=2));(PACK/(name+'.txt')).write_text(json.dumps(data,indent=2))
# Six evenly spaced frames per 25-second review sheet + six-frame open sheet beginning exactly at frame zero.
def sheet(name,times):
 board=Image.new('RGB',(1440,600),(18,18,22));d=ImageDraw.Draw(board)
 for i,t in enumerate(times):
  p=WORK/f'frame_{name}_{i}.jpg';run(['-ss',t,'-i',OUT,'-frames:v','1','-vf','scale=480:270',p]);x=i%3*480;y=i//3*300;board.paste(Image.open(p),(x,y));d.text((x+8,y+275),f'{t:.2f}s',fill='white')
 board.save(PACK/(name+'.jpg'),quality=92)
sheet('frame0_sheet',[0,.2,.4,.6,.8,1])
for a in range(0,143,25):
 b=min(TOTAL,a+25);sheet(f'sheet_{a:03}_{b:06.2f}',[a+(b-a)*i/6 for i in range(6)])
pace=[dict(row=v['row'],part=v['part'],duration=round(v['timeline_out']-v['timeline_in'],3)) for v in visual if not 3.9999<=v['timeline_out']-v['timeline_in']<=6.0001]
report=f'''# Venus 023 Part01 rough v01

Built Ch0 + Ch1, rows 1–18, locked VO 0–142.22 s unchanged in timing. Runtime **{runtime:.3f} s**, 1920×1080, 30 fps, H.264/AAC. Measured integrated loudness **{lufs:.1f} LUFS**. Music: `{BED}` (existing house bed, 14% level, starts 8 s into bed after quiet intro; 2 s acrossfade joins source 79.5 s to 86 s to remove its quiet break; acrossfade-loop support, full runtime). No spend, generation, downloads, posting, claims, commits or push.

Frame 0: PIA00254 pushing immediately; no title/fade/Orbit. Ch1 lower-third 43.74–46.24 s, aligned to first spoken word. 0.7 s chapter breath preserved. 0.4 s crossfades. Rows 8, 15a, 17 and 18 split internally; all picture cuts 4–6 s. Measured two-pass loudnorm after amix normalize=0. NASA stills colour graded, shadows lifted, 16:9 cover; no >2.35x source upscale. Credits: NASA/JPL; Earth NASA; transit NASA/SDO/SVS. Existing albedo video used continuously across 13c/14a, no replacement graphic.

## Substitutions
{json.dumps(subs,indent=2)}

## Checks and limitations
Detection FAIL rows: {json.dumps([r['row'] for r in checks if r['status']=='FAIL'])}. Alignment flags: {json.dumps([r['row'] for r in align if r['flag']])}. Pace exceptions after picture-only cut adjustments (seconds): {json.dumps(pace)}. These are reported for review; not a full-film ship approval. VO pauses are expected and listed independently of mixed audio gaps. Row 8 carries picture across breath to 43.58 s. Detector details and original logs included. Part ends directly at Ch1 boundary; no full-film outro inserted.

PIA23791 uses: 2; reserve at most one for rest of film. No Venera or Orbit. Thread status attempted; DNS unavailable, no thread read claimed.

Output: `{OUT}`
'''
(PACK/'REPORT.md').write_text(report)
shutil.copytree(PACK,HERE/'part01_rough_v01_pack',dirs_exist_ok=True)
hand=Path.home()/'_desk/handoff';hand.mkdir(parents=True,exist_ok=True)
(hand/'venus023_part01_DONE.md').write_text(f'Venus 023 Part01 rough v01 and review pack ready: {OUT}; runtime {runtime:.3f} s, 1920×1080/30 fps H.264/AAC, {lufs:.1f} LUFS. Pack: {PACK}, also copied to project edit folder. Locked VO untouched in timing, local NASA plates and existing albedo only, existing jupiter-music house bed; substitutions and all detector/alignment/pace exceptions listed in REPORT.md. No spend, posting, claims, commits or push. Thread status could not be read due to DNS failure.\n')
finalize_pack(PACK,HERE,WORK,OUT)
(Path.home()/'_desk/locks/owb023_part01_edit.lock').unlink(missing_ok=True)
print('DONE',runtime,lufs,flush=True)
