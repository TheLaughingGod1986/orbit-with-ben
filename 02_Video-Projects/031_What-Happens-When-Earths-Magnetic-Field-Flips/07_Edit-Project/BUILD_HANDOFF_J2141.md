# J2141 resumable picture build — 4 Nov 2026

Worker: codex. Spend: £0. **Partial work, no KEEP, no Chief PASS, no film stage approval.**

## Continuation checkpoint (6 Nov, Commons real-picture harvest)

Preserve **1/3**. Branch `worker/J2141-commons-v01` adds two candidates to
`HARVEST_POOL_v01.json` (eight total). This is a partial harvest, not KEEP.

- R34a: Pseudopanax's Tāne Mahuta photograph, 3264×4896. Commons records
  the photographer's public-domain release. This is the living-tree
  establishing shot, never the ancient tree sampled for Laschamp evidence.
- R37b: Fjturban's `Cuevamanos.jpg`, 4161×2774, CC BY-SA 3.0. Credit author,
  file URL and licence, indicate crop/grade, and carry share-alike obligations
  for adaptations into delivery. It illustrates cave art; do not imply that
  these particular stencils date to the Laschamp event.

Original images, original Commons API, file-page rights evidence, licence
terms and a contact sheet live at `/Users/benjaminoats/_desk/J2141-commons-v01/`.
The pool records SHA-256 for originals and evidence, plus original Commons
SHA-1. `HARVEST_COMMONS_TECHNICAL_CHECK_v01.json` records successful hash,
metadata, native-size and planned-reuse checks for these two files only.
The contact sheet and larger source stills were viewed. Crop/blur recipes
are recorded but unrendered; subject clearance, grading, motion and finished
composite QA remain open. Both are planned once, maximum twice.

`harvest_commons_nature.py` reproduces this two-file harvest with author and
licence guards; it verifies recorded media on repeat and preserves existing
files. Run with `/usr/bin/python3 .../harvest_commons_nature.py --out <dir>
--manifest <pool.json>`. Media is outside git; no paid generation or credit.

R37a horse investigation reached its **three-candidate limit**: Lascaux2.jpg
is 598×450 (3.21× full-width upscale); Lascaux, horse.JPG is explicitly a
museum replica; Chauvethorses.jpg is 400×300 (4.8×). None is admitted.
Detailed URLs/outcomes live in the pool's `search_checkpoints_v01`. Chief
must scope a genuinely new source/approach or accurate alternative; a new
worker must not reset this search. R34b swamp-kauri slab remains missing:
the one examined Commons furniture image is not a recovered research slab.
No image was downloaded for these rejected candidates.

Prior outputs on PRs #539, #551, #555, #562, #564, #569 and #571 remain
separate and must be integrated by Chief while preserving every renderer
mode. They already cover the later opening/field/SAA/dynamo/sky/core/timeline
batches absent from main's older handoff; do not build those again.

Remaining J2141 action: wider real-picture harvest (including R41 ISS limb),
Mars/Earth body comparison, R30 remaining twist component, source-ID and
sourced-simulation conflicts, all composites and full picture/polish QA.
No Chief PASS or film-stage approval. Spend £0. No live render or download.
Both repos pulled successfully. NAS offload deferred to 01:00–06:00 at about
8.3 GB free; the earlier detached offload `.done` is present with exit 0, so
no second copy was started. No NAS assets deleted. Nothing needs Ben.

## Continuation checkpoint (5 Nov, seventh run)

Preserve **1/3**, same PR #495. Added `code_graphics.py comparisons` and
three unique source-linked alpha renders, 1920×1080 / 25 fps:

- R30 recap, 307.12–312.88 s: sequential global-field −9%, pole 55 km/yr,
  Atlantic dent 2 lobes labels (SOURCES rows 1, 8, 12). This is a recap
  component, not the complete triptych/twist scene. Requires moving ISS plate.
- R40 dipole-strength component, 409.54–414.46 s: bar falls from normal
  100% to approximately 10%, sharing zero and scale (SOURCES row 15).
  This depicts the main dipole only; multipole geometry remains unfinished.
- R44 duration comparison, 452.70–458.22 s: Mars atmosphere loss over
  billions of years versus Earth's few-thousand-year field flip (row 17).
  Qualitative labels avoid inventing an exact value for “billions”. It does
  not substitute for the remaining physical planet comparison. Final
  few-thousand-years label has 1.32 s; review actual playback readability.

