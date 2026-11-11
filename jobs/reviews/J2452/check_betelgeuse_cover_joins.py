#!/usr/bin/env python3
"""Independently read back every opaque frame and sparse dissolve endpoints."""
import argparse,json,subprocess,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();out=args.out
r=json.loads((out/'REPORT.json').read_text()); samples=[];checks=[];full_checks=[]
root=Path(__file__).resolve().parents[3]
for i,j in enumerate(r['joins'],1):
    c=json.load(open(root/'jobs/reviews/J2452/betelgeuse_orbit_readback_v01.json'))['covers'][i-1]
    a,b=j['nominal_orbit_local_s']
    def raw(path):
        data=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',path,'-vf','scale=320:180','-pix_fmt','rgb24','-f','rawvideo','-'])
        return np.frombuffer(data,np.uint8).reshape((-1,180,320,3))
    actual=raw(j['output']);reference=raw(c['output'])
    errors=[]
    left,right=j['fully_opaque_local_s']
    for frame in range(round(left*30)+1,round(right*30)):
        refidx=min(max(frame-120,0),len(reference)-1)
        errors.append(float(np.abs(actual[frame].astype(float)-reference[refidx].astype(float)).mean()))
    full_checks.append(dict(join=i,frames_compared=len(errors),maximum_mean_absolute_pixel_error=max(errors),threshold=2,pass_check=max(errors)<2))
    for name,t in [('before',1),('fade_in',3),('opaque_start',a),('middle',(a+b)/2),('opaque_end',b-1/30),('fade_out',b+1),('after',b+3)]:
        f=out/f'join_{i:02d}_{name}.png'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-n','-ss',str(t),'-i',j['output'],'-frames:v','1',str(f)],check=True)
        samples.append((f,f'Join {i}: {name} {t:.3f}s'))
        if name.startswith('opaque') or name=='middle':
            ref=out/f'ref_{i:02d}_{name}.png';rt=min(t-4,c['duration_s']-1/30)
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-n','-ss',str(max(0,rt)),'-i',c['output'],'-frames:v','1',str(ref)],check=True)
            x=np.asarray(Image.open(f)).astype(float);y=np.asarray(Image.open(ref)).astype(float)
            mae=float(np.abs(x-y).mean());checks.append(dict(join=i,time_s=t,reference_cover_time_s=rt,mean_absolute_pixel_error=mae,threshold=2,pass_check=mae<2))
    assert hashlib.sha256(Path(j['output']).read_bytes()).hexdigest()==j['sha256']
sheet=Image.new('RGB',(3*640,5*390),(25,25,25));d=ImageDraw.Draw(sheet)
for k,(f,label) in enumerate(samples):
    x=(k%3)*640;y=(k//3)*390;sheet.paste(Image.open(f).resize((640,360)),(x,y+30));d.text((x+8,y+8),label,fill='white')
sheet.save(out/'ENDPOINTS.jpg',quality=92)
(out/'READBACK.json').write_text(json.dumps(dict(status='SAVED_JOIN_FRAME_READBACK',opaque_checks=checks,every_opaque_frame_checks=full_checks,all_opaque_checks_pass=all(c['pass_check'] for c in checks+full_checks),hashes_match=True,limitations='Every opaque output frame compared at 320x180; sparse full-size endpoint samples; no moving-video perception or final chapter QA.'),indent=2)+'\n')
print(json.dumps(dict(samples=checks,every_frame=full_checks),indent=2))
assert all(c['pass_check'] for c in checks+full_checks), 'Saved opaque frames differ from the replacement; candidate rejected'
