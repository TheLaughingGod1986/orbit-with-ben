#!/usr/bin/env python3
"""Remove outgoing Orbit ghost frames; preserve all candidate versions and VO timing."""
import json,shutil
from pathlib import Path
import build_public_andromeda as b
SRC=b.OUT;OUT=SRC.with_name('public_andromeda_v04')
def main():
 OUT.mkdir(exist_ok=False)
 report=json.loads((SRC/'BUILD.json').read_text());rows=json.loads((SRC/'source_cuts.json').read_text())
 pieces=[SRC/f'piece_{i:02d}.mp4' for i in range(len(rows))]
 changed={2,4,12}
 for i in changed:
  p=OUT/f'piece_{i:02d}.mp4';n=round((rows[i]['timeline_out']-rows[i]['timeline_in'])*30);keep=n-90
  b.run(['-i',str(pieces[i]),'-vf',f'trim=end_frame={keep},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=3','-frames:v',str(n),*b.enc(),str(p)])
  pieces[i]=p;rows[i]['repair']='Last three seconds held on preceding clean source frame; eliminates first Orbit frame in outgoing dissolve. No narration movement.'
 durations=[r['timeline_out']-r['timeline_in'] for r in rows]
 halves=[round(min(1,durations[i]/3,durations[i+1]/3)*30)/30 for i in range(len(rows)-1)]
 joined=[]
 for i,(p,dur) in enumerate(zip(pieces,durations)):
  a=halves[i-1] if i else 0;z=dur-(halves[i] if i<len(rows)-1 else 0)
  dst=SRC/f'interior_v02_{i:02d}.mp4'
  if i in changed:
   dst=OUT/dst.name;b.run(['-ss',str(a),'-i',str(p),'-t',str(z-a),*b.enc(),str(dst)])
  joined.append(dst)
  if i==len(rows)-1:continue
  dst=SRC/f'join_v02_{i:02d}.mp4'
  if i in changed or i+1 in changed:
   h=halves[i];width=2*h;dst=OUT/dst.name
   graph=f'[0:v]trim=start={dur-h}:end={dur},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={h}[a];[1:v]trim=end={h},setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration={h}[b];[a][b]xfade=transition=fade:duration={width}:offset=0,format=yuv420p[v]'
   b.run(['-i',str(p),'-i',str(pieces[i+1]),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-t',str(width),*b.enc(),str(dst)])
  joined.append(dst)
 listing=OUT/'concat.txt';listing.write_text(''.join(f"file '{p}'\n" for p in joined));final=OUT/'019_andromeda_undarkened_v02.mp4'
 b.run(['-f','concat','-safe','0','-i',str(listing),'-i',str(b.NARR),'-map','0:v','-map','1:a','-af','volume=-0.5dB','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(report['duration_s']),str(final)])
 changes=json.loads((SRC/'changed_cuts.json').read_text())
 for i in changed:changes.append(dict(row=f'clean-tail-{i}',timeline_in=rows[i]['timeline_out']-3,timeline_out=rows[i]['timeline_out'],source=f'clean-tail-{i}',framing=dict(offset=0),src_w=1280,upscale=1.5))
 (OUT/'changed_cuts.json').write_text(json.dumps(changes,indent=2)+'\n');shutil.copyfile(SRC/'full_pixel_cuts.json',OUT/'full_pixel_cuts.json')
 (OUT/'source_cuts.json').write_text(json.dumps(rows,indent=2)+'\n')
 report.update(output=str(final),sha256=b.sha(final),repair='Three outgoing tails held on preceding clean frames; all saved-candidate checks and cover inspection must be repeated. No gate waived.')
 (OUT/'BUILD.json').write_text(json.dumps(report,indent=2)+'\n');print(final,flush=True)
if __name__=='__main__':main()
