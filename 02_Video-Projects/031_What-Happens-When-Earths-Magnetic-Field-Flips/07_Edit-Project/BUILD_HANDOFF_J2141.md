# J2141 resumable picture build — 4 Nov 2026

Worker: cursor. Spend: £0. **Partial work, no KEEP, no Chief PASS, no film stage approval.**

## R6 tight-edge search (7 Nov UTC, Cursor)

Preserve **1/3**, PR **#575**, starting at `95f4f3e1f6`. Spend **£0**.
The wide plate `plate_031_r06_lava_v01.mp4` is unchanged. This pass looked
for the shot list's second R6 beat: a tight glowing edge of lava on the
ground. Three candidates were examined. None is that beat. No new plate.

- The existing fissure-20 overflight stays a wide aerial through the end
  card. Stills at 12 s, 18 s and 24 s were looked at again. Source
  6.00–12.68 s is not reused for the tight beat.
- North-side spatter, Commons `PD-USGov-USGS`, 34.6 s:
  `/Users/benjaminoats/_desk/J2141-lava-edge-v01/fissure20_north_spatter.webm`
  (`3bffd0b475d2d5bd28773038087f62c199ee5d0717bed2e929efd0d4160e210a`).
  A night fountain after the USGS title card. The lower half is black.
  It does not show lava advancing over clay.
- Afternoon fountaining, Commons `PD-USGov-USGS`, 27.3 s:
  `/Users/benjaminoats/_desk/J2141-lava-edge-v01/fissure20_afternoon_fountain.webm`
  (`c3bef5d9ca531a7056c166d39dd1e43b4dc639988ece055333d0d57f6bc7116e`).
  A daylight fountain behind a spatter mound. Title and end cards sit
  outside the picture. The end card calls the dark mound spatter fragments.
  It is not a tight edge baking clay.

A fourth Commons file, the 3:45 AM fissure-20 spatter, is described as
fountaining and was not downloaded. It is the same night-fountain class.
`HARVEST_R06_EDGE_SEARCH_v01.json` and the pool checkpoint
`R6 tight glowing lava edge on the ground` record the hashes and the
licence pages. Stills were inspected as stills. No motion or audio review.

**Do not restart this fissure-20 search.** Chief needs a new source, or an
accurate alternative, before another tight-edge pass. Next harvest that is
still open: basalt, cores and wildlife, then the remaining composites and
full picture/polish QA. Nothing needs Ben.

## R6 USGS lava checkpoint (7 Nov UTC, Cursor)

Preserve **1/3**, PR **#575**, starting at `d58877f18c`. Spend **£0**.
Added `harvest_usgs_lava.py` and `HARVEST_USGS_LAVA_TECHNICAL_CHECK_v01.json`.
Pool now has the fissure-20 overflight as asset
`commons_usgs_fissure20_overflight`. No media in git.

One Commons file, category **PD USGS**, template `PD-USGov-USGS`.
The saved English template says the file is public domain in the United
States because it contains only U.S. Geological Survey material. The original
end card, kept as `sample_30s.jpg`, identifies it as a Hawaiian Volcano
Observatory helicopter overflight of a fast-moving lava flow from Fissure 20
at 7:52 AM HST on 19 May 2018. Credit on the plate is **USGS**. Source audio
is the helicopter and is excluded. Commons' own description line is truncated
by the uploader; the end card is the fuller identification.

Plate `plate_031_r06_lava_v01.mp4` is 167 frames / 6.68 s, 1920×1080, 25 fps,
silent, full decode, no loop and no interpolation. It uses source
**6.00–12.68 s**, after the opening USGS card and the yellow date caption,
and before the end card near 26.5 s. Black side bars are cropped (6 px each
side) and the burned-in USGS bug is cropped with the bottom 180 px, then the
picture is scaled uniformly **1.20×** and centre-cut. The existing R6 FACT
overlay `code_graphic_031_r06_fact_v01` (hash unchanged) starts **4.20 s**
into the plate, which is film **50.84 s**, the locked cue "baking the mud".
Film window remains **46.64–53.32 s**. This is the wide flow only. The shot
list's tight glowing-edge beat is not in this interval and is still open.
Do not reuse 6.00–12.68 s for row 7.

Media and `CONTACT_v01.jpg`: `/Users/benjaminoats/_desk/J2141-lava-v01/`.
Four encoded stills were inspected as stills. Component polish on this one
plate: **PASS, 0 failures, 0 warnings**. That is not a film PASS, KEEP, or
motion review. Reproduce into a fresh directory with `--render`; an existing
plate is verified and refused for overwrite:

```sh
/usr/bin/python3 <film>/07_Edit-Project/harvest_usgs_lava.py \
  --media-root <dir> --manifest <pool.json> --fact-card <r06 fact mov> --render
```

One archive candidate was examined. Two other Commons USGS fissure-20 titles
were identified and not downloaded. No exhausted search was restarted. NAS
offload at session start found nothing old enough to move; about 9.4 GB free.
No NAS deletion and no paid action.

**Next:** the tight lava edge, then basalt, cores and wildlife, plus the
remaining composites and full picture/polish QA. Source-ID and
sourced-simulation gate conflicts below stay with the Chief. Nothing needs Ben.

## R27 remaining composites checkpoint (7 Nov UTC, Codex)

Preserve **1/3**, PR **#575**, starting at `1bf020f12d`. Spend **£0**.
Added `composite_hubble.py` and `COMPOSITE_HUBBLE_TECHNICAL_CHECK_v01.json`.
Two unique 1920×1080 / 25 fps silent source-linked composites:

- Film **280.42–284.74 s**: existing `hubble_saa` alpha overlay on NASA
  STS-125 original **116.00–120.32 s**, 108 frames / 4.32 s. Sharp telescope
  left, existing schematic right. This orbit loop is illustrative, not a
  measured track/map; its explanatory geometry/readability still needs review.
- Film **284.74–289.02 s**: NASA STS-125 **668.80–673.08 s**, 107 frames /
  4.28 s; existing FACT starts 0.02 s later at **284.76 s** and lasts 3.6 s.
  Sharp telescope sits upper right, clear of the lower-left caption. NASA
  archival servicing footage illustrates Hubble, not an actual SAA shutdown.

