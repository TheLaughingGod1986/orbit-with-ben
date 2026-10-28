#!/usr/bin/env python3
"""Prepare only the authorized S2 sentence-pause change, no spoken word changes."""
import copy,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
key='S2_027_emwQsPxnRGM'
old=json.loads((R/'jobs/reviews/J0936_v04_PREP_v07_maps.json').read_text())
s=copy.deepcopy(old['shorts'][key]);v=s['vo_splice_map']
c=json.loads(Path('/Users/benjaminoats/_desk/reviews/J1100/audio_candidates/CANDIDATES.json').read_text())[key]
v['subspans']=c['subspans'];v['vo_end_s']=c['duration_with_1s_loop_s']-1;v['total_duration_s']=c['duration_with_1s_loop_s'];v['seventy_pct_mark_s']=v['total_duration_s']*.7
v['auditions']['full_vo_audition']={'wav_path':c['file'],'sha256':c['sha256']}
def shift(t):return round(t+(.47 if t>=2.54 else 0)+(.32 if t>=4.98 else 0),3)
for row in s['shot_plan']:
 row['timeline_in']=shift(row['timeline_in']);row['timeline_out']=shift(row['timeline_out']);row['timeline_dur']=round(row['timeline_out']-row['timeline_in'],3)
 if row['row']=='s02_iss_hurricane':pass
 if row['timeline_dur']!=round(row.get('source_dur',0),3) and row['row']!='s_loop':
  # Only second shot grows across the two new pauses; all other source windows stay fixed.
  if row['timeline_in']<2.54<row['timeline_out']:
   row['source_dur']=row['timeline_dur'];row['source_out']=row['source_in']+row['source_dur']
card=s['single_teaching_overlay'];card['timeline_in']=shift(card['timeline_in']);card['timeline_out']=shift(card['timeline_out'])
v['keyword_timings']={k:shift(t) if isinstance(t,(float,int)) else t for k,t in v.get('keyword_timings',{}).items()}
s['J1100_change']='Question-end pause 0.65s and answer-end pause 0.50s. Exact words and other audio unchanged; full final AAC listening outstanding.'
out={'shorts':{key:s}};p=R/'jobs/reviews/J1100/maps_s2.json';p.write_text(json.dumps(out,indent=2)+'\n')
print(hashlib.sha256(p.read_bytes()).hexdigest())
