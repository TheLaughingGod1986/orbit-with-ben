# J3902 — Independent Completed-Cut & Upload-Package QA Review for OWB:064 (Master v03, PR #1390)

- **Job:** `J3902` (`kind: qa`, `ref: J3023`, `board: 064 edit`)
- **Film:** `OWB:064` — *Every Planet Explained in 12 Minutes (Mercury to Neptune)* (`02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes`)
- **Candidate PR:** `TheLaughingGod1986/orbit-with-ben#1390` (branch `gemini/J3023-owb064-assembly`, HEAD `81e0cdfc136f65ab00316b49db8e133fba12fd6a`)
- **Reviewer:** `gemini` (Gemini 4 Neon, specialist worker on the Mac mini; `chief_relay.py status` at `2026-11-27T14:04Z` elects **Chief: Codex (`codex` UP)** while `claude` is out of usage until `2026-11-27T17:50:00Z`)
- **Timestamp:** `2026-11-27T14:05Z`
- **Spend / Publishing Guard:** **£0 cash, 0 Flow/Vertex/ElevenLabs credits.** Zero uploads, scheduling, privacy edits, or YouTube Studio test arming (`T045` remains `proposed`, `video: null`).
- **Honest Capability Scope:** Recorded via `chief_relay.py capabilities --agent gemini --available ""`. This review directly inspected text files, JSON/code, exact SHA-256 hashes, `ffprobe`/`ffmpeg` loudness & `blackdetect` measurements, independent re-runs of all six machine gates plus `youtube:package --dry-run`, all 17 warned frames on `picture_qa_review.jpg`, the `J3719_v02` thumbnail preview sheet, 46 freshly extracted still frames from `master_v03.mp4`, and 10 freshly extracted still frames from `064_every_planet_explained_trailer.mp4`. **This session claims neither audio hearing nor moving-video playback perception; Ben's final watch supplies actual audio and motion review.**

---

## Recommendation to Elected Chief (`codex`)

**RECOMMENDATION: `FIX` (Targeted Package-Only Repair — `master_v03.mp4` itself is `KEEP`)**

- **Long Master `064_every_planet_explained_master_v03.mp4` (`sha256=d59057aed1590e7f6ef097513256a0548c4f9b1d7e544c4bade28aa83fef647a`): `KEEP` — do NOT re-render.** All six machine gates pass on independent re-execution, loudness and CFR delivery specs are verified, prior versions `v01`/`v02` and all locked inputs (`v04` script, `v01` VO, `R11` `PIA00215`, `PIA18033` Suomi NPP credit, `J3719_v02` thumbs, zero `PIA00271`/`PIA00233`) are intact, and every flagged `picture_qa`/`polish_gate` frame plus 46 independent master frames passed visual inspection.
- **Upload Package & Social Trailer (`PR #1390` / `11_Upload-Package/`): `FIX` required before Chief PASS, PR #1390 merge, and `J3023` `jobs.py awaits` handoff.** Direct visual inspection of the 37 s vertical 9:16 trailer caught severe horizontal text/graphic clipping across ~11 seconds of the cut, plus provenance/credit drift in `POOL_PROVENANCE_J3023_v02.json` and `Descriptions/`. Because Ben's watch deadline is **Fri 11 Dec 2026 18:00 London** (14 days away; planned air **Wed 16 Dec 2026 18:00 London**) and fixing the trailer + package metadata costs **£0** and requires **zero re-render of `master_v03.mp4`**, fixing these now prevents a broken Reels trailer from shipping via Buffer.

---

## 1. Exact Deliverable & Hash Verification (Independent Check on `studio-live` & PR #1390)

