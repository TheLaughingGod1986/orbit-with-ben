#!/usr/bin/env python3
"""Read back saved mix against narration at three windows per chapter."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from build_sleep_bed import digest
p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();r=json.loads(a.report.read_text());rows=[]
def samples(path,start):
    b=subprocess.check_output(['ffmpeg','-v','error','-nostdin','-ss',str(start),'-i',str(path),'-t','4','-ac','1','-ar','4000','-f','f32le','-'])
    return np.frombuffer(b,dtype='<f4').astype(float)
assert digest(r['output'])==r['sha256']
for c in r['chapters']:
    for offset in [5,c['narration_end_s']/2-c['start_s']/2,c['narration_end_s']-c['start_s']-8]:
        x=samples(c['narration'],offset);y=samples(r['output'],c['start_s']+offset);n=min(len(x),len(y));x=x[:n];y=y[:n]
        rms=float(np.sqrt(np.mean(x*x)));corr=float(np.corrcoef(x,y)[0,1])
        assert rms>1e-4,(c['film'],offset,'silent verification window')
        assert corr>.85,(c['film'],offset,corr)
        rows.append(dict(film=c['film'],chapter_offset_s=offset,mix_time_s=c['start_s']+offset,window_s=4,correlation=corr,narration_rms=rms))
a.out.write_text(json.dumps(dict(status='HASH_AND_39_WINDOW_PLACEMENT_READBACK_PASS',mix=r['output'],sha256=r['sha256'],windows=rows,limitations='Sparse waveform checks verify placement, not a listening review or every-sample QA. Final AV/AAC checks pending.'),indent=2)+'\n');print(len(rows),'placement windows PASS')
