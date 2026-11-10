# J2299 — partial source recovery and picture reconciliation

6 November 2026 · Codex worker · **Incomplete; no media approval or assembly release.**

The incorrect lock captions cannot safely drive assembly. `PICTURE_RECONCILIATION_J2299_v01.json` records a decision for all 32 caption differences, retains the scope of all 17 false-subject exclusions, and restores the 67 row boundaries and spoken lines from the accepted VO-derived `SHOT_LIST_v01.md`. This is a correction draft, not a replacement approved shot list or an executable cuts manifest. Previous files remain untouched. Draft evidence is PR #578 at `adab48f716e066f57e2e1c9f56c3de789dda854e`.

## Delivered evidence

- `SOURCE_AUDIT_J2299_v01.json`: fresh exact-ID NASA API queries for the union of 46 PIA IDs in the shot list and stills lock. 45 exact records; PIA01389 has no exact result and stays unresolved. Its old Saturn caption is explicitly draft evidence, not a freshly verified record. Metadata descriptions resolve PIA01492 as Neptune despite its generic title.
- `EXTERNAL_RECORDS_J2299_v01.json`: eight fresh Commons API records, including licence/credit metadata and the actual resolved filenames. The purported 1783 naming letter resolves to **On the Diameter and Magnitude of the Georgium Sidus**, not proof of a naming letter. Do not use that PDF as a specific historical document without checking its contents.
- `STILLS_POOL_STATUS_v03.json`: all 43 lock-pool files now have Mini-readable paths. **41 images match the recorded SHA-256; two original PDFs are recovered but the prior Quick Look JPEG rasters have not been reproduced.** Auxiliary Orbit, real Moon and simulated-Venus files are identified separately. Seven previously available pool/auxiliary files were freshly hash checked. Availability is not suitability or permission.
- All media and cached source records live under `/Users/benjaminoats/_desk/cache/J2299`, or the existing recorded Mini/NAS paths. No NAS writes/deletions. The shared folder had no J2290 transfer; public recovery was used.
- Source contact sheets: `source_sheet_1.jpg`, `source_sheet_2.jpg`, `source_sheet_3.jpg` in that cache. First two sheets inspected as stills; not a full-size review of every source, and no moving playback review.
- Three opener candidate files and static/probe evidence: `OPENER_SEARCH_J2299_v01.json`. All three new deep-candidate slots are used. **Do not reset the search budget on restart.**

## Concrete corrections

PIA18033 is the real Earth used by the original shot list, while PIA00271 is simulated Venus. PIA00141 is Miranda terrain; PIA01361 is a moon montage. Saturn, Io, Ariel and Jupiter files cannot serve the lock's Uranus/Miranda captions. Pluto PIA19857/PIA19952 belongs in the spoken Pluto bridge, rather than the false Uranus roles. PIA01488 depicts an enhanced Uranus upper-atmosphere photograph and can be considered for the pressure row; it does not itself show a descent or validate pressure values. Multi-panel/labelled source files remain unsuitable as whole finished shots.

The NASA general usage page was cached and hashed; it does **not** grant blanket NASA public-domain status to third-party material. In particular PIA17306 names Lawrence Sromovsky/Wisconsin/Keck. Its specific rights remain to establish. ESA/Webb pages and CC BY 4.0 conditions are cached and hashed; full listed credits are required. Commons terms are per record. Neither this note nor a source host establishes all final usage permissions.

## Opener decision for Chief

Required input is R01 0.00–6.22 s, sharp native moving Uranus with a recognisable sideways/ring answer, no baked labels/montage, <=2.35x upscale, and no excluded `svs20390` reuse. Existing PIA01283 is a 737x256 still sequence, not a movie. PIA01280 is also a still.

Three new candidates examined:

1. ESA/Webb `weic2602c`, 20 s, 1920x1080/25 fps: the inspected 3 s frame is visibly diffuse spectroscopy imagery without a clear sideways-ring answer. Its official description identifies a time-lapse from spectroscopy slices, not conventional cloud photography. CC BY 4.0 with the full ESA/Webb/NASA/CSA/STScI/Tiranti/Melin/Zamani credit. No motion suitability ruling made.
2. NASA Hubble *Seasonal Changes on Uranus*, `STScI-01EVSN15BQ2SME252D8AQKPP0Y`: 176x272 encoded source, 133.33 s/30 fps. The inspected sample has baked date/title/credit text and a tiny body. Even the entire image at 2.35x is only 414x639; enlarging the planet to the intended opener is unsuitable.
3. ESO `uranus`: 680x280, 8 s/12 fps. The inspected sample is visibly noisy and soft without the required vertical-ring answer. Official caption acknowledges changing seeing. CC BY 4.0 with full ESO/C. Dumas, B. Sicardy, and J.-E. Arlot credit. No motion review made.

Chief must choose a revised opener under the missing-footage rule, or scope a genuinely new bounded source approach with a recorded reason. A concrete option for Chief to consider is a clearly disclosed generated Uranus world shot supporting the locked sideways-planet line, separately scoped through the approved Flow/Veo route with bounded takes, live balance check and explicit credit cap. **This is a proposal only; J2299 authorises no generation.** Script, VO and excluded Short opener remain locked.

## Graphics and remaining production

All 14 J2290 graphic durations match the accepted shot-list row durations (within 0.01 s). This does not prove word-level animation timing. R26 uses the `retrograde_tilt` name; its axial-tilt alias is not an extra cut. Magnetic tilt/offset belongs to R46; R52 is the interior/fluid mantle. Names and spans are recorded in the reconciliation manifest.

The draft says R54 is NASA before R55; **accepted R54 is CODE**. Rendering R55 as another full-frame pressure graphic violates separation. A simple source-type relabel does not fix this: the revised shot needs real moving imagery between diagrams. Further review must also fix the persistent labels/cards, picture changes within long rows, true globe scaling (including Miranda/Moon), source crops, house type, grain and credits. The old code cannot be promoted by changing only its fps.

**Not delivered:** the 14 Mini graphic binaries or corrected versions; complete crop/cut assignments and reuse tally; PDF document rasters; full rights clearance; a compliant native opener; final cuts/pool QA inputs; rendered frame sheet; picture_qa/polish reports. No checks were run against a nonexistent finished cut. No KEEP/PASS is inferred from any byte or duration check.

After Chief's opener/shot decision, resume this same job and five-step plan (still 0/5 complete: step 1 is only partial). Finish all source/row/rights corrections, produce corrected smooth drafts, verify actual files, then deliver applicable gates and hand off explicitly to **J2300**, whose reviewer must have demonstrated moving-video input. J2300 remains dependent; do not close J2299 or release assembly to bypass that review. No money, generation, VO/music credit, YouTube or social state was changed.
