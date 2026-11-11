#!/usr/bin/env python3
"""Finished-master Proxima chapter; no source-film reconstruction or source audio. Candidate requires full undarkened gates and cover inspection before grading."""
import hashlib,json,subprocess as sp
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3]
OUT=Path('/Users/ben/_desk/J2452-sleep-scratch/public_proxima_v01')
MASTER=Path('/Volumes/data/mac-mini-archive/youtube-staging/026/026_NearestStar_v06_cfr18.mp4')
NARR=Path('/Users/ben/_desk/J2452-sleep-scratch/narration_026_v02/chapter_026_narration_v01.wav')

def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def run(a):sp.run(['ffmpeg','-v','error','-nostdin','-n',*a],check=True,timeout=420)
def enc():return ['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000']
def main():
 OUT.mkdir(exist_ok=True)
 chapter=json.loads((ROOT/'jobs/reviews/J2452/picture_timeline_v01.json').read_text())['chapters'][11]
 assert sha(NARR)==chapter['narration_sha256']
 assert sha(MASTER)=='6e587bb5ac33552cef55ac897d89f5516a90acef9473155254dd313fc73e09d3', 'Source differs from recorded upload master'
 # Finished-master card times come from its checked v03 assembler.
 # Exact card/Orbit windows checked against source assembler and source sheet.
 # Retain this finished picture; narration and timeline never move.
 covers=[(32.8,36.2,36.3,'chapter-1 cover'),(122.0,124.8,118.5,'chapter-2 cover'),(127.4,138.1,0,'plate:eso1323a.jpg'),(232,235.7,236,'chapter-3 cover'),(312.1,324,0,'plate:heic1007a.jpg'),(378.8,381.7,381.8,'chapter-5 cover')]
 title=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(title)
 d.text((90,940),"XII · Proxima Centauri in the Dark",font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',42),fill=(234,230,223,166));title.save(OUT/'title.png')
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
  if i==0:
   run(['-reinit_filter','0','-ss',str(src),'-i',str(MASTER),'-loop','1','-i',str(OUT/'title.png'),'-filter_complex_threads','1','-filter_complex',f'[0:v]{vf}[base];[1:v]format=rgba,fade=t=in:st=0:d=1.5:alpha=1,fade=t=out:st=4.5:d=1.5:alpha=1[t];[base][t]overlay=0:0:enable=lt(t\\,6)[v]','-map','[v]','-frames:v',str(frames),*enc(),str(dest)])
  elif label.startswith('plate:'):
   plate=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/07_Edit-Project/pool_v01')/label.split(':',1)[1]
   with Image.open(plate) as im:
    im=im.convert('RGB');w,h=im.size;cw=min(w,h*16/9);ch=cw*9/16
    im=im.crop(((w-cw)/2,(h-ch)/2,(w+cw)/2,(h+ch)/2));im.resize((2112,1188),Image.Resampling.LANCZOS).save(OUT/f'plate_{i:02d}.png')
   run(['-loop','1','-framerate','30','-i',str(OUT/f'plate_{i:02d}.png'),'-vf',f"zoompan=z='1+0.025*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,format=yuv420p",'-frames:v',str(frames),*enc(),str(dest)])
  else:run(['-reinit_filter','0','-ss',str(src),'-i',str(MASTER),'-vf',vf,'-frames:v',str(frames),*enc(),str(dest)])
  rows.append(dict(row=f'piece-{i}',timeline_in=start/30,timeline_out=end/30,source=MASTER.name,framing=dict(offset=src),src_w=1920,upscale=1,label=label,original_master_range=[a,b]))
  pieces.append((dest,dur));clock+=b-a
  print('saved',i,label,dur,flush=True)
 # Two-second cloned-handle dissolves preserve the complete narration clock.
 joined=[];changes=[dict(row='quiet-title',timeline_in=0,timeline_out=6,source='quiet-title',framing=dict(offset=0),src_w=1920,upscale=1)]
 for i,((src,dur),row) in enumerate(zip(pieces,rows)):
  a=1 if i else 0;b=dur-(1 if i<len(pieces)-1 else 0)
  if len(pieces)==1:
   joined.append(src);continue
  dest=OUT/f'interior_{i:02d}.mp4';run(['-ss',str(a),'-i',str(src),'-t',str(b-a),*enc(),str(dest)]);joined.append(dest)
  if row['label']!='public':changes.append(dict(row=f'cover-{i}',timeline_in=row['timeline_in'],timeline_out=row['timeline_out'],source=f'cover-{i}',framing=dict(offset=0),src_w=1920,upscale=1))
  if i==len(pieces)-1:continue
  dest=OUT/f'join_{i:02d}.mp4'
  graph=f'[0:v]trim=start={dur-1}:end={dur},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1[a];[1:v]trim=end=1,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=1[b];[a][b]xfade=transition=fade:duration=2:offset=0,format=yuv420p[v]'
  run(['-i',str(src),'-i',str(pieces[i+1][0]),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-t','2',*enc(),str(dest)]);joined.append(dest)
  t=row['timeline_out'];changes.append(dict(row=f'join-{i}',timeline_in=t-1,timeline_out=t+1,source=f'join-{i}',framing=dict(offset=0),src_w=1920,upscale=1))
 listing=OUT/'concat.txt';listing.write_text(''.join(f"file '{p}'\n" for p in joined))
 final=OUT/'026_proxima_undarkened_v01.mp4'
 run(['-f','concat','-safe','0','-i',str(listing),'-i',str(NARR),'-map','0:v','-map','1:a','-af','volume=-0.5dB','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(round(clock*30)/30),str(final)])
 full=[dict(row=f'pixel-{k}',timeline_in=k,timeline_out=min(k+2,clock),source=MASTER.name,framing=dict(offset=k),src_w=1920,upscale=1) for k in range(0,int(clock)+1,2)]
 for name,data in [('full_pixel_cuts.json',full),('changed_cuts.json',changes),('source_cuts.json',rows)]: (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
 report=dict(status='CANDIDATE_GATES_PENDING',film='026',output=str(final),sha256=sha(final),source_master=str(MASTER),source_sha256=sha(MASTER),narration_sha256=sha(NARR),expected_frames=round(clock*30),duration_s=round(clock*30)/30,slices=chapter['slices'],planned_ranges=chapter['planned_ranges'],covers=covers,darkening='Pending: whole chapter is after 20:30, apply measured 85 percent grade after undarkened gates.',fallback='Plan-named alternative starfields eso1323a and heic1007a cover Orbit. Chapter cards use neighbouring finished-master footage. Historical template note: Cover plates have no named official ID in the plan and no 03_Footage folder on NAS. Use finished-master neighbouring sky and existing illustrated views, preserving credits. Donor intervals are recorded in source_cuts.json. Current finished v03 differs from the plan. Source sheet and full-master assembler identify two Orbit windows and six chapter-card windows, replaced with neighbouring finished-master pictures. No hook caption in opening; source labels retained. Existing labels and generated picture retained under the Chief ruling.',inherited='Charts/labels and untouched public-master stretches retained under 09:29Z ruling; no gate waiver.')
 (OUT/'BUILD.json').write_text(json.dumps(report,indent=2)+'\n');print(final,flush=True)
if __name__=='__main__':main()
