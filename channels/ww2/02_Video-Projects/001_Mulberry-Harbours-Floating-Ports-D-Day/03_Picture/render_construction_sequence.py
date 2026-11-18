"""Narration-timed construction explanation. Conceptual, not a surveyed plan."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
from draw_engineering import W,H,PAPER,INK,WATER,ACCENT,text,arrow,phoenix,pier
P=Path(__file__).parent
SCENES=[(629.86,'order'),(635.1,'archive_dock'),(640.38,'bridging'),(645.36,'assault'),(651.24,'summer'),(654.84,'total'),(658.46,'dimensions'),(663.96,'width'),(668.3,'archive_scaffold'),(674.16,'tonnage'),(679.04,'equipment'),(683.44,'chambers'),(689.12,'bottleneck'),(696.42,'capacity'),(700.22,'engineers'),(705.8,'thames'),(712.82,'excavate'),(720.4,'levee'),(723.944,'base'),(732.524,'breach'),(738.864,'tow'),(746.364,'walls'),(752.264,'end')]
ARCH={'archive_dock':'H_35379_30910542.jpg','archive_scaffold':'H_40320_30910479.jpg'}
def frame(kind,p):
 if kind=='bridging':return pier(p)
 if kind in ('dimensions','tonnage'):return phoenix(p if kind=='dimensions' else 1)
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 text(d,(80,45),'BUILDING A PORT BEFORE D-DAY',52)
 text(d,(80,125),'Own explanatory schematic | Not a surveyed site, reconstruction or calculated engineering model',26)
 d.line((80,190,1840,190),fill=INK,width=2)
 text(d,(80,1008),'Inherited J2991 sources: S5 (ICE, 1948) | S20-S23 | Locked narration unchanged',26)
 if kind in ('excavate','levee','base','breach','tow','walls'):
  titles={'excavate':'EXCAVATE BESIDE THE THAMES','levee':'KEEP THE RIVER OUT','base':'POUR THE LOWER SECTION','breach':'ADMIT WATER AT HIGH TIDE','tow':'TOW THE FLOATING TRAY','walls':'FINISH THE WALLS AFLOAT'}
  text(d,(100,240),titles[kind],45,ACCENT)
  d.rectangle((100,450,1820,900),fill='#c8b999')
  d.rectangle((100,570,650,900),fill=WATER)
  d.rectangle((800,500,1680,820),fill=PAPER)
  if kind in ('breach','tow','walls'):
   water=810-int(240*p) if kind=='breach' else 570
   d.rectangle((650,450,800,820),fill=PAPER)
   d.rectangle((650,water,1680,820),fill=WATER)
  else:d.rectangle((650,450,800,820),fill='#c8b999')
  if kind in ('base','breach','tow','walls'):
   y=760 if kind=='base' else min(760,water+80) if kind=='breach' else 650
   x=900-int(500*p) if kind=='tow' else 900
   top=y-(60 if kind=='base' else 100)-(int(160*p) if kind=='walls' else 0)
   d.line((x,top,x,y,x+620,y,x+620,top),fill=INK,width=18)
   text(d,(850,920),'Simplified section | Construction stages, not actual basin geometry',26)
  if kind=='excavate':
   arrow(d,(1100,340),(1100,500+int(210*p)));text(d,(1200,365),'12 basins',40)
  if kind=='levee':arrow(d,(530,370),(720,465));text(d,(100,330),'EARTH BANK',35)
  if kind=='base':text(d,(960,370),'LOWER 15 FEET',42)
  if kind=='walls':text(d,(960,370),'UPPER 45 FEET',42)
  if kind=='tow':arrow(d,(700,580),(200,580));text(d,(100,340),'TO WET DOCKS',38)
  if kind=='breach':arrow(d,(380,550),(950,550));text(d,(100,340),'BREACH THE BANK',38)
 elif kind in ('assault','summer','total'):
  n=147 if kind=='assault' else 65 if kind=='summer' else 212
  label={'assault':'FOR THE JUNE ASSAULT','summer':'SUPPLEMENTARY SUMMER UNITS','total':'PHOENIX CAISSONS IN ALL'}[kind]
  text(d,(120,250),label,46,ACCENT)
  for i in range(n):
   x=120+i%27*60;y=380+i//27*56
   d.rectangle((x,y,x+43,y+31),fill=INK if i<int(n*p) else '#c5c7bf')
  text(d,(1250,855),str(n),100,ACCENT);text(d,(120,930),'Each box represents one caisson; different classes had different sizes',28)
 else:
  cards={'order':('SEPTEMBER 1943 → MAY 1944','Ministry of Supply and War Office | Contractors build the components'),
   'width':('56 FEET 3 INCHES','Type A1 width | Largest class'),
   'equipment':('CREW QUARTERS + BOFORS','Equipment named in the narration; locations not reconstructed'),
   'chambers':('22 FLOODING CHAMBERS','Kingston valves control the admission of water'),
   'bottleneck':('DRY DOCKS ALREADY OCCUPIED','Warships and Atlantic freighters compete for dock space'),
   'capacity':('ROOM FOR FEWER THAN A THIRD','A different construction method was needed'),
   'engineers':('McALPINE + MOWLEM','A workaround on the muddy banks of the Thames'),
   'thames':('ROTHERHITHE · DEPTFORD','ERITH · BARKING | Thames construction sites')}
  title,sub=cards[kind];text(d,(120,330),title,58,ACCENT);text(d,(120,450),sub,34)
  if kind=='width':
   d.rectangle((750,580,1150,910),fill='#b3b8b2',outline=INK,width=8);arrow(d,(750,550),(1150,550));arrow(d,(1150,550),(750,550))
  elif kind=='chambers':
   for i in range(22):
    x=130+i%11*145;y=620+i//11*120;d.rectangle((x,y,x+120,y+80),outline=INK,width=4)
   text(d,(130,900),'Count only; actual partition arrangement is not reconstructed',28)
  else:d.line((120,760,120+int(1650*p),760),fill=ACCENT,width=7)
 return im

def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--originals',type=Path,required=True);a.add_argument('--vo',type=Path,required=True);a.add_argument('--stt',type=Path,required=True);a.add_argument('--render',action='store_true');args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 words=json.loads(args.stt.read_text())['words'];sources={r['file']:r for r in json.loads((P/'archive_cleared_v07.json').read_text())['records']};rows=[]
 for i,((start,kind),(end,_)) in enumerate(zip(SCENES,SCENES[1:])):
  first,last=round(start*25),round(end*25);key=f'construction_{i+1:02}_{kind}_v14';target=args.out/(key+'.mp4')
  word=min((w for w in words if w['text'].strip()),key=lambda w:abs(w['start']-start));assert abs(word['start']-start)<.001
  r=dict(scene=kind,start_s=first/25,end_s=last/25,frames=last-first,film_start_frame=first,film_end_frame=last,anchor=word,source='Inherited J2991 S5 / S20-S23',file=target.name,status='DRAFT_NOT_QUALITY_APPROVED')
  if kind in ARCH:
   rec=sources[ARCH[kind]];f=args.originals/rec['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==rec['sha256']
   im=ImageOps.exif_transpose(Image.open(f)).convert('RGB');scale=min(1.4,1700/im.width,850/im.height);assert scale*1.02<=2.35
   plate=Image.new('RGB',(W,H),PAPER);sz=(round(im.width*scale),round(im.height*scale));plate.paste(im.resize(sz,Image.Resampling.LANCZOS),((W-sz[0])//2,(960-sz[1])//2));plate.save(args.out/(key+'.jpg'))
   credit=Image.new('RGBA',(W,H));d=ImageDraw.Draw(credit);text(d,(45,955),rec['subject'],29);text(d,(45,1010),'IWM '+rec['fields_verbatim']['catalogue_number']+' | Crown copyright expired | via Wikimedia Commons',25);credit.save(args.out/(key+'_credit.png'))
   r.update(source_file=rec['file'],source_sha256=rec['sha256'],url=rec['url'],maximum_upscale=scale*1.02)
   if args.render:subprocess.run(['ffmpeg','-v','error','-n','-loop','1','-i',str(args.out/(key+'.jpg')),'-i',str(args.out/(key+'_credit.png')),'-filter_complex',f"[0:v]zoompan=z='1+0.02*on/{last-first-1}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=25[v];[v][1:v]overlay=0:0,format=yuv420p[o]",'-map','[o]','-frames:v',str(last-first),'-an','-c:v','libx264','-preset','veryfast','-crf','20','-threads','2',str(target)],check=True)
  else:
   frame(kind,.9).save(args.out/(key+'.jpg'),quality=92)
   if args.render:
    proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','25','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-threads','2','-pix_fmt','yuv420p',str(target)],stdin=subprocess.PIPE)
    for n in range(last-first):proc.stdin.write(frame(kind,n/max(last-first-1,1)).tobytes())
    proc.stdin.close();assert proc.wait()==0
  if args.render:
   subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True);r['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
  rows.append(r);print(key,flush=True)
 m=dict(start_s=rows[0]['start_s'],end_s=rows[-1]['end_s'],scenes=rows,review='Technical and still-image evidence only; no audio/motion verdict; no score')
 if args.render:
  listing=args.out/'concat.txt';listing.write_text(''.join("file '"+r['file']+"'\n" for r in rows));silent=args.out/'construction_silent_v14.mp4';preview=args.out/'construction_narration_v14.mp4'
  subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(silent)],check=True)
  subprocess.run(['ffmpeg','-v','error','-n','-i',str(silent),'-ss',str(m['start_s']),'-i',str(args.vo),'-map','0:v','-map','1:a','-t',str(m['end_s']-m['start_s']),'-c:v','copy','-c:a','aac','-b:a','192k',str(preview)],check=True)
  subprocess.run(['ffmpeg','-v','error','-i',str(preview),'-f','null','-'],check=True)
  m['preview_sha256']=hashlib.sha256(preview.read_bytes()).hexdigest()
 (args.out/'construction_manifest_v14.json').write_text(json.dumps(m,indent=2)+'\n')
if __name__=='__main__':main()
