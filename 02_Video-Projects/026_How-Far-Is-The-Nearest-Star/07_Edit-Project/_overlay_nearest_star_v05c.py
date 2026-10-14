#!/usr/bin/env python3
"""026 Nearest Star v05c (J0148): v05b's picture and audio with the per-chapter NUMBER overlays from
rough_v05b_pack/TEACHING_GATE_PREP_v05b.md ("Overlay fixes"), under Chief's J0145 rulings (12 Oct: a to-scale graphic
with no numeral is not a NUMBER; a numeral for a spoken number is a WORDS pass). Overlays only: no cut, VO, bed or
graphic changes. Each label is the VO's own words (numerals for spoken numbers), 4 words or fewer, in on the word's start
(0.35 s fade and rise), out by 4 s, in clear space off the subject, chapter-card house style. A label may run across one
cut where its own shot ends within a second of the word and the next shot leaves the same space clear.
Chapter 5's three dates build one timeline: 2016, then 2031 and 2035 drop onto the same strip.
Numbers checked against 01_Script/SOURCES.md (see the notes). `--plan` prints the labels without rendering."""
from pathlib import Path
import json, subprocess as sp, sys, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent; EP=HERE.parent
SRC=Path('/private/tmp/nearest026_rough_work_v05b')
V05B_PIC=SRC/'picture.mp4'; V05B=SRC/'026_NearestStar_v05b_PHONE.mp4'
WORK=Path('/private/tmp/nearest026_rough_work_v05c'); PACK=HERE/'rough_v05c_pack'; PK5B=HERE/'rough_v05b_pack'
OUT=Path('/private/tmp/026_NearestStar_v05c_PHONE.mp4')
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
ENC=['-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4']
NAVY=(23,36,55,220); YELLOW=(255,214,0,255)
words=json.loads((PK5B/'nearest_star_words_list.json').read_text())
def at(token,near):
 return min((w for w in words if w['text'].rstrip('.,?').lower()==token.lower()),key=lambda w:abs(w['start']-near))['start']

# (row, text, in = start of the VO word, out, centre x, top y, px, source check)
LABELS=[
 ('2','More than 4 years',at('more',11.1),13.5,960,120,76,'SOURCES row 3: light takes about 4.24 years'),
 ('14','1838',at('eighteen',182.6),186.5,420,820,84,'SOURCES: Bessel, 61 Cygni parallax 1838 (WHEN)'),
 ('14','About 13 kilometers',at('about',194.3),197.8,1430,850,72,'SOURCES: 2 cm coin at about 13.2 km; runs into row 14 eso1250a (Bessel shot ends 195.4)'),
 ('15','More than a billion',at('more',211.3),214.8,960,880,72,'SOURCES: Gaia DR3 1.46 billion with parallax'),
 ('15','About 5 kilometers',at('about',222.0),224.4,1540,880,72,'SOURCES: coin at about 5.4 km'),
 ('18','About 15 meters',at('about',246.5),250.0,960,880,72,'SOURCES: pinhead 15 m at 1:10^10'),
 ('20','About 4,000 kilometers',at('about',269.6),272.0,960,120,72,'SOURCES: Proxima about 4,000 km at 1:10^10'),
 ('22','1977',at('nineteen',300.3),303.3,1560,110,84,'SOURCES: Voyager 1 launched 5 Sep 1977 (WHEN); runs into PIA21739 (Voyager shot ends 300.8)'),
 ('22','About 2.5 kilometers',at('about',306.5),310.5,1420,120,72,'SOURCES: about 2.6 km at 1:10^10; VO "about two and a half"'),
 ('28','Every 11 days',at('every',391.1),394.6,960,110,72,'SOURCES: Proxima b orbit 11.2 days; runs into eso1629e (shot ends 391.9)'),
 ('31','About 20 years',at('about',434.9),438.4,960,110,72,'SOURCES: Starshot about 20 years; runs into the next CamA frame (shot ends 436.6)'),
]
# Chapter 5 timeline: (row, dates on the strip, the date that drops in, in, out, centre x, top y, source check)
YEARS=(2014,2037)
TIMELINE=[
 ('28',[2016],2016,at('2016',382.1),385.6,960,860,'SOURCES: Anglada-Escude et al. 2016 (Proxima b found); runs into eso1629d (shot ends 383.0)'),
 ('32',[2016,2031],2031,at('2031',449.3),452.4,960,90,'SOURCES: message sent Oct 2026 arrives about Jan 2031'),
 ('32',[2016,2031,2035],2035,at('2035',455.7),459.2,960,90,'SOURCES: earliest reply about Apr 2035; runs into PIA26147 (shot ends 457.4)'),
]
TW,TH=1400,180

