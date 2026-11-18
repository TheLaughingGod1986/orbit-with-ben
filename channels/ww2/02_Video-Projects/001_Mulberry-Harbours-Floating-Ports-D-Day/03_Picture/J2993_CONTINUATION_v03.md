# J2993 continuation — 18 November 2026

Codex covering. Work remains in progress. No finished master, full-film QA verdict, or submission for Ben's watch. £0 spent in this run.

## This checkpoint

- Ten new 1920×1080, 25 fps, silent 12-second graphic drafts: G1, G4, G6, G8, G9, G10, G11a, G13, G14, G15. Original G11 remains from the earlier checkpoint. Five graphics remain: G2, G3, G5, G7, G12.
- `draw_engineering.py` draws tide/shore change, the floating Spud/Whale mechanism, harbour components, Type A1 dimensions, construction totals and target-versus-July-average cargo bars. `draw_operational_maps.py` draws approximate endpoint maps using the existing Natural Earth geography cache. These are explanatory schematics, not reconstructed engineering plans or surveyed historical routes.
- Still samples inspected for layout and geometry. Fixed the first G6 draft's disconnected supports before the current render. No motion or audio perception is claimed.
- All ten current MP4s fully decoded without error: 1920×1080, 25 fps, 300 frames, 12 seconds, no audio. See the two technical-check JSON files. Python compilation and diff whitespace check also completed.
- Current media lives on studio-live under `03_Picture/engineering_drafts_v02/` and `03_Picture/operational_maps_drafts_v01/`. All 44 current files were copied and SHA-256 verified; exact paths are in `graphics_media_sha256_v02.json`. The earlier three-graphic `engineering_drafts_v01/` checkpoint is superseded. Use v02 for the six current engineering clips.
- Archive retry has finished (exit 0; no tmux process remains). Nine downloaded retry files have matching hashes; caption/contact-sheet findings are in `archive_retry_review_v03.json`. Duplicate scans do not add coverage. 26-G-2963 has a candidate despite its record's ERROR status, and shows waves at a sunken-ship breakwater, not destroyed caissons. 80-G-252794 remains unresolved. All these candidates still require primary rights verification and full-resolution assessment; no KEEP is asserted.
- Added `graphic_coverage_v01.json` with narration-anchor assignments and the remaining graphics. G13 belongs at S43b, not S41. A twelve-second graphic is a building block, not permission to freeze or repeat it for the full paragraph.
- `11_Upload-Package/metadata_draft_v01.json` contains the existing 69-character script title, draft description/Sources line/tags and six provisional Scribe-aligned chapter times. It is explicitly not uploadable: final archive credits, final-master timings, the master itself and QA are missing. No channel account or upload was touched.

## Reproduce current drafts

From this film's `03_Picture/`, run the two Python renderers with fresh output folders under `$STUDIO_SCRATCH` (ffmpeg refuses overwriting). Engineering needs `--out <folder> --video`. Maps additionally need `--geography /Users/benjaminoats/_desk/ww2/J2993/ne_10m_admin_0_countries.geojson`. Inputs remain `/tmp/J2993-inputs/`; narration and Scribe remain on studio-live at the paths in the earlier handoff. Source values are from J2991's existing SOURCES.md S5; cargo comparison uses S3. These implementations do not constitute a new independent claims pass.

## Resume without repeating completed work

1. Read this file and `ARCHIVE_CORRECTIONS_v02.md`. Preserve the existing five-step job plan at 1/5; archive clearance is not complete. Do not restart the completed archive downloader. Inspect manifest outcomes rather than using its exit code as an approval.
2. Finish primary rights/subject checks and replacement images for rejected or underspecified shots. This run's direct IWM BU1024 fetch returned 403 and Navy 80-G-285176 returned 502. Exact-ID indexed searches did not resolve IWM A25799/H35379; no clearance was inferred. Do not restart unchanged broad searches indefinitely.
3. Review G8's component schematic against the upstream narration's “five interlocking rings” wording; no literal concentric rings are asserted by this draft. Complete the five remaining graphics and expand coverage within long narration paragraphs.
4. Resolve the four previously flagged fuzzy anchors and build the actual edit to the existing narration. Finish a new WW2 score under the written credit rules; do not borrow OWB/HOS media. Assemble the full film, verify technical audio/picture/caption checks, finish credits and chapters, then submit the finished cut through the normal review/Ben-watch path.

Worktree: `/tmp/J2993-wt`, branch `codex/J2993-picture-prep`, existing OWB draft PR #1012. The shared queue still records repo=owb for J2993, so this run preserves that existing continuation point; the newer standalone WW2 checkout is not substituted or force-updated. Nothing has been merged.
