# OWB `032` Short #1 (Active #1 · Fire on Titan) Build & Gate Report — `J3758` (`v01`)

- **Job:** `J3758` (`Backlog OWB: next Short cut from a locked long (existing VO + picture only)`)
- **Selection Basis:** `032_What-Would-Happen-If-You-Landed-On-Titan` (*What Would Happen If You Landed on Titan? (Seas of Liquid Gas)*, YouTube `T3cBBss1F60`, live since `Wed 25 Nov 2026 18:00 London`) had the fewest Shorts built among locked/live standalone OWB longs (**1** built: `fri27_opening_testA` / `BLCuJ4EKic4`, vs 2 on `031`/`033`/`034` and 3–9 on `021`–`029`; `030` has no locked long and `J01` is a compilation).
- **Parent Long (`032`):** *What Would Happen If You Landed on Titan? (Seas of Liquid Gas)* (`T3cBBss1F60`, approved master `v02` `sha256: 519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073`)
- **Short Slug / Stem:** `strike_match_fire` / `032_short_strike_match_fire_v01`
- **Short Title:** *How Would You Light a Fire on Titan?* (Alt: *What Happens If You Strike a Match on Titan?*)
- **Target Free Slot (gate check date):** `Fri 18 Dec 2026 11:30Z` (`2026-12-18`, non-colliding `Mon/Wed/Fri/Sat` slot; **never uploaded by this job**)
- **Spend:** `£0.00` (existing locked VO `titan_landing_vo_v02b.wav`, `J2089`/`J2378` picture harvest, `titan_score_bed_v01.mp3`, and synthesized house SFX kit `kit_v01` only)

---

## 1. Verified Source & Output SHA-256 Manifest (NAS `studio-live`)

All `_v01` exports and sidecars were verified by SHA-256 on the NAS under `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/strike_match_fire/06_Final-Exports/` (and mirrored to `10_Shorts/`):

| Artifact | Path (under `032.../10_Shorts/strike_match_fire/06_Final-Exports/`) | SHA-256 |
|---|---|---|
| **Short Master (`v01`)** | `032_short_strike_match_fire_v01.mp4` (`1080x1920`, `30/1` fps CFR, `24.900 s`, `747` frames) | `494f092b857df509e419b2b04967c337acde9af88d362725cd2e94e34acf2386` |
| **Frame-0 Still** | `032_short_strike_match_fire_v01_frame0.jpg` | `2a3ffffa8e92a118d3818062527303a9cc972ed86e185697ee8d094df0ec24e6` |
| **Custom Short Cover** | `032_short_strike_match_fire_v01_cover.jpg` (`FIRE ON / TITAN?`, `126 px`, zero Orbit) | `11410819204f4de8fa081b7c4e5a2015d07ed47cc88eb63eb09c512ba1036de4` |
| **Gate Opening Sheet** | `032_short_strike_match_fire_v01_open_sheet.jpg` | `87ea144f5436cb0dffe7e86a0d1c264eb489ce5c80dc06fd4ee1a4739750ca0c` |
| **10-Shot Contact Sheet** | `032_short_strike_match_fire_v01_review_10shots.jpg` | `eae94880ff09424711cd319420f9d4f213b3cc8facc1c6d82b8160e91a468a78` |
| **Input: Approved Long Master `v02`** | `../../09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` | `519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073` |
| **Input: Locked Master VO (`v02b`)** | `../../02_Voiceover/titan_landing_vo_v02b.wav` | `55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5` |
| **Input: Score Bed (`v01`)** | `../../05_Music/titan_score_bed_v01.mp3` | `02c7d95865f8b39de4f9d3dfda8aa85084ecea04fc56dbd6776268279dab8f9e` |

- **Excluded `RLSJm59OSzI` Assets Verified Absent (`0` overlap):** `PIA14925`, `PIA06230`, `PIA09739`, `PIA21625`.
- **Distinct Frame-0 Opening:** Uses `SVS20311_Dragonfly_Drill_1080.mp4` (`offset=4.20 s`), distinct from `BLCuJ4EKic4` (`SVS20311_DF_End_Pan_1080.mp4`).

