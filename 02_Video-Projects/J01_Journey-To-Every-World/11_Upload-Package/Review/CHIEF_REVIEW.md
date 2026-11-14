# J2823 — J01 Journey Film 01 Release Upload Package (`11_Upload-Package/`)

**Worker draft (`gemini`). No final OK, PASS, merge, YouTube upload, or scheduling decision made.**

- **Title (A):** `A Calm Journey From Venus to a Dying Star` (41 chars)
  - **Backup B:** `From Earth to Orion: A 600-Light-Year Space Journey` (51 chars)
  - **Backup C:** `What Happens as You Journey 600 Light-Years From Earth?` (55 chars)
- **Thumbnails (`08_Thumbnail/j01_v01/`, reviewed in `J2222` `fd789925ca`):**
  - **Primary A (`thumb_A_real_venera_mars.jpg`):** `VENUS TO A DYING STAR` (`SHA-256: ab44fa3fb16ca8d4e97c52a0500894f97bb3d3247fb62b10539eb038ef799c00`)
  - **Variant B (`thumb_B_bright_supergiant_scale.jpg`):** `700 TIMES OUR SUN` (`SHA-256: ff6701a4ba47a078177fc7c9a92a235e9d91a5195bbac25ad5eb51b32e62e3cc`)
  - **Variant C (`thumb_C_outward_worlds_lineup.jpg`):** `7 WORLDS IN 1 HOUR` (`SHA-256: 610e9463e67edef2836a3c033262f9d130a41a6477092b2852002849e131b470`)
- **Upload gate:** Held (`privacy: "private"`, `schedule: null`) until Ben's UAT watch on `J2222` (`awaits_ben`) passes.

## Deliverables & Verification

1. **Chapters, Description, Sources & Agency Credits (`Chapters/j01_chapters_v01.txt`, `Descriptions/j01_description_v01.txt`):**
   - Exact timestamps verified against `07_Edit-Project/J01_Journey_v01_timeline.json`:
     - `0:00` — A Two-Light-Hour Bubble (Cold Open)
     - `0:50` — Part 1: Earth's Rotation (0 km — Ground Zero)
     - `8:36` — Part 2: Venus (38 Million km — 2 Light-Minutes)
     - `17:10` — Part 3: Mars (225 Million km — 12.5 Light-Minutes)
     - `25:17` — Part 4: Gliese 710 & The Oort Cloud (0.16 Light-Years — 10,000 AU)
     - `33:10` — Part 5: Proxima Centauri (4.24 Light-Years — 40 Trillion km)
     - `41:23` — Part 6: Near the Speed of Light (Relativistic Interstellar Flight)
     - `49:28` — Part 7: Betelgeuse (548 Light-Years — Orion's Shoulder)
     - `57:43` — Looking Back Across 600 Light-Years
   - Includes links to all 7 individual films (`6bbbvfCx6zY`, `VBaYRPp85Sw`, `Js6EQJ8qDi8`, `F-jImX5h7ws`, `c5AdqQsnnys`, `rVqgtkBV3jc`, `vP1BbqZ_dnM`), complete `Sources:` block (`Williams 2024`, `Stephenson et al. 2016`, `Donahue et al. 1982`, `Hassler et al. 2014`, `Bailer-Jones 2022`, `Gaia Collaboration 2023`, `Ashby 2003`, `Taylor & Wheeler 1992`, `Joyce et al. 2020`, `Montargès et al. 2021`), complete agency/archive `Image credits:` across `023–029`, and truthful `Pictures:` making-of line (no AI checkers named).
2. **Captions (`Captions/J01_Journey_v03_en-GB.srt`):**
   - `988` cues spanning `0.000–3484.439 s` across the full `3502.300 s` timeline (`8` linking VO segments from `04_Audio/J2784_PACE_v01.json` + `7` parent film VO caption timelines `027`, `023`, `025`, `028`, `026`, `024`, `029`).
   - Verified `en-GB` spelling (`kilometres`, `metre`, `vapour`, `centimetres`, `neighbourhood`, `colour`, `travelled`, `modelled`, `sulphuric`), `max_line_len = 42`, `max_lines = 2`, `overlaps = 0`.
3. **Vertical Trailer (`Trailer/j01_trailer_v01.mp4`, `Trailer/make_trailer_v01.sh`, `Review/TRAILER_RECIPE.md`):**
   - `51.000 s` (`1224` frames at `24/1` fps CFR, `608×1080`, H.264/AAC `48 kHz` stereo, SHA-256 `f3565f50e25061a28bc84e5e40a2a4a03748f024b91f6897e9e80a365aab749e`).
   - Cut from `J01_Journey_v03.mp4` Cold Open (`0.000–50.125 s`, holding final cold-open frame to `51.000 s` before Chapter Card 1), full 16:9 frame (`608×342`) centered on blurred/darkened `608×1080` moving background, `"Full film on YouTube"` lower-band CTA from `47.50 s`, two-pass `loudnorm` (`-14.01 LUFS`, `-0.82 dBTP`, `LRA 3.00 LU`).
4. **Manifest & Dry-Run Verification (`PACKAGE_MANIFEST.json`, `PACKAGE_UPLOAD_RESULT_2026-11-14T13-16-32-505Z.json`):**
   - `cd 07_Content-Ops && npm run youtube:package -- --package ../02_Video-Projects/J01_Journey-To-Every-World/11_Upload-Package --video /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/07_Edit-Project/J01_Journey_v03.mp4 --dry-run` → `ok: true`, `dryRun: true`, `sha256: bb93ea1343acde3f9f2f438e04b471e4c13044892b6b0861453839e14c71bb32`.
   - `python3 scripts/listing_package.py 02_Video-Projects/J01_Journey-To-Every-World/11_Upload-Package` → PASS (exit 0).
