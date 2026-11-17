# Topic Go/No-Go Sheet & Opportunity Score — `OWB:070`

- **Film:** `OWB:070` (`02_Video-Projects/070_Every-Mars-Rover-Explained-In-10-Minutes`)
- **Source Brief Job:** `J2912` (`gemini`, `2026-11-16`) · **Rule-E Review Job:** `J2920` (`gemini`, `2026-11-16`)
- **Full Audit Record:** [`jobs/reviews/J2920/REVIEW.md`](../../../jobs/reviews/J2920/REVIEW.md)
- **Verdict:** **GO (Pre-cleared in `jobs/WIP.json` `next` — `95 / 100` Opportunity Score; all 6 `J2920` fixes applied; waits on `studio/plan.json` `064` format-test readout & Rule G slot)**
- **Primary Complete-Tour Title (`Rule 26` + `studio/plan.json`, `55 chars`):** `Every Mars Rover Explained in 10 Minutes (All 6 Rovers)`
- **Compact Number-in-Title Variant (`Rule 15`, `40 chars`):** `Every Mars Rover Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-16_public_search.json`](./evidence_2026-11-16_public_search.json), [`evidence_2026-11-16_neighbours.json`](./evidence_2026-11-16_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2920`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `16` public OWB longs + `86` Shorts (`2026-11-15.json` & `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1–§1.2 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | Pre-cleared candidate `(a)` in `jobs/reviews/J2912/RULING.md`; covers the chronological 6-rover tour (`Sojourner 1997`, `Spirit/Opportunity 2004`, `Curiosity 2012`, `Zhurong 2021`, `Perseverance 2021`) whereas `025` is a single-question survival essay that never mentions `Sojourner`, `Zhurong`, or `Perseverance` in its spoken script |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `11` on-topic `≥1M` videos in the main table (`1.09M–26.14M`: Mark Rober `26.14M`, ElderFox `13.75M` & `2.97M` & `1.09M`, Jared Owen `6.27M`, NASA JPL `5.85M`, TED `5.64M`, Real Engineering `5.45M`, TED-Ed `2.15M`, Astrum Extra `1.64M`, NASA `1.25M`, plus `ER6EO4B7V68` `3.59M` and `X2UaFuJsqxk` `3.24M`) verified in saved JSONs (`J2920` FIX 1 & 2 applied) |
| **4. Rule 26 Search + `studio/plan.json` Alignment** | Autocomplete phrase + ranking check + `studio/plan.json` tour format | **PASS** | `#1` autocomplete `every mars rover explained`; built natively in `studio/plan.json` Step 3's number-in-title complete-tour format (`Every X Explained in 10 Minutes`) |
| **5. Two `22–27 s` Short Angles (`E1` + Rule 6 Fixes + `J2732` / `6831935790` Subject/Title Hypothesis)** | `24 s` (`63w` & `60w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `≥70%` payoff withholding, `0` collisions; distinct hardware/titles spaced `≥3 d` apart (`Learning 33`) | **PASS** | `S01` *How Did Perseverance Make Breathable Oxygen on Mars?* (`52 chars`, `800 °C OXYGEN BOX` mid-overlay, `122 g` `O₂` payoff at `≥70%`, `J2920` FIX 4) & `S02` *How Small Was the First Mars Rover Compared to Today's?* (`55 chars`, `11.5 kg` Sojourner vs `1,025 kg` Perseverance, `1 CM/S TOP SPEED` mid-overlay, `J2920` FIX 5). Carries forward the `J2732` / `6831935790` morning-read hypothesis: avoids repeating `025`'s back-to-back `"90-Day Rover / 14 Years"` Opportunity angle (`B1z2dv7m7Vk` `59` next-morning views, `uhZSRcvngvE` `30` next-morning views = `7.08%` of recent 10-Short median `423.5`) while preserving distinct Mars hardware angles (`iyvWYFP_ETA` `1,025` and `RT-ec4_GcOk` `1,118` next-morning views). |
