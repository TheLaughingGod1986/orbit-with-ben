# Topic Go/No-Go Sheet & Opportunity Score — `OWB:076`

- **Film:** `OWB:076` (`02_Video-Projects/076_Every-Space-Shuttle-Explained-In-10-Minutes`)
- **Source Brief Job:** `J2948` (`gemini` on the Mac mini, `2026-11-16`) · **Rule-E Review Job:** Queued (`--after J2948`)
- **Status:** **IN REVIEW — APPENDED TO `jobs/WIP.json` `next` (`95 / 100` Est. Opportunity Score; waiting on Rule-E review, `studio/plan.json` `064` format-test readout & Rule G slot)**
- **Primary Complete-Tour Title (`Rule 26` + `studio/plan.json`, `65 chars`):** `Every Space Shuttle Explained in 10 Minutes (All 6 NASA Orbiters)`
- **Exact `#1` Autocomplete Variant (`Rule 26`, `65 chars`):** `Every Space Shuttle Mission Explained in 10 Minutes (135 Flights)`
- **Compact Number-in-Title Variant (`Rule 15`, `43 chars`):** `Every Space Shuttle Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-16_public_search.json`](./evidence_2026-11-16_public_search.json), [`evidence_2026-11-16_neighbours.json`](./evidence_2026-11-16_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2948`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `17` public OWB longs + `86` Shorts (`2026-11-16.json` & refreshed `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1–§1.2 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | `0` existing films or idea briefs cover NASA's Space Shuttle fleet (`Enterprise`, `Columbia`, `Challenger`, `Discovery`, `Atlantis`, `Endeavour`, `135 missions` from `1981–2011`); distinct from open PR `#853` (`065` ISS deorbit in 2031) and `074` (`Apollo Moon Landings`) |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `17` on-topic `≥1M` videos in the main table (`1.24M–21.88M`), including `11` strictly on-topic `≥1M` education videos in `neighbours.json` alone (Tier-1 `TED` Chris Hadfield `10.19M`, Tier-1 `TED-Ed` `1.79M` + `706k`, `Real Engineering` `4.83M` / `2.11M`, `SmarterEveryDay` `13.40M` / `7.16M` / `5.37M` / `5.02M` / `4.09M` / `1.95M` / `1.30M`, with off-topic rows marked `onTopic: false`) |
| **4. Rule 26 Search + `studio/plan.json` Alignment** | Autocomplete phrase + ranking check + `studio/plan.json` tour format | **PASS** | `#1` exact autocomplete matches across all 4 queries (`every space shuttle explained`, `every space shuttle mission explained`, `space shuttle explained`, `how the space shuttle works`; `328.1k` The Interpreter, `219.7k` Dr_Curio, `190.4k` CaljuCotcas, `146.9k` Classic Aerospace History, `88.2k` Supernova breakouts); built natively in `studio/plan.json` Step 3's number-in-title complete-tour format |
| **5. Two `22–27 s` Short Angles (`E1` + Rule 6 Payoff Withholding)** | `24 s` (`58w` & `59w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `≥70%` payoff withholding, `0` collisions | **PASS** | `S01` *Why Didn't the Space Shuttle Melt During Re-Entry From Space?* (`61 chars`, `TWENTY-EIGHT THOUSAND KILOMETRES` mid-overlay matching VO, answer starts at word `43/58 = 74.1% ≥ 70%`) & `S02` *How Did Space Shuttle Astronauts Fix the Hubble Space Telescope?* (`64 chars`, `TWO MICROMETRES TOO FLAT` mid-overlay matching VO, answer starts at word `47/59 = 79.7% ≥ 70%`) |
