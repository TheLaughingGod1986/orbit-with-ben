# 033 — Stills Lock & Picture Plan (`STILLS_LOCK_v01.md`)

- **Film:** `033_Why-This-Planet-Has-21-Year-Winters` (*Why This Planet Has 21-Year Winters*)
- **Job:** `J2256` (`033 Uranus: stills lock + OMNI R29/R55 price-pass brief from SHOT_LIST_v01 (no mint, £0)`)
- **Upstream Lock:** `SHOT_LIST_v01.md` (`d67daf94` / OWB PR `#544`, Chief `h94` planning PASS in `jobs/reviews/J2238/REVIEW.md`)
- **Runtime:** `629.40 s` (`10:29.40`) across 67 rows (`R01–R67`) and 5 chapter cards (`3.50 s` breath total)
- **Spend / Generation:** **£0** (no Veo/Omni/Flow/Vertex calls; no plate marked KEEP from filenames alone)

---

## 1. Frame-0 & Opening Picture Lock (`R01`, `0.00–6.22 s`)

1. **Frame 0 (`0.00–2.00 s`) Native Moving Picture Lock:**
   - **Primary moving source:** `PIA01283` (*Hubble NICMOS False-Color Uranus with Moving Clouds and Rings Time-Lapse Sequence*, 28 July 1997, Erich Karkoschka / STScI `PRC97-36b`).
   - **High-res detail companion:** `PIA01280` (*Hubble Views Big Clouds on Uranus*, NICMOS 6-cloud northern spring sequence, `PRC97-36a`).
   - **0:00–0:05 Answer Image Lock:** Frame `0.00 s` opens directly on the real moving Hubble time-lapse sequence of Uranus tipped on its side (`97.77°` axial tilt) with its vertical ring system and bright high-altitude methane clouds rotating around the sunlit pole. No black frame, no fade-from-black at `0.00 s`, no observatory exterior, and no code graphic.
   - **Standalone Short Non-Reuse Proof (`ZpEA8stoSPA`):**
     - The standalone Short *Why Does Uranus Roll On Its Side?* (`ZpEA8stoSPA`, `s4_uranus`) uses NASA SVS `svs20390_shot9_beauty_rings.mp4` (`/Volumes/data/mac-mini-archive/scratch/J1206/raw/Shot9_1k_mp4.mp4`, `2,517,679` bytes, SHA-256 `f964c7f1dd92c5626135f9915ba5d532a3114284cf24115fd393a9756249fb3e`, defined in `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/plates_v02.json`).
     - **`svs20390_shot9_beauty_rings.mp4` is strictly excluded from Film 033** so Frame 0 and all 67 rows of the long film are 100% distinct from the standalone Short open.

---

## 2. Local & NAS Verification of the 43-Asset Pool (`SHOT_LIST_v01.md` §4)

Every local checkout (`/Users/benjaminoats/YouTube/orbit-with-ben`, `/Users/benjaminoats/_desk/cache`, `/private/tmp`) and NAS archive path (`/Volumes/data/mac-mini-archive/`) was audited against the 43-asset pool in `SHOT_LIST_v01.md` §4.

- **Verified on Local Disk or NAS:** **5 of 43** primary pool assets (`#10 weic2310a`, `#12 PIA18182`, `#13 PIA00346`, `#14 PIA00143`, `#15 PIA01391`) + **2 auxiliary assets** (`PIA00405` Earth Moon reference for `R59` code graphic, and canonical `orbit-seedance-reference-16x9-v01.png` for `R29`/`R55`).
- **Missing (to harvest via £0 NASA / STScI / ESA / Wikimedia public-domain APIs):** **38 of 43** primary pool assets (plus `PIA00271` Earth Blue Marble reference used inside `R26` code graphic).

### 2A. Verified Assets on Local Disk / NAS (with SHA-256 & Resolution Notes)

