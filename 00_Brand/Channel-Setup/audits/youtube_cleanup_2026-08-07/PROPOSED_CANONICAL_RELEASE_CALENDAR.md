# Proposed Canonical Release Calendar (REVISED — proposal only)

Generated: `2026-08-07T15:04:28Z`

**Status:** PROPOSAL ONLY — not applied. No `videos.update`. No privacy changes.

**Verdict:** `CALENDAR NEEDS REVIEW`

## Scheduling principles

- Max 1 Short/day · max 1 long-form/week · existing IDs only · no deletes/re-uploads
- No placeholder dates · no same-day unrelated family collision · cluster by family
- Observation first, then conservative recovery cadence
- Timezone: `Europe/Paris` (CEST, UTC+2 in August) with UTC stored

## Weekday correction

Previous proposal incorrectly treated **14 Aug 2026** as Thursday.

Programmatic check (`zoneinfo Europe/Paris`):

| Date | Weekday |
|------|---------|
| 2026-08-13 | Thursday |
| 2026-08-14 | Friday |
| 2026-08-20 | Thursday |
| 2026-08-21 | Friday |

## Observation (Phase 1)

- Window: **2026-08-07 to 2026-08-09**
- New publishing: **none**
- Note: No new scheduled publishing in observation window. Preferred recovery observation 7–9 Aug. Live YouTube currently still has OLD applied calendar (includes Aug 8–9 BH Shorts) — this REVISED proposal supersedes it but is NOT applied.

## Exact proposed schedule

| Date | Weekday | Local (Paris) | UTC | Family | Type | Title | YouTube ID | Current state | Proposed state | Validation |
|------|---------|---------------|-----|--------|------|-------|------------|---------------|----------------|------------|
| 2026-08-10 | Monday | 12:30 | `2026-08-10T10:30:00Z` | BLACK_HOLE | shorts | Time Appears to Stop at a Black Hole | `tUAdhOnMW2g` | private+publishAt=2026-08-08T10:30:00Z | private+scheduled | **PASS** |
| 2026-08-11 | Tuesday | 12:30 | `2026-08-11T10:30:00Z` | BLACK_HOLE | shorts | Would You Look Back? | `svYOx07OrIM` | private+publishAt=2026-08-09T10:30:00Z | private+scheduled | **PASS** |
| 2026-08-12 | Wednesday | 12:30 | `2026-08-12T10:30:00Z` | BLACK_HOLE | shorts | What You Would See Falling Into a Black Hole | `B2STcIAF1lY` | private+publishAt=2026-08-10T10:30:00Z | private+scheduled | **PASS** |
| 2026-08-13 | Thursday | 19:00 | `2026-08-13T17:00:00Z` | EXOPLANETS | longform | Alien Worlds: The Strangest Planets We've Ever Found | Orbit's Cosmic Journey | `b8-X_FyJnHM` | private+publishAt=2026-08-14T17:00:00Z | private+scheduled | **PASS** |
| 2026-08-13 | Thursday | 21:00 | `2026-08-13T19:00:00Z` | EXOPLANETS | shorts | It Rains Glass Sideways on This Alien World | `ho9VJxp7f3A` | private+publishAt=2026-08-14T19:00:00Z | private+scheduled | **PASS** |
| 2026-08-14 | Friday | 12:30 | `2026-08-14T10:30:00Z` | EXOPLANETS | shorts | We Found Planets Made of Diamond | `aoR-dA_g7eI` | private+publishAt=2026-08-15T10:30:00Z | private+scheduled | **PASS** |
| 2026-08-15 | Saturday | 12:30 | `2026-08-15T10:30:00Z` | EXOPLANETS | shorts | Three Suns in the Sky — Real Alien Worlds | `6QFGAFZk264` | private+publishAt=2026-08-16T10:30:00Z | private+scheduled | **PASS** |
| 2026-08-16 | Sunday | 12:30 | `2026-08-16T10:30:00Z` | EXOPLANETS | shorts | The Hottest Nights in the Universe | `eOOFVrJ2Ojc` | private+publishAt=2026-08-17T10:30:00Z | private+scheduled | **PASS** |
| 2026-08-20 | Thursday | 19:00 | `2026-08-20T17:00:00Z` | JWST | longform | What the James Webb Telescope Discovered That Changes Everything | Orbit's Cosmic Journey | `tfTkMdE7qqw` | private+publishAt=2026-08-21T17:00:00Z | private+scheduled | **PASS** |
| 2026-08-20 | Thursday | 21:00 | `2026-08-20T19:00:00Z` | JWST | shorts | These Galaxies Appeared Too Early | `bLv0RfidjSg` | private+publishAt=2026-08-21T19:00:00Z | private+scheduled | **PASS** |
| 2026-08-21 | Friday | 12:30 | `2026-08-21T10:30:00Z` | JWST | shorts | How Did Black Holes Get So Big So Fast? | `PcP64way3xA` | private+publishAt=2026-08-22T10:30:00Z | private+scheduled | **PASS** |
| 2026-08-22 | Saturday | 12:30 | `2026-08-22T10:30:00Z` | JWST | shorts | Why JWST Pictures Don't Match the Textbook | `pjIevt27Svo` | private+publishAt=2026-08-23T10:30:00Z | private+scheduled | **PASS** |
| 2026-08-23 | Sunday | 12:30 | `2026-08-23T10:30:00Z` | JWST | shorts | What JWST's Infrared Eyes Can See | `AeFm7gWyWik` | private+publishAt=2026-08-24T10:30:00Z | private+scheduled | **PASS** |

