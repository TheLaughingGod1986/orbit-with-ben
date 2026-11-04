#!/usr/bin/env python3
"""032 quantitative overlay stills for pre-render review. No animation render authority.

Each row has its own file and source pointer. Transparent overlays composite over
approved moving real plates; no illustrative preview background enters the film.
Units and baseline are explicit. Values remain those locked in SOURCES.md.
"""
import argparse,hashlib,json,math,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
from code_graphics import W,H,GOLD,WHITE,font
# Each comparison is a single idea, using an honest linear scale from zero.
SPECS=[
 {'id':'r03_pressure','row':3,'kind':'bars','title':'PRESSURE','unit':'BAR','values':[('EARTH',1),('TITAN',1.47)],'max':1.5,'source_rows':[1]},
 {'id':'r25_pressure','row':25,'kind':'bars','title':'PRESSURE','unit':'BAR','values':[('EARTH',1),('TITAN',1.47)],'max':1.5,'source_rows':[1]},
 {'id':'r04_cold','row':4,'kind':'thermometer','title':'ALMOST NO OXYGEN','unit':'°C','value':-179,'source_rows':[1,8,9]},
 {'id':'r19_temp_scale','row':19,'kind':'thermometer','title':'TITAN','unit':'°C','value':-179,'source_rows':[8]},
 {'id':'r26_airmix','row':26,'kind':'composition','title':'TITAN AIR','unit':'%','values':[('NITROGEN',95),('METHANE',5)],'source_rows':[9],'fallback':'£0 R26; no Orbit generation'},
 {'id':'r27_airmix','row':27,'kind':'composition','title':'TITAN AIR','unit':'%','values':[('NITROGEN',95),('METHANE',5)],'source_rows':[9]},
 {'id':'r27_density','row':27,'kind':'bars','title':'AIR DENSITY','unit':'× EARTH','values':[('EARTH',1),('TITAN',4)],'max':4,'source_rows':[9]},
 {'id':'r27_gravity','row':27,'kind':'bars','title':'GRAVITY','unit':'× EARTH','values':[('EARTH',1),('TITAN',1/7)],'max':1,'display':['1','≈ 1/7'],'source_rows':[9]},
 {'id':'r28_rain','row':28,'kind':'rain','title':'EARTH RAIN','diameter':6.5,'speed':9.2,'source_rows':[10]},
 {'id':'r29_rain','row':29,'kind':'rain','title':'TITAN RAIN','diameter':9.5,'speed':1.6,'source_rows':[10]},
 {'id':'r33_depth_ligeia','row':33,'kind':'depth','title':'LIGEIA MARE','value':160,'display':'≈ 160 M','source_rows':[12]},
 {'id':'r34_depth_kraken','row':34,'kind':'depth','title':'KRAKEN MARE','value':300,'display':'≥ 300 M','lower_bound':True,'source_rows':[12]},
 {'id':'r39_oxygen','row':39,'kind':'bars','title':'EARTH AIR','unit':'%','values':[('NITROGEN',78),('OXYGEN',21)],'max':100,'source_rows':[9,14]},
 {'id':'r40_airmix','row':40,'kind':'composition','title':'TITAN AIR','unit':'%','values':[('NITROGEN',95),('METHANE',5)],'source_rows':[9,14],'footnote':'ALMOST NO OXYGEN'},
 {'id':'r45_density','row':45,'kind':'bars','title':'AIR DENSITY','unit':'× EARTH','values':[('EARTH',1),('TITAN',4)],'max':4,'source_rows':[15]},
 {'id':'r45_gravity','row':45,'kind':'bars','title':'GRAVITY','unit':'× EARTH','values':[('EARTH',1),('TITAN',1/7)],'max':1,'display':['1','≈ 1/7'],'source_rows':[15]},
 {'id':'r46_lift_28x','row':46,'kind':'equation','title':'OUR ROUGH SUM','lines':['4× AIR','÷ 1/7 WEIGHT','≈ 28× EASIER'],'source_rows':[15],'fallback':'£0 R46; composite over approved APL dune plate'},
 {'id':'r49_daynight','row':49,'kind':'daynight','title':'TITAN DAYTIME','source_rows':[16]},
]
BLUE=(102,205,245,255);DIM=(198,215,232,230)
def text(d,xy,s,size=58,col=WHITE):
 d.text(xy,s,font=font(size),fill=col,stroke_width=3,stroke_fill=(20,28,42,255))
