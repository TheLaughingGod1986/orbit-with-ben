# Scheduled Orbit Shorts against the first-second rule (J2493)

Written 10 Nov 2026 by claudecode. Table only: nothing built, nothing changed on YouTube, £0.

Schedule source: `05_Analytics/owb/snapshots/2026-11-10.json` (publishAt per video) merged with `00_Brand/Channel-Setup/social/UPLOADS.json` (export file, sha256). The brief says twenty; the merge gives **24**, because UPLOADS.json has no publishAt for four that the snapshot shows scheduled (B1z2dv7m7Vk, bSjWiCbB7pY, gmzaCfJF1gA, kKN8Ale42sE) and none for xvarZP2aYyE, while it still carries a stale 30 Nov publishAt for `bizlhspnVvY` (comets v01), which the snapshot shows with no schedule: xvarZP2aYyE (comets v04) holds that slot. bizlhspnVvY is left out.

"sha ok" means the file to hand hashes to the sha256 recorded at upload, so it is the bytes on YouTube.

## Step 1: what is scheduled and where its file is

| # | Airs (UTC) | Video id | Title | Export file | File to hand | In scope |
|---|---|---|---|---|---|---|
| 1 | 2026-11-10 11:30 | `ffYKoNVPoqg` | What Would Standing on Saturn's Moon Titan Feel Like? | `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s6_titan_v11.mp4` | Mini (sha ok) | no: airs inside 48 h |
| 2 | 2026-11-11 11:30 | `B1z2dv7m7Vk` | Why Did a 90-Day Mars Rover Last 14 Years? | `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/wed11_opening_testA/06_Final-Exports/wed11_opening_testA_v07.mp4` | Mini (sha ok), NAS (sha ok) | no: airs inside 48 h |
| 3 | 2026-11-12 11:30 | `N42gKBbD7tE` | How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years? | `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports/thu12_length_test_dust_v01.mp4` | none. Ruled KNOWN (J1320): uploaded bytes not kept; YouTube copy is canonical | no: no file to gate |
| 4 | 2026-11-13 11:30 | `bSjWiCbB7pY` | How Did a Helicopter Fly 72 Times on Mars? | `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/fri13_ingenuity_72_v02.mp4` | none. Ruled KNOWN (J1320): uploaded bytes not kept; YouTube copy is canonical | no: no file to gate |
| 5 | 2026-11-14 11:30 | `gmzaCfJF1gA` | Why Does Pluto's Giant Ice Heart Have Zero Craters? | `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s7_pluto_heart_v01.mp4` | Mini (sha ok) | yes |
| 6 | 2026-11-16 11:30 | `HZGTovJu_TQ` | If You Can't See the Nearest Star, How Far Away Is It? | `../../../../Volumes/data/mac-mini-archive/youtube-staging/026/shorts_j0141/mon16_cant_see_nearest_star_v01.mp4` | Mini (sha ok), NAS (sha ok) | yes |
| 7 | 2026-11-17 11:30 | `kKN8Ale42sE` | How Far From Earth Is Voyager 1 Right Now? | `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s8_voyager1_v01.mp4` | Mini (sha DIFFERS) | yes |
| 8 | 2026-11-18 11:30 | `cwU_0WWeNZ4` | If Voyager Needs 75,000 Years, How Far Is the Nearest Star? | `../../../../Volumes/data/mac-mini-archive/youtube-staging/026/shorts_j0141/wed18_robot_reach_nearest_star_v01.mp4` | Mini (sha ok), NAS (sha ok) | yes |
| 9 | 2026-11-20 11:30 | `aAUgIGEuPwQ` | The Nearest Star Is a Cherry Past Cairo. How Do We Know? | `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/fri20_grapefruit_cherry/06_Final-Exports/fri20_grapefruit_cherry_v04.mp4` | Mini (sha ok), NAS (sha ok) | yes |
| 10 | 2026-11-21 11:30 | `rvug71d7Dqk` | Muons Shouldn't Reach the Ground. They Do. | `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/fri06_muons_ground_v04.mp4` | Mini (sha ok) | yes |
| 11 | 2026-11-23 11:30 | `Dm4xsF1Ateg` | Why Do You Weigh Less at Earth's Equator? | `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/10_Shorts/lift_equator_weight/06_Final-Exports/earth_equator_weight_v07.mp4` | Mini (sha ok), NAS (sha ok) | yes |
| 12 | 2026-11-25 11:30 | `xdurJQcoiGM` | Where Will the International Space Station Crash? | `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/06_Final-Exports/owb_ar2_iss_2030_deorbit_v13.mp4` | Mini (sha ok) | yes |
| 13 | 2026-11-27 11:30 | `93JL_IK57EM` | Will Asteroid 2024 YR4 Hit the Moon in 2032? | `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/06_Final-Exports/owb_ar1_2024_yr4_moon_v06.mp4` | Mini (sha ok) | yes |
| 14 | 2026-11-28 11:30 | `MScK2CK2ZFg` | Where Will the 2027 Total Solar Eclipse Last Over Six Minutes? | `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/06_Final-Exports/owb_ar3_2027_eclipse_v14.mp4` | Mini (sha ok) | yes |
| 15 | 2026-11-30 11:30 | `xvarZP2aYyE` | Why Will Gliese 710's Comets Arrive After It Has Gone? | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/028_short_mon30_comets_v04/028_short_mon30_comets_v04.mp4` | NAS archive only (no sha256 recorded at upload, so not provable as the uploaded bytes) | yes |
| 16 | 2026-12-02 11:30 | `v6euXX2omz4` | Is a Star Really Coming Towards Us? | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/028_short_wed02_opening_testA_v04/028_short_wed02_opening_testA_v04.mp4` | Mini (sha ok), NAS (sha ok) | yes |
| 17 | 2026-12-04 11:30 | `BTuL_QBbEgY` | How Close Will Gliese 710 Come to the Sun? | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/fri04_scale/06_Final-Exports/028_short_fri04_scale_v07.mp4` | Mini (sha ok), NAS (sha ok) | yes |
| 18 | 2026-12-05 11:30 | `C8lPx5N2DwM` | What Happens When Earth's Magnetic Field Flips? | `02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01.mp4` | NAS (sha ok) | yes |
| 19 | 2026-12-07 11:30 | `lsOCcIYCud0` | What Will the Night Sky Look Like When Gliese 710 Arrives? | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/lift_night_sky_35yr/06_Final-Exports/028_short_lift_night_sky_35yr_v07.mp4` | Mini (sha ok), NAS (sha ok) | yes |
| 20 | 2026-12-09 11:30 | `SWDCZfWZVao` | Why Did Betelgeuse Suddenly Lose Two-Thirds of Its Light? | `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/wed09_great_dimming/06_Final-Exports/029_short_wed09_great_dimming_v04.mp4` | Mini (sha ok), NAS (sha ok) | yes |
| 21 | 2026-12-11 11:30 | `k2kEaA7ICjc` | Is Betelgeuse Really About to Explode? | `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/fri11_opening_testA/06_Final-Exports/029_short_fri11_opening_testA_v04.mp4` | Mini (sha ok), NAS (sha ok) | yes |
| 22 | 2026-12-12 11:30 | `QEoYKIVvKBA` | What If the Solar Wind Blew Earth's Atmosphere Into Space? | `02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03.mp4` | NAS (sha ok) | yes |
| 23 | 2026-12-14 11:30 | `heiGCnGKTkE` | How Bright Will Betelgeuse Get When It Explodes? | `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/mon14_half_moon_daylight/06_Final-Exports/029_short_mon14_half_moon_daylight_v04.mp4` | Mini (sha ok), NAS (sha ok) | yes |
| 24 | 2026-12-16 11:30 | `f17XCtUmN-g` | What Happens When Gliese 710 Passes Through the Oort Cloud? | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/lift_oort_marbles/06_Final-Exports/028_short_lift_oort_marbles_v03.mp4` | Mini (sha ok), NAS (sha ok) | yes |

