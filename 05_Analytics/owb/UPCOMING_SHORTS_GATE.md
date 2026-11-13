# Upcoming Shorts: gate check

Written by `gate_upcoming.py` at 2026-11-13 06:40 London for Shorts scheduled in the next 14 days. Don't edit by hand.

| Airs (London) | Short | In library | Gate |
|---|---|---|---|
| 2026-11-13 11:30 | [Why Does Pluto's Giant Ice Heart Have Zero Craters?](https://youtu.be/z5V6gIXXYs8) `z5V6gIXXYs8` | yes | PASS |
| 2026-11-14 11:30 | [How Did a Helicopter Fly 72 Times on Mars?](https://youtu.be/RT-ec4_GcOk) `RT-ec4_GcOk` | yes | PASS |
| 2026-11-16 11:30 | [If You Can't See the Nearest Star, How Far Away Is It?](https://youtu.be/aEfdxex__Bo) `aEfdxex__Bo` | yes | PASS |
| 2026-11-17 11:30 | [How Far From Earth Is Voyager 1 Right Now?](https://youtu.be/kKN8Ale42sE) `kKN8Ale42sE` | yes | **FAIL** |
| 2026-11-18 11:30 | [If Voyager Needs 75,000 Years, How Far Is the Nearest Star?](https://youtu.be/dH_yCRmzkMo) `dH_yCRmzkMo` | yes | PASS |
| 2026-11-20 11:30 | [The Nearest Star Is a Cherry Past Cairo. How Do We Know?](https://youtu.be/aAUgIGEuPwQ) `aAUgIGEuPwQ` | yes | PASS |
| 2026-11-21 11:30 | [Muons Shouldn't Reach the Ground. They Do.](https://youtu.be/rvug71d7Dqk) `rvug71d7Dqk` | yes | **FAIL** |
| 2026-11-23 11:30 | [Why Do You Weigh Less at Earth's Equator?](https://youtu.be/Dm4xsF1Ateg) `Dm4xsF1Ateg` | yes | PASS |
| 2026-11-25 11:30 | [Where Will the International Space Station Crash?](https://youtu.be/xdurJQcoiGM) `xdurJQcoiGM` | yes | **FAIL** |

## Details

### kKN8Ale42sE: FAIL

```
FAIL  owb_sa_s8_voyager1_v01.mp4  dur=20.74s  audio=-18.9dB  motion=16.19  f0diff=0.33  cut1=4.6s  vo_onset=0.07s  tail_gap=3.00s  vo_src=mix  dhash=63c7cf89332769e0  visor=0.0
   full-bleed 0.00s  fills the frame  sharp above/middle/below=0.116/0.221/0.043  detail top/centre/bottom=18.46/4.49/1.65  spread top/bottom=56.63/7.06
   full-bleed 0.25s  fills the frame  sharp above/middle/below=0.129/0.219/0.078  detail top/centre/bottom=18.62/5.65/12.0  spread top/bottom=56.62/41.02
   full-bleed 0.50s  fills the frame  sharp above/middle/below=0.123/0.219/0.086  detail top/centre/bottom=18.5/5.85/12.09  spread top/bottom=56.98/41.72
   full-bleed whole Short  4/21 frames padded at one a second, 8/42 at two a second  padded stretches: 5-9s (blur-pad, no edge)  no end card named in meta
   FAIL  the picture does not fill 9:16 on 8/42 frames sampled twice a second (19.0%; 0 with a straight edge at the picture; limit 15% when no edge is found): 5-9s (blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
   warn  duration 20.7s outside 22–27s band
   warn  gap from last word to end is 3.00s > 1.5s (last word 17.74s, duration 20.74s)
   warn  [report-only] pushed still at frame 0 (mean 0–1.5 s frame diff 0.33 < 1.50) — use moving footage
   warn  [report-only] first cut at 4.60s > 3.0s (scene-change detect)
   warn  [report-only] spoken text contains meta-promise ("stay, and i'll show you")
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/orbit_shorts_gate/owb_sa_s8_voyager1_v01_open_sheet.jpg
```

### kKN8Ale42sE: report-only (would fail 60% stayed gate)

- pushed still at frame 0 (mean 0–1.5 s frame diff 0.33 < 1.50) — use moving footage
- first cut at 4.60s > 3.0s (scene-change detect)
- spoken text contains meta-promise ("stay, and i'll show you")

### rvug71d7Dqk: FAIL

```
FAIL  fri06_muons_ground_v04.mp4  dur=22.2s  audio=-17.8dB  motion=17.25  f0diff=3.94  cut1=3.0s  vo_onset=0.10s  tail_gap=1.03s  vo_src=mix  dhash=dc7360b603214413  visor=0.0
   full-bleed 0.00s  fills the frame  sharp above/middle/below=0.358/0.729/0.132  detail top/centre/bottom=12.17/11.83/2.89  spread top/bottom=43.73/34.22
   full-bleed 0.25s  fills the frame  sharp above/middle/below=0.374/0.735/0.126  detail top/centre/bottom=12.3/11.8/3.14  spread top/bottom=43.59/34.17
   full-bleed 0.50s  fills the frame  sharp above/middle/below=0.387/0.747/0.128  detail top/centre/bottom=12.26/11.71/3.2  spread top/bottom=43.46/34.06
   full-bleed whole Short  13/23 frames padded at one a second, 25/45 at two a second  padded stretches: 3-4s (blur-pad), 6-7s (blur-pad), 11-22s (blur-pad / blur-pad, no edge)  no end card named in meta
   FAIL  the picture does not fill 9:16 on 13/23 frames sampled once a second (57%, limit 10%): 3-4s (blur-pad), 6-7s (blur-pad), 11-22s (blur-pad / blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/orbit_shorts_gate/fri06_muons_ground_v04_open_sheet.jpg
```

### xdurJQcoiGM: FAIL

```
FAIL  owb_ar2_iss_2030_deorbit_v13.mp4  dur=18.4s  audio=-17.5dB  motion=31.03  f0diff=7.53  cut1=2.4s  vo_onset=0.04s  tail_gap=0.14s  vo_src=mix  dhash=351dc3cb919ee9ce  visor=0.0
   full-bleed 0.00s  fills the frame  sharp above/middle/below=None/0.895/None  detail top/centre/bottom=27.35/18.29/16.72  spread top/bottom=60.83/45.53
   full-bleed 0.25s  fills the frame  sharp above/middle/below=None/0.913/None  detail top/centre/bottom=27.03/18.52/20.14  spread top/bottom=61.09/46.34
   full-bleed 0.50s  fills the frame  sharp above/middle/below=None/0.921/None  detail top/centre/bottom=26.65/18.93/20.37  spread top/bottom=61.73/46.2
   full-bleed whole Short  4/19 frames padded at one a second, 7/37 at two a second  padded stretches: 15-18s (blur-pad, no edge)  no end card named in meta
   FAIL  the picture does not fill 9:16 on 7/37 frames sampled twice a second (18.9%; 0 with a straight edge at the picture; limit 15% when no edge is found): 15-18s (blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
   warn  duration 18.4s outside 22–27s band
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/orbit_shorts_gate/owb_ar2_iss_2030_deorbit_v13_open_sheet.jpg
```