def frame(s,t=1.8):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 # 160 px margins, occupies left region; exact placement needs plate-specific QA.
 x,y=160,200;p=max(0,min(1,t/1.2));text(d,(x,y),s['title'],64,GOLD)
 k=s['kind']
 if k=='bars':
  end=1140;d.line((x,420,end,420),fill=DIM,width=3);text(d,(end+20,395),s['unit'],38)
  for i,(label,v) in enumerate(s['values']):
   yy=500+i*160;text(d,(x,yy),label,48)
   d.rounded_rectangle((x+260,yy,x+260+max(2,720*v/s['max']*p),yy+60),radius=8,fill=BLUE if i==0 else GOLD)
   value=s.get('display',[f'{v:g}' for _,v in s['values']])[i];text(d,(x+260,yy+72),value,48)
  text(d,(x,860),'0',36)
 elif k=='composition':
  # A composition bar, not a flat celestial body. Total width is exactly 100%.
  d.rounded_rectangle((x,440,x+1100,550),radius=10,outline=DIM,width=3)
  xx=x
  for i,(label,v) in enumerate(s['values']):
   ww=1100*v/100*p;d.rectangle((xx,443,xx+ww,547),fill=BLUE if i==0 else GOLD);xx+=ww
   text(d,(x,620+i*95),f'{label}  {v:g}%',58,BLUE if i==0 else GOLD)
  if s.get('footnote'):text(d,(x,840),s['footnote'],48)
 elif k=='thermometer':
  # Freezing baseline zero, cooling downward; never describes Celsius as a ratio.
  xx=x+120;top=370;bottom=850
  d.rounded_rectangle((xx,top,xx+70,bottom),radius=28,outline=DIM,width=4)
  d.rectangle((xx+8,top+8,xx+62,top+8+(bottom-top-16)*p),fill=BLUE)
  for v in [0,-50,-100,-150,-179]:
   yy=top+(bottom-top)*(-v/179);d.line((xx+80,yy,xx+110,yy),fill=WHITE,width=3);text(d,(xx+130,yy-24),f'{v} °C',46)
 elif k=='rain':
  rr=s['diameter']*14;cx=x+230;cy=500+(t%1)*s['speed']*10
  d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=BLUE,outline=WHITE,width=3)
  d.line((cx-rr,cy+rr+35,cx+rr,cy+rr+35),fill=WHITE,width=4)
  text(d,(x+500,440),f"{s['diameter']:g} MM",64,GOLD);text(d,(x+500,550),f"{s['speed']:g} M/S",64)
  text(d,(x+500,670),'MODEL MAXIMUM',38)
 elif k=='depth':
  d.line((x,380,x+1100,380),fill=BLUE,width=5);end=400+400*(s['value']/300)*p
  d.line((x+150,400,x+150,end),fill=GOLD,width=10)
  if s.get('lower_bound'):
   d.polygon([(x+130,end-20),(x+170,end-20),(x+150,end+25)],fill=GOLD)
   text(d,(x+260,790),'LOWER BOUND',42)
  else:d.line((x+100,end,x+200,end),fill=GOLD,width=6)
  text(d,(x+260,550),s['display'],80,GOLD)
 elif k=='equation':
  for i,l in enumerate(s['lines']):text(d,(x,410+i*155),l,74,GOLD if i==2 else WHITE)
 elif k=='daynight':
  d.rectangle((x,460,x+1000*p,570),fill=GOLD);text(d,(x,640),'≈ 8 EARTH DAYS',68)
  text(d,(x,740),'DAYTIME',46)
 opacity=max(0,min(1,t/.4,(3.6-t)/.4))
 if opacity<1:im.putalpha(im.getchannel("A").point(lambda a:round(a*opacity)))
 return im

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--approved',nargs='*',default=[]);ap.add_argument('--review-ref');a=ap.parse_args()
 if a.render and (not a.approved or not a.review_ref):ap.error('Render needs individually approved ids and review reference')
 out=Path(a.out);out.mkdir(exist_ok=True,parents=True)
 sheet=Image.new('RGB',(1280,360*math.ceil(len(SPECS)/2)),(35,49,68));sd=ImageDraw.Draw(sheet);clips=[]
 for i,s in enumerate(SPECS):
  dest=out/('code_graphic_032_'+s['id']+'_v01.png');im=frame(s);im.save(dest)
  tile=Image.new('RGBA',(W,H),(40,58,79,255));tile.alpha_composite(im);tile=tile.convert('RGB').resize((640,360));x=(i%2)*640;y=(i//2)*360;sheet.paste(tile,(x,y));sd.text((x+8,y+8),s['id'],fill='white')
  clips.append({**s,'preview':str(dest),'preview_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'review_status':'DRAFT_STILL_REVIEW_REQUIRED','rendered':False,'needs_background':'graded moving real plate; not yet selected','contrast_on_actual_composite':'UNVERIFIED','safe_placement_on_actual_subject':'UNVERIFIED'})
 if a.render:
  for s,rec in zip(SPECS,clips):
   if s['id'] not in a.approved:continue
   dest=out/('code_graphic_032_'+s['id']+'_v01.mov')
   proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgba','-video_size',f'{W}x{H}','-framerate','30','-i','pipe:0','-an','-c:v','qtrle',str(dest)],stdin=subprocess.PIPE)
   try:
    for j in range(108):proc.stdin.write(frame(s,j/30).tobytes())
    proc.stdin.close()
    if proc.wait():raise RuntimeError('ffmpeg render failed')
   except BaseException:proc.kill();raise
   rec.update(rendered=True,render=str(dest),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),review_ref=a.review_ref,review_status='RENDERED_NOT_FINAL_COMPOSITE')
 sheet.save(out/'data_previews.jpg',quality=94)
 (out/'DATA_MANIFEST_v01.json').write_text(json.dumps({'job':'J2089','status':'DRAFT_NOT_APPROVED_TO_RENDER','clips':clips},indent=2)+'\n')
if __name__=='__main__':main()
