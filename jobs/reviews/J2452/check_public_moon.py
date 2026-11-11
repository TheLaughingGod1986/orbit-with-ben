#!/usr/bin/env python3
"""Read back the saved Moon candidate, normal gates and brightest windows."""
import hashlib
import json
import subprocess as sp
import sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
OUT=Path('/Users/ben/_desk/J2452-sleep-scratch/public_moon_v02')
def main():
    build=json.loads((OUT/'BUILD.json').read_text()); video=build['output']
    changed=json.loads((OUT/'changed_cuts.json').read_text())
    # Inspect half-second neighbourhoods on both sides of every new trim/join.
    # Each transition groups contiguous sampling rows under one identity;
    # their offsets advance through that finished transition interval.
    dense=[]
    for i,c in enumerate(changed):
        lo=max(0,c['timeline_in']-2); hi=min(build['duration_s'],c['timeline_out']+2)
        for k,t in enumerate(np.arange(lo,hi,.5)):
            dense.append(dict(row=f'change-{i}-{k}',timeline_in=float(t),timeline_out=float(min(t+.5,hi)),
                              source=f'finished_transition_{i}',framing=dict(offset=float(t-lo)),src_w=1920,upscale=1))
    (OUT/'changed_dense_cuts.json').write_text(json.dumps(dense,indent=2)+'\n')
    commands=[
        [sys.executable,str(ROOT/'scripts/polish_gate.py'),video,'--cuts',str(OUT/'full_pixel_cuts.json'),'--out',str(OUT/'POLISH_GATE.json')],
        [sys.executable,str(ROOT/'scripts/picture_qa.py'),video,'--cuts',str(OUT/'changed_dense_cuts.json'),'--out-dir',str(OUT/'joins_qa')],
    ]
    codes=[]
    for i,cmd in enumerate(commands):
        with (OUT/f'gate_{i}.log').open('w') as log:
            codes.append(sp.run(cmd,stdout=log,stderr=sp.STDOUT,timeout=300).returncode)
        print('gate finished',i,codes[-1],flush=True)
    probe=json.loads(sp.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',video]))
    dec=sp.run(['ffmpeg','-v','error','-i',video,'-f','null','-'],capture_output=True,text=True,timeout=180)
    levels=sp.run(['ffmpeg','-v','info','-i',video,'-vn','-af','loudnorm=I=-20:TP=-6:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,timeout=180)
    text=levels.stderr; levels=json.loads(text[text.rfind('{'):text.rfind('}')+1])
    # Whole-video luminance scan at 4 fps; rank non-overlapping 2 s windows.
    raw=sp.check_output(['ffmpeg','-v','error','-i',video,'-an','-vf','fps=4,scale=160:90,format=gray','-f','rawvideo','-'],timeout=180)
    frames=np.frombuffer(raw,np.uint8).reshape(-1,90,160)
    candidates=[]
    for k in range(0,len(frames)-7,8):
        candidates.append(dict(start_s=k/4,end_s=(k+8)/4,mean_luma=float(frames[k:k+8].mean())))
    bright=sorted(candidates,key=lambda x:x['mean_luma'],reverse=True)[:5]
    for i,b in enumerate(bright):
        path=OUT/f'brightest_{i+1:02d}.jpg'
        sp.run(['ffmpeg','-v','error','-n','-ss',str(b['start_s']+1),'-i',video,'-frames:v','1',str(path)],check=True)
        b['frame']=str(path)
    pixel=json.loads((OUT/'POLISH_GATE.json').read_text())
    changed_ranges=[(c['timeline_in']-2,c['timeline_out']+2) for c in changed]
    for f in pixel['failed']:
        f['classification']='NEW_EDIT_NEIGHBOURHOOD' if any(a<=f['t']<=b for a,b in changed_ranges) else 'in the public film'
        s=next(x for x in build['slices'] if x['chapter_in_s']<=f['t']<x['chapter_out_s'])
        f['master_time_s']=s['master_in_s']+f['t']-s['chapter_in_s']
    inherited=pixel['failed']
    report=dict(status='READBACK_ONLY_NOT_UAT',output=video,
                sha256=hashlib.file_digest(open(video,'rb'),'sha256').hexdigest(),
                probe=probe,full_decode_exit=dec.returncode,decode_stderr=dec.stderr,
                gate_exit_codes=codes,pixel_verdict=pixel['verdict'],inherited_findings=inherited,
                levels=levels,brightest_two_second_windows=bright,
                darkening='Not active in chapter 1; the undarkened saved file is the delivered file. No brightness change or frame-count change.',
                final_bed_and_silence='Final assembly step: this chapter contains only the clean narration; single bed and full-film silence gate still owed.')
    (OUT/'READBACK.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['sha256','gate_exit_codes','pixel_verdict','inherited_findings','levels']},indent=2),flush=True)

if __name__=='__main__': main()
