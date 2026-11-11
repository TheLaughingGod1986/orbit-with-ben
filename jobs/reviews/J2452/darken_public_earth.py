#!/usr/bin/env python3
"""Grade only after undarkened edit gates, then measure the actual saved pixels."""
import hashlib,json,re,subprocess as sp
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import build_public_earth as b
SRC=b.OUT.with_name('public_earth_v02')
OUT=b.OUT.with_name('public_earth_dark_v01')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def scan(p):
 r=sp.run(['ffmpeg','-v','info','-xerror','-i',str(p),'-an','-vf','showinfo,fps=4,scale=160:90,format=gray','-f','rawvideo','-'],capture_output=True,check=True,timeout=300)
 n=[int(x) for x in re.findall(rb'\bn:\s*(\d+)\s+pts:',r.stderr)]
 return np.frombuffer(r.stdout,np.uint8).reshape(-1,90,160),max(n)+1

def main():
 build=json.loads((SRC/'BUILD.json').read_text());read=json.loads((SRC/'READBACK.json').read_text())
 assert build.get('quiet_title_verified') is True, 'Restore and inspect the quiet title, then rerun undarkened gates first'
 assert read['gate_exit_codes'] in ([0,0],[1,0])
 assert all(x['classification']=='in the public film' for x in read['inherited_findings'])
 assert float(read['levels']['input_tp'])<=-6
 assert sha(Path(build['output']))==read['sha256']==build['sha256']
 OUT.mkdir(exist_ok=False)
 # Use the delivered preceding chapter lengths, plus their two four-second breaths.
 nas=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/j2452/public_chapters_v01')
 moon=json.loads(next(nas.glob('013*/CHAPTER.json')).read_text())
 saturn=json.loads((nas/'021_saturn_v05/CHAPTER.json').read_text())
 start=moon['build']['duration_s']+saturn['build']['duration_s']+8
 assert abs(start-967.2)<.1,start
 video=OUT/'027_earth_darkened_v01.mp4'
 # Scale legal-range signal above black. The latest ruling's 85% measured
 # brightness target controls this test grade; no additional highlight clipping.
 factor=f'(1-0.15*clip((T+{start}-1170)/60,0,1))'
 vf=f"geq=lum='16+floor((lum(X,Y)-16)*{factor}+0.5)':cb='cb(X,Y)':cr='cr(X,Y)'"
 b.run(['-i',build['output'],'-vf',vf,'-map','0:v','-map','0:a','-frames:v',str(build['expected_frames']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(video)])
 before,n0=scan(build['output']);after,n1=scan(video)
 assert n0==n1==build['expected_frames'],(n0,n1)
 assert before.shape==after.shape
 means0=before.mean(axis=(1,2));means1=after.mean(axis=(1,2));mask=np.arange(len(before))/4+start>=1230
 ratio=float(means1[mask].mean()/means0[mask].mean())
 assert .83<=ratio<=.87,ratio
 windows=[]
 for k in range(0,len(before)-7,8):
  if k/4+start<1230:continue
  m0=float(before[k:k+8].mean());m1=float(after[k:k+8].mean())
  windows.append(dict(chapter_start_s=k/4,source_mean_luma=m0,graded_mean_luma=m1,ratio=m1/m0 if m0 else None))
 assert all(w['ratio'] is not None and .83<=w['ratio']<=.87 for w in windows), ('Brightness window outside tolerance', [w for w in windows if w['ratio'] is None or not .83<=w['ratio']<=.87])
 probe=json.loads(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=nb_frames,duration','-of','json',str(video)]))
 source_probe=read['probe'];assert abs(float(probe['format']['duration'])-float(source_probe['format']['duration']))<.001
 bright=sorted([dict(start_s=k/4,end_s=(k+8)/4,mean_luma=float(after[k:k+8].mean())) for k in range(0,len(after)-7,8)],key=lambda x:x['mean_luma'],reverse=True)[:5]
 sheet=Image.new('RGB',(960,1470),'#161616');d=ImageDraw.Draw(sheet)
 for i,w in enumerate(bright):
  frame=OUT/f'brightest_{i+1:02d}.jpg';sp.run(['ffmpeg','-v','error','-n','-ss',str(w['start_s']+1),'-i',str(video),'-frames:v','1',str(frame)],check=True)
  im=Image.open(frame).convert('RGB');im.thumbnail((480,270));sheet.paste(im,(0,i*294));d.text((490,i*294+12),f"{w['start_s']:.2f}-{w['end_s']:.2f}s\nMean luma {w['mean_luma']:.2f}",fill='white');w['frame']=str(frame)
 sheet.save(OUT/'BRIGHTEST_WINDOWS.jpg',quality=90)
 report=dict(status='DARKENED_CHAPTER_VERIFIED_NOT_FINAL_COMPILATION',output=str(video),sha256=sha(video),source_undarkened=str(SRC),source_sha256=build['sha256'],compilation_start_s=start,frames_before=n0,frames_after=n1,probe=probe,post_2030_brightness_ratio=ratio,target_ratio=.85,tolerance=.02,post_2030_two_second_measurements=windows,brightest_two_second_windows=bright,grade=vf,undarkened_build=build,undarkened_readback=read,remaining='NAS save and destination hashes; final continuous bed, full-film loudness/peak/silence/CTA/join checks, reel and Ben watch card. Public-source charts and labels retained; dissolves only on compilation edits.')
 (OUT/'DARKEN_READBACK.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['output','sha256','frames_after','post_2030_brightness_ratio']},indent=2))
if __name__=='__main__':main()
