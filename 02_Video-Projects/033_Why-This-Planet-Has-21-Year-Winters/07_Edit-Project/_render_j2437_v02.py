#!/usr/bin/env python3
"""J2437: render changed opening, preserve original downstream picture/audio, run gates."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _assemble_033_full_master_v01 as a
a.CUTS_JSON = HERE / 'cuts_033_j2299_v01.json'
a.SHOT_MD = HERE / 'SHOT_LIST_v02.md'
a.SHOT_CSV = HERE / 'shot_list_v02.csv'
a.PACK = a.EDIT / 'full_master_v02_pack'
a.OUT = a.OUT.with_name(a.OUT.name.replace('_v01.', '_v02.'))
OLD = a.OUT.with_name(a.OUT.name.replace('_v02.', '_v01.'))
EXPECTED = '9e9712781a99ad07e6bc753728e716cbf5ef1dc4e4ad9b80ea45c1a55f785552'

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def main():
    if sha(OLD) != EXPECTED:
        raise RuntimeError('Original master hash differs from J2403 handoff; stop')
    a.WORK.mkdir(parents=True, exist_ok=True)
    a.PACK.mkdir(parents=True, exist_ok=True)
    tasks = a.build_tasks()
    assert len(tasks) == 147
    assert sum(t['n_main'] + t['n_breath'] for t in tasks[:13]) == 928
    assert all(t['n_main'] <= 96 for t in tasks[:13])
    assert all(Path(t['cut']['source']).is_file() for t in tasks[:13])
    print('Rendering 13 opening cuts; preserving v01 from frame 928 onward', flush=True)
    paths = a.render_all_cuts(tasks[:13])
    tail = a.WORK / 'v01_tail_from_frame928.mp4'
    if not a.frames_ok(tail, a.TOTAL_FRAMES - 928):
        a.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-reinit_filter', '0', '-i', str(OLD),
               '-vf', 'trim=start_frame=928,setpts=N/(24*TB)', *a.ENC,
               '-frames:v', str(a.TOTAL_FRAMES - 928), str(tail)])
    if not a.frames_ok(tail, a.TOTAL_FRAMES - 928):
        raise RuntimeError('Tail frame count differs from expected 14178; stop before concat')
    picture = a.WORK / 'picture_v02.mp4'
    a.concat_picture(paths + [tail], picture)
    assert a.frames_ok(picture, a.TOTAL_FRAMES)
    # Copy AAC packets unchanged; locked VO, bed, SFX and their timing are untouched.
    if not a.OUT.exists():
        a.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(picture), '-i', str(OLD),
               '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy', '-movflags', '+faststart', str(a.OUT)])
    assert a.frames_ok(a.OUT, a.TOTAL_FRAMES)
    # Reconstruct the unchanged pre-master stems from the prior documented mix gains.
    mix = json.loads((a.EDIT / 'full_master_v01_pack/mix_report_v01.json').read_text())
    a.run(['ffmpeg', '-v', 'error', '-y', '-i', str(a.VO_WAV), '-af',
           f'aformat=channel_layouts=stereo:sample_rates=48000,apad=whole_dur={a.TOTAL},atrim=0:{a.TOTAL}',
           str(a.WORK / 'vo_laid_v01.wav')])
    shutil.copy2(a.FILM / '06_Sound-Effects/uranus_sfx_stem_v01.wav', a.WORK / 'sfx_laid_v01.wav')
    a.run(['ffmpeg', '-v', 'error', '-y', '-i', str(a.BED_MP3), '-af',
           f"volume={mix['bed_gain_db']}dB,atrim=0:{a.TOTAL},aresample=48000", str(a.WORK / 'bed_laid_v01.wav')])
    # Prove the delivered audio packets match the original audio packets.
    audio_hashes = []
    for video in (OLD, a.OUT):
        raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(video), '-map', '0:a:0',
                                       '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-'], text=True)
        audio_hashes.append(raw.strip())
    assert audio_hashes[0] == audio_hashes[1]
    (a.PACK / 'preservation.json').write_text(json.dumps({
        'original_sha256': EXPECTED, 'audio_packet_hash': audio_hashes[0],
        'preserved_picture_from_frame': 928, 'preserved_picture_from_s': 928 / 24,
        'tail_method': 'disable filter reinit on color metadata changes, trim decoded frames from 928, regenerate CFR timestamps from frame index; no source substitutions',
        'sfx_check': 'unchanged existing stem; bed reconstructed at documented -30 dB gain',
        'perception': 'automated checks only; no claim of watching motion or hearing audio'
    }, indent=2) + '\n')
    results = a.run_gates()
    print(json.dumps(results, indent=2), flush=True)
    if any(results[k]['code'] for k in ('clip_check', 'picture_qa', 'polish_gate', 'music_gate', 'sfx_level')):
        raise RuntimeError('One or more automated gates failed; no UAT mirrors created')
    phone = a.OUT.with_name(a.OUT.stem + '_PHONE.mp4')
    if not phone.exists():
        a.run(['ffmpeg', '-v', 'error', '-i', str(a.OUT), '-vf', 'scale=960:540',
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-c:a', 'copy',
               '-movflags', '+faststart', str(phone)])
    mirrors = [Path('/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT'),
               Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/OWB UAT']
    for root in mirrors:
        root.mkdir(parents=True, exist_ok=True)
        for src in (a.OUT, phone):
            dst = root / src.name
            if not dst.exists():
                shutil.copy2(src, dst)
            assert sha(dst) == sha(src)
    (a.PACK / 'delivery_v02.json').write_text(json.dumps({
        'master': str(a.OUT), 'sha256': sha(a.OUT), 'phone': str(phone),
        'phone_sha256': sha(phone), 'mirrors': [str(p) for p in mirrors],
        'review': 'Automated checks complete; Chief review required'
    }, indent=2) + '\n')
    print('J2437 render and automated checks complete; Chief review required', flush=True)

if __name__ == '__main__':
    main()
