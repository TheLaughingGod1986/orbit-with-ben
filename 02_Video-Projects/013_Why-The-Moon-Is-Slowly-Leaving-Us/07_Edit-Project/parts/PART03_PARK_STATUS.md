# Part 03 — Why It Drifts — PARKED (feedback only)

**Date:** 2026-09-04  
**Scope:** Part 03 only. Do **not** remint Part 01 LOCKED v04 or Part 02 LOCKED v01.  
**Ben ping:** none (park silently until credits exist).

## Verdict

Part 03 cannot assemble. World-plate gen died mid-batch on **Flow credits empty** and **Gemini Veo 429**. Freeze-pad is forbidden. Picture-first Orbit house needs the remaining plates first.

## Inventory (repo + prior batch notes)

| Item | State |
|------|--------|
| VO | Ready — `02_Voiceover/parts/moon_leaving_part-03_vo_v01.txt` (~**136.7s**) |
| Score bed | Plan ready — `05_Music/moon-leaving-part03_score_bed_v01_plan.json` (+ mp3 on Mac) |
| Prompt list | **18** world prompts — `07_Edit-Project/parts/part-03_flow_prompts_v01.json` |
| Captured plates | **~7–10 unique** on Mac under `04_Generated-Clips/part03/flow_world_v01/` (~**80s** if 10×8s) |
| Still needed | **~8–11** more unique world plates → **~18** total for VO coverage |
| Rough / UAT mp4 | **Missing** — see `07_Edit-Project/parts/moon_leaving_part-03_STATUS.txt` |
| Part 01 | **LOCKED v04** — leave alone (`07_Edit-Project/parts/_locked_p01_v04/`) |
| Part 02 | **LOCKED v01** — leave alone (`07_Edit-Project/parts/_locked_p02_v01/`) |

Exact on-disk MP4s live on the Mac mini / iCloud checkout; this cloud workspace only has prompts + status (no plate binaries in git).

## Blockers

1. **Google Flow** — Start disabled / “Insufficient credits” after partial gens. Gallery already harvested.
2. **Gemini API Veo** — `429 RESOURCE_EXHAUSTED` (prepaid depleted).
3. **House rules** — no freeze-pad; no Part 01/02 plate reuse inside Part 03; no knockoff Orbit.

## Resume when credits exist (Mac mini)

1. Confirm Flow AI credits **or** Gemini Veo prepaid are live (no Ben ping from agents).
2. Resume only:  
   `07_Edit-Project/_gen_part03_flow_world_v01.py`  
   (skips stems that already have `p03_XX_*.mp4`; targets 18).
3. Capture remaining unique world plates into  
   `04_Generated-Clips/part03/flow_world_v01/`.
4. Assemble Part 03 rough — picture-first Orbit house (Orbit only on house beats; world carries science).
5. Drop rough into `OWB UAT/` and clear this park flag.

## Explicit non-actions

- Do not remint / rebuild Part 01 LOCKED v04  
- Do not remint / rebuild Part 02 LOCKED v01  
- Do not freeze-pad to fake ~137s coverage  
- Do not ping Ben about top-up  
- Do not ship a Part 03 rough with <~18 unique world plates
