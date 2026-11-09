#!/usr/bin/env python3
"""Verify exact recovered Commons originals; no archive search or approval."""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image

def sha(path, algorithm='sha256'):
    return hashlib.new(algorithm, Path(path).read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pool', type=Path, required=True)
    ap.add_argument('--recovery', type=Path, required=True)
    ap.add_argument('--report', type=Path, required=True)
    a=ap.parse_args()
    if a.report.exists(): raise FileExistsError(a.report)
    pool=json.loads(a.pool.read_text()); recovery=json.loads(a.recovery.read_text())
    originals={r['asset_id']:r for r in pool['assets']}; checks=[]
    for record in recovery['assets']:
        original=originals[record['asset_id']]
        with Image.open(record['local_path']) as im:
            im.verify()
        with Image.open(record['local_path']) as im:
            size=list(im.size)
        api=json.loads(Path(record['source_evidence_path']).read_text())
        info=next(iter(api['query']['pages'].values()))['imageinfo'][0]
        assertions=dict(
            original_sha256=sha(record['local_path'])==original['sha256']==record['sha256'],
            commons_sha1=sha(record['local_path'],'sha1')==info['sha1']==original['source_sha1'],
            native_dimensions=size==[original['width'],original['height']]==[info['width'],info['height']],
            licence_unchanged=info['extmetadata']['LicenseShortName']['value']==original['licence']==record['licence'],
            reuse_cap=original['planned_appearances']<=original['max_appearances']<=2,
            attribution_preserved=original['credit']==record['credit'] and original['rights_obligations']==record['rights_obligations'])
        for path_key,hash_key in [('source_evidence_path','source_evidence_sha256'),('licence_evidence_path','licence_evidence_sha256'),('licence_terms_path','licence_terms_sha256')]:
            if record.get(path_key):assertions[path_key]=sha(record[path_key])==record[hash_key]
        if not all(assertions.values()):raise ValueError((record['asset_id'],assertions))
        original['macbook_recovery']=record
        checks.append(dict(asset_id=record['asset_id'],checks=assertions,local_path=record['local_path'],sha256=record['sha256'],dimensions=size))
    contact=recovery['nature_contact_sheet']
    if sha(contact)!=recovery['nature_contact_sheet_sha256']:raise ValueError('Contact hash')
    pool['nature_contact_sheet_macbook']=contact
    pool['nature_contact_sheet_macbook_sha256']=sha(contact)
    a.pool.write_text(json.dumps(pool,indent=2)+'\n')
    a.report.write_text(json.dumps(dict(job='J2141',worker='macbook-2',spend_gbp=0,source_pr=572,source_commit='cb3ecfa51c8373badff8dbd1b8c64d1ab9cd8f3f',scope='Exact original recovery, provenance and static-file integrity only; no KEEP, composite or film QA',checks=checks,contact_sheet=contact,contact_sha256=sha(contact)),indent=2)+'\n')
if __name__=='__main__':main()
