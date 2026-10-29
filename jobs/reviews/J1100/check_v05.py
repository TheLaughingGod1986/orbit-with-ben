#!/usr/bin/env python3
"""Final-media measurements for J1032; logs real failures, grants no waivers or PASS."""
import sys
import argparse,hashlib,importlib.util,json,math,re,subprocess,time
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def command(a,log):
 with log.open('w') as f:r=subprocess.run([str(x) for x in a],stdout=f,stderr=subprocess.STDOUT)
 return r.returncode

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--version',default='v05',choices=['v05','v06']);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--media-root',type=Path,required=True);ap.add_argument('--reviewed-ok',type=Path);a=ap.parse_args()
 pools={}
 for p in a.media_root.glob('02_Video-Projects/*/10_Shorts/**/pool_v03.json'):
  try:
   items=json.loads(p.read_text())
   if isinstance(items,list):
    for v in items:pools[v.get('file_id','')]=v.get('title','')
  except (ValueError,TypeError):pass
 summary={}
 for source in sorted(a.source.glob('*/*_'+a.version+'.mp4')):
  key=source.parent.name;d=a.out/key
  started=time.monotonic()
  while not (d/'FINISH_COMPLETE.json').exists():
   done=Path('/Users/benjaminoats/_desk/logs/J1032-finish04.done')
   if done.exists() and done.read_text().strip()!='0':raise RuntimeError('Finishing failed; inspect finish04 log')
   if time.monotonic()-started>1800:raise RuntimeError('Finishing checkpoint timed out')
   time.sleep(5)
  if (d/'FINAL_MEASUREMENTS.json').exists():
   summary[key]=json.loads((d/'FINAL_MEASUREMENTS.json').read_text());continue
  video=d/source.name;prep=json.loads((source.parent/'locked_preparation.json').read_text());rows=[];pool=[]
  for r in prep['shot_plan']:
   # Reuse follows the underlying plate, not the intermediate film container.
   # Preserve container path/hash/offset separately for exact extraction provenance.
   container_name=Path(r['source_path']).name
   name=r['underlying_id']
   title=pools.get(name) or name
   rows.append({'row':r['row'],'timeline_in':round(r['timeline_in']*30)/30,'timeline_out':round(r['timeline_out']*30)/30,'source':name,'video':r['video'],'upscale':r['upscale'],'framing':{'offset':r['source_in']},'source_path':r['source_path'],'source_container':container_name,'source_sha256':r['source_sha256'],'underlying_id':r['underlying_id']})
   pool.append({'file_id':name,'title':title})
  dump(d/'cuts.json',rows);dump(d/'pool.json',pool)
  words=[w for sp in prep['vo_splice_map']['subspans'] for w in sp['words']]
  meta={'job':'J1100','version':a.out.name,'file':str(video),'planned_title':prep['local_title'],'spoken':' '.join(w['word'] for w in words),'words':words,'last_word_end_s':words[-1]['end'],'vo_stem':str(source.parent/'stem_vo.wav'),'status':'UNREVIEWED','preparation_sha256':'e76ca28f2b959fb344b2ce1c86ae2ce283d99c1a892048d6fc65c577ba63a5e2'}
  dump(d/(video.stem+'_meta.json'),meta)
  results={}
  cmds={
   'shorts':[sys.executable,a.media_root/'00_Brand/Channel-Setup/tools/gate_shorts_open.py','check',video,'--air-date',prep['air_date'],'--id',prep['youtube_id'],'--meta',d/(video.stem+'_meta.json'),'--vo',source.parent/'stem_vo.wav','--sheet-dir',d/'shorts_gate','--json'],
   'picture':[sys.executable,a.media_root/'scripts/picture_qa.py',video,'--cuts',d/'cuts.json','--pool',d/'pool.json','--out-dir',d/'picture_qa'],
   'polish':[sys.executable,a.media_root/'scripts/polish_gate.py',video,'--cuts',d/'cuts.json','--out',d/'polish_gate.json'],
   'sfx':[sys.executable,a.media_root/'scripts/sfx_kit.py','level','--vo',source.parent/'stem_vo.wav','--sfx',source.parent/'stem_sfx.wav','--bed',source.parent/'stem_bed.wav','--minutes',prep['vo_splice_map']['total_duration_s']/60],
  }
  if a.reviewed_ok:
   for gate in ('picture','polish'):cmds[gate] += ['--reviewed-ok',a.reviewed_ok]
  for gate,cmd in cmds.items():
   print(key,gate,flush=True);results[gate]={'exit_code':command(cmd,d/(gate+'.log'))}
  inputs=json.loads((source.parent/'input_hashes.json').read_text())
  film=next((a.media_root/'02_Video-Projects').glob(prep['film'].split(':')[1]+'_*'))
  results['music']={'exit_code':command([sys.executable,a.media_root/'scripts/music_gate.py',film,'--bed',inputs['bed_path'],'--video',video,'--out',d/'music_gate.json'],d/'music.log')}
  # Decode all output frames for dark-run measurement, every third frame for OCR.
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vf','scale=180:320,format=gray','-f','rawvideo','-'])
  frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,320,180);dump(d/'actual_seam.json',{'first_frame_to_last_diff':float(np.abs(frames[0].astype(float)-frames[-1].astype(float)).mean()),'frames':len(frames)});black=(frames<20).mean(axis=(1,2));run=worst=0
  for v in black:
   run=run+1 if v>.85 else 0;worst=max(worst,run)
  dump(d/'dark_run.json',{'frames':len(frames),'worst_consecutive':worst,'pass':worst<3,'black_fraction_by_frame':black.tolist()})
  ocr=d/'ocr';ocr.mkdir(exist_ok=True)
  command(['ffmpeg','-y','-v','error','-i',video,'-vf',"select='not(mod(n,3))',scale=540:960",'-fps_mode','vfr',ocr/'%05d.png'],d/'ocr_extract.log')
  pattern=re.compile(r'https?://|www\.|\.com\b|\.org\b|\.gov\b|\.int\b|copyright|all rights reserved|youtube|J\d{4}|\.mp4|\.webm|\.mov|F-jImX5h7ws|'+re.escape(prep['youtube_id']),re.I)
  records=[];hits=[]
  for i,p in enumerate(sorted(ocr.glob('*.png'))):
   t=subprocess.run(['tesseract',str(p),'stdout','--psm','6'],capture_output=True,text=True).stdout.strip();rec={'frame':i*3,'time':i/10,'text':t};records.append(rec)
   if pattern.search(t):hits.append(rec)
  dump(d/'ocr_every_third.json',{'pass':not hits,'samples':len(records),'hits':hits,'records':records})
  # Full runtime at 2fps, retaining individual frames for full-size inspection.
  sheetdir=d/'runtime_frames';sheetdir.mkdir(exist_ok=True)
  command(['ffmpeg','-y','-v','error','-i',video,'-vf','fps=2,scale=270:480',sheetdir/'%04d.jpg'],d/'sheets_extract.log')
  imgs=sorted(sheetdir.glob('*.jpg'));sheet=Image.new('RGB',(270*8,506*math.ceil(len(imgs)/8)),(35,40,55));draw=ImageDraw.Draw(sheet)
  for i,p in enumerate(imgs):
   x=(i%8)*270;y=(i//8)*506;sheet.paste(Image.open(p),(x,y));draw.text((x+5,y+482),f'{i/2:.1f}s',fill='white')
  sheet.save(d/'whole_runtime_2fps.jpg',quality=93)
  results.update({'dark_pass':worst<3,'ocr_pass':not hits,'audio_and_loop':json.loads((d/'FINISH_COMPLETE.json').read_text()),'status':'UNREVIEWED; music gate, visual flags, finished audio listening and verified delivery still required'})
  dump(d/'FINAL_MEASUREMENTS.json',results);summary[key]=results;print(key,'MEASURED; no approval',flush=True)
 dump(a.out/'BATCH_MEASUREMENTS.json',summary)
if __name__=='__main__':main()