| Pool # | Canonical ID | Title & Agency | Verified Local / NAS Path(s) | Native Dimensions & Size | SHA-256 Digest | Assembler / Resolution Note |
|---|---|---|---|---|---|---|
| **10** | `weic2310a` / `STScI-01GWQDPJTF1MY8ZGN4WBMWMACJ` | JWST NIRCam Uranus with 11 of 13 rings & polar cap (6 Feb 2023; NASA/ESA/CSA/STScI) | **Local PNG (preferred):** `/Users/benjaminoats/_desk/cache/J2089/jwst_v01/uranus_nircam_unannotated.png`<br>**Local Meta:** `/Users/benjaminoats/_desk/cache/J2089/jwst_v01/record.json`<br>**NAS JPEG:** `/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/webb_weic2310a.jpg` | PNG: `2000×2000` (`2,449,044` B)<br>JPG: `1268×1268` (`205,179` B) | PNG: `e5f7a1a0e10a6e6c769b40ecbb2f4dd78ea2ada65f2e96efd69c113ea29f52a7`<br>JPG: `cbe6b51ce9d813f74c0406575f1ed01633459d26aca6e42179ead05bb41c9d8a` | Use the `2000×2000` unannotated PNG (`1.08×` to 1080p height; no baked labels). Locked to **`R06`** & **`R21`** (2 appearances). |
| **12** | `PIA18182` | Voyager 2 Uranus at True-Colour / Natural-Colour Full Globe (Jan 1986; NASA/JPL-Caltech) | **Local 1:** `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/03_Reference-Material/harvest_J2089_v01/PIA18182.jpg`<br>**Local 2:** `/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA18182.jpg`<br>**NAS:** `/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/PIA18182.jpg` | `1720×1720` (`83,489` B)<br>*(Meta JSON: `8d2b75ca...`)* | `3dcc83114f1a25caa1ae1a1436830fffaa15a3e429666dbf4c68bcf035e8932b` | `1720×1720` (`0.63×` to 1080p height; well under `2.0×`). Locked to **`R08`** & **`R30`** (2 appearances). |
| **13** | `PIA00346` | Color Voyager 2 Image Showing Crescent Uranus (25 Jan 1986; NASA/JPL) | **NAS:** `/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/PIA00346.jpg` | `540×800` (`22,673` B) | `e01ab238b83014b428c01bfcf99179d6aee92c767275836a0e24602e1ccb664b` | **Resolution Alert:** Native NASA JPL Photojournal file is `540×800` (not `1600×1600` as estimated in `SHOT_LIST_v01.md` §4). Must composite as a sharp inset at **`≤ 1.85×`** (`≤ 999×1480`) over graded `#050814` starfield + feathered glow so upscale never exceeds `2.0×` (`picture_qa.py` WARN threshold) or `2.35×` (FAIL threshold). Locked to **`R09`** & **`R23`** (2 appearances). |
| **14** | `PIA00143` | Uranus Final Crescent Image — Outbound Toward Neptune (25 Jan 1986; NASA/JPL) | **NAS:** `/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/PIA00143.jpg` | `794×960` (`26,412` B) | `f01898cf2636fb81db534edad198af4031c81274db9e5289f1207d8a982d6cbe` | Native `794×960` (`1.125×` to 1080p height; keep `≤ 1.85×` on `#050814` starfield). Locked to **`R09`** & **`R65`** (2 appearances). |
| **15** | `PIA01391` | Uranus Three-Filter Crescent Sliver (25 Jan 1986; NASA/JPL) | **NAS:** `/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/PIA01391.jpg` | `1000×1000` (`29,274` B) | `9f97cd7b6b272186c75b389112bbfcee555988c5c0720b1138bc072583533b95` | Native `1000×1000` (`1.08×` to 1080p height; keep `≤ 1.85×` on `#050814` starfield). Locked to **`R28`** & **`R65`** (2 appearances). |
| **Aux A** | `PIA00405` | Galileo Earth's Moon Real Globe (used inside `R59` `code_graphic_033_r59_miranda_size_scale.mp4`) | **Local:** `/Users/benjaminoats/_desk/cache/J2089/size_sources_v01/PIA00405.jpg` | `1350×1359` (`408,513` B) | `fc93286c2d73a64f2b095c2e1f1df867b0e96ad0b9515987f9b38fd2ed91a641` | Real Moon globe for `R59` 7-to-1 Moon vs Miranda scale graphic (no flat discs). |
| **Aux B** | `orbit-seedance-reference-16x9-v01.png` | Canonical Orbit 16:9 Seedance Start-Frame Reference (`R29`, `R55`) | **Local:** `/Users/benjaminoats/YouTube/orbit-with-ben/01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png` | `16:9` PNG (`761,432` B) | `922298a14991f128482122ffd91ff48775f96d81ed838d69dc3009b3914f9472` | Required canonical start frame if Chief approves `R29` / `R55` Omni generation (contains no whole planet disc). |