### Phase structure

#### Black Hole (Phase 2)

- Mon 10 Aug 12:30 — `tUAdhOnMW2g`
- Tue 11 Aug 12:30 — `svYOx07OrIM`
- Wed 12 Aug 12:30 — `B2STcIAF1lY`
- Fourth BH Short `w1ej9u0rPTA` → **BH_SHORT_HELD_FOR_LATER**

#### Optional (NOT auto-applied)

- Sun 9 Aug 12:30 Paris (`2026-08-09T10:30:00Z`) — `w1ej9u0rPTA` — Do NOT apply automatically. Prefer BH_SHORT_HELD_FOR_LATER unless explicitly approved for Sun 9 Aug observation-edge slot.

#### Exoplanets (Phase 3)

- Thu 13 Aug 19:00 — long `b8-X_FyJnHM`
- Thu 13 Aug 21:00 — short `ho9VJxp7f3A`
- Fri 14 / Sat 15 / Sun 16 Aug 12:30 — `aoR-dA_g7eI` · `6QFGAFZk264` · `eOOFVrJ2Ojc`

#### JWST (Phase 4)

- Thu 20 Aug 19:00 — long `tfTkMdE7qqw`
- Thu 20 Aug 21:00 — short `bLv0RfidjSg`
- Fri 21 / Sat 22 / Sun 23 Aug 12:30 — `PcP64way3xA` · `pjIevt27Svo` · `AeFm7gWyWik`

## Not-ready IDs (Phase 5) — do not schedule

| YouTube ID | Live privacy | publishAt | Private OK? | Unscheduled OK? | Reason |
|------------|--------------|-----------|-------------|-----------------|--------|
| `HvAKGjx4lv0` | unlisted | `None` | **NO** | yes | historical replacement / manual review — Legacy BH reserve (time-stops variant). Live unlisted + publishAt null. Not in canonical registry. Overlaps topic with scheduled tUAdhOnMW2g. Do not schedule/delete/replace. |
| `icedH_gK8JE` | private | `None` | yes | yes | edit not approved — BH reserve Short (eyes). Cleared from Dec-31 hold; kept private unscheduled. Not production-approved for recovery cadence. |
| `Web2otrTcT0` | private | `None` | yes | yes | metadata incomplete — Exoplanets reserve Short (eyeball). Cleared Dec-31 hold; private unscheduled. Not in approved exo Short sequence. |
| `1qts3tIsg9c` | private | `None` | yes | yes | edit not approved — Exoplanets reserve Short (habitability). Cleared Dec-31 hold; private unscheduled. |
| `dPMJQp2gMNc` | private | `None` | yes | yes | duplicate / accidental early publication — Fermi Short accidental early public; privatized 2026-08-07. Registry notes ACCIDENTAL_EARLY_PUBLICATION. Keep private unscheduled. |
| `rFJoOdQAc9c` | private | `None` | yes | yes | duplicate / accidental early publication — Fermi Zoo Short accidental early public; privatized 2026-08-07. Keep private unscheduled. |

