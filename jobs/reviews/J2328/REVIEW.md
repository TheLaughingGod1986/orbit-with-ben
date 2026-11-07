# J2328 Review — Topic Go/No-Go Prep for Next History of Science Holiday Films (`012` Mendel & `014` Anning)

**Date:** 2026-11-07 · **Reviewer:** `macbook-2` (`gemini-argon`) · **Spend:** £0  
**HOS PR:** [TheLaughingGod1986/history-of-science#453](https://github.com/TheLaughingGod1986/history-of-science/pull/453) (`macbook/J2328`, commit `0b0649f`)  
**Decision:** **KEEP / READY FOR ENTRY** (`012` and `014` remain in `jobs/WIP.json` `next_hos` behind `011` and are **not** entered into `active` in this job).

---

## Summary Table

| Film | Proposed Air Slot | Working Title (Main A / T&C B) | Neighbour Gate (`neighbours.py`) | Search (`public_search.py`) | Short-First Waiver Needed? | Existing Script & `SOURCES_v01.md` State | Go/No-Go Sheet in HOS PR #453 |
|---|---|---|---|---|---|---|---|
| **HOS 012** (`012_Mendel-Pea-Plants`, `next_hos` #2) | **Thu 24 Dec 2026** 18:00 UK | **A:** *Genetics: The Monk Who Counted 28,000 Pea Plants*<br>**B:** *How a Monk and 28,000 Pea Plants Solved Genetics* | **PASS** — **8 education videos ≥ 1M views** (need ≥ 3), led by TED-Ed *How Mendel's pea plants helped us understand genetics* (**5.05M views**, exact Mendeleev-style scientist+experiment match) | `"gregor mendel pea plants"` (`yes`), `"how mendel discovered genetics"` (`related`); slots #2–#5 in GB top 5 under 190k views | **NO** — HOS locks *"Never a Short before its long is public"* (`HOS_STRATEGY.md`, `STUDIO_PLAYBOOK.md` §1, `AGENTS.md` Never list). Waive if audited under OWB rubric. | `mendel_script_master_v01.md` (`J0260`) **93.5/100 PASS** (1,311 words, 8/8 gates, `DATA: 5`, `SCALE: 5`, `WHO: 9`, `WHEN: 17`, `FACT: 4`); `J0268`/`J0269` stay cancelled. `SOURCES_v01.md` has 33 rows `TO VERIFY` (queue `--kind facts` on entry). | `00_Brand/Channel-Setup/ideas/012_Mendel-Pea-Plants/TOPIC_GO_NO_GO.md` (+ `PRE_BUILD_VIDIQ_AUDIT.md`) |
| **HOS 014** (`014_Anning-Fossils-Extinction`, `next_hos` #3) | **Thu 31 Dec 2026** 18:00 UK | **A:** *Extinction: The 12-Year-Old Who Dug Up a Sea Dragon*<br>**B:** *How a 12-Year-Old Girl Proved Extinction Is Real* | **PASS** — **3–4 education videos ≥ 1M views** (need ≥ 3): Natural History Museum *How do dinosaur fossils form?* (**5.23M**), SciShow *10 Oldest Fossils* (**1.80M**), TED-Ed *When will the next mass extinction occur?* (**1.78M**), Extra History *Mary Anning* (**1.17M**) | `"mary anning fossils"` (`yes`, all 5 top GB slots < 1M); all 5 top GB slots for Title A < 580k views | **NO** — HOS locks *"Never a Short before its long is public"*. Waive if audited under OWB rubric. | `anning_script_master_v01.md` (`J0364`) **93.8/100 PASS** (1,301 words, 8/8 gates, `DATA: 5`, `SCALE: 5`, `WHO: 9`, `WHEN: 13`, `FACT: 4`). `SOURCES_v01.md` has 28 rows `TO VERIFY` (queue `--kind facts` on entry). | `00_Brand/Channel-Setup/ideas/014_Anning-Fossils-Extinction/TOPIC_GO_NO_GO.md` (+ `PRE_BUILD_VIDIQ_AUDIT.md`) |

---

## Guardrails Verified

- **No production started:** Neither `012` nor `014` was moved into `active` (`jobs/WIP.json` and queue focus untouched; `011` *Anesthesia* remains #1 in `next_hos`).
- **No full script restarted:** `J0268`/`J0269` remain cancelled; existing `v01` draft scripts (`93.5` and `93.8` PASS) are preserved for the `--kind facts` verification pass once each film enters `active`.
- **HOS repo checks:** `00_Brand/Channel-Setup/tools/check_all.sh` → `ALL CHECKS PASS`.
