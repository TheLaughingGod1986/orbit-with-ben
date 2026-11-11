#!/usr/bin/env python3
"""Repair only the saved subscribe dissolve; preserve clock and all other parts."""
import json
from pathlib import Path
import build_public_venus as b
SRC=b.OUT
OUT=SRC.with_name('public_venus_v02')
def main():
 OUT.mkdir(exist_ok=False)
 build=json.loads((SRC/'BUILD.json').read_text())
 # Candidate v01 stills locate the residual pill only in join_02 at 204–205.5s.
 # The incoming master shot is clean by 219.7s; use that same shot's clean
 # one-second window for the incoming handle, leaving all narration unchanged.
 graph='[0:v]trim=start=2.2:end=3.2,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1[a];[1:v]trim=start=1.5:end=2.5,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=1[b];[a][b]xfade=transition=fade:duration=2:offset=0,format=yuv420p[v]'
 join=OUT/'join_02.mp4'
 b.run(['-i',str(SRC/'piece_02.mp4'),'-i',str(SRC/'piece_03.mp4'),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-t','2',*b.enc(),str(join)])
 listing=(SRC/'concat.txt').read_text().replace(str(SRC/'join_02.mp4'),str(join))
 (OUT/'concat.txt').write_text(listing)
 video=OUT/'023_venus_undarkened_v02.mp4'
 b.run(['-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-i',str(b.NARR),'-map','0:v','-map','1:a','-af','volume=-0.5dB','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(build['duration_s']),str(video)])
 for name in ['full_pixel_cuts.json','changed_cuts.json','source_cuts.json']:
  (OUT/name).write_bytes((SRC/name).read_bytes())
 build.update(output=str(video),sha256=b.sha(video),status='REPAIRED_CANDIDATE_REQUIRES_NEW_GATES',repair='Only join_02 incoming picture handle advances 1.5s within same master shot to omit lingering Subscribe pill. Narration clock unchanged; inspect edges and rerun full gates.')
 (OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n')
 print(video,flush=True)
if __name__=='__main__':main()
