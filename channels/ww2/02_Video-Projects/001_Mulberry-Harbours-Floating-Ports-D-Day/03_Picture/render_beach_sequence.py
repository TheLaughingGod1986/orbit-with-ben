"""S08/S09: original beach-logistics explanation on the locked narration clock.
All quantities inherited from J2991 claim 8 (S2/S3/S5). Not a reconstruction.
"""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from draw_engineering import W,H,PAPER,INK,WATER,ACCENT,text,arrow
SCENES=[(228.42,'beaches'),(235.36,'problem'),(240.,'tide'),(245.1,'range'),(251.08,'slope'),(255.5,'retreat'),(260.959,'lst'),(267.3,'drop'),(271.86,'stranded'),(275.2,'refloat'),(279.1,'liberty'),(288.66,'transfer'),(298.5,'gale'),(309.,'end')]

def ship(d,x,y,large=False):
    length=400 if large else 270
    d.polygon([(x,y),(x+length,y),(x+length-40,y+65),(x+30,y+65)],fill=INK)
    d.rectangle((x+45,y-55,x+105,y),fill=INK)
    if large:
        for xx in (x+170,x+290):
            d.line((xx,y,xx,y-150),fill=INK,width=6)
            d.line((xx,y-145,xx+80,y-70),fill=INK,width=4)

