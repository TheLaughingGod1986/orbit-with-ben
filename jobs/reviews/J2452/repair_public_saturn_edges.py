#!/usr/bin/env python3
"""Second bounded cover repair, preserving both rejected candidates."""
import json
from pathlib import Path
import build_public_saturn as b
SRC=b.OUT.with_name('public_saturn_v02');OUT=b.OUT.with_name('public_saturn_v03')
def main():
 OUT.mkdir(exist_ok=False);build=json.loads((SRC/'BUILD.json').read_text())
 patches=[(73,103,28,10,'Orbit-cover-second-neighbour'),(208,224,244,16,'rain-cover-exit')]
 args=['-i',build['output']];filters=['[0:v]setpts=PTS-STARTPTS[base0]']
 for a,z,donor,dur,label in patches:args+=['-ss',str(donor),'-t',str(dur),'-i',str(b.MASTER)]
 for i,(a,z,donor,dur,label) in enumerate(patches):
  n=i+1;filters.append(f'[{n}:v]setpts={(z-a)/dur}*(PTS-STARTPTS),fps=30,scale=1920:1080,setsar=1,format=rgba,fade=t=in:st=0:d=1:alpha=1,fade=t=out:st={z-a-1}:d=1:alpha=1,setpts=PTS+{a}/TB[p{i}]');filters.append(f'[base{i}][p{i}]overlay=eof_action=pass:enable=between(t\\,{a}\\,{z})[base{n}]')
 final=OUT/'021_saturn_undarkened_v03.mp4'
 b.run([*args,'-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','[base2]','-map','0:a','-t',str(build['duration_s']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(final)])
 changes=json.loads((SRC/'changed_cuts.json').read_text())
 for a,z,donor,dur,label in patches:changes.append(dict(row=label,timeline_in=a,timeline_out=z,source=label,framing=dict(offset=0),src_w=1920,upscale=1))
 build.update(output=str(final),sha256=b.sha(final),parent_candidate=str(SRC),second_repair_patches=[dict(chapter_in_s=a,chapter_out_s=z,master_donor_in_s=donor,donor_duration_s=dur,label=label) for a,z,donor,dur,label in patches],second_repair='Orbit neighbour candidate retained dark/seam findings; reuse the same film ring close-up that passed first-act cover, slowed 3x in picture only. Cover rain exit through next usable public picture. Narration untouched. No threshold or review override.')
 for name,data in [('BUILD.json',build),('changed_cuts.json',changes)]: (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
 (OUT/'full_pixel_cuts.json').write_text((SRC/'full_pixel_cuts.json').read_text());print(final,flush=True)
if __name__=='__main__':main()
