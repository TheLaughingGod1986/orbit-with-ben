# Topic Go/No-Go Sheet & Opportunity Score — `OWB:071`

- **Film:** `OWB:071` (`02_Video-Projects/071_Why-Did-NASA-Crash-Cassini-Into-Saturn`)
- **Source Brief Job:** `J2912` (`gemini`, `2026-11-16`) · **Rule-E Review Job:** `J2920` (`gemini`, `2026-11-16`)
- **Full Audit Record:** [`jobs/reviews/J2920/REVIEW.md`](../../../jobs/reviews/J2920/REVIEW.md)
- **Verdict:** **GO (Pre-cleared in `jobs/WIP.json` `next` — `96 / 100` Opportunity Score; all 6 `J2920` fixes applied; paused behind `studio/plan.json` format tests)**
- **Primary Search-Led Title (`Rule 26`, `62 chars`):** `Why Did NASA Crash Cassini Into Saturn? (To Protect Two Moons)`
- **Compact Search Question Variant (`Rule 15`, `39 chars`):** `Why Did NASA Crash Cassini Into Saturn?`
- **`studio/plan.json` Multi-Mission Tour Recast (`64 chars`):** `Every Spacecraft We Crashed Into a World Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-16_public_search.json`](./evidence_2026-11-16_public_search.json), [`evidence_2026-11-16_neighbours.json`](./evidence_2026-11-16_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2920`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `16` public OWB longs + `86` Shorts (`2026-11-15.json` & `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | Pre-cleared candidate `(b)` in `jobs/reviews/J2912/RULING.md`; `0` existing films or idea briefs cover Cassini's `15 Sep 2017` planetary-protection atmospheric plunge, its `22` Grand Finale ring-gap dives, or its `100%` thruster battle inside Saturn's upper atmosphere |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `9` on-topic `≥1M` videos in the main table (`1.05M–9.28M`: Astrum `9.28M`, `2.50M`, `1.17M`, `1.05M`, NASA JPL `5.81M`, `1.92M`, `1.62M`, CrashCourse `1.65M`, NASA `1.22M`, plus WSJ `6.73M` & Secrets of the Universe `3.85M`) verified in saved JSONs (`J2920` FIX 3 applied) |
| **4. Rule 26 Search + `studio/plan.json` Pause Note** | Autocomplete phrase + ranking check + `studio/plan.json` tour recast | **PASS** | Autocomplete on `cassini crash into saturn footage`, `cassini saturn final images`, and `cassini grand finale`; records small-channel competition (`8–518` views, `J2920` FIX 2), includes 6-mission tour recast (`64 chars`, `J2920` FIX 6), and waits in `jobs/WIP.json` `next` behind `studio/plan.json` pause |
| **5. Two `22–27 s` Short Angles (`E1` + Policy/Rule 6 Fixes)** | `24 s` (`64w` & `62w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `≥70%` payoff withholding, policy-clean | **PASS** | `S01` *Why Did NASA Crash a $4 Billion Spacecraft Into Saturn?* (`55 chars`, `2 HIDDEN OCEAN MOONS` mid-overlay, `113,000 km/h` plunge at `≥70%`, `J2920` FIX 5) & `S02` *What Did Cassini Find Inside the Gap Under Saturn's Rings?* (`58 chars`, `22 RING-GAP DIVES` Frame-0 hook, `2,000 KM RING GAP` mid-overlay, `J2920` FIX 1 & 5) |
