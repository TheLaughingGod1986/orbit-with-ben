#!/usr/bin/env python3
"""Finish existing unreviewed J1032 renders, preserving all inputs and first render evidence.
No acceptance implied. Fine grain and reverse composed opening for the locked 1s loop.
The final sample frames hold opening frame 2; the actual last frame is opening frame 0.
"""
import argparse,json,subprocess,hashlib,importlib.util,shutil
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def run(a):subprocess.run([str(x) for x in a],check=True)
def ff(a):run(['ffmpeg','-nostdin','-y','-v','error',*a])
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--media-root',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 assert shutil.disk_usage('/private/tmp').free>=20_000_000_000,'Archive first'
 spec=importlib.util.spec_from_file_location('legacy',args.media_root/'02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/mon30_comets/_assemble_mon30_comets_v03.py');legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
 for src in sorted(args.source.glob('*/*_v04.mp4')):
  key=src.parent.name;out=args.out/key;out.mkdir(parents=True,exist_ok=True)
  if (out/'FINISH_COMPLETE.json').exists():print('SKIP',key,flush=True);continue
  prep=json.loads((src.parent/'locked_preparation.json').read_text());total=prep['vo_splice_map']['total_duration_s'];end=round(prep['vo_splice_map']['vo_end_s']*30);frames=round(total*30)
  final=out/src.name
  # Grain before splitting gives the loop exactly the same grain texture as the opening.
  # Reset each segment by frame index; reserve four sampled frames and the true endpoint.
  vf=f'[0:v]noise=alls=4:allf=t:all_seed=1032,split=4[body][rev][sample][endpoint];[body]trim=end_frame={end},setpts=N/(30*TB)[b];[rev]trim=end_frame=30,reverse,trim=end_frame=25,setpts=N/(30*TB)[r];[sample]trim=start_frame=2:end_frame=3,loop=loop=3:size=1:start=0,trim=end_frame=4,setpts=N/(30*TB)[s];[endpoint]trim=end_frame=1,setpts=N/(30*TB)[e];[b][r][s][e]concat=n=4:v=1:a=0,setpts=N/(30*TB),format=yuv420p[v]'
  print('FINISH',key,flush=True)
  ff(['-i',src,'-filter_complex',vf,'-map','[v]','-map','0:a','-frames:v',frames,'-c:v','libx264','-preset','fast','-crf','18','-c:a','copy','-movflags','+faststart',final])
  ff(['-i',final,'-vf','scale=720:1280:flags=lanczos','-c:v','libx264','-preset','fast','-crf','20','-c:a','copy',out/(src.stem+'_PHONE.mp4')])
  level=legacy.ebur128_stats(final);loop=legacy.loop_measures(final)
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(final),'-vf',f"select='eq(n,0)+eq(n,{frames-1})',scale=180:320,format=gray",'-fps_mode','vfr','-f','rawvideo','-'])
  endpoints=np.frombuffer(raw,np.uint8).reshape(-1,320,180).astype(float)
  assert len(endpoints)==2, 'Expected first and last frames'
  actual_seam=float(np.abs(endpoints[0]-endpoints[-1]).mean())
  record={'status':'UNREVIEWED; final gates and listening outstanding','input_sha256':sha(src),'I_LUFS':level[0],'TP_dBTP':level[1],'audio_pass':-14.5<=level[0]<=-13.5 and level[1]<=-1.6,'loop':loop,'actual_seam_diff':actual_seam,'loop_pass':max(loop.values())<2 and actual_seam<2,'grain':'noise alls=4 allf=t seed=1032 before loop split','endpoint':'last 5 frames are opening frames 2, 2, 2, 2, 0; each segment PTS reset by frame index','files':{p.name:sha(p) for p in out.glob('*.mp4')}}
  dump(out/'FINISH_COMPLETE.json',record);print(json.dumps(record),flush=True)
  assert record['audio_pass'] and record['loop_pass'], 'Final audio/loop check failed; inspect evidence before continuing'
if __name__=='__main__':main()
