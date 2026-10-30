import sys,json,math
from pathlib import Path
S=Path(sys.argv[1]); sys.path.insert(0,str(S))
src=(S/'_build_code_graphics_v02.py').read_text().replace("/System/Library/Fonts/Supplemental/Didot.ttc","/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf").replace(",index=1)",")")
(S/'cgmod.py').write_text(src)
import cgmod
from PIL import Image,ImageDraw,ImageFont
specs=json.loads((S/'PICTURE_PLAN_v03.json').read_text())['code_graphics'];bg=cgmod.paper()
out=S/'strips';out.mkdir(exist_ok=True)
fnt=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",28)
for part in range(2,6):
  board=json.loads((S/f'parts/part-{part:02}_plates_v03.json').read_text())
  for row in board['plates']:
    k=f"P{part}:{row['id']}"
    if k not in specs: continue
    spec=cgmod.lock_label(k,specs[k]);name=row['id'].split('_',1)[1];dur=row['use_s']
    ov=spec['layout_mode']=='moving_plate_overlay'
    ts=[dur*f for f in (0.08,0.3,0.5,0.7,0.92)]
    tiles=[]
    for t in ts:
      lay=cgmod.graphic(name,t,dur,spec['label'],alpha_layer=ov)
      base=Image.new('RGBA',lay.size,(70,80,95,255)) if ov else bg  # grey stand-in for the moving plate
      im=Image.alpha_composite(base,lay).convert('RGB').resize((640,360));ImageDraw.Draw(im).text((10,8),f"{t:.1f}s",fill='yellow',font=fnt);tiles.append(im)
    sheet=Image.new('RGB',(640*5,400),(20,20,20));[sheet.paste(im,(i*640,0)) for i,im in enumerate(tiles)]
    ImageDraw.Draw(sheet).text((10,365),f"{k}  [{spec['layout_mode']}]  label: {spec['label']}  use {dur}s  vo: {row.get('vo_land','')[:120]}",fill='white',font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",22))
    sheet.save(out/f"{k.replace(':','_')}.jpg",quality=85);print(k,spec['label'],dur,ov)
