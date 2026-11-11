#!/usr/bin/env python3
"""Reproduce the REJECTED diagnostic Venus recipe, never a production recipe.

See VENUS_PICTURE_FINDINGS_2026-11-11.md before using these source choices.
"""
import hashlib,json,tarfile
from pathlib import Path
root=Path('jobs/reviews/J2452');local=Path('/Users/ben/_desk/J2452-sleep-scratch/venus_picture_assets_v01');local.mkdir(exist_ok=False)
wanted={'PIA00271.jpg','as17-148-22727.jpg','PIA00270.jpg','PIA00104.jpg','PIA00252.jpg','PIA00108.jpg'};assets={}
archive=Path('/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb023.tar')
with tarfile.open(archive) as t:
 for m in t:
  name=Path(m.name).name
  if name in wanted and name not in assets:
   data=t.extractfile(m).read();out=local/name;out.write_bytes(data)
   assets[name]=dict(path=str(out),archive=str(archive),member=m.name,sha256=hashlib.sha256(data).hexdigest())
   print(name,flush=True)
   if len(assets)==len(wanted):break
assert len(assets)==len(wanted)
(root/'venus_picture_assets_v01.json').write_text(json.dumps(assets,indent=2)+'\n')
chapter=json.loads((root/'picture_timeline_v01.json').read_text())['chapters'][4]
cuts=json.loads(Path('02_Video-Projects/023_What-Happened-To-Venus/07_Edit-Project/full_rough_v05e_pack/cuts_v05e.json').read_text())
# Replacements remove the actual v05e chart/Orbit/mission-title rows, rather than approximate plan windows.
replacements={'albedo.mp4':'PIA00271.jpg','heavyh.mp4':'PIA00270.jpg','deuterium.mp4':'PIA00104.jpg','nightlid.mp4':'PIA00108.jpg','venus_row39a_split_labelled_v04.mp4':'as17-148-22727.jpg','venus_row39b_alpha_regio_v04.mp4':'PIA00108.jpg','line.mp4':'PIA00252.jpg','orbit_looks_back_earth_omni_v01_t0-5s.mp4':'PIA00271.jpg','13887_DAVINCI_PEVAA.mp4':'PIA00270.jpg','veritas-cut7-16.jpg':'PIA00104.jpg'}
shots=[];clock=0
for sl in chapter['slices']:
 a,b=sl['master_in_s'],sl['master_out_s'];edges=[a]+[c['timeline_in'] for c in cuts if a<c['timeline_in']<b]+[b]
 # Collapse tiny edge fragments into their neighbour; do not change the slice's audio clock.
 if edges[1]-edges[0]<2.1:edges.pop(1)
 if edges[-1]-edges[-2]<2.1:edges.pop(-2)
 for x,y in zip(edges,edges[1:]):
  c=next(c for c in cuts if c['timeline_in']<=((x+y)/2)<c['timeline_out'])
  old=clock;clock+=y-x;frames=round(clock*30)-round(old*30);d=frames/30
  replacement=replacements.get(c['source']);source=assets[replacement]['path'] if replacement else chapter['master']
  shots.append(dict(source=source,source_in_s=0 if replacement else x,duration_s=d,still=bool(replacement),master_in_s=x,master_out_s=y,original_source=c['source'],replacement=replacement))
recipe=dict(film='023',status='CANDIDATE_REQUIRES_FRAME_AND_PICTURE_QA',global_start_s=chapter['compilation_start_s'],duration_s=chapter['duration_s'],shots=shots,limitations=['Not a finished compilation; no audio mux, inter-film breath or chapter title yet.','Covers require subject/provenance review and reuse QA; archived plates retain their original agency identities.','Final picture_qa must run without waivers; no full-frame or perceptual approval claimed.','Cumulative frame quantization preserves 491.4-second chapter duration; confirm sync on final master.'])
assert abs(sum(s['duration_s'] for s in shots)-chapter['duration_s'])<.001
(root/'venus_picture_recipe_v01.json').write_text(json.dumps(recipe,indent=2)+'\n')
print(len(shots),'shots',sum(s['duration_s'] for s in shots),flush=True)
