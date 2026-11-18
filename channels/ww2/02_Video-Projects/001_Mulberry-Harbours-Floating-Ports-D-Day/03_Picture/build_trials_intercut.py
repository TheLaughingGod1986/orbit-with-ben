"""Add three licensed, subject-matched archival intercuts to the trial section.
Preserve complete originals: never crop the Quebec leaders' heads out of frame.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
P=Path(__file__).parent
CHOICES={'lochner':('A_25826_25084662.jpg','Robert Lochner | Short Lake House'),
'bombardon':('A_25814_25084644.jpg','Bombardon experiments | Weymouth Bay, April 1944'),
'approval':('H_32129_30910182.jpg','Quebec Conference | August 1943')}
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--trials',type=Path,required=True);a.add_argument('--originals',type=Path,required=True);a.add_argument('--vo',type=Path,required=True);args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 m=json.loads((args.trials/'trials_sequence_manifest_v11.json').read_text());records={r['file']:r for r in json.loads((P/'archive_cleared_v07.json').read_text())['records']};archive=[];listing=[]
 for r in m['scenes']:
  if r['scene'] in CHOICES:
   name,caption=CHOICES[r['scene']];source=args.originals/name;rec=records[name]
   assert hashlib.sha256(source.read_bytes()).hexdigest()==rec['sha256']
   im=ImageOps.exif_transpose(Image.open(source)).convert('RGB');scale=min(1.4,1720/im.width,850/im.height);assert scale*1.02<=2.35
   plate=Image.new('RGB',(1920,1080),'#e2dfd6');size=(round(im.width*scale),round(im.height*scale));plate.paste(im.resize(size,Image.Resampling.LANCZOS),((1920-size[0])//2,(980-size[1])//2));f=args.out/(source.stem+'_full_plate.png');plate.save(f)
   label=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(label);font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',25)
   for y,t in [(958,caption),(1010,'IWM '+rec['fields_verbatim']['catalogue_number']+' | Crown copyright expired | via Wikimedia Commons')]:
    d.rectangle((30,y-5,1890,y+38),fill=(25,25,25,200));d.text((45,y),t,font=font,fill='white')
   credit=args.out/(source.stem+'_credit.png');label.save(credit);clip=args.out/(r['scene']+'_archive_v13.mp4')
   subprocess.run(['ffmpeg','-v','error','-n','-loop','1','-i',str(f),'-i',str(credit),'-filter_complex',f"[0:v]zoompan=z='1+0.02*on/{r['frames']-1}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=25[v];[v][1:v]overlay=0:0,format=yuv420p[o]",'-map','[o]','-frames:v',str(r['frames']),'-an','-c:v','libx264','-preset','veryfast','-crf','20','-threads','2',str(clip)],check=True)
   archive.append(dict(scene=r['scene'],source_file=name,source_sha256=rec['sha256'],catalogue=rec['fields_verbatim']['catalogue_number'],url=rec['url'],caption=caption,maximum_upscale=scale*1.02,frames=r['frames'],file=clip.name,sha256=hashlib.sha256(clip.read_bytes()).hexdigest()))
  else:clip=args.trials/r['file']
  listing.append("file '"+str(clip)+"'\n")
 (args.out/'concat.txt').write_text(''.join(listing));silent=args.out/'trials_intercut_silent_v13.mp4'
 subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(args.out/'concat.txt'),'-c','copy',str(silent)],check=True)
 preview=args.out/'trials_intercut_narration_v13.mp4'
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(silent),'-ss',str(m['start_s']),'-i',str(args.vo),'-map','0:v','-map','1:a','-t',str(m['end_s']-m['start_s']),'-c:v','copy','-c:a','aac','-b:a','192k',str(preview)],check=True)
 subprocess.run(['ffmpeg','-v','error','-i',str(preview),'-f','null','-'],check=True)
 (args.out/'archive_intercuts_v13.json').write_text(json.dumps(dict(start_s=m['start_s'],end_s=m['end_s'],intercuts=archive,note='Three prior-cleared sources; source subjects and all source edges retained. Still/technical checks only. No film approval.',preview_sha256=hashlib.sha256(preview.read_bytes()).hexdigest()),indent=2)+'\n')
if __name__=='__main__':main()
