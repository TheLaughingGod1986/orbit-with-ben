# OWB:064 Thumbnail & Packaging Manifest — `J3817` (`J3719_v02`)

- **Episode:** `OWB:064` — *Every Planet Explained in 12 Minutes (Mercury to Neptune)* *(Lead Title A per `J3719` `DECISION.md`)*
- **Job:** `J3817` (`gemini`, specialist worker fallback on `--kind thumb`) implementing `05_Analytics/tests/panels/owb-064-every-planet/DECISION.md` (`J3719`, 2-of-2 consensus from `codex.md` `J3716` and `gemini.md` `J3717`; `cursor.md` `J3718` cancelled after 24 h cutoff)
- **Schedule:** Pre-assembly (`J3023`); Ben watch deadline **Fri 11 Dec 2026 18:00 London**; planned air slot **Wed 16 Dec 2026 18:00 London**
- **Spend:** `£0.00` cash, `0` Flow/Vertex credits (Pillow/Python composition strictly from verified real NASA/JPL/ESA spacecraft plates already on `studio-live`; zero Orbit character; zero paid generation)
- **Locked assets untouched:** All `v01` thumbnails, `BUILD_REPORT_v01.md`, `THUMB_SCORES_v01.json`, `SHOT_LIST_v01.md`, and locked VO (`every_planet_explained_vo_v01.wav`, `4b478fcd...`, `683.86 s`) left 100% unmodified.
- **No YouTube / Studio changes:** No upload, no scheduling, and no Studio Test & Compare armed here (`T045` remains `status: "proposed"`, `video: null` in `05_Analytics/tests/THUMB_LEDGER.json` until after `J3818` QA, Chief PASS, Ben UAT watch, and upload).
- **Builder script:** `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/08_Thumbnail/build_064_thumbs_v02.py`

---

## 1. Provenance Fix (`PIA00271` Removed Everywhere)

- **`PIA00271` rejected:** Verified via NASA Photojournal (`https://science.nasa.gov/resource/venus-computer-simulated-global-view-of-the-northern-hemisphere/`) as *"Venus - Computer Simulated Global View of the Northern Hemisphere"* (Magellan radar mosaic simulation, `picture_qa` `KIND_FAIL`). Removed from Thumbnails A & B and replaced in `SHOT_LIST_v02.md` Row `R09`.
- **Verified replacement on Thumbnails A & B:** Real Mariner 10 Venus sulfuric-acid cloud imagery already harvested on `studio-live`: `harvest_J3022_v01/PIA23791.jpg` (`sha256=853268f7922ea572a0966df4a378e6b54221102d6740bdc78f4011708ee71007`), cropped strictly to the **right-hand colour-enhanced globe** (`x = 1160..2245`) cleanly away from the central white divider.

---

## 2. Rebuilt `J3719_v02` Thumbnails (`1920x1080`, `thumb_preview.py long --score` PASS)

Output directory on NAS:
`/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/08_Thumbnail/J3719_v02/`