Media, six inspected sample stills and CONTACT_v01.jpg:
`/Users/benjaminoats/_desk/J2141-r27-composite-v02/`. Both outputs use `_v02`
filenames. Earlier v01 outputs remain in their own folder: the FACT card
intersected the subject in sampled stills, so do not assemble v01. Full-size
midpoints and the current sheet inspected as static images only. Source
interval 664.48–673.08 was rejected as an uninterrupted proposal because
samples reveal an internal cabin-view cut. No new archive search or reset of
any exhausted budget. New intervals do not overlap the earlier approach and
release plates: this reel now has four assigned source stretches, below five.

Original/catalog/terms and both overlay SHA-256 verified before rendering.
Each new output fully decodes, has exact frame count/duration, no audio,
1920×1080 yuv420p at 25 fps. Both component polish checks **PASS, 0 failures,
0 warnings**; their reports/hashes are in the technical record. The crop is
928×696 at (176,12); blurred fill is 2.07×, sharp inset 1.16×. Four-sided
feather, light grade, fine grain and NASA credit applied. Source audio excluded;
no loops, interpolation, slowdown, VO changes or source overwrites.

Reproduce into a fresh output directory with `/usr/bin/python3
<film>/07_Edit-Project/composite_hubble.py --out <fresh-directory>`.
Detached **J2141-r27-composite-v02 finished exit 0**. Log and completion:
`/Users/benjaminoats/_desk/logs/J2141-r27-composite-v02.log` and `.done`.
No active render/download. NAS offload was invoked first; it deferred to the
01:00–06:00 window with 10.9 GB free. No NAS deletion or paid action.

This is a technical component checkpoint, no KEEP, whole-film PASS, audio or
motion perception. Remaining wider harvest, other composites, coverage/reuse
accounting, existing source/gate conflicts and full picture/polish QA remain.
Nothing needs Ben at this checkpoint.

## R41 finished plate checkpoint (7 Nov UTC, Codex)

Preserve queue **1/3**, PR **#575**. Starts from `7d089900d8`. Spend **£0**.
Built the already harvested NASA *Sunset over China* interval 3.60–8.00 s
into `plate_031_r41_atmosphere_v02.mp4` under
`/Users/benjaminoats/_desk/J2141-r41-plate-v02/`. No new archive search.

R41 film window is 418.86–423.24 s (4.38 s); encode is exactly 110 frames /
4.40 s at 25 fps. Trim 0.02 s from its tail at final timeline assembly;
never retime or trim the VO. Crop 1024×576 at (0,96), scale 1.875×, light
grade, fine grain and NASA corner credit. Native 12 fps time-lapse converted
to 25 fps by duplication: no loop, interpolation, slowdown or generated image.
Source is sunset, never relabel sunrise. NASA source audio excluded.

Source, catalog, excerpt and terms hashes verified. Entire output decodes;
1920×1080, yuv420p, 25 fps, no audio, exactly 110 frames. Six encoded stills
and CONTACT_v01.jpg inspected: blue atmospheric band and sun remain visible;
no source title/end-card in sampled frames. Component check output:

```text
polish gate PASS: 0 of 1 rows failed, 0 to look at
```

`HARVEST_R41_TECHNICAL_CHECK_v02.json` records hashes, command, metadata,
samples and component polish report/hash. `build_r41_limb.py` reproduces into
a fresh directory and refuses existing outputs. Preserve v01 (108 frames /
4.32 s) as failed evidence: do not assemble. Corrected v02 resets source PTS
and requests 110 frames explicitly. No checker changed or gate waived.

Detached `J2141-r41-plate-v02` completed **exit 0**; no active render. Log and
completion: `/Users/benjaminoats/_desk/logs/J2141-r41-plate-v02.log` and `.done`.
Media is persistent under `_desk`; no media committed. Required NAS offload
deferred to its 01:00–06:00 window with about 9.5 GB free; no NAS deletion.

This is component technical/still evidence only, no motion/audio perception,
KEEP, whole-film QA or picture-stage approval. Continue wider real-picture
harvest, remaining composites, coverage/reuse checks and full picture/polish
QA. Preserve exhausted search budgets and existing source/gate conflicts.
Nothing needs Ben at this checkpoint; no public or paid action.

## Hubble footage checkpoint (6 Nov, Codex)

Preserve queue **1/3**, PR **#575**, `worker/J2141-integrated-v01`.
Starts at `d957ee63c2`; spend **£0**, no publishing changes or stage approval.
Added one NASA original; pool now **17 assets**. No media in git.

NASA SVS **13160**, *NASA Resource Reel – Hubble 25th Anniversary – Highlights
from STS-125 Hubble Servicing Mission 4*. The official catalog identifies
approach and departure footage. Credit **NASA's Goddard Space Flight Center**
(the corner label reads NASA). Original WEBM, source page and NASA media terms
are preserved and SHA-256 recorded under
`/Users/benjaminoats/_desk/J2141-hubble-v01/`. Factual educational use with
acknowledgment and no implied endorsement; source audio entirely excluded.
These are NASA servicing-mission images, not the separately found animated
Hubble deployment or the IMAX feature. Terms are per this asset/interval;
recheck separately credited material before using another part of the reel.

Two adjacent R27a candidate cuts, before `hubble_saa` begins at **280.42 s**:

- Approach **112.00–116.00 s** → film **272.94–276.94 s**:
  `plate_031_r27_approach_v01.mp4`, 4.00 s.
- Release **661.00–664.48 s** → film **276.94–280.42 s**:
  `plate_031_r27_release_v03.mp4`, 3.48 s.

They form one film window with two distinct source stretches (no reused frames).
Preserve this assignment in the film-wide reuse accounting; neither is a
blanket approval to repeat the reel elsewhere. The 4:3 archive picture is
retained with feathered blurred fill, a light grade, fine grain and NASA
credit. Foreground scale is 1.50× / 1.55×; blurred fill 2.00× / 2.07×.
No looping, slowdown, interpolation or generated picture. Native source is
published around 59.94 fps and is converted to 25 fps by frame selection.
Archive softness and the full-frame look still require capable review.

The original fully decodes; both current plates fully decode, match hashes,
1920×1080, 25 fps, yuv420p, exact intended durations and no audio streams.
`HARVEST_HUBBLE_TECHNICAL_CHECK_v01.json` includes commands, hashes, formats,
source crop, source intervals, film positions, and component gate outputs.
`harvest_hubble.py` reproduces current versions into a fresh media directory,
refusing existing media. Final still sheet **CONTACT_v03.jpg** inspected.
This is still/technical evidence only: no motion, playback or audio review.

