#!/usr/bin/env python3
"""Cover compilation-only cards and widen cover neighbourhoods with adjacent master picture."""
import json
from pathlib import Path
import build_public_sun as b
SRC=b.OUT;OUT=SRC.with_name('public_sun_v02')
def main():
 OUT.mkdir(exist_ok=False)
 build=json.loads((SRC/'BUILD.json').read_text());patches=[(16,24,113,7,'first-trim-detail'),(222,239,266,12,'subscribe-join-detail'),(361,382,365,9,'Orbit-cover-detail')]
 args=['-i',build['output']]
 for a,z,donor,dur,label in patches:args+=['-ss',str(donor),'-t',str(dur),'-i',str(b.MASTER)]
 filters=['[0:v]setpts=PTS-STARTPTS[base0]']
 for i,(a,z,donor,dur,label) in enumerate(patches):
  n=i+1;ratio=(z-a)/dur
  filters.append(f'[{n}:v]setpts={ratio}*(PTS-STARTPTS),fps=30,scale=1920:1080,setsar=1,format=rgba,fade=t=in:st=0:d=1:alpha=1,fade=t=out:st={z-a-1}:d=1:alpha=1,setpts=PTS+{a}/TB[p{i}]')
  filters.append(f'[base{i}][p{i}]overlay=eof_action=pass:enable=between(t\\,{a}\\,{z})[base{n}]')
 final=OUT/'022_sun_undarkened_v02.mp4'
 b.run([*args,'-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','[base3]','-map','0:a','-t',str(build['duration_s']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(final)])
 changes=json.loads((SRC/'changed_cuts.json').read_text())
 changes.append(dict(row='tail-trim',timeline_in=build['duration_s']-.5,timeline_out=build['duration_s'],source='tail-trim',framing=dict(offset=0),src_w=1920,upscale=1))
 for a,z,donor,dur,label in patches:changes.append(dict(row=label,timeline_in=a,timeline_out=z,source=label,framing=dict(offset=0),src_w=1920,upscale=1))
 build.update(output=str(final),sha256=b.sha(final),parent_candidate=str(SRC),repair_patches=[dict(chapter_in_s=a,chapter_out_s=z,master_donor_in_s=donor,donor_duration_s=dur,label=label) for a,z,donor,dur,label in patches],repair='Repair new-edit near-black failures at first trim, subscribe removal and Orbit cover with neighbouring finished-master solar/cloud footage. Timing and narration unchanged; new full gates required.')
 (OUT/'source_cuts.json').write_bytes((SRC/'source_cuts.json').read_bytes());(OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n');(OUT/'changed_cuts.json').write_text(json.dumps(changes,indent=2)+'\n');(OUT/'full_pixel_cuts.json').write_text((SRC/'full_pixel_cuts.json').read_text());print(final,flush=True)
if __name__=='__main__':main()
