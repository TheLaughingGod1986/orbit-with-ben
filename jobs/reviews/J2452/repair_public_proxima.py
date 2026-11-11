"""Repair two cover donors only, preserving the candidate and complete narration clock."""
import json,shutil
from pathlib import Path
from PIL import Image
import build_public_proxima as b
SRC=b.OUT;OUT=SRC.with_name('public_proxima_v02')
def main():
 OUT.mkdir(exist_ok=False)
 report=json.loads((SRC/'BUILD.json').read_text());rows=json.loads((SRC/'source_cuts.json').read_text());pieces=[SRC/f'piece_{i:02d}.mp4' for i in range(len(rows))]
 # The old donor was a code graphic; use the film's neighbouring clean starfield.
 p=OUT/'piece_03.mp4';dur=rows[3]['timeline_out']-rows[3]['timeline_in'];b.run(['-ss','138.2','-i',str(b.MASTER),'-vf','setpts=PTS-STARTPTS,scale=1920:1080,setsar=1,fps=30,format=yuv420p','-frames:v',str(round(dur*30)),*b.enc(),str(p)]);pieces[3]=p;rows[3]['framing']['offset']=138.2
 # heic1007a is a nebula, not a starfield: use the plan's copied Hubble starfield.
 plate=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/07_Edit-Project/pool_v01/heic0809a.jpg');assert b.sha(plate)=='10d4c8ef7b9cf7c0faf79b84ddaf74fa55aafd3bf185ffb431fea9327cbf9f5e'
 with Image.open(plate) as im:
  im=im.convert('RGB');w,h=im.size;cw=min(w,h*16/9);ch=cw*9/16;im=im.crop(((w-cw)/2,(h-ch)/2,(w+cw)/2,(h+ch)/2));im.resize((2112,1188),Image.Resampling.LANCZOS).save(OUT/'hubble.png')
 dur=rows[9]['timeline_out']-rows[9]['timeline_in'];frames=round(dur*30);p=OUT/'piece_09.mp4';b.run(['-loop','1','-framerate','30','-i',str(OUT/'hubble.png'),'-vf',f"zoompan=z='1+0.025*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,format=yuv420p",'-frames:v',str(frames),*b.enc(),str(p)]);pieces[9]=p;rows[9]['label']='plate:heic0809a.jpg'
 joined=[]
 for i,(p,row) in enumerate(zip(pieces,rows)):
  dur=row['timeline_out']-row['timeline_in'];a=1 if i else 0;z=dur-(1 if i<len(rows)-1 else 0)
  dst=SRC/f'interior_{i:02d}.mp4'
  if i in (3,9):dst=OUT/dst.name;b.run(['-ss',str(a),'-i',str(p),'-t',str(z-a),*b.enc(),str(dst)])
  joined.append(dst)
  if i==len(rows)-1:continue
  dst=SRC/f'join_{i:02d}.mp4'
  if i in (2,3,8,9):
   dst=OUT/dst.name;graph=f'[0:v]trim=start={dur-1}:end={dur},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1[a];[1:v]trim=end=1,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=1[b];[a][b]xfade=transition=fade:duration=2:offset=0,format=yuv420p[v]';b.run(['-i',str(p),'-i',str(pieces[i+1]),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-t','2',*b.enc(),str(dst)])
  joined.append(dst)
 listing=OUT/'concat.txt';listing.write_text(''.join(f"file '{p}'\n" for p in joined));final=OUT/'026_proxima_undarkened_v02.mp4'
 b.run(['-f','concat','-safe','0','-i',str(listing),'-i',str(b.NARR),'-map','0:v','-map','1:a','-af','volume=-0.5dB','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(report['duration_s']),str(final)])
 for name in ['full_pixel_cuts.json','changed_cuts.json']:shutil.copyfile(SRC/name,OUT/name)
 (OUT/'source_cuts.json').write_text(json.dumps(rows,indent=2)+'\n');report.update(output=str(final),sha256=b.sha(final),fallback='NGC 6752 eso1323a and Hubble starfield heic0809a cover the two Orbit windows. Chapter-2 donor is neighbouring clean starfield at master 138.2s; other chapter cards use neighbouring finished-master picture. Version one local candidate retained; heic1007a nebula was rejected as wrong subject. Charts and teaching labels stay.',covers=[(32.8,36.2,36.3,'chapter-1 cover'),(122,124.8,138.2,'chapter-2 cover'),(127.4,138.1,0,'plate:eso1323a.jpg'),(232,235.7,236,'chapter-3 cover'),(312.1,324,0,'plate:heic0809a.jpg'),(378.8,381.7,381.8,'chapter-5 cover')]);(OUT/'BUILD.json').write_text(json.dumps(report,indent=2)+'\n');print(final,flush=True)
if __name__=='__main__':main()
