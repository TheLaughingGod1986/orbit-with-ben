#!/usr/bin/env python3
"""Independent saved-file timing/source read-back for the bounded sky repair."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from build_orion_source_repair import sha
p=argparse.ArgumentParser();p.add_argument('repair',type=Path);a=p.parse_args();r=json.loads((a.repair/'REPORT.json').read_text())
assert sha(Path(r['output']))==r['sha256'] and sha(Path(r['source']))==r['source_sha256']
def frame(path,t,grade=False):
 vf=('colorchannelmixer=rr=.85:gg=.85:bb=.85,limiter=min=16:max=180:planes=1,' if grade else '')+'crop=1920:980:0:0,scale=480:245,format=gray'
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf',vf,'-f','rawvideo','-'])
 return np.frombuffer(b,dtype=np.uint8).astype(float)
rows=[]
for t in [1.2,3,5]:
 actual=frame(r['replacement'],t);expected=frame(r['source'],10.2+t,True)
 mae=float(np.abs(actual-expected).mean());corr=float(np.corrcoef(actual,expected)[0,1]);assert mae<3 and corr>.98,(t,mae,corr)
 rows.append(dict(replacement_s=t,source_s=10.2+t,mean_absolute_error=mae,correlation=corr))
report=dict(status='SPARSE_SOURCE_INTERVAL_READBACK_PASS',samples=rows,source_sha256=r['source_sha256'],replacement_sha256=r['replacement_sha256'],output_sha256=r['sha256'],limitations=['Three spatial samples, not an every-frame or moving-video review.','Credit strip excluded from source comparison; credit checked against SOURCE_POOL_v03.'])
(a.repair/'READBACK.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
