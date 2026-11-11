#!/usr/bin/env python3
"""Integrate the checked ten-second repair without altering chapter duration."""
import argparse,json,subprocess
from pathlib import Path
from build_orion_source_repair import sha,run
p=argparse.ArgumentParser();p.add_argument('--join',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
r=json.loads((a.join/'REPORT.json').read_text());source=Path(r['source']);patch=Path(r['output'])
assert sha(source)==r['source_sha256'] and sha(patch)==r['sha256']
assert json.loads((a.join/'POLISH_GATE_CORRECTED.json').read_text())['verdict']=='PASS'
a.out.mkdir(parents=True,exist_ok=False)
encode=['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','6','-r','30','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000']
prefix=a.out/'prefix.mp4';suffix=a.out/'suffix.mp4'
run(['-i',str(source),'-frames:v','12915',*encode,str(prefix)])
print('prefix saved',flush=True)
run(['-ss','441.1','-i',str(source),'-frames:v','1596',*encode,str(suffix)])
listing=a.out/'concat.txt';listing.write_text(''.join("file '"+str(x)+"'\n" for x in [prefix,patch,suffix]))
out=a.out/'029_picture_orion_repaired.mp4';run(['-f','concat','-safe','0','-i',str(listing),'-c','copy',str(out)])
run(['-i',str(out),'-f','null','-'])
report=dict(status='ONE_SOURCE_REPAIR_INTEGRATED_SIX_DARK_FAILURES_AND_OTHER_WORK_REMAIN',source=str(source),source_sha256=sha(source),patch=str(patch),patch_sha256=sha(patch),repair=r['repair'],output=str(out),sha256=sha(out),frames=14829,duration_s=494.3,chapter_range_s=[430.5,441.1],opaque_range_s=[432.5,439.1],pieces=[dict(path=str(x),sha256=sha(x)) for x in [prefix,patch,suffix]],limitations=['No narration or timing change.','Not final picture QA; six dark source spans, graphics, reuse, titles, other chapters and final assembly remain.'])
(a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
root=Path(__file__).resolve().parent
cuts=json.loads((root/'betelgeuse_chapter_source_map_v01.json').read_text())
for c in cuts:
 if c['plate_id']=='r36_orion_b':
  c['previous_source']=c['source'];c.update(source='orion_rise_vlt.mp4',framing=dict(offset=0),upscale=1,credit='ESO/B. Tafreshi (twanight.org) · CC BY 4.0',sleep_repair=r['repair']['output'])
(a.out/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n');print(out,flush=True)
