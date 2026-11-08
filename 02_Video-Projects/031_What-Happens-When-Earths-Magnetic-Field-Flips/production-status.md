# Production status — 031 What Happens When Earth's Magnetic Field Flips?

| Field | Value |
|-------|-------|
| Slug | `031_What-Happens-When-Earths-Magnetic-Field-Flips` |
| Gate | BLOCK on `prebuild_vidiq` sign-off (all script/structure checks OK) |
| Script review | PASS 95.4 / 100 (`magnetic_field_flip_script_master_v01.md`, 1,300 spoken words, 6 chapters, J0259) |
| VO | locked `magnetic_field_flip_vo_v02a` (Chief h32, J1295, 31 Oct 2026). h24's 20 ms / 40 ms fades were too short |
| CG | pending (Vertex Veo / Omni Orbit-only) |
| Runtime target | 7–9 min (~8.8 min est.) |
| Shorts | 2 active + 1 reserve (`10_Shorts/SHORTS_PLAN_v01.md`, J2147, 5 Nov 2026): Path A **Sat 5 Dec 11:30Z** (Test A opening, `33.00 s`) & **Sat 12 Dec 11:30Z** (solar wind vs atmosphere, `24.48 s`), reserve **Fri 18 Dec 11:30Z** (worldwide auroras, `23.50 s`); Path B **Wed 2 Dec 11:30Z** go-public day slot if Chief shifts `028` `v6euXX2omz4` to Sat 5 Dec |

## VO lock (Chief h32, J1295, 31 Oct 2026)

Locked stem `02_Voiceover/magnetic_field_flip_vo_v02a`. Built from the v02 parts only. Each part fades out with `afade=t=out:curve=qsin` ending on its last sample: ch00 `st=35.24:d=0.12`, ch01 `st=88.38:d=0.02`, ch02 `st=100.28:d=0.04`, ch03 `st=92.14:d=0.02`, ch04 `st=73.96:d=0.04`, ch05 `st=86.22:d=0.02`, ch06 `st=87.42:d=0.18`. This replaces the h24 fades (ch00 20 ms, ch06 40 ms), which stopped above −50 dBFS. No re-take, no ElevenLabs, no new STT. The 1905 date/place card spells PONTFAREIN (h24).

| Check | Result |
|-------|--------|
| Duration | 568.280 s, 27,277,440 frames, pcm_s16le, 48 kHz stereo |
| Loudness | I −19.9 LUFS, LRA 4.8 LU, true peak −3.5 dBFS |
| ch00 tail | last 10 ms RMS −56.11 dBFS, last sample 0/0 |
| ch01 tail | last 10 ms RMS −71.55 dBFS, last sample 0/0 |
| ch02 tail | last 10 ms RMS −58.22 dBFS, last sample 0/0 |
| ch03 tail | last 10 ms RMS −71.09 dBFS, last sample 0/0 |
| ch04 tail | last 10 ms RMS −58.07 dBFS, last sample 0/0 |
| ch05 tail | last 10 ms RMS −59.52 dBFS, last sample 0/0 |
| ch06 tail | last 10 ms RMS −57.08 dBFS, last sample 0/0 |
| Null vs v02 | max abs diff 0 outside 35.240–35.360, 124.440–124.460, 225.440–225.480, 318.320–318.340, 393.000–393.040, 479.960–479.980 and 568.100–568.280 s |
| wav sha256 | `3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6` (matches Chief sim) |
| mp3 sha256 | `334085b5f1eb1992a0fd7f31ff46f97b24b0443158551f2cf91476a9d9c31347` (libmp3lame 128k, same settings as v02) |
| Word timings | copied from `stt/magnetic_field_flip_vo_v02/` to `stt/magnetic_field_flip_vo_v02a/` |

v01 and v02 (wav, mp3, parts, stt) were not modified.

## Blockers

- [ ] Pre-build vidIQ signed + neighbour pass (≥3 education/space videos ≈1M+ views) + Chief topic lock
- [x] Script ≥ 90 (`review:script` PASS 95.4/100 on `v01`)
- [ ] Gemini `facts` quote check on `01_Script/SOURCES.md` + `CLAUDE_QUOTE_CHECK_v01.md`
- [ ] Stills locked before Veo/Omni spend

