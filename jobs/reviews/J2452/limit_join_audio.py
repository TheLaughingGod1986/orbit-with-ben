#!/usr/bin/env python3
"""Bounded peak-limited final mix; independently measure the saved PCM output."""
import argparse,json,re,subprocess as sp
from pathlib import Path
from join_public_chapters import sha

def run(args,log):
 with log.open('w') as f:
  sp.run(['ffmpeg','-hide_banner','-nostdin','-n','-filter_threads','2',*map(str,args)],stdout=f,stderr=sp.STDOUT,check=True,timeout=240)
def summary(text):
 s=text[text.rfind('Summary:'):]
 return dict(integrated_lufs=float(re.search(r'I:\s*([-\d.]+) LUFS',s)[1]),lra_lu=float(re.search(r'LRA:\s*([-\d.]+) LU',s)[1]),true_peak_dbtp=float(re.search(r'Peak:\s*([-\d.]+) dBFS',s)[1]))
def main():
 p=argparse.ArgumentParser();p.add_argument('--scratch',type=Path,required=True);p.add_argument('--raw-measurement',type=Path,required=True);a=p.parse_args();out=a.scratch/'final_join_v01'
 original=summary(a.raw_measurement.read_text());gain=-20-original['integrated_lufs'];target=out/'sleep_audio_master_candidate_v02.wav'
 timeline=json.loads((out/'TIMELINE.json').read_text());duration=timeline['duration_s']
 if not target.exists():
  # Four-times oversampling places the limiter before downsampling; the extra
  # 0.5 dB ceiling margin is still checked with an independent true-peak pass.
  run(['-i',out/'sleep_mix_pre_master_v01.wav','-af',f'volume={gain}dB,aresample=192000,alimiter=limit=0.473151258961:attack=5:release=50:level=false:latency=true,aresample=48000','-t',duration,'-c:a','pcm_s24le',target],out/'AUDIO_LIMIT.log')
 log=out/'AUDIO_SAVED_EBUR128.log'
 run(['-i',target,'-af','ebur128=peak=true,silencedetect=n=-60dB:d=3','-f','null','-'],log)
 text=log.read_text();m=summary(text);gaps=re.findall(r'silence_duration: ([0-9.]+)',text)
 actual=float(json.loads(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(target)]))['format']['duration'])
 ok=-20.5<=m['integrated_lufs']<=-19.5 and m['true_peak_dbtp']<=-6 and m['lra_lu']<=5 and not gaps and abs(actual-duration)<.001
 report=dict(status='PASS_PCM_AUDIO_ONLY' if ok else 'FAIL',path=str(target),sha256=sha(target),duration_s=actual,raw_levels=original,gain_db=gain,limiter=dict(oversample_hz=192000,ceiling_db=-6.5,attack_ms=5,release_ms=50,latency_compensated=True),saved_levels=m,silence_over_3s=gaps,limitations='Final AAC read-back, CTA audit and picture/join gates remain required. No listening claim.')
 (out/'AUDIO_READBACK_V02.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True);assert ok
if __name__=='__main__':main()
