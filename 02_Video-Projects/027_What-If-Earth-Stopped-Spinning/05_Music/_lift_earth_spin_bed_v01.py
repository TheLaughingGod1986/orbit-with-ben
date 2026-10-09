#!/usr/bin/env python3
"""J0080: 027's score bed came back full length in one take (490 s of 490 s asked), so no continuation or join.

The take eases into a hushed section at ~268-390 s (short-term ~-33 LUFS, ~17 dB under the bed's median), the brief's
"slow patient world". music_gate reads 10.3 s of it as the music stopping, so that passage alone is lifted 6 dB with
3 s ramps (265-268 up, 390-393 down), as 024's hushed bridge was. Writes earth-spin_score_bed_v01_lift.mp3 and a
check JSON (same gap rule as music_gate: >15 dB under median for >6 s).
"""
import json, re, statistics, subprocess as sp, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / 'earth-spin_score_bed_v01.mp3', HERE / 'earth-spin_score_bed_v01_lift.mp3'
LIFT_DB, LIFT_IN, LIFT_OUT, RAMP = 6.0, 268.0, 390.0, 3.0
VO_TOTAL = 460.0

lift = (f"volume='pow(10,{LIFT_DB}*max(0,min(1,min((t-{LIFT_IN}+{RAMP})/{RAMP},({LIFT_OUT}+{RAMP}-t)/{RAMP})))/20)'"
        ":eval=frame")
sp.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(SRC), '-af', f'{lift},alimiter=limit=0.95',
        '-ar', '44100', '-b:a', '192k', str(OUT)], check=True)

dur = float(sp.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(OUT)], text=True))
log = sp.run(['ffmpeg', '-nostats', '-hide_banner', '-i', str(OUT), '-af',
              'ebur128=metadata=1:peak=true,ametadata=print:key=lavfi.r128.S', '-f', 'null', '-'],
             capture_output=True, text=True).stderr
st, t = [], None
for line in log.splitlines():
    m = re.search(r'pts_time:([\d.]+)', line)
    if m: t = float(m.group(1))
    m = re.search(r'lavfi\.r128\.S=(-?[\d.]+)', line)
    if m and t is not None: st.append((t, float(m.group(1))))
integ = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', log)[-1])
peak = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', log)[-1])
film = [v for tt, v in st if 3.0 <= tt <= min(VO_TOTAL, dur)]
med = statistics.median(film)
runs, run_start, prev = [], None, None
for tt, v in st:
    if not 3.0 <= tt <= min(VO_TOTAL, dur):
        continue
    if v < med - 15:
        run_start = tt if run_start is None else run_start
    elif run_start is not None:
        runs.append((run_start, prev - run_start)); run_start = None
    prev = tt
longest = max(runs, key=lambda r: r[1], default=(0.0, 0.0))
res = dict(bed=OUT.name, source=SRC.name, seconds=round(dur, 2), vo_total=VO_TOTAL, covers_vo=dur >= VO_TOTAL,
           integrated_lufs=integ, true_peak_dbfs=peak, film_median_short_term=round(med, 1),
           hush_lift_db=LIFT_DB, hush_lift_s=[LIFT_IN - RAMP, LIFT_OUT + RAMP],
           longest_gap_s=round(longest[1], 1), longest_gap_at_s=round(longest[0], 1), gap_rule='>15 dB under median for >6 s',
           passed=longest[1] <= 6.0 and dur >= VO_TOTAL)
(HERE / 'earth-spin_score_bed_v01_lift_check.json').write_text(json.dumps(res, indent=2) + '\n')
print(json.dumps(res, indent=2))
sys.exit(0 if res['passed'] else 1)