## `npm run review:script` (J0259, 15 Oct 2026)

```
# magnetic_field_flip_script_master_v01.md

**Decision:** PASS · **Score:** 95.4 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1321 · Est. min: 8.8 · Chapters: 6
Pass threshold: 90
```

## J1752 final VO review — 3 November 2026

Technical verification PASS against the actual Mini output: both full hashes match J1295, 568.280 s, -19.9 LUFS / -3.5 dBTP, all seven tails below -50 dBFS and ending 0/0, null outside h32 fades exactly zero. Evidence: `02_Voiceover/review_J1752/measurements.json` and `REVIEW.md`.

Final approval remains pending: codex could measure the files but had no audio listening input; nothing was heard in this session. Required FIX is completion of the listening review, not a media rebuild. Responsible reviewer: elected Chief with actual Mini audio listening capability, resuming J1752 (1/3 complete). No other stage is approved.

## J1810 capability validation — 4 November 2026

Fresh native Gemini audio fixture test failed: the first claimed perception contradicted the fixture, and independent recheck explicitly reported no reliable audio perception. J1752 retains technical PASS at 1/3; no VO was heard or approved. J1810 owns demonstrating a reliable native listening route before any specialist handoff. [Evidence](../../jobs/reviews/J1810/REPORT.md). No Ben production-review action.

## J2381 Long Master `v01` Assembly & Gates — 8 November 2026

Assembled `031_What-Happens-When-Earths-Magnetic-Field-Flips` long master `v01` (`570.80 s` / `14,270` frames at `25 fps` CFR, `1920x1080`, `yuv420p`, `-14.6 LUFS`, `-1.0 dBTP`) from the 54-row shot list (`SHOT_LIST_v02.md`), completed £0 J2141 picture package, £0 chapter-shaped score bed (`magnetic_field_flip_score_bed_v01.mp3`), and £0 house SFX kit (`06_Sound-Effects/kit_v01`).

- **Master MP4 (NAS):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/09_Final-Export/031_what_happens_when_earths_magnetic_field_flips_master_v01.mp4` (`SHA-256: 1b90d78270d4f06b436b42e1a31d700171850511cb7790e43a546da2e20bc69b`)
- **Score Bed MP3 (NAS):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/05_Music/magnetic_field_flip_score_bed_v01.mp3` (`SHA-256: 9fe2f87876f9b0bbf1a80fb58d14f2ded4fddf4437efc3a83dfa4e321d0ec71f`)
- **Handoff & Pack:** `07_Edit-Project/ASSEMBLY_HANDOFF_J2381_v01.md` and `07_Edit-Project/full_master_v01_pack/`

```
clip_check: 54 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.

picture QA PASS: 0 of 115 cuts fail, 11 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v01_pack/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v01_pack/picture_qa_review.jpg

music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM

SFX level PASS: VO -19.9 LUFS, SFX -45.3 LUFS, 15 hits
```

## J2387 Long Master `v02` Repair & Gates (J2382 FIX) — 8 November 2026

Repaired `031_What-Happens-When-Earths-Magnetic-Field-Flips` long master `v02` (`570.80 s` / `14,270` frames at `25 fps` CFR, `1920x1080`, `yuv420p`, `-14.6 LUFS`, `-1.0 dBTP`, `0` black frames) addressing all 5 `J2382` review defects while preserving `master_v01.mp4` untouched (`SHA-256: 1b90d78270d4f06b436b42e1a31d700171850511cb7790e43a546da2e20bc69b`):

