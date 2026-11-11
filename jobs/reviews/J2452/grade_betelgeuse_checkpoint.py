#!/usr/bin/env python3
"""Lift shadow detail in the six failed spans; preserve the previous checkpoint."""
import argparse, hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=False)
source=Path('/Users/ben/_desk/J2452-sleep-scratch/betelgeuse_chapter_v01/029_picture_checkpoint.mp4')
assert hashlib.file_digest(source.open('rb'),'sha256').hexdigest() == '69151e31eee05f9bab481fd16893fb50f8c8e3720e0fc39a1379b7e9302095dc'
fail=json.loads((ROOT/'betelgeuse_chapter_v01/FAILURES.json').read_text())
spans=[x['chapter_range_s'] for x in fail['failures'] if any('near-black' in s for s in x['why'])]
# Grade the entire shot rather than selected gate samples; no timing changes.
condition='+'.join(f'gte(t,{lo})*lt(t,{hi})' for lo,hi in spans)
graph=f"lutyuv=y='16+164*pow(clip((val-16)/164,0,1),0.70)':enable='{condition}',limiter=min=16:max=180:planes=1"
output=a.out/'029_picture_shadow_grade_v04.mp4'
cmd=['ffmpeg','-hide_banner','-nostdin','-v','error','-n','-i',str(source),'-vf',graph,'-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','6','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-video_track_timescale','90000',str(output)]
subprocess.run(cmd,check=True)
subprocess.run(['ffmpeg','-v','error','-nostdin','-i',str(output),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(output)]))
assert int(probe['streams'][0]['nb_read_frames'])==14829
sha=lambda x:hashlib.file_digest(x.open('rb'),'sha256').hexdigest()
(a.out/'REPORT.json').write_text(json.dumps(dict(covers=json.loads((source.parent/'REPORT.json').read_text())['covers'],source=str(source),source_sha256=sha(source),output=str(output),sha256=sha(output),spans=spans,filter=graph,frames=14829,duration_s=494.3,status='SHADOW_GRADE_CHECKPOINT_NOT_UAT',limitations=['Gutter finding retained; no override.','Code graphics, reuse, finishing, title and compilation assembly remain.','Normal polish gate must be rerun.']),indent=2)+'\n')
print(output)
