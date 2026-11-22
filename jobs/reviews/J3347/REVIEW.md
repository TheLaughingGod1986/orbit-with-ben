# `J3347` — Rule-E Topic Go/No-Go Review: `HOS:129` (`How Was the Microwave Invented? (A Radar Accident)`)

| Field | Value |
|---|---|
| **Job ID & Reviewer** | `J3347` · `gemini` (`review` lane; elected acting Chief for HOS under 11 Nov 2026 chain `Grok -> Claude -> Codex -> Gemini`) |
| **Target Proposal (`J3270`)** | **`HOS:129`** (`02_Video-Projects/129_Spencer-Boot-Randall-How-Was-The-Microwave-Invented`) |
| **Source PRs (`J3270`)** | HOS PR [`#724`](https://github.com/TheLaughingGod1986/history-of-science/pull/724) (`macbook/J3270`, contains both `128` and `129`) · OWB PR [`#1156`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1156) (`macbook/J3270`, appends `HOS:128` & `HOS:129` to `jobs/WIP.json` `next_hos`) |
| **Rule-E Verdict — `HOS:129`** | **GO (`96.4 / 100` · `9.64 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`How Was the Microwave Invented? (A Radar Accident)`, `50 chars <= 50` Rule 15 & Rule 26; `Title B` `How Does a Microwave Work? (The 1945 Radar Twist)`, `49 chars <= 50`; `Title C` `How Was the Microwave Invented? (Percy Spencer's 1945 Magnetron)`, `64 chars <= 70`; `0` exact title collisions across all 3 long titles and both `16–19 s` Short titles) |
| **Production & Claim Guard** | **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND.** Active `WIP.json["active"]` holds `4 / 4` HOS slots (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). All historical and scientific claims in `TOPIC.md` §4–§5 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes awaiting verbatim primary-source quotes in `SOURCES.md` and `facts` lane (`gemini-agy`) verification when an active HOS WIP slot opens. |
| **Merge Note** | Isolated HOS review PR (`gemini/J3347`) touches only `02_Video-Projects/129_Spencer-Boot-Randall-How-Was-The-Microwave-Invented/` so it merges cleanly alongside `gemini/J3346` (HOS PR `#725`, `HOS:128`). Both halves of `J3270` (`HOS:128` via `J3346` and `HOS:129` via `J3347`) are now Rule-E **GO**; left PRs open for Chief merge (matching `HOS:120–128` precedent under Rule E/H). |
| **Spend** | `£0.00` / `0` credits |

---

## 1. Executive Summary & Audit Fixes Applied

`HOS:129` (*How Was the Microwave Invented? (A Radar Accident)*) from `J3270` passes all `10 / 10` `AGENTS.md` Rule-E and `STUDIO_PLAYBOOK.md` §2 gates with a **`96.4 / 100` (`9.64 / 10` Opportunity Score) GO** verdict in `jobs/WIP.json` `next_hos`, with four targeted packaging, physics, and template refinements applied on isolated HOS branch `gemini/J3347`:

1. **Fixed Thumbnail A §2.5 title-word repetition (`RESOLVED`):** Changed Thumb A cover text from `RADAR ACCIDENT` (repeated `Radar Accident` verbatim from Title A and `Radar` from Title B, violating `studio/RULES.md` line 215 & `THUMBNAIL_AND_TITLE_RULES.md` §2.5 *Cover text never repeats the title*) to **`MELTED CANDY BAR`** (`3 words`, gold on `MELTED`, zero word overlap with Titles A/B/C, concretely names the iconic melted bar beside the magnetron).
2. **Fixed Thumbnail C §2.B.1 vague pronoun teaser (`RESOLVED`):** Changed Thumb C cover text from `IT EXPLODED` (vague pronoun `"IT"`, violating `THUMBNAIL_AND_TITLE_RULES.md` §2.B.1 *The hook words name the thing or make a dare*) to **`THE EGG EXPLODED`** (`3 words`, gold on `EXPLODED`, concretely names the exploding-egg hero object, zero word overlap with Titles A/B/C). Thumb B (`2.45 BILLION/SEC`, `2 tokens`, gold on `2.45`) passes cleanly.
3. **Tightened microwave dielectric-heating physics & anti-myth guardrails (`RESOLVED`):**
   - Updated `TOPIC.md` §3 Thumb B and §4 Act III to separate `2.45 GHz` full wave cycles (`2.45 billion cycles/s`) from electric-field polarity reversals (`4.9 billion reversals/s`), framed heating as **dielectric heating / dipolar relaxation** transferring kinetic energy via collisions with neighbouring molecules, and added an explicit anti-myth guardrail against calling `2.45 GHz` "the resonant frequency of water" (it is an ISM band chosen for centimetre-scale penetration depth).
   - Clarified metal-in-microwave physics (smooth cavity walls act as a reflective waveguide; thin sharp points/edges concentrate induced charge past air's dielectric breakdown).
4. **Aligned Shorts template, logged `<1M` off-topic neighbour exclusions & added review sheets (`RESOLVED`):**
   - Added the Ben 19 Nov 2026 `16–19 s` Shorts house-rules precedence header to `10_Shorts/README.md` (over the copied legacy `22–27 s` template).
   - Transparently documented the three `<1M` off-topic rows in `evidence_2026-11-22_neighbours.json` (`Khan Academy` Cosmic Microwave Background `69,506` & `8,230`, `TEDx Talks` metaphor `15,410`; `0` off-topic `≥1M` rows) in `PRE_BUILD_VIDIQ_AUDIT.md`, `production-status.md`, and `TOPIC_GO_NO_GO_SHEET.md`.
   - Added `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md` (`10 / 10` Rule-E gates `PASS` + mandatory script-stage `SOURCES.md` guardrails, including Randall & Boot 21 Feb 1940 Birmingham magnetron & Tizard Mission with zero WW2 combat overlap, Percy Spencer primary-source verification of the candy bar/popcorn/egg sequence & US Patent `2,495,429`, non-resonance `2.45 GHz` physics, 1947 Radarange specs/price & 1967 Amana Radarange RR-1, and year-accurate `WHO` cards) and `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` (`9.64 / 10` = `96.4 / 100`).
   - Confirmed `hos-search-2027-01` (`J3224`) is accurately labelled `pending Ben's OK` (`needsBen` in `studio/plan.json` per `LEARNINGS.md` rule 34 item 7) and that `HOS:129` independently passes every currently in-force HOS topic gate.

---

## 2. Independent Verification of Raw Evidence (`2026-11-22`, `£0.00` Spend)

- **Neighbour Gate (`evidence_2026-11-22_neighbours_129.json`):** `gate = PASS`, `bigCount = 3`, `hasTed = true`, `failedQueries = []`. All `3` raw `≥1M` rows are strictly on-topic education videos (`0` off-topic `≥1M` rows):
  1. `Tom Scott` — `2tdiKTSdE9Y` *I promise this story about microwaves is interesting.* (`8,957,052` views, Tier 2)
  2. `TED-Ed` ★ — `ZExGV6jSuBw` *Why can't you put metal in a microwave? - Aaron Slepkov* (`2,114,636` views, Tier 1)
  3. `SciShow` — `ZqAZz-JhvYA` *Why Can't I Put Metal in the Microwave?* (`1,329,055` views, Tier 2)
  - Additional on-topic `<1M` row: `National Geographic` `l_M5HzWlM40` (`56,191` views). Three `<1M` rows are off-topic (`Khan Academy` `VQf9aLWp3x4` `69,506`, `TEDx Talks` `60AbkEg14RY` `15,410`, `Khan Academy` `2-1Sb1fa1W4` `8,230`) and excluded.
- **Public Search & Autocomplete (`evidence_2026-11-22_public_search_129.json`, `10` queries, `0` empty searches):**
  - `autocomplete = yes` on all `5` core search phrases: `"how was the microwave invented"` (`3` suggestions), `"how does a microwave work"` (`10`), `"who invented the microwave"` (`3`), `"percy spencer microwave"` (`2`), `"why can't you put metal in a microwave"` (`6`).
  - Ranking videos include `Tom Scott` (`8,957,052`), `Sabin Civil Engineering` (`8,011,520`), `ElectroBOOM` (`5,795,769`), `engineerguy` (`5,389,161`), `TED-Ed` (`2,114,632`), `SciShow` (`1,329,055`), `Weird History Food` (`340,942`); `#2–#4` on `"percy spencer microwave"` sit at `224–795` views.
  - **Exact title collisions:** `0` across Title A (`50 chars`), Title B (`49 chars`), Title C (`64 chars`), Short S01 (`56 chars`), and Short S02 (`44 chars`).
- **Non-Duplication Check:** Zero overlap across HOS `02_Video-Projects/` (`000–018`, `099–119`), open HOS PRs (`120–128`, `130–131`), `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json`.
- **HOS CI & Board Checks:** `python3 00_Brand/Channel-Setup/tools/status_board.py --check` and `00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/129_Spencer-Boot-Randall-How-Was-The-Microwave-Invented` verified `PASS` on isolated branch `gemini/J3347`.

---

## 3. Opportunity Score Breakdown (`9.64 / 10` = `96.4 / 100`)

| Factor | Weight | Score (`/10`) | Weighted |
|---|---:|---:|---:|
| 1. Proven search intent | 25% | `9.6` | `2.400` |
| 2. Competition gap | 20% | `9.7` | `1.940` |
| 3. Narrative & visual arc | 20% | `9.8` | `1.960` |
| 4. Brand & guardrail fit | 20% | `9.5` | `1.900` |
| 5. Series / cluster potential | 15% | `9.6` | `1.440` |
| **Total** | **100%** | — | **`9.640 / 10` (`96.4 / 100`)** |

---

## 4. Next Steps

1. Both halves of `J3270` (`HOS:128` via `J3346` / HOS PR `#725` / OWB PR `#1157` and `HOS:129` via `J3347` / HOS `gemini/J3347` / OWB `gemini/J3347`) are now Rule-E **GO** (`97.1 / 100` and `96.4 / 100`) and ready for Chief merge (superseding raw HOS PR `#724` and merging OWB PR `#1156` `jobs/WIP.json` `next_hos` append alongside the two review PRs).
2. Keep `HOS:129` in `jobs/WIP.json` `next_hos` under Rule G until an active HOS slot opens (or Ben approves `hos-search-2027-01` in `studio/plan.json`), at which point queue `SOURCES.md` verbatim quotes + `facts` lane (`gemini-agy`) before script lock.
