# J2089 v31 — current graphics inventory and protected source decisions

7 November 2026, codex specialist worker, GBP0. Original plan remains 1/4.
Resume worker/J2089-rights, /private/tmp/J2089-rights, based on 7aabea0c3a.

CURRENT_EXPORT_INVENTORY_v31.json reconciles 12 current manifests, applies later
correction manifests by id, and verifies all 62 current render files against
their recorded SHA256. All 62 files in the historical v22 inventory also match.
Uranus uses render_sha256 rather than sha256; both schemas are handled.
GRAPHICS_COVERAGE_v01.json now points to the current inventory and explicitly
marks legacy remaining_builds/preview notes as historical. No media or approval
was changed. This removes the misleading implication that completed renders
still need to be rebuilt. Reproduce with reconcile_export_inventory_032.py.

## Chief decisions required before further harvest/composite work

The missing-footage search has already crossed multiple worker runs. Do not
restart its investigation budget or keep issuing decorative composite trials.
Chief should read HARVEST_INVENTORY_v23.json, RIGHTS_REVIEW_v27.md and the latest
SHOT_LIST_v07.md, and give one bounded next scope:

- Frame 0: name an acceptable native-motion source or explicitly scope the
  approved fallback route. Existing Huygens reconstruction was rejected; a
  still push is not native motion.
- Huygens: resolve quality/crop acceptability for the reserved mosaics before
  using them, preserving final appearance/upscale checks.
- Dragonfly/APL: provide the documented reuse permission or choose/scope an
  honest alternative. Existing policy evidence is not a clip-specific grant.
- Resolve picture/source acceptance for the remaining allocations, including
  PIA10008's map/grid/missing-data hold; rights evidence alone is insufficient.
- Use a reviewer with demonstrated moving_video_input for J2346 (R23) and
  J2363 (R16). These remain separate open jobs, not approvals of J2089.

After those decisions, finish licensed harvest, actual moving-plate composites,
Short decoded-frame/crop exclusions, final reuse/VO timing and all film gates.
The original 1/4 is retained because licensed harvest is unfinished. No stage
PASS, final OK, locked script/VO edits, generation, YouTube or social writes.
No public push attempted; existing local integration restriction preserved.

Storage: this run began below 8GB free. Guarded nas_offload.py --apply started,
then was interrupted safely to resume detached as tmux J2089-offload-1518.
Log /Users/benjaminoats/_desk/logs/J2089-offload-1518.log; completion
/Users/benjaminoats/_desk/logs/J2089-offload-1518.done. Check before restarting;
missing completion means still running. Local/NAS partial retained for retry.
