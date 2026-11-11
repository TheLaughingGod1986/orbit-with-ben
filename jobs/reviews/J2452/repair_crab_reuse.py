#!/usr/bin/env python3
"""Replace the third Crab appearance with a different official observation.

Preserves the silent chapter frame clock; no source-master or narration edits.
"""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from build_orion_source_repair import sha,run

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--photo',type=Path,required=True);a=p.parse_args()
 base=Path('/Users/ben/_desk/J2452-sleep-scratch/late_observatory_v04/029_picture_observatory_repaired_framefixed.mp4')
 assert sha(base)=='4037046cbea93cbc2ad02b468016b5ec90def570122de11fad850e6a13e19760'
 cuts=json.loads((base.parent/'cuts.json').read_text());row=next(c for c in cuts if c['plate_id']=='r35_crab')
 # Source pixels change slightly before the rounded cut-list boundary.
 # Cover three additional frames of the preceding graphic; keep the audio clock.
 previous=cuts[cuts.index(row)-1]
 row['previous_timeline_in']=row['timeline_in'];row['timeline_in']=421.4
 previous['previous_timeline_out']=previous['timeline_out'];previous['timeline_out']=421.4
 row['previous_master_range_s']=list(row['master_range_s']);row['master_range_s'][0]=441.9
 previous['master_range_s'][1]=441.9
 lo,hi=round(row['timeline_in']*30),round(row['timeline_out']*30);n=hi-lo
 assert (lo,hi,n)==(12642,12975,333)
 a.out.mkdir(parents=True,exist_ok=False)
 photo=Image.open(a.photo);assert photo.size==(10509,9151)
 credit='NASA, ESA, CSA, STScI, T. Temim (Princeton University)'
 overlay=Image.new('RGBA',(1920,1080));draw=ImageDraw.Draw(overlay);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',27)
 draw.text((45,990),'Webb infrared observation',font=font,fill=(234,230,223,166))
 draw.text((45,1025),credit,font=font,fill=(234,230,223,166));overlay.save(a.out/'credit.png')
 prepared=a.out/'source_crop.png'
 run(['-i',str(a.photo),'-frames:v','1','-vf','scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160',str(prepared)])
 enc=['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','6','-r','30','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000']
 patch=a.out/'crab.mp4'
 graph=f"[0:v]zoompan=z='1.01+0.02*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,colorchannelmixer=rr=.85:gg=.85:bb=.85,limiter=min=16:max=180:planes=1[plate];[plate][1:v]overlay=0:0,format=yuv420p[v]"
 run(['-loop','1','-i',str(prepared),'-loop','1','-i',str(a.out/'credit.png'),'-filter_complex',graph,'-map','[v]','-frames:v',str(n),*enc,str(patch)])
 before=a.out/'before.png';after=a.out/'after.png'
 run(['-i',str(base),'-vf',f'select=eq(n\\,{lo-1})','-frames:v','1',str(before)])
 run(['-ss',str(hi/30),'-i',str(base),'-frames:v','1',str(after)])
 dissolved=a.out/'crab_dissolved.mp4'
 graph=f"[0:v][1:v]overlay=enable='gte(t,{n/60})'[bg];[2:v]format=yuva420p,fade=t=in:st=0:d=2:alpha=1,fade=t=out:st={n/30-2}:d=2:alpha=1[p];[bg][p]overlay,format=yuv420p[v]"
 run(['-loop','1','-i',str(before),'-loop','1','-i',str(after),'-i',str(patch),'-filter_complex',graph,'-map','[v]','-frames:v',str(n),*enc,str(dissolved)])
 output=a.out/'029_picture_crab_repaired.mp4'
 graph=f"[1:v]setpts=PTS-STARTPTS+{lo}/30/TB[p];[0:v][p]overlay=eof_action=pass:enable='between(t,{lo/30},{(hi-.5)/30})',format=yuv420p[v]"
 run(['-i',str(base),'-i',str(dissolved),'-filter_complex',graph,'-map','[v]','-frames:v','14829',*enc,str(output)])
 run(['-i',str(output),'-f','null','-'])
 row['previous_source']=row['source'];row.update(source=a.photo.name,kind='still',framing={'box':[0,0,1,1],'pct':.02},upscale=1920/3840,credit=credit,overlays=[],sleep_repair=str(patch),sleep_repair_fades_s=2)
 provenance=dict(id='weic2326a',title='The Crab Nebula',page='https://esawebb.org/images/weic2326a/',download='https://cdn.esawebb.org/archives/images/large/weic2326a.jpg',terms='https://esawebb.org/copyright/',licence='CC BY 4.0',credit=credit,dimensions=list(photo.size),checked='2026-11-11',modifications='16:9 crop, slow push, 15 percent sleep darkening, luma cap; full credit and infrared identification visible')
 (a.out/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
 (a.out/'pool.json').write_text(json.dumps([dict(source=a.photo.name,**provenance)],indent=2)+'\n')
 report=dict(status='BOUNDED_CRAB_REPAIR_NOT_FINAL_QA_OR_UAT',base=str(base),base_sha256=sha(base),source=str(a.photo),source_sha256=sha(a.photo),provenance=provenance,patch=str(patch),patch_sha256=sha(patch),dissolved=str(dissolved),dissolved_sha256=sha(dissolved),output=str(output),sha256=sha(output),frames=14829,duration_s=494.3,chapter_replace_frames=[lo,hi],master_range_s=row['master_range_s'],limitations=['Different real Crab observation, not a renamed or recropped copy of Hubble crab.jpg.','No claim that this still demonstrates expansion over time.','Two-second endpoint dissolves use neighbouring frames; their original graphics and labels remain for later repair.','Normal combined QA, full compilation and final gates remain.'])
 (a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(output)
if __name__=='__main__':main()
