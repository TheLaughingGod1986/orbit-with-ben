#!/usr/bin/env python3
"""Tactical synthesis and contextual Bogue inset. Not a May action photograph."""
import hashlib,pathlib
from PIL import Image,ImageDraw
import detection_maps as dm
import convoy_maps as cm
S={
'L039':[('all','Spring 1943: the elements combine','A developing system, not an instant switch'),('reach','Longer reach','Aircraft can get farther from shore'),('radar','Radar search','Detecting a contact'),('bearing','Radio direction finding','Exploit transmissions used to organise attacks'),('escort','Escorts beside the merchantmen','The close screen remains'),('fog','Weather tests the system','Poor visibility limits air operations')],
'L049':[('carrier','Another layer of protection','Small escort carriers'),('photo','USS Bogue','Identity photograph • not a May patrol scene'),('carrier','Move the starting point','A flight deck travelling at sea'),('nearby','Nearer the supported ships','Carrier aircraft need not fly from a distant shore')]
}
ROOT=pathlib.Path('/Volumes/data/studio-live/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943')
PHOTO=ROOT/'03_Picture/archive/P4.jpg'
if hashlib.sha256(PHOTO.read_bytes()).hexdigest()!='6ffe77d6b667970e1a91d91f0fea06f74e4ec7c44c699e0e7d0cca0adc66558f':raise ValueError('Bogue archive hash mismatch')
P4=Image.open(PHOTO).convert('RGB')
def render(row,t,duration):
 mode,heading,note=S[row['line_id']][int(row['shot_id'].split('.')[1])-1];u=min(1,max(0,t/max(.01,duration)))
 im=cm.BG.copy();d=ImageDraw.Draw(im);dm.text(d,(90,55),heading,55);dm.text(d,(94,140),note,29)
 def label(x,y,s,c=dm.PAPER,n=28):dm.text(d,(x,y),s,n,c)
 cx=1100+70*u;cy=700
 for dx,dy in [(-35,-25),(35,-25),(-35,25),(35,25)]:cm.boat(d,cx+dx,cy+dy,dm.GOLD)
 for dx in [-130,130]:cm.boat(d,cx+dx,cy,dm.BLUE)
 label(cx-65,cy+70,'Convoy')
 if row['line_id']=='L039':
  if mode in ('all','reach','radar','fog'):
   start=cm.xy(-6,55);end=(cx-100,430);dm.arrow(d,start,end,dm.GOLD);dm.plane(d,start[0]+(end[0]-start[0])*u,start[1]+(end[1]-start[1])*u)
  if mode in ('all','radar','bearing'):
   cm.boat(d,1370,470,dm.RED,True)
   if mode in ('all','radar'):dm.wave(d,(cx+130,cy-25),(1340,500),t);label(1170,340,'Radar contact',dm.BLUE)
   if mode in ('all','bearing'):dm.bearing(d,(cx-130,cy-20),(1320,450));label(450,390,'Passive bearing guides search')
  if mode=='escort':label(610,390,'The screen stays with the convoy',dm.BLUE)
  if mode=='fog':
   for x,y in [(850,420),(1030,460),(1180,400)]:d.ellipse((x-130,y-35,x+170,y+90),fill=(158,174,174))
   label(480,345,'Poor visibility',dm.PAPER)
 else:
  bx=710+70*u;cm.boat(d,bx,520,dm.BLUE);dm.plane(d,bx+120*u,400);dm.arrow(d,(bx+50,470),(cx-40,430),dm.GOLD);label(450,570,'Moving carrier base',dm.BLUE)
  if mode=='photo':
   # Native 800x519 inset: dated separately from the schematic patrol map.
   im.paste(P4,(120+int(10*u),275));d=ImageDraw.Draw(im)
   d.rectangle((105,805,1000,885),fill=dm.PAPER);label(125,820,'Bogue near Norfolk • 20 June 1943',dm.INK,28);label(125,855,'US Navy / NARA 80-G-71314 • public domain',dm.INK,24)
   label(1100,390,'Flight deck at sea',dm.GOLD)
 dm.text(d,(95,948),'SCHEMATIC • no exact tracks, ship counts, patrol radii or battle positions',26)
 dm.text(d,(95,1002),row['shot_id']+' | Natural Earth public-domain coastlines • original studio diagram',25)
 return im
