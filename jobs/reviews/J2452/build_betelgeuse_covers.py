#!/usr/bin/env python3
"""Checkpoint two real-photograph Orbit covers; never mark the chapter complete."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path('/Users/ben/_desk/J2452-sleep-scratch/betelgeuse_covers_v03')
MASTER=Path('/Volumes/data/mac-mini-archive/youtube-staging/029/029_Betelgeuse_full_rough_v03b.mp4')
PHOTO=Path('/Users/ben/_desk/J2452-sleep-scratch/betelgeuse_covers_v01/eso0927e.tif')
CREDIT='ESO/Digitized Sky Survey 2. Acknowledgment: Davide De Martin.'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def ff(args):
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-n',*args],check=True)
def main():
 global OUT,PHOTO
 parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);parser.add_argument('--photo',type=Path,default=PHOTO);args=parser.parse_args();OUT=args.out;PHOTO=args.photo
 from PIL import Image,ImageDraw,ImageFont
 OUT.mkdir(exist_ok=False)
 assert digest(MASTER)=='54e04d3bfcb42bcf9066a0613254f10c978435b148d158468711e25908060c93'
 im=Image.open(PHOTO);assert im.size==(7106,5332),im.size
 cuts=json.loads((ROOT/'02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/full_rough_v03b_pack/cuts_v03b.json').read_text())
 chapter=next(c for c in json.loads((ROOT/'jobs/reviews/J2452/picture_timeline_v01.json').read_text())['chapters'] if c['film']=='029')
 rows=[c for c in cuts if c['kind']=='omni'];assert len(rows)==2
 samples=[];covers=[];clock=0
 for n,c in enumerate(rows,1):
  a,b=c['timeline_in'],c['timeline_out'];sl=next(s for s in chapter['slices'] if s['master_in_s']<=a and b<=s['master_out_s'])
  ca=sl['chapter_in_s']+a-sl['master_in_s'];cb=sl['chapter_in_s']+b-sl['master_in_s']
  # Cumulative absolute chapter-frame rounding avoids arbitrary duration drift.
  frames=round(cb*30)-round(ca*30);duration=frames/30
  dest=OUT/f'cover_{n:02d}.mp4'
  credit=OUT/'credit.txt'
  if not credit.exists():credit.write_text(CREDIT+' (crop, grade, motion)')
  creditpng=OUT/'credit_overlay.png'
  if not creditpng.exists():
   overlay=Image.new('RGBA',(1920,1080));cd=ImageDraw.Draw(overlay)
   cd.text((45,1025),credit.read_text(),font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',27),fill=(234,230,223,166))
   overlay.save(creditpng)
  vf=("scale=4800:-2,crop=4800:2700,zoompan=z='1.01+0.02*on/"+str(frames)+"':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=3840x2160:fps=30,scale=1920:1080:flags=lanczos,"
      "colorchannelmixer=rr=0.85:gg=0.85:bb=0.85,format=yuv420p,limiter=min=16:max=180:planes=1")
  ff(['-loop','1','-i',str(PHOTO),'-loop','1','-i',str(creditpng),'-filter_complex','[0:v]'+vf+'[plate];[plate][1:v]overlay=0:0,format=yuv420p[v]','-map','[v]','-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-video_track_timescale','90000',str(dest)])
  ff(['-i',str(dest),'-f','null','-'])
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(dest)]))['streams'][0]
  assert int(probe['nb_read_frames'])==frames
  covers.append(dict(row=c['row'],original_source=c['source'],master_in_s=a,master_out_s=b,chapter_in_s=round(ca,6),chapter_out_s=round(cb,6),compilation_in_s=round(chapter['compilation_start_s']+ca,6),compilation_out_s=round(chapter['compilation_start_s']+cb,6),output=str(dest),frames=frames,duration_s=duration,sha256=digest(dest),status='COVER_ONLY_NOT_JOINED_OR_FULL_CHAPTER_QA'))
  for tag,t in [('before',a-.1),('inside',a+(b-a)/2),('after',b+.1)]:
   f=OUT/f'window_{n:02d}_{tag}.jpg';ff(['-ss',str(t),'-i',str(MASTER),'-frames:v','1','-vf','scale=640:360',str(f)])
   samples.append((f,f'{n}: master {t:.3f}s {tag}'))
  f=OUT/f'cover_{n:02d}_middle.jpg';ff(['-ss',str(duration/2),'-i',str(dest),'-frames:v','1','-vf','scale=640:360',str(f)]);samples.append((f,f'{n}: replacement midpoint'))
 sheet=Image.new('RGB',(1280,4*390),(25,25,25));draw=ImageDraw.Draw(sheet)
 for i,(f,label) in enumerate(samples):
  x=(i%2)*640;y=(i//2)*390;sheet.paste(Image.open(f),(x,y+30));draw.text((x+8,y+8),label,fill='white')
 sheetpath=OUT/'ORBIT_AND_COVERS.jpg';sheet.save(sheetpath,quality=90)
 report=dict(status='TWO_ORBIT_COVERS_BUILT_NOT_A_PICTURE_CHAPTER',master=str(MASTER),master_sha256=digest(MASTER),observation='Orbit is visible in both sampled windows; the plan zero-Orbit assertion was false.',boundary_basis='Exact original cut-list coordinates. Before/inside/after still probes are sparse visual evidence, not every-frame boundary certification.',photo=dict(id='eso0927e',title='Digitized Sky Survey image of Betelgeuse',page='https://www.eso.org/public/images/eso0927e/',download='https://cdn.eso.org/images/original/eso0927e.tif',credit=CREDIT,licence='CC BY 4.0, ESO copyright page; no identifiable people',terms='https://www.eso.org/public/outreach/copyright/',dimensions=list(im.size),sha256=digest(PHOTO),path=str(PHOTO),modifications='16:9 crop, slow push, 15 percent darkening, luma cap, visible full credit',source_upscale_max=1920/4800),covers=covers,preview=dict(path=str(sheetpath),sha256=digest(sheetpath)),remaining='Inspect stills; source/pixel QA on covers; exact endpoint joins, bright graphic replacements, full picture chapter and final compilation gates remain.')
 (ROOT/'jobs/reviews/J2452/betelgeuse_orbit_readback_v01.json').write_text(json.dumps(report,indent=2)+'\n')
 pool=[dict(source='eso0927e.tif',title='Digitized Sky Survey image of Betelgeuse',credit=CREDIT)]
 (ROOT/'jobs/reviews/J2452/betelgeuse_covers_pool_v01.json').write_text(json.dumps(pool,indent=2)+'\n')
 for n,c in enumerate(covers,1):
  cc=[dict(row=str(n),timeline_in=0,timeline_out=c['duration_s'],source='eso0927e.tif',kind='still',upscale=.8,framing={})]
  (ROOT/f'jobs/reviews/J2452/betelgeuse_cover_{n:02d}_cuts_v01.json').write_text(json.dumps(cc,indent=2)+'\n')
 print(json.dumps(dict(covers=len(covers),frames=[c['frames'] for c in covers],report='betelgeuse_orbit_readback_v01.json')))
if __name__=='__main__':main()
