#!/usr/bin/env python3
"""J0068: re-join 025's bed per Claude #6071929578.

Take 2 enters under take 1 before its quiet tail (8 s equal-power crossfade, 3 s fade-up from -6 dB),
take 1's own dip at 139-149 s raw is lifted 4 dB, and the joined bed is slowed 6% (pitch kept) so it
runs the full 490.2 s cut. Writes mars-robot_score_bed_v01_full.mp3 and a loudness check JSON.
"""
import json, re, statistics, subprocess as sp, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
T1, T2 = HERE / 'mars-robot_score_bed_v01.mp3', HERE / 'mars-robot_score_bed_v01b.mp3'
OUT = HERE / 'mars-robot_score_bed_v01_full.mp3'
J_RAW, XF, LEAD, T2_GAIN, TEMPO = 150.0, 8.0, 7.0, 7.3, 0.941
RIDE = (139.0, 149.0, 4.0, 2.0)  # start, end, dB, ramp
FILM_TOTAL = 490.2

a, b, db, r = RIDE
ride = (f"volume='if(between(t,{a-r},{a}),pow(10,{db}*(t-{a-r})/{r}/20),"
        f"if(between(t,{a},{b}),pow(10,{db}/20),"
        f"if(between(t,{b},{b+r}),pow(10,{db}*({b+r}-t)/{r}/20),1)))':eval=frame")
fadeup = "volume='if(lt(t,3),pow(10,(-6+2*t)/20),1)':eval=frame"
fc = (f"[0:a]atrim=0:{J_RAW+XF},asetpts=PTS-STARTPTS,{ride}[t1];"
      f"[1:a]atrim=start={LEAD},asetpts=PTS-STARTPTS,volume={T2_GAIN}dB,{fadeup}[t2];"
      f"[t1][t2]acrossfade=d={XF}:c1=qsin:c2=qsin,atempo={TEMPO},alimiter=limit=0.95[m]")
sp.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(T1), '-i', str(T2),
        '-filter_complex', fc, '-map', '[m]', '-ar', '44100', '-b:a', '192k', str(OUT)], check=True)

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
film = [v for tt, v in st if 3.0 <= tt <= min(FILM_TOTAL, dur)]
med = statistics.median(film)
win = [(tt, v) for tt, v in st if 140.0 <= tt <= 200.0]
low_t, low_v = min(win, key=lambda x: x[1])
res = dict(bed=OUT.name, seconds=round(dur, 2), film_total=FILM_TOTAL, covers_cut=dur >= FILM_TOTAL,
           integrated_lufs=integ, true_peak_dbfs=peak, film_median_short_term=round(med, 1),
           window='2:20-3:20 (140-200 s film time)', window_min_short_term=round(low_v, 1),
           window_min_at_s=round(low_t, 1), max_drop_below_median_lu=round(med - low_v, 1),
           limit_lu=6.0, passed=(med - low_v) <= 6.0 and dur >= FILM_TOTAL,
           join_film_s=round(J_RAW / TEMPO, 1), crossfade_film_s=round(XF / TEMPO, 1))
(HERE / 'mars-robot_score_bed_v01_full_join_check.json').write_text(json.dumps(res, indent=2) + '\n')
print(json.dumps(res, indent=2))
sys.exit(0 if res['passed'] else 1)
