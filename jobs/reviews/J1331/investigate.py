"""Bounded, read-only J1331 records. No upload/materialise/cleanup calls."""
from pathlib import Path
import csv, datetime, hashlib, json, os, re, subprocess

ROOT = Path('/Users/benjaminoats/YouTube/orbit-with-ben')
OUT = Path(__file__).parent
ICLOUD = Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs'
FAMILIES = ['/private/tmp/J1321-media', '/private/tmp/J1321-render', '/private/tmp/J1324-render']
def save(name, obj):
    (OUT/name).write_text(json.dumps(obj, indent=2)+'\n')
def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def measure():
    files=[]
    for root in FAMILIES:
        for dp, ds, fs in os.walk(root, followlinks=False):
            ds[:]=[d for d in ds if not Path(dp,d).is_symlink()]
            for f in fs:
                p=Path(dp,f); s=p.lstat()
                files.append({'path':str(p),'bytes':s.st_size,'allocated_bytes':s.st_blocks*512,'symlink':p.is_symlink(),'decision':'KEEP','reference':'J1329 result: AR2 v08 picture FIX; J1321/J1324 acceptance unresolved'})
    return {'at':stamp(),'df':subprocess.check_output(['df','-k',str(ROOT)],text=True),'files':files,'family_allocations':{r:sum(f['allocated_bytes'] for f in files if f['path'].startswith(r+'/')) for r in FAMILIES}}
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
    return h.hexdigest()

first=measure(); save('measurements.json',{'first':first})
original=list(csv.DictReader((ROOT/'jobs/reviews/J1326/file_decisions.csv').open()))
candidates=[r for r in original if str(ROOT/'OWB UAT')+'/' in r['exact_path']]
assert len(candidates)==120
q=json.loads((ROOT/'jobs/queue.json').read_text())['jobs']
# Read only tracked text in the relevant film, queue records, watch register and social manifests.
tracked=subprocess.check_output(['git','ls-files','jobs','02_Video-Projects/029_Is-Betelgeuse-About-To-Explode','05_Analytics/kanban','00_Brand/Channel-Setup/social'],cwd=ROOT,text=True).splitlines()
texts={}
for name in tracked:
    p=ROOT/name
    if p.suffix in ('.json','.md','.py','.csv','.txt') and p.is_file() and p.stat().st_size<12_000_000 and not name.startswith('jobs/reviews/J1326/'):
        texts[name]=p.read_text(errors='replace').splitlines()
regs={}
for p in [ROOT/'05_Analytics/kanban/watch_uploads.json',Path.home()/'.config/studio-kanban/watch_uploads.json']:
    regs[str(p)]={k:v for k,v in json.loads(p.read_text()).get('files',{}).items() if '029_short' in k}
save('watch_registers.json',regs)
rows=[]
for c in candidates:
    p=Path(c['exact_path']); rel=p.relative_to(ROOT).as_posix()
    stem=re.search(r'029_short_.+?_v\d+',p.name).group(0)
    refs=[]
    for name,lines in texts.items():
        hits=[i+1 for i,line in enumerate(lines) if stem in line]
        if hits: refs.append({'file':name,'lines':hits[:30],'match':stem})
    cloud=ICLOUD/rel
    s=p.lstat()
    # Preserve version/history records regardless of which physical copy the card resolves to.
    version=re.search(r'_v(\d+)',stem).group(1)
    role='current repaired/uploaded v04 package (J0961/J0991)' if version=='04' else 'preceding watch v03 package (J0961 approval history)' if version=='03' else 'earlier upload/watch/rebuild history; exclusions not cleared by version age'
    rows.append({'exact_path':str(p),'allocated_bytes':s.st_blocks*512,'bytes':s.st_size,'decision':'KEEP','reason':role,'references':refs,'cloud_equivalent':str(cloud),'cloud_exists':cloud.is_file(),'relative_ask_resolution':str(cloud) if cloud.is_file() else str(p),'resolution_caveat':'ask_watch tries CloudDocs first, then publisher ROOT, then main checkout; no function invoked (would auto-upload). Nested paths require their exact relative key. R2 playback does not read this local file.','symlink':p.is_symlink()})
groups={}
for row in rows:
    refs=row.pop('references')
    key=refs[0]['match'] if refs else Path(row['exact_path']).name
    groups[key]=refs
    row['reference_group']=key
save('reference_groups.json',groups)
save('candidate_decisions.json',rows)
save('queue_dependencies.json',[{k:j.get(k) for k in ['id','title','status','remaining_action','result','progress','waiting_on']} for j in q if j['id'] in ['J1100','J1213','J1241','J1320','J1321','J1322','J1324','J1329'] or (j.get('status') not in ['done','cancelled'] and 'AR2' in json.dumps(j))])
old=json.loads((ROOT/'jobs/reviews/J1326/uat_hash_proof.json').read_text())
proof=[]
for row in old['files']:
    p=Path(row['source']); h=sha(p)
    copies=[]
    for c in row['copies']:
        dest=Path(c['path'])
        try:
            dh=sha(dest); copies.append({'path':str(dest),'sha256':dh,'match':dh==h,'bytes':dest.stat().st_size})
        except OSError as e: copies.append({'path':str(dest),'error':type(e).__name__})
    proof.append({'source':str(p),'sha256':h,'matches_J1326':h==row['sha256'],'bytes':p.stat().st_size,'allocated_bytes':p.stat().st_blocks*512,'copies':copies,'decision':'KEEP','reference':'candidate_decisions.json exact source; watch/upload/current/previous/rebuild exclusions not waived'})
save('media_hashes.json',{'at':stamp(),'nas_df':subprocess.check_output(['df','-k','/Volumes/data'],text=True),'files':proof})
second=measure(); save('measurements.json',{'first':first,'second':second})
save('proposal.json',{'allowlist':[],'proposed_recoverable_bytes':0,'all_120':'KEEP','scratch':'KEEP all three families pending picture acceptance','authority':'Records only; elected Chief must rule on any recovery. No J1100 restart or J1322 change.'})
print(json.dumps({'candidates':len(rows),'allocated_bytes':sum(r['allocated_bytes'] for r in rows),'no_reference':sum(not groups[r['reference_group']] for r in rows),'media_proofs':len(proof),'all_match':all(any(c.get('match') for c in r['copies']) for r in proof),'family_allocations':second['family_allocations'],'df':second['df']}))
