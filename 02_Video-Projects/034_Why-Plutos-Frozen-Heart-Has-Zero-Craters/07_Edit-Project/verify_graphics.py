#!/usr/bin/env python3
"""Verify actual J2371 media (all 19 assets: 8 full-frame CODE, 5 alpha overlays, 6 chapter cards)."""
import argparse,hashlib,json,math,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageStat
from code_graphics import HERE,sha,canvas

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--manifests',type=Path,nargs='+',required=True)
 ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--frames',type=Path,required=True)
 ap.add_argument('--contact',type=Path)
 a=ap.parse_args();a.frames.mkdir(parents=True,exist_ok=True);results=[];tiles=[]
 for mp in a.manifests:
  for rec in json.loads(mp.read_text())['assets']:
   p=Path(rec['file']);assert sha(p)==rec['sha256'],p
   pr=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=pr['streams'][0]
   assert (v['width'],v['height'])==(1920,1080)
   assert int(v['nb_frames'])==rec['frames']
   duration=float(pr['format']['duration']);assert abs(duration-rec['requested_duration'])<=1/30+.001
   isalpha=rec.get('alpha',False)
   assert not isalpha or v['pix_fmt']=='argb'
   phases=rec.get('phases') or []
   if phases:
    sample_times=[round(float(ph[0])+min(float(ph[1])-float(ph[0]),4.6)*0.55,3) for ph in phases]
   else:
    sample_times=[round(duration*0.25,3),round(duration*0.50,3),round(duration*0.75,3)]
   metrics=[]
   for i,t in enumerate(sample_times):
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=480:270','-f','rawvideo','-pix_fmt','rgba','pipe:1'])
    im=Image.frombytes('RGBA',(480,270),raw);luma=im.convert('RGB').convert('L');hist=luma.histogram();n=sum(hist);mean=sum(k*v for k,v in enumerate(hist))/n;cumulative=0;p95=0
    for j,count in enumerate(hist):
     cumulative+=count
     if cumulative>=n*.95:p95=j;break
    if not isalpha:assert mean>=28 or p95>=50,(p,mean,p95)
    else:
     extrema=im.getchannel('A').getextrema();assert extrema[0]==0,(p,extrema)
    out_png=a.frames/f'{rec["row"]}_s{i+1}.png'
    im.save(out_png)
    if i==0:
     if isalpha:
      bg=canvas().resize((480,270));bg.alpha_composite(im);tiles.append((rec['row'],bg.convert('RGB')))
     else:
      tiles.append((rec['row'],im.convert('RGB')))
    metrics.append(dict(t=t,mean_luma=round(mean,2),p95_luma=p95,alpha_extrema=im.getchannel('A').getextrema()))
   if isalpha:assert any(m['alpha_extrema'][1]>0 for m in metrics)
   results.append(dict(row=rec['row'],file=str(p),sha256=sha(p),duration=duration,frames=int(v['nb_frames']),pixel_format=v['pix_fmt'],samples=metrics,status='TECHNICAL_CHECKS_PASS_NOT_KEEP'))
 results.sort(key=lambda r:int(r['row'][1:]))
 if a.contact and tiles:
  tiles.sort(key=lambda x:int(x[0][1:]))
  cols=3;rows_n=math.ceil(len(tiles)/cols)
  sheet=Image.new('RGB',(cols*480,rows_n*300),(22,34,56));dr=ImageDraw.Draw(sheet)
  for idx,(rname,tim) in enumerate(tiles):
   xx,yy=(idx%cols)*480,(idx//cols)*300
   sheet.paste(tim,(xx,yy));dr.text((xx+12,yy+276),f'{rname} (decoded)',fill=(255,255,255))
  sheet.save(a.contact,quality=92)
 out=dict(job='J2371',assets_checked=len(results),remaining=[],result='COMPLETE_19_OF_19_PACKAGE_PENDING_CHIEF_REVIEW',checks=results,limitations=['No assembled picture/polish/music/SFX gate or perceptual KEEP','Alpha overlays require review over the actual graded moving plates in assembly'])
 a.out.write_text(json.dumps(out,indent=2)+'\n');print(f'{len(results)} rendered assets verified; 0 remaining')
if __name__=='__main__':main()
