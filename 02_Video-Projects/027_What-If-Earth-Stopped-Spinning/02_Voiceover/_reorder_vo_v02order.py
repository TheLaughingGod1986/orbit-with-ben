#!/usr/bin/env python3
"""027 VO in SHOT_LIST_v02 order (J0077): the recorded take earth_spin_vo_v01, re-cut, no new voice.
v01 spans (Scribe word times): open 0.16-22.56, agenda 23.80-39.50 cut, sudden stop 111.92-181.46,
speed 40.38-111.08, subscribe + slow stop to the end 182.42-460.34.
Each span is cut 0.35 s outside its first and last word with 10 ms fades, so every join is a 0.7 s pause
(the chapter-card gap). Writes earth_spin_vo_v02order.wav and words_v02order.json ({"words":[{text,start,end}]},
the shape the 026 assembler reads), plus a span map from new to v01 time."""
from pathlib import Path
import json, subprocess as sp

HERE = Path(__file__).resolve().parent
SRC = HERE / 'earth_spin_vo_v01.wav'
OUT = HERE / 'earth_spin_vo_v02order.wav'
PAD = 0.35
SPANS = [  # (label, first word start, last word end) in v01 time
    ('open rows 1-3', 0.16, 22.56),
    ('sudden stop rows 10-15', 111.92, 181.46),
    ('speed rows 5-9', 40.38, 111.08),
    ('subscribe + rows 16-37', 182.42, 460.34),
]
raw = json.loads((HERE / 'stt/earth_spin_vo_v01/stt_raw.json').read_text())
words = [w for w in raw['words'] if w.get('type') == 'word']
src_len = float(raw['audio_duration_secs'])

parts, out_words, spans_map, t = [], [], [], 0.0
for k, (label, a, b) in enumerate(SPANS):
    i0, i1 = max(0.0, a - PAD), min(src_len, b + PAD)
    L = i1 - i0
    parts.append(f"[0:a]atrim={i0:.3f}:{i1:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={L - 0.01:.3f}:d=0.01[p{k}]")
    inside = [w for w in words if w['start'] >= a - 0.01 and w['end'] <= b + 0.01]
    out_words += [dict(text=w['text'], start=round(w['start'] - i0 + t, 3), end=round(w['end'] - i0 + t, 3), v01_start=w['start']) for w in inside]
    spans_map.append(dict(label=label, v01_in=round(i0, 3), v01_out=round(i1, 3), new_in=round(t, 3), new_out=round(t + L, 3), words=len(inside)))
    t += L

fc = ';'.join(parts) + ';' + ''.join(f'[p{k}]' for k in range(len(SPANS))) + f'concat=n={len(SPANS)}:v=0:a=1[a]'
sp.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(SRC), '-filter_complex', fc, '-map', '[a]',
        '-c:a', 'pcm_s24le', str(OUT)], check=True)
dur = float(sp.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(OUT)], text=True))
kept = sum(s['words'] for s in spans_map)
cut = [w for w in words if 23.80 - 0.01 <= w['start'] and w['end'] <= 39.50 + 0.01]
assert kept + len(cut) == len(words), (kept, len(cut), len(words))
assert abs(dur - t) < 0.05, (dur, t)
(HERE / 'words_v02order.json').write_text(json.dumps(dict(source=SRC.name, out=OUT.name, duration=round(dur, 3),
    last_word_end=out_words[-1]['end'], spans=spans_map, words=out_words), indent=1))
print(json.dumps(dict(duration=round(dur, 3), last_word_end=out_words[-1]['end'], words=len(out_words),
    agenda_words_cut=len(cut), first_answer_at=spans_map[1]['new_in'] + PAD, spans=spans_map), indent=1))
