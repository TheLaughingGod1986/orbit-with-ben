#!/usr/bin/env python3
"""Verify J2141 MacBook opening, field, sky and bodies renders; creates contact sheets.

Technical and static frame verification only. Does not approve moving-plate
composites, audio/playback review or whole-film QA.
"""
import hashlib
import io
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent


def luma_stats(rgba):
    rgb = rgba.convert('RGB')
    vals = [0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in rgb.getdata()]
    vals.sort()
    return round(sum(vals) / len(vals), 2), round(vals[int(len(vals) * 0.95)], 2)


def verify_batch(manifest_name, report_name, sample_fracs, limitations):
    manifest = json.loads((HERE / manifest_name).read_text())
    words_path = HERE.parent / '02_Voiceover/stt/magnetic_field_flip_vo_v02a/stt_raw.json'
    assert hashlib.sha256(words_path.read_bytes()).hexdigest() == manifest['locked_words_sha256']
    graphics = manifest['graphics']
    sheet = Image.new('RGB', (1600, len(graphics) * 210), (28, 43, 63))
    checks = []
    for row_index, record in enumerate(graphics):
        media = Path(record['path'])
        digest = hashlib.sha256(media.read_bytes()).hexdigest()
        assert digest == record['sha256'], (media, digest, record['sha256'])
        probe = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(media)
        ]))
        assert len(probe['streams']) == 1
        stream = probe['streams'][0]
        expected_fmt = 'argb' if record['alpha'] else 'yuv420p'
        assert (stream['width'], stream['height'], stream['pix_fmt'], stream['r_frame_rate']) == (
            1920, 1080, expected_fmt, '25/1'
        ), stream
        dur = float(probe['format']['duration'])
        assert abs(dur - record['duration_s']) < 0.025, (dur, record['duration_s'])
        decoded = subprocess.run(
            ['ffmpeg', '-v', 'error', '-i', str(media), '-f', 'null', '-'],
            capture_output=True, check=True
        )
        assert not decoded.stderr, decoded.stderr.decode()
        samples = []
        for j, frac in enumerate(sample_fracs):
            seconds = round(min(record['duration_s'] - 0.04, record['duration_s'] * frac), 3)
            if j == 0 and record['alpha']:
                seconds = 0.0
            png = subprocess.check_output([
                'ffmpeg', '-v', 'error', '-ss', str(seconds), '-i', str(media),
                '-frames:v', '1', '-f', 'image2pipe', '-c:v', 'png', '-'
            ])
            frame = Image.open(io.BytesIO(png)).convert('RGBA')
            if record['alpha']:
                bbox = frame.getchannel('A').getbbox()
                if seconds == 0.0:
                    assert bbox is None, f'Expected transparent start frame for {record["id"]}'
                else:
                    assert bbox is not None, f'Expected visible alpha content at {seconds}s for {record["id"]}'
                bg = Image.new('RGBA', frame.size, (28, 43, 63, 255))
                bg.alpha_composite(frame)
                tile = bg.convert('RGB').resize((320, 180))
                sample_info = dict(
                    seconds=seconds,
                    alpha_bbox=bbox,
                    decoded_rgba_sha256=hashlib.sha256(frame.tobytes()).hexdigest(),
                )
            else:
                mean_y, p95_y = luma_stats(frame)
                assert mean_y >= 28.0, f'Mean luma below 28 on {record["id"]}: {mean_y}'
                tile = frame.convert('RGB').resize((320, 180))
                sample_info = dict(
                    seconds=seconds,
                    mean_luma=mean_y,
                    p95_luma=p95_y,
                    decoded_rgba_sha256=hashlib.sha256(frame.tobytes()).hexdigest(),
                )
            sheet.paste(tile, (j * 320, row_index * 210))
            ImageDraw.Draw(sheet).text(
                (j * 320 + 8, row_index * 210 + 184),
                f"{record['id']} +{seconds:.2f}s",
                fill='white'
            )
            samples.append(sample_info)
        distinct_hashes = len({s['decoded_rgba_sha256'] for s in samples})
        assert distinct_hashes >= 3, f'Expected animated variation in {record["id"]}'
        checks.append(dict(
            id=record['id'],
            row=record['row'],
            path=str(media),
            sha256=digest,
            bytes=media.stat().st_size,
            alpha=record['alpha'],
            pix_fmt=expected_fmt,
            duration_s=dur,
            full_decode='PASS',
            format='PASS',
            distinct_sample_frames=distinct_hashes,
            samples=samples,
        ))
    contact = Path(graphics[0]['path']).parent / 'CONTACT_TECHNICAL_v01.jpg'
    sheet.save(contact, quality=92)
    report = dict(
        job='J2141',
        status='technical_checks_only',
        spend_gbp=0,
        manifest=manifest_name,
        checks=checks,
        contact_sheet=str(contact),
        contact_sheet_sha256=hashlib.sha256(contact.read_bytes()).hexdigest(),
        limitations=limitations,
    )
    (HERE / report_name).write_text(json.dumps(report, indent=2) + '\n')
    print(f'{manifest_name}: {len(checks)} verified -> {contact}')


def main():
    verify_batch(
        'CODE_OPENING_MACBOOK_v01.json',
        'CODE_OPENING_MACBOOK_TECHNICAL_CHECK_v01.json',
        [0.0, 0.25, 0.5, 0.75, 0.94],
        [
            'Static samples and full decode only; no playback or audio perception claimed.',
            'poledrift and flip use verified GSFC_20171208_Archive_e000678 Earth disc.',
            'layers and when1905 are alpha overlays requiring graded moving plates.',
        ],
    )
    verify_batch(
        'CODE_FIELD_MACBOOK_v01.json',
        'CODE_FIELD_MACBOOK_TECHNICAL_CHECK_v01.json',
        [0.0, 0.25, 0.5, 0.75, 0.95],
        [
            'Static samples and full decode only; no playback or audio perception claimed.',
            'strata, matuyama_map and grid_shield are explanatory schematics, not measured maps.',
            'extinction_check is an alpha overlay requiring a graded moving fossil plate.',
        ],
    )
    verify_batch(
        'CODE_SKY_MACBOOK_v01.json',
        'CODE_SKY_MACBOOK_TECHNICAL_CHECK_v01.json',
        [0.0, 0.35, 0.58, 0.78, 0.94],
        [
            'Static samples and full decode only; no playback or audio perception claimed.',
            'aurora uses verified GSFC_20171208_Archive_e001788 Blue Marble.',
            'temp_poles and poles_map are alpha overlays requiring graded moving plates.',
        ],
    )
    verify_batch(
        'CODE_BODIES_MACBOOK_v01.json',
        'CODE_BODIES_MACBOOK_TECHNICAL_CHECK_v01.json',
        [0.05, 0.25, 0.5, 0.75, 0.94],
        [
            'Static samples and full decode only; no playback or audio perception claimed.',
            'Equal-diameter NASA Earth (as17-148-22727) and Mars (PIA00407) icons identify gravity bars (1.00 vs 0.38).',
            'Replaces CODE_SCALES_v01.json R44 gravity overlay; do not stack consecutively.',
        ],
    )


if __name__ == '__main__':
    main()
