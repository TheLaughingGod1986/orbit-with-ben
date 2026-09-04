# Production status — 013 Why the Moon Is Slowly Leaving Us

| Field | Value |
|-------|-------|
| Slug | `013_Why-The-Moon-Is-Slowly-Leaving-Us` |
| Channel | Orbit with Ben |
| Gate | **PASS** |
| Script review | **90.4 PASS** |
| Part 01 | **LOCKED v04** (Ben 2026-09-04) — **do not remint** |
| Part 01 UAT | `OWB UAT/moon_leaving_part-01_LOCKED_v04.mp4` |
| Part 02 | **LOCKED v01** (Ben 2026-09-04) — **do not remint** |
| Part 02 UAT | `OWB UAT/moon_leaving_part-02_LOCKED_v01.mp4` |
| Part 03 | **PARKED** — VO + music ready · waiting on Flow / Veo credits |
| Part 03 VO | `02_Voiceover/parts/moon_leaving_part-03_vo_v01.txt` (~136.7s) |
| Part 03 music | `05_Music/moon-leaving-part03_score_bed_v01_plan.json` (+ mp3 on Mac) |
| Part 03 plates | `04_Generated-Clips/part03/flow_world_v01/` — **~7–10 unique / ~18** (~80s at 10) |
| Part 03 UAT | `07_Edit-Project/parts/moon_leaving_part-03_STATUS.txt` (no mp4 yet) |
| Part 03 park note | `07_Edit-Project/parts/PART03_PARK_STATUS.md` |

## Why Part 03 is parked

Picture gen blocked mid-batch on **both** paths:

1. **Google Flow** — Start replaced by insufficient-credits warning after partial gens. Gallery harvested; still short of ~18 unique world plates.
2. **Gemini API Veo** — `429 RESOURCE_EXHAUSTED` — prepaid depleted (Orbitwithben + History of Science keys).

Cannot assemble a shippable Part 03 rough without ~18 unique world plates (**no freeze-pad**, **no Part 01/02 reuse**).

**Park:** leave Part 03 until Flow AI credits or Gemini Veo prepaid exist. Do **not** ping Ben. When credits are live, resume `07_Edit-Project/_gen_part03_flow_world_v01.py`, mint the remaining plates, assemble picture-first Orbit house, drop rough into OWB UAT.

## Locks

- Part 01 bundle: `07_Edit-Project/parts/_locked_p01_v04/` — leave alone  
- Part 02 bundle: `07_Edit-Project/parts/_locked_p02_v01/` — leave alone  

## Do not

- Remint Part 01 LOCKED v04 or Part 02 LOCKED v01  
- Ship knockoff Orbit  
- Put OWB files in HOS UAT  
- Reuse Part 01/02 plates inside Part 03  
- Freeze-pad scenery to fake coverage  
- Ping Ben about the credit top-up  
