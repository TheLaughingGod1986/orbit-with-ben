#!/usr/bin/env python3
"""Read back saved repair/join frames, geometry, timestamp clock and hashes."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from build_orion_source_repair import sha,run
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
r=json.loads((a.out/'REPORT.json').read_text());v=Path(r['output']);assert sha(v)==r['sha256']
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_frames','-show_entries','frame=best_effort_timestamp_time,width,height','-of','json',str(v)]))['frames']
frames=r['frames'];assert len(info)==frames
assert all(x['width']==1920 and x['height']==1080 and abs(float(x['best_effort_timestamp_time'])-i/30)<.00002 for i,x in enumerate(info))
def rgb(path,start,frames):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-ss',str(start),'-i',str(path),'-frames:v',str(frames),'-vf','scale=320:180,format=rgb24','-f','rawvideo','-']),np.uint8).reshape(-1,180,320,3)
start=432.5 if frames==14829 else 2
b=rgb(v,start,198);c=rgb(r['repair']['output'],0,198);err=np.abs(b.astype(float)-c.astype(float)).mean(axis=(1,2,3));assert len(err)==198 and err.max()<2,err.max()
readback=dict(status='SAVED_JOIN_CHECK_ONLY_NOT_COMPILATION_PASS',sha256=sha(v),frames=frames,clock='constant 30 fps, every frame checked',opaque_frames_checked=198,max_rgb_mae=float(err.max()),threshold=2,source_repair_sha256=sha(Path(r['repair']['output'])))
(a.out/'READBACK.json').write_text(json.dumps(readback,indent=2)+'\n')
s=Image.new('RGB',(1440,870),(25,25,25));d=ImageDraw.Draw(s)
for i,t in enumerate([0,.5,1,2,5.3,8.566667,9.1,10.1,10.566667]):
 t+=430.5 if frames==14829 else 0
 pix=rgb(v,t,1)[0];im=Image.fromarray(pix).resize((480,270));s.paste(im,((i%3)*480,(i//3)*290+20));d.text(((i%3)*480+5,(i//3)*290+3),str(t),fill='white')
s.save(a.out/'SHEET.jpg');print(readback)
