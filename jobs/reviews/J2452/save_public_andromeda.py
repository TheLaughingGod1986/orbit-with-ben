#!/usr/bin/env python3
"""Save this verified chapter additively, with destination byte read-back."""
import json,shutil
from pathlib import Path
from darken_public_andromeda import OUT,sha
DEST=Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/j2452/public_chapters_v01/019_andromeda_v01')
def main():
 r=json.loads((OUT/'DARKEN_READBACK.json').read_text());b=r['undarkened_build'];q=r['undarkened_readback']
 assert Path('/Volumes/data').is_mount()
 assert r['frames_before']==r['frames_after']==b['expected_frames']
 assert r['brightness_measurement'].startswith('Decoded legal-range Y plane')
 assert .83<=r['post_2030_brightness_ratio']<=.87
 assert r['timed_grade_two_second_measurements']
 assert all(abs(w['actual_ratio']-w['expected_ratio'])<=.02 for w in r['timed_grade_two_second_measurements'])
 assert r['post_2030_two_second_measurements']
 assert all(w['ratio'] is not None and .83<=w['ratio']<=.87 for w in r['post_2030_two_second_measurements'])
 assert q['gate_exit_codes'] in ([0,0],[1,0]) and all(x['classification']=='in the public film' for x in q['inherited_findings'])
 assert sha(Path(r['output']))==r['sha256']
 DEST.mkdir(parents=True,exist_ok=False);copies=[]
 for p in [Path(r['output']),OUT/'BRIGHTEST_WINDOWS.jpg']:
  target=DEST/p.name
  with p.open('rb') as src,target.open('xb') as dst:shutil.copyfileobj(src,dst,1048576)
  digest=sha(target);assert digest==sha(p)
  copies.append(dict(path=str(target),sha256=digest,bytes=target.stat().st_size))
 record=dict(status='CHAPTER_SAVED_NOT_FINAL_UAT',build=b,readback=q,darkening=r,copies=copies,notes='Thirteenth chapter only. Full compilation, bed and sound checks, joins, reel and Ben watch card still owed. Finished-source charts and labels retained; dissolves only on compilation edits. No upload or spend.')
 (DEST/'CHAPTER.json').write_text(json.dumps(record,indent=2)+'\n');assert json.loads((DEST/'CHAPTER.json').read_text())==record
 saved=dict(destination=str(DEST),copies=copies,record_sha256=sha(DEST/'CHAPTER.json'))
 (OUT/'NAS_COPY.json').write_text(json.dumps(saved,indent=2)+'\n');print(json.dumps(saved,indent=2))
if __name__=='__main__':main()
