"""Remaining WW2:001 explanatory drafts, from the existing J2991 brief.
No surveyed topography, weapon positions, facsimile, or engineering reconstruction.
Values inherited from the existing script; final editorial review remains required.
"""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from draw_engineering import W,H,PAPER,INK,WATER,ACCENT,text,arrow

def base(title,sub,source):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im)
    text(d,(80,45),title,54);text(d,(80,125),sub,29)
    d.line((80,190,1840,190),fill=INK,width=2)
    text(d,(80,1008),'Own illustration | '+source,25)
    return im,d

def dieppe(p):
    im,d=base('DIEPPE: THE BEACH WAS A BARRIER','19 August 1942 | Conceptual obstacles, not a tactical map','J2991 SOURCES.md S7: Stacey (1955)')
    d.rectangle((100,350,1820,650),fill=WATER)
    d.rectangle((100,650,1820,890),fill='#b8ac91')
    d.polygon([(100,350),(360,350),(490,650),(100,650)],fill='#c9c8b5')
    d.polygon([(1530,350),(1820,350),(1820,650),(1430,650)],fill='#c9c8b5')
    text(d,(140,260),'WEST HEADLAND',30);text(d,(1430,260),'EAST HEADLAND',30)
    text(d,(740,425),'SEA APPROACH',36)
    d.rectangle((500,815,1410,840),fill=INK)
    text(d,(700,860),'SEA WALL',32)
    for x,y in [(630,695),(950,735),(1220,690)]:
        d.rounded_rectangle((x,y,x+90,y+35),radius=10,fill=INK)
        d.rectangle((x+25,y-18,x+65,y),fill=INK)
    if p>.25:text(d,(690,565),'SHINGLE BEACH',34)
    if p>.6:text(d,(560,930),'29 Churchill tanks landed; obstacles blocked progress',32,ACCENT)
    return im

def logistics(p):
    im,d=base('THE SUPPLIES COULD NOT WAIT','Daily planning requirements | Two stated milestones, not a time series','J2991 SOURCES.md S3: Ruppenthal (1953)')
    for i,(label,val) in enumerate([('D+14',12000),('D+30',20000)]):
        y=290+i*180;text(d,(120,y+20),label,44)
        d.rectangle((380,y,380+val*.058*p,y+100),fill=ACCENT if i else INK)
        if p>.85:text(d,(400+val*.058,y+25),f'{val:,} tons/day',34)
    d.line((200,800,1730,800),fill=INK,width=5)
    for x,label,sub in [(230,'6 JUNE','D-DAY'),(850,'27 JUNE','CHERBOURG CAPTURED'),(1540,'AUGUST','BULK CARGO RAMPS UP')]:
        d.ellipse((x-10,790,x+10,810),fill=ACCENT)
        text(d,(x-90,720),label,30);text(d,(x-120,845),sub,25)
    text(d,(200,940),'Timeline milestones are evenly spaced for readability',27)
    return im

def directive(p):
    im,d=base('PIERS FOR USE ON BEACHES','Winston Churchill | 30 May 1942','J2991 SOURCES.md S1: TNA PREM 3/216/1')
    lines=['They must float up and down with the tide.',
           'The anchor problem must be mastered.',
           'Let me have the best solution worked out.',
           "Don’t argue the matter.",
           'The difficulties will argue for themselves.']
    for i,line in enumerate(lines):
        if p>=i/7:text(d,(160,290+i*115),line,49,ACCENT if i==0 else INK)
    text(d,(160,925),'Typeset extract from the minute; not an image of the original document',29)
    return im

def trials(p):
    im,d=base('THE GARLIESTON TEST','August 1943 | Conceptual failure and flexibility; not an engineering reconstruction','J2991 SOURCES.md S5: ICE (1948); S6: Hartcup (2011)')
    for left,label in [(120,'HIPPO / CROCODILE'),(1040,'WHALE / BEETLE')]:
        text(d,(left,255),label,39)
        d.rectangle((left,520,left+740,790),fill=WATER)
        d.rectangle((left,790,left+740,820),fill='#b8ac91')
    d.rectangle((680,455+70*p,790,790),fill=INK)
    d.line((170,470,735,470+70*p),fill=ACCENT,width=18)
    text(d,(160,865),'Rigid support: scour vulnerability',31)
    pts=[]
    for i in range(5):
        x=1080+i*155;y=470+30*math.sin(i+p*math.pi*2)
        pts.append((x,y));d.rounded_rectangle((x-40,y+25,x+40,y+65),radius=16,fill=INK)
    d.line(pts,fill=ACCENT,width=16)
    text(d,(1090,865),'Floating supports: flex with waves',31)
    text(d,(120,935),'Illustrative movement only; no calculated deflection or seabed dimensions',28)
    return im

def reef(p):
    im,d=base('EXPOSURE AND SHELTER','June 1944 gale | Conceptual sections; no surveyed depths or wave simulation','J2991 SOURCES.md S2, S5: SHAEF; ICE (1948)')
    for i,(label,reef_on) in enumerate([('OMAHA | MULBERRY A',False),('ARROMANCHES | MULBERRY B',True)]):
        top=280+i*335
        text(d,(100,top-45),label,34)
        d.rectangle((100,top+70,1820,top+260),fill=WATER)
        floor=[(100,top+250),(1820,top+250)]
        if reef_on:floor=[(100,top+250),(700,top+250),(940,top+115),(1110,top+115),(1280,top+250),(1820,top+250)]
        d.polygon(floor+[(1820,top+280),(100,top+280)],fill='#a99f88')
        wave=[]
        for x in range(100,1800,4):
            amp=24 if not reef_on or x<1000 else 10
            wave.append((x,top+70+amp*math.sin(x/65-p*math.pi*4)))
        d.line(wave,fill=INK,width=5)
        d.rectangle((1680,top+30,1750,top+170),fill=ACCENT)
        if reef_on:text(d,(900,top+170),'CALVADOS REEF',29)
    text(d,(100,970),'Wave amplitude is illustrative, not a measured reduction ratio',26)
    return im

GRAPHICS={'G2':dieppe,'G3':logistics,'G5':directive,'G7':trials,'G12':reef}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--video',action='store_true');a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True);records=[]
    for gid,draw in GRAPHICS.items():
        files=[]
        for label,p in [('start',0),('mid',.5),('end',1)]:
            f=a.out/f'{gid}_{label}_draft_v01.png';draw(p).save(f);files.append(f)
        if a.video:
            f=a.out/f'{gid}_draft_v01.mp4'
            proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','25','-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(f)],stdin=subprocess.PIPE)
            for n in range(300):proc.stdin.write(draw(n/299).tobytes())
            proc.stdin.close()
            if proc.wait():raise RuntimeError(gid+' encode failed')
            files.append(f)
        records.append({'graphic':gid,'status':'DRAFT_REVIEW_REQUIRED','files':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]})
    (a.out/'remaining_graphics_manifest_v01.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':main()
