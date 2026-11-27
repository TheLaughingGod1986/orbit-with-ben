# OWB `032` Short #2 (`dry_desert_two_oceans`) Correction & Gate Report — `J3856` (`v02`)

- **Job:** `J3856` (Chief FIX follow-up to `J3853` / `jobs/reviews/J3853/REVIEW.md`, commit `d0e3eaaa54`, PR `#1366`)
- **Parent Long (`032`):** *What Would Happen If You Landed on Titan? (Seas of Liquid Gas)* (`T3cBBss1F60`, live since `2026-11-25T18:00:24Z`, listing title verified in `05_Analytics/owb/snapshots/2026-11-27.json`; approved master `v02` `sha256: 519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073`)
- **Short Slug / Stem:** `dry_desert_two_oceans` / `032_short_dry_desert_two_oceans_v02`
- **Short Title:** *Is Titan Just a Dry Desert?* (Alt: *Does Saturn's Moon Titan Hide Two Oceans?*)
- **Gate Check Date:** `2026-12-26` (**non-colliding gate-check date ONLY — NOT an approved schedule slot; zero upload or scheduling**)
- **Spend:** `£0.00` (existing locked `titan_landing_vo_v02b.wav`, existing `J2089`/`J2378` picture harvest, existing `titan_score_bed_v01.mp3`, synthesized house SFX `kit_v01` only)
- **Preserved Versions:** `032_short_dry_desert_two_oceans_v01.mp4` (`sha256: 07ef33e02198e039d5e2ffefecaf32583037204aad9816e3a497ba3cf4825758`) preserved untouched beside `v02`; `J3853` remains held; zero changes to existing Shorts, Buffer posts, slots, or `UPLOADS.json`.

---

## 1. Point-by-Point Resolution of `jobs/reviews/J3853/REVIEW.md`

1. **Moving bridge (`1.900–8.500 s`):**
   - Replaced `v01` static orb zooms (`S02`, `S03`, `video=False`) with real 1080p60 moving NASA SVS 20311 Titan footage (`video=True`, `upscale=1.78x`):
     - `S02_dunes` (`1.900–4.733 s`): `SVS20311_DF_End_Pan_1080.mp4` (`offset=0.100 s`, `x0=1180..1312` pure towering golden dunes + pebbles, zero clipped spacecraft edge, genuine source motion `diff=7.2..9.6`).
     - `S03_radar_sweep` (`4.733–8.500 s`): `SVS20311_DF_Open_1080.mp4` (`offset=12.000 s`, `x0=500..820`, active scanning beam + sweeping terrain pan, genuine source motion `diff=3.45..20.55`, `>10 s` separation from `S01` `offset=1.800 s`).
   - Preserves `Cut 1 = 1.900 s <= 2.80 s`, `Cut 2 = 4.733 s <= 4.80 s`, `max shot = 3.767 s <= 4.00 s`.
   - **Bounded asset search & Chief S03 fallback options:** Across `032/03_Reference-Material/harvest_J2089_v01/`, `032/04_Generated-Clips/`, `032/07_Edit-Project/`, `021`, `027`, `033`, `034`, `064`, `J01`, `_sleep_video_01`, `_desk/cache/J2089/additional_v01/` (marked `CANDIDATE_NOT_KEEP` / `PENDING_ASSET_SPECIFIC_TERMS`), and `mac-mini-archive` (`021` `veo_cassini_ring_rain_v03.mp4` is 720p Saturn ring rain, exceeding 2.35× for 1920 px), **zero approved moving Cassini-orbiter / North-Pole-radar video exists**. To honour `OWB-2026-11-E1` without waiving it, `S03` uses approved moving `SVS20311_DF_Open_1080.mp4` (`offset=12.00 s`). If Chief prefers a Cassini-specific visual for `S03`, concrete fallback options for Chief ruling are:
     - **(A)** Approve harvesting & KEEP-clearing an official NASA/JPL public-domain Cassini Titan North Pole radar flyover movie (`£0`);
     - **(B)** Issue an explicit per-cut Chief E1 waiver for a Cassini still plate on `S03` while `S01`–`S02` remain moving; or
     - **(C)** Authorise a Flow Veo clip of Cassini orbiting Titan.
2. **Teaching accuracy & payoff timing (`S08`, `20.400–24.000 s`):**
   - Removed Apollo 17 Earth (`AS17-148-22727`), removed unsourced `0.72`/`0.96` bars, and removed the extra early `"2 OCEANS: GAS + WATER"` pill.
   - Built ONE Titan-specific animated depth cutaway (`code_graphic_032_s2_titan_ocean_depth_9x16_v02.mp4`) using real Cassini ISS Titan (`PIA14602.jpg`, approved `ocean_graphic.py` disc crop) strictly inside the `16:9` safe band (`y = 656..1264`), with labels `<= 3` words from spoken `S52` and `SOURCES.md` Row 13 (`"an ocean 35 to 50 miles (55 to 80 kilometers) below the icy ground"`):
     - `20.40–21.00 s`: `TITAN` + `ICY CRUST` + animated depth bracket `55–80 KM BELOW` + lower zoom connector hugging crust bottom (verified zero spoiler at `20.8 s`).
     - `21.000 s` (`78.1% >= 70%`, exact spoken onset of `"second"`): open-bottomed cyan subsurface layer sweeps in + `HIDDEN OCEAN` reveals (no invented ocean floor; footer `NOT TO SCALE`).
     - `22.700 s` (synced to `"of liquid water"`): `LIQUID WATER` reveals cleanly inside the subsurface layer.
3. **Full-frame `S04` composition (`8.500–12.067 s`):**
   - Replaced `v01`'s floating diagonal starfield edge on `PIA21434.jpg` with a verified interior `9:16` crop strictly inside the illuminated northern seas (`crop_box=(460, 150, 949, 1020)`, `z1=1.02`, `border_min=49.0`, `upscale=2.25x <= 2.35x`, zero diagonal border, zero starfield fill, zero radar scanline seams; `PIA17031.jpg` was tested first and rejected because its Cassini radar scanlines tripped `polish_gate` horizontal-seam FAIL).
4. **Reproducible evidence & NAS verification:**
   - Full `v02` master, stems, sidecars, captions, `cuts.json`, `pool.json`, `meta.json`, `summary.json`, 7 full-size (`1080×1920`) corrected-shot/graphic stills, 10-shot contact sheet, opening sheet, cover, and all gate outputs verified by SHA-256 on NAS beside preserved `v01`.

---

## 2. Verified Source & Output SHA-256 Manifest (NAS `studio-live`)

Pack directory: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/dry_desert_two_oceans/06_Final-Exports/` (key artifacts also mirrored to `10_Shorts/`).

| Artifact | File | SHA-256 |
|---|---|---|
| **Short Master (`v02`)** | `032_short_dry_desert_two_oceans_v02.mp4` (`1080×1920`, `30/1` CFR, `26.900 s`, `807` frames) | `34c800a4a9bf034cbc9f498903621998d407355f845e8c5f437d71246025c906` |
| **Preserved `v01` Master (untouched)** | `032_short_dry_desert_two_oceans_v01.mp4` | `07ef33e02198e039d5e2ffefecaf32583037204aad9816e3a497ba3cf4825758` |
| **Frame-0 Still** | `032_short_dry_desert_two_oceans_v02_frame0.jpg` | `c85567b679af81bee72d16be8970e1744974f8c3b307a7f52bbf74d9a3191900` |
| **Custom Short Cover** | `032_short_dry_desert_two_oceans_v02_cover.jpg` | `8acb817fa135a0c3a37b6205458674b9c4da49093a859ca6f1d08e4b162c1127` |
| **Gate Opening Sheet** | `032_short_dry_desert_two_oceans_v02_open_sheet.jpg` | `14e84527af32be22ba968e7662124033d6497f6934f84e427532f04fd244325e` |
| **10-Shot Review Sheet** | `032_short_dry_desert_two_oceans_v02_review_10shots.jpg` | `11e3a219ab56caf845e2671fc38842b98dc899dc9694b4d8ff2de02220bad74c` |
| **Full-size Still `S02` (`3.3 s`)** | `032_short_dry_desert_two_oceans_v02_still_S02_dunes_3.3s.jpg` | `8b9782ec157f2e4751f3e8f81212c4de62fc6ddedce9f97cc8b7e6431ed28099` |
| **Full-size Still `S03` (`6.6 s`)** | `032_short_dry_desert_two_oceans_v02_still_S03_radar_sweep_6.6s.jpg` | `4601128f1a51e4e6582d8045b1b9768f9362521a31952081522d0c195fcb3f63` |
| **Full-size Still `S04` (`10.3 s`)** | `032_short_dry_desert_two_oceans_v02_still_S04_coastline_10.3s.jpg` | `80f32980718c3c802111015d4c5484e69f08a15e2be44a41a38cc35a48c90455` |
| **Full-size Still `S07` (`18.6 s`)** | `032_short_dry_desert_two_oceans_v02_still_S07_cassini_gravity_18.6s.jpg` | `24d80ccfb82c21e1a72f53c27f10c87c0c040d613c79b5e8ee4de6b24f7bfb0d` |
| **Full-size Still `S08` (`20.8 s` pre-payoff)** | `032_short_dry_desert_two_oceans_v02_still_S08_graphic_20.8s_pre_payoff.jpg` | `6049601859b55d6c557e903f054ab2bc6904aba6c8a203642bd49f750020a884` |
| **Full-size Still `S08` (`21.8 s` payoff)** | `032_short_dry_desert_two_oceans_v02_still_S08_graphic_21.8s_payoff.jpg` | `54da3608ab4d99b22b84d8cacedd3bd54c16d4fc3725b97124ebffe406b61a5c` |
| **Full-size Still `S08` (`23.4 s` liquid water)** | `032_short_dry_desert_two_oceans_v02_still_S08_graphic_23.4s_liquid_water.jpg` | `1891701ec2cbb3d8b2f733382e96a137423905d2f2561e16d9f77c171a1662e4` |
| **Input: Approved Long `v02`** | `../../09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` | `519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073` |
| **Input: Locked VO `v02b`** | `../../02_Voiceover/titan_landing_vo_v02b.wav` | `55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5` |
| **Input: Score Bed `v01`** | `../../05_Music/titan_score_bed_v01.mp3` | `02c7d95865f8b39de4f9d3dfda8aa85084ecea04fc56dbd6776268279dab8f9e` |

Full per-asset source SHA-256 provenance (`SVS20311_DF_Open_1080.mp4`, `SVS20311_DF_End_Pan_1080.mp4`, `SVS20311_Dragonfly_Drill_1080.mp4`, `PIA21434.jpg`, `PIA20021_right_panel_1440x1144.jpg`, `PIA14922.jpg`, `PIA14602.jpg`, `weic2310a.png`) is recorded in `032_short_dry_desert_two_oceans_v02_meta.json` and `_summary.json`. Zero barred `RLSJm59OSzI` assets (`PIA14925`, `PIA06230`, `PIA09739`, `PIA21625`).

---

## 3. All 7 Gates (`7/7 PASS`) + Canonical MP3 Music Check & Warning Review

| Gate | Verdict | Key Readout & Warning Review |
|---|---|---|
| **1. `gate_shorts_open.py` (NAS copy)** | **PASS (`rc=0`)** | `dur=26.9s`, `motion=25.65`, `f0diff=9.67`, `cut1=1.9s`, `vo_onset=0.06s`, `tail_gap=0.66s`, `dhash=00f0e91745418580`, `visor=0.0`, **`0/27` & `0/54` padded frames (`padded stretches: none`)**. Advisory warn `26.90s outside 16.0–19.0s band` reviewed: J3853/J3856 permits `22–27 s` lift. |
| **2. `thumb_preview.py` (Frame 0)** | **PASS (`rc=0`)** | `saturation=137.6`, `near_black=1%` |
| **3. `thumb_preview.py` (Cover)** | **PASS (`rc=0`)** | `saturation=170.9`, `near_black=2%` (`TITAN'S / 2 OCEANS?`, `126 px`, zero Orbit) |
| **4. `sfx_kit.py level`** | **PASS (`rc=0`)** | `VO -16.8 LUFS`, `SFX -44.0 LUFS`, `Bed -34.9 LUFS`, `AAC -14.1 LUFS / -2.2 dBTP`, `9` detected hits |
| **5. `music_gate.py`** | **PASS (`rc=0`)** | `titan_score_bed_v01.mp3`, `585.4 s`, `70.6 BPM` (`Pace: 68-78 BPM`). Default check logged 13 unreadable historical-file warnings; supplemental canonical uniqueness check (`_music_gate_canonical_mp3.txt`) against all **13 readable canonical NAS OWB `.mp3` beds** (`023, 024, 026, 027, 028, 029, 030, 031, 033, 034, 064`) returned **PASS (`rc=0`, 0 warnings)**. |
| **6. `polish_gate.py`** | **PASS (`rc=0`)** | **`0 of 10` rows failed.** 1 WARN on `S02_dunes` (`edge density 0.0172 < film p5 0.0207`) visually inspected at full size (`S02_dunes_3.3s.jpg`): smooth golden haze sky over crisp dune ridge and pebbled foreground, clean full-bleed motion. |
| **7. `picture_qa.py`** | **PASS (`rc=0`)** | **`0 of 10` cuts fail.** 2 WARNs visually inspected at full size: `S02_dunes` low-detail (above) and `S04_coastline` `upscaled 2.25x <= 2.35x` (`S04_coastline_10.3s.jpg`): clean interior northern-seas texture behind title banner, zero border/seam artifacts. |

---

## 4. `OWB-2026-11-E1` Measurements & Loop Record

- **Spoken script (verbatim `S44+S45+S46+S52`, `65` words, `0` words split across cuts):** *"Is Titan just a dry desert? Wrong. The equator may be lined with dunes, but when Cassini swept its radar across Titan's North Pole, it uncovered a drowned coastline of bays and islands filled with liquid natural gas. And far beneath Titan's icy crust, tens of kilometers down, Cassini's gravity measurements revealed a second hidden ocean of liquid water likely mixed with salts and ammonia."*
- **VO onset:** `0.060 s` (`<= 0.15 s`) | **Surprise:** `"dry"` starts `1.000 s`, `"desert?"` ends `1.840 s`, `"Wrong."` starts `1.990 s`
- **Cut 1:** `1.900 s <= 2.80 s` | **Cut 2:** `4.733 s <= 4.80 s` | **All cuts (s):** `1.900, 4.733, 8.500, 12.067, 14.200, 16.767, 20.400, 24.000, 26.267` | **Max shot:** `3.767 s <= 4.00 s`
- **Inter-sentence breaths:** `S44->S45 = 0.150 s`, `S45->S46 = 0.150 s`, `S46->S52 = 0.160 s` (all `< 0.25 s`)
- **Spoken & visual payoff agreement:** `"second"` starts **`21.000 s` (`78.1% >= 70.0%`)**; visual `HIDDEN OCEAN` reveal starts **`21.000 s` (`78.1%`)**; `LIQUID WATER` reveals at **`22.700 s`**; zero early spoiler pill.
- **Last word / loop:** `"ammonia."` ends `26.240 s`; loop point `26.900 s`; **tail gap = `0.660 s < 1.20 s`**; seamless pre-roll return (`S10_loop`) into frame 0; zero end card / zero CTA.
- **Written last-line-to-first-line loop connection:** *"...likely mixed with salts and ammonia." -> "Is Titan just a dry desert?"*
