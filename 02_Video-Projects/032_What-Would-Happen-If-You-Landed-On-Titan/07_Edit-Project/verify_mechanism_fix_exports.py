"""Measure the two J2277 exports; this does not review motion or composites."""
import hashlib
import json
import subprocess
from pathlib import Path

import mechanism_graphics as graphics

HERE = Path(__file__).resolve().parent
OUT = Path('/Users/benjaminoats/_desk/cache/J2089/mechanism_renders_v02_fixes')
REVIEWED = {
    'r10_spectrum': '57576de51068f012d3790464010d661c38127d59bdbf343bc511fa162ec302e0',
    'r32_scalemap': '9fabc50ef3a8dfcfd01e53edb6182816c83da4208540c8ec667ce424a9947124',
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    manifest = json.loads((OUT / 'MECHANISM_MANIFEST_v01.json').read_text())
    records = [r for r in manifest['clips'] if r['rendered']]
    assert {r['id'] for r in records} == set(REVIEWED)
    results = []
    for record in records:
        clip_id = record['id']
        assert record['review_ref'] == 'J2277'
        assert sha(record['preview']) == record['preview_sha256'] == REVIEWED[clip_id]
        assert sha(record['render']) == record['sha256']
        spec = next(s for s in graphics.SPECS if s['id'] == clip_id)
        probe = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-show_streams', '-show_format',
            '-of', 'json', record['render']]))
        assert len(probe['streams']) == 1  # silent picture, no model audio
        stream = probe['streams'][0]
        assert (stream['width'], stream['height'], stream['pix_fmt'],
                stream['codec_name'], stream['r_frame_rate'], int(stream['nb_frames'])) == (
                    1920, 1080, 'argb', 'qtrle', '30/1', 108)
        assert abs(float(probe['format']['duration']) - 3.6) < .001
        decoder = subprocess.Popen([
            'ffmpeg', '-v', 'error', '-i', record['render'], '-f', 'rawvideo',
            '-pix_fmt', 'rgba', 'pipe:1'], stdout=subprocess.PIPE)
        try:
            for index in range(108):
                expected = graphics.frame(spec, index / 30).tobytes()
                assert decoder.stdout.read(len(expected)) == expected, (clip_id, index)
            assert not decoder.stdout.read(1)
            assert decoder.wait() == 0
        finally:
            decoder.stdout.close()
            if decoder.poll() is None:
                decoder.kill()
                decoder.wait()
        results.append(dict(id=clip_id, render=record['render'], sha256=record['sha256'],
                            reviewed_preview_sha256=REVIEWED[clip_id], review_ref='J2277',
                            exact_decoded_frames=108, duration=3.6, width=1920,
                            height=1080, fps=30, pixel_format='argb', audio_streams=0))
        print(clip_id, '108 exact decoded frames; reviewed preview hash matches', flush=True)
    result = dict(job='J2089', status='MEASUREMENTS_ONLY_NOT_COMPOSITE_APPROVAL',
                  exports=results, perceived_motion=False, perceived_audio=False,
                  remaining=['Licensed harvest and source allocations', 'R18/R23 graphics',
                             'Frame-0 native motion and APL rights', 'Graded composites and film gates'])
    (HERE / 'MECHANISM_FIX_EXPORT_VERIFICATION_v01.json').write_text(
        json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
