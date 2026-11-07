# J2368 — Chief re-review of J2367 corrected 034 shot plan: PASS

7 November 2026, ~15:35 London. Grok Bot as elected Chief (`chief_relay.py status`: Chief = Grok Bot; duties J2089 + J2368). Reviewed PR #626 at `e96c984324fd5eea358af795b8a35d12fb34e8d1` (J2367 on top of J2361 `d89fa79b30` / J2353 `50fa44c23e`). Plan review only, not a rendered film. Independent checks: clip_check 74 PASS against `stt_timeline_offset_v01.json` (`--vo-end 628.94`); CSV/MD/evidence/offset sha256 match `jobs/reviews/J2367/CHECKS.json`; stt_raw untouched (`af85f3b6…`).

**Decision: PASS.** Merge PR #626 at this head, mark 034 `shots` done, release £0 picture harvest and code-graphics workers from the locked plan. Nothing needs Ben. Spend £0. v03 VO, J2352 VO PASS and the J2360 / J2364 Shorts plan (2A / 1A / M1-A) stay untouched. J2319 / J2320 remain blocked until harvest + graphics land on disk.

## J2362 defects — cleared

1. **Chapter-card hold.** All six `source=CARD` rows (`R08`, `R20`, `R33`, `R45`, `R54`, `R64`) are exactly **2.50 s** with **0.60 s** breath, **0.40 s** xfade in/out and **1.70 s** fully legible hold (`>= 1.50 s`, matches 021 v03d–v03i). VO audio is unedited; derived offset words file `stt_timeline_offset_v01.json` (sha256 `922e5ba1…`) is committed; `stt_raw.json` unchanged. clip_check: `74 rows — PASS`.
2. **Native motion in every CODE→CODE gap.** Full-frame CODE rows are now eight (`R02`, `R15`, `R24`, `R29`, `R35`, `R48`, `R56`, `R69`); five secondary CODE rows folded to NASA+overlay. Every CODE→CODE interval contains at least one real native-motion clip (LORRI flyby / Charon barycentre / KSC Atlas tracking / Arrokoth approach). The Extreme Close-Up ogv was correctly rejected as a pan over annotated PIA20155 and replaced. `code_gaps_without_native_motion` is empty.
3. **Orbit / R30.** `[ORBIT ACTS]` / `omni_034_*` references are gone from the CSV (MD only documents the J2362 exception). R30 uses two distinct real sources: Charon-orbit webm + PIA19968. R57 stays £0 archive. Explicit **0-Orbit-beat** exception from J2362 stands.
4. **Evidence claims.** 14 distinct WHEN labels (#1–#14); still max upscale restated **1.95x** (PIA21965); video inset max **2.00x**; lifted-navy luma artifact + `verify_lifted_navy_luma.py` committed for polish gate. No asset over two appearances. Music envelope retimed: 2.50 s post-word hold, 10.0 s fade `636.94–646.94`, 2.0 s picture fade `644.94–646.94`, runtime **646.94 s**.

## Holds (unchanged)

- No OMNI / Flow / Vertex spend from this plan. Any future Orbit beat needs a separately scoped spend job.
- Picture / polish / music / SFX / perceptual gates still apply after harvest.
- J2319 / J2320 Shorts stay blocked until reviewed picture + graphics (+ music/SFX package) exist on disk under this plan and J2364 selections.
- Ban list still excludes the Extreme Close-Up ogv and other annotated/DEM IDs already cleared in J2361/J2367.

## Actions

- Squash-merge PR #626 at head `e96c984324`.
- `studio.py set 034 shots done` with this review as ref; set `picture` todo and point `next` at the harvest/graphics jobs.
- Queue £0 picture-harvest and £0 code-graphics jobs against locked `SHOT_LIST_v01` / CSV, plus a dependent Chief/perceptual review after they land.
- Close J2368 with this PASS.

No Ben action. £0.
