#!/usr/bin/env python3
"""J2556 timing edit; existing locked take only, no API calls.
Word times are mapped from Scribe, not a new perceptual/ASR review.
"""
import hashlib,json,subprocess,wave
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
SRC=HERE/'supermoon_2026_11_24_c7_trim1_vo_v01.wav'
assert hashlib.sha256(SRC.read_bytes()).hexdigest()=='95a24bc9c4b1352f333c121e96d88483afd7688229e037ba9a51958feeb9f385'
SR=48000
# source in/out, pitch-preserving tempo; gaps cut only between Scribe words.
SPANS=[(.03,.18,1.45),(.225,.58,1.45),(.665,1.10,1.45),(1.185,1.42,1.45),(1.575,1.98,1.45),(2.055,2.58,1.45),
       (2.775,3.38,1.25),(3.555,4.26,1.25),
       (5.04,6.45,1.),(6.67,8.65,1.),(8.9,11.7,1.),(11.85,17.3,1.),(17.77,20.,1.)]
# 0.18-second breath to 'If' includes its 0.18-second source preroll.
with wave.open(str(SRC),'rb') as w:
 raw=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).reshape(-1,2)
source_words=json.loads((HERE/'supermoon_2026_11_24_c7_trim1_vo_v01_words.json').read_text())
for word in source_words:
 assert any(a<=word['start'] and word['end']<=z for a,z,_ in SPANS), f'Word crosses splice: {word}'
parts=[]; mapping=[];acc=0
for i,(a,z,rate) in enumerate(SPANS):
 chunk=raw[round(a*SR):round(z*SR)].copy().astype(float)
 n=480;curve=np.sin(np.linspace(0,np.pi/2,n))
 if i:chunk[:n]*=curve[:,None]
 chunk[-n:]*=curve[::-1,None]
 result=subprocess.run(['ffmpeg','-v','error','-f','s16le','-ar',str(SR),'-ac','2','-i','pipe:0','-af',f'atempo={rate}','-f','s16le','pipe:1'],input=np.round(chunk).astype(np.int16).tobytes(),capture_output=True,check=True)
 part=np.frombuffer(result.stdout,dtype=np.int16).reshape(-1,2).copy()
 mapping.append(dict(source_start=a,source_end=z,output_start=acc/SR,output_end=(acc+len(part))/SR,tempo=rate))
 parts.append(part);acc+=len(part)
out=np.concatenate(parts);n=7680;out[-n:]=np.round(out[-n:].astype(float)*np.sin(np.linspace(np.pi/2,0,n))[:,None]).astype(np.int16)
stem='supermoon_2026_11_24_vo_v02b'
with wave.open(str(HERE/(stem+'.wav')),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(out.tobytes())
def map_time(t):
 for m in mapping:
  if t<=m['source_end']:
   fraction=max(0,min(1,(t-m['source_start'])/(m['source_end']-m['source_start'])))
   return round(m['output_start']+fraction*(m['output_end']-m['output_start']),4)
 return round(len(out)/SR,4)
words=json.loads((HERE/'supermoon_2026_11_24_c7_trim1_vo_v01_words.json').read_text())
words=[dict(word=w['word'],start=map_time(w['start']),end=map_time(w['end'])) for w in words]
assert words[5]['end']<=1.5
assert words[8]['end']<=2.55
assert .16<=words[9]['start']-words[8]['end']<.25
assert 17<=len(out)/SR+1<=20
(HERE/(stem+'_words.json')).write_text(json.dumps(words,indent=2)+'\n')
report=dict(source=str(SRC),source_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(),duration_s=len(out)/SR,mapping=mapping,words_provenance='Scribe source timestamps mapped through edits; requires independent listen',new_takes=0,credits_spent=0,sha256_wav=hashlib.sha256((HERE/(stem+'.wav')).read_bytes()).hexdigest())
(HERE/(stem+'_EDIT.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));print(json.dumps(words,indent=2))
