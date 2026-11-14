# OWB Weekly Thumbnail Audit — Design Review Brief (`J2834`, 14 November 2026)

- **Date:** 2026-11-14
- **Job:** `J2834` (`macbook-2`)
- **Builder:** `00_Brand/Channel-Setup/tools/build_weekly_thumbs_j2834.py`
- **Status:** Proposed (`T035`, `T036`, `T037` in `05_Analytics/tests/THUMB_LEDGER.json`); awaiting independent Packaging Panel (`owb-j2834-weekly-2026-11-14`) + Chief PASS before any YouTube Studio Test & Compare arming.
- **Shared NAS Review Bundle (mounted on both Mini and MacBook):**
  - `168×94` + `352×198` Live A vs Proposed B Phone Sheet: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v02/PHONE_SHEET_v02.jpg` (`sha256=98b44bf69eae5b7850981e5a282a96335363ad1b2aac41c8fa73762f85accea1`)
  - `thumb_preview.py` Score Sheet: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v02/THUMB_PREVIEW_SCORE_SHEET.jpg` (`sha256=d8280407c98c00fc657d6d986b621552b2d6a455ed5f8b5d39f0daf0e7e18ac8`)
  - Manifest: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v02/DESIGN_MANIFEST.json`

---

## Why These Three Videos Were Selected

Across all 21 public and scheduled Orbit With Ben long films on 14 November 2026:
- **13 longs** currently have an active or scheduled Test & Compare running in Studio (`3xrxdmaOwJI`, `rVqgtkBV3jc`, `vP1BbqZ_dnM`, `h8HGfyShEHI`, `G5uMANXHtNU`, `Yk1tLh23rko`, `c5AdqQsnnys`, `6bbbvfCx6zY`, `-jmMROGoZCM`, `ojk-dfOpAmw`, `VBaYRPp85Sw`, `55AEQwvs36g`, `Js6EQJ8qDi8`) — preserved untouched per the Never list.
- **2 longs** (`2fsQcea-voM` Moon and `b8-X_FyJnHM` Alien Worlds) already hold Chief-approved `J2676` `B_v02` candidates (`T024`, `T026`) recorded on 12 November (`J2702`).
- **2 longs** (`F-jImX5h7ws` Star Visitor scheduled 29 Nov and `NbW5G1BpPY0` Europa) already PASS all thumbnail style gates (`sat=223.5/black=9.4%` and `sat=100.4/black=4.3%`).
- Of the remaining 4 untested public longs (`m09jUdwC5hk`, `Mo93x0fxB1Q`, `ziKBPJ6FY0U`, `REXYxuLOBoI`) whose prior 14-day tests finished inconclusive (`draw` — `"Not enough impressions to declare a winner"`), the **3 weakest by CTR + style failure** are:
  1. **`m09jUdwC5hk`** (*How Long Will Anything in Space Last?*): **28d 93 impr / 0.00% CTR** (lifetime 0.0% CTR); Style FAIL (near-duplicate red-dwarf `THE LAST LIGHT` concept, no focal pointer/scale).
  2. **`Mo93x0fxB1Q`** (*Why Haven't We Found Aliens Yet? The Fermi Paradox Explained*): **lifetime 97 impr / 0.0% CTR**; Style FAIL (`near_black=42.1% > 30%`, 1-word vague `SILENCE` centred directly over subject).
  3. **`ziKBPJ6FY0U`** (*JWST Found Galaxies That Shouldn't Exist Yet*): **lifetime 130 impr / 1.5% CTR**; Style FAIL (`near_black=39.9% > 30%`, no yellow hook word, vague `TOO EARLY?` overlapping telescope).

---

## Candidate Summary & `thumb_preview.py --score` Gate

```text
PASS  m09jUdwC5hk_B_v04.jpg  saturation=202.5  near_black=5%
PASS  Mo93x0fxB1Q_B_v04.jpg  saturation=167.3  near_black=6%
PASS  ziKBPJ6FY0U_B_v05.jpg  saturation=142.1  near_black=6%
```

Every candidate applies the 12 November `J2456` / `J2701` lessons: **100% real NASA public-domain photography** (no flat vector illustrations, no fake planetary scale like Earth inside a 2.5-light-year nebula, no ungrounded numbers), **2–3 words in the clean upper-22% top band** with 1 yellow word (`#FFE600`), **one variable per test** (thumbnail-only Test & Compare with baseline title unchanged; separate Title-Only B recorded for a subsequent round), and bottom-right duration-badge zone (`x>980, y>600`) completely clear.

