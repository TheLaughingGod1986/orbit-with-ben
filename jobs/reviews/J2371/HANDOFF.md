# J2371 — partial graphics package, continuation required

7 November 2026. Worker `macbook`. **Not complete, not KEEP, not assembly-ready.**
£0 / zero credits. No generation service, YouTube, scheduling, source-media writes,
or NAS writes. HOS checkout untouched. Locked CSV, script and VO unchanged.

## Delivered on disk

17 draft media files under `/Users/ben/_desk/renders/J2371/`:

- Six chapter cards R08/R20/R33/R45/R54/R64: 1920×1080, 30 fps, exactly 75 frames /
  2.50 seconds; 0.40-second text entry/exit, 1.70-second full-opacity hold, lifted
  navy background. Assembly still owns the actual crossfades against its plates.
- Five transparent QTRLE/ARGB overlay MOVs R17/R38/R43/R52/R61, with CSV phase
  boundaries rounded to the nearest frame. No baked plate or black slab. Static
  label holds capped at 3.8 seconds. R43 includes its 25 OCTOBER 2016 callout.
- Six full-frame **drafts** R02/R24/R29/R35/R56/R69, H.264, real harvested NASA
  source images, row-specific graphic objects. These are initial layouts requiring
  the refinements below, not an artistic or scientific approval.

`GRAPHICS_MANIFEST_v02.json` is authoritative: it selects cards/overlays v02,
R29 v02 (masked out a neighbouring-body crop edge), and the other full frames v01.
Older versions remain untouched. Every selected media file has a SHA-256 hash.
Full-frame source hashes and exact NAS input paths are recorded. Media is **local
on the MacBook only**, not delivered to studio-live. This follows this run's
instruction to keep writes inside the checkouts / `_desk`. No media is in git.

## Evidence

`VERIFICATION_v02.json`: 17 actual encoded files read back; hashes, 1920×1080,
frame counts, duration within 1/30 second of CSV, alpha format for overlays,
and three decoded samples per file checked. Full decode ran for every render.
Opaque sampled frames pass mean luma >=28 or p95 >=50; transparent overlays
must be assessed after compositing, not as opaque black pictures.

The existing `verify_lifted_navy_luma.py` ran and reproduced the committed model
artifact without a git diff. The renderer uses its #162238/#1F3150 endpoints.
Preview contact sheets and decoded PNGs are under the render directory. The
worker inspected still sheets; no moving-video or listening claim is made.

## Remaining work, in order

1. **R15 source/layout decision.** The locked plan names PIA20534 as a Pluto
   panorama, but also asks for a Pluto disc in its third phase. The harvested
   2042×1006 PIA20534 is a rectangular surface panorama, not a full globe.
   Ask the reviewer for a consistent layout or approved genuine-globe replacement;
   do not map this panorama onto an invented spherical surface. No R15 was made.
2. **R48 geography input.** Obtain a sourced vector Texas + Oklahoma boundary
   with provenance and appropriate projection/scale, then implement its two
   phases over the existing PIA14458. Do not draw an invented state outline.
   No R48 was made. Sibling harvest still owns its stills/native-motion work.
3. **Finish the six full-frame drafts against the plan.** R02 currently uses a
   separate width object, rather than a caliper anchored across the glacier;
   finish the geographic comparison. R24's half-Pluto bar needs an unambiguous
   comparison reference (Moon disappears in phase 2 to avoid misidentification).
   R29 is a dial/sightline sketch, not a physically modelled barycentric/rotation
   explanation; check the facing-hemisphere teaching before KEEP. R35's boost
   preview follows the CSV but needs a VO-word timing check. R56 needs explicit
   thermometer scale endpoints and confirmation of the temperature-range cue.
   R69 needs the planned moving distance counter and a clearer trajectory scale;
   its current arrow is an uncalibrated progress path.
4. **Overlay integration.** Composite the five alpha gauges over the exact graded
   NASA plates and inspect subject clearance, actual VO-word timing and physical
   clarity. R38 uses discrete timeline milestones, not a proportional time axis;
   integrate with the film's progressive timeline. R52/R61 are diagram drafts,
   not measured terrain cross-sections. Recheck their explanatory geometry.
5. **House typography.** This machine has no Roboto. Drafts use the explicit
   Arial Bold fallback from the existing 031 renderer. Supply approved house
   font and rerender before final graphic approval; do not call fallback final.
6. Deliver approved media to studio-live through an authorised continuation,
   verify the copy hashes, then run the assembled picture/polish/perceptual gates.
   Technical checks here do not waive any production gate or unblock Shorts.

The next worker should reuse these renderers and manifests, use a fresh output
version, and preserve old files. Successful encoding is not completion of J2371.

## Reproduce

Python environment used: `/Users/ben/_desk/J2141-venv/bin/python` (Pillow).
`ffmpeg` / `ffprobe` are on PATH. No numpy or paid API required.
From the film's `07_Edit-Project` directory:

```sh
python code_graphics.py --out <new-version-dir> --manifest <cards-overlays.json>
python full_frame_graphics.py --sources <harvest_v01/matched> --out <new-version-dir> --manifest <full-frame.json>
python verify_graphics.py --manifests <cards-overlays.json> <full-frame.json> --out <verification.json> --frames <decoded-frames-dir>
```

`--preview` produces stills without encoding; full-frame `--rows R29` selects
specific implemented rows. The tools refuse to overwrite existing media.
Unsupported R15/R48 are explicitly recorded as remaining work.
