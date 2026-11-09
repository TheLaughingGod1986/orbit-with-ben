#!/usr/bin/env python3
"""Technical evidence for the R35 draft; no picture or motion approval."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image
import ocean_graphic as g


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',type=Path,required=True)
    a=ap.parse_args();m=json.loads(a.manifest.read_text())
    assert g.sha(g.SOURCE)==m['source_sha256']
    assert g.sha(m['preview'])==m['preview_sha256']
    with Image.open(m['preview']) as im:
        assert im.convert('RGBA').tobytes()==g.frame(2).tobytes()
    assert g.photo().width <= g.CROP[2]-g.CROP[0]
    assert all(len(s.replace('·','').split())<=4 for s in g.LABELS)
    checks=[]
    for i in range(109):
        f=g.frame(i/30);box=f.getchannel('A').getbbox()
        assert box is None or (96<=box[0]<box[2]<=1824 and 54<=box[1]<box[3]<=1026)
        checks.append(dict(frame=i,alpha_bounds=box,build_progress=g.progress(i/30)))
    assert checks[0]['alpha_bounds'] is None and checks[-1]['alpha_bounds'] is None
    assert all(x['build_progress']<=y['build_progress'] for x,y in zip(checks,checks[1:]))
    assert g.frame(.8).tobytes()!=g.frame(1.4).tobytes()
    p=subprocess.run([sys.executable,g.__file__,'--out',str(a.manifest.parent),'--render'],capture_output=True,text=True)
    assert p.returncode==2 and 'individual still review' in p.stderr
    result=dict(job='J2089',status='MEASUREMENTS_ONLY',source_hash='MATCH',preview_hash='MATCH',
        preview_reproduced=True,source_upscale=480/510,labels_at_most_four_words=True,
        transparent_entry_exit=True,changing_frames=True,render_guard='REJECTED_DRAFT',frames=checks,
        not_verified=['Scientific/editorial acceptance of schematic','Source reuse allocation',
                      'Final moving plate, contrast and timing','Audio or moving-video perception'])
    (a.manifest.parent/'OCEAN_CHECKS_v01.json').write_text(json.dumps(result,indent=2)+'\n')
    print('109 layouts; source/preview hashes; exact preview; no upscale; label bounds; alpha entry/exit; changing frames; draft render rejection verified.')


if __name__=='__main__':main()
