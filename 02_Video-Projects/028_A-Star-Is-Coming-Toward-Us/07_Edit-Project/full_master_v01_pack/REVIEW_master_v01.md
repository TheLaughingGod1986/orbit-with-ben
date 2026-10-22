# 028 A Star Is Coming Toward Us (Gliese 710) — Full Master v01 Review (`J0859`, 22 Oct 2026)

**Cut:** `028_Gliese710_full_master_v01.mp4` (`472.83 s`, `61` cuts, max single picture `14.66 s`, `-14.1 LUFS` / `-1.3 dBTP`, **£0 spend**)
**SHA-256 (all 3 copies identical):** `42d5c760178458aedbfa530332f82b2b1007ca339cc6519aa087e518d34fdc1b`

## 1. Three £0 Fixes Applied (Before vs After — see `sheet_fixes_v01.jpg` & `sheet_pills_midpoint_v01.jpg`)

| Fix | Before (`part_roughs_v01` / `J0855`) | After (`full_master_v01` / `J0859`) | Verification |
|---|---|---|---|
| **1. `r19_subscribe` (`204.21–209.89 s` / `3:27`)** | Used `eso_startrails.mp4` (`offset=18.0 s`), which repeated the concentric star-trails sky from `r13_star_trails` (`2:10`, 77 s earlier). | Swapped `r19_subscribe` to `gaia_gliese_encounter.mov` at `offset=20.5 s` (`vcrop=(1536, 864, 192, 108)`, `1.25x` upscale) with the house `SUBSCRIBE` pill (`206.80–209.44 s`) and `ESA/Gaia/DPAC · CC BY-SA 3.0 IGO` credit on the free interval. All 3 uses of `gaia_gliese_encounter.mov` (`8.0 s`, `20.5 s`, `31.0 s`) are disjoint and `>= 10.5 s` apart. | `picture_qa.py` **PASS** (0 reuse fails; moving 3D starfield flyby, not star trails). |
| **2. `gaia_motion_1_6my.mp4` reuse (`5` uses → `3` uses, never two in a row)** | Used 5 times (`r01_stars_streaming` at `0:00`, `r02_gaia_span_2` at `0:06`, `r12_stars_move` at `1:57`, `r27_leaving` at `5:05`, `r38_return` at `7:43`), including two back-to-back in the open. | 1. **Merged `r01` + `r02`** into one continuous opening shot `r01_stars_streaming` (`0.00–13.66 s`, `offset=3.80 s` → `[3.80, 17.46]`, with an internal framing step at `6.12 s` from `1.33x` to `1.43x`).<br>2. **Replaced `part04` `r27_leaving`** (`305.02–316.04 s` / `5:05`) with `eso_startrails.mp4` at `offset=14.0 s` (`vcrop=(1664, 936, 0, 0)`, `1.15x` upscale; `eso_startrails.mp4` is now used only twice in the film, at `offset=0.0 s` on `r13_star_trails` and `offset=14.0 s` on `r27_leaving`, 171 s apart).<br>3. **Kept exactly 3 disjoint stretches of `gaia_motion_1_6my.mp4`**: `r01_stars_streaming` (`0:00`, `offset=3.80 s`), `r12_stars_move` (`1:57`, `offset=18.0 s`), and `r38_return` (`7:43`, `offset=31.0 s`). | `picture_qa.py` **PASS** (`3` uses total, never two in a row, all `>= 13.0 s` apart in source offset). |
| **3. Pill legibility (`'5 times closer'` at `2:52` and `'100 metres'` at `3:19`, plus all 22 pills)** | On `part02_rough_v01_contact_sheet.jpg`, `r16_sunrise_break` (`cut_mid=172.385 s`) and `r18_shell` (`cut_mid=199.73 s`) had `film_start` (`172.40 s` and `199.68 s`) right at the cut midpoint, so the contact sheet caught the first 0–2 frames of their 0.35 s alpha fade-in (`p99=91.0` and `p99=150.0`). | Added a `0.40 s` fade-in lead before `film_start` on `r15_gaia_craft` (`'1 billion stars'`), `r16_sunrise_break` (`'5 times closer'`), and `r18_shell` (`'100 metres'`) plus strict `:enable='between(t,la,lb)'` gating so the 0.35 s slide-up/fade-in completes right as the SFX tick lands at `film_start`. At `2:52.4` (`cut_mid`) AND `2:53.8` (`pill_mid`), `'5 times closer'` is now `p99=255.0 / max=255`; at `3:19.7` (`cut_mid`) AND `3:20.9` (`pill_mid`), `'100 metres'` is now `p99=255.0 / max=255`. Checked all 22 pills at each pill's midpoint (`sheet_pills_midpoint_v01.jpg`, `pills_midpoint_stats_v01.json`): all 22 reach `max=255, p99=255.0` full opacity with the identical dark navy backing box `(23, 36, 55, 220)`. | `22/22` pills verified at `p99=255.0 / max=255` full opacity (`sheet_pills_midpoint_v01.jpg` & `sheet_fixes_v01.jpg`). |

