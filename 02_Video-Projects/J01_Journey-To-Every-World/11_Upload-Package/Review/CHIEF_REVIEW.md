# J2823 / J2826 — J01 Journey Film 01 Release Upload Package (`11_Upload-Package/`)

**Elected Acting-Chief (`gemini`) Ruling (`J2826`, `2026-11-14`): `PASS` (`KEEP` on pre-upload `11_Upload-Package/` after fixing thumbnail SHA-256/byte/hook metadata in `PACKAGE_MANIFEST.json` and `MEDIA_MANIFEST.json`; Private YouTube upload stays held on Ben's UAT watch `J2222` `awaits_ben`).**

- **Title (A, primary):** `A Calm Journey From Venus to a Dying Star` (41 chars <= 50 chars, LEARNINGS rule 15)
  - **Backup B:** `From Earth to Orion: A 600-Light-Year Space Journey` (51 chars)
  - **Backup C:** `What Happens as You Journey 600 Light-Years From Earth?` (55 chars)
- **Thumbnails (`08_Thumbnail/j01_v01/`, reviewed and visually verified in `J2222` `fd789925ca`, `J2821` `2ff9f5ccd5`, and `J2826`):**
  - **Primary A (`thumb_A_real_venera_mars.jpg`):** `464°C TO -60°C` (`402,683 B`, `SHA-256: 1578850020d005e1130904378df57c59eec09d03c6bb4caae47504b5e52c700b`, `sat=120.1, near_black=10%`)
  - **Variant B (`thumb_B_bright_supergiant_scale.jpg`):** `764× OUR SUN` (`384,325 B`, `SHA-256: 8683d73456275cd868077a02c342b677946f2f9ef5109e66dd4acac9ea90a92e`, `sat=120.5, near_black=2%`)
  - **Variant C (`thumb_C_outward_worlds_lineup.jpg`):** `EARTH TO ORION` (`168,115 B`, `SHA-256: d9434ff33bb95ff572bd2ed47e0b15d76eff093e81db426f42d9996bc3c56d6d`, `sat=155.6, near_black=4%`)
- **Upload gate:** Held (`privacy: "private"`, `schedule: null`) until Ben's UAT watch on `J2222` (`awaits_ben`) passes.

## Deliverables & Verification

1. **Chapters, Description, Sources & Agency Credits (`Chapters/j01_chapters_v01.txt`, `Descriptions/j01_description_v01.txt`):**
   - Exact timestamps verified against `07_Edit-Project/J01_Journey_v01_timeline.json`:
     - `0:00` — A Bubble Two Light-Hours Wide (Cold Open) (`0.000 s`)
     - `0:50` — Part 1: The Ground Moving Under Your Feet — What If Earth Stopped Spinning? (0 km) (`50.162 s`)
     - `8:36` — Part 2: The Twin That Lost Its Water — What Happened to Venus? (40 Million km) (`515.642 s`)
     - `17:10` — Part 3: The Red World Full of Quiet Machines — Could a Robot Survive on Mars? (225 Million km) (`1029.635 s`)
     - `25:17` — Part 4: The Star Heading for Our Outer Edge — Gliese 710 & the Oort Cloud (13,000 AU) (`1517.445 s`)
     - `33:10` — Part 5: Four Light-Years Through the Dark — Reaching Proxima Centauri (4.24 Light-Years) (`1989.848 s`)
     - `41:23` — Part 6: When Your Clock Slows Down — Travelling Near the Speed of Light (0.99c) (`2483.401 s`)
     - `49:28` — Part 7: The Dying Giant That Made Us — Is Betelgeuse About to Explode? (600 Light-Years) (`2967.896 s`)
     - `57:43` — Back to the Ground Under Your Feet (`3463.229 s`)
   - Includes links to all 7 individual films (`6bbbvfCx6zY`, `VBaYRPp85Sw`, `Js6EQJ8qDi8`, `F-jImX5h7ws`, `c5AdqQsnnys`, `rVqgtkBV3jc`, `vP1BbqZ_dnM`), complete `Sources:` block (`Williams 2024`, `Stephenson et al. 2016`, `Donahue et al. 1982`, `Hassler et al. 2014`, `Bailer-Jones 2022`, `Gaia Collaboration 2023`, `Ashby 2003`, `Taylor & Wheeler 1992`, `Joyce et al. 2020`, `Montargès et al. 2021`), complete agency/archive `Image credits:` across `023–029`, and truthful `Pictures:` making-of line (no AI checkers named).
2. **Captions (`Captions/J01_Journey_v03_en-GB.srt`):**
   - `988` cues spanning `0.000–3484.439 s` across the full `3502.300 s` timeline (`8` linking VO segments from `02_Voiceover/J2784_PACE_v01.json` + `7` parent film VO caption timelines `027`, `023`, `025`, `028`, `026`, `024`, `029`).
   - Verified `en-GB` spelling (`kilometres`, `metre`, `vapour`, `centimetres`, `neighbourhood`, `colour`, `travelled`, `modelled`, `sulphuric`), `max_line_len = 42`, `max_lines = 2`, `overlaps = 0`.
3. **Vertical Trailer (`Trailer/j01_trailer_v01.mp4`, `Trailer/make_trailer_v01.sh`, `Review/TRAILER_RECIPE.md`):**
   - `51.000 s` (`1224` frames at `24/1` fps CFR, `608×1080`, H.264/AAC `48 kHz` stereo, `5,500,877 B`, SHA-256 `f3565f50e25061a28bc84e5e40a2a4a03748f024b91f6897e9e80a365aab749e`).
   - Directly watched and listened to (`audio_input` + `moving_video_input`) via `read_file` in `J2826`: Cold Open narration (`00:00–00:50`, `"Every machine humanity has ever landed on another world... It begins right where you are sitting."`) plays cleanly over the centered `16:9` frame (`OUTWARD FROM EARTH` distance map at `00:05`, Venus radar at `00:09`, rover hardware at `00:19`, stellar core shells at `00:28`, `SUNLIGHT 8 MINUTES` map at `00:32`, coastal tide boats at `00:38`, Earth rotation arrows + `"Full film on YouTube"` lower-band CTA at `00:48–00:51`), with two-pass `loudnorm` (`-14.01 LUFS`, `-0.82 dBTP`, `LRA 3.00 LU`).
4. **Manifest & Dry-Run Verification (`PACKAGE_MANIFEST.json`, `PACKAGE_UPLOAD_RESULT_*.json`):**
   - `cd 07_Content-Ops && npm run youtube:package -- --package ../02_Video-Projects/J01_Journey-To-Every-World/11_Upload-Package --video /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/07_Edit-Project/J01_Journey_v03.mp4 --dry-run` → `ok: true`, `dryRun: true`, `sha256: bb93ea1343acde3f9f2f438e04b471e4c13044892b6b0861453839e14c71bb32`.
   - `listing_package.inspect` → `complete: true`, `missing: []`, `status: "Ready to upload"`.
