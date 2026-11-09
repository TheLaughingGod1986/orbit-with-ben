#!/usr/bin/env python3
"""Reproducible measurements for J2089 partial inputs. No review verdict."""
import hashlib,json,subprocess
from pathlib import Path
from PIL import Image
import code_graphics as teaching
import data_graphics as data
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 pool=json.loads((HERE/'HARVEST_POOL_v01.json').read_text());checks=[]
 for a in pool['assets']:
  p=Path(a['local_path']);assert sha(p)==a['sha256']
  with Image.open(p) as im:assert im.size==(a['width'],a['height']);im.verify()
  assert sha(a['source_evidence_path'])==a['source_evidence_sha256']
  checks.append({'asset_id':a['asset_id'],'image_and_source_hashes':'MATCH','dimensions':[a['width'],a['height']]})
 overlay=json.loads((HERE/'OVERLAY_MANIFEST_v01.json').read_text());clips=[]
 for c in overlay['clips']:
  assert sha(c['render'])==c['sha256']
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,pix_fmt,nb_frames:format=duration','-of','json',c['render']]))
  v=probe['streams'][0];assert (v['width'],v['height'],v['pix_fmt'],int(v['nb_frames']))==(1920,1080,'argb',108)
  assert abs(float(probe['format']['duration'])-3.6)<.001
  subprocess.run(['ffmpeg','-v','error','-i',c['render'],'-f','null','-'],check=True)
  clips.append({'id':c['id'],'hash':'MATCH','decode_exit':0,'duration':3.6,'frames':108,'pixel_format':'argb'})
 bounds=[]
 for module in [teaching,data]:
  for s in module.SPECS:
   start=module.frame(s,0).getchannel('A');mid=module.frame(s,1.8).getchannel('A');end=module.frame(s,3.6).getchannel('A')
   assert start.getbbox() is None and end.getbbox() is None
   box=mid.getbbox();assert box and 95<=box[0]<box[2]<=1825 and 54<=box[1]<box[3]<=1026
   bounds.append({'id':s['id'],'mid_alpha_bounds':box,'entry_exit_alpha':'ZERO','canvas_safe_area':'WITHIN_5_PERCENT'})
 result={'job':'J2089','status':'MEASUREMENTS_ONLY_NOT_KEEP_OR_PASS','source_images':checks,'teaching_renders':clips,'overlay_bounds':bounds,'not_verified':['Actual composite contrast >=4.5:1','Subject-safe placement on chosen graded moving plates','Native motion perception','All asset rights/crops/Short-frame exclusion','All required DATA/mechanism builds']}
 (HERE/'J2089_VERIFICATION_v02.json').write_text(json.dumps(result,indent=2)+'\n')
 print(f'Measured: {len(checks)} image/source hash pairs, {len(clips)} complete overlay decodes, {len(bounds)} alpha/safe-area checks. No final picture verdict.')
if __name__=='__main__':main()
