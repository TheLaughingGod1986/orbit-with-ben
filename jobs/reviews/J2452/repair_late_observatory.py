#!/usr/bin/env python3
"""Replace repeated La Silla footage with the film's own cleared Gemini photo.

A bounded chapter repair, without changing the source master or audio clock.
"""
import argparse,json,subprocess
from pathlib import Path
from build_orion_source_repair import sha,run

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 base=Path('/Users/ben/_desk/J2452-sleep-scratch/closing_integrated_v01/029_picture_closing_repaired.mp4')
 assert sha(base)=='e98ee41b19755d7b42e0b96e28d9bcf1d83b4b43e4e1d33bc91a958dd0c3d8d8'
 cuts=json.loads((base.parent/'cuts.json').read_text());row=next(c for c in cuts if c['plate_id']=='r30_vlt')
 assert sum(c['source']=='gemini_night.jpg' for c in cuts)==1
 source=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/gemini_night.jpg')
 pool=json.loads(Path('02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/SOURCE_POOL_v03.json').read_text())
 asset=next(x for x in pool['assets'] if x['id']=='gemini_night');assert asset['status']=='ok'
 lo,hi=round(row['timeline_in']*30),round(row['timeline_out']*30);n=hi-lo
 a.out.mkdir(parents=True,exist_ok=False)
 from PIL import Image,ImageDraw,ImageFont
 credit=Image.new('RGBA',(1920,1080));ImageDraw.Draw(credit).text((45,1025),'Gemini North / NOIRLab / P. Horalek',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',27),fill=(234,230,223,140));credit.save(a.out/'credit.png')
 enc=['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','6','-r','30','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000']
 # A slow crop of the real photograph, no invented geometry or subject substitution.
 # Gemini is an establishing plate under "Not in our lifetimes, almost certainly";
 # it is not presented as VLT or a resolved image of Betelgeuse.
 prepared=a.out/'source_crop.png'
 run(['-i',str(source),'-frames:v','1','-vf','scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160',str(prepared)])
 patch=a.out/'observatory.mp4'
 graph=f"[0:v]zoompan=z='1.015+0.015*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,colorchannelmixer=rr=.85:gg=.85:bb=.85,limiter=min=16:max=180:planes=1[plate];[plate][1:v]overlay=0:0,format=yuv420p[v]"
 run(['-loop','1','-i',str(prepared),'-loop','1','-i',str(a.out/'credit.png'),'-filter_complex',graph,'-map','[v]','-frames:v',str(n),*enc,str(patch)])
 # Build two-second endpoint dissolves from neighbouring shots, never from
 # the repeated La Silla shot being removed. Narration time is unchanged.
 before=a.out/'before.png';after=a.out/'after.png'
 run(['-ss',str((lo-1)/30),'-i',str(base),'-frames:v','1',str(before)])
 run(['-ss',str(hi/30),'-i',str(base),'-frames:v','1',str(after)])
 dissolved=a.out/'observatory_dissolved.mp4'
 graph=f"[0:v][1:v]overlay=enable='gte(t,{n/60})'[bg];[2:v]format=yuva420p,fade=t=in:st=0:d=2:alpha=1,fade=t=out:st={n/30-2}:d=2:alpha=1[p];[bg][p]overlay,format=yuv420p[v]"
 run(['-loop','1','-i',str(before),'-loop','1','-i',str(after),'-i',str(patch),'-filter_complex',graph,'-map','[v]','-frames:v',str(n),*enc,str(dissolved)])
 output=a.out/'029_picture_observatory_repaired.mp4'
 graph=f"[1:v]setpts=PTS-STARTPTS+{lo}/30/TB[p];[0:v][p]overlay=eof_action=pass:enable='between(t,{lo/30},{(hi-.5)/30})',format=yuv420p[v]"
 run(['-i',str(base),'-i',str(dissolved),'-filter_complex',graph,'-map','[v]','-frames:v','14829',*enc,str(output)])
 run(['-i',str(output),'-f','null','-'])
 s=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(output)]))['streams'][0];assert int(s['nb_read_frames'])==14829
 row['previous_source']=row['source'];row.update(source=source.name,kind='still',framing={'box':[0,0,1,1],'pct':.015},upscale=1,credit=asset['credit']+' · CC BY 4.0',sleep_repair=str(patch),sleep_repair_fades_s=2)
 (a.out/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
 report=dict(status='BOUNDED_OBSERVATORY_REPAIR_NOT_FINAL_QA_OR_UAT',base=str(base),base_sha256=sha(base),source=str(source),source_sha256=sha(source),provenance=asset,patch=str(patch),patch_sha256=sha(patch),dissolved=str(dissolved),dissolved_sha256=sha(dissolved),output=str(output),sha256=sha(output),frames=14829,duration_s=494.3,chapter_replace_frames=[lo,hi],master_range_s=row['master_range_s'],limitations=['Two two-second endpoint dissolves use neighbouring shot holds; the repeated La Silla shot is fully removed.','Not VLT; no location is named in this spoken window.','Normal combined source/pixel QA and saved-frame readback remain.','Other reuse, graphics, twelve picture chapters and final assembly remain.'])
 (a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(output)
if __name__=='__main__':main()
