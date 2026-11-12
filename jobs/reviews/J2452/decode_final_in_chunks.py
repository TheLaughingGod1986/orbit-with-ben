#!/usr/bin/env python3
"""Resume exact 60-second decode coverage with a bounded worker runtime.

Each successful block is checkpointed. A partial/interrupted block is never
credited. No process remains running when this command exits.
"""
import argparse,json,subprocess as sp,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--scratch',type=Path,required=True);p.add_argument('--seconds-budget',type=int,default=300);a=p.parse_args();s=a.scratch/'final_join_v01'
source=s/'sleep_picture_candidate_v04.mp4';identity=json.loads((s/'PICTURE_V04.json').read_text());record=s/'FINAL_DECODE_BLOCKS_V04.json'
r=json.loads(record.read_text()) if record.exists() else dict(status='PARTIAL',picture_sha256=identity['sha256'],expected_frames=195070,blocks=[])
assert r['picture_sha256']==identity['sha256'];deadline=time.monotonic()+a.seconds_budget
for first in range(0,195070,1800):
 count=min(1800,195070-first)
 if any(b['first_frame']==first for b in r['blocks']):continue
 if time.monotonic()+45>deadline:break
 log=s/f'decode_v04_{first:06d}.log';progress=s/f'decode_v04_{first:06d}.progress'
 with log.open('w') as f:
  try:
   x=sp.run(['ffmpeg','-v','error','-xerror','-nostdin','-threads','4','-ss',str(first/30),'-i',str(source),'-map','0:v','-frames:v',str(count),'-f','null','-','-progress',str(progress)],stdout=f,stderr=sp.STDOUT,timeout=max(1,deadline-time.monotonic()))
  except sp.TimeoutExpired:print('Stopped at budget; incomplete block not credited',flush=True);break
 text=progress.read_text();values=dict(line.split('=',1) for line in text.splitlines() if '=' in line)
 ok=x.returncode==0 and int(values.get('frame',0))==count and values.get('progress')=='end' and log.stat().st_size==0
 if not ok:raise RuntimeError(f'Decode failed at frame {first}; see {log}')
 r['blocks'].append(dict(first_frame=first,frames=count,exit_code=0));r['decoded_frames']=sum(b['frames'] for b in r['blocks']);r['status']='PASS' if r['decoded_frames']==195070 else 'PARTIAL';record.write_text(json.dumps(r,indent=2)+'\n');print(first,count,r['decoded_frames'],flush=True)
