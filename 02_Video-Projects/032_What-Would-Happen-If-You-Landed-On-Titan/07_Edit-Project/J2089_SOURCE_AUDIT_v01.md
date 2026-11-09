# J2089 — 032 picture input audit and first teaching-overlay drafts

4 November 2026 · Codex specialist worker · £0 spent · PARTIAL, not KEEP or PASS.

## Delivered

All 17 pinned PIA IDs queried against the NASA Images API. Original advertised image links downloaded, decoded, SHA-256 recorded with source metadata and dimensions in `HARVEST_POOL_v01.json`. The pool deliberately leaves every licence pending a per-asset check. NASA hosting alone is not clearance.

Media and source responses: `/Users/benjaminoats/_desk/cache/J2089/harvest_v01/`.
Contact sheet: `contact_sheet.jpg` in that directory; Codex inspected the still contact sheet. This is no moving-picture review.

13 row-specific transparent overlay preview PNGs: 2 WHO cards, 7 date/timeline stages, 4 FACT cards. `code_graphics.py` supplies 0.4 s entry/exit and 3.6 s duration; its alpha-MOV renderer requires individually named approved ids plus a review reference. No motion renders produced before Chief frame review. Plain navy in the review sheet is preview-only; compositing must use an approved graded moving real plate, off its subject. `OVERLAY_MANIFEST_v01.json` pins preview hashes and SOURCES row references.

Preview sheet: `/Users/benjaminoats/_desk/cache/J2089/teaching_previews_v01/teaching_previews.jpg`.

## Source corrections needed before assembly

The approved shot-list descriptions disagree with live NASA records:

| ID | Actual asset | Planned use affected |
|---|---|---|
| PIA01536 | Detail of Triton Surface | R13 Voyager orange Titan |
| PIA08399 | Map of Titan — October 2007, labelled | R4/R11 atmospheric limb |
| PIA11831 | Hotei, two-panel release | R50 Selk Crater |
| PIA14909 | Titan Up Front, Titan with Saturn | R3/R44 close haze/crescent framing |
| PIA17172 | The Day the Earth Smiled, Saturn panorama | R14/R28 Titan clouds |
| PIA17655 | Titan North, labelled polar map | R33/R34 Ligeia/strait plate |
| PIA20016 | Peering Through Titan Haze, infrared composite | R6 natural-colour Titan beside Saturn; R35 needs correct disclosure |
| PIA20021 | Mystery Feature Evolves in Titan Ligeia Mare | R9/R23 distant crescent |
| PIA21445 | Earth Between the Rings of Saturn | R38/R40 Kraken shoreline |

Low resolution/panels: PIA07231 is 305×261, PIA07233 is 177×255 with annotations; PIA07232's release is 546×693 with a narrow image and white surround. Neither scaling the release canvas nor adding a blurred background proves the subject is sharp enough. PIA07236 is 600×601. These require exact crop/upscale calculations and frame review, not a blanket acceptance. PIA09182 is an 18,881×1,792 swath; Belet identity/interval must be checked. PIA10008 also requires a crop without grid, gaps or a misleading coastline.

NASA API search-only leads, not approved replacements: PIA08167 / PIA12511 / PIA12606 for haze; PIA21450 / PIA17168 / PIA21610 / PIA21624 for cloud views; PIA19051 / PIA21434 / PIA19046 for Kraken. PIA02238 matches Voyager thick haze but needs a new resolution decision (it was rejected from the Short at 2.41×). No substitute was silently added to the approved shot list. Search queries examined titles only; no extra in-depth missing-footage candidate review was started.

## Short exclusion and reuse

The uploaded S6 v02 recipe names PIA14925, PIA06230, PIA09739 and PIA21625. None overlaps this pinned-ID pool. PIA07232 was an unused/rejected Short candidate, as ASSEMBLY_STATUS records. Do not reject it merely because the candidate list contained it. Final-frame/hash exclusion remains unverified.

The pool's `referenced_rows` includes negative references (e.g. “replaces third use”); it is NOT a validated appearance tally. Enforce ≤2 actual appearances using the final cut manifest, including rows whose IDs are only in the shot-list tally.

## Next work / review request

Chief: review the concrete source mismatches and the 13 teaching-overlay stills. Correct the approved shot list or assign replacement assets with accurate credits/disclosures; approve/revise the stills before animation rendering. No waiver, generation spend or script/VO change is requested.

Then resume this same J2089 plan (1/4 done): finish licensed harvest (including Huygens/Dragonfly/Cassini motion, portrait and JWST), build all remaining DATA/mechanism graphics and R26/R46 £0 fallbacks, render approved overlays, and verify the package. It is not assembly-ready. No shot/picture stage approval is claimed.

## Local checks and disk

All 17 downloaded files decoded with Pillow; metadata hashes and image hashes recorded. All 13 preview files generated. No audio/motion perception claimed. Use the existing `/Users/benjaminoats/_desk/venv-graphics/bin/python` (system Python lacks Pillow).

NAS is mounted; low-disk offload started detached as `J2089-offload`, using the existing checksum-verifying `nas_offload.py --apply`. Log `/Users/benjaminoats/_desk/logs/J2089-offload.log`; completion `/Users/benjaminoats/_desk/logs/J2089-offload.done`. Missing `.done` means still running: never start a duplicate. Dry run found only ~490 MB eligible, insufficient to restore 20 GB. No large render started.
