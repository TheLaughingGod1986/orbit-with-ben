#!/usr/bin/env python3
"""Vectorized exact spatial grade, avoiding per-pixel expression interpretation.
No gate bypass: verify saved output with darken_public_light.py afterwards.
"""
import argparse,hashlib,json,subprocess as sp,time
from pathlib import Path
import numpy as np
SRC=Path('/Users/ben/_desk/J2452-sleep-scratch/public_light_v06/024_light_undarkened_v04.mp4')
OUT=SRC.parent.with_name('public_light_dark_v05')
W,H=1920,1080

def main(seconds=None):
 OUT.mkdir(exist_ok=True)
 target=OUT/('probe.mp4' if seconds else '024_light_darkened_v05.mp4')
 assert not target.exists()
 assert hashlib.file_digest(SRC.open('rb'),'sha256').hexdigest()=='621f6d198475a1e02f240f56691e41f16794625850c25315fa0ae5b30d87fcae'
 # This is exactly the tested spatial rounding expression, precalculated.
 phase=((np.arange(H)[:,None]+np.arange(W)[None,:])%20).astype(np.uint16)*256
 vals=np.arange(256,dtype=float)
 table=np.clip(np.floor((vals[None,:]-16)*.85+16+np.arange(20)[:,None]/20),0,255).astype(np.uint8).ravel()
 chroma=np.clip((vals-128)*.85+128,0,255).astype(np.uint8)
 dec=['ffmpeg','-v','error','-nostdin','-threads','2','-i',str(SRC)]
 if seconds:dec+=['-t',str(seconds)]
 dec+=['-an','-pix_fmt','yuv420p','-f','rawvideo','-']
 enc=['ffmpeg','-v','error','-nostdin','-n','-f','rawvideo','-pix_fmt','yuv420p','-s','1920x1080','-r','30','-i','-','-i',str(SRC),'-map','0:v','-map','1:a','-c:v','libx264','-preset','ultrafast','-crf','0','-threads','4','-pix_fmt','yuv420p','-video_track_timescale','90000','-c:a','copy','-shortest',str(target)]
 n=0;start=time.monotonic();size=W*H*3//2
 with (OUT/('probe_decode.log' if seconds else 'render_decode.log')).open('wb') as de, (OUT/('probe_encode.log' if seconds else 'render_encode.log')).open('wb') as ee:
  decoder=sp.Popen(dec,stdout=sp.PIPE,stderr=de);encoder=sp.Popen(enc,stdin=sp.PIPE,stderr=ee)
  try:
   while True:
    assert time.monotonic()-start<600, 'Bounded render timeout'
    raw=decoder.stdout.read(size)
    if not raw:break
    assert len(raw)==size
    frame=np.frombuffer(raw,np.uint8);y=frame[:W*H].reshape(H,W)
    encoder.stdin.write(table[phase+y].tobytes())
    encoder.stdin.write(chroma[frame[W*H:]].tobytes())
    n+=1
    if n%900==0:print(json.dumps(dict(frames=n,elapsed_s=time.monotonic()-start)),flush=True)
   encoder.stdin.close()
   assert decoder.wait(timeout=30)==0
   assert encoder.wait(timeout=60)==0
  finally:
   for proc in (decoder,encoder):
    if proc.poll() is None:proc.kill();proc.wait()
 assert n==(round(seconds*30) if seconds else 13900), n
 record=dict(output=str(target),frames=n,elapsed_s=time.monotonic()-start,method='Exact spatial luma LUT; chroma scaled by 0.85; lossless H.264',source_sha256=hashlib.file_digest(SRC.open('rb'),'sha256').hexdigest(),sha256=hashlib.file_digest(target.open('rb'),'sha256').hexdigest(),status='RENDER_ONLY_REQUIRES_NATIVE_SAVED_PIXEL_VERIFICATION')
 (OUT/('PROBE_RENDER.json' if seconds else 'RENDER.json')).write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seconds',type=float);main(p.parse_args().seconds)
