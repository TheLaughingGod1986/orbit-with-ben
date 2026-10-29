#!/usr/bin/env python3
"""Deliver immutable Gemini advisory notes alongside worker media with independent hashes."""
import hashlib,json,os,shutil
from pathlib import Path
ROOT=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
TASK=Path(__file__).resolve().parent
PAIRS=[('GEMINI_AAC_S6.md','028_short_lift_night_sky_35yr_v05','028_A-Star-Is-Coming-Toward-Us/10_Shorts/lift_night_sky_35yr'),('GEMINI_AAC_S2_S5.md','earth_equator_weight_v05','027_What-If-Earth-Stopped-Spinning/10_Shorts/lift_equator_weight'),('GEMINI_AAC_S2_S5.md','028_short_fri04_scale_v05','028_A-Star-Is-Coming-Toward-Us/10_Shorts/fri04_scale')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert os.path.ismount('/Volumes/data')
 records=[]
 for name,stem,film in PAIRS:
  p=TASK/'evidence'/name
  if not p.exists():continue
  dests=[ROOT/'02_Video-Projects'/film/'06_Final-Exports',Path('/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT')/stem,Path('/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT')/stem]
  for d in dests:
   q=d/(stem+'_GEMINI_ADVISORY.md')
   if q.exists():assert sha(p)==sha(q),str(q)
   else:shutil.copy2(p,q)
   assert sha(q)==sha(p);records.append({'path':str(q),'sha256':sha(q)})
 (TASK/'evidence/GEMINI_ADVISORY_DELIVERY.json').write_text(json.dumps({'status':'Gemini advisory only; not Chief PASS','files':records},indent=2)+'\n');print('Verified advisory copies',len(records))
if __name__=='__main__':main()
