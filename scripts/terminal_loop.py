"""Evidence-checked, opt-in prescribed Short return; never a media KEEP.

Schema and limits: STUDIO_PLAYBOOK.md, Picture QA terminal-loop contract.
All file references are actual local inputs, not attestations that a check passed.
"""
import hashlib
import importlib.util
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
        '-show_entries', 'stream=width,height,avg_frame_rate,sample_aspect_ratio:format=duration', '-of', 'json', str(path)],
        capture_output=True, check=True, timeout=30).stdout)


def frame(path, time, crop=None, recipe=None):
    filters = list(recipe or [])
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


def integers(value, length, name):
    if not isinstance(value, list) or len(value) != length or any(type(n) is not int for n in value):
        raise ValueError(f'{name} must contain integer pixels')
    return value


def scale_before_crop(framing, stream):
    """Version 2 has one fixed operation order, with no implicit parameters."""
    if set(framing) != {'operations', 'output', 'portrait_width'}:
        raise ValueError('unexpected or missing version 2 framing fields')
    ops = framing['operations']
    fields = [{'op','width','height','interpolation'}, {'op','x','y','width','height'},
              {'op','num','den'}, {'op','num','den'}]
    if not isinstance(ops, list) or len(ops) != 4:
        raise ValueError('scale, crop, setsar, fps operations required in order')
    for op, name, keys in zip(ops, ('scale','crop','setsar','fps'), fields):
        if not isinstance(op, dict) or set(op) != keys or op['op'] != name:
            raise ValueError('invalid operation fields or order')
        if any(type(v) is not int for k,v in op.items() if k not in ('op','interpolation')):
            raise ValueError('operation parameters must be integers')
    scale, crop, sar, fps = ops
    sw, sh = scale['width'], scale['height']
    iw, ih = stream['width'], stream['height']
    if min(sw, sh) <= 0 or sw * ih != sh * iw or sw * 100 > iw * 235:
        raise ValueError('scale must be uniform and at most 2.35x')
    if scale['interpolation'] != 'lanczos':
        raise ValueError('only explicit lanczos interpolation is supported')
    x,y,w,h = (crop[k] for k in ('x','y','width','height'))
    output = integers(framing['output'], 2, 'output')
    if min(x,y) < 0 or min(w,h) <= 0 or x+w > sw or y+h > sh:
        raise ValueError('crop outside scaled source bounds')
    if output != [w,h] or any(n <= 0 or n % 2 for n in output):
        raise ValueError('output must equal crop and contain positive even dimensions')
    rule = framing['portrait_width']
    if rule == 'exact':
        if w * 16 != h * 9:
            raise ValueError('output must be exact portrait 9:16')
    elif rule == 'nearest_even':
        # Integer arithmetic: nearest even width, exact ties toward the larger width.
        nearest = 2 * ((h * 9 + 16) // 32)
        if w != nearest or abs(w * 16 - h * 9) > 16:
            raise ValueError('output width must be nearest even to height * 9/16')
    else:
        raise ValueError('explicit exact or nearest_even portrait width rule required')
    if sar != {'op':'setsar','num':1,'den':1}:
        raise ValueError('square sample aspect 1:1 required')
    if stream.get('sample_aspect_ratio') != '1:1':
        raise ValueError('square source pixels required')
    if min(fps['num'],fps['den']) <= 0:
        raise ValueError('positive rational output fps required')
    return output, [f'scale={sw}:{sh}:flags=lanczos', f'crop={w}:{h}:{x}:{y}',
                    'setsar=1/1', f"fps={fps['num']}/{fps['den']}"]


def shorts_band():
    """Read this checkout's open gate, the channel's single duration authority."""
    path = Path(__file__).resolve().parents[1] / '00_Brand/Channel-Setup/tools/gate_shorts_open.py'
    spec = importlib.util.spec_from_file_location('_terminal_loop_open_gate', path)
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    low, high = map(number, gate.DUR_BAND)
    if low <= 0 or high < low:
        raise ValueError('invalid channel Shorts duration band')
    return low, high


def validate(cuts, declaration, video=None):
    """Return a structured result; invalid declarations never confer an exemption.

    preflight eligibility verifies actual source/VO/evidence bytes and bounds. The
    rendered pass samples opening and tail correspondence, not seamless motion.
    """
    result = dict(status='invalid', eligible_cut=None, errors=[], evidence={},
                  pending=['rendered pixel/loop checks', 'human moving/phone and audio review'])
    try:
        d = declaration
        if type(d['version']) is not int or d['version'] not in (1, 2) or d['format'] != 'short':
            raise ValueError('only version 1 or 2 prescribed Shorts are supported')
        if set(d) != {'version','format','cut','duration','last_vo_word','source','words','vo','prescription','source_in','source_out','framing'}:
            raise ValueError('missing or unexpected terminal-loop declaration fields')
        if type(d['cut']) is not int or d['cut'] != len(cuts) - 1 or d['cut'] < 2:
            raise ValueError('exactly one final row must be declared')
        # No roles on body rows and no multiple declarations, even if names differ.
        if any(c.get('role') for c in cuts[:-1]) or cuts[-1].get('role') != 'prescribed_terminal_loop':
            raise ValueError('only final row may have prescribed_terminal_loop role')
        k = d['cut']; first, tail = cuts[0], cuts[k]
        duration = number(d['duration'])
        low, high = shorts_band()
        if not low <= duration <= high:
            raise ValueError(f'Short duration must be {low:g}–{high:g} seconds')
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
            if set(c['framing']) != ({'offset', 'crop', 'output'} if d['version'] == 1 else
                                     {'offset', 'operations', 'output', 'portrait_width'}):
                raise ValueError('explicit offset, crop and output framing required')
        if {a: b for a, b in first['framing'].items() if a != 'offset'} != d['framing'] or \
           {a: b for a, b in tail['framing'].items() if a != 'offset'} != d['framing']:
            raise ValueError('opening and return framing must match declaration')
        if d['version'] == 2:
            expected = json.dumps(d['framing'], sort_keys=True, allow_nan=False)
            for row in (first, tail):
                actual = {k:v for k,v in row['framing'].items() if k != 'offset'}
                if json.dumps(actual, sort_keys=True, allow_nan=False) != expected:
                    raise ValueError('opening and return recipe types/values must match exactly')
        recipe = None
        crop = None
        if d['version'] == 2:
            output, recipe = scale_before_crop(d['framing'], stream)
        else:
            if set(d['framing']) != {'crop', 'output'}:
                raise ValueError('unexpected version 1 framing fields')
            crop = integers(d['framing']['crop'], 4, 'crop')
            output = integers(d['framing']['output'], 2, 'output')
            x, y, w, h = crop
            if min(x, y) < 0 or min(w, h, *output) <= 0 or x+w > stream['width'] or y+h > stream['height']:
                raise ValueError('crop/output outside source bounds')
            if output[0] * 16 != output[1] * 9:
                raise ValueError('output must be portrait 9:16')
        start, end = number(d['source_in']), number(d['source_out'])
        if start < 0 or end > bound or end <= start or abs(end-start-length) > 1e-6:
            raise ValueError('source interval outside bounds or duration mismatch')
        opening_start = number(first['framing']['offset'])
        opening_end = opening_start + first['timeline_out']
        if number(tail['framing']['offset']) != start:
            raise ValueError('source interval must match actual tail offset')
        if opening_start < 0 or opening_end > bound:
            raise ValueError('opening interval outside source bounds')
        if start < opening_end and opening_start < end:
            raise ValueError('terminal source window overlaps opening')
        if abs(end - opening_start) > 1e-6:
            raise ValueError('terminal pre-roll must end at opening source offset')
        # Decode both ends of the explicit interval, not just a caller's metadata.
        fps_n, fps_d = map(float, stream['avg_frame_rate'].split('/'))
        fps = fps_n / fps_d
        if not math.isfinite(fps) or fps <= 0:
            raise ValueError('invalid source frame rate')
        # The tail is native pre-roll immediately before frame zero, not a replay.
        # Check each window against its own source frames.
        samples = [(opening_start, 0.0),
                   (max(opening_start, opening_end - 1/fps),
                    max(0.0, first['timeline_out'] - 1/fps)),
                   (start, tail['timeline_in']),
                   (max(start, end - 1/fps), tail['timeline_out'] - min(length, 1/fps))]
        frame_hashes = [hashlib.sha256(frame(src, t, crop, recipe)).hexdigest() for t, _ in samples]
        result['evidence'] = dict(source=str(src), sha256=digest(src), source_in=start, source_out=end,
            opening_source_in=opening_start, opening_source_out=opening_end,
            source_duration=bound, framing=d['framing'], last_vo_word=last_word,
            words_sha256=digest(words_path), prescription_sha256=digest(prescription),
            source_sample_sha256=frame_hashes)
        if video:
            render = probe(video); rs = render['streams'][0]
            if [rs['width'], rs['height']] != output or abs(number(float(render['format']['duration']))-duration) > .05:
                raise ValueError('rendered dimensions/duration disagree with Short contract')
            if d['version'] == 2:
                declared_fps = d['framing']['operations'][3]
                rn, rd = map(int, rs['avg_frame_rate'].split('/'))
                if min(rn, rd) <= 0 or rn * declared_fps['den'] != rd * declared_fps['num'] or rs.get('sample_aspect_ratio') != '1:1':
                    raise ValueError('rendered fps/SAR disagree with explicit recipe')
            errors = []
            for source_t, render_t in samples:
                expected = frame(src, source_t, crop, recipe)
                actual = frame(video, render_t)
                mae = sum(abs(a-b) for a,b in zip(expected, actual)) / len(actual)
                errors.append(round(mae, 4))
                if mae > 8:
                    raise ValueError(f'rendered opening/return correspondence failed at {render_t:g}s (MAE {mae:.2f})')
            result['evidence']['rendered_frame_mae'] = errors
            result['evidence']['render_sha256'] = digest(video)
            result['pending'] = ['human moving/phone and audio review; samples do not establish seamless motion']
        result.update(status='rendered_correspondence' if video else 'source_preflight', eligible_cut=k)
    except (KeyError, TypeError, ValueError, OSError, IndexError, subprocess.SubprocessError, ZeroDivisionError) as exc:
        result['errors'].append(str(exc))
    return result
