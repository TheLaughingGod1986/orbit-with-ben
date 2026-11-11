#!/usr/bin/env python3
"""Build a bounded join for the original-source Chajnantor component."""
import argparse, json
from pathlib import Path
from build_orion_source_repair import sha, run
p=argparse.ArgumentParser();p.add_argument('--repair',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=False)
r=json.loads((a.repair/'REPORT.json').read_text());patch=Path(r['output'])
assert sha(patch)==r['sha256']
assert json.loads((a.repair/'qa/picture_qa.json').read_text())['verdict']=='PASS'
source=Path('/Users/ben/_desk/J2452-sleep-scratch/betelgeuse_chapter_orion_repaired_v01/029_picture_orion_repaired.mp4')
assert sha(source)=='8f4e2bde4a3143e09c3b0597eed6bd0f74bc52668716ba610268b557ef4e14e1'
start=round(234.3*30);end=round(240.78*30);lo=start-60;hi=end+60
d=(hi-lo)/30;fade=(end-start+60)/30
graph=f'[0:v]fps=30,setpts=PTS-STARTPTS,scale=in_color_matrix=bt709,format=rgb24[base];[1:v]fps=30,setpts=PTS-STARTPTS,scale=in_color_matrix=bt709,format=rgba,tpad=start_mode=clone:start_duration=2:stop_mode=clone:stop_duration=2,trim=duration={d},fade=t=in:st=0:d=2:alpha=1,fade=t=out:st={fade}:d=2:alpha=1[cover];[base][cover]overlay=eof_action=pass:format=rgb,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]'
out=a.out/'chajnantor_join.mp4'
run(['-ss',str(lo/30),'-i',str(source),'-i',str(patch),'-filter_complex',graph,'-map','[v]','-frames:v',str(hi-lo),'-an','-c:v','libx264','-preset','fast','-crf','18','-threads','4','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000',str(out)])
run(['-i',str(out),'-f','null','-'])
report=dict(status='JOIN_NOT_INTEGRATED_NOT_UAT',source=str(source),source_sha256=sha(source),repair=r,output=str(out),sha256=sha(out),chapter_frames=[lo,hi],opaque_frames=[start,end],frames=hi-lo,graph=graph)
(a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
cuts=[]
for i,(x,y) in enumerate([(0,2),(2,fade),(fade,d)]):
 cuts.append(dict(row=str(i),source='chajnantor_mw.m4v' if i==1 else 'adjacent_picture',kind='video',timeline_in=x,timeline_out=y,upscale=1.5 if i==1 else 1,framing=dict(offset=3.25) if i==1 else {}))
(a.out/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
print(out)
