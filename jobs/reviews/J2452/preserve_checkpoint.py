#!/usr/bin/env python3
"""Add three verified J2452 intermediates to their own NAS film folders.

No overwrite, deletion, master/KEEP claim, or external service action.
"""
import hashlib
import json
import shutil
from pathlib import Path

SCRATCH = Path('/Users/ben/_desk/J2452-sleep-scratch')
FILMS = Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects')
FILES = [
    ('alma_betelgeuse_v02/029_picture_alma_betelgeuse.mp4', '_sleep_video_01/j2452/checkpoint_20261111_v01/029_picture_alma_betelgeuse_v02.mp4', '85d0090af6bb829b314b7a10dcdb703dce3565eb216c7114802016f8ef29c73b'),
    ('audio_timeline_v01/sleep_audio_master_candidate_v01.wav', '_sleep_video_01/j2452/checkpoint_20261111_v01/sleep_audio_master_candidate_v01.wav', 'c4da38de048054099a2e94dead8e3c07438fcaa0e24f1deac657c1c01f25f804'),
    ('alma_betelgeuse_source_v01/potw1726a.jpg', '029_Is-Betelgeuse-About-To-Explode/03_Footage/potw1726a_sleep_j2452_v01.jpg', '3f75e8b1df70dca7f0e828e8fd640880a7bfcbdef0945304792bace2eb243bbe'),
]

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def main():
    assert Path('/Volumes/data').is_mount(), 'NAS must be mounted'
    evidence = []
    for local, remote, expected in FILES:
        source, target = SCRATCH / local, FILMS / remote
        assert sha(source) == expected, f'Local hash mismatch: {source.name}'
        assert target.parent.parent.is_dir(), 'Existing film/store folder required'
        target.parent.mkdir(exist_ok=True)
        if target.exists():
            assert sha(target) == expected, f'Existing destination differs: {target.name}'
            action = 'existing matching file retained'
        else:
            with source.open('rb') as src, target.open('xb') as dst:
                shutil.copyfileobj(src, dst, 8 * 1024 * 1024)
            action = 'exclusive additive copy'
        assert source.stat().st_size == target.stat().st_size
        assert sha(target) == expected, f'NAS read-back mismatch: {target.name}'
        evidence.append(dict(local=str(source), nas=str(target), bytes=target.stat().st_size,
                             sha256=expected, readback='MATCH', action=action))
        print(f'Checked {target.name}', flush=True)
    result = dict(status='INTERMEDIATES_PRESERVED_NOT_MASTER_OR_UAT', files=evidence,
                  limitations=['Picture QA still fails seven reuse rows.',
                               'Audio candidate has no final AV or listening approval.',
                               'No full compilation, reel or delivery to Ben.'])
    output = Path(__file__).with_name('checkpoint_nas_readback_20261111_v01.json')
    output.write_text(json.dumps(result, indent=2) + '\n')

if __name__ == '__main__':
    main()
