# J3337 Cover v02 Review Handoff — 7 Dec 2026 Roman Telescope First Images Dated-Event Short

- **Job:** `J3337` (`Roman Telescope 7 Dec dated-event Short: rebuild cover v02 only (opaque spacecraft, no galaxy bleed-through), thumb_preview, park for Chief`, `kind: thumb`)
- **Parent Build & Chief Ruling:** `J3331` / `jobs/reviews/J3331/REVIEW.md` (`22 Nov 2026`: **`VIDEO v01 KEEP` (LOCKED)** / **`COVER v01 FIX`**)
- **Spend:** **`£0` / `0` credits** (cover-only rebuild from existing public-domain NASA SVS `#15081` & `#5587` assets)
- **Upload / Schedule / Studio Changes:** **None** (parked for Chief visual review before UAT staging and `jobs.py awaits J3331`)

## 1. Defect Fixed

In `assemble_j3331.py:460`, `build_cover_image()` blended `42%` of the Hubble Ultra Deep Field additively across the full frame without masking the spacecraft (`comp = np.clip(a_h + a_u * 0.42, 0, 255)`), causing orange/blue galaxies to shine through the metallic hull and white sunshield of NASA's Roman Space Telescope.

`build_cover_v02.py` builds **`11_Upload-Package/roman_2026_12_07_cover_v02.jpg`** (`1080×1920`, `368,454` bytes) directly from the clean, unlabelled NASA Goddard SVS `#15081` Milky Way hero frame (`frame 55` of the `36.0 s` Roman sweep, cropped strictly inside `x <= 863, y <= 1620` with zero bottom-right `"Animation"` credit) with **zero additive Hubble UDF overlay**:
- **100% solid, opaque Roman Space Telescope** metallic hull and bright white sunshield — zero galaxy bleed-through or double-exposure ghosting anywhere on the spacecraft.
- **Clean NASA SVS `#5587` full Moon disc** (`frame 7864`, `205×205 px` at `(774, 672)`) with a subtle outer lunar glow, positioned cleanly inside the `16:9` centre crop (`y = 656..1264`) and well clear of the spacecraft body.
- **Bold house typography:** `**100** / HUBBLES` (yellow `100`, white `HUBBLES`, 2 words, zero words shared with title *What Will NASA's Roman Telescope Reveal on Dec 7?*).

## 2. Automated Gate & Visual Verification

- **`thumb_preview.py short --score` (`0` — PASS):**
  ```text
  /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_dated_shorts/2026-12-07_roman-telescope-first-images/07_Edit-Project/assembly_j3331_v01/qa/cover_v02_thumb_preview.jpg
  PASS  roman_2026_12_07_cover_v02.jpg  saturation=101.2  near_black=18%
  ```
- **Direct Visual Inspection (`image_input` via `read_file`):**
  - Inspected full-size `11_Upload-Package/roman_2026_12_07_cover_v02.jpg` (`1080×1920`) and `07_Edit-Project/assembly_j3331_v01/qa/cover_v02_thumb_preview.jpg` (`110×196` tile + `168×94` centre `16:9` crop).
  - Confirmed 100% opaque spacecraft hull and sunshield with zero galaxy bleed-through, crisp full Moon inside the `16:9` crop with margin above and below, vibrant Milky Way backdrop, and instant phone legibility for `100 / HUBBLES`.
- **Locked `v01` Integrity Check:** All **57/57** files in `DELIVERY_v01_SHA256.json` — including locked video `06_Final-Exports/owb_dated_2026_12_07_roman_first_images_v01.mp4` (`ff52475588e5ecee1caca6840105711bfed2b67c6b83ab3f08239e3761e47bd1`) and untouched `11_Upload-Package/roman_2026_12_07_cover_v01.jpg` (`c17ac08de15dac4ac383e846374f8bd52059b14175ff985c7341f06bfb52c305`) — remain verified byte-for-byte untouched.

## 3. NAS Delivery & SHA-256 (`DELIVERY_v01_cover_v02_SHA256.json`)

Base folder: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_dated_shorts/2026-12-07_roman-telescope-first-images/`

| Deliverable | Relative Path | Bytes | SHA-256 |
|---|---|---:|---|
| **Locked Video `v01` (untouched)** | `06_Final-Exports/owb_dated_2026_12_07_roman_first_images_v01.mp4` | `68,281,951` | `ff52475588e5ecee1caca6840105711bfed2b67c6b83ab3f08239e3761e47bd1` |
| **New Cover `v02`** | `11_Upload-Package/roman_2026_12_07_cover_v02.jpg` | `368,454` | `fecf983184783f57874b8fd330baf9f894041e805673827463ea4507225155d3` |
| **Cover `v02` Phone Preview** | `07_Edit-Project/assembly_j3331_v01/qa/cover_v02_thumb_preview.jpg` | `33,931` | `ba33b5c7853deeac93ccc05083865c21589f2603b0746b6d33ccc00412965f61` |
| **Untouched Cover `v01` (superseded)** | `11_Upload-Package/roman_2026_12_07_cover_v01.jpg` | `706,400` | `c17ac08de15dac4ac383e846374f8bd52059b14175ff985c7341f06bfb52c305` |

## 4. Next Step (Parked for Chief Visual Review)

1. Chief visually inspects `roman_2026_12_07_cover_v02.jpg` and `cover_v02_thumb_preview.jpg`.
2. On `KEEP`, Chief merges this metadata PR, stages locked `owb_dated_2026_12_07_roman_first_images_v01.mp4` + `roman_2026_12_07_cover_v02.jpg` to OWB UAT / `WATCH_FULL` (SHA-256 verified), and arms `jobs.py awaits J3331` for Ben's watch (due **Wed 2 Dec 2026 18:00 London** ahead of **Thu 3 Dec 2026 11:30 London** publish; Related `ziKBPJ6FY0U`; if missed, do not upload).
