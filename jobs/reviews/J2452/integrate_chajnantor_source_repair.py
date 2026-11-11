#!/usr/bin/env python3
"""Verify saved join pixels, then retain a new unapproved picture checkpoint."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from build_orion_source_repair import sha,run
p=argparse.ArgumentParser();p.add_argument('--join',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
r=json.loads((a.join/'REPORT.json').read_text());source=Path(r['source']);patch=Path(r['output']);component=Path(r['repair']['output'])
assert sha(source)==r['source_sha256'] and sha(patch)==r['sha256'] and sha(component)==r['repair']['sha256']
assert json.loads((a.join/'POLISH_GATE.json').read_text())['verdict']=='PASS'
def pixels(path,start,count):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(start),'-i',str(path),'-frames:v',str(count),'-vf','scale=320:180','-pix_fmt','rgb24','-f','rawvideo','-'])
 return np.frombuffer(raw,dtype=np.uint8).reshape(count,180,320,3).astype(np.float32)
lo,hi=r['chapter_frames'];start,end=r['opaque_frames'];count=end-start
err=np.abs(pixels(patch,2,count)-pixels(component,0,count)).mean(axis=(1,2,3))
assert float(err.max())<2,float(err.max())
a.out.mkdir(parents=True,exist_ok=False)
encode=['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','6','-r','30','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000']
prefix=a.out/'prefix.mp4';suffix=a.out/'suffix.mp4'
run(['-i',str(source),'-frames:v',str(lo),*encode,str(prefix)])
run(['-ss',str(hi/30),'-i',str(source),'-frames:v',str(14829-hi),*encode,str(suffix)])
listing=a.out/'concat.txt';listing.write_text(''.join("file '"+str(x)+"'\n" for x in [prefix,patch,suffix]))
out=a.out/'029_picture_chajnantor_repaired.mp4'
run(['-f','concat','-safe','0','-i',str(listing),'-c','copy',str(out)])
run(['-i',str(out),'-f','null','-'])
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(out)]))['streams'][0]
assert int(info['nb_read_frames'])==14829
err2=np.abs(pixels(out,start/30,count)-pixels(component,0,count)).mean(axis=(1,2,3))
assert float(err2.max())<2,float(err2.max())
cuts=json.loads((source.parent/'cuts.json').read_text())
for c in cuts:
 if c['plate_id']=='r24_superk':
  c.update(sleep_repair=str(component),framing=dict(offset=3.25),upscale=1.5,overlays=[])
(a.out/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
report=dict(status='PICTURE_CHECKPOINT_NOT_FULL_QA_OR_UAT',source=str(source),source_sha256=sha(source),join=r,output=str(out),sha256=sha(out),frames=14829,duration_s=494.3,opaque_readback=dict(frames=count,join_max_mae=float(err.max()),chapter_max_mae=float(err2.max()),threshold=2),limitations=['Other dark spans and diagram replacements remain.','Final compilation, sound and NAS delivery remain.'])
(a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
print(out)
