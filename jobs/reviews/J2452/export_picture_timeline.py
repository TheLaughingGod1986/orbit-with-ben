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
# Actual-master read-back overrides the plan's earlier zero-Orbit assertion.
for chapter in chapters:
    if chapter['film']=='029':
        chapter['required_orbit_covers'] = []
        for start,end,source in [(123.16,130.42,'sun_orbit_row67_omni_v01.mp4'),(282.16,286.08,'orbit_thumb_omni_v01.mp4')]:
            matches=[sl for sl in chapter['slices'] if sl['master_in_s'] <= start and end <= sl['master_out_s']]
            assert len(matches)==1
            sl=matches[0]
            chapter['required_orbit_covers'].append(dict(master_in_s=start,master_out_s=end,chapter_in_s=round(sl['chapter_in_s']+start-sl['master_in_s'],6),chapter_out_s=round(sl['chapter_in_s']+end-sl['master_in_s'],6),compilation_in_s=round(sl['compilation_in_s']+start-sl['master_in_s'],6),compilation_out_s=round(sl['compilation_in_s']+end-sl['master_in_s'],6),original_source=source,status='REQUIRED_NOT_BUILT',evidence='jobs/reviews/J2452/betelgeuse_orbit_readback_v01.json'))
readback=root/'jobs/reviews/J2452/betelgeuse_orbit_readback_v01.json'
if readback.exists():
    cover_report=json.loads(readback.read_text())
    for chapter in chapters:
        if chapter['film']=='029':
            for requirement,cover in zip(chapter['required_orbit_covers'],cover_report['covers']):
                assert requirement['original_source']==cover['original_source']
                requirement.update(status='COVER_COMPONENT_BUILT_NOT_JOINED_OR_FULL_CHAPTER_QA',candidate_path=cover['output'],candidate_sha256=cover['sha256'])
# A complete silent 029 checkpoint proves cover placement, not sleep-picture QA.
checkpoint=root/'jobs/reviews/J2452/betelgeuse_chapter_v01'
if (checkpoint/'READBACK.json').exists():
    saved=json.loads((checkpoint/'REPORT.json').read_text())
    verified=json.loads((checkpoint/'READBACK.json').read_text())
    assert saved['sha256']==verified['sha256'] and verified['all_opaque_checks_pass']
    for chapter in chapters:
        if chapter['film']=='029':
            assert abs(saved['duration_s']-chapter['duration_s'])<.002
            chapter['picture_status']='COVERS_INTEGRATED_NOT_FINAL_SLEEP_PICTURE_QA'
            chapter['picture_checkpoint']={k:saved[k] for k in ['output','sha256','frames','duration_s','limitations']}
            for requirement in chapter['required_orbit_covers']:
                requirement['status']='COVER_INTEGRATED_AND_PIXEL_CHECKED_NOT_FULL_CHAPTER_QA'
report=dict(status='CORRECTED_COORDINATES_ONLY_NOT_FINAL_PICTURE_CUT_LIST',duration_s=round(global_t,6),chapters=chapters,darkening=dict(ramp_global_s=[1170,1230],multiplier=[1,.85],hold_multiplier=.85,highlight_luma_cap_after_ramp=180),final_fade_global_s=[round(global_t-20,6),round(global_t,6)],remaining='Validate actual frames and all cover windows; render picture chapters with matching duration/settings; two-second dissolves must not shorten or shift narration. Final AV QA and NAS master/reel pending.')
(root/'jobs/reviews/J2452/picture_timeline_v01.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'{len(chapters)} chapters; {global_t:.2f} s including breaths/fade')
