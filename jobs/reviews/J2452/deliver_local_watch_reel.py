#!/usr/bin/env python3
"""Copy the decoded local review reel only after the master safety copy passes."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    folder = args.scratch / 'final_join_v01'
    master = json.loads((folder / 'MASTER_DELIVERY_V01.json').read_text())
    assert master['status'] == 'MUXED_AND_SAFETY_COPIED_REEL_AND_UAT_PENDING'
    record = json.loads((folder / 'LOCAL_REEL_V01.json').read_text())
    assert record['status'] == 'LOCAL_DECODED_NAS_COPY_PENDING'
    source = Path(record['file'])
    assert source.stat().st_size == record['bytes'] and sha(source) == record['sha256']
    store = Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01')
    assert Path('/Volumes/data').is_mount()
    assert args.destination.resolve().is_relative_to(store.resolve())
    with source.open('rb') as left, args.destination.open('xb') as right:
        shutil.copyfileobj(left, right, length=8 * 1024 * 1024)
    assert sha(args.destination) == record['sha256']
    record.update(status='DECODED_AND_NAS_HASH_VERIFIED', nas_path=str(args.destination))
    (folder / 'REEL_DELIVERY_V01.json').write_text(json.dumps(record, indent=2) + '\n')
    print('Reel destination hash PASS', flush=True)


if __name__ == '__main__':
    main()
