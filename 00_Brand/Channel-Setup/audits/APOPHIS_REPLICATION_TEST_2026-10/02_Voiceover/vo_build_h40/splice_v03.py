#!/usr/bin/env python3
"""Chief h40 (J1306): build apophis_ar1_vo_v03 and apophis_ar3_vo_v03 by removing whole sentences
from the recorded v02 takes at room-tone points (< -70 dB). No word is re-voiced and no sample inside a
kept span is changed except a 10 ms qsin fade at each join (fade-out at the end of a span, fade-in at
the start of the next), plus, on AR1 only, a 160 ms qsin fade-out ending on the last frame: the
ElevenLabs C7 retake "knowing..." is cut off by the API at about -21 dBFS, and Cursor's 10 ms fade left the
last 20 ms at -32 dB (the h23/h31/h32/h39 too-short-fade case). 160 ms starts after the vowel, in the
nasal murmur, and gives last 10 ms -73.6 / last 20 ms -49.0. Deterministic.
usage (from 02_Voiceover/): python3 vo_build_h40/splice_v03.py ar1|ar3
  ar1: apophis_ar1_vo_v02.wav -> apophis_ar1_vo_v03.wav  (drops "Sixty metres wide, it matches a
       fifteen-storey building."; tightens the 0.94 s pause before "Look up knowing..." to 0.69 s)
  ar3: apophis_ar3_vo_v02.wav -> apophis_ar3_vo_v03.wav  (drops "Its shadow spans two hundred and
       fifty-eight kilometres." and "That nearly triples twenty twenty-six's two-minute eclipse.")"""
import sys,os,wave,hashlib,numpy as np
SR=48000; F=480  # 10 ms
END_FADE={'ar1':7680,'ar3':0}  # frames
JOBS={
 'ar1':('apophis_ar1_vo_v02.wav','9154050eee7ae6a9245897368dff3282f0bd68f3dc5f28169cedf2e1d9ed28d6',1104000,
        'apophis_ar1_vo_v03.wav',
        [(0,381600),          # 0.000-7.950  "Asteroid ... December twenty-second, twenty thirty-two."
         (585600,1012320),    # 12.200-21.090 "Early tracking ... It will miss, passing ... kilometres up."
         (1030800,1104000)]), # 21.475-23.000 "Look up knowing..." (C7 retake 1, to file end)
 'ar3':('apophis_ar3_vo_v02.wav','03d0e06380a3237257058b8d4a84a31e760af048ef1dc616a0031ea738e1ea2a',1255680,
        'apophis_ar3_vo_v03.wav',
        [(0,318240),          # 0.000-6.630  "The twenty twenty-seven solar eclipse ... for over six minutes."
         (742320,1106400),    # 15.465-23.050 "Totality crosses Spain and North Africa, peaking over Egypt at six minutes twenty-three seconds."
         (1119360,1255680)]), # 23.320-26.160 "Millions can look up as..." (to file end)
}
src,sha,nf,dst,spans=JOBS[sys.argv[1]]
assert hashlib.sha256(open(src,'rb').read()).hexdigest()==sha, src+' is not the h40-reviewed take'
assert not os.path.exists(dst), dst+' exists; refusing to overwrite'
w=wave.open(src); p=w.getparams(); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2); w.close()
assert (p.nchannels,p.sampwidth,p.framerate,p.nframes)==(2,2,SR,nf)
up=np.sin(np.pi/2*(np.arange(F)+1)/F); down=up[::-1]
parts=[]
for i,(s,e) in enumerate(spans):
  x=a[s:e].astype(float)
  if i>0: x[:F]*=up[:,None]
  if i<len(spans)-1: x[-F:]*=down[:,None]
  parts.append(np.round(x).astype(np.int16))
o=np.concatenate(parts)
n=END_FADE[sys.argv[1]]
if n:
  g=np.sin(np.pi/2*(np.arange(n,0,-1)-1)/n)
  o[-n:]=np.round(o[-n:].astype(float)*g[:,None]).astype(np.int16)
w=wave.open(dst,'wb'); w.setparams(p); w.writeframes(o.tobytes()); w.close()
print('wrote',dst,len(o),'frames',len(o)/SR,'s',hashlib.sha256(open(dst,'rb').read()).hexdigest())
