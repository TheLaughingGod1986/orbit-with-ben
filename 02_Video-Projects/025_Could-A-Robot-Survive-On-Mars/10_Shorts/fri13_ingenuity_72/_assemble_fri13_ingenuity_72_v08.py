#!/usr/bin/env python3
"""J2549: replace only Chief-named v07 windows; copy its AAC audio unchanged. No upload."""
from pathlib import Path
import importlib.util, json, subprocess, hashlib, shutil, sys
from PIL import Image, ImageEnhance
REPO=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
WORK=Path('/Volumes/MiniWork/scratch/J2549-v08/render');WORK.mkdir(parents=True,exist_ok=True)
POOL=Path('/Volumes/MiniWork/scratch/J2549-v08/assets')
NAS=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports')
SRC=NAS/'fri13_ingenuity_72_v07.mp4'; OUT=WORK/'fri13_ingenuity_72_v08.mp4'
def run(a):subprocess.run([str(x) for x in a],check=True)
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
assert sha(SRC)=='947f5c726d6686c3c8317c4b7e02be4953412c1ad15f574573190e9fe1f3a688'
assert not OUT.exists(), 'Never overwrite existing version'
spec=importlib.util.spec_from_file_location('v06',HERE/'_assemble_fri13_ingenuity_72_v06.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.WORK=WORK;m.wed.WORK=WORK
raw=json.loads((HERE/'words.json').read_text())['words'];words=[dict(word=w['text'],start=w['start'],end=w['end']) for w in raw]
caps=m.caption_track_safe(words,26.4);title=WORK/'title.png';m.wed.title_png(title,with_id=False)
# Actual v06 cut boundaries on its 30 fps frame grid (84,176,298,432,566).
spans=[(84,176,'PIA24542_full.jpg',(7100,4200,6000)),(298,432,'PIA24542_full.jpg',(5900,3400,2100))]
clips=[];evidence=[]
for i,(a,b,name,center) in enumerate(spans):
 im=Image.open(POOL/name).convert('RGB');sw,sh=im.size
 # Crop to true 9:16 inside the source. Panorama edges excluded by central crop.
 cx,cy,bh=center;bw=bh*9/16;dest=WORK/f'replacement_{i}.mp4'
 p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','14',str(dest)],stdin=subprocess.PIPE)
 for n in range(b-a):
  u=n/max(1,b-a-1);z=1+.06*u;w,h=bw/z,bh/z
  x=max(0,min(sw-w,cx-w/2+u*bw*.025));y=max(0,min(sh-h,cy-h/2))
  frame=im.resize((1080,1920),Image.Resampling.BICUBIC,box=(x,y,x+w,y+h));p.stdin.write(frame.tobytes())
 p.stdin.close();assert p.wait()==0
 clips.append(dest);evidence.append(dict(start_frame=a,end_frame=b,source=name,sha256=sha(POOL/name),size=[sw,sh],max_upscale=1920/(bh/1.06)))
inputs=['ffmpeg','-y','-v','error','-i',SRC]
for c in clips: inputs+=['-i',c]
inputs+=['-f','concat','-safe','0','-i',caps,'-loop','1','-i',title]
f=[];prior='0:v'
for i,(a,b,*_) in enumerate(spans):
 f+=[f'[{i+1}:v]setpts=PTS+{a}/30/TB[r{i}]',f'[{prior}][r{i}]overlay=0:0:enable=\'gte(n,{a})*lt(n,{b})\':eof_action=pass[v{i}]'];prior=f'v{i}'
enable='+'.join(f'(gte(n,{a})*lt(n,{b}))' for a,b,*_ in spans)
f += [f'[3:v]fps=30,format=rgba[cp]',f'[{prior}][cp]overlay=0:0:enable=\'{enable}\':eof_action=pass[vc]',f'[vc][4:v]overlay=0:0:enable=\'gte(n,298)*lte(t,14)\':shortest=1,format=yuv420p[v]']
run(inputs+['-filter_complex',';'.join(f),'-map','[v]','-map','0:a','-c:v','libx264','-preset','veryfast','-crf','16','-r','30','-fps_mode','cfr','-c:a','copy','-t','26.4','-movflags','+faststart',OUT])
(WORK/'replacement_evidence.json').write_text(json.dumps(dict(source_sha256=sha(SRC),output_sha256=sha(OUT),spans=evidence,audio='AAC packets stream-copied from v07'),indent=2)+'\n')
print(OUT,sha(OUT),flush=True)
