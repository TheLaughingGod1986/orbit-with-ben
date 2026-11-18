"""S10-S14 narration-timed design explanation. Original schematics, not plans.
Claims inherited from J2991 S1/S5/S6; no narration changes or new research.
"""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from draw_engineering import W,H,PAPER,INK,WATER,ACCENT,text,arrow,pier
SCENES=[(309.,'seed'),(312.44,'date'),(319.66,'title'),(323.18,'barges'),(327.72,'obstacle'),(332.44,'minute'),(334.58,'float'),(338.84,'anchor'),(342.34,'solution'),(344.8,'argue'),(346.44,'difficulties'),(350.72,'office'),(360.94,'rivals'),(365.62,'hughes'),(371.1,'hippo'),(379.46,'crocodile'),(384.74,'beckett'),(391.9,'rigid'),(396.88,'wave'),(401.78,'whale'),(407.24,'beetles'),(412.78,'open'),(421.,'torsion'),(430.,'swells'),(434.14,'spud'),(438.9,'dimensions'),(444.66,'winches'),(454.96,'end')]

def frame(kind,p):
    if kind in ('spud','dimensions','winches'):
        im=pier((1-math.cos(math.pi*p))/2);d=ImageDraw.Draw(im)
        if kind=='dimensions':
            d.rectangle((70,220,1850,315),fill=PAPER)
            text(d,(90,235),'200 × 60 feet | Four 89-foot legs',47,ACCENT)
        return im
    im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
    text(d,(80,45),'DESIGNING A PORT THAT COULD FLOAT',51)
    text(d,(80,125),'Own explanatory illustration | Not a facsimile, vessel plan or engineering reconstruction',27)
    d.line((80,190,1840,190),fill=INK,width=2)
    text(d,(80,1008),'Inherited sources: J2991 S1 (Churchill minute); S5 (ICE, 1948); S6 (Hartcup)',25)
    cards={'seed':('BEFORE DIEPPE','The solution had already been proposed'),
      'date':('30 MAY 1942','Winston Churchill → Mountbatten'),
      'title':('PIERS FOR USE ON BEACHES','A one-page minute'),
      'obstacle':('THE SAME OBSTACLE','An invasion could not wait for the tide'),
      'minute':('A SHORT DIRECTIVE','Typeset extracts follow; not the original document'),
      'office':('WAR OFFICE','Directorate of Transportation | Sir Bruce White'),
      'rivals':('EARLY 1943','Three rival designs'),
      'hughes':('HUGH IORYS HUGHES','Concrete Hippos and steel Crocodiles'),
      'beckett':('ALLAN BECKETT','A floating roadway'),
      'float':('They must float up and down','with the tide.'),
      'anchor':('The anchor problem','must be mastered.'),
      'solution':('Let me have the best','solution worked out.'),
      'argue':('Don’t argue the matter.',''),
      'difficulties':('The difficulties will argue','for themselves.')}
    if kind in cards:
        title,sub=cards[kind]
        text(d,(150,340),title,65,ACCENT);text(d,(150,465),sub,46)
        if kind in ('float','anchor','solution','argue','difficulties'):
            text(d,(150,650),'Churchill | 30 May 1942 | Extract from the minute',31)
        d.line((150,785,150+int(1550*p),785),fill=ACCENT,width=7)
        if kind=='rivals':
            for i,s in enumerate(['HIPPO / CROCODILE','WHALE / BEETLE','BOMBARDON']):text(d,(150+i*560,620),s,31)
    elif kind in ('barges','hippo','crocodile'):
        water_y=690+int(80*p) if kind=='barges' else 680
        d.rectangle((100,water_y,1820,930),fill=WATER)
        d.polygon([(100,610),(100,930),(720,930)],fill='#c6b99a')
        if kind=='barges':
            d.polygon([(700,650),(1050,650),(1010,720),(740,720)],fill=INK)
            text(d,(150,290),'BARGES ON TIDAL FLATS',55,ACCENT)
            text(d,(150,390),'Churchill’s First World War experience',36)
        else:
            d.rectangle((1410,590,1620,930),fill=INK)
            text(d,(1400,510),'HIPPO',34)
            if kind=='crocodile':
                d.line((360,580,1510,580),fill=ACCENT,width=15)
                for x in range(400,1450,140):d.line((x,580,x+70,520,x+140,580),fill=INK,width=5)
                text(d,(400,400),'CROCODILE: RIGID LATTICE BRIDGE',43,ACCENT)
            else:
                text(d,(150,290),'TOW, THEN SINK INTO POSITION',48,ACCENT)
                arrow(d,(1500,350),(1500,380+int(150*p)))
            text(d,(110,965),'Side elevation; water depth and shoreline geometry are illustrative',26)
    else:
        d.rectangle((100,630,1820,930),fill=WATER)
        labels={'rigid':'THE PROBLEM WITH A RIGID BRIDGE','wave':'ONE PONTOON RISES; THE NEXT FALLS','whale':'WHALE: A FLOATING STEEL ROADWAY','beetles':'80-FOOT SPANS ON BEETLE PONTOONS','open':'OPEN CENTRE, FLEXIBLE SIDE GIRDERS','torsion':'UP TO 40 DEGREES OF TWIST','swells':'FOLLOWING DIAGONAL SWELLS'}
        text(d,(120,275),labels[kind],46,ACCENT)
        if kind in ('open','torsion','swells'):
            # Oblique conceptual view: two side girders, no invented stress result.
            amp=70*p if kind=='torsion' else 45*math.sin(p*math.pi)
            for offset in (0,160):
                pts=[(300,590+offset),(1500,590+offset+(amp if offset==0 else -amp))]
                d.line(pts,fill=INK,width=18)
            for i in range(7):
                x=300+i*200;dy=amp*i/6
                d.line((x,590+dy,x,750-dy),fill='#748b8f',width=5)
            text(d,(400,870),'Conceptual torsion; no measured deflection drawn',31)
        else:
            pts=[]
            for i in range(6):
                x=240+i*280;y=590+45*math.sin(i+p*math.pi*2)
                pts.append((x,y));d.rounded_rectangle((x-65,y+35,x+65,y+95),radius=18,fill=INK)
            if kind=='rigid':d.line((240,590,1640,590),fill=ACCENT,width=16)
            else:d.line(pts,fill=ACCENT,width=16)
            if kind=='beetles':text(d,(500,860),'BEETLES SUPPORT THE ROADWAY',38)
            else:text(d,(250,860),'Schematic wave motion; no calculated loading shown',30)
    return im

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--vo',type=Path);a.add_argument('--render',action='store_true');args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    records=[]
    for i,((start,kind),(end,_)) in enumerate(zip(SCENES,SCENES[1:])):
        first,last=round(start*25),round(end*25);key=f'design_{i+1:02}_{kind}_v10';frame(kind,.9).save(args.out/(key+'.jpg'),quality=92)
        r=dict(scene=kind,start_s=first/25,end_s=last/25,film_start_frame=first,film_end_frame=last,frames=last-first,source='J2991 S1 S5 S6 / inherited design claims',status='DRAFT_NOT_QUALITY_APPROVED')
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
        listing=args.out/'concat.txt';listing.write_text(''.join("file '"+r['file']+"'\n" for r in records));silent=args.out/'design_sequence_silent_v10.mp4'
        subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(silent)],check=True)
        if args.vo:
            target=args.out/'design_narration_preview_v10.mp4'
            subprocess.run(['ffmpeg','-v','error','-n','-i',str(silent),'-ss',str(manifest['start_s']),'-i',str(args.vo),'-map','0:v','-map','1:a','-t',str(manifest['end_s']-manifest['start_s']),'-c:v','copy','-c:a','aac','-b:a','192k',str(target)],check=True)
            subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
            manifest['preview']=dict(file=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    (args.out/'design_sequence_manifest_v10.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