1. Removed `cosmic_wave_ov.png` concentric bullseye/grid overlay from `R01 c1`, `R15 c2`, `R25 c1..c4`, and `R50 c1`.
2. Capped `nasa_svs_3822_magfield_left.mp4` to `4` stretches (`<= 5` limit across all sources in `cuts_v02.json`: `hdev_earth_views_iss_2019.mp4: 5`, `nasa_svs_3822_magfield_left.mp4: 4`, `nasa_svs_12312_dscovr_epic_earth.mp4: 4`, `nasa_svs_12296_earth_interior_cutaway.mp4: 4`, `iss030e078095_aurora_timelapse.mp4: 3`, `nasa_svs_20297_magnetosphere_earth_only.mp4: 3`) with honest source attribution in `cuts_v02.json`.
3. Rebuilt `R32 c2` (`5:29`, `code_graphic_031_r32_paleo_v02.mp4`) with animated paleointensity comparison bars (`TODAY` `2.0x` vs `MILLION-YEAR AVERAGE` `1.0x`, `TWICE ITS AVERAGE`) on the right (`x=1080..1700`) over the rotating Earth interior cutaway (`nasa_svs_12296_earth_interior_cutaway.mp4`) shifted left (`0` overlap), and rebuilt `R33 c3` (`code_graphic_031_r33c_paleo_dip_v02.mp4`, `LASCHAMP DIP`) over a softly blurred moving core plate (`gblur=sigma=32`) with zero split-panel seam.
4. Cropped `PIA20016.jpg` (`R54 c2`, `9:27`) to `(0, 40, 1277, 758)` (`upscale 1.504x <= 2.35x`) above its burned-in source caption (`...iv. of Idaho (PIA20016)`) with clean house corner credit (`NASA/JPL-Caltech/Univ. of Idaho`).
5. Updated `R22` subscribe card (`3:27`) to `"NEW SPACE MYSTERIES EVERY WEEK"`.

- **Master `v02` MP4 (NAS):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/09_Final-Export/031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4` (`SHA-256: 680598ae3420afa9fd40efc954cf06cefcfff234044a62e90af6a143fdf4de43`)
- **Handoff & Pack:** `07_Edit-Project/ASSEMBLY_HANDOFF_J2387_v02.md` and `07_Edit-Project/full_master_v02_pack/`

```
clip_check: 54 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.

picture QA PASS: 0 of 115 cuts fail, 8 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v02_pack/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v02_pack/picture_qa_review.jpg

music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM

SFX level PASS: VO -19.9 LUFS, SFX -45.3 LUFS, 15 hits
```

## J2389 Active Short #2 (`031_short_sat12_solar_wind_air_v01`) Assembly & Gates — 8 November 2026

Built `031` Active Short #2 (*What If the Solar Wind Blew Earth's Atmosphere Into Space?*, `24.48 s` / `612` frames at `25 fps` CFR, `1080x1920`, `yuv420p`, `-14.0 LUFS`, `-2.2 dBTP`, £0 spend, no YouTube upload) lifting verbatim sentences `s65, s67, s70, s74` (`398.42–461.62 s`, `64` words) from locked VO `magnetic_field_flip_vo_v02a.wav` (`SHA-256: 3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6`), `magnetic_field_flip_score_bed_v01.mp3`, house SFX `kit_v01`, and `R39–R44` plates free of any synthetic bullseye overlay.

- **Short 2 MP4 (NAS):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01.mp4` (`SHA-256: 2f0f7e82e7d4c36d484d3bbf1ba7516118b3d1cdf61b788119996dc5ca85547c`)
- **Frame 0 (`1080x1920`):** `.../031_short_sat12_solar_wind_air_v01_frame0.jpg` (`SHA-256: 525885ee2c836f8fb5114532de207a83c5a5409d0b200bad83b5d961fd09762d`)
- **Custom Cover (`1080x1920`):** `.../031_short_sat12_solar_wind_air_v01_cover.jpg` (`SHA-256: b3f860ab6b94133c0bd637cdbba2ab6724f669876f61b5b9dee2c622c26a69d5`)
- **Handoff & Assembler:** `10_Shorts/SHORT2_SOLAR_WIND_AIR_HANDOFF_J2389_v01.md` and `10_Shorts/_assemble_031_short2_v01.py`

