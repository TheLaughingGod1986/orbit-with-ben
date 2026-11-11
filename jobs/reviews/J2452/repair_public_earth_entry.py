#!/usr/bin/env python3
"""Repair the remaining changed-window pixels and restore the quiet chapter title."""
import json
import build_public_earth as b
SRC=b.OUT.with_name('public_earth_v03')
OUT=b.OUT.with_name('public_earth_v04')
def main():
 OUT.mkdir(exist_ok=False)
 build=json.loads((SRC/'BUILD.json').read_text())
 final=OUT/'027_earth_undarkened_v04.mp4'
 graph="[0:v]setpts=PTS-STARTPTS[base];[1:v]setpts=3*(PTS-STARTPTS),fps=30,scale=1920:1080,setsar=1,format=rgba,fade=t=in:st=0:d=1:alpha=1,fade=t=out:st=8:d=1:alpha=1,setpts=PTS+57/TB[patch];[base][patch]overlay=eof_action=pass:enable=between(t\\,57\\,66)[fixed];[2:v]format=rgba,fade=t=in:st=0:d=1.5:alpha=1,fade=t=out:st=4.5:d=1.5:alpha=1[title];[fixed][title]overlay=0:0:enable=lt(t\\,6)[out]"
 b.run(['-i',build['output'],'-ss','54','-t','3','-i',str(b.MASTER),'-loop','1','-i',str(b.OUT/'title.png'),'-filter_complex_threads','1','-filter_complex',graph,'-map','[out]','-map','0:a','-frames:v',str(build['expected_frames']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(final)])
 changes=json.loads((SRC/'changed_cuts.json').read_text())
 changes.append(dict(row='northpole-entry-repair',timeline_in=57,timeline_out=66,source='northpole-entry-repair',framing=dict(offset=0),src_w=1920,upscale=1))
 build.update(output=str(final),sha256=b.sha(final),parent_candidate=str(SRC),quiet_title_verified=False,title_follow_up='Restored original quiet-title overlay; inspect encoded frame before delivery.',entry_repair=dict(chapter_in_s=57,chapter_out_s=66,master_donor_in_s=54,donor_duration_s=3,reason='Three remaining near-black edit-neighbourhood samples; neighbouring daylight ISS master stretch, inspected at one-second intervals before use.'))
 for name,data in [('BUILD.json',build),('changed_cuts.json',changes)]: (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
 (OUT/'full_pixel_cuts.json').write_text((SRC/'full_pixel_cuts.json').read_text())
 print(final,flush=True)
if __name__=='__main__':main()
