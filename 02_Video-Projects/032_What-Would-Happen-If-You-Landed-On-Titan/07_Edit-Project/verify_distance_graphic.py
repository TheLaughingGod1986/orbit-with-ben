"""Reproduce R19 hashes, exact bar ratio, safe area and alpha; no motion verdict."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
import distance_graphic as g

ap=argparse.ArgumentParser()
ap.add_argument('--manifest',type=Path,required=True)
ap.add_argument('--out',type=Path,required=True)
a=ap.parse_args()
m=json.loads(a.manifest.read_text())
assert g.sha(m['source'])==m['source_sha256']
assert g.sha(m['preview'])==m['preview_sha256']
samples=[]
for i in range(109):
    t=i/30
    box=g.frame(t).getchannel('A').getbbox()
    if i in (0,108): assert box is None
    else:
        assert box and box[0]>=95 and box[1]>=54 and box[2]<=1825 and box[3]<=1026
    widths=g.widths(t)
    if widths[0]: assert abs(widths[1]/widths[0]-9.5)<1e-10
    samples.append(dict(frame=i,bbox=box,widths=widths))
assert g.frame(.7).tobytes()!=g.frame(2.4).tobytes()
assert g.widths(2.4)==[900/9.5,900]
probe=subprocess.run([sys.executable,g.__file__,'--render','--out','/private/tmp/J2089-distance-rejected'],capture_output=True,text=True)
assert probe.returncode==2 and 'approval under J2260' in probe.stderr
a.out.write_text(json.dumps(dict(job='J2089',status='MEASUREMENTS_ONLY',
    frames=samples,verified_frame_count=109,source_hash='MATCH',preview_hash='MATCH',
    ratio=9.5,upscale=460/(g.CROP[2]-g.CROP[0]),unapproved_render_exit=probe.returncode,
    motion_perception=False,remaining=['Individual still review','Source reuse allocation','Composite and final gates']),indent=2)+'\n')
print('109 layouts, common 9.5 ratio, clear alpha endpoints, hashes and render rejection verified.')
