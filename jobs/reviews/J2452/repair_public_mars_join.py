#!/usr/bin/env python3
"""Cover compilation-only cards and widen cover neighbourhoods with adjacent master picture."""
import json
from pathlib import Path
import build_public_mars as b
SRC=b.OUT.with_name('public_mars_v03');OUT=SRC.with_name('public_mars_v04')
def main():
 OUT.mkdir(exist_ok=False)
 build=json.loads((SRC/'BUILD.json').read_text());patches=[(209,217,250,8,'subscribe-join-detail')]
 args=['-i',build['output']]
 for a,z,donor,dur,label in patches:args+=['-ss',str(donor),'-t',str(dur),'-i',str(b.MASTER)]
 filters=['[0:v]setpts=PTS-STARTPTS[base0]']
 for i,(a,z,donor,dur,label) in enumerate(patches):
  n=i+1;ratio=(z-a)/dur
  filters.append(f'[{n}:v]setpts={ratio}*(PTS-STARTPTS),fps=30,scale=1920:1080,setsar=1,format=rgba,fade=t=in:st=0:d=1:alpha=1,fade=t=out:st={z-a-1}:d=1:alpha=1,setpts=PTS+{a}/TB[p{i}]')
  filters.append(f'[base{i}][p{i}]overlay=eof_action=pass:enable=between(t\\,{a}\\,{z})[base{n}]')
 final=OUT/'025_mars_undarkened_v04.mp4'
 b.run([*args,'-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','[base1]','-map','0:a','-t',str(build['duration_s']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(final)])
 changes=json.loads((SRC/'changed_cuts.json').read_text())
 changes.append(dict(row='tail-trim',timeline_in=build['duration_s']-.5,timeline_out=build['duration_s'],source='tail-trim',framing=dict(offset=0),src_w=1920,upscale=1))
 for a,z,donor,dur,label in patches:changes.append(dict(row=label,timeline_in=a,timeline_out=z,source=label,framing=dict(offset=0),src_w=1920,upscale=1))
 build['cover_provenance']={'winter_plate':'PIA19400.tif','sha256':'2a666f7bbc233be8b0d40a6bd51cdc2ccea5bf5aae516d1eeba04442dd53497e','existing_record':'jobs/reviews/J2548/COPIED.md','wheel_fallback':'Named PIA19803 and alternative wheel pool absent at the named NAS and archived edit paths; own neighbouring finished-master rover picture used, no new search or generation.'}
 build.update(output=str(final),sha256=b.sha(final),parent_candidate=str(SRC),repair_patches=[dict(chapter_in_s=a,chapter_out_s=z,master_donor_in_s=donor,donor_duration_s=dur,label=label) for a,z,donor,dur,label in patches],repair='Fix picture_qa low-detail failure at chapter 213.5 seconds, inside the new subscribe-removal join. Cover chapter 209–217 with own finished-master 250–258 solar-panel/ground picture and one-second edge fades. No narration change; rerun gates.')
 (OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n');(OUT/'changed_cuts.json').write_text(json.dumps(changes,indent=2)+'\n');(OUT/'full_pixel_cuts.json').write_text((SRC/'full_pixel_cuts.json').read_text());print(final,flush=True)
if __name__=='__main__':main()
