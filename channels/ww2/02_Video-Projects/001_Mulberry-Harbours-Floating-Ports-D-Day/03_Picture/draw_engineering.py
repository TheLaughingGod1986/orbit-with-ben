"""Own WW2:001 teaching schematics. Drafts for review, never surveyed plans.

Values follow J2991 SCRIPT.md/SOURCES.md, S5 (ICE 1948), pending final review.
Render with --out <scratch folder> [--video]. No archive images or paid calls.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
PAPER, INK, WATER, ACCENT = '#eee9dd', '#243c42', '#c1d6db', '#ae4c2d'
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'

def text(d, xy, value, size=34, fill=INK):
    d.text(xy, value, font=ImageFont.truetype(FONT, size), fill=fill)

def canvas(title, subtitle):
    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    text(d, (80, 50), title, 58)
    text(d, (80, 135), subtitle, 30)
    d.line((80, 200, 1840, 200), fill=INK, width=2)
    text(d, (80, 1008), 'Own illustration | Schematic, not to scale | J2991: ICE, The Civil Engineer in War, vol. 2 (1948)', 25)
    return im, d

def arrow(d, a, b, colour=ACCENT, width=7):
    d.line((a,b), fill=colour, width=width)
    t=math.atan2(b[1]-a[1], b[0]-a[0])
    d.polygon([b,(b[0]-24*math.cos(t-.45),b[1]-24*math.sin(t-.45)),
               (b[0]-24*math.cos(t+.45),b[1]-24*math.sin(t+.45))],fill=colour)

def tide(p):
    im,d=canvas('THE TIDE CHANGES THE SHORE', 'A fixed quay cannot follow the changing water level')
    # Schematic beach slope: higher water reaches farther inland.
    water_y=780-260*p
    d.rectangle((240,water_y,1760,930),fill=WATER)
    d.polygon([(240,930),(240,440),(1480,930)], fill='#c7ba99')
    d.line((240,440,1480,930),fill=INK,width=5)
    for y,label in [(520,'HIGH WATER'),(780,'LOW WATER')]:
        d.line((1210,y,1770,y),fill='#77969c',width=3)
        text(d,(1430,y-45),label,28)
    arrow(d,(1800,520),(1800,780));arrow(d,(1800,780),(1800,520))
    text(d,(1500,630),'24 feet',46,ACCENT)
    text(d,(330,360),'SHORE',34)
    text(d,(1100,870),'SEA',34)
    # Moving intersection is the actual displayed shoreline.
    x=240+(water_y-440)*1240/490
    d.ellipse((x-13,water_y-13,x+13,water_y+13),fill=ACCENT)
    text(d,(80,245),'Spring tidal range in the narration; no beach gradient implied',30)
    return im

def pier(p):
    im,d=canvas('A PIER THAT FOLLOWS THE TIDE', 'Spud pierhead rises on fixed legs; Whale roadway links it to shore')
    water_y=740-150*p
    d.rectangle((80,water_y,1835,930),fill=WATER)
    d.polygon([(80,470),(340,470),(600,930),(80,930)],fill='#c7ba99')
    text(d,(90,390),'SHORE',30)
    d.rectangle((80,918,1835,940),fill='#978d78')
    # Side elevation: only the two near legs are visible, of four in plan.
    for x in (1280,1650):
        d.rectangle((x-13,340,x+13,918),fill=INK)
    y=water_y-45
    d.rounded_rectangle((1180,y,1740,y+86),radius=12,fill=ACCENT)
    text(d,(1360,y+19),'SPUD',32,'#ffffff')
    # Continuous hinged roadway, with floating supports.
    points=[(320,480),(600,y),(790,y),(980,y),(1180,y)]
    for x,yy in points[1:-1]:
        d.rounded_rectangle((x-60,water_y-15,x+60,water_y+45),radius=20,fill='#6d8589')
        d.line((x,yy,x,water_y-15),fill=INK,width=10)
    for x,yy in points:
        d.ellipse((x-8,yy-8,x+8,yy+8),fill=ACCENT)
    d.line(points,fill=INK,width=18)
    text(d,(555,350),'HINGED WHALE SPANS',34)
    text(d,(690,830),'BEETLE PONTOONS',30)
    arrow(d,(860,820),(980,water_y+45),INK,4)
    text(d,(1230,270),'FIXED LEGS',30)
    arrow(d,(1450,315),(1650,370),INK,4)
    text(d,(90,965),'Side view: two of the four legs shown',26)
    return im

def harbour(p):
    im,d=canvas('LAYERS OF SHELTER', 'Mulberry components: a conceptual layout, not a surveyed harbour plan')
    d.rectangle((80,245,1840,930),fill=WATER)
    d.rectangle((80,865,1840,930),fill='#c7ba99')
    text(d,(1500,880),'SHORE',30)
    text(d,(1500,265),'OPEN SEA',30)
    # Component positions are explanatory only; do not imply measured distances.
    layers=[(0,'BOMBARDON',330),(1,'PHOENIX',450),(2,'GOOSEBERRY',565)]
    for i,label,y in layers:
        active=p >= i/5
        colour=INK if active else '#94adb0'
        for x in range(180,1380,180):
            if label=='BOMBARDON':
                d.rounded_rectangle((x,y,x+120,y+20),radius=10,fill=colour)
            elif label=='PHOENIX':
                d.rectangle((x,y,x+155,y+35),fill=colour)
            else:
                d.polygon([(x,y),(x+145,y),(x+120,y+30),(x+25,y+30)],fill=colour)
        text(d,(1430,y-5),label,30,colour)
    if p>=.6:
        d.rectangle((680,675,970,725),fill=ACCENT)
        text(d,(1060,685),'SPUD PIERHEAD',30)
        d.line((980,705,1040,705),fill=INK,width=3)
    if p>=.8:
        d.line((815,725,815,865),fill=INK,width=18)
        text(d,(1060,790),'WHALE ROADWAY',30)
        d.line((830,810,1040,810),fill=INK,width=3)
    text(d,(100,960),'Not concentric rings; positions and spacing vary between harbours',26)
    return im

def phoenix(p):
    im,d=canvas('A CONCRETE GIANT THAT COULD FLOAT', 'Type A1 Phoenix caisson | Side elevation, simplified')
    x,y,scale=240,420,6
    length,height=204*scale,60*scale
    d.rectangle((x,y,x+length,y+height),fill='#b3b8b2',outline=INK,width=6)
    # Outline only: internal partition arrangement is not reconstructed.
    for xx in range(x+40,int(x+length),100):
        d.line((xx,y+20,xx,y+height-20),fill='#9da49e',width=2)
    d.rectangle((80,740,1840,930),fill=WATER)
    d.line((80,740,1840,740),fill='#6b929a',width=3)
    text(d,(80,890),'Illustrative waterline; no loading condition implied',27)
    arrow(d,(x,y-65),(x+length,y-65));arrow(d,(x+length,y-65),(x,y-65))
    text(d,(700,y-125),'204 feet long',43)
    arrow(d,(1640,y),(1640,y+height));arrow(d,(1640,y+height),(1640,y))
    text(d,(1680,y+145),'60 ft',40)
    if p>.25: text(d,(480,520),'6,044 TONS',66,INK)
    if p>.6: text(d,(480,615),'Type A1 | largest class',34,INK)
    text(d,(80,255),'Dimensions and stated tonnage follow the narration',30)
    return im


def industry(p):
    im,d=canvas('BUILDING THE HARBOURS', 'Britain | Construction mobilisation, 1943-1944')
    stats=[('45,000','workers'),('300+','firms'),('600,000','cubic yards of concrete'),
           ('31,000','tons of reinforcing steel')]
    for i,(number,label) in enumerate(stats):
        x=120+(i%2)*900;y=300+(i//2)*300
        visible=p>=i/5
        c=ACCENT if visible else '#9e9d94'
        text(d,(x,y),number,90,c)
        text(d,(x,y+120),label,36,INK)
    text(d,(120,925),'Materials and workforce totals, not a month-by-month production series',28)
    return im


def cargo(p):
    im,d=canvas('CARGO THROUGH MULBERRY B', 'Arromanches | July 1944 daily average against design target')
    # Do not invent a monthly time series from two summary values.
    x0=530;scale=.15
    for i,(label,value,c) in enumerate([('Design target',6000,'#7a9297'),('July average',6765,ACCENT)]):
        y=380+i*230
        text(d,(100,y+20),label,40)
        d.rectangle((x0,y,x0+value*scale*p,y+110),fill=c)
        if p>.85:text(d,(x0+value*scale+25,y+24),f'{value:,}',46,c)
    text(d,(530,865),'Tons per day | Same scale for both bars',32)
    # This graphic uses S3, not the engineering source used by other panels.
    d.rectangle((0,995,W,H),fill=PAPER)
    text(d,(80,1008),'Own chart | Ruppenthal, Logistical Support of the Armies, vol. I (1953) | J2991 SOURCES.md S3',25)
    return im


GRAPHICS={'G4':tide,'G6':pier,'G8':harbour,'G9':phoenix,'G10':industry,'G14':cargo}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--out',type=Path,required=True)
    a.add_argument('--video',action='store_true')
    args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    records=[]
    for gid,draw in GRAPHICS.items():
        paths=[]
        for name,p in [('start',0),('mid',.5),('end',1)]:
            f=args.out/f'{gid}_{name}_draft_v01.png';draw(p).save(f);paths.append(f)
        if args.video:
            f=args.out/f'{gid}_draft_v01.mp4'
            cmd=['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}',
                 '-r','25','-i','-','-an','-c:v','libx264','-preset','fast','-crf','18',
                 '-pix_fmt','yuv420p',str(f)]
            proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
            for n in range(300):
                # High-low-high water, gentle twelve-second teaching loop.
                p=(1-math.cos(2*math.pi*n/299))/2 if gid in ('G4','G6') else min(1,n/240)
                proc.stdin.write(draw(p).tobytes())
            proc.stdin.close()
            if proc.wait(): raise RuntimeError(f'{gid} encode failed')
            paths.append(f)
        records.append({'graphic':gid,'status':'DRAFT_REVIEW_REQUIRED','source':('J2991 SOURCES.md S3; Ruppenthal 1953' if gid=='G14' else 'J2991 SOURCES.md S5; ICE 1948'),
                        'files':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in paths]})
    (args.out/'engineering_manifest_v01.json').write_text(json.dumps(records,indent=2)+'\n')

if __name__=='__main__':main()