Both current component polish checks report **0 failed, 0 warnings**.
Earlier candidates and failures remain as evidence:
- Release v01 at 646 s contains an internal cabin cut; superseded, do not assemble.
- Release v02 chooses the right telescope interval but FAILs the split-panel
  check due to a residual embedded pillarbox edge. v03 crops that source border
  (928×696 at 176,12), retaining the telescope. No checker change or waiver.
The original v01 contact sheet and v02 gate FAIL remain in the media folder.
Component checks are not KEEP, a film PASS or approval.

Detached **J2141-hubble-v01 finished exit 0**. Log and completion:
`/Users/benjaminoats/_desk/logs/J2141-hubble-v01.log` and `.done`.
The two short corrective encodes finished in-session, with no active render.
One archive candidate examined in about 12 active minutes; search stopped
with candidates. No exhausted horse or other missing-input budget reset.
NAS offload was attempted first and deferred to 01:00–06:00 by the existing
rule, about 14 GB free. No NAS files removed or overwritten.

**Next:** continue wider real-picture harvest (lava/basalt, cores, wildlife,
Earth); compose remaining row graphics; reconcile existing source/gate conflicts;
perform full picture/polish QA and actual motion-capable review. The Hubble
row after 280.42 s still needs its graphic/FACT moving-plate composite.
Chief retains protected decisions; nothing new needs Ben at this checkpoint.

## Solar footage checkpoint (6 Nov, Codex)

Preserve queue **1/3** and PR **#575**, `worker/J2141-integrated-v01`.
This checkpoint starts from `fc61709050`. Spend **£0**, no publishing change.

Added two NASA SDO observed-image originals, bringing the pool to **16 assets**.
Originals, saved source pages/terms, sample sheets, row plates and composite:
`/Users/benjaminoats/_desk/J2141-solar-v01/` (about 70 MB). No media in git.

- R14b: NASA SVS **3693**, AIA launching filament, bands 304/171/211.
  Source 6.00–8.42 s, intended film 138.70–141.12 s, following the existing
  R14 core graphic ending 138.70. Crop `[320,0,1600,900]`, scale **1.2×**;
  removes baked source timestamp. This is false-colour EUV observational
  imagery with NASA's editorial zoom, not a computer simulation. Credit:
  **NASA/Goddard Space Flight Center Scientific Visualization Studio**.
  The prominence/corona is not a photospheric-temperature measurement; it
  illustrates the Sun in the approved comparison, not a thermometer.
- R46a: NASA SVS **12706**, separately credited raw **10 September 2017
  X8.2 flare**, 171/304-angstrom blend. Source 9.00–11.34 s, intended film
  469.88–472.22 s; next is existing `grid_shield` on “hardening”. Full frame,
  **1×**, credit **NASA/GSFC/SDO**. This is the raw event file, not the
  produced September sequence with Killer Tracks music. No source audio.

NASA media terms and individual credits saved and hashed. Factual educational
use with acknowledgment and no implied endorsement; no third-party visual
restriction found on these items. Do not use NASA identifiers as promotion.
The native observed time-lapses convert 30/29.97 fps to 25 fps by frame
selection, with no looping, slowdown, optical flow or generated picture.
Both plates have a light grade, fine grain and lower-left NASA/SDO credit.

R14 FACT composite uses the **unchanged** existing alpha card (SOURCES row 6),
starting at film **139.18 s**, with `overlay=0:-720` into upper-left sky,
clear of the prominence in sampled stills. Its original 1.92 s duration
remains; playback readability still needs the established review/final watch.
`COMPOSITE_RECIPE.json` and the tracked technical manifest contain the exact
command, input hashes and filter. No VO or sourced number changed.

Both originals, both plates and the composite fully decode. Hashes, dimensions,
25 fps, yuv420p, duration and absent audio checked. At 25 fps, intended durations
2.42/2.34 s encode 2.44/2.36 s; final assembler cuts on locked boundaries,
without shifting narration or the next graphic. Sampled source and output
sheets viewed as **stills only**, no motion/audio perception claimed.

Component polish outputs (all **0 failed, 0 warnings**):
```
polish gate PASS: 0 of 1 rows failed, 0 to look at -> polish_r14.json
polish gate PASS: 0 of 1 rows failed, 0 to look at -> polish_r46.json
polish gate PASS: 0 of 1 rows failed, 0 to look at -> polish_composite_r14_v02.json
```
Initial composite check misclassified moving video as a still because its
cut entry omitted `framing.offset`; the initial FAIL is preserved. Corrected
record names the actual original and offset 6.0. Same video passes; no checker
change, disabled check or waiver. Existing `owb-cg` venv supplied NumPy after
the worktree's default Python lacked it. No dependencies installed.

`HARVEST_SOLAR_TECHNICAL_CHECK_v01.json` embeds gate results, hashes, exact
recipes and static limits. `harvest_solar.py` reproduces indexing/plates from
preserved originals/evidence, refusing existing media. Component PASSes are
not a full-film PASS, KEEP, stage approval or final OK.

Detached batch **J2141-solar-v01 finished exit 0**, no active render/download.
Log and completion: `/Users/benjaminoats/_desk/logs/J2141-solar-v01.log` and
`.done`. The short FACT composite rendered in-session and completed exit 0.
Two solar candidates examined in about ten active minutes; search stopped
with candidates. No exhausted horse or other search budget reset. About
17 GiB free at start; daytime bulk NAS moves deferred by the existing rule.

**Next:** remaining real footage (lava/basalt, cores, wildlife, Hubble and
Earth), row composites, coverage/reuse accounting, source/gate-conflict
resolution and full QA. Earlier checkpoints and assets remain intact.
Nothing needs Ben at this build checkpoint. No KEEP or film-stage approval.

## Aurora footage checkpoint (6 Nov, Codex)

Preserve queue **1/3** and PR **#575**, branch
`worker/J2141-integrated-v01`. This checkpoint starts from `8b4f8386d0`.
The complete package remains unfinished. Spend **£0**; no public changes.

Three NASA CEO originals downloaded and fully decoded; two selected as
static candidates. Pool now contains **14 assets**, including the unassigned
third clip. Source excerpts, catalog, FAQ terms, hashes and contact sheet:
`/Users/benjaminoats/_desk/J2141-aurora-v01/`. FAQ explicitly allows reuse
and requests credit to **Earth Science and Remote Sensing Unit, NASA Johnson
Space Center** and a link to `https://eol.jsc.nasa.gov/` in delivery credits.
Per-item catalog identifies the crew origin and contains no third-party notice.
No source audio is used. Media stays outside git.