`CODE_COMPARISONS_v01.json` records source rows, Scribe cue starts, paths and
hashes. `CODE_COMPARISONS_TECHNICAL_CHECK_v01.json` records all three hash,
format, alpha, duration and complete error-free decode checks. Media/contact
sheet: `/Users/benjaminoats/_desk/J2141-comparisons-v01/` (6,739,921 bytes).
Five static samples per render checked; contact sheet viewed. Navy is preview
background only; graded moving plates, clearance and actual motion/composite
review remain required. No KEEP, PASS or stage approval. Reproduce into a new
directory: `code_graphics.py comparisons --out ... --manifest ...`.

Detached `J2141-comparisons-v01` finished exit 0; no active render. Log and
completion: `/Users/benjaminoats/_desk/logs/J2141-comparisons-v01.log` and
`.done`. NAS offload ran first: nothing old enough, about 14 GB free. No archive
search, paid generation or publishing change; £0 spend. Remaining archive
harvest, mechanisms, progressive timeline, R41, composites and full QA remain
unfinished. Existing source-ID and sourced-simulation gate conflicts below
still require Chief reconciliation. Next run resumes this same branch.

## Continuation checkpoint (5 Nov, fifth run)

Queue remains **1/3**, same PR #495. Added three 3.6 s transparent WHEN
renders via `code_graphics.py dates`: R19 (197.00 s, 83 MILLION YEARS,
SOURCES row 7), R24 (234.58 s, 2013 / 3 SPACECRAFT, row 9), R33
(341.38 s, 41,000 YEARS AGO / LASCHAMP EVENT, row 14). Starts are checked
against locked Scribe word starts. No words or VO changed. These are date
call-outs, not the still-required building timeline. Their animated line is
an entrance accent, not a quantitative time axis. Captions fade in/out;
3.6 s duration keeps all holds below four seconds.

`CODE_DATES_v01.json` records source rows, timings and hashes;
`CODE_DATES_TECHNICAL_CHECK_v01.json` records full error-free decode,
1920×1080, argb alpha, 25 fps and duration checks. Media and inspected static
contact sheet: `/Users/benjaminoats/_desk/J2141-dates-v01/`. Preview navy
is a viewing background only. Place over graded moving plates, clear of the
subject and existing FACT graphics. Actual playback/composite readability
and full QA remain unreviewed. No KEEP, Chief PASS or stage approval.

Detached batch `J2141-dates-v01` finished exit 0, no active render. Log:
`/Users/benjaminoats/_desk/logs/J2141-dates-v01.log`, completion `.done`.
Existing output refusal is inherited from the evidence encoder. Reproduce
into a fresh media directory with `code_graphics.py dates --out ... --manifest ...`.
NAS offload found no eligible old scratch; approximately 15 GB free. Small
batch only, £0 spent. No archive search conducted; no search budget reset.
Remaining archive harvest, other mechanisms/timeline, R41 fallback, R44
duration comparison, composites and full QA remain unfinished. Source-ID
and sourced-simulation gate conflicts below remain for Chief reconciliation.

## Continuation checkpoint (5 Nov, fourth run)

Continue this same branch / PR #495 at **1/3**. Added three source-linked,
row-specific transparent 1920×1080 / 25 fps overlays in `CODE_SCALES_v01.json`:

- R36 qualitative duration brackets, 373.84–378.72 s, SOURCES row 14.
  “COLLAPSE / A FEW HUNDRED YEARS” changes to “WEAK PHASE / LESS THAN 1,000 YEARS”.
  Equal bracket lengths intentionally encode no exact value for “a few”.
  The final number has only 1.3 s in the locked line; readability at speed
  requires actual composite review, never extend the row or narration.
- R44 gravity bars, 449.92–452.20 s, SOURCES row 17. Shared zero and scale:
  Mars 0.38 relative to Earth 1.00. Alpha overlay requires real moving Mars
  imagery underneath; no flat-disc planet. This completes only the gravity
  comparison, not the remaining billions-versus-thousands duration comparison.
- R52 generations tally, 534.48–537.92 s, SOURCES row 18. Exactly 400 cells;
  first 40 blue, remaining 360 gold. 40–400 human generations corresponds to
  1,000–10,000 years at the source record's 25 years per generation. This is
  arithmetic, not a demographic dataset. Aurora plate / later dynamo still needed.

`scale_graphics.py`, exposed through `code_graphics.py scales`, reuses the
existing evidence encoder with optional explicit specs/frame callbacks. Existing
`evidence` mode keeps its original defaults. All three have 0.4 s alpha fades,
labels of at most four words and no still hold exceeding four seconds.
Existing output files are refused. Reproduce in a **fresh** media directory:

