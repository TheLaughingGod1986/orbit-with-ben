# J3818 — Fresh Post-J3835 Exact-File QA Review: `OWB:064` `J3719_v02` Thumbnails, `THUMB_LEDGER.json` (`T045`), `SHOT_LIST_v02.md` & `R11` / Earth Attribution Corrections

- **Date:** 2026-11-27T10:04Z
- **Reviewer:** `gemini` (specialist worker on Mac mini; advisory review only — elected Chief is `codex` per `chief_relay.py status`; reopened by `claude` acting Chief sweep at `2026-11-27T09:56Z`).
- **Reviewed Target:** PR `#1361` (`macbook/J3835`, head commit `9ff96bd97b0d018d8a5825858a0d2ebc382fcce9`), superseding PR `#1358` (`J3817`) and the earlier pre-J3835 `J3818` draft on PR `#1359`.
- **Ref:** `J3011`, `J3021`, `J3022`, `J3023`, `J3719` (`DECISION.md` on `main` `fbdfbada07`), `J3817` (PR `#1358`, superseded), `J3829` (Chief FIX `7bd7345ae8`), `J3835` (PR `#1361` `9ff96bd97b`), `J3839`.
- **Film / Deadlines:** `OWB:064` (`02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes`) · Ben watch deadline **Fri 11 Dec 2026 18:00 London** · Planned air slot **Wed 16 Dec 2026 18:00 London**.
- **Scope:** Read-only QA review (£0 spend, 0 credits, no upload, no YouTube Studio changes, no merges). Static images, hashes, and text/JSON records only — no audio or moving-video review is claimed (`chief_relay.py capabilities` recorded empty).
- **Verdict (advisory):** **`KEEP`** — all `J3829` Chief FIX items (`PIA00233` hard-rejected and replaced with verified real Magellan overhead SAR `PIA00215` in executable R11 inputs; `PIA18033` Earth attribution corrected to NASA/NOAA Suomi NPP Blue Marble 2012 across all records with existing JPEG hashes preserved) and all 5 original `J3818` checklist items PASS exact-file, hash, visual (`1920x1080` + `168x94` + `PIA00215` 16:9 crops), provenance, and shot-list verification. Ready for elected Chief (`codex`) to issue formal PASS, merge PR `#1361` + this updated PR `#1359` (zero conflicts), close superseded PR `#1358` unmerged, clear `J3022`'s hold, and advance `J3023` assembly.

> **Transparency note on independence & supersession:** The prior unconditional `KEEP` in PR `#1359` predated `J3829` and `J3835` and is completely superseded by this review. The `J3835` corrections in PR `#1361` (`9ff96bd97b`) were authored by `macbook` and independently verified from scratch in this session on the Mac mini. Final PASS, PR merges/closures, and `J3022`/`J3023` release authority remain strictly with the elected Chief (`codex`).

---

## 1. `J3829` Chief FIX Verification (PR `#1361` · `9ff96bd97b`)

**Result: PASS**

### 1a. `PIA00233` Removed & Replaced by Verified Real Magellan Overhead SAR `PIA00215` in Row `R11`
- **`PIA00233` (`KIND_FAIL` 3-D radar/altimetry terrain reconstruction) removed from active inputs:**
  - `0` occurrences in `SHOT_LIST_v02.md` shot table, `cuts_064_j3022_v01.json`, `pool_064_j3022_v01.json`, and `build_j3022_plan_and_pool.py`.
  - Retained strictly as a `HARD REJECT / KIND_FAIL` record in `POOL_PROVENANCE_J3022_v01.json` (lines 713–720) and `SHOT_LIST_v02.md` (line 33). All prior optional/allowed wording is removed.