def pill(text,px,dst):
 f=ImageFont.truetype(FONT,px);w=int(f.getlength(text));h=int(px*1.55);padx=int(px*0.55)
 img=Image.new('RGBA',(w+2*padx,h),(0,0,0,0));d=ImageDraw.Draw(img)
 d.rounded_rectangle((0,0,w+2*padx-1,h-1),radius=int(px*0.32),fill=NAVY)
 d.text((padx,int(px*0.22)),text,font=f,fill='white');img.save(dst);return img.size

def year_x(y):return int(70+(TW-140)*(y-YEARS[0])/(YEARS[1]-YEARS[0]))
LINE_Y=128
def strip(dates,dst):
 """The strip with the dates already said (white); the new date is drawn separately so it can drop in."""
 img=Image.new('RGBA',(TW,TH),(0,0,0,0));d=ImageDraw.Draw(img);f=ImageFont.truetype(FONT,56)
 d.rounded_rectangle((0,0,TW-1,TH-1),radius=26,fill=NAVY)
 d.line((50,LINE_Y,TW-50,LINE_Y),fill=(255,255,255,200),width=6)
 for y in dates:
  x=year_x(y);d.ellipse((x-13,LINE_Y-13,x+13,LINE_Y+13),fill='white')
  d.text((x-int(f.getlength(str(y)))//2,22),str(y),font=f,fill='white')
 img.save(dst);return img.size
def marker(y,dst):
 img=Image.new('RGBA',(TW,TH),(0,0,0,0));d=ImageDraw.Draw(img);f=ImageFont.truetype(FONT,56);x=year_x(y)
 d.ellipse((x-16,LINE_Y-16,x+16,LINE_Y+16),fill=YELLOW)
 d.text((x-int(f.getlength(str(y)))//2,22),str(y),font=f,fill=YELLOW);img.save(dst)

problems=[]
for r,t,a,b,*_ in LABELS:
 n=len(t.split())
 if n>4:problems.append(f'{t!r} has {n} words')
 if b-a>4.0+0.05:problems.append(f'{t!r} holds {b-a:.2f}s > 4s')
 if b-a<1.5:problems.append(f'{t!r} only {b-a:.2f}s')
for r,ds,new,a,b,*_ in TIMELINE:
 if b-a>4.05 or b-a<1.5:problems.append(f'timeline {new} holds {b-a:.2f}s')
for r,t,a,b,cx,y,px,note in LABELS:print(f'row {r:>3} {a:7.2f}-{b:7.2f} ({b-a:4.2f}s) {t:24} @({cx},{y}) {px}px  {note}')
for r,ds,new,a,b,cx,y,note in TIMELINE:print(f'row {r:>3} {a:7.2f}-{b:7.2f} ({b-a:4.2f}s) timeline {"·".join(map(str,ds)):16} new {new} @({cx},{y})  {note}')
print('problems:',problems or 'none')
if '--plan' in sys.argv or problems:raise SystemExit(1 if problems else 0)

WORK.mkdir(parents=True,exist_ok=True);PACK.mkdir(parents=True,exist_ok=True)
items=[]  # (file, in, out, x, y, rise, meta)
for k,(r,t,a,b,cx,y,px,note) in enumerate(LABELS):
 name=f'code_graphic_026_row{r}_{k:02}.png';w,h=pill(t,px,WORK/name)
 items.append((name,a,b,cx-w//2,y,22,dict(row=r,text=t,size=[w,h],check=note)))
for j,(r,ds,new,a,b,cx,y,note) in enumerate(TIMELINE):
 k=len(LABELS)+j;base=f'code_graphic_026_row{r}_{k:02}_timeline.png';mk=f'code_graphic_026_row{r}_{k:02}_timeline_{new}.png'
 strip([d for d in ds if d!=new],WORK/base);marker(new,WORK/mk)
 items.append((base,a,b,cx-TW//2,y,0,dict(row=r,text='timeline '+' '.join(map(str,ds)),size=[TW,TH],check=note)))
 items.append((mk,a+0.15,b,cx-TW//2,y,-40,dict(row=r,text=str(new),size=[TW,TH],check=note,drops_onto=base)))
for it in items:shutil.copyfile(WORK/it[0],PACK/it[0])

inputs=['-i',V05B_PIC];fc='[0:v]null[v0];';ov=[]
for k,(name,a,b,x,y,rise,meta) in enumerate(items):
 dur=b-a
 inputs+=['-loop','1','-framerate','30','-t',f'{dur:.3f}','-i',WORK/name]
 fc+=(f"[{k+1}:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={max(0,dur-0.3):.3f}:d=0.3:alpha=1,"
      f"setpts=PTS-STARTPTS+{a:.3f}/TB[o{k}];"
      f"[v{k}][o{k}]overlay=x={x}:y='{y}+{rise}*max(0\\,1-(t-{a:.3f})/0.35)':eval=frame:eof_action=pass[v{k+1}];")
 ov.append(dict(file=name,start=round(a,3),end=round(b,3),x=x,y=y,**meta))
fc+=f'[v{len(items)}]format=yuv420p[v]'
(WORK/'fc.txt').write_text(fc)
p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*map(str,inputs),'-/filter_complex',str(WORK/'fc.txt'),'-map','[v]',*ENC,str(WORK/'picture.mp4')],capture_output=True,text=True)
if p.returncode:raise SystemExit(p.stderr[-4000:])
p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(WORK/'picture.mp4'),'-i',str(V05B),'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',str(OUT)],capture_output=True,text=True)
if p.returncode:raise SystemExit(p.stderr[-4000:])

cards=json.loads((PK5B/'overlays_v05b.json').read_text())
(PACK/'overlays_v05c.json').write_text(json.dumps(dict(cards_from_v05b=cards,labels=ov),indent=2))
cuts=json.loads((PK5B/'cuts_v05b.json').read_text())
for c in cuts:c['overlays']=[o['file'] for o in ov if c['timeline_in']<=o['start']<c['timeline_out']]
(PACK/'cuts_v05c.json').write_text(json.dumps(cuts,indent=2))
for n in ('polish_reviewed_ok_v05b.json','nearest_star_words_list.json'):shutil.copyfile(PK5B/n,PACK/n)

tiles=[]
for k,o in enumerate(o for o in ov if 'drops_onto' not in o):
 t=min(o['start']+0.9,(o['start']+o['end'])/2);dst=WORK/f'still_{k:02}.jpg'
 sp.run(['ffmpeg','-y','-v','error','-ss',f'{t:.3f}','-i',str(OUT),'-frames:v','1','-vf','scale=640:360',str(dst)],check=True)
 tiles.append((dst,f"{int(t//60)}:{t%60:04.1f} row {o['row']} {o['text']}"))
cols=4;rows=(len(tiles)+cols-1)//cols;board=Image.new('RGB',(cols*640,rows*384),(18,18,22));d=ImageDraw.Draw(board)
for i,(pth,label) in enumerate(tiles):
 x=i%cols*640;y=i//cols*384;board.paste(Image.open(pth),(x,y));d.text((x+8,y+364),label,fill='white')
board.save(PACK/'overlay_stills_v05c.jpg',quality=88)
h=hashlib.sha256()
with OUT.open('rb') as fh:
 for blk in iter(lambda:fh.read(1<<20),b''):h.update(blk)
(PACK/'SHA256.txt').write_text(f'{h.hexdigest()}  {OUT.name}\n')
print('wrote',OUT,h.hexdigest())
