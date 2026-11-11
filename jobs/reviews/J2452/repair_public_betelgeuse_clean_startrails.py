"""Repair only the rejected 93.1-99.0s cover with finished-master startrails."""
import json,shutil
from pathlib import Path
import build_public_betelgeuse as b
SRC=b.OUT.with_name('public_betelgeuse_v06')
OUT=SRC.with_name('public_betelgeuse_v07')
def main():
 OUT.mkdir(exist_ok=False)
 build=json.loads((SRC/'BUILD.json').read_text())
 assert b.sha(Path(build['output']))==build['sha256'], 'Prior candidate changed'
 assert b.sha(b.MASTER)==build['source_sha256'], 'Finished master changed'
 # Chapter clock ranges include pre-existing dissolves. Fade handles are outside forbidden images.
 patches=[(93.1,99.0,49.5,'chapter-2-clean-startrails',None)]
 pieces=[];cursor=0;enc=['-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-an']
 for i,(a,z,donor,label,c) in enumerate(patches):
  if a>cursor:
   dest=OUT/f'public_{i:02d}.mp4';b.run(['-ss',str(cursor),'-i',build['output'],'-frames:v',str(round((a-cursor)*30)),*enc,str(dest)]);pieces.append(dest)
  dur=z-a;source=Path(c['candidate_path']) if c else b.MASTER
  local=OUT/f'donor_{i:02d}.mp4'
  timing=f'(PTS-STARTPTS)*{dur/1.5}'
  if c:
   n=float(json.loads(b.sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(source)]))['format']['duration']);timing=f'(PTS-STARTPTS)*{dur/n}'
  lift=',eq=brightness=0.02' if c else ''
  b.run(['-ss',str(donor),'-t','1.5','-i',str(source),'-vf',f'setpts={timing},fps=30,scale=1920:1080{lift}','-frames:v',str(round(dur*30)),*enc,str(local)])
  dest=OUT/f'patch_{i:02d}.mp4'
  graph=f'[0:v]setpts=PTS-STARTPTS[base];[1:v]setpts=PTS-STARTPTS,format=yuva420p,fade=t=in:st=0:d=0.5:alpha=1,fade=t=out:st={dur-.5}:d=0.5:alpha=1[p];[base][p]overlay=eof_action=pass[v]'
  b.run(['-ss',str(a),'-i',build['output'],'-i',str(local),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-frames:v',str(round(dur*30)),*enc,str(dest)]);pieces.append(dest);cursor=z
  print('patched',label,flush=True)
 dest=OUT/'public_last.mp4';b.run(['-ss',str(cursor),'-i',build['output'],'-frames:v',str(build['expected_frames']-round(cursor*30)),*enc,str(dest)]);pieces.append(dest)
 listing=OUT/'concat.txt';listing.write_text(''.join(f"file '{p}'\n" for p in pieces))
 b.run(['-f','concat','-safe','0','-i',str(listing),'-i',build['output'],'-map','0:v','-map','1:a','-c','copy','-t',str(build['duration_s']),str(OUT/'029_betelgeuse_undarkened_v07.mp4')])
 for name in ['full_pixel_cuts.json','source_cuts.json']:shutil.copyfile(SRC/name,OUT/name)
 changes=json.loads((SRC/'changed_cuts.json').read_text())
 changes.extend(dict(row=label+'-expanded',timeline_in=a,timeline_out=z,source=label,framing=dict(offset=0),src_w=1920,upscale=1) for a,z,_,label,_ in patches)
 (OUT/'changed_cuts.json').write_text(json.dumps(changes,indent=2)+'\n')
 build.update(output=str(OUT/'029_betelgeuse_undarkened_v07.mp4'),edge_repair=patches,previous_candidate=str(SRC),sha256=b.sha(OUT/'029_betelgeuse_undarkened_v07.mp4'))
 (OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n')
if __name__=='__main__':main()
