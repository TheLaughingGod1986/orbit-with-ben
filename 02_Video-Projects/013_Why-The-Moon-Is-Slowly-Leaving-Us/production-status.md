# Production status — 013 Why the Moon Is Slowly Leaving Us

| Field | Value |
|-------|-------|
| Slug | `013_Why-The-Moon-Is-Slowly-Leaving-Us` |
| Channel | Orbit with Ben |
| Gate | **PASS** |
| Script review | **90.4 PASS** |
| Part 01 | **LOCKED v04** (Ben 2026-09-04) |
| Part 01 UAT | `OWB UAT/moon_leaving_part-01_LOCKED_v04.mp4` |
| Part 02 | **LOCKED v01** (Ben 2026-09-04 — “looks good / already tried”) |
| Part 02 UAT | `OWB UAT/moon_leaving_part-02_LOCKED_v01.mp4` |
| Part 03 | **BLOCKED** — VO + music ready · **no rough in iCloud yet** |
| Part 03 VO | `02_Voiceover/parts/moon_leaving_part-03_vo_v01` (~136.7s) |
| Part 03 music | `05_Music/moon-leaving-part03_score_bed_v01.mp3` |
| Part 03 plates | `04_Generated-Clips/part03/flow_world_v01/` — **3 / ~18** |
| Part 03 UAT | `OWB UAT/moon_leaving_part-03_STATUS.txt` (explains missing mp4) |

## Why Part 03 is not in iCloud

Picture gen is blocked on **both** paths:

1. **Google Flow** — Start replaced by “Insufficient credits warning” (low/empty Flow credits). Gallery already harvested; no unused world plates left beyond the 3 on disk.
2. **Gemini API Veo** — `429 RESOURCE_EXHAUSTED` — prepaid credits depleted on the Ultra billing account (Orbitwithben + History of Science keys).

Cannot assemble a shippable Part 03 rough without ~18 unique world plates (no freeze-pad, no Part 01/02 reuse).

**Unblock:** Ben tops up Flow AI credits **or** Gemini API prepaid in AI Studio, then say “credits topped up”.

## Part 02 lock

- Bundle: `07_Edit-Project/parts/_locked_p02_v01/`
- Do not regenerate unless Ben reopens.

## Do not

- Ship knockoff Orbit
- Put OWB files in HOS UAT
- Reuse Part 01/02 plates inside Part 03
- Freeze-pad scenery to fake coverage
