"""Join verified section clocks with one continuous original-narration extract.
A section preview for editorial work, never the finished film or a quality pass.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
SECTIONS=[('J2993-dieppe-v08','dieppe_sequence_silent_v08.mp4',2202,4214),('J2993-ports-v12','ports_sequence_silent_v12.mp4',4214,5710),('J2993-beach-v09','beach_sequence_silent_v09.mp4',5710,7725),('J2993-design-v10','design_sequence_silent_v10.mp4',7725,11374),('J2993-trials-intercut-v13','trials_intercut_silent_v13.mp4',11374,15746)]
def probe(f):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_frames,duration','-of','json',str(f)]))['streams']
def main():
 p=argparse.ArgumentParser();p.add_argument('--scratch',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--vo',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);records=[]
 for folder,file,start,end in SECTIONS:
  f=a.scratch/folder/file;v=next(s for s in probe(f) if s['codec_type']=='video');assert int(v['nb_frames'])==end-start;assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'25/1')
  if records:assert records[-1]['end_frame']==start
  records.append(dict(file=str(f),start_frame=start,end_frame=end,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 listing=a.out/'concat.txt';listing.write_text(''.join("file '"+r['file']+"'\n" for r in records));silent=a.out/'chapter_88s_to_630s_silent_v13.mp4';preview=a.out/'chapter_88s_to_630s_narration_v13.mp4'
 subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(silent)],check=True)
 start,end=SECTIONS[0][2]/25,SECTIONS[-1][3]/25
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(silent),'-ss',str(start),'-i',str(a.vo),'-map','0:v','-map','1:a','-t',str(end-start),'-c:v','copy','-c:a','aac','-b:a','192k',str(preview)],check=True)
 subprocess.run(['ffmpeg','-v','error','-i',str(preview),'-f','null','-'],check=True)
 streams=probe(preview);assert int(next(s for s in streams if s['codec_type']=='video')['nb_frames'])==SECTIONS[-1][3]-SECTIONS[0][2]
 for s in streams:assert abs(float(s['duration'])-(end-start))<.021
 (a.out/'chapter_preview_manifest_v13.json').write_text(json.dumps(dict(start_s=start,end_s=end,frames=SECTIONS[-1][3]-SECTIONS[0][2],sections=records,streams=streams,preview_sha256=hashlib.sha256(preview.read_bytes()).hexdigest(),vo_sha256=hashlib.sha256(a.vo.read_bytes()).hexdigest(),status='DRAFT_NOT_QUALITY_APPROVED',review='Technical checks and stills only. No motion/audio verdict. Original VO continuous; no score.'),indent=2)+'\n')
if __name__=='__main__':main()
