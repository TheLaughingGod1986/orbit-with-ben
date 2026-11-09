# J2150: 032 DATA stills and source conflicts (J2089 / PR491 head)

4 Nov 2026 · Claude (review lane) · £0. Checked `data_graphics.py` SPECS against `01_Script/SOURCES.md` rows 1–16 and SHOT_LIST_v03. The colour sheet lives on the Mini, so the checks below are on values, scales, labels and the one-idea rule. Composite contrast and placement stay with picture QA on the graded plates.

## DATA stills: 14 KEEP, 4 CHANGE

KEEP as built: r03/r25 pressure (1 vs 1.47 bar, row 1, linear from 0) · r19 thermometer (−179 °C, row 8) · r26/r27/r40 air mix (95/5, row 9) · r27/r45 density 4× and gravity ≈1/7 (rows 9, 15; both bars from 0, "× EARTH") · r29 Titan rain 9.5 mm / 1.6 m/s (row 10) · r33 Ligeia ≈160 m and r34 Kraken ≥300 m with LOWER BOUND on one shared depth scale (row 12) · r46 "OUR ROUGH SUM" 4× ÷ 1/7 ≈ 28× (row 15, labelled as ours) · r49 ≈8 Earth days daytime (row 16).

CHANGE:
1. **r04_cold:** two ideas on one card (title "ALMOST NO OXYGEN" over a temperature scale). Title it `TITAN SURFACE` and put `ALMOST NO OXYGEN` as a footnote line (as r40 does).
2. **r28_rain and r29_rain:** the "MODEL MAXIMUM" label doesn't match the source wording ("Earth's biggest raindrops", row 10). Label both `BIGGEST DROPS`.
3. **r39_oxygen:** 78% nitrogen isn't in SOURCES rows 9 or 14 ("nitrogen is most of Earth's air"; 21% oxygen). Show oxygen only: bars `EARTH 21%` vs `TITAN ≈ 0` ("almost none"), max 25, linear from 0. If Gemini adds a sourced 78% row later, the nitrogen bar can come back.
4. **Shot-list text to match:** R4 and R39 descriptions in SHOT_LIST_v03 change the same way.

Render approval: all 18, with the four changes, may render under this review reference (J2150) once changed.

## Source conflicts

- **R25 (PIA07233, an annotated aerial site estimate):** wrong subject. Use **PIA07232**, the Huygens surface view, as an inset card at no more than 2× native size, cropped clear of the white surround. Credit `ESA/NASA/JPL/University of Arizona`. The real surface view at small size beats a big wrong image.
- **R38 (PIA19051, elevation-derived perspective):** a reconstruction, which is a picture_qa FAIL (AGENTS *Picture and music QA*). Drop it. Use **PIA14584** ("Titan Kraken Mare") at R38 as use 1 of 2; R40 stays use 2 of 2, reframed.
- **R50 (PIA16638, Sinlap/Soi two-panel with scale text):** crop to the Sinlap panel only, with no scale text or labels (a labelled image is a FAIL). If the crop keeps less than 50% of the native pixels or a label stays in frame, drop the plate. R50 then runs the CODE map pin ("SELK CRATER · DRAGONFLY TARGET") over the APL Dragonfly dune plate already in the pool.
- **ESA Huygens descent movie (data-derived colourized animation):** a reconstruction, so a picture_qa FAIL: **not used**. The descent chapter uses the real DISR stills and Cassini plates.

Next: J2089 applies these (SHOT_LIST_v04 plus a data_graphics.py update), renders, and carries on with the remaining harvest. No money, VO or script change.
