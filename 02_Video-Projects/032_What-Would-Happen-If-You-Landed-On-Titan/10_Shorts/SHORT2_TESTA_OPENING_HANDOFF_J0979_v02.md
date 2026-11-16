# OWB `032` Short #2 (`Test A` Opening) Build & Gate Report — `J0979` (`v02`)

- **Job:** `J0979` (`Backlog OWB: next Short cut from a locked long (existing VO + picture only)`)
- **Reopened Under:** `J2850` (`jobs/reviews/J2850/REVIEW.md`, `e7da793304`) & `J2173` (`jobs/reviews/J2173/REVIEW.md`)
- **Parent Long (`032`):** *What Would Happen If You Landed on Titan? (Seas of Liquid Gas)* (`T3cBBss1F60`, Private scheduled `Wed 25 Nov 2026 18:00Z`, approved master `v02` `sha256: 519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073`)
- **Short Slug / Stem:** `fri27_opening_testA` / `032_short_fri27_opening_testA_v02`
- **Short Title:** *Could You Survive Stepping Onto Saturn's Moon Titan?* (Alt: *What Would Happen If You Landed on Titan?*)
- **Target Reserve Slot:** `Fri 27 Nov 2026 11:30Z` (`2026-11-27`, 2 days after `032` long `T3cBBss1F60` goes public; **never uploaded by this job**; `AR1` `93JL_IK57EM` left untouched)
- **Spend:** `£0.00` (existing locked VO `titan_landing_vo_v02b.wav`, `J2089`/`J2378` picture harvest, `titan_score_bed_v01.mp3`, and synthesized house SFX kit `kit_v01` only)

---

## 1. Verified Source & Output SHA-256 Manifest (NAS `studio-live`)

All existing `_v01` files on the NAS were left untouched. All `_v02` exports and sidecars were verified by SHA-256 on the NAS under `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/fri27_opening_testA/06_Final-Exports/` (and mirrored to `10_Shorts/`):

| Artifact | Path (under `032.../10_Shorts/fri27_opening_testA/06_Final-Exports/`) | SHA-256 |
|---|---|---|
| **Short Master (`v02`)** | `032_short_fri27_opening_testA_v02.mp4` (`1080x1920`, `30/1` fps CFR, `30.000 s`, `900` frames) | `ea9f43867d7acc729400376b55a913f695f3aa66ca705adb1b4ec320f4b78a17` |
| **Frame-0 Still** | `032_short_fri27_opening_testA_v02_frame0.jpg` | `999b9f1c1c65752692b5345c091797def8821c70ea92f5e91c16e093adabadb6` |
| **Custom Short Cover** | `032_short_fri27_opening_testA_v02_cover.jpg` (`SURVIVE ON / TITAN?`) | `9cd9e5e7fe8e310eeaebb63814679cc92d0b47f32d763f59cf3ea51d9fda05ca` |
| **Gate Opening Sheet** | `032_short_fri27_opening_testA_v02_open_sheet.jpg` | `302564b55a2a034f5818a6d79ef1173a634d2f6aa6928c95aed9c02412637a1c` |
| **12-Shot Contact Sheet** | `032_short_fri27_opening_testA_v02_review_12shots.jpg` | `d5816490fcac003c3a4fcd3710d8a8d98941fbcbfcaeb8a5ec440cae62c48afe` |
| **Input: Approved Long Master `v02`** | `../../09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` | `519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073` |
| **Input: Locked Master VO (`v02b`)** | `../../02_Voiceover/titan_landing_vo_v02b.wav` | `55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5` |
| **Input: Score Bed (`v01`)** | `../../05_Music/titan_score_bed_v01.mp3` | `02c7d95865f8b39de4f9d3dfda8aa85084ecea04fc56dbd6776268279dab8f9e` |

- **Excluded `RLSJm59OSzI` Assets Verified Absent (`0` overlap):** `PIA14925`, `PIA06230`, `PIA09739`, `PIA21625`.

---

## 2. All 7 Automated Ship & QA Gates (`7/7 PASS`)

| Gate | Command / Check | Verdict | Key Readout |
|---|---|---|---|
| **1. `gate_shorts_open.py`** | `gate_shorts_open.py check ... --air-date 2026-11-27` | **PASS (`rc=0`)** | `dur=30.0s` (Test A `30–38s` band), `motion=14.51`, `f0diff=4.28`, `cut1=2.47s`, `vo_onset=0.11s`, `tail_gap=1.19s`, `visor=0.0`, **`0/30` (`0/60`) padded frames across whole Short (`padded stretches: none`)** |
| **2. `thumb_preview.py` (Frame 0)** | `thumb_preview.py short ..._frame0.jpg --score` | **PASS (`rc=0`)** | `saturation=133.8`, `near_black=1%` |
| **3. `thumb_preview.py` (Cover)** | `thumb_preview.py short ..._cover.jpg --score` | **PASS (`rc=0`)** | `saturation=160.3`, `near_black=2%` (`SURVIVE ON / TITAN?`, `122 px`, zero Orbit) |
| **4. `sfx_kit.py level`** | `sfx_kit.py level --vo ... --sfx ... --bed ...` | **PASS (`rc=0`)** | `VO -16.8 LUFS`, `SFX -38.7 LUFS`, `Bed -34.8 LUFS`, `AAC -14.1 LUFS / -2.0 dBTP`, `6` house SFX hits |
| **5. `music_gate.py`** | `music_gate.py 032_... --bed titan_score_bed_v01.mp3 --video ...` | **PASS (`rc=0`)** | `titan_score_bed_v01.mp3`, `585.4 s`, `70.6 BPM` (`Pace: 68-78 BPM`), runs full cut |
| **6. `polish_gate.py`** | `polish_gate.py ... --cuts ..._cuts.json` | **PASS (`rc=0`)** | **`0 of 12` rows failed** (`0` seams, `0` near-black, `0` push jitter) |
| **7. `picture_qa.py`** | `picture_qa.py ... --cuts ..._cuts.json --pool ..._pool.json` | **PASS (`rc=0`)** | **`0 of 12` cuts fail** (`max upscale = 1.99x <= 2.00x`, `0` reuse fails, `0` split-panel fails) |

