# J3544 v04 correction evidence — not a script lock

`macbook-2`, 24 November 2026. Implements `J3539` independent FIX review (`jobs/reviews/J3539/REVIEW.md` and `CLAUDE_QUOTE_CHECK_v03.md`) while retaining all four `J3520` Chief fixes (`jobs/reviews/J3520/CHIEF_RULING.md`). `J3020` remains held for independent review (`J3545`) and elected Chief lock; `J3021` narration is not released. Air slot Wed 16 December 2026 18:00 London and finished-cut watch deadline Fri 11 December 2026 18:00 London unchanged.

## Exact bytes, counts, and opening timing

- **Master & draft (byte-identical):** `every_planet_explained_script_master_v04.md` and `episode_script_draft_v04.md`, SHA-256 `556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8` (`35,984` bytes).
- **Sources ledger:** `01_Script/SOURCES.md`, SHA-256 `4a7e3fa5c74a548764886a274514d2590e5951e5e8782aa8118566d252fdc415` (`16` rows, strict 7-column markdown verified; verbatim live excerpts verified across Rows 1–16 including tightened Row 8 Ingenuity, Row 12 Saturn ellipsis, and Row 16 Voyager 2 attribution).
- **Spoken counts:** `1,296` spoken words (alphanumeric tokens); `1,341` whitespace tokens; `8,471` spoken characters including spaces. Excludes headings, bracket annotations, and HTML comments, preserving the `v02`/`v03` counting convention. Reproduce with `python3 jobs/reviews/J3544/count_script.py`; full chapter breakdown in `jobs/reviews/J3544/COUNTS_v04.json`.
- **Opening timing (expanded spoken words):** Sentence 1 (`"On Mercury, the Sun's closest planet, why does water ice survive four-hundred-and-thirty-degree heat?"`) = `17` expanded spoken words (`~7.03 s` at 145 wpm, `< 8.0 s`); sentence 2 (`"The ice hides in polar craters that never see sunlight."`) = `10` expanded words (`~11.17 s` cumulative, concrete spoken answer well before `0:20` / `0:30`); payoff contrast (`−180 °C`) by `~25 s`. Estimated total runtime: `606.28 s` including `18 s` end hold (planning estimate only, no audio rendered).
- **Teaching markers:** `DATA: 8`, `SCALE: 8`, `WHO: 7`, `WHEN: 8`, `FACT: 4`, `NUMBER OBJECT: 8`, `[ORBIT ACTS]: 2`, `[CHAPTER CARD]: 7` (+ Mercury cold open = 8 planets).

## Corrections implemented in v04 (all four J3520 fixes retained + all seven J3539 items + Gauss/ESA tightening)

