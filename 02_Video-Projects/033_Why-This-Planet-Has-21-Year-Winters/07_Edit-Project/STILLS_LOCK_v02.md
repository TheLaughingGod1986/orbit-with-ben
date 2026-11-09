# 033 — Reconciled Stills Lock & Picture Plan (`STILLS_LOCK_v02.md`)

- **Film:** `033_Why-This-Planet-Has-21-Year-Winters` (*Why This Planet Has 21-Year Winters*)
- **Job:** `J2299` (`033 picture: correct source identities and deliver reviewable opener and graphics`)
- **Upstream References:** `J2297` Chief FIX of `J2290` PR `#578` (`adab48f716e066f57e2e1c9f56c3de789dda854e`); `J2386` Chief Ruling (`5e68ec6532`, `jobs/reviews/J2386/CHIEF_RULING.md`); `SHOT_LIST_v01.md` / `SHOT_LIST_v02.md`
- **Preserved History:** `SHOT_LIST_v01.md`, `STILLS_LOCK_v01.md`, `STILLS_POOL_STATUS_v01.json`, `STILLS_POOL_STATUS_v02.json`, and `J2299_HANDOFF_v01.md` remain untouched in git history and working tree.
- **Runtime & Structure:** `629.40 s` (`10:29.40`) across `67` spoken/end-hold rows (`R01–R67`) and `144` cuts (`mean 4.35 s/cut`, `max 6.00 s/cut`).
- **Spend / Generation:** **£0** (`0` credits spent; Option B £0 fallbacks active; no KEEP or media PASS claimed from checksums or job completion; handed off to `J2300` moving-video QA).

---

## 1. Reconciled Opener (`R01`) & Cloud Passage (`R55`) Under `J2386` (`5e68ec6532`)

