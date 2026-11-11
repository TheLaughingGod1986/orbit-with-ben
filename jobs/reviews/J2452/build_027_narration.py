#!/usr/bin/env python3
"""Build the reusable chapter-03 narration stem only, never a finished film.
Requires completed waveform alignment and master-ASR timing evidence.
No source media edits, network calls, spending, or detached processes.
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path

def run(args):
 return subprocess.run(args,check=True,capture_output=True,text=True)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--alignment',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 alignment=json.loads(a.alignment.read_text())
 assert alignment['film']=='027'
 assert all(m['correlation']>=.95 and abs(m['offset_s'])<.001 for m in alignment['matches']), 'Laid narration does not match master at zero offset'
 source=alignment['narration'][0]
 words=json.loads(Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/j2452/asr/027_words.json').read_text())['words']
 ranges=[[0,164.45],[169.90,443.50]]
 for lo,hi in ranges:
  assert not any(w['s']<t<w['e'] for t in [lo,hi] for w in words), 'A cut intersects a word'
 kept=[w for w in words if any(lo<=w['s'] and w['e']<=hi for lo,hi in ranges)]
 text=' '.join(w['w'] for w in kept)
 assert not re.search(r'\b(subscrib\w*|next week)\b',text,re.I)
 assert 'We make one of these every week' not in text
 total=sum(hi-lo for lo,hi in ranges)
 chain='[0:a]asplit=2[a][b];[a]atrim=0:164.45,asetpts=PTS-STARTPTS[a0];[b]atrim=169.90:443.50,asetpts=PTS-STARTPTS[b0];[a0][b0]concat=n=2:v=0:a=1,highpass=f=85,treble=g=-2.5:f=5500,acompressor=threshold=-22dB:ratio=3:attack=15:release=250:makeup=2'
 first=run(['ffmpeg','-nostdin','-v','info','-i',source,'-filter_complex',chain+',loudnorm=I=-20.2:TP=-6.2:LRA=5:print_format=json[out]','-map','[out]','-f','null','-'])
 m=json.loads(re.findall(r'\{[^{}]+\}',first.stderr,re.S)[-1])
 norm=f"loudnorm=I=-20.2:TP=-6.2:LRA=5:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
 output=a.out/'chapter_03_027_narration_v01.wav'
 assert not output.exists(), 'Versioned output already exists; preserve it'
 run(['ffmpeg','-nostdin','-v','error','-i',source,'-filter_complex',chain+','+norm+'[out]','-map','[out]','-ac','2','-ar','48000','-c:a','pcm_s24le',str(output)])
 check=run(['ffmpeg','-nostdin','-v','info','-i',str(output),'-af','loudnorm=I=-20.2:TP=-6.2:LRA=5:print_format=json','-f','null','-'])
 levels=json.loads(re.findall(r'\{[^{}]+\}',check.stderr,re.S)[-1])
 assert -20.7<=float(levels['input_i'])<=-19.7 and float(levels['input_tp'])<=-6
 report=dict(status='NARRATION_CHECKPOINT_ONLY',source=source,source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),output=str(output),output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),plan_ranges=[[0,164.90],[169.42,443.50]],used_ranges=ranges,duration_s=total,levels=levels,kept_transcript=text,removed_transcript=' '.join(w['w'] for w in words if 164.45<=w['s'] and w['e']<=169.90),remaining='Picture, covers, diagrams/cards removal, continuous bed and final master gates are not built or passed.')
 (a.out/'chapter_03_027_narration_v01.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['status','output','duration_s','output_sha256','levels']},indent=2))
if __name__=='__main__':main()
