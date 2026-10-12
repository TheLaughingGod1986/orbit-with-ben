#!/usr/bin/env python3
"""024 Light Speed v05d (J0149): v05c's 23 labels on v05d's picture (row 2's second shot moved off the source's fade).
Only "7 years" changes: it now holds to 12.8 s, clear of the row 2 -> 3 crossfade (12.83 s). Labels from
full_rough_v05b_pack/TEACHING_GATE_PREP_v05b.md ("Overlay fixes"). No VO, bed or graphic changes.
Each label is the VO's own words (numerals for spoken numbers), 4 words or fewer, in on the word's start (0.35 s fade
and rise), out by the next cut or 4 s, placed in clear space off the subject, chapter-card house style.
Numbers checked against 01_Script/SOURCES.md (see LABELS notes). `--plan` prints the labels without rendering."""
from pathlib import Path
import json, subprocess as sp, sys, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent; EP=HERE.parent
V05B_PIC=Path('/private/tmp/light024_full_work_v05d/picture.mp4'); V05B=Path('/private/tmp/light024_full_work_v05d/cards_only_v05d.mp4')
WORK=Path('/private/tmp/light024_full_work_v05d/labels'); PACK=HERE/'full_rough_v05d_pack'; PK5B=HERE/'full_rough_v05d_pack'
OUT=Path('/private/tmp/024_LightSpeed_full_rough_v05d.mp4')
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
ENC=['-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4']
words=json.loads((EP/'02_Voiceover/words.json').read_text())['words']
def at(token,near):
 return min((w for w in words if w['text'].rstrip('.,').lower()==token.lower()),key=lambda w:abs(w['start']-near))['start']

# (row, text, in = start of the VO word, out, centre x, top y, px, source check)
GX=[255,607,952,1305,1650]; GY=715
LABELS=[
 ('2','1 year',at('one',7.7),10.9,960,830,76,'SOURCES row 2: 1 ship year = 7.09 Earth years at 0.99c'),
 ('2','7 years',at('seven',11.0),12.8,960,830,76,'same; v05d row 2 runs EV from 75.0 s (bright to the cut), out before the 12.83 s crossfade'),
 ('8','7 millionths',at('seven-millionths',53.4),57.2,1380,150,72,'Ashby 2003: SR -7.2 us/day'),
 ('8','about 46',at('forty-six',61.0),62.13,1380,150,72,'Ashby 2003: GR +45.9 us/day'),
 ('8','38 millionths a day',at('thirty-eight-millionths',63.6),67.05,1380,150,72,'Ashby 2003: net +38.7 us/day'),
 ('9','10 kilometers every day',at('ten',75.7),79.7,960,840,72,'FLAG: Ashby gives ~11.6 km/day; VO says "around ten"'),
 ('11','1971',at('1971',85.2),88.0,330,120,84,'Hafele & Keating 1972 (flights 1971)'),
 ('16','10%',at('10%',157.4),161.3,GX[1],GY,60,'formula: gamma(0.1c)=1.005'),
 ('16','90%',at('90%',162.3),166.2,GX[2],GY,60,'SOURCES row 2: gamma 2.294'),
 ('16','99%',at('99%',167.9),171.4,GX[3],GY,60,'SOURCES row 2: gamma 7.089'),
 ('16','7 to 1',at('seven',169.7),171.4,GX[3],GY+90,60,'SOURCES row 2: 7.09'),
 ('16','99.99%',at('99.99%',171.7),175.6,GX[4],GY,60,'formula: gamma(0.9999c)=70.7'),
 ('16','70 to 1',at('seventy',174.6),175.6,GX[4],GY+90,60,'formula: 70.7'),
 ('17','660 meters',at('660',193.0),195.0,960,820,76,'Frisch & Smith 1963: ~660 m; over the clouds: a top pill on black sky trips the split-panel gutter check'),
 ('18','1963',at('1963',199.7),203.6,330,120,84,'Frisch & Smith 1963'),
 ('22','20 years',at('twenty',238.5),240.7,557,110,72,'formula: 10 ly at 0.99c, Earth 20.2 yr (home = blue left dial)'),
 ('22','about 3 years',at('three',241.3),245.2,1450,120,72,'formula: ship 2.85 yr'),
 ('25','10 light-years',at('Ten',276.7),278.5,960,150,72,'contraction plate: 10 ly'),
 ('25','one and a half',at('one',278.9),282.4,960,150,72,'10/7.09 = 1.41 ly; VO "about one and a half"'),
 ('30','90 to 99%',at('90',342.2),344.3,960,150,72,'SOURCES rows 8-9'),
 ('30','nearly five times',at('nearly',344.4),347.9,960,150,72,'SOURCES row 9: 4.7x (prep "five times as much" dropped "nearly")'),
 ('35','over 20 years',at('twenty',413.6),416.0,960,110,72,'SOURCES row 20: 22.4 yr crew time'),
 ('36','100,000 years',at('hundred',422.3),426.2,1350,120,72,'SOURCES row 20: ~100,000 yr on Earth'),
]

