#!/usr/bin/env python3
"""Audit cached source bytes and build a current candidate sheet. No approval."""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw
HERE=Path(__file__).resolve().parent

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 pool=json.loads((HERE/'HARVEST_POOL_v01.json').read_text())
 assets=list(pool['assets'])+[pool['jwst_status']]
 size=json.loads((HERE/'SIZE_MANIFEST_v01.json').read_text())
 for s in size['assets']:
  if s['id'] not in {x['asset_id'] for x in assets}:
   record=dict(asset_id=s['id'],local_path=s['path'],sha256=s['sha256'],referenced_rows=[9],credit=s['credit'],review_status='SEE_J2247')
   metadata=Path(s['path']).with_name(s['id']+'_metadata.json')
   record.update(metadata_path=str(metadata),metadata_sha256=sha(metadata))
   assets.append(record)
 results=[];errors=[]
 sheet=Image.new('RGB',(1200,290*((len(assets)+3)//4)),(32,42,58));draw=ImageDraw.Draw(sheet)
 for i,s in enumerate(assets):
  row={'id':s['asset_id'],'rows':s.get('referenced_rows',[s['row']] if 'row' in s else []),'image_hash':'UNVERIFIED','evidence':[]}
  try:
   assert sha(s['local_path'])==s['sha256'],'image hash mismatch'
   row['image_hash']='MATCH'
   with Image.open(s['local_path']) as im:
    row['dimensions']=list(im.size)
    if 'width' in s:assert list(im.size)==[s['width'],s['height']],'dimension mismatch'
    preview=im.convert('RGB');preview.thumbnail((288,210))
   x=i%4*300;y=i//4*290
   sheet.paste(preview,(x+(300-preview.width)//2,y))
   draw.text((x+6,y+214),s['asset_id']+' R'+','.join(map(str,row['rows'])),fill='white')
   draw.text((x+6,y+233),s.get('review_status','CANDIDATE')[:38],fill='white')
   draw.text((x+6,y+252),'SOURCE ONLY / NOT FINAL COMPOSITE',fill=(240,200,110))
   for field in ['source_evidence','metadata','assets']:
    path=s.get(field+'_path');expected=s.get(field+'_sha256')
    if path and expected:
     assert sha(path)==expected,field+' hash mismatch'
     row['evidence'].append(field+':MATCH')
   row['missing_source_evidence']=not bool(row['evidence'])
  except Exception as e:row['error']=str(e);errors.append(s['asset_id']+': '+str(e))
  results.append(row)
 exports=json.loads((HERE/'J2089_EXPORT_HASHES_v22.json').read_text())['exports']
 for path,expected in exports.items():
  try:assert sha(path)==expected,'hash mismatch'
  except Exception as e:errors.append(path+': '+str(e))
 sheet.save(out/'contact_sheet.jpg',quality=92)
 result={'job':'J2089','status':'MEASUREMENTS_ONLY_NOT_FILM_PASS','assets':results,'exports_checked':len(exports),'errors':errors,'contact_sheet':str(out/'contact_sheet.jpg'),'contact_sheet_sha256':sha(out/'contact_sheet.jpg'),'unverified':['per-asset rights','final crops and actual reuse','Short frame exclusion','motion','composites and final gates']}
 (HERE/'HARVEST_INVENTORY_v23.json').write_text(json.dumps(result,indent=2)+'\n')
 print(f'{len(results)} cached source images; {len(exports)} export hashes; {len(errors)} errors; '+str(sum(r.get('missing_source_evidence',False) for r in results))+' missing source-evidence entries')
 if errors:raise SystemExit(1)
if __name__=='__main__':main()
