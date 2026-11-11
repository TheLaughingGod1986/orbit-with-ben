#!/usr/bin/env python3
"""Cover compilation-only cards and widen cover neighbourhoods with adjacent master picture."""
import json
from pathlib import Path
import build_public_earth as b
SRC=b.OUT;OUT=SRC.with_name('public_earth_v02')
def main():
 OUT.mkdir(exist_ok=False)
 build=json.loads((SRC/'BUILD.json').read_text());patches=[(22,27.5,26.6,5.5,'act-sudden-stop'),(64.8,75.6,125,10.8,'northpole-boundaries'),(92,97.5,97,5.5,'act-speed'),(168.35,174.05,181,5.7,'act-slow-stop-boundaries'),(212.35,221.85,226.4,9.5,'sunset-boundaries'),(241.5,247,251.2,5.5,'act-already-slowing'),(349.75,355.35,361,5.6,'act-score-boundaries')]
 args=['-i',build['output']]
 for a,z,donor,dur,label in patches:args+=['-ss',str(donor),'-t',str(dur),'-i',str(b.MASTER)]
 filters=['[0:v]setpts=PTS-STARTPTS[base0]']
 for i,(a,z,donor,dur,label) in enumerate(patches):
  n=i+1;ratio=(z-a)/dur
  filters.append(f'[{n}:v]setpts={ratio}*(PTS-STARTPTS),fps=30,scale=1920:1080,setsar=1,format=rgba,fade=t=in:st=0:d=1:alpha=1,fade=t=out:st={z-a-1}:d=1:alpha=1,setpts=PTS+{a}/TB[p{i}]')
  filters.append(f'[base{i}][p{i}]overlay=eof_action=pass:enable=between(t\\,{a}\\,{z})[base{n}]')
 final=OUT/'027_earth_undarkened_v02.mp4'
 b.run([*args,'-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','[base7]','-map','0:a','-t',str(build['duration_s']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(final)])
 changes=json.loads((SRC/'changed_cuts.json').read_text())
 changes.append(dict(row='tail-trim',timeline_in=build['duration_s']-.5,timeline_out=build['duration_s'],source='tail-trim',framing=dict(offset=0),src_w=1920,upscale=1))
 for a,z,donor,dur,label in patches:changes.append(dict(row=label,timeline_in=a,timeline_out=z,source=label,framing=dict(offset=0),src_w=1920,upscale=1))
 build['fallback']='EPIC absent at named locations. Named Five_Minutes_in_Orbit pool file inspected at 18s: near-black night view and premature EOF decoder warning; master neighbour fallback used, no extended search.'
 build.update(output=str(final),sha256=b.sha(final),parent_candidate=str(SRC),repair_patches=[dict(chapter_in_s=a,chapter_out_s=z,master_donor_in_s=donor,donor_duration_s=dur,label=label) for a,z,donor,dur,label in patches],repair='Additional chapter-card covers plus widened cover boundaries, finishing the fade-in before the first unwanted frame and starting fade-out after its last frame. Master 248.38-250.88 maps to chapter 242.93-245.43 after the removed subscribe sentence. Own neighbouring master pictures; no narration changes or gate override.')
 (OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n');(OUT/'changed_cuts.json').write_text(json.dumps(changes,indent=2)+'\n');(OUT/'full_pixel_cuts.json').write_text((SRC/'full_pixel_cuts.json').read_text());print(final,flush=True)
if __name__=='__main__':main()
