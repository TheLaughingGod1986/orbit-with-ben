#!/usr/bin/env python3
"""Apply a small display-luma lift to entire failed observation shots.

Preserves observation geometry and the prior repaired chapter. This is a
presentation grade, not recovered scientific detail or a gate exemption.
"""
import argparse
import json
import subprocess
from pathlib import Path
from build_orion_source_repair import sha, run

p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
root = Path(__file__).resolve().parent
source = Path('/Users/ben/_desk/J2452-sleep-scratch/betelgeuse_chajnantor_repaired_v01/029_picture_chajnantor_repaired.mp4')
assert sha(source) == '3b37262c97c2efab7110179baa65ab7b1ca30bb0bbe0bac643b672cd444684fd'
cuts = json.loads((source.parent / 'cuts.json').read_text())
spans = [c for c in cuts if c['source'] in ('sphere_dec.jpg', 'companion_speckle.jpg')]
assert len(spans) == 5
# Six 8-bit luma code values: a restrained presentation lift over the complete
# observation windows, retaining chroma and the existing Y=180 highlight cap.
# The 0.3 s shoulders are INSIDE each shot; adjacent shots remain unchanged.
weights = []
for c in spans:
    lo, hi = round(c['timeline_in'] * 30) / 30, round(c['timeline_out'] * 30) / 30
    weights.append(f'if(between(T,{lo},{hi}),min(1,min((T-{lo})/0.3,({hi}-T)/0.3)),0)')
expr = 'min(180,lum(X,Y)+6*(' + '+'.join(weights) + '))'
graph = f"geq=lum='{expr}':cb='cb(X,Y)':cr='cr(X,Y)',format=yuv420p"
a.out.mkdir(parents=True, exist_ok=False)
output = a.out / '029_picture_observation_grade.mp4'
run(['-i', str(source), '-vf', graph, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-threads', '6', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_trc', 'bt709', '-color_primaries', 'bt709', '-video_track_timescale', '90000', str(output)])
run(['-i', str(output), '-f', 'null', '-'])
info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-of', 'json', str(output)]))['streams'][0]
assert int(info['nb_read_frames']) == 14829
(a.out / 'cuts.json').write_text(json.dumps(cuts, indent=2) + '\n')
report = dict(status='PRESENTATION_GRADE_NOT_FULL_PICTURE_QA_OR_UAT', source=str(source), source_sha256=sha(source), output=str(output), sha256=sha(output), frames=14829, duration_s=494.3, spans=spans, filter=graph, luma_lift_code_values=6, shoulder_s=0.3, limitations=['Does not recover source detail or change scientific interpretation.', 'Original graphics, repeats, labels, finishing and other chapters remain.', 'Normal gates must run without exemptions.'])
(a.out / 'REPORT.json').write_text(json.dumps(report, indent=2) + '\n')
print(output)