```sh
/usr/bin/python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py scales --out <fresh-media-dir> --manifest <new-manifest.json>
```

Media: `/Users/benjaminoats/_desk/J2141-scales-v01/` (6,581,767 bytes total).
`CODE_SCALES_TECHNICAL_CHECK_v01.json` records all three hashes, 1920×1080,
25 fps, argb alpha, duration within half a frame and full error-free decode.
Five static alpha samples recorded per render; individual 75% preview stills
inspected. `CONTACT_v01.jpg` uses a neutral navy background, not a finished
plate composite. No audio, motion, composite, subject clearance, playback
legibility or Chief approval claimed. No media in git.

Detached batch `J2141-scales-v01` completed exit 0; no render remains active.
Log `/Users/benjaminoats/_desk/logs/J2141-scales-v01.log`; completion `.done`.
NAS offload ran with filesystem access before building, found no eligible old
scratch; about 10.4 GB free. This small batch adds about 6.6 MB only. No archive
inputs searched; prior missing-footage budgets were not reset. Both checkouts
synced; HOS inbox and channel balance skipped as instructed. Existing renders,
locked words and sources preserved. Spend £0.

Remaining: wider harvest, all other mechanism/timeline renders, R41 fallback,
remaining R44 duration comparison, plate composites and full QA. Asset-ID and
sourced-simulation/map gate conflicts below still need Chief reconciliation;
this worker makes no protected decision. Resume at 1/3, no stage approval.

## Continuation checkpoint (5 Nov, third run)

Continue this branch / PR #495 at **1/3**. Added five distinct row-specific
1920×1080 / 25 fps renders, recorded in `CODE_EVIDENCE_v01.json`:

- R18 barcode schematic, 191.48–195.04 s, from SOURCES row 7. Mirrored stripes
  spread from a central ridge. Stripe widths are illustrative, not a measured
  reversal chronology. The preceding real seafloor plate remains required.
- R19 alpha tally, 199.10–202.38 s, SOURCES row 7. A tally builds to 183 at the
  spoken number. It is not a graph of event times. The 83-million-year WHEN
  item remains unfinished. Keep the existing FACT card clear at lower left.
- R35 alpha tree rings, 362.10–373.06 s, SOURCES row 14. The sourced 6% endpoint
  uses a zero-to-100 slider; illustrative incoming particles and a growing
  highlight show radioactive carbon recorded in a generic tree ring. This is
  not an actual kauri isotope record. Plate changes are still needed underneath
  this 10.96 s overlay. The existing diary FACT goes at lower left.
- R42 alpha mass-per-area comparison, 427.04–433.60 s, SOURCES row 16: 1 kg
  per square centimetre of air versus 10 m of water. These are local columns,
  not a drawing of a planet; column heights are schematic. The actual mass
  comparison comes from the locked line/source, not a simulated dataset.
- R43 gas-collision schematic, 441.28–445.50 s, SOURCES row 16. Incoming
  particles stop at gas molecules above the ground. Positions and collision
  depths are illustrative, not an atmospheric transport calculation. The
  preceding 434.52–441.28 s still needs its own real imagery / approved cut.

Renderer: `evidence_graphics.py`, exposed as `code_graphics.py evidence`.
All individual captions fade in/out over 0.35 s, have at most four words, and
hold for under four seconds. Alpha overlays have 0.4 s overall fades. Full
frame cuts start on locked words and end without splitting a word. Existing
renders are refused, not overwritten. Reproduce to a **fresh** directory:

```sh
/usr/bin/python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py evidence --out <fresh-media-dir> --manifest <new-manifest.json>
```

Media: `/Users/benjaminoats/_desk/J2141-evidence-v01/`. Contact sheet:
`CONTACT_v01.jpg` in that directory (neutral preview backgrounds are not
actual composites). `CODE_EVIDENCE_TECHNICAL_CHECK_v01.json` records all five
hash matches, dimensions, 25 fps, duration within half a frame, alpha/pixel
format and full decode without errors. Five static times per graphic checked;
opaque samples have mean luma ≥28. The contact sheet was inspected as stills.
These are technical/static checks only; **no motion, audio or composite review**.

Detached batch `J2141-evidence-v01` completed exit 0; no render is still active.
Log `/Users/benjaminoats/_desk/logs/J2141-evidence-v01.log`, completion `.done`.
No new archive input was searched in this run, so no missing-footage search
budget was consumed. Existing six harvest candidates and all previous media
were retained. Before work, NAS offload ran and found nothing old enough;
roughly 13 GB free. This small batch adds about 23 MB, no large scratch render.

