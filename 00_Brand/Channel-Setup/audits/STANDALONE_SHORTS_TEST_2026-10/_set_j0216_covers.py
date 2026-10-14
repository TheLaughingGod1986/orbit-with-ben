import sys,json,pathlib,time
from datetime import datetime,timezone
from playwright.sync_api import sync_playwright
root=pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0,str(root/'scripts'))
import apply_yellow_white_v04_thumbs as v
v.CDP='http://127.0.0.1:9223'
base=pathlib.Path(__file__).resolve().parent
v.SHOTS=pathlib.Path('/private/tmp/J0216-studio-shots');v.SHOTS.mkdir(exist_ok=True)
manifest=json.loads((base/'08_Covers/MANIFEST.json').read_text())
rows=[]
with sync_playwright() as pw:
 ctx=pw.chromium.connect_over_cdp(v.CDP).contexts[0]
 for n,s in enumerate(manifest['shorts'],1):
  pack=base/'11_Upload-Package'/s['id']
  live=[json.loads(f.read_text()) for f in pack.glob('PACKAGE_UPLOAD_RESULT_*.json') if not json.loads(f.read_text())['dryRun']]
  good=[r for r in live if r['ok'] and r['upload']['platformPostId']]
  if not good: continue
  row=v.apply_one(ctx,{'id':good[-1]['upload']['platformPostId'],'cover':pathlib.Path(s['file']),'related':''},n)
  row['slug']=s['id'];row['at']=datetime.now(timezone.utc).isoformat();rows.append(row)
  (base/'J0216_STUDIO_COVERS.json').write_text(json.dumps({'results':rows},indent=2)+'\n')
  print(json.dumps(row),flush=True)
  if row.get('error')=='BLOCKED_NEED_BEN_LOGIN':break