---

### 2B. Missing IDs Only (38 Pool Assets + 1 Code-Graphic Aux ID for £0 Harvest)

Per Deliverable 1 (*"list missing IDs only"*), the following **38 pool IDs** from `SHOT_LIST_v01.md` §4 (plus `PIA00271` for the `R26` Earth-vs-Uranus scale graphic) are not yet on local disk or NAS and must be fetched via £0 public-domain harvest before assembly:

1. `PIA01283` (#1 — Hubble NICMOS Uranus moving clouds & rings time-lapse sequence, `PRC97-36b`)
2. `PIA01280` (#2 — Hubble NICMOS 6 clouds on Uranus, `PRC97-36a`)
3. `File:Herschel_40_foot_telescope.jpg` (#3 — William Herschel's telescope engraving, Wikimedia Commons)
4. `File:William_Herschel01_hires.jpg` (#4 — Lemuel Francis Abbott 1785 portrait of William Herschel, NPG / Wikimedia Commons)
5. `File:Caroline_Herschel-1829.jpg` (#5 — Melchior Gommar Tieleman 1829 portrait of Caroline Herschel, Wikimedia Commons)
6. `File:Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg` (#6 — Royal Society *Phil. Trans.* Vol. 71 p. 492 title page, 26 April 1781)
7. `File:Herschel_1783_Georgium_Sidus_letter_Phil_Trans.jpg` (#7 — Herschel letter to Sir Joseph Banks naming *Georgium Sidus*, *Phil. Trans.* Vol. 73, 1783)
8. `File:Portret_van_Johann_Elert_Bode,_RP-P-1913-254.jpg` (#8 — Johann Elert Bode portrait engraving, Rijksmuseum / Wikimedia Commons)
9. `File:Martin_Heinrich_Klaproth_portrait.jpg` (#9 — Martin Heinrich Klaproth portrait engraving, Wikimedia Commons)
10. `weic2332a` / `STScI-01HGG9F546W7BDCRK3N9WRWT9Z` (#11 — JWST NIRCam wide/close 4-filter Uranus with inner/outer rings & moons, 18 Dec 2023)
11. `PIA17306` (#16 — Voyager 2 departure artwork / trajectory context, NASA/JPL)
12. `KAO_airborne_915_in_flight` / `ARC-1979-AC79-0334` (#17 — NASA Gerard P. Kuiper Airborne Observatory C-141A `N714NA` in flight, NASA Ames)
13. `ARC-1973-AC73-4189-89` (#18 — NASA KAO 36-inch / 91.4 cm airborne infrared telescope cavity & cabin interior, NASA Ames)
14. `PIA01534` (#19 — Hubble ACS Uranus ring system & dark-band clouds, Aug 2003, Showalter & Lissauer)
15. `PIA01364` (#20 — Voyager 2 Uranus Rings in False Colour showing 9 main rings + epsilon ring, 1986)
16. `PIA01356` (#21 — Voyager 2 Cordelia and Ophelia shepherd moons flanking epsilon ring, 21 Jan 1986)
17. `PIA01978` (#22 — Voyager 2 backlit dust lanes in Uranus rings, 24 Jan 1986, `236 s` exposure)
18. `PIA01361` (#23 — Voyager 2 False-Colour Polar Haze Over Uranus South Pole, Jan 1986)
19. `PIA01278` (#24 — Hubble WFPC2 Four Major Uranian Moons & Rings, 1997)
20. `PIA01279` (#25 — Hubble NICMOS Uranus Cloud System & Ring Plane Sequence, 1997)
21. `PIA18033` / `heic1424a` (#26 — Hubble WFC3 Monster Storms on Uranus, Nov 2014)
22. `PIA02875` (#27 — Hubble WFPC2 4-Panel Seasonal Roll of Uranus 1994–1998)
23. `PIA01492` (#28 — Hubble WFPC2 Uranus Clouds and Ring System in Four Infrared Filters, Aug 1998)
24. `PIA00369` / `STScI-PRC06-42a` (#29 — Hubble ACS Dark Cloud in Atmosphere of Uranus, 23 Aug 2006)
25. `PIA01975` / `STScI-PRC06-47a` (#30 — Hubble ACS Ariel and Its Shadow Crossing Uranus, 26 July 2006)
26. `PIA02963` / `STScI-PRC07-32a` (#31 — Hubble WFPC2 Edge-On Ring Crossing at 2007 Equinox, Aug 2007)
27. `PIA19857` / `heic1116a` (#32 — Hubble WFC3 Uranus Auroral Bright Spots & Ring System, Nov 2011)
28. `PIA01354` (#33 — Voyager 2 True & False-Colour Side-by-Side Comparison of Uranus, 17 Jan 1986)
29. `PIA00141` (#34 — Voyager 2 Uranus Upper Atmosphere & High-Altitude Methane Haze Limb, 1986)
30. `PIA00037` (#35 — Voyager 2 Uranus with Major Moons Montage, 1986)
31. `PIA01486` (#36 — Voyager 2 Miranda High-Resolution Global Mosaic, 24 Jan 1986)
32. `PIA01490` (#37 — Voyager 2 Miranda Nine-Image South Polar Mosaic, 24 Jan 1986)
33. `PIA01488` (#38 — Voyager 2 Miranda Inverness Corona "The Chevron", 24 Jan 1986)
34. `PIA01389` (#39 — Voyager 2 Miranda Elsinore Corona & Ridged Terrain, 24 Jan 1986)
35. `PIA01390` (#40 — Voyager 2 Miranda Arden Corona Grooves and Troughs, 24 Jan 1986)
36. `PIA01485` (#41 — Voyager 2 Verona Rupes Ice Cliff on Miranda Limb, 24 Jan 1986)
37. `PIA00032` (#42 — Voyager 2 Verona Rupes Perspective View, 24 Jan 1986)
38. `PIA19952` (#43 — Hubble WFC3 Dynamic Atmosphere of Uranus at 20-Year Mark, 2015)
- **Code-Graphic Auxiliary ID to include in £0 harvest:** `PIA00271` (Apollo 17 Blue Marble Earth globe used inside `R26` `code_graphic_033_r26_axial_tilt_97deg.mp4` for the 4-Earth-diameters scale comparison).

---

## 3. Stills-Lock & Picture-Plan Rules (`≤ 2` Appearances Across All 67 Rows)

To guarantee `picture_qa.py` passes with **0 `STILL_REUSE` fails** (every still plate appears at most **2 times** across `0.00–629.40 s`; back-to-back cuts with no intervening plate count as 1 appearance, and non-contiguous cuts count as separate appearances), the following explicit row locks govern `cuts.json` and assembly:

### 3A. Five Explicit Row-Reconciliations from `SHOT_LIST_v01.md` §3 vs §4

1. **`weic2310a` vs `weic2332a` vs `PIA01490` (`R06`, `R15`, `R21`, `R50`, `R67` — `SHOT_LIST_v01.md` line 170):**
   - In `SHOT_LIST_v01.md` §3, `R06` listed both `weic2310a` (Cut 1) and `weic2332a` (Cut 2), while `weic2310a` also appeared in `R21` and `R67` Cut 3, and `weic2332a` also appeared in `R15` and `R50`.
   - **Locked Allocation (`≤ 2` appearances each):**
     - **`weic2310a`** (`/Users/benjaminoats/_desk/cache/J2089/jwst_v01/uranus_nircam_unannotated.png`):
       - Appearance 1: **`R06`** (`25.03–31.55 s`, `6.52 s` — both sub-cuts `25.03–28.29 s` wide zoom-in and `28.29–31.55 s` polar-cap drift use `weic2310a` contiguously).
       - Appearance 2: **`R21`** (`176.72–183.37 s`, `6.65 s` — inner/outer ring resolve).
     - **`weic2332a`** (`STScI-01HGG9F546W7BDCRK3N9WRWT9Z`):
       - Appearance 1: **`R15`** (`117.52–122.67 s`, `5.15 s` — post-Ch-1-breath JWST wide-field beauty).
       - Appearance 2: **`R50`** (`444.70–453.80 s`, `9.10 s` — JWST infrared upper-atmosphere heat glow).
     - **`PIA01490`** (*Miranda 9-Image South Polar Mosaic*):
       - Appearance 1: **`R60`** (`551.84–557.99 s`, `6.15 s` — Miranda full south-polar mosaic).
       - Appearance 2: **`R67` Cut 3** (`623.40–629.40 s`, `6.00 s` — replaces `weic2310a` on the final Miranda cliff/mosaic recall + end-hold).

2. **`PIA01280` Standalone Still Plate vs `R01` Native Motion & `CODE` Globes (`R01`, `R16`, `R34`):**
   - **`R01`** (`0.00–6.22 s`) is logged in `cuts.json` under native motion sequence **`PIA01283`** (`source_type: "native_motion"`, with `PIA01280` composited only inside the `PIA01283` time-lapse render).
   - **`PIA01280`** as a standalone still plate (`source_type: "nasa_still"`) is locked to:
     - Appearance 1: **`R16`** (`122.67–127.12 s`, `4.45 s`).
     - Appearance 2: **`R34`** (`293.78–304.09 s`, `10.31 s`).
   - Where `PIA01280` provides the real planet globe texture inside bespoke `CODE` renders (`R26`, `R35`, `R43`, `R64`), each row is logged in `cuts.json` under its own `code_graphic_033_rNN_*.mp4` filename (`source_type: "code_graphic"`), never as a raw `PIA01280` still cut.

3. **Non-Contiguous Same-Row / Adjacent-Row Pairs (`Bode` in `R12`/`R13`, `PIA00369` in `R39`/`R40`):**
   - `SHOT_LIST_v01.md` §4 noted `Bode` (`R12, R13`) and `PIA00369` (`R39, R40`) as `1 (2 rows)`. Because another plate sits between their two cuts (`R13` Cut 1 `File:William_Herschel01_hires.jpg` sits between `R12` Cut 3 and `R13` Cut 2; `R39` Cut 2–3 `PIA01975` sits between `R39` Cut 1 and `R40` Cut 1), `picture_qa.py` counts each pair as **2 separate appearances**. Since neither asset is used anywhere else in the film, both sit cleanly at **`2` appearances (`≤ 2` PASS)**.

4. **Contiguous Cross-Row Pairs (`ARC-1973-AC73-4189-89` in `R18→R19`, `PIA01492` in `R36→R37`, `PIA19952` in `R66→R67`):**
   - `ARC-1973-AC73-4189-89` runs at the end of `R18` (Cut 2–3, `147.92–154.38 s`) and opens `R19` (Cut 1, `155.08–157.39 s` after the `0.70 s` Ch 1→Ch 2 card breath). Even if `picture_qa.py` splits across the chapter card, that is at most **2 appearances (`≤ 2` PASS)**.
   - `PIA01492` runs at the end of `R36` (Cut 3, `320.78–325.68 s`) and directly into `R37` (Cut 1–2, `325.68–332.39 s`) with no intervening source = **1 continuous appearance** (or at most 2 if split by row, `≤ 2` PASS).
   - `PIA19952` runs at the end of `R66` (Cut 2, `605.80–611.40 s`) and directly into `R67` (Cut 1, `611.40–617.40 s`) with no intervening source = **1 continuous appearance** (or at most 2 if split by row, `≤ 2` PASS).

5. **`R55` £0 Fallback Plate Selection (`493.01–505.35 s`):**
   - If Chief selects the **£0 fallback** for `R55` (`[ORBIT ACTS]` Beat 2) instead of `OMNI`, `SHOT_LIST_v01.md` §3 suggested `PIA01361` + `PIA01354`. However, `PIA01361` already has 2 appearances (`R25`, `R56` Cut 1) and `PIA01354` already has 2 appearances (`R56` Cut 2, `R58`).
   - **Stills-Lock Rule for `R55` £0 Fallback:**
     - **Cut 1 (`493.01–497.10 s`):** Use **`PIA00141`** (*Voyager 2 Uranus Upper Atmosphere & High-Altitude Methane Haze Limb*, which otherwise has only **1** appearance in `R62` Cut 2 → becomes **2 appearances**).
     - **Cut 2–3 (`497.10–505.35 s`):** Use **`PIA01361`** (*Voyager 2 False-Colour Polar Haze Over Uranus South Pole*), which flows **contiguously** into `R56` Cut 1 (`505.35–509.60 s`, also `PIA01361`) so `R55 Cut 2–3 + R56 Cut 1` forms a single contiguous stretch = **2 total appearances** (`R25` and `R55–R56`).
     - Result: Even under the £0 fallback for `R55`, **every still in Film 033 stays at `≤ 2` appearances**.

---

## 4. Complete 43-Asset Locked Appearance Ledger (`≤ 2` Cap Check)

| # | Canonical ID | Status | Locked Standalone Row(s) in `cuts.json` | Standalone Appearances (`picture_qa.py`) | Upscale / Framing Lock |
|---|---|---|---|---|---|
| 1 | `PIA01283` | MISSING (harvest) | `R01`, `R33` (`native_motion` time-lapse) | 2 (motion) | Native time-lapse composited on `#050814` starfield (`≤ 1.85×`) |
| 2 | `PIA01280` | MISSING (harvest) | `R16`, `R34` (plus globe texture inside `R01`, `R26`, `R35`, `R43`, `R64` renders) | **2** (`R16`, `R34`) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 3 | `File:Herschel_40_foot_telescope.jpg` | MISSING (harvest) | `R03`, `R05` (Cut 1) | **2** | Full 16:9 crop (`≤ 1.35×`), warm 1781 grade |
| 4 | `File:William_Herschel01_hires.jpg` | MISSING (harvest) | `R04`, `R13` (Cut 1) | **2** | 16:9 crop + feathered dark vignette (`≤ 1.35×`) |
| 5 | `File:Caroline_Herschel-1829.jpg` | MISSING (harvest) | `R05` (Cut 2) | **1** | 16:9 crop + feathered dark vignette (`≤ 1.50×`) |
| 6 | `File:Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg` | MISSING (harvest) | `R10`, `R11` (Cut 1) | **2** | Warm parchment grade (`≤ 1.35×`) |
| 7 | `File:Herschel_1783_Georgium_Sidus_letter_Phil_Trans.jpg` | MISSING (harvest) | `R11` (Cut 2), `R12` (Cut 1–2) | **1** (contiguous `R11→R12`) | Warm parchment grade (`≤ 1.35×`) |
| 8 | `File:Portret_van_Johann_Elert_Bode,_RP-P-1913-254.jpg` | MISSING (harvest) | `R12` (Cut 3), `R13` (Cut 2) | **2** (separated by `R13` Cut 1) | Warm archival engraving grade (`≤ 1.35×`) |
| 9 | `File:Martin_Heinrich_Klaproth_portrait.jpg` | MISSING (harvest) | `R13` (Cut 3), `R14` (Cut 2) | **2** (separated by `R14` Cut 1) | Warm archival engraving grade (`≤ 1.50×`) |
| 10 | `weic2310a` / `STScI-01GWQDPJTF1MY8ZGN4WBMWMACJ` | **VERIFIED LOCAL & NAS** | **`R06`** (Cut 1–2), **`R21`** | **2** (`R06`, `R21`) | Use local `2000×2000` unannotated PNG (`1.08×`) |
| 11 | `weic2332a` / `STScI-01HGG9F546W7BDCRK3N9WRWT9Z` | MISSING (harvest) | **`R15`**, **`R50`** | **2** (`R15`, `R50`) | Native 4K JWST wide-field (`< 1.0×`) |
| 12 | `PIA18182` | **VERIFIED LOCAL & NAS** | `R08`, `R30` (`R02` if £0 fallback replaces `R08` or shares `≤ 2`) | **2** (`R08`, `R30`) | Local `1720×1720` (`0.63×`); note: if `R02` uses £0 fallback, use `PIA01279` or `PIA18182` contiguous with `R08` Analysis below |
| 13 | `PIA00346` | **VERIFIED NAS** | `R09` (Cut 1), `R23` (Cut 2) | **2** (`R09`, `R23`) | **Native `540×800`: lock inset at `≤ 1.85×` on `#050814` starfield** |
| 14 | `PIA00143` | **VERIFIED NAS** | `R09` (Cut 2), `R65` (Cut 2) | **2** (`R09`, `R65`) | Native `794×960`: lock inset at `≤ 1.85×` on `#050814` starfield |
| 15 | `PIA01391` | **VERIFIED NAS** | `R28`, `R65` (Cut 1) | **2** (`R28`, `R65`) | Native `1000×1000`: lock inset at `≤ 1.85×` on `#050814` starfield |
| 16 | `PIA17306` | MISSING (harvest) | `R09` (Cut 3) | **1** | Logged as `WARN` artist concept on `picture_qa_review.jpg` |
| 17 | `KAO_airborne_915_in_flight` (`ARC-1979-AC79-0334`) | MISSING (harvest) | `R17`, `R18` (Cut 1) | **1** (contiguous `R17→R18`) | 16:9 crop (`≤ 1.35×`) |
| 18 | `ARC-1973-AC73-4189-89` | MISSING (harvest) | `R18` (Cut 2–3), `R19` (Cut 1) | **2** (across Ch 1→Ch 2 breath) | 16:9 crop (`≤ 1.35×`) |
| 19 | `PIA01534` | MISSING (harvest) | `R19` (Cut 2), `R24` (Cut 1) | **2** (`R19`, `R24`) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 20 | `PIA01364` | MISSING (harvest) | `R22` (Cut 1), `R24` (Cut 2) | **2** (`R22`, `R24`) | 16:9 crop (`≤ 1.50×`) |
| 21 | `PIA01356` | MISSING (harvest) | `R22` (Cut 2) | **1** | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 22 | `PIA01978` | MISSING (harvest) | `R23` (Cut 1), `R24` (Cut 3) | **2** (`R23`, `R24`) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 23 | `PIA01361` | MISSING (harvest) | `R25`, `R56` (Cut 1) *(+ `R55` Cut 2–3 contiguous into `R56` Cut 1 if `R55` £0)* | **2** (`R25`, `R55–R56`) | 16:9 crop (`≤ 1.50×`) |
| 24 | `PIA01278` | MISSING (harvest) | `R27` (Cut 1), `R58` (Cut 2) | **2** (`R27`, `R58`) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 25 | `PIA01279` | MISSING (harvest) | `R27` (Cut 2), `R33` (Cut 2) | **2** (`R27`, `R33`) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 26 | `PIA18033` / `heic1424a` | MISSING (harvest) | `R31`, `R41` (Cut 1) | **2** (`R31`, `R41`) | 16:9 crop (`≤ 1.35×`) |
| 27 | `PIA02875` | MISSING (harvest) | `R36` (Cut 1–2), `R41` (Cut 2) | **2** (`R36`, `R41`) | 16:9 crop (`≤ 1.50×`) |
| 28 | `PIA01492` | MISSING (harvest) | `R36` (Cut 3), `R37` (Cut 1–2) | **1** (contiguous `R36→R37`) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 29 | `PIA00369` / `STScI-PRC06-42a` | MISSING (harvest) | `R39` (Cut 1), `R40` (Cut 1) | **2** (separated by `R39` Cut 2–3) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 30 | `PIA01975` / `STScI-PRC06-47a` | MISSING (harvest) | `R39` (Cut 2–3), `R40` (Cut 2) | **2** (separated by `R40` Cut 1) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 31 | `PIA02963` / `STScI-PRC07-32a` | MISSING (harvest) | `R42`, `R44` (Cut 1) | **2** (`R42`, `R44`) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 32 | `PIA19857` / `heic1116a` | MISSING (harvest) | `R44` (Cut 2), `R49` | **2** (`R44`, `R49`) | 16:9 crop (`≤ 1.35×`) |
| 33 | `PIA01354` | MISSING (harvest) | `R56` (Cut 2), `R58` (Cut 1) | **2** (`R56`, `R58`) | 16:9 crop (`≤ 1.50×`) |
| 34 | `PIA00141` | MISSING (harvest) | `R62` (Cut 2) *(+ `R55` Cut 1 if `R55` £0 fallback)* | **1** (or **2** if `R55` £0) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 35 | `PIA00037` | MISSING (harvest) | `R57` (Cut 1–2), `R66` (Cut 1) | **2** (`R57`, `R66`) | 16:9 crop (`≤ 1.35×`) |
| 36 | `PIA01486` | MISSING (harvest) | `R58` (Cut 3), `R60` (Cut 1) | **2** (`R58`, `R60`) | 16:9 crop (`≤ 1.35×`) |
| 37 | `PIA01490` | MISSING (harvest) | **`R60` (Cut 2)**, **`R67` (Cut 3)** | **2** (`R60`, `R67`) | 16:9 crop (`≤ 1.35×`) |
| 38 | `PIA01488` | MISSING (harvest) | `R61` (Cut 1), `R63` (Cut 1) | **2** (`R61`, `R63`) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 39 | `PIA01389` | MISSING (harvest) | `R61` (Cut 2) | **1** | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 40 | `PIA01390` | MISSING (harvest) | `R61` (Cut 3), `R63` (Cut 2) | **2** (`R61`, `R63`) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 41 | `PIA01485` | MISSING (harvest) | `R62` (Cut 1), `R63` (Cut 3) | **2** (`R62`, `R63`) | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 42 | `PIA00032` | MISSING (harvest) | `R62` (Cut 2 / £0 fallback for `R62`) | **1** | Sharp inset `≤ 1.85×` over `#050814` starfield |
| 43 | `PIA19952` | MISSING (harvest) | `R66` (Cut 2), `R67` (Cut 1) | **1** (contiguous `R66→R67`) | 16:9 crop (`≤ 1.35×`) |

### 4A. Note on Optional `VEO (flag)` £0 Fallback Plate Caps (`R02`, `R51`, `R62`)

Because `R02`, `R51`, and `R62` default to **£0 NASA/archival plates** unless Chief separately approves Veo generation:
- **`R02` (`6.22–13.09 s`) £0 Fallback:** To keep `PIA18182` (`R08`, `R30`) and `weic2310a` (`R06`, `R21`) at exactly 2 appearances each, `R02` £0 fallback uses **`PIA01283`** Cut 2 (`6.22–9.65 s`, continuing `R01` contiguously so `R01→R02 Cut 1` = 1 contiguous appearance of `PIA01283`) + **`File:Caroline_Herschel-1829.jpg`** or **`PIA01389`** / **`PIA00141`** (each currently at 1 appearance), **OR** `R08` swaps to `PIA00141` so `PIA18182` serves `R02` and `R30` (2 appearances). **Locked preference for `R02` £0 fallback:** Use `PIA18182` in `R02` (`6.22–13.09 s`) and `R30` (`252.30–262.14 s`) = **2 appearances**, and assign **`PIA00141`** (*Voyager 2 Uranus pale cyan atmospheric limb*) to `R08` (`38.28–47.41 s`) and `R55` Cut 1 (`493.01–497.10 s`) = **2 appearances**.
- **`R51` (`453.80–465.28 s`) £0 Fallback:** Uses graded deep-space Voyager 2 outbound plate **`PIA17306`** (currently 1 appearance in `R09` Cut 3 → becomes **2 appearances**) + bespoke animated 3D magnetic dipole & `59°` offset axis overlay (`code_graphic` overlay over moving plate, flanked by non-CODE `R50` and `R52` `CODE`). Wait: since `R52` (`465.28–475.15 s`) is a `CODE` row (`code_graphic_033_r52_magnetic_offset_59deg.mp4`), `R51` **must remain `source_type: "nasa_still"`** (never `code_graphic`, so no two `CODE` rows run back-to-back!). Therefore `R51` £0 fallback is strictly a moving camera move across `PIA17306` (Cut 1–2) + `File:Caroline_Herschel-1829.jpg` / `PIA01356` (2nd appearance of `PIA01356`, Cut 3) with standard edit-level lower-third text only, keeping `R51` as real/archival plate footage before `R52` `CODE`.
- **`R62` (`570.42–582.89 s`) £0 Fallback:** Uses **`PIA01485`** (Cut 1, `570.42–574.60 s`) + **`PIA00032`** (Cut 2–3, `574.60–582.89 s`) with the edit-level Verona Rupes `20 km` / `12 minutes` free-fall counter overlay (`source_type: "nasa_still"`, sitting cleanly between `R61` `NASA` and `R63` `NASA`). Both `PIA01485` (`R62`, `R63`) and `PIA00032` (`R62` only) remain `≤ 2` appearances.
