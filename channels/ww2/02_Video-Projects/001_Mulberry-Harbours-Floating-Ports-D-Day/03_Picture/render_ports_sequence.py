"""S06/S07 sourced port-denial explanation on the locked narration clock.
Original conceptual diagrams; not a surveyed plan or a reconstruction.
"""
import argparse,hashlib,json,math,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
from draw_engineering import W,H,PAPER,INK,WATER,ACCENT,text,arrow
SCENES=[(168.58,'morgan'),(176.02,'overlord'),(182.36,'ports'),(192.28,'charges'),(198.88,'inland'),(203.28,'quays'),(205.8,'blockships'),(210.56,'lesson'),(213.14,'capture'),(220.74,'mines'),(223.34,'delay'),(228.42,'end')]

def frame(kind,p):
    im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
    text(d,(80,45),'CAPTURING A PORT WAS NOT ENOUGH',52)
    text(d,(80,125),'Own explanatory illustration | Not a surveyed harbour, fortification map or reconstruction',27)
    d.line((80,190,1840,190),fill=INK,width=2)
    text(d,(80,1008),'Inherited sources: J2991 S2 (SHAEF); S3 (Ruppenthal, 1953) | S06-S07',26)
    cards={'morgan':('SPRING 1943','Frederick Morgan | COSSAC planning staff'),
      'overlord':('OPERATION OVERLORD','The lesson of Dieppe'),
      'ports':('FORTIFIED CHANNEL PORTS','Cherbourg · Le Havre · Boulogne · Calais · Dunkirk'),
      'lesson':('MORGAN’S WARNING','Capture did not guarantee a working harbour'),
      'capture':('27 JUNE 1944','US troops take Cherbourg'),
      'delay':('BULK CARGO: AUGUST','A captured port still needed extensive clearance and repair')}
    if kind in cards:
        title,sub=cards[kind];text(d,(150,340),title,65,ACCENT);text(d,(150,465),sub,39)
        d.line((150,790,150+int(1520*p),790),fill=ACCENT,width=7)
        if kind=='delay':
            for x,label in [(200,'6 JUNE: D-DAY'),(770,'27 JUNE: CAPTURE'),(1400,'AUGUST')]:
                d.ellipse((x-8,865,x+8,881),fill=INK);text(d,(x-60,900),label,26)
            d.line((200,873,1400,873),fill=INK,width=4)
            text(d,(200,950),'Milestones spaced for legibility; not a proportional timeline',24)
    else:
        d.rectangle((100,350,1820,900),fill=WATER)
        d.rectangle((100,350,370,900),fill='#c6b99a');d.rectangle((1550,350,1820,900),fill='#c6b99a')
        d.rectangle((100,350,1820,450),fill='#c6b99a')
        d.rectangle((370,450,1550,480),fill=INK)
        d.rectangle((370,480,440,700),fill=INK);d.rectangle((1480,480,1550,700),fill=INK)
        labels={'charges':'LOCK GATES, CRANES AND QUAY WALLS','inland':'EVEN AN INLAND CAPTURE COULD COME TOO LATE','quays':'DEMOLITION DISABLES THE QUAYS','blockships':'SCUTTLED SHIPS BLOCK THE ENTRANCE','mines':'WRECKAGE AND MINES DELAY CARGO'}
        text(d,(120,260),labels[kind],41,ACCENT)
        # Generalised gantry and basin: no invented exact positions.
        d.line((560,450,560,360,760,360),fill=INK,width=10)
        d.line((750,360,750,420),fill=INK,width=4)
        if kind=='charges':
            for x,y in [(570,440),(900,465),(1480,620)]:
                d.ellipse((x-15,y-15,x+15,y+15),fill=ACCENT)
            text(d,(560,760),'Functional targets only; no charge locations reconstructed',29)
        elif kind=='inland':
            arrow(d,(950,500),(950,590+int(150*p)))
            text(d,(560,800),'A port could be denied before surrender',34)
        elif kind=='quays':
            for x in (620,880,1120):
                d.line((x,445,x+60,480,x+25,520),fill=ACCENT,width=12)
            text(d,(560,800),'Cargo-handling infrastructure destroyed',34)
        else:
            d.polygon([(700,740),(1150,740),(1100,820),(740,820)],fill=INK)
            d.rectangle((820,695,930,740),fill=INK)
            d.line((700,715,1150,840),fill=ACCENT,width=9)
            if kind=='mines':
                for x,y in [(520,650),(1270,650),(1370,820)]:
                    d.ellipse((x-15,y-15,x+15,y+15),fill=ACCENT)
            text(d,(530,940),'Symbolic basin and obstacles; not the actual Cherbourg layout',28)
    return im

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--vo',type=Path);a.add_argument('--render',action='store_true');args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    records=[]
    for i,((start,kind),(end,_)) in enumerate(zip(SCENES,SCENES[1:])):
        first,last=round(start*25),round(end*25);key=f'ports_{i+1:02}_{kind}_v12';frame(kind,.9).save(args.out/(key+'.jpg'),quality=92)
        r=dict(scene=kind,start_s=first/25,end_s=last/25,film_start_frame=first,film_end_frame=last,frames=last-first,source='J2991 S2 S3 / inherited port denial claims',status='DRAFT_NOT_QUALITY_APPROVED')
        if args.render:
            target=args.out/(key+'.mp4');proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','25','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-threads','2','-pix_fmt','yuv420p',str(target)],stdin=subprocess.PIPE)
            for n in range(last-first):proc.stdin.write(frame(kind,n/max(last-first-1,1)).tobytes())
            proc.stdin.close()
            if proc.wait():raise RuntimeError(kind)
            subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
            r.update(file=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        records.append(r);print(key,flush=True)
    manifest=dict(start_s=records[0]['start_s'],end_s=records[-1]['end_s'],fps=25,scenes=records,review='TECHNICAL_AND_STILLS_ONLY')
    if args.render:
        listing=args.out/'concat.txt';listing.write_text(''.join("file '"+r['file']+"'\n" for r in records));silent=args.out/'ports_sequence_silent_v12.mp4'
        subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(silent)],check=True)
        if args.vo:
            target=args.out/'ports_narration_preview_v12.mp4'
            subprocess.run(['ffmpeg','-v','error','-n','-i',str(silent),'-ss',str(manifest['start_s']),'-i',str(args.vo),'-map','0:v','-map','1:a','-t',str(manifest['end_s']-manifest['start_s']),'-c:v','copy','-c:a','aac','-b:a','192k',str(target)],check=True)
            subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
            manifest['preview']=dict(file=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    (args.out/'ports_sequence_manifest_v12.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
