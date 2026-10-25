# J0921 Thumbnail Route and Provenance (0 Credits)

All three A/B/C cover variants for **029 Betelgeuse** (*Is Betelgeuse About to Explode?*) were built at **0 credits (£0)** by `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/08_Thumbnail/build_betelgeuse_covers_v01.py` using approved project harvest plates (`07_Edit-Project/harvest_v01/`) and Pillow/NumPy compositing + colour grading (`THUMBNAIL_AND_TITLE_RULES.md` §2, §2.A, §2.B). No paid image generation API, Flow, or Vertex call was invoked.

## Variants

1. **Variant A — `BRIGHT AS MOON` (yellow hook word: `MOON`)**
   - **Layout:** Top band (`BRIGHT AS MOON`, Arial Black 114 pt, cap height 82 px = 11.4% of 720p height), ESO VLT/SPHERE January 2019 resolved Betelgeuse image (`sphere_jan.jpg`, `eso2003b`, CC BY 4.0) on the left (`cx=370, cy=445`), NASA/GSFC First Quarter Moon (`half_moon.jpg`, public domain) on the right (`cx=930, cy=435`) with earthshine-lifted night side and sunlit golden-ivory terminator.
   - **Score (`thumb_preview.py --score`):** `saturation=140.1`, `near_black=6.0%`, `PASS` (0 fails).

2. **Variant B — `PAST MARS` (yellow hook word: `MARS`)**
   - **Layout:** Left clear-edge band (`PAST` / `MARS`, Arial Black 118 pt, cap height 84 px = 11.7% of 720p height), ESO VLT/SPHERE Betelgeuse (`sphere_jan.jpg`, `eso2003b`, CC BY 4.0) large on the right (`cx=895, cy=380`, clear of the 028 `STAR VISITOR` top-band layout), with NASA DSCOVR EPIC Earth (`dscovr_epic.jpg`, public domain) and NASA SDO HMI Continuum Sun (`sdo_hmi_continuum.jpg`, public domain) in the lower-left as the scale reference (`THUMBNAIL_AND_TITLE_RULES.md` §2.A.5 & §2.A.8).
   - **Score (`thumb_preview.py --score`):** `saturation=150.1`, `near_black=10.2%`, `PASS` (0 fails).

3. **Variant C — `IT WAS DUST` (yellow hook word: `DUST`)**
   - **Layout:** Top band (`IT WAS DUST`, Arial Black 114 pt, cap height 82 px = 11.4% of 720p height), ESO/ESA/Hubble Great Dimming dust cloud impression (`dust_impression.jpg`, `heic2014a` / `eso2003`, CC BY 4.0, credit `ESO, ESA/Hubble, M. Kornmesser`) center-right (`cx=790, cy=435`) with NASA Apollo 17 Blue Marble Earth (`blue_marble.jpg`, `AS17-148-22727`, public domain) at lower-left (`cx=235, cy=495`) as observer vantage scale reference.
   - **Score (`thumb_preview.py --score`):** `saturation=143.3`, `near_black=7.1%`, `PASS` (0 fails).

## Hard-Fail & Packaging Checks (§2.B)

- **No Orbit:** Verified on all three variants (`no Orbit on long thumbs`).
- **HOOK:** Names the consequence/scale/finding (`BRIGHT AS MOON`, `PAST MARS`, `IT WAS DUST`), complements and never repeats the title *Is Betelgeuse About to Explode?*, no vague questions or threat framing.
- **BAND:** 2–3 words in a top band (A, C) or left edge band (B); zero pixel overlap between text bounding boxes and any hero/scale-reference bounding box; zero overlap with the bottom-right YouTube duration badge (`[1080, 620, 1280, 720]`).
- **GRADE:** All three pass `thumb_preview.py long ... --score` with mean HSV saturation 140.1–150.1 (≥ 120 target) and near-black 6.0%–10.2% (≤ 30% cap).
- **PHONE:** Every word verified readable at `168×94` in `Review/thumb_preview_v01.jpg` and alongside 028 (`STAR VISITOR`) in `Review/owb_family_sheet_v01.jpg`.
