"""Lift only the edited last-card neighbourhood before normal gates and sleep grade."""
import json,shutil
from pathlib import Path
import build_public_proxima as b
SRC=b.OUT.with_name('public_proxima_v02');OUT=b.OUT.with_name('public_proxima_v03')
def main():
 OUT.mkdir(exist_ok=False);r=json.loads((SRC/'BUILD.json').read_text());v=OUT/'026_proxima_undarkened_v03.mp4'
 vf="eq=brightness='0.10*max(0,min(1,min(t-357,378-t)))':eval=frame"
 b.run(['-i',r['output'],'-vf',vf,'-map','0:v','-map','0:a','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(v)])
 for n in ['source_cuts.json','full_pixel_cuts.json']:shutil.copyfile(SRC/n,OUT/n)
 c=json.loads((SRC/'changed_cuts.json').read_text());c.append(dict(row='last-card-pixel-repair',timeline_in=357,timeline_out=378,source='last-card-pixel-repair',framing=dict(offset=0),src_w=1920,upscale=1));(OUT/'changed_cuts.json').write_text(json.dumps(c,indent=2)+'\n');r.update(output=str(v),sha256=b.sha(v),pixel_repair=dict(interval=[357,378],filter=vf,reason='Near-black failures in newly changed last-card neighbourhood; no waiver. Smooth one-second ramps, source motion and narration unchanged.'));(OUT/'BUILD.json').write_text(json.dumps(r,indent=2)+'\n');print(v)
if __name__=='__main__':main()
