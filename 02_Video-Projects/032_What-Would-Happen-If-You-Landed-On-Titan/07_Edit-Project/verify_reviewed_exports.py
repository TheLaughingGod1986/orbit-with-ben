#!/usr/bin/env python3
"""Verify J2177/J2247/J2264 exports against reviewed stills and decoded pixels.

Measurements only: no assertion of perceived motion, composite quality or KEEP.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import mechanism_graphics as mechanism
import size_graphic as size
import ocean_graphic as ocean
import orbit_period_graphic as orbit_period
import distance_graphic as distance
import pebble_ruler_graphic as pebble_ruler
import landing_record_graphic as landing_record

HERE = Path(__file__).resolve().parent
CACHE = Path('/Users/benjaminoats/_desk/cache/J2089')
ROOT = HERE.parents[2]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--review-root', type=Path, default=ROOT)
    ap.add_argument('--only', choices=['orbit_period','distance','pebble_ruler','landing_record'])
    ap.add_argument('--output', type=Path, default=HERE/'REVIEWED_EXPORTS_VERIFICATION_v01.json')
    args = ap.parse_args()
    manifest = json.loads((CACHE/'mechanism_renders_v01/MECHANISM_MANIFEST_v01.json').read_text())
    records = [(r, lambda t, s=r: mechanism.frame(s,t), 'J2177')
               for r in manifest['clips'] if r['rendered']]
    for name, module, review in [('size',size,'J2247'),('ocean',ocean,'J2264'),('orbit_period',orbit_period,'J2262'),('distance',distance,'J2260'),('pebble_ruler',pebble_ruler,'J2296'),('landing_record',landing_record,'J2304')]:
        r = json.loads((CACHE/f'{name}_renders_v01/{name.upper()}_MANIFEST_v01.json').read_text())
        records.append((r,module.frame,review))
    assert len(records) == 21
    if args.only:
        records = [r for r in records if r[0]['id'] == {'orbit_period':'r08_orbit_period','distance':'r19_distance','pebble_ruler':'r18_ruler','landing_record':'r23_landing_record'}[args.only]]
        assert len(records) == 1
    results = []
    for r, frame, review in records:
        review_text = (args.review_root/f'jobs/reviews/{review}/REVIEW.md').read_text()
        assert r['review_ref'] == review
        assert r['preview_sha256'] == sha(r['preview'])
        assert r['preview_sha256'] in review_text, f"Preview is not the reviewed version: {r['id']}"
        assert sha(r['render']) == r['sha256']
        # Preserve each source photo and the reviewed crop implementation.
        for asset in r.get('assets',[]):
            assert sha(asset['path']) == asset['sha256']
        if 'source_sha256' in r:
            assert sha(r['source']) == r['source_sha256']
        probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
            '-show_entries','stream=width,height,pix_fmt,nb_frames,r_frame_rate,codec_name:format=duration',
            '-of','json',r['render']]))
        stream = probe['streams'][0]
        assert (stream['width'],stream['height'],stream['pix_fmt'],stream['codec_name'],
                int(stream['nb_frames']),stream['r_frame_rate']) == (1920,1080,'argb','qtrle',108,'30/1')
        assert abs(float(probe['format']['duration'])-3.6) < .001
        proc = subprocess.Popen(['ffmpeg','-v','error','-i',r['render'],'-f','rawvideo',
                                 '-pix_fmt','rgba','pipe:1'],stdout=subprocess.PIPE)
        try:
            for i in range(108):
                expected = frame(i/30).tobytes()
                actual = proc.stdout.read(len(expected))
                assert actual == expected, (r['id'], i, 'Decoded pixels differ from reviewed generator')
            assert not proc.stdout.read(1)
            assert proc.wait() == 0
        finally:
            proc.stdout.close()
            if proc.poll() is None:
                proc.kill()
                proc.wait()
        results.append(dict(id=r['id'],review_ref=review,render=r['render'],sha256=r['sha256'],
            reviewed_preview_sha256=r['preview_sha256'],decoded_exact_frames=108,
            width=1920,height=1080,duration=3.6,fps=30,pixel_format='argb'))
        print(r['id'], '108 exact decoded frames', flush=True)
    output = dict(job='J2089',status='MEASUREMENTS_ONLY_NOT_COMPOSITE_APPROVAL',exports=results,
        unverified=['Perceived motion/audio','Composite contrast and subject placement',
                    'Final source reuse, footage rights and frame0','Final film gates'])
    args.output.write_text(json.dumps(output,indent=2)+'\n')


if __name__ == '__main__':
    main()
