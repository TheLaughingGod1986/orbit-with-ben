# Topic Go/No-Go Sheet & Opportunity Score — `OWB:079`

- **Film:** `OWB:079` (`02_Video-Projects/079_Why-Is-Space-Cold-If-The-Sun-Is-So-Hot`)
- **Source Brief Job:** `J2967` (`macbook`, `2026-11-17`) · **Rule-E Review Job:** Queued (`kind:review`)
- **Status:** **READY FOR RULE-E REVIEW IN `jobs/WIP.json` `next` (`95 / 100` Opportunity Score; held under `studio/plan.json` single-question pause after `034` Pluto on `2026-12-13` until format tests read out)**
- **Primary Search-Led Title (`Rule 26`, `64 chars`):** `Why Is Space Cold If the Sun Is Hot? (And 121°C in Direct Light)`
- **Exact `#1` Autocomplete Variant B (`Rule 26`, `56 chars`):** `Why Is Space So Cold When the Sun Is So Hot? (-270°C)`
- **Compact Search Question Variant (`Rule 15`, `38 chars`):** `Why Is Space So Cold If the Sun Is Hot?`
- **Complete-Tour Contingency Recast (`studio/plan.json`, `58 chars`):** `Every Extreme Temperature in Space Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-17_public_search.json`](./evidence_2026-11-17_public_search.json), [`evidence_2026-11-17_neighbours.json`](./evidence_2026-11-17_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2967`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `17` public OWB longs + `86` Shorts (`2026-11-16.json` & refreshed `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1 (full table in `078/TOPIC.md` §1.1–§1.2) |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | `0` existing films or idea briefs cover why outer space is cold (`2.725 K` / `-270.4 °C`) when the Sun burns at `5,500 °C`, the `+121 °C` / `-157 °C` astronaut spacesuit temperature split, `JWST`'s `318 °C` sunshield temperature drop, or the `1 K` Boomerang Nebula; distinct from `022` (solar fusion brightening over billions of years) and `053` (Parker Solar Probe corona entry) |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `13` strictly on-topic `≥1M` education videos in `neighbours.json` (`1.07M–2.82M`: `CrashCourse` `2.82M`/`2.38M`/`2.27M`/`2.17M`/`2.08M`/`2.05M`/`2.03M`/`1.77M`/`1.49M`/`1.32M`, `Khan Academy` `1.57M`/`1.07M`, `PBS Space Time` `1.42M`, plus Tier-1 `TED` Aaswath Raman `512,211` & Tier-1 `TED-Ed` Tejal Gala `261,837`, with off-topic rows marked `onTopic: false`) |
| **4. Rule 26 Search + `studio/plan.json` Alignment** | Autocomplete phrase + ranking check + `studio/plan.json` contingency note | **PASS** | `#1` exact autocomplete matches across all 4 queries (`why is space cold if the sun is hot`, `why is space so cold`, `is space hot or cold`, `coldest place in the universe`; `462,475` SciShow Space, `453,005` Insane Curiosity, `414,380` Sleep On Science, `374,690` BRIGHT SIDE, `356,580` Calm Space, `348,082` vlogbrothers, `199,658` Science ABC); includes `58-char` complete-tour contingency recast (`Every Extreme Temperature in Space Explained in 10 Minutes`) |
| **5. Two `22–27 s` Short Angles (`E1` + Rule 6 Payoff Withholding)** | `24 s` (`57w` & `59w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `≥70%` payoff withholding, `0` collisions | **PASS** | `S01` *Why Is Outer Space Freezing Cold If the Sun Is So Blazing Hot?* (`62 chars`, `8-word` Sentence 1, `FIVE THOUSAND DEGREES CELSIUS` mid-overlay matching VO, answer starts at word `42/57 = 73.7% ≥ 70%` [`42/57 = 73.7%` hyphen-split]) & `S02` *Why Does an Astronaut's Suit Hit 121°C and -157°C at Once?* (`58 chars`, `8-word` Sentence 1, `NO AIR IN SPACE` mid-overlay matching VO, answer starts at word `51/59 = 86.4% ≥ 70%` [`53/61 = 86.9%` hyphen-split]) |
