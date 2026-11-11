#!/usr/bin/env python3
"""Integrate the checked closing interval, retaining the full chapter clock."""
import argparse,json,subprocess
from pathlib import Path
from build_orion_source_repair import sha,run
p=argparse.ArgumentParser();p.add_argument('--repair',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
r=json.loads((a.repair/'REPORT.json').read_text());base=Path(r['base']);patch=Path(r['output'])
assert sha(base)==r['base_sha256'] and sha(patch)==r['sha256']
assert json.loads((a.repair/'POLISH_GATE_CORRECTED.json').read_text())['verdict']=='PASS'
a.out.mkdir(parents=True,exist_ok=False)
lo,hi=r['chapter_replace_frames'];prefix=a.out/'prefix.mp4'
run(['-i',str(base),'-frames:v',str(lo),'-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','6','-r','30','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000',str(prefix)])
listing=a.out/'concat.txt';listing.write_text(''.join("file '"+str(x)+"'\n" for x in [prefix,patch]))
output=a.out/'029_picture_closing_repaired.mp4';run(['-f','concat','-safe','0','-i',str(listing),'-c','copy',str(output)]);run(['-i',str(output),'-f','null','-'])
s=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(output)]))['streams'][0];assert int(s['nb_read_frames'])==hi==14829
cuts=json.loads((a.repair/'chapter_cuts.json').read_text());(a.out/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
report=dict(status='CLOSING_REPAIR_INTEGRATED_NOT_FINAL_QA_OR_UAT',output=str(output),sha256=sha(output),frames=hi,duration_s=hi/30,repair=r,prefix_sha256=sha(prefix),limitations=['Normal whole-chapter pixel and source QA still required.','Twelve other reuse failures and original graphics remain.','Other chapters, final mux, NAS master/reel and UAT remain.'])
(a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(output)
