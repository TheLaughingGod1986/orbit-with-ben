#!/usr/bin/env python3
"""Read-only integrity audit of the retained J2452 components, not media QA."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def check(path, expected):
    path = Path(path)
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    actual = digest.hexdigest()
    return dict(path=str(path), bytes=path.stat().st_size, sha256=actual,
                expected_sha256=expected, match=actual == expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    audio = json.loads((root / 'audio_timeline_v01/REPORT.json').read_text())
    picture = json.loads((root / 'picture_timeline_v01.json').read_text())
    qa = json.loads((root / 'alma_betelgeuse_qa_v02/picture_qa.json').read_text())
    copied = json.loads((root / 'checkpoint_nas_readback_20261111_v01.json').read_text())
    checks = []
    for chapter in audio['chapters']:
        result = check(chapter['narration'], chapter['narration_sha256'])
        result['film'] = chapter['film']
        checks.append(result)
    checks.append(check(audio['output'], audio['sha256']))
    checks.append(check(qa['video'], '85d0090af6bb829b314b7a10dcdb703dce3565eb216c7114802016f8ef29c73b'))
    for item in copied['files']:
        checks.append(check(item['nas'], item['sha256']))
    expected_order = ['013', '021', '027', '025', '023', '031', '020', '022',
                      '028', '029', '024', '026', '019']
    assert [c['film'] for c in audio['chapters']] == expected_order
    assert [c['film'] for c in picture['chapters']] == expected_order
    clock = []
    for a, p in zip(audio['chapters'], picture['chapters']):
        delta = p['duration_s'] - (a['narration_end_s'] - a['start_s'])
        clock.append(dict(film=a['film'], duration_s=p['duration_s'],
                          audio_picture_duration_delta_s=round(delta, 6)))
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', qa['video']]))
    report = dict(status='INTEGRITY_ONLY_NOT_FINAL_QA',
                  hash_checks=checks, chapter_clock=clock,
                  audio_duration_s=audio['duration_s'],
                  adopted_picture_probe=probe,
                  inherited_picture_failures=qa['failed'],
                  remaining='Seven 029 reuse failures and retained graphics; twelve other picture chapters; finishing, final gates, reel, delivery and UAT.',
                  limitations=['No fresh loudness, silence, CTA, pixel or listening test.',
                               'The retained QA report still FAILs; hashes do not confer approval.'])
    with args.out.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    assert all(c['match'] for c in checks), 'Component hash mismatch'
    assert all(abs(c['audio_picture_duration_delta_s']) < .001 for c in clock)
    print(f'{len(checks)} complete hash read-backs match; 13 chapter clocks match; inherited QA FAIL remains.')


if __name__ == '__main__':
    main()
