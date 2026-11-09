#!/usr/bin/env python3
"""Verify the MacBook mechanism checkpoint, not film/composite approval."""
import hashlib, io, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
HERE = Path(__file__).resolve().parent

def main():
    import math
    from grain_revision_graphics import grain_angle
    assert all(abs(grain_angle(i, 5.6)-math.pi) < 1e-9 for i in range(15))
    manifest = HERE / 'CODE_GRAINS_v04.json'
    data = json.loads(manifest.read_text())
    sheet = Image.new('RGB', (1200, 2*250), (25, 42, 64))
    draw = ImageDraw.Draw(sheet)
    checks = []
    for row, item in enumerate(data['graphics']):
        path = Path(item['path'])
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
            '-show_streams', '-show_format', '-of', 'json', str(path)]))
        stream = probe['streams'][0]
        duration = float(probe['format']['duration'])
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path),
                        '-f', 'null', '-'], check=True)
        assert digest == item['sha256'], path
        assert (stream['width'], stream['height']) == (1920, 1080), path
        assert stream['r_frame_rate'] == '25/1', path
        assert abs(duration-item['duration_s']) <= .02, path
        assert stream['pix_fmt'] == ('argb' if item['alpha'] else 'yuv420p'), path
        assert len(probe['streams']) == 1 and stream['codec_type'] == 'video', path
        samples = []
        for col, fraction in enumerate((.15, .5, .85)):
            at = fraction * duration
            raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(at),
                '-i', str(path), '-frames:v', '1', '-f', 'image2pipe',
                '-vcodec', 'png', '-'])
            im = Image.open(io.BytesIO(raw)).convert('RGBA')
            bg = Image.new('RGBA', im.size, (25,42,64,255))
            bg.alpha_composite(im)
            thumb = ImageOps.contain(bg.convert('RGB'), (390, 220))
            sheet.paste(thumb, (col*400, row*250))
            draw.text((col*400+5, row*250+224), f"R{item['row']} {at:.2f}s", fill='white')
            samples.append({'time_s': round(at,3),
                'decoded_rgba_sha256': hashlib.sha256(im.tobytes()).hexdigest()})
        assert len({x['decoded_rgba_sha256'] for x in samples}) == 3, path
        checks.append({'id': item['id'], 'path': str(path), 'sha256': digest,
            'hash_match': True, 'width': stream['width'], 'height': stream['height'],
            'fps': stream['r_frame_rate'], 'pix_fmt': stream['pix_fmt'],
            'duration_s': duration, 'full_decode': 'PASS',
            'three_sample_frames_differ': True, 'samples': samples})
    contact = Path(data['graphics'][0]['path']).parent / 'CONTACT_TECHNICAL_v04.jpg'
    if contact.exists(): raise FileExistsError(contact)
    sheet.save(contact, quality=93)
    report = {'job':'J2141', 'worker':'macbook', 'spend_gbp':0,
        'scope':'Technical decode and three static samples; no motion, audio, composite or approval claim',
        'manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
        'contact_sheet':str(contact),
        'contact_sheet_sha256':hashlib.sha256(contact.read_bytes()).hexdigest(),
        'checks':checks}
    target = HERE / 'CODE_GRAINS_TECHNICAL_CHECK_v04.json'
    if target.exists(): raise FileExistsError(target)
    target.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'verified':len(checks), 'contact_sheet':str(contact)}))

if __name__ == '__main__': main()
