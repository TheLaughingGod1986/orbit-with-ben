#!/usr/bin/env python3
"""J0078: join 023's two score-bed takes into one full-length bed.

Take 1 (270 s) runs to the 3:44 chapter break ("Where Did the Water Go?"); take 2 (the continuation
take, 330 s, about 10 dB quieter with a sparse opening minute) enters under it with an 8 s equal-power
crossfade centred on 224 s. Take 2 is lifted 9.9 dB to take 1's level with its sparse opening minute (raw 35-95 s) ridden up 6 dB (no compression: it pushed the
bed's band profile to 0.82 against 025's bed in music_gate's reused check). The join check looks at
the 30 s around the crossfade; take 2's own breaths are left to music_gate's gap check. Writes venus_score_bed_v01_full.mp3 and a join check JSON.
"""
import json, re, statistics, subprocess as sp, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
T1, T2 = HERE / 'venus_score_bed_v01.mp3', HERE / 'venus_score_bed_v01b.mp3'
OUT = HERE / 'venus_score_bed_v01_full.mp3'
J, XF, LEAD, T2_GAIN = 224.0, 8.0, 20.0, 9.9
RIDE = (35.0, 95.0, 6.0, 2.0)  # take 2 raw start, end, dB, ramp: its sparse opening minute
FILM_TOTAL = 513.0

a, b, db, r = (RIDE[0] - LEAD, RIDE[1] - LEAD, RIDE[2], RIDE[3])
ride = (f"volume='if(between(t,{a-r},{a}),pow(10,{db}*(t-{a-r})/{r}/20),"
        f"if(between(t,{a},{b}),pow(10,{db}/20),"
        f"if(between(t,{b},{b+r}),pow(10,{db}*({b+r}-t)/{r}/20),1)))':eval=frame")
fadeup = "volume='if(lt(t,3),pow(10,(-6+2*t)/20),1)':eval=frame"
fc = (f"[0:a]atrim=0:{J + XF / 2},asetpts=PTS-STARTPTS[t1];"
      f"[1:a]atrim=start={LEAD},asetpts=PTS-STARTPTS,volume={T2_GAIN}dB,{ride},{fadeup}[t2];"
      f"[t1][t2]acrossfade=d={XF}:c1=qsin:c2=qsin,alimiter=limit=0.95[m]")
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
win = [(tt, v) for tt, v in st if J - 15 <= tt <= J + 15]
low_t, low_v = min(win, key=lambda x: x[1])
res = dict(bed=OUT.name, seconds=round(dur, 2), film_total=FILM_TOTAL, covers_cut=dur >= FILM_TOTAL,
           integrated_lufs=integ, true_peak_dbfs=peak, film_median_short_term=round(med, 1),
           window=f'{J - 15:.0f}-{J + 15:.0f} s around the join', window_min_short_term=round(low_v, 1),
           window_min_at_s=round(low_t, 1), max_drop_below_median_lu=round(med - low_v, 1),
           limit_lu=6.0, passed=(med - low_v) <= 6.0 and dur >= FILM_TOTAL,
           join_s=J, crossfade_s=XF, take2_from_s=LEAD, take2_gain_db=T2_GAIN, take2_ride=RIDE)
(HERE / 'venus_score_bed_v01_full_join_check.json').write_text(json.dumps(res, indent=2) + '\n')
print(json.dumps(res, indent=2))
sys.exit(0 if res['passed'] else 1)