- **Verified replacement `PIA00215` (*Venus - Alpha Regio*, real Magellan overhead SAR, NASA/JPL Public Domain):**
  - Official source: `https://science.nasa.gov/photojournal/venus-alpha-regio/`
  - NAS destination file: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/03_Reference-Material/J3835_radar_v01/PIA00215.jpg`
  - Independently recomputed NAS SHA-256: `46dc965a02d4bff533685892ad16a76845a384d482ffaedda024c870b5b8a7b4` (`2,046,040` bytes, `2782×2666`, mode `L`) — **byte-for-byte identical** to the `023` archive shelf copy (`/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/07_Edit-Project/nasa_pool_v01/magellan_extra/PIA00215.jpg`) and matches `jobs/reviews/J3835/EVIDENCE.json`, `pool_064_j3022_v01.json`, and `POOL_PROVENANCE_J3022_v01.json`.
  - **Independent visual inspection of raw plate & exact 16:9 crops:** Inspected full `PIA00215.jpg` plus rendered exact crops `(350, 600, 2550, 1838)` (`2200×1238`, aspect `1.7771`, `0.873×` downscale to `1920×1080`) and optional push-end `(430, 645, 2470, 1793)` (`2040×1148`, aspect `1.7770`, `0.941×` downscale to `1920×1080`). Both crops show crisp real Venusian volcanic pancake domes and tectonic fractures with **zero black borders or radar data gaps**, strictly `<= 1.0×` scale (no upscaling), and no invented perspective.
  - **Executable timing preserved (`cuts_064_j3022_v01.json`):** Diff against `origin/main` confirms **only 1 of 86 cut entries changed** (index `13`, `R11`: `timeline_in=118.05`, `timeline_out=124.4`, `upscale=1.0`, exact `PIA00215` path and `crop_xyxy=[350, 600, 2550, 1838]`). Transition at `124.40 s` to `code_graphic_064_r14_venus_spin.mp4` (`124.40–130.75 s`) and all other 85 cuts are untouched.

### 1b. `PIA18033` Earth Attribution Corrected to NASA/NOAA Suomi NPP Blue Marble 2012
- Visual inspection of all three `J3719_v02` thumbnails confirms `PIA18033` depicts North America / Mexico (*Blue Marble 2012*, NASA/NOAA Suomi NPP VIIRS), not Apollo 17 (`AS17-148-22727`).
- Verified attribution corrected to **`NASA/NOAA Suomi NPP Blue Marble 2012`** / **`NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring`** (`https://science.nasa.gov/image-detail/amf-pia18033/`) across all affected records in PR `#1361`:
  - `08_Thumbnail/BUILD_REPORT_v02.md`
  - `08_Thumbnail/build_064_thumbs_v02.py` (diff vs PR `#1358` is strictly comments/docstrings only — zero executable rendering code changed)
  - `05_Analytics/tests/panels/owb-064-every-planet/DECISION.md`
  - `05_Analytics/tests/THUMB_LEDGER.json` (row `T045` note)
  - `07_Edit-Project/SHOT_LIST_v02.md` (row `R15`)
  - `07_Edit-Project/pool_064_j3022_v01.json`, `07_Edit-Project/POOL_PROVENANCE_J3022_v01.json`, and `07_Edit-Project/build_j3022_plan_and_pool.py`
- Zero leftover `"Apollo 17"` attribution on `PIA18033` in any active record. All 4 existing NAS thumbnail/sheet JPEG hashes remain unchanged.

### 1c. `J3835` Record Integrity & Merge Cleanliness
- Recomputed SHA-256 on all 12 files listed in `jobs/reviews/J3835/SHA256SUMS.txt` against `origin/macbook/J3835` (`9ff96bd97b`): **12/12 exact match**.
- All JSON files parse cleanly; both Python files (`build_064_thumbs_v02.py`, `build_j3022_plan_and_pool.py`) pass `ast.parse`.
- `git merge-tree --write-tree origin/main origin/macbook/J3835` succeeds with **zero conflicts** (`MERGE_TREE_CLEAN=YES`).

---

## 2. Exact NAS Thumbnail Files, SHA-256 Hashes & `THUMB_LEDGER.json` (`T045`)

**Result: PASS**

| Artifact (`08_Thumbnail/J3719_v02/`) | Size / Bytes | Recomputed NAS SHA-256 | Matches `THUMB_SCORES_v02.json` | Matches PR `#1361` `T045` |
|---|---|---|---|---|
| `064_thumb_A_extreme_worlds_v02.jpg` | `1920x1080` / `251,971` | `bc1b60dbacf405e9ef2c2bf169f5442cea1e5312dd56ceade96560c73fb2e393` | YES | YES |
| `064_thumb_B_venus_uranus_v02.jpg` | `1920x1080` / `221,422` | `29ea71dab31ab13efa723d5257856324be02a91e96f1aaa47783f3a395b34c75` | YES | YES |
| `064_thumb_C_real_nasa_saturn_v02.jpg` | `1920x1080` / `202,465` | `4ec5544c4fd9a7e9338bb207be936c90ec2d0683eb307e45d3224aa7458903f1` | YES | YES |
| `064_thumbs_ABC_v02_preview_sheet.jpg` | `173,117` | `22ac3dfb600b8d514e76d923c2f05f697023d26e95405d01b2cdb798bad73160` | YES | n/a |
| `THUMB_SCORES_v02.json` (NAS == PR `#1361`) | `2,308` | `0358f12ee1b160c6814df6f2e85a689443a2b4dfa407c6b111d69e4878416a1d` | Byte-for-byte identical | n/a |

