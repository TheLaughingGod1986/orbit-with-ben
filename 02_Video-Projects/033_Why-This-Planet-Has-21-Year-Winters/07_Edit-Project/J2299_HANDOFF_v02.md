# J2299 — Complete Source Reconciliation, 24fps Graphics & QA Handoff (`J2299_HANDOFF_v02.md`)

- **Date:** 8 November 2026
- **Worker:** `gemini` (`J2299`)
- **Film / Stage:** `OWB:033` (*Why This Planet Has 21-Year Winters*) — `picture`
- **Status:** **Deliverables 1–5 complete (`£0` spend, `0` KEEP assigned); handed off to dependent moving-video QA job `J2300` and Chief review.**

---

## 1. Deliverable Checklist & Verification

1. **43 Pool IDs + Auxiliaries Audited & Reconciled (`SOURCE_AUDIT_J2299_v01.json`, `EXTERNAL_RECORDS_J2299_v01.json`, `STILLS_POOL_STATUS_v03.json`, `PICTURE_RECONCILIATION_J2299_v01.json`):**
   - All `32` `identity_mismatches_vs_lock_caption` and all `17` `do_not_treat_as_lock_subject` exclusions in `STILLS_POOL_STATUS_v02.json` are reconciled against official NASA, ESA/Hubble, ESA/Webb, and Wikimedia Commons records.
   - `PIA00271` (simulated radar Venus) is excluded from Earth roles (`PIA18033` Blue Marble serves all Earth cuts and globes).
   - `PIA00141` (Voyager 2 Miranda ridged terrain) is excluded from Uranus limb roles and used only in Miranda rows `R56` and `R62`.
   - `PIA01361` (5-moon montage strip), `PIA01283` (3-panel strip), `PIA00369` (4-panel strip), baked-label images (`PIA01975`, `PIA01976`, `PIA01278`, `PIA01281`, `PIA01282`, `File:36 Inch Airborne Infrared Telescope (6996884880).jpg`), wrong-planet files (`PIA01364`, `PIA01389`, `PIA01390`, `PIA01486`, `PIA01485`, `PIA02875`), and third-party Keck image `PIA17306` are excluded from `cuts_033_j2299_v01.json`.
   - Both Royal Society PDFs are rasterized at 200 DPI (`pool_original_pdf_raster_pending: 0`); `File_Herschel_1783_Georgium_Sidus_letter_Phil_Trans.jpg.pdf` (actually Herschel's 1783 diameter paper, not the Banks naming letter) is excluded from `R13`.
   - New plan versions `SHOT_LIST_v02.md` and `STILLS_LOCK_v02.md` preserve all `67` row boundaries (`0.00–629.40 s`), chapter pauses, and locked spoken lines from `SHOT_LIST_v01.md`.

2. **Opener `R01` (`0.00–4.35 s`) Resolved Under `J2386` (`5e68ec6532`):**
   - Uses Chief-accepted 24fps `97.77°` sideways Uranus sourced composite `r01_sourced_composite_v01_silent.mp4` (`SHA-256 aab9aa2af9dd8cd50195a0b91efe495abaf9f06be2daf72bd893014b56503e6d`, active interval `0.40–4.75 s` in `6.00 s` master, built from `PIA18182` `3dcc83114f` + JWST NIRCam `weic2310a` `e5f7a1a0e1`). `svs20390` exclusion retained.

3. **Mini-Readable Harvest & Checksum Manifests (`£0` Spend, No Media in Git):**
   - `72` verified source images, single-globe borderless crops, and PDF page rasters synced to `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01` with `SHA256SUMS.txt` (and local Mini cache `/Users/benjaminoats/_desk/cache/J2299/harvest`).
   - All `14` MacBook J2290 draft graphics were obtained/reproduced and superseded by `20` smooth `24 fps` renders (`19` active row graphics + `1` byte-identical `R26` alias `code_graphic_033_r26_axial_tilt_97deg.mp4`) in `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2299_code_graphics_v01` and `/Users/benjaminoats/_desk/cache/J2299/code_graphics_v01` with `SHA256SUMS.txt`.

4. **24fps Code Graphics & `R55` Separation (`CODE_GRAPHICS_J2299_v02.json`):**
   - Every graphic renders at `24 fps` (`1920×1080`, `libx264` CRF 18) with continuous starfield/plate motion (`0` frozen frame pairs across all 20 files), stage cuts every `3.3–5.6 s` matching `cuts_033_j2299_v01.json`, animated cards `≤ 3.85 s` (`0.35 s` fade in/out), `≤ 4` words per label, `1` label at a time, and white Didot italic corner credits only when no card is active.
   - Real observed globes with true diameter ratios: `R14` Uranus `PIA18182` (`560 px`) vs 4 Earths `PIA18033` (`140 px` each = `4.00:1`); `R59` Miranda `PIA01490` (`90 px`) vs Moon `PIA00405` (`630 px` = `1:7.00`).
   - `R26` uses `code_graphic_033_r26_retrograde_tilt.mp4` (`8.30 s`) with byte-identical alias `code_graphic_033_r26_axial_tilt_97deg.mp4` (not an extra cut). `R46` (`14.12 s`) is `code_graphic_033_r46_corkscrew_magnet.mp4`; `R52` (`13.90 s`) is `code_graphic_033_r52_interior_mantle.mp4`.
   - `R55` (`493.01–505.35 s`) uses Chief-accepted 3-cut cloud passage `r55_passage_v01_silent.mp4` (`SHA-256 4aa82d0e721988513eba44c38332b5537a9d6f41f9f406ab5d9623b04642483f`) under `J2334`/`J2386`, retiring `code_graphic_033_r55_pressure_gauge.mp4` so `R54` `CODE` is followed by moving world imagery.

5. **QA Reports, Contact Sheet & Explicit Handoff to `J2300`:**
   - `cuts_033_j2299_v01.json` (`144` cuts across `67` rows, `0.00–629.40 s`) & `pool_033_j2299_v01.json`.
   - `picture_qa_033_j2299_cuts_v01.json`: **`PASS`** (`0` failed, `0` warnings).
   - `polish_gate_j2299_reel_v01.json` (on `j2299_opener_and_graphics_reel_v01_silent.mp4`): **`PASS`** (`0` failed, `2` warnings).
   - `picture_qa_j2299_reel_v01.json` (on `j2299_opener_and_graphics_reel_v01_silent.mp4`): **`PASS`** (`0` failed, `2` warnings).
   - Contact sheet: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2299_code_graphics_v01/j2299_graphics_frame_sheet_v01.jpg`.
   - **Explicit Handoff:** No KEEP or media PASS is claimed from checksums, static sheets, or automated gates. `J2299` hands off to **`J2300`** (`033 picture: moving-video QA of opener and 14 graphics before Chief release`) for moving-video playback inspection and to Chief for picture stage release.
