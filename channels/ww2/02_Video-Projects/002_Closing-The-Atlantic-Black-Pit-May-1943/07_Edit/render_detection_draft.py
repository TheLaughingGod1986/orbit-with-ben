#!/usr/bin/env python3
"""Detached-friendly draft batch. Writes .done even on failure."""
import argparse,hashlib,json,pathlib,subprocess,sys,traceback

def run(cmd):subprocess.run([str(x) for x in cmd],check=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('--media',type=pathlib.Path,required=True);p.add_argument('--done',type=pathlib.Path,required=True);p.add_argument('--renderer',default='detection_maps.py',choices=['detection_maps.py','convoy_maps.py','ending_maps.py','geography_maps.py','aircraft_maps.py','early_maps.py','synthesis_maps.py','carrier_maps.py']);p.add_argument('--batch',default='detection_v01',choices=['detection_v01','convoys_v01','ending_v01','geography_v01','aircraft_v01','early_v01','synthesis_v01','carrier_v01']);a=p.parse_args();code=1
 try:
  edit=pathlib.Path(__file__).resolve().parent;out=a.media/'03_Picture/maps'/a.batch;out.mkdir(parents=True,exist_ok=True)
  run([sys.executable,edit/a.renderer,'--out',out,'--video'])
  manifest=json.loads((out/'MANIFEST.json').read_text());rows=manifest['rows'];fps=manifest['fps'];audio=a.media/'02_Voiceover/atlantic_black_pit_vo_v01.wav'
  if hashlib.sha256(audio.read_bytes()).hexdigest()!=manifest['audio_sha256']:raise ValueError('VO hash mismatch')
  for prev,cur in zip(rows,rows[1:]):
   if prev['cut_end_s']!=cur['cut_start_s']:raise ValueError('Noncontiguous edit')
  start=round(rows[0]['cut_start_s']*fps)/fps;frames=sum(r['frames'] for r in rows);duration=frames/fps
  concat=out/'concat.txt';concat.write_text(''.join("file '"+pathlib.Path(r['video']).name+"'\n" for r in rows))
  video=out/(a.batch+'_with_vo_DRAFT_v01.mp4')
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',concat,'-ss',start,'-i',audio,'-t',duration,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',video])
  run(['ffmpeg','-v','error','-i',video,'-f','null','-'])
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]));v=next(x for x in probe['streams'] if x['codec_type']=='video')
  if (v['width'],v['height'],int(v['nb_read_frames']))!=(1920,1080,frames):raise ValueError('Wrong dimensions or frame count')
  (out/'TECHNICAL_CHECK.json').write_text(json.dumps({'state':'draft_decode_checked_not_watch_review','sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'video':str(video),'source_audio_sha256':manifest['audio_sha256'],'source_start_s_quantized':start,'source_end_s_quantized':start+duration,'duration_s':duration,'frames':frames,'fps':fps,'width':v['width'],'height':v['height'],'decode':'success','music':'absent; draft VO only','motion_perception':False,'audio_perception':False},indent=2)+'\n')
  print('COMPLETE',video,flush=True);code=0
 except Exception:traceback.print_exc()
 finally:a.done.parent.mkdir(parents=True,exist_ok=True);a.done.write_text(str(code)+'\n')
 return code
if __name__=='__main__':raise SystemExit(main())
