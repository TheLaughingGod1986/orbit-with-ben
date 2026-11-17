# `J2918` — Rule-E Topic Go/No-Go Review: `HOS:109` (`109_Lewis-Pickering-WilderSmith-Smulders-Why-Fingers-Wrinkle`)

| Field | Value |
|---|---|
| **Job ID & Reviewer** | `J2918` · `macbook` (Gemini 4 Argon High / `gemini-argon`, `review` lane) |
| **Target Film** | `HOS:109` (`02_Video-Projects/109_Lewis-Pickering-WilderSmith-Smulders-Why-Fingers-Wrinkle` · *Why Do Fingers Wrinkle in Water? (The Cut-Nerve Proof)*) |
| **Source Proposal (`J2891`)** | HOS PR [`#602`](https://github.com/TheLaughingGod1986/history-of-science/pull/602) (`gemini/J2891-hos-topics-108-109`) · OWB PR [`#951`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/951) (`gemini/J2891-hos-wip-108-109`) |
| **Review Deliverables (`J2918`)** | HOS PR [`#603`](https://github.com/TheLaughingGod1986/history-of-science/pull/603) (`macbook/J2918`, isolated to `109_Lewis-Pickering-WilderSmith-Smulders-Why-Fingers-Wrinkle`) · `jobs/reviews/J2918/REVIEW.md` (this file) |
| **Rule-E Verdict** | **GO (`95.5 / 100` · `9.55 / 10` Opportunity Score) — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G** |
| **Production & Claim Guard** | **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND.** Active HOS slots in `jobs/WIP.json` are `4 / 4` full (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). All historical and scientific claims in `TOPIC.md` §4–§5 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes until an active HOS WIP slot opens, exact primary-source quotes are recorded in `SOURCES.md`, and the `facts` lane (`gemini-agy`) verifies every claim. |
| **Spend** | `£0.00` / `0` credits |

---

## 1. Executive Verdict

**Verdict: `GO` (`95.5 / 100` · `9.55 / 10` Opportunity Score, pre-cleared in `jobs/WIP.json` `next_hos` under Rule G).**

`HOS:109` (*Why Do Fingers Wrinkle in Water? (The Cut-Nerve Proof)*) passes every mandatory gate in `AGENTS.md` Rule E, `STUDIO_PLAYBOOK.md` §2, `05_Analytics/LEARNINGS.md` Rules 1–33, and `jobs/reviews/J2748/RULING.md`:

1. **Data-First Analytics Comparison (`J2748` Ruling #2–#3):** `TOPIC.md` §1 cites the exact snapshot timestamp (`05_Analytics/hos/snapshots/2026-11-15.json`, `takenAt: 2026-11-15T06:40:28.409Z`), the lifetime Studio read (`05_Analytics/hos/studio_ctr.json`, `readAt: 2026-11-15T07:53:35.291276+00:00`), and `05_Analytics/hos/channel_daily.json` (`through: 2026-11-13`), states the exact numerator (`views`) and calendar-day denominator (`age_days = max((date(2026,11,15) - published_date).days, 1)`), ranks all `7` public HOS longs (`002` `#1` at `2.73/d` & `1,160` impr; `004` `#2` at `1.10/d` & `837` impr; `006` `#3` at `1.00/d` & `66.54%` avg view %) and all `29` public HOS Shorts (`29bpGAI0wb8` `#1` at `40.90/d`; `PFj6172YU4Q` `#2` at `31.29/d`; `AMSriTQ-lcQ` `#3` at `15.22/d`), and frames small-N patterns explicitly as hypotheses.
2. **Signed-Out YouTube Autocomplete & Ranking Proof (`LEARNINGS.md` Rule 26):** Verified in `11_Upload-Package/evidence_2026-11-15_public_search.json` and `evidence_2026-11-15_neighbours.json` (`2026-11-15`):
   - `"why do fingers wrinkle in water"` → **`autocomplete = yes`** (`4` suggestions: `"why do fingers wrinkle in water"`, `"why do fingers get wrinkly in water"`, `"why do my hands wrinkle in water so fast"`, `"why fingers prune in water"`).
   - `"why do fingers prune in water"` → **`autocomplete = yes`** (`3` suggestions: `"why do fingers wrinkle in water"`, `"why do my hands wrinkle in water so fast"`, `"why fingers prune in water"`).
   - `"how skin works"` → **`autocomplete = yes`** (`10` suggestions including `"how skin works"`, `"how skin works animation"`, `"how your skin works"`).
   - `"sympathetic nervous system"` → **`autocomplete = yes`** (`10` suggestions including `"sympathetic nervous system"`, `"sympathetic nervous system anatomy"`, `"sympathetic nervous system physiology"`).
   - **Rule 26(a) Two Ranking Videos:**
     1. **Colossal Cranium** [`DspDvog4W00`](https://youtu.be/DspDvog4W00) — *Why Does Skin Wrinkle in Water? | COLOSSAL QUESTIONS* (**`1,370,412` views**)
     2. **SciShow** [`kqhoLNUTS8I`](https://youtu.be/kqhoLNUTS8I) — *Why Do We Wrinkle When Wet?* (**`1,180,362` views** in `public_search.json` / **`1,180,364` views** in `neighbours.json`), alongside **BYJU'S** [`-5V5BjunAwE`](https://youtu.be/-5V5BjunAwE) (**`505,669` views**), **SciShow Kids** [`uWjlRlpHlbA`](https://youtu.be/uWjlRlpHlbA) (**`398,961` views**), **Seeker** [`Aa1FRQ2o-wI`](https://youtu.be/Aa1FRQ2o-wI) (**`172,928` views**), and **TED-Ed** [`k7ve_ibAY1s`](https://youtu.be/k7ve_ibAY1s) (*Why do fingers become pruney? - Mark Changizi*, **`115,153` views**).
3. **Education Neighbour Gate (`STUDIO_PLAYBOOK.md` §2 Step 4):** `evidence_2026-11-15_neighbours.json` passes with **`bigCount = 11` education videos `≥ 1,000,000` views** (threshold `≥ 3`), `hasTed = true`, `gate = PASS`, and `failedQueries = []`, plus `Colossal Cranium` (`1,370,412` views) in `evidence_2026-11-15_public_search.json` (`12` total `≥ 1M` videos across both files).
4. **Raw-JSON Verification & Corrections Applied in HOS PR [`#603`](https://github.com/TheLaughingGod1986/history-of-science/pull/603):** During line-by-line review of `evidence_2026-11-15_neighbours.json` and `evidence_2026-11-15_public_search.json`, several transcribed IDs/titles in PR `#602`'s markdown tables were corrected in HOS PR `#603` so all markdown tables match the raw JSON evidence verbatim:
   - `VVL-8zr2hk4` is `TED-Ed` *How your muscular system works - Emma Bryce* (`3,268,747` views), not Hilary Coller;
   - `gsV7SJDDCY4` is `TED-Ed` *How X-rays see through your skin - Ge Wang* (`2,363,909` views), not Eleanor Nelsen;
   - `CrashCourse` *Sympathetic Nervous System: Crash Course Anatomy & Physiology #14* is `0IDgBlCHVsA` (`2,837,651` views), not `x8tF2aQ3V1k`;
   - Added the 10th and 11th `≥1M` neighbours from `neighbours.json`: `Amoeba Sisters` `t1iQHHJ0YyE` (*Integumentary System*, `1,639,077` views) and `SciShow` `kqhoLNUTS8I` (*Why Do We Wrinkle When Wet?*, `1,180,364` views), replacing two videos (`LM682F16ebU`, `HiuXfbwND9s`) that were not in `evidence_2026-11-15_neighbours.json`;
   - Updated the `public_search.json` IDs/titles for `Colossal Cranium` (`DspDvog4W00`, *Why Does Skin Wrinkle in Water? | COLOSSAL QUESTIONS*, `1,370,412` views) and `SciShow` (`kqhoLNUTS8I`, *Why Do We Wrinkle When Wet?*, `1,180,362` views);
   - Updated `TOPIC.md` §2 open-PR references (`#572` `102/103` Ozone Hole / Blue Sky, `#581` `104/105` Speed of Light / Venus Flytrap, `#588` `106/107` Eels / Autumn Leaves, `#602` `108` Ice Slippery) and `jobs/WIP.json` active HOS count (`4 / 4` full: `HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`).
5. **Exact Title Collision Check (`0` Collisions on All 5 Candidates):** All 5 candidate titles (`A`, `B`, `C`, `S01`, `S02`) were queried in `evidence_2026-11-15_public_search.json` and confirmed to have **`0` exact matches**.

---

## 2. Rule-E 10-Gate Rubric Table

| # | Gate | Requirement | Evidence (`HOS:109`) | Result |
|---:|---|---|---|---|
| **1** | **Data-first analytics comparison (`J2748` Ruling #2–#4)** | Single consistent `views/day` ranking across all public longs & Shorts with exact timestamps and denominators; small-N framed as hypotheses | `2026-11-15T06:40:28.409Z` snapshot + `2026-11-15T07:53:35.291276+00:00` `studio_ctr.json` + `channel_daily.json` (`through: 2026-11-13`); all `7` longs and `29` Shorts ranked by `views/day` | **PASS** |
| **2** | **Signed-out YouTube autocomplete (`Rule 26`)** | Primary search phrase autocompletes (`suggest = yes`) in signed-out YouTube GB | `"why do fingers wrinkle in water"` = **yes** (`4` suggestions), `"why do fingers prune in water"` = **yes** (`3` suggestions), `"how skin works"` = **yes** (`10` suggestions), `"sympathetic nervous system"` = **yes** (`10` suggestions) | **PASS** |
| **3** | **Two ranking videos named (`Rule 26a`)** | Name 2 live ranking videos on the phrase with IDs and view counts | 1) `Colossal Cranium` `DspDvog4W00` (**`1,370,412` views**) · 2) `SciShow` `kqhoLNUTS8I` (**`1,180,362` views** in `public_search.json` / **`1,180,364` views** in `neighbours.json`), plus `TED-Ed` `k7ve_ibAY1s` (**`115,153` views**) | **PASS** |
| **4** | **Education neighbour gate (`STUDIO_PLAYBOOK.md` §2 Step 4)** | `≥ 3` education videos at `≥ 1,000,000` views (`gate = PASS`) + TED/TED-Ed presence | **`11` education videos `≥ 1M` views** in `evidence_2026-11-15_neighbours.json` (`hasTed = true`, `gate = PASS`: 4 `TED-Ed` `2.36M–3.54M` + `k7ve_ibAY1s` `115.2k`, 3 `CrashCourse` `2.84M–5.94M`, `Veritasium` `4.84M`, 2 `Amoeba Sisters` `1.64M–4.32M`, `SciShow` `1.18M`) + `Colossal Cranium` `1.37M` in `public_search.json` | **PASS** |
| **5** | **Exact title collision check (`public_search.py`)** | `0` exact collisions on Long Titles A, B, C and Short Titles `S01`, `S02` | All `5` candidate titles verified in `evidence_2026-11-15_public_search.json` with **`0` exact matches** | **PASS** |
| **6** | **Non-duplication check (`AGENTS.md`)** | Zero overlap across `02_Video-Projects/`, `ideas/`, `VIDEO_BACKLOG.json`, open PRs, and `WIP.json` | Verified across `02_Video-Projects/000–101`, open PRs `#572`/`#581`/`#588`/`#602` (`102–108`), `ideas/011–095` + `IDEAS_*.md`, `VIDEO_BACKLOG.json`, and `WIP.json` | **PASS** |
| **7** | **Visual proof-first hook (`0:05–0:15`, Rules 10 & 30)** | Physical apparatus / clinical proof in first `15 s`; zero *"By the end of this film..."* agenda line | Cold open on a patient's hand lifted from a warm hospital water basin in `1935` London showing three median-nerve-denervated fingers completely smooth right beside two deeply wrinkled healthy fingers (`0:05–0:15`) | **PASS** |
| **8** | **Two search-titled Shorts (`Rules 1, 2, 24, 27, 28`)** | `2` question-titled Shorts (`22–27 s`), `0%` Explorer & `0%` bars on Frame 0, `0.0 s` 2–3 word hook (`#FFE000` key word), payoff `≥70%` runtime, `<1.0 s` tail, zero CTA | `S01` (*Why Doesn't Cut-Nerve Skin Wrinkle in Warm Water?*, `49 chars`, `0` collisions) and `S02` (*Do Wrinkled Fingers Really Help You Grip Wet Objects?*, `53 chars`, `0` collisions) | **PASS** |
| **9** | **Unverified claims guard (`J2748` Ruling #4)** | All historical & scientific claims marked **UNVERIFIED**; `01_Script/episode_script_draft_v01.md` untouched template | Explicit notices in `TOPIC.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, `TOPIC_GO_NO_GO_SHEET.md`, `TOPIC_OPPORTUNITY_SCORE.md`, `production-status.md`, `README.md`; script draft untouched | **PASS** |
| **10** | **WIP cap & spend guard (`Rule G`)** | `£0.00` spent; `status.json` all stages `"todo"` while in `next_hos` | `£0.00` spent; all `12` stages in `status.json` `"todo"`; `status_board.py --check` and `check_all.sh` PASS | **PASS** |

---

## 3. Opportunity Score Breakdown (`9.55 / 10` = `95.5 / 100`)

| Dimension | Weight | Score (1–10) | Weighted | Summary |
|---|---:|---:|---:|---|
| 1. Evergreen search intent | 25% | `10.0` | `2.50` | `"why do fingers wrinkle in water"`, `"why do fingers prune in water"`, `"how skin works"`, and `"sympathetic nervous system"` all autocomplete (`yes`) in YouTube GB; ranking videos at `1.37M` (`Colossal Cranium` `DspDvog4W00`) and `1.18M` (`SciShow` `kqhoLNUTS8I`). |
| 2. Competition gap | 20% | `9.0` | `1.80` | Existing videos are `2–5 min` single-beat summaries (`SciShow` `2:10`, `Colossal Cranium` `2:17`, `TED-Ed` `4:21`); none tell the chronological `80-year` experimental detective story (`1935–1936 -> 1973 -> 2003 -> 2011/2013`). |
| 3. Narrative & visual arc | 20% | `9.5` | `1.90` | Striking `0:05–0:15` visual proof (three smooth denervated fingers beside two wrinkled fingers in a 1935 hospital basin), digital glomus-body vasoconstriction diagrams, watershed rain-tread channels, and the timed submerged wet-marble experiment. |
| 4. Brand & guardrail fit | 20% | `10.0` | `2.00` | Pure HOS wonder-through-proof lane on a universal human-hand mystery; zero medical advice, zero fearbait, zero duplication across HOS or OWB. |
| 5. Series / cluster potential | 15% | `9.0` | `1.35` | Anchors the HOS **Human Body & Nervous Reflex Cluster** with `005` (Harvey circulation, `#2` Short `PFj6172YU4Q` `31.29/d`), `011` (Anaesthesia), `019` (Galvani/Volta), `033` (Cajal/Loewi), `051` (Capsaicin/TRPV1), and `086` (Pain/Endorphins). |
| **Total Opportunity Score** | **100%** | — | **`9.55 / 10` (`95.5 / 100`)** | **GO (threshold `≥ 7.5` exceeded by `+2.05`)** |

---

## 4. Verification & Checks Run

- `python3 00_Brand/Channel-Setup/tools/status_board.py --check` (in HOS): **`16 status files and BOARD.json are in order` (`PASS`)**
- `00_Brand/Channel-Setup/tools/check_all.sh` (in HOS): **`ALL CHECKS PASS`** (`durable desk handoffs`, `email ratchet`, `no media`, `status board in sync`, `ElevenLabs guard tests`, `vo_check word tests`, `atempo check tests`, `voice speed`, `contract tests`, `package-lint`)
