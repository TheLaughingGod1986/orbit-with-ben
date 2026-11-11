#!/usr/bin/env python3
"""Next run: integrate the prepared title-free cover and rerun all chapter gates."""
import json,shutil
from pathlib import Path
import build_public_light as b
SRC=b.OUT.with_name('public_light_v04');OUT=b.OUT.with_name('public_light_v06')
PATCH=b.OUT.with_name('light_clean_starfield_v01')
def main():
 build=json.loads((SRC/'BUILD.json').read_text());patch=json.loads((PATCH/'BUILD.json').read_text())
 assert b.sha(Path(patch['output']))==patch['sha256']
 OUT.mkdir(exist_ok=False);video=OUT/'024_light_undarkened_v04.mp4'
 graph='[1:v]setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.6,format=yuva420p,fade=t=in:st=0:d=0.4:alpha=1,fade=t=out:st=6.2:d=0.4:alpha=1,setpts=PTS+196/TB[p];[0:v][p]overlay=enable=between(t\\,196\\,202.6):eof_action=pass[v]'
 b.run(['-i',build['output'],'-i',patch['output'],'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-map','0:a','-frames:v',str(build['expected_frames']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(video)])
 for name in ['full_pixel_cuts.json','source_cuts.json','changed_cuts.json']:shutil.copyfile(SRC/name,OUT/name)
 changes=json.loads((OUT/'changed_cuts.json').read_text())
 changes.append(dict(row='extended-title-free-cover',timeline_in=196,timeline_out=202.6,source='finished-master-title-free-221-224',src_w=1920,upscale=1))
 (OUT/'changed_cuts.json').write_text(json.dumps(changes,indent=2)+'\n')
 build.update(output=str(video),sha256=b.sha(video),starfield_repair=patch,starfield_hold_extension_s=0.6,starfield_exit_fade_s=[202.2,202.6],unwanted_cards_removed_verified=False,next='Run check_public_light.py --out public_light_v06 and inspect_public_light.py --out public_light_v06; verify no title at 199-202s, including fade edges. Only then mark verified, set darken SRC to v06, grade and NAS-save.')
 (OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n');print(video)
if __name__=='__main__':main()
