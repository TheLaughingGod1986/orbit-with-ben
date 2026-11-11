#!/usr/bin/env python3
"""Cover three measured dark edit neighbourhoods with finished-master neighbours."""
import json,shutil
from pathlib import Path
import build_public_light as b
SRC=b.OUT.with_name('public_light_v03');OUT=b.OUT.with_name('public_light_v04')
def main():
 build=json.loads((SRC/'BUILD.json').read_text());OUT.mkdir(exist_ok=False)
 fixes=[(196,202,221,'starfield trim cover'),(425.5,430.5,306,'Earth return cover'),(459.5,build['duration_s'],307,'Earth ending cover')]
 inputs=['-i',build['output']]
 for a,z,donor,label in fixes:inputs+=['-ss',str(donor),'-i',str(b.MASTER)]
 graph=[];prev='0:v'
 for i,(a,z,donor,label) in enumerate(fixes,1):
  dur=z-a;fadeout='' if i==len(fixes) else f',fade=t=out:st={dur-.4}:d=0.4:alpha=1'
  graph.append(f'[{i}:v]trim=duration={dur},setpts=PTS-STARTPTS,format=yuva420p,fade=t=in:st=0:d=0.4:alpha=1{fadeout},setpts=PTS+{a}/TB[p{i}]')
  graph.append(f'[{prev}][p{i}]overlay=enable=between(t\\,{a}\\,{z}):eof_action=pass[o{i}]');prev=f'o{i}'
 video=OUT/'024_light_undarkened_v03.mp4'
 b.run([*inputs,'-filter_complex_threads','1','-filter_complex',';'.join(graph),'-map',f'[{prev}]','-map','0:a','-frames:v',str(build['expected_frames']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(video)])
 for name in ['full_pixel_cuts.json','source_cuts.json']:shutil.copyfile(SRC/name,OUT/name)
 changes=json.loads((SRC/'changed_cuts.json').read_text())
 changes.extend(dict(row=label,timeline_in=a,timeline_out=z,source=b.MASTER.name,src_w=1920,upscale=1,donor_start_s=donor) for a,z,donor,label in fixes)
 (OUT/'changed_cuts.json').write_text(json.dumps(changes,indent=2)+'\n')
 build.update(output=str(video),sha256=b.sha(video),pixel_repairs=fixes,pixel_repair_reason='v03 edit QA has 14 failures at the subscribe trim, closing Orbit cover exit and ending trim. Replace dark neighbours, no waiver; fresh gates still required.')
 (OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n');print(video,flush=True)
if __name__=='__main__':main()
