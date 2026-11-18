#!/usr/bin/env python3
"""L002–L014: convoy problem, March patrols and submarine constraints.
Original explanatory schematics; no invented exact tracks, losses or equipment sizes.
"""
from PIL import Image,ImageDraw
import detection_maps as dm
import convoy_maps as cm
S={
'L002':[('combined','By the end of May','The balance of advantage had changed'),('combined','More ways to reach a convoy','Longer shore reach • carriers at sea'),('withdraw','Losses changed the decision','The offensive became unacceptable to its commander'),('pressure','A dangerous hunting ground','Aircraft and escorts threaten the attackers'),('combined','More than extra fuel','A combined operational system')],
'L003':[('arrive','Britain depended on arrivals','Ships carry the supply line'),('cargo','Cargo for Britain and the Allied build-up','Food • fuel • men • equipment'),('loss','More than a missing hull','A lost ship meant a lost delivery'),('loss','Cargo that would not arrive','The strategic cost of a sinking')],
'L004':[('attack','Break the supply movement','German submarine campaign'),('gather','Concentrate against merchant shipping','Dönitz directs the campaign'),('search','An immense search area','A convoy first had to be found'),('shadow','Find, then keep contact','An attack began with a search problem')],
'L005':[('screen','Protection through grouping','Escorts protect merchant ships together'),('attack','A convoy was no fortress','The crossing still had to be made'),('weather','Darkness, weather and attackers','Approaches from beyond the close screen'),('attack','More than one approach','Escorts could face pressure from several directions')],
'L006':[('march','March 1943','HX 229 and SC 122 • running convoy battle'),('marchattack','Boats gathered around the convoys','Schematic approaches, not exact tracks'),('marchloss','Escorts fought to keep attacks away','Merchant ships were torpedoed'),('march','Beyond reliable air support','The cost of an intermittent patrol presence')],
'L007':[('longsearch','More than 20 hours airborne','Liberator patrol seeking SC 122 • official RAF account'),('failed','The convoy was not found','A long flight did not guarantee a rendezvous'),('longsearch','Reaching far across the sea','Distance was one achievement'),('failed','Finding was another task','North Atlantic weather complicated the search')],
'L008':[('iceland','Iceland towards HX 229','Liberator patrol • official RAF account'),('wind','Delayed by crosswind','Strong wind across the runways'),('four','Four hours of cover','After reaching the convoy'),('four','Protection had limits','Weather • distance • time before return')],
'L009':[('gap','What the air gap meant','A practical problem, not a permanent shape'),('gap','No fixed patch to colour in','Patrol protection depended on conditions'),('budget','A moving target and a return journey','Base distance • fuel • weather • search'),('combined','Make help more dependable','Turn reach into effective protection')],
'L010':[('subsection','Not a whole patrol underwater','Conventional U-boats of this campaign'),('diesel','Two operating conditions','Diesel on the surface • batteries below'),('subsection','Concealment with limits','Submergence restricted the boat'),('charge','Recharge on the surface','Batteries needed charging • surface speed was better')],
'L011':[('pressure','Value beyond sinkings','An aircraft could disrupt an attack'),('dive','A forced dive changes the hunt','Less freedom than on the surface'),('lag','Harder to shadow or move ahead','Submerged limitations interrupt contact'),('dive','Disrupt the hunt','Protection without a wreck')],
'L012':[('tanker','An example from March','SC 122 • tanker astern'),('sunderland','A Sunderland finds the threat','A U-boat near a straggling tanker'),('tankerdiving','Aircraft attacks, submarine dives','No sinking inferred'),('tankerdiving','Prevent the attack on the tanker','The merchant ship is the objective'),('tanker','Beyond a tally of sinkings','Measure the protection provided')],
'L013':[('radio','Contact could spread','The submarine method needed information'),('radio','Call other boats towards a convoy','Contact report brings others'),('radio','Transmitting carried a risk','Useful to German commanders, audible to listeners'),('bearing','Allied listeners could find direction','A bearing, not an exact position')],
'L014':[('uncertain','An imperfect view','No all-seeing intelligence map'),('uncertain','Late or incomplete information','The search picture has limits'),('uncertain','The convoy keeps moving','Headquarters must interpret a changing situation'),('order','Information must become action','A useful order to a ship or aircraft at sea')]
}
def render(row,t,duration):
 mode,heading,note=S[row['line_id']][int(row['shot_id'].split('.')[1])-1];u=min(1,max(0,t/max(.01,duration)))
 im=cm.BG.copy();d=ImageDraw.Draw(im);dm.text(d,(90,55),heading,55);dm.text(d,(94,140),note,29)
 def label(x,y,s,c=dm.PAPER,n=28):dm.text(d,(x,y),s,n,c)
 cx=1000+120*u;cy=700
 for dx,dy in [(-35,-25),(35,-25),(-35,25),(35,25)]:cm.boat(d,cx+dx,cy+dy,dm.GOLD)
 for dx in [-130,130]:cm.boat(d,cx+dx,cy,dm.BLUE)
 label(cx-60,cy+70,'Convoy');dm.arrow(d,(cx+185,cy),(1660,cy),dm.GOLD)
 label(290,810,'Newfoundland');label(1210,260,'Iceland',dm.INK);label(1620,550,'Britain',dm.INK)
 if mode in ('combined','pressure','budget','longsearch','failed','gap'):
  start=cm.xy(-6,55);end=(cx-100,430);dm.arrow(d,start,end,dm.GOLD)
  if mode!='gap':dm.plane(d,start[0]+(end[0]-start[0])*u,start[1]+(end[1]-start[1])*u)
  if mode=='combined':cm.boat(d,650+100*u,500,dm.BLUE);dm.plane(d,700+150*u,390);label(460,550,'Carrier base',dm.BLUE)
  if mode in ('failed','gap'):label(550,370,'Search remains uncertain',dm.PAPER)
  if mode=='budget':label(450,360,'OUTWARD   /   SEARCH   /   RETURN',dm.GOLD)
  if mode=='longsearch':label(540,350,'More than 20 hours • not a route measurement',dm.GOLD)
 if mode in ('attack','gather','shadow','pressure','screen','weather'):
  for x,y in [(cx-260,490),(cx+230,520)]:
   cm.boat(d,x,y,dm.RED,True)
   if mode in ('attack','gather'):dm.arrow(d,(x,y+25),(cx,y+120),dm.RED)
  if mode=='shadow':dm.arrow(d,(cx-240,520),(cx+30,520),dm.RED);label(550,340,'Maintain contact before attack',dm.RED)
  if mode=='screen':label(530,350,'Close escort screen',dm.BLUE)
 if mode in ('cargo','arrive','loss'):
  if mode=='cargo':
   for i,name in enumerate(['Food','Fuel','Men','Equipment']):
    x=220+i*380;d.rectangle((x,340,x+330,440),outline=dm.GOLD,width=4);label(x+30,370,name,dm.GOLD)
  if mode=='arrive':label(1300,810,'Arrival',dm.GOLD)
  if mode=='loss':
   d.line((cx-75,cy-65,cx+5,cy+15),fill=dm.RED,width=6);d.line((cx-75,cy+15,cx+5,cy-65),fill=dm.RED,width=6);label(500,360,'Symbolic loss • no numerical tally')
 if mode in ('march','marchattack','marchloss'):
  # Two schematic convoy lanes, no historical separation or exact track implied.
  for name,y in [('HX 229',400),('SC 122',530)]:
   dm.arrow(d,(480,y),(1450,y),dm.GOLD);cm.boat(d,800+200*u,y-15,dm.GOLD);label(270,y-20,name)
   if mode!='march':cm.boat(d,1050,y-80,dm.RED,True);dm.arrow(d,(1050,y-55),(1000,y-5),dm.RED)
  if mode=='marchloss':label(470,820,'Torpedo losses • escort response • no tally')
 if mode in ('iceland','wind','four'):
  start=cm.xy(-20,64);dest=(cx,510);dm.arrow(d,start,dest,dm.GOLD);dm.plane(d,start[0]+(dest[0]-start[0])*u,start[1]+(dest[1]-start[1])*u)
  if mode=='wind':
   d.line((1300,370,1550,370),fill=dm.PAPER,width=6);dm.arrow(d,(1420,300),(1420,440),dm.RED);label(470,360,'Crosswind delays departure',dm.GOLD)
  elif mode=='four':label(520,360,'Four hours over the ships',dm.GOLD)
 if mode=='weather':
  for x,y in [(720,410),(950,420),(1120,390)]:d.ellipse((x-110,y-30,x+170,y+80),fill=(149,167,171))
 if mode in ('subsection','diesel','charge'):
  # Separate engineering panel: no hull type, layout or dimensions implied.
  d.rounded_rectangle((250,310,1710,590),radius=10,fill=dm.PAPER);dm.text(d,(300,330),'OPERATING CONDITIONS • SCHEMATIC',30)
  d.line((300,440,1660,440),fill=dm.SEA,width=4);cm.boat(d,850,420,dm.INK,True);cm.boat(d,1280,520,dm.INK,True)
  dm.text(d,(330,380),'SURFACE: diesel / recharge',29);dm.text(d,(1030,550),'SUBMERGED: battery',29)
 if mode in ('dive','lag'):
  dm.plane(d,700+150*u,400);cm.boat(d,1260,490+80*u,dm.RED,True);dm.arrow(d,(1370,480),(1370,600),dm.RED)
  label(470,340,'Dive interrupts the surface hunt',dm.GOLD)
  if mode=='lag':dm.arrow(d,(cx+80,600),(cx+260,600),dm.GOLD)
 if mode in ('tanker','sunderland','tankerdiving'):
  cm.boat(d,650,690,dm.GOLD);label(490,765,'Tanker astern');cm.boat(d,650,470+(75*u if mode=='tankerdiving' else 0),dm.RED,True)
  if mode!='tanker':dm.plane(d,420+120*u,360);dm.arrow(d,(500,400),(620,470),dm.GOLD)
  if mode=='tankerdiving':dm.arrow(d,(750,450),(750,590),dm.RED)
 if mode in ('radio','bearing'):
  cm.boat(d,1250,430,dm.RED,True)
  if mode=='radio':
   for x,y in [(650,390),(820,510)]:cm.boat(d,x,y,dm.RED,True);dm.wave(d,(1200,430),(x+45,y),t,dm.RED)
   label(480,325,'Contact report to other boats',dm.RED)
  else:dm.bearing(d,(cx-130,cy-25),(1250,430));label(500,335,'Passive listening: direction only',dm.BLUE)
 if mode in ('uncertain','order'):
  d.ellipse((650,330,1470,565),outline=dm.GOLD,width=4);label(770,400,'Uncertain search area',dm.GOLD)
  if mode=='order':dm.arrow(d,(750,490),(cx-130,cy-40),dm.BLUE);label(400,570,'Information → useful order',dm.BLUE)
 if mode=='withdraw':
  for x in [750,1250]:cm.boat(d,x,450,dm.RED,True);dm.arrow(d,(x,475),(x-60,570),dm.RED)
  label(560,340,'Change operating area',dm.RED)
 dm.text(d,(95,948),'SCHEMATIC • no exact tracks, ship counts, numerical ranges or battle positions',26)
 dm.text(d,(95,1002),row['shot_id']+' | Natural Earth public-domain coastlines • original studio diagram',25)
 return im
if __name__=='__main__':dm.SPECS=S;dm.render=render;dm.main()
