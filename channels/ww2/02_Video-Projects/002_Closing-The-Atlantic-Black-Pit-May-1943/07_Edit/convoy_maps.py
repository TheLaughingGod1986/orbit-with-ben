#!/usr/bin/env python3
"""L040–L048 original convoy comparison maps; illustrative, never exact tracks."""
import json,math,pathlib
from PIL import Image,ImageDraw
import detection_maps as dm
S={
'L040':[
('west','ONS 5: westbound','From Britain towards North America'),
('west','Late April into early May','ONS 5 • 1943'),
('attack','Submarines converged','Escorts faced repeated attacks'),
('weather','No controlled conditions','A convoy under pressure'),
('weather','Through difficult seas','Protection had to work in the weather')],
'L041':[
('weather','Weather shaped the fight','Conditions mattered at sea and in the air'),
('weather','Storms and poor visibility','Ships and aircraft were affected'),
('search','Assigned is not found','A patrol still had to locate the convoy'),
('weather','Weather at both ends','Base conditions and search conditions'),
('search','An order is not support','Finding the convoy was essential')],
'L042':[
('iceland','From Iceland to ONS 5','More than 1,000 miles from base • not a range circle'),
('fog','The crew saw nothing','Patches of fog • short time over convoy'),
('fog','Reach was not effectiveness','Distance alone could not clear the fog')],
'L043':[
('radar','Fog changed the advantage','Surface escorts with radar'),
('radar','Weather and shipborne radar','Factors in the surface encounter'),
('limited','Keep the contribution clear','Fog limited air operations • no air attack depicted')],
'L044':[
('loss','Merchant ships were lost','Symbolic losses • not a numerical tally'),
('loss','The passage had a cost','No graphic depiction of casualties'),
('subloss','U-boats also suffered losses','Symbolic losses • not a numerical tally'),
('subloss','A costly way to cut supply','The convoy remained the objective')],
'L045':[
('limited','ONS 5 complicates the answer','Longer range was one part of the defence'),
('limited','Not bombers alone','This fog battle needs a different explanation'),
('combined','Several forms of protection','Aircraft when available • escorts close in'),
('radar','When aircraft were limited','Surface ships still had to fight')],
'L046':[
('east','SC 130: later in May','A different convoy • a different result'),
('east','No merchant ship lost','Through a concentration of submarines'),
('sightings','Aircraft made repeated sightings','Observation is not destruction'),
('eight','Eight sightings in one sortie','120 Squadron Liberator • sightings, not boats sunk')],
'L047':[
('eight','Sightings are not sinkings','Not eight boats destroyed or eight unique boats'),
('sightings','Attention around the convoy','Aircraft searched the approaches'),
('combined','Pressure beyond the screen','Aircraft farther out • escorts closer in'),
('combined','Defences worked together','Different methods protected one passage')],
'L048':[
('arrive','What did success look like?','Judge the protected passage'),
('arrive','Arrival without loss','No dramatic sinking needed to make the point'),
('arrive','SC 130 shows the result','Merchant ships reached their destination'),
('arrive','Its merchant ships got through','The protected convoy arrived'),
('cargo','The cargo was the purpose','Supply delivered • not an attack tally')]
}
COAST=pathlib.Path('/Volumes/data/studio-live/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/03_Picture/maps/M001/ne_110m_land.geojson')
GEO=json.loads(COAST.read_text())
def boat(d,x,y,c,sub=False):
 d.polygon([(x-25,y-7),(x+25,y-7),(x+35,y),(x+22,y+8),(x-22,y+8),(x-33,y)],fill=c)
 d.rectangle((x-5,y-20,x+7,y-6),fill=c)
 if not sub:d.line((x,y-20,x,y-32),fill=c,width=2)
def xy(lon,lat):return ((lon+75)/80*1750+85,(70-lat)/32*675+225)
def base():
 im=Image.new('RGB',(1920,1080),dm.PAPER);mp=Image.new('RGB',(1750,675),dm.SEA);d=ImageDraw.Draw(mp)
 for x in range(0,1750,150):d.line((x,0,x,675),fill=(83,109,118))
 for y in range(0,675,100):d.line((0,y,1750,y),fill=(83,109,118))
 for feature in GEO['features']:
  polys=feature['geometry']['coordinates'];polys=[polys] if feature['geometry']['type']=='Polygon' else polys
  for poly in polys:
   for k,ring in enumerate(poly):d.polygon([(xy(*v[:2])[0]-85,xy(*v[:2])[1]-225) for v in ring],fill=(177,181,158) if k==0 else dm.SEA)
 im.paste(mp,(85,225));return im
