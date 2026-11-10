"""J1208 source-only evidence. No perceptual review or finished-cut gate claim."""
from pathlib import Path
import json,subprocess,hashlib
import numpy as np
ROOT=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
OUT=Path.home()/'_desk/handoff/J1208/flow-20261105'
def ff(*args):subprocess.run(['ffmpeg','-y','-v','error',*map(str,args)],check=True)
for subject in ['S5','S6']:
 src=OUT/f'{subject}_flow_t2_silent.mp4'
 if not src.exists():continue
 cuts=[dict(row='preroll',timeline_in=0,timeline_out=1.15,source=str(src),upscale=1.5,framing={'offset':0}),dict(row='opening',timeline_in=1.15,timeline_out=3.85,source=str(src),upscale=1.5,framing={'offset':1.15})]
 cutfile=OUT/f'{subject}_t2_source_cuts.json';cutfile.write_text(json.dumps(cuts,indent=2))
 pool=OUT/f'{subject}_t2_source_pool.json';pool.write_text(json.dumps([{'file':str(src),'title':f'Generated explanatory {subject} illustration; Flow Veo 3.1 Fast; not observational footage'}]))
 qa=OUT/f'{subject}_t2_source_qa'
 r=subprocess.run(['python3',str(ROOT/'scripts/picture_qa.py'),str(src),'--cuts',str(cutfile),'--pool',str(pool),'--out-dir',str(qa)],capture_output=True,text=True)
 print(subject,'source QA exit',r.returncode,r.stdout,flush=True)
 (OUT/f'{subject}_t2_source_qa_stdout.txt').write_text(r.stdout+r.stderr)
 ff('-i',src,'-vf','fps=2,scale=270:-2,tile=4x4','-frames:v','1',OUT/f'{subject}_t2_sheet.jpg')
 for t in (0,0.575,1.15,2.5,3.8):ff('-ss',t,'-i',src,'-frames:v','1',OUT/f'{subject}_t2_t{t:.3f}.png')
 ff('-i',src,'-t','3.85','-vf','scale=360:640','-an',OUT/f'{subject}_t2_phone_source.mp4')
 ff('-ss','1.15','-i',src,'-t','2.7','-an',OUT/f'{subject}_t2_opening.mp4')
 ff('-i',src,'-t','1.15','-an',OUT/f'{subject}_t2_preroll.mp4')
 def gray(t):
  data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(src),'-frames:v','1','-vf','scale=180:320,format=gray','-f','rawvideo','-'])
  return np.frombuffer(data,np.uint8).astype(float)
 metrics={'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'opening_source':[1.15,3.85],'preroll_source':[0,1.15],'upscale_to_1080x1920':1.5,'crop':'none','speed':1,'MAD_opening_first_to_1_5s':float(np.abs(gray(1.15)-gray(2.65)).mean()),'native_video_review':'NOT PERFORMED; text/stills/metrics only','phone_review':'NOT PERFORMED; file supplied','loop_preroll_review':'NOT PERFORMED; intervals supplied','finished_cut_gates':'NOT RUN: silent source candidates, no finished cuts'}
 (OUT/f'{subject}_t2_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
