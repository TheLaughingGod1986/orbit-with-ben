#!/usr/bin/env python3
"""Original sentence-specific detection diagrams, L030–L038.
Render drafts, never an approval. Geometry is schematic, not historical position,
range, wavelength, timing or equipment dimensions. No external artwork.
"""
import argparse, hashlib, json, math, pathlib, subprocess
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1920,1080,25
PAPER=(230,227,211); INK=(39,55,61); SEA=(73,99,109)
GOLD=(243,205,104); BLUE=(121,211,226); RED=(246,145,113)
FONT='/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
# Each entry is authored against its exact locked sentence, not keyword-generated.
# Mode, heading, local annotation. Public metadata retains the complete spoken line.
SPECS={
'L030':[
('night','A contact in darkness','A surfaced U-boat'),
('radar','Radar: transmit and receive','Radio waves • target echo'),
('warning','Metox warning receiver','Listens for earlier radar'),
('dive','Warning before arrival','Earlier radar → warning → dive')],
'L031':[
('warning','Finding versus warning','Aircraft searches • submarine listens'),
('approach','Closing the contact','Aircraft approach'),
('dive','Time to disappear','Warning gives a chance to dive'),
('warning','Can the enemy hear it?','Earlier radar transmissions'),
('warning','Equipment changes the contest','No fixed warning interval')],
'L032':[
('newradar','A different radar band','Centimetric airborne radar • 1943'),
('waves','Shorter wavelengths','Qualitative comparison • not to scale'),
('newradar','The Metox limitation','No equivalent Metox warning'),
('newradar','Detection without old warning','Metox limitation, not universal invisibility')],
'L033':[
('deployment','Not an overnight change','Different units • different readiness'),
('deployment','Fitting sets took work','Delivery → fitting → readiness'),
('deployment','Spreading through squadrons','Spring 1943 • no single switch date'),
('deployment','A developing capability','Not simultaneous Atlantic-wide coverage')],
'L034':[
('approach','Finding was one problem','Final approach remained another'),
('light','The Leigh Light','Night illumination example'),
('light','Radar, then illumination','Example combination • not every VLR aircraft')],
'L035':[
('passive','Radio direction finding','A different method'),
('passive','Listen to the transmitter','No Allied outgoing pulse'),
('passive','HF/DF: huff-duff','High-frequency direction finding'),
('bearing','A direction to investigate','A bearing, not an exact position'),
('bearing','Direction without the words','Message content not required')],
'L036':[
('methods','Three kinds of information','Keep the methods distinct'),
('methods','Different methods','Content • direction • echo'),
('methods','Contributions, not equivalents','Each supplies different information'),
('uncertain','No all-seeing chart','Search uncertainty remains')],
'L037':[
('bearing','One bearing is a direction','Not an exact point'),
('crossbearings','Narrowing a search area','Illustrative uncertainty • not a fix'),
('crossbearings','Information has limits','A search area is not visual identification'),
('crossbearings','Where to look next','Guide a search, then identify the contact')],
'L038':[
('escort','Detection creates a chance','Escort response still required'),
('sonar','Above and below water','Surface radar • underwater sonar'),
('escort','Contact is not an attack','Weapons and tactics still required'),
('escort','Crews turn information into action','Interpret the contact • handle the ship')]
}
def font(n):return ImageFont.truetype(FONT,n)
def text(d,xy,s,n=34,c=INK):
 f=font(n);box=d.textbbox(xy,s,font=f)
 if box[0]<0 or box[2]>W or box[3]>H:raise ValueError('Text outside frame: '+s)
 d.text(xy,s,font=f,fill=c)
def arrow(d,a,b,c=BLUE,width=5):
 d.line([a,b],fill=c,width=width);ang=math.atan2(b[1]-a[1],b[0]-a[0]);r=18
 d.polygon([b,(b[0]-r*math.cos(ang-.5),b[1]-r*math.sin(ang-.5)),(b[0]-r*math.cos(ang+.5),b[1]-r*math.sin(ang+.5))],fill=c)
