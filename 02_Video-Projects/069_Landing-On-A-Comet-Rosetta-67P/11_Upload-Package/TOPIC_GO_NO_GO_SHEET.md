# Topic Go/No-Go Sheet & Opportunity Score — `OWB:069`

- **Film:** `OWB:069` (`02_Video-Projects/069_Landing-On-A-Comet-Rosetta-67P`)
- **Source Brief Job:** `J2828` (`gemini`, `2026-11-15`) · **Rule-E Review Job:** `J2911` (`macbook-2` + `gemini`, `2026-11-15`)
- **Full Audit Record:** [`jobs/reviews/J2911/REVIEW.md`](../../../jobs/reviews/J2911/REVIEW.md)
- **Verdict:** **GO (Pre-cleared in `jobs/WIP.json` `next` — `94 / 100` Opportunity Score; all 7 `J2911` fixes applied; paused behind `studio/plan.json` format tests)**
- **Primary Search-Led Title (`Rule 26` + `Rule 18`, `65 chars`):** `Landing on a Comet: What Real Spacecraft Footage Showed (Rosetta)`
- **Compact Real-Imagery Variant (`Rule 15` + `Rule 18`, `48 chars`):** `What Real Images From Comet 67P Showed (Rosetta)`
- **Evidence Files:** [`evidence_2026-11-15_public_search.json`](./evidence_2026-11-15_public_search.json), [`evidence_2026-11-15_neighbours.json`](./evidence_2026-11-15_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2911`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `16` public OWB longs + `86` Shorts (`2026-11-15.json` & `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | `0` hits for `Rosetta`, `67P`, or `Halley` across all existing project folders and `IDEAS_*.md` files |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `6` on-topic `≥1M` comet/Rosetta videos verified in `evidence_2026-11-15_public_search.json` (`2.76M` Astrum, `2.67M` AumSum, `1.78M` Learn Bright, `1.69M` Peekaboo Kidz, `1.18M` CrashCourse, `1.01M` Astronimate) + Vox (`830K`) (`J2911` FIX 4 applied) |
| **4. Rule 26 Search + `studio/plan.json` Pause Note** | Autocomplete phrase + top 2 ranking videos + contingency note | **PASS** | Autocomplete `landing on a comet`, `rosetta comet 67p`, `why do comets have tails`; tour recast renamed *Every World Our Spacecraft Have Landed On (7 Worlds Explained)* and marked contingency only (`J2911` FIX 5 applied) |
| **5. Two `22–27 s` Short Angles (`E1` + Fixes)** | `24–25 s` (`60w` & `62w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, verified science | **PASS** | `S01` *What Did Rosetta Film 13 Kilometres Above a Comet?* (`50 chars`, `13 km` OSIRIS dust + Canis Major stars accuracy, `J2911` FIX 1 & 2) & `S02` *Why Did Our First Comet Lander Bounce a Kilometre High?* (`55 chars`, `g ≈ 1.8 × 10⁻⁴ m/s²`, `J2911` FIX 3 & 7) |