def frame(kind,p):
    im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
    text(d,(80,45),'WHY OPEN BEACHES WERE NOT ENOUGH',52)
    text(d,(80,125),'Own explanatory illustration | Not a surveyed profile or operational reconstruction',28)
    d.line((80,190,1840,190),fill=INK,width=2)
    text(d,(80,1008),'J2991 claim 8 | SHAEF; Ruppenthal (1953), p. 287; ICE / Pavry (1948)',26)
    if kind in ('beaches','problem','tide','range','slope','retreat'):
        y=650+int(150*p) if kind in ('slope','retreat') else 800-int(150*p)
        d.rectangle((120,y,1800,935),fill=WATER)
        d.polygon([(120,490),(120,935),(1450,935)],fill='#c6b99a')
        d.line((120,490,1450,935),fill=INK,width=4)
        text(d,(170,550),'SHORE',32);text(d,(1480,855),'SEA',32)
        titles={'beaches':'LAND ACROSS OPEN BEACHES','problem':'THE SHORELINE MOVES','tide':'THE CHANNEL TIDE RISES AND FALLS','range':'UP TO 24 FEET','slope':'A GENTLY SLOPING BEACH','retreat':'UP TO HALF A MILE OUT TO SEA'}
        text(d,(150,275),titles[kind],51,ACCENT)
        if kind in ('tide','range'):
            for yy,label in [(650,'HIGH WATER'),(800,'LOW WATER')]:
                d.line((1100,yy,1760,yy),fill='#74949c',width=3);text(d,(1400,yy-45),label,26)
            arrow(d,(1780,650),(1780,800));arrow(d,(1780,800),(1780,650))
            if kind=='range':text(d,(150,365),'Spring tides | height of a two-storey house',33)
        elif kind in ('slope','retreat'):
            xx=120+(y-490)*1330/445
            d.ellipse((xx-12,y-12,xx+12,y+12),fill=ACCENT)
            if kind=='retreat':
                arrow(d,(610,900),(610+int(700*p),900))
                text(d,(150,370),'Waterline retreat | twice a day',35)
        else:d.line((150,390,150+int(1200*p),390),fill=ACCENT,width=6)
        text(d,(140,960),'Vertical and horizontal scales differ; no measured beach gradient shown',26)
    elif kind in ('lst','drop','stranded','refloat'):
        # Same stylised beach and hull across all four phases: no hull jump at cuts.
        level={'lst':600,'drop':600+int(190*p),'stranded':790,'refloat':790-int(190*p)}[kind]
        hull_y= min(level-45,710)
        d.rectangle((100,level,1820,930),fill=WATER)
        d.polygon([(100,700),(100,930),(1820,930)],fill='#c6b99a')
        ship(d,660,hull_y)
        labels={'lst':'LST: BEACH NEAR HIGH WATER','drop':'WAIT FOR THE TIDE TO DROP','stranded':'STRANDED FOR 10–12 HOURS','refloat':'NEXT HIGH TIDE: FLOAT FREE'}
        text(d,(150,280),labels[kind],52,ACCENT)
        if kind=='drop':
            xx=970+int(450*p);d.rectangle((xx,760,xx+100,810),fill=ACCENT)
            for dx in (20,80):d.ellipse((xx+dx-10,800,xx+dx+10,820),fill=INK)
            arrow(d,(960,700),(1300,745))
        elif kind=='stranded':
            text(d,(150,390),'Vehicle unloading does not mean a quick return to sea',34)
            d.arc((1340,510,1640,810),-90,-90+max(1,int(330*p)),fill=ACCENT,width=14)
        elif kind=='refloat':arrow(d,(650,900),(650+int(400*p),900))
        text(d,(140,960),'Conceptual tidal cycle; hull, beach and water levels are illustrative',26)
    else:
        d.rectangle((100,690,1820,930),fill=WATER)
        d.rectangle((100,850,450,930),fill='#c6b99a')
        ship(d,1250,625,True)
        labels={'liberty':'LIBERTY SHIPS: ANCHOR OFFSHORE','transfer':'EVERY CRATE NEEDS ANOTHER TRANSFER','gale':'A GALE CAN HALT BEACH UNLOADING'}
        text(d,(150,275),labels[kind],48,ACCENT)
        if kind=='liberty':
            text(d,(150,375),'10,000 tons of cargo | two miles offshore',38)
            arrow(d,(460,820),(1600,820));arrow(d,(1600,820),(460,820))
        elif kind=='transfer':
            xx=1060-int(450*p)
            d.polygon([(xx,740),(xx+190,740),(xx+160,780),(xx+25,780)],fill=INK)
            cy=510+int(180*p);d.rectangle((1140,cy,1190,cy+45),fill=ACCENT)
            d.line((1165,465,1165,cy),fill=INK,width=3)
            text(d,(150,380),'Barges and DUKW amphibious trucks',38)
        else:
            for k in range(3):
                pts=[(x,720+k*52+int(15*math.sin(x/100-p*6))) for x in range(470,1800,8)]
                d.line(pts,fill='#537984',width=5)
            text(d,(150,380),'Open swells interrupt the supply chain',38)
            d.line((640,810,640+int(600*p),810),fill=ACCENT,width=8)
        text(d,(140,960),'Schematic cargo flow; vessel silhouettes and distances are not to scale',26)
    return im

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--vo',type=Path);a.add_argument('--render',action='store_true');args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    records=[]
    for i,((start,kind),(end,_)) in enumerate(zip(SCENES,SCENES[1:])):
        first,last=round(start*25),round(end*25);key=f'beach_{i+1:02}_{kind}_v09';frame(kind,.9).save(args.out/(key+'.jpg'),quality=92)
        r=dict(scene=kind,start_s=first/25,end_s=last/25,film_start_frame=first,film_end_frame=last,frames=last-first,source='J2991 claim 8 / S2 S3 S5',status='DRAFT_NOT_QUALITY_APPROVED')
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
        listing=args.out/'concat.txt';listing.write_text(''.join("file '"+r['file']+"'\n" for r in records));silent=args.out/'beach_sequence_silent_v09.mp4'
        subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(silent)],check=True)
        if args.vo:
            target=args.out/'beach_narration_preview_v09.mp4'
            subprocess.run(['ffmpeg','-v','error','-n','-i',str(silent),'-ss',str(manifest['start_s']),'-i',str(args.vo),'-map','0:v','-map','1:a','-t',str(manifest['end_s']-manifest['start_s']),'-c:v','copy','-c:a','aac','-b:a','192k',str(target)],check=True)
            subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
            manifest['preview']=dict(file=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    (args.out/'beach_sequence_manifest_v09.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
