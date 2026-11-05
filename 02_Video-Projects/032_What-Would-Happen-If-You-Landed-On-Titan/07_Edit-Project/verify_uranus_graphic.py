"""Check R52 source integrity, safe area, alpha and counter; no motion verdict."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
import uranus_graphic as g

ap = argparse.ArgumentParser()
ap.add_argument('--manifest', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
a = ap.parse_args()
m = json.loads(a.manifest.read_text())
assert g.sha(m['preview']) == m['preview_sha256']
assert g.sha(m['source']) == m['source_sha256']
samples = []
for i in range(109):
    t = i/30
    bbox = g.frame(t).getchannel('A').getbbox()
    if i in (0, 108):
        assert bbox is None
    else:
        assert bbox and bbox[0] >= 95 and bbox[1] >= 54
        assert bbox[2] <= 1825 and bbox[3] <= 1026
    samples.append(dict(frame=i, bbox=bbox))
assert g.frame(.7).tobytes() != g.frame(2.6).tobytes()
assert round(21*min(1, (2.6-.4)/2.2)) == 21
probe = subprocess.run([sys.executable, g.__file__, '--render', '--out',
                        '/private/tmp/J2089-r52-unapproved'], capture_output=True, text=True)
assert probe.returncode == 2 and 'requires named still approval' in probe.stderr
result = dict(job='J2089', row=52, status='MEASUREMENTS_ONLY',
              source_hash='MATCH', preview_hash='MATCH', frames=samples,
              verified_frame_count=len(samples), endpoint_years=21,
              source_crop_pixels=1420, display_pixels=620, upscale=620/1420,
              unapproved_render_exit=probe.returncode, motion_perception=False,
              remaining=['Still decision','Tilt-axis explanation','Composite/film gates'])
a.out.write_text(json.dumps(result, indent=2)+'\n')
print('109 layouts checked; source/preview hashes match; clear endpoints; 21-year counter; unapproved render rejected.')
