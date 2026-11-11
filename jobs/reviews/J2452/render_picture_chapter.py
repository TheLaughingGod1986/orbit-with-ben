#!/usr/bin/env python3
"""Render a checkpoint chapter from explicit source spans, preserving its audio clock.

Dissolves use cloned endpoint handles, not overlapping narration time.
Short source rows get shorter handles instead of being merged into neighbours.
Intermediate and source files are never overwritten. Final gates remain separate.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path

def run(cmd):
    p=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-n',*cmd],capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-4000:])
def digest(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def encode(codec):
    options=['-b:v','6M'] if codec=='h264_videotoolbox' else ['-preset','fast','-crf','18']
    return ['-an','-c:v',codec,*options,'-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000']
def main():
    p=argparse.ArgumentParser();p.add_argument('--diagnostic',action='store_true',help='Required: this prototype and its Venus source recipe are not production approved');p.add_argument('--encoder',choices=['h264_videotoolbox','libx264'],default='h264_videotoolbox');p.add_argument('--recipe',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    recipe=json.loads(a.recipe.read_text())
    if not a.diagnostic: p.error('Diagnostic prototype only; source QA and finishing corrections are required before production use')
    if recipe['global_start_s'] < 1230: p.error('This diagnostic grade supports only chapters entirely after the darkening ramp')
    a.out.mkdir(parents=True,exist_ok=False)
    shots=recipe['shots'];durations=[];paths=[]
    # Render every shot independently; source handles cannot introduce a removed card.
    for i,s in enumerate(shots):
        d=s['duration_s'];assert d>=1/30, s
        out=a.out/f'shot_{i:03d}.mp4'
        inp=['-ss',str(s.get('source_in_s',0)),'-i',s['source']]
        if s.get('still'):inp=['-loop','1','-i',s['source']]
        vf='scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=30,setpts=PTS-STARTPTS'
        if s.get('still'):
            vf+=",zoompan=z='1.01+0.015*on/"+str(round(d*30))+"':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30"
        vf+=',colorchannelmixer=rr=0.85:gg=0.85:bb=0.85,format=yuv420p,limiter=min=16:max=180:planes=1'
        run([*inp,'-t',str(d),'-vf',vf,*encode(a.encoder),str(out)])
        durations.append(round(d*30)/30);paths.append(out)
        print('shot',i,flush=True)
    # Encode stable interiors, then two-second endpoint dissolves at every cut.
    pieces=[]
    # Integer-frame handles preserve even sub-second rows and the exact clock.
    frames=[round(d*30) for d in durations]
    handles=[min(30,(frames[i]-1)//2,(frames[i+1]-1)//2) for i in range(len(frames)-1)]
    if any(h<1 for h in handles): raise ValueError('One-frame edge row needs an explicit picture decision; never merge silently')
    for i,(src,d) in enumerate(zip(paths,durations)):
        start=handles[i-1]/30 if i else 0
        end=d-(handles[i]/30 if i<len(paths)-1 else 0)
        out=a.out/f'interior_{i:03d}.mp4'
        run(['-ss',str(start),'-i',str(src),'-t',str(end-start),*encode(a.encoder),str(out)]);pieces.append(out)
        if i==len(paths)-1:continue
        trans=a.out/f'dissolve_{i:03d}.mp4'
        h=handles[i]/30
        graph=f'[0:v]trim=start={d-h}:end={d},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={h}[a];[1:v]trim=end={h},setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration={h}[b];[a][b]xfade=transition=fade:duration={2*h}:offset=0,format=yuv420p[v]'
        run(['-i',str(src),'-i',str(paths[i+1]),'-filter_complex',graph,'-map','[v]','-t',str(2*h),*encode(a.encoder),str(trans)]);pieces.append(trans)
        print('join',i,flush=True)
    listing=a.out/'concat.txt';listing.write_text(''.join("file '"+str(x)+"'\n" for x in pieces))
    final=a.out/'picture_candidate.mp4';run(['-f','concat','-safe','0','-i',str(listing),'-c','copy',str(final)])
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(final)]))
    run(['-i',str(final),'-f','null','-'])
    result=dict(status='PICTURE_CANDIDATE_NOT_FINAL_QA',recipe_sha256=digest(a.recipe),output=str(final),sha256=digest(final),expected_duration_s=sum(durations),actual_duration_s=float(probe['format']['duration']),shots=len(shots),dissolves=len(shots)-1,dissolve_durations_s=[2*h/30 for h in handles],limiter_planes='luma_only',probe=probe,limitations=recipe['limitations'])
    assert abs(result['expected_duration_s']-result['actual_duration_s'])<0.08,result
    (a.out/'REPORT.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
