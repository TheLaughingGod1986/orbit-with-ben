from pathlib import Path
import subprocess, numpy as np, json, hashlib
from PIL import Image,ImageDraw
out=Path('/private/tmp/j1220-evidence');out.mkdir(exist_ok=True)
root=Path('/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT')
result={}
for ver in ['v06','v07']:
 p=root/f'standalone_shorts_uranus_{ver}'/f'owb_sa_s4_uranus_{ver}.mp4'
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-t','3','-vf','scale=540:960','-pix_fmt','rgb24','-f','rawvideo','-'])
 a=np.frombuffer(raw,np.uint8).reshape(-1,960,540,3)
 steps=[]
 for prev,cur in zip(a[:80],a[1:81]):
  x=prev[300:700,100:450].mean(2);y=cur[300:700,100:450].mean(2)
  win=np.outer(np.hanning(x.shape[0]),np.hanning(x.shape[1]))
  f=np.fft.fft2((x-x.mean())*win)*np.conj(np.fft.fft2((y-y.mean())*win));f/=np.maximum(np.abs(f),1e-8)
  c=np.fft.ifft2(f).real; yy,xx=np.unravel_index(c.argmax(),c.shape)
  if xx>c.shape[1]//2: xx-=c.shape[1]
  if yy>c.shape[0]//2: yy-=c.shape[0]
  steps.append([int(xx)*2,int(yy)*2])
 s=np.array(steps)
 result[ver]={'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest(),'method':'adjacent frame phase correlation, Hann-windowed subject ROI x200:900 y600:1400, 540x960 decode; shifts expressed at full 1080 width','steps':steps,'mean':s.mean(0).tolist(),'std':s.std(0).tolist(),'acceleration_rms':np.sqrt(np.mean(np.diff(s,axis=0)**2,axis=0)).tolist()}
 for k in range(3):
  sheet=Image.new('RGB',(10*162,3*310));d=ImageDraw.Draw(sheet)
  for n in range(30):
   idx=k*30+n;im=Image.fromarray(a[idx]).resize((162,288));x=(n%10)*162;y=(n//10)*310
   sheet.paste(im,(x,y+20));d.text((x+2,y+2),f'{ver} f{idx} {idx/30:.3f}s',fill='white')
  sheet.save(out/f'{ver}_allframes_{k}.jpg')
result['note']='Translation variation measures jitter; average drift alone does not measure shake.'
(out/'motion.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:{x:y for x,y in v.items() if x!='steps'} if isinstance(v,dict) else v for k,v in result.items()},indent=2))