| Variant | File (under `J3719_v02/`) | Top-Band Hook (`y=0..21%`, `#FFE000` yellow hook word) | Composition & Key Fixes | `thumb_preview --score` | Exact SHA-256 |
|---|---|---|---|---|---|
| **A (Lead Arm 1)** | `064_thumb_A_extreme_worlds_v02.jpg` | `8` (white) + `EXTREME` (`#FFE000`) + `WORLDS` (white) | Deep-navy cosmic backdrop (`18.1%` near-black; removed flat periwinkle gradient, white paint dots, and black cutout halos). Clear focal hierarchy: Juno Jupiter (`PIA22946`) + illuminated Cassini Saturn with full uncolliding rings (`PIA11141`) dominating `>35%` of lower-centre/mid; crisp Apollo 17 Blue Marble Earth (`PIA18033`) anchor lower-left; remaining real NASA worlds (`PIA15162` Mercury, `PIA23791` right-globe Mariner 10 Venus, `PIA00407` Mars, `PIA18182` Uranus, `PIA01492` Neptune) spaced cleanly along a depth arc. **Editorial lineup, not to scale.** Bottom-right (`x>75%, y>78%`) clear. | **PASS** (`sat=172.3`, `near_black=18.1%`) | `bc1b60dbacf405e9ef2c2bf169f5442cea1e5312dd56ceade96560c73fb2e393` |
| **B (Challenger B)** | `064_thumb_B_venus_uranus_v02.jpg` | `464°C` (`#FFE000`, left) \| `-224°C` (white, right, custom bold minus bar legible at `168x94`; `"TO"` dropped) | Real Mariner 10 Venus clouds (`PIA23791` right globe) on left graded warm golden-amber at moderate saturation (`161.5`, strictly `<= 175`, zero Sun look) vs real Voyager 2 Uranus (`PIA18182`, 033 shelf) crisp ice-cyan on right matching `-224.2 °C` coldest planetary atmosphere (Ch 7). Both globes shifted below clean dark-navy top band (`y=0..21%`); white divider starts strictly below top band (`y=232`) with zero letter overlap. Crisp Apollo 17 Earth (`PIA18033`) on lower-centre seam for scale; bottom-right clear. *(Description explicitly distinguishes Venus's `464 °C` surface heat from Uranus's `−224.2 °C` atmospheric minimum.)* | **PASS** (`sat=161.5`, `near_black=19.5%`) | `29ea71dab31ab13efa723d5257856324be02a91e96f1aaa47783f3a395b34c75` |
| **C (Challenger C — Rule 19)** | `064_thumb_C_real_nasa_saturn_v02.jpg` | `REAL` (`#FFE000`) + `NASA PHOTOS` (white) | 3-panel triptych scrapped completely. Single uncropped, aspect-preserved real NASA Cassini Saturn-and-rings hero frame (`PIA11141.jpg`) filling `>40%` of frame over deep-navy graded space (zero top-bar leak, zero dark-disc artifact, stray corner moon removed). Framed Apollo 17 Earth (`PIA18033`, `132 px` diameter circular scale inset, `~1.76×` enlarged over strict `1:9.45` ratio for `168x94` phone legibility) on lower-left with one thin white `§2.B.4` pointer arrow pointing at Earth; top-band text completely off Saturn and its rings; bottom-right clear. | **PASS** (`sat=180.6`, `near_black=18.1%`) | `4ec5544c4fd9a7e9338bb207be936c90ec2d0683eb307e45d3224aa7458903f1` |

- **Combined phone-size preview sheet (`168x94` + `360x202`):**
  `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/08_Thumbnail/J3719_v02/064_thumbs_ABC_v02_preview_sheet.jpg`
  - SHA-256: `22ac3dfb600b8d514e76d923c2f05f697023d26e95405d01b2cdb798bad73160` (`173,117` bytes)
- **Machine scores & hashes JSON:** `08_Thumbnail/THUMB_SCORES_v02.json` (mirrored to NAS `J3719_v02/THUMB_SCORES_v02.json`).
- **Visual inspection (`1920x1080` + `168x94`):** All three variants and the combined preview sheet were visually inspected directly: every word (including `-224°C`'s bold minus bar) reads cleanly at `168x94`, zero letters touch planets or dividers, zero black cutout halos remain, zero Orbit appears, and bottom-right duration zones are clear.

---

## 3. Approved Packaging Text Reference (from `J3719` `DECISION.md`, for `J3023` Upload Package)

- **Lead Title A (`57` chars — zero word overlap with all three `v02` thumbnails):**
  `Every Planet Explained in 12 Minutes (Mercury to Neptune)`
- **Reserves:**
  - `B (53 chars): Every Planet Explained: 430°C Ice to Supersonic Winds` *(never pair with Thumb B)*
  - `C (53 chars): Every Planet Explained: From Mercury's Ice to Neptune`
  - `D (45 chars): Every Planet Explained: A Tour in NASA Images` *(never pair with Thumb C)*
- **Description opening block (for `J3023` `11_Upload-Package/`):**
  > Every planet explained in 12 minutes — a fact-checked tour of all eight worlds in our Solar System from Mercury's hidden polar ice to Neptune's supersonic winds, built with real NASA, ESA, and spacecraft imagery alongside clear scale comparisons.
  >
  > Travel outward from 0.4 AU to 30 AU across all eight planets: compare Venus's 464 °C surface heat with Uranus's −224.2 °C atmospheric minimum, see why Jupiter has no solid ground, and trace the spacecraft missions that revealed each world.
- **Tightened listing chapters (`J3719`, verified against `J3023` export):**
  - `0:00` Mercury — Ice at 430 °C
  - `1:22` Venus — Why It Burns
  - `2:38` Earth — What Shields Our Oceans
  - `4:12` Mars — The Frozen Robot Desert
  - `5:25` Jupiter — What Happens If You Land?
  - `6:47` Saturn — Vanishing Rings & Polar Hexagon
  - `8:17` Uranus — Why Winter Lasts 21 Years
  - `9:45` Neptune — Supersonic Winds at the Edge

---

## 4. Next Steps

- `J3818`: Independent exact-file QA review of `J3719_v02` thumbnails and `SHOT_LIST_v02.md` before Chief PASS and `J3023` assembly.
