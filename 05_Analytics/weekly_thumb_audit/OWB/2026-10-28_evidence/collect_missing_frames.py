import concurrent.futures as cf,datetime as dt,hashlib,json,pathlib,subprocess
O=pathlib.Path(__file__).parent; R=pathlib.Path('/Users/benjaminoats/YouTube/orbit-with-ben');D=O/'fresh_frame0';D.mkdir(exist_ok=True)
f=json.loads((O/'frame0_inventory.json').read_text()); vids={v['id']:v for v in json.loads((O/'inventory_raw.json').read_text())['videos']};u=json.loads((R/'00_Brand/Channel-Setup/social/UPLOADS.json').read_text())['videos']
def run(x):
 vid=x['id'];out=D/f'{vid}.png';v=vids[vid];source='public YouTube stream';data={'id':vid,'read_at':dt.datetime.now(dt.timezone.utc).isoformat()}
 try:
  if v['status']['privacyStatus']=='public':
   p=subprocess.run(['yt-dlp','--no-warnings','-f','best[height<=720][ext=mp4]/best[height<=720]','--get-url',f'https://www.youtube.com/watch?v={vid}'],capture_output=True,text=True,timeout=90)
   if p.returncode: raise RuntimeError('yt-dlp failed: '+p.stderr[-200:])
   inp=p.stdout.strip().splitlines()[0]
  else:
   path=pathlib.Path(u.get(vid,{}).get('file','/nonexistent'));path=path if path.is_absolute() else R/path
   if not path.is_file():raise RuntimeError('No accessible registered master; scheduled stream not requested')
   inp=str(path);source='registered local master: '+inp
  p=subprocess.run(['ffmpeg','-v','error','-y','-i',inp,'-frames:v','1',str(out)],capture_output=True,timeout=60)
  if p.returncode:raise RuntimeError('ffmpeg failed; signed URL deliberately omitted')
  from PIL import Image
  with Image.open(out) as im: size=im.size
  data.update(source=source,path=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),size=size)
 except Exception as e: data['error']=str(e)
 print(vid,'OK' if 'path' in data else data['error'],flush=True);return data
with cf.ThreadPoolExecutor(max_workers=4) as ex: rows=list(ex.map(run,[x for x in f if not x['file_exists']]))
(O/'fresh_frame0.json').write_text(json.dumps(rows,indent=2))
