#!/usr/bin/env python3
"""J2141: one bounded R14 SDO observation candidate, never automatic KEEP.

Use /usr/bin/python3 (Pillow). HTTPS downloads use curl's current TLS stack.
Original, source evidence and decoded static samples remain outside git.
"""
import argparse
import hashlib
import io
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageStat

HERE = Path(__file__).resolve().parent
PAGE = 'https://svs.gsfc.nasa.gov/4323/'
NAME = 'June2015LimbLoops_304A_1080p.mp4'
IDENT = 'SVS4323_SDO_AIA304_motion'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fetch(url, path):
    if path.exists():
        raise FileExistsError(path)
    subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                    '--max-time', '90', '--proto', '=https', '--proto-redir', '=https',
                    '--output', str(path), url], check=True)
    return path.read_bytes()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--pool', type=Path, default=HERE/'HARVEST_POOL_v01.json')
    args = ap.parse_args()
    pool = json.loads(args.pool.read_text())
    if any(a['asset_id'] == IDENT for a in pool['assets']):
        raise ValueError('Already registered; preserve candidate and investigation budget')
    args.out.mkdir(parents=True, exist_ok=False)
    evidence = []
    for name, url in [('svs4323.html', PAGE), ('svs4323.json', 'https://svs.gsfc.nasa.gov/api/4323/'),
                      ('svs_usage.html', 'https://svs.gsfc.nasa.gov/help/'),
                      ('nasa_media_policy.html', 'https://www.nasa.gov/nasa-brand-center/images-and-media/')]:
        p = args.out/name
        fetch(url, p)
        evidence.append(dict(url=url, path=str(p), sha256=sha(p)))
    api = json.loads((args.out/'svs4323.json').read_text())
    media = [i.get('instance', i.get('media', {})) for g in api['media_groups'] for i in g['items']]
    m, = [m for m in media if m.get('filename') == NAME]
    source = m['url'].replace('http://', 'https://', 1)
    original = args.out/NAME
    fetch(source, original)
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(original)]))
    v, = [s for s in probe['streams'] if s['codec_type'] == 'video']
    if (v['width'], v['height']) != (1920, 1080):
        raise ValueError('Unexpected dimensions')
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(original), '-map', '0:v:0', '-f', 'null', '-'], check=True)
    # One interval, examined once; sampling proves changing decoded pixels only.
    times = [2, 3, 4, 5, 6]
    samples = []
    sheet = Image.new('RGB', (1920, 760), (30, 45, 65))
    draw = ImageDraw.Draw(sheet)
    for n, t in enumerate(times):
        raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(original), '-frames:v', '1', '-f', 'image2pipe', '-c:v', 'png', '-'])
        im = Image.open(io.BytesIO(raw)).convert('RGB')
        p = args.out/('sample_%02ds.png' % t)
        im.save(p)
        y = im.convert('YCbCr').getchannel('Y'); hist = y.histogram(); total = im.width*im.height
        cumulative = 0
        for p95, count in enumerate(hist):
            cumulative += count
            if cumulative >= total*.95: break
        samples.append(dict(time_s=t, path=str(p), sha256=sha(p),
                            mean_luma=round(ImageStat.Stat(y).mean[0], 2), p95_luma=p95))
        im.thumbnail((620, 349)); x=(n%3)*640; yy=(n//3)*380
        sheet.paste(im, (x, yy)); draw.text((x+12, yy+351), 'SDO AIA 304 | source %.1f s' % t, fill='white')
    contact = args.out/'CONTACT_SDO_MOTION_v01.jpg'; sheet.save(contact, quality=94)
    assert len({s['sha256'] for s in samples}) == len(samples)
    rec = dict(asset_id=IDENT, title=api['title'], source_page=PAGE, source_url=source,
               local_path=str(original), sha256=sha(original), bytes=original.stat().st_size,
               width=v['width'], height=v['height'], fps=v['r_frame_rate'], duration_s=float(probe['format']['duration']),
               rows=[14], assigned_uses=0, max_uses=2, native_motion=True,
               observation='SDO AIA 304 angstrom EUV observation, time-compressed and false-colour; not a visible-light temperature comparison or a computer simulation.',
               credit="NASA's Scientific Visualization Studio / SDO",
               licence='Public domain subject to NASA media conditions',
               licence_status='SVS_public_domain_default_no_item_exception_found_worker_check',
               rights_review='SVS help permits use unless otherwise noted. Item page requests NASA SVS credit; no separate rights exception or licensed music found. Preserve named contractor credits in source/API evidence. No endorsement; use video silently.',
               source_evidence=evidence, download_status='downloaded', generation_authorized=False,
               candidate_interval=dict(source_in_s=2, source_out_s=6, duration_s=4, speed=1,
                                       crop='full 1920x1080; no stretch or upscale',
                                       film_placement='R14 after core graphic; compositor to fit locked line and FACT overlay'),
               review_status='pending_static_inspection_grade_composite_and_reviewer_decision',
               review_note='Candidate only. No KEEP, playback review, film gate or claim of temperature from false colour. Add corner NASA credit; check full composite for near-black, grain and FACT clearance.')
    report = dict(job='J2141', asset_id=IDENT, spend_gbp=0, full_decode='PASS', probe=probe,
                  original_sha256=rec['sha256'], decoded_samples=samples, distinct_sample_hashes=True,
                  contact_sheet=dict(path=str(contact), sha256=sha(contact)),
                  limitations='Changing sample pixels do not prove motion quality; no audio or actual playback review. Full film/composite gates remain open.')
    report_path = HERE/'HARVEST_SDO_MOTION_TECHNICAL_CHECK_v01.json'
    if report_path.exists(): raise FileExistsError(report_path)
    report_path.write_text(json.dumps(report, indent=2)+'\n')
    pool['assets'].append(rec)
    pool['sdo_r14_motion_investigation'] = dict(date='2026-11-07', candidates_examined=1,
        interval_examined_s=[2, 6], status='one_candidate_downloaded_and_sampled_not_admitted',
        budget_note='One new moving candidate; prior PIA22661 still was already unsuitable. Do not reset cumulative 20-minute/three-candidate budget.',
        next_action='Review sampled source and composite over locked R14; no further search unless this candidate fails with a concrete reason.')
    args.pool.write_text(json.dumps(pool, indent=2)+'\n')
    print(json.dumps(dict(asset_id=IDENT, duration_s=rec['duration_s'], samples=samples, contact_sheet=str(contact)), indent=2))


if __name__ == '__main__':
    main()
