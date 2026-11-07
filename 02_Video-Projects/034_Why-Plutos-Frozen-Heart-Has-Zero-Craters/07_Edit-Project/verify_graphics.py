#!/usr/bin/env python3
"""Verify actual J2371 media, not just the theoretical background canvas."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageStat
from code_graphics import HERE,sha

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--manifests',type=Path,nargs='+',required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--frames',type=Path,required=True);a=ap.parse_args();a.frames.mkdir(parents=True,exist_ok=True);results=[]
 for mp in a.manifests:
  for rec in json.loads(mp.read_text())['assets']:
   p=Path(rec['file']);assert sha(p)==rec['sha256'],p
   pr=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=pr['streams'][0]
   assert (v['width'],v['height'])==(1920,1080)
   assert int(v['nb_frames'])==rec['frames']
   duration=float(pr['format']['duration']);assert abs(duration-rec['requested_duration'])<=1/30+.001
   isalpha=rec.get('alpha',False)
   assert not isalpha or v['pix_fmt']=='argb'
   metrics=[]
   for i,t in enumerate([.1,duration/2,duration-.1]):
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=480:270','-f','rawvideo','-pix_fmt','rgba','pipe:1'])
    im=Image.frombytes('RGBA',(480,270),raw);luma=im.convert('RGB').convert('L');hist=luma.histogram();n=sum(hist);mean=sum(i*v for i,v in enumerate(hist))/n;cumulative=0;p95=0
    for j,count in enumerate(hist):
     cumulative+=count
     if cumulative>=n*.95:p95=j;break
    if not isalpha:assert mean>=28 or p95>=50,(p,mean,p95)
    else:
     extrema=im.getchannel('A').getextrema();assert extrema[0]==0,(p,extrema)
    im.save(a.frames/f'{rec["row"]}_{i}.png');metrics.append(dict(t=round(t,4),mean_luma=round(mean,2),p95_luma=p95,alpha_extrema=im.getchannel('A').getextrema()))
   if isalpha:assert any(m['alpha_extrema'][1]>0 for m in metrics)
   results.append(dict(row=rec['row'],file=str(p),sha256=sha(p),duration=duration,frames=int(v['nb_frames']),pixel_format=v['pix_fmt'],samples=metrics,status='TECHNICAL_CHECKS_PASS_NOT_KEEP'))
 out=dict(job='J2371',assets_checked=len(results),remaining=['R15','R48'],result='PARTIAL_PACKAGE',checks=results,limitations=['No assembled picture/polish/music/SFX gate or perceptual KEEP','Alpha overlays require review over the actual graded moving plates','Rendering of R15 and R48 is not implemented','Technical checks do not prove scientific geometry or VO synchronisation'])
 a.out.write_text(json.dumps(out,indent=2)+'\n');print(f'{len(results)} rendered assets verified; R15/R48 remain')
if __name__=='__main__':main()
