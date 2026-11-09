import concurrent.futures as cf,json,pathlib,subprocess,datetime
O=pathlib.Path(__file__).parent
qs=['The Last Star: What Happens When a Red Dwarf Dies?','What Happens During the Milky Way Andromeda Collision?','How Long Will Anything in Space Last?']
def run(q):
 p=subprocess.run(['yt-dlp','--flat-playlist','--dump-single-json','ytsearch10:'+q],capture_output=True,text=True,timeout=90)
 if p.returncode:return {'query':q,'error':p.stderr[-500:]}
 j=json.loads(p.stdout)
 return {'query':q,'url':'https://www.youtube.com/results?search_query='+__import__('urllib.parse',fromlist=['quote']).quote(q),'results':[{'rank':i+1,'id':e.get('id'),'title':e.get('title'),'channel':e.get('channel'),'channel_id':e.get('channel_id'),'channel_url':e.get('channel_url'),'url':e.get('url')} for i,e in enumerate(j.get('entries',[]))]}
with cf.ThreadPoolExecutor(max_workers=3) as ex: rows=list(ex.map(run,qs))
(O/'search.json').write_text(json.dumps({'read_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'three provisional design candidates only; nonpersonalized yt-dlp search, not universal ranking','queries':rows},indent=2));print(json.dumps(rows,indent=2))
