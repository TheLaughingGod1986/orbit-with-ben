#!/usr/bin/env python3
"""Remove production IDs below the content area; retain v01 and all warnings."""
import argparse,hashlib,json,pathlib,subprocess,traceback

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--media',type=pathlib.Path,required=True);p.add_argument('--done',type=pathlib.Path,required=True);a=p.parse_args();code=1
 try:
  edit=pathlib.Path(__file__).resolve().parent;m=json.loads((edit/'FULL_DRAFT_v01.json').read_text());src=pathlib.Path(m['video'])
  if sha(src)!=m['sha256']:raise ValueError('Source draft hash mismatch')
  out=a.media/'07_Edit/picture_polish_v02';out.mkdir(parents=True,exist_ok=True)
  dst=out/'atlantic_picture_polish_DRAFT_v02.mp4'
  if dst.exists():raise FileExistsError('Refusing to overwrite existing render')
  # All post-opening renderer footers use PAPER (230,227,211). Content and
  # archive rights captions end above y=990. Opening has a different design.
  vf="drawbox=x=0:y=990:w=iw:h=90:color=0xe6e3d3:t=fill:enable='gte(t,21.6)'"
  subprocess.run(['ffmpeg','-v','error','-n','-i',str(src),'-map','0:v:0','-map','0:a:0','-vf',vf,'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dst)],check=True)
  subprocess.run(['ffmpeg','-v','error','-i',str(dst),'-f','null','-'],check=True)
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(dst)]));v=next(s for s in probe['streams'] if s['codec_type']=='video')
  if (v['width'],v['height'],int(v['nb_read_frames']),v['avg_frame_rate'])!=(1920,1080,m['frames'],'25/1'):raise ValueError('Unexpected picture format')
  # Encoded AAC packets must be unchanged: no remix, normalization or new VO.
  def audio_hash(path):return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
  ah=audio_hash(src)
  if audio_hash(dst)!=ah:raise ValueError('Audio packets changed')
  result={'state':'picture_polish_draft_no_music_no_perceptual_QA','video':str(dst),'sha256':sha(dst),'source_sha256':m['sha256'],'frames':m['frames'],'fps':25,'duration_s':m['duration_s'],'decode':'success','audio_packet_hash':ah,'audio_packet_copy_verified':True,'change':'Clear production footer below y=990 after 21.60s; preserve opening, schematic warnings at y=948 and archive rights at y=968. Credits remain in description.','audio_perception':False,'moving_video_perception':False,'music':'absent'}
  (out/'TECHNICAL_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);code=0
 except Exception:traceback.print_exc()
 finally:a.done.parent.mkdir(parents=True,exist_ok=True);a.done.write_text(str(code)+'\n')
 return code
if __name__=='__main__':raise SystemExit(main())
