#!/usr/bin/env python3
"""Independent transcript of decoded final AAC; no API, no script supplied to ASR."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
p=argparse.ArgumentParser();p.add_argument('video',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
model=WhisperModel('base.en',device='cpu',compute_type='int8',download_root='/Users/benjaminoats/_desk/cache/whisper',local_files_only=True)
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(a.video),'-ar','16000','-ac','1','-f','f32le','-']),dtype=np.float32)
segments,_=model.transcribe(audio,language='en',beam_size=5,temperature=0,condition_on_previous_text=False,word_timestamps=True);segments=list(segments)
out={'status':'ASR evidence only; does not satisfy listening by ear','input':str(a.video),'model':'base.en','text':' '.join(s.text.strip() for s in segments),'segments':[{'start':s.start,'end':s.end,'text':s.text,'words':[{'word':w.word,'start':w.start,'end':w.end} for w in s.words]} for s in segments]}
a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['text'])
