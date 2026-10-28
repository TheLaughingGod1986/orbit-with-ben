#!/usr/bin/env python3
"""Correct four dark Orion intervals; preserve accepted audio and all timings.

Run after archival. Produces unreviewed media alongside finish08, never publishes.
"""
import argparse
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, required=True)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--media-root', type=Path, required=True)
    a = ap.parse_args()
    assert shutil.disk_usage('/private/tmp').free >= 20_000_000_000, 'Archive first'
    spec = importlib.util.spec_from_file_location('finish', Path(__file__).resolve().parents[1] / 'finish_j1100_s2_v05.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    legacy_path = a.media_root / '02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/mon30_comets/_assemble_mon30_comets_v03.py'
    spec = importlib.util.spec_from_file_location('legacy', legacy_path)
    legacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(legacy)
    for src in sorted(a.input.glob('*/*_v05.mp4')):
        key = src.parent.name
        d = a.out / key
        d.mkdir(parents=True, exist_ok=True)
        if (d / 'FINISH_COMPLETE.json').exists():
            continue
        prep = json.loads((a.source / key / 'locked_preparation.json').read_text())
        rows = [r for r in prep['shot_plan'] if 'orion_paranal' in r['row']]
        dest = d / src.name
        changes = []
        if rows:
            assert len(rows) == 1 and key.startswith(('S3_', 'S4_', 'S5_', 'S6_'))
            r = rows[0]
            start_frame = round(r['timeline_in'] * 30)
            end = round(r['timeline_out'] * 30) / 30
            if key == 'S6_028_X768qs8sNQs':
                # Preserve exact first-cut transition at frame 74 (2.467s, scdet=10.757) by lifting frames 60..73 (2.000..2.433s, after 0..1.5s opening metrics) and starting s02_orion_paranal lift at frame 75 (2.500s).
                start_frame += 1
                start = start_frame / 30
                vf = f"eq=brightness=0.03:enable='between(n,60,73)',eq=gamma=1.25:brightness=0.015:enable='gte(t,{start})*lt(t,{end})'"
            else:
                start = start_frame / 30
                vf = f"eq=gamma=1.25:brightness=0.015:enable='gte(t,{start})*lt(t,{end})'"
            mod.ff(['-i', src, '-vf', vf, '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-c:a', 'copy', '-movflags', '+faststart', dest])
            changes.append({'row': r['row'], 'start': start, 'end': end, 'filter': vf})
            mod.ff(['-i', dest, '-vf', 'scale=720:1280:flags=lanczos', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-c:a', 'copy', d / (src.stem + '_PHONE.mp4')])
        elif key == 'S1_026_A6TW_6CXhcs':
            # Replace single stray internal flash at frame 70 (2.333s) of s00_sdo_gold_sun before s01 cut at frame 71 (2.367s).
            fc = '[0:v]split[a][b];[a][b]freezeframes=first=70:last=70:replace=69[v]'
            mod.ff(['-i', src, '-filter_complex', fc, '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-c:a', 'copy', '-movflags', '+faststart', dest])
            changes.append({'row': 's00_sdo_gold_sun', 'frame': 70, 'replace': 69, 'filter_complex': fc})
            mod.ff(['-i', dest, '-vf', 'scale=720:1280:flags=lanczos', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-c:a', 'copy', d / (src.stem + '_PHONE.mp4')])
        else:
            shutil.copy2(src, dest)
            shutil.copy2(src.with_name(src.stem + '_PHONE.mp4'), d / (src.stem + '_PHONE.mp4'))
        # The AAC packets must remain identical, not merely equal in loudness.
        def audio_hash(p):
            return subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(p), '-map', '0:a:0', '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-']).decode().strip()
        assert audio_hash(src) == audio_hash(dest), 'Accepted AAC changed'
        record = json.loads((src.parent / 'FINISH_COMPLETE.json').read_text())
        level = legacy.ebur128_stats(dest)
        loop = legacy.loop_measures(dest)
        record.update(input_sha256=mod.sha(src), corrections=changes,
                      I_LUFS=level[0], TP_dBTP=level[1],
                      audio_pass=-14.5 <= level[0] <= -13.5 and level[1] <= -1.6,
                      loop=loop, loop_pass=max(loop.values()) < 2,
                      status='UNREVIEWED; final gates, audio listening and durable delivery outstanding',
                      files={p.name: mod.sha(p) for p in d.glob('*.mp4')})
        # Prior endpoint value is historical; final checker measures actual new endpoints.
        record.pop('actual_seam_diff', None)
        mod.dump(d / 'FINISH_COMPLETE.json', record)
        print(key, json.dumps(record), flush=True)
        assert record['audio_pass'] and record['loop_pass']


if __name__ == '__main__':
    main()
