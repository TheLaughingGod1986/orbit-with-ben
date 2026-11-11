#!/usr/bin/env python3
"""Cover the outgoing Moon fade and rebuild its first compilation dissolve."""
import json
from pathlib import Path
import build_public_moon as b

SRC=Path('/Users/ben/_desk/J2452-sleep-scratch/public_moon_v04')
OUT=SRC.with_name('public_moon_v06')
OUT.mkdir(exist_ok=False)
join=OUT/'join_00_held.mp4'
sections=Path(json.loads((SRC/'BUILD.json').read_text())['source_sections'])
opening=OUT/'titled_interior_00_held.mp4'
# The failed sample is 17.65s: the public master's outgoing fade, before
# our dissolve. Hold its neighbouring clean frame from 17.0s through this
# cover window instead of lifting an unrelated transition.
b.run(['-i',str(SRC/'titled_interior_00.mp4'),'-vf',
       'trim=end=17.033333,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1',
       '-t','17.9',*b.enc(),str(opening)])
graph='[0:v]trim=start=17:end=17.033333,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.4[a];[1:v]trim=end=0.2,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=0.2[b];[a][b]xfade=transition=fade:duration=0.4:offset=0,format=yuv420p[v]'
b.run(['-i',str(sections/'slice_00.mp4'),'-i',str(sections/'slice_01.mp4'),
       '-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-t','0.4',*b.enc(),str(join)])
lines=(SRC/'concat.txt').read_text().splitlines()
lines[0]=f"file '{opening}'"
lines[1]=f"file '{join}'"
(OUT/'concat.txt').write_text('\n'.join(lines)+'\n')
final=OUT/'013_moon_undarkened_v03.mp4'
b.run(['-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-i',str(b.NARR),
       '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','440.3',str(final)])
report=json.loads((SRC/'BUILD.json').read_text())
report.update(output=str(final),sha256=b.sha(final),parent_candidate=str(SRC),
              repair='Cover the public outgoing fade with the neighbouring clean frame at chapter 17.0s, held to the first dissolve; unchanged narration clock. Re-encode only first interior and dissolve.')
(OUT/'BUILD.json').write_text(json.dumps(report,indent=2)+'\n')
for name in ['full_pixel_cuts.json','changed_cuts.json']:
    data=json.loads((SRC/name).read_text())
    if name=='changed_cuts.json':
        data.append(dict(row='opening-fade-cover',timeline_in=17.0,timeline_out=18.3,source='neighbouring_clean_frame',framing=dict(offset=0),src_w=1920,upscale=1))
    (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
print(final)
