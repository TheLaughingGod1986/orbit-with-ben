#!/usr/bin/env python3
"""Restore two rounded frame gaps at their exact timeline boundaries, not at the end."""
import json,shutil
from pathlib import Path
import build_public_andromeda as b
SRC=b.OUT.with_name('public_andromeda_v04');OUT=SRC.with_name('public_andromeda_v05')
def main():
 OUT.mkdir(exist_ok=False);r=json.loads((SRC/'BUILD.json').read_text());rows=json.loads((SRC/'source_cuts.json').read_text());paths=[Path(l[6:-1]) for l in (SRC/'concat.txt').read_text().splitlines()];changes=json.loads((SRC/'changed_cuts.json').read_text());fixes=[]
 for i,row in enumerate(rows[:-1]):
  gap=round((rows[i+1]['timeline_in']-row['timeline_out'])*30)
  if not gap:continue
  assert gap==1 and i in (7,9)
  p=paths[2*i];dst=OUT/f'interior_fixed_{i:02d}.mp4'
  import subprocess as sp
  n=int(json.loads(sp.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(p)]))['streams'][0]['nb_frames'])
  b.run(['-i',str(p),'-vf','tpad=stop_mode=clone:stop_duration=0.1','-frames:v',str(n+1),*b.enc(),str(dst)]);paths[2*i]=dst
  fixes.append(dict(piece=i,frame_added_at_s=row['timeline_out'],reason='Floating-point rounding evaluated end differently from next start; add held frame inside same clean piece.'))
  row['timeline_out']=rows[i+1]['timeline_in']
 listing=OUT/'concat.txt';listing.write_text(''.join(f"file '{p}'\n" for p in paths));final=OUT/'019_andromeda_undarkened_v03.mp4'
 b.run(['-f','concat','-safe','0','-i',str(listing),'-i',str(b.NARR),'-map','0:v','-map','1:a','-af','volume=-0.5dB','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(r['duration_s']),str(final)])
 for name in ['full_pixel_cuts.json','changed_cuts.json']:shutil.copyfile(SRC/name,OUT/name)
 (OUT/'source_cuts.json').write_text(json.dumps(rows,indent=2)+'\n');r.update(output=str(final),sha256=b.sha(final),rounding_repairs=fixes,unwanted_cards_removed_verified=False)
 (OUT/'BUILD.json').write_text(json.dumps(r,indent=2)+'\n');print(final)
if __name__=='__main__':main()
