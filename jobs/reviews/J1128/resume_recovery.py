import sys,pathlib,json,datetime,shutil,time
ROOT=pathlib.Path('/private/tmp/J1128-wt')
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'jobs/reviews/J1128'))
import nas_offload as no
from verify_archive import verified
from research_metadata import compact
nas=pathlib.Path('/Volumes/data');assert no.nas_ready(nas)[0]
base=nas/'mac-mini-archive/mini-tmp-scratch/2026-10-28'
report={'before':shutil.disk_usage('/Users/benjaminoats').free,'results':[]}
def archive(src,dst,mode):
 before=no.manifest(src)
 if not dst.exists():no.copy_tree(src,dst)
 after=no.manifest(dst)
 assert verified(src,dst,before,after),f'archive mismatch {src}'
 assert no.manifest(src)==before,f'source changed {src}'
 (dst/'SHA256SUMS.txt').write_text(''.join(f'{h}  {k}\n' for k,(_,h) in sorted(after.items())))
 if mode=='move':no.empty_local(src,dst,sum(v[0] for v in before.values())//(1024*1024),datetime.datetime.now().isoformat())
 else:
  for p in src.glob('*.json'):
   old=json.loads(p.read_text());p.write_text(json.dumps(compact(old),ensure_ascii=False)+'\n')
 row={'source':str(src),'archive':str(dst),'mode':mode,'files':len(before),'free_bytes':shutil.disk_usage('/Users/benjaminoats').free}
 report['results'].append(row);print(json.dumps(row),flush=True)
 pathlib.Path('/Users/benjaminoats/_desk/logs/J1128/resumed.json').write_text(json.dumps(report,indent=2))
# These two attempts have already finished and retained the local copy.
archive(pathlib.Path('/Users/benjaminoats/chief_tmp'),base/'chief_tmp','move')
archive(pathlib.Path('/Users/benjaminoats/.local/share/cursor-mac-mini-worker/artifacts'),base/'artifacts','move')
for job,folder in [('J1107','details'),('j1106','details'),('j1106','extra_details')]:
 src=pathlib.Path('/Users/benjaminoats/_desk')/job/'competitors'/folder
 dst=base/f'J1128-{job}-{folder}'
 archive(src,dst,'compact')
# Never race the original worker's third archive.
while not pathlib.Path('/Users/benjaminoats/_desk/logs/J1128-recover.done').exists():time.sleep(10)
rows=json.loads(pathlib.Path('/Users/benjaminoats/_desk/logs/J1128/recovery.json').read_text())['moves']
for row in rows:
 if 'cursor-mac-mini-hos-worker' in row['path'] and not row['ok']:
  archive(pathlib.Path(row['path']),pathlib.Path(row['nas']),'move')
print('COMPLETE',shutil.disk_usage('/Users/benjaminoats').free,flush=True)
