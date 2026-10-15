#!/usr/bin/env python3
"""027 Earth Spin v01i (J0256): v01h's labels plus one NUMBER label on the open (0:00-0:23), whose only graphic
(row 3 speed globe) is text-free: "About 1,000 km/h" on "about a thousand kilometers an hour" (SOURCES row 1).
v01h's master was purged from /private/tmp, so this rebuilds from v01g (OWB UAT copy, sha256 as in rough_v01g_pack).

027 Earth Spin v01h (J0154): v01g's picture and audio with NUMBER overlays on chapter 5, "Keeping Score"
(5:57-7:26), the one chapter of v01g with no numeral on screen (its two clocks are text-free). AGENTS.md Reference
lessons item 6, under Chief's J0145 rulings (12 Oct: a to-scale graphic with no numeral is not a NUMBER; a numeral for a
spoken number is a WORDS pass). Overlays only: no cut, VO, bed or graphic changes. Each label is the VO's own words
(numerals for spoken numbers), 4 words or fewer, in on the word's start (0.35 s fade and rise), out before its shot's
cut, never up more than 4 s, in clear space off the subject, in the 026 v05c house pill.
The chapter's three dates build one timeline: 1972 shows alone beside the clock, then 2016 and 2035 drop onto the strip.
Numbers checked against 01_Script/SOURCES.md. `--plan` prints the labels without rendering."""
from pathlib import Path
import json, subprocess as sp, sys, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent; EP=HERE.parent
SRC=Path('/private/tmp/earth027_rough_work_v01g'); V01G=SRC/'027_EarthSpin_rough_v01g.mp4'
WORK=Path('/private/tmp/earth027_rough_work_v01i'); PACK=HERE/'rough_v01i_pack'; PKG=HERE/'rough_v01g_pack'
OUT=Path('/private/tmp/027_EarthSpin_rough_v01i.mp4')
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
ENC=['-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4']
NAVY=(23,36,55,220); YELLOW=(255,214,0,255)
words=json.loads((PKG/'earth_spin_words_list.json').read_text())
cuts=json.loads((PKG/'cuts_v01g.json').read_text())
def at(token,near):
 return min((w for w in words if w['text'].rstrip('.,?').lower()==token.lower()),key=lambda w:abs(w['start']-near))['start']
def cut_at(t):return next(c for c in cuts if c['timeline_in']<=t<c['timeline_out'])

# (text, in = start of the VO word, out, centre x, top y, px, source check)
LABELS=[
 ('Late 1960s',at('late',362.0),365.4,430,880,76,'SOURCES row 16: caesium SI second, 13th CGPM 1967 (WHEN); bottom-left over the clock hardware, off both faces'),
 ('1972',at('nineteen-seventy-two',372.5),376.0,1710,470,84,'SOURCES row 17: leap seconds since 1972 (WHEN, first date of the timeline); right of the full-height clock dial'),
 ('27 times',at('twenty-seven',376.7),379.9,1680,470,76,'SOURCES row 17: exactly 27 leap seconds, 1972 to 2016; right of the clock dial'),
 ('More than a millisecond',at('more',396.9),398.9,960,880,72,'SOURCES row 18: shortest days 1.47-1.66 ms short (2020-2024); over the ice below the melt pond'),
 ('4.5 billion years ago',at('about',434.5),437.2,960,50,72,'SOURCES row 21: 4.54 +/- 0.05 Gyr (VO "about four and a half billion years ago"); top band above the meteors'),
 ('About 1,000 km/h',at('about',6.9),9.25,520,880,80,'SOURCES row 1: London 465.1 m/s x cos 51.5 = about 1,040 km/h (VO "about a thousand kilometers an hour"); bottom-left over the Atlantic, Britain is at the top edge'),
]
# (dates on the strip, the date that drops in, in, out, centre x, top y, source check)
YEARS=(1964,2043)
TIMELINE=[
 ([1972,2016],2016,at('twenty-sixteen',382.5),385.5,1200,860,'SOURCES row 17: last leap second 31 Dec 2016; lower right over the night ocean, clear of the shuttle'),
 ([1972,2016,2035],2035,at('twenty-thirty-five',402.3),404.3,960,60,'SOURCES row 19: CGPM 2022 Resolution 4, by 2035; top band over the instrument case, clear of the cabling'),
]
TW,TH=1200,180

def pill(text,px,dst):
 f=ImageFont.truetype(FONT,px);w=int(f.getlength(text));h=int(px*1.55);padx=int(px*0.55)
 img=Image.new('RGBA',(w+2*padx,h),(0,0,0,0));d=ImageDraw.Draw(img)
 d.rounded_rectangle((0,0,w+2*padx-1,h-1),radius=int(px*0.32),fill=NAVY)
 d.text((padx,int(px*0.22)),text,font=f,fill='white');img.save(dst);return img.size

