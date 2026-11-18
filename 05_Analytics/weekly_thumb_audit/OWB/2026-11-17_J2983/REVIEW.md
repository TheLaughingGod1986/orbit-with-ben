# OWB Weekly Thumbnail Audit — Rebuilt Challenger Bs (`J2983` / `J2843`, v03)

- **Date:** 2026-11-17
- **Job:** `J2983` (`macbook`), implementing Packaging Panel synthesis `J2843` (`05_Analytics/tests/panels/owb-j2834-weekly-2026-11-14/DECISION.md`, PR #982)
- **Builder:** `00_Brand/Channel-Setup/tools/build_weekly_thumbs_j2834.py`
- **Status:** Proposed (`T037`, `T038`, `T039` in `05_Analytics/tests/THUMB_LEDGER.json`, reconciled cleanly after `main`'s `T032`/`T033` and `J2834`'s `T034`–`T036` back-fills); parked for Chief gate `J2844` before conditional Studio arming (`J2845`–`J2847`).
- **Prior Drafts Preserved Untouched (`J2834_v02`):**
  - `m09jUdwC5hk_B_v04.jpg` (`647a2b6f6704d7a1c0f3c02b7a855f7a90e33246871973b426806eee5585dc18`)
  - `Mo93x0fxB1Q_B_v04.jpg` (`d4f7b6d242175ef4d7df2769f34c26c9cfc04de6787d7ee8f10ccf77d068bf41`)
  - `ziKBPJ6FY0U_B_v05.jpg` (`bb8d3132b7a556ce2ec2208825c79a3d4ca2fc7643951f05d7459e014036ea51`)

## `thumb_preview.py long --score` Verification (on Staged NAS Files)

```text
/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v03/THUMB_PREVIEW_SCORE_SHEET.jpg
PASS  m09jUdwC5hk_B_v05.jpg  saturation=175.2  near_black=14%
PASS  Mo93x0fxB1Q_B_v05.jpg  saturation=163.8  near_black=10%
PASS  ziKBPJ6FY0U_B_v06.jpg  saturation=165.8  near_black=13%
```

- **Phone & Home Comparison Sheet (`168×94` + `352×198`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v03/PHONE_SHEET_v03.jpg` (`sha256=f0f1d53b05977a77a4e7d1d6f54477a28fadf1806786d35a109036b80ea3c18e`)
- **Score Sheet:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v03/THUMB_PREVIEW_SCORE_SHEET.jpg` (`sha256=6272227a7d5e4840569c7c14074a9be2343d9c9aa38810147c5de7be1700186a`)

---

## Rebuilt Candidates & §2.B Review Gate

### 1. `T037` — `m09jUdwC5hk` (*How Long Will Anything in Space Last?* — Compilation `owb_compilation_v05`)

- **Rebuilt File:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v03/m09jUdwC5hk_B_v05.jpg`
- **SHA-256:** `6f9512774d0d4e3bab181017729dfda396c0612755a4b57bf02810cd62dd8b69` (`263,554` bytes, `1280×720`)
- **Cover Text:** **`RINGS ARE LEAVING`** (`LEAVING` in `#FFE600`, `RINGS ARE` in `#FFFFFF`, `hook_box=[51, 30, 1210, 122]`)
- **Panel Consensus Fixes Applied (`codex.md` + `cursor.md`):**
  - Replaced the flat cyan UV/IR Helix Nebula (`PIA09178`) and passive `ALL STARS FADE` hook with the lossless official NASA/JPL/Space Science Institute Cassini backlit mosaic **`PIA08329` (*In Saturn's Shadow*)**, showing Saturn and its golden-amber backlit rings filling over half the frame (`saturation=175.2`, `near_black=14%`).
  - Aimed one crisp white discovery arrow directly into the inner C/D-ring gap raining inward toward Saturn's equatorial atmosphere (paying off Chapter 1 at `0:53 The Rings Are Leaving` and line 1 of `owb_compilation_v05_description.txt`: *"Saturn's rings are raining into the planet right now"*).
  - Bottom-right duration badge zone (`x>980, y>600`) completely clear.
- **Single-Variable Round 2 Title B (recorded in ledger, held until Round 1 thumbnail test completes):**
  `How Long Will the Universe Last? (Until the Last Star Dies)` (`59` chars; reserve: `When Will Saturn's Rings, the Moon and the Last Star Die?`, `57` chars).
- **§2.B Gate:** **HOOK: PASS** · **BAND: PASS** · **GRADE: PASS** · **PHONE: PASS**

### 2. `T038` — `Mo93x0fxB1Q` (*Why Haven't We Found Aliens Yet? The Fermi Paradox Explained* — `001`)

- **Rebuilt File:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/08_Thumbnails/repackage_2026-11/J2834_v03/Mo93x0fxB1Q_B_v05.jpg`
- **SHA-256:** `95d1a92bd988667743c068e4fe69d67b5d6eeea7097aad2a28de9151d7836578` (`495,044` bytes, `1280×720`)
- **Cover Text:** **`ZERO SIGNALS`** (`ZERO` in `#FFE600`, `SIGNALS` in `#FFFFFF`, `hook_box=[144, 25, 1117, 127]`)
- **Panel Consensus Fixes Applied (`3/3`: `codex.md` + `cursor.md` + `gemini.md`):**
  1. Cropped `PIA12348` full-bleed across `1280×720` with a smooth cosine-feathered top dark-navy gradient (`y=0..192`), completely eliminating the horizontal seam at `y≈72`.
  2. Shifted the bright Galactic Centre core left and moved the yellow search reticle onto the outer dark dust lane (`cx=955, cy=382`, clear of `x>980, y>600`), darkening and desaturating the dust pocket by ~44% with a soft wide feather so the target visibly reads as **empty sky** at `168×94`.
  3. Extended and anchored the Goldstone 70-m DSN antenna (`PIA26716`) cleanly through the bottom-left frame edge (eliminating the slanted corner gap) and pulled highlights down ~13% with a subtle blue sky-side rim light so the parabolic steel mesh retains crisp structural contrast (`saturation=163.8`, `near_black=10%`).
- **Single-Variable Round 2 Title B (kept per `2/3 ≥ 8/10` panel vote):**
  `Fermi Paradox: Why Haven't We Found Aliens Yet?` (`47` chars).
- **§2.B Gate:** **HOOK: PASS** · **BAND: PASS** · **GRADE: PASS** · **PHONE: PASS**

### 3. `T039` — `ziKBPJ6FY0U` (*JWST Found Galaxies That Shouldn't Exist Yet* — `004`)

- **Rebuilt File:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J2834_v03/ziKBPJ6FY0U_B_v06.jpg`
- **SHA-256:** `ffcb7a69ad24434fb2c814682aa58e126de6cb77e047916316b3fb8dd9a14478` (`447,369` bytes, `1280×720`)
- **Cover Text:** **`300 MILLION YEARS`** (`300` in `#FFE600`, `MILLION YEARS` in `#FFFFFF`, tightened letter/word tracking for thicker phone-size strokes, `hook_box=[43, 28, 1219, 124]`)
- **Panel Consensus Fixes Applied (`codex.md` + `gemini.md` + `cursor.md`):**
  - Replaced the foreground `SMACS 0723` gravitational lensing arc and off-target empty-sky circle with the official public-domain NASA/ESA/CSA/STScI **JADES NIRCam deep field & native pullout of `JADES-GS-z14-0`** (`STScI-01HZ083EXXCJNE64ERAH2ER2FM` / `STScI-01HZ08HBSZYHDA52NPPB1BP4SR`, spectroscopically confirmed at `z=14.32`, **~290–300 million years after the Big Bang**).
  - Placed the small yellow origin circle (`[468, 434, 34]`) directly on the exact pixel coordinates of `JADES-GS-z14-0` in the deep field, matched the `4.5×` loupe (`[895, 406, 170]`, bottom `y=576 < 600` clear of duration badge) to that exact compact crimson galaxy source at identical `-28°` roll orientation, dimmed foreground diffraction-spiked star glare by ~32%, and eliminated background posterisation (`saturation=165.8`, `near_black=13%`).
  - **Accurate Script Verification (`02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/01_Script/jwst_script_master_v01.md`, Scene 04, line 143):**
    > *"Some of the galaxies Webb confirmed are luminous when the universe was only about **three hundred million years** old."*
- **Live Title Kept (`2/3 ≥ 8/10`); Single-Variable Round 2 Title B (if ever tested later):**
  `James Webb Telescope: The Galaxies That Shouldn't Exist Yet` (`59` chars; reserve: `Why Did JWST Find Galaxies That Shouldn't Exist Yet?`, `52` chars — drops >60-char drafts and avoids repeating `300 Million Years`).
- **§2.B Gate:** **HOOK: PASS** · **BAND: PASS** · **GRADE: PASS** · **PHONE: PASS**
