#!/usr/bin/env python3
"""Move the quiet name above the source film's Opportunity caption before QA."""
import json
from PIL import Image,ImageDraw,ImageFont
import build_public_mars as b
SRC=b.OUT.with_name('public_mars_v02');OUT=b.OUT.with_name('public_mars_v03')
def main():
 OUT.mkdir(exist_ok=False)
 build=json.loads((SRC/'BUILD.json').read_text())
 im=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(im)
 d.text((90,80),'IV · Night on the Red Dust',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',42),fill=(234,230,223,166));im.save(OUT/'title.png')
 video=OUT/'025_mars_undarkened_v03.mp4'
 graph='[1:v]setpts=PTS-STARTPTS,format=yuv420p[clean];[0:v][clean]overlay=eof_action=pass:enable=lt(t\\,7)[base];[2:v]format=rgba,fade=t=in:st=0:d=1.5:alpha=1,fade=t=out:st=4.5:d=1.5:alpha=1[title];[base][title]overlay=enable=lt(t\\,6)[v]'
 b.run(['-i',build['output'],'-t','7','-i',str(b.MASTER),'-loop','1','-i',str(OUT/'title.png'),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-map','0:a','-frames:v',str(build['expected_frames']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(video)])
 changes=json.loads((SRC/'changed_cuts.json').read_text());changes.append(dict(row='quiet-title-repair',timeline_in=0,timeline_out=7,source='quiet-title-repair',framing=dict(offset=0),src_w=1920,upscale=1))
 build.update(output=str(video),sha256=b.sha(video),parent_candidate=str(SRC),quiet_title_repair='Original source picture restored over the first seven seconds, with quiet name at y=80; source Opportunity label remains at bottom. Inspect frame at three seconds before delivery.')
 (OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n')
 (OUT/'changed_cuts.json').write_text(json.dumps(changes,indent=2)+'\n')
 (OUT/'full_pixel_cuts.json').write_text((SRC/'full_pixel_cuts.json').read_text())
 print(video,flush=True)
if __name__=='__main__':main()