def year_x(y):return int(90+(TW-180)*(y-YEARS[0])/(YEARS[1]-YEARS[0]))
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
for t,a,b,*_ in LABELS:
 n=len(t.split())
 if n>4:problems.append(f'{t!r} has {n} words')
 if b-a>4.0+0.05:problems.append(f'{t!r} holds {b-a:.2f}s > 4s')
 if b-a<1.5:problems.append(f'{t!r} only {b-a:.2f}s')
 if cut_at(a)['timeline_out']<b-0.01:problems.append(f'{t!r} runs past its cut at {cut_at(a)["timeline_out"]:.2f}')
for ds,new,a,b,*_ in TIMELINE:
 if b-a>4.05 or b-a<1.5:problems.append(f'timeline {new} holds {b-a:.2f}s')
 if cut_at(a)['timeline_out']<b-0.01:problems.append(f'timeline {new} runs past its cut')
for t,a,b,cx,y,px,note in LABELS:print(f'row {cut_at(a)["row"]:>3} {a:7.2f}-{b:7.2f} ({b-a:4.2f}s) {t:24} @({cx},{y}) {px}px  {note}')
for ds,new,a,b,cx,y,note in TIMELINE:print(f'row {cut_at(a)["row"]:>3} {a:7.2f}-{b:7.2f} ({b-a:4.2f}s) timeline {"·".join(map(str,ds)):16} new {new} @({cx},{y})  {note}')
print('problems:',problems or 'none')
if '--plan' in sys.argv or problems:raise SystemExit(1 if problems else 0)

WORK.mkdir(parents=True,exist_ok=True);PACK.mkdir(parents=True,exist_ok=True)
items=[]  # (file, in, out, x, y, rise, meta)
for k,(t,a,b,cx,y,px,note) in enumerate(LABELS):
 r=cut_at(a)['row'];name=f'code_graphic_027_row{r}_{k:02}.png';w,h=pill(t,px,WORK/name)
 items.append((name,a,b,cx-w//2,y,22,dict(row=r,text=t,size=[w,h],check=note)))
for j,(ds,new,a,b,cx,y,note) in enumerate(TIMELINE):
 r=cut_at(a)['row'];k=len(LABELS)+j
 base=f'code_graphic_027_row{r}_{k:02}_timeline.png';mk=f'code_graphic_027_row{r}_{k:02}_timeline_{new}.png'
 strip([d for d in ds if d!=new],WORK/base);marker(new,WORK/mk)
 items.append((base,a,b,cx-TW//2,y,0,dict(row=r,text='timeline '+' '.join(map(str,ds)),size=[TW,TH],check=note)))
 items.append((mk,a+0.15,b,cx-TW//2,y,-40,dict(row=r,text=str(new),size=[TW,TH],check=note,drops_onto=base)))
for it in items:shutil.copyfile(WORK/it[0],PACK/it[0])

inputs=['-i',V01G];fc='[0:v]null[v0];';ov=[]
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
p=sp.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(WORK/'picture.mp4'),'-i',str(V01G),'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',str(OUT)],capture_output=True,text=True)
if p.returncode:raise SystemExit(p.stderr[-4000:])

cards=json.loads((PKG/'overlays_v01g.json').read_text())
(PACK/'overlays_v01i.json').write_text(json.dumps(dict(cards_from_v01g=cards,labels=ov),indent=2))
for c in cuts:c['overlays']=[o['file'] for o in ov if c['timeline_in']<=o['start']<c['timeline_out']]
(PACK/'cuts_v01i.json').write_text(json.dumps(cuts,indent=2))
for n in ('polish_reviewed_ok_v01g.json','picture_qa_reviewed_ok_v01g.json','earth_spin_words_list.json'):shutil.copyfile(PKG/n,PACK/n)

tiles=[]
for k,o in enumerate(o for o in ov if 'drops_onto' not in o):
 t=min(o['start']+0.9,(o['start']+o['end'])/2)
 for tag,src in (('before',V01G),('after',OUT)):
  dst=WORK/f'still_{k:02}_{tag}.jpg'
  sp.run(['ffmpeg','-y','-v','error','-ss',f'{t:.3f}','-i',str(src),'-frames:v','1','-vf','scale=640:360',str(dst)],check=True)
  tiles.append((dst,f"{tag} {int(t//60)}:{t%60:04.1f} row {o['row']} {o['text']}"))
cols=2;rows=(len(tiles)+cols-1)//cols;board=Image.new('RGB',(cols*640,rows*384),(18,18,22));d=ImageDraw.Draw(board)
for i,(pth,label) in enumerate(tiles):
 x=i%cols*640;y=i//cols*384;board.paste(Image.open(pth),(x,y));d.text((x+8,y+364),label,fill='white')
board.save(PACK/'overlay_stills_v01i.jpg',quality=88)
h=hashlib.sha256()
with OUT.open('rb') as fh:
 for blk in iter(lambda:fh.read(1<<20),b''):h.update(blk)
(PACK/'SHA256.txt').write_text(f'{h.hexdigest()}  {OUT.name}\n')
print('wrote',OUT,h.hexdigest())
