#!/usr/bin/env python3
"""Replace two third-use Betelgeuse stills with an official ALMA observation."""
import argparse,json,subprocess
from pathlib import Path
from build_orion_source_repair import sha,run
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
base=Path('/Users/ben/_desk/J2452-sleep-scratch/home_earth_v04/029_picture_home_earth.mp4')
assert sha(base)=='759c3d853b0a5d87fae4ac1471091cf87cb899f41197b6c1f91be2de3682b9cd'
src=Path('/Users/ben/_desk/J2452-sleep-scratch/alma_betelgeuse_source_v01/potw1726a.jpg')
assert sha(src)=='3f75e8b1df70dca7f0e828e8fd640880a7bfcbdef0945304792bace2eb243bbe'
cs=json.loads((base.parent/'cuts.json').read_text());a.out.mkdir(parents=True,exist_ok=False)
credit='ALMA (ESO/NAOJ/NRAO)/E. O’Gorman/P. Kervella'
asset=dict(id='potw1726a',title='Betelgeuse captured by ALMA',credit=credit,licence='CC BY 4.0',page='https://www.eso.org/public/images/potw1726a/',file='https://cdn.eso.org/images/publicationjpg/potw1726a.jpg',terms='https://www.eso.org/public/outreach/copyright/',status='ok',note='Observation at 338 GHz; no labels, no simulation. Cropped, gently pushed and darkened; not a before/after epoch comparison.')
(a.out/'pool.json').write_text(json.dumps([dict(asset,source=src.name)],indent=2)+'\n')
im=Image.open(src).convert('RGB');assert im.size==(4000,4000)
# Central-lower 16:9 crop contains the complete emitting surface; no padding.
im.crop((0,1000,4000,3250)).save(a.out/'plate.png')
c=Image.new('RGBA',(1920,1080));ImageDraw.Draw(c).text((45,1025),credit,font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',27),fill=(234,230,223,200));c.save(a.out/'credit.png')
enc=['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','6','-r','30','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000']
patches=[]
for plate_id in ['r07_sphere_jan','r36_visir']:
 row=next(c for c in cs if c['plate_id']==plate_id);lo,hi=round(row['timeline_in']*30),round(row['timeline_out']*30);lo-=15;n=hi-lo
 prev=cs[cs.index(row)-1];prev['timeline_out']=lo/30;row['timeline_in']=lo/30
 patch=a.out/(plate_id+'.mp4')
 graph=f"[0:v]zoompan=z='1+0.012*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,colorchannelmixer=rr=.85:gg=.85:bb=.85,limiter=min=16:max=180:planes=1[p];[p][1:v]overlay,format=yuv420p[v]"
 run(['-loop','1','-i',str(a.out/'plate.png'),'-loop','1','-i',str(a.out/'credit.png'),'-filter_complex',graph,'-map','[v]','-frames:v',str(n),*enc,str(patch)])
 for name,frame in [('before',lo-1),('after',hi)]:run(['-i',str(base),'-vf',f"select='eq(n,{frame})'",'-frames:v','1',str(a.out/(plate_id+'_'+name+'.png'))])
 dissolved=a.out/(plate_id+'_dissolved.mp4')
 graph=f"[0:v][1:v]overlay=enable='gte(t,{n/60})'[bg];[2:v]format=yuva420p,fade=t=in:st=0:d=0.5:alpha=1,fade=t=out:st={n/30-.5}:d=0.5:alpha=1[p];[bg][p]overlay,format=yuv420p[v]"
 run(['-loop','1','-i',str(a.out/(plate_id+'_before.png')),'-loop','1','-i',str(a.out/(plate_id+'_after.png')),'-i',str(patch),'-filter_complex',graph,'-map','[v]','-frames:v',str(n),*enc,str(dissolved)])
 row.update(previous_source=row['source'],source=src.name,kind='still',framing={'box':[0,.25,1,.8125],'pct':.012},upscale=1,overlays=[],credit=credit,sleep_repair=str(patch),sleep_repair_fades_s=.5)
 patches.append(dict(plate_id=plate_id,frames=[lo,hi],patch=str(patch),dissolved=str(dissolved),dissolved_sha256=sha(dissolved)))
out=a.out/'029_picture_alma_betelgeuse.mp4';inputs=['-i',str(base)];filters=[];prev='0:v'
for i,p in enumerate(patches,1):
 inputs+=['-i',p['dissolved']];lo,hi=p['frames'];filters.append(f"[{i}:v]setpts=PTS-STARTPTS+{lo}/30/TB[p{i}];[{prev}][p{i}]overlay=eof_action=pass:enable='between(t,{lo/30},{(hi-.5)/30})'[v{i}]");prev=f'v{i}'
run([*inputs,'-filter_complex',';'.join(filters),'-map',f'[{prev}]','-frames:v','14829',*enc,str(out)])
run(['-i',str(out),'-f','null','-'])
(a.out/'cuts.json').write_text(json.dumps(cs,indent=2)+'\n')
r=dict(status='BOUNDED_REPAIR_NOT_FINAL_QA_OR_UAT',base=str(base),base_sha256=sha(base),source=str(src),source_sha256=sha(src),provenance=asset,output=str(out),sha256=sha(out),frames=14829,duration_s=494.3,patches=patches,limitations=['Real submillimetre observation, not visible-light colour or a 2019 dimming comparison.','Narration and source masters untouched.','Two appearances of this observation; remaining picture QA failures stay authoritative.'])
(a.out/'REPORT.json').write_text(json.dumps(r,indent=2)+'\n');print(out)
