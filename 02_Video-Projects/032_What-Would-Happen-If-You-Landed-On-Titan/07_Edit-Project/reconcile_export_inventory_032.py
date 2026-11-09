import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
files=['OVERLAY_MANIFEST_v01.json','DATA_MANIFEST_v02.json','MECHANISM_RENDER_MANIFEST_v01.json','MECHANISM_FIX_RENDER_MANIFEST_v01.json','PROCESS_RENDER_MANIFEST_v03.json','SIZE_RENDER_MANIFEST_v01.json','OCEAN_RENDER_MANIFEST_v01.json','ORBIT_PERIOD_RENDER_MANIFEST_v01.json','DISTANCE_RENDER_MANIFEST_v01.json','PEBBLE_RULER_RENDER_MANIFEST_v01.json','LANDING_RECORD_RENDER_MANIFEST_v01.json','URANUS_RENDER_MANIFEST_v01.json']
records={}; conflicts=[]
for n in files:
 d=json.loads((p/n).read_text())
 for r in d.get('clips',[d]):
  if not r.get('render'): continue
  old=records.get(r['id'])
  records[r['id']]={k:r.get(k) for k in ['id','row','render','sha256','review_ref','review_refs']}
  records[r['id']]['manifest']=n
  records[r['id']]['sha256']=r.get('sha256',r.get('render_sha256'))
  if old and old['render']!=r['render']: conflicts.append({'id':r['id'],'earlier':old['render'],'current':r['render'],'reason':'Later correction manifest takes precedence in inventory only; no new approval'})
comp_by_id={}
comp_manifest_p=p/'COMPOSITES_MANIFEST_v01.json'
if comp_manifest_p.is_file():
 cm=json.loads(comp_manifest_p.read_text())
 comp_by_id={c['id']:c for c in cm.get('composites',[])}
 nas_exports_dir=Path(cm.get('nas_exports_dir',''))
for r in records.values():
 path=Path(r['render']); r['exists']=path.is_file(); r['actual_sha256']=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
 r['hash_matches']=r['actual_sha256']==r['sha256']; r['composite_approval']='NOT_INFERRED_FROM_RENDER'
 if r['id'] in comp_by_id:
  c=comp_by_id[r['id']]
  r['nas_render']=str(nas_exports_dir/path.name)
  r['composite_mp4']=c['video']
  r['composite_sha256']=c['sha256']
  r['background_asset_id']=c['asset_id']
  r['background_mode']=c['mode']
assert all(r['hash_matches'] for r in records.values())
prior=json.loads((p/'J2089_EXPORT_HASHES_v22.json').read_text())['exports']
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in prior.items())
out={'job':'J2089','scope':'Current manifest inventory; file presence and SHA256 only','rendered_unique_ids':len(records),'rendered_unique_files':len({r['render'] for r in records.values()}),'historical_preserved_files':len(prior),'superseded_manifest_allocations':conflicts,'exports':sorted(records.values(),key=lambda r:(r['row'],r['id'])),'limits':['No perceived audio or motion review','No final composite or source-rights approval','No film-stage completion; licensed harvest still incomplete']}
(p/'CURRENT_EXPORT_INVENTORY_v31.json').write_text(json.dumps(out,indent=2)+'\n')
g=json.loads((p/'GRAPHICS_COVERAGE_v01.json').read_text())
g['current_export_inventory']='CURRENT_EXPORT_INVENTORY_v31.json'
g['legacy_fields_notice']='remaining_builds, mechanism_note and process_note describe historical build stages only; consult current_export_inventory for rendered files. They do not imply final composite approval.'
g['current_rendered_ids']=[r['id'] for r in out['exports']]
g['current_hash_verified_export_count']=len(records)
(p/'GRAPHICS_COVERAGE_v01.json').write_text(json.dumps(g,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['exports','superseded_manifest_allocations']},indent=2))