def boat(d,x,y,c=GOLD,sub=False):
 d.polygon([(x-65,y-12),(x+65,y-12),(x+86,y),(x+58,y+15),(x-58,y+15),(x-80,y)],fill=c)
 d.rectangle((x-12,y-35,x+14,y-10),fill=c)
 if not sub:d.line((x+1,y-35,x+1,y-65),fill=c,width=4)
def plane(d,x,y):
 d.polygon([(x+55,y),(x-22,y-10),(x-28,y-62),(x-41,y-62),(x-42,y-10),(x-70,y-23),(x-70,y+23),(x-42,y+10),(x-41,y+62),(x-28,y+62),(x-22,y+10)],fill=GOLD)
def wave(d,a,b,t,c=BLUE,frequency=5):
 pts=[]
 for i in range(181):
  u=i/180;pts.append((a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u+14*math.sin(u*math.tau*frequency-t*3)))
 d.line(pts,fill=c,width=4)
def bearing(d,origin,target,c=BLUE):
 # Broad wedge represents qualitative uncertainty, not a numeric confidence interval.
 x,y=target;d.polygon([origin,(x-100,y-100),(x+110,y+100)],fill=(90,125,137));arrow(d,origin,target,c)
def render(row,t,duration):
 mode,heading,note=SPECS[row['line_id']][int(row['shot_id'].split('.')[1])-1]
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 text(d,(90,55),heading,58);text(d,(94,140),note,31)
 d.rounded_rectangle((85,225,1835,900),radius=14,fill=SEA)
 for x in range(140,1800,100):d.line((x,245,x,880),fill=(83,109,118),width=1)
 for y in range(280,880,100):d.line((105,y,1815,y),fill=(83,109,118),width=1)
 u=max(0,min(1,t/max(duration,.01))); ox,oy=420,510; tx,ty=1410,570
 def label(x,y,s,c=PAPER):text(d,(x,y),s,30,c)
 if mode=='deployment':
  for i,(name,shift) in enumerate([('Unit A',0),('Unit B',1),('Unit C',2)]):
   y=370+i*165;label(170,y,name)
   for j,status in enumerate(['Delivery','Fitting','Ready']):
    x=490+j*400;d.rounded_rectangle((x,y-12,x+265,y+65),radius=8,fill=(159,168,157) if j+shift>min(3,1+int(u*3)) else (211,190,130));text(d,(x+20,y+7),status,30)
    if j<2:arrow(d,(x+280,y+25),(x+375,y+25),PAPER)
  label(480,840,'Illustrative stages; no unit-by-unit dates asserted')
 elif mode=='waves':
  label(190,340,'Earlier sets');wave(d,(520,390),(1650,390),t,frequency=4)
  label(190,610,'New sets');wave(d,(520,660),(1650,660),t,frequency=13)
  label(540,810,'Wavelength comparison only • no numeric scale')
 elif mode=='methods':
  items=[('MESSAGE CONTENT','Reading an encrypted message'),('RADIO BEARING','Listening for direction'),('RADAR ECHO','Transmitting and receiving')]
  active=min(2,int(u*3))
  for i,(name,desc) in enumerate(items):
   y=330+i*170;d.rounded_rectangle((180,y-15,1740,y+110),radius=8,outline=GOLD if i==active else (137,159,164),width=4);label(220,y+12,name,GOLD if i==active else PAPER);label(720,y+12,desc)
 elif mode in ('passive','bearing','crossbearings','uncertain'):
  boat(d,380,740,BLUE);label(225,785,'Allied listening position')
  if mode=='passive':
   boat(d,tx,ty,RED,True);wave(d,(tx-90,ty),(470,700),t,RED);arrow(d,(1260,590),(520,680),RED);label(1270,625,'Enemy transmitter');label(710,740,'Signal travels to listener')
  else:
   bearing(d,(380,710),(1450,370));label(560,520,'Direction band',BLUE)
   if mode=='crossbearings':
    boat(d,1430,780,BLUE);bearing(d,(1430,750),(1340,340),GOLD);d.ellipse((1220,300,1460,500),outline=GOLD,width=4);label(1020,260,'Possible search area',GOLD)
   if mode=='uncertain':label(700,795,'No exact submarine position supplied')
 elif mode=='sonar':
  d.line((120,510,1800,510),fill=PAPER,width=4);boat(d,440,495,BLUE);boat(d,1390,470,RED,True);boat(d,1240,740,RED,True)
  arrow(d,(530,445),(1290,445));label(650,370,'Surface radar')
  wave(d,(500,540),(1150,730),t);label(610,710,'Sonar below water');label(970,825,'Separate detection examples')
 elif mode=='escort':
  boat(d,520+60*u,565,BLUE);boat(d,1350,570,RED,True);arrow(d,(650,550),(1170,550));label(350,680,'Escort response');label(1180,680,'Contact')
  label(510,800,'Detection → interpretation → manoeuvre')
 else:
  px=420+100*u if mode in ('approach','light') else 420
  plane(d,px,440);suby=570+(110*u if mode=='dive' else 0);boat(d,tx,suby,RED,True)
  label(220,330,'Allied aircraft',GOLD);label(1270,suby+65,'U-boat',RED)
  if mode=='night':label(700,760,'Darkness limits visual search')
  elif mode=='light':
   d.polygon([(px+60,455),(1350,520),(1490,625)],fill=(184,176,131));label(690,740,'Radar approach → illumination')
  else:
   wave(d,(px+80,440),(tx-80,550),t,frequency=12 if mode=='newradar' else 5);arrow(d,(px+100,470),(tx-130,565),BLUE)
   if mode=='radar':arrow(d,(tx-150,600),(px+120,520),PAPER);label(720,690,'Transmit → echo')
   elif mode in ('warning','dive'):
    label(1150,770,'Metox warning',GOLD)
    if mode=='dive':arrow(d,(1550,550),(1550,720),RED);label(710,750,'Dive before aircraft arrives')
   elif mode=='newradar':label(800,760,'No equivalent Metox warning',GOLD)
   elif mode=='approach':label(780,750,'Closing distance • no timing scale')
 text(d,(95,948),'SCHEMATIC • positions, dimensions and intervals illustrative',28)
 text(d,(95,1002),row['shot_id']+'  |  Original Field Order History diagram',25)
 return im

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,required=True);ap.add_argument('--video',action='store_true');ap.add_argument('--only');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 film=pathlib.Path(__file__).resolve().parents[1];edl=json.loads((film/'07_Edit/EDL_v01.json').read_text());rows=[r for r in edl['rows'] if r['line_id'] in SPECS and (not a.only or r['shot_id']==a.only)];manifest=[]
 for row in rows:
  duration=row['cut_end_s']-row['cut_start_s'];frames=round(row['cut_end_s']*FPS)-round(row['cut_start_s']*FPS)
  still=a.out/(row['shot_id']+'.jpg');render(row,duration*.5,duration).save(still,quality=94)
  item={k:row[k] for k in ['shot_id','line_id','narration','picture_id','cut_start_s','cut_end_s','boundary_review']};item.update(mode=SPECS[row['line_id']][int(row['shot_id'].split('.')[1])-1][0],still=str(still),frames=frames,state='draft_requires_picture_review')
  if a.video:
   path=a.out/(row['shot_id']+'.mp4');proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(path)],stdin=subprocess.PIPE)
   for n in range(frames):proc.stdin.write(render(row,n/FPS,duration).tobytes())
   proc.stdin.close()
   if proc.wait():raise RuntimeError('ffmpeg failed: '+row['shot_id'])
   item.update(video=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
  manifest.append(item);print(row['shot_id'],frames,flush=True)
 (a.out/'MANIFEST.json').write_text(json.dumps({'state':'draft_not_QA_or_approval','fps':FPS,'audio_sha256':edl['audio_sha256'],'rows':manifest},indent=2)+'\n')
 thumbs=[]
 for r in manifest:
  im=Image.open(r['still']);im.thumbnail((480,270));thumbs.append(im.copy())
 sheet=Image.new('RGB',(480*4,300*math.ceil(len(thumbs)/4)),PAPER)
 for i,im in enumerate(thumbs):sheet.paste(im,(i%4*480,i//4*300))
 sheet.save(a.out/'CONTACT.jpg',quality=90)
if __name__=='__main__':main()
