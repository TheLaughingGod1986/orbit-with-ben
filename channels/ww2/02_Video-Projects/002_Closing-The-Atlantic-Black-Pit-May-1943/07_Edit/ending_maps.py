#!/usr/bin/env python3
"""Original ending diagrams L050–L058, authored to the locked spoken sentences.
All routes, search sectors and symbols are qualitative. No historical positions,
loss tally, continuous coverage, equipment dimensions or numerical range claim.
"""
import math
from PIL import Image,ImageDraw
import detection_maps as dm
import convoy_maps as cm
S={
'L050': [('combined','Two approaches, one passage','Shore patrols and carrier aircraft'),('shore','Reach from the edges','Land-based patrol aircraft'),('carrier','A moving starting point','Carrier aircraft begin at sea'),('escort','Beside the merchant ships','Surface escorts remain with the convoy'),('combined','Fewer long unprotected passages','Search remains intermittent')],
'L051': [('withdraw','24 May 1943','Dönitz orders withdrawal from the North Atlantic convoy battle'),('withdraw','The offensive became unsustainable','Losses changed the operational decision'),('date','Black May','A decisive reversal in the convoy battle'),('withdraw','Seek less dangerous areas','Broad withdrawal direction, not an exact order map')],
'L052': [('continue','The war at sea continued','May was a turning point, not the end'),('continue','Attacks and losses continued','No claim that submarine warfare stopped'),('gaps','No unbroken roof','Gaps remain between aircraft searches'),('weather','Operational limits remain','Weather • serviceability • distance'),('combined','A changed balance','Principal North Atlantic convoy routes')],
'L053': [('combined','Closing the gap','A change in operational advantage'),('gaps','No perfectly watched patch','No precise instant of complete coverage'),('combined','Aircraft, bases and carriers','More ways to reach the convoy'),('information','Used together','Escorts and information direct the response')],
'L054': [('scope','What does a loss total count?','Compare the scope before comparing the number'),('scope','Different definitions','Waters • causes • period'),('withdraw','The decision matters here','Losses forced an operational reversal'),('withdraw','The spring offensive could not continue','North Atlantic convoys • existing terms')],
'L055': [('chain','No single invention did it all','Each answered a different problem'),('radar','Finding is not delivering','Radar supplies a contact, not a cargo'),('escort','An escort has limits','A local screen cannot cover every approach'),('weather','Reach is not a sighting','A patrol can arrive and see nothing'),('chain','People made the system work','Different tasks • difficult conditions')],
'L056': [('shore','Air power changed the encounter','Pressure beyond the close escort screen'),('dive','Aircraft could break the contact','Forced dive • interrupted shadowing • possible attack'),('shore','Farther from shore','Very long range Liberator patrols'),('carrier','An airfield at sea','Escort carriers brought aircraft from another direction')],
'L057': [('arrival','Success was an arrival','Merchant ships reach Britain'),('cargo','The cargo reached its destination','Supply delivered'),('return','Another crossing could begin','Continued movement across the Atlantic'),('cargo','The strategic purpose','Britain and the Allied build-up'),('arrival','Keep the movement alive','Success did not require destroying every submarine')],
'L058': [('overview','Return to the North Atlantic','The convoy remains the centre of the story'),('turnback','At the beginning','Shore aircraft turn back while the ships continue'),('information','By the end','More ways to reach, find and bring help'),('combined','A changed encounter far from land','Aircraft • escorts • information • arrival')]
}
def render(row,t,duration):
 mode,heading,note=S[row['line_id']][int(row['shot_id'].split('.')[1])-1]
 im=cm.BG.copy();d=ImageDraw.Draw(im);dm.text(d,(90,55),heading,55);dm.text(d,(94,140),note,29)
 u=min(1,max(0,t/max(.01,duration)));cx=1000+90*u;cy=690
 def label(x,y,s,c=dm.PAPER,n=28):dm.text(d,(x,y),s,n,c)
 label(300,790,'Newfoundland');label(1210,260,'Iceland',dm.INK);label(1610,550,'Britain',dm.INK)
 # A symbolic convoy and two escorts: icons never encode historical counts.
 for dx,dy in [(-35,-25),(35,-25),(-35,25),(35,25)]:cm.boat(d,cx+dx,cy+dy,dm.GOLD)
 for dx in [-120,120]:cm.boat(d,cx+dx,cy,dm.BLUE)
 label(cx-70,cy+65,'Convoy');dm.arrow(d,(cx+180,cy),(1640,cy),dm.GOLD)
 shore=mode in ('shore','combined','information','overview','gaps','turnback')
 carrier=mode in ('carrier','combined','information','overview','gaps')
 if shore:
  start=cm.xy(-8,55);end=(cx+100,470)
  # Dashed search paths leave visible gaps; not a radius or constant roof.
  for i in range(0,10,2):
   a=i/10;b=(i+1)/10;d.line((start[0]+(end[0]-start[0])*a,start[1]+(end[1]-start[1])*a,start[0]+(end[0]-start[0])*b,start[1]+(end[1]-start[1])*b),fill=dm.GOLD,width=4)
  v=(1-abs(2*u-1)) if mode=='turnback' else u
  dm.plane(d,start[0]+(end[0]-start[0])*v,start[1]+(end[1]-start[1])*v)
  label(1320,380,'Shore patrol',dm.GOLD)
 if carrier:
  cm.boat(d,700+70*u,530,dm.BLUE);label(480,565,'Carrier: moving base',dm.BLUE)
  dm.plane(d,770+130*u,400);dm.arrow(d,(790,460),(1040,440),dm.GOLD)
 if mode in ('information','radar'):
  cm.boat(d,1320,510,dm.RED,True);dm.wave(d,(cx+120,cy-15),(1300,530),t);label(1120,350,'Radar search',dm.BLUE)
  if mode=='information':dm.bearing(d,(cx-120,cy-10),(1260,450));label(480,350,'Radio bearing guides search',dm.PAPER)
 if mode=='escort':
  dm.arrow(d,(cx+120,cy-30),(cx+240,cy-170),dm.BLUE);label(620,390,'Close screen • local response',dm.BLUE)
 if mode in ('weather','gaps','continue'):
  if mode=='weather':
   for x,y in [(850,450),(1030,490),(1170,425)]:d.ellipse((x-110,y-45,x+160,y+80),fill=(153,169,170))
   label(650,370,'Poor visibility / unavailable aircraft')
  elif mode=='gaps':label(660,360,'Searches leave gaps',dm.GOLD)
  else:cm.boat(d,1280,440,dm.RED,True);label(590,360,'Operations continue after May 1943')
 if mode in ('withdraw','date'):
  d.rounded_rectangle((370,300,1480,410),radius=12,fill=dm.PAPER);dm.text(d,(500,318),'24 MAY 1943',55)
  if mode=='withdraw':
   for x in [800,1180]:cm.boat(d,x,490,dm.RED,True);dm.arrow(d,(x,515),(x-60,600),dm.RED)
   label(420,835,'Broad change of operating area • not exact tracks',dm.PAPER,26)
 if mode=='scope':
  # Deliberately no quantitative graph: incompatible totals cannot be compared.
  for i,(title,sub) in enumerate([('WATERS','North Atlantic / all waters'),('CAUSES','Which kinds of loss?'),('PERIOD','Which dates?')]):
   x=260+i*510;d.rounded_rectangle((x,315,x+470,485),radius=8,fill=dm.PAPER);dm.text(d,(x+25,335),title,35);dm.text(d,(x+25,410),sub,25)
 if mode=='chain':
  labels=['Find','Interpret','Respond','Protect','Arrive']
  for i,s in enumerate(labels):
   x=210+i*325;d.rounded_rectangle((x,330,x+280,440),radius=8,fill=dm.PAPER);dm.text(d,(x+25,365),s,34)
   if i<4:dm.arrow(d,(x+285,385),(x+318,385),dm.GOLD)
 if mode=='dive':
  dm.plane(d,700+150*u,400);cm.boat(d,1310,510+70*u,dm.RED,True);dm.arrow(d,(1390,500),(1390,605),dm.RED);label(590,345,'Aircraft approach → submarine dives',dm.GOLD)
 if mode in ('arrival','cargo','return'):
  label(1240,770,'Destination: Britain',dm.GOLD)
  if mode=='return':dm.arrow(d,(1600,460),(700,460),dm.PAPER);label(800,390,'Next crossing',dm.PAPER)
  if mode=='cargo':
   for i,s in enumerate(['Food','Fuel','Equipment']):
    x=400+i*370;d.rectangle((x,340,x+320,440),outline=dm.GOLD,width=4);label(x+35,370,s,dm.GOLD)
 dm.text(d,(95,948),'SCHEMATIC • no exact tracks, ship counts, patrol radius or battle positions',27)
 dm.text(d,(95,1002),row['shot_id']+' | Natural Earth public-domain coastlines • original studio diagram',25)
 return im
if __name__=='__main__':dm.SPECS=S;dm.render=render;dm.main()
