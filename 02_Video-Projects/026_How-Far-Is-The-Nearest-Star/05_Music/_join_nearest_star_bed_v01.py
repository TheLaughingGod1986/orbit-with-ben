#!/usr/bin/env python3
"""J0075: join 026's two score-bed takes (025's method, Claude's brief).

Take 1 (170 s returned of 520 s asked) fades out from ~112 s raw, so take 2 (the continuation, 380 s) enters under
it with an 8 s equal-power crossfade at 104-112 s raw, lifted 11 dB to take 1's level with a 3 s fade-up from -6 dB.
The joined bed is slowed 7% (pitch kept) so the crossfade lands just before chapter 2 "Measuring the Gap" (VO 122 s)
and the bed runs past the 491 s VO with room for breaths and the end hold. Writes nearest-star_score_bed_v01_full.mp3
and a join check JSON.
"""
import json, re, statistics, subprocess as sp, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
T1, T2 = HERE / 'nearest-star_score_bed_v01.mp3', HERE / 'nearest-star_score_bed_v01b.mp3'
OUT = HERE / 'nearest-star_score_bed_v01_full.mp3'
J_RAW, XF, LEAD, T2_GAIN, TEMPO = 104.0, 8.0, 0.0, 11.0, 0.93
VO_TOTAL, CHAPTER2_VO_S = 491.0, 122.1

fadeup = "volume='if(lt(t,3),pow(10,(-6+2*t)/20),1)':eval=frame"
fc = (f"[0:a]atrim=0:{J_RAW+XF},asetpts=PTS-STARTPTS[t1];"
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
join_film = J_RAW / TEMPO
film = [v for tt, v in st if 3.0 <= tt <= min(VO_TOTAL, dur)]
med = statistics.median(film)
# Take 2 breathes (~3 s dips every ~13 s), so judge sustained gaps as music_gate does: >15 dB under for >6 s.
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
res = dict(bed=OUT.name, seconds=round(dur, 2), vo_total=VO_TOTAL, covers_vo=dur >= VO_TOTAL,
           integrated_lufs=integ, true_peak_dbfs=peak, film_median_short_term=round(med, 1),
           join_film_s=round(join_film, 1), crossfade_film_s=round(XF / TEMPO, 1), chapter2_vo_s=CHAPTER2_VO_S,
           longest_gap_s=round(longest[1], 1), longest_gap_at_s=round(longest[0], 1), gap_rule='>15 dB under median for >6 s',
           passed=longest[1] <= 6.0 and dur >= VO_TOTAL)
(HERE / 'nearest-star_score_bed_v01_full_join_check.json').write_text(json.dumps(res, indent=2) + '\n')
print(json.dumps(res, indent=2))
sys.exit(0 if res['passed'] else 1)
