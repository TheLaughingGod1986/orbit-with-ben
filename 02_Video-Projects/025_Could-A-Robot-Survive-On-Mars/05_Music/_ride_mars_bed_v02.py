#!/usr/bin/env python3
"""J0068: opening ride on 025's bed per Claude #6072407565.

From mars-robot_score_bed_v01_full.mp3 (kept): lift 0.5-25 s towards 10 dB under the bed's median level, capped at
+12 dB, with 2 s ramps in and out. The level is music_gate's own measure (3 s rolling RMS, 100 ms hop, median with
the first 3 s and last 15 s skipped). Writes mars-robot_score_bed_v02_full.mp3 and a check JSON that also confirms
the bed (at the cut's 0.134 mix gain) stays at least 10 dB under the VO for 0-25 s.
"""
import json, subprocess as sp, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE / 'mars-robot_score_bed_v01_full.mp3'
OUT = HERE / 'mars-robot_score_bed_v02_full.mp3'
VO = HERE.parent / '02_Voiceover/mars_robot_vo_v01.mp3'
SR, HOP, WIN = 44100, 4410, 30
A, B, RAMP, CAP, UNDER = 0.5, 25.0, 2.0, 12.0, 10.0
MIX_GAIN_DB = 20 * np.log10(0.134)


def decode(p, ch):
    raw = sp.run(['ffmpeg', '-v', 'error', '-i', str(p), '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'],
                 capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).astype(np.float64)


def level(mono):
    n = len(mono) // HOP
    rms2 = (mono[:n * HOP].reshape(n, HOP) ** 2).mean(1) + 1e-12
    return 10 * np.log10(np.convolve(rms2, np.ones(WIN) / WIN, 'same') + 1e-12)


x = decode(SRC, 2)
lv = level(x.mean(1))
n = len(lv)
med = float(np.median(lv[30:n - 150]))
t = np.arange(n) / 10
want = np.clip((med - UNDER) - lv, 0, CAP)
want = np.convolve(want, np.ones(20) / 20, 'same')  # 2 s smoothing so the ride follows phrases, not single bars
env = np.clip(np.minimum((t - A) / RAMP, (B - t) / RAMP), 0, 1)
gain_db = want * env
g = 10 ** (np.interp(np.arange(len(x)) / SR, t, gain_db) / 20)
y = np.clip(x * g[:, None], -0.98, 0.98).astype(np.float32)
sp.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-',
        '-c:a', 'libmp3lame', '-b:a', '192k', str(OUT)], input=y.tobytes(), check=True)

ly = level(decode(OUT, 1)[:, 0])
vo = level(decode(VO, 1)[:, 0])
m = min(250, len(vo), len(ly))
speech = vo[:m] > np.max(vo[:m]) - 30
margin = vo[:m] - (ly[:m] + MIX_GAIN_DB)
res = dict(src=SRC.name, out=OUT.name, median_level_db=round(med, 1), target_db=round(med - UNDER, 1), cap_db=CAP,
           window_s=[A, B], ramp_s=RAMP, max_gain_db=round(float(gain_db.max()), 1),
           min_level_0_25_before=round(float(lv[5:250].min() - med), 1),
           min_level_0_25_after=round(float(ly[5:250].min() - med), 1),
           vo_over_bed_min_db_0_25=round(float(margin[speech].min()), 1),
           vo_over_bed_min_at_s=round(float(t[:m][speech][np.argmin(margin[speech])]), 1),
           vo_margin_ok=bool(margin[speech].min() >= 10.0))
(HERE / 'mars-robot_score_bed_v02_full_ride_check.json').write_text(json.dumps(res, indent=2) + '\n')
print(json.dumps(res, indent=2))
sys.exit(0 if res['vo_margin_ok'] else 1)
