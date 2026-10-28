import sys,pathlib,json,datetime,shutil
sys.path.insert(0,'/private/tmp/J1128-wt/scripts')
import nas_offload as no
from research_metadata import compact
nas=pathlib.Path('/Volumes/data');assert no.nas_ready(nas)[0]
report=[]
for job,folder in [('J1107','details'),('j1106','details'),('j1106','extra_details')]:
 src=pathlib.Path('/Users/benjaminoats/_desk')/job/'competitors'/folder
 dst=no.dest_for(src,nas,datetime.date.today().isoformat())
 # Give each research archive a unique, identifiable name.
 dst=dst.with_name('J1128-'+job+'-'+dst.name)
 assert not dst.exists()
 before=no.manifest(src);no.copy_tree(src,dst);assert no.manifest(dst)==before;assert no.manifest(src)==before
 (dst/'SHA256SUMS.txt').write_text(''.join(f'{h}  {k}\n' for k,(_,h) in sorted(before.items())))
 saved=0;count=0
 for p in src.glob('*.json'):
  old=p.read_bytes();j=json.loads(old);new=(json.dumps(compact(j),ensure_ascii=False)+'\n').encode()
  p.write_bytes(new);saved+=len(old)-len(new);count+=1
 row={'source':str(src),'nas_originals':str(dst),'files':count,'saved_bytes':saved};report.append(row);print(json.dumps(row),flush=True)
# Fix the actual resumable collectors, retaining the same fields they read.
for job in ['J1107','j1106']:
 base=pathlib.Path('/Users/benjaminoats/_desk')/job/'competitors'
 for name in ['collect.py','extra_study.py']:
  p=base/name
  if not p.exists():continue
  s=p.read_text()
  if 'def compact_research(' not in s:
   helper='\ndef compact_research(j):\n return {k:v for k,v in j.items() if k in '+repr(sorted(__import__('research_metadata').FIELDS))+'}\n'
   # insert before first function definition, after imports/initialisation
   at=s.index('\ndef ');s=s[:at]+helper+s[at:]
   if name=='collect.py':
    s=s.replace("j=json.loads(p.stdout);path.write_text(json.dumps(j));return j", "j=json.loads(p.stdout);j=compact_research(j) if path.parent.name == 'details' else j;path.write_text(json.dumps(j));return j")
   else:s=s.replace('dest.write_text(json.dumps(j))','j=compact_research(j);dest.write_text(json.dumps(j))')
   p.write_text(s)
  compile(s,str(p),'exec')
  target=pathlib.Path('/private/tmp/J1128-wt/jobs/reviews/J1128/collectors')/job/name
  target.parent.mkdir(parents=True,exist_ok=True);target.write_text(s)
pathlib.Path('/Users/benjaminoats/_desk/logs/J1128/compact.json').write_text(json.dumps(report,indent=2))
