#!/usr/bin/env python3
"""Export corrected picture coordinates without claiming cover/QA completion."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[3]
index=json.loads((root/'jobs/reviews/J2452/narration_v03/ALL_CHAPTERS.json').read_text())
inputs={c['film']:c for c in json.loads((root/'jobs/reviews/J2452/alignment_v02/inputs_v01.json').read_text())}
chapters=[];global_t=0
for number,c in enumerate(index['chapters'],1):
    r=json.loads((root/c['report']).read_text());t=0;slices=[]
    if 'source_recipes' in r:
        ranges=[(x['master_in_s'],x['master_out_s'],x['source_out_s']-x['source_in_s']) for x in r['source_recipes']]
    else:
        ranges=[(a,b,b-a) for a,b in r['used_ranges']]
    for a,b,d in ranges:
        slices.append(dict(master_in_s=a,master_out_s=b,chapter_in_s=round(t,6),chapter_out_s=round(t+d,6),compilation_in_s=round(global_t+t,6),compilation_out_s=round(global_t+t+d,6)))
        t+=d
    assert abs(t-c['duration_s'])<.002,(c['film'],t,c['duration_s'])
    chapters.append(dict(number=number,film=c['film'],master=inputs[c['film']]['master'],narration=c['output'],narration_sha256=c['sha256'],report=c['report'],planned_ranges=r.get('plan_ranges',r.get('plan_master_ranges')),slices=slices,compilation_start_s=round(global_t,6),duration_s=c['duration_s'],breath_after_s=4 if number<13 else 20,picture_status='NOT_RENDERED; cover windows and source cut softening still required',moon_note='Raw audio tails exceed source-part picture; use clean plate holds and verify actual PTS' if c['film']=='013' else None))
    global_t+=t+(4 if number<13 else 20)
report=dict(status='CORRECTED_COORDINATES_ONLY_NOT_FINAL_PICTURE_CUT_LIST',duration_s=round(global_t,6),chapters=chapters,darkening=dict(ramp_global_s=[1170,1230],multiplier=[1,.85],hold_multiplier=.85,highlight_luma_cap_after_ramp=180),final_fade_global_s=[round(global_t-20,6),round(global_t,6)],remaining='Validate actual frames and all cover windows; render picture chapters with matching duration/settings; two-second dissolves must not shorten or shift narration. Final AV QA and NAS master/reel pending.')
(root/'jobs/reviews/J2452/picture_timeline_v01.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'{len(chapters)} chapters; {global_t:.2f} s including breaths/fade')
