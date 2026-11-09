from PIL import Image,ImageOps,ImageDraw,ImageFont
from pathlib import Path
import json,textwrap
O=Path(__file__).parent;j=json.loads((O/'extra_study.json').read_text());es={}
for g in j['groups']:
 for e in g['all_90d']:
  if e['id'] in g['fast_ids']+g['slow_ids']:es[e['id']]={**e,'group':g['channel']+' '+g['tab']}
rows=list(es.values());font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',15)
for start in range(0,len(rows),12):
 im=Image.new('RGB',(1200,1000),'#ededed');d=ImageDraw.Draw(im)
 for n,e in enumerate(rows[start:start+12]):
  x=(n%3)*400;y=(n//3)*250;p=O/'extra_thumbs'/f"{e['id']}.jpg"
  if p.exists():
   with Image.open(p) as src: im.paste(ImageOps.contain(src.convert('RGB'),(390,165)),(x,y))
  label=f"{e['id']} | {e['group']}\n{e['views_per_day']:,.0f}/day | {e['published'][:10]}\n"+'\n'.join(textwrap.wrap(e['title'],48)[:2]);d.multiline_text((x+3,y+169),label,fill='black',font=font)
 im.save(O/f'extra_sheet_{start//12+1}.jpg')
(O/'extra_coded_order.json').write_text(json.dumps([{'id':e['id'],'title':e['title'],'group':e['group']} for e in rows],indent=2))
