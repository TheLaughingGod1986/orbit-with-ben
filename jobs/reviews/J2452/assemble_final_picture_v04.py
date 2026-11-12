#!/usr/bin/env python3
"""Stream-copy saved picture interiors with the separately gated Saturn exit."""
import json,subprocess as sp,hashlib
from pathlib import Path
S=(Path.home()/'_desk/J2452-sleep-scratch/final_join_v01')
t=json.loads((S/'TIMELINE.json').read_text());assert json.loads((S/'SATURN_EXIT_REPAIR_V04.json').read_text())['status']=='PASS'
parts=[]
for i,c in enumerate(t['chapters']):
 parts.extend([S/'saturn_prefix_v05.mp4',S/'saturn_exit_v04.mp4'] if i==1 else [Path(c['path'])])
 parts.append(S/'final_fade.mp4' if i==12 else S/('join_endpoint_v04_02.mp4' if i==1 else f'join_endpoint_v02_{i+1:02d}.mp4'))
f=S/'picture_concat_v04.txt';f.write_text(''.join(f"file '{p}'\n" for p in parts))
p=S/'sleep_picture_candidate_v04.mp4'
if not p.exists():sp.run(['ffmpeg','-v','error','-nostdin','-n','-f','concat','-safe','0','-i',str(f),'-map','0:v','-an','-c:v','copy',str(p)],check=True,timeout=180)
v=json.loads(sp.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))['streams'][0]
assert int(v['nb_frames'])==t['expected_frames']
with p.open('rb') as h:d=hashlib.file_digest(h,'sha256').hexdigest()
(S/'PICTURE_V04.json').write_text(json.dumps(dict(status='ASSEMBLED_FULL_DECODE_AND_BOUNDARIES_PENDING',frames=int(v['nb_frames']),duration_s=v['duration'],sha256=d,parts=[str(p) for p in parts]),indent=2)+'\n')
print(v['nb_frames'],v['duration'],d,flush=True)
