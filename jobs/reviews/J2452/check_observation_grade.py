#!/usr/bin/env python3
"""Independently check a saved observation grade's scope and preserved clock."""
import argparse
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from build_orion_source_repair import sha

p = argparse.ArgumentParser()
p.add_argument('directory', type=Path)
a = p.parse_args()
r = json.loads((a.directory / 'REPORT.json').read_text())
source, output = Path(r['source']), Path(r['output'])
assert sha(source) == r['source_sha256'] and sha(output) == r['sha256']

def gray(path, t):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(path), '-frames:v', '1', '-vf', 'scale=480:270,format=gray', '-f', 'rawvideo', '-'])
    return np.frombuffer(raw, np.uint8).reshape(270, 480).astype(np.float32)

samples = []
sheet = Image.new('RGB', (960, 5 * 294), '#15202c')
draw = ImageDraw.Draw(sheet)
for i, c in enumerate(r['spans']):
    lo, hi = round(c['timeline_in'] * 30) / 30, round(c['timeline_out'] * 30) / 30
    for label, t in [('before', lo - .2), ('inside_start', lo + .4), ('middle', (lo + hi) / 2), ('inside_end', hi - .4), ('after', hi + .2)]:
        old, new = gray(source, t), gray(output, t)
        delta = new - old
        measured = dict(row=c['row'], source=c['source'], position=label, t=t, mean_delta=float(delta.mean()), mean_absolute_delta=float(np.abs(delta).mean()), p99_absolute_delta=float(np.percentile(np.abs(delta), 99)))
        # Six TV-range code values become roughly seven full-range gray values.
        # Tolerances allow codec error, not missing or mis-timed coverage.
        if label.startswith('inside') or label == 'middle':
            assert 5 < measured['mean_delta'] < 8.5, measured
        else:
            assert measured['mean_absolute_delta'] < 1.5, measured
        samples.append(measured)
        if label == 'middle':
            sheet.paste(Image.fromarray(old.astype('uint8')).convert('RGB'), (0, i * 294 + 24))
            sheet.paste(Image.fromarray(new.astype('uint8')).convert('RGB'), (480, i * 294 + 24))
            draw.text((8, i * 294 + 5), f"{c['source']} {t:.2f}s: prior / saved grade", fill='white')
# Midpoints of the two retained Orbit covers and two original-source repairs.
for t in (111.5, 263.5, 237.5, 435.5):
    difference = np.abs(gray(output, t) - gray(source, t))
    measured = dict(position='retained_repair', t=t, mean_absolute_delta=float(difference.mean()))
    assert measured['mean_absolute_delta'] < 1.5, measured
    samples.append(measured)
sheet.save(a.directory / 'observation_grade_comparison.jpg')
report = dict(status='SAMPLED_GRADE_SCOPE_PASS_NOT_FULL_PICTURE_QA', output_sha256=sha(output), samples=samples, limitations=['Sampled luma evidence; no every-frame visual watch.', 'No scientific detail recovery claimed.', 'Normal polish and picture QA remain authoritative.'])
(a.directory / 'READBACK.json').write_text(json.dumps(report, indent=2) + '\n')
print(report['status'])
