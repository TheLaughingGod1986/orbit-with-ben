#!/usr/bin/env python3
"""Repair the new-title neighbourhood's measured near-black opening, preserving clock."""
import json,shutil
from pathlib import Path
import build_public_light as b
SRC=b.OUT; OUT=SRC.with_name('public_light_v03')
def main():
 build=json.loads((SRC/'BUILD.json').read_text());OUT.mkdir(exist_ok=False)
 cover=OUT/'opening.mp4'
 graph='[0:v]setpts=PTS-STARTPTS,scale=1920:1080,setsar=1,fps=30,format=yuv420p[base];[1:v]format=rgba,fade=t=in:st=0:d=1.5:alpha=1,fade=t=out:st=4.5:d=1.5:alpha=1[t];[base][t]overlay=0:0:enable=lt(t\\,6)[v]'
 b.run(['-ss','303','-i',str(b.MASTER),'-loop','1','-i',str(SRC/'title.png'),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-frames:v','270',*b.enc(),str(cover)])
 first=OUT/'opening_interior.mp4';b.run(['-i',str(cover),'-frames:v','240',*b.enc(),str(first)])
 join=OUT/'opening_join.mp4';graph='[0:v]trim=start=8:end=9,setpts=PTS-STARTPTS[a];[1:v]trim=start=8:end=9,setpts=PTS-STARTPTS[b];[a][b]xfade=transition=fade:duration=1:offset=0,format=yuv420p[v]'
 b.run(['-i',str(cover),'-i',build['output'],'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-frames:v','30',*b.enc(),str(join)])
 rest=OUT/'rest.mp4';b.run(['-ss','9','-i',build['output'],'-frames:v',str(build['expected_frames']-270),*b.enc(),str(rest)])
 listing=OUT/'concat.txt';listing.write_text(''.join(f"file '{p}'\n" for p in [first,join,rest]))
 final=OUT/'024_light_undarkened_v02.mp4';b.run(['-f','concat','-safe','0','-i',str(listing),'-i',build['output'],'-map','0:v','-map','1:a','-c','copy','-t',str(build['duration_s']),str(final)])
 for name in ['full_pixel_cuts.json','source_cuts.json']:
  shutil.copyfile(SRC/name,OUT/name)
 changes=json.loads((SRC/'changed_cuts.json').read_text());changes.append(dict(row='opening-cover',timeline_in=0,timeline_out=9,source='finished-master-Earth-neighbour',src_w=1920,upscale=1));(OUT/'changed_cuts.json').write_text(json.dumps(changes,indent=2)+'\n')
 build.update(output=str(final),sha256=b.sha(final),opening_repair='New-title neighbourhood failed near-black check. Cover chapter 0-8 seconds with finished-master Earth/ISS 303-311s, dissolve over 8-9 seconds to original picture. Same narration clock and frame count; no source search or generation.')
 (OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n');print(final,flush=True)
if __name__=='__main__':main()
