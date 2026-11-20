#!/usr/bin/env python3
"""Time-bounded opaque label backplates; preserve original geometry and mix."""
import argparse,json,pathlib,subprocess,traceback
from PIL import Image,ImageDraw
import detection_maps as dm
import early_maps as early
import geography_maps as geo
from score_candidate import sha

def main():
 p=argparse.ArgumentParser();p.add_argument('--media',type=pathlib.Path,required=True);p.add_argument('--done',type=pathlib.Path,required=True);p.add_argument('--prepare-only',action='store_true');a=p.parse_args();code=1
 try:
  edit=pathlib.Path(__file__).resolve().parent;root=a.media
  src=root/'07_Edit/score_mix_candidate_v03/atlantic_score_mix_CANDIDATE_v03.mp4'
  evidence=json.loads((edit/'SCORE_MIX_v03.json').read_text())
  if sha(src)!=evidence['sha256']:raise ValueError('Mix hash mismatch')
  out=root/'07_Edit/label_polish_candidate_v04';out.mkdir(exist_ok=True)
  dst=out/'atlantic_label_polish_CANDIDATE_v04.mp4'
  if dst.exists():raise FileExistsError('Preserve existing render')
  rows=json.loads((edit/'EDL_v02.json').read_text())['rows'];groups=[[],[]]
  for r in rows:
   line=r['line_id'];idx=int(r['shot_id'].split('.')[1])-1
   if line in early.S and early.S[line][idx][0]=='combined':groups[0].append(r)
   if line in geo.S and geo.S[line][idx][0] in ('carrier','both'):groups[1].append(r)
  labels=[('Carrier base',450,545),('Moving carrier base',410,560)]
  filters=[];inputs=[];record=[]
  for i,((text,x,y),group) in enumerate(zip(labels,groups)):
   font=dm.font(28);box=font.getbbox(text);w=box[2]+24;h=48
   im=Image.new('RGB',(w,h),dm.PAPER);d=ImageDraw.Draw(im);d.rectangle((0,0,w-1,h-1),outline=dm.INK,width=2);d.text((12,4),text,font=font,fill=dm.INK)
   png=out/f'label_{i}.png';im.save(png);inputs+=['-i',str(png)]
   # Half-open frame intervals match the conformed final edit at 25 fps.
   spans=[(round(r['cut_start_s']*25),round(r['cut_end_s']*25)-1) for r in group]
   enable='+'.join(f'between(n,{lo},{hi})' for lo,hi in spans)
   prev='0:v' if i==0 else f'v{i-1}'
   filters.append(f"[{prev}][{i+1}:v]overlay=x={x}:y={y}:enable='{enable}'[v{i}]")
   record.append({'label':text,'x':x,'y':y,'width':w,'height':h,'shots':[r['shot_id'] for r in group],'frame_intervals_inclusive':spans})
  (out/'LABEL_PLAN.json').write_text(json.dumps(record,indent=2)+'\n')
  filt=';'.join(filters);(out/'filter.txt').write_text(filt)
  if a.prepare_only:return 0
  subprocess.run(['ffmpeg','-v','error','-n','-i',str(src),*inputs,'-filter_complex',filt,'-map','[v1]','-map','0:a:0','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dst)],check=True)
  subprocess.run(['ffmpeg','-v','error','-i',str(dst),'-f','null','-'],check=True)
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(dst)]));v=next(s for s in probe['streams'] if s['codec_type']=='video')
  if (v['width'],v['height'],int(v['nb_read_frames']),v['avg_frame_rate'])!=(1920,1080,36076,'25/1'):raise ValueError('Frame format changed')
  def audio_hash(path):return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
  ah=audio_hash(src)
  if audio_hash(dst)!=ah:raise ValueError('Audio packets changed')
  report={'video':str(dst),'sha256':sha(dst),'source_sha256':evidence['sha256'],'frames':36076,'duration_s':float(probe['format']['duration']),'fps':25,'decode':'success','audio_packets_unchanged':True,'audio_packet_hash':ah,'label_changes':record,'approval':False,'audio_perception':False,'moving_video_perception':False,'pending':'Full capable watch/listen; remaining map/pacing assessment and voice review reconciliation'}
  (out/'TECHNICAL_CHECK.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True);code=0
 except Exception:traceback.print_exc()
 finally:
  if not a.prepare_only:a.done.write_text(str(code)+'\n')
 return code
if __name__=='__main__':raise SystemExit(main())
