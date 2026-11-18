#!/usr/bin/env python3
"""Cross-check draft picture manifests against locked EDL; report missing work."""
import argparse,hashlib,json,pathlib

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--media',type=pathlib.Path,required=True);a=p.parse_args();edit=pathlib.Path(__file__).resolve().parent;edl=json.loads((edit/'EDL_v01.json').read_text());expected={r['shot_id']:r for r in edl['rows']};rendered={};batches=[]
 for batch in ['early_v01','geography_v01','aircraft_v01','detection_v01','synthesis_v01','convoys_v01','carrier_v01','ending_v01']:
  folder=a.media/'03_Picture/maps'/batch;m=json.loads((folder/'MANIFEST.json').read_text());check=json.loads((folder/'TECHNICAL_CHECK.json').read_text())
  if m['audio_sha256']!=edl['audio_sha256'] or check['source_audio_sha256']!=edl['audio_sha256']:raise ValueError('Mismatched narration')
  for r in m['rows']:
   e=expected[r['shot_id']]
   for key in ['narration','picture_id','cut_start_s','cut_end_s']:
    if r[key]!=e[key]:raise ValueError('Stale picture row '+r['shot_id']+' '+key)
   if r['shot_id'] in rendered:raise ValueError('Duplicate shot')
   if sha(pathlib.Path(r['video']))!=r['sha256']:raise ValueError('Picture hash mismatch')
   rendered[r['shot_id']]=r
  if sha(pathlib.Path(check['video']))!=check['sha256']:raise ValueError('Draft sequence hash mismatch')
  batches.append(check)
 archive=json.loads((edit/'ARCHIVE_HARVEST.json').read_text());thumbs=a.media/'03_Picture/previews'
 result={'state':'partial_draft_no_stage_approval','edl_rows':len(expected),'sentence_clips_rendered':len(rendered),'sentence_rows_not_in_these_batches':len(expected)-len(rendered),'opening_separate':'M001/opening_with_vo_DRAFT_v01.mp4 covers first four sentences; not counted in these batches','batches':batches,'rendered_shots':list(rendered),'remaining_line_ids':sorted({r['line_id'] for k,r in expected.items() if k not in rendered and r['line_id']!='L001'}),'original_boundary_flags_resolved_in_v02':[r['shot_id'] for r in expected.values() if r['boundary_review']],'archive':[{k:r.get(k) for k in ['key','id','status','file','pixels','sha256']} for r in archive],'thumbnail_candidates':[{'file':str(thumbs/name),'sha256':sha(thumbs/name)} for name in ['thumbnail_A_candidate_v01.jpg','thumbnail_B_candidate_v01.jpg']],'not_done':['EDL_v02 length conform and chapter pauses','Film-specific music','Full film assembly and technical QA','Capable watch/listen review','Chief review and Ben-watch delivery']}
 (edit/'PICTURE_BUILD_v01.json').write_text(json.dumps(result,indent=2)+'\n');print(len(rendered),'sentence clips checked against EDL and hashes;',len(expected)-len(rendered),'outside these batches')
if __name__=='__main__':main()
