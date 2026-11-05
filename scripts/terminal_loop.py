"""Evidence-checked, opt-in prescribed Short return; never a media KEEP.

Schema and limits: STUDIO_PLAYBOOK.md, Picture QA terminal-loop contract.
All file references are actual local inputs, not attestations that a check passed.
"""
import hashlib
import json
import math
import subprocess
from pathlib import Path


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('expected a finite number')
    return value


def digest(path):
    with open(path, 'rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def evidence(item):
    path = Path(item['path']).resolve(strict=True)
    if digest(path) != item['sha256']:
        raise ValueError(f'evidence hash mismatch: {path}')
    return path


def probe(path):
    return json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,avg_frame_rate:format=duration', '-of', 'json', str(path)],
        capture_output=True, check=True, timeout=30).stdout)


def frame(path, time, crop=None):
    filters = []
    if crop:
        x, y, w, h = crop
        filters.append(f'crop={w}:{h}:{x}:{y}')
    filters += ['scale=96:170', 'format=gray']
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(time), '-i', str(path),
        '-frames:v', '1', '-vf', ','.join(filters), '-f', 'rawvideo', '-'],
        capture_output=True, check=True, timeout=30).stdout
    if len(raw) != 96 * 170:
        raise ValueError('source/render frame unavailable')
    return raw


