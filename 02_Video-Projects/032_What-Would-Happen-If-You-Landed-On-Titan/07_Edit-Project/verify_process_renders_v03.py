"""Verify the seven J2198-reviewed process exports; no composite approval."""
import hashlib
import json
import subprocess
from pathlib import Path

CACHE = Path('/Users/benjaminoats/_desk/cache/J2089')
HERE = Path(__file__).resolve().parent


def main():
    clips = []
    for folder, refs, ids in [
        ('process_renders_v02', ['J2192', 'J2198'], {
            'r21_cycle_clouds', 'r21_cycle_lakes', 'r25_heated_suit',
            'r29_rain_comparison', 'r45_lift_mechanism'}),
        ('process_fire_renders_v03', ['J2198'], {
            'r39_fire_partners', 'r40_fire_missing'}),
    ]:
        manifest = json.loads((CACHE / folder / 'PROCESS_MANIFEST_v01.json').read_text())
        found = set()
        for clip in manifest['clips']:
            if clip['id'] not in ids:
                continue
            found.add(clip['id'])
            path = Path(clip['render'])
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            assert digest == clip['sha256'], path
            preview = Path(clip['preview'])
            assert hashlib.sha256(preview.read_bytes()).hexdigest() == clip['preview_sha256']
            probe = json.loads(subprocess.check_output([
                'ffprobe', '-v', 'error', '-count_frames', '-show_streams',
                '-show_format', '-of', 'json', str(path)]))
            stream = probe['streams'][0]
            assert len(probe['streams']) == 1
            assert (stream['width'], stream['height']) == (1920, 1080)
            assert stream['pix_fmt'] == 'argb'
            assert stream['r_frame_rate'] == '30/1'
            assert int(stream['nb_read_frames']) == 108
            assert abs(float(probe['format']['duration']) - 3.6) < .001
            subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path),
                            '-f', 'null', '-'], check=True, capture_output=True)
            clips.append(dict(id=clip['id'], row=clip['row'], render=str(path),
                              sha256=digest, bytes=path.stat().st_size,
                              preview=str(preview), preview_sha256=clip['preview_sha256'],
                              review_refs=refs, frames=108, duration=3.6,
                              dimensions=[1920,1080], pix_fmt='argb',
                              full_decode='OK', source_rows=clip['source_rows'],
                              composite_status='UNVERIFIED'))
        assert found == ids, (folder, found, ids)
    assert len(clips) == 7
    result = dict(job='J2089', spend_gbp=0,
                  status='SEVEN_REVIEWED_PROCESS_EXPORTS_TECHNICALLY_VERIFIED',
                  clips=clips,
                  limitations=['No audio or moving-video perception claimed',
                               'Final moving-plate composites, timing and gates remain',
                               'Frame-0 motion, PIA07232 reuse and APL rights unresolved',
                               'J2177 mechanism review remains separate'])
    (HERE / 'PROCESS_RENDER_MANIFEST_v03.json').write_text(json.dumps(result, indent=2)+'\n')
    print('7/7 hashes, alpha formats, dimensions, duration, frames and full decodes verified.')


if __name__ == '__main__':
    main()
