# Topic Go/No-Go Sheet & Opportunity Score — `OWB:080`

- **Film:** `OWB:080` (`02_Video-Projects/080_Every-Rocket-Explained-In-10-Minutes`)
- **Source Brief Job:** `J2974` (`macbook`, `2026-11-17`)
- **Status:** **READY FOR RULE-E REVIEW (`96 / 100` Opportunity Score; appended to `jobs/WIP.json` `next`, waiting on `studio/plan.json` `064` format-test readout & Rule G slot)**
- **Primary Complete-Tour Title (`Rule 26` + `studio/plan.json`, `58 chars`):** `Every Rocket Explained in 10 Minutes (Saturn V to Starship)`
- **Exact `#1` Autocomplete + Span Variant (`Rule 26`, `54 chars`):** `Every Rocket Explained in 10 Minutes (V-2 to Starship)`
- **Compact Number-in-Title Variant (`Rule 15`, `36 chars`):** `Every Rocket Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-17_public_search.json`](./evidence_2026-11-17_public_search.json), [`evidence_2026-11-17_neighbours.json`](./evidence_2026-11-17_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2974`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `17` public OWB longs + `87` Shorts (`2026-11-17.json` & `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1–§1.2 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | `0` existing films or idea briefs cover a complete tour of orbital launch vehicles (`V-2` `1944` & `R-7 Semyorka` `1957` to `Saturn V`, `Soviet N1`, `Soyuz`, `Ariane 5`, `Falcon 9`, `SLS`, and `Starship`); distinct from `074` (`Every Apollo Moon Landing`), `076` (`Every Space Shuttle`), and `078` (`Every Space Station`) |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `14` strictly on-topic `≥1M` videos in the main table (`1.07M–16.43M`), combining all `10` strictly on-topic `≥1M` education videos in `neighbours.json` (`SmarterEveryDay` `13.40M`, `5.37M`, `5.02M`, `Veritasium` `13.20M`, `Real Engineering` `4.84M`, `2.11M`, `The Royal Institution` `4.27M`, `Simple History` `1.95M`, Tier-1 `TED-Ed` `1.79M`, `minutephysics` `1.07M`, with off-topic rows marked `onTopic: false`) with `4` on-topic `≥1M` videos in `public_search.json` (`Jared Owen` `16.43M` & `4.99M`, `Peekaboo Kidz` `1.89M`, `Science ABC` `1.28M`) |
| **4. Rule 26 Search + `studio/plan.json` Alignment** | Autocomplete phrase + ranking check + `studio/plan.json` tour format | **PASS** | `#1` exact autocomplete matches across all 3 core queries (`every rocket explained`, `how rockets work`, `saturn v rocket explained`; `765.3k` The Space Race *Every Single Soviet and Russian Rocket Explained*, `745.7k` Hazegrayart *N1 Rocket Launch Failures*, `54.3k` Supernova, `45.3k` Primolution); built natively in `studio/plan.json` Step 3's number-in-title complete-tour format |
| **5. Two `22–27 s` Short Angles (`E1` + Rule 6 Payoff Withholding)** | `24 s` (`58w` & `57w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `≥70%` payoff withholding, `0` collisions | **PASS** | `S01` *How Did NASA's Saturn V Burn 15 Tonnes of Rocket Fuel a Second?* (`63 chars`, `8-word` Sentence 1, `THREE THOUSAND TONNES UPHILL` mid-overlay matching VO, answer starts at word `42/58 = 72.4% ≥ 70%` [`43/59 = 72.9%` hyphen-split]) & `S02` *Why Did the Giant Soviet N1 Moon Rocket Explode on Every Launch?* (`64 chars`, `8-word` Sentence 1, `THIRTY SMALLER ENGINES` mid-overlay matching VO, answer starts at word `41/57 = 71.9% ≥ 70%` [`41/58 = 70.7%` hyphen-split]) |
