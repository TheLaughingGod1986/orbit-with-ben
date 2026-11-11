#!/usr/bin/env python3
"""Resume Sun/Venus clean narration, preserving the locked Venus v05e mute.
Outputs are narration intermediates only. Never overwrites existing media.
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--film', choices=['022', '023'], required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    alignment_path = HERE / 'alignment_v02' / f'{a.film}_alignment.json'
    alignment = json.loads(alignment_path.read_text())
    matches = [m for m in alignment['matches'] if m['correlation'] >= .8]
    assert len(matches) >= 20 and all(m['offset_s'] == 0 for m in matches)
    assert len({m['source'] for m in matches}) == 1
    source = matches[0]['source']
    if a.film == '023':
        wordfile = ROOT / '02_Video-Projects/023_What-Happened-To-Venus/07_Edit-Project/full_rough_v05e_pack/venus_words_list.json'
        plan = [[.08, 35.8], [43.2, 212.2], [218.2, 504.8]]
        ranges = [[0, 35.8], [43.2, 212.2], [218.2, 504.8]]
        mutes = [[435.4, 436.7]]
        mute_authority = '023 _assemble_venus_full_v05e.py: Ben v05d notes / Chief 6107826583; false People have landed there sentence silenced in locked v05e'
    else:
        wordfile = ROOT / '02_Video-Projects/022_Is-the-Sun-Getting-Brighter/02_Voiceover/words.json'
        plan = [[0, 21.2], [30.82, 236.5], [242.6, 495.5]]
        ranges = [[0, 21.2], [30.5, 236.5], [242.38, 495.5]]
        mutes = []
        mute_authority = None
    raw = json.loads(wordfile.read_text())
    raw = raw if isinstance(raw, list) else raw['words']
    words = [dict(w=w.get('text', w.get('word')), s=w['start'], e=w['end']) for w in raw]
    for t in [t for r in ranges for t in r]:
        assert not any(w['s'] < t < w['e'] for w in words), f'Word intersected at {t}'
    kept = [w for w in words if any(lo <= w['s'] and w['e'] <= hi for lo, hi in ranges) and not any(lo <= w['s'] and w['e'] <= hi for lo, hi in mutes)]
    text = ' '.join(w['w'] for w in kept)
    assert not re.search(r'\b(subscrib\w*|next week|in this film|stay with me)\b', text, re.I)
    for lo, hi in ranges:
        retained = [w for w in kept if lo <= w['s'] and w['e'] <= hi]
        assert re.search(r'[.!?]["\u201d]*$', retained[-1]['w'])
    silence_run = run(['ffmpeg', '-nostdin', '-v', 'info', '-i', source, '-af', 'silencedetect=n=-38dB:d=0.12', '-f', 'null', '-'])
    events = re.findall(r'silence_(start|end): ([\d.]+)', silence_run.stderr)
    silence, start = [], None
    for kind, value in events:
        if kind == 'start':
            start = float(value)
        elif start is not None:
            silence.append([start, float(value)])
            start = None
    boundaries = []
    for t in [t for r in ranges for t in r if t != 0]:
        intervals = [s for s in silence if s[0] <= t <= s[1]]
        assert intervals, f'Boundary {t} is not in measured silence'
        boundaries.append(dict(time_s=t, silence_intervals=intervals,
                               previous=next((w for w in reversed(words) if w['e'] <= t), None),
                               next=next((w for w in words if w['s'] >= t), None)))
    prefix = ''.join(f"volume=enable='between(t,{lo},{hi})':volume=0," for lo, hi in mutes)
    n = len(ranges)
    parts = [f'[0:a]{prefix}apad=whole_dur={alignment["master_duration_s"]},asplit={n}' + ''.join(f'[s{i}]' for i in range(n))]
    for i, (lo, hi) in enumerate(ranges):
        parts.append(f'[s{i}]atrim={lo}:{hi},asetpts=PTS-STARTPTS[p{i}]')
    parts.append(''.join(f'[p{i}]' for i in range(n)) + f'concat=n={n}:v=0:a=1,highpass=f=85,treble=g=-2.5:f=5500,acompressor=threshold=-22dB:ratio=3:attack=15:release=250:makeup=2')
    chain = ';'.join(parts)
    target = 'loudnorm=I=-20.2:TP=-6.2:LRA=5'
    first = run(['ffmpeg', '-nostdin', '-v', 'info', '-i', source, '-filter_complex', chain + ',' + target + ':print_format=json[out]', '-map', '[out]', '-f', 'null', '-'])
    m = json.loads(re.findall(r'\{[^{}]+\}', first.stderr, re.S)[-1])
    norm = target + f':measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true'
    output = a.out / f'chapter_{a.film}_narration_v01.wav'
    assert not output.exists(), 'Preserve existing output; choose a new version directory'
    run(['ffmpeg', '-nostdin', '-v', 'error', '-n', '-i', source, '-filter_complex', chain + ',' + norm + '[out]', '-map', '[out]', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s24le', str(output)])
    duration = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(output)]).stdout)
    assert abs(duration - sum(hi-lo for lo, hi in ranges)) < .001
    check = run(['ffmpeg', '-nostdin', '-v', 'info', '-i', str(output), '-af', target + ':print_format=json', '-f', 'null', '-'])
    levels = json.loads(re.findall(r'\{[^{}]+\}', check.stderr, re.S)[-1])
    assert -20.5 <= float(levels['input_i']) <= -19.5 and float(levels['input_tp']) <= -6
    report = dict(status='NARRATION_CHECKPOINT_ONLY', film=a.film, source=source, source_sha256=digest(source), output=str(output), output_sha256=digest(output), duration_s=duration, levels=levels, plan_ranges=plan, used_ranges=ranges, boundaries=boundaries, mutes=mutes, mute_authority=mute_authority, word_file=str(wordfile.relative_to(ROOT)), word_file_sha256=digest(wordfile), alignment_file=str(alignment_path.relative_to(ROOT)), alignment_sha256=digest(alignment_path), kept_transcript=text, removed_transcript=' '.join(w['w'] for w in words if w not in kept), remaining='Picture, bed, master/reel and final gates pending; no listening claim')
    report_path = a.out / f'chapter_{a.film}_narration_v01.json'
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:report[k] for k in ['film','output','duration_s','levels']}, indent=2))

if __name__ == '__main__':
    main()
