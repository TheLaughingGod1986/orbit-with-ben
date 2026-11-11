#!/usr/bin/env python3
"""Build a bounded original-source repair for 029 row 36; never approve compilation."""
import argparse, hashlib, json, subprocess
from pathlib import Path

def sha(p):
    with p.open('rb') as h:return hashlib.file_digest(h,'sha256').hexdigest()
def run(args):
    subprocess.run(['ffmpeg','-hide_banner','-v','error','-nostdin','-n',*args],check=True)
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    source=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/orion_rise_vlt.mp4')
    out=a.out/'orion_source_repair.mp4'
    # Alternate clean Orion footage already in the film pool.
    # Modest source exposure +0.263 stops before the required sleep darkening.
    # Use 6.6 seconds of native 6.8-second source; no retiming, loops or endpoint clones.
    from PIL import Image, ImageDraw, ImageFont
    overlay=Image.new('RGBA',(1920,1080))
    ImageDraw.Draw(overlay).text((45,1025),'ESO/B. Tafreshi (twanight.org)',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',27),fill=(234,230,223,140))
    credit=a.out/'credit.png';overlay.save(credit)
    graph="setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,fps=30,colorchannelmixer=rr=1.2:gg=1.2:bb=1.2,colorchannelmixer=rr=.85:gg=.85:bb=.85,limiter=min=16:max=180:planes=1,format=yuv420p[plate];[plate][1:v]overlay=0:0,format=yuv420p[v]"
    run(['-i',str(source),'-loop','1','-i',str(credit),'-filter_complex','[0:v]'+graph,'-map','[v]','-frames:v','198','-an','-c:v','libx264','-preset','fast','-crf','18','-threads','4','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000',str(out)])
    run(['-i',str(out),'-f','null','-'])
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(out)]))['streams'][0]
    assert int(info['nb_read_frames'])==198
    # Round absolute timeline endpoints, not each independent duration.
    assert round(439.09*30)-round(432.5*30)==198
    cuts=[dict(row='36',source=source.name,kind='video',timeline_in=0,timeline_out=6.6,upscale=1,framing=dict(offset=0,speed=1))]
    (a.out/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
    report=dict(status='SOURCE_REPAIR_CANDIDATE_NOT_INTEGRATED_NOT_UAT',source=str(source),source_sha256=sha(source),output=str(out),sha256=sha(out),frames=198,duration_s=6.6,master_range_s=[453,459.59],chapter_range_s=[432.5,439.09],used_chapter_frames=[12975,13173],filter=graph,provenance=dict(id='vlttimelapseorion',title='VLT Auxiliary Telescopes time-lapse (Orion rising)',page='https://www.eso.org/public/videos/vlttimelapseorion/',credit='ESO/B. Tafreshi (twanight.org)',licence='CC BY 4.0 per film SOURCE_POOL_v03.json; existing asset, no download'),limitations=['Not Betelgeuse resolved surface or companion imagery. Orion sky establishing shot under closing question.','Source still requires full-frame framing review and normal gates.','No source-master or narration modification.','Six dark spans, graphics, reuse and full compilation work remain.'])
    (a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    for n,t in enumerate([0,1.65,3.3,4.95,6.5666667]):run(['-ss',str(t),'-i',str(out),'-frames:v','1','-vf','scale=960:540',str(a.out/f'frame_{n}.jpg')])
    print(out)
if __name__=='__main__':main()
