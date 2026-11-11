#!/usr/bin/env python3
"""Read back the saved Sun candidate, normal gates and brightest windows."""
import argparse
import hashlib
import json
import re
import subprocess as sp
import sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
OUT=Path('/Users/ben/_desk/J2452-sleep-scratch/public_sun_v01')
def main():
    global OUT
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=OUT)
    OUT=parser.parse_args().out
    build=json.loads((OUT/'BUILD.json').read_text()); video=build['output']
    full=json.loads((OUT/'full_pixel_cuts.json').read_text())
    # Merge a sub-frame tail into its preceding sampling bin. Seeking after
    # the final PTS returns no frame even while container duration continues.
    last_pts=(build['expected_frames']-1)/30
    while len(full)>1 and full[-1]['timeline_in']>=last_pts:
        full.pop()
    full[-1]['timeline_out']=build['duration_s']
    (OUT/'full_pixel_cuts.json').write_text(json.dumps(full,indent=2)+'\n')
    changed=json.loads((OUT/'changed_cuts.json').read_text())
    # The ending trim is also this job's edit: its two-second neighbourhood
    # must never be classified as untouched public-film picture.
    changed.append(dict(row='end-trim',timeline_in=build['duration_s'],timeline_out=build['duration_s'],source='end-trim'))
    # Inspect half-second neighbourhoods on both sides of every new trim/join.
    # Each transition groups contiguous sampling rows under one identity;
    # their offsets advance through that finished transition interval.
    # Merge overlapping edit neighbourhoods: inspect every covered half-second
    # once, retaining a continuous identity for repeat checking within each.
    intervals=sorted((max(0,c['timeline_in']-2),min(last_pts,c['timeline_out']+2)) for c in changed)
    merged=[]
    for lo,hi in intervals:
        if merged and lo<=merged[-1][1]: merged[-1][1]=max(merged[-1][1],hi)
        else: merged.append([lo,hi])
    dense=[]
    for i,(lo,hi) in enumerate(merged):
        for k,t in enumerate(np.arange(lo,hi,.5)):
            dense.append(dict(row=f'change-{i}-{k}',timeline_in=float(t),timeline_out=float(min(t+.5,hi)),
                              source=f'finished_transition_{i}',framing=dict(offset=float(t-lo)),src_w=1920,upscale=1))
    (OUT/'changed_dense_cuts.json').write_text(json.dumps(dense,indent=2)+'\n')
    pool=[dict(source=f'finished_transition_{i}',title='Finished Sun picture surrounding compilation edits') for i in range(len(merged))]
    (OUT/'changed_pool.json').write_text(json.dumps(pool,indent=2)+'\n')
    commands=[
        [sys.executable,str(ROOT/'scripts/polish_gate.py'),video,'--cuts',str(OUT/'full_pixel_cuts.json'),'--out',str(OUT/'POLISH_GATE.json')],
        [sys.executable,str(ROOT/'scripts/picture_qa.py'),video,'--cuts',str(OUT/'changed_dense_cuts.json'),'--pool',str(OUT/'changed_pool.json'),'--out-dir',str(OUT/'joins_qa')],
    ]
    codes=[]
    for i,cmd in enumerate(commands):
        with (OUT/f'gate_{i}.log').open('w') as log:
            codes.append(sp.run(cmd,stdout=log,stderr=sp.STDOUT,timeout=300).returncode)
        print('gate finished',i,codes[-1],flush=True)
    if not (OUT/'POLISH_GATE.json').exists():
        failure=dict(status='GATE_EXECUTION_FAILED_NOT_A_PASS',gate_exit_codes=codes,logs=[str(OUT/f'gate_{i}.log') for i in range(2)])
        (OUT/'GATE_EXECUTION_FAILURE.json').write_text(json.dumps(failure,indent=2)+'\n')
        raise RuntimeError('Pixel gate did not produce its report; inspect the execution log before any delivery')
    probe=json.loads(sp.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',video]))
    levels=sp.run(['ffmpeg','-v','info','-i',video,'-vn','-af','loudnorm=I=-20:TP=-6:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,timeout=180)
    text=levels.stderr; levels=json.loads(text[text.rfind('{'):text.rfind('}')+1])
    # Whole-video luminance scan at 4 fps; rank non-overlapping 2 s windows.
    scan=sp.run(['ffmpeg','-v','info','-xerror','-threads','4','-reinit_filter','0','-i',video,'-an','-vf','showinfo,fps=4,scale=160:90,format=gray','-f','rawvideo','-'],capture_output=True,check=True,timeout=300)
    (OUT/'decode_scan.log').write_bytes(scan.stderr)
    raw=scan.stdout
    decoded=[int(x) for x in re.findall(r'\bn:\s*(\d+)\s+pts:',scan.stderr.decode(errors='replace'))]
    if not decoded or max(decoded)+1 != build['expected_frames']: raise ValueError(('decoded frame count',max(decoded)+1 if decoded else None,build['expected_frames']))
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
                probe=probe,full_decode_exit=scan.returncode,decoded_frames=max(decoded)+1,decode_scan='Full decode with showinfo count before fps reduction; same pass supplies brightness scan.',
                gate_exit_codes=codes,pixel_verdict=pixel['verdict'],inherited_findings=inherited,
                levels=levels,brightest_two_second_windows=bright,
                darkening='PENDING: this chapter follows the darkening ramp; apply and measure the constant 85 percent grade after undarkened gates.',
                final_bed_and_silence='Final assembly step: this chapter contains only the clean narration; single bed and full-film silence gate still owed.')
    (OUT/'READBACK.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['sha256','gate_exit_codes','pixel_verdict','inherited_findings','levels']},indent=2),flush=True)

if __name__=='__main__': main()
