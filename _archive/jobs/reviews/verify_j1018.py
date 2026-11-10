#!/usr/bin/env python3
"""Read-only J1018 map/inspection audit; no listening or final-media PASS."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
maps_path = ROOT / 'jobs/reviews/J0936_v04_PREP_v04_maps.json'
maps = json.loads(maps_path.read_text())
old = json.loads((ROOT / 'jobs/reviews/J0936_v04_PREP_v03_maps.json').read_text())
log_path = Path('/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json')
log = json.loads(log_path.read_text())
records = {(r['short_id'], r['row']): r for r in log['shots']}
out = {'maps_sha256': hashlib.sha256(maps_path.read_bytes()).hexdigest(),
       'inspection_log_sha256': hashlib.sha256(log_path.read_bytes()).hexdigest(),
       'source_window_mismatches': [], 'vo_subspans_unchanged': {},
       'reported_missing_syllable_bridge_arithmetic': [],
       'scope': 'Arithmetic and stored-log provenance only. Missing syllable is reported by Gemini; Codex has not independently listened.'}
for sid, s in maps['shorts'].items():
    vm = s['vo_splice_map']
    out['vo_subspans_unchanged'][sid] = vm['subspans'] == old['shorts'][sid]['vo_splice_map']['subspans']
    for r in s['shot_plan']:
        if r['row'] == 's_loop':
            continue
        stored = records[(sid, r['row'])]
        for k in ('source_path', 'source_in', 'source_out'):
            if stored[k] != r[k]:
                out['source_window_mismatches'].append([sid, r['row'], k, stored[k], r[k]])
    if s['film'] != 'OWB:028':
        continue
    spans = vm['subspans']
    for a, b in zip(spans, spans[1:]):
        if a['source_in'] == 43.5 and b['source_in'] == 44.1:
            continuous = b['source_out'] - a['source_in']
            slot = b['timeline_end'] - a['timeline_start']
            out['reported_missing_syllable_bridge_arithmetic'].append({
                'short': sid, 'spans': [a['span_index'], b['span_index']],
                'source_interval': [a['source_in'], b['source_out']],
                'omitted_source_interval': [a['source_out'], b['source_in']],
                'continuous_source_duration': round(continuous, 3),
                'current_output_slot': round(slot, 3),
                'extra_time_at_1x': round(continuous-slot, 3),
                'required_tempo_to_keep_slot': round(continuous/slot, 6),
                'subject_end_if_only_bridge_added': round(b['timeline_end']+continuous-slot, 3)})
out['s5_overlay'] = maps['shorts']['S5_028_jJ5LkFGyzLI']['single_teaching_overlay']
out['inspection_counts'] = {k: log[k] for k in ('total_body_shots', 'total_30fps_frames_decoded', 'total_2fps_ocr_frames_scanned')}
out['verifier_scope_findings'] = [
    'earliest_spoken_answer is a supplied word index; verifier checks its coordinates, not semantic earliest-answer choice.',
    'Source-window decode and OCR are read from a saved log, not rerun by verify_j0936_prep_v04.py.',
    '2fps OCR/contact sheets are samples for textual content; 30fps luma/scdet does not inspect every frame for text.',
    'Multimodal reviewer statements and numeric subject occupancy are supplied assertions, not computed by the verifier.'
]
(ROOT / 'jobs/reviews/J1018_2026-10-27_verification.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out['reported_missing_syllable_bridge_arithmetic'], indent=2))
