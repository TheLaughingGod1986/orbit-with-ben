# Production status — 013 Why the Moon Is Slowly Leaving Us

| Field | Value |
|-------|-------|
| Slug | `013_Why-The-Moon-Is-Slowly-Leaving-Us` |
| Channel | Orbit with Ben |
| Gate | **PASS** |
| Script review | **90.4 PASS** |
| Part 01 | **LOCKED v04** (Ben 2026-09-04 — “best yet / 99%”) |
| Part 01 UAT | `OWB UAT/moon_leaving_part-01_LOCKED_v04.mp4` |
| Part 02 | **LOCKED v01** (Ben 2026-09-04 — “looks good”) |
| Part 02 UAT | `OWB UAT/moon_leaving_part-02_LOCKED_v01.mp4` |
| Part 03 | **IN PROGRESS** — VO + music ready · **blocked on Flow credits** |
| Part 03 VO | `02_Voiceover/parts/moon_leaving_part-03_vo_v01.{txt,wav,mp3}` (~136.7s) |
| Part 03 music | `05_Music/moon-leaving-part03_score_bed_v01.mp3` |
| Part 03 plates | `04_Generated-Clips/part03/flow_world_v01/` — **3 / ~18** unique MP4s |
| Part 03 blocker | `04_Generated-Clips/part03/FLOW_CREDITS_BLOCKER.json` |

## Part 01 lock

- Do not regenerate Part 01 unless Ben reopens.
- Bundle: `07_Edit-Project/parts/_locked_p01_v04/`

## Part 02 lock

- Chapter: **When It Was Closer**.
- Bundle: `07_Edit-Project/parts/_locked_p02_v01/`
- World-only · ducked underscore · unique Flow plates (no Part 01 reuse).
- Do not regenerate Part 02 unless Ben reopens.

## Part 03 — Why It Drifts

- VO + score bed ready for assemble.
- Prompts: `07_Edit-Project/parts/part-03_flow_prompts_v01.json` (16).
- Gen helper: `07_Edit-Project/_gen_part03_flow_world_v01.py`.
- **BLOCKER:** Google Flow shows insufficient credits — Start disabled. Need Ben to top up / wait for monthly reset (or approve an alternate world CG path). Do **not** buy credits without asking.
- Need ~18 unique world plates (~8s) for VO length — no freeze-pad, no Part 01/02 cutscene reuse, no Orbit (dosage used in Part 01).
- After plates: assemble `moon_leaving_part-03_rough_v01.mp4` → OWB UAT.

## Do not

- Ship knockoff Orbit
- Put OWB files in HOS UAT
- Reuse Part 01/02 plate files inside Part 03
- Freeze-pad / loop scenery to stretch short coverage
