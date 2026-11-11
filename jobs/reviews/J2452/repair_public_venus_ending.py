#!/usr/bin/env python3
"""Cover the ending trim with neighbouring finished-master picture; keep audio clock."""
import json
import build_public_venus as b
SRC=b.OUT.with_name('public_venus_v02');OUT=SRC.with_name('public_venus_v03')
def main():
 OUT.mkdir(exist_ok=False)
 build=json.loads((SRC/'BUILD.json').read_text())
 # The final crescent sky fails low detail at the new ending trim. Extend
 # neighbouring Venus picture, as permitted by the brief, with no replay loop.
 a=477.4;z=build['duration_s'];donor=480;duration=12
 graph=f'[0:v]setpts=PTS-STARTPTS[base];[1:v]setpts={(z-a)/duration}*(PTS-STARTPTS),fps=30,scale=1920:1080,setsar=1,format=rgba,fade=t=in:st=0:d=1:alpha=1,setpts=PTS+{a}/TB[p];[base][p]overlay=eof_action=repeat:enable=gte(t\\,{a})[v]'
 final=OUT/'023_venus_undarkened_v03.mp4'
 b.run(['-i',build['output'],'-ss',str(donor),'-t',str(duration),'-i',str(b.MASTER),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-map','0:a','-frames:v',str(build['expected_frames']),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-r','30','-video_track_timescale','90000','-c:a','copy',str(final)])
 changes=json.loads((SRC/'changed_cuts.json').read_text());changes.append(dict(row='ending-cover',timeline_in=a,timeline_out=z,source='ending-cover',framing=dict(offset=0),src_w=1920,upscale=1))
 build.update(output=str(final),sha256=b.sha(final),parent_candidate=str(SRC),ending_repair=dict(chapter_in_s=a,chapter_out_s=z,master_donor_in_s=donor,donor_duration_s=duration,reason='New ending trim low-detail failure; extend neighbouring finished-master Venus shot with one-second dissolve. Whole narration unchanged.'),status='REPAIRED_CANDIDATE_REQUIRES_NEW_GATES')
 for name in ['full_pixel_cuts.json','source_cuts.json']:(OUT/name).write_bytes((SRC/name).read_bytes())
 (OUT/'changed_cuts.json').write_text(json.dumps(changes,indent=2)+'\n');(OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n')
if __name__=='__main__':main()