## Step 2 and 3: gate result per Short, and what a re-cut would need

`gate_shorts_open.py check --report-only --json`, each run under a 240 s limit; none hung. FAIL here means it would fail the 60% stayed gate (still at frame 0, first cut after 3.0 s, or a meta-promise line) or first-second check 9 (slow fade from black, missing hook text at 0.0 s). Hard gate fails (length, loudness, Orbit at frame 0, near-duplicate open): none on any of the 20.

**Result: 4 FAIL, 16 PASS, 4 not gated.**

| # | Airs | Video id | First-second | Voice onset | Movement at frame 0 (0-1.5 s diff, floor 1.50) | First cut | Meta-promise | Other warnings |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-10 | `ffYKoNVPoqg` | not gated (airs inside 48 h) | | | | | |
| 2 | 2026-11-11 | `B1z2dv7m7Vk` | not gated (airs inside 48 h) | | | | | |
| 3 | 2026-11-12 | `N42gKBbD7tE` | not gated (no file to gate) | | | | | |
| 4 | 2026-11-13 | `bSjWiCbB7pY` | not gated (no file to gate) | | | | | |
| 5 | 2026-11-14 | `gmzaCfJF1gA` | **FAIL** | 0.07 s | 0.64 (still) | 5.90 s | ("stay, and i'll show you") | gap from last word to end is 3.01s > 1.5s (last word 19.42s, duration 22.43s) |
| 6 | 2026-11-16 | `HZGTovJu_TQ` | **FAIL** | 0.04 s | 2.08 | 4.80 s | none | none |
| 7 | 2026-11-17 | `kKN8Ale42sE` | **FAIL** | 0.07 s | 0.33 (still) | 4.60 s | ("stay, and i'll show you") | duration 20.7s outside 22–27s band; gap from last word to end is 3.00s > 1.5s (last word 17.74s, duration 20.74s) |
| 8 | 2026-11-18 | `cwU_0WWeNZ4` | **FAIL** | 0.00 s | 0.46 (still) | 2.87 s | none | none |
| 9 | 2026-11-20 | `aAUgIGEuPwQ` | PASS | 0.00 s | 3.58 | 2.37 s | none | possible Orbit at 0 s (visor 0.0018) — eyeball the sheet |
| 10 | 2026-11-21 | `rvug71d7Dqk` | PASS | 0.10 s | 3.94 | 3.00 s | none | none |
| 11 | 2026-11-23 | `Dm4xsF1Ateg` | PASS | 0.03 s | 6.10 | 2.30 s | none | none |
| 12 | 2026-11-25 | `xdurJQcoiGM` | PASS | 0.04 s | 7.53 | 2.40 s | none | duration 18.4s outside 22–27s band |
| 13 | 2026-11-27 | `93JL_IK57EM` | PASS | 0.04 s | 4.95 | 2.40 s | none | duration 19.4s outside 22–27s band |
| 14 | 2026-11-28 | `MScK2CK2ZFg` | PASS | 0.04 s | 3.04 | 2.40 s | none | duration 17.1s outside 22–27s band |
| 15 | 2026-11-30 | `xvarZP2aYyE` | PASS | 0.00 s | 3.26 | 2.53 s | none | none |
| 16 | 2026-12-02 | `v6euXX2omz4` | PASS | 0.00 s | 3.19 | 2.20 s | none | none |
| 17 | 2026-12-04 | `BTuL_QBbEgY` | PASS | 0.03 s | 5.32 | 2.43 s | none | possible Orbit at 0 s (visor 0.0015) — eyeball the sheet |
| 18 | 2026-12-05 | `C8lPx5N2DwM` | PASS | 0.08 s | 9.28 | 2.32 s | none | duration 33.0s outside 22–27s band |
| 19 | 2026-12-07 | `lsOCcIYCud0` | PASS | 0.00 s | 2.98 | 2.47 s | none | none |
| 20 | 2026-12-09 | `SWDCZfWZVao` | PASS | 0.05 s | 4.62 | 2.70 s | none | gap from last word to end is 2.29s > 1.5s (last word 20.41s, duration 22.70s) |
| 21 | 2026-12-11 | `k2kEaA7ICjc` | PASS | 0.08 s | 5.94 | 2.23 s | none | duration 33.9s outside 22–27s band; gap from last word to end is 2.32s > 1.5s (last word 31.58s, duration 33.90s) |
| 22 | 2026-12-12 | `QEoYKIVvKBA` | PASS | 0.09 s | 5.01 | 2.36 s | none | none |
| 23 | 2026-12-14 | `heiGCnGKTkE` | PASS | 0.06 s | 7.57 | 3.00 s | none | gap from last word to end is 2.29s > 1.5s (last word 21.64s, duration 23.93s) |
| 24 | 2026-12-16 | `f17XCtUmN-g` | PASS | 0.00 s | 1.91 | 2.97 s | none | none |

