#!/usr/bin/env python3
"""L015–L019: qualitative geography, patrol time, and moving carrier base.
No metric range circle or exact historical route is drawn.
"""
from PIL import Image,ImageDraw
import detection_maps as dm
import convoy_maps as cm
S={
'L015':[('bases','Geography shaped the task','The North Atlantic is a large operating space'),('bases','Three approaches to the Atlantic','Newfoundland • Iceland • Northern Ireland'),('gap','Between useful patrol areas','Ships could not count on the same air protection'),('change','The boundaries could change','Aircraft • bases • operating conditions'),('gap','No permanent fence','Patrol protection was conditional')],
'L016':[('limit','Distance is not coverage','A maximum reach is not a working patrol'),('limit','Reach alone is not a patrol','The aircraft must do more than arrive'),('budget','Outward flight, search, return','Illustrative stages • no numerical time scale'),('brief','A brief visit near the edge','Transit uses part of the available flying time')],
'L017':[('escort','The escorts remained','No aircraft did not mean no defenders'),('escort','Travelling with the merchantmen','Surface ships formed the close screen'),('tasks','Competing escort tasks','Stay with convoy • investigate • respond'),('search','Seeing beyond the close screen','Aircraft add a farther search')],
'L018':[('both','Two answers to distance','Extend from shore and start at sea'),('both','Longer shore reach, carriers at sea','Complementary ways to bring aircraft'),('gap','Neither worked alone','The Atlantic still presented gaps and limits'),('both','Less room and time for the attacker','Pressure from aircraft and escorts'),('ready','Available where needed','Reach must become an actual patrol')],
'L019':[('both','Two starting points','Fixed shore base • moving carrier'),('shore','A fixed land base','The convoy moves through its useful reach'),('carrier','A moving base at sea','The carrier moves closer to the supported ships'),('both','Different answers to distance','Shore reach and a travelling airfield'),('both','Complementary capabilities','Neither made the other redundant')]
}
def render(row,t,duration):
 mode,heading,note=S[row['line_id']][int(row['shot_id'].split('.')[1])-1]
 im=cm.BG.copy();d=ImageDraw.Draw(im);u=min(1,max(0,t/max(.01,duration)))
 dm.text(d,(90,55),heading,55);dm.text(d,(94,140),note,29)
 def label(x,y,s,c=dm.PAPER,n=28):dm.text(d,(x,y),s,n,c)
 bases=[('Newfoundland',-53,48,300,800),('Iceland',-20,64,1210,260),('Northern Ireland',-6,55,1490,520)]
 for name,lon,lat,lx,ly in bases:
  x,y=cm.xy(lon,lat);d.ellipse((x-8,y-8,x+8,y+8),fill=dm.GOLD);label(lx,ly,name,dm.INK if name!='Newfoundland' else dm.PAPER)
  if mode in ('bases','change','gap'):
   # Broken segments represent examples of searches, never a filled cover zone.
   ex,ey=(x+180,y-70) if lon<-40 else (x-210,y+120)
   for i in range(0,10,2):
    a=i/10;b=(i+1)/10;d.line((x+(ex-x)*a,y+(ey-y)*a,x+(ex-x)*b,y+(ey-y)*b),fill=dm.GOLD,width=4)
   if mode!='gap':dm.plane(d,x+(ex-x)*u,y+(ey-y)*u)
 cx=930+140*u;cy=690
 for dx,dy in [(-35,-25),(35,-25),(-35,25),(35,25)]:cm.boat(d,cx+dx,cy+dy,dm.GOLD)
 for dx in [-125,125]:cm.boat(d,cx+dx,cy,dm.BLUE)
 label(cx-65,cy+70,'Convoy');dm.arrow(d,(cx+175,cy),(1600,cy),dm.GOLD)
 if mode in ('shore','both','search','limit','brief','budget','ready'):
  start=cm.xy(-6,55);dest=(cx,470)
  dm.arrow(d,start,dest,dm.GOLD);dm.plane(d,start[0]+(dest[0]-start[0])*u,start[1]+(dest[1]-start[1])*u)
  if mode not in ('budget','ready'):label(1130,370,'From shore',dm.GOLD)
 if mode in ('carrier','both'):
  carrier=(670+120*u,520);cm.boat(d,*carrier,dm.BLUE);dm.arrow(d,(carrier[0]+50,carrier[1]-40),(cx,430),dm.GOLD);dm.plane(d,carrier[0]+120*u,400);label(420,565,'Moving carrier base',dm.BLUE)
 if mode in ('gap','limit','brief'):
  label(550,360,'Search is intermittent',dm.GOLD)
  if mode=='brief':label(590,425,'Outward + return legs reduce time on station')
 if mode=='budget':
  # Equal-width editorial cards are stages, not measured allocations.
  for i,title in enumerate(['OUTWARD','SEARCH','RETURN']):
   x=300+i*440;d.rounded_rectangle((x,310,x+390,420),radius=8,fill=dm.PAPER);dm.text(d,(x+30,343),title,35)
  label(440,850,'Stage cards show order, not proportional flight times',dm.PAPER,26)
 if mode=='tasks':
  dm.arrow(d,(cx+125,cy-15),(cx+250,cy-140),dm.BLUE);cm.boat(d,cx+280,cy-170,dm.RED,True)
  for i,title in enumerate(['Stay close','Investigate','Respond']):
   x=320+i*440;d.rectangle((x,330,x+390,425),outline=dm.GOLD,width=3);label(x+35,360,title,dm.GOLD)
 if mode=='escort':label(610,370,'Close screen travels with convoy',dm.BLUE)
 if mode=='search':d.arc((cx-290,350,cx+290,680),190,340,fill=dm.GOLD,width=4);label(540,325,'Search beyond the screen',dm.GOLD)
 if mode in ('ready','change'):
  for i,title in enumerate(['Aircraft','Equipment','Crew','Patrol']):
   x=250+i*365;d.rounded_rectangle((x,315,x+315,415),radius=8,fill=dm.PAPER);dm.text(d,(x+25,345),title,33)
 dm.text(d,(95,948),'SCHEMATIC • no exact tracks, ship counts, numeric patrol radii or continuous coverage',26)
 dm.text(d,(95,1002),row['shot_id']+' | Natural Earth public-domain coastlines • original studio diagram',25)
 return im
if __name__=='__main__':dm.SPECS=S;dm.render=render;dm.main()
