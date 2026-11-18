#!/usr/bin/env python3
"""L020–L029: aircraft conversion, archive evidence and operational organisation.
Archive images retain native pixels or are reduced; no inferred equipment callouts.
"""
import hashlib,json,pathlib
from PIL import Image,ImageDraw
import detection_maps as dm
import convoy_maps as cm
S={
'L020':[('P1','The Liberator','Aldergrove lineup • official RAF photograph'),('america','American bomber, maritime role','Built in America • adapted to patrol at sea'),('range','Into the central Atlantic','Very long range patrols'),('budget','Go, search, return','Useful patrol time matters as well as distance')],
'L021':[('fuel','Extra fuel','One part of the conversion'),('fitting','Long-range tanks took work','Official history records slow fitting'),('fitting','Assignment was not readiness','A new command did not complete a conversion'),('ready','Equipment and preparation','Making the aircraft useful at sea')],
'L022':[('radar','Another conversion','Equipment for finding submarines'),('radar','Radar helps search','An echo can guide the crew'),('fitting','Radar fitting also took time','No instant fleet-wide change'),('search','Range without detection','A vast search area • limited information'),('range','Detection without range','The search area must first be reached')],
'L023':[('P1','The conversion in photographs','Aldergrove • official RAF image CH 18035'),('P1','One aircraft family','120 Squadron and 86 Squadron Liberators'),('P1','Different radar installations','Mixed fits recorded in the photograph'),('P1','Different equipment','Do not assume every Liberator had the same fit')],
'L024':[('P2','Work between patrols','Aldergrove • April 1943'),('P2','Daily inspection','An armourer cleans a Liberator rear turret'),('P2','Ordinary maintenance mattered','Official RAF image CH 18031'),('P2','Preparation before take-off','Ground work supports the flying crew')],
'L025':[('command','John Slessor','Coastal Command • early 1943'),('command','Max Horton','Western Approaches'),('command','Two services, the same convoy','Air and naval forces • limited resources'),('priority','Where could protection do most good?','Allocate the available aircraft')],
'L026':[('conference','A daily telephone conference','Coastal Command • Western Approaches • Admiralty'),('priority','Use the latest information','Choose convoys for air protection'),('scarce','Not every convoy could be covered','Aircraft were a scarce resource'),('priority','Concentrate on threatened convoys','Allocation follows the assessed threat')],
'L027':[('allies','A shared Atlantic problem','Cooperation across national boundaries'),('allies','British, Canadian and American forces','Shared purpose • different procedures'),('washington','Washington • March 1943','Convoy arrangements and Newfoundland VLR commitments'),('allies','Cooperation was part of defence','Link the commands as well as the patrols')],
'L028':[('system','Aircraft and organisation','A machine is part of an operating system'),('equipment','Fuel and radar','Reach plus a means to search'),('system','Put the patrol in the right place','Orders • information • maintenance • trained crews'),('system','What the whole system enabled','Preparation becomes an actual patrol'),('radar','A new way to see','Detection joins the operational system')],
'L029':[('fitting','From invention to operations','A promising design still needs deployment'),('ready','Deliver, fit, use','Squadron → aircraft → working patrol'),('fitting','Delays were part of the story','Official history records delays and successes'),('ready','Paper promise is not protection','The aircraft must reach a threatened convoy')]
}
ROOT=pathlib.Path('/Volumes/data/studio-live/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943')
EDIT=pathlib.Path(__file__).resolve().parent
ASSETS={x['key']:x for x in json.loads((EDIT/'ARCHIVE_HARVEST.json').read_text())}
PHOTOS={}
for key in ('P1','P2'):
 a=ASSETS[key];path=pathlib.Path(a['file'])
 if hashlib.sha256(path.read_bytes()).hexdigest()!=a['sha256']:raise ValueError('Archive hash mismatch')
 PHOTOS[key]=Image.open(path).convert('RGB')
