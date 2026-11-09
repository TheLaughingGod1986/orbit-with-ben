# J2306 Condition Verification Review — J2299 (`033 picture: correct source identities and deliver reviewable opener and graphics`)

- **Job**: `J2306` (`Verify condition for J2299`)
- **Parent Job**: `J2299` (`033 picture: correct source identities and deliver reviewable opener and graphics`, `film: 033`, `stage: picture`, `repo: owb`, `progress: 0/5`, `after: J2290`)
- **Upstream & Dependent Jobs**:
  - `J2238` (`Chief: resolve 033 shots orphan-review`, `status: done`, `SHOT_LIST_v01.md` planning PASS `d67daf94`)
  - `J2256` (`033 Uranus: stills lock + OMNI R29/R55 price-pass brief from SHOT_LIST_v01`, `status: done`, Option B `£0` / no Omni)
  - `J2290` (`033 Uranus: £0 harvest 38 missing stills + CODE graphics from STILLS_LOCK_v01`, `status: done`, open PR #578 `adab48f716e066f57e2e1c9f56c3de789dda854e`, delivery only, not approval)
  - `J2297` (`Chief: resolve 033 picture orphan-review`, `status: done`, FIX ruling in `jobs/reviews/J2297/REVIEW.md`, PR #580)
  - `J2300` (`033 picture: review corrected source map, native opener and graphics`, `status: open`, `after: J2299`, `required_capabilities: ["moving_video_input"]`)
- **Reviewer**: `gemini` (`gemini-argon`, 7 November 2026)
- **Verdict**: **CONDITION NOT YET SATISFIED (`HOLD / WAIT FOR CHIEF`) — Keep `J2299` blocked at step `0/5` (`--type input --recheck J2306`, next check `2026-11-07T06:45:00Z`). Draft PR #584 (`06ae7792d7d0ce38172386f40d507bf5ecdc2a4d`) and PR #578 (`adab48f716e066f57e2e1c9f56c3de789dda854e`) remain `OPEN` with `0` Chief comments or rulings. All 43 pool inputs (`41` exact-hash images + `2` original PDFs), `3` auxiliary files, `3` cached usage-terms records, `3` contact sheets, `3` exhausted `R01` opener candidates, and locked VO (`3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460`) are verified on disk, while the elected Chief's `R01` opener fallback/source decision and `R54` CODE -> `R55` graphic separation ruling remain pending, and `0/14` corrected graphic renders, `0/2` PDF rasters, and final picture QA/polish gates have been delivered on the Mini. Zero generation, zero spend (`£0.00`).**

---

## 1. Recorded Waiting Condition on `J2299`

`J2299` is held (`hold.type = "input"`, `recheck_task = "J2306"`) with:
> `parked for Chief: approve a specific R01 fallback or genuinely new bounded source approach, and resolve R54/R55 graphic separation, using PR584 / 06ae7792d7. Three new candidates exhausted; do not repeat their search. Existing PIA opener files are stills. No paid generation authorised. Then finish source rights/crops, PDF rasters, 14 corrected renders and final gates under same 0/5 plan; J2300 moving-video QA remains dependent.`

---

## 2. Direct Verification Evidence (`2026-11-07T00:45Z`)

1. **Chief Decision & PR Status (`PR #584` and `PR #578`) — UNMET:**
   - **Draft PR #584** (`codex/J2299-source-reconciliation`, head `06ae7792d7d0ce38172386f40d507bf5ecdc2a4d`) remains `OPEN` with `0` comments and `0` reviews.
   - **PR #578** (`macbook/J2290`, head `adab48f716e066f57e2e1c9f56c3de789dda854e`) remains `OPEN` with `0` comments and `0` reviews (unmerged draft evidence only).
   - No Chief ruling, commit, or new queue job has been recorded since `2026-11-06T21:14Z` to:
     1. Approve a specific `R01` (`0.00–6.22 s`) fallback under the missing-footage rule or scope a genuinely new bounded source approach (after all `3/3` new deep-candidate slots were exhausted in `OPENER_SEARCH_J2299_v01.json` and `PIA01283`/`PIA01280` were confirmed as stills, with `svs20390_shot9_beauty_rings.mp4` strictly excluded because it is the standalone Short `ZpEA8stoSPA` opener).
     2. Resolve the **`R54` CODE -> `R55` graphic adjacency conflict** (accepted `SHOT_LIST_v01.md` `R54` is `CODE`, so rendering `R55` as another full-frame pressure diagram violates code-graphic separation; `R55` requires real moving imagery between diagrams or an explicit Chief shot-list/row revision).

2. **On-Disk Verification of `PR #584` (`06ae7792d7`) Partial Evidence — VERIFIED:**
   - **43/43 Primary Pool Inputs (`STILLS_POOL_STATUS_v03.json`)**:
     - `41/43` image files exist at their recorded Mini/NAS paths and match their expected SHA-256 digests (`BYTES_VERIFIED_NOT_KEEP`).
     - `2/43` historical Phil. Trans. entries are present as recovered original PDFs awaiting raster reproduction (`ORIGINAL_PDF_RECOVERED_RASTER_PENDING`):
       - `File:Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg` -> `/Users/benjaminoats/_desk/cache/J2299/harvest/File_Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg_page1.pdf` (`1f4eaddf5c0e317cec4f072d624e0ceccbf6d6bc1f55f42408f0eab9af88b316`)
       - `File:Herschel_1783_Georgium_Sidus_letter_Phil_Trans.jpg` -> `/Users/benjaminoats/_desk/cache/J2299/harvest/File_Herschel_1783_Georgium_Sidus_letter_Phil_Trans.jpg_page1.pdf` (`4874a44234212d7bddef596a7615b00890f5200e757aa9d80278d66b29eadbf4`, resolved in `EXTERNAL_RECORDS_J2299_v01.json` as *On the Diameter and Magnitude of the Georgium Sidus*, not a naming letter)
   - **3/3 Auxiliary Assets**:
     - `PIA00405`: `/Users/benjaminoats/_desk/cache/J2089/size_sources_v01/PIA00405.jpg` (`fc93286c2d73a64f2b095c2e1f1df867b0e96ad0b9515987f9b38fd2ed91a641`)
     - `orbit-seedance-reference-16x9-v01.png`: `01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png` (`922298a14991f128482122ffd91ff48775f96d81ed838d69dc3009b3914f9472`)
     - `PIA00271` (simulated Venus, excluded as Earth): `/Users/benjaminoats/_desk/cache/J2299/harvest/PIA00271.jpg` (`0c3e270656d41ec81bf7acd73830cb6285d9bc80f6b13fdbe5f38cd596253262`)
   - **3/3 Contact Sheets (`SOURCE_SHEETS_J2299_v01.json`)**:
     - `source_sheet_1.jpg`: `f0a7a2f26dedc6edc50378d801ef45e60716848df4168a0ee6a71c058b791521`
     - `source_sheet_2.jpg`: `e20bfd369f0b5a73f05ae77f2abc94299778022478302d61729474eca277bbd0`
     - `source_sheet_3.jpg`: `b02fa170753d58e074efe5d1243b617ea1c97454b6e40c855f8922be06be042f`
   - **3/3 Exhausted `R01` Opener Candidates (`OPENER_SEARCH_J2299_v01.json`, `new_deep_candidates_used: 3/3`)**:
     - `weic2602c.mp4`: `deca60d4dbf82e19243104ccbd4c3406428198e242c9632b0ecca3eb83920de2` (`NOT_ACCEPTED_FROM_STATIC_SOURCE_EVIDENCE` — diffuse spectroscopy slices, no clear sideways rings)
     - `hubble_seasonal_1999.mp4`: `54696e5bf1467fa4fb412fb45e8d7660c50789b4fee2b1eac6152520a2cb4d10` (`NOT_ACCEPTED_FROM_STATIC_SOURCE_EVIDENCE` — `176x272` with baked text and tiny subject)
     - `eso_uranus.mov`: `4aba1a3c57850de6929b414d085535451a7c0bfab817c11f934c23ed52962acd` (`NOT_ACCEPTED_FROM_STATIC_SOURCE_EVIDENCE` — `680x280` `12 fps` noisy/soft without vertical-ring answer)
   - **Reconciliation Counters (`PICTURE_RECONCILIATION_J2299_v01.json`)**:
     - `accepted_rows_preserved`: `67`, `prior_caption_differences_reconciled`: `32`, `prior_exclusions_retained`: `17`, `draft_graphic_files_audited`: `14`, `draft_graphic_duration_matches`: `14`, `mini_graphics_delivered`: `0`, `keep_assigned`: `0`.
   - **Preserved Locked VO & Spend Guard**:
     - `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/02_Voiceover/uranus_vo_v01.wav` matches `3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460` (`uranus_vo_v01.mp3`: `f6e35088c5a71876ff1022a97d81e91dced6bf3f967b9eb7acb156bd7e543868`).
     - `05_Analytics/ai_spend/ledger.jsonl` records **`0` spend entries (`£0.00`)** for `OWB:033` / `J2299` / `J2290`.

3. **Remaining Work on `J2299` After Chief Decision (`step 0/5`):**
   - Finish source rights/crops (`PIA17306` Sromovsky/Wisconsin/Keck credit/terms, `PIA01389` replacement/exclusion, Commons/ESA/Webb credits) and rasterise the `2` Phil. Trans. PDFs (accounting for `File:Herschel_1783_Georgium_Sidus_letter_Phil_Trans.jpg` being the diameter paper rather than the naming letter).
   - Render and hash-verify all `14` corrected smooth (`24/30 fps`) graphic binaries on the Mini (resolving `R54`/`R55` separation, `R26` `retrograde_tilt`, `R46` magnetic offset vs `R52` fluid mantle, card hold `<= 4 s`, `<= 4`-word labels, picture changes every `4–6 s`, true globe scaling for Miranda/Moon, house type, grain, and credits).
   - Deliver executable cuts/pool manifests, rendered frame sheet, and `picture_qa.py` / `polish_gate` reports, then hand off to `J2300` (`moving_video_input` QA).

---

## 3. Queue Action & Protected Elected-Chief Handoff

- Because `scripts/jobs.py` (`set_wait` line 354) restricts `jobs.py wait J2299 --recheck J2306` to the elected Chief (`Only the elected Chief may record a condition check`, currently `Chief: Codex`), `J2306` is parked for Chief with complete verification evidence in this document.
- Elected Chief (`codex`) can either issue the `R01` opener + `R54`/`R55` ruling and reopen `J2299`, or record the condition check and close `J2306` with:
  ```bash
  python3 scripts/jobs.py wait J2299 --agent codex --type input --recheck J2306 \
    --condition "J2306 condition check (jobs/reviews/J2306/REVIEW.md): CONDITION UNMET. Draft PR584 (06ae7792d7) and PR578 (adab48f716) remain OPEN with 0 Chief rulings; all 43 pool inputs (41 exact-hash images + 2 original PDFs), 3 auxiliaries, 3 contact sheets, 3 exhausted R01 opener candidates and locked VO (3d73576e0c) verified on disk, with 0/14 Mini graphic renders delivered and £0 spend. Chief must approve a specific R01 0.00-6.22s fallback or genuinely new bounded source approach (3 new candidates exhausted; PIA01283/PIA01280 are stills; svs20390 excluded; no paid generation authorised) and resolve R54 CODE -> R55 graphic separation. Then finish source rights/crops, PDF rasters, 14 corrected renders and final gates under same 0/5 plan; J2300 moving-video QA remains dependent." \
    --check-at "2026-11-07T06:45:00Z" \
    --action "Chief opener/shot decision (R01 fallback + R54/R55 separation), then corrected graphic renders and complete picture QA pack" --git
  python3 scripts/jobs.py done J2306 --agent codex --ref jobs/reviews/J2306/REVIEW.md \
    --result "HOLD / CONDITION UNMET (jobs/reviews/J2306/REVIEW.md): PR #584 (06ae7792d7) verified on disk (41 exact-hash images + 2 PDFs, 3 auxiliaries, 3 sheets, 3 exhausted R01 candidates, locked VO 3d73576e0c, 0/14 Mini graphics, £0 spend); Chief R01 fallback/source decision and R54/R55 separation ruling still pending; J2299 kept blocked at 0/5 (--recheck J2306, next check 2026-11-07T06:45:00Z)." --git
  ```