| Deliverable | Expected (J3902 / PR #1390) | Independently Verified | Result |
|---|---|---|---|
| **Master v03** (`09_Final-Export/064_every_planet_explained_master_v03.mp4`) | `d59057aed1590e7f6ef097513256a0548c4f9b1d7e544c4bade28aa83fef647a`, `557,502,349` B, `1920x1080`, `24/1` CFR, `701.875 s`, `-14.4 LUFS`, `-1.5 dBTP` | Exact SHA-256 & byte match (`557,502,349` B); `ffprobe`: `1920x1080`, `24/1` CFR, `16,845` frames, `701.875 s`, AAC `48 kHz` stereo; independent `ffmpeg loudnorm`: `-14.5 LUFS`, `-1.3 dBTP`, `LRA 3.9 LU`; `blackdetect`: zero black in film body (only `0.375 s` tail fade `701.458–701.833 s`) | **PASS** |
| **Prior Master v01** (`064_every_planet_explained_master_v01.mp4`) | Preserved (`3fb6a311…`) | `3fb6a31154e6a06db50b05d1534f44a47365a60a097434275fec6a60c8dfde7b` (`488,572,407` B) intact on `studio-live` | **PASS** |
| **Prior Master v02** (`064_every_planet_explained_master_v02.mp4`) | Preserved (`2543bb94…`) | `2543bb941a5f2ac46464e0f49084f20598d80be28a59a569ea562f58320f7193` (`554,537,028` B) intact on `studio-live` | **PASS** |
| **Locked VO v01** (`02_Voiceover/every_planet_explained_vo_v01.wav`) | `4b478fcd…` untouched | `4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa` exact match | **PASS** |
| **Locked Script v04** (`01_Script/every_planet_explained_script_master_v04.md`) | `556f3c8d…`, `review:script` `91.6/100` | `556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8`; `npm run review:script` independently returned **PASS `91.6 / 100`** | **PASS** |
| **R11 Magellan SAR `PIA00215.jpg`** (`03_Reference-Material/J3835_radar_v01/PIA00215.jpg`) | `46dc965a…`, crop `(350,600,2550,1838)` → push `(430,645,2470,1793)`, `118.05–124.40 s`, followed by `r14_venus_spin_v02` through `130.75 s` | Exact SHA-256 `46dc965a02d4bff533685892ad16a76845a384d482ffaedda024c870b5b8a7b4`; cut `#027` (`118.05–124.40 s`) & `#028` (`124.40–130.75 s`) match verbatim; full-size frame `t=120.5 s` inspected: razor-sharp overhead Alpha Regio pancake domes, zero borders/gaps, `Credit: NASA / JPL (Magellan SAR)` | **PASS** |
| **Forbidden Sources Absent** | Zero `PIA00271`, zero `PIA00233` (and zero retired `Five_Minutes_in_Orbit.webm` / `JPL-20210222-M2020f-0001.mp4`) | `cuts=0`, `pool=0`, `desc=0` for `PIA00271` and `PIA00233`; zero active cut/pool sources use `Five_Minutes_in_Orbit.webm` or `JPL-20210222-M2020f-0001.mp4` (3 string hits in `cuts_064_j3023_v02.json` are solely historical `"note": "J3023 v02 fix: replaced …"` annotations) | **PASS** |
| **`PIA18033` Suomi NPP Credit** | `NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring` | Present verbatim in `Descriptions/every_planet_explained_long_description_v01.txt` | **PASS** |
| **Thumbnails `J3719_v02` & Ledger `T045`** | `A` `bc1b60db…`, `B` `29ea71da…`, `C` `4ec5544c…`, preview sheet `22ac3dfb…`; `T045` `proposed` / `video: null` | All four NAS SHA-256s match `THUMB_LEDGER.json` & `PACKAGE_MANIFEST.json` verbatim; preview sheet visually re-checked; `T045` confirmed `status: "proposed"`, `video: null` | **PASS** |
| **Vertical 9:16 Social Trailer** (`11_Upload-Package/Trailer/064_every_planet_explained_trailer.mp4`) | `771d1f2a…`, `37 s`, `9:16` | Hash matches (`771d1f2a368ad4dbe1ee7b4cb541b0422a8d4d739ae946a8923f5ae9a4fe3cff`, `9,879,657` B, `37.038 s`, `-14.4 LUFS`, `-1.1 dBTP`), **BUT FAILS visual 9:16 framing QA** (see Defect 1 below) | **FAIL (FIX)** |

---

## 2. Independent Machine Gate Re-Verification

All six machine gates plus `youtube:package --dry-run` were independently re-executed against the exact PR #1390 tree (`81e0cdfc13`) and NAS `master_v03.mp4`:

| Gate | Independent Result | Notes |
|---|---|---|
| `clip_check.py --words stt_raw.json --vo-end 683.86 --repeat-ok R27` | **PASS** (`54 rows — PASS`) | Confirmed `--repeat-ok R27` is a legitimate intentional transition in locked script `v04` (`"What looms beyond the asteroid belt?"` → `"Beyond the asteroid belt at seven hundred and seventy-eight million kilometres..."`), not a VO stumble. Every chapter card `C02–C08` follows the preceding sentence with a `0.56–0.60 s` breath. |
| `picture_qa.py` (`full_master_v03_pack/PICTURE_QA.md` + `picture_qa_review.jpg`) | **PASS** (`0/138` fail, `17` warn) | All 17 warned frames directly inspected visually on `picture_qa_review.jpg`: 12 real NASA spacecraft mosaic/map keyword warns (`PIA17386`, `PIA19411`, `PIA00407`, `PIA02982`, `PIA17172`, `PIA00317`) and 5 low-detail warns (`PIA19400` ×2, `PIA14944`, `PIA01492`, New Horizons Pluto `11:39`) — every frame is authentic, crisp, unpadded spacecraft imagery. |
| `polish_gate.py` (`full_master_v03_pack/polish_gate_v03.json`) | **PASS** (`0/138` fail, `5` warn) | All 5 warns match the 5 low-detail frames above; verified directly on extracted master frames. |
| `music_gate.py --others` (vs all readable OWB NAS beds) | **PASS** (`0` fail, `0` warn) | Independently verified against other OWB NAS `.mp3` beds: `every_planet_score_bed_v01.mp3`, `701.9 s`, `70.6 BPM`, brief `Pace: 68-76 BPM`. |
| `sfx_kit.py level` (exact NAS stems `064_vo/sfx/music_stem_v01.wav`) | **PASS** | Independently returned `SFX level PASS: VO -20.2 LUFS, SFX -48.2 LUFS, 25 hits`. |
| `npm run gate:episode` & `npm run review:script` | **PASS** | `gate:episode` returned `PASS` (`93.1/100`, auto-selecting `script_master_v01.md`); `review:script -- --file ...v04.md` returned `PASS` (`91.6/100`). |
| `npm run youtube:package -- --dry-run` | **PASS** (`ok: true`) | Exact SHA-256 `d59057ae…`, title, description, chapters, 18 tags, pinned comment, `thumb_A`, trailer resolved; zero upload/schedule performed. |

---

## 3. Direct Visual Inspection Summary

### 3.1 Master v03 (`master_v03.mp4`) — **KEEP**

Directly inspected all 17 frames on `full_master_v03_pack/picture_qa_review.jpg` plus **46 freshly extracted frames** across the timeline (opening `0:00–0:32`, all 7 chapter cards `C02–C08`, `R11` `PIA00215`, `R14` `r14_venus_spin_v02`, `Venera 13`, both Orbit Omni clips `156 s` & `203 s`, all 6 historical portraits `Gauss`/`Galileo`/`Herschel`/`Le Verrier`/`Galle`/`Lassell`, `R20` ISS `243.5 s`, `R21` mid-film subscribe cue `247 s`, `R22` Mars `PIA00407` & `PIA19400`, `R26` `PIA24542_full`, `R35`/`R38` `PIA21046`, `R37` `PIA14944`, `R41` `r01_sourced_composite`, `R42` `PIA18182` & `weic2310a`, `R50` `PIA01492`, `R53` `r62_solar_comparison_timeline`, and `R54` Pluto `696–700.2 s`):

- **Opening `0:00–0:32.85` (`J2428` / `DECISION.md`):** All 10 beats (`R01a–R04b`) are strictly `2.15–3.80 s` (`<= 4.0 s`), alternating real MESSENGER Mercury plates with split `r03a`/`r03b` graphics; frame 0 (`t=0.5 s`) shows clean circular Mercury (`PIA15162`) on lifted cosmic navy with the centered `01 / 08 · MERCURY` progress strip, zero black halo or star bleed, and zero Orbit/chapter card before `0:30`.
- **Zero back-to-back code graphics** across all 138 cuts.
- **v02 → v03 visual fixes verified in rendered pixels:** `PIA21046` (`7:26`, `8:15`) shows clean Saturn & rings with zero bottom black strip; `GLOBE_ON_BLACK` planets (`PIA15162`, `PIA00407`, `PIA01492`, `PIA18182`) show smooth circular limbs without rectangular edge clipping; `PIA19400` (`4:26`, `4:30`) is full-bleed 16:9 with zero blurred pillarbox bars; `plate_031_r25` (`4:03`) is bright real sunlit ISS/Soyuz over Earth (zero red animation); `R54` Pluto (`11:39`) shows textured cratered terrain beside Sputnik Planitia.
- **Teach-on-Screen & Polish Pass (`TEACH_AND_POLISH_REVIEW_v03.md`):** Verified accurate across all 8 chapters (NUMBER objects + VO-matched `<= 4`-word labels, all 7 named people with WHO cards, recurring `1610–2024` timeline, lifted-navy backdrops, agency corner credits).

### 3.2 Social Trailer (`064_every_planet_explained_trailer.mp4`) — **FAIL (Blocking Defect 1)**

Directly inspected 10 frames extracted across `0.5 s – 35.5 s` (`0.5, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 28.0, 32.0, 35.5 s`). `_build_064_trailer_v01.py` applies a blind centre-crop (`crop=ih*608/1080:ih`) to `0.00–32.85 s` of the 16:9 master, slicing off horizontal graphics and text across three segments (~11 s of the 37 s cut):

1. **`0:00–0:03.5` (`tr_000.5`):** The 16:9 bottom progress strip is clipped on both margins — `"01 / 08 · MERCURY"` is cut off to **`"ERCURY"`**, and `SATURN / URANUS / NEPTUNE` are cropped off the right edge.
2. **`0:15.0–0:18.8` (`tr_016.0`):** `code_graphic_064_r03a_mercury_sunlight.mp4` is brutally cropped — top-left heading `"MERCURY · 58 MILLION KM"` is truncated to **`"ON KM"`**, the Mercury globe is cropped completely off the left edge, and the temperature bar is sliced at both edges.
3. **`0:22.1–0:25.7` (`tr_024.0`):** `code_graphic_064_r03b_mercury_night.mp4` loses `"NIGHT PLUNGE"` and the Mercury globe off the left edge, clips `+430 °C DAY` / `-164 °C NIGHT`, and pushes `"WITHOUT AN ATMOSPHERE"` flush across the left/right edges.
4. **Minor container/encoding polish on trailer:** `ffprobe` reports `avg_frame_rate=10911744/454861` (`start_pts=262` / `0.0213 s` offset from `-f concat -c copy`) at `608x1080` (`end_card.png` at `35.5 s` itself is legible and clean).

---

## 4. Required Targeted Fixes (Before Chief PASS & PR #1390 Merge)

All fixes below are **£0 spend**, require **zero re-render of `master_v03.mp4` (`d59057ae…`)**, and should land on `gemini/J3023-owb064-assembly` (PR #1390) followed by a quick targeted re-check:

1. **[Blocking] Rebuild vertical 9:16 social trailer cleanly (`064_every_planet_explained_trailer.mp4`):**
   - Preserve `v01` (`771d1f2a…`) or record updated SHA-256 in `11_Upload-Package/PACKAGE_MANIFEST.json`.
   - Keep the exact `0:00–32.85 s` master audio + `4.15 s` `"Full film on YouTube"` end card, encoded in one clean pass at exact `24/1` CFR (`1080x1920` preferred or `608x1080` with `start_pts=0`).
   - Do NOT centre-crop wide 16:9 graphic/progress-strip segments: replace `0:00–3.5 s`, `15.0–18.8 s`, and `22.1–25.7 s` with full-bleed vertical NASA Mercury imagery + vertically centered 9:16-safe call-outs (`01 / 08 · MERCURY`, `+430 °C DAY`, `-180 °C NIGHT`, etc.) safely inside the 9:16 margins. Verify every cut of the rebuilt trailer via extracted still frames.
2. **[Required] Sync `POOL_PROVENANCE_J3023_v02.json` and `Descriptions/` Image Credits:**
   - **`07_Edit-Project/POOL_PROVENANCE_J3023_v02.json`:** Add the 3 actually-active v02/v03 cut assets currently missing from `active_assets` (`plate_031_r21_earth_limb_v01.mp4`, `plate_031_r25_iss_orbit_cuts_v01.mp4`, `plate_031_r26_iss_clouds_v01.mp4`) and remove retired `plate_031_r42a_iss_blue_limb_v01.mp4` from `active_assets` (move to `rejected_assets`).
   - **`11_Upload-Package/Descriptions/every_planet_explained_long_description_v01.txt` (line 17):** All NASA PIA IDs in cuts and description reconcile 1-to-1 (`0` missing, `0` extra; `3,346` chars `<= 5,000`), and `PIA18033` Suomi NPP credit is exact. Add explicit naming/attribution for the 3 active Neptune-chapter historical portraits (`613.55–644.45 s`: `Urbain Le Verrier`, `Johann Gottfried Galle`, `William Lassell`, Wikimedia Commons PD) alongside Jensen 1840 (Gauss), Sustermans 1636 (Galileo), and Abbott 1785 (Herschel).
3. **[Minor PR Hygiene]:**
   - Normalize CRLF (`\r\n`) trailing whitespace in `07_Edit-Project/shot_list_v02.csv` (`git diff --check` flagged every line).
   - Check `PACKAGE_MANIFEST.json` `"categoryId": "27"` (Education) vs `youtube:package --dry-run` resolved `"categoryId": "28"` (Science & Technology, OWB uploader default) so manifest and uploader output agree (`"28"`).

---

## 5. Transparent Non-Blocking Observations (For Chief & Ben's Watch)

- **Narrated chapter cards (`C02–C08`):** Because locked `every_planet_explained_vo_v01.wav` (`4b478fcd…`, `683.86 s`) was recorded with `0.7 s` inter-chapter gaps and laid continuously without inserting `2.4 s` silent pauses, each `2.40 s` chapter card (`C02–C08`) starts `0.56–0.60 s` after the preceding chapter's final word, and the next chapter's opening distance phrase (`"At 108 million kilometers..."`, etc.) begins `~0.24–0.36 s` into the card (`VO rms -19.5` to `-22.2 dBFS`, `peak -3.7` to `-6.1 dBFS` across `C02–C08`). `clip_check.py` explicitly permits narrated cards and passes cleanly; **Ben's watch supplies the actual audio/pacing check.**
- **Cut `#39` (`plate_031_r26_iss_clouds_v01.mp4`, `186.95–193.15 s`):** Cut length is `6.20 s` vs `5.96 s` source duration (`0.24 s` `tpad` tail hold — well under the `4 s` static-hold limit).
- **Mid-film `[SUBSCRIBE BEAT]` (`R21`, `35.9%`):** Lower-third `"SUBSCRIBE TO ORBIT WITH BEN / NEW SPACE MYSTERIES EVERY WEEK"` carries no subscriber count and follows OWB `studio/RULES.md` (single mid-film beat allowed).
- **Jupiter in-film chapter card (`C05`, `324.80 s`):** Retains `J3022`/`J3883`-approved `"METALLIC HYDROGEN"` sub-line while listing/description chapters use the panel's spoiler-free `"5:25 Jupiter — What Happens If You Land?"` per `DECISION.md` line 140.
- **Privacy & repo hygiene:** Zero secrets, account emails, private IPs, or media binaries in PR #1390 (`81e0cdfc13`).
- **Companion Shorts reminder for `J3023`:** When `J3023` sets `jobs.py awaits` after Chief PASS, ensure the two linked companion Shorts follow-up jobs required by the `J3023` brief are tracked without expanding the long-VO scope.

---

## 6. Elected-Chief Next Steps

Because `gemini` is a specialist worker and **Codex (`codex`)** is elected Chief:
1. Chief reviews this independent `FIX` report and confirms whether to keep `master_v03.mp4` (`d59057ae…`) untouched while directing a targeted `J3023` package-only fix on PR #1390 (rebuilt 9:16 trailer + `POOL_PROVENANCE_J3023_v02.json` 3-clip sync + Neptune portrait credit line + CSV LF / `categoryId` hygiene).
2. After targeted trailer/package re-check passes, Chief merges PR #1390 and releases `J3023` to place `OWB:064` on Ben's watch board by **Fri 11 Dec 2026 18:00 London** (planned air **Wed 16 Dec 2026 18:00 London**; `T045` stays `proposed` / `video: null` until post-watch upload).
