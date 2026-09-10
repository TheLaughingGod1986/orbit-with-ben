# Production status — 013 Why the Moon Is Slowly Leaving Us

| Field | Value |
|-------|-------|
| Slug | `013_Why-The-Moon-Is-Slowly-Leaving-Us` |
| Channel | Orbit with Ben |
| Part 01 | **LOCKED v04** — do not remint |
| Part 01 UAT | `OWB UAT/moon_leaving_part-01_LOCKED_v04.mp4` |
| Part 02 | **LOCKED v01** — do not remint |
| Part 02 UAT | `OWB UAT/moon_leaving_part-02_LOCKED_v01.mp4` |
| Part 03 | **ROUGH v03 in UAT** — v02 notes fixed (music audible · scenes re-sequenced) · awaiting Ben watch |
| Part 03 rough | `07_Edit-Project/parts/moon_leaving_part-03_rough_v03.mp4` (136.7s · 19 VO-timed beds) · v01/v02 kept for compare |
| Part 03 UAT | **`OWB UAT/moon_leaving_part-03_rough_v03.mp4`** — watch this (v01/v02 left alongside) |
| Part 03 audio | VO −16 LUFS + score bed −22 LUFS, 3.5:1 duck, mix 0.85 (`05_Music/moon-leaving-part03_score_bed_v01.mp3`) — v01/v02 bed at −28/8:1/0.55 was inaudible |
| Part 03 plates | 19 unique world plates · cuts on VO gaps · open = beach at dusk, tide running · no Orbit |

## Part 03 notes

- Chapter: **Why It Drifts**
- World-only (Orbit dosage already used in Part 01)
- Soft lunar underscore, sidechain-ducked under VO
- No freeze-pad / still-push / Ken Burns

## Do not

- Remint Part 01 or Part 02 LOCKED
- Ship knockoff Orbit
- Put OWB files in HOS UAT

## UAT 2026-09-10

Ben FAIL: nonsense tidal “water plane through Earth/Moon” plate. Doc: `07_Edit-Project/parts/PART03_UAT_FAIL_tidal_plane_2026-09-10.md`. Regen bulge plates; reassemble rough v02. Do not remint Part 01/02.

2026-09-10 late: rough **v02** built and delivered to OWB UAT. 9 plates quarantined (4 water-plane culprits + 2 same-look on spot-check + 3 sliced-planet / ringed-Moon), 9 clean replacements minted x1 in Google Flow (project `59f2b559`), each QC'd first/mid/last. Cuts now sit on VO paragraph gaps; no freeze-pad, no loop, no reuse. Detail: `07_Edit-Project/parts/PART03_UAT_FAIL_tidal_plane_2026-09-10.md` (Result section).

2026-09-11 00:15: Ben on v02 — "no music" + "scenes repeat too much". **v03** delivered: music bed raised ~12 dB under VO (measured −30 dB ducked stem vs −42 dB), sequence rebuilt so no look family runs back-to-back (Moon-over-sea 4-in-a-row → 3 spread), new terminator plate `p03_05`, gears under "as long as that gear turns", `p03_14` dropped. Google Flow **and** Gemini API credits both exhausted mid-run — six more variety plates are prompted in `parts/part-03_flow_prompts_v03_variety.json` (`_gen_part03_flow_variety_v03.py` / `_gen_part03_veo_world_v03.py`) for when credits return.
