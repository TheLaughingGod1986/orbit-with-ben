#!/usr/bin/env python3
"""R14 source-linked solar-surface candidate. No KEEP or composite approval."""
import argparse, hashlib, io, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageStat
HERE=Path(__file__).resolve().parent
EXPECTED='242b625e1082b23b52a2fb4b1b6aca7655772fdef85c75bae73e2225f24b8a48'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--source',type=Path,required=True)
 ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--report',type=Path,required=True)
 a=ap.parse_args()
 if a.report.exists():raise FileExistsError(a.report)
 if sha(a.source)!=EXPECTED:raise ValueError('Original source hash mismatch')
 a.out.mkdir(parents=True,exist_ok=False)
 # R14 solar comparison starts at the locked word "about". 60 frames fit
 # inside 138.70..141.12, leaving 0.02 s inside the row for the compositor.
 dest=a.out/'031_r14_sdo_surface_candidate_v03.mp4'
 vf='crop=960:540:520:350,scale=1920:1080:flags=lanczos,eq=gamma=1.15:saturation=1.05,fps=25'
 cmd=['ffmpeg','-v','error','-xerror','-n','-ss','2','-i',str(a.source),'-t','2.40','-vf',vf,'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(dest)]
 subprocess.run(cmd,check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]))
 v,=probe['streams']
 assert v['codec_type']=='video' and (v['width'],v['height'])==(1920,1080)
 assert v['avg_frame_rate']=='25/1' and abs(float(v['duration'])-2.40)<.02
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(dest),'-f','null','-'],check=True)
 sheet=Image.new('RGB',(1920,780),(30,45,65));d=ImageDraw.Draw(sheet);samples=[]
 for n,t in enumerate([0,.6,1.2,1.8,2.36]):
  raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(dest),'-frames:v','1','-f','image2pipe','-c:v','png','-'])
  im=Image.open(io.BytesIO(raw)).convert('RGB');p=a.out/f'sample_{n}.png';im.save(p)
  y=im.convert('YCbCr').getchannel('Y');hist=y.histogram()
  samples.append(dict(time_s=t,path=str(p),sha256=sha(p),mean_luma=round(ImageStat.Stat(y).mean[0],2),near_black_fraction=round(sum(hist[:20])/(1920*1080),4)))
  im.thumbnail((620,349));x=(n%3)*640;yy=(n//3)*390;sheet.paste(im,(x,yy));d.text((x+12,yy+355),f'R14 candidate +{t:.2f}s',fill='white')
 contact=a.out/'CONTACT_R14_v03.jpg';sheet.save(contact,quality=93)
 assert len({s['sha256'] for s in samples})==len(samples)
 record=dict(job='J2141',row=14,spend_gbp=0,status='candidate_pending_composite_review',source_asset_id='SVS4323_SDO_AIA304_motion',source_page='https://svs.gsfc.nasa.gov/4323/',source_path=str(a.source),source_sha256=EXPECTED,source_rows=[6],source_interval_s=[2,4.4],film_start_s=138.7,film_duration_s=2.4,locked_row_end_s=141.12,remaining_row_s=.02,crop_xywh=[520,350,960,540],upscale=2,filter=vf,path=str(dest),sha256=sha(dest),bytes=dest.stat().st_size,credit='NASA/SDO',disclosure='SDO AIA 304 angstrom; false-colour time-lapse observations',full_decode='PASS',probe=probe,samples=samples,contact_sheet=str(contact),contact_sheet_sha256=sha(contact),limitations='No composite or playback review. Existing R14 FACT card overlaps solar surface at its default lower-left position; editor must establish subject clearance before use. Corner NASA/SDO credit and all film gates still required. This is a short comparison insert, not the full row.')
 a.report.write_text(json.dumps(record,indent=2)+'\n')
 print(dest)
if __name__=='__main__':main()
