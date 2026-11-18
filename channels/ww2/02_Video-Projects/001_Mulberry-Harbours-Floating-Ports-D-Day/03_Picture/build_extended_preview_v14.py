"""Extend the continuous narration draft through the construction section."""
import hashlib,json,subprocess
from pathlib import Path
S=Path('/Volumes/MiniWork/scratch');O=S/'J2993-chapter-v14';O.mkdir(exist_ok=True)
V=Path('/Volumes/data/studio-live/ww2/02_Video-Projects/001_Mulberry-Harbours-Floating-Ports-D-Day/02_Voiceover/mulberry_harbours_vo_v01.wav')
inputs=[S/'J2993-chapter-v13/chapter_88s_to_630s_silent_v13.mp4',S/'J2993-construction-v14/construction_silent_v14.mp4']
expected=[13544,3061]
for f,n in zip(inputs,expected):
 s=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=nb_frames,width,height,r_frame_rate','-of','json',str(f)]))['streams'][0]
 assert int(s['nb_frames'])==n and (s['width'],s['height'],s['r_frame_rate'])==(1920,1080,'25/1')
listing=O/'concat.txt';listing.write_text(''.join("file '"+str(f)+"'\n" for f in inputs));silent=O/'chapter_88s_to_752s_silent_v14.mp4';preview=O/'chapter_88s_to_752s_narration_v14.mp4'
subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(silent)],check=True)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(silent),'-ss','88.08','-i',str(V),'-map','0:v','-map','1:a','-t','664.2','-c:v','copy','-c:a','aac','-b:a','192k',str(preview)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(preview),'-f','null','-'],check=True)
streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(preview)]))['streams']
assert int(next(s for s in streams if s['codec_type']=='video')['nb_frames'])==16605
for s in streams:assert abs(float(s['duration'])-664.2)<.021
(O/'chapter_preview_manifest_v14.json').write_text(json.dumps(dict(start_s=88.08,end_s=752.28,frames=16605,duration_s=664.2,inputs=[dict(file=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in inputs],vo_sha256=hashlib.sha256(V.read_bytes()).hexdigest(),preview_sha256=hashlib.sha256(preview.read_bytes()).hexdigest(),review='Technical and still evidence only; no audio/motion verdict; no score; DRAFT_NOT_QUALITY_APPROVED'),indent=2)+'\n')
