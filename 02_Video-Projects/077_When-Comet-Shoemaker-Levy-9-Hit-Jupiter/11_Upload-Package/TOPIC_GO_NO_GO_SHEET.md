# Topic Go/No-Go Sheet & Opportunity Score — `OWB:077`

- **Film:** `OWB:077` (`02_Video-Projects/077_When-Comet-Shoemaker-Levy-9-Hit-Jupiter`)
- **Source Brief Job:** `J2948` (`gemini` on the Mac mini, `2026-11-16`) · **Rule-E Review Job:** Queued (`--after J2948`)
- **Status:** **IN REVIEW — APPENDED TO `jobs/WIP.json` `next` (`96 / 100` Est. Opportunity Score; waiting on Rule-E review, `studio/plan.json` format-test readout & Rule G slot)**
- **Primary Search-Led Title (`Rule 26`, `67 chars`):** `What Happened When Comet Shoemaker-Levy 9 Hit Jupiter? (1994 Crash)`
- **Compact Search Question Variant (`Rule 15`, `50 chars`):** `Why Did Comet Shoemaker-Levy 9 Crash Into Jupiter?`
- **`studio/plan.json` Complete-Tour Recast (`62 chars`):** `Every Giant Impact in the Solar System Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-16_public_search.json`](./evidence_2026-11-16_public_search.json), [`evidence_2026-11-16_neighbours.json`](./evidence_2026-11-16_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2948`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `17` public OWB longs + `86` Shorts (`2026-11-16.json` & refreshed `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | `0` mentions of `Shoemaker-Levy 9` (`D/1993 F2`) anywhere in `02_Video-Projects/` or `ideas/`; distinct from `020` (`Falling Into Jupiter`), `047` (`Great Red Spot Shrinking`), and `069` (`Rosetta 67P`) |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `9` on-topic `≥1M` videos in the main table (`1.18M–3.15M`), including `7` strictly on-topic `≥1M` Tier-2 education videos in `neighbours.json` alone (`CrashCourse` `2.38M` / `2.04M` / `2.02M` / `1.83M` / `1.76M` / `1.34M` / `1.18M`, plus Tier-1 `TED` Phil Plait `152k` & `TED-Ed` `139k`, with off-topic rows marked `onTopic: false`) |
| **4. Rule 26 Search + `studio/plan.json` Alignment** | Autocomplete phrase + ranking check + `studio/plan.json` contingency recast | **PASS** | `#1` exact autocomplete matches on `shoemaker levy 9`, `comet shoemaker levy 9`, & `comet hits jupiter`; small-channel competition (`311` to `118.5k` views) recorded honestly; held in `WIP.json` `next` with `62-char` complete-tour recast `Every Giant Impact in the Solar System Explained in 10 Minutes` |
| **5. Two `22–27 s` Short Angles (`E1` + Rule 6 Payoff Withholding)** | `24 s` (`58w` & `58w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `≥70%` payoff withholding, `0` collisions | **PASS** | `S01` *Why Did Jupiter Tear Comet Shoemaker-Levy 9 Into 21 Giant Pieces?* (`65 chars`, `FORTY THOUSAND KILOMETRES ABOVE` mid-overlay matching VO, answer starts at word `43/58 = 74.1% ≥ 70%`) & `S02` *How Did Comet Shoemaker-Levy 9 Leave Earth-Sized Scars on Jupiter?* (`66 chars`, `SIXTY KILOMETRES PER SECOND` mid-overlay matching VO, answer starts at word `42/58 = 72.4% ≥ 70%`) |
