#!/usr/bin/env python3
"""Restore S5 opening captions over accepted v04; preserve AAC and all existing timing.
Produces unreviewed media only. Does not publish, deliver, or waive any gate.
"""
import hashlib, importlib.util, json, shutil, subprocess
from pathlib import Path
from PIL import Image
ROOT=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
OUT=Path('/Users/benjaminoats/_desk/renders/J1100-attempt03/S5_028_jJ5LkFGyzLI')
SOURCE=Path('/Users/benjaminoats/_desk/renders/J1032/S5_028_jJ5LkFGyzLI')
SRC=Path('/Users/benjaminoats/_desk/renders/J1032-finish12/S5_028_jJ5LkFGyzLI/S5_028_jJ5LkFGyzLI_v04.mp4')
KEY='S5_028_jJ5LkFGyzLI'
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ff(a):subprocess.run(['ffmpeg','-nostdin','-v','error','-y',*map(str,a)],check=True)
def ah(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
def main():
 assert shutil.disk_usage(ROOT).free>=20_000_000_000,'Disk below 20GB'
 OUT.mkdir(parents=True,exist_ok=True)
 assert not (OUT/'FINISH_COMPLETE.json').exists(),'Already complete; inspect rather than duplicate'
 m=load('drawing',ROOT/'jobs/reviews/render_j1032_v04.py')
 legacy=load('legacy',ROOT/'02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/mon30_comets/_assemble_mon30_comets_v03.py')
 prep=json.loads((SOURCE/'locked_preparation.json').read_text())
 words=[w for sp in prep['vo_splice_map']['subspans'] for w in sp['words']]
 groups=[];g=[]
 for w in words:
  g.append(w)
  if len(g)==3 or w['word'][-1:] in '.,?!':groups.append(g);g=[]
 if g:groups.append(g)
 layers=OUT/'opening_caption_layers';layers.mkdir(exist_ok=True)
 opening=prep['shot_plan'][0]
 opening_frames=round(opening['timeline_out']*30)
 hook=Image.open(Path('/Users/benjaminoats/_desk/reviews/J1017/openings')/(KEY+'_v04_overlay.png')).convert('RGBA')
 # The accepted overlay itself contains a static opening caption. Rebuild this code layer.
 hook.paste((0,0,0,0),(0,1400,1080,1920))
 for n in range(opening_frames):
  t=n/30;im=hook.copy()
  for i,g in enumerate(groups):
   stop=groups[i+1][0]['start'] if i+1<len(groups) else g[-1]['end']+.05
   if g[0]['start']<=t<stop:
    m.text(im,[' '.join(w['word'] for w in g).upper()],1498,54);break
  im.save(layers/f'{n:05d}.png')
 final=OUT/(KEY+'_v05.mp4')
 end=round(prep['vo_splice_map']['vo_end_s']*30)
 total=round(prep['vo_splice_map']['total_duration_s']*30)
 loop_filter=f"[captioned]split=4[body][rev][sample][endpoint];[body]trim=end_frame={end},setpts=N/(30*TB)[b];[rev]trim=end_frame=30,reverse,trim=end_frame=25,setpts=N/(30*TB)[r];[sample]trim=start_frame=2:end_frame=3,loop=loop=3:size=1:start=0,trim=end_frame=4,setpts=N/(30*TB)[s];[endpoint]trim=end_frame=1,setpts=N/(30*TB)[e];[b][r][s][e]concat=n=4:v=1:a=0,setpts=N/(30*TB),format=yuv420p[v]"
 raw=OUT/'opening_raw.mp4'
 assert sha(ROOT/opening['source_path'])==opening['source_sha256']
 ff(['-ss',opening['source_in'],'-t',opening['source_dur']+.15,'-i',ROOT/opening['source_path'],'-an','-vf',opening['crop_filter']+',noise=alls=4:allf=t:all_seed=1032','-frames:v',opening_frames,'-c:v','libx264','-preset','fast','-crf','16',raw])
 fc=f"[1:v][2:v]overlay=0:0,trim=end_frame={opening_frames},setpts=N/(30*TB)[open];[0:v]trim=start_frame={opening_frames}:end_frame={end},setpts=N/(30*TB)[rest];[open][rest]concat=n=2:v=1:a=0[captioned];"+loop_filter
 ff(['-i',SRC,'-i',raw,'-framerate','30','-i',layers/'%05d.png','-filter_complex',fc,'-frames:v',total,'-map','[v]','-map','0:a','-c:v','libx264','-preset','fast','-crf','18','-c:a','copy','-movflags','+faststart',final])
 assert ah(SRC)==ah(final),'AAC changed'
 ff(['-i',final,'-vf','scale=720:1280:flags=lanczos','-c:v','libx264','-preset','fast','-crf','20','-c:a','copy',OUT/(KEY+'_v05_PHONE.mp4')])
 for p in ['locked_preparation.json','locked_shots.json','input_hashes.json','stem_vo.wav','stem_bed.wav','stem_sfx.wav']:shutil.copy2(SOURCE/p,OUT/p)
 level=legacy.ebur128_stats(final);loop=legacy.loop_measures(final)
 record={'status':'UNREVIEWED; final gates and actual AAC listening/transcript comparison required','input_sha256':sha(SRC),'output_sha256':sha(final),'I_LUFS':level[0],'TP_dBTP':level[1],'audio_pass':-14.5<=level[0]<=-13.5 and level[1]<=-1.6,'loop':loop,'loop_pass':max(loop.values())<2,'AAC_packet_hash_unchanged':True,'change':'Rebuilt opening from the exact locked NASA source/crop and code hook, replacing its static bottom caption with complete timed opening captions. Body after frame 73 preserved. v04 preserved. Rebuilt the existing 1s reverse loop from the corrected captioned opening. No change to VO, hook, plates, title banner, card or timing.','caption_groups':groups}
 (OUT/'FINISH_COMPLETE.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(record),flush=True)
 assert record['audio_pass'] and record['loop_pass']
if __name__=='__main__':main()