## 2. £0 Score Bed + House SFX + Master Mix (`05_Music/` & `06_Sound-Effects/`)

- **Score bed (`05_Music/gliese_score_bed_v01.mp3`):** `472.84 s`, `70.6 BPM` (brief `Pace: 64-74 BPM`), `-35.4 LUFS` integrated (`16–21 dB` below VO across 30 s windows, J0079 envelope-ducked under speech with `0` breaches in `sfx_kit.py level --bed`), shifting between `awe` pads (`Ch 0 Open`, `Ch 3 Into the Oort Cloud`, `Ch 5 A New Brightest Star`, `Ch 6b closing payoff`) and `explain` plucked celesta/harp arpeggio (`Ch 1`, `Ch 2`, `Ch 4`, `Ch 6a`) at chapter cards.
- **House SFX (`06_Sound-Effects/stem_sfx_v01.wav`):** `36` cues (`-31.6 LUFS` integrated vs `-14.7 LUFS` VO = `16.9 LU` under VO, `0` breaches): an SFX tick on all `22` teaching pills, all `6` chapter cards, the `SUBSCRIBE` pill, and the `2` ruler scale bars (`>= 0.5 s` between all ticks), plus soft whooshes and `4` low rumbles.
- **Master mix (`028_Gliese710_full_master_v01.mp4`):** two-pass linear `loudnorm` to **`-14.1 LUFS` / `-1.3 dBTP`**.

## 3. Gate Outputs (All PASS)

- **`clip_check.py`:** `clip_check: 61 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.`
- **`picture_qa.py`:** `picture QA PASS: 0 of 61 cuts fail, 6 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v01_pack/picture_qa_v01/PICTURE_QA.md`
- **`polish_gate.py`:** `polish gate PASS: 0 of 61 rows failed, 3 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v01_pack/polish_gate_v01.json`
- **`music_gate.py --video`:** `WARN reused: couldn't read saturn_long_vo_v02_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read jupiter-vo.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read jupiter-music.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read friday_black_dwarf_short_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v02_LISTEN.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v02_how_long.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03_tightened.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03b_tightened_LOCK.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03b_tightened_LOCK.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v02_how_long.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03_tightened.wav to compare (OSError); download it or pass --others
music gate PASS: gliese_score_bed_v01.mp3, 472.8 s, about 70.6 BPM, brief Pace: 64-74 BPM`
- **`sfx_kit.py level`:** `sfx level PASS: VO -14.7 LUFS, SFX -31.6 LUFS (36 hits), 0 fails` (`06_Sound-Effects/sfx_level_v01.json`)
- **`npm run gate:episode`:** `PASS — VO / Gemini Veo allowed · Script score: 91/100 · PASS` (`episode_gate_v01.txt`)
