"""Verify the J2251 export mechanically; no audio or motion judgement."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
import uranus_graphic as g

p = argparse.ArgumentParser()
p.add_argument('--manifest', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
m = json.loads(a.manifest.read_text())
reviewed = json.loads(Path(g.__file__).with_name('URANUS_MANIFEST_v01.json').read_text())
assert m['review_ref'] == 'J2251' and m['approved_id'] == 'r52_uranus_21y'
assert m['preview_sha256'] == reviewed['preview_sha256'] == g.sha(m['preview'])
assert m['source_sha256'] == reviewed['source_sha256'] == g.sha(m['source'])
assert m['render_sha256'] == g.sha(m['render'])
info = json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames',
    '-show_streams','-of','json',m['render']]))
assert len(info['streams']) == 1
s = info['streams'][0]
assert (s['codec_name'],s['pix_fmt'],s['width'],s['height']) == ('qtrle','argb',1920,1080)
assert s['r_frame_rate'] == '30/1' and int(s['nb_read_frames']) == 108
assert abs(float(s['duration']) - 3.6) < .00001
proc = subprocess.Popen(['ffmpeg','-v','error','-i',m['render'],'-f','rawvideo',
    '-pix_fmt','rgba','pipe:1'],stdout=subprocess.PIPE)
# Every decoded frame must exactly equal the approved generator's RGBA frame.
for i in range(108):
    expected = g.frame(i/30).tobytes()
    actual = proc.stdout.read(len(expected))
    assert actual == expected, f'decoded frame {i} differs'
assert not proc.stdout.read(1)
assert proc.wait() == 0
negative = subprocess.run([sys.executable,g.__file__,'--render','--out',
    '/private/tmp/J2089-r52-approval-guard'],capture_output=True,text=True)
assert negative.returncode == 2 and 'requires named still approval' in negative.stderr
result = dict(job='J2089',id=m['id'],review_ref='J2251',render=m['render'],
    render_sha256=m['render_sha256'],preview_hash='MATCH_REVIEWED',source_hash='MATCH_REVIEWED',
    codec=s['codec_name'],pixel_format=s['pix_fmt'],width=s['width'],height=s['height'],
    fps=s['r_frame_rate'],duration=float(s['duration']),decoded_frames=108,
    exact_rgba_frames=108,unapproved_render_exit=negative.returncode,
    audio_perception=False,moving_video_perception=False,composite_status='UNVERIFIED',
    remaining=['Reviewed moving real background and contrast/placement checks',
               'Single PIA18182 appearance within R52; weic2310a tilt clause with INFRARED VIEW',
               'Final composite, moving-image review and film gates'])
a.out.write_text(json.dumps(result,indent=2)+'\n')
print('108 decoded frames exactly match approved generator; source/preview/render hashes match; qtrle ARGB 1920x1080 30fps 3.6s; approval guard rejects.')