### The four FAILs, soonest first

**2026-11-14 `gmzaCfJF1gA` Why Does Pluto's Giant Ice Heart Have Zero Craters?**

- pushed still at frame 0 (mean 0–1.5 s frame diff 0.64 < 1.50) — use moving footage
- first cut at 5.90s > 3.0s (scene-change detect)
- spoken text contains meta-promise ("stay, and i'll show you")
- Fix: Re-cut for picture: open on moving footage and bring the first cut inside 3 s (existing picture, existing voice). The "stay, and I'll show you" line: a trim only if it is its own sentence in the take; if it runs into the next words it needs a new voice take. Not checked which (no transcript tool here).

**2026-11-16 `HZGTovJu_TQ` If You Can't See the Nearest Star, How Far Away Is It?**

- first cut at 4.80s > 3.0s (scene-change detect)
- Fix: Re-cut only: bring the first cut inside 3 s (now 4.80 s). Existing picture and voice.

**2026-11-17 `kKN8Ale42sE` How Far From Earth Is Voyager 1 Right Now?**

- pushed still at frame 0 (mean 0–1.5 s frame diff 0.33 < 1.50) — use moving footage
- first cut at 4.60s > 3.0s (scene-change detect)
- spoken text contains meta-promise ("stay, and i'll show you")
- Fix: Same as Pluto: re-cut for the still open and the 4.60 s first cut; the "stay, and I'll show you" line is a trim if separable, else a new voice take. Note the file on the Mini does not hash to the uploaded sha256, so these readings may not be the uploaded cut.

