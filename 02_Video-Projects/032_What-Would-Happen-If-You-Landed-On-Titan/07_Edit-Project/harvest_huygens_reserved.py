#!/usr/bin/env python3
"""Download only J2177's two reserved DISR mosaics; no motion or KEEP claim."""
import argparse, hashlib, json, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw
HERE=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'OrbitWithBen source verification'}),timeout=35) as r: return r.read()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);records=[]
    for nid,row in [('PIA07870',16),('PIA07871',51)]:
        meta_path=out/(nid+'_metadata.json');meta_path.write_bytes(fetch('https://images-api.nasa.gov/search?nasa_id='+nid))
        items=json.loads(meta_path.read_bytes())['collection']['items']
        item=next(i for i in items if i['data'][0]['nasa_id']==nid);meta=item['data'][0]
        assets_path=out/(nid+'_assets.json');assets_path.write_bytes(fetch(item['href']))
        links=json.loads(assets_path.read_bytes());url=next(u for u in links if '~orig' in u and u.lower().endswith(('.jpg','.png','.jpeg')))
        p=out/(nid+Path(url).suffix)
        if not p.exists():p.write_bytes(fetch(url))
        with Image.open(p) as im:
            size=im.size;im.verify()
        records.append({'asset_id':nid,'reserved_row':row,'title':meta['title'],'description':meta.get('description',''),'credit':meta.get('secondary_creator',''),'source_page':'https://images.nasa.gov/details/'+nid,'download_url':url,'local_path':str(p),'sha256':sha(p),'width':size[0],'height':size[1],'metadata_path':str(meta_path),'metadata_sha256':sha(meta_path),'assets_path':str(assets_path),'assets_sha256':sha(assets_path),'status':'CANDIDATE_NOT_KEEP','rights_status':'CREDIT_RECORDED_PER_ASSET_TERMS_REVIEW_REQUIRED','motion':'STILL_NOT_NATIVE_MOTION','short_exclusion':'FINAL_CROP_COMPARISON_REQUIRED'})
        print(nid,meta['title'],size,meta.get('secondary_creator',''))
    sheet=Image.new('RGB',(1600,1000),(30,37,51));d=ImageDraw.Draw(sheet)
    for i,r in enumerate(records):
        with Image.open(r['local_path']) as im:
            im=im.convert('RGB');im.thumbnail((780,900));sheet.paste(im,(i*800+(800-im.width)//2,40))
        d.text((i*800+10,10),r['asset_id']+' '+r['title'][:55],fill='white')
    sheet.save(out/'contact_sheet.jpg',quality=94)
    result={'job':'J2089','review_allocation':'J2177 / SHOT_LIST_v05','spend_gbp':0,'assets':records,'contact_sheet':str(out/'contact_sheet.jpg'),'limitations':['No native motion proof or frame-0 approval','No blanket rights clearance from NASA hosting','Crop, upscale, source labels, Short exclusion and final reuse require review']}
    (HERE/'HUYGENS_RESERVED_POOL_v01.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
