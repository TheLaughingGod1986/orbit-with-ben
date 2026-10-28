#!/usr/bin/env python3
"""No-spend diagnostic auditions; not accepted VO or replacement masters."""
import copy, hashlib, json, subprocess, wave
from pathlib import Path
import numpy as np
ROOT=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
OUT=Path('/Users/benjaminoats/_desk/reviews/J1100/audio_candidates')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','48000','-f','s16le','-']),np.int16).copy()
def save(p,a):
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(a.astype(np.int16).tobytes())
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 maps=json.loads((ROOT/'jobs/reviews/J0936_v04_PREP_v07_maps.json').read_text())['shorts']
 records={}
 for key in ['S2_027_emwQsPxnRGM','S6_028_X768qs8sNQs']:
  s=copy.deepcopy(maps[key]);v=s['vo_splice_map'];src=ROOT/Path(v['vo_source_path']);data=pcm(src)
  spans=v['subspans'];opening=v['opening_question_span_count'];changes=[]
  if key.startswith('S2'):
   # Sentence boundaries only; preserve every existing spoken sample and within-sentence splice.
   spans[6]['gap_after']=.65;spans[9]['gap_after']=.50
   changes=['Question-end pause 0.18 -> 0.65s.','Answer-end pause 0.18 -> 0.50s.','Existing fragment prosody retained; actual listening required before deciding whether the permitted post-reset pickup is needed.']
  else:
   # Restore native continuous "look like when" rather than shortened replacement "like".
   # Preserve the exact accepted words and question order. No time stretching anywhere.
   old=spans[:opening];spec=[(39.22,39.36,[old[0]['words'][0]]),(40.20,40.34,old[1]['words']),(338.78,338.86,old[2]['words']),(39.60,40.14,old[3]['words']),(40.40,41.16,old[4]['words']+old[5]['words']+old[6]['words']),(43.50,44.54,old[7]['words']),(41.30,41.86,old[8]['words'])]
   new=[]
   for i,(a,b,words) in enumerate(spec):
    words=copy.deepcopy(words)
    if i==4:
     for w,ab in zip(words,[(40.4,40.58),(40.64,41.02),(41.06,41.16)]):w['src_start'],w['src_end']=ab
    new.append({'source_in':a,'source_out':b,'tempo':1.0,'gap_after':.10 if i<6 else .30,'words':words,'text':' '.join(w['word'] for w in words)})
   spans=new+spans[opening:];opening=7
   changes=['Restored native continuous phrase look like when at 40.40-41.16s.','Question boundaries spaced 0.10s; end pause 0.30s; no atempo.','Diagnostic only: longer named-subject timing conflicts with old <=2.5s preparation lock; requires Chief ruling or a newly authorized complete-question pickup.']
  pieces=[];now=v['onset_s'];pieces.append(np.zeros(round(now*48000),np.int16));words=[]
  for sp in spans:
   assert sp['tempo']==1.0
   a,b=sp['source_in'],sp['source_out'];seg=data[round(a*48000):round(b*48000)].copy()
   # Same 5ms edge fades as accepted builder; do not trim phonemes further.
   n=min(240,len(seg)//4);seg[:n]=(seg[:n]*np.linspace(0,1,n)).astype(np.int16);seg[-n:]=(seg[-n:]*np.linspace(1,0,n)).astype(np.int16)
   sp['timeline_start']=now;sp['timeline_end']=now+(b-a)
   for w in sp['words']:
    w=copy.deepcopy(w);w['start']=now+w['src_start']-a;w['end']=now+w['src_end']-a;words.append(w)
   pieces.append(seg);gap=sp['gap_after'];pieces.append(np.zeros(round(gap*48000),np.int16));now+=b-a+gap
  out=OUT/(key+'_candidate.wav');
  if not out.exists():save(out,np.concatenate(pieces))
  else:
   with wave.open(str(out),'rb') as existing:assert existing.readframes(existing.getnframes())==np.concatenate(pieces).astype(np.int16).tobytes(),'Existing candidate differs'
  question_end=spans[opening-1]['timeline_end'];subject_end=next(w['end'] for w in words if w['word'].strip('.,?!') in ['710','equator'])
  records[key]={'status':'DIAGNOSTIC ONLY; no listening, acceptance, final media or gate claim','file':str(out),'sha256':sha(out),'source':str(src),'source_sha256':sha(src),'changes':changes,'question_end_s':question_end,'named_subject_end_s':subject_end,'duration_with_1s_loop_s':now+1,'words':words,'subspans':spans}
 (OUT/'CANDIDATES.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps({k:{a:v[a] for a in ['file','sha256','question_end_s','named_subject_end_s','duration_with_1s_loop_s']} for k,v in records.items()},indent=2))
if __name__=='__main__':main()
