#!/usr/bin/env python3
"""Two-pass sleep mix normalization, followed by independent saved-file gates."""
import argparse,json,re,subprocess as sp
from pathlib import Path
from join_public_chapters import sha

def ff(args):
 p=sp.run(['ffmpeg','-v','info','-nostdin','-n',*map(str,args)],capture_output=True,text=True,check=True,timeout=300)
 return p.stderr

def levels(log):return json.loads(re.findall(r'\{[^{}]+\}',log,re.S)[-1])
def main():
 p=argparse.ArgumentParser();p.add_argument('--scratch',type=Path,required=True);a=p.parse_args();out=a.scratch/'final_join_v01'
 raw=out/'sleep_mix_pre_master_v01.wav';measurement=out/'MIX_FIRST_PASS.json'
 if measurement.exists():m=json.loads(measurement.read_text())
 else:
  m=levels(ff(['-i',raw,'-af','loudnorm=I=-20:TP=-6.2:LRA=5:print_format=json','-f','null','-']));measurement.write_text(json.dumps(m,indent=2)+'\n')
 print('first pass',m,flush=True)
 filt='loudnorm=I=-20:TP=-6.2:LRA=5:linear=true:'+':'.join(f'{k}={m[v]}' for k,v in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])
 target=out/'sleep_audio_master_candidate_v01.wav'
 if not target.exists():ff(['-i',raw,'-af',filt,'-ar','48000','-c:a','pcm_s24le',target])
 log=ff(['-i',target,'-af','loudnorm=I=-20:TP=-6.2:LRA=5:print_format=json,silencedetect=n=-60dB:d=3','-f','null','-']);(out/'AUDIO_GATE.log').write_text(log)
 m=levels(log);gaps=re.findall(r'silence_duration: ([0-9.]+)',log)
 duration=float(json.loads(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(target)]))['format']['duration'])
 expected=json.loads((out/'TIMELINE.json').read_text())['duration_s']
 verdict=(-20.5<=float(m['input_i'])<=-19.5 and float(m['input_tp'])<=-6 and not gaps and abs(duration-expected)<.001)
 report=dict(status='PASS_AUDIO_ONLY' if verdict else 'FAIL',path=str(target),sha256=sha(target),duration_s=duration,expected_duration_s=expected,measured_saved_levels=m,silence_over_3s=gaps,limitations='Final AAC read-back, full picture decode, join QA, CTA audit, reel and NAS copies remain required. No listening claim.')
 (out/'AUDIO_READBACK.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True);assert verdict
if __name__=='__main__':main()