1. **Retained J3520 fixes:** Jupiter planets-only mass (`more than twice the mass of all the other planets combined`), Galileo `58-minute` data return without crushing claim or mixed depth endpoints (far-deeper metallic hydrogen kept separate), Earth equatorial speed (`1,670 km/h`) vs named Cyclone Olivia `408 km/h` non-tornadic gust (`4.093×`), Neptune `roughly five times the speed of Cyclone Olivia's record gust` (`2,000 / 408 = 4.902×`, Voyager 2 and New Horizons kept distinct).
2. **Mercury tilt, immediate answer, timing & first-30s sequence (J3539 #1, #7):** Replaced `Tilted just two degrees` with `With almost no axial tilt`, logging the NASA general page (`2°`) vs NSSDCA technical fact sheet (`0.034°`, ~2 arcminutes) conflict explicitly (numeric overlays use `0.034°`, never `2°`). Phrased `March 2011 to April 2015` explicitly as MESSENGER's orbital mission interval. Shortened sentence 1 to `17` expanded words (`~7.03 s`), added the immediate spoken answer `"The ice hides in polar craters that never see sunlight."`, and reordered `[VISUAL MUST]` strictly in spoken-line order with real Mercury imagery between any two graphics.
3. **Venus water inference, Donahue PMID `17783310`, Venera SP-4524 & live quotes (J3539 #5, #6):** Replaced `the scar of a lost ocean` with `evidence that Venus once held much more water`, backed by live verbatim PubMed XML excerpt for Donahue et al. (1982, *Science* 216, 630–633, **PMID `17783310`**; explicitly superseding erroneous `PMID 17782980` in preserved `jobs/reviews/J3538/GEMINI_RAW_v03.txt`). Replaced broken NSSDCA `1981-106D` URL with NASA SP-4524 *Deep Space Chronicle* (printed p. 129, PDF p. 141) verbatim Venera 13 quote (`1 March 1982`, `127` min vs `32` min planned lifetime). Replaced stale Row 3/4 Venus prose with live 24 Nov 2026 excerpts and labelled NSSDCA parameters explicitly as `[table values]`.
4. **Earth WMO source & Gauss/ESA separation (J3539 #6 + optional tightening):** Replaced redirecting `wmo.asu.edu` with working `https://wmo.int/asu-map?map=Wind_028` and Geoscience Australia verbatim excerpts. Separated Gauss's `1830s` absolute magnetic-intensity measurement from ESA's dated `2020` report of a roughly `9%` global-average weakening over the past two centuries.
5. **Mars magnetic history, MOLA elevation vs relief, 624 km removal & 90-Martian-day unit (J3539 #2, #6, brief):** Applied J3539's replacement removing the 4-billion-year shutdown date and compressed cooling causal chain (`Mars has no global magnetic field today, though its crust preserves traces from four billion years ago...`), backed by live verbatim NASA Mars Facts text. Removed unsourced tectonic/hotspot claim, explicitly labelled Olympus Mons `21.3 km` as MOLA elevation above Mars's zero-elevation equipotential datum (`21,287.4 m`, distinct from `−378 m` basal elevation and `21,665.4 m` relief; Smith et al. 2001 Table 8 + NASA PGDA Product 62). Removed unsourced `624 km` and misattributed PIA25476 text quote; backed Arizona-sized base with NASA Mars Facts. Updated Opportunity to `ninety-Martian-day design life`.
6. **Saturn colour-change uncertainty, radial ring extent & FACT label (J3539 #3, #7):** Qualified 2012–2016 hexagon colour change (`while the region inside the hexagon changed from blue to gold between 2012 and 2016, possibly because of seasonal haze`, matching PIA21049). Clarified `282,000 km` as radial extent from the planet (never full diameter). Shortened `FACT:` label to `Less dense` (2 words, exact spoken fragment) with Saturn (`687 kg/m³`) and `"Water"` (`1,000 kg/m³`) on separate equal-volume comparator labels.
7. **Uranus scope qualifiers (J3539 #4):** Applied J3539's exact replacements keeping `Voyager 2` (`24 January 1986`) separate from the `−224.2 °C` (`49 K`) atmospheric minimum (`colder than Neptune in some places`), specifying magnetic tilt `from its rotation axis`, `at least eighty per cent of its mass` as hot dense fluid, and `~4,982 °C` `near the core`. Updated `FACT:` card to `21-year winter` (2 words, verbatim from VO).
8. **Recurring building timeline (J3539 #7):** Added a single persistent **Historical Exploration Timeline (1610–2024)** launched in Chapter 1 and built across all eight chapters as spoken dates land (`1965`, `Mar 2011–Apr 2015`, `1978`, `1 Mar 1982`, `1830s`, `2020`, `10 Jun 2018`, `18 Jan 2024`, `1610`, `late 1800s`, `7 Dec 1995`, `2014`, `early 1980s`, `2012–2016`, `2017`, `13 Mar 1781`, `24 Jan 1986`, `23 Sep 1846`, `10 Oct 1846`, `25 Aug 1989`, `2011`, `Jul 2015`), keeping deep-time spans (`83 million years`, `4 billion years ago`) as separate era call-outs.

## Preserved history, gates, and zero-spend scope

- Historical `v01`, `v02`, `v03` scripts, `SOURCES_v01–v03.md`, `SCRIPT_NOTES_v01–v03.md`, `MUSIC_BRIEF_v01/v03`, `jobs/reviews/J3538/` (including `GEMINI_RAW_v03.txt`), and `jobs/reviews/J3539/` are preserved byte-for-byte.
- Automated `review:script`: **`91.6 / 100` PASS** (`jobs/reviews/J3544/SCRIPT_REVIEW_v04.txt`).
- Explicit-v04 `gate:episode --require-checklist`: **PASS** (`jobs/reviews/J3544/EPISODE_GATE_v04.txt`). Neither structural gate is a factual lock or narration authorisation.
- Fresh Gemini audit output: preserved in `jobs/reviews/J3544/GEMINI_RAW_v04.txt` (prompt in `jobs/reviews/J3544/GEMINI_PROMPT.txt`; see `jobs/reviews/J3544/RESULT.md` for exact hash and summary).
- Zero-spend / no-generation scope unchanged: no audio, images, video, or music generated; no NAS writes; no upload, schedule, or privacy changes.

## Estimated chapter windows (`jobs/reviews/J3544/COUNTS_v04.json`)

| Chapter | Spoken words | Characters | Start s | End s |
|---|---:|---:|---:|---:|
| Mercury | 168 | 1069 | 0.0 | 76.02 |
| Venus | 147 | 923 | 76.02 | 143.34 |
| Earth | 161 | 1123 | 143.34 | 216.47 |
| Mars | 141 | 944 | 216.47 | 281.31 |
| Jupiter | 161 | 1046 | 281.31 | 354.43 |
| Saturn | 186 | 1188 | 354.43 | 437.9 |
| Uranus | 162 | 1043 | 437.9 | 511.43 |
| Neptune | 170 | 1128 | 511.43 | 588.28 |
