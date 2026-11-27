# J3818 — Exact-File QA Review: `OWB:064` `J3719_v02` Thumbnails, `THUMB_LEDGER.json` (`T045`) & `SHOT_LIST_v02.md`

- **Date:** 2026-11-27T00:24Z
- **Reviewer:** `gemini` (specialist worker on Mac mini; advisory review only — elected Chief is `codex` per `chief_relay.py status`).
- **Ref:** `J3011`, `J3021`, `J3022`, `J3023`, `J3719` (`DECISION.md`, merged via PR #1357 at `2026-11-26T23:57:06Z`), `J3817` (PR #1358, head `2eb6fafcf66e3b03cb1b85c0a80231e6649e05c5`)
- **Film / Deadlines:** `OWB:064` (`02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes`) · Ben watch deadline **Fri 11 Dec 2026 18:00 London** · Planned air slot **Wed 16 Dec 2026 18:00 London**.
- **Scope:** Read-only QA review (£0 spend, 0 credits, no upload, no YouTube Studio changes, no merges).
- **Current disposition: FIX / awaiting independent re-review.** The original advisory KEEP was superseded by J3829. J3835 supplies corrected R11/provenance records for independent review; this document does not release J3022 or J3023. Measurements below are the original Gemini observations, not a new worker PASS.

> **Transparency note on routing:** Both `J3817` (fallback lane 2 on `--kind thumb`) and `J3818` (fallback lane 3 on `--kind review` while `claude` is out of usage until `2026-11-27T07:50:00Z`) ran on `gemini`. Every NAS file, SHA-256 hash, `thumb_preview.py --score` check, raw NASA source plate, full-size JPEG, `168x94` phone sheet, `THUMB_LEDGER.json` diff, and `SHOT_LIST_v02.md` row was re-verified from scratch in this session. Final independent PASS and merge authority rests with Chief (`codex`).

---

## 1. Exact Files & SHA-256 Verification (`J3719_v02/` vs `THUMB_SCORES_v02.json` vs `THUMB_LEDGER.json` `T045`)

**Result: PASS** (with 1 expected merge-conflict note for Chief on `THUMB_LEDGER.json` below).

| Artifact | Size / Bytes | Recomputed NAS SHA-256 | Matches `THUMB_SCORES_v02.json` | Matches PR #1358 `T045` |
|---|---|---|---|---|
| `064_thumb_A_extreme_worlds_v02.jpg` | `1920x1080` / `251,971` | `bc1b60dbacf405e9ef2c2bf169f5442cea1e5312dd56ceade96560c73fb2e393` | YES | YES |
| `064_thumb_B_venus_uranus_v02.jpg` | `1920x1080` / `221,422` | `29ea71dab31ab13efa723d5257856324be02a91e96f1aaa47783f3a395b34c75` | YES | YES |
| `064_thumb_C_real_nasa_saturn_v02.jpg` | `1920x1080` / `202,465` | `4ec5544c4fd9a7e9338bb207be936c90ec2d0683eb307e45d3224aa7458903f1` | YES | YES |
| `064_thumbs_ABC_v02_preview_sheet.jpg` | `173,117` | `22ac3dfb600b8d514e76d923c2f05f697023d26e95405d01b2cdb798bad73160` | YES | n/a |
| `THUMB_SCORES_v02.json` (NAS == PR #1358 repo) | `2,308` | `0358f12ee1b160c6814df6f2e85a689443a2b4dfa407c6b111d69e4878416a1d` | Byte-for-byte identical | n/a |

- **NAS path verified:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/08_Thumbnail/J3719_v02/`
- **`THUMB_LEDGER.json` row `T045` (PR #1358):** `status: "proposed"`, `video: null`, `title: "Every Planet Explained in 12 Minutes (Mercury to Neptune)"`, `job: "J3817"`, `maker: "gemini"` on all three arms, exact NAS paths and SHA-256 hashes verified 3/3.
- **Prior `v01` files untouched (verified on NAS):**
  - `064_thumb_A_all_8_worlds_v01.jpg`: `8b70c45888cd030d3addcf1b5ba140b8720dce1149e7089f60157d1803b2955b`
  - `064_thumb_B_464c_to_minus224c_v01.jpg`: `898576f023e394aad43fa2e2d691c705b8f94493854af5deb5ba3c8af3cd224f`
  - `064_thumb_C_real_nasa_photos_v01.jpg`: `f9349d8fcb18297e1041374a2bf60a8632b7a353f9586a962ad6963588098cf4`
  - `064_thumbs_ABC_v01_preview_sheet.jpg`: `73c7a0d253a74869b9bf74c38203b10ae933305c01229c4e1bccbbc8341be28a`
- **Chief merge-conflict note (`THUMB_LEDGER.json`):** PR #1357 (merged `2026-11-26T23:57:06Z`) added a placeholder `T045` row on `main` (`sha256: null`, `maker: "codex"`). Because PR #1358 branched from pre-#1357 `main`, `git merge-tree main pr-1358` reports a single-hunk conflict on `05_Analytics/tests/THUMB_LEDGER.json`. When merging PR #1358, resolve `T045` cleanly in favour of PR #1358's populated `T045` entry (keeping `status: "proposed"`, `video: null`, `maker: "gemini"`, and the three verified `v02` SHA-256 hashes).

---

## 2. Visual Inspection (`1920x1080` + `168x94` Phone Sheet) & Machine Gate

**Result: PASS** on all three variants.

### Independent `thumb_preview.py long --score` re-run
- **Variant A (`064_thumb_A_extreme_worlds_v02.jpg`):** `PASS  saturation=172.3  near_black=18%` (`18.1%`; `sat >= 120`, `near_black <= 28%`)
- **Variant B (`064_thumb_B_venus_uranus_v02.jpg`):** `PASS  saturation=161.5  near_black=20%` (`19.5%`; `sat` inside `~150–165` target and strictly `<= 175`, `near_black <= 28%`)
- **Variant C (`064_thumb_C_real_nasa_saturn_v02.jpg`):** `PASS  saturation=180.6  near_black=18%` (`18.1%`; `sat >= 120`, `near_black <= 28%`)

### Visual & rule checks (full-size JPEGs + `064_thumbs_ABC_v02_preview_sheet.jpg` + raw NASA plates)
- **Channel-wide checks:** Zero Orbit character on any variant. Bottom-right duration zone (`x > 75%`, `y > 78%`) clear dark-navy space on all three. House heavy sans capitals (`Bebas Neue`), single `#FFE000` yellow hook word + white rest, heavy dark stroke/shadow, readable at `168x94`.
- **Variant A (`8 EXTREME WORLDS`):**
  - **HOOK:** PASS (`8 EXTREME WORLDS`, names the scope/worlds).
  - **BAND:** PASS (`EXTREME` `#FFE000`, `8` and `WORLDS` white, cleanly in deep-navy top band `y = 0..21%`, zero letters touching planets).
  - **ART/PROVENANCE:** Deep-navy cosmic backdrop replaces v01's flat periwinkle gradient, white speckles, and hard black cutout halos; feathered planet limbs look clean. Clear Jupiter (`PIA22946`) + illuminated Saturn with full uncolliding rings (`PIA11141`) focal hierarchy; crisp Blue Marble Earth (`PIA18033`) scale cue lower-left; real Mariner 10 Venus (`PIA23791.jpg` right colour-enhanced globe, visually confirmed against raw `PIA23791.jpg`) replaces simulated `PIA00271`. Editorial non-scale lineup documented in `BUILD_REPORT_v02.md`.
  - **PHONE (`168x94`):** PASS — headline and Jupiter/Saturn/Earth read immediately.
- **Variant B (`464°C` | `-224°C`):**
  - **HOOK:** PASS (`464°C` `#FFE000` left, `-224°C` white right; `"TO"` dropped so nothing crosses seam).
  - **BAND:** PASS — both globes sit below the clean dark-navy top band (`y = 0..21%`); white vertical divider starts strictly below the text band (`y = 232`) with zero text overlap; custom bold minus bar in `-224°C` is crisp and unmistakable at `168x94`.
  - **ART/PROVENANCE:** Left globe is real Mariner 10 Venus (`PIA23791.jpg` right globe, visually verified) graded warm golden-amber at `sat=161.5` — clearly reads as cloudy Venus, not the Sun. Right globe is real Voyager 2 Uranus (`PIA18182.jpg`, visually verified against raw `033` shelf file, `sha256=3dcc8311...`) in crisp ice-cyan matching Chapter 7's `−224.2 °C` coldest planetary atmosphere (Neptune `PIA01492` removed). Crisp Blue Marble Earth (`PIA18033`) anchors scale on the lower-centre seam, clear of bottom-right.
  - **PHONE (`168x94`):** PASS — strongest instant colour-contrast pop and crisp `-` sign legibility at thumbnail size.
- **Variant C (`REAL NASA PHOTOS`):**
  - **HOOK:** PASS (`REAL` `#FFE000`, `NASA PHOTOS` white).
  - **BAND:** PASS — cleanly in dark-navy top band completely off Saturn and its rings.
  - **ART/PROVENANCE:** Rule 19 compliant single uncropped, aspect-preserved Cassini Saturn-and-rings hero (`PIA11141.jpg`, visually verified against raw `PIA11141.jpg`, including Saturn's authentic shadow across the left rear ring; 3-panel triptych scrapped; zero black-disc artifact, zero top-bar leak, stray bottom-left moon suppressed) filling `>40%` of frame. Crisp Blue Marble Earth (`PIA18033`) scale inset on lower-left with thin white `§2.B.4` pointer arrow, clear of rings and bottom-right (`~1.76×` phone-legibility enlargement explicitly documented in `BUILD_REPORT_v02.md`).
  - **PHONE (`168x94`):** PASS — Saturn + rings, Earth inset, and headline read instantaneously.
- **Required corrected attribution for `J3023` credits:** `DECISION.md` and `J3817` specified `PIA18033` from the `033` shelf and referred to it as "Apollo 17 Blue Marble". Visual inspection of `HARVEST_033/PIA18033.jpg` confirms it is NASA/NOAA's authentic Suomi NPP VIIRS *Blue Marble 2012* (North America view), not Apollo 17 (`AS17-148-22727`). Because `J3817` used the exact requested NASA ID `PIA18033`, no thumbnail rework is needed; `J3023` should simply credit `NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring (PIA18033)` accurately in the description's Image Credits.

---

## 3. Title / Thumbnail Pairing, Description First Line & Chapters (`DECISION.md` Lock)

**Result: PASS**

- **Lead Title A (`57` chars, `<= 60` chars):** `Every Planet Explained in 12 Minutes (Mercury to Neptune)`
  - Matches `#1` search phrase (`Every Planet Explained`) and `#2` GB autocomplete (`every planet explained in 12 minutes`); honest to `11:42` (`701.86 s`) planned timeline.
- **Programmatic word-overlap check against all three `v02` hooks:**
  - vs `8 EXTREME WORLDS`: `[]` (**0 shared words**)
  - vs `464°C -224°C`: `[]` (**0 shared words**)
  - vs `REAL NASA PHOTOS`: `[]` (**0 shared words**)
- **Preservation for `J3023`:** `08_Thumbnail/BUILD_REPORT_v02.md` §3 preserves verbatim:
  - Lead Title A + Reserves B/C/D with exact pairing guards (never pair Reserve B with Thumb B; never pair Reserve D with Thumb C);
  - Exact two-paragraph description opening block from `DECISION.md` (including explicit Venus `464 °C` surface heat vs Uranus `−224.2 °C` atmospheric minimum distinction);
  - All 8 tightened listing chapters (`0:00 Mercury — Ice at 430 °C` through `9:45 Neptune — Supersonic Winds at the Edge`), removing the Jupiter midpoint-twist spoiler and over-definitive `"Knocked Sideways"` origin framing on Uranus.

---

## 4. `SHOT_LIST_v02.md` Verification (`0:00–0:32.85` Opening & Row `R09` Venus)

**Original opening/R09 observations only; overall shot list requires re-review.** (`SHOT_LIST_v01.md` untouched; locked VO `every_planet_explained_vo_v01.wav` `4b478fcd` `683.86 s` untouched).

- **Opening cadence `0:00–0:32.85` (10 contiguous rows `R01a–R04b`, zero gaps/overlaps, every interval `<= 4.0 s`):**
  - `R01a` `0.00–3.50` (`3.50 s`, `NASA`, `PIA15162` + `01 / 08 · MERCURY` progress strip, no chapter card, no Orbit)
  - `R01b` `3.50–7.10` (`3.60 s`, `NASA`, `PIA17386`)
  - `R02a` `7.10–9.30` (`2.20 s`, `NASA`, `PIA16523`)
  - `R02b` `9.30–11.45` (`2.15 s`, `NASA`, `PIA16523` tight polar push-in `<= 2.35×`, back-to-back = 1 appearance)
  - `R03a` `11.45–15.00` (`3.55 s`, `NASA`, `PIA17386`)
  - `R03b` `15.00–18.80` (`3.80 s`, `CODE`, `code_graphic_064_r03a_mercury_sunlight.mp4`)
  - `R03c` `18.80–22.10` (`3.30 s`, `NASA`, `PIA19411` — real Mercury imagery separating full-screen graphics)
  - `R03d` `22.10–25.70` (`3.60 s`, `CODE`, `code_graphic_064_r03b_mercury_night.mp4`)
  - `R04a` `25.70–29.25` (`3.55 s`, `NASA`, `PIA11364`, `WHO #1: Giuseppe Colombo (1920–1984) — Italian mathematician`)
  - `R04b` `29.25–32.85` (`3.60 s`, `NASA`, `PIA16853`, `WHEN: 1965`)
- **Rule checks across all 60 rows:**
  - First chapter card: `C02` at `81.90 s` (strictly `> 0:45`).
  - Consecutive `CODE` rows: **0**.
  - Stills exceeding `MAX_REUSE = 2` non-adjacent appearances across the full film: **0** (`PIA15162`: 1, `PIA17386`: 2, `PIA16523`: 1, `PIA19411`: 2, `PIA11364`: 2, `PIA16853`: 2, `PIA23791`: 2, `pvo_uv_790205`: 1).
- **Row `R09` (`82.20–93.80 s`) Venus provenance repair:**
  - `PIA00271` (NASA Magellan *"Computer Simulated Global View of the Northern Hemisphere"*, `KIND_FAIL`) is **completely removed** from the shot table (`0` occurrences) and logged under Hard Rejects.
  - Replaced with real Mariner 10 Venus (`PIA23791.jpg` right colour-enhanced globe cropped off divider) + verified 023-shelf Pioneer Venus Orbiter UV clouds (`pvo_uv_790205.jpg`, verified on archive NAS at `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/07_Edit-Project/nasa_pool_v01/pioneer/pvo_uv_790205.jpg`, exact SHA-256 `f9d45efa36ac2bd00bc72f5abf8beedd0ee75d06c99c629012e27c87ee59db80`).
  - J3829 invalidated the original PIA00233 acceptance: a 3-D reconstruction is KIND_FAIL. J3835 removes it from R11 and executable pool/cut inputs and selects verified real overhead SAR PIA00215. Exact path, hash, resolution and crop are in SHOT_LIST_v02.md and jobs/reviews/J3835/EVIDENCE.json. Independent review must verify this change.


---

## 5. Independent J3818 re-review required

The unconditional KEEP and release recommendation are withdrawn by J3829. Review the J3835 correction PR together with #1358/#1359. Verify the required PIA00215 substitution, overhead radar provenance and crop, unchanged timing/VO and four thumbnail hashes, corrected Suomi NPP credits, and the populated proposed T045 row. Only the independent reviewer may issue the next KEEP/FIX. Confirm required merges separately and verify J3022 readiness before any J3023 advance. Ben watch Fri 11 Dec 18:00 London and planned air Wed 16 Dec 18:00 London remain unchanged.

The existing J3023 work still includes syncing opening/R09 executable inputs to SHOT_LIST_v02 and rendering its split Mercury graphics and progress strip. Historical v01 shot-list files are not current assembly instructions. Do not run the legacy plan builder blindly: it predates the opening/R09 repairs. PIA00233 is rejected, never an optional fallback.
