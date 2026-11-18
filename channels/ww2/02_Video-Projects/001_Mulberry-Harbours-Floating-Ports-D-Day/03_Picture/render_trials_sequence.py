"""S15-S19: original narration-timed trial and harbour-component diagrams.
Inherits J2991 S5/S6; no surveyed layout or new historical claims.
"""
import argparse,hashlib,json,math,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
from draw_engineering import W,H,PAPER,INK,WATER,ACCENT,text,arrow,harbour
from draw_remaining import trials
SCENES=[(454.96,'lochner'),(461.62,'energy'),(465.76,'bombardon'),(472.8,'ballast'),(476.88,'rows'),(483.98,'test'),(492.62,'conditions'),(499.08,'prototypes'),(512.26,'gale'),(519.3,'scour'),(523.8,'tilt'),(529.16,'whale'),(536.9,'anchor'),(540.28,'fluke'),(547.52,'holding'),(553.36,'quebec'),(562.62,'approval'),(572.86,'a'),(576.84,'b'),(583.26,'deadline'),(588.52,'layers'),(592.22,'outer'),(599.62,'phoenix'),(612.44,'gooseberries'),(619.28,'spud'),(625.36,'roadway'),(629.86,'end')]

def frame(kind,p):
    if kind in ('prototypes','gale','scour','tilt','whale'):
        im=trials(p);d=ImageDraw.Draw(im)
        d.rectangle((75,210,1840,320),fill=PAPER)
        label={'prototypes':'FULL-SCALE PROTOTYPES | SUMMER 1943','gale':'AUGUST 1943: A SUMMER GALE','scour':'SAND SCOURED FROM UNDER FIXED HIPPOS','tilt':'PIERS TILTED; CROCODILE SPANS DISLODGED','whale':'WHALE ROADWAY SURVIVED UNDAMAGED'}[kind]
        text(d,(120,235),label,40,ACCENT)
        return im
    if kind in ('layers','outer','phoenix','gooseberries','spud','roadway'):
        value={'layers':0,'outer':.12,'phoenix':.3,'gooseberries':.5,'spud':.7,'roadway':1}[kind]
        im=harbour(value);d=ImageDraw.Draw(im)
        # One active component per sentence, without implying measured layout.
        d.rectangle((75,215,1825,315),fill=WATER)
        labels={'layers':'FIVE INTERLOCKING COMPONENTS','outer':'OUTER SHELTER: TWO LINES OF BOMBARDONS','phoenix':'THE MAIN WALL: PHOENIX CAISSONS','gooseberries':'SHALLOWER WATER: SCUTTLED BLOCKSHIPS','spud':'INSIDE: FLOATING SPUD PIERHEADS','roadway':'WHALE ROADWAYS LINK PIERHEADS TO THE BEACH'}
        text(d,(115,250),labels[kind],34,ACCENT)
        d.line((130,915,130+int(1200*p),915),fill=ACCENT,width=5)
        return im
    im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
    text(d,(80,45),'FROM EXPERIMENT TO INVASION HARBOUR',49)
    text(d,(80,125),'Own explanatory illustration | Not an operational reconstruction or technical plan',28)
    d.line((80,190,1840,190),fill=INK,width=2)
    text(d,(80,1008),'Inherited sources: J2991 S5 (ICE, 1948); S6 (Hartcup, Code Name Mulberry)',25)
    cards={'lochner':('COMMANDER ROBERT LOCHNER','Admiralty | The outer sea wall'),
       'test':('GARLIESTON, WIGTOWN BAY','Secret experimental port | Southwest Scotland'),
       'conditions':('THE CONDITIONS HAD TO MATCH','Tides, mudflats and gales'),
       'quebec':('THE QUEBEC CONFERENCE','Churchill, Mountbatten and Bruce White'),
       'approval':('24 AUGUST 1943','Two portable harbours approved'),
       'a':('MULBERRY A','US First Army | Omaha Beach'),
       'b':('MULBERRY B','British Second Army | Arromanches, Gold Beach'),
       'deadline':('NINE MONTHS TO D-DAY','Not a single caisson had been poured')}
    if kind in cards:
        title,sub=cards[kind];text(d,(150,350),title,65,ACCENT);text(d,(150,480),sub,40)
        d.line((150,790,150+int(1500*p),790),fill=ACCENT,width=7)
    elif kind in ('energy','bombardon','ballast','rows'):
        d.rectangle((120,550,1800,930),fill=WATER)
        if kind=='energy':
            text(d,(150,280),'WAVE ENERGY NEAR THE SURFACE',47,ACCENT)
            for k in range(3):
                pts=[(x,550+k*45+int(26/(k+1)*math.sin(x/80-p*math.pi*2))) for x in range(150,1760,7)]
                d.line(pts,fill=INK,width=5-k)
            text(d,(150,820),'Illustrative waves; no measured energy profile',32)
        elif kind in ('bombardon','ballast'):
            # Cross-section only, no unsupported stress or stability calculation.
            d.polygon([(840,350),(1060,350),(1060,500),(1300,500),(1300,600),(1060,600),(1060,865),(840,865),(840,600),(600,600),(600,500),(840,500)],fill=INK)
            if kind=='ballast':d.rectangle((855,640,1045,850),fill=ACCENT)
            text(d,(150,250),'BOMBARDON: FLOATING STEEL CROSS' if kind=='bombardon' else 'LOWER ARM FLOODED',45,ACCENT)
            text(d,(145,920),'Conceptual section; dimensions and immersion are not drawn to scale',28)
            d.line((150,400,150+int(350*p),400),fill=ACCENT,width=6)
        else:
            text(d,(150,275),'MOORED IN DOUBLE ROWS',51,ACCENT)
            for y in (630,790):
                for x in range(250,1600,270):d.rounded_rectangle((x,y,x+180,y+35),radius=12,fill=INK)
            text(d,(150,390),'Designed to reduce an eight-foot wave',37)
            d.line((150,465,150+int(1350*p),465),fill=ACCENT,width=6)
    else:
        text(d,(150,280),'BECKETT’S KITE ANCHOR',55,ACCENT)
        if kind=='holding':
            text(d,(180,450),'30 TONS',100,ACCENT)
            text(d,(180,580),'Holding tension stated for the kite anchor',39)
            text(d,(180,735),'Three-ton conventional anchors dragged',39)
            text(d,(180,865),'Anchor mass and holding tension are different quantities',30)
            d.line((180,940,180+int(1400*p),940),fill=ACCENT,width=6)
        else:
            d.rectangle((100,780,1820,940),fill='#b8ac91')
            y=660+int(110*p) if kind=='fluke' else 660
            d.polygon([(750,y),(1020,y-75),(1170,y+15),(900,y+90)],outline=INK,fill='#93a5a5')
            d.line((750,y,900,y+90,1020,y-75,1170,y+15),fill=INK,width=7)
            arrow(d,(1170,y+15),(1500,y-120))
            text(d,(150,390),'PULL DRIVES THE FLUKE DEEPER' if kind=='fluke' else 'THE STORM TESTED THE ANCHOR',42)
            text(d,(150,950),'Conceptual anchor action, not a fabrication drawing or measured seabed section',25)
    return im

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--vo',type=Path);a.add_argument('--render',action='store_true');args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    records=[]
    for i,((start,kind),(end,_)) in enumerate(zip(SCENES,SCENES[1:])):
        first,last=round(start*25),round(end*25);key=f'trials_{i+1:02}_{kind}_v11';frame(kind,.9).save(args.out/(key+'.jpg'),quality=92)
        r=dict(scene=kind,start_s=first/25,end_s=last/25,film_start_frame=first,film_end_frame=last,frames=last-first,source='J2991 S5 S6 / inherited trials and harbour claims',status='DRAFT_NOT_QUALITY_APPROVED')
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
        listing=args.out/'concat.txt';listing.write_text(''.join("file '"+r['file']+"'\n" for r in records));silent=args.out/'trials_sequence_silent_v11.mp4'
        subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(silent)],check=True)
        if args.vo:
            target=args.out/'trials_narration_preview_v11.mp4'
            subprocess.run(['ffmpeg','-v','error','-n','-i',str(silent),'-ss',str(manifest['start_s']),'-i',str(args.vo),'-map','0:v','-map','1:a','-t',str(manifest['end_s']-manifest['start_s']),'-c:v','copy','-c:a','aac','-b:a','192k',str(target)],check=True)
            subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
            manifest['preview']=dict(file=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    (args.out/'trials_sequence_manifest_v11.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