- R4c: **Aurora Borealis over Europe**, 5 April 2012, Expedition 30.
  Source 8.00–11.44 s; film candidate 31.86–35.30 s (after existing compass).
  This is Europe, never relabelled South Atlantic. Crop 1024×576 at (0,64).
  The remaining 0.02 s to row end is an assembly boundary, not a VO edit.
- R36: **Aurora Australis south of Australia**, 11 September 2011,
  Expedition 28; catalog pass rounds east of New Zealand. Source 18–22.88 s;
  film 373.84–378.72 s. Crop 1024×576 at (0,192). Row's existing 4.88 s
  duration overlay is composited as `composite_031_r36_durations_v02.mp4`.
  Its alpha layer moves **−950 px x / −300 px y**, into dark sky above and
  left of the aurora. **Reject v01 composite:** labels crossed the aurora
  and pale clouds, despite its polish metric PASS. v02 stills inspected.
  Original alpha/source words and timing are unchanged; SOURCES row 14.
- R50b: same southern sequence, **different interval 4–8 s**, film
  517.86–521.86 s. A 10 s source gap separates this from R36, satisfying
  the repeat-stretch rule. Two source stretches only; neither loops.
- **Northern United States**, 13 April 2012: downloaded/decoded but
  **unassigned**. Sampled frames are dark, with prominent station hardware.
  Do not count it as a usable aurora separator without further evidence.

All three row plates: 1920×1080, 25 fps, yuv420p, H.264 CRF18; source
1024×768 / 12 fps, crop then **1.875×** scale. This is native time-lapse
with frames duplicated for 25 fps, no optical flow, loop or invented frames.
Fine grain and small lower-left NASA credit added. Encoded stills inspected.
All originals, plates and v02 composite fully decode. **Polish PASS** on
midpoint samples for each of the three plates and v02 composite, no warnings.
These are component checks, not a whole-film picture/polish PASS or a claim
to hearing audio/watching motion. Ben's final watch remains under the existing
4 Nov rule; no capability-only hold is needed.

`HARVEST_AURORA_TECHNICAL_CHECK_v01.json` carries the media hashes, crop and
source intervals, reports (with report hashes), source alpha hash and exact
v02 composite filter. `harvest_aurora.py` indexes verified local originals and
builds the three plates with `--render`; existing media is refused. Run with
`/usr/bin/python3` (Pillow); use default `python3` for polish (NumPy).
This ffmpeg lacks drawtext, so the script uses a Pillow alpha NASA label.
The v02 composite recipe in the manifest uses ffmpeg overlay on the preserved
plate plus the preserved alpha MOV; never overwrite either earlier version.

Detached render completed **exit 0**, no live render/download remains.
Log/completion: `/Users/benjaminoats/_desk/logs/J2141-aurora-v01.log` and
`.done`. The corrected run's session was `J2141-aurora-v02` (already exited).
No master/UAT copy is claimed; these are persistent `_desk` components.
Disk has about 21 GB free; no NAS move was needed.

**Next:** continue the unfilled real-picture harvest (lava/basalt, cores,
wildlife, SDO/Hubble, remaining Earth clips). R2 needs its own northern
limb candidate; do not reuse the R4 interval. Preserve the exhausted horse
search budget and Titan/sourced-map conflicts. Then assemble overlays with
plates, check all row coverage/reuse and run full picture/polish QA. The
film stage remains in progress, no KEEP or final approval; nothing needs Ben.

## R41 limb checkpoint (6 Nov, Cursor)

Resume queue **1/3**. This branch continues PR575 at 59b9952551.
Harvested one NASA ISS limb plate for row 41. Spend £0. Two candidates
examined; the search stopped there.

- Admitted candidate: Gateway to Astronaut Photography, *Sunset over China*,
  Expedition 30, 13 April 2012, frames ISS030-E-235718 to ISS030-E-235829.
  File `sunsetchina_iss_20120413HD_web.mp4`, 1024×768, 12 fps, 13.83 s,
  sha256 `b547de4b…d2d48a`. Full-frame scale to 1920 is 1.875, under 2.35.
  Proposed use **3.60–8.00 s** (4.40 s). Stills at 3.6, 4, 7 and 8 s show
  the sun on Earth's limb and a blue atmospheric band, Earth in the lower
  frame. Mean luma on those stills is about 39–42. The opening title is
  still up at 2.8 s. The NASA end card is up by 11.2 s. Cut both out.
- Identity: the catalog calls this a **sunset**. It is not relabelled
  sunrise. It is the atmospheric-dome picture for the air row.
- Not admitted: *Sunrise and Sunset around Summer Solstice*
  (`solstice_iss_20120606HD_web.mp4`). Stills at 12, 24, 36 and 48 s show
  the limb, but the solar arrays cover it. The blue line is only an edge
  behind the arrays.

Media and contact sheet: `/Users/benjaminoats/_desk/J2141-r41-v01/`.
`HARVEST_POOL_v01.json` now has 11 candidates. No motion playback review.
No KEEP, PASS or stage approval. These are stills of single frames.

Remaining: the wider NOAA, USGS, ESA and Commons harvest, plate composites,
and full picture QA. No public state change and no Ben action.

## Twist-card checkpoint (6 Nov, Cursor)

Resume queue **1/3**. This branch continues PR575 at 98a638df88.
Added `code_graphics.py twist`: one alpha R30 card, 313.82–317.78 s,
1920×1080 / 25 fps, 99 frames. It follows the existing recap
(`code_graphic_031_r30_recap_v01`, ending 312.88 s) and does not replace it.
Labels match the locked line: `CASE CLOSED?` until the word "Are" (315.52 s),
then `ARE WE OVERDUE?`. Each line is under four seconds and under four words.
No locked words changed. No new measured claim.

The shot list's 0.3 s hard cut to black is an assembly cut after this card.
It is not baked here: a black frame would be a slab. Both overlays need the
graded moving ISS night-limb plate underneath, with that plate already
separating R29 from R30. Static samples of the encoded file were inspected
on a navy preview ground. That ground is not the plate.

Media and contact sheet: `/Users/benjaminoats/_desk/J2141-twist-v01/`
(1,529,406 bytes). `CODE_TWIST_v01.json` and
`CODE_TWIST_TECHNICAL_CHECK_v01.json` record the hash, argb, 25 fps,
3.96 s, 99-frame full decode and five distinct sample frames. Frame 0 is
transparent (fade in). No audio or moving-picture perception is claimed.
No KEEP, PASS or stage approval.

