"""Reproduce draft layout and protect earlier exports; no media-review verdict."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image
import landing_record_graphic as g

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    a = ap.parse_args()
    subprocess.run([sys.executable, g.__file__, '--out', str(a.out)], check=True)
    boxes = []
    for i in range(109):
        box = g.frame(i/30).getchannel('A').getbbox()
        if box:
            assert 96 <= box[0] < box[2] <= 1824, (i,box)
            assert 54 <= box[1] < box[3] <= 1026, (i,box)
            boxes.append(box)
    assert g.frame(0).getbbox() is None
    assert g.frame(3.6).getbbox() is None
    assert g.frame(.8).tobytes() != g.frame(1.8).tobytes()
    assert g.sha(g.SOURCE) == g.SOURCE_HASH
    m = json.loads((a.out/'LANDING_RECORD_MANIFEST_v01.json').read_text())
    assert g.sha(m['preview']) == m['preview_sha256']
    with Image.open(m['preview']) as im:
        assert im.tobytes() == g.frame(2.4).tobytes()
    for label in m['labels']:
        assert len(label.split()) <= 4
    rejected = a.out/'rejected_export'
    result = subprocess.run([sys.executable,g.__file__,'--out',str(rejected),'--render'],capture_output=True)
    assert result.returncode == 2 and not rejected.exists()
    here = Path(__file__).resolve().parent
    old = json.loads((here/'J2089_EXPORT_HASHES_v20.json').read_text())['exports']
    for path, expected in old.items():
        assert g.sha(path) == expected, path
    (here/'LANDING_RECORD_MANIFEST_v01.json').write_text(json.dumps(m,indent=2)+'\n')
    checks = dict(job='J2089',status='MEASUREMENTS_ONLY_DRAFT_NOT_APPROVAL',
        sampled_frames=109,all_alpha_bounds_inside_5_percent=True,
        entry_exit_alpha_zero=True,changing_connector=True,preview_exact_pixels='MATCH',
        source_and_preview_hashes='MATCH',source_upscale=1.0,
        labels_at_most_four_words=True,unapproved_export_exit=2,
        preserved_exports=len(old),all_preserved_export_hashes='MATCH',
        not_verified=['Shot-list alternative and source allocation approval',
          'Per-asset rights and final reuse count','Graded moving composite, subject placement and contrast',
          'Actual moving-image/audio perception','Final picture and polish gates'])
    (here/'LANDING_RECORD_CHECKS_v01.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(f'109 planned layouts, alpha, hashes, exact preview pixels and export guard checked; {len(old)} prior export hashes unchanged. Draft only.')

if __name__ == '__main__':
    main()
