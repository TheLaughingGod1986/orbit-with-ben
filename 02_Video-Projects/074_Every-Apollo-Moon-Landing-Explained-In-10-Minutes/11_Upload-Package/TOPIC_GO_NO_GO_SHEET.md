# Topic Go/No-Go Sheet & Opportunity Score — `OWB:074`

- **Film:** `OWB:074` (`02_Video-Projects/074_Every-Apollo-Moon-Landing-Explained-In-10-Minutes`)
- **Source Brief Job:** `J2939` (`gemini` on the Mac mini, `2026-11-16`) · **Rule-E Review Job:** `J2941` (`gemini`, `2026-11-16`, `jobs/reviews/J2941/REVIEW.md`)
- **Status:** **GO — PRE-CLEARED IN `jobs/WIP.json` `next` (`95 / 100` Opportunity Score; all `6` fixes applied; waiting on `studio/plan.json` `064` format-test readout & Rule G slot)**
- **Primary Complete-Tour Title (`Rule 26` + `studio/plan.json`, `66 chars`):** `Every Apollo Moon Landing Explained in 10 Minutes (All 6 Landings)`
- **Exact `#1` Autocomplete Variant (`Rule 26`, `62 chars`):** `Every Apollo Mission Explained in 10 Minutes (Apollo 11 to 17)`
- **Compact Number-in-Title Variant (`Rule 15`, `49 chars`):** `Every Apollo Moon Landing Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-16_public_search.json`](./evidence_2026-11-16_public_search.json), [`evidence_2026-11-16_neighbours.json`](./evidence_2026-11-16_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2939`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `17` public OWB longs + `86` Shorts (`2026-11-16.json` & refreshed `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1–§1.2 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | Covers all `6` crewed Apollo lunar landings (`Apollo 11, 12, 14, 15, 16, 17`) + `Apollo 13` (`1969–1972`); `013` is on `3.82 cm/yr` tidal recession and `066` (PR `#901`) is on tidal locking & robotic far-side missions |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `14` on-topic `≥1M` videos in the main table (`1.92M–31.10M`), including `7` strictly on-topic `≥1M` education videos in `neighbours.json` alone (`Kurzgesagt` `22.63M` / `20.79M` / `17.48M` / `2.49M`, `SmarterEveryDay` `5.37M` / `5.02M`, `CrashCourse` `1.92M`, plus Tier-1 `TED` `883k` & `TED-Ed` `536k`, with off-topic rows marked `onTopic: false`) |
| **4. Rule 26 Search + `studio/plan.json` Alignment** | Autocomplete phrase + ranking check + `studio/plan.json` tour format | **PASS** | `#1` exact autocomplete `every apollo mission explained` (`528.4k` Supernova, `93.4k` Dr_Curio, `74.3k` Dan Severns, `55.9k` The Space Explained breakouts); built natively in `studio/plan.json` Step 3's number-in-title complete-tour format |
| **5. Two `22–27 s` Short Angles (`E1` + Rule 6 Payoff Withholding)** | `24 s` (`63w` & `61w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `≥70%` payoff withholding, `0` collisions | **PASS** | `S01` *How Did Apollo 11 Land on the Moon With 25 Seconds of Fuel Left?* (`64 chars`, `FIVE COMPUTER OVERLOAD ALARMS` mid-overlay matching VO, answer starts at word `45/63 = 71.4% ≥ 70%`) & `S02` *Why Did Apollo 17 Find Orange Soil on the Moon?* (`47 chars`, `DECEMBER 1972 AT SHORTY` mid-overlay matching VO, answer starts at word `45/61 = 73.8% ≥ 70%`) |