---

### 1. `T035` — `m09jUdwC5hk` (*How Long Will Anything in Space Last?* — Compilation `owb_compilation_v05` / `005`)

- **Live Baseline A:**
  - Title (`37` chars): `How Long Will Anything in Space Last?`
  - Cover Text: `THE LAST LIGHT`
  - File: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v02/m09jUdwC5hk_live_A.jpg` (`sha256=d86457f3a6d6b96dc448a7ac72840d4e341b6e5e95eb52d91b00cf5741a6bcef`)
  - Problem: `0.00%` CTR on 93 28d impressions; visually indistinguishable from `REXYxuLOBoI` (*The Last Star* `LAST LIGHT`).
- **Proposed Challenger B (Thumbnail-Only Test & Compare, Title Unchanged):**
  - Cover Text: **`ALL STARS FADE`** (`FADE` in `#FFE600`, `ALL STARS` in `#FFFFFF`, top band `y=29..127`)
  - File: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v02/m09jUdwC5hk_B_v04.jpg`
  - SHA-256: `647a2b6f6704d7a1c0f3c02b7a855f7a90e33246871973b426806eee5585dc18` (`287,186` bytes, `1280×720`)
  - Gate Score: **PASS** (`saturation=202.5`, `near_black=5%`)
  - Source Plate: NASA/JPL-Caltech `PIA09178` (Spitzer infrared + GALEX ultraviolet Helix Nebula — real dying Sun-like star shedding outer gas shells around its central white-dwarf core; public domain) + crisp white pointer arrow (`draw_arrow`) highlighting the white-dwarf remnant at the eye's centre. No false Earth/planet scale overlay.
  - Script & Package Reference: `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/11_Upload-Package/owb_compilation_v05/PACKAGE_MANIFEST.json`, `02_Video-Projects/005_The-Last-Star-In-The-Universe/01_Script/`.
- **Separate Title-Only B Proposal (held for subsequent single-variable test):**
  - `How Long Will Everything in Space Last? (10 Trillion Years)` (`59` chars)

---

### 2. `T036` — `Mo93x0fxB1Q` (*Why Haven't We Found Aliens Yet? The Fermi Paradox Explained* — `001_Will-We-Ever-Meet-Aliens`)

- **Live Baseline A:**
  - Title (`60` chars): `Why Haven't We Found Aliens Yet? The Fermi Paradox Explained`
  - Cover Text: `SILENCE`
  - File: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/08_Thumbnails/repackage_2026-11/J2834_v02/Mo93x0fxB1Q_live_A.jpg` (`sha256=8355ef032a8967fb13c0aaff91f8d859a901f3926894e6c339c0ed1df796a877`)
  - Problem: `0.0%` lifetime CTR on 97 impressions; `near_black=42.1% > 30%` cap; 1-word `SILENCE` sits directly across the middle of the frame.
- **Proposed Challenger B (Thumbnail-Only Test & Compare, Title Unchanged):**
  - Cover Text: **`ZERO SIGNALS`** (`ZERO` in `#FFE600`, `SIGNALS` in `#FFFFFF`, top band `y=29..127`)
  - File: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/08_Thumbnails/repackage_2026-11/J2834_v02/Mo93x0fxB1Q_B_v04.jpg`
  - SHA-256: `d4f7b6d242175ef4d7df2769f34c26c9cfc04de6787d7ee8f10ccf77d068bf41` (`524,432` bytes, `1280×720`)
  - Gate Score: **PASS** (`saturation=167.3`, `near_black=6%`)
  - Source Plates:
    1. NASA/JPL-Caltech/ESA/CXC/STScI `PIA12348` (Great Observatories Hubble + Spitzer + Chandra Milky Way Galactic Centre composite, public domain).
    2. NASA/JPL-Caltech `PIA26716` (real Goldstone Deep Space Network 70-meter radio telescope photograph, sky keyed cleanly and anchored bottom-left below `y=720`) aimed at a crisp empty yellow search reticle (`cx=875, cy=420`) on the Galactic Centre star cloud. Directly echoes Astrum's 119k/day 11 Nov hit (`MS8eLbSvb3c`, `RARE SIGNAL` over Milky Way core) while paying off our spoken Fermi Paradox script (`02_Video-Projects/001_Will-We-Ever-Meet-Aliens/01_Script/aliens_script_v01.md`).
- **Separate Title-Only B Proposal (held for subsequent single-variable test):**
  - `Fermi Paradox: Why Haven't We Found Aliens Yet?` (`47` chars — front-loads the search term `Fermi Paradox` and cuts 13 chars).

