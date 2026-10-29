import sys,pathlib,json,datetime,shutil,subprocess,os
sys.path.insert(0,'/private/tmp/J1128-wt/scripts')
import nas_offload as no
nas=pathlib.Path('/Volumes/data'); now=datetime.datetime.now(datetime.timezone.utc); date=now.date().isoformat()
assert no.nas_ready(nas)[0]
log=pathlib.Path('/Users/benjaminoats/_desk/logs/J1128');log.mkdir(exist_ok=True)
report={'before':shutil.disk_usage('/Users/benjaminoats').free,'moves':[]}
# Explicitly selected obsolete scratch, all unchanged for more than 48 h. No worktrees or UAT directories.
for name in ['/Users/benjaminoats/chief_tmp','/Users/benjaminoats/.local/share/cursor-mac-mini-worker/artifacts','/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts']:
 p=pathlib.Path(name);size,newest=no.scan(p)
 assert now.timestamp()-newest>48*3600,(name,newest)
 r=no.offload_one(p,nas,date,now.isoformat());report['moves'].append(r)
 print(json.dumps(r),flush=True)
report['after']=shutil.disk_usage('/Users/benjaminoats').free
(log/'recovery.json').write_text(json.dumps(report,indent=2))