Reproduce into a fresh directory; existing output is refused:

```sh
/usr/bin/python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py twist --out <fresh-dir> --manifest <new-json>
```

All 14 earlier CLI modes stay in place. £0. No archive search, so the R41
and horse search budgets are unchanged. NAS offload still had nothing old
enough; about 3.8 GB free, so this batch stayed a small overlay.

Remaining: wider real-picture harvest, the R41 ISS sunrise-limb fallback,
moving plates around the R44 duration overlay, composites, source/gate
reconciliation and full QA. No public state change and no Ben action.

## Body comparison checkpoint (6 Nov, Codex)

Resume queue **1/3**. This branch continues PR575 integration at 40cbc13347.
Added `code_graphics.py bodies`: one full-frame R44 gravity component,
449.92–452.20 s, 1920×1080 / 25 fps, 57 frames. It reuses the existing
sourced common-zero bars (Earth 1.00, Mars 0.38; SOURCES row17) and adds real
NASA planet icons. Equal display diameters identify bars; this is not a
planet-size scale. Replace the older R44 alpha gravity component, never
insert this as another consecutive diagram. No locked words or cues changed.

The previous DSCOVR photo was already at two uses, so it is **not** reused.
Harvested NASA Apollo `as17-148-22727` instead (one candidate, about three
active minutes), verified original/API/policy hashes and inspected the
original still. Pool now has ten candidates. NASA image, API and source
preview live in `/Users/benjaminoats/_desk/J2141-bodies-v01/`; crop coordinates
and provenance are in the pool. Mars uses existing PIA00407: row38 and the
continuous row44 appearance remain its two-use limit. Track that at assembly.

Rendered media and encoded contact sheet:
`/Users/benjaminoats/_desk/J2141-bodies-render-v01/`.
`CODE_BODIES_TECHNICAL_CHECK_v01.json` records PASS for input/evidence hashes,
output hash, dimensions, fps, pixel format, 2.28 s duration, complete decode,
locked start cue, and five distinct encoded frames above the near-black floor.
The encoded contact sheet was inspected as stills. This does not establish
actual motion/audio perception, whole-film QA, KEEP or film-stage approval.
The gravity figure has a short reading window inherited from the locked cue.

Detached `J2141-bodies-v01` finished exit0; no live render. Log and completion:
`/Users/benjaminoats/_desk/logs/J2141-bodies-v01.log` and `.done`.
Reproduce with `code_graphics.py bodies --out <fresh-dir> --manifest <new-json>`
using `/usr/bin/python3`; existing media is refused. All 13 older CLI modes
are preserved. Added bytes are small (render 179,943 bytes); no paid spend.

NAS headroom: about 5 GB free. Required offload ran detached as
`J2141-scratch-emergency`, finished exit0 and found no eligible old scratch.
Log/completion use that name under `/Users/benjaminoats/_desk/logs/`.
No NAS file deleted; the older offload was already finished before this run.
The empty untracked shared-checkout blocker `reopen` was preserved at
`/Users/benjaminoats/_desk/rescue/J2141-20261106/reopen`.

Remaining: wider real-picture harvest, R41 ISS limb, moving plates around
the R44 duration overlay, R30 twist component, composites, source/gate
reconciliation and full QA. The R41 archive catalog was briefly located at
https://eol.jsc.nasa.gov/Videos/CrewEarthObservationsVideos/ (about two active
minutes); no clip candidate was downloaded/examined in depth or admitted.
Preserve prior missing-input budgets and the horse three-candidate limit.
No public state change, Ben action, KEEP or stage approval. £0.

## Integration checkpoint (6 Nov, Codex)

Resume at **1/3**. This branch consolidates the code and records from PRs
539, 551, 555, 562, 564, 569, 571 and 572. `INTEGRATION_SOURCES_v01.json`
records immutable source commits. All unique renderer modules/manifests are
retained; the shared `code_graphics.py` exposes all 13 batch commands.
The Commons harvest pool is retained, including its rights restrictions and
three-candidate horse-search limit. Original imported checkpoints follow below.
This is code/records integration, not acceptance of those batches or a film PASS.

`INTEGRATION_TECHNICAL_CHECK_v01.json`: all 13 CLI help paths exit 0;
all 73 manifest media entries exist and match their recorded SHA-256 values,
including superseded versions retained for evidence. No media copied or
re-rendered. £0 spent. No active render started. Previous technical reports
remain original evidence, not newly executed decode or visual checks.

Next: finish missing real-picture harvest, Mars/Earth body comparison and
R41 limb fallback; compose with moving plates and perform full picture QA.
Review overlapping cards/timelines and source-ID/simulation conflicts before
assembly acceptance. The source PRs remain open; merge or supersede them only
after this integration is reviewed. Do not rebuild their batches by mistake.
No Ben action, publishing change, KEEP or film-stage approval.

Disk policy checked: NAS offload deferred by its own 01:00–06:00 window,
with more than 8 GB free. This checkpoint adds text/code only.

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


# Consolidated continuation checkpoints

Imported without granting KEEP or film-stage approval. Original PRs remain open.

## Imported checkpoint: PR #539, d3377ec121c5

Worker: cursor (this checkpoint). Spend: £0. **Partial work, no KEEP, no Chief PASS, no film stage approval.**

## Continuation checkpoint (5 Nov, eighth run)

