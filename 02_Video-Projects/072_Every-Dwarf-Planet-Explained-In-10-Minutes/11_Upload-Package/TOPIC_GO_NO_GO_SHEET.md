# Topic Go/No-Go Sheet & Opportunity Score — `OWB:072`

- **Film:** `OWB:072` (`02_Video-Projects/072_Every-Dwarf-Planet-Explained-In-10-Minutes`)
- **Source Brief Job:** `J2929` (`macbook-2`, `2026-11-16`)
- **Status:** **GO (`95 / 100` Opportunity Score, `J2931` Rule-E review by `gemini`, `2026-11-16`; `jobs/reviews/J2931/REVIEW.md`; pre-cleared in `jobs/WIP.json` `next`, waiting on `studio/plan.json` `064` format-test readout & Rule G slot)**
- **Primary Complete-Tour Title (`Rule 26` + `studio/plan.json`, `64 chars`):** `Every Dwarf Planet Explained in 10 Minutes (All 5 Dwarf Planets)`
- **Compact Number-in-Title Variant (`Rule 15`, `42 chars`):** `Every Dwarf Planet Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-16_public_search.json`](./evidence_2026-11-16_public_search.json), [`evidence_2026-11-16_neighbours.json`](./evidence_2026-11-16_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2929` / `J2931`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `16` public OWB longs + `86` Shorts (`2026-11-15.json` & `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1–§1.2 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | Covers the complete 5-dwarf-planet tour (`Ceres`, `Pluto`, `Haumea`, `Makemake`, `Eris`) + `Quaoar`/`Sedna` and the `2006` IAU planetary definition; `034` is a single-question deep dive on Pluto's heart and `048` is on Ceres's Occator salt domes, while neither covers `Eris`, `Haumea`, `Makemake`, or `2024` `JWST` hydrothermal methane |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `11` on-topic `≥1M` videos in the main table (`1.04M–96.03M`), including `4` strictly on-topic tier-1/tier-2 `≥1M` videos in `neighbours.json` alone (`Kurzgesagt` `4.33M`, `TED-Ed` `3.44M`, `CrashCourse` `2.04M`, `SciShow Kids` `1.59M`, with off-topic rows marked `onTopic: false`) |
| **4. Rule 26 Search + `studio/plan.json` Alignment** | Autocomplete phrase + ranking check + `studio/plan.json` tour format | **PASS** | `#1` exact autocomplete `every dwarf planet explained` (`128.7k` Dr_Curio, `36.7k` The Escalist, `36.1k` Supernova small-channel breakouts); built natively in `studio/plan.json` Step 3's number-in-title complete-tour format |
| **5. Two `22–27 s` Short Angles (`E1` + Rule 6 Payoff Withholding)** | `24 s` (`64w` & `62w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `≥70%` payoff withholding, `0` collisions | **PASS** | `S01` *Why Is Dwarf Planet Haumea Shaped Like a Rugby Ball?* (`52 chars`, `LESS THAN FOUR HOURS` mid-overlay matching VO, answer starts at word `45/64 = 70.3% ≥ 70%`) & `S02` *Why Did Discovering Eris Cost Pluto Its Planet Status?* (`54 chars`, `IN JANUARY 2005` mid-overlay matching VO, answer starts at word `45/62 = 72.6% ≥ 70%`) |
