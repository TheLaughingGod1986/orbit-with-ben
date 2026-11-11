"""Lift only the edited last-card neighbourhood before normal gates and sleep grade."""
import json,shutil
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import build_public_proxima as b
SRC=b.OUT.with_name('public_proxima_v02');OUT=b.OUT.with_name('public_proxima_v05')
def main():
 OUT.mkdir(exist_ok=False);r=json.loads((SRC/'BUILD.json').read_text());v=OUT/'026_proxima_undarkened_v05.mp4'
 vf="eq=brightness='0.10*max(0,min(1,min(t-357,378-t)))':eval=frame"
 for k,text in enumerate(['ESO','ESA/Hubble & NASA']):
  im=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(im);d.text((40,1015),text,font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',28),fill=(255,255,255,204));im.save(OUT/f'credit_{k}.png')
 graph=f"[0:v]{vf}[base];[base][1:v]overlay=0:0:enable='between(t,115.1,125.8)'[a];[a][2:v]overlay=0:0:enable='between(t,292.2,304.1)'[v]"
 b.run(['-i',r['output'],'-loop','1','-i',str(OUT/'credit_0.png'),'-loop','1','-i',str(OUT/'credit_1.png'),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-map','0:a','-frames:v',str(r['expected_frames']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy','-t',str(r['duration_s']),str(v)])
 for n in ['source_cuts.json','full_pixel_cuts.json']:shutil.copyfile(SRC/n,OUT/n)
 c=json.loads((SRC/'changed_cuts.json').read_text());c.append(dict(row='last-card-pixel-repair',timeline_in=357,timeline_out=378,source='last-card-pixel-repair',framing=dict(offset=0),src_w=1920,upscale=1));(OUT/'changed_cuts.json').write_text(json.dumps(c,indent=2)+'\n');r.update(output=str(v),sha256=b.sha(v),pixel_repair=dict(interval=[357,378],filter=vf,credits='Added ESO and ESA/Hubble & NASA corner credits to new starfield covers; credit and licence copied from pool_v03.json',reason='Near-black failures in newly changed last-card neighbourhood; no waiver. Smooth one-second ramps, source motion and narration unchanged.'));(OUT/'BUILD.json').write_text(json.dumps(r,indent=2)+'\n');print(v)
if __name__=='__main__':main()
