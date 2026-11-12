#!/usr/bin/env python3
"""Bounded repair using Saturn's previously measured clean neighboring frame.

Preserves original chapter clock; changes picture only, retains all audio in
separately verified PCM. Never overwrites saved chapters or prior candidates.
"""
import json, subprocess as sp, hashlib, sys
from pathlib import Path
S=(Path.home()/'_desk/J2452-sleep-scratch/final_join_v01')
T=json.loads((S/'TIMELINE.json').read_text());c=T['chapters'][1];n=T['chapters'][2]
def run(a):sp.run(['ffmpeg','-v','error','-nostdin','-n',*map(str,a)],check=True,timeout=150)
def frames(p):return int(sp.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','csv=p=0',str(p)]))
def enc():return ['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-r','30','-video_track_timescale','90000']
# Exact existing keyframe: no full chapter transcode.
k=15016;start=k/30;tailframes=c['frames']-k
prefix=S/'saturn_prefix_v05.mp4';tail=S/'saturn_exit_v04.mp4';join=S/'join_endpoint_v04_02.mp4'
if not prefix.exists():run(['-i',c['path'],'-frames:v',k,'-map','0:v','-c:v','copy',prefix])
assert frames(prefix)==k,(frames(prefix),k)
if not tail.exists():
 g=f'[0:v]setpts=PTS-STARTPTS,trim=duration=5.5[a];[1:v]trim=end_frame=1,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=20[b];[a][b]xfade=transition=fade:duration=2:offset=3.5,format=yuv420p[v]'
 run(['-ss',start,'-i',c['path'],'-ss','505','-i',c['path'],'-filter_complex_threads','1','-filter_complex',g,'-map','[v]','-frames:v',tailframes,*enc(),tail])
assert frames(tail)==tailframes
if not join.exists():
 g='[0:v]trim=end_frame=1,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=3,trim=duration=3,fps=30,setsar=1[a];[1:v]trim=end_frame=1,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=3,trim=duration=3,fps=30,setsar=1[b];[a][b]xfade=transition=fade:duration=2:offset=1,format=yuv420p[v]'
 run(['-ss','505','-i',c['path'],'-i',n['path'],'-filter_complex_threads','1','-filter_complex',g,'-map','[v]','-frames:v','120',*enc(),join])
assert frames(join)==120
# Gate a contiguous neighborhood including unchanged lead-in and incoming Earth.
earth=S/'earth_head_v04.mp4'
if not earth.exists():run(['-i',n['path'],'-frames:v','90',*enc(),earth])
listing=S/'saturn_neighborhood_v04.txt';listing.write_text(''.join(f"file '{p}'\n" for p in [tail,join,earth]))
video=S/'saturn_neighborhood_v04.mp4'
if not video.exists():run(['-f','concat','-safe','0','-i',listing,'-an','-c:v','copy',video])
qa=S/'saturn_neighborhood_qa_v04';qa.mkdir(exist_ok=True)
d=frames(video)/30
cuts=[dict(row=f'boundary-{i}',timeline_in=i/2,timeline_out=min((i+1)/2,d),source='saturn-earth-neighborhood',framing=dict(offset=i/2),src_w=1920,upscale=1) for i in range(int(d*2))]
(qa/'cuts.json').write_text(json.dumps(cuts));(qa/'pool.json').write_text(json.dumps([dict(source='saturn-earth-neighborhood',title='Public Saturn neighboring frame and Earth chapter transition')]))
with (qa/'gate.log').open('w') as log:
 code=sp.run([sys.executable,'scripts/picture_qa.py',str(video),'--cuts',str(qa/'cuts.json'),'--pool',str(qa/'pool.json'),'--out-dir',str(qa)],stdout=log,stderr=sp.STDOUT,timeout=180).returncode
report=dict(status='PASS' if code==0 else 'FAIL',gate_exit=code,prefix_frames=k,tail_frames=tailframes,chapter_frames=c['frames'],donor_second=505,tail_start_s=start,fade_start_s=start+3.5,fade_duration_s=2,neighborhood=str(video),gate=str(qa/'picture_qa.json'),limitations='Picture-only repair. Original PCM narration remains unchanged; full assembly checks pending.')
(S/'SATURN_EXIT_REPAIR_V04.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));sys.exit(code)
