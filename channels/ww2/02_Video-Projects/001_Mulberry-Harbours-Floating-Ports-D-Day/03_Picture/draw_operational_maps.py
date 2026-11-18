"""Own schematic endpoint maps for WW2:001. Never historical tracks or surveys.

Geography: Natural Earth public-domain countries, recorded by draw_channel_map.py.
Endpoints are approximate town coordinates. Labels and connections need review.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
W,H=1920,1080
SEA,LAND,INK,RED='#c1d6db','#eee9dd','#243c42','#ae4c2d'
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
POINTS={'Cherbourg':(-1.62,49.64),'Le Havre':(.11,49.49),'Boulogne':(1.61,50.73),
'Calais':(1.85,50.95),'Arromanches':(-.62,49.34),'Omaha':(-.87,49.37),
'Selsey':(-.79,50.73),'Dungeness':(.97,50.92),'Isle of Wight':(-1.30,50.65),'Antwerp':(4.40,51.22)}
MAPS={
'G1':{'title':'PORTS AND THE OPEN BEACHES','subtitle':'The invasion supply problem | Normandy, June 1944',
'points':['Cherbourg','Le Havre','Boulogne','Calais','Arromanches','Omaha'],'routes':[],
'note':'Port locations and landing areas only; no fortification sectors reconstructed'},
'G11a':{'title':'WAITING OFF THE SOUTH COAST','subtitle':'Phoenix staging locations | April-May 1944',
'points':['Selsey','Dungeness'],'routes':[],
'note':'Town locations indicate staging areas; no exact underwater parking ground implied'},
'G13':{'title':'FUEL UNDER THE CHANNEL','subtitle':'Operation PLUTO | Bambi and Dumbo endpoint connections',
'points':['Isle of Wight','Cherbourg','Dungeness','Boulogne'],
'routes':[('Isle of Wight','Cherbourg'),('Dungeness','Boulogne')],
'note':'Schematic endpoint connections, not surveyed pipeline tracks or simultaneous commissioning'},
'G15':{'title':'FROM NORMANDY TO ANTWERP','subtitle':'Supply ports | Antwerp opened to shipping on 28 November 1944',
'points':['Arromanches','Cherbourg','Antwerp'],'routes':[],
'note':'Port locations only; no troop movements, supply routes or Scheldt clearance boundary implied'}
}

def text(d,xy,s,size=32,c=INK):d.text(xy,s,font=ImageFont.truetype(FONT,size),fill=c,stroke_width=2,stroke_fill=LAND)
def xy(lon,lat):return (100+(lon+3.1)*220,220+(52.1-lat)*225)

def render(geo,gid,p):
 spec=MAPS[gid];im=Image.new('RGB',(W,H),SEA);d=ImageDraw.Draw(im)
 for f in geo['features']:
  g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
  for poly in polys:
   ring=poly[0]
   if any(-5<pt[0]<7 and 48<pt[1]<54 for pt in ring):d.polygon([xy(*pt[:2]) for pt in ring],fill=LAND,outline='#809498',width=2)
 # Schematic routes progressively draw. Always communicate their limitations.
 for a,b in spec['routes']:
  a=xy(*POINTS[a]);b=xy(*POINTS[b]);q=(a[0]+(b[0]-a[0])*p,a[1]+(b[1]-a[1])*p)
  d.line((a,q),fill=RED,width=7)
 offsets={'Omaha':(-180,20),'Arromanches':(10,45),'Cherbourg':(-190,-40),'Le Havre':(5,10),
 'Calais':(35,-30),'Boulogne':(-170,20),'Dungeness':(15,-45),'Selsey':(-120,-70),
 'Isle of Wight':(-250,30),'Antwerp':(-140,18)}
 for i,n in enumerate(spec['points']):
  if not spec['routes'] and p<i/max(1,len(spec['points'])):continue
  x,y=xy(*POINTS[n]);d.ellipse((x-9,y-9,x+9,y+9),fill=RED)
  dx,dy=offsets[n];text(d,(x+dx,y+dy),n,31)
 d.rectangle((0,0,W,195),fill=LAND);text(d,(75,38),spec['title'],54);text(d,(75,125),spec['subtitle'],29)
 text(d,(575,320),'BRITAIN',38);text(d,(995,860),'FRANCE',38)
 text(d,(500,660),'ENGLISH CHANNEL',30,'#607b7d')
 d.rectangle((0,970,W,H),fill=LAND)
 text(d,(65,985),spec['note'],23)
 text(d,(65,1030),'Own map | Natural Earth public-domain geography | Approximate endpoints',23)
 return im

def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--geography',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--video',action='store_true');args=a.parse_args()
 args.out.mkdir(parents=True,exist_ok=True);geo=json.loads(args.geography.read_text());manifest=[]
 for gid in MAPS:
  files=[]
  for label,p in [('start',0),('mid',.5),('end',1)]:
   f=args.out/f'{gid}_{label}_draft_v01.png';render(geo,gid,p).save(f);files.append(f)
  if args.video:
   f=args.out/f'{gid}_draft_v01.mp4'
   proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','25','-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(f)],stdin=subprocess.PIPE)
   for n in range(300):proc.stdin.write(render(geo,gid,min(1,n/225)).tobytes())
   proc.stdin.close()
   if proc.wait():raise RuntimeError(gid+' encode failed')
   files.append(f)
  manifest.append({'graphic':gid,'status':'DRAFT_REVIEW_REQUIRED','geography':'Natural Earth public domain','endpoints':{n:POINTS[n] for n in MAPS[gid]['points']},'spec':MAPS[gid],'files':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]})
 (args.out/'operational_maps_manifest_v01.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