Remaining: wider licensed harvest; all other mechanism/timeline renders;
R41 atmosphere fallback; moving-plate composites, actual motion-capable
review and full QA. R21 fallback already exists in v02 mechanisms. Reconcile
R54 identities and sourced-simulation/map conflicts below before admitting
those candidates. The stage is unfinished and no Ben action is requested by
this checkpoint.

## Continuation checkpoint (4 Nov, second run)

Continue **this same branch/PR #495**, at **1/3**. Added:

- Six distinct 1920×1080 / 25 fps mechanism renders in `CODE_MECHANISMS_v02.json`: R4 compass inversion; R7 cooling/locking magnetic grains; R8 reversed grains; R20 100%→91% field-strength bars; R21 alpha compass wobble (the authorised £0 fallback); R49 nearest-local-pole compass. All use their own row filenames. R21 requires a graded moving Earth-limb plate underneath. R20 is also alpha and requires a moving plate with subject clearance.
- `mechanism_graphics.py`, called through `code_graphics.py mechanisms`, implements those three modes only. Strength bars share zero and use sourced endpoints, not invented historical measurements. Compass/grain geometries are explanatory schematics. Full-frame endpoints are checked against locked words. R7 ends at 59.92 s in a word gap; R49 ends at 503.88 s after “nearest”. All labels have four words or fewer.
- `CODE_MECHANISMS_TECHNICAL_CHECK_v02.json`: all six fully decoded; hashes, frame rates, dimensions, duration and pixel formats match. Static samples at five times checked label bounds, opaque-frame mean luma ≥28 and transparent-overlay start. These checks do **not** establish motion quality or composite acceptance. Static contact sheet inspected: `/Users/benjaminoats/_desk/J2141-mechanisms-v02/CONTACT_v02.jpg`.
- Brunhes and Gauss original Commons portraits downloaded, with per-file public-domain assertions checked, HTML/API evidence and hashes added to `HARVEST_POOL_v01.json`. Pool now holds six candidates. Brunhes is 804×983; use a portrait inset/cutout within the upscale cap, not a full-width stretch. No portrait cutout/parallax has been produced. Updated contact sheet: `/Users/benjaminoats/_desk/J2141-portraits/contact_sheet_portraits_v02.jpg`.

Media stays outside git under `/Users/benjaminoats/_desk/J2141-mechanisms-v02/` and `J2141-portraits/`. The smaller v01 mechanism batch is superseded: R7/R49 endpoints needed correction. Preserve it as evidence, do not assemble from it. `CODE_MECHANISMS_v01.json` records that supersession.

Reproduce into a **fresh** directory (existing renders are refused):

```sh
/usr/bin/python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py mechanisms --out <fresh-media-dir> --manifest <new-manifest.json>
```

Use `/usr/bin/python3`: it has Pillow 11.3.0; Homebrew/default python lacks Pillow. No packages installed. The original `harvest_picture_v01.py` needs requests in its original environment; the new portrait harvester uses stdlib HTTP plus Pillow.

Both detached mechanism batches completed exit 0; no live render remains. Current logs/completion: `/Users/benjaminoats/_desk/logs/J2141-mechanisms-v02.log` and `.done`. No second worker should restart that completed batch. NAS offload was attempted before building and **deferred to 01:00–06:00 by the existing script**, with ~9.4 GiB free. This small batch added ~7 MB of mechanism media plus ~1.4 MB of portraits, not a large scratch render. Restore headroom before larger work.

Remaining build: wider unsearched archive harvest; the other mechanisms listed below (except compass, grains and strength now implemented); R41 atmosphere fallback; actual composites and full QA. R20's graphic starts on “1830s”, while the older WHO overlay still lasts to 209.08 s; exact compositor transition needs review. The approved row says a five-second strength chart, but the actual remaining spoken span is ~3.8 s. Do not extend the row or clip narration to make five seconds.

Existing Chief decisions needed on R54 asset identities and sourced simulation/map separators below remain unresolved by this worker. No new Chief authority, KEEP, PASS, film-stage completion, paid generation or YouTube change is claimed. Two portrait inputs examined (one candidate each, under five active minutes total); the broader missing inputs were not searched in this continuation.

## Landed in this worker branch

