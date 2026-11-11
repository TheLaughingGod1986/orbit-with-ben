#!/usr/bin/env python3
"""Finished-master Light Speed chapter; no source-film reconstruction or source audio. Candidate requires full undarkened gates and cover inspection before grading."""
import hashlib,json,subprocess as sp
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3]
OUT=Path('/Users/ben/_desk/J2452-sleep-scratch/public_light_v02')
MASTER=Path('/Volumes/data/mac-mini-archive/youtube-staging/024/024_LightSpeed_v06.mp4')
NARR=Path('/Users/ben/_desk/J2452-sleep-scratch/narration_v01/chapter_024_narration_v01.wav')

def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def run(a):sp.run(['ffmpeg','-v','error','-nostdin','-n',*a],check=True,timeout=420)
def enc():return ['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000']
def main():
 OUT.mkdir(exist_ok=True)
 chapter=json.loads((ROOT/'jobs/reviews/J2452/picture_timeline_v01.json').read_text())['chapters'][10]
 assert sha(NARR)==chapter['narration_sha256']
 assert sha(MASTER)=='8d0b131771c1e6bfc8b33f49f5c628e96ae3db3af7a890864f2239960a5bde02'
 # Exact finished-master card windows and Orbit intervals from the v06 pack.
 covers=[(41.6,44.7,44.8,'GPS card cover'),(110.5,113.4,113.5,'light rule card cover'),(141.1,145.6,136.7,'light-clock neighbour cover'),(219.45,220.7,221,'subscribe tail cover'),(224.2,227.2,227.3,'trip card cover'),(232.9,236,232.9,'pre-Omni departure cover'),(279.9,287.1,279.9,'pre-Omni contraction cover'),(312.4,317.5,307,'Earth neighbour cover'),(324.2,327.3,327.4,'energy card cover'),(399,402,402.1,'future card cover'),(442.2,446.2,442.2,'pre-Omni closing cover')]
 title=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(title)
 d.text((90,940),"XI · Clocks Near the Speed of Light",font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',42),fill=(234,230,223,166));title.save(OUT/'title.png')
 recipes=[]
 for s in chapter['slices']:
  lo,hi=s['master_in_s'],s['master_out_s']; cursor=lo
  for a,b,donor,label in covers:
   if b<=lo or a>=hi:continue
   a=max(a,lo);b=min(b,hi)
   if a>cursor:recipes.append((cursor,a,cursor,'public'))
   recipes.append((a,b,donor,label));cursor=b
  if cursor<hi:recipes.append((cursor,hi,cursor,'public'))
 clock=0;pieces=[];rows=[]
 for i,(a,b,src,label) in enumerate(recipes):
  end=round((clock+b-a)*30); start=round(clock*30);frames=end-start;dur=frames/30
  dest=OUT/f'piece_{i:02d}.mp4'
  vf='setpts=PTS-STARTPTS,scale=1920:1080,setsar=1,fps=30,format=yuv420p'
  input_master=Path('/Volumes/data/mac-mini-archive/youtube-staging/024/024_LightSpeed_v05d.mp4') if label.startswith('pre-Omni') else MASTER
  old=OUT.with_name('public_light_v01')/dest.name
  if dest.exists():
   count=int(json.loads(sp.check_output(['ffprobe','-v','error','-show_entries','stream=nb_frames','-of','json',str(dest)]))['streams'][0]['nb_frames'])
   if count!=frames: dest=OUT/f'piece_{i:02d}_corrected.mp4';old=OUT/'never-reuse' 
  if dest.exists():
   pass
  elif old.exists() and i<12 and i!=5:
   import shutil
   shutil.copyfile(old,dest)
  elif i==0:
   run(['-reinit_filter','0','-ss',str(src),'-i',str(input_master),'-loop','1','-i',str(OUT/'title.png'),'-filter_complex_threads','1','-filter_complex',f'[0:v]{vf}[base];[1:v]format=rgba,fade=t=in:st=0:d=1.5:alpha=1,fade=t=out:st=4.5:d=1.5:alpha=1[t];[base][t]overlay=0:0:enable=lt(t\\,6)[v]','-map','[v]','-frames:v',str(frames),*enc(),str(dest)])
  else:run(['-reinit_filter','0','-ss',str(src),'-i',str(input_master),'-vf',vf,'-frames:v',str(frames),*enc(),str(dest)])
  rows.append(dict(row=f'piece-{i}',timeline_in=start/30,timeline_out=end/30,source=input_master.name,framing=dict(offset=src),src_w=1920,upscale=1,label=label,original_master_range=[a,b]))
  pieces.append((dest,dur));clock+=b-a
  print('saved',i,label,dur,flush=True)
 # One-second cloned-handle dissolves preserve the complete narration clock.
 joined=[];changes=[dict(row='quiet-title',timeline_in=0,timeline_out=6,source='quiet-title',framing=dict(offset=0),src_w=1920,upscale=1)]
 for i,((src,dur),row) in enumerate(zip(pieces,rows)):
  a=.5 if i else 0;b=dur-(.5 if i<len(pieces)-1 else 0)
  if len(pieces)==1:
   joined.append(src);continue
  dest=OUT/f'interior_final_{i:02d}.mp4';run(['-ss',str(a),'-i',str(src),'-t',str(b-a),*enc(),str(dest)]);joined.append(dest)
  if row['label']!='public':changes.append(dict(row=f'cover-{i}',timeline_in=row['timeline_in'],timeline_out=row['timeline_out'],source=f'cover-{i}',framing=dict(offset=0),src_w=1920,upscale=1))
  if i==len(pieces)-1:continue
  dest=OUT/f'join_short_handles_{i:02d}.mp4'
  graph=f'[0:v]trim=start={dur-.5}:end={dur},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.5[a];[1:v]trim=end=0.5,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=0.5[b];[a][b]xfade=transition=fade:duration=1:offset=0,format=yuv420p[v]'
  run(['-i',str(src),'-i',str(pieces[i+1][0]),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-t','1',*enc(),str(dest)]);joined.append(dest)
  t=row['timeline_out'];changes.append(dict(row=f'join-{i}',timeline_in=t-.5,timeline_out=t+.5,source=f'join-{i}',framing=dict(offset=0),src_w=1920,upscale=1))
 listing=OUT/'concat.txt';listing.write_text(''.join(f"file '{p}'\n" for p in joined))
 final=OUT/'024_light_undarkened_v01.mp4'
 run(['-f','concat','-safe','0','-i',str(listing),'-i',str(NARR),'-map','0:v','-map','1:a','-af','volume=-0.5dB','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(round(clock*30)/30),str(final)])
 full=[dict(row=f'pixel-{k}',timeline_in=k,timeline_out=min(k+2,clock),source=MASTER.name,framing=dict(offset=k),src_w=1920,upscale=1) for k in range(0,int(clock)+1,2)]
 for name,data in [('full_pixel_cuts.json',full),('changed_cuts.json',changes),('source_cuts.json',rows)]: (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
 report=dict(status='CANDIDATE_GATES_PENDING',film='024',output=str(final),sha256=sha(final),source_master=str(MASTER),source_sha256=sha(MASTER),narration_sha256=sha(NARR),expected_frames=round(clock*30),duration_s=round(clock*30)/30,slices=chapter['slices'],planned_ranges=chapter['planned_ranges'],covers=covers,darkening='Pending: whole chapter is after 20:30, apply measured 85 percent grade after undarkened gates.',fallback='Plan-named pre-Omni master retains Orbit in two windows, rejected by sampled stills. Those windows use finished-master neighbouring light-clock and Earth pictures. Remaining three pre-Omni windows contain no Orbit in sampled stills. Cards use neighbouring finished-master pictures. Source charts and labels retained. No source rebuild or generation.',inherited='Charts/labels and untouched public-master stretches retained under 09:29Z ruling; no gate waiver.')
 (OUT/'BUILD.json').write_text(json.dumps(report,indent=2)+'\n');print(final,flush=True)
if __name__=='__main__':main()
