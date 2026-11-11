#!/usr/bin/env python3
"""Build one corrected reusable narration stem, never a finished film.
Requires completed waveform alignment and master-ASR timing evidence.
No source media edits, network calls, spending, or detached processes.
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path

def run(args):
 return subprocess.run(args,check=True,capture_output=True,text=True)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--film',required=True);ap.add_argument('--alignment',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 alignment=json.loads(a.alignment.read_text())
 assert alignment['film']==a.film
 strong=[m for m in alignment['matches'] if m['correlation']>=.8]
 assert len(strong)>=(19 if a.film=='019' else 20), 'Insufficient alignment evidence'
 offset={'031':.005,'019':3.005}.get(a.film,0)
 assert all(abs(m['offset_s']-offset)<.001 for m in strong), 'Changing offsets require a laid narration reconstruction'
 assert len({m['source'] for m in strong})==1, 'Multiple sources require reconstruction'
 source=strong[0]['source']
 cut=next(c for c in json.loads(Path(__file__).with_name('corrected_audio_cuts_v01.json').read_text()) if c['film']==a.film)
 words=json.loads(Path(f'/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/j2452/asr/{a.film}_words.json').read_text())['words']
 ranges=cut['used_ranges']
 for lo,hi in ranges:
  assert not any(w['s']<t<w['e'] for t in [lo,hi] for w in words), 'A cut intersects a word'
 kept=[w for w in words if any(lo<=w['s'] and w['e']<=hi for lo,hi in ranges)]
 text=' '.join(w['w'] for w in kept)
 assert not re.search(r'\b(subscrib\w*|next week)\b',text,re.I)
 assert not any(phrase in text.lower() for phrase in ['we make one of these every week','in this film','stay with me','next, we'])
 total=sum(hi-lo for lo,hi in ranges)
 # Delay positive master/source offset before trimming on master time.
 n=len(ranges)
 parts=[f"[0:a]adelay={offset*1000}:all=1,apad=whole_dur={alignment['master_duration_s']},asplit={n}"+''.join(f"[s{i}]" for i in range(n))]
 for i,(lo,hi) in enumerate(ranges):
  parts.append(f"[s{i}]atrim={lo}:{hi},asetpts=PTS-STARTPTS[p{i}]")
 parts.append(''.join(f"[p{i}]" for i in range(n))+f"concat=n={n}:v=0:a=1,highpass=f=85,treble=g=-2.5:f=5500,acompressor=threshold=-22dB:ratio=3:attack=15:release=250:makeup=2")
 chain=';'.join(parts)
 first=run(['ffmpeg','-nostdin','-v','info','-i',source,'-filter_complex',chain+',loudnorm=I=-20.2:TP=-6.2:LRA=5:print_format=json[out]','-map','[out]','-f','null','-'])
 m=json.loads(re.findall(r'\{[^{}]+\}',first.stderr,re.S)[-1])
 norm=f"loudnorm=I=-20.2:TP=-6.2:LRA=5:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
 output=a.out/f'chapter_{a.film}_narration_v01.wav'
 assert not output.exists(), 'Versioned output already exists; preserve it'
 run(['ffmpeg','-nostdin','-v','error','-i',source,'-filter_complex',chain+','+norm+'[out]','-map','[out]','-ac','2','-ar','48000','-c:a','pcm_s24le',str(output)])
 actual_duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(output)]).stdout.strip())
 assert abs(actual_duration-total)<.001, 'Saved narration duration does not match cut timeline'
 check=run(['ffmpeg','-nostdin','-v','info','-i',str(output),'-af','loudnorm=I=-20.2:TP=-6.2:LRA=5:print_format=json','-f','null','-'])
 levels=json.loads(re.findall(r'\{[^{}]+\}',check.stderr,re.S)[-1])
 assert -20.7<=float(levels['input_i'])<=-19.7 and float(levels['input_tp'])<=-6
 report=dict(status='NARRATION_CHECKPOINT_ONLY',alignment_file=str(a.alignment),alignment_sha256=hashlib.sha256(a.alignment.read_bytes()).hexdigest(),source=source,source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),output=str(output),output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),film=a.film,plan_ranges=cut['plan_ranges'],source_offset_s=offset,used_ranges=ranges,duration_s=total,levels=levels,kept_transcript=text,removed_transcript=' '.join(w['w'] for w in words if not any(lo<=w['s'] and w['e']<=hi for lo,hi in ranges)),remaining='Picture, covers, diagrams/cards removal, continuous bed and final master gates are not built or passed.')
 (a.out/f'chapter_{a.film}_narration_v01.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['status','output','duration_s','output_sha256','levels']},indent=2))
if __name__=='__main__':main()
