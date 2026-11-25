# `J3409` — Rule-E Topic Go/No-Go Review: `HOS:132` (`Why Is Glass Transparent? (The Quantum Gap)`)

| Field | Value |
|---|---|
| **Job ID & Reviewer** | `J3409` · `gemini` (`review` lane under `AGENTS.md` Rule E; Grok Bot is Chief for HOS; merges stay with Chief) |
| **Target Proposal (`J3408`)** | **`HOS:132`** (`02_Video-Projects/132_Zachariasen-Zanotto-Pilkington-Why-Is-Glass-Transparent`) |
| **Source PRs (`J3408`)** | HOS PR [`#733`](https://github.com/TheLaughingGod1986/history-of-science/pull/733) (`gemini/J3408-hos-132-133`, contains both `132` and `133`) · OWB PR [`#1208`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1208) (`gemini/J3408-wip-hos-132-133`, appends `HOS:132` & `HOS:133` to `jobs/WIP.json` `next_hos`) |
| **Rule-E Verdict — `HOS:132`** | **GO (`95.1 / 100` · `9.51 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`Why Is Glass Transparent? (The Quantum Gap)`, `43 chars ≤ 50` Rule 15 & Rule 26; `0` exact title collisions; `10 / 10` Rule-E gates PASS) |
| **Rule G & Production Status** | Active `WIP.json["active"]` holds `4 / 4` HOS slots (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). `HOS:132` remains in `next_hos` with all `status.json` stages `todo`. All historical/scientific claims remain **UNVERIFIED** pending an active WIP slot, `SOURCES.md` verbatim quotes, and the `facts` lane (`gemini-agy`). `£0.00` spent. |

---

## 1. Review Fixes Applied on Isolated HOS Branch `gemini/J3409`

Because HOS PR `#733` bundles both `HOS:132` and `HOS:133`, `J3409` opens an isolated HOS PR (`gemini/J3409` → `main`) touching only `02_Video-Projects/132_Zachariasen-Zanotto-Pilkington-Why-Is-Glass-Transparent/` so it merges cleanly alongside `J3410` (`HOS:133`), with the following review fixes applied:

1. **Removed unsaved evidence citation (`TOPIC.md` §3 Rule 26a):** Removed `Fermilab` `NLmpNM0sgYk` (`861,283` views), which did not appear in either saved `2026-11-23` JSON file, and cited the saved `Veritasium` `c6wuh0NRG1s` (*Is Glass a Liquid?*, `5,789,606` views) alongside `TED-Ed` `VwRLIt6jgdM` (`5,032,342`), `Be Smart` `FnDP1sjKGfU` (`1,854,079`), `Veritasium` `2oDXbFcHliM` (`9,814,172` / `9,814,162`), and `Sixty Symbols` `Omr0JNyDBI0` (`1,526,530`).
2. **Excluded `<1M` off-topic/tangential neighbour rows (`TOPIC.md` §3 & `PRE_BUILD_VIDIQ_AUDIT.md`):** Removed `TED-Ed` `d5_h1VuwD6g` (*Rapid prototyping Google Glass*, `466,294` views) from cited neighbours and transparently excluded all three `<1M` off-topic/tangential rows (`d5_h1VuwD6g`, `Khan Academy` `sv8-y7N0Ryw` water-glass refraction `12,411`, and `TEDx Talks` `dlrNp_Vgw7o` glass art `1,471`), while noting `TED-Ed` `oULkYytYPgs` (`2.03M`) is adjacent amorphous metallic-glass physics (`3` directly on glass/transparency + `1` adjacent `>=1M` = `4` total in `neighbours.json`, `0` off-topic at `>=1M`).
3. **Thumbnail §2.5 / §2.6 / §2.B.1 fixes (`TOPIC.md` §3):**
   - **Thumb A:** Replaced `9 EV BARRIER` (mobile jargon + risks conflating pure fused silica `~9 eV` with soda-lime window glass) and removed AI-painted band-gap ladder text per §2.6 → **`LIGHT PASSES THROUGH`** (`3 words`, gold on `PASSES`, zero overlap with Titles A/A1/B/C).
   - **Thumb B:** Replaced `NOT A LIQUID` (repeated `A`/`LIQUID` from Title B) and removed painted `>10^32 YRS` text on the hourglass per §2.6 → **`WINDOWS NEVER FLOW`** (`3 words`, gold on `NEVER`, concrete subject per §2.B.1, zero overlap with Titles A/A1/B/C).
   - **Thumb C:** Confirmed **`MOLTEN TIN`** (`2 words`, gold on `MOLTEN`, zero overlap with Titles A/A1/B/C).
4. **Critical physics & historical accuracy guardrails (`TOPIC.md` §4–§5, `10_Shorts/README.md`, `TOPIC_GO_NO_GO_SHEET.md`):**
   - Separated **pure fused silica ($\text{SiO}_2$, `~9 eV` deep-UV gap, transmits UVB)** from **ordinary soda-lime window glass (`~3.9–4.1 eV` / `~300–320 nm` UVB cutoff, transmits most UVA)**; updated Short `S02` overlay from `9 EV QUANTUM GAP` to **`BLOCKS SUNBURN UVB`**.
   - Distinguished **Zachariasen (1932)** (theoretical random-network paper) from **B. E. Warren (1933–1937)** (experimental X-ray diffraction confirmation).
   - Clarified amorphous glass's band gap stems from **short-range $\text{Si–O}$ bonding**, not long-range crystalline Bloch periodicity.
   - Logged **Zanotto (1998)** (`~10^32 yr`) vs **Zanotto & Gupta (1999)** (`~10^23 yr`) and medieval **cylinder (muff)** + **crown** glass manufacturing.
   - Flagged **Alastair Pilkington**'s 1970 knighthood so 1952/1959 `WHO` cards never use *"Sir"*.
5. **Completed `PRE_BUILD_VIDIQ_AUDIT.md`** (blank template on PR `#733`) and added `TOPIC_GO_NO_GO_SHEET.md` and `TOPIC_OPPORTUNITY_SCORE.md`.

---

## 2. Independent Verification Summary (`10 / 10` Rule-E Gates PASS)

- **Analytics (`2026-11-23`):** Verified `05_Analytics/hos/snapshots/2026-11-23.json` (`takenAt: 2026-11-23T06:40:34.195Z`) and `studio_ctr.json` (`readAt: 2026-11-23T07:11:17.265966+00:00`) match `TOPIC.md` §1 (`002` `162v / 1,163 impr`, `004` `35v / 840 impr`, `006` `15v / 48.15% avg`, `007` `7v`, `005` `7v / 17 impr / 6.73%`, `001` `7v`, `003` `5v`).
- **Neighbours (`evidence_2026-11-23_neighbours_132.json`):** `gate = PASS`, `bigCount = 4`, `hasTed = true`, `failedQueries = []` (`Veritasium` `9,814,162`, `TED-Ed` ★ `5,032,327`, `TED-Ed` ★ `2,031,710`, `Be Smart` `1,854,087`; `0` off-topic `≥1M` rows; `3` `<1M` off-topic/tangential rows transparently excluded).
- **Public Search & Autocomplete (`evidence_2026-11-23_public_search_132.json`):** `10` queries / `75` rows, `4/4` core phrases `autocomplete = yes`, `0` exact title collisions across all 4 long titles (`43`, `49`, `52`, `56` chars) and 2 Short titles (`49`, `44` chars).
- **Non-Duplication:** Zero overlap across HOS `02_Video-Projects/` (`000–018`, `099–119`), open HOS PRs (`120–131`, `133`), `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json`.
- **HOS CI & Board Checks:** `python3 00_Brand/Channel-Setup/tools/status_board.py --check` and `00_Brand/Channel-Setup/tools/check_all.sh` verified `PASS` on isolated branch `gemini/J3409`.

---

## 3. Opportunity Score Breakdown (`9.51 / 10` = `95.1 / 100`)

| Factor | Weight | Score (`/10`) | Weighted |
|---|---:|---:|---:|
| 1. Proven search intent | 25% | `9.6` | `2.400` |
| 2. Competition gap | 20% | `9.4` | `1.880` |
| 3. Narrative & visual arc | 20% | `9.6` | `1.920` |
| 4. Brand & guardrail fit | 20% | `9.4` | `1.880` |
| 5. Series / cluster potential | 15% | `9.5` | `1.425` |
| **Total** | **100%** | — | **`9.505 / 10` (`95.1 / 100`)** |

---

## 4. Next Steps

1. `J3410` independently reviews the paired second half of `J3408` (`HOS:133`).
2. Chief merges the isolated HOS review PR (`gemini/J3409`, touching only `HOS:132`), this OWB review PR (`gemini/J3409`), and OWB PR `#1208` (`jobs/WIP.json` `next_hos` append) once `J3410` completes (superseding raw HOS PR `#733`).
3. Keep `HOS:132` in `jobs/WIP.json` `next_hos` under Rule G until an active HOS WIP slot opens, at which point queue `SOURCES.md` verbatim quotes + `facts` lane (`gemini-agy`) before script lock.
