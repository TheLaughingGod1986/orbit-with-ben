# Production status — 013 Why the Moon Is Slowly Leaving Us

| Field | Value |
|-------|-------|
| Channel | Orbit with Ben |
| Episode | 013 Why the Moon Is Slowly Leaving Us |
| Part 01 | **LOCKED v04** — do not remint |
| Part 02 | **LOCKED v01** — QC remint queue (diagram numerals + ocean bulge) — do not overwrite LOCKED |
| Part 03 | **LOCKED v04** Ben PASS 2026-09-11 — keep LOCKED; **NOT tidal-cleared** |
| Part 03 provisional | **ROUGH v05** FAIL→KEEP swap ready in OWB UAT (do not LOCK) |
| Part 03 remint A/B/C | **BLOCKED** — Google SMS rate limit on `benoats@googlemail.com` |
| Part 04 | **IN PREP** — VO ready · 12 Flow prompts staged · mint after P03 remint |
| Part 04 VO | `02_Voiceover/parts/moon_leaving_part-04_vo_v01.wav` (~116.2s) |
| Part 04 prompts | `07_Edit-Project/parts/part-04_flow_prompts_v01.json` (12 plates) |
| Flow credits | **CLEARED** (~25,050 on benoats@googlemail.com) — login is the blocker, not credits |

## Part 03 lock + QC

- Approved picture: Ben PASS → `moon_leaving_part-03_LOCKED_v04.mp4`
- QC green 2026-09-12: still has HARD tidal-plane FAILs in locked cut (`remint_queue.md`)
- Overnight remint A/B/C (12 Sep): **0 plates landed** — login re-auth failed / session expired / now SMS rate-limited

## Part 03 provisional v05 (2026-09-13)

Watch file: `OWB UAT/moon_leaving_part-03_rough_v05.mp4`

Swaps (unused KEEP-class plates, no freeze-pad, no LOCKED overwrite):

| Slot | Was (FAIL) | Now |
|------|------------|-----|
| 15.2–19.5s | `p03_03` flat water shelf | `harvest_03` (bulge-on-globe) |
| 19.5–27.5s | `gallery_03` flat water + Moon on horizon | `p03_14` |
| 27.5–35.4s | `harvest_00` tidal funnel (mid) | `harvest_02` |

**Not tidal-cleared.** Proper remint plates still required before any re-LOCK.

## Next

1. Ben: when Google SMS cools down, verify Flow as `benoats@googlemail.com` (never `benoats86@gmail.com`).
2. Run `04_Generated-Clips/part03/_remint_2026-09-12/_run_remint_abc_when_ready.py --mint`
3. Quarantine FAIL plates → rebuild rough → new UAT id → Ben re-pass before LOCK
4. Then P02 remint queue, then Part 04 mint (Veo 3.1 Fast)

## Do not

- Remint / overwrite Part 01 / 02 / 03 LOCKED files
- Mint on wrong Google account (`benoats86@gmail.com` @ ~50 credits)
- Ship knockoff Orbit
- Put OWB files in HOS UAT
