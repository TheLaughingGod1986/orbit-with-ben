#!/usr/bin/env python3
"""J2478 Chief natural-speed ruling, 11 November 05:54Z; timing edit; existing locked take only, no API calls.
Word times are mapped from Scribe, not a new perceptual/ASR review.
"""
import hashlib,json,wave
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
SRC=HERE/'supermoon_2026_11_24_c7_trim1_vo_v01.wav'
assert hashlib.sha256(SRC.read_bytes()).hexdigest()=='95a24bc9c4b1352f333c121e96d88483afd7688229e037ba9a51958feeb9f385'
SR=48000
# Source in/out; rate is asserted 1.0. No resampling or tempo processing.
SPANS=[(.03,.185,1.),(.22,.585,1.),(.66,1.105,1.),(1.20,1.425,1.),(1.58,1.985,1.),(2.06,2.585,1.),
       (2.78,3.385,1.),(3.475,4.265,1.),
       (5.065,6.45,1.),(6.67,8.65,1.),(8.9,11.7,1.),(11.85,17.3,1.),(17.77,20.,1.)]
assert all(rate == 1. for _,_,rate in SPANS)
# Last date chunk has 25ms postroll and If chunk 155ms preroll: 180ms breath.
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
 part=np.round(chunk).astype(np.int16)
 mapping.append(dict(source_start=a,source_end=z,output_start=acc/SR,output_end=(acc+len(part))/SR,tempo=rate))
 parts.append(part);acc+=len(part)
out=np.concatenate(parts);n=7680;out[-n:]=np.round(out[-n:].astype(float)*np.sin(np.linspace(np.pi/2,0,n))[:,None]).astype(np.int16)
stem='supermoon_2026_11_24_vo_v02d'
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
# Scribe missed the onset of 'twenty'; waveform shows onset at source 3.49s.
words[8]['start']=map_time(3.49)
assert words[0]['start'] <= .15
assert words[5]['end'] <= 2.8
assert words[9]['start'] <= 4.8
assert all(.039 <= words[i+1]['start']-words[i]['end'] <= .051 for i in range(7))
assert 0 <= words[8]['start']-words[7]['end'] <= .15
assert .139 <= words[14]['start']-words[13]['end'] <= .141
assert .16<=words[9]['start']-words[8]['end']<.25
assert 17<=len(out)/SR+1<=20
(HERE/(stem+'_words.json')).write_text(json.dumps(words,indent=2)+'\n')
report=dict(source=str(SRC),source_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(),duration_s=len(out)/SR,mapping=mapping,words_provenance='Scribe source timestamps mapped through edits; no resampling or tempo filter; requires output ASR and final watch',new_takes=0,credits_spent=0,sha256_wav=hashlib.sha256((HERE/(stem+'.wav')).read_bytes()).hexdigest())
(HERE/(stem+'_EDIT.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));print(json.dumps(words,indent=2))