def render(row,t,duration):
 mode,heading,note=S[row['line_id']][int(row['shot_id'].split('.')[1])-1];u=min(1,max(0,t/max(.01,duration)))
 im=Image.new('RGB',(1920,1080),dm.PAPER) if mode in PHOTOS else cm.BG.copy();d=ImageDraw.Draw(im)
 dm.text(d,(90,55),heading,55);dm.text(d,(94,140),note,29)
 def label(x,y,s,c=dm.PAPER,n=28):dm.text(d,(x,y),s,n,c)
 if mode in PHOTOS:
  photo=PHOTOS[mode].copy();photo.thumbnail((1120,720));x=100+int(15*u);y=225+(720-photo.height)//2;im.paste(photo,(x,y));d=ImageDraw.Draw(im)
  lines=['IWM / Air Ministry',ASSETS[mode]['id'],'Official RAF photograph','Crown copyright expired']
  if mode=='P1':lines+=['Aldergrove, circa 1943','120 Sqn Mark IIIs','86 Sqn Mark V','Mixed radar fits']
  else:lines+=['Aldergrove, April 1943','Armourer cleaning turret','Daily inspection']
  for i,s in enumerate(lines):label(1280,280+i*65,s,dm.INK,28)
  dm.text(d,(95,968),'IWM / Air Ministry official photograph • Crown copyright expired',26)
 else:
  cx=1000+60*u;cy=700
  for dx,dy in [(-35,-25),(35,-25),(-35,25),(35,25)]:cm.boat(d,cx+dx,cy+dy,dm.GOLD)
  for dx in [-125,125]:cm.boat(d,cx+dx,cy,dm.BLUE)
  label(cx-60,cy+60,'Convoy');dm.arrow(d,(cx+180,cy),(1630,cy),dm.GOLD)
  if mode in ('range','search','radar','budget','fuel','ready','equipment'):
   start=cm.xy(-6,55);end=(cx-60,470);dm.arrow(d,start,end,dm.GOLD);dm.plane(d,start[0]+(end[0]-start[0])*u,start[1]+(end[1]-start[1])*u)
  if mode in ('radar','equipment'):
   cm.boat(d,1250,540,dm.RED,True);dm.wave(d,(1040,460),(1200,530),t);label(450,350,'Equipment: detect a contact',dm.GOLD)
  if mode=='fuel':label(450,350,'Fuel allocation extends useful reach',dm.GOLD);label(450,405,'No tank position or capacity inferred')
  if mode in ('fitting','ready','system','equipment','budget'):
   names={'fitting':['Deliver','Fit','Check','Deploy'],'ready':['Equipment','Crew','Readiness','Patrol'],'system':['Prepare','Inform','Direct','Patrol'],'equipment':['Fuel','Radar','Crew','Patrol'],'budget':['Outward','Search','Return']}[mode]
   for i,s in enumerate(names):
    x=240+i*(1450//len(names));d.rounded_rectangle((x,315,x+320,415),radius=8,fill=dm.PAPER);dm.text(d,(x+25,345),s,32)
  if mode=='search':label(470,350,'Reach alone does not identify a target',dm.GOLD)
  if mode in ('command','conference','priority','scarce'):
   names=['Coastal Command','Western Approaches','Admiralty intelligence']
   for i,s in enumerate(names):
    x=180+i*555;d.rounded_rectangle((x,310,x+520,420),radius=8,fill=dm.PAPER);dm.text(d,(x+18,345),s,30)
    if i<2:dm.arrow(d,(x+522,365),(x+550,365),dm.GOLD)
   if mode=='conference':label(630,465,'Telephone coordination',dm.GOLD)
   if mode in ('priority','scarce'):
    cm.boat(d,550,590,dm.GOLD);label(420,640,'Other convoy');dm.arrow(d,(950,460),(cx,630),dm.GOLD);label(1100,555,'Assessed threat',dm.GOLD)
  if mode in ('america','allies','washington'):
   names=['United States','Canada','Britain'] if mode!='washington' else ['Washington','Newfoundland','Atlantic convoys']
   for i,s in enumerate(names):
    x=240+i*520;d.rounded_rectangle((x,320,x+460,430),radius=8,fill=dm.PAPER);dm.text(d,(x+25,352),s,31)
    if i<2:dm.arrow(d,(x+462,375),(x+515,375),dm.GOLD)
   label(530,490,'Cooperation / allocation links, not a flight route')
  dm.text(d,(95,948),'SCHEMATIC • no exact tracks, ship counts, patrol radii or equipment dimensions',26)
 dm.text(d,(95,1010),row['shot_id']+' | Original Field Order History picture • archive rights in provenance log',24)
 return im
if __name__=='__main__':dm.SPECS=S;dm.render=render;dm.main()
