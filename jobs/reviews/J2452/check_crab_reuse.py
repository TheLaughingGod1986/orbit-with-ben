#!/usr/bin/env python3
"""Read back the saved repair independently; no perceptual approval claim."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from build_orion_source_repair import sha
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();r=json.loads((a.directory/'REPORT.json').read_text())
assert sha(Path(r['output']))==r['sha256'] and sha(Path(r['source']))==r['source_sha256']
def frame(path,t):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf','scale=480:270','-pix_fmt','rgb24','-f','rawvideo','-'])
 return np.frombuffer(b,np.uint8).reshape(270,480,3)
lo,hi=r['chapter_replace_frames'];rows=[];images=[]
for t in [5,100,250,329,340,440,490]:
 actual=frame(r['output'],t);expected=frame(r['base'],t);mae=float(np.abs(actual.astype(float)-expected).mean());assert mae<1.5,(t,mae)
 rows.append(dict(chapter_s=t,comparison='unchanged base',mean_absolute_error=mae))
for t in [2.2,5.5,8.5]:
 actual=frame(r['output'],lo/30+t);expected=frame(r['patch'],t);mae=float(np.abs(actual.astype(float)-expected).mean());assert mae<1.5,(t,mae)
 rows.append(dict(chapter_s=lo/30+t,comparison='opaque replacement',mean_absolute_error=mae))
for t in [421.4,421.6,422.0,427,432.0,432.4,432.6]:images.append((t,frame(r['output'],t)))
sheet=Image.new('RGB',(1440,600),(30,30,30));d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(images):
 x=i%3*480;y=i//3*200
 # Fit all seven samples, with clear labels.
 sheet.paste(Image.fromarray(im).resize((320,180)),(x,y+20));d.text((x,y+2),f'{t:.2f}s',fill='white')
sheet.save(a.directory/'READBACK_SHEET.jpg',quality=93)
frames=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',r['output']]))['frames']
assert len(frames)==14829 and all(abs(float(f['best_effort_timestamp_time'])-i/30)<.00002 for i,f in enumerate(frames))
def sequence(path,t,n):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v',str(n),'-vf','scale=320:180','-pix_fmt','rgb24','-f','rawvideo','-'])
 return np.frombuffer(b,np.uint8).reshape(n,180,320,3)
expected_path=a.directory/'crab_dissolved.mp4'
actual=sequence(r['output'],lo/30,hi-lo).astype(float);expected=sequence(expected_path,0,hi-lo).astype(float)
errors=np.abs(actual-expected).mean(axis=(1,2,3));assert float(errors.max())<2,(float(errors.max()))
replacement=dict(frames_compared=hi-lo,mean_error=float(errors.mean()),maximum_frame_mean_error=float(errors.max()),threshold=2,dissolved_sha256=sha(expected_path))
out=dict(replacement_window=replacement,status='CLOCK_REPLACEMENT_WINDOW_AND_SPARSE_OUTSIDE_READBACK_PASS',sha256=r['sha256'],frames=len(frames),duration_s=len(frames)/30,samples=rows,limitations=['All replacement-window frames compared at 320x180; outside it, seven sparse still comparisons. Not full-film or moving-picture/listening review.','Normal combined picture QA remains authoritative; no failure waived.'])
(a.directory/'READBACK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
