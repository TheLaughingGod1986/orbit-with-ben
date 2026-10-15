# 027 thumbnail A/B/C — J0328 worker handoff

15 October 2026. Codex. Drafts for Chief review; no final approval, upload, scheduling or live Test & Compare.

## Deliverables

`abc_v01/earth_spin_thumb_A.jpg`: **OCEANS MOVE** (answer: the slow-stop ocean redistribution).
`abc_v01/earth_spin_thumb_B.jpg`: **ONE-YEAR DAYS** (the no-spin solar-day consequence).
`abc_v01/earth_spin_thumb_C.jpg`: **AIR RACES ON** (the sudden-stop inertia question).

All use the approved real EPIC Earth hero, no Orbit, with house Arial Black, white text and one yellow hook word. The text stays on the clear left edge, away from the globe and duration badge. The intact 650 px globe occupies 36% of the 1280×720 frame. B/C test different consequences on the same plate, not unrelated art. Claims are already in this film's SOURCES.md and CLAUDE_CLAIMS_v01.md; no spoken lines changed.

The original /private/tmp EPIC clip is gone. Recovered its unobscured Earth from frame zero of the locked v01l master (crop 460,40–1460,1040), excluding the master’s NASA credit in the lower left. This is the same opening view; a small amount of the master’s finishing is baked in. Graded the globe and composited it on a blue/purple/teal radial backdrop. No generated imagery or credit spend.

## Verification

`thumb_preview.py long ... --score` exited 0 for all three. A: saturation 156.2, near-black 2.6%; B: 121.1, 2.5%; C: 160.4, 2.1%. Phone sheet inspected at the provided 168×94 size: all words readable, globe whole, text separate. These are automated checks and worker observations; Chief owns the creative review and final decision.

`abc_v01/META.json` records the full hashes and source-frame hash. JPEGs are below 400 KB each. `abc_v01/contact_sheet.jpg` is the review contact sheet.

The dry-run returned `ok: true`, `dryRun: true`, `published: false`, thumbnail A resolved and three ABC entries. Private, intended schedule 2026-11-22T18:00:00Z. Master SHA-256 remains `7d51961fabfe7e4e66e2e3bfd457b5f0fe9fa995572682cab6ecb5c7f94d4c96`. The dry-run's `api_done` thumbnail and `scheduledOnPlatform: true` fields are simulated checklist fields, not evidence of any live change.

Planned test T008 in THUMB_LEDGER.json has no video ID, start date or result. It must not be treated as an armed test or maker-performance evidence.

## Durable media

Mini: `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/08_Thumbnail/abc_v01/`

NAS: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/08_Thumbnail/abc_v01/`

Each NAS copy was SHA-256 verified. Source `epic_master_frame0.png` is kept there too, so the builder can run after temporary files disappear. No media is committed. Run the builder with `~/.venvs/orbit-code-graphics/bin/python build_abc_v01.py --source <durable source frame>`.

## Next

Chief reviews the three hooks and contact sheet and merges the PR if accepted. The existing package still needs its other outstanding items (including trailer and captions) and final approval. This job neither changes those nor approves the existing title. No upload or Test & Compare has been started.

Disk: 13 GiB free. Existing MOVED_TO_NAS notes confirm older 027 scratch was archived earlier today; current/previous cuts retained. No additional superseded render batch identified, and no files deleted.
