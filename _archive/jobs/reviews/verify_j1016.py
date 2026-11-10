"""Read-only independent checks. Run from the media-bearing OWB checkout."""
import hashlib, importlib.util, json
from pathlib import Path
ROOT = Path.cwd()
mp = ROOT / 'jobs/reviews/J0936_v04_PREP_v03_maps.json'
x = json.loads(mp.read_bytes())
spec = importlib.util.spec_from_file_location('gate', ROOT / '00_Brand/Channel-Setup/tools/gate_shorts_open.py')
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
out = {'maps_sha256': hashlib.sha256(mp.read_bytes()).hexdigest(), 'shorts': {}}
old = json.loads((ROOT / 'jobs/reviews/J0936_v04_PREP_v02_maps.json').read_text())
for sid,s in x['shorts'].items():
 v=s['vo_splice_map']; errs=[]
 for r in v['subspans']:
  for w in r['words']:
   for a,b in [('start','src_start'),('end','src_end')]:
    expected=r['timeline_start']+(w[b]-r['source_in'])/r['tempo']
    if abs(w[a]-expected)>.002: errs.append([r['span_index'],w['word'],a,w[a],expected])
 auditions={}
 for k,a in v['auditions'].items():
  p=Path(a['wav_path']);auditions[k]={'exists':p.exists(),'hash_matches':p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256']}
 f=s['frame0_gate_verification']; mismatch=[]
 for e in f['compared_library_entries']:
  actual=(int(f['dhash_0_3s'],16)^int(e['dhash'],16)).bit_count()
  if actual != e['hamming_bits']: mismatch.append(e['id'])
 row={'word_output_coordinate_errors':errs,'auditions':auditions,'stored_hash_distance_errors':mismatch,'words':[v['whitespace_words'],v['spoken_words']],'duration_s':v['total_duration_s']}
 p=Path('/Users/benjaminoats/_desk/reviews/J1015/openings')/(sid+'_open.mp4')
 if p.exists():
  row['measured_opening']={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dhash':f'{g.dhash(p):016x}','motion':g.motion_first_second(p),'sustained_difference':g.frame0_diff_0_1_5s(p)}
 if 'test_a_exemption' in s:
  row['test_a_subspans_equal_v02']=v['subspans']==old['shorts'][sid]['vo_splice_map']['subspans']
 out['shorts'][sid]=row
s=x['shorts']['S5_028_jJ5LkFGyzLI'];out['scale_card_timing']={'card':s['single_teaching_overlay']['card_text'],'card_in':16.0,'card_out':19.8,'spoken_fifth_start':20.08,'spoken_light_year_start':20.56,'matches_spoken_line':False}
out['limits']='No listening/prosody PASS; no full-window video/OCR PASS. Supplied verifier asserts stored pixel metrics, not fresh measurements. Stored dHash arithmetic is not proof that preview and source agree.'
print(json.dumps(out,indent=2))
