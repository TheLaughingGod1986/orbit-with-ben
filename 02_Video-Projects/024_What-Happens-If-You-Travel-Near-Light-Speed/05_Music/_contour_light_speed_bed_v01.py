#!/usr/bin/env python3
"""J0089 step 1: loudness contour of light-speed_score_bed_v01_full.mp3 for Claude (who can't hear the mp3 from the cloud).

Momentary (400 ms) and short-term (3 s) LUFS over the full bed, with the 5:16-5:24 join crossfade and the 3:48-4:13
bridge lift marked. The join check is 023's (J0078): the lowest short-term reading within +-15 s of the join, against
the film median (3 s to the end of the VO); limit 6 LU. Also lists every stretch where short-term sits >15 dB under the
median for >6 s (music_gate's gap rule). Writes light-speed_score_bed_v01_full_contour.png/.jpg and _contour.json.
"""
import json, re, statistics, subprocess as sp
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BED = HERE / 'light-speed_score_bed_v01_full.mp3'
J, XF, VO_TOTAL, LIFT = 316.0, 8.0, 491.1, (228.0, 253.0)
CHAPTERS = [('Your Clock Is Already Slow', 42.0), ('Why Light Sets the Limit', 110.7), ('The Trip', 224.4),
            ('The Price of Every Nine', 324.5), ('A One-Way Ticket to the Future', 399.2)]

log = sp.run(['ffmpeg', '-nostats', '-hide_banner', '-i', str(BED), '-af',
              'ebur128=metadata=1,ametadata=print:key=lavfi.r128.M,ametadata=print:key=lavfi.r128.S', '-f', 'null', '-'],
             capture_output=True, text=True).stderr
M, S, t = [], [], None
for line in log.splitlines():
    m = re.search(r'pts_time:([\d.]+)', line)
    if m: t = float(m.group(1)); continue
    m = re.search(r'lavfi\.r128\.([MS])=(-?[\d.inf]+)', line)
    if m and t is not None:
        v = max(float(m.group(2)), -70.0)
        (M if m.group(1) == 'M' else S).append((t, v))
dur = M[-1][0]
film = [v for tt, v in S if 3.0 <= tt <= VO_TOTAL]
med = statistics.median(film)
win = [(tt, v) for tt, v in S if J - 15 <= tt <= J + 15]
low_t, low_v = min(win, key=lambda x: x[1])
gaps, start, prev = [], None, None
for tt, v in S:
    if not 3.0 <= tt <= VO_TOTAL: continue
    if v < med - 15: start = tt if start is None else start
    elif start is not None: gaps.append((round(start, 1), round(prev - start, 1))); start = None
    prev = tt
holes = [g for g in gaps if g[1] > 6.0]
lift_win = [v for tt, v in S if LIFT[0] <= tt <= LIFT[1]]
res = dict(bed=BED.name, seconds=round(dur, 2), vo_total=VO_TOTAL, film_median_short_term=round(med, 1),
           join_s=J, crossfade_s=XF, window=f'{J - 15:.0f}-{J + 15:.0f} s around the join',
           window_min_short_term=round(low_v, 1), window_min_at_s=round(low_t, 1),
           join_drop_below_median_lu=round(med - low_v, 1), join_limit_lu=6.0, join_passed=(med - low_v) <= 6.0,
           bridge_lift_s=list(LIFT), bridge_min_short_term=round(min(lift_win), 1),
           bridge_drop_below_median_lu=round(med - min(lift_win), 1),
           gaps_over_15db_under=gaps, holes_over_6s=holes, no_hole=not holes)
(HERE / 'light-speed_score_bed_v01_full_contour.json').write_text(json.dumps(res, indent=2) + '\n')

fig, ax = plt.subplots(figsize=(18, 6), dpi=110)
ax.plot([a for a, _ in M], [b for _, b in M], lw=0.5, color='#7aa6d6', label='momentary (400 ms)')
ax.plot([a for a, _ in S], [b for _, b in S], lw=1.4, color='#16325c', label='short-term (3 s)')
ax.axhline(med, color='green', ls='--', lw=1, label=f'film median {med:.1f} LUFS')
ax.axhline(med - 6, color='orange', ls=':', lw=1, label='median - 6 LU (join limit)')
ax.axhline(med - 15, color='red', ls=':', lw=1, label='median - 15 LU (gap rule)')
ax.axvspan(J, J + XF, color='red', alpha=0.25, label='join crossfade 5:16-5:24')
ax.axvspan(J - 15, J + 15, color='red', alpha=0.06)
ax.axvspan(*LIFT, color='gold', alpha=0.3, label='bridge lift +5 dB 3:48-4:13')
ax.axvline(VO_TOTAL, color='grey', lw=1, ls='-.', label='VO ends 8:11')
for name, ct in CHAPTERS:
    ax.axvline(ct, color='grey', lw=0.6, alpha=0.6)
    ax.text(ct + 2, -12.5, name, fontsize=7, rotation=90, va='top', color='dimgrey')
ax.plot([low_t], [low_v], 'rv')
ax.annotate(f'join window low {low_v:.1f} @ {int(low_t // 60)}:{low_t % 60:04.1f} ({med - low_v:.1f} LU under)',
            (low_t, low_v), xytext=(low_t + 10, low_v - 6), fontsize=8, arrowprops=dict(arrowstyle='->'))
ax.set_xticks(range(0, int(dur) + 1, 30))
ax.set_xticklabels([f'{s // 60}:{s % 60:02d}' for s in range(0, int(dur) + 1, 30)])
ax.set_xlim(0, dur); ax.set_ylim(-50, -8)
ax.set_xlabel('bed time (m:ss) = film time'); ax.set_ylabel('LUFS')
ax.set_title(f'024 Light Speed bed v01_full: loudness contour ({dur:.0f} s). Join drop {med - low_v:.1f} LU (limit 6); '
             f'holes >6 s at >15 dB under: {len(holes)}')
ax.legend(loc='lower left', fontsize=8, ncol=4); ax.grid(alpha=0.25)
fig.tight_layout()
for ext in ('png', 'jpg'):  # PNGs are git-ignored; the jpg is the one Claude reads
    fig.savefig(HERE / f'light-speed_score_bed_v01_full_contour.{ext}')
print(json.dumps(res, indent=2))
