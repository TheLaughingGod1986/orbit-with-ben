import json,pathlib,hashlib,datetime,concurrent.futures
root=pathlib.Path('/Users/benjaminoats/YouTube/orbit-with-ben');rel='00_Brand/Channel-Setup/audits/qa_sweeps/J1066_QA_SWEEP_INVENTORY_2026-10-28.json'
x=json.loads((root/rel).read_text());out={'copies_identical':(root/rel).read_bytes()==(pathlib.Path('/Users/benjaminoats/YouTube/History Of Science')/rel).read_bytes(),'files':[],'gate_issues':[],'aliases':[]}
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
tasks=[]
for e in x['entries']:
 if e.get('pack_members'):
  tasks.extend((e['export_id'],m['path'],m['sha256']) for m in e['pack_members'])
 elif e.get('archive_member') or 'stub' in e.get('media_storage_kind',''):pass
 else:tasks.append((e['export_id'],e['media_path'],e['media_sha256']))
 for k in ['picture_qa','polish_gate','music_gate']:
  g=e[k];p=g.get('path')
  if not p:continue
  try:
   raw=pathlib.Path(p).read_text()
   if p.endswith('.json'):
    gd=json.loads(raw)
    if gd.get('verdict')=='FAIL' or gd.get('failed'):out['gate_issues'].append([e['export_id'],k,'FAIL'])
    v=gd.get('video')
    if v and pathlib.Path(v).name!=pathlib.Path(e.get('original_local_media_path',e['media_path'])).name:out['aliases'].append({'id':e['export_id'],'gate':k,'video':v,'exists':pathlib.Path(v).exists()})
   mt=datetime.datetime.fromisoformat(e['media_mtime_utc'].replace('Z','+00:00')).timestamp()
   if pathlib.Path(p).stat().st_mtime+1<mt:out['gate_issues'].append([e['export_id'],k,'stale actual mtime'])
  except Exception as ex:out['gate_issues'].append([e['export_id'],k,str(ex)])
def check(t):
 i,p,h=t
 try:
  a=sha(p);return {'id':i,'path':p,'match':a==h,'actual':a}
 except Exception as ex:return {'id':i,'path':p,'error':str(ex)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 out['files']=list(pool.map(check,tasks))
pathlib.Path('/private/tmp/j1075-evidence.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'copies_identical':out['copies_identical'],'files_checked':len(out['files']),'file_issues':[r for r in out['files'] if not r.get('match')],'gate_issues':out['gate_issues'],'aliases':out['aliases']},indent=2))
