#!/usr/bin/env python3
"""Build a 12:26 review reel, including each chapter's brightest window."""
import argparse
import hashlib
import json
import shutil
import subprocess as sp
from pathlib import Path


def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--scratch', type=Path, required=True)
    p.add_argument('--destination', type=Path, required=True)
    a = p.parse_args()
    s = a.scratch / 'final_join_v01'
    delivery = json.loads((s / 'MASTER_DELIVERY_V01.json').read_text())
    master = s / delivery['file']
    assert sha(master) == delivery['sha256']
    recipe = json.loads(Path('jobs/reviews/J2452/final_join_v04/REEL_RECIPE_V01.json').read_text())
    timeline = json.loads((s / 'TIMELINE.json').read_text())
    segments = recipe['segments'][:]
    for chapter in timeline['chapters']:
        reports = [json.loads(f.read_text()) for f in Path(chapter['path']).parent.glob('*.json')]
        report = next(r for r in reports if r.get('brightest_two_second_windows'))
        window = report['brightest_two_second_windows'][0]
        segments.append(dict(label=f"Brightest window: {chapter['film']}",
                             start_s=chapter['start_s'] + window['start_s'], duration_s=2))
    folder = s / 'watch_reel_v01'
    folder.mkdir(exist_ok=True)
    parts = []
    clock = 0
    for i, segment in enumerate(segments):
        segment['reel_start_s'] = clock
        clock += segment['duration_s']
        output = folder / f'part_{i:02d}.mp4'
        assert not output.exists(), 'Preserve previous output; choose a new version before retry'
        sp.run(['ffmpeg', '-v', 'error', '-nostdin', '-n', '-threads', '2',
                '-ss', str(segment['start_s']), '-i', str(master), '-t', str(segment['duration_s']),
                '-vf', 'scale=1280:720', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                '-threads', '4', '-c:a', 'aac', '-b:a', '192k', '-r', '30', str(output)],
               check=True, timeout=240)
        parts.append(output)
        print('Rendered', segment['label'], flush=True)
    listing = folder / 'concat.txt'
    listing.write_text(''.join(f"file '{f}'\n" for f in parts))
    reel = folder / a.destination.name
    sp.run(['ffmpeg', '-v', 'error', '-nostdin', '-n', '-f', 'concat', '-safe', '0',
            '-i', str(listing), '-c', 'copy', '-movflags', '+faststart', str(reel)], check=True, timeout=60)
    sp.run(['ffmpeg', '-v', 'error', '-xerror', '-nostdin', '-threads', '4', '-i', str(reel),
            '-f', 'null', '-'], check=True, timeout=180)
    assert Path('/Volumes/data').is_mount()
    store = Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01')
    assert a.destination.resolve().is_relative_to(store.resolve())
    with reel.open('rb') as source, a.destination.open('xb') as target:
        shutil.copyfileobj(source, target, length=8 * 1024 * 1024)
    digest = sha(reel)
    assert sha(a.destination) == digest
    result = dict(status='DECODED_AND_NAS_HASH_VERIFIED', nas_path=str(a.destination),
                  sha256=digest, bytes=reel.stat().st_size, planned_duration_s=clock,
                  segments=segments, note='720p review proxy; final master retains 1080p. Segment joins are review jumps.')
    (s / 'REEL_DELIVERY_V01.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Reel delivered', digest, flush=True)


if __name__ == '__main__':
    main()
