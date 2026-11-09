#!/usr/bin/env python3
"""Resumable initial J2141 NASA harvest. £0. Candidates require Chief acceptance.
Media and original API/usage evidence are written outside git; JSON records hashes.
"""
import argparse, hashlib, json
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageOps

ITEMS = [
 ('PIA00407',[38,44],'Mars global views; inspect layout before selecting single globe.'),
 ('PIA20016',[54],'QUARANTINE: infrared composite, not the natural-colour Titan beside Saturn requested by R54.'),
 ('PIA14909',[54],'True-colour Titan in front of Saturn; not the isolated haze limb described for R54b.'),
 ('GSFC_20171208_Archive_e001788',[],'Earth texture candidate only; not a replacement for locked DSCOVR moving sequence.')]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def get(url):
 r=requests.get(url,timeout=45);r.raise_for_status();return r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--media-root',type=Path,required=True);ap.add_argument('--manifest',type=Path,required=True);a=ap.parse_args()
 a.media_root.mkdir(parents=True,exist_ok=True); records=[]
 policy='https://www.nasa.gov/nasa-brand-center/images-and-media/'
 p=a.media_root/'NASA_MEDIA_POLICY.html';p.write_bytes(get(policy).content)
 for ident,rows,note in ITEMS:
  url='https://images-api.nasa.gov/search?nasa_id='+ident
  body=get(url).json();item=next(x for x in body['collection']['items'] if x['data'][0]['nasa_id']==ident);d=item['data'][0]
  evidence=a.media_root/(ident+'_api.json');evidence.write_text(json.dumps(body,indent=2))
  link=next(x for x in item['links'] if x.get('rel')=='canonical');u=link['href'];f=a.media_root/(ident+'.jpg')
  if not f.exists():f.write_bytes(get(u).content)
  with Image.open(f) as im:im.verify()
  with Image.open(f) as im: w,h=im.size
  rec=dict(asset_id=ident,title=d['title'],description=d.get('description'),source_page='https://images.nasa.gov/details/'+ident,source_api=url,source_url=u,credit=d.get('secondary_creator',d.get('center')),local_path=str(f),sha256=sha(f),bytes=f.stat().st_size,width=w,height=h,rows=rows,download_status='downloaded',review_status='pending_chief_review',review_note=note,licence_status='pending_per_asset_rights_check',licence_policy=policy,licence_evidence_path=str(p),licence_evidence_sha256=sha(p),source_evidence_path=str(evidence),source_evidence_sha256=sha(evidence),generation_authorized=False)
  if ident=='PIA00407':rec['licence_status']='US_federal_NASA_JPL_USGS_material_subject_to_NASA_media_conditions'
  records.append(rec)
 sheet=Image.new('RGB',(1280,800),(30,45,65));draw=ImageDraw.Draw(sheet)
 for i,r in enumerate(records):
  im=Image.open(r['local_path']).convert('RGB');im.thumbnail((600,320));x=(i%2)*640;y=(i//2)*400;sheet.paste(im,(x+(640-im.width)//2,y));draw.text((x+16,y+330),r['asset_id']+' | '+r['title'][:45],fill='white')
 out=a.media_root/'contact_sheet.jpg';sheet.save(out,quality=92)
 a.manifest.write_text(json.dumps(dict(job='J2141',status='partial_harvest_not_KEEP',spend_gbp=0,assets=records,contact_sheet=str(out),contact_sheet_sha256=sha(out)),indent=2)+'\n')
 print('Downloaded',len(records),'candidates; manifest',a.manifest)
if __name__=='__main__':main()
