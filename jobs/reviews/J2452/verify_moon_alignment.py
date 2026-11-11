#!/usr/bin/env python3
"""Dense read-only Moon alignment validation against the finished master.
No offset is interpolated across a source-part change. Windows with poor SNR
are reported, not silently counted as matches. Run in the J2452 ASR venv.
"""
import json,subprocess
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
j=json.loads((HERE/'alignment_v02/013_alignment.json').read_text())
def dec(p):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',p,'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32).astype(float)
m=dec(j['master']);out=[]
for src,offset in zip(j['narration'],[.02625,95.33875,240.133,382.82675]):
 x=dec(src); checks=[]
 for t in np.arange(1,len(x)/8000-2,3):
  s=round(t*8000);k=round((t+offset)*8000);q=x[s:s+16000];v=m[k:k+16000]
  q-=q.mean();v-=v.mean();den=np.linalg.norm(q)*np.linalg.norm(v)
  corr=float(np.dot(q,v)/den) if den>1e-8 else None
  checks.append(dict(source_s=float(t),master_s=float(t+offset),correlation=corr))
 out.append(dict(source=src,offset_s=offset,checks=checks))
p=Path('/Users/ben/_desk/J2452-sleep-scratch/moon_dense_alignment_v01.json');p.write_text(json.dumps(out,indent=2)+'\n')
for r in out: print(Path(r['source']).name,len(r['checks']),min((c['correlation'] for c in r['checks'] if c['correlation'] is not None),default=0))