- `harvest_picture_v01.py`: resumable NASA API download and hash/evidence recorder.
- `HARVEST_POOL_v01.json`: four downloaded candidates with original API metadata, credits, file hashes, dimensions and individual pending rights/review states. Media and contact sheet live in the shared 031 `07_Edit-Project/harvest_v01/`, outside git. Not the complete licensed harvest.
- `code_graphics.py cards`: all three WHO and six FACT overlays named in SHOT_LIST_v02. Each gets a unique row-specific transparent 1920×1080/25 fps qtrle MOV; no baked black slab. Animation in/out: 0.4 s. WHO durations: 3.6 s. Labels and biography years follow the approved shot list/SOURCES row 19. Source-row links and exact Scribe cue starts are in `CODE_CARDS_v01.json`.
- `CODE_CARDS_TECHNICAL_CHECK_v01.json`: all nine hashes match, alpha format is argb, dimensions and durations match, and full ffmpeg decode completes without errors. These are encoding checks only. Static preview sheet/full-size WHO frame inspected; no claim to hearing audio or seeing moving video.
- Outputs live under shared 031 `07_Edit-Project/code_cards_v01/`; no media committed.

## Exact resume state

Queue plan remains **1/3**: brief/input review finished; build still partial; full package verification not started. Preserve that denominator. No other queue job taken.

Detached render was `tmux J2141-cards`, using `/private/tmp/J2141-render-cards.sh`. It **finished, exit 0**. Logs: `/Users/benjaminoats/_desk/logs/J2141-cards.log`, completion: `/Users/benjaminoats/_desk/logs/J2141-cards.done`. Do not mistake the completed nine-card batch for all graphics being complete.

Reproduce cards from this branch:

```sh
python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py cards --out <persistent-media-dir> --manifest <new-manifest-path>
```

## Observed issues for Chief/editor

1. NASA API ID verification contradicts R54's asset descriptions. **PIA20016 = Peering Through Titan Haze**, infrared composite, not natural-colour Titan beside Saturn. **PIA14909 = Titan Up Front**, true-colour Titan in front of Saturn/rings, not an isolated haze-limb photograph. Both are downloaded candidates, not admitted shots. Resolve R54 explicitly; no silent substitution. NASA metadata and the contact sheet preserve the evidence.
2. NASA institutional hosting alone is not a blanket per-asset licence. The two Titan credits include universities/Space Science Institute; their rights remain pending. Blue Marble texture also remains a candidate. PIA00407 credits NASA/JPL/USGS; its use is subject to NASA media conditions. Keep third-party rights checks open.
3. The shot list calls sourced simulations/maps “real” separators (e.g. R13, R15, R16, R18, R23/24, R39/47). AGENTS picture QA still forbids sourced simulations/maps/labelled graphics. Rule-E GO is recorded, but this job does not explicitly waive that gate. Chief needs to reconcile these rows before admission; do not turn a sourced map into an accepted code graphic by relabelling it.
4. R35's literal cue leaves only **1.24 s** inside its row. Its FACT card needs readability/timing review on the actual composite. Other FACT durations: R6 2.44 s, R14 1.92 s, R19 1.96 s, R27 3.6 s, R45 3.4 s. Do not mark legibility from encoding metrics.
5. The nine overlays require graded moving/blurred real plates. They have not been composited; near-black, subject clearance, timing fit and motion QA remain open. Preview backgrounds are transparent, not intended black picture.

## Work still unfinished

- Wider NASA/SVS, NOAA/NCEI, USGS/USFWS, ESA/DTU and Commons harvest, per-file terms/attribution verification, candidate inspection, interval/crop assignment, reuse tally and complete contact sheet. No active search budget was consumed on these unsearched missing inputs; do not repeatedly revisit the rejected Titan interpretation.
- Mechanisms: poledrift, flip, compass, timeline, grains, matuyama_map, strata, layers, dynamo, barcode, strength, belts, hubble_saa, sat_safe, saa, triptych, paleo, rings, multipole, column, mars_vs_earth, extinction_check, grid_shield, poles_map, aurora, generations. `code_graphics.py` intentionally exposes only the implemented cards mode; it does not fake unsupported modes.
- £0 R21 compass and R41 NASA atmosphere fallbacks; no OMNI or paid generation attempted.
- Full row renders, cue/composite review, actual motion-capable review and applicable picture/polish gates. The film has not been assembled.

Disk: NAS offload ran with elevated filesystem access before building; **nothing in /private/tmp was old enough**. Free space remained ~12.6 GB, so this run used a small media batch (~18 MB of cards), not a large scratch render. Restore headroom before larger work; never delete/overwrite NAS assets.

Next worker continues J2141 from this branch/PR. Chief decides the asset/gate conflicts; no Ben action requested by this partial handoff.