```
PASS  031_short_sat12_solar_wind_air_v01.mp4  dur=24.48s  audio=-16.9dB  motion=37.63  f0diff=11.21  cut1=2.36s  vo_onset=0.09s  tail_gap=1.46s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01_vo.wav  dhash=a917d9dbeb9d99db  visor=0.0

PASS  031_short_sat12_solar_wind_air_v01_frame0.jpg  1080x1920  223KB  sharp=303  bright=117
PASS  031_short_sat12_solar_wind_air_v01_cover.jpg  1080x1920  458KB  sharp=767  bright=124

SFX level PASS: VO -16.5 LUFS, SFX -38.5 LUFS, 5 hits
music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM
polish gate PASS: 0 of 9 rows failed, 1 to look at
picture QA PASS: 0 of 9 cuts fail, 1 to look at
```

## J2390 Edit Review (`master_v02` + Shorts 1 & 2) — 8 November 2026

Reviewed `031_What-Happens-When-Earths-Magnetic-Field-Flips` long master `v02` (`J2387`) and Active Short #2 `v01` (`J2389`). Full report in `jobs/reviews/J2390/REVIEW.md`.

- **Long Master `v02` (`J2387`):** **KEEP** (`031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4`, `SHA-256: 680598ae3420afa9fd40efc954cf06cefcfff234044a62e90af6a143fdf4de43`, `570.80 s`, `14,270` frames at `25 fps` CFR, `-14.6 LUFS`, `-1.0 dBTP`, `0` black frames). All 5 `J2382` FIX items resolved (`0` bullseye overlays, `<= 5` stretches across all sources with honest `cuts_v02.json`, animated paleointensity bars on `R32`/`R33c`, cropped `PIA20016` caption on `R54 c2`, `"NEW SPACE MYSTERIES EVERY WEEK"` on `R22`) and all 5 automated gates `PASS`. Staged to NAS `OWB UAT` and iCloud `OWB UAT`.
- **Active Short #2 `v01` (`J2389`, `031_short_sat12_solar_wind_air_v01.mp4`):** **FIX** — rebuild as `v02` (`031_short_sat12_solar_wind_air_v02.mp4`, preserving `v01` untouched) removing: (1) `get_nebula_wave()` diagonal sine-wave plaid and `make_cosmic_backdrop()` painted circle dots across the 9:16 top/bottom backdrop; (2) crude yellow/cyan `od.arc()` cartoon curves, `plasma_wave` sine ripple, and dark-ringed Earth cutout on `R39a` (`0.00–2.36 s`), `frame0.jpg`, `cover.jpg`, and `R39_loop`; (3) `R39b` (`2.36–3.32 s`) ghost double-exposed Blue Marble Earth over `svs_3822_magfield_left.mp4`; (4) `R42a` (`9.32–12.68 s`) `1 KILOGRAM` / `1 cm²` graphic text colliding beneath the `9.00–14.00 s` parent-title banner.
- **Active Short #1 (`J2388`):** Still `open` (not yet built when `J2390` was dispatched). Updated `J2388` deadline to `2026-12-02 18:00` and strictly chained `J2388 -> Short 2 v02 repair -> Shorts 1 & 2 review + UAT handoff`.

## J2388 Active Short #1 (`031_short_testA_opening_flip_v01`) Assembly & Gates — 8 November 2026

Built `031` Active Short #1 (Test A Opening Short: *What Happens When Earth's Magnetic Field Flips?*, `33.00 s` / `825` frames at `25 fps` CFR, `1080x1920`, `yuv420p`, `-14.1 LUFS`, `-2.1 dBTP`, £0 spend, no YouTube upload) lifting verbatim sentences `s00–s08` (`0.14–35.32 s`, `96` words, ending cleanly on the three concrete questions `031` answers per `LEARNINGS 17`) from locked VO `magnetic_field_flip_vo_v02a.wav` (`SHA-256: 3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6`), `magnetic_field_flip_score_bed_v01.mp3`, house SFX `kit_v01`, and repaired `v02` opening cuts (`R01–R04`) reframed to `9:16` over natural Gaussian-blurred NASA moving plates (free of any synthetic bullseye overlay, sine-wave plaid, painted dots, or cartoon arcs, and with honest `R03` DSCOVR EPIC pixels and zero text collision under the `9.0–14.0 s` parent-title banner).