Preserve **1/3**. New branch `worker/J2141-opening-v01` (PR #495 is already merged). Added `code_graphics.py opening` and four row graphics, 1920×1080 / 25 fps:

- R1 poledrift, 4.52–8.34 s (file 3.84 s after frame rounding): real DSCOVR Earth disc, schematic arc from the Canadian side of this Americas plate off the top limb toward Siberia. Labels `1831 → TODAY`, `UP TO 55 KM/YR`, `> MARATHON / YR` (SOURCES row 1). Not a plotted World Magnetic Model track.
- R2 flip, 12.54–17.08 s (file 4.56 s): same Earth disc, bar magnet turns N to the south, blue air shell stays the same size. `POLES SWAP` holds under 4 s. This is the £0 picture for the question, not an atmosphere-loss shot.
- R13 layers alpha, 125.9–131.76 s (file 5.84 s): depth counter to `3,000 KM` / `BENEATH YOUR FEET` / `LIQUID OUTER CORE` (SOURCES row 6). Needs a graded moving plate. Not a measured core cross-section.
- R5 when1905 alpha, 36.14–39.36 s (file 3.20 s): `1905` / `PONTFAREIN, FRANCE`. A place stamp only, not the building timeline.

`CODE_OPENING_v01.json` and `CODE_OPENING_TECHNICAL_CHECK_v01.json` record cues, hashes, 1920×1080, 25 fps, pixel format, duration and error-free decode. Opaque preview mean luma is about 53. Alpha previews are transparent, so their luma is not a composite result. Media and contact sheet: `/Users/benjaminoats/_desk/J2141-opening-v01/`. Static stills inspected. No motion, audio or composite review. No KEEP, PASS or stage approval.

Earth plate `GSFC_20171208_Archive_e000678` (DSCOVR EPIC, 6 July 2015) is copied into `harvest_v01/` from the 029 harvest of the same NASA id and added to `HARVEST_POOL_v01.json`. Rows 1 and 2 share it, which is the two-use cap. Reproduce into a fresh directory:

```sh
/usr/bin/python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py opening --out <fresh-media-dir> --manifest <new-manifest.json>
```

No detached render left running. This batch is about 9 MB. £0. R21 compass fallback already exists. R41 is still the NASA ISS sunrise-limb plate, not built here. Wider archive harvest, the remaining mechanisms (timeline, strata, dynamo, belts, hubble_saa, sat_safe, saa, triptych, paleo, multipole, mars_vs_earth, extinction_check, grid_shield, poles_map, aurora, matuyama map) and full QA remain. Source-ID and sourced-simulation gate conflicts below still need Chief reconciliation.

## Earlier checkpoint

## Imported checkpoint: PR #551, 5a2a23be2829

Worker: cursor (this checkpoint). Spend: £0. **Partial work, no KEEP, no Chief PASS, no film stage approval.**

## Continuation checkpoint (5 Nov, ninth run)

Preserve **1/3**. New branch `worker/J2141-field-v01` from main. PR #539
(`worker/J2141-opening-v01`) is still open and is **not** in this branch.
Poledrift, flip, the 3,000 km depth ruler and the 1905 Pontfarein stamp stay
on that PR. This branch adds `code_graphics.py field` and four row graphics,
1920×1080 / 25 fps:

- R11 strata, 99.12–111.40 s (file 12.28 s): younger bands point north, older
  bands point south, gold line at `780,000 YEARS AGO` (SOURCES rows 4 and 5).
  The shot-list scale `> 2× modern humans (~300,000 years)` is not drawn.
  Those words are not in the locked line, so the label would fail WORDS.
  Needles are a schematic, not a measured rock section.
- R10 matuyama_map, 94.92–98.88 s (file 3.96 s): labelled blobs `MANCHURIA`
  and `JAPAN` with sample dots on the spoken names (SOURCES row 4). Not a
  traced coastline. The WHO card ends as "Japan" starts.
- R45 extinction_check alpha, 462.40–469.00 s (file 6.60 s): illustrative
  reversal stripes against three extinction marks and `NO LINK` (SOURCES
  row 2). Not a dated extinction chart. Lower third stays clear for the
  existing FACT card. Needs the fossil plate underneath.
- R46 grid_shield, 472.22–479.98 s (file 7.76 s): one satellite and three
  pylons under a shield arc. Storm strokes stop left of the arc. Labels
  `SATELLITES`, `POWER GRIDS` and `SOLAR STORMS` each hold under 4 s. Starts
  at "hardening" so an SDO plate can lead the row.

`CODE_FIELD_v01.json` records cues, source rows, paths and hashes.
`CODE_FIELD_TECHNICAL_CHECK_v01.json` records hash matches, error-free full
decode, 1920×1080, 25 fps, yuv420p or argb, and exact durations. Opaque mean
luma is about 44–59. The alpha overlay starts transparent. Static stills
inspected, including `CONTACT_v01.jpg` (the encoder's 75% preview frames;
the 780,000 label is on the later strata frames). No motion, audio or
composite review. No KEEP, PASS or stage approval.

Media: `/Users/benjaminoats/_desk/J2141-field-v01/` (about 4.2 MB). Reproduce
into a fresh directory:

```sh
/usr/bin/python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py field --out <fresh-media-dir> --manifest <new-manifest.json>
```

Detached `J2141-field-v01` finished exit 0. Log and completion:
`/Users/benjaminoats/_desk/logs/J2141-field-v01.log` and `.done`. No second
copy. £0. No archive search. The `field` dispatch in `code_graphics.py` sits
on the same line as PR 539's `opening` dispatch; keep both when merging.

Remaining: wider harvest, timeline, dynamo, belts, hubble_saa, sat_safe, saa,
the rest of the triptych, paleo, multipole geometry, the physical Mars
comparison, poles_map, aurora, the R41 ISS limb, composites and full QA.
Once PR 539 lands, DSCOVR `GSFC_20171208_Archive_e000678` is already at two
uses (rows 1 and 2); poles_map needs a different Earth plate. Source-ID and
sourced-simulation gate conflicts below still need Chief. No Ben action.

## Earlier checkpoint

## Imported checkpoint: PR #555, e7e3774e6343

Worker: cursor (this checkpoint). Spend: £0. **Partial work, no KEEP, no Chief PASS, no film stage approval.**

## Continuation checkpoint (5 Nov, tenth run)

Preserve **1/3**. New branch `worker/J2141-saa-v01` from main. PR #539
(`worker/J2141-opening-v01`) and PR #551 (`worker/J2141-field-v01`) are still
open and are **not** in this branch. Poledrift, flip, layers, the 1905 stamp,
strata, the sample map, extinction and the shield stay on those PRs.

This branch adds `code_graphics.py saa` and five 1920×1080 / 25 fps renders:

- R25 belts hold, 246.50–251.14 s: the belt rises to the spoken line and the
  label `600 KILOMETERS` lands on that word (SOURCES row 10). `BEYOND` is the
  word before it. Limb arc, not a flat-disc planet. The `600` label has about
  one second.
- R25 belts sag, 259.90–264.78 s: the same surface zero drops to `200 KILOMETERS`,
  then `HALF THE HEIGHT` and `SPACE STATION`. The station mark is twice the
  200 km line. `400 KM` is not labelled: it is not in this spoken line.
  A real ISS plate belongs in the gap 251.14–259.90 s, so these two renders
  are not back to back.
- R27 hubble_saa alpha, 280.42–284.74 s: an orbit dot crosses a dent wedge.
  Labels `SEVEN TO NINE`, `ORBITS`, `EVERY DAY` (SOURCES row 11). It ends as
  the existing FACT card starts at 284.76 s. Lower left stays empty. Not a
  count of measured Hubble orbits.
- R28 sat_safe alpha, 296.96–299.80 s: panel lights go out under `SHUT DOWN`
  and `NON-ESSENTIAL` (SOURCES row 11). Needs the ISS plate underneath.
- R29 saa, 301.20–306.32 s: one region widens, then splits. Labels `SINCE 1970`,
  `WIDENED`, `TWO LOBES` (SOURCES row 12). Not a coastline. `24,000 nT`,
  `22,000 nT` and `20 km/yr` stay off screen because this line does not say them.

`CODE_SAA_v01.json` records cues, source rows, paths and hashes.
`CODE_SAA_TECHNICAL_CHECK_v01.json` records hash matches, error-free full
decode, 1920×1080, 25 fps, yuv420p or argb, durations within half a frame,
and five distinct frames each. Opaque mean luma is about 41–53. Alpha
overlays start transparent. Static stills inspected, including
`CONTACT_v01.jpg`. No motion, audio or composite review. No KEEP, PASS or
stage approval.

Media: `/Users/benjaminoats/_desk/J2141-saa-v01/`. Reproduce into a fresh
directory:

```sh
/usr/bin/python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py saa --out <fresh-media-dir> --manifest <new-manifest.json>
```

Rendered in this run, exit 0. £0. No archive search. No paid generation.

Remaining: wider licensed harvest, the building timeline, dynamo, paleo,
multipole geometry, the physical Mars comparison, poles_map, aurora, the R41
ISS limb, composites and full QA. R21's compass fallback is already in the
mechanisms batch. Source-ID and sourced-simulation gate conflicts below still
need Chief. No Ben action.

## Earlier checkpoint

## Imported checkpoint: PR #562, a81037731246

Worker: cursor (this checkpoint). Spend: £0. **Partial work, no KEEP, no Chief PASS, no film stage approval.**

## Continuation checkpoint (5 Nov, dynamo run)

Preserve **1/3**. New branch `worker/J2141-dynamo-v01` from main. Open PRs
#539 (opening), #551 (field) and #555 (SAA) are not in this branch. This
branch adds `code_graphics.py dynamo` and three full-frame 1920×1080 / 25 fps
schematics on the harvested Blue Marble disc:

- R16 align, 159.32–168.76 s (file 9.44 s): iron-current loops ease into one
  dipole before "However". Longer than the shot list's 8 s because 8 s would
  cut inside "steady south pole". The SVS separator still starts on "However".
  Loops are a schematic, not a measured core flow (SOURCES row 6).
- R17 tip, 172.68–188.36 s (file 15.68 s): backwards eddies fight the main
  flow, the dipole weakens, then turns over. The file includes the pause
  after "over." and ends as row 18's first word starts. Not a sourced
  simulation frame.
- R52 settle, 544.00–547.70 s (file 3.72 s, 93 frames): loops slow and the
  compass's red north-seeking end locks toward the bottom of the frame,
  labelled `COMPASS SOUTH`. This is not the generations tally. It ends as
  row 53 starts.

Labels are four words or fewer and each caption window is under 4 s.
`CODE_DYNAMO_v01.json` records cues, source rows, paths and hashes.
`CODE_DYNAMO_TECHNICAL_CHECK_v01.json` records hash matches, error-free full
decode, 1920×1080, 25 fps and yuv420p. Static samples sit near mean luma 47–50.
Contact sheet: `/Users/benjaminoats/_desk/J2141-dynamo-v01/CONTACT_v01.jpg`.
Stills inspected. No motion, audio or composite review. No KEEP, PASS or
stage approval.

Media: `/Users/benjaminoats/_desk/J2141-dynamo-v01/` (about 8 MB). Reproduce
into a fresh directory:

```sh
/usr/bin/python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py dynamo --out <fresh-media-dir> --manifest <new-manifest.json>
```

Disk about 13 GB free, above the 8 GB daytime NAS exception, so no scratch
move. £0. No archive search. Still unfinished: paleo, poles_map, aurora, the
building timeline, flip use 2, layers tight on the core, multipole part 2,
the full triptych, the wider harvest, composites and QA. R21 compass fallback
is already in mechanisms v02. R41 stays the NASA atmosphere plate, not a new
render. Chief still owns the R54 asset-identity and sourced-simulation gate
conflicts below.


## Imported checkpoint: PR #564, 8150ceb5f217

Worker: codex, then cursor. Spend: £0. **Partial work, no KEEP, no Chief PASS, no film stage approval.**

## Continuation checkpoint (5 Nov, cursor sky batch)

Preserve **1/3**. This branch is `worker/J2141-sky-v01`, from current `origin/main`. It does not contain the still-open partials on PRs #539 (opening), #551 (field), #555 (SAA) and #562 (dynamo). Those already render poledrift, flip, layers, the 1905 stamp, strata, the Matuyama map, extinction check, grid shield, belts, Hubble SAA, satellite safe-mode, the anomaly chart and the dynamo align/tip/settle. This batch adds the five named graphics none of those branches include:

- R32 `paleo`, 326.34–336.10 s (9.76 s), full frame. Two bars on one zero: today's field at the 100,000-year high, and the million-year average at half height, which is the sourced "twice". No `8×10²²` figure. Not a sediment-core plot.
- R40 `temp_poles`, 415.04–417.92 s (2.88 s), alpha. Six temporary poles pop inside a ring after the existing dipole-strength overlay. Label `TEMPORARY POLES`.
- R47 `tangle`, 488.14–492.86 s (4.72 s), full frame. Starts on "tangling", after room for the NASA SVS plate at the head of the row. Label `SEVERAL POLES`. Schematic lines, not a Glatzmaier frame.
- R48 `poles_map`, 493.66–499.30 s (5.64 s), alpha. Pin is for southern Africa on `harvest_v01/GSFC_20171208_Archive_e001788.jpg` pasted at (510, 90) at 900 px. Tahiti is named (`NORTH POLE` / `TAHITI` / `PACIFIC`) and not pinned: that Blue Marble face does not show the Pacific. The pin pulses so it does not sit still for 4 s.
- R51 `aurora`, 522.62–532.98 s (10.36 s), full frame. The same Blue Marble, circular-masked onto navy and dimmed, with moving green and crimson arcs. City cards `LONDON`, `CAIRO`, `MUMBAI`, `SYDNEY` each fade within 3.2 s of the locked word. They are names, not map coordinates. Small `NASA` credit, bottom left. The 0.06 s past "nights" sits in the pause before the next sentence (534.48 s).

`CODE_SKY_v01.json` and `CODE_SKY_TECHNICAL_CHECK_v01.json` record hashes, 1920×1080, 25 fps, alpha or yuv420p, and error-free full decodes. Opaque mid-frames sit above the near-black floor (paleo ~35, tangle ~30, aurora ~43). Alpha frames are transparent on purpose. Media and contact sheet: `/Users/benjaminoats/_desk/J2141-sky-v01/` (about 8.7 MB). Stills of the previews were inspected. No motion, composite or playback review. No KEEP or PASS.

Detached `J2141-sky-v01` finished exit 0. Log and completion: `/Users/benjaminoats/_desk/logs/J2141-sky-v01.log` and `.done`. Reproduce into a fresh directory:

```sh
/usr/bin/python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py sky --out <fresh-media-dir> --manifest <new-manifest.json>
```

The harvest photograph is gitignored and already lives in the film's `07_Edit-Project/harvest_v01/`. Spend £0. No new archive search, so no missing-footage budget was used.

Still unfinished: the wider NASA/NOAA/USGS/ESA/Commons harvest, a single building timeline (only separate WHEN stamps exist), the R30 "CASE CLOSED?" card, the R33 near-zero dip, a physical Mars/Earth body comparison, the R41 NASA limb fallback plate, plate composites and picture/polish QA. Open PRs #539, #551, #555 and #562 still need a merge that keeps every `code_graphics.py` mode. Source-ID and sourced-simulation gate conflicts below remain for Chief. No Ben action.
## Imported checkpoint: PR #569, 332e9697e8a0

Worker: cursor. Spend: £0. **Partial work, no KEEP, no Chief PASS, no film stage approval.**

## Continuation checkpoint (6 Nov, core batch)

Preserve **1/3**. This branch adds three full-frame £0 renders only. It does
not merge open PRs #539, #551, #555, #562 or #564, and it does not drop their
modes. Reproduce into a fresh directory:

```sh
/usr/bin/python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py core --out <fresh-media-dir> --manifest <new-manifest.json>
```

- R12 `flip_tight`, 112.98–121.98 s: second, tighter dipole turn on the harvested Blue Marble (`GSFC_20171208_Archive_e000678`). The air ring stays. A dive toward a golden core starts on "secret". This is not the R2 wide flip.
- R14 `layers_core`, 132.70–138.70 s: churning outer core, labels OUTER CORE then LIQUID IRON. Ends before the FACT card at 139.18 s. No temperature figure.
- R33 `paleo_dip`, 345.00–349.16 s: qualitative bar for "nearly to zero" then "snapped back". It starts after the existing 3.6 s Laschamp date card. It is not the sourced 6% rings chart.

Media: `/Users/benjaminoats/_desk/J2141-core-v01/`. Technical checks in `CODE_CORE_TECHNICAL_CHECK_v01.json`. Navy preview is not a finished plate. No motion, audio or composite review. £0.

Still open: wider harvest, the building timeline, Mars/Earth bodies under the existing R44 overlays, the R41 ISS limb fallback, composites, QA, and a Chief merge of the open graphic PRs that keeps every mode. Titan identity and sourced-simulation gates stay with Chief. No Ben action.

## Continuation checkpoint (5 Nov, seventh run)

## Imported checkpoint: PR #571, 8ae3c85e0923

## Continuation checkpoint (6 Nov, Codex timeline batch)

Preserve queue **1/3**. Added `code_graphics.py timeline` with five unique
3.6 s alpha overlays at locked date cues: R5 1905 (36.14), R10 1929
(89.94), R20 1830s (209.10), R24 2013 (234.58), R29 1970 (301.44).
Dates accumulate in narrative order and retain chronological screen order.
Spacing is categorical and labelled “NOT TO SCALE”; no invented historical
measurements. Source links remain SOURCES rows 3, 4, 8, 9, 12.

These are the **historical-date** timeline components. Geological ages and
physical durations remain separate; this does not certify every WHEN in the
film. Replace standalone WHEN stamps in these windows rather than stacking
them: in particular the earlier R24 date overlay and PR539 R5 place stamp.
R5 still needs its Pontfarein place caption. The upper timeline leaves the
lower WHO/FACT region clear, but all subject clearance needs composite review.

`CODE_TIMELINE_v01.json` records sources, state, timings, paths and hashes.
`CODE_TIMELINE_TECHNICAL_CHECK_v01.json`: PASS for all five hashes,
1920×1080 / 25 fps / argb, 3.6 s, exact locked date starts, alpha bounds and
complete error-free decode. Static encoded-frame sample inspected. No actual
motion/audio review, composite acceptance, KEEP or film-stage approval.

Media: `/Users/benjaminoats/_desk/J2141-timeline-v01/` (6,482,299 bytes),
including `CONTACT_v01.jpg` and `encoded_final_timeline.png`.
Detached tmux `J2141-timeline-v01` finished exit 0; log and completion:
`/Users/benjaminoats/_desk/logs/J2141-timeline-v01.log` and `.done`.
Reproduce into a fresh directory with `code_graphics.py timeline --out …
--manifest …`; existing media is refused. £0 spent; no archive search,
search-budget reset, narration change or publishing change.

NAS offload was required at ~10 GB free and began copying old scratch
`/private/tmp/j1843-capacity`. The original in-process copier was stopped
before restarting under detached tmux `J2141-scratch-offload`; the partial NAS
copy is retained and the existing script resumes it under its lock/checksum
rules. Log: `/Users/benjaminoats/_desk/logs/J2141-scratch-offload.log`;
completion: same prefix `.done`. Missing completion means still running:
never start another copy. No successful offload or regained headroom claimed.

Earlier open PRs #539/#551/#555/#562/#564/#569 remain separate and must be
integrated without losing their CLI modes. Remaining work: licensed archive
harvest, Mars/Earth bodies, R41 ISS atmosphere fallback, complete row
composites and QA. Source-ID and sourced-simulation/map gate conflicts below
remain unresolved; no gate has been waived by this build checkpoint.

## Imported checkpoint: PR #572, cb3ecfa51c83

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
