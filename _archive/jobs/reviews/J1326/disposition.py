from pathlib import Path
import json,os,csv,collections,re
O=Path(__file__).parent
old=json.load(open('/private/tmp/J1322-records/jobs/reviews/J1322/deferred.json')); census=json.load(open(O/'census_first.json'))['files']; refs=json.load(open(O/'reference_excerpts.json'))
summary=[]; counts=collections.Counter(); total=0
with O.joinpath('file_decisions.csv').open('w') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['exact_path','current_allocated_bytes','owner','decision','reason_id'])
 for group in old:
  p=group['candidate']; name=Path(p).name
  if 'code_graphics_v0' in p: reason='HOS008_ROW_CLEARANCE'
  elif 'APOPHIS_REPLICATION' in p:reason='APOPHIS_REPAIR_HOLD'
  elif 'OWB UAT/' in p:reason='UAT_WATCH_OR_VERSION'
  elif 'MOVED_TO_NAS' in p:reason='DURABLE_POINTER'
  elif any(t in name for t in ['s05_valves_v02','s02_tied_arm_v04']):reason='CURRENT_BUILDER_STEMS'
  elif '006_' in p or any(t in name for t in ['s06_blood_pressure','s07_heart_pulse','s08_capillaries']):reason='ONLY_CURRENT_WORK_VERSION'
  else:reason='CURRENT_PREVIOUS_OR_HISTORIC_INPUT'
  allocated=0
  for row in group['files']:
   s=census.get(row['path']); a=s['allocated'] if s else 0
   w.writerow([row['path'],a,s['owner'] if s else 'not in census','KEEP',reason]);allocated+=a;counts[reason]+=1
  total+=allocated
  summary.append({'path':p,'decision':'KEEP','reason_id':reason,'files':len(group['files']),'allocated_bytes':allocated,'baseline_allocated':sum(x['allocated'] for x in group['files']),'reference_evidence_key':p})
O.joinpath('candidate_decisions.json').write_text(json.dumps(summary,indent=2))
O.joinpath('proposal.json').write_text(json.dumps({'eligible_files':[],'eligible_allocated_bytes':0,'reason':'No candidate meets all inactivity, exact watch-path, current/previous, rebuild-input and exclusion conditions simultaneously. Hash equality alone does not waive exclusions.','all_original_candidates_allocated':total,'file_decision_counts':dict(counts),'no_move_no_unlink':True,'requires':'Chief exact-path ruling, then fresh df and source/reference recheck. J1100 remains held at worker 2/3 with h43-LOOP.'},indent=2))
print('decisions',sum(counts.values()),'retained GiB',round(total/2**30,3))
