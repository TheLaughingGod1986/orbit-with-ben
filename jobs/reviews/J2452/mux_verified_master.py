#!/usr/bin/env python3
"""Mux only fully decoded candidates; add and hash-check the NAS safety copy.

Run within one worker session with sufficient time for both copies and hashes.
Never replaces an existing media file. Interrupted copies are retained and must
be investigated before retrying with another version.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
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
    picture = folder / 'sleep_picture_candidate_v04.mp4'
    audio = folder / 'sleep_audio_encoded_v05.m4a'
    coverage = json.loads((folder / 'FINAL_DECODE_BLOCKS_V04.json').read_text())
    assert coverage['status'] == 'PASS'
    cursor = 0
    for block in sorted(coverage['blocks'], key=lambda b: b['first_frame']):
        assert block['first_frame'] == cursor and block['exit_code'] == 0
        assert block['frames'] == min(1800, 195070 - cursor)
        cursor += block['frames']
    assert cursor == 195070
    assert sha(picture) == coverage['picture_sha256']
    assert sha(audio) == '2ed0fc501d49a91f2987632b3931124e0c15f017883959396c8fe5e2dbd6bb01'
    destination = args.destination
    store = Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01')
    assert Path('/Volumes/data').is_mount()
    assert destination.resolve().is_relative_to(store.resolve())
    assert destination.parent.is_dir() and not destination.exists()
    master = folder / destination.name
    assert not master.exists()
    subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-n', '-i', str(picture),
                    '-i', str(audio), '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy',
                    '-movflags', '+faststart', str(master)], check=True, timeout=240)
    # Safety copy follows mux immediately; preserve both files on any failure.
    with master.open('rb') as source, destination.open('xb') as target:
        shutil.copyfileobj(source, target, length=8 * 1024 * 1024)
    expected = sha(master)
    assert sha(destination) == expected
    packet_hashes = {}
    for kind, original in [('v', picture), ('a', audio)]:
        def payload_hash(path):
            return sp_hash(path, kind)
        reference = payload_hash(original)
        assert payload_hash(master) == reference, f'{kind} packet payload changed during mux'
        packet_hashes[kind] = reference
    streams = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
                        '-show_streams', '-of', 'json', str(master)]))['streams']
    video = next(s for s in streams if s['codec_type'] == 'video')
    assert int(video['nb_frames']) == 195070
    assert abs(float(video['duration']) - 195070 / 30) < .04
    result = dict(status='MUXED_AND_SAFETY_COPIED_REEL_AND_UAT_PENDING',
                  file=master.name, nas_path=str(destination), bytes=master.stat().st_size,
                  sha256=expected, frames=int(video['nb_frames']), streams=streams,
                  packet_payload_sha256=packet_hashes)
    # Keep device-specific stream fields in local scratch, not public git.
    (folder / 'MASTER_DELIVERY_V01.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'streams'}), flush=True)


def sp_hash(path, kind):
    value = subprocess.check_output(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(path),
                  '-map', f'0:{kind}:0', '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-'], timeout=180)
    return value.decode().strip()


if __name__ == '__main__':
    main()
