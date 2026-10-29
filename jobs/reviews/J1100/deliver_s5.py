#!/usr/bin/env python3
"""Hash-verified delivery of S5 worker evidence, not a Chief PASS or Ben watch handoff."""
import hashlib,json,os,shutil
from pathlib import Path
ROOT=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
SRC=Path('/Users/benjaminoats/_desk/renders/J1100-attempt03/S5_028_jJ5LkFGyzLI')
STEM='028_short_fri04_scale_v05'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert os.path.ismount('/Volumes/data'),'NAS is not mounted'
 destinations=[ROOT/'02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/fri04_scale/06_Final-Exports',Path('/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT')/STEM,Path('/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT')/STEM]
 meta=json.loads((SRC/'S5_028_jJ5LkFGyzLI_v05_meta.json').read_text());meta.update(status='WORKER EVIDENCE ONLY; actual AAC listening/caption reconciliation and Chief replacement review outstanding',planned_file=str(destinations[0]/(STEM+'.mp4')))
 (SRC/(STEM+'_meta.json')).write_text(json.dumps(meta,indent=2)+'\n')
 note='J1100 S5 worker evidence only. No Chief PASS or Ben watch handoff.\nActual AAC listening at 0-5s and complete caption-vs-audio reconciliation remain outstanding.\nASR hears differences at will/So; inspect the audio rather than rewriting the captions from ASR.\nS2 and S6 remain incomplete. No upload or swap authorized by this record.\n'
 (SRC/'WORKER_STATUS.txt').write_text(note)
 mapping={'S5_028_jJ5LkFGyzLI_v05.mp4':STEM+'.mp4','S5_028_jJ5LkFGyzLI_v05_PHONE.mp4':STEM+'_PHONE.mp4','whole_runtime_2fps.jpg':STEM+'_whole_runtime_2fps.jpg',STEM+'_meta.json':STEM+'_meta.json','FINAL_MEASUREMENTS.json':STEM+'_measurements.json','final_AAC_ASR.json':STEM+'_AAC_ASR.json','polish_gate_locked_rulings.json':STEM+'_polish_locked_rulings.json','WORKER_STATUS.txt':STEM+'_WORKER_STATUS.txt'}
 records=[]
 for srcname,name in mapping.items():
  p=SRC/srcname;expected=sha(p)
  for d in destinations:
   d.mkdir(parents=True,exist_ok=True);q=d/name
   if q.exists():assert sha(q)==expected,f'Existing destination differs: {q}'
   else:shutil.copy2(p,q)
   assert sha(q)==expected;records.append({'path':str(q),'sha256':expected,'bytes':q.stat().st_size})
 result={'status':'PARTIAL J1100 WORKER EVIDENCE; not approved','files':records,'source':str(SRC),'Chief_review_required':True,'actual_AAC_listening_done':False}
 (SRC/'delivery_verified.json').write_text(json.dumps(result,indent=2)+'\n')
 for d in destinations:(d/(STEM+'_sha256_manifest.json')).write_text(json.dumps(result,indent=2)+'\n')
 print(f'Verified {len(records)} copies; no approval or upload')
if __name__=='__main__':main()