---

## 2. All 7 Automated Ship & QA Gates (`7/7 PASS`)

| Gate | Command / Check | Verdict | Key Readout |
|---|---|---|---|
| **1. `gate_shorts_open.py`** | `gate_shorts_open.py check ... --air-date 2026-12-18` | **PASS (`rc=0`)** | `dur=24.9s` (inside J3758 `22–27 s` band; gate prints standard `16.0–19.0 s` advisory warn), `motion=24.39`, `f0diff=6.93`, `cut1=1.77s`, `vo_onset=0.07s`, `tail_gap=1.07s`, `visor=0.0`, **`0/25` (`0/50`) padded frames across whole Short (`padded stretches: none`)** |
| **2. `thumb_preview.py` (Frame 0)** | `thumb_preview.py short ..._frame0.jpg --score` | **PASS (`rc=0`)** | `saturation=149.3`, `near_black=1%` |
| **3. `thumb_preview.py` (Cover)** | `thumb_preview.py short ..._cover.jpg --score` | **PASS (`rc=0`)** | `saturation=191.6`, `near_black=1%` (`FIRE ON / TITAN?`, `126 px`, zero Orbit) |
| **4. `sfx_kit.py level`** | `sfx_kit.py level --vo ... --sfx ... --bed ...` | **PASS (`rc=0`)** | `VO -16.3 LUFS`, `SFX -41.5 LUFS`, `Bed -34.7 LUFS`, `AAC -14.1 LUFS / -2.2 dBTP`, `7` detected hits |
| **5. `music_gate.py`** | `music_gate.py 032_... --bed titan_score_bed_v01.mp3 --video ...` | **PASS (`rc=0`)** | `titan_score_bed_v01.mp3`, `585.4 s`, `70.6 BPM` (`Pace: 68-78 BPM`), runs full cut |
| **6. `polish_gate.py`** | `polish_gate.py ... --cuts ..._cuts.json` | **PASS (`rc=0`)** | **`0 of 10` rows failed** (`0` seams, `0` near-black, `0` push jitter; 1 low-detail WARN on `S07_titan_sky` `PIA17177.jpg` visually inspected — clean glowing Titan crescent on crisp starfield) |
| **7. `picture_qa.py`** | `picture_qa.py ... --cuts ..._cuts.json --pool ..._pool.json` | **PASS (`rc=0`)** | **`0 of 10` cuts fail** (`max upscale = 1.78x <= 2.00x`, `0` reuse fails, `0` split-panel fails) |

### Exact `gate_shorts_open.py` Output (NAS Copy)

```text
PASS  032_short_strike_match_fire_v01.mp4  dur=24.9s  audio=-16.7dB  motion=24.39  f0diff=6.93  cut1=1.77s  vo_onset=0.07s  tail_gap=1.07s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/strike_match_fire/06_Final-Exports/032_short_strike_match_fire_v01_vo.wav  dhash=76eae264e88a9e36  visor=0.0
   full-bleed 0.00s  fills the frame  sharp above/middle/below=0.188/0.352/0.823  detail top/centre/bottom=12.11/7.02/7.36  spread top/bottom=64.8/12.25
   full-bleed 0.25s  fills the frame  sharp above/middle/below=0.191/0.363/0.811  detail top/centre/bottom=13.52/7.02/7.29  spread top/bottom=68.44/12.3
   full-bleed 0.50s  fills the frame  sharp above/middle/below=0.202/0.368/0.805  detail top/centre/bottom=13.57/6.63/7.17  spread top/bottom=74.77/12.35
   full-bleed whole Short  0/25 frames padded at one a second, 0/50 at two a second  padded stretches: none  end card 23.9-24.9s judged apart
   warn  duration 24.90s outside 16.0–19.0s band
   sheet /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/strike_match_fire/06_Final-Exports/032_short_strike_match_fire_v01_open_sheet.jpg
```

---

## 3. Required Brief, `OWB-2026-11-E1`, 60% Stayed & 70% Viewed Checklist