### Exact `gate_shorts_open.py` Output

```text
PASS  032_short_fri27_opening_testA_v02.mp4  dur=30.0s  audio=-16.7dB  motion=14.51  f0diff=4.28  cut1=2.47s  vo_onset=0.11s  tail_gap=1.19s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/fri27_opening_testA/06_Final-Exports/032_short_fri27_opening_testA_v02_vo.wav  dhash=62f07030ab1680a2  visor=0.0
   full-bleed 0.00s  fills the frame  sharp above/middle/below=None/0.529/None  detail top/centre/bottom=11.7/8.33/4.69  spread top/bottom=49.35/10.35
   full-bleed 0.25s  fills the frame  sharp above/middle/below=None/0.522/None  detail top/centre/bottom=11.63/8.0/4.63  spread top/bottom=49.11/10.61
   full-bleed 0.50s  fills the frame  sharp above/middle/below=None/0.506/None  detail top/centre/bottom=11.81/7.81/4.52  spread top/bottom=48.61/10.96
   full-bleed whole Short  0/30 frames padded at one a second, 0/60 at two a second  padded stretches: none  end card 28.9-30.0s judged apart
   warn  duration 30.0s outside 22–27s band
```

---

## 3. Required Brief, `OWB-2026-11-E1`, 60% Stayed & 70% Viewed Checklist

- **#1 · Keeper Title & Question:** *Could You Survive Stepping Onto Saturn's Moon Titan?* — positive survival question asked in `s01` (`0.130–5.210 s`: *"If you stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"*).
- **#2 · First-Second Rule (`0.0–1.5 s`, `J2429`):**
  - Frame-0 source: real moving NASA SVS 20311 `SVS20311_DF_End_Pan_1080.mp4` (`offset=2.20 s`, full-bleed `1080x1920` `cover`, `f0diff=4.28 >= 1.50`, `visor=0.0`, `near_black=1% <= 30%`, `0` blur-pad bars).
  - Hook caption on frame 0 (`0.00–2.10 s`): `STEP OUT` (white) / `ON TITAN?` (`#FFE000` yellow), `130 px` Arial Black.
  - First spoken word onset: `0.130 s` (`gate_shorts_open` `vo_onset=0.11 s <= 0.15 s`).
  - Meta-promise / spoken CTA present: **`no`** (`0` meta-promises, `0` spoken CTAs).
- **#3 & E1 · Cut Timings & Pacing (`12` shots, `11` cuts, `0` words split across cuts):**
  - **Cut 1:** `2.467 s <= 2.80 s`
  - **Cut 2:** `4.100 s <= 4.80 s`
  - **All cut timestamps (s):** `2.467`, `4.100`, `6.900`, `8.533`, `11.633`, `14.733`, `16.433`, `19.700`, `23.400`, `25.833`, `28.933`
  - **Longest plate hold:** `3.700 s <= 4.00 s`
- **#6 · Payoff Timing (`>= 70%` runtime):**
  - Runtime: `30.000 s` (`Test A` `30–38 s` window); `0.70 x 30.000 s = 21.000 s`.
  - Actual lethal payoff (`s05`: *"What would kill you is the cold and the fact that there is almost no oxygen to breathe"*) starts at **`23.530 s` (`78.4% >= 70.0%` PASS)**, well clear of the `9.00–14.00 s` parent-long title banner (`What Would Happen If You Landed on Titan? (Seas of Liquid Gas)`).
- **#7 · Sentence-1 Seam (`4–5 s`):**
  - `s01` → `s02` VO breath tightened from `1.140 s` to **`0.230 s < 0.25 s`** (`5.210–5.440 s`), bridging over `SVS20311_Dragonfly_Landed_Closeup.png` (`4.100–6.900 s`) and moving `SVS20311_DF_Intake_shot_1080.mp4` (`6.900–8.533 s`) straight into *"Your body would not explode, and your blood would not boil."*
- **Single Teach-on-Screen Number Object (`16.433–19.700 s`):**
  - Native `9:16` animated pressure comparison (`EARTH AIR 1.00 BAR` with real Apollo 17 `AS17-148-22727` globe vs `TITAN SKY` building to `1.47 BAR` with real Cassini `PIA20016` globe) + `1.47 BAR (1.5× EARTH)` pill (`16.55–19.55 s`, inside `16:9` safe band `bbox=[167, 1190, 912, 1260]`).
- **Loop Tail (`< 1.20 s` E1 limit):**
  - Last spoken word (`"breathe"`) ends at `28.810 s`; loop seam at `30.000 s` → **tail gap = `1.190 s < 1.20 s`**, with continuous moving preroll (`1.133 -> 2.200 s` of `SVS20311_DF_End_Pan_1080.mp4`) arriving on the exact frame-0 framing and score bed running through the seam.
  - Loop sentence (`s05` → `s01`): *"...What would kill you is the cold and the fact that there is almost no oxygen to breathe — if you stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"*
