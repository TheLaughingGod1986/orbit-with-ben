# Topic Go/No-Go Sheet & Opportunity Score — `OWB:070`

- **Film:** `OWB:070` (`02_Video-Projects/070_Every-Mars-Rover-Explained-In-10-Minutes`)
- **Source Brief Job:** `J2912` (`gemini`, `2026-11-16`)
- **Status:** Queued for Rule-E Topic Go/No-Go Review (`96 / 100` Pre-Build Opportunity Score; appended to `jobs/WIP.json` `next` under Rule G and `studio/plan.json` Step 3)
- **Primary Complete-Tour Title (`Rule 26` + `studio/plan.json`, `55 chars`):** `Every Mars Rover Explained in 10 Minutes (All 6 Rovers)`
- **Compact Number-in-Title Variant (`Rule 15`, `40 chars`):** `Every Mars Rover Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-16_public_search.json`](./evidence_2026-11-16_public_search.json), [`evidence_2026-11-16_neighbours.json`](./evidence_2026-11-16_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Pre-Check (`J2912`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `16` public OWB longs + `86` Shorts (`2026-11-15.json` & `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1–§1.2 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | Pre-cleared candidate `(a)` in `jobs/reviews/J2912/RULING.md`; covers the chronological 6-rover tour (`Sojourner 1997`, `Spirit/Opportunity 2004`, `Curiosity 2012`, `Zhurong 2021`, `Perseverance 2021`) whereas `025` is a single-question survival essay that never mentions `Sojourner`, `Zhurong`, or `Perseverance` in its spoken script |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `11` on-topic `≥1M` videos (`1.09M–26.14M`: Mark Rober `26.14M`, ElderFox `13.75M` & `2.97M` & `1.09M`, Jared Owen `6.27M`, NASA JPL `5.85M`, TED `5.64M`, Real Engineering `5.45M`, TED-Ed `2.15M`, Astrum Extra `1.64M`, NASA `1.25M`) verified in saved JSONs |
| **4. Rule 26 Search + `studio/plan.json` Alignment** | Autocomplete phrase + ranking check + `studio/plan.json` tour format | **PASS** | `#1` autocomplete `every mars rover explained`; built natively in `studio/plan.json` Step 3's number-in-title complete-tour format (`Every X Explained in 10 Minutes`) |
| **5. Two `22–27 s` Short Angles (`E1`)** | `24 s` (`63w` & `57w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `0` collisions | **PASS** | `S01` *How Did Perseverance Make Breathable Oxygen on Mars?* (`52 chars`, `MOXIE` `122 g` `O₂` at `800 °C`) & `S02` *How Small Was the First Mars Rover Compared to Today's?* (`55 chars`, `11.5 kg` Sojourner vs `1,025 kg` Perseverance) |
