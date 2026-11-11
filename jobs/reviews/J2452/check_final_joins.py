#!/usr/bin/env python3
"""Run unmodified picture QA on each new chapter breath, without waivers."""
import argparse,json,subprocess as sp,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def main():
 p=argparse.ArgumentParser();p.add_argument('--scratch',type=Path,required=True);a=p.parse_args();out=a.scratch/'final_join_v01';reports=[]
 for i in range(1,13):
  video=out/f'join_endpoint_v{3 if i==2 else 2:02d}_{i:02d}.mp4';qa=out/f'join_qa_v03_{i:02d}';qa.mkdir(exist_ok=True)
  cuts=[dict(row=f'join-{i}-{k}',timeline_in=k/2,timeline_out=(k+1)/2,source=f'join-{i}',framing=dict(offset=k/2),src_w=1920,upscale=1) for k in range(8)]
  (qa/'cuts.json').write_text(json.dumps(cuts));(qa/'pool.json').write_text(json.dumps([dict(source=f'join-{i}',title='New endpoint-hold chapter dissolve')]))
  with (qa/'gate.log').open('w') as log:
   code=sp.run([sys.executable,str(ROOT/'scripts/picture_qa.py'),str(video),'--cuts',str(qa/'cuts.json'),'--pool',str(qa/'pool.json'),'--out-dir',str(qa)],stdout=log,stderr=sp.STDOUT,timeout=120).returncode
  reports.append(dict(join=i,exit_code=code,report=str(qa/'picture_qa.json')));print(i,code,flush=True)
 (out/'JOIN_GATES_V03.json').write_text(json.dumps(dict(status='PASS' if all(r['exit_code']==0 for r in reports) else 'FAIL',joins=reports,limitations='Standalone new breaths only; boundaries with complete chapters and final fade still require whole-film checks.'),indent=2)+'\n')
if __name__=='__main__':main()
