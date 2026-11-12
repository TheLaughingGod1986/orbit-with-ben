#!/usr/bin/env python3
"""Normal pixel/source QA across compilation joins and both adjoining seconds."""
import json,subprocess as sp,sys
from pathlib import Path
S=(Path.home()/'_desk/J2452-sleep-scratch/final_join_v01');T=json.loads((S/'TIMELINE.json').read_text());R=[]
for i,c in enumerate(T['chapters'][:-1]):
 if i==1:
  r=json.loads((S/'SATURN_EXIT_REPAIR_V04.json').read_text());R.append(dict(join=2,exit_code=r['gate_exit'],report=r['gate']));continue
 q=S/f'boundary_qa_v04_{i+1:02d}';q.mkdir(exist_ok=True);v=q/'neighborhood.mp4';n=T['chapters'][i+1];j=S/f'join_endpoint_v02_{i+1:02d}.mp4'
 if not v.exists():
  g='[0:v]trim=duration=3,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[2:v]trim=duration=3,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]'
  sp.run(['ffmpeg','-v','error','-nostdin','-n','-ss',str(c['duration_s']-3),'-i',c['path'],'-i',str(j),'-i',n['path'],'-filter_complex_threads','1','-filter_complex',g,'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4',str(v)],check=True,timeout=90)
 cuts=[dict(row=f'join-{i+1}-{k}',timeline_in=k/2,timeline_out=(k+1)/2,source=f'boundary-{i+1}',framing=dict(offset=k/2),src_w=1920,upscale=1) for k in range(20)]
 (q/'cuts.json').write_text(json.dumps(cuts));(q/'pool.json').write_text(json.dumps([dict(source=f'boundary-{i+1}',title='Public-film endpoints and compilation dissolve')]))
 with (q/'gate.log').open('w') as f:
  code=sp.run([sys.executable,'scripts/picture_qa.py',str(v),'--cuts',str(q/'cuts.json'),'--pool',str(q/'pool.json'),'--out-dir',str(q)],stdout=f,stderr=sp.STDOUT,timeout=120).returncode
 R.append(dict(join=i+1,exit_code=code,report=str(q/'picture_qa.json')));print(i+1,code,flush=True)
 (S/'BOUNDARY_GATES_V04.json').write_text(json.dumps(dict(status='PASS' if len(R)==12 and all(r['exit_code']==0 for r in R) else 'INCOMPLETE_OR_FAIL',joins=R),indent=2)+'\n')
