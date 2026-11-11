#!/usr/bin/env python3
"""Save a ten-second join candidate with original-source Orion replacement."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from build_orion_source_repair import sha,run
p=argparse.ArgumentParser();p.add_argument('--repair',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=False)
r=json.loads((a.repair/'REPORT.json').read_text());clip=Path(r['output']);assert sha(clip)==r['sha256']
source=Path('/Users/ben/_desk/J2452-sleep-scratch/betelgeuse_chapter_v01/029_picture_checkpoint.mp4');assert sha(source)=='69151e31eee05f9bab481fd16893fb50f8c8e3720e0fc39a1379b7e9302095dc'
# Opaque over all 198 source-shot frames; two-second fades in adjacent shots.
graph='[0:v]fps=30,setpts=PTS-STARTPTS,scale=in_color_matrix=bt709,format=rgb24[base];[1:v]fps=30,setpts=PTS-STARTPTS,scale=in_color_matrix=bt709,format=rgba,tpad=start_mode=clone:start_duration=2:stop_mode=clone:stop_duration=2,trim=duration=10.6,fade=t=in:st=0:d=2:alpha=1,fade=t=out:st=8.6:d=2:alpha=1[cover];[base][cover]overlay=eof_action=pass:format=rgb,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]'
out=a.out/'orion_repaired_join.mp4'
run(['-ss','430.5','-i',str(source),'-i',str(clip),'-filter_complex',graph,'-map','[v]','-frames:v','318','-an','-c:v','libx264','-preset','fast','-crf','18','-threads','4','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000',str(out)])
run(['-i',str(out),'-f','null','-'])
report=dict(status='JOIN_CANDIDATE_NOT_FULL_CHAPTER_OR_UAT',source=str(source),source_sha256=sha(source),repair=r,output=str(out),sha256=sha(out),chapter_range_s=[430.5,441.1],opaque_range_s=[432.5,439.1],frames=318,graph=graph)
(a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
cuts=[dict(row=str(i),source='join' if i!=2 else 'orion_rise_vlt.mp4',timeline_in=lo,timeline_out=hi,kind='video',framing=({'offset':0} if i==2 else {}),upscale=1) for i,(lo,hi) in enumerate([(0,2),(2,8.6),(8.6,10.6)],1)]
(a.out/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
print(out)
