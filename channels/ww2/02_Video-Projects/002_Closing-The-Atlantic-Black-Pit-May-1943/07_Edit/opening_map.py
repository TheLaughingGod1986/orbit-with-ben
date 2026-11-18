#!/usr/bin/env python3
"""Render L001 opening schematic: convoy continues; shore aircraft turns back.
No patrol-radius claim, exact convoy track, or historical ship-count claim.
"""
import argparse,hashlib,json,math,pathlib,subprocess
from PIL import Image,ImageDraw,ImageFont
URL='https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson'
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--seconds',type=float,default=24);p.add_argument('--video',action='store_true');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 coast=a.out/'ne_110m_land.geojson'
 if not coast.exists():coast.write_bytes(subprocess.check_output(['curl','--fail','--silent','--show-error','--location','--max-time','40',URL]))
 geo=json.loads(coast.read_text());W,H=1920,1080
 def xy(lon,lat):return ((lon+85)/100*W,(75-lat)/45*H)
 bg=Image.new('RGB',(W,H),(40,64,76));d=ImageDraw.Draw(bg)
 for lon in range(-80,20,10):
  x,_=xy(lon,40);d.line((x,0,x,H),fill=(58,80,88),width=1)
 for lat in range(30,80,5):
  _,y=xy(-40,lat);d.line((0,y,W,y),fill=(58,80,88),width=1)
 for f in geo['features']:
  polys=f['geometry']['coordinates'];polys=[polys] if f['geometry']['type']=='Polygon' else polys
  for poly in polys:
   for k,ring in enumerate(poly):d.polygon([xy(*v[:2]) for v in ring],fill=(177,177,152) if k==0 else (40,64,76))
 font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',34);small=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',24);title=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',55)
 for text,lon,lat in [('NEWFOUNDLAND',-66,47),('ICELAND',-25,67),('BRITAIN',-6,57)]:d.text(xy(lon,lat),text,font=small,fill=(249,242,218))
 d.text((80,65),'THE GAP IN THE SKY',font=title,fill=(249,242,218));d.text((82,139),'North Atlantic • Spring 1943',font=font,fill=(216,209,183))
 d.text((80,1000),'SCHEMATIC • routes and symbols are illustrative; no scale of patrol reach',font=small,fill=(239,233,212))
 def frame(t):
  im=bg.copy();dr=ImageDraw.Draw(im);u=min(1,max(0,t/a.seconds));cx,cy=xy(-47+11*u,49+u)
  # Three symbolic merchants and two escorts, explicitly schematic, always retained.
  for dx,dy in [(-30,-15),(0,0),(30,15)]:
   x,y=cx+dx,cy+dy;dr.polygon([(x-12,y-5),(x+13,y-5),(x+20,y),(x+13,y+5),(x-12,y+5)],fill=(241,229,181))
  for dx,dy in [(-45,40),(42,-35)]:
   x,y=cx+dx,cy+dy;dr.polygon([(x-15,y-4),(x+20,y),(x-15,y+4)],fill=(150,207,214))
  dr.text((cx-90,cy+72),'Convoy + escorts',font=small,fill=(249,242,218))
  q=min(t/9.92,1);lon=-58+14*q if t<9.92 else -44-14*min((t-9.92)/8,1);x,y=xy(lon,53)
  dr.line([xy(-58,53),xy(-44,53)],fill=(136,171,176),width=3)
  direction=1 if t<9.92 else -1
  dr.polygon([(x+20*direction,y),(x-10*direction,y-5),(x-5*direction,y-22),(x-14*direction,y-22),(x-17*direction,y-4),(x-28*direction,y-8),(x-28*direction,y+8),(x-17*direction,y+4),(x-14*direction,y+22),(x-5*direction,y+22),(x-10*direction,y+5)],fill=(244,219,144))
  dr.text((520,395),'Shore aircraft turns back' if t>=9.92 else 'Shore-based air patrol',font=small,fill=(244,219,144))
  return im
 for t in [0,8,16,23]:frame(min(t,a.seconds)).save(a.out/f'opening_{t:02d}s.jpg',quality=93)
 if a.video:
  proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate','25','-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(a.out/'M001_opening_draft_v01.mp4')],stdin=subprocess.PIPE)
  for n in range(round(a.seconds*25)):proc.stdin.write(frame(n/25).tobytes())
  proc.stdin.close()
  if proc.wait():raise RuntimeError('ffmpeg failed')
 (a.out/'PROVENANCE.json').write_text(json.dumps({'data_url':URL,'sha256':hashlib.sha256(coast.read_bytes()).hexdigest(),'terms':'https://www.naturalearthdata.com/about/terms-of-use/','licence':'Natural Earth public domain','state':'draft; geographic projection and timing need picture review','depiction':'Symbolic eastbound convoy with escorts; illustrative shore aircraft return; no exact historical track, patrol radius or ship count'},indent=2)+'\n')
 print(a.out)
if __name__=='__main__':main()