- **#1 · Keeper Title & Question:** *How Would You Light a Fire on Titan?* (37 chars, positive question naming Titan). Verbatim VO (`s60, s61, s62, s64, s66`, `73` words): *"Titan has lakes of fuel and methane in its sky, but almost no oxygen. Its air is mostly nitrogen. If you struck a match or fired a rocket thruster in Titan's atmosphere, the fuel around you would not catch fire. In fact, Titan flips fire backwards. On Titan, if you wanted a flame, you would have to carry a tank of oxygen on your back and spray it out into the methane sky."*
- **#2 · First-Second Rule (`0.0–1.5 s`, `J2429`):**
  - Frame-0 source: real moving NASA SVS 20311 `SVS20311_Dragonfly_Drill_1080.mp4` (`offset=4.20 s`, full-bleed `1080x1920` `cover`, `f0diff=6.93 >= 1.50`, `visor=0.0`, `near_black=1% <= 30%`, `0` blur-pad bars).
  - Hook caption on frame 0 (`0.00–1.76 s`): `LAKES OF` (white) / `METHANE` (`#FFE000` yellow), `130 px` Arial Black, clears cleanly before Cut 1 at `1.767 s`.
  - First spoken word (`"Titan"`) onset: `0.094 s` (`gate_shorts_open` `vo_onset=0.07 s <= 0.15 s`); surprise `"lakes of fuel"` completes by `1.61 s`.
  - Meta-promise / spoken CTA present: **`no`** (`0` meta-promises, `0` spoken CTAs).
- **#3 & E1 · Cut Timings & Pacing (`10` shots, `9` cuts, `0` words split across cuts):**
  - **Cut 1:** `1.767 s <= 2.80 s`
  - **Cut 2:** `4.300 s <= 4.80 s`
  - **All cut timestamps (s):** `1.767`, `4.300`, `7.167`, `11.133`, `13.633`, `16.633`, `18.667`, `21.400`, `23.867`
  - **Longest plate hold:** `3.966 s <= 4.00 s`
- **#6 · Payoff Timing (`>= 70%` runtime):**
  - Runtime: `24.900 s` (inside `22–27 s`); `0.70 x 24.900 s = 17.430 s`.
  - Actual answer (`"you would have to carry a tank of oxygen on your back and spray it out into the methane sky"`) starts at **`18.854 s` (`75.7% >= 70.0%` PASS)**, completely clear of the `9.00–14.00 s` parent-long title banner (`What Would Happen If You Landed on Titan? (Seas of Liquid Gas)`).
- **#7 · Sentence-1 Seam (`4–5 s`):**
  - `s60` → `s61` VO breath tightened to **`0.220 s < 0.25 s`** (`5.174–5.394 s`), bridging cleanly over the animated air-mix comparison graphic (`4.300–7.167 s`) into *"Its air is mostly nitrogen."*
- **Single Teach-on-Screen Number Object (`4.300–7.167 s`, clear of `0–2 s` and `9–14 s`):**
  - Native `9:16` animated atmosphere comparison (`EARTH AIR 21% OXYGEN` with real Apollo 17 `AS17-148-22727` globe vs `TITAN AIR 95% NITROGEN / ~0% OXYGEN` with real Cassini `PIA20016` globe; sourced from `032/01_Script/SOURCES.md` Rows 9 & 14) + `95% N2 · ~0% O2` yellow pill (`4.45–7.05 s`, inside `16:9` safe band `bbox=[262, 1190, 817, 1248]`).
- **Loop Tail (`< 1.20 s` E1 limit):**
  - Last spoken word (`"sky."`) ends at `23.834 s`; loop seam at `24.900 s` → **tail gap = `1.066 s < 1.20 s`**, with continuous moving pre-roll (`3.167 -> 4.200 s` of `SVS20311_Dragonfly_Drill_1080.mp4`) arriving on exact frame 0, score bed running through the seam, and clean `16:9`-band parent long title end card (zero video ID printed).
  - Loop sentence (`s66` → `s60`): *"...spray it out into the methane sky — Titan has lakes of fuel and methane in its sky, but almost no oxygen."*
