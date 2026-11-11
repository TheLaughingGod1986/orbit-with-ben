#!/usr/bin/env python3
"""Finish saved Moon sections: title only the opening, then mux by stream copy."""
import json
from pathlib import Path
import build_public_moon as b

SRC=Path('/Users/ben/_desk/J2452-sleep-scratch/public_moon_v03')
OUT=Path('/Users/ben/_desk/J2452-sleep-scratch/public_moon_v04')
OUT.mkdir(exist_ok=False)
title=OUT/'titled_interior_00.mp4'
b.run(['-i',str(SRC/'interior_00.mp4'),'-loop','1','-i',str(SRC/'title.png'),
       '-filter_complex_threads','1','-filter_complex',
       '[1:v]format=rgba,fade=t=in:st=0:d=1.5:alpha=1,fade=t=out:st=4.5:d=1.5:alpha=1[t];[0:v][t]overlay=0:0:enable=lt(t\\,6),format=yuv420p[v]',
       '-map','[v]','-t','17.9',*b.enc(),str(title)])
lines=(SRC/'concat.txt').read_text().splitlines(); lines[0]=f"file '{title}'"
(OUT/'concat.txt').write_text('\n'.join(lines)+'\n')
final=OUT/'013_moon_undarkened_v01.mp4'
b.run(['-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-i',str(b.NARR),
       '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','440.3',str(final)])
chapter=json.loads((b.ROOT/'jobs/reviews/J2452/picture_timeline_v01.json').read_text())['chapters'][0]
clock=0; changed=[]
for i,s in enumerate(chapter['slices'][:-1]):
    end=round(s['chapter_out_s']*30)/30
    changed.append(dict(row=f'join-{i}',timeline_in=end-.2,timeline_out=end+.2,source=f'new-dissolve-{i}',framing=dict(offset=0),src_w=1920,upscale=1))
changed.append(dict(row='quiet-title',timeline_in=0,timeline_out=6,source='quiet-title',framing=dict(offset=0),src_w=1920,upscale=1))
for i in [1,2,3,5]:
    end=round(chapter['slices'][i]['chapter_out_s']*30)/30
    changed.append(dict(row=f'tail-hold-{i}',timeline_in=end-.25,timeline_out=end,source=f'tail-hold-{i}',framing=dict(offset=0),src_w=1920,upscale=1))
full=[dict(row=f'pixel-{k}',timeline_in=k,timeline_out=min(k+2,440.3),source=b.MASTER.name,framing=dict(offset=k),src_w=1920,upscale=1) for k in range(0,441,2)]
report=dict(status='CANDIDATE_GATES_PENDING',film='013',output=str(final),sha256=b.sha(final),expected_frames=13209,duration_s=440.3,
            source_master=str(b.MASTER),narration_sha256=b.sha(b.NARR),planned_ranges=chapter['planned_ranges'],slices=chapter['slices'],
            source_sections=str(SRC),finishing='Only 17.9-second opening interior re-encoded for title; remaining saved sections stream copied. Existing 0.4-second joins retain narration clock.',
            darkening='Identity: Moon ends before the 19:30 ramp. No darkened second copy or encode.',
            breath='Four-second inter-film breath still owed at final assembly.',
            covers='Corrected slices exclude source Orbit, agenda and act cards. Raw narration tails use short endpoint holds; no new footage.',
            inherited='Public-film charts and labels retained under Chief ruling of 11 Nov 09:29Z.')
for name,data in [('BUILD.json',report),('full_pixel_cuts.json',full),('changed_cuts.json',changed)]:
    (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
print(final,flush=True)
