#!/usr/bin/env python3
"""Original deterministic additive score candidate; no samples or paid service.
No perceptual approval is implied. Render to a NEW output directory only.
"""
import argparse, hashlib, json, math, pathlib, subprocess, wave
import numpy as np

SR=48000
DURATION=1443.04
# Boundaries follow delivered narration, not planning estimates.
CHAPTERS=[0,223.99,481.158,746.412,986.862,1258.996,DURATION]
# D-minor / suspended voicings, with a relative-major lift at the outcome.
CHORDS=[(38,45,53,57),(34,41,50,57),(41,48,53,57),(36,43,52,55)]

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(8388608),b''): h.update(b)
 return h.hexdigest()

def tone(t,midi,phase=0):
 f=440*2**((midi-69)/12)
 return (np.sin(2*np.pi*f*t+phase)+.18*np.sin(4*np.pi*f*t+phase)+.06*np.sin(6*np.pi*f*t+phase))/1.24

def chapter_signal(t,chapter):
 # A slow harmonic bed, each chord swelling and overlapping over 16 beats.
 bpm=[64,64,72,72,66,68][chapter]; bar=60/bpm*16
 gain=[.75,.68,.85,.80,.92,.72][chapter]
 x=np.zeros((len(t),2),dtype=np.float64)
 for k in range(max(0,int(t[0]//bar)-1),int(t[-1]//bar)+1):
  local=t-k*bar
  env=np.clip(local/3,0,1)*np.clip((bar+3-local)/3,0,1)
  chord=CHORDS[(k+chapter)%4]
  if chapter==5: chord=[(41,48,57,60),(36,43,55,60),(34,41,53,57),(38,45,53,57)][k%4]
  for n,m in enumerate(chord):
   amp=[.34,.22,.14,.10][n]
   sig=tone(t,m,n*.31)*env*amp
   pan=[.4,.6,.25,.75][n]
   x[:,0]+=sig*math.sqrt(1-pan); x[:,1]+=sig*math.sqrt(pan)
 # Quiet plucked fifth/octave figure in technical chapters; no percussion.
 if chapter in (2,3,4):
  beat=60/bpm*2
  age=np.mod(t,beat); n=(np.floor(t/beat).astype(int)%4)
  notes=np.array([62,69,65,69])[n]
  freq=440*2**((notes-69)/12)
  pluck=np.sin(2*np.pi*freq*age)*np.exp(-age*3)*np.minimum(age/.025,1)*.065
  x+=pluck[:,None]
 return x*gain

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args()
 a.out.mkdir(parents=True,exist_ok=False)
 dst=a.out/'atlantic_original_score_candidate_v01.wav'
 with wave.open(str(dst),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
  for start in range(0,round(DURATION*SR),SR*8):
   end=min(round(DURATION*SR),start+SR*8); t=np.arange(start,end)/SR
   signal=np.zeros((len(t),2))
   for ch,(lo,hi) in enumerate(zip(CHAPTERS,CHAPTERS[1:])):
    # Equal-gain chapter crossfades; chord changes remain continuous.
    weight=np.clip((t-lo+3)/6,0,1)*np.clip((hi+3-t)/6,0,1)
    if ch==0:weight=np.clip((hi+3-t)/6,0,1)
    if ch==5:weight=np.clip((t-lo+3)/6,0,1)
    if np.any(weight):signal+=chapter_signal(np.maximum(t-lo,0),ch)*weight[:,None]
   envelope=np.minimum(t/4,1)*np.minimum((DURATION-t)/5,1)
   # Headroom, no clipping, no limiting artefacts. Final LUFS set separately.
   signal*=envelope[:,None]*.14
   w.writeframes(np.round(np.clip(signal,-.99,.99)*32767).astype('<i2').tobytes())
 report={'state':'original_score_candidate_requires_listening','wav':str(dst),'sha256':sha(dst),'duration_s':DURATION,'sample_rate':SR,'channels':2,'chapter_starts_s':CHAPTERS[:-1],'creation':'Studio original additive synthesis; no recordings, samples, borrowed melodies or generated-service assets.','spend':0,'audio_perception':False,'approval':False}
 (a.out/'SCORE_PROVENANCE.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':main()
