#!/usr/bin/env python3
"""J2089: bounded, resumable pinned-ID source harvest. No generation or approval."""
import argparse, concurrent.futures, hashlib, json, re, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw
HERE=Path(__file__).resolve().parent

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"OrbitWithBen source audit"}),timeout=30) as r: return r.read()
def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    shot=(HERE/'SHOT_LIST_v02.md').read_text()
    ids=sorted(set(re.findall(r'PIA[0-9]{5}',shot)))
    def one(nid):
        rec={'asset_id':nid,'source_page':f'https://images.nasa.gov/details/{nid}',
             'referenced_rows':[int(l.split('|')[1]) for l in shot.splitlines() if re.match(r'\| \d+ \|',l) and nid in l],
             'review_status':'CANDIDATE_NOT_KEEP','licence_status':'PENDING_PER_ASSET_TERMS_CHECK'}
        try:
            raw=fetch('https://images-api.nasa.gov/search?nasa_id='+nid)
            (out/(nid+'_metadata.json')).write_bytes(raw)
            items=json.loads(raw)['collection']['items'];item=next(i for i in items if i['data'][0]['nasa_id']==nid)
            meta=item['data'][0];rec.update(title=meta['title'],description=meta.get('description'),credit=meta.get('secondary_creator'),metadata_sha256=sha(raw),metadata_path=str(out/(nid+'_metadata.json')))
            links=[l for l in item.get('links',[]) if l.get('render')=='image']
            link=max(links,key=lambda l:l.get('width',0)*l.get('height',0))
            dest=out/(nid+Path(link['href']).suffix)
            if not dest.exists():dest.write_bytes(fetch(link['href']))
            data=dest.read_bytes()
            with Image.open(dest) as im: rec.update(width=im.width,height=im.height);im.verify()
            rec.update(local_path=str(dest),download_url=link['href'],sha256=sha(data),bytes=len(data),download_status='downloaded')
        except Exception as e:rec.update(download_status='ERROR',error=str(e))
        print(nid,rec.get('title'),rec.get('error',''),flush=True);return rec
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:assets=list(ex.map(one,ids))
    flags=json.loads((HERE/'SOURCE_AUDIT_FLAGS_v01.json').read_text())
    for r in assets:r['source_audit_issue']=flags.get(r['asset_id'])
    pool={'job':'J2089','shot_list_sha256':sha(shot.encode()),'status':'PARTIAL_SOURCE_AUDIT_NOT_ASSEMBLY_READY','spend_gbp':0,'assets':assets,
          'outstanding':['Resolve pinned-ID/description mismatches','Verify licences and attribution per asset','Exclude actual RLSJm59OSzI used frames/hash matches','Harvest motion, portrait and Uranus JWST inputs','Build and review row-specific graphics'],
          'contact_sheet':str(out/'contact_sheet.jpg')}
    (HERE/'HARVEST_POOL_v01.json').write_text(json.dumps(pool,indent=2)+'\n')
    good=[r for r in assets if r.get('download_status')=='downloaded']
    sheet=Image.new('RGB',(1200,260*((len(good)+3)//4)),(30,37,51));d=ImageDraw.Draw(sheet)
    for i,r in enumerate(good):
        x=(i%4)*300;y=(i//4)*260
        with Image.open(r['local_path']) as im:
            im=im.convert('RGB');im.thumbnail((288,210));sheet.paste(im,(x+(300-im.width)//2,y))
        d.text((x+5,y+212),r['asset_id'],fill='white');d.text((x+5,y+230),r['title'][:40],fill='white')
    sheet.save(out/'contact_sheet.jpg',quality=90)
    (out/'SHA256SUMS.txt').write_text(''.join(r['sha256']+'  '+Path(r['local_path']).name+'\n' for r in good))
if __name__=='__main__':main()
