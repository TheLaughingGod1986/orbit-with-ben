#!/usr/bin/env python3
"""Join verified local chapter copies; retain their encoded picture interiors.

Run with --scratch pointing to the existing J2452 scratch folder. Outputs are
new versioned candidates, never source replacements. Final gates remain required.
"""
import argparse, hashlib, json, subprocess as sp
from pathlib import Path
ORDER=['013','021','027','025','023','031','020','022','028','029','024','026','019']
NAS=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/j2452/public_chapters_v01')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def run(args):
 sp.run(['ffmpeg','-v','error','-nostdin','-n',*map(str,args)],check=True,timeout=180)
def probe(p):
 return json.loads(sp.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))['streams']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--scratch',type=Path,required=True);ap.add_argument('--phase',choices=['prepare','picture','mix'],required=True);a=ap.parse_args()
 out=a.scratch/'final_join_v01';out.mkdir(exist_ok=True)
 manifest=out/'TIMELINE.json'
 if a.phase=='prepare':
  chapters=[];clock=0
  for film in ORDER:
   record=next(NAS.glob(f'{film}*/CHAPTER.json'));r=json.loads(record.read_text());delivery=r['copies'][0]
   candidate=Path(r.get('darkening',{}).get('output',r['build']['output']))
   assert candidate.exists() and sha(candidate)==delivery['sha256'],film
   streams=probe(candidate);v=next(s for s in streams if s['codec_type']=='video');n=int(v['nb_frames']);d=n/30
   assert v['width']==1920 and v['height']==1080 and v['pix_fmt']=='yuv420p' and v['r_frame_rate']=='30/1'
   chapters.append(dict(film=film,path=str(candidate),sha256=delivery['sha256'],frames=n,duration_s=d,start_s=clock,record=str(record),video_profile=v['profile']))
   clock+=d+(4 if film!=ORDER[-1] else 20)
  assert abs(chapters[2]['start_s']-967.2)<.01,'Earth grade ramp must stay aligned'
  manifest.write_text(json.dumps(dict(status='PREPARED_NOT_GATED',chapters=chapters,duration_s=clock,expected_frames=round(clock*30),breath_s=4,final_fade_s=20),indent=2)+'\n')
  print('prepared',clock,flush=True);return
 data=json.loads(manifest.read_text());chapters=data['chapters']
 if a.phase=='picture':
  parts=[]
  for i,c in enumerate(chapters):
   parts.append(Path(c['path']))
   if i==12:
    tail=out/'final_fade.mp4'
    if not tail.exists():
     run(['-ss',c['duration_s']-1/30,'-i',c['path'],'-vf','tpad=stop_mode=clone:stop_duration=20,trim=duration=20,setpts=PTS-STARTPTS,fade=t=out:st=0:d=20','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-r','30','-video_track_timescale','90000',tail])
    assert int(probe(tail)[0]['nb_frames'])==600
    parts.append(tail);continue
   nxt=chapters[i+1];join=out/f'join_{i+1:02d}.mp4'
   if not join.exists():
    graph='[0:v]setpts=PTS-STARTPTS,fps=30,setsar=1[a];[1:v]setpts=PTS-STARTPTS,fps=30,setsar=1[b];[a][b]xfade=transition=fade:duration=2:offset=1,format=yuv420p[v]'
    run(['-ss',c['duration_s']-3,'-i',c['path'],'-t','3','-i',nxt['path'],'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-frames:v','120','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-r','30','-video_track_timescale','90000',join])
   assert int(probe(join)[0]['nb_frames'])==120
   parts.append(join);print('join',i+1,flush=True)
  listing=out/'picture_concat.txt';listing.write_text(''.join(f"file '{p}'\nduration {int(probe(p)[0]['nb_frames'])/30:.9f}\n" for p in parts))
  picture=out/'sleep_picture_candidate_v01.mp4'
  if not picture.exists():run(['-f','concat','-safe','0','-i',listing,'-map','0:v','-an','-c:v','copy',picture])
  v=probe(picture)[0];assert int(v['nb_frames'])==data['expected_frames'],v
  (out/'PICTURE.json').write_text(json.dumps(dict(status='CANDIDATE_FULL_DECODE_AND_JOIN_GATES_PENDING',path=str(picture),sha256=sha(picture),frames=int(v['nb_frames']),duration_s=v['duration'],parts=[str(p) for p in parts]),indent=2)+'\n');return
 # Decode each chapter's already checked clean narration to the exact picture clock.
 args=[];graph=[];labels=[]
 for i,c in enumerate(chapters):
  args+=['-i',c['path']];pad=4 if i<12 else 20;d=c['duration_s']
  graph.append(f'[{i}:a]apad,atrim=duration={d},asetpts=PTS-STARTPTS,apad=pad_dur={pad},atrim=duration={d+pad}[n{i}]');labels.append(f'[n{i}]')
 graph.append(''.join(labels)+'concat=n=13:v=0:a=1[vo]')
 loop=a.scratch/'music_v02/drone_loop_78s_minus35_v01.wav'
 expected=json.loads(Path('jobs/reviews/J2452/music_v02/REPORT.json').read_text())['outputs'][1]['sha256'];assert sha(loop)==expected
 args+=['-stream_loop','-1','-i',loop]
 swells=[]
 for c in chapters[:-1]:
  t=c['start_s']+c['duration_s']-3
  swells.append(f'if(between(t,{t},{t+4}),(t-{t})/4,if(between(t,{t+4},{t+6}),1,if(between(t,{t+6},{t+10}),({t+10}-t)/4,0)))')
 expr='1+0.2589254118*('+ '+'.join(swells)+')';duration=data['duration_s']
 graph.append(f"[13:a]atrim=duration={duration},asetpts=PTS-STARTPTS,volume='{expr}':eval=frame,afade=t=in:d=2,afade=t=out:st={duration-20}:d=20[bed]")
 graph.append('[vo][bed]amix=inputs=2:duration=first:normalize=0[mix]')
 raw=out/'sleep_mix_pre_master_v01.wav'
 if not raw.exists():run([*args,'-filter_complex',';'.join(graph),'-map','[mix]','-ar','48000','-c:a','pcm_s24le',raw])
 print('raw mix ready; loudness normalization and saved-file verification still required',flush=True)
if __name__=='__main__':main()
