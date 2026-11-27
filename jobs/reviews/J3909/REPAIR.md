# J3909 — OWB 064 trailer and package repair

Worker: macbook-2. Package repair for independent J3910 recheck; no package PASS or UAT release.

## Replacement

`11_Upload-Package/Trailer/064_every_planet_explained_trailer_v05.mp4` on studio-live:
SHA-256 `e57cd79a668d558e2ee451f31b85bb81b515d3169150484112b73bd2b57646ce`, 8,800,139 bytes.
608×1080, exact 24/1 CFR, video start PTS 0, 888 frames / 37 seconds. Full decode succeeded.
Original trailer `771d1f2a368ad4dbe1ee7b4cb541b0422a8d4d739ae946a8923f5ae9a4fe3cff` preserved.
Worker candidates v02 and v04 were rejected at boundary inspection; preserved on NAS and never selected in final manifest. v03 was not copied to NAS.

Ten vertical opening cuts rebuilt on exact frame intervals in TRAILER_BUILD.json. The original master was not rendered or edited. True NASA globe images remain completely inside the vertical margins; source maps fill the frame. No cropped horizontal progress strip or graph survives. Bars animate inside the margins; numerical labels do not interpolate through false values.

44 extracted stills inspected: frame 0, each cut's boundary/adjacent frames, interior frames in the three flagged intervals, and the end card. Frame numbers: 0,12,83,84,85,170,171,172,223,224,225,274,275,276,359,360,361,396,451,452,453,454,480,530,531,532,533,576,617,618,619,620,650,703,704,705,750,787,788,789,790,816,852,876. Final sheet is local at `J3909-evidence/v05_inspection_sheet.jpg` under the slot2 worker folder (not committed: no media in git). Independent reviewer should extract the same frames from the NAS v05.

The old-overlay method exposed one-frame flashes at boundaries; final recipe instead builds one continuous 789-frame opening before concatenating the original end-card frames. Original end-card pictures, title, fades and ordering are retained from normalized source frame 789 onward; 24 fps quantizes the nominal 4.15-second end card to the available frames. Original AAC packets are copied, not encoded: the full 37-second ADTS SHA-256 is identical (`audio_identity.json`), proving both opening and end-card audio unchanged. No hearing or moving-playback perception is claimed.

## Spoken facts

Locked script v04, SOURCES_v03.md Mercury row, and locked Scribe word times checked. The 15–18.875s callout is **UP TO 7× / brighter**, matching “up to seven times brighter” at 15.54–16.98s; the 22.167–25.792s callout is **−180 °C / at night**, matching minus one hundred and eighty degrees Celsius at 22.38–25.04s. No animated intermediate temperature from the long or the review's −164 example was copied. 1965 and Giuseppe Colombo match the locked next sentence. Numerical facts rechecked at https://science.nasa.gov/mercury/facts/ (NASA Mercury Facts; temperatures, distance and sunlight sections). The scene index 01/08 is packaging, not a new scientific claim.

## Package corrections

- Added all three active Earth/ISS assets, with actual file hashes and exact cut intervals; moved retired r42a asset to rejected with no active intervals. Every cut source now has an active provenance row (zero missing).
- Added explicit Le Verrier, Galle and Lassell credits. Exact Commons source pages and file hashes are in PORTRAIT_CREDITS_J3909.json; original portrait creators are unknown, not falsely credited to uploaders. Le Verrier's page lists Magnus Manske as uploader; its historical source is Smithsonian Libraries via Wikipedia. Galle is unknown photographer, 1880 (Commons PD-old-90 / US pre-1931). Lassell is unknown photographer, 19th century, Steinicke collection (Commons PD-old; file cleanup by Supportstorm). Source pages checked 27 Nov 2026.
- CSV normalized to LF; manifest categoryId 28; exact versioned trailer path/hash/size recorded.
- Description 3,707 characters, preserving PIA18033 NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring credit.

## Immutable checks and remaining gate

`locked_hashes.json`: master d59057ae, locked script 556f3c8d, VO 4b478fcd, R11 PIA00215 46dc965a and all J3719_v02 thumbnails/preview hash-match. Cuts unchanged, including R11 interval. No active PIA00271/PIA00233; original source exclusions unchanged. T045 remains proposed, video null. No spend, generation, upload, schedule/privacy edits, Buffer changes, merge or UAT handoff. J3910 and elected-Chief review remain required.

Validation: final uploader dry run returned `ok: true`, `dryRun: true`, resolved category 28, exact master d59057ae and trailer v05. Its simulated scheduling fields are dry-run output only; no platform state changed. `git diff --check` clean; 13 email/private-network checks passed; builder compiled and completed a full encode/decode. Portrait original downloads independently SHA-256-match all three active files (PORTRAIT_SOURCE_MATCH.json).