1. **`R01` (`0.00–4.35 s`, followed by `R02` `4.35–8.18 s`):**
   - Uses Chief-accepted 24fps `97.77°` sideways Uranus sourced composite:
     - **NAS Path:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2334_fix/r01_sourced_composite_v01_silent.mp4`
     - **SHA-256:** `aab9aa2af9dd8cd50195a0b91efe495abaf9f06be2daf72bd893014b56503e6d` (`1,148,935` bytes, `1920×1080`, `24 fps`, `6.00 s` master, active interval `0.40–4.75 s`, `0` frozen pairs)
     - **Provenance:** Built from verified Voyager 2 `PIA18182` (`3dcc83114f...`) + JWST NIRCam `weic2310a` (`e5f7a1a0e1...`).
     - **Exclusions Retained:** Standalone Short `ZpEA8stoSPA` opener `svs20390_shot9_beauty_rings.mp4` (`f964c7f1dd...`) and 3-panel still `PIA01283` remain strictly excluded.
2. **`R55` (`493.01–505.35 s`, `12.34 s` across 3 cuts):**
   - Uses Chief-accepted 24fps 3-cut cloud passage (`r55_passage_v01_silent.mp4`, SHA-256 `4aa82d0e721988513eba44c38332b5537a9d6f41f9f406ab5d9623b04642483f`) under `J2334`/`J2386`:
     - **Cut 1 (`493.010–496.968 s`):** `r55_cut1_r55b_100x_silent.mp4` (SHA-256 `df6d92d597f73a99c4a6b547fb2573c3c94b3b719888c437721104437574c475`, from `r55b` `1e71287f9a` at `1.00×`).
     - **Cut 2 (`496.968–500.927 s`):** `r55_cut2_r55b_128x_vortex_silent.mp4` (SHA-256 `75adc0df00474f7fa51f8c4f691688753e8cf400e066e6612fb5bc5244bf1cd3`, from `r55b` `1.28×` crop).
     - **Cut 3 (`500.927–505.350 s`):** `r55_cut3_pia01488_pushin_silent.mp4` (SHA-256 `3b606e6edff47e9e4a1f621b208ab75d213ca0a96778a8858b94162c6f168857`, from `PIA01488` `9c49e13d8d` `1.00×` smooth push-in).
   - **Separation Lock:** `code_graphic_033_r55_pressure_gauge.mp4` is **RETIRED** so `R54` (`CODE`: `code_graphic_033_r54_core_vs_cloud_temp.mp4`) is separated from `R59` (`CODE`) by moving world imagery in `R55`–`R58`.

---

## 2. Source Identity & Rights Reconciliation Summary (`43` Pool IDs + Auxiliaries)

All `43` primary pool IDs and auxiliary files were audited against official NASA Images API (`SOURCE_AUDIT_J2299_v01.json`), ESA/Hubble & ESA/Webb records, and Wikimedia Commons API (`EXTERNAL_RECORDS_J2299_v01.json`):

- **All `17` False-Subject Exclusions Enforced (`0` false-subject assignments in `cuts_033_j2299_v01.json`):**
  1. `PIA00271` is Magellan simulated radar Venus, **not** Apollo 17 Blue Marble Earth (`PIA18033` is used for real Earth in `R04`, `R27`, `R05`, and `R14`).
  2. `PIA00141` is Voyager 2 Miranda ridged terrain/fault canyons, **not** Uranus atmospheric limb (restored exclusively to Miranda rows `R56` Cut 1 and `R62` Cut 2).
  3. `PIA01361` is a 5-moon montage strip of Uranian satellites, **not** Uranus polar haze (excluded as a multi-panel montage).
  4. `PIA01364`, `PIA01389` (0 exact NASA API hits; draft Saturn rings), `PIA01390` (Saturn B-ring), and `PIA01486` (Saturn rings) are **Saturn**, not Uranus/Miranda (all 4 excluded).
  5. `PIA01485` is **Io** south polar region, not Miranda Verona Rupes (excluded; `PIA00044` and `PIA00141` serve Miranda cliffs).
  6. `PIA02875` is **Jupiter** 5-micron hot spot, not Uranus seasons (excluded).
  7. `PIA19857` and `PIA19952` are **New Horizons Pluto**, not Uranus aurora/atmosphere (restricted strictly to the spoken Pluto bridge `R66` and end-hold `R67` Cut 1).
  8. `PIA01534`, `PIA01356`, and `PIA00037` depict Uranian moon **Ariel** (`R25`, `R32`, `R33`, `R39`), not Uranus rings or full-system montage.
  9. `PIA01978` depicts **Titania**, not ring dust lanes (excluded; `PIA01350` and `PIA00142` serve ring dust lanes).
  10. `PIA01354` depicts **Miranda** (`R56` Cut 2, `R58` Cut 2), not Uranus true/false colour.
- **Multi-Panel, Labelled, PDF & Third-Party Rights Corrections:**
  - **Multi-panel strips excluded or cropped to single borderless globes:** `PIA01283` (3-panel strip) and `PIA00369` (4-panel strip) are excluded; `PIA00032` (`PIA00032_left_globe.jpg`), `PIA01279` (`PIA01279_left_globe.jpg`, `PIA01279_right_globe.jpg`), `stsci-h-p1906a-f-1028x543` (`stsci-h-p1906a-f_uranus_globe.png`), `GSFC_20171208_Archive_e000100` (`GSFC_20171208_Archive_e000100_right_globe.jpg`), `PIA02963` (`PIA02963_borderless.jpg`), and `ARC-1973-AC73-4189-89` (`ARC-1973-AC73-4189-89_borderless.jpg`) use verified single-globe/borderless crops in `harvest_J2299_v01`.
  - **Baked-label diagrams/stills excluded:** `PIA01975`, `PIA01976`, `PIA01278`, `PIA01281`, `PIA01282`, and cutaway diagram `File:36 Inch Airborne Infrared Telescope (6996884880).jpg` are excluded from `cuts_033_j2299_v01.json`.
  - **Third-party Keck image excluded:** `PIA17306` (credit: Lawrence Sromovsky / UW-Madison / W.M. Keck Observatory, non-blanket NASA PD) is excluded and replaced in `R42`/`R44` by NASA/ESA/STScI Hubble NICMOS `PIA01279` single-globe crops and WFC3 `stsci-h-p1906c-f-514x514.a.png`.
  - **Historical PDF rasters & 1783 document correction:** Both Royal Society PDFs are rasterized at 200 DPI in `harvest_J2299_v01`. `File_Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg_page1.jpg` (`1219×1890`) serves `R11` Cut 3. Because Commons `File:Herschel 1783 Georgium Sidus letter Phil Trans.jpg` (`10.1098/rstl.1783.0001`) is actually Herschel's paper *On the Diameter and Magnitude of the Georgium Sidus* and not the naming letter to Sir Joseph Banks, it is excluded from `R13` (which uses Abbott's 1785 Herschel portrait, Bode's Rijksmuseum portrait, and `PIA18182`).

---

## 3. Active Stills Appearance Ledger in `cuts_033_j2299_v01.json` (`42` Active Stills, All `≤ 2` Appearances)

| # | Filename in `harvest_J2299_v01` | Verified Identity & Provenance | Mini-Readable NAS Path | SHA-256 Prefix | Rows Used | Contiguous Appearances (`picture_qa.py`) |
|---:|---|---|---|---|---|---:|
| 1 | `ARC-1973-AC73-4189-89_borderless.jpg` | NASA Ames Kuiper Airborne Observatory C-141A in flight (borderless crop) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/ARC-1973-AC73-4189-89_borderless.jpg` | `f04c19df8038912a…` | `R18`, `R19` | **1** (`≤ 2`) |
| 2 | `File_Gerard_Kuiper_1964.jpg` | Astronomer Gerard P. Kuiper (1964) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/File_Gerard_Kuiper_1964.jpg` | `8d1dfbfe76c34752…` | `R58` | **1** (`≤ 2`) |
| 3 | `File_Herschel_40_foot_telescope.jpg.jpg` | William Herschel 40-foot telescope engraving (1789) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/File_Herschel_40_foot_telescope.jpg.jpg` | `09057c23bdc16fb8…` | `R10` | **1** (`≤ 2`) |
| 4 | `File_Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg_page1.jpg` | William Herschel Account of a Comet, Philosophical Transactions (1781), page 1 | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/File_Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg_page1.jpg` | `9744042cee7c413e…` | `R11` | **1** (`≤ 2`) |
| 5 | `File_McDonald_Observatory_near_Fort_Davis_part_of_University_of_Texas_at_Austin_04.JPG` | McDonald Observatory domes in the Davis Mountains, Texas | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/File_McDonald_Observatory_near_Fort_Davis_part_of_University_of_Texas_at_Austin_04.JPG` | `1d50aad2adcc0db3…` | `R57` | **1** (`≤ 2`) |
| 6 | `GSFC_20171208_Archive_e000100_right_globe.jpg` | Hubble STIS ultraviolet view of Uranus aurorae (single-globe crop) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/GSFC_20171208_Archive_e000100_right_globe.jpg` | `c47ce78799d1401b…` | `R45`, `R47` | **2** (`≤ 2`) |
| 7 | `KAO_airborne_915_in_flight.jpg` | NASA Kuiper Airborne Observatory C-141A aircraft in flight | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/KAO_airborne_915_in_flight.jpg` | `06f6c3faf40b6510…` | `R19` | **1** (`≤ 2`) |
| 8 | `PIA00032_left_globe.jpg` | Voyager 2 Uranus true-colour single globe (left crop of PIA00032) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00032_left_globe.jpg` | `6ffcb1edc8009914…` | `R11`, `R31` | **2** (`≤ 2`) |
| 9 | `PIA00037.jpg` | Voyager 2 closest-approach view of Uranian moon Ariel | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00037.jpg` | `ab0795fc0f5b54c7…` | `R25`, `R39` | **2** (`≤ 2`) |
| 10 | `PIA00042.jpg` | Voyager 2 colour view of Miranda | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00042.jpg` | `fc8239dc71f1b373…` | `R60`, `R65` | **2** (`≤ 2`) |
| 11 | `PIA00044.jpg` | Voyager 2 close-up of Verona Rupes cliff on Miranda | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00044.jpg` | `1703748b82965a1c…` | `R62`, `R65` | **2** (`≤ 2`) |
| 12 | `PIA00141.jpg` | Voyager 2 close-up of Miranda ridged terrain and canyons | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00141.jpg` | `0490d7266a6a62c8…` | `R56`, `R62` | **2** (`≤ 2`) |
| 13 | `PIA00142.jpg` | Voyager 2 view of Uranus nine known rings | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00142.jpg` | `f667e288b7d90105…` | `R33`, `R49` | **2** (`≤ 2`) |
| 14 | `PIA00143.jpg` | Voyager 2 Uranus ring system back-lit | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00143.jpg` | `f01898cf2636fb81…` | `R07`, `R18` | **2** (`≤ 2`) |
| 15 | `PIA00346.jpg` | Voyager 2 parting view of Uranus crescent | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00346.jpg` | `e01ab238b83014b4…` | `R07`, `R30` | **2** (`≤ 2`) |
| 16 | `PIA01279_left_globe.jpg` | Hubble NICMOS visible-light view of Uranus globe (left crop of PIA01279) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01279_left_globe.jpg` | `1664d3929b8ddef9…` | `R42` | **1** (`≤ 2`) |
| 17 | `PIA01279_right_globe.jpg` | Hubble NICMOS near-infrared view of Uranus cloud bands (right crop of PIA01279) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01279_right_globe.jpg` | `8c9172bd4f13fb0d…` | `R42`, `R44` | **2** (`≤ 2`) |
| 18 | `PIA01280.jpg` | Hubble Space Telescope view of Uranus clouds and rings | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01280.jpg` | `d92dbaf18c810260…` | `R16`, `R34` | **2** (`≤ 2`) |
| 19 | `PIA01350.jpg` | Voyager 2 forward-scattered dust lanes in Uranus rings | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01350.jpg` | `e81d0dd5c44c5cb6…` | `R33`, `R48` | **2** (`≤ 2`) |
| 20 | `PIA01354.jpg` | Voyager 2 view of Miranda full hemisphere | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01354.jpg` | `d4f3c4883b05c62e…` | `R56`, `R58` | **2** (`≤ 2`) |
| 21 | `PIA01356.jpg` | Voyager 2 view of Uranian moon Ariel fault valleys | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01356.jpg` | `c8aa53c979b922c0…` | `R33`, `R39` | **2** (`≤ 2`) |
| 22 | `PIA01391.jpg` | Voyager 2 Uranus crescent in natural colour | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01391.jpg` | `9f97cd7b6b272186…` | `R02`, `R32` | **2** (`≤ 2`) |
| 23 | `PIA01487.jpg` | Voyager 2 false-colour view of Uranus ring system | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01487.jpg` | `c8236841d46f75a7…` | `R30`, `R63` | **2** (`≤ 2`) |
| 24 | `PIA01488.jpg` | Voyager 2 enhanced-colour view of Uranus upper atmosphere | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01488.jpg` | `9c49e13d8da1c052…` | `R27` | **1** (`≤ 2`) |
| 25 | `PIA01490.jpg` | Voyager 2 view of Miranda south polar hemisphere | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01490.jpg` | `d703d20d9a53ad57…` | `R60`, `R67` | **2** (`≤ 2`) |
| 26 | `PIA01492.jpg` | Voyager 2 full-disk view of Neptune | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01492.jpg` | `97b57802f44be221…` | `R36`, `R37` | **1** (`≤ 2`) |
| 27 | `PIA01534.jpg` | Voyager 2 view of Uranian moon Ariel | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01534.jpg` | `fab354bd791efd8c…` | `R25`, `R32` | **2** (`≤ 2`) |
| 28 | `PIA01977.jpg` | Voyager 2 close-up of Uranus rings | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01977.jpg` | `0fb521f190a7ba19…` | `R28`, `R50`, `R51` | **2** (`≤ 2`) |
| 29 | `PIA01984.jpg` | Voyager 2 narrow-angle approach view of Uranus against background starfield | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01984.jpg` | `0079640fa162b60c…` | `R12`, `R16` | **2** (`≤ 2`) |
| 30 | `PIA01985.jpg` | Voyager 2 view of Uranus rings | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01985.jpg` | `fb96f29056d2fa35…` | `R21`, `R53` | **2** (`≤ 2`) |
| 31 | `PIA02963_borderless.jpg` | Hubble Space Telescope Uranus outer rings and moons (borderless crop) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA02963_borderless.jpg` | `c4ca9704656909a4…` | `R09`, `R23` | **2** (`≤ 2`) |
| 32 | `PIA18033.jpg` | Earth Blue Marble from Apollo 17 | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA18033.jpg` | `872e1a5317ac3161…` | `R04`, `R27` | **2** (`≤ 2`) |
| 33 | `PIA18182.jpg` | Voyager 2 Uranus full globe in natural colour | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA18182.jpg` | `3dcc83114f1a25ca…` | `R09`, `R13` | **2** (`≤ 2`) |
| 34 | `PIA18185.jpg` | Voyager 2 view of Miranda icy geology | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA18185.jpg` | `3c63e1c8cdc23475…` | `R63`, `R67` | **2** (`≤ 2`) |
| 35 | `PIA19857.jpg` | New Horizons LORRI/Ralph global view of Pluto | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA19857.jpg` | `fc8e5537ef7a5aee…` | `R66` | **1** (`≤ 2`) |
| 36 | `PIA19952.jpg` | New Horizons high-resolution view of Pluto Tombaugh Regio heart | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA19952.jpg` | `257757c3f7a481a6…` | `R66`, `R67` | **1** (`≤ 2`) |
| 37 | `Portret_van_Johann_Elert_Bode__RP-P-1913-254.jpg.jpg` | Portrait of astronomer Johann Elert Bode (Rijksmuseum RP-P-1913-254) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/Portret_van_Johann_Elert_Bode__RP-P-1913-254.jpg.jpg` | `564726f995cea5d7…` | `R12`, `R13` | **2** (`≤ 2`) |
| 38 | `William_Herschel01_hires.jpg.jpg` | Lemuel Francis Abbott portrait of William Herschel (1785) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/William_Herschel01_hires.jpg.jpg` | `5fed724745acea7e…` | `R10`, `R13` | **2** (`≤ 2`) |
| 39 | `stsci-h-p1906a-f_uranus_globe.png` | Hubble WFC3 view of Uranus north polar cloud hood (single-globe crop) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/stsci-h-p1906a-f_uranus_globe.png` | `f28179ddf2a1c7f7…` | `R36`, `R40` | **2** (`≤ 2`) |
| 40 | `stsci-h-p1906c-f-514x514.a.png` | Hubble WFC3 view of Uranus bright polar cloud cap and methane storm | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/stsci-h-p1906c-f-514x514.a.png` | `dda3dee3e6821c56…` | `R41`, `R44` | **2** (`≤ 2`) |
| 41 | `weic2310a_unannotated.png` | JWST NIRCam Uranus rings and polar cap (weic2310a unannotated) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/weic2310a_unannotated.png` | `e5f7a1a0e10a6e6c…` | `R06`, `R21` | **2** (`≤ 2`) |
| 42 | `weic2332a_hires.jpg` | JWST NIRCam wide-field view of Uranus, rings, and moons (weic2332a) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/weic2332a_hires.jpg` | `b241901c2754e811…` | `R15`, `R50` | **2** (`≤ 2`) |

---

## 4. Delivered `24 fps` Code Graphics Inventory (`19` Active + `1` R26 Alias = `20` MP4s, `0` Frozen Pairs)

All 20 files live on NAS (`/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2299_code_graphics_v01`) and local Mini cache (`/Users/benjaminoats/_desk/cache/J2299/code_graphics_v01`) with verified `SHA256SUMS.txt`.

| # | Row | Filename | Duration (s) | Frames (`@24fps`) | SHA-256 Prefix | Luma / Motion Metrics | Reconciliation & Scale Note |
|---:|---|---|---:|---:|---|---|---|
| 1 | **R03** | `code_graphic_033_r03_winter_counter.mp4` | `5.19` | `125` (`24 fps`) | `0780bbaa7fbc5885…` | `luma=84.12`, `std=39.97`, `frozen=0` | 21-year winter shadow sweep and counter |
| 2 | **R05** | `code_graphic_033_r05_tilt_gauge.mp4` | `7.06` | `169` (`24 fps`) | `c9e38e5af0ff7f84…` | `luma=85.31`, `std=39.81`, `frozen=0` | Earth PIA18033 23.44 deg vs Uranus PIA18182 97.77 deg |
| 3 | **R08** | `code_graphic_033_r08_hook_temp_drop.mp4` | `10.04` | `241` (`24 fps`) | `9467a5224d16cccf…` | `luma=62.08`, `std=55.52`, `frozen=0` | -224.2 C gauge and real Uranus PIA18182 + Neptune PIA01492 |
| 4 | **R14** | `code_graphic_033_r14_diameter_scale.mp4` | `10.39` | `249` (`24 fps`) | `16d31cdb3390231c…` | `luma=84.38`, `std=39.21`, `frozen=0` | True 4:1 diameter scale: 560px Uranus vs four 140px Earths |
| 5 | **R17** | `code_graphic_033_r17_distance_orbit_bar.mp4` | `8.89` | `213` (`24 fps`) | `88068ca864ea0533…` | `luma=74.36`, `std=46.28`, `frozen=0` | 2.9 billion km distance and 84-year orbital ring |
| 6 | **R20** | `code_graphic_033_r20_occultation_trace.mp4` | `13.39` | `321` (`24 fps`) | `91e98e7a806b6ac7…` | `luma=66.92`, `std=39.57`, `frozen=0` | 1977 KAO stellar occultation 5-dip pre/post trace |
| 7 | **R22** | `code_graphic_033_r22_inner_rings.mp4` | `6.51` | `156` (`24 fps`) | `d74fe84050d1f65f…` | `luma=78.08`, `std=52.45`, `frozen=0` | Charcoal-dark inner rings 2% albedo comparison |
| 8 | **R24** | `code_graphic_033_r24_outer_ring_colors.mp4` | `5.46` | `131` (`24 fps`) | `85eff7a5bc273a19…` | `luma=54.33`, `std=47.18`, `frozen=0` | Outer red (Nu) and blue (Mu) rings |
| 9 | **R26** | `code_graphic_033_r26_retrograde_tilt.mp4` | `8.30` | `199` (`24 fps`) | `c5df4c8cda9ee30f…` | `luma=84.27`, `std=39.08`, `frozen=0` | 97.77 deg axial tilt and retrograde spin on real Uranus |
| 10 | **R29** | `code_graphic_033_r29_seasonal_dial.mp4` | `12.44` | `299` (`24 fps`) | `23d84c2756288e59…` | `luma=87.25`, `std=41.74`, `frozen=0` | Option B £0 84-year orbit and 21-year winter dial |
| 11 | **R35** | `code_graphic_033_r35_methane_spectrum.mp4` | `8.16` | `196` (`24 fps`) | `a15846780ff4af7b…` | `luma=60.48`, `std=52.68`, `frozen=0` | 2.3% methane fraction and red-light absorption |
| 12 | **R38** | `code_graphic_033_r38_cold_paradox_bar.mp4` | `10.26` | `246` (`24 fps`) | `1e750b90510094f4…` | `luma=83.5`, `std=35.98`, `frozen=0` | Neptune PIA01492 vs Uranus PIA18182 internal heat flux |
| 13 | **R43** | `code_graphic_033_r43_wind_gauge.mp4` | `6.96` | `167` (`24 fps`) | `67bb643f240ece5c…` | `luma=61.76`, `std=55.22`, `frozen=0` | 900 km/h (560 mph) zonal wind arc |
| 14 | **R46** | `code_graphic_033_r46_corkscrew_magnet.mp4` | `14.12` | `339` (`24 fps`) | `bf2c24cc5584c23e…` | `luma=84.58`, `std=40.13`, `frozen=0` | 58.6 deg magnetic tilt and 1/3 radius offset |
| 15 | **R52** | `code_graphic_033_r52_interior_mantle.mp4` | `13.90` | `334` (`24 fps`) | `c62b9defe25c6d2e…` | `luma=83.83`, `std=38.68`, `frozen=0` | Interior cutaway: outer gas, 80% hot icy fluid, rocky core |
| 16 | **R54** | `code_graphic_033_r54_core_vs_cloud_temp.mp4` | `5.77` | `138` (`24 fps`) | `9e7fc9740a2d0062…` | `luma=83.94`, `std=37.31`, `frozen=0` | Cloud -224.2 C vs core ~5,000 C bar comparison |
| 17 | **R59** | `code_graphic_033_r59_miranda_size_scale.mp4` | `11.30` | `271` (`24 fps`) | `28d2d80557215d7f…` | `luma=78.76`, `std=22.84`, `frozen=0` | True 1:7 scale: Miranda PIA01490 (90px) vs Moon PIA00405 (630px) |
| 18 | **R61** | `code_graphic_033_r61_canyon_depth_scale.mp4` | `8.37` | `201` (`24 fps`) | `9bdc72c389e06435…` | `luma=80.42`, `std=34.04`, `frozen=0` | Verona Rupes 20 km cliff vs 1.6 km Grand Canyon (12x) |
| 19 | **R64** | `code_graphic_033_r64_dual_viewpoint_2024.mp4` | `8.34` | `200` (`24 fps`) | `93272de89fcbffa9…` | `luma=79.75`, `std=51.49`, `frozen=0` | Voyager 2 1986 vs JWST NIRCam dual perspective |
| 20 | **R26_ALIAS** | `code_graphic_033_r26_axial_tilt_97deg.mp4` | `8.30` | `199` (`24 fps`) | `c5df4c8cda9ee30f…` | `luma=84.27`, `std=39.08`, `frozen=0` | Byte-identical alias of code_graphic_033_r26_retrograde_tilt.mp4 |

---

## 5. Automated Gate Verdicts (`picture_qa.py` & `polish_gate.py`)

1. **67-Row Cut List & Pool Check (`picture_qa_033_j2299_cuts_v01.json`):**
   - Verdict: **`PASS`** (`0` failed, `0` warnings across `144` cuts covering `0.00–629.40 s`).
   - Still appearances: max `2` (`≤ 2` lock). Max upscale: `1.92×` (`≤ 2.0×` warn / `≤ 2.35×` fail). Adjacent `CODE` rows: `0`.
2. **24fps Opener + 19 Code Graphics + R55 Passage Review Reel (`j2299_opener_and_graphics_reel_v01_silent.mp4`):**
   - `polish_gate_j2299_reel_v01.json`: **`PASS`** (`0` failed).
   - `picture_qa_j2299_reel_v01.json`: **`PASS`** (`0` failed).
   - Contact sheet: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2299_code_graphics_v01/j2299_graphics_frame_sheet_v01.jpg` (46 tiles showing `25%` Stage 1 and `75%` Stage 2 frames across `R01`, all 19 code graphics, and `R55` Cuts 1–3).