def pill(text,px,dst):
 f=ImageFont.truetype(FONT,px);w=int(f.getlength(text));h=int(px*1.55);padx=int(px*0.55)
 img=Image.new('RGBA',(w+2*padx,h),(0,0,0,0));d=ImageDraw.Draw(img)
 d.rounded_rectangle((0,0,w+2*padx-1,h-1),radius=int(px*0.32),fill=(23,36,55,220))
 d.text((padx,int(px*0.22)),text,font=f,fill='white');img.save(dst);return img.size

problems=[]
for r,t,a,b,*_ in LABELS:
 n=len(t.split())
 if n>4:problems.append(f'{t!r} has {n} words')
 if b-a>4.0+0.05:problems.append(f'{t!r} holds {b-a:.2f}s > 4s')
 if b-a<0.3:problems.append(f'{t!r} only {b-a:.2f}s')
for r,t,a,b,cx,y,px,note in LABELS:print(f'row {r:>3} {a:7.2f}-{b:7.2f} ({b-a:4.2f}s) {t:24} @({cx},{y}) {px}px  {note}')
print('problems:',problems or 'none')
if '--plan' in sys.argv or problems:raise SystemExit(1 if problems else 0)

WORK.mkdir(parents=True,exist_ok=True);PACK.mkdir(parents=True,exist_ok=True)
inputs=['-i',V05B_PIC];fc='[0:v]null[v0];';ov=[]
for k,(r,t,a,b,cx,y,px,note) in enumerate(LABELS):
 name=f'code_graphic_024_row{r}_{k:02}.png';p=WORK/name;w,h=pill(t,px,p);shutil.copyfile(p,PACK/name)
 x=cx-w//2;dur=b-a
 inputs+=['-loop','1','-framerate','30','-t',f'{dur:.3f}','-i',p]
 fc+=(f"[{k+1}:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={max(0,dur-0.3):.3f}:d=0.3:alpha=1,"
      f"setpts=PTS-STARTPTS+{a:.3f}/TB[o{k}];"
      f"[v{k}][o{k}]overlay=x={x}:y='{y}+22*max(0\\,1-(t-{a:.3f})/0.35)':eval=frame:eof_action=pass[v{k+1}];")
 ov.append(dict(file=name,row=r,text=t,start=round(a,3),end=round(b,3),x=x,y=y,size=[w,h],check=note))
fc+=f'[v{len(LABELS)}]format=yuv420p[v]'
(WORK/'fc.txt').write_text(fc)
p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,inputs),'-/filter_complex',str(WORK/'fc.txt'),'-map','[v]',*ENC,str(WORK/'picture.mp4')],capture_output=True,text=True)
if p.returncode:raise SystemExit(p.stderr[-4000:])
p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(WORK/'picture.mp4'),'-i',str(V05B),'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',str(OUT)],capture_output=True,text=True)
if p.returncode:raise SystemExit(p.stderr[-4000:])

cards=json.loads((PK5B/'overlays_v05d.json').read_text())
(PACK/'overlays_v05d.json').write_text(json.dumps(dict(cards_from_v05b=cards,labels=ov),indent=2))
cuts=json.loads((PK5B/'cuts_v05d.json').read_text())
for c in cuts:c['overlays']=[o['file'] for o in ov if c['timeline_in']<=o['start']<c['timeline_out']]
(PACK/'cuts_v05d.json').write_text(json.dumps(cuts,indent=2))
rok=json.loads((HERE/'full_rough_v05c_pack/reviewed_ok_v05.json').read_text())
rok.pop('Earth_Views_from_the_International_Space_Station.mp4@122')  # the 0:11 black is gone in v05d
(PACK/'reviewed_ok_v05d.json').write_text(json.dumps(rok,indent=2))

tiles=[]
for k,o in enumerate(ov):
 t=min(o['start']+0.6,(o['start']+o['end'])/2);dst=WORK/f'still_{k:02}.jpg'
 sp.run(['ffmpeg','-y','-v','error','-ss',f'{t:.3f}','-i',str(OUT),'-frames:v','1','-vf','scale=640:360',str(dst)],check=True)
 tiles.append((dst,f"{int(t//60)}:{t%60:04.1f} row {o['row']} {o['text']}"))
cols=4;rows=(len(tiles)+cols-1)//cols;board=Image.new('RGB',(cols*640,rows*384),(18,18,22));d=ImageDraw.Draw(board)
for i,(pth,label) in enumerate(tiles):
 x=i%cols*640;y=i//cols*384;board.paste(Image.open(pth),(x,y));d.text((x+8,y+364),label,fill='white')
board.save(PACK/'overlay_stills_v05d.jpg',quality=88)
h=hashlib.sha256()
with OUT.open('rb') as fh:
 for blk in iter(lambda:fh.read(1<<20),b''):h.update(blk)
(PACK/'SHA256.txt').write_text(f'{h.hexdigest()}  {OUT.name}\n')
print('wrote',OUT,h.hexdigest())
