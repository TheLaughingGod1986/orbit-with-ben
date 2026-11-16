# Topic Go/No-Go Sheet & Opportunity Score — `OWB:075`

- **Film:** `OWB:075` (`02_Video-Projects/075_What-Was-Oumuamua-The-First-Interstellar-Object`)
- **Source Brief Job:** `J2939` (`gemini` on the Mac mini, `2026-11-16`) · **Rule-E Review Job:** `J2941` (`gemini`, `2026-11-16`, `jobs/reviews/J2941/REVIEW.md`)
- **Status:** **GO — PRE-CLEARED IN `jobs/WIP.json` `next` (`96 / 100` Opportunity Score; all `6` fixes applied; waiting on `studio/plan.json` format-test readout & Rule G slot)**
- **Primary Search-Led Title (`Rule 26`, `61 chars`):** `What Was 'Oumuamua? (The First Interstellar Object Explained)`
- **Compact Search Question Variant (`Rule 15`, `50 chars`):** `What Was 'Oumuamua? The First Interstellar Visitor`
- **`studio/plan.json` Complete-Tour Recast (`65 chars`):** `Every Interstellar Object Ever Discovered Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-16_public_search.json`](./evidence_2026-11-16_public_search.json), [`evidence_2026-11-16_neighbours.json`](./evidence_2026-11-16_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2939` / `J2941`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `17` public OWB longs + `86` Shorts (`2026-11-16.json` & refreshed `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | `0` mentions of `'Oumuamua` (`1I/2017 U1`) or `2I/Borisov` anywhere in the repo; covers humanity's first interstellar visitors (`e = 1.201` & `e = 3.357`) and the `2023` `Bergner & Seligman` (*Nature*) `H₂` radiolysis solution |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `11` on-topic `≥1M` videos in the main table (`1.18M–7.95M`), including `5` strictly on-topic `≥1M` Tier-1/Tier-2 videos in `neighbours.json` alone (Tier-1 `TED` Karen J. Meech `7.95M`, `CrashCourse` `2.04M` / `1.34M` / `1.18M`, `PBS Space Time` `1.55M`, with off-topic rows marked `onTopic: false`) |
| **4. Rule 26 Search + `studio/plan.json` Alignment** | Autocomplete phrase + ranking check + `studio/plan.json` contingency recast | **PASS** | `#1` exact autocomplete matches on `oumuamua explained`, `oumuamua`, & `interstellar object`; small-channel competition (`27` to `155.6k` views) recorded honestly; held in `WIP.json` `next` with `65-char` complete-tour recast `Every Interstellar Object Ever Discovered Explained in 10 Minutes` |
| **5. Two `22–27 s` Short Angles (`E1` + Rule 6 Payoff Withholding)** | `24 s` (`60w` & `63w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `≥70%` payoff withholding, `0` collisions | **PASS** | `S01` *Why Did Interstellar Object 'Oumuamua Speed Up Leaving the Sun?* (`63 chars`, `FORTY THOUSAND KILOMETRES AHEAD` mid-overlay matching VO, answer starts at word `44/60 = 73.3% ≥ 70%`) & `S02` *How Did Astronomers Spot 'Oumuamua Passing Through Our Solar System?* (`68 chars`, `EIGHTY-SEVEN KILOMETRES PER SECOND` mid-overlay matching VO, answer starts at word `46/63 = 73.0% ≥ 70%`) |