- **Short 1 MP4 (NAS):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01.mp4` (`SHA-256: ebe11bb730ccfab8681d564d3588d17011a28629c7b6f926eba952bfc98c4bcd`)
- **Frame 0 (`1080x1920`):** `.../031_short_testA_opening_flip_v01_frame0.jpg` (`SHA-256: aa0763c2f1e553ac373e6596c684c1145b115242afcac0c9fa15d8eaf0030ada`)
- **Custom Cover (`1080x1920`):** `.../031_short_testA_opening_flip_v01_cover.jpg` (`SHA-256: 8f5be5cd1e41b0b5df695d6fbbe6e69682965f010ddc70f2e70b9bb053caee5d`)
- **Handoff & Assembler:** `10_Shorts/SHORT1_TESTA_OPENING_FLIP_HANDOFF_J2388_v01.md` and `10_Shorts/_assemble_031_short1_v01.py`

```
PASS  031_short_testA_opening_flip_v01.mp4  dur=33.0s  audio=-16.7dB  motion=27.25  f0diff=9.28  cut1=2.32s  vo_onset=0.08s  tail_gap=1.46s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_vo.wav  dhash=982b074783078b06  visor=0.0
   warn  duration 33.0s outside 22–27s band

PASS  031_short_testA_opening_flip_v01_frame0.jpg  saturation=105.4  near_black=1%
PASS  031_short_testA_opening_flip_v01_cover.jpg  saturation=138.1  near_black=2%

SFX level PASS: VO -16.3 LUFS, SFX -40.2 LUFS, 6 hits
music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM
polish gate PASS: 0 of 13 rows failed, 1 to look at
picture QA PASS: 0 of 13 cuts fail, 1 to look at
```


## J2394 Active Short #2 `v02` (`031_short_sat12_solar_wind_air_v02`) Repair & Gates — 8 November 2026

Rebuilt `031` Active Short #2 (*What If the Solar Wind Blew Earth's Atmosphere Into Space?*, `24.48 s` / `612` frames at `25 fps` CFR, `1080x1920`, `yuv420p`, `-14.0 LUFS`, `-2.2 dBTP`, £0 spend, no YouTube upload) as `031_short_sat12_solar_wind_air_v02.mp4` leaving `v01` untouched on NAS (`2f0f7e82e7d4c36d484d3bbf1ba7516118b3d1cdf61b788119996dc5ca85547c`), resolving all 4 `J2390` FIX items:
1. Removed `get_nebula_wave()` and `make_cosmic_backdrop()` completely; every shot uses full `9:16` reframing (`<= 2.35x` upscale) or `composite_band_on_natural_blur()` with a 96-px cosine feather over a clean, natural Gaussian-blurred vertical fill from real moving NASA pixels.
2. Removed `od.arc()` cartoon curves, `plasma_wave` sine ripple, and dark-ringed Earth cutout on `R39a` (`0.00–2.36 s`), `frame0.jpg`, `cover.jpg`, and `R39_loop` (`23.16–24.48 s`), rendering directly from clean graded 4K NASA SVS 20297 footage (`svs_20297_van_allen_earth_only.mp4` @ `6.4 s`, `upscale=0.95x`).
3. Removed the ghost double-exposed Blue Marble Earth on `R39b` (`2.36–3.32 s`), rendering directly from a single clean moving NASA SVS 3822 geomagnetic field lines plate (`svs_3822_magfield_left.mp4` @ `28.0 s`, full `9:16` reframe `upscale=1.40x`).
4. Eliminated the `9.00–14.00 s` parent-title banner text collision on `R42a` (`9.32–12.68 s`) by rendering a clean text-free moving NASA ISS sunlit orbital pass (`hdev_earth_views_iss_2019.mp4` @ `128.0 s`, `upscale=1.25x`) followed by DSCOVR EPIC (`nasa_svs_12312_dscovr_epic_earth.mp4` @ `16.0 s` on `R42b`).

- **Short 2 `v02` MP4 (NAS & iCloud UAT):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02.mp4` (also mirrored with matching SHA-256 to `10_Shorts/031_short_sat12_solar_wind_air_v02.mp4`, NAS `OWB UAT/031_shorts_v02/031_short_sat12_solar_wind_air_v02.mp4`, and iCloud `OWB UAT/031_shorts_v02/031_short_sat12_solar_wind_air_v02.mp4` — `SHA-256: 4f25b1cd9d2c806367a98f3a7e173bbd0d16dc3390e0c882c223c23af6f10450`)
- **Frame 0 (`1080x1920`):** `.../031_short_sat12_solar_wind_air_v02_frame0.jpg` (`SHA-256: f6b31eba43715fa776345296cbc51a1a6ef454865b3600b377e305535bd1a843`)
- **Custom Cover (`1080x1920`):** `.../031_short_sat12_solar_wind_air_v02_cover.jpg` (`SHA-256: 63c43e387c209af75bea5d73c43b6c1556b8bbcbe7a69d90c31d2fc362d94e1f`)
- **Handoff & Assembler:** `10_Shorts/SHORT2_SOLAR_WIND_AIR_HANDOFF_J2394_v02.md` and `10_Shorts/_assemble_031_short2_v02.py`

