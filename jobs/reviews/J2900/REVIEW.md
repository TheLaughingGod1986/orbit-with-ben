# J2900 — 033 Uranus Long Thumbnail Concepts A/B/C Review (`Rule H` + `Rule 19` + `OWB UAT` Staging)

- **Reviewer:** `gemini` (`Gemini 4 Argon (High)`, elected acting Chief & `review` chain lane)
- **Date:** 2026-11-15
- **Film:** `033_Why-This-Planet-Has-21-Year-Winters` (*Why Knocked-Sideways Uranus Has 21-Year Winters*)
- **Target Job Reviewed:** `J2899` (`f33d8f03df` / `f767ab52a8` by `cursor`)
- **Verdict:** **`KEEP` (`PASS`)** — All three `1920x1080` long thumbnail concepts (`033_thumb_A_v01.jpg`, `033_thumb_B_v01.jpg`, `033_thumb_C_v01.jpg`) and their `168x94` preview sheets (`033_thumb_{A,B,C}_v01_sheet.jpg`) pass `thumb_preview.py long --score` (`sat = 131.1 / 151.6 / 175.4 >= 120`, `near_black = 2.3% / 4.4% / 2.2% <= 30%`) and pass visual inspection across `HOOK`, `BAND`, `GRADE`, and `PHONE`. SHA-256 parity is verified across the git repo, NAS `OWB UAT`, and iCloud `OWB UAT` alongside `033_why_this_planet_has_21_year_winters_master_v04_PHONE.mp4`, and proposed unarmed row `T033` is verified in `05_Analytics/tests/THUMB_LEDGER.json`. `stages.thumbs.state` is marked `"done"` in `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/status.json`, unblocking `J2901` (`11_Upload-Package` build & dry-run).

---

## 1. Visual & Automated Gate Scores (`HOOK / BAND / GRADE / PHONE`)

All 6 image files (`033_thumb_{A,B,C}_v01.jpg` at `1920x1080` and `033_thumb_{A,B,C}_v01_sheet.jpg` at `168x94` + `640x360`) were directly inspected with `read_file` and re-verified with `python3 00_Brand/Channel-Setup/tools/thumb_preview.py long <thumb> --out <sheet> --score`:

| Concept | File | SHA-256 | Hook (`#FFD60A` Gold Word) | Source Plate (`harvest_J2299_v01`) | Sat (`>=100` / `>=120`) | Near-Black (`<=30%`) | `HOOK` | `BAND` | `GRADE` | `PHONE` (`168x94`) | Verdict |
|---|---|---|---|---|---:|---:|---|---|---|---|---|
| **A** (Rule 19 real frame) | `033_thumb_A_v01.jpg` | `9c029267c0a80fbb13572c40cc7b42cf012f2582bfcc3d5c49bf7c8f7a325e6f` | `21-YEAR WINTER` (`WINTER`) | NASA/ESA/CSA JWST NIRCam `weic2332a_hires.jpg` (`PIA25770` / `STScI-01GWQ3`) | `131.1` | `2.3%` | **PASS** | **PASS** | **PASS** | **PASS** | **KEEP** |
| **B** (Rule 12 comparison) | `033_thumb_B_v01.jpg` | `1185ea680e5284c6f893769a94e1280c28a36828803671a445effdc8ed629a8e` | `COLDER THAN NEPTUNE` (`COLDER`) | NASA/JPL Voyager 2 `PIA18182.jpg` (`24 Jan 1986`) + JWST `weic2310a_unannotated.png` | `151.6` | `4.4%` | **PASS** | **PASS** | **PASS** | **PASS** | **KEEP** |
| **C** (Rule 12 + 14 bright field) | `033_thumb_C_v01.jpg` | `48abb438ed7a8de3fa0a7d5b1474c725efbc48198c4260b35da5dce5607bc1b2` | `97.77° SIDEWAYS` (`97.77°`) | NASA/ESA/CSA JWST `weic2310a_unannotated.png` (bright cyan grade) | `175.4` | `2.2%` | **PASS** | **PASS** | **PASS** | **PASS** | **KEEP** |

### Criterion-by-Criterion Notes
1. **`HOOK` (`PASS` on A, B, C):**
   - Each concept uses 2–3 words in bold condensed uppercase (`BebasNeue-Regular.ttf`, SIL OFL) with one warm gold hook word (`#FFD60A`: `WINTER`, `COLDER`, `97.77°`), crisp white (`#FFFFFF`) on the remaining words, and a heavy dark navy stroke (`rgb(10, 12, 22)`).
   - None of the hooks repeats the full listing title (*Why Knocked-Sideways Uranus Has 21-Year Winters*); each adds an immediate concrete hook (`21-YEAR WINTER`, `COLDER THAN NEPTUNE`, `97.77° SIDEWAYS`).
