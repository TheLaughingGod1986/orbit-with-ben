#!/usr/bin/env python3
"""Independent frame-clock and replacement coverage readback; no visual approval."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from build_orion_source_repair import sha
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();r=json.loads((a.directory/'REPORT.json').read_text())
assert sha(Path(r['output']))==r['sha256'] and sha(Path(r['source']))==r['source_sha256']
def seq(path,t,n):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v',str(n),'-vf','scale=320:180','-pix_fmt','rgb24','-f','rawvideo','-'])
 return np.frombuffer(b,np.uint8).reshape(n,180,320,3)
replacements=[]
for p in r['patches']:
 lo,hi=p['frames'];actual=seq(r['output'],lo/30,hi-lo).astype(float);expected=seq(p['dissolved'],0,hi-lo).astype(float);errs=np.abs(actual-expected).mean(axis=(1,2,3));assert errs.max()<2,float(errs.max());replacements.append(dict(plate_id=p['plate_id'],frames=hi-lo,maximum_frame_error=float(errs.max())))
rows=[]
for t in [5,100,250,400,471,477,490]:
 e=float(np.abs(seq(r['output'],t,1).astype(float)-seq(r['base'],t,1).astype(float)).mean());assert e<1.5,(t,e);rows.append(dict(time_s=t,mean_error=e))
frames=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',r['output']]))['frames'];assert len(frames)==14829 and all(abs(float(f['best_effort_timestamp_time'])-i/30)<.00002 for i,f in enumerate(frames))
sheet=Image.new('RGB',(960,600),(30,30,30));d=ImageDraw.Draw(sheet)
for i,t in enumerate([357.2,357.7,360,364.9,432,434.5,438.5]):
 x=i%3*320;y=i//3*200;sheet.paste(Image.fromarray(seq(r['output'],t,1)[0]),(x,y+20));d.text((x,y),str(t),fill='white')
sheet.save(a.directory/'READBACK_SHEET.jpg')
o=dict(status='CLOCK_AND_REPLACEMENT_READBACK_PASS',frames=len(frames),replacements=replacements,unchanged_samples=rows,sha256=r['sha256'],limitations=['Replacement compared every frame at 320x180; seven sparse samples elsewhere.','Not listening or moving-picture review; normal QA remains authoritative.']);(a.directory/'READBACK.json').write_text(json.dumps(o,indent=2)+'\n');print(json.dumps(o,indent=2))
