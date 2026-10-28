#!/usr/bin/env python3
"""Recover interpreter-only gate failures and independently transcribe final AAC locally."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
D=Path('/Users/benjaminoats/_desk/renders/J1100-attempt03/S5_028_jJ5LkFGyzLI')
V=D/'S5_028_jJ5LkFGyzLI_v05.mp4'
def main():
 summary=json.loads((D/'FINAL_MEASUREMENTS.json').read_text())
 (D/'FINAL_MEASUREMENTS_initial_interpreter_failures.json').write_text(json.dumps(summary,indent=2)+'\n')
 cmds={
 'picture':[ROOT/'scripts/picture_qa.py',V,'--cuts',D/'cuts.json','--pool',D/'pool.json','--out-dir',D/'picture_qa'],
 'polish':[ROOT/'scripts/polish_gate.py',V,'--cuts',D/'cuts.json','--out',D/'polish_gate.json'],
 'music':[ROOT/'scripts/music_gate.py',ROOT/'02_Video-Projects/028_A-Star-Is-Coming-Toward-Us','--bed',ROOT/'02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/05_Music/gliese_score_bed_v03.mp3','--video',V,'--out',D/'music_gate.json']}
 for name,args in cmds.items():
  print(name,flush=True)
  with (D/(name+'_py314.log')).open('w') as f:r=subprocess.run([sys.executable,*map(str,args)],stdout=f,stderr=subprocess.STDOUT)
  summary[name]={'exit_code':r.returncode,'log':str(D/(name+'_py314.log'))}
 (D/'FINAL_MEASUREMENTS.json').write_text(json.dumps(summary,indent=2)+'\n')
 # A transcript of the delivered AAC, independent of the script or timing map. No cloud API.
 from faster_whisper import WhisperModel
 model=WhisperModel('base.en',device='cpu',compute_type='int8',download_root='/Users/benjaminoats/_desk/cache/whisper')
 import numpy as np
 audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(V),'-ar','16000','-ac','1','-f','f32le','-']),dtype=np.float32)
 segments,info=model.transcribe(audio,language='en',beam_size=5,temperature=0,condition_on_previous_text=False,word_timestamps=True)
 segments=list(segments)
 out={'status':'ASR evidence only; human listening and caption comparison still required','model':'base.en','input':str(V),'text':' '.join(s.text.strip() for s in segments),'segments':[{'start':s.start,'end':s.end,'text':s.text,'words':[{'word':w.word,'start':w.start,'end':w.end,'probability':w.probability} for w in s.words]} for s in segments]}
 (D/'final_AAC_ASR.json').write_text(json.dumps(out,indent=2)+'\n');print(out['text'],flush=True)
if __name__=='__main__':main()
