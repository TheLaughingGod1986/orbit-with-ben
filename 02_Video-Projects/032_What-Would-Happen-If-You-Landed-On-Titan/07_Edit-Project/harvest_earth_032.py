#!/usr/bin/env python3
"""Harvest NASA's R39 Blue Marble; preserve existing records; no approval implied."""
from pathlib import Path
import json,hashlib,urllib.request
from PIL import Image
base=Path(__file__).resolve().parent
out=Path('/Users/benjaminoats/_desk/cache/J2089/earth_v30');out.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fetch(url,name):
 p=out/name
 if not p.exists():
  data=urllib.request.urlopen(url,timeout=40).read(25*1024*1024+1)
  assert len(data)<=25*1024*1024
  p.write_bytes(data)
 return p
page='https://science.nasa.gov/resource/the-blue-marble/'
url='https://assets.science.nasa.gov/content/dam/science/psd/solar/2023/09/i/IMG004849.jpg'
src=fetch(page,'source.html');assert b'AS17-148-22727' in src.read_bytes()
policy=fetch('https://www.nasa.gov/nasa-brand-center/images-and-media/','nasa_policy.html')
image=fetch(url,'AS17-148-22727.jpg')
with Image.open(image) as im:
 im.load();w,h=im.size
 im.thumbnail((1000,1000));im.convert('RGB').save(out/'inspection.jpg')
record={'asset_id':'AS17-148-22727','title':'The Blue Marble','source_page':page,'download_url':url,'local_path':str(image),'sha256':sha(image),'width':w,'height':h,'bytes':image.stat().st_size,'source_evidence_path':str(src),'source_evidence_sha256':sha(src),'credit':'NASA Johnson Space Center','credit_required':'NASA Johnson Space Center','referenced_rows':[39],'download_status':'downloaded','review_status':'CANDIDATE_NOT_KEEP','licence_status':'NASA_AUTHORED_PHOTOGRAPH_POLICY_EVIDENCE_SAVED_FOR_REVIEW','licence_policy':'https://www.nasa.gov/nasa-brand-center/images-and-media/','policy_evidence_path':str(policy),'policy_evidence_sha256':sha(policy),'licence_basis':'NASA source identifies Apollo 17 astronaut photograph AS17-148-22727 and credits NASA Johnson Space Center. Retain credit; no endorsement. Worker evidence collection, not Chief release.','motion':'STILL_NOT_NATIVE_MOTION','quality_status':'CROP_GRADE_AND_COMPOSITE_REVIEW_REQUIRED','actual_appearance_count':'UNVERIFIED_UNTIL_FINAL_CUT_MANIFEST','proposed_placement':'Preserve complete Earth as inset over graded moving picture; do not stretch square image or crop planet to fill 16:9. Still push is decorative motion only.','short_exclusion':'FINAL_DECODED_FRAME_AND_CROP_COMPARISON_REQUIRED'}
poolpath=base/'HARVEST_POOL_v01.json';pool=json.loads(poolpath.read_text());existing=next((a for a in pool['assets'] if a['asset_id']==record['asset_id']),None)
if existing is None:pool['assets'].append(record)
else:assert existing==record,'Existing record differs; preserve it and investigate'
poolpath.write_text(json.dumps(pool,indent=2)+'\n')
report={'job':'J2089','row':39,'asset':record,'checks':{'source_id_present':True,'image_decodes':True,'source_hash':sha(src),'image_hash':sha(image),'policy_hash':sha(policy)},'limits':['No source rights ruling, KEEP, motion review or film PASS','Final crop, grade, contrast, actual reuse and Short frame exclusion remain required']}
(base/'EARTH_HARVEST_v30.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'path':str(image),'width':w,'height':h,'sha256':sha(image),'preview':str(out/'inspection.jpg')}))