2. **`BAND` (`PASS` on A, B, C):**
   - All three hooks sit strictly inside the top 20% band (`TOP = 0.20`), leaving the Uranus disk, bright polar cap, and vertical ring plane completely unobstructed.
   - Bottom-right duration badge zone is completely clear of text and key features on all three concepts.
   - Zero Orbit character on any long thumbnail (Standing Lesson 3).
3. **`GRADE` (`PASS` on A, B, C):**
   - All three concepts exceed both the `sat >= 100` minimum and the `sat >= 120` target (`131.1`, `151.6`, `175.4`) while staying far below the `near_black <= 30%` cap (`2.3%`, `4.4%`, `2.2%`).
   - Concept A fulfills Rule 19 using a single verified real JWST NIRCam spacecraft frame (`weic2332a_hires.jpg`, `PIA25770` / `STScI-01GWQ3`) showing Uranus's vertical rings and bright polar cap, shadow-lifted in its own sky colour with no inner rectangle or artificial border.
4. **`PHONE` (`168x94`, `PASS` on A, B, C):**
   - Inspected `033_thumb_A_v01_sheet.jpg`, `033_thumb_B_v01_sheet.jpg`, and `033_thumb_C_v01_sheet.jpg`: at `168x94` mobile feed size, all three hook lines and the sideways ring silhouette (plus the pale Voyager globe contrast in Concept B) are immediately legible.

---

## 2. `OWB UAT` Staging & `THUMB_LEDGER.json` Verification (`PASS`)

### A. SHA-256 Parity Across Repo, NAS, and iCloud `OWB UAT`
Verified identical SHA-256 digests across all working, archive, and UAT locations alongside `033_why_this_planet_has_21_year_winters_master_v04_PHONE.mp4` (`J2890` `awaits_ben`):

| File | Bytes | SHA-256 | Verified Locations |
|---|---:|---|---|
| `033_thumb_A_v01.jpg` | `307,979` | `9c029267c0a80fbb13572c40cc7b42cf012f2582bfcc3d5c49bf7c8f7a325e6f` | Git `08_Thumbnail/`, NAS `studio-live/.../08_Thumbnail/`, NAS `/Volumes/data/studio-live/orbit-with-ben/OWB UAT/`, NAS `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/`, iCloud `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/` |
| `033_thumb_B_v01.jpg` | `299,990` | `1185ea680e5284c6f893769a94e1280c28a36828803671a445effdc8ed629a8e` | Git `08_Thumbnail/`, NAS `studio-live/.../08_Thumbnail/`, NAS `/Volumes/data/studio-live/orbit-with-ben/OWB UAT/`, NAS `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/`, iCloud `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/` |
| `033_thumb_C_v01.jpg` | `245,430` | `48abb438ed7a8de3fa0a7d5b1474c725efbc48198c4260b35da5dce5607bc1b2` | Git `08_Thumbnail/`, NAS `studio-live/.../08_Thumbnail/` |
| `033_why_this_planet_has_21_year_winters_master_v04_PHONE.mp4` | `48,345,183` | `3ef32f4b673431835449a590f2246de19d84ff32a330893709cb2ccf6b954a19` | NAS `/Volumes/data/studio-live/orbit-with-ben/OWB UAT/`, NAS `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/`, iCloud `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/`, R2 `owb-033-v04` |

### B. `05_Analytics/tests/THUMB_LEDGER.json` Row `T033`
- Verified entry `T033` (`status: "proposed"`, `started: null`, `channel: "owb"`, `film: "OWB:033"`, `job: "J2899"`, `tags: ["rule19", "rule12", "rule14"]`):
  - Arm `a`: `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/08_Thumbnail/033_thumb_A_v01.jpg` (`21-YEAR WINTER`, SHA-256 `9c029267c0a80fbb13572c40cc7b42cf012f2582bfcc3d5c49bf7c8f7a325e6f`)
  - Arm `b`: `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/08_Thumbnail/033_thumb_B_v01.jpg` (`COLDER THAN NEPTUNE`, SHA-256 `1185ea680e5284c6f893769a94e1280c28a36828803671a445effdc8ed629a8e`)
  - Variant `c`: `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/08_Thumbnail/033_thumb_C_v01.jpg` (`97.77° SIDEWAYS`, SHA-256 `48abb438ed7a8de3fa0a7d5b1474c725efbc48198c4260b35da5dce5607bc1b2`)
- Zero Studio changes made; zero paid generation (`£0`); zero YouTube uploads.

---

## 3. Stage Progression & Next Steps

- Updated `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/status.json` `stages.thumbs` to `state: "done"` (`ref: "jobs/reviews/J2900/REVIEW.md"`).
- `J2901` (`033 Uranus: build 11_Upload-Package (PACKAGE_MANIFEST, chapters, credits, en-GB SRT, trailer) + dry-run (no upload)`) is now unblocked to run next.