- **`THUMB_LEDGER.json` isolation check:** Comparing PR `#1361` against its `origin/main` merge-base confirms **only `T045` changed**. Row `T045` retains `status: "proposed"`, `video: null`, `title: "Every Planet Explained in 12 Minutes (Mercury to Neptune)"`, `job: "J3817"`, `maker: "gemini"` on all 3 arms, exact NAS paths and SHA-256s, and updated Suomi NPP attribution. The prior PR `#1358` merge conflict with PR `#1357` is cleanly resolved in PR `#1361`.
- **Locked VO unchanged:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/every_planet_explained_vo_v01.wav` recomputed SHA-256 `4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa` (`683.86 s`, exact match). Prior `v01` thumbnails and `SHOT_LIST_v01.md` untouched.

---

## 3. Visual Inspection (`1920x1080` + `168x94` Phone Sheet) & Machine Gate

**Result: PASS** on all three variants.

### Independent `thumb_preview.py long --score` re-run
- **Variant A (`064_thumb_A_extreme_worlds_v02.jpg`):** `PASS  saturation=172.3  near_black=18%` (`18.1%`; `sat >= 120`, `near_black <= 28%`)
- **Variant B (`064_thumb_B_venus_uranus_v02.jpg`):** `PASS  saturation=161.5  near_black=20%` (`19.5%`; `sat` inside `~150–165` target and strictly `<= 175`, `near_black <= 28%`)
- **Variant C (`064_thumb_C_real_nasa_saturn_v02.jpg`):** `PASS  saturation=180.6  near_black=18%` (`18.1%`; `sat >= 120`, `near_black <= 28%`)

### Direct visual check (full-size JPEGs A/B/C + `064_thumbs_ABC_v02_preview_sheet.jpg`)
- **Channel-wide:** Zero Orbit character on any variant; bottom-right duration zone (`x > 75%`, `y > 78%`) clear dark-navy space on all three; house heavy sans caps, single `#FFE000` yellow hook word + white rest, dark-navy top band (`y = 0..21%`) completely off globes/rings/dividers.
- **Variant A (`8 EXTREME WORLDS`):** Deep-navy cosmic backdrop (no periwinkle gradient, dots, or black cutout halos); clear Jupiter (`PIA22946`) + illuminated Saturn (`PIA11141`, uncolliding rings) focal hierarchy; real Mariner 10 Venus (`PIA23791` right globe); crisp NASA/NOAA Suomi NPP Blue Marble 2012 Earth (`PIA18033`) scale anchor lower-left; readable at `168x94`.
- **Variant B (`464°C` | `-224°C`):** Real Mariner 10 Venus (`PIA23791` right globe, warm golden-amber at `sat=161.5` — clearly Venus, not the Sun) vs real Voyager 2 Uranus (`PIA18182`, crisp ice-cyan matching Ch 7 `-224.2 °C`, Neptune `PIA01492` removed); `"TO"` dropped; white vertical divider stops cleanly below the top text band; bold minus sign unmistakably readable at `168x94`; crisp Earth (`PIA18033`) scale anchor on lower-centre seam.
- **Variant C (`REAL NASA PHOTOS`):** Rule 19 single uncropped, aspect-preserved Cassini Saturn-and-rings hero (`PIA11141`, 3-panel triptych scrapped, no black-disc artifact, no top-bar leak); crisp framed Earth (`PIA18033`) lower-left scale inset with thin white `§2.B.4` pointer arrow; top-band text completely off Saturn and rings; instant recognition at `168x94`.

---

## 4. Title / Thumbnail Pairing, Description First Line & Chapters (`DECISION.md`)

**Result: PASS**

- **Lead Title A (`57` chars, `<= 60` chars):** `Every Planet Explained in 12 Minutes (Mercury to Neptune)`
- **Programmatic word-overlap check against all three `v02` hooks:**
  - vs `8 EXTREME WORLDS`: `[]` (**0 shared words**)
  - vs `464°C / -224°C`: `[]` (**0 shared words**)
  - vs `REAL NASA PHOTOS`: `[]` (**0 shared words**)
- **Preservation for `J3023`:** Verified verbatim match between `DECISION.md` and `08_Thumbnail/BUILD_REPORT_v02.md` §3 for Lead Title A + Reserves B/C/D (with pairing guards), exact two-paragraph description opening block (explicitly distinguishing Venus `464 °C` surface heat vs Uranus `−224.2 °C` atmospheric minimum), and all 8 tightened listing chapters (`0:00 Mercury — Ice at 430 °C` through `9:45 Neptune — Supersonic Winds at the Edge`).

---

## 5. `SHOT_LIST_v02.md` Opening (`0:00–0:32.85`), `R09` & `J3023` Assembly Handoff

**Result: PASS** (with explicit `J3023` assembly boundary recorded below)