def validate(cuts, declaration, video=None):
    """Return a structured result; invalid declarations never confer an exemption.

    preflight eligibility verifies actual source/VO/evidence bytes and bounds. The
    rendered pass samples opening and tail correspondence, not seamless motion.
    """
    result = dict(status='invalid', eligible_cut=None, errors=[], evidence={},
                  pending=['rendered pixel/loop checks', 'human moving/phone and audio review'])
    try:
        d = declaration
        if type(d['version']) is not int or d['version'] != 1 or d['format'] != 'short':
            raise ValueError('only version 1 prescribed Shorts are supported')
        if set(d) != {'version','format','cut','duration','last_vo_word','source','words','vo','prescription','source_in','source_out','framing'}:
            raise ValueError('missing or unexpected terminal-loop declaration fields')
        if type(d['cut']) is not int or d['cut'] != len(cuts) - 1 or d['cut'] < 2:
            raise ValueError('exactly one final row must be declared')
        # No roles on body rows and no multiple declarations, even if names differ.
        if any(c.get('role') for c in cuts[:-1]) or cuts[-1].get('role') != 'prescribed_terminal_loop':
            raise ValueError('only final row may have prescribed_terminal_loop role')
        k = d['cut']; first, tail = cuts[0], cuts[k]
        duration = number(d['duration'])
        if not 22 <= duration <= 27:
            raise ValueError('Short duration must be 22–27 seconds')
        previous = 0
        for c in cuts:
            a, b = number(c['timeline_in']), number(c['timeline_out'])
            if abs(a - previous) > 1e-6 or b <= a:
                raise ValueError('timeline must be ordered, contiguous, start at zero')
            previous = b
        if abs(previous - duration) > 1e-6:
            raise ValueError('duration does not match complete timeline')
        length = tail['timeline_out'] - tail['timeline_in']
        if not 0 < length <= 1.0 + 1e-6 or tail.get('spoken', '').strip():
            raise ValueError('return must be <=1 second and contain no spoken line')
        prescription = evidence(d['prescription'])
        words_path = evidence(d['words'])
        words = json.loads(words_path.read_text())
        vo = evidence(d['vo'])
        if words['vo_sha256'] != digest(vo) or not words['words']:
            raise ValueError('word alignment must reference actual locked VO')
        ends = [number(w['end']) for w in words['words']]
        if any(e < 0 for e in ends) or ends != sorted(ends):
            raise ValueError('invalid word alignment ends')
        last_word = number(d['last_vo_word'])
        if abs(last_word - ends[-1]) > 1e-6 or last_word > tail['timeline_in']:
            raise ValueError('return overlaps last VO word or alignment disagrees')
        src = evidence(d['source'])
        # Resolve aliases to the opening, but never manufacture a new identity.
        if Path(first['source']).resolve(strict=True) != src or Path(tail['source']).resolve(strict=True) != src:
            raise ValueError('return must reference the actual opening source')
        if first.get('video') is not True or tail.get('video') is not True:
            raise ValueError('opening/return must be footage')
        info = probe(src); stream = info['streams'][0]
        bound = float(info['format']['duration'])
        if not math.isfinite(bound) or bound <= 0:
            raise ValueError('invalid probed source duration')
        # This intentionally small recipe admits no unmodelled filters/speed/flip.
        for c in (first, tail):
            if set(c['framing']) != {'offset', 'crop', 'output'}:
                raise ValueError('explicit offset, crop and output framing required')
        if {a: b for a, b in first['framing'].items() if a != 'offset'} != d['framing'] or \
           {a: b for a, b in tail['framing'].items() if a != 'offset'} != d['framing']:
            raise ValueError('opening and return framing must match declaration')
        crop, output = d['framing']['crop'], d['framing']['output']
        if len(crop) != 4 or len(output) != 2 or any(type(n) is not int for n in crop + output):
            raise ValueError('crop/output must contain integer pixels')
        x, y, w, h = crop
        if min(x, y) < 0 or min(w, h, *output) <= 0 or x+w > stream['width'] or y+h > stream['height']:
            raise ValueError('crop/output outside source bounds')
        if output[0] * 16 != output[1] * 9:
            raise ValueError('output must be portrait 9:16')
        start, end = number(d['source_in']), number(d['source_out'])
        if start < 0 or end > bound or end <= start or abs(end-start-length) > 1e-6:
            raise ValueError('source interval outside bounds or duration mismatch')
        if number(first['framing']['offset']) != start or number(tail['framing']['offset']) != start:
            raise ValueError('source interval must return to actual opening offset')
        if start + first['timeline_out'] > bound:
            raise ValueError('opening interval outside source bounds')
        # Decode both ends of the explicit interval, not just a caller's metadata.
        fps_n, fps_d = map(float, stream['avg_frame_rate'].split('/'))
        fps = fps_n / fps_d
        if not math.isfinite(fps) or fps <= 0:
            raise ValueError('invalid source frame rate')
        sample_end = max(start, end - 1/fps)
        samples = [(start, 0.0, tail['timeline_in']),
                   (sample_end, sample_end-start, tail['timeline_in']+sample_end-start)]
        frame_hashes = []
        for source_t, _, _ in samples:
            frame_hashes.append(hashlib.sha256(frame(src, source_t, crop)).hexdigest())
        result['evidence'] = dict(source=str(src), sha256=digest(src), source_in=start, source_out=end,
            source_duration=bound, framing=d['framing'], last_vo_word=last_word,
            words_sha256=digest(words_path), prescription_sha256=digest(prescription),
            source_sample_sha256=frame_hashes)
        if video:
            render = probe(video); rs = render['streams'][0]
            if [rs['width'], rs['height']] != output or abs(number(float(render['format']['duration']))-duration) > .05:
                raise ValueError('rendered dimensions/duration disagree with Short contract')
            errors = []
            for source_t, opening_t, tail_t in samples:
                expected = frame(src, source_t, crop)
                for t in (opening_t, tail_t):
                    actual = frame(video, t)
                    mae = sum(abs(a-b) for a,b in zip(expected, actual)) / len(actual)
                    errors.append(round(mae, 4))
                    if mae > 8:
                        raise ValueError(f'rendered opening/return correspondence failed at {t:g}s (MAE {mae:.2f})')
            result['evidence']['rendered_frame_mae'] = errors
            result['evidence']['render_sha256'] = digest(video)
            result['pending'] = ['human moving/phone and audio review; samples do not establish seamless motion']
        result.update(status='rendered_correspondence' if video else 'source_preflight', eligible_cut=k)
    except (KeyError, TypeError, ValueError, OSError, IndexError, subprocess.SubprocessError, ZeroDivisionError) as exc:
        result['errors'].append(str(exc))
    return result
