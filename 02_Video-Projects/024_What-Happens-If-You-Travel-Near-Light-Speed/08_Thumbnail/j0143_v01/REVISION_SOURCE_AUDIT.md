# J0143 revision — source decision needed

Codex, 12 Oct 2026. Worker audit only; no editorial PASS or final OK.

Chief reopened J0143 at 10:49Z and recorded the changes on thread #6122765281: replace Voyager with the ship from 024’s locked trip picture, make it at least 40% of frame height, add a blue rim glow, retain the approved answer and teaser copy, and update PR #139.

## Finding

The current v05b trip chapter contains no suitable whole ship plate that I could locate. I inspected every trip cut on a contact sheet, the corresponding source inventory, the graphics implementation and the Omni return sheet. The available craft are:

- **3:44–3:53, row 21:** Artemis launch footage, dominated by exhaust. This is a launch rocket, not a whole ship cruising in blue starlight.
- **5:06.87–5:12.70, row 26:** `Earth_Views_from_the_International_Space_Station.mp4`, source offset 110 seconds. Docked spacecraft appear on the right, but the assembly is clipped by the top and right frame edges. I checked source frames at 90, 95, 100, 105, 110, 115, 120 and 125 seconds; these do not supply a whole isolated ship.
- **5:12.70–5:17.07, row 27:** `orbit_returns_omni_v01.mp4`, source offset 5 seconds. Orbit floats over Earth beside cropped station structures; no whole ship can be taken from this shot without inventing missing structure.
- The other trip shots show Earth, ISS crew, clocks, starlight and contraction bars. `code_graphics.py` represents the ship in the contraction graphic as a dot, not a ship asset.

The source audit contact sheet is `/Users/benjaminoats/_desk/handoff/J0143-trip-source-audit.jpg`. It uses the existing v05b per-cut review frames, labelled with cut index, film time and source. The final tile is the start of the following chapter for boundary context. `REVISION_SOURCE_AUDIT.json` records the trip cut list and SHA-256 hashes. Media remains outside git.

## Disposition and next step

**Parked for Chief: identify the intended whole-ship file/frame in 024, or approve an alternative existing no-spend plate.** The current inventory does not support the specified revision while keeping the subject whole. Voyager remains rejected; v01 is retained for history and is not a newly approved deliverable.

Once that source is named: mask/crop the existing ship, size its visible body to at least 288 px on the 720 px cover, add the blue rim, retain `YOU: 1 YEAR / EARTH: 7 YEARS` and `OUTRUN / EARTH’S CLOCK`, render both, re-run the colour gate and inspect the 168×94 tiles, then return for Chief review. No new cover was scored in this run: the old v01 automated results do not approve this revision.

Queue progress remains 1/3: source audit complete; revised covers and final evidence await the source decision. No spend, generation, Studio change, upload, merge or rule change.
