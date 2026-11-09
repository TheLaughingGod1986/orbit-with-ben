# J2367 — OWB 034 Pluto Shot-List Repair (Addressing J2362 Chief FIX on PR #626)

- **Job:** `J2367` (`034 Pluto: repair chapter-card hold, moving separators and Orbit-row retype from J2362`)
- **Worker:** `gemini` (Gemini 4 Argon, specialist worker covering `J2367`; not Chief — no stage PASS, merge, or spend approval claimed; dependent Chief re-review owns merge, `034 shots` done, and harvest/graphics release)
- **Date:** 7 November 2026
- **Branch / PR:** `j2353-pluto-shot-list` (PR #626, repaired on top of `d89fa79b30477b07d21e868f876cd52056b83fd6`)
- **Untouched Locks:** Locked `v03` script (`01_Script/pluto_frozen_heart_script_master_v03.md`), `J2352` full VO PASS (`02_Voiceover/pluto_frozen_heart_vo_v03.wav`, SHA-256 `2be8030b6c42b673…`), raw Scribe word file (`02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_raw.json`, SHA-256 `af85f3b6fbcb4c0f…`), and the separate `J2360` Short 2 plan are all untouched.
- **Spend:** **£0 / 0 credits** (zero-spend repair only; no generation, assembly, or upload performed; `J2319`/`J2320` holds and all media gates remain in force).

---

## 1. Chapter-Card Hold (`2.50 s` Total / `1.70 s` Fully Legible Hold `>= 1.50 s` Across All `6` `source=CARD` Rows)

- Added a timeline pause at each of the `6` `source=CARD` rows (`R08`, `R20`, `R33`, `R45`, `R54`, `R64`) where picture and music continue while the unedited VO audio is offset downstream.
- Every chapter card now has an exact **`0.60 s` breath** (`0.50–0.80 s` rule) after the preceding sentence's final word end, **`0.40 s` crossfade in**, **`1.70 s` fully legible hold** (`>= 1.50 s`, matching `021` `v03d–v03i` precedent `1.5–4.5 s`), and **`0.40 s` crossfade out** before the next spoken word (`2.50 s` total card row duration).
- Committed the derived offset words file `02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_timeline_offset_v01.json` (SHA-256 `922e5ba1c79c41b812361ba7456bb9d3ed2563cd3e382b10ba9c64f18440114c`) without modifying `stt_raw.json` (`af85f3b6fbcb4c0f…`).
- Retimed all downstream rows (`R09`–`R74`), overlay markers, `05_Music/MUSIC_BRIEF_v01.md`, `06_Sound-Effects/SFX_PLAN_v01.md`, and the `18.00 s` `R74` end hold (`628.94–646.94 s`; `2.50 s` post-word full-level hold `628.820–631.32 s`, `10.00 s` music fade `636.94–646.94 s`, `2.00 s` picture fade `644.94–646.94 s`). New delivery runtime is **`646.94 s`** (`10:46.94`).

| Card Row | Chapter | Card Title | Raw Prev Word End (s) | Raw Next Word Start (s) | Old Span (`J2361`) | Added Pause (s) | Cumulative Offset After (s) | Shifted Prev Word End (s) | Breath (s) | New Card Span `vo_in–vo_out` (s) | Total Dur (s) | Legible Hold (`0.40 s` xfade in/out) | Shifted Next Word Start (s) |
|---|---|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|
| `R08` | Ch 1 | `The Girl Who Named a World` | `65.160` | `66.040` | `65.76–66.04 (0.28 s)` | `+2.22` | **`+2.22`** | `65.160` | **`0.60`** | **`65.76–68.26`** | **`2.50`** | **`1.70 s (66.16–67.86)`** | `68.260` |
| `R20` | Ch 2 | `The Moon That Never Sets` | `158.620` | `159.480` | `159.22–159.48 (0.26 s)` | `+2.24` | **`+4.46`** | `160.840` | **`0.60`** | **`161.44–163.94`** | **`2.50`** | **`1.70 s (161.84–163.54)`** | `163.940` |
| `R33` | Ch 3 | `Nine Years to the Kuiper Belt` | `260.540` | `261.420` | `261.14–261.42 (0.28 s)` | `+2.22` | **`+6.68`** | `265.000` | **`0.60`** | **`265.60–268.10`** | **`2.50`** | **`1.70 s (266.00–267.70)`** | `268.100` |
| `R45` | Ch 4 | `The Glacier That Breathes` | `367.620` | `368.520` | `368.22–368.52 (0.30 s)` | `+2.20` | **`+8.88`** | `374.300` | **`0.60`** | **`374.90–377.40`** | **`2.50`** | **`1.70 s (375.30–377.00)`** | `377.400` |
| `R54` | Ch 5 | `Where Water Is Bedrock` | `451.060` | `451.960` | `451.66–451.96 (0.30 s)` | `+2.20` | **`+11.08`** | `459.940` | **`0.60`** | **`460.54–463.04`** | **`2.50`** | **`1.70 s (460.94–462.64)`** | `463.040` |
| `R64` | Ch 6 | `Beyond the Frozen Heart` | `533.660` | `535.060` | `534.26–535.06 (0.80 s)` | `+1.70` | **`+12.78`** | `544.740` | **`0.60`** | **`545.34–547.84`** | **`2.50`** | **`1.70 s (545.74–547.44)`** | `547.840` |

### Pasted `clip_check.py` Output (`74 rows — PASS` Against `stt_timeline_offset_v01.json`)

```text
$ python3 00_Brand/Channel-Setup/tools/clip_check.py 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/shot_list_v01.csv --words 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_timeline_offset_v01.json --vo-end 628.94
clip_check: 74 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.
```

---

## 2. Real Moving Separators Across All `CODE -> CODE` Gaps & `R05`/`R50` OGV Verification

- **Verification of `File:New Horizons Extreme Close-Up Of Pluto Surface (No Audio).ogv` (`R05`/`R50`):** Downloaded the original `1280x720` file (`sha256: 4ae583a8dccd13e94d1b6755f56ccacaf33e331ce1a0c6e7566b6381fa7504b3`) and inspected extracted frames via `read_file`. Confirmed it is **a synthetic pan across the static `PIA20155` LORRI mosaic strip AND contains baked-in yellow labels (*Washboard terrain*, *Mountainous shoreline*, *Cellular plains*) plus an orange `10 miles` scale bar**. Removed from `R05` and `R50` and added to `banned_and_deduplicated_ids`.
- **Bounded Native-Motion Search (`18` active minutes, logged in `07_Edit-Project/NATIVE_MOTION_SEARCH_LOG_v01.json`):**
  - Replaced `R05` and `R50` with `File:Video - Nasa’s New Horizons - Pluto Flyby 14 7 2015 (51718116305).webm` (`1920x1080` native `1.00x`, `sha256: 993979846dcbf0246a34de47af1bc5e7ed96fd10322e235681af8c8df82269ca`, visually verified via `read_file`: real 27-frame raw New Horizons LORRI flyby exposure sequence `nh-lorri-lor_0299178877..0299178929` with zero text and zero scale bars).
  - Added `File:Video - Pluto and its moon Charon orbiting each other - Nasa-s New Horizons (51712771431).webm` (`1028x840` clean upper crop from `1028x1024`, `1.29x` upscale on lifted `#162238`–`#1F3150` starry canvas, `sha256: 89f4eb6318a6311195bdd19ba9f748a323d2064a7bc65d97f2dd7ac6edc5b5d4`, visually verified via `read_file`: real 7-frame LORRI barycentre sequence) in `R19` (`1st app.`) and `R30` (`2nd and final app.`).
  - Added `ksc_011906_nh_launch` (`800x450 -> 1600x900` `2.00x` inset, `sha256: df0c050d9030a264…`) in `R37` and `ksc_011906_nh_srbjett` (`800x450 -> 1600x900` `2.00x` inset, `sha256: d57e64dfcf9e815e…`) in `R40`.
  - Added `File:VIDEO - Arrokoth Flyby - Kuiper Belt - NASA's New Horizons 2019 (52829322492).webm` (`1920x1080` native `1.00x`, `sha256: 49963c0e035753d0…`, real 9-frame LORRI Arrokoth flyby sequence) in `R67` Cut 2 alongside `File:New Horizons Approach to Arrokoth.ogv` (`800x500 -> 1440x900` `1.80x` inset, trimmed `0.0–4.2 s`).
- **Secondary `CODE` Restructure (`8` Full-Frame `CODE` Rows + `5` Folded `source=NASA` Overlay Rows):** Folded the `5` secondary Part-2 `CODE` rows (`R17`, `R38`, `R43`, `R52`, `R61`) into `source=NASA` rows with animated edit overlays (`overlay_034_r17_sunlight_distance_bar`, `overlay_034_r38_elliptical_orbit_bar`, `overlay_034_r43_downlink_gauge`, `overlay_034_r52_mountain_atmosphere_gauge`, `overlay_034_r61_basal_melting_cutaway`) over graded NASA archive plates (`<= 2` appearances per asset). Every single `CODE -> CODE` interval across all `8` `source=CODE` rows (`R02`, `R15`, `R24`, `R29`, `R35`, `R48`, `R56`, `R69`) now contains `1–3` real native-motion video clips:
  1. `R02 -> R15`: `R03` (`File:The Pluto System As Seen By New Horizons Spacecraft.webm`) + `R05` (`File:Video - Nasa’s New Horizons - Pluto Flyby 14 7 2015 (51718116305).webm`)
  2. `R15 -> R24`: `R19` (`File:Video - Pluto and its moon Charon orbiting each other - Nasa-s New Horizons (51712771431).webm`)
  3. `R24 -> R29`: `R25` (`File:The Pluto System As Seen By New Horizons Spacecraft.webm`)
  4. `R29 -> R35`: `R30` (`File:Video - Pluto and its moon Charon orbiting each other - Nasa-s New Horizons (51712771431).webm`) + `R34` (`ksc_011906_nh_launchchange`)
  5. `R35 -> R48`: `R36` (`ksc_011906_nh_spacesep`) + `R37` (`ksc_011906_nh_launch`) + `R40` (`ksc_011906_nh_srbjett`)
  6. `R48 -> R56`: `R50` (`File:Video - Nasa’s New Horizons - Pluto Flyby 14 7 2015 (51718116305).webm`)
  7. `R56 -> R69`: `R67` (`File:New Horizons Approach to Arrokoth.ogv` + `File:VIDEO - Arrokoth Flyby - Kuiper Belt - NASA's New Horizons 2019 (52829322492).webm`)

---

## 3. Orbit Ruling (`J2362` Chief Explicit `0`-Orbit-Beat Exception) & `R30` Second Distinct Real Source

- Removed all `[ORBIT ACTS]` tags and all `optional omni_034_*` references from `shot_list_v01.csv` and `SHOT_LIST_v01.md`; retyped `R30` and `R57` as plain `source=NASA` archive rows under Chief's `J2362` explicit `0`-Orbit-beat exception and `£0` archive route approval.
- Added `File:Video - Pluto and its moon Charon orbiting each other - Nasa-s New Horizons (51712771431).webm` (`Cut 1`, `4.44 s`) inside `R30` alongside `PIA19968` (`Cuts 2–3`, `9.04 s` across two crops) so `R30` (`13.48 s`) uses two distinct real sources (`1` native LORRI video sequence + `1` LORRI/MVIC still) instead of holding `13.5 s` on a single still.

---

## 4. Corrected Evidence Claims (`14` Distinct `WHEN` Labels, `1.95x` Still / `2.00x` Video Inset Max Upscale, Committed Luma Artifact)

- **`14` Distinct `WHEN` Labels:** Consolidated `R03`'s `13–14 JULY 2015` label as `WHEN #1` and renumbered `WHEN #1` through `WHEN #14` across `shot_list_v01.csv`, `SHOT_LIST_v01.md`, `SFX_PLAN_v01.md`, and `SOURCE_EVIDENCE_v01.json`.
- **True Max Upscale (`<= 2.35x` Cap):** Restated the true maximum still upscale as **`1.95x`** (`PIA21965`, `985x554 -> 1920x1080`) and maximum video inset upscale as **`2.00x`** (`800x450 -> 1600x900` on lifted `#162238`–`#1F3150` starry canvas for the KSC launch clips), all well within the `<= 2.35x` ceiling. Also replaced all placeholder video SHA-256 hashes in `SOURCE_EVIDENCE_v01.json` with the exact SHA-256 hashes of the downloaded original video files.
- **Lifted-Navy Luma Artifact & Polish-Gate Target:** Committed `07_Edit-Project/verify_lifted_navy_luma.py` and `07_Edit-Project/LIFTED_NAVY_LUMA_ARTIFACT_v01.json` (SHA-256 `248990cd4bd7e9b3e8b438e5a4aee28eb9b8914fbd3f9c29a4d1076d99d1f6d1`), documenting the deterministic BT.601 luma distribution (`canvas_only mean_luma = 39.78`, `p95_luma = 44.99`) and marking the composed `R01` (`PIA20291` over `#162238`–`#1F3150`) luma (`expected mean_luma 52.0–62.0`, `p95 175.0–210.0`) as an explicit assembly verification target for `polish_gate.py`.
