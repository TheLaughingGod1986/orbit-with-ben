#!/usr/bin/env python3
"""Verify source hashes against the current Titan standalone replacement. No frame-review claim."""
import json, hashlib
from pathlib import Path
repo=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
p=Path(__file__).resolve().parent
h=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
social=repo/'00_Brand/Channel-Setup/social/UPLOADS.json'
u=json.loads(social.read_text())
if 'videos' in u:u=u['videos']
old=u['RLSJm59OSzI'];new=u[old['supersededBy']]
meta=repo/'jobs/reviews/J1199/owb_sa_s6_titan_v11_meta.json'
m=json.loads(meta.read_text())
assert m['sha256']==new['sha256']
pool=json.loads((p/'HARVEST_POOL_v01.json').read_text())
short=[]
for c in m['cuts']:
 f=Path(c['source'])
 if f.suffix.lower()=='.jpg' and not any(x['path']==str(f) for x in short):
  short.append({'asset_id':f.stem,'path':str(f),'sha256':h(f)})
f=Path(m['opening']['source'])
assert h(f)==m['opening']['source_sha256']
short.append({'asset_id':'S6_flow_t2_silent','path':str(f),'sha256':h(f),'used_frames':'0..91 (tail 0..27, opening 28..91)'})
checks=[]
for a in pool['assets']:
 f=Path(a['local_path'])
 actual=h(f)
 assert actual==a['sha256'],a['asset_id']
 checks.append({'asset_id':a['asset_id'],'sha256':actual,'matches_short_source':[s['asset_id'] for s in short if s['sha256']==actual]})
assert not any(c['matches_short_source'] for c in checks)
master=repo/new['file']
master_record={'path':str(master),'exists':master.exists(),'expected_sha256':new['sha256']}
if master.exists():
 master_record['actual_sha256']=h(master)
 assert master_record['actual_sha256']==new['sha256']
result={'job':'J2089','scope':'SOURCE_ID_AND_EXACT_FILE_HASH_EXCLUSION_ONLY_NOT_FRAME_REVIEW','old_short':{'id':'RLSJm59OSzI','privacy':old['privacyStatus'],'publishAt':old['publishAt']},'current_short':{'id':old['supersededBy'],'publishAt':new['publishAt'],'master':master_record},'evidence':[{'path':str(social),'sha256':h(social)},{'path':str(meta),'sha256':h(meta)}],'current_short_sources':short,'long_source_checks':checks,'conservative_excluded_ids':pool['excluded_short_asset_ids'],'result':'NO_EXACT_SOURCE_FILE_HASH_OVERLAP','limits':['No decoded-frame or perceptual comparison performed','No final long cut exists; crops, derivatives and generated composites remain unverified','Historical PIA14925 exclusion retained despite replacement opener','No KEEP, motion review or film-stage approval']}
(p/'SHORT_SOURCE_EXCLUSION_v28.json').write_text(json.dumps(result,indent=2)+'\n')
pool['short_exclusion_evidence']={'record':'SHORT_SOURCE_EXCLUSION_v28.json','current_short_id':old['supersededBy'],'old_short_id':'RLSJm59OSzI','status':result['result'],'limitation':'Exact source-file hash/ID check only; final decoded-frame comparison unverified. Preserve all four historical excluded PIA IDs plus S6_flow_t2_silent source.'}
pool['excluded_short_source_sha256']=[s['sha256'] for s in short]
(p/'HARVEST_POOL_v01.json').write_text(json.dumps(pool,indent=2)+'\n')
print(json.dumps({'sources':len(short),'long_sources':len(checks),'overlap':0,'master':master_record},indent=2))
