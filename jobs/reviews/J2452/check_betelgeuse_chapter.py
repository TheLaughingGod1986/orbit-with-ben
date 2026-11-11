#!/usr/bin/env python3
"""Read back full-chapter clock and every opaque cover frame independently."""
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

def frames(path,start,count):
    vf="scale=320:180"
    data=subprocess.check_output(['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-ss',f'{start/30:.9f}','-i',str(path),'-vf',vf,'-fps_mode','passthrough','-frames:v',str(count),'-pix_fmt','rgb24','-f','rawvideo','-'])
    a=np.frombuffer(data,np.uint8).reshape((-1,180,320,3));assert len(a)==count,(len(a),count);return a

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    r=json.loads((a.out/'REPORT.json').read_text());path=Path(r['output'])
    assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256']
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v','-show_frames','-show_entries','frame=best_effort_timestamp_time,width,height,pix_fmt','-of','json',str(path)]))['frames']
    times=[float(x['best_effort_timestamp_time']) for x in probe]
    assert len(times)==r['frames'] and all(abs(t-i/30)<.00002 for i,t in enumerate(times))
    assert all((x['width'],x['height'],x['pix_fmt'])==(1920,1080,'yuv420p') for x in probe)
    checks=[];samples=[]
    for n,c in enumerate(r['covers'],1):
        left=round(c['opaque_in_s']*30)+1;right=round(c['opaque_out_s']*30)
        actual=frames(path,left,right-left)
        refprobe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',c['cover']]))['streams'][0]
        ref=frames(c['cover'],0,int(refprobe['nb_read_frames']))
        errors=[]
        for offset,x in enumerate(actual):
            idx=min(max(left+offset-round(c['chapter_in_s']*30),0),len(ref)-1)
            errors.append(float(np.abs(x.astype(float)-ref[idx].astype(float)).mean()))
        checks.append(dict(cover=n,frames_compared=len(errors),maximum_mean_absolute_rgb_error=max(errors),threshold=2,pass_check=max(errors)<2))
        for label,t in [('before',c['opaque_in_s']-3),('fade in',c['opaque_in_s']-1),('opaque start',c['opaque_in_s']+.1),('middle',(c['chapter_in_s']+c['chapter_out_s'])/2),('opaque end',c['opaque_out_s']-.1),('fade out',c['opaque_out_s']+1),('after',c['opaque_out_s']+3)]:
            im=frames(path,round(t*30),1)[0];samples.append((im,f'Cover {n} {label}: {t:.3f}s'))
    for t in [21.1,22.1,23.1,226.1,227.1,228.1]:
        samples.append((frames(path,round(t*30),1)[0],f'Removed-block join: {t:.3f}s'))
    sheet=Image.new('RGB',(1280,((len(samples)+3)//4)*210),(25,25,25));d=ImageDraw.Draw(sheet)
    for i,(im,label) in enumerate(samples):
        x=(i%4)*320;y=(i//4)*210;sheet.paste(Image.fromarray(im),(x,y+30));d.text((x+4,y+6),label,fill='white')
    sheet.save(a.out/'READBACK_SHEET.jpg',quality=93)
    result=dict(status='SAVED_FULL_CHAPTER_CLOCK_AND_COVER_READBACK',sha256=r['sha256'],frames=len(times),duration_s=len(times)/30,constant_frame_clock=True,geometry=[1920,1080,'yuv420p'],hash_match=True,opaque_checks=checks,all_opaque_checks_pass=all(x['pass_check'] for x in checks),limitations=r['limitations'])
    (a.out/'READBACK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_opaque_checks_pass']
if __name__=='__main__':main()
