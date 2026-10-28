import pathlib,sys,json,datetime,shutil
ROOT=pathlib.Path('/private/tmp/J1128-wt')
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'jobs/reviews/J1128')]
import nas_offload as no
from verify_archive import verified
names=['j0935_mon09_v02','j0935_mon09_v03','j0935_wed11_v03','j0935_wed11_v04','j0935_thu12_v03','j0935_fri13_v03']
assert no.nas_ready()[0]
rep={'before':shutil.disk_usage('/').free,'moves':[]}
for name in names:
 src=pathlib.Path('/private/tmp')/name
 before=no.manifest(src)
 assert before
 _,newest=no.scan(src)
 assert datetime.datetime.now().timestamp()-newest>48*3600
 dst=no.dest_for(src,no.NAS_MOUNT,'2026-10-28')
 no.copy_tree(src,dst)
 after=no.manifest(dst)
 assert verified(src,dst,before,after),name
 assert no.manifest(src)==before,name
 (dst/'SHA256SUMS.txt').write_text(''.join(f'{h}  {k}\n' for k,(_,h) in sorted(after.items())))
 no.empty_local(src,dst,sum(v[0] for v in before.values())//1048576,datetime.datetime.now().isoformat())
 rep['moves'].append({'source':str(src),'archive':str(dst),'files':len(before),'bytes':sum(v[0] for v in before.values())})
 rep['after']=shutil.disk_usage('/').free
 pathlib.Path('/Users/benjaminoats/_desk/logs/J1128/final-scratch.json').write_text(json.dumps(rep,indent=2))
 print(name,rep['after'],flush=True)
print('COMPLETE',rep['after'],flush=True)
