#!/usr/bin/env python3
"""Source hashes and all-position native 16:9 crop measurements; no KEEP verdict."""
import hashlib,json,math
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 pool=json.loads((HERE/'HUYGENS_RESERVED_POOL_v01.json').read_text());checks=[]
 # Smallest integer 16:9 crop that does not exceed 2.35x at 1920x1080.
 width,height=16*math.ceil(1920/2.35/16),9*math.ceil(1920/2.35/16)
 for r in pool['assets']:
  for p,h in [(r['local_path'],r['sha256']),(r['metadata_path'],r['metadata_sha256']),(r['assets_path'],r['assets_sha256'])]:assert sha(p)==h
  with Image.open(r['local_path']) as im:
   assert im.size==(r['width'],r['height']);a=np.asarray(im.convert('L'))
  # Mosaic gaps may be lifted dark grey, not digital zero. Pixel counts alone
  # cannot distinguish seams/low-detail science data: full-size still review remains required.
  mask=(a<32).astype(np.int64);s=np.pad(mask,((1,0),(1,0))).cumsum(0).cumsum(1)
  counts=s[height:,width:]-s[:-height,width:]-s[height:,:-width]+s[:-height,:-width]
  y,x=np.unravel_index(counts.argmin(),counts.shape);fraction=float(counts[y,x]/(width*height))
  crop=(int(x),int(y),int(x+width),int(y+height));dest=Path(r['local_path']).with_name(r['asset_id']+'_minimum_dark_crop.jpg')
  with Image.open(r['local_path']) as im:im.crop(crop).save(dest,quality=95)
  checks.append({'asset_id':r['asset_id'],'hashes':'MATCH','native_dimensions':[r['width'],r['height']],'origins_tested':int(counts.size),'crop_size':[width,height],'upscale':1920/width,'minimum_below_32_fraction':fraction,'minimum_dark_crop':crop,'preview':str(dest),'preview_sha256':sha(dest),'verdict':'MEASUREMENTS_ONLY_REQUIRES_STILL_REVIEW','not_verified':['Mosaic seams and actual subject detail','Rights','Short exclusion','Native motion (both are stills)']})
 result={'job':'J2089','threshold_note':'Below 32 catches lifted mosaic voids; not proof of plate quality','checks':checks}
 (HERE/'HUYGENS_RESERVED_CHECKS_v01.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