**2026-11-18 `cwU_0WWeNZ4` If Voyager Needs 75,000 Years, How Far Is the Nearest Star?**

- pushed still at frame 0 (mean 0–1.5 s frame diff 0.46 < 1.50) — use moving footage
- Fix: Re-cut only: start on moving footage (frame 0 is a pushed still; first cut is already at 2.87 s). Existing picture and voice.

### Not measured

- **When the subject and surprise word are spoken:** not measured. The gate does not time individual words, and no speech-to-text tool is installed on the Mini (`whisper`, `whisper-cli`, `mlx_whisper` all absent). Voice onset above is the nearest reading: every one of the 20 starts speaking within 0.10 s.
- **Longest pause in sentence 1:** not reliable. Silence detection on the first 6 s of each final mix (-35 dB, 0.12 s) found a gap on only three (HZGTovJu_TQ 0.72 s at 3.54 s, cwU_0WWeNZ4 0.71 s at 3.69 s, aAUgIGEuPwQ 0.25 s at 3.17 s); on the rest the music bed sits above the threshold, so no gap shows. It needs the voice stems, and the sentence boundary needs a transcript.
- **The four not gated:** ffYKoNVPoqg (10 Nov) and B1z2dv7m7Vk (11 Nov) air inside 48 h; N42gKBbD7tE (12 Nov) and bSjWiCbB7pY (13 Nov) have no kept export (J1320 ruling).

### For the Chief

- Re-cut candidates by air date: gmzaCfJF1gA (14 Nov), HZGTovJu_TQ (16 Nov), kKN8Ale42sE (17 Nov), cwU_0WWeNZ4 (18 Nov). Each re-cut is a new cut and needs Ben's watch before it replaces a scheduled upload.
- Everything from 20 Nov onward passes the checks the gate can run. rvug71d7Dqk and heiGCnGKTkE sit exactly on the 3.00 s first-cut limit; f17XCtUmN-g is at 2.97 s.
- UPLOADS.json still carries a 30 Nov publishAt on bizlhspnVvY (comets v01), which the 10 Nov snapshot shows unscheduled. Worth confirming in Studio that only xvarZP2aYyE airs that day.
- xvarZP2aYyE has no sha256 in UPLOADS.json and kKN8Ale42sE's local file does not match its recorded sha256.
- Nothing was built, uploaded or changed.
