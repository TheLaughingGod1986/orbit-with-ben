#!/usr/bin/env python3
"""Replace only the final sky shot with a distinct native source interval."""
import argparse,json,subprocess
from pathlib import Path
from build_orion_source_repair import sha,run

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 root=Path(__file__).resolve().parent
 base=Path('/Users/ben/_desk/J2452-sleep-scratch/observation_grade_v02/029_picture_observation_grade.mp4')
 assert sha(base)=='8496226aca2f3f37b62fd2ae0b09f648fc3f0d972ae43212a8fa43c1f1abe979'
 source=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/lasilla_mw.mp4')
 cuts=json.loads((base.parent/'cuts.json').read_text());last=cuts[-1]
 assert last['plate_id']=='r39_return' and last['source']==source.name
 lo=round(last['timeline_in']*30);hi=14829;frames=hi-lo
 # Previous appearance uses [0,5.23]; this uses [10.2,15.7333]. No loops or speed changes.
 assert 10.2+frames/30<17.6
 a.out.mkdir(parents=True,exist_ok=False)
 from PIL import Image,ImageDraw,ImageFont
 credit=Image.new('RGBA',(1920,1080));ImageDraw.Draw(credit).text((45,1025),'ESO/S. Brunier',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',27),fill=(234,230,223,140));credit.save(a.out/'credit.png')
 enc=['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','6','-r','30','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-video_track_timescale','90000']
 replacement=a.out/'closing_sky.mp4'
 graph='[0:v]setpts=PTS-STARTPTS,fps=30,setsar=1,colorchannelmixer=rr=.85:gg=.85:bb=.85,limiter=min=16:max=180:planes=1[plate];[plate][1:v]overlay=0:0,format=yuv420p[v]'
 run(['-ss','10.2','-i',str(source),'-loop','1','-i',str(a.out/'credit.png'),'-filter_complex',graph,'-map','[v]','-frames:v',str(frames),*enc,str(replacement)])
 # Two-second endpoint dissolve replaces equal timeline time, without moving VO.
 join=a.out/'closing_join.mp4';start=(lo-30)/30
 graph='[0:v]setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1[a];[1:v]trim=end=1,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=1[b];[a][b]xfade=transition=fade:duration=2:offset=0,format=yuv420p[v]'
 run(['-ss',str(start),'-t','1','-i',str(base),'-i',str(replacement),'-filter_complex',graph,'-map','[v]','-frames:v','60',*enc,str(join)])
 # Save a bounded join+tail for normal pixel QA before committing a full chapter encode.
 tail=a.out/'tail.mp4';run(['-ss','1','-i',str(replacement),'-frames:v',str(frames-30),*enc,str(tail)])
 listing=a.out/'concat.txt';listing.write_text(''.join("file '"+str(x)+"'\n" for x in [join,tail]))
 output=a.out/'closing_join_and_tail.mp4';run(['-f','concat','-safe','0','-i',str(listing),'-c','copy',str(output)]);run(['-i',str(output),'-f','null','-'])
 count=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(output)]))['streams'][0];assert int(count['nb_read_frames'])==frames+30
 last['previous_framing']=last['framing'];last['framing']={'offset':10.2,'speed':1};last['sleep_repair']=str(replacement)
 (a.out/'chapter_cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
 local=[dict(row='join',source='closing_join.mp4',kind='video',timeline_in=0,timeline_out=2,upscale=1,framing={'offset':0}),dict(row='39',source=source.name,kind='video',timeline_in=2,timeline_out=(frames+30)/30,upscale=1,framing={'offset':11.2})]
 (a.out/'cuts.json').write_text(json.dumps(local,indent=2)+'\n')
 report=dict(status='BOUNDED_CLOSING_REPAIR_NOT_INTEGRATED_NOT_UAT',base=str(base),base_sha256=sha(base),source=str(source),source_sha256=sha(source),source_interval_s=[10.2,10.2+frames/30],previous_interval_s=[0,5.23],replacement=str(replacement),replacement_sha256=sha(replacement),output=str(output),sha256=sha(output),frames=frames+30,chapter_range_s=[start,494.3],chapter_replace_frames=[lo-30,hi],credit='ESO/S. Brunier; inherited film pool credit; no new download',limitations=['Normal polish and full-size still inspection required.','Not integrated; chapter source QA still has other failures.','No narration, source-master or timing change.'])
 (a.out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
 for i,t in enumerate([0,.5,1,1.5,2,3.5,5,6.5]):
  if t<(frames+30)/30:run(['-ss',str(t),'-i',str(output),'-frames:v','1','-vf','scale=960:540',str(a.out/f'frame_{i}.jpg')])
 print(output)
if __name__=='__main__':main()
