#!/usr/bin/env python3
"""Build only Moon/Saturn narration intermediates from measured sentence pauses.
Requires the local ASR evidence directory produced by transcribe_remaining.py.
Does not overwrite media, modify source films, add music or claim final QA.
"""
import argparse,json,re,subprocess,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent

def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--film',choices=['013','021'],required=True);ap.add_argument('--asr',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 a.out.mkdir(parents=True,exist_ok=True)
 alignment=json.loads((HERE/'alignment_v02'/f'{a.film}_alignment.json').read_text())
 sources=alignment['narration']
 durations=[float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',s]).stdout) for s in sources]
 if a.film=='013':
  offsets=[.02625,95.33875,240.133,382.82675]
  recipes=[(0,2.5,20.6),(0,46.7,durations[0]),(1,0,durations[1]),(2,0,durations[2]),(3,0,92.15),(3,104.3,durations[3])]
  plan=[[3,21.4],[34.2,500.8]]
 else:
  offsets=[0];recipes=[(0,0,9.6),(0,21.0,209.65),(0,219.55,540.2)]
  plan=[[0,8.95],[21.55,209.65],[219.55,540.2]]
 evidence=[];allwords=[]
 for i,src in enumerate(sources):
  asrfile=a.asr/f'{a.film}_{i+1}_asr.json';j=json.loads(asrfile.read_text());assert j['source']==src
  words=[w for s in j['segments'] for w in s['words']];allwords.append(words)
  sil=run(['ffmpeg','-nostdin','-v','info','-i',src,'-af','silencedetect=n=-38dB:d=0.12','-f','null','-'])
  ints=[];start=None
  for kind,val in re.findall(r'silence_(start|end): ([\d.]+)',sil.stderr):
   if kind=='start':start=float(val)
   elif start is not None:ints.append([start,float(val)]);start=None
  checks=[]
  for idx,lo,hi in recipes:
   if idx!=i:continue
   for t in [lo,hi]:
    if t==0 or abs(t-durations[i])<.001:continue
    assert not any(w['s']<t<w['e'] for w in words),(src,t,'ASR word interior')
    pauses=[v for v in ints if v[0]<=t<=v[1]];assert pauses,(src,t,'not measured silence')
    checks.append(dict(time_s=t,pauses=pauses,previous=next((w for w in reversed(words) if w['e']<=t),None),next=next((w for w in words if w['s']>=t),None)))
  evidence.append(dict(source=src,sha256=digest(src),duration_s=durations[i],asr_file=str(asrfile),asr_sha256=digest(asrfile),boundaries=checks))
 kept=[];removed=[]
 for i,words in enumerate(allwords):
  for w in words:
   (kept if any(idx==i and lo<=w['s'] and w['e']<=hi for idx,lo,hi in recipes) else removed).append(w['w'].strip())
 transcript=' '.join(kept)
 assert not re.search(r'\b(subscrib\w*|next week|next,|in this film|stay with me|orbit stands|then orbit looks)\b',transcript,re.I)
 # Split each input only as often as needed; concatenate complete sentence ranges.
 filters=[];counts={i:sum(idx==i for idx,_,_ in recipes) for i in range(len(sources))};labels={}
 for i,n in counts.items():
  filters.append(f'[{i}:a]asplit={n}'+''.join(f'[s{i}_{k}]' for k in range(n)));labels[i]=0
 for k,(i,lo,hi) in enumerate(recipes):
  n=labels[i];labels[i]+=1;filters.append(f'[s{i}_{n}]atrim={lo}:{hi},asetpts=PTS-STARTPTS[p{k}]')
 filters.append(''.join(f'[p{k}]' for k in range(len(recipes)))+f'concat=n={len(recipes)}:v=0:a=1,highpass=f=85,treble=g=-2.5:f=5500,acompressor=threshold=-22dB:ratio=3:attack=15:release=250:makeup=2')
 chain=';'.join(filters);inputs=[x for s in sources for x in ['-i',s]];target='loudnorm=I=-20.2:TP=-6.2:LRA=5'
 first=run(['ffmpeg','-nostdin','-v','info',*inputs,'-filter_complex',chain+','+target+':print_format=json[out]','-map','[out]','-f','null','-'])
 m=json.loads(re.findall(r'\{[^{}]+\}',first.stderr,re.S)[-1]);norm=target+f':measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true'
 output=a.out/f'chapter_{a.film}_narration_v01.wav';assert not output.exists()
 run(['ffmpeg','-nostdin','-n','-v','error',*inputs,'-filter_complex',chain+','+norm+'[out]','-map','[out]','-ac','2','-ar','48000','-c:a','pcm_s24le',str(output)])
 check=run(['ffmpeg','-nostdin','-v','info','-i',str(output),'-af',target+':print_format=json','-f','null','-']);levels=json.loads(re.findall(r'\{[^{}]+\}',check.stderr,re.S)[-1])
 assert -20.5<=float(levels['input_i'])<=-19.5 and float(levels['input_tp'])<=-6
 duration=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(output)]).stdout);assert abs(duration-sum(hi-lo for _,lo,hi in recipes))<.002
 report=dict(status='NARRATION_INTERMEDIATE_ONLY',film=a.film,plan_master_ranges=plan,source_recipes=[dict(source=sources[i],source_in_s=lo,source_out_s=hi,master_in_s=round(lo+offsets[i],6),master_out_s=round(hi+offsets[i],6)) for i,lo,hi in recipes],evidence=evidence,output=str(output),output_sha256=digest(output),duration_s=duration,levels=levels,kept_transcript=transcript,removed_transcript=' '.join(removed),remaining='Picture covers, music bed, transitions, final master/reel and gates; no listening claim')
 (a.out/f'chapter_{a.film}_narration_v01.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(film=a.film,output=str(output),duration_s=duration,levels=levels),indent=2))
if __name__=='__main__':main()