---

### 3. `T037` — `ziKBPJ6FY0U` (*JWST Found Galaxies That Shouldn't Exist Yet* — `004_JWST-Discoveries-That-Change-Everything`)

- **Live Baseline A:**
  - Title (`44` chars): `JWST Found Galaxies That Shouldn't Exist Yet`
  - Cover Text: `TOO EARLY?`
  - File: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J2834_v02/ziKBPJ6FY0U_live_A.jpg` (`sha256=a25ab9578e3d583bb826597ee52e631bb902ed3c5e2a82f3d307d72751e24adc`)
  - Problem: `1.5%` lifetime CTR on 130 impressions; `near_black=39.9% > 30%` cap; all-white `TOO EARLY?` has no yellow accent word and overlaps the telescope mirror.
- **Proposed Challenger B (Thumbnail-Only Test & Compare, Title Unchanged):**
  - Cover Text: **`300 MILLION YEARS`** (`300` in `#FFE600`, `MILLION YEARS` in `#FFFFFF`, top band `y=33..123`)
  - File: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J2834_v02/ziKBPJ6FY0U_B_v05.jpg`
  - SHA-256: `bb8d3132b7a556ce2ec2208825c79a3d4ca2fc7643951f05d7459e014036ea51` (`368,332` bytes, `1280×720`)
  - Gate Score: **PASS** (`saturation=142.1`, `near_black=6%`)
  - Source Plate: NASA/ESA/CSA/STScI `webb_first_deep_field.jpg` (real Webb's First Deep Field SMACS 0723 NIRCam photograph, public domain) + `4.5×` magnified circular loupe (`zx=890, zy=405`, bottom edge `y=573` clear of duration badge) connected by a white pointer arrow from the source crimson high-redshift galaxy and gravitational lensing arc.
  - Spoken Script Verification: Verified verbatim against `02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/01_Script/jwst_script_master_v01.md` Scene 04 (`"Galaxies that existed just three hundred million years after the Big Bang — bright, massive, already containing billions of stars."`).
- **Separate Title-Only B Proposal (held for subsequent single-variable test):**
  - `James Webb Telescope: Galaxies 300 Million Years After the Big Bang` (`67` chars) or `JWST Found Giant Galaxies 300 Million Years After the Big Bang` (`62` chars).

---

## Studio Arming Guardrail (`Never` List Compliance)

All three videos (`m09jUdwC5hk`, `Mo93x0fxB1Q`, `ziKBPJ6FY0U`) currently retain finished, inconclusive 14-day Test & Compare reports (`T018`, `T005`, `T007`, `"Not enough impressions to declare a winner"`) in YouTube Studio, all read back and recorded in `THUMB_LEDGER.json` today (`2026-11-14`). Per `AGENTS.md` and `J2702`, conditional Studio arming jobs queued after the Packaging Panel Decision **must** perform a fresh read-only Studio check first, preserve any running test, and press `New test` → `Continue` over a recorded finished `draw` report **only when the Chief's PASS explicitly authorizes starting the successor test** (exactly as Chief authorized on `T030`/`T031` in `J2449`/`J2737`).
