#!/usr/bin/env python3
"""Read-only ASR timing evidence for existing narration; never approval or new VO."""
import argparse,json,subprocess
import numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--film',choices=['013','021'],required=True);p.add_argument('--model',required=True);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=True)
row=json.loads((HERE/'alignment_v02'/f'{a.film}_alignment.json').read_text())
m=WhisperModel(a.model,device='cpu',compute_type='int8',cpu_threads=4)
for i,src in enumerate(row['narration']):
 out=a.out/f'{a.film}_{i+1}_asr.json'
 if out.exists():continue
 audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',src,'-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32).copy()
 segments,info=m.transcribe(audio,language='en',word_timestamps=True,beam_size=5,vad_filter=False)
 data=[]
 for s in segments:
  data.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(w=w.word,s=w.start,e=w.end,p=w.probability) for w in s.words]))
 out.write_text(json.dumps(dict(source=src,model=a.model,segments=data,warning='ASR timing aid; validate sentence cuts with waveform pauses and locked script'),indent=2)+'\n')
 print(out,flush=True)
