# J2089 Checkpoint v32 — Step 2 of 4 Locked (`HARVEST_POOL_v01.json` + `SHOT_LIST_v08.md`)

**Date:** 2026-11-07T18:12Z  
**Agent:** `gemini` (acting Chief on Mac mini)  
**Branch / Worktree:** `worker/J2089-rights` at `/private/tmp/J2089-rights`  
**Governing Scope:** `jobs/reviews/J2089/CHIEF_SCOPE_v31.md`  
**Spend:** £0.00 (no Vertex, Flow, or ElevenLabs calls)

## 1. Completed in Step 2 of 4 (`50%`)
1. **Harvested & Visually Verified NASA Goddard SVS 20311 Dragonfly Release + Extra NASA Mission Plates on `studio-live`:**
   - Stored on NAS (`studio-live`) at:
     `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/03_Reference-Material/harvest_J2089_v01/svs_20311/`
   - Saved source evidence (`svs_20311_api.json`, `svs_20311_page.html`, `science_nasa_dragonfly.html`, `PIA01050_metadata.json`, `PIA22766_metadata.json`, `SSC20210116_GR8438_metadata.json`, `PIA17172_metadata.json`, `PIA21445_metadata.json`, `PIA20021_metadata.json`) and manifests (`SVS20311_HARVEST_MANIFEST.json`, `EXTRA_NASA_HARVEST_MANIFEST.json`).
   - **Dragonfly motion clips (SVS 20311, Credit: `NASA/Johns Hopkins APL/Goddard Space Flight Center`):**
     - `SVS20311_DF_End_Pan_1080.mp4` (`1920×1080`, `12.52 s`, sha256 `8b516948a072009741f70a9081b019256862f26279971499eb089df62f8c604f`) -> Rows `37, 46, 49` (3 stretches `>10 s` apart).
     - `SVS20311_DF_Open_1080.mp4` (`1920×1080`, `24.45 s`, sha256 `95277151b09234fa8ffbb55f665df51cb2e843fdba483cf01b92488e880015b5`) -> Rows `44, 45, 48` (3 stretches `>10 s` apart).
     - `SVS20311_Dragonfly_Drill_1080.mp4` (`1920×1080`, `12.70 s`, sha256 `090782cba81ecaa50934f457054f34db6df34243faabbdad97236f67ff8c448f`) -> Row `50` (1 stretch).
     - `SVS20311_DF_Intake_shot_1080.mp4` (`1920×1080`, `13.23 s`, sha256 `a56340821e8378f84980f813bf02dcda41d9c1f0a6950cf960949d643d5cbeb3`) -> Reserve (`[]`).
   - **Dragonfly stills:**
     - `SVS20311_Dragonfly_Landed_Closeup.png` (`2250×1567`, sha256 `049c56cea98693bc26f88928f1a068e4d4f1c970cb6b554dd11867ed41f6ba36`) -> Rows `47, 50` (2 uses).
     - `NASA_Dragonfly_BannerFactSheet_2024.jpg` (`7500×3048`, sha256 `448b957db627fb63a5f5ed44fa2589a21d08ff511f4048a2ff3e7f34ba0e0d41`, Credit: `NASA/Johns Hopkins APL/Steve Gribben`) -> Rows `5, 47` (2 uses).
   - **Clean right-panel crop of `PIA20021.jpg` (`CHIEF_SCOPE_v31.md` §4):**
     - `PIA20021_right_panel_1440x1144.jpg` (`1440×1144`, crop box `(420, 36, 1860, 1180)` from `PIA20021.jpg`, sha256 `e38201c4f15f5e95c1171b3f00e2a9d33dd26e3997bf30697fc6d5e1ca5c779e`) -> Rows `31, 32` (2 uses, paired with `PIA17031` in Row `31, 33`).
   - **Additional NASA mission stills:**
     - `PIA01050.jpg` (`1901×2850`, Cassini-Huygens Titan IVB launch) -> Row `15` (1 use).
     - `PIA22766.jpg` (`3000×1266`, Cassini backlit Saturn & rings) -> Rows `3, 19` (2 uses).
     - `SSC20210116_GR8438.jpg` (`5400×3590`, NASA Stennis RS-25 hot-fire test plume in Earth air) -> Row `42` (1 use).
     - `PIA17172.jpg` (`9000×3500`, Cassini Saturn/Titan backlit panorama) -> Rows `10, 27` (2 uses).
     - `PIA21445.jpg` (`1020×1020`, Cassini Titan golden haze crescent) -> Rows `22, 26` (2 uses).

2. **Locked `SHOT_LIST_v08.md`, `HARVEST_POOL_v01.json`, and `HARVEST_INVENTORY_v23.json`:**
   - `SHOT_LIST_v08.md` (`sha256: efba940f89b8dc3ce5c2c41e461519e14b8af082b6473480b5787d1dc6129c9c`) locks all 52 rows.
   - `inventory_harvest_032.py --out /Users/benjaminoats/_desk/cache/J2089/inventory_v32` passed with:
     `39 cached source images; 62 export hashes; 0 errors; 0 missing source-evidence entries`.
   - Every active still has `≤ 2` uses; every active video clip has `≤ 3` stretches separated by `> 10 s`; 0 excluded Short assets (`PIA14925`, `PIA06230`, `PIA09739`, `PIA21625`) or rejected sources (`PIA07870`, `PIA07871`, `PIA10008`, `PIA07233`, `PIA16638`, `PIA19051`, `huygens_descent`, `dragonfly_at_titan`) are referenced in any row.

## 2. Next Steps (Step 3 of 4 & Step 4 of 4)
- **Step 3 of 4:** Render the graded 1080p30 moving-plate composites for Rows 1–52 (`R16` `032_r16_cassini_counter_draft_v01.mp4` and `R23` `032_r23_composite_preview_v02.mp4` are already `KEEP` under `CHIEF_SCOPE_v31.md`) to `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/composites_v01/` (never on root `/` since `/` has 11 GiB free).
- **Step 4 of 4:** Run `picture_qa.py`, `polish_gate.py`, and Short frame-exclusion checks on the completed picture pool and close `J2089`.
