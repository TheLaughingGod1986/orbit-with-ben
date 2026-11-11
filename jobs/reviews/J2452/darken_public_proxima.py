#!/usr/bin/env python3
"""Grade only after undarkened edit gates, then measure the actual saved pixels."""
import argparse,hashlib,json,re,subprocess as sp
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import build_public_proxima as b
SRC=b.OUT.with_name('public_proxima_v03')
OUT=b.OUT.with_name('public_proxima_dark_v01')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def scan(p):
 # Read native decoded Y before averaging: 8-bit resizing rounds near-black
 # values and can change a two-second ratio by several percentage points.
 log=OUT/(Path(p).stem+'_native_decode.log')
 values=[]; frame_bytes=1920*1080
 weights=np.maximum(np.arange(256,dtype=np.float64)-16,0)
 with log.open('wb') as err:
  proc=sp.Popen(['ffmpeg','-v','info','-xerror','-threads','4','-i',str(p),'-an','-filter_threads','2','-vf','showinfo,fps=4,extractplanes=y','-f','rawvideo','-'],stdout=sp.PIPE,stderr=err)
  try:
   while True:
    raw=proc.stdout.read(frame_bytes)
    if not raw:break
    assert len(raw)==frame_bytes, 'Truncated native luma frame'
    counts=np.bincount(np.frombuffer(raw,np.uint8),minlength=256)
    values.append(float(counts@weights/frame_bytes))
   assert proc.wait(timeout=30)==0,log
  finally:
   if proc.poll() is None:proc.kill();proc.wait()
 n=[int(x) for x in re.findall(rb'\bn:\s*(\d+)\s+pts:',log.read_bytes())]
 return np.asarray(values).reshape(-1,1,1),max(n)+1

def main(verify_existing=False):
 build=json.loads((SRC/'BUILD.json').read_text());read=json.loads((SRC/'READBACK.json').read_text())
 assert build.get('unwanted_cards_removed_verified') is True, 'Inspect all cover edges and record unwanted_cards_removed_verified before grading'
 assert read['gate_exit_codes'] in ([0,0],[1,0])
 assert all(x['classification']=='in the public film' for x in read['inherited_findings'])
 assert float(read['levels']['input_tp'])<=-6
 assert sha(Path(build['output']))==read['sha256']==build['sha256']
 if not verify_existing: OUT.mkdir(exist_ok=False)
 # Use the delivered preceding chapter lengths, plus their two four-second breaths.
 nas=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/j2452/public_chapters_v01')
 records=[json.loads(p.read_text()) for p in nas.glob('*/CHAPTER.json')]
 assert len(records)==11, len(records)
 start=sum(r['build']['duration_s']+4 for r in records)
 assert start>=1230,start
 video=OUT/'026_proxima_darkened_v01.mp4'
 # Ordered spatial rounding preserves the fractional 0.85 luma change
 # without a uniform rounding bias; lossless encoding preserves the result.
 vf=r'geq=lum=floor((lum(X\,Y)-16)*0.85+16+mod(X+Y\,20)/20):cb=(cb(X\,Y)-128)*0.85+128:cr=(cr(X\,Y)-128)*0.85+128'
 if not verify_existing:
  from render_proxima_lut import main as render
  render()
 before,n0=scan(build['output']);after,n1=scan(video)
 assert n0==n1==build['expected_frames'],(n0,n1)
 assert before.shape==after.shape
 means0=before.mean(axis=(1,2));means1=after.mean(axis=(1,2));mask=np.arange(len(before))/4+start>=1230
 ratio=float(means1[mask].mean()/means0[mask].mean())
 assert .83<=ratio<=.87,ratio
 ramp_checks=[]
 for k in range(0,len(before)-7,8):
  times=np.arange(k,k+8)/4+start
  expected=1-.15*np.clip((times-1170)/60,0,1)
  base_means=means0[k:k+8]
  wanted=float(np.sum(base_means*expected)/np.sum(base_means))
  actual=float(means1[k:k+8].mean()/base_means.mean())
  ramp_checks.append(dict(chapter_start_s=k/4,expected_ratio=wanted,actual_ratio=actual))
 assert all(abs(w['actual_ratio']-w['expected_ratio'])<=.02 for w in ramp_checks), ('Timed grade outside tolerance',[w for w in ramp_checks if abs(w['actual_ratio']-w['expected_ratio'])>.02])
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
  frame=OUT/f'brightest_{i+1:02d}.jpg'
  if not frame.exists():sp.run(['ffmpeg','-v','error','-n','-ss',str(w['start_s']+1),'-i',str(video),'-frames:v','1',str(frame)],check=True)
  im=Image.open(frame).convert('RGB');im.thumbnail((480,270));sheet.paste(im,(0,i*294));d.text((490,i*294+12),f"{w['start_s']:.2f}-{w['end_s']:.2f}s\nMean luma {w['mean_luma']:.2f}",fill='white');w['frame']=str(frame)
 sheet.save(OUT/'BRIGHTEST_WINDOWS.jpg',quality=90)
 report=dict(status='DARKENED_CHAPTER_VERIFIED_NOT_FINAL_COMPILATION',output=str(video),sha256=sha(video),source_undarkened=str(SRC),source_sha256=build['sha256'],compilation_start_s=start,frames_before=n0,frames_after=n1,probe=probe,post_2030_brightness_ratio=ratio,target_ratio=.85,tolerance=.02,post_2030_two_second_measurements=windows,brightest_two_second_windows=bright,grade=vf,brightness_measurement='Decoded legal-range Y plane, black 16 subtracted and clipped at zero; native 1920x1080 pixels averaged at 4 fps, with no spatial resizing or intermediate quantization. Avoids chroma-dependent YUV-to-gray conversion.',timed_grade_two_second_measurements=ramp_checks,undarkened_build=build,undarkened_readback=read,remaining='NAS save and destination hashes; final continuous bed, full-film loudness/peak/silence/CTA/join checks, reel and Ben watch card. Public-source charts and labels retained; dissolves only on compilation edits.')
 (OUT/'DARKEN_READBACK.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['output','sha256','frames_after','post_2030_brightness_ratio']},indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--verify-existing',action='store_true')
 main(parser.parse_args().verify_existing)