BG=base()
def render(row,t,duration):
 mode,heading,note=S[row['line_id']][int(row['shot_id'].split('.')[1])-1];im=BG.copy();d=ImageDraw.Draw(im);dm.text(d,(90,55),heading,58);dm.text(d,(94,140),note,31)
 def label(x,y,s,c=dm.PAPER):dm.text(d,(x,y),s,29,c)
 label(300,770,'Newfoundland');d.line([(450,760),xy(-56,49)],fill=dm.PAPER,width=2);label(1200,265,'Iceland',dm.INK);label(1620,540,'Britain',dm.INK)
 u=min(1,max(0,t/max(.01,duration)));west=row['line_id']<'L046';convoy='ONS 5' if west else 'SC 130';cx=1130-180*u if west else 920+180*u;cy=660
 # Symbolic group size only; explicitly disclaimed below the map.
 for dx,dy in [(-45,-25),(25,-25),(-45,25),(25,25)]:boat(d,cx+dx,cy+dy,dm.GOLD)
 for dx,dy in [(-120,0),(110,0)]:boat(d,cx+dx,cy+dy,dm.BLUE)
 label(cx-80,cy+75,convoy)
 if west:dm.arrow(d,(1190,770),(760,770),dm.PAPER)
 else:dm.arrow(d,(750,770),(1270,770),dm.PAPER)
 label(690,820,'Westbound' if west else 'Eastbound')
 if mode in ('attack','weather','loss','subloss','radar'):
  for x,y in [(cx-220,cy-135),(cx+180,cy-145)]:
   boat(d,x,y,dm.RED,True)
   if mode=='attack':dm.arrow(d,(x,y+25),(cx,y+100),dm.RED)
 if mode in ('weather','fog','limited','radar','search'):
  overlay=Image.new('RGBA',im.size,(0,0,0,0));od=ImageDraw.Draw(overlay)
  for x,y in [(720,480),(1050,460),(880,570)]:od.ellipse((x-130,y-90,x+260,y+150),fill=(220,226,224,80))
  im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB');d=ImageDraw.Draw(im);label(800,350,'Poor visibility',dm.PAPER)
 if mode in ('iceland','fog','search'):
  start=xy(-20,64);end=(cx,cy-145);dm.arrow(d,start,end,dm.GOLD);dm.plane(d,start[0]+(end[0]-start[0])*u,start[1]+(end[1]-start[1])*u)
  if mode=='iceland':label(450,410,'More than 1,000 miles from base',dm.GOLD)
  elif mode=='fog':label(410,410,'Journey made • no sighting',dm.GOLD)
  else:label(430,410,'Search still required',dm.GOLD)
 if mode in ('radar','limited'):
  dm.wave(d,(cx+110,cy),(cx+180,cy-145),t)
  label(450,410,'Surface escort radar',dm.BLUE)
  if mode=='limited':label(440,460,'Air operations limited by fog',dm.GOLD)
 if mode in ('loss','subloss'):
  x,y=(cx-45,cy-25) if mode=='loss' else (cx-220,cy-135)
  d.line((x-40,y-40,x+40,y+40),fill=dm.PAPER,width=7);d.line((x-40,y+40,x+40,y-40),fill=dm.PAPER,width=7)
  label(440,395,'Loss symbol, not a count')
 if mode in ('combined','sightings','eight'):
  dm.plane(d,cx-200+170*u,555 if mode=='eight' else 430)
  if mode!='eight':dm.arrow(d,(cx-220,470),(cx+130,470),dm.GOLD)
  if mode=='combined':label(440,365,'Aircraft search farther out',dm.GOLD);label(440,410,'Escorts protect close approaches',dm.BLUE)
  elif mode=='sightings':
   for x,y in [(cx-220,520),(cx+170,470)]:d.ellipse((x-22,y-22,x+22,y+22),outline=dm.RED,width=4)
   label(440,365,'Observations around the convoy',dm.GOLD)
  else:
   # A boxed record counter, not geographic observation positions or submarine icons.
   d.rounded_rectangle((440,325,1650,445),radius=8,fill=dm.PAPER)
   for i in range(8):
    x=470+i*145;d.ellipse((x,350,x+75,425),outline=dm.INK,width=3);dm.text(d,(x+23,363),str(i+1),30,dm.INK)
   label(470,455,'Eight observation records, one sortie',dm.GOLD)
 if mode in ('arrive','cargo','east'):
  dm.arrow(d,(cx+170,620),(1630,620),dm.GOLD);label(1220,760,'Destination: Britain',dm.GOLD)
  if mode=='cargo':
   for i,name in enumerate(['Food','Fuel','Equipment']):
    x=450+i*330;d.rectangle((x,345,x+265,420),outline=dm.GOLD,width=3);label(x+35,365,name,dm.GOLD)
 dm.text(d,(95,948),'SCHEMATIC • no exact track, ship count, patrol radius or battle position',28)
 dm.text(d,(95,1002),row['shot_id']+'  |  Natural Earth public-domain coastlines • original studio diagram',25)
 return im
if __name__=='__main__':dm.SPECS=S;dm.render=render;dm.main()
