# OWB `032` Short #2 (`dry_desert_two_oceans`) Correction & Gate Report — `J3865` (`v03`)

- **Job:** `J3865` (Chief FIX follow-up to `J3856` / `J3853` — `jobs/reviews/J3856/REVIEW.md` on `codex/J3856-review`, PR `#1366`)
- **Parent Long (`032`):** *What Would Happen If You Landed on Titan? (Seas of Liquid Gas)* (`T3cBBss1F60`, live since `2026-11-25T18:00:24Z`, listing title verified in `05_Analytics/owb/snapshots/2026-11-27.json`; approved master `v02` `sha256: 519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073`)
- **Short Slug / Stem:** `dry_desert_two_oceans` / `032_short_dry_desert_two_oceans_v03`
- **Short Title:** *Is Titan Just a Dry Desert?* (Alt: *Does Saturn's Moon Titan Hide Two Oceans?*)
- **Gate Check Date:** `2026-12-26` (**non-colliding gate-check date ONLY — NOT an approved schedule slot; zero upload or scheduling**)
- **Spend:** `£0.00` (existing locked `titan_landing_vo_v02b.wav`, existing `J2089`/`J2378` picture harvest + new £0 NASA GSFC Public Domain SVS 12709 clip, existing `titan_score_bed_v01.mp3`, synthesized house SFX `kit_v01` only; zero generation, zero VO changes, zero E1 waiver)
- **Preserved Versions & Hold State:** Both `v01` (`sha256: 07ef33e02198e039d5e2ffefecaf32583037204aad9816e3a497ba3cf4825758`) and `v02` (`sha256: 34c800a4a9bf034cbc9f498903621998d407355f845e8c5f437d71246025c906`) are preserved untouched beside `v03` on NAS. `J3853` and `J3856` remain held. Zero changes to existing Shorts, Buffer posts, slots, or `UPLOADS.json`.

---

## 1. Point-by-Point Resolution of `jobs/reviews/J3856/REVIEW.md`

1. **`S03` Cassini replacement (`4.733–8.500 s`) — Bounded External Official NASA/JPL/Cassini Search (Option A):**
   - Executed a bounded external search of official NASA/JPL/Cassini catalogs (NASA JPL Photojournal / `science.nasa.gov`, NASA Image and Video Library API `images-api.nasa.gov`, NASA Goddard SVS API `svs.gsfc.nasa.gov`) within Chief's cap (**9 active minutes <= 20 min**, **2 of 3 deep candidates examined**, zero local-cache repeat, zero spend, zero generation, zero E1 waiver):
     - **Candidate 1 — REJECTED:** `PIA17656` (*Flying over an Extraterrestrial Land of Lakes — Cassini Radar North Polar Flyover*, NASA/JPL-Caltech/ASI/USGS, Public Domain, `PIA17656_Unannotated-ProRes.mov`, `63.66 s`). Native height is `1280x720`, requiring `1920/720 = 2.67x` upscale for full-bleed `1080x1920`, exceeding the `2.35x` `picture_qa` hard ceiling. (Also verified via XMP:Ingredients that SVS 12709's `288.27–296.80 s` flyover embeds this same 720p `PIA17656` file.)
     - **Candidate 2 — ACCEPTED:** `GSFC_20170912_Cassini_m12709_CIRS_Short` (NASA SVS 12709, `https://svs.gsfc.nasa.gov/12709`, XMP ingredient `Cassini_Saturn_Animation_Reel.mov` at `259.43–263.93 s`, extracted clean window `259.967–263.900 s`, used in `S03` at `offset=0.033 s` -> source `260.000–263.767 s`). Native `1920x1080`, `30/1` fps, `1.78x <= 2.35x` full-bleed upscale. Credit: `NASA/Goddard Space Flight Center/JPL-Caltech`. Rights: U.S. Government / NASA GSFC Public Domain visual asset; original third-party Killer Tracks music stripped via `-an` (silent video only).
     - **Saved archival asset & provenance on NAS:** `03_Reference-Material/harvest_J3865_v01/SVS12709_Cassini_Titan_Flyby_260_264_1080.mp4` (`sha256: 96749f161f522658833e9fff4f61d17170eb99d11c1fc7a82885bddaee982fa9`) + `SVS12709_PROVENANCE.json`.
     - **Native motion evidence (fixed crop across 113 frames):** `min=3.60`, `median=5.84`, `max=6.97` (strong continuous native motion on every frame).
     - **Full-size visual inspection (`5.2 s`, `6.6 s`, `8.1 s` stills):** Shows the actual **Cassini orbiter** (large silver/white high-gain radar dish, magnetometer/RTG booms, golden thermal foil) flying smoothly across Titan's illuminated golden hazy globe — zero Dragonfly hardware, zero text/watermarks, zero fade frames, crisp full-bleed `9:16`. (Note for transparency: this depicts Cassini flying over Titan's globe during *"when Cassini swept its radar across Titan's North Pole"*, immediately cutting at `8.500 s` into the actual Cassini north-polar sea imagery `PIA21434` / `PIA20021` on `S04`–`S05`.)
2. **`S08` Simplified, Readable, Locked-Spoken-Word Teaching Graphic (`20.400–24.000 s`):**
   - Completely removed unspoken `55–80 KM BELOW` range and right-side depth bracket.
   - Built ONE simplified Titan-specific animated graphic (`code_graphic_032_s2_titan_ocean_depth_9x16_v03.mp4`) using real Cassini ISS Titan (`PIA14602.jpg`, approved disc crop) strictly inside the `16:9` centre safe band (`y = 656..1264`), with **every main teaching label rendered at `68 px` Arial Black (`11.18%` of `608 px` safe-band height, strictly within `67–73 px` / `11–12%`)** and timed directly from `words.json`:
     - `20.400–21.000 s` (verified at `20.8 s` full-size & phone preview): real Cassini Titan + `TITAN` (`68 px`) + curved `ICY CRUST` (`68 px`) only — **zero early ocean payoff**.
     - `21.000 s` (`78.1% >= 70.0%`, exact spoken start of `"second"`): open-bottomed cyan subsurface layer sweeps in smoothly (soft alpha fade at bottom, no ocean floor / no invented proportions).
     - `21.520 s` (exact spoken start of `"hidden"` in `"hidden ocean"`, `21.52–22.32 s`; verified at `22.0 s`): `HIDDEN OCEAN` (`68 px` yellow) reveals on one bold line.
     - `22.960 s` (exact spoken start of `"liquid"` in `"liquid water"`, `22.96–23.76 s`; verified at `23.4 s`): `LIQUID WATER` (`68 px` white) reveals on one bold line.
     - Subordinate qualitative disclaimer `NOT TO SCALE` (`26 px`, `y = 1214..1239`, clearly above captions and inside `y <= 1264`).
   - Verified legibility at full size (`1080x1920`) and on `032_short_dry_desert_two_oceans_v03_phone_graphic_preview.jpg` (`360x640` and `240x427` compact phone scales).
3. **`S04` Clean Full-Frame Reframing Preserved (`8.500–12.067 s`):**
   - Preserved exact `v02` interior `9:16` crop of `PIA21434.jpg`: `crop_box=(460, 150, 949, 1020)`, `z1=1.02`, `upscale=2.25x <= 2.35x`.
   - Visually inspected full-size (`S04_coastline_10.3s.jpg`): clean full-bleed northern-seas frame with zero diagonal black border, zero starfield fill, and zero radar scanlines; naturally soft Cassini VIMS near-infrared texture sits cleanly behind the crisp centered parent title.

---

## 2. Verified Source & Output SHA-256 Manifest (NAS `studio-live`)

Pack directory: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/dry_desert_two_oceans/06_Final-Exports/` (key review files mirrored identically in `10_Shorts/`).

| Artifact | File | SHA-256 |
|---|---|---|
| **Short Master (`v03`)** | `032_short_dry_desert_two_oceans_v03.mp4` (`1080×1920`, `30/1` CFR, `26.900 s`, `807` frames) | `5b5703855c18a7fea0a8e502ba394ca7af0bb6abeda9f66f6e46229b0bacfe13` |
| **Preserved `v01` Master (untouched)** | `032_short_dry_desert_two_oceans_v01.mp4` | `07ef33e02198e039d5e2ffefecaf32583037204aad9816e3a497ba3cf4825758` |
| **Preserved `v02` Master (untouched)** | `032_short_dry_desert_two_oceans_v02.mp4` | `34c800a4a9bf034cbc9f498903621998d407355f845e8c5f437d71246025c906` |
| **Frame-0 Still** | `032_short_dry_desert_two_oceans_v03_frame0.jpg` | `c85567b679af81bee72d16be8970e1744974f8c3b307a7f52bbf74d9a3191900` |
| **Custom Short Cover** | `032_short_dry_desert_two_oceans_v03_cover.jpg` | `8acb817fa135a0c3a37b6205458674b9c4da49093a859ca6f1d08e4b162c1127` |
| **Gate Opening Sheet** | `032_short_dry_desert_two_oceans_v03_open_sheet.jpg` | `9c8727227b6807692b0d02fc5881af606ff3f9305f0ede9a634aba90416c9d49` |
| **10-Shot Review Sheet** | `032_short_dry_desert_two_oceans_v03_review_10shots.jpg` | `ff702dc22f0bad547b926a01b6d86676c372216f65299d15e879a30265661e33` |
| **Phone Graphic Preview (`360×640` & `240×427`)** | `032_short_dry_desert_two_oceans_v03_phone_graphic_preview.jpg` | `c94d41ae36b347dcbd02c37b192d87f85c923e6ac11b74273bd2a3a04e93def2` |
| **Full-size Still `S02` (`3.3 s`)** | `032_short_dry_desert_two_oceans_v03_still_S02_dunes_3.3s.jpg` | `8b9782ec157f2e4751f3e8f81212c4de62fc6ddedce9f97cc8b7e6431ed28099` |
| **Full-size Still `S03` (`5.2 s`)** | `032_short_dry_desert_two_oceans_v03_still_S03_cassini_titan_5.2s.jpg` | `d29d77c4a0ae6e4a27fd741baa420c2e70ac9af83aac2ed2000a734d93b9f0a3` |
| **Full-size Still `S03` (`6.6 s`)** | `032_short_dry_desert_two_oceans_v03_still_S03_cassini_titan_6.6s.jpg` | `c841df5404d6c48509c2d082ea6cf6fb275263dd1f5cde1ab7d12b3b48e04e64` |
| **Full-size Still `S03` (`8.1 s`)** | `032_short_dry_desert_two_oceans_v03_still_S03_cassini_titan_8.1s.jpg` | `9e22911655aacdfb5065186fabd6e17c0fde13d45a2ce50a859af7cbde7bd0a9` |
| **Full-size Still `S04` (`10.3 s`)** | `032_short_dry_desert_two_oceans_v03_still_S04_coastline_10.3s.jpg` | `902bb422aeb21246129ec650627334fe59fafd0cf09820ed7acf6adc5f89d81c` |
| **Full-size Still `S07` (`18.6 s`)** | `032_short_dry_desert_two_oceans_v03_still_S07_cassini_gravity_18.6s.jpg` | `24d80ccfb82c21e1a72f53c27f10c87c0c040d613c79b5e8ee4de6b24f7bfb0d` |
| **Full-size Still `S08` (`20.8 s` pre-payoff)** | `032_short_dry_desert_two_oceans_v03_still_S08_graphic_20.8s_pre_payoff.jpg` | `c8d6d39e509be606cfa744cf2682cf15c655083340dc414c364d13efac75e116` |
| **Full-size Still `S08` (`22.0 s` hidden ocean)** | `032_short_dry_desert_two_oceans_v03_still_S08_graphic_22.0s_hidden_ocean.jpg` | `f4efd8d631599d3bc3dbb28c13e8374ac83fa1f1d34e72299027424ce299e920` |
| **Full-size Still `S08` (`23.4 s` liquid water)** | `032_short_dry_desert_two_oceans_v03_still_S08_graphic_23.4s_liquid_water.jpg` | `50a5b3fdd8dcf822f4d7d02a25b2b8f0d3cac86202b6e2baa86a5b432e155117` |
| **New `S03` Source Clip (NAS)** | `../../../03_Reference-Material/harvest_J3865_v01/SVS12709_Cassini_Titan_Flyby_260_264_1080.mp4` | `96749f161f522658833e9fff4f61d17170eb99d11c1fc7a82885bddaee982fa9` |
| **Input: Approved Long `v02`** | `../../../09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` | `519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073` |
| **Input: Locked VO `v02b`** | `../../../02_Voiceover/titan_landing_vo_v02b.wav` | `55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5` |
| **Input: Score Bed `v01`** | `../../../05_Music/titan_score_bed_v01.mp3` | `02c7d95865f8b39de4f9d3dfda8aa85084ecea04fc56dbd6776268279dab8f9e` |

Full per-asset source provenance and SHA-256 checksums for all inputs are recorded in `032_short_dry_desert_two_oceans_v03_meta.json`, `_summary.json`, and `harvest_J3865_v01/SVS12709_PROVENANCE.json`. Zero barred `RLSJm59OSzI` assets (`PIA14925`, `PIA06230`, `PIA09739`, `PIA21625`).

---

## 3. All 7 Fresh Gates (`7/7 PASS`) + Canonical MP3 Music Check & Warning Review

| Gate | Verdict | Key Readout & Explicit Warning Review |
|---|---|---|
| **1. `gate_shorts_open.py` (NAS copy)** | **PASS (`rc=0`)** | `dur=26.9s`, `audio=-16.8dB`, `motion=25.65`, `f0diff=9.67`, `cut1=1.9s`, `vo_onset=0.06s`, `tail_gap=0.66s`, `dhash=00f0e91745418580`, `visor=0.0`, `full-bleed 0.00/0.25/0.50s fills the frame`. **2 advisory warnings reviewed:** (a) `duration 26.90s outside 16.0–19.0s band` — permitted by the J3853/J3856/J3865 brief (`22–27 s` lift); (b) `7/54 sampled frames: 5-8s (blur-pad, no edge)` — visually inspected full-size at `5.2 s`, `6.6 s`, and `8.1 s`: **genuine full-bleed `9:16`** (`1.78x` vertical fill crop from native `1920x1080`). The Cassini orbiter sits sharply in the middle while Titan's smooth golden atmospheric haze and dark space limb fill top/bottom with zero straight edges and zero blurred-copy padding. |
| **2. `thumb_preview.py` (Frame 0)** | **PASS (`rc=0`)** | `saturation=137.6`, `near_black=1%` |
| **3. `thumb_preview.py` (Cover)** | **PASS (`rc=0`)** | `saturation=170.9`, `near_black=2%` (`TITAN'S / 2 OCEANS?`, `126 px`, zero Orbit) |
| **4. `sfx_kit.py level`** | **PASS (`rc=0`)** | `VO -16.8 LUFS`, `SFX -44.2 LUFS`, `Bed -34.9 LUFS`, `AAC -14.1 LUFS / -2.2 dBTP`, `10` detected hits |
| **5. `music_gate.py`** | **PASS (`rc=0`)** | `titan_score_bed_v01.mp3`, `585.4 s`, `70.6 BPM` (`Pace: 68-78 BPM`). Default check logged 13 unreadable historical-file warnings; supplemental canonical uniqueness check (`_music_gate_canonical_mp3.txt`) against all **13 readable canonical NAS OWB `.mp3` beds** returned **PASS (`rc=0`, 0 warnings)**. |
| **6. `polish_gate.py` (NAS copy)** | **PASS (`rc=0`)** | **`0 of 10` rows failed.** 1 WARN on `S02_dunes` (`edge density 0.0172 < film p5 0.0207`) visually inspected at full size (`S02_dunes_3.3s.jpg`): smooth golden haze sky over crisp dune ridge and pebbled foreground, clean full-bleed motion. |
| **7. `picture_qa.py` (NAS copy)** | **PASS (`rc=0`)** | **`0 of 10` cuts fail.** 3 WARNs visually inspected at full size (`picture_qa_review.jpg` + individual stills): (a) `S02_dunes` low-detail (above); (b) `S03_cassini_titan_flyby` `(animation)` — verified crisp official NASA GSFC/JPL 1080p Cassini orbiter flying over Titan at `5.2/6.6/8.1 s`, zero text/Dragonfly/artifacts; (c) `S04_coastline` `upscaled 2.25x <= 2.35x` — verified clean interior northern-seas frame at `10.3 s` behind crisp parent title, zero border/seam artifacts. |

---

## 4. `OWB-2026-11-E1` Measurements & Loop Record

- **Spoken script (verbatim `S44+S45+S46+S52`, `65` words, `0` words split across cuts):** *"Is Titan just a dry desert? Wrong. The equator may be lined with dunes, but when Cassini swept its radar across Titan's North Pole, it uncovered a drowned coastline of bays and islands filled with liquid natural gas. And far beneath Titan's icy crust, tens of kilometers down, Cassini's gravity measurements revealed a second hidden ocean of liquid water likely mixed with salts and ammonia."*
- **VO onset:** `0.060 s` (`<= 0.15 s`) | **Surprise:** `"dry"` starts `1.000 s`, `"desert?"` ends `1.840 s`, `"Wrong."` starts `1.990 s`
- **Cut 1:** `1.900 s <= 2.80 s` | **Cut 2:** `4.733 s <= 4.80 s` | **All cuts (s):** `1.900, 4.733, 8.500, 12.067, 14.200, 16.767, 20.400, 24.000, 26.267` | **Max shot:** `3.767 s <= 4.00 s`
- **Moving bridge (`1.900–8.500 s`):** 100% `video=True` (`S02` SVS 20311 End Pan + `S03` SVS 12709 Cassini/Titan Flyby, both `1.78x` full-bleed `1080p`).
- **Inter-sentence breaths:** `S44->S45 = 0.150 s`, `S45->S46 = 0.150 s`, `S46->S52 = 0.160 s` (all `< 0.25 s`)
- **Spoken & visual payoff agreement (`words.json`):** `"second"` starts **`21.000 s` (`78.1% >= 70.0%`)** (ocean sweep starts `21.000 s`); `"hidden"` starts **`21.520 s`** (`HIDDEN OCEAN` reveals `21.520 s`); `"liquid"` starts **`22.960 s`** (`LIQUID WATER` reveals `22.960 s`); zero early spoiler pill.
- **Last word / loop:** `"ammonia."` ends `26.240 s`; loop point `26.900 s`; **tail gap = `0.660 s < 1.20 s`**; seamless pre-roll return (`S10_loop`) into frame 0; zero end card / zero CTA.
- **Written last-line-to-first-line loop connection:** *"...likely mixed with salts and ammonia." -> "Is Titan just a dry desert?"*
