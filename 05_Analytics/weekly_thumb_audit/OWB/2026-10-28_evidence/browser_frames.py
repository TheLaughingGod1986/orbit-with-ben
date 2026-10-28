from playwright.sync_api import sync_playwright
from pathlib import Path
import json,base64,hashlib,datetime
O=Path('/Users/benjaminoats/_desk/j1106');D=O/'browser_frame0';D.mkdir(exist_ok=True)
rows=[]
with sync_playwright() as p:
 b=p.chromium.connect_over_cdp('http://127.0.0.1:9223');pg=b.contexts[0].new_page()
 try:
  for old in json.loads((O/'fresh_frame0.json').read_text()):
   if 'error' not in old:continue
   vid=old['id'];row={'id':vid,'read_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'public watch player in existing Orbit browser; decoded video at requested t=0, not API thumbnail'}
   try:
    pg.goto('https://www.youtube.com/watch?v='+vid,wait_until='domcontentloaded',timeout=20000)
    pg.wait_for_function('()=>{let v=document.querySelector("video");return v&&v.readyState>=2&&v.videoWidth>0}',timeout=15000)
    pg.locator('video').evaluate('(v)=>{v.pause();v.currentTime=0}')
    pg.wait_for_function('()=>{let v=document.querySelector("video");return v&&!v.seeking&&v.readyState>=2}',timeout=10000)
    pg.locator('video').evaluate('(v)=>v.pause()')
    pg.wait_for_timeout(400)
    result=pg.locator('video').evaluate('''(v)=>{let c=document.createElement('canvas');c.width=v.videoWidth;c.height=v.videoHeight;c.getContext('2d').drawImage(v,0,0);return {image:c.toDataURL('image/png'),time:v.currentTime,width:v.videoWidth,height:v.videoHeight,duration:v.duration,paused:v.paused}}''')
    raw=base64.b64decode(result.pop('image').split(',')[1]);dest=D/(vid+'.png');dest.write_bytes(raw)
    row.update(result,path=str(dest),sha256=hashlib.sha256(raw).hexdigest())
   except Exception as e:row['error']=type(e).__name__+': '+str(e).split('Call log:')[0][:180]
   rows.append(row);(O/'browser_frame0.json').write_text(json.dumps(rows,indent=2)+'\n');print(vid,'saved' if 'path' in row else row['error'],flush=True)
 finally:pg.close()
