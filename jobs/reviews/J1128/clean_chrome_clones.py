"""Clear only old unused macOS Chrome code-sign cache clones; never profiles."""
import datetime,json,os,pathlib,shutil,subprocess,time,argparse
ROOT=pathlib.Path('/private/var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/X/com.google.Chrome.code_sign_clone')
def candidates(root,active,now):
 return [p for p in root.iterdir() if p.name.startswith('code_sign_clone.') and not p.is_symlink() and p.is_dir() and now-p.stat().st_mtime>6*3600 and (p/'Google Chrome.app.bundle').is_dir() and not any(str(p)+'/' in x for x in active)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');a=ap.parse_args()
 r=subprocess.run(['lsof','-n','-d','txt','-Fn'],capture_output=True,text=True)
 if r.returncode or len(r.stdout.splitlines())<100:raise RuntimeError('active executable inventory failed; retain all clones')
 active=[x[1:] for x in r.stdout.splitlines() if x.startswith('n/')]
 rows=candidates(ROOT,active,time.time()); rep={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before':shutil.disk_usage('/').free,'selected':[str(p) for p in rows],'removed':[]}
 out=pathlib.Path('/Users/benjaminoats/_desk/logs/J1128/chrome-clones.json')
 out.write_text(json.dumps(rep,indent=2));print('selected',len(rows),flush=True)
 if a.apply:
  for p in rows:
   # Recheck active executable references immediately before each removal.
   q=subprocess.run(['lsof','-n','-d','txt','-Fn'],capture_output=True,text=True)
   if q.returncode:raise RuntimeError('lsof failed; stopped')
   if str(p)+'/' in q.stdout:continue
   shutil.rmtree(p);rep['removed'].append(str(p));rep['after']=shutil.disk_usage('/').free
   out.write_text(json.dumps(rep,indent=2));print(len(rep['removed']),rep['after'],flush=True)
 rep['after']=shutil.disk_usage('/').free;out.write_text(json.dumps(rep,indent=2));print('complete',rep['after'],flush=True)
if __name__=='__main__':main()