- **Opening cadence `0:00–0:32.85` (10 contiguous rows `R01a–R04b`, `0.00 s` gaps, every interval strictly `<= 4.0 s`):**
  - `R01a` `0.00–3.50` (`3.50 s`, `NASA`, `PIA15162` + `01 / 08 · MERCURY` progress strip)
  - `R01b` `3.50–7.10` (`3.60 s`, `NASA`, `PIA17386`)
  - `R02a` `7.10–9.30` (`2.20 s`, `NASA`, `PIA16523`)
  - `R02b` `9.30–11.45` (`2.15 s`, `NASA`, `PIA16523` tight polar push-in `<= 2.35×`, back-to-back = 1 appearance)
  - `R03a` `11.45–15.00` (`3.55 s`, `NASA`, `PIA17386`)
  - `R03b` `15.00–18.80` (`3.80 s`, `CODE`, `code_graphic_064_r03a_mercury_sunlight.mp4`)
  - `R03c` `18.80–22.10` (`3.30 s`, `NASA`, `PIA19411` — real Mercury imagery separating graphics)
  - `R03d` `22.10–25.70` (`3.60 s`, `CODE`, `code_graphic_064_r03b_mercury_night.mp4`)
  - `R04a` `25.70–29.25` (`3.55 s`, `NASA`, `PIA11364`, `WHO #1: Giuseppe Colombo (1920–1984) — Italian mathematician`)
  - `R04b` `29.25–32.85` (`3.60 s`, `NASA`, `PIA16853`, `WHEN: 1965`)
- **Full-table checks (60 rows):** First chapter card is `C02` at `81.90 s` (`> 0:45`); `0` consecutive `CODE` rows; `PIA00271` completely removed from `R09` (replaced with `PIA23791` right globe + verified 023-shelf `pvo_uv_790205`); `PIA00233` completely removed from `R11` (replaced with verified overhead SAR `PIA00215`).
- **Required `J3023` assembly execution checklist (documented per `J3835` `HANDOFF.md`):**
  1. `cuts_064_j3022_v01.json`, `pool_064_j3022_v01.json`, and `POOL_PROVENANCE_J3022_v01.json` already incorporate the `R11` `PIA00215` replacement and `PIA18033` Suomi NPP attribution, while still retaining the pre-`v02` opening (`R01–R04`) and `R09` (`PIA00271`) entries. `J3023` **must** generate `v02` executable cut/pool inputs synchronized to `SHOT_LIST_v02.md` (splitting `R01a–R04b`, removing `PIA00271` from `R09` -> `PIA23791` right globe + `pvo_uv_790205`), render `code_graphic_064_r03a_mercury_sunlight.mp4`, `code_graphic_064_r03b_mercury_night.mp4`, and the `01 / 08 · MERCURY` progress strip, and verify `picture_qa.py` PASS on the `v02` cut/pool files.
  2. Never run the historical `build_j3022_plan_and_pool.py` script during assembly.
  3. Credit `PIA18033` as `NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring (PIA18033)` and `PIA00215` as `NASA/JPL (PIA00215)` in the `11_Upload-Package` description Image Credits.

---

## 6. Overlapping PR Reconciliation (`#1358`, `#1359`, `#1361`) & Chief Handoff

| PR | Branch | State / Action for Elected Chief (`codex`) |
|---|---|---|
| **PR `#1358`** | `gemini/J3817-owb064-thumbs-v02` | **SUPERSEDED — DO NOT MERGE.** Converted to Draft with warning comment. Chief: close PR `#1358` unmerged so its stale `PIA00233` optional wording, `Apollo 17` misattribution, and `THUMB_LEDGER.json` conflict are never restored. |
| **PR `#1361`** | `macbook/J3835` (`9ff96bd97b`) | **READY TO MERGE.** Carries all 5 `J3817` files with `J3835` fixes applied, corrected `07_Edit-Project` files, updated `DECISION.md`, and `jobs/reviews/J3835/` evidence (`MERGE_TREE_CLEAN=YES` against `origin/main`). |
| **PR `#1359`** | `gemini/J3818-owb064-review` | **READY TO MERGE (updated directly on top of `9ff96bd97b`).** Replaces the superseded pre-J3835 unconditional `KEEP` with this fresh post-J3835 `KEEP` review (1 commit ahead of `#1361`, modifying only `jobs/reviews/J3818/REVIEW.md`, zero conflicts). |

**Next steps for elected Chief (`codex`):**
1. Issue formal Chief PASS on this `J3818` review and PR `#1361` (`9ff96bd97b`).
2. Merge PR `#1361` then PR `#1359` (or merge PR `#1359` directly, which includes `9ff96bd97b`), and close superseded PR `#1358` unmerged.
3. Clear `J3022`'s hold (ensuring `J3023` executes the `SHOT_LIST_v02.md` opening/`R09` sync + split Mercury graphics noted in §5) and advance `J3023` assembly ahead of Ben's **Fri 11 Dec 2026 18:00 London** watch deadline (planned air **Wed 16 Dec 2026 18:00 London**).
4. `T045` remains `status: "proposed"` (`video: null`); no YouTube upload, scheduling, or Studio test arming occurs until after Ben's UAT watch.
