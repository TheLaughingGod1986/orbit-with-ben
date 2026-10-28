import json,copy,hashlib
from pathlib import Path
r=Path(__file__).resolve().parents[3];key='S6_028_X768qs8sNQs'
s=copy.deepcopy(json.loads((r/'jobs/reviews/J0936_v04_PREP_v07_maps.json').read_text())['shorts'][key]);v=s['vo_splice_map'];c=json.loads(Path('/Users/benjaminoats/_desk/reviews/J1100/audio_candidates/CANDIDATES.json').read_text())[key];delta=round(c['duration_with_1s_loop_s']-v['total_duration_s'],3)
v['subspans']=c['subspans'];v['opening_question_span_count']=7
for sp in v['subspans']:
 for w in sp['words']:w['start']=round(sp['timeline_start']+w['src_start']-sp['source_in'],3);w['end']=round(sp['timeline_start']+w['src_end']-sp['source_in'],3)
v['subspans'][6]['words'][-1]['word']='arrives?'
v['total_duration_s']=round(c['duration_with_1s_loop_s'],3);v['vo_end_s']=round(v['total_duration_s']-1,3);v['seventy_pct_mark_s']=v['total_duration_s']*.7;v['auditions']['full_vo_audition']={'wav_path':c['file'],'sha256':c['sha256']}
for i,row in enumerate(s['shot_plan']):
 if i>1:row['timeline_in']=round(row['timeline_in']+delta,3)
 if i>=1:row['timeline_out']=round(row['timeline_out']+delta,3)
 row['timeline_dur']=round(row['timeline_out']-row['timeline_in'],3)
# Preserve accepted first cut at 2.48s; extend only the second moving source window.
row=s['shot_plan'][1];row['source_dur']=row['timeline_dur'];row['source_out']=round(row['source_in']+row['source_dur'],3)
card=s['single_teaching_overlay']
for field in ['timeline_in','timeline_out']:card[field]=round(card[field]+delta,3)
for w in v['keyword_timings'].values():
 w['start']=round(w['start']+delta,3);w['end']=round(w['end']+delta,3);w['pct_of_total']=round(100*w['start']/v['total_duration_s'],2)
s['J1100_change']={'Chief_exception':'Claude acting Chief, queue reopen 2026-10-28T23:38Z: natural phrase; subject completes 3.215s','delta_s':delta,'question_end_s':c['question_end_s'],'no_atempo':True,'status':'UNREVIEWED; Gemini actual AAC listening required'}
p=r/'jobs/reviews/J1100/maps_s6.json';p.write_text(json.dumps({'shorts':{key:s}},indent=2)+'\n');h=hashlib.sha256(p.read_bytes()).hexdigest()
a=(r/'jobs/reviews/render_j1100_s2_v05.py').read_text().replace('a5b0843eb9c0026f5e917361b317a5f6d88b97662829029f58b54a532e6a78d1',h).replace('maps_s2.json','maps_s6.json').replace('j1100_s2_02_','j1100_s6_02_')
(r/'jobs/reviews/render_j1100_s6_v05.py').write_text(a)
print('delta',delta,'duration',v['total_duration_s'],'card',card['timeline_in'],card['timeline_out'],'sha',h)
