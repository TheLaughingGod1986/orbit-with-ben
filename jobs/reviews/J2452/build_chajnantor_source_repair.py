#!/usr/bin/env python3
"""Render the original Chajnantor shot without the master's crushed-shadow LUT.

This is a bounded component, not approval of the chapter or compilation.
"""
import argparse
import json
import subprocess
from pathlib import Path
from build_orion_source_repair import sha, run

p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
a.out.mkdir(parents=True, exist_ok=False)
from PIL import Image, ImageDraw, ImageFont
credit = a.out / 'credit.png'
overlay = Image.new('RGBA', (1920, 1080))
ImageDraw.Draw(overlay).text((45, 1025), 'ESO',
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 27),
    fill=(234, 230, 223, 140))
overlay.save(credit)
source = Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/chajnantor_mw.m4v')
# Preserve the actual sky and native motion. The old master used a black-level
# subtraction LUT. Start again from the original; no gamma or black lift.
graph = ('setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,fps=30,'
         'colorchannelmixer=rr=.85:gg=.85:bb=.85,'
         'limiter=min=16:max=180:planes=1,format=yuv420p')
output = a.out / 'chajnantor_source_repair.mp4'
frames = round(240.78 * 30) - round(234.30 * 30)
run(['-ss', '3.25', '-i', str(source), '-loop', '1', '-i', str(credit),
     '-filter_complex', '[0:v]' + graph + '[plate];[plate][1:v]overlay=0:0,format=yuv420p[v]', '-map', '[v]',
     '-frames:v', str(frames), '-an', '-c:v', 'libx264', '-preset', 'fast',
     '-crf', '18', '-threads', '4', '-pix_fmt', 'yuv420p',
     '-colorspace', 'bt709', '-color_trc', 'bt709', '-color_primaries', 'bt709',
     '-video_track_timescale', '90000', str(output)])
run(['-i', str(output), '-f', 'null', '-'])
info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
    '-count_frames', '-show_streams', '-of', 'json', str(output)]))['streams'][0]
assert int(info['nb_read_frames']) == frames
cuts = [dict(row='24', source=source.name, kind='video', timeline_in=0,
    timeline_out=frames / 30, upscale=1.5, framing=dict(offset=3.25))]
(a.out / 'cuts.json').write_text(json.dumps(cuts, indent=2) + '\n')
report = dict(status='ORIGINAL_SOURCE_COMPONENT_NOT_INTEGRATED_NOT_UAT',
    source=str(source), source_sha256=sha(source), output=str(output),
    sha256=sha(output), frames=frames, duration_s=frames / 30,
    master_range_s=[254.8, 261.28], chapter_range_s=[234.3, 240.78],
    source_interval_s=[3.25, 3.25 + frames / 30], filter=graph,
    provenance=dict(id='chajnantor_mw', title='Milky Way over Chajnantor',
        page='https://www.eso.org/public/videos/chajnantormilkyway/',
        credit='ESO', licence='CC BY 4.0 per film SOURCE_POOL_v03.json'),
    limitations=['Existing footage under pulsation narration is a sky establishing shot, not a resolved pulsation observation.',
        'Dissolve handles, reuse review and integration remain.',
        'Run normal picture QA; no failure is waived.'])
(a.out / 'REPORT.json').write_text(json.dumps(report, indent=2) + '\n')
for i, t in enumerate([0, 1.6, 3.2, 4.8, (frames - 1) / 30]):
    run(['-ss', str(t), '-i', str(output), '-frames:v', '1',
         '-vf', 'scale=960:540', str(a.out / f'frame_{i}.jpg')])
print(output)
