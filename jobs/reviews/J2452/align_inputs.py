#!/usr/bin/env python3
"""J2452 read-only waveform alignment. No generation, source edits or background jobs.
Run using _desk/J2141-venv/bin/python (numpy), with --out under local _desk.
Sparse correlations are alignment evidence, not approval of cuts or source identity.
"""
import argparse, json, re, subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
LIVE=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects')
ARCH=Path('/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects')
ORDER=['013','021','027','025','023','031','020','022','028','029','024','026','019']
def decode(p):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','4000','-f','f32le','-']),np.float32).astype(np.float64)
def only(base,pattern):
 a=list(base.glob(pattern)); assert len(a)==1,(pattern,a);return a[0]
def inventory():
 old=json.loads((LIVE/'_sleep_video_01/j2452/inputs.json').read_text())
 masters={j['film']:j['file'] for j in old}
 text=(ROOT/'05_Analytics/owb/SLEEP_VIDEO_01_NAS_INPUT_CHECK.md').read_text()
 for film in ['013','023','022']:
  line=next(l for l in text.splitlines() if l.startswith('| ') and f'`{film}`' in l and '.mp4`' in l)
  masters[film]=re.search(r'`(/Volumes/[^`]+\.mp4)`',line)[1]
 masters['021']=str(only(LIVE,'021*/07_Edit-Project/saturn_film/saturn_first_cut_v03f.mp4'))
 stems={
 '013':sorted(p for p in ARCH.glob('013*/02_Voiceover/parts/*.wav') if not p.name.startswith('._')),
 '021':[Path('/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-021/work_first_cut_v03f/vo_timeline.wav')],
 '027':[Path('/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-15/earth027_v_before_last/earth027_score_v01i/stem_vo_v01i.wav')],
 '023':[only(LIVE,'023*/02_Voiceover/venus_vo_v01.wav')],
 '024':[only(LIVE,'024*/02_Voiceover/light_speed_vo_v01.wav')],
 '025':[only(LIVE,'025*/02_Voiceover/mars_robot_vo_v01.wav')],
 '026':[only(LIVE,'026*/02_Voiceover/nearest_star_vo_v01.wav')],
 '031':[only(LIVE,'031*/07_Edit-Project/full_master_v02_work/vo_laid_v02.wav')],
 '020':[only(ARCH,'020*/02_Voiceover/jupiter_vo_v01.mp3')],
 '022':[only(ARCH,'022*/02_Voiceover/parts/sun_brighter_vo_v01.wav')],
 '028':[only(LIVE,'028*/02_Voiceover/star_coming_vo_v01.wav'),only(LIVE,'028*/02_Voiceover/J1100_s5_open_pickup_v01.wav')],
 '029':[only(LIVE,'029*/02_Voiceover/betelgeuse_vo_v01.wav')],
 '019':[only(ARCH,'019*/02_Voiceover/parts/andromeda_collision_vo_v03_full.wav')]}
 return [dict(film=f,master=masters[f],narration=[str(p) for p in stems[f]],upload_sha256=next((j.get('sha256_recorded') for j in old if j['film']==f),None)) for f in ORDER]
def align(row,out):
 m=decode(row['master']); sources=[decode(p) for p in row['narration']]
 # Precompute FFT and window energies for normalized matched filtering.
 size=16000
 cache=[]
 for x in sources:
  n=1<<(len(x)+size-1).bit_length();cs=np.r_[0,np.cumsum(x)];sq=np.r_[0,np.cumsum(x*x)]
  energy=sq[size:]-sq[:-size]-(cs[size:]-cs[:-size])**2/size
  cache.append((x,n,np.fft.rfft(x,n),np.maximum(energy,1e-20)))
 matches=[]
 for t in range(5,int(len(m)/4000)-5,20):
  q=m[t*4000:t*4000+size].copy();q-=q.mean();qe=np.dot(q,q)
  if qe<1e-9:continue
  candidates=[]
  for i,(x,n,xf,energy) in enumerate(cache):
   if len(x)<size:continue
   c=np.fft.irfft(xf*np.fft.rfft(q[::-1],n),n)[size-1:len(x)]/np.sqrt(energy*qe)
   c[energy < max(float(energy.max())*1e-5, 1e-10)] = -1
   k=int(np.argmax(c));candidates.append(dict(source=row['narration'][i],source_s=k/4000,correlation=round(float(c[k]),6)))
  best=max(candidates,key=lambda c:c['correlation']);best.update(master_s=t,offset_s=round(t-best['source_s'],5));matches.append(best)
 result=dict(**row,master_duration_s=len(m)/4000,matches=matches,warning='Sparse waveform matches only. Do not interpolate across changing offsets. All sentence cuts and cover windows still need validation.')
 (out/f"{row['film']}_alignment.json").write_text(json.dumps(result,indent=2)+'\n')
 print(row['film'], 'samples',len(matches),'strong',sum(x['correlation']>=.8 for x in matches),'min',min(x['correlation'] for x in matches),flush=True)
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',required=True,type=Path);a.add_argument('--film',action='append');args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 rows=inventory()
 for row in rows:
  for p in [row['master']]+row['narration']:assert Path(p).is_file(),p
 (args.out/'inputs_v01.json').write_text(json.dumps(rows,indent=2)+'\n')
 for row in rows:
  if args.film and row['film'] not in args.film:continue
  if (args.out/f"{row['film']}_alignment.json").exists(): print(row['film'],'existing checkpoint; skipped',flush=True);continue
  align(row,args.out)
if __name__=='__main__':main()
