#!/usr/bin/env python3
"""Replace repeated closing sky with the film's cleared Earth photograph."""
import argparse,json,subprocess
from pathlib import Path
from build_orion_source_repair import sha,run
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
base=Path('/Users/ben/_desk/J2452-sleep-scratch/crab_reuse_v02/029_picture_crab_repaired.mp4')
assert sha(base)=='78dc108fc34a242733b8ba65bfe331c110ce9275c2bb3ba51d9bf1d8531bde39'
cs=json.loads((base.parent/'cuts.json').read_text());row=next(c for c in cs if c['plate_id']=='r38_night')
assert sum(c['source']=='blue_marble.jpg' for c in cs)==1
src=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/blue_marble.jpg')
pool=json.loads(Path('02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/SOURCE_POOL_v03.json').read_text());asset=next(x for x in pool['assets'] if x['id']=='blue_marble');assert asset['status']=='ok'
original_lo=round(row['timeline_in']*30);lo,hi=original_lo-6,round(row['timeline_out']*30);n=hi-lo
prev=cs[cs.index(row)-1];assert prev['plate_id']=='r38_m42';prev['timeline_out']=lo/30;row['timeline_in']=lo/30
a.out.mkdir(parents=True,exist_ok=False)
credit=Image.new('RGBA',(1920,1080));ImageDraw.Draw(credit).text((45,1025),'NASA / Apollo 17',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',27),fill=(234,230,223,180));credit.save(a.out/'credit.png')
enc=['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','6','-r','30','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000']
# Fit the entire Earth into the central 1000px; black source space extends
# naturally across 16:9, rather than cropping the planet or inventing detail.
im=Image.open(src).convert('RGB');mask=im.convert('L').point(lambda x:255 if x>15 else 0);box=mask.getbbox();assert box;im=im.crop(box);im.thumbnail((3400,2000));canvas=Image.new('RGB',(3840,2160));canvas.paste(im,((3840-im.width)//2,(2160-im.height)//2));canvas.save(a.out/'earth.png')
patch=a.out/'earth.mp4';graph=f"[0:v]zoompan=z='1+0.012*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=3840x2160:fps=30,scale=1920:1080:flags=lanczos,colorchannelmixer=rr=.85:gg=.85:bb=.85,limiter=min=16:max=180:planes=1[p];[p][1:v]overlay,format=yuv420p[v]"
run(['-loop','1','-i',str(a.out/'earth.png'),'-loop','1','-i',str(a.out/'credit.png'),'-filter_complex',graph,'-map','[v]','-frames:v',str(n),*enc,str(patch)])
for name,t in [('before',(lo-1)/30),('after',hi/30)]:run(['-i',str(base),'-vf',f"select='eq(n,{round(t*30)})'",'-frames:v','1',str(a.out/(name+'.png'))])
dissolved=a.out/'earth_dissolved.mp4';graph=f"[0:v][1:v]overlay=enable='gte(t,{n/60})'[bg];[2:v]format=yuva420p,fade=t=in:st=0:d=0.5:alpha=1,fade=t=out:st={n/30-.5}:d=0.5:alpha=1[p];[bg][p]overlay,format=yuv420p[v]"
run(['-loop','1','-i',str(a.out/'before.png'),'-loop','1','-i',str(a.out/'after.png'),'-i',str(patch),'-filter_complex',graph,'-map','[v]','-frames:v',str(n),*enc,str(dissolved)])
out=a.out/'029_picture_home_earth.mp4';graph=f"[1:v]setpts=PTS-STARTPTS+{lo}/30/TB[p];[0:v][p]overlay=eof_action=pass:enable='between(t,{lo/30},{(hi-.5)/30})',format=yuv420p[v]"
run(['-i',str(base),'-i',str(dissolved),'-filter_complex',graph,'-map','[v]','-frames:v','14829',*enc,str(out)])
run(['-i',str(out),'-f','null','-'])
row.update(previous_source=row['source'],source=src.name,kind='still',framing={'box':[0,0,1,1],'pct':.012},upscale=1,overlays=[],credit='NASA / Apollo 17',sleep_repair=str(patch),sleep_repair_fades_s=.5)
(a.out/'cuts.json').write_text(json.dumps(cs,indent=2)+'\n')
r=dict(status='BOUNDED_REPAIR_NOT_FINAL_QA_OR_UAT',base=str(base),base_sha256=sha(base),source=str(src),source_sha256=sha(src),provenance=asset,source_crop_pixels=list(box),output=str(out),sha256=sha(out),patch=str(patch),dissolved=str(dissolved),dissolved_sha256=sha(dissolved),frames=14829,duration_s=494.3,chapter_replace_frames=[lo,hi],master_range_s=row['master_range_s'],spoken_line='The bigger question is closer to home.',limitations=['A second appearance of the same real Earth photograph, not a new observation.','0.5-second dissolves use neighbouring frames; narration and master unchanged.','Remaining graphics, reuse and full compilation checks remain.'])
(a.out/'REPORT.json').write_text(json.dumps(r,indent=2)+'\n');print(out)