## Omitted production-ready / approved assets (Phase 11)

| YouTube ID | Why omitted | Safe? | Remain private? | Future slot |
|------------|-------------|-------|-----------------|-------------|
| `w1ej9u0rPTA` | Fourth approved BH Short — cadence holds to max 3 in Phase 2; optional Sun 9 Aug only with explicit approval | True | True | After JWST window or when BH recovery needs a refill — TBD |
| `gPCpMsB0w2E` | Beyond Thu–Sun JWST recovery window (max 1 long + 4 Shorts). Do not extend schedule to fit all. | True | True | Mon–Wed after 23 Aug or next JWST refill week |
| `YsyPMhNmHMk` | Additional approved JWST Short beyond Phase 4 window. | True | True | After gPCpMsB0w2E or paired with later long |

## Family coherence

| ID | contentId | relatedLongId | Coherence | Notes |
|----|-----------|---------------|-----------|-------|
| `tUAdhOnMW2g` | `v002-bh-nf01` | `3xrxdmaOwJI` | PASS | — |
| `svYOx07OrIM` | `v002-bh-nf-look-back` | `3xrxdmaOwJI` | PASS | — |
| `B2STcIAF1lY` | `v002-bh-nf02` | `3xrxdmaOwJI` | PASS | — |
| `b8-X_FyJnHM` | `v003-exo-long` | `None` | PASS | — |
| `ho9VJxp7f3A` | `v003-exo-short-01` | `None` | PASS | relatedLongFormVideoId missing in registry (family inferred from contentId) |
| `aoR-dA_g7eI` | `v003-exo-short-02` | `None` | PASS | relatedLongFormVideoId missing in registry (family inferred from contentId) |
| `6QFGAFZk264` | `v003-exo-short-03` | `None` | PASS | relatedLongFormVideoId missing in registry (family inferred from contentId) |
| `eOOFVrJ2Ojc` | `v003-exo-short-04` | `None` | PASS | relatedLongFormVideoId missing in registry (family inferred from contentId) |
| `tfTkMdE7qqw` | `v004-jwst-long` | `None` | PASS | — |
| `bLv0RfidjSg` | `v004-jwst-short-01` | `None` | PASS | relatedLongFormVideoId missing in registry (family inferred from contentId) |
| `PcP64way3xA` | `v004-jwst-short-02` | `None` | PASS | relatedLongFormVideoId missing in registry (family inferred from contentId) |
| `pjIevt27Svo` | `v004-jwst-short-03` | `None` | PASS | relatedLongFormVideoId missing in registry (family inferred from contentId) |
| `AeFm7gWyWik` | `v004-jwst-short-04` | `None` | PASS | relatedLongFormVideoId missing in registry (family inferred from contentId) |

## Collision checks

- same-day Short collisions: none
- duplicate IDs: none
- duplicate minutes: none
- same-day unrelated family: none
- family mismatches: none

## Shelf health (read-only)

- shelf verify ok: **True** (`2026-08-07T15:03:05.726Z`)
- public count: 6 (expected 6)
- unexpectedPublic: []
- recovery escalateNow: False
- canonical publics: `Mo93x0fxB1Q`, `1HuV8o3gOss`, `KcKBixwmcV4`, `3xrxdmaOwJI`, `JRfhE6yWom4`, `L2OFjL4neOo`

## Live drift

Live API still has previous APPLIED calendar on 16 IDs. Revised proposal requires future apply to move/clear those publishAt values. No mutation in this phase.

## Verdict reasons

- HvAKGjx4lv0 is unlisted (expected private) with publishAt null — not-ready private confirm fails for 1/6
- Live YouTube still carries superseded applied schedule (expected until approval)
- Exo/JWST registry rows lack relatedLongFormVideoId (family still PASS via contentId/family fields)

## Next action

**AWAITING APPROVAL — NO SCHEDULE APPLIED**

