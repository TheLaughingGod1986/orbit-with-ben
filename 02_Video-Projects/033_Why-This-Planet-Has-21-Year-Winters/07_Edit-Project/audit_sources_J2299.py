#!/usr/bin/env python3
"""Recheck official NASA identity records; recover draft harvest bytes without approving them."""
import concurrent.futures, hashlib, io, json, pathlib, re, urllib.request, urllib.parse, subprocess
from PIL import Image
HERE=pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path('/Users/benjaminoats/_desk/cache/J2299')
OUT.mkdir(parents=True,exist_ok=True)
UA='OrbitWithBenStudio/1.0 source identity audit'
def get(url):
 req=urllib.request.Request(url.replace('http://','https://'),headers={'User-Agent':UA})
 with urllib.request.urlopen(req,timeout=35) as r:return r.read()
def record(ident):
 try:
  url='https://images-api.nasa.gov/search?'+urllib.parse.urlencode({'nasa_id':ident})
  data=get(url); (OUT/(ident+'_record.json')).write_bytes(data)
  items=json.loads(data)['collection']['items']
  exact=[i for i in items if i['data'][0].get('nasa_id')==ident]
  if len(exact)!=1:raise ValueError('exact record count '+str(len(exact)))
  item=exact[0];d=item['data'][0]
  return {'canonical_id':ident,'source_api':url,'record_sha256':hashlib.sha256(data).hexdigest(),'metadata':d,'asset_manifest_url':item.get('href'),'status':'IDENTITY_RECORD_ONLY_NOT_KEEP'}
 except Exception as e:return {'canonical_id':ident,'status':'UNRESOLVED','error':str(e)}
def recover(a):
 r={'canonical_id':a['canonical_id'],'source_page':a.get('source_page'),'download_url':a.get('download_url'),'expected_sha256':a.get('sha256'),'catalogue_title_from_draft':a.get('catalogue_title'),'credit_from_draft':a.get('credit'),'licence_from_draft':a.get('licence'),'status':'NOT_KEEP'}
 try:
  dest=OUT/'harvest'/pathlib.Path(a['local_path']).name;dest.parent.mkdir(exist_ok=True)
  data=dest.read_bytes() if dest.exists() else get(a['download_url'])
  actual=hashlib.sha256(data).hexdigest()
  if actual!=a['sha256']:raise ValueError('download hash differs from J2290: '+actual)
  dest.write_bytes(data)
  im=Image.open(io.BytesIO(data));r.update(local_path=str(dest),sha256=actual,bytes=len(data),dimensions=list(im.size),status='BYTES_VERIFIED_NOT_KEEP')
 except Exception as e:r['error']=str(e)
 return r
if __name__=='__main__':
 draft_path=HERE/'HARVEST_MANIFEST_J2290.json'
 draft=json.loads(draft_path.read_text() if draft_path.exists() else subprocess.check_output(['git','show','adab48f716e066f57e2e1c9f56c3de789dda854e:'+str(draft_path.relative_to(HERE.parents[2]))],text=True))
 lock=(HERE/'STILLS_LOCK_v01.md').read_text();shot=(HERE/'SHOT_LIST_v01.md').read_text()
 ids=sorted(set(re.findall(r'PIA\d{5}',lock+shot)))
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
  records=list(ex.map(record,ids));harvest=list(ex.map(recover,draft['assets']))
 result={'job':'J2299','draft_ref':'adab48f716e066f57e2e1c9f56c3de789dda854e','source_records':records,'recovered_harvest':harvest,'summary':{'nasa_ids_checked':len(ids),'exact_records':sum(r['status']!='UNRESOLVED' for r in records),'harvest_requested':len(harvest),'hash_verified':sum(r['status']=='BYTES_VERIFIED_NOT_KEEP' for r in harvest)},'warning':'Identity and byte verification only. Terms, visual suitability and row assignment require review. No KEEP or motion approval.'}
 (HERE/'SOURCE_AUDIT_J2299_v01.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result['summary']))