```
PASS  031_short_sat12_solar_wind_air_v02.mp4  dur=24.48s  audio=-16.9dB  motion=22.1  f0diff=3.63  cut1=2.36s  vo_onset=0.09s  tail_gap=1.46s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_vo.wav  dhash=bc17cffffe9fccd8  visor=0.0

PASS  031_short_sat12_solar_wind_air_v02_frame0.jpg  saturation=101.5  near_black=0%
PASS  031_short_sat12_solar_wind_air_v02_cover.jpg  saturation=111.2  near_black=0%

SFX level PASS: VO -16.5 LUFS, SFX -38.5 LUFS, 5 hits
music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM
polish gate PASS: 0 of 9 rows failed, 1 to look at
picture QA PASS: 0 of 9 cuts fail, 1 to look at
```


## J2395 Review of Shorts 1 & 2 (`J2388` + `J2394` `v02`) & UAT Handoff — 8 November 2026

Reviewed `031` Active Short #1 (`J2388`, `031_short_testA_opening_flip_v01.mp4`) and repaired Active Short #2 `v02` (`J2394`, `031_short_sat12_solar_wind_air_v02.mp4`) alongside Long Master `v02` (`J2390` **KEEP**, `SHA-256: 680598ae3420afa9fd40efc954cf06cefcfff234044a62e90af6a143fdf4de43`):
- **Short 1 (`J2388`):** **KEEP** (`SHA-256: ebe11bb730ccfab8681d564d3588d17011a28629c7b6f926eba952bfc98c4bcd`, `33.00 s` @ `25 fps` CFR; all 7 gates `PASS`; 13-shot contact sheet verified clean).
- **Short 2 `v02` (`J2394`):** **KEEP** (`SHA-256: 4f25b1cd9d2c806367a98f3a7e173bbd0d16dc3390e0c882c223c23af6f10450`, `24.48 s` @ `25 fps` CFR; all 7 gates `PASS`; 9-shot contact sheet verified clean of all 4 `J2390` items; `v01` preserved untouched on NAS).
- **UAT & R2 Watch Streams:** Built 720p proxy `031_what_happens_when_earths_magnetic_field_flips_master_v02_PHONE.mp4` (`SHA-256: a8c748f68cf2215f224f0d616b145ec45ffe04db4b0bfd305a9541bbc9931c9d`), verified SHA-256 across NAS `studio-live`, NAS `OWB UAT`, and iCloud `OWB UAT`, uploaded Long `v02` (`owb-031-v02`) and Shorts 1 (`owb-j2395-2-v01`) & 2 `v02` (`owb-j2395-3-v02`) to R2, set `jobs.py awaits J2395` for Ben's final watch (`Wed 02 Dec 2026 18:00` London), and advanced `jobs/WIP.json` (`OWB:031` -> UAT; `OWB:J01` enters `active`). Full review: `jobs/reviews/J2395/REVIEW.md`.

