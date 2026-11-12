#!/usr/bin/env python3
"""Verify an existing NAS prefix, append missing bytes, then hash the full copy.

Never truncates or overwrites a NAS file. Safe only after the original writer
has exited. A bounded run checkpoints partial work without claiming delivery.
"""
import argparse
import hashlib
import json
import subprocess as sp
import time
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--scratch', type=Path, required=True)
    p.add_argument('--destination', type=Path, required=True)
    p.add_argument('--seconds-budget', type=int, default=900)
    p.add_argument('--copy-only', action='store_true', help='Checkpoint the complete copy; full NAS hash remains required')
    a = p.parse_args()
    s = a.scratch / 'final_join_v01'
    record = json.loads((s / 'LOCAL_MASTER_CANDIDATE_V01.json').read_text())
    source = s / record['file']
    destination = a.destination
    assert Path('/Volumes/data').is_mount()
    store = Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01')
    assert destination.resolve().is_relative_to(store.resolve())
    assert source.stat().st_size == record['bytes']
    checkpoint = s / 'MASTER_COPY_PREFIX_CHECKPOINT_V01.json'
    def remember_prefix():
        stat = destination.stat()
        checkpoint.write_text(json.dumps(dict(source_sha256=record['sha256'],
            destination=str(destination), bytes=stat.st_size, mtime_ns=stat.st_mtime_ns,
            status='COPY_PROVENANCE_ONLY_FULL_DESTINATION_HASH_REQUIRED'), indent=2) + '\n')
    deadline = time.monotonic() + a.seconds_budget
    def check_time():
        if time.monotonic() >= deadline:
            raise TimeoutError('Budget reached; partial copy preserved, no delivery claimed')
    def digest(path):
        result = hashlib.sha256()
        with path.open('rb') as handle:
            while chunk := handle.read(8 * 1024 * 1024):
                check_time()
                result.update(chunk)
        return result.hexdigest()
    assert digest(source) == record['sha256']
    size = destination.stat().st_size if destination.exists() else 0
    assert size <= record['bytes']
    known = json.loads(checkpoint.read_text()) if checkpoint.exists() else {}
    stat = destination.stat() if destination.exists() else None
    known_prefix = bool(stat and known.get('source_sha256') == record['sha256']
                        and known.get('destination') == str(destination)
                        and known.get('bytes') == size and known.get('mtime_ns') == stat.st_mtime_ns)
    # A complete destination is checked by its full SHA-256 below. Re-reading it
    # once for a byte comparison and again for hashing wastes an entire NAS pass.
    if size and size < record['bytes'] and not known_prefix:
        with source.open('rb') as left, destination.open('rb') as right:
            remaining = size
            while remaining:
                check_time()
                length = min(8 * 1024 * 1024, remaining)
                assert left.read(length) == right.read(length), 'NAS prefix mismatch; preserve and investigate'
                remaining -= length
    print('Existing prefix provenance checkpoint matched' if known_prefix
          else 'Existing prefix verified', size, flush=True)
    try:
        with source.open('rb') as left, destination.open('ab' if size else 'xb') as right:
            left.seek(size)
            while chunk := left.read(8 * 1024 * 1024):
                check_time()
                right.write(chunk)
    except TimeoutError:
        remember_prefix()
        raise
    remember_prefix()
    if a.copy_only:
        print('Copy complete; full destination hash and delivery record still required', flush=True)
        return
    assert digest(destination) == record['sha256']
    # Verify the mux retained exactly the already checked encoded packet data.
    import mux_verified_master as mux
    payloads = {}
    for kind, original in [('v', s / 'sleep_picture_candidate_v04.mp4'), ('a', s / 'sleep_audio_encoded_v05.m4a')]:
        check_time()
        expected = mux.sp_hash(original, kind)
        assert mux.sp_hash(source, kind) == expected
        payloads[kind] = expected
    streams = json.loads(sp.check_output(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(source)]))['streams']
    video = next(x for x in streams if x['codec_type'] == 'video')
    assert int(video['nb_frames']) == 195070
    result = dict(status='MUXED_AND_SAFETY_COPIED_REEL_AND_UAT_PENDING', file=source.name,
                  nas_path=str(destination), bytes=record['bytes'], sha256=record['sha256'],
                  frames=195070, streams=streams, packet_payload_sha256=payloads)
    (s / 'MASTER_DELIVERY_V01.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Full NAS hash and mux payloads PASS', flush=True)


if __name__ == '__main__':
    main()
