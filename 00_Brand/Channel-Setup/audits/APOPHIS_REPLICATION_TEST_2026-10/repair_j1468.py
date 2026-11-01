#!/usr/bin/env python3
"""J1468: no-spend audio-only remux of accepted AR cohort; never overwrite inputs."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
REPO=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
WT=Path(__file__).resolve().parents[4]
REL=Path('00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10')
A=REPO/REL
E=WT/REL/'J1468_evidence'
B='owb-standalone-shorts_score_bed_v01'
SPECS=[('ar1','assembly_j1308_v01','v01','v02','owb_ar1_2024_yr4_moon','49b3e4f0f7276885f942d3451978eba33c9a2fec68216fcafdd79466f877cd07'),('ar2','assembly_j1321_delivery_v02','v06','v07','owb_ar2_iss_2030_deorbit','6d517aad6c61a0f12d67b4f2f7990f94ea165e17e01055b56873e89415bf8e67'),('ar3','assembly_j1345_v05','v05','v06','owb_ar3_2027_eclipse','3a2fc5b53e2cfafe4d55422f4f8ae7894ffdb81a727bf47f605e01070a58f13d')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(c):
 r=subprocess.run(list(map(str,c)),capture_output=True,text=True)
 if r.returncode: print(r.stderr,flush=True)
 r.check_returncode();return r
def ff(*args):return run(['ffmpeg','-hide_banner','-nostats',*args])
def dur(p):return float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).stdout)
def vhash(p):return run(['ffmpeg','-v','error','-i',p,'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-']).stdout.strip()
def gate(name,cmd,ev):
 r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True)
 (ev/(name+'.txt')).write_text(r.stdout+r.stderr)
 return r.returncode

def main():
 music=A/'05_Music';music.mkdir(exist_ok=True)
 for ext in ['.mp3','_plan.json']:
  src=REPO/'00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/05_Music'/(B+ext)
  dst=music/src.name
  if dst.exists():assert sha(src)==sha(dst)
  else:shutil.copy2(src,dst)
  if ext.endswith('json'):
   (WT/REL/'05_Music').mkdir(exist_ok=True)
   shutil.copy2(src,WT/REL/'05_Music'/src.name)
 records=[]
 for ar,folder,old,new,slug,expected in SPECS:
  inp=A/'07_Edit-Project'/folder/ar
  src=inp/f'owb_apophis_{ar}_{old}.mp4'
  assert sha(src)==expected,src
  out=A/'07_Edit-Project/assembly_j1468'/ar;out.mkdir(parents=True,exist_ok=True)
  ev=E/ar;ev.mkdir(parents=True,exist_ok=True)
  target=out/f'owb_apophis_{ar}_{new}.mp4'
  assert not target.exists(),f'refusing overwrite {target}'
  seconds=dur(src)
  for f in ['stem_vo.wav','stem_sfx.wav','cuts.json','pool.json']:shutil.copy2(inp/f,out/f)
  # Preserve source VO and SFX; fixed quiet bed plus speech-keyed ducking.
  ff('-n','-i',music/(B+'.mp3'),'-i',out/'stem_vo.wav','-filter_complex',f'[0:a]atrim=0:{seconds},asetpts=PTS-STARTPTS,loudnorm=I=-40:TP=-9:LRA=11,aresample=48000[b];[b][1:a]sidechaincompress=threshold=0.015:ratio=4:attack=15:release=200:makeup=1[a]','-map','[a]','-t',seconds,'-ac','2',out/'stem_bed.wav')
  mix='[0:a][1:a][2:a]amix=inputs=3:duration=longest:normalize=0'
  p=ff('-i',out/'stem_vo.wav','-i',out/'stem_sfx.wav','-i',out/'stem_bed.wav','-filter_complex',mix+',loudnorm=I=-14:TP=-2.0:LRA=11:print_format=json[a]','-map','[a]','-f','null','-').stderr
  m=json.loads(p[p.rindex('{'):p.rindex('}')+1])
  norm=f"loudnorm=I=-14:TP=-2.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
  if ar=='ar3':norm='volume=8dB'
  ceiling='0.78' if ar=='ar3' else '0.7943'
  ff('-n','-i',out/'stem_vo.wav','-i',out/'stem_sfx.wav','-i',out/'stem_bed.wav','-i',src,'-filter_complex',mix+','+norm+f',alimiter=limit={ceiling}:level=false:attack=5:release=50,aresample=48000[a]','-map','3:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','256k','-t',seconds,'-movflags','+faststart',target)
  vh=vhash(src);assert vhash(target)==vh
  final=A/'06_Final-Exports'/f'{slug}_{new}.mp4';final.parent.mkdir(exist_ok=True)
  assert not final.exists();shutil.copy2(target,final);assert sha(final)==sha(target)
  pack=WT/REL/'11_Upload-Package'/slug/'PACKAGE_MANIFEST.json'
  manifest=json.loads(pack.read_text());manifest['video']=str(REL/'06_Final-Exports'/final.name);pack.write_text(json.dumps(manifest,indent=2)+'\n')
  for f in ['cuts.json','pool.json']:shutil.copy2(out/f,ev/f)
  py=sys.executable
  results={}
  results['sfx_level']=gate('sfx_level',[py,REPO/'scripts/sfx_kit.py','level','--vo',out/'stem_vo.wav','--sfx',out/'stem_sfx.wav','--bed',out/'stem_bed.wav','--minutes',seconds/60,'--out',ev/'sfx_level.json'],ev)
  results['music_gate']=gate('music_gate',[py,REPO/'scripts/music_gate.py',A,'--bed',music/(B+'.mp3'),'--video',final,'--out',ev/'music_gate.json'],ev)
  results['picture_qa']=gate('picture_qa',[py,REPO/'scripts/picture_qa.py',final,'--cuts',out/'cuts.json','--pool',out/'pool.json','--out-dir',ev/'picture'],ev)
  results['polish_gate']=gate('polish_gate',[py,REPO/'scripts/polish_gate.py',final,'--cuts',out/'cuts.json','--out',ev/'polish_gate.json'],ev)
  results['shorts_gate']=gate('shorts_gate',[py,REPO/'00_Brand/Channel-Setup/tools/gate_shorts_open.py','check',final,'--vo',out/'stem_vo.wav','--script',A/'02_Voiceover'/f'{ar}_locked_v01.txt','--json','--sheet-dir',out/'shorts_gate'],ev)
  measure=ff('-i',final,'-af','loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-').stderr
  measured=json.loads(measure[measure.rindex('{'):measure.rindex('}')+1])
  tail=ff('-sseof','-1','-i',final,'-af','volumedetect','-f','null','-').stderr
  (ev/'tail_audio.txt').write_text(tail)
  row=dict(short=ar,source=str(src),source_sha256=expected,master=str(target),final=str(final),sha256=sha(final),picture_stream_hash=vh,picture_bitstream_unchanged=True,seconds=seconds,stems={f:str(out/f) for f in ['stem_vo.wav','stem_sfx.wav','stem_bed.wav']},mix_measurement=measured,gates=results)
  (ev/'DELIVERY.json').write_text(json.dumps(row,indent=2)+'\n');records.append(row)
  print(ar,results,flush=True)
  assert sha(src)==expected
 (E/'DELIVERY.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':main()
