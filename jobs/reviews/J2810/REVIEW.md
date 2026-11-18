# `J2810` — Rule-E Topic Go/No-Go Review: `HOS:104` (`104_Roemer-Fizeau-Foucault-Speed-Of-Light`)

| Field | Value |
|---|---|
| **Job ID & Reviewer** | `J2810` · `macbook` (`gemini-argon` / `gemini-agy`, `review` lane) |
| **Target Film** | `HOS:104` (`02_Video-Projects/104_Roemer-Fizeau-Foucault-Speed-Of-Light` · *How Did We Measure the Speed of Light? (A 720-Tooth Wheel)*) |
| **Source Proposal (`J2809`)** | HOS PR [`#581`](https://github.com/TheLaughingGod1986/history-of-science/pull/581) (`gemini/J2809-hos-topics-104-105`) · OWB PR [`#916`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/916) (`gemini/J2809-hos-topics-104-105`) |
| **Review Deliverables (`J2810`)** | HOS PR [`#582`](https://github.com/TheLaughingGod1986/history-of-science/pull/582) (`macbook/J2810`, isolated to `104_Roemer-Fizeau-Foucault-Speed-Of-Light`) · `jobs/reviews/J2810/REVIEW.md` (this file) |
| **Rule-E Verdict** | **GO (`96 / 100` · `9.60 / 10` Opportunity Score) — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G** |
| **Production & Claim Guard** | **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND.** Active `WIP.json["hos"]` has `6 / 6` slots full (`007`, `008`, `009`, `010`, `011`, `013`). All historical and scientific claims in `TOPIC.md` §2–§3 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes until an active HOS WIP slot opens, exact primary-source quotes are recorded in `SOURCES.md`, and the `facts` lane (`gemini-agy`) verifies every claim. |
| **Spend** | `£0.00` / `0` credits |

---

## 1. Executive Verdict

**Verdict: `GO` (`96 / 100` · `9.60 / 10` Opportunity Score, pre-cleared in `jobs/WIP.json` `next_hos` under Rule G).**

`HOS:104` (*How Did We Measure the Speed of Light? (A 720-Tooth Wheel)*) passes every mandatory gate in `AGENTS.md` Rule E, `STUDIO_PLAYBOOK.md` §2, `05_Analytics/LEARNINGS.md` Rules 1–31, and `jobs/reviews/J2748/RULING.md`:

1. **Data-First Analytics Comparison (`J2748` Ruling #2–#3):** `TOPIC.md` §1 cites exact snapshot timestamps (`2026-11-12T06:40:28.196Z` and `2026-11-13T06:40:29.166Z`) and the lifetime Studio read (`2026-11-12T07:07:54.728116+00:00`), states the exact numerator (`video.views`) and calendar-day denominator (`ageDays`), ranks all `7` public HOS longs and `28` public HOS Shorts by `views/day` without changing denominators mid-table (`PFj6172YU4Q`: `215v / 4d = 53.8/d` on `12 Nov`, `216v / 5d = 43.2/d` on `13 Nov`), provides separate rankings by impressions, CTR, stayed-to-watch (`-3L6HzJ_d_4` `#1` at `76.47%`), and avg % viewed (`pWySvZsneZg` `#1` at `112.43%`, `c2q7w0pgcn8` `#2` at `105.30%`), marks `<10`-view retention curves as `UNKNOWN`, and treats title/opening patterns as testable hypotheses.
2. **Signed-Out YouTube Autocomplete & Ranking Proof (`LEARNINGS.md` Rule 26):** Verified in `11_Upload-Package/evidence_2026-11-14_public_search.json` and `evidence_2026-11-14_neighbours.json` (`2026-11-14`):
   - `"how did we measure the speed of light"` → **`autocomplete = yes`** (`10` suggestions including `"how did we measure the speed of light"`, `"how we first measured the speed of light"`).
   - `"speed of light"` → **`autocomplete = yes`** (`10` suggestions including `"speed of light"`, `"speed of light explained"`, `"speed of light experiment"`).
   - `"fizeau"` → **`autocomplete = yes`** (`"fizeau experiment speed of light"`, `"fizeau's method to determine speed of light"`).
   - **Rule 26(a) Two Ranking Videos:**
     1. **Veritasium** [`pTn6Ewhb27k`](https://youtu.be/pTn6Ewhb27k) — *Why No One Has Measured The Speed Of Light* (**`24,352,264` views**)
     2. **Rational Thinker** [`Jl1I4MA-TaU`](https://youtu.be/Jl1I4MA-TaU) — *How the Speed of Light Was First Measured* (**`2,001,964` views**), alongside **Susskind Speaks** [`QqcLRZdVBIg`](https://youtu.be/QqcLRZdVBIg) (**`1,130,896` views**), **Carter Studios - Physics** [`8z1WR4b0hJY`](https://youtu.be/8z1WR4b0hJY) (**`799,836` views**), and **ayuta** [`a6gl8KZM0PM`](https://youtu.be/a6gl8KZM0PM) (*How to find the speed of light (Fizeau experiment)*, **`512,454` views**).
3. **Education Neighbour Gate (`STUDIO_PLAYBOOK.md` §2 Step 4):** `evidence_2026-11-14_neighbours.json` passes with **`bigCount = 11` education videos `≥ 1,000,000` views** (threshold `≥ 3`), `hasTed = true`, `gate = PASS`, and `failedQueries = []`, plus `4` additional `≥ 1M` education videos in `evidence_2026-11-14_public_search.json` (`15` total `≥ 1M` videos across both files).
4. **Exact Title Collision Check (`0` Collisions on All 5 Disambiguated Candidates):**
   - **Title A (Primary Proposal, Rule 26, `58 chars`):** `How Did We Measure the Speed of Light? (A 720-Tooth Wheel)` — **`0` exact collisions** (disambiguated from bare `How Did We Measure the Speed of Light?` on `Exploded View` `jMyuc5-1QF8`).
   - **Title B (T&C, Rule 23, `52 chars`):** `The 720-Tooth Wheel That Measured the Speed of Light` — **`0` exact collisions**.
   - **Title C (Rule 26 Exact Phrase First, `57 chars`):** `Speed of Light: How a 720-Tooth Wheel Measured It in 1849` — **`0` exact collisions** *(plus optional `≤50`-char Rule 15 tighter variant for packaging: `Speed of Light: Fizeau's 720-Tooth Wheel (1849)`, `47 chars`)*.
   - **Short `S01` (`51 chars`):** `How Did Jupiter's Moons Measure the Speed of Light?` — **`0` exact collisions**.
   - **Short `S02` (`57 chars`):** `Why Does Light Slow Down in Water? (Foucault's 1850 Test)` — **`0` exact collisions** (disambiguated from bare `Why does light slow down in water?` on `Fermilab` `CUjt36SD3h8`, `1,309,684` views).
5. **Reviewer Catch & Fix on HOS PR `#582`:**
   - In `TOPIC.md` line 194 of PR `#581`, the footnote beneath the `neighbours.py` top-12 table mistakenly stated that the 11th `≥1M` neighbour in `evidence_2026-11-14_neighbours.json` was `minutephysics` `b9F8Wn41NR4` (`1,500,829` views). Cross-checking `evidence_2026-11-14_neighbours.json` lines 198–208 confirmed that the actual 11th `≥1M` entry in that file is **`Veritasium` [`vVKFBaaL4uM`](https://youtu.be/vVKFBaaL4uM) (*Can You Go the Speed of Light?*, `2,289,873` views)**, alongside `3Blue1Brown` `KTzGBJPuJwM` (`2,896,005` views), `Rational Thinker` `Jl1I4MA-TaU` (`2,001,964` views), `Fermilab` `CUjt36SD3h8` (`1,309,684` views), and `Susskind Speaks` `QqcLRZdVBIg` (`1,130,896` views) in `evidence_2026-11-14_public_search.json`. Fixed in `TOPIC.md` on HOS PR `#582`.

---

## 2. 10-Gate Rule-E Checklist (`TOPIC_GO_NO_GO_SHEET.md`)

| # | Gate | Requirement | Evidence Verified | Verdict |
|---:|---|---|---|---|
| **1** | **Data-first analytics comparison** | Consistent `views/day` ranking (`12 Nov` & `13 Nov` snapshots + `12 Nov` `studio_ctr.json`), explicit numerators/denominators, separate metric rankings, `UNKNOWN` on small samples, hypotheses framing | `TOPIC.md` §1.1–§1.3 verified against `05_Analytics/hos/snapshots/2026-11-12.json`, `2026-11-13.json`, and `studio_ctr.json` | **PASS** |
| **2** | **Signed-out YouTube autocomplete (`Rule 26`)** | Primary phrase autocompletes (`suggest = yes`) in signed-out YouTube GB | `"how did we measure the speed of light"` = **yes** (`10` suggestions) · `"speed of light"` = **yes** (`10` suggestions) · `"fizeau"` = **yes** (`10` suggestions) | **PASS** |
| **3** | **Two ranking videos named (`Rule 26a`)** | Name 2 live ranking videos on the phrase with IDs and view counts | 1) `Veritasium` `pTn6Ewhb27k` (**`24,352,264` views**) · 2) `Rational Thinker` `Jl1I4MA-TaU` (**`2,001,964` views**) | **PASS** |
| **4** | **Education neighbour gate (`STUDIO_PLAYBOOK.md` §2 Step 4)** | `≥ 3` education videos at `≥ 1,000,000` views (`gate = PASS`) + TED/TED-Ed presence | **`11` education videos `≥ 1M` views** in `evidence_2026-11-14_neighbours.json` (`hasTed = true`, `gate = PASS`: 4 `TED-Ed` `1.02M–3.70M`, 3 `Veritasium` `2.29M–24.35M`, `Vsauce` `10.05M`, `Kurzgesagt` `9.99M`, `PBS Space Time` `7.13M`, `minutephysics` `4.30M`) + `4` more `≥ 1M` in `public_search.json` | **PASS** |
| **5** | **Exact title collision check (`public_search.py`)** | `0` exact collisions on Long Titles A, B, C and Short Titles `S01`, `S02` | All `5` candidate titles verified in `evidence_2026-11-14_public_search.json` with **`0` exact matches** | **PASS** |
| **6** | **Non-duplication check (`AGENTS.md`)** | Zero overlap across `02_Video-Projects/`, `ideas/`, `VIDEO_BACKLOG.json`, and `WIP.json` (`hos`, `next_hos`, `owb`) | Verified across `02_Video-Projects/000–105`, `ideas/011–097`, `VIDEO_BACKLOG.json`, `WIP.json`, and `OWB:024` | **PASS** |
| **7** | **Visual proof-first hook (`0:05–0:15`, Rules 10 & 30)** | Physical apparatus / mechanism in first `15 s`; zero *"By the end of this film..."* agenda line | Cold open on Fizeau's spinning **720-tooth brass cogwheel** slicing a lantern beam across Paris and eclipsing the returning flash (`0:05–0:15`) | **PASS** |
| **8** | **Two search-titled Shorts (`Rules 1, 2, 24, 27, 28`)** | `2` question-titled Shorts (`22–27 s`), `0%` Explorer & `0%` bars on Frame 0, `0.0 s` 2–3 word hook (`#FFE000` key word), payoff `≥70%` runtime, `<1.0 s` tail, zero CTA | `S01` (*How Did Jupiter's Moons Measure the Speed of Light?*, `51 chars`, Frame 0 `1676 ECLIPSE`) and `S02` (*Why Does Light Slow Down in Water? (Foucault's 1850 Test)*, `57 chars`, Frame 0 `SLOWER IN WATER`) | **PASS** |
| **9** | **Unverified claims guard (`J2748` Ruling #4)** | All historical & scientific claims marked **UNVERIFIED**; `01_Script/episode_script_draft_v01.md` untouched template | Explicit notices in `TOPIC.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, `TOPIC_GO_NO_GO_SHEET.md`, `TOPIC_OPPORTUNITY_SCORE.md`, `production-status.md`, `README.md`; script draft untouched | **PASS** |
| **10** | **WIP cap & spend guard (`Rule G`)** | `£0.00` spent; `status.json` all stages `"todo"` while in `next_hos` | `£0.00` spent; all `12` stages in `status.json` `"todo"`; `status_board.py --check` and `check_all.sh` PASS | **PASS** |

---

## 3. Opportunity Score Breakdown (`9.60 / 10` = `96 / 100`)

| Dimension | Weight | Score (1–10) | Weighted | Summary |
|---|---:|---:|---:|---|
| 1. Evergreen search intent | 25% | `10.0` | `2.50` | `"how did we measure the speed of light"`, `"speed of light"`, and `"fizeau"` all autocomplete (`yes`) in YouTube GB; ranking videos at `24.35M` (`Veritasium`) and `2.00M` (`Rational Thinker`). |
| 2. Competition gap | 20% | `9.0` | `1.80` | Big physics channels focus on relativistic paradoxes or theory; no painted-3D History of Science narrative walks chronologically through the 4 physical apparatuses (`1638 -> 1676 -> 1849 -> 1850/1862`). |
| 3. Narrative & visual arc | 20% | `10.0` | `2.00` | High-contrast mechanical & astronomical visuals: Galileo's hilltop lanterns, Jupiter's shadow cone eclipsing Io, Fizeau's 720-tooth brass wheel chopping a Paris beam, and Foucault's rotating mirror & water tube. |
| 4. Brand & guardrail fit | 20% | `10.0` | `2.00` | Pure HOS wonder-through-measurement lane; zero fearbait, zero conspiracy, zero duplication across HOS or OWB. |
| 5. Series / cluster potential | 15% | `8.7` | `1.30` | Anchors the HOS **Light & Optics Experimental Cluster** with `018` (IR/UV), `103` (Blue Sky), `025` (Young/Fresnel/Einstein), `032` (Michelson–Morley), and `038` (Doppler). |
| **Total Opportunity Score** | **100%** | — | **`9.60 / 10` (`96 / 100`)** | **GO (threshold `≥ 7.5` exceeded by `+2.10`)** |

---

## 4. Verification & Checks Run

- `python3 00_Brand/Channel-Setup/tools/status_board.py --check` (in HOS): **`16 status files and BOARD.json are in order` (`PASS`)**
- `00_Brand/Channel-Setup/tools/check_all.sh` (in HOS): **`ALL CHECKS PASS`** (`durable desk handoffs`, `email ratchet`, `no media`, `status board in sync`, `ElevenLabs guard tests`, `vo_check word tests`, `atempo check tests`, `voice speed`, `contract tests`, `package-lint`)
