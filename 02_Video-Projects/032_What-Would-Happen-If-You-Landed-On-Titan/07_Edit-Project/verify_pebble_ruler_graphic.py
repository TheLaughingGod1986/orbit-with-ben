"""Measure draft registration/layout; no visual/motion approval."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageChops
import pebble_ruler_graphic as g
out=Path('/Users/benjaminoats/_desk/cache/J2089/pebble_ruler_previews_v03')
subprocess.run([sys.executable,str(Path(g.__file__)),'--out',str(out)],check=True)
boxes=[]
for i in range(109):
    t=i/30
    f=g.frame(t)
    box=f.getchannel('A').getbbox()
    if box:
        assert box[0]>=96 and box[1]>=54 and box[2]<=1824 and box[3]<=1026, (i,box)
        boxes.append(box)
assert g.frame(0).getbbox() is None and g.frame(3.6).getbbox() is None
assert ImageChops.difference(g.frame(.8).convert("RGB"),g.frame(1.8).convert("RGB")).getbbox()
assert g.sha(g.SOURCE)==g.SOURCE_HASH
assert max(g.DISPLAY[0]/314,g.DISPLAY[1]/629)<1.44
for x,y in g.ENDPOINTS:
    assert g.CROP[0]<=x<g.CROP[2] and g.CROP[1]<=y<g.CROP[3]
m=json.loads((out/'PEBBLE_RULER_MANIFEST_v01.json').read_text())
assert g.sha(m['preview'])==m['preview_sha256']
with Image.open(m['preview']) as im:
    assert im.tobytes()==g.frame(2.4).tobytes()
probe=out/'rejected_render'
r=subprocess.run([sys.executable,str(Path(g.__file__)),'--out',str(probe),'--render'],capture_output=True)
assert r.returncode==2 and not probe.exists()
here=Path(__file__).resolve().parent
(here/'PEBBLE_RULER_MANIFEST_v01.json').write_text(json.dumps(m,indent=2)+'\n')
(here/'PEBBLE_RULER_CHECKS_v01.json').write_text(json.dumps(dict(job='J2089',status='MEASUREMENTS_ONLY',sampled_frames=109,all_bounds_inside_5_percent=True,entry_exit_alpha_zero=True,changing_bracket=True,source_and_preview_hashes='MATCH',preview_exact_pixels='MATCH',upscale=m['max_upscale'],render_guard_exit=2,source_endpoints=g.ENDPOINTS,not_verified=['Endpoint identity/registration approval','Rights/reuse clearance','Moving composite and motion/audio input','Final picture/polish gates']),indent=2)+'\n')
print('109 layout samples, source/preview hashes, exact preview pixels, alpha and render guard verified; draft only.')
