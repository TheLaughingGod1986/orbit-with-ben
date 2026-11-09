#!/usr/bin/env python3
"""Save per-asset landing pages and credit evidence; never grants KEEP or rights."""
import concurrent.futures,hashlib,html,json,re,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=Path('/Users/benjaminoats/_desk/cache/J2089/harvest_v03')
def fetch(u):
 r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'OrbitWithBen source verification'}),timeout=30)
 return r.url,r.read()
def sha(b):return hashlib.sha256(b).hexdigest()
def one(a):
 try:
  url,raw=fetch('https://photojournal.jpl.nasa.gov/catalog/'+a['asset_id'])
  path=OUT/(a['asset_id']+'_source.html');path.write_bytes(raw)
  s=raw.decode();credit=re.search(r'<div[^>]*class="hds-credits[^>]*>(.*?)</div>',s,re.S)
  credit=html.unescape(re.sub('<[^>]+>',' ',credit.group(1))) if credit else ''
  credit=' '.join(credit.split());a.update(source_page=url,source_evidence_path=str(path),source_evidence_sha256=sha(raw),page_credit=credit)
  # NASA's site contains unrelated recommendation tiles. Only the asset's own credit
  # is recorded; a search across whole HTML is not a copyright determination.
  a['licence_policy']='https://www.jpl.nasa.gov/jpl-image-use-policy/'
  a['licence_basis']='JPL image-use policy: reuse subject to asset-specific ownership/credit and special cases. Not a blanket public-domain declaration.'
  a['licence_status']='CREDIT_CHECKED_THIRD_PARTY_TERMS_STILL_TO_CONFIRM' if any(t in (credit+a.get('credit','')) for t in ['ESA','ASI','DLR','University','Cornell','Institute']) else 'NASA_JPL_REUSE_POLICY_CREDIT_REQUIRED'
  a['credit_required']=a.get('credit') or credit
  a['quality_status']='CANDIDATE_CROP_AND_COMPOSITE_REVIEW_REQUIRED'
 except Exception as e:a['page_audit_error']=str(e)
 return a
if __name__=='__main__':
 p=HERE/'HARVEST_POOL_v01.json';pool=json.loads(p.read_text())
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:pool['assets']=list(ex.map(one,pool['assets']))
 for label,u in [('JPL_IMAGE_USE','https://www.jpl.nasa.gov/jpl-image-use-policy/'),('NASA_MEDIA_USE','https://www.nasa.gov/nasa-brand-center/images-and-media/')]:
  try:
   _,b=fetch(u);(OUT/(label+'.html')).write_bytes(b)
  except Exception as e:print(label,e)
 pool['source_review_ref']='jobs/reviews/J2090/REVIEW.md'
 pool['excluded_short_asset_ids']=['PIA14925','PIA06230','PIA09739','PIA21625']
 pool['source_audit_note']='Old flags are historical v02 findings, not blanket rejection of corrected v03 sources. Per-asset source evidence now saved.'
 p.write_text(json.dumps(pool,indent=2)+'\n')
 print('Landing pages saved:',sum('source_evidence_path'in a for a in pool['assets']))
