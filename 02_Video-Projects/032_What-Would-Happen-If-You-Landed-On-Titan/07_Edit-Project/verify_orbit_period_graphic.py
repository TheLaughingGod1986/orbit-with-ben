#!/usr/bin/env python3
"""Reproduce R08 source/preview/layout measurements. No review verdict."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
import orbit_period_graphic as g


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',type=Path,required=True)
    a=ap.parse_args();m=json.loads(a.manifest.read_text())
    assert g.sha(g.SOURCE)==m['source_sha256']
    assert g.sha(m['preview'])==m['preview_sha256']
    from PIL import Image
    with Image.open(m['preview']) as im:
        assert im.convert('RGBA').tobytes()==g.frame(2.4).tobytes()
    assert all(a<=b for a,b in zip(g.photo().size,Image.open(g.SOURCE).size))
    checks=[]
    for j in range(109):
        t=j/30;box=g.frame(t).getchannel('A').getbbox()
        assert box is None or (96<=box[0]<box[2]<=1824 and 54<=box[1]<box[3]<=1026)
        checks.append(dict(frame=j,alpha_bounds=box,progress=g.progress(t)))
    assert checks[0]['alpha_bounds'] is None and checks[-1]['alpha_bounds'] is None
    assert all(a['progress']<=b['progress'] for a,b in zip(checks,checks[1:]))
    assert g.progress(.4)==0 and g.progress(2.4)==1
    assert g.frame(.8).tobytes()!=g.frame(1.5).tobytes()
    guard=subprocess.run([sys.executable,str(Path(g.__file__)),'--out',str(a.manifest.parent),'--render'],capture_output=True,text=True)
    assert guard.returncode==2 and 'approval under J2262' in guard.stderr
    out=dict(job='J2089',status='MEASUREMENTS_ONLY',source_hash='MATCH',preview_hash='MATCH',
        preview_reproduced=True,source_not_upscaled=True,render_guard='REJECTED_WITHOUT_J2262',
        entry_exit_alpha='ZERO',changing_frames=True,frames=checks,
        not_verified=['Reviewer acceptance of period-dial interpretation','Final composite and source reuse allocation','Moving-video/audio perception'])
    (a.manifest.parent/'ORBIT_PERIOD_CHECKS_v01.json').write_text(json.dumps(out,indent=2)+'\n')
    print('109 layouts, monotonic full dial, alpha, source/preview hashes, exact preview reproduction and draft render guard verified.')

if __name__=='__main__':main()
