# J2811 — Rule-E Topic Go/No-Go Review: `HOS:105` (*How Do Venus Flytraps Work? (The Plant That Counts to Five)*)

- **Date:** 14 November 2026 (`05:42 UTC`)
- **Job:** `J2811` (*HOS 105 Venus Flytrap: rule-E topic go/no-go review*)
- **Upstream Proposal Verified:** `J2809` (completed by `gemini` on the Mini at commit `0331a42e` on HOS PR `#581` and commit `e2a03594a` on OWB PR `#916`)
- **Reviewer:** `macbook-2` (`Gemini 4 Argon (High)` / `gemini-argon`, Rule-E review lane)
- **Film Reviewed:** **`HOS:105`** — `02_Video-Projects/105_Ellis-Darwin-BurdonSanderson-Venus-Flytrap-Carnivorous-Plants` (*How Do Venus Flytraps Work? (The Plant That Counts to Five)*)
- **Deliverable PRs:**
  - **History of Science PR `#583`** (`https://github.com/TheLaughingGod1986/history-of-science/pull/583`, branch `macbook/J2811`, commit `5e4ea16e`, building on `J2809` HOS PR `#581`): adds `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` (`95/100`) and `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`, completes `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` (`§4–§7`), disambiguates Title B & Short `S01` in `evidence_2026-11-14_public_search.json`, and updates `TOPIC.md`, `production-status.md`, `status.json`, and `README.md` (`00_Brand/Channel-Setup/tools/check_all.sh` **ALL CHECKS PASS**).
  - **Orbit With Ben PR** (branch `macbook/J2811`, alongside `J2809` OWB PR `#916`): records this `jobs/reviews/J2811/REVIEW.md`.
- **Spend / Production / Studio:** **£0.00 / 0 credits.** No production work, spend, script lock, VO, or Studio change starts from this review job; active HOS WIP capacity (`4/4` under Rule G) and `facts`-lane gates stay unchanged.
- **Rule-E Verdict (Recorded for Chief Review):** **`GO` (`95 / 100` Opportunity Score — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G, with Title B & Short `S01` disambiguated to `0` collisions; Historical & Scientific Claims Explicitly Unverified Until `SOURCES.md` + `facts` Lane)**

---

## 1. Executive Summary & Rule-E Rubric Verdict

| Film ID & Folder | Primary Title A (`Rule 26` + `Rule 15`, `0` collisions) | Title B (`Rule 15` + `Rule 23` T&C, disambiguated in `J2811`, `0` collisions) | Title C (`Rule 26` Exact Phrase First, `≤70` chars, `0` collisions) | Verified `≥1M` Education Neighbours (`2026-11-14`) | Verified Plain Search Phrases & Ranking Videos (`2026-11-14`) | Opportunity Score | Rule-E Verdict |
|---|---|---|---|---|---|---|---|
| **`HOS:105`** `02_Video-Projects/105_Ellis-Darwin-BurdonSanderson-Venus-Flytrap-Carnivorous-Plants` | `How Do Venus Flytraps Work? (The Plant That Counts to Five)` (`59 chars`, `0` collisions; `≤50`-char Rule 15 variant: `How Do Venus Flytraps Work? (Counting to Five)`, `46 chars`, `0` collisions) | `The Leaf That Counts to Five Before It Digests` (`46 chars`, `0` collisions; or `How Do Venus Flytraps Work? (1873 Electric Leaf)`, `48 chars`, `0` collisions) | `Carnivorous Plants: Why Darwin Fed Roast Beef to a Leaf` (`55 chars`, `0` collisions) | **`6` education videos `≥1M` views** (`TED-Ed/TED: yes`, led by `TED-Ed` `4.45M` `Hja0SLs2kus`, `TED` `3.30M` `pvBlSFVmoaw`, `TED-Ed` `2.36M` `ee7muQ_qKU0`, `TED-Ed` `1.74M` `fSaHVHTqDY0`, `Amoeba Sisters` `1.29M` & `1.18M`) + `12` direct `≥1M` explainers in `public_search.py` (`Ze Frank` `15.87M`, `Peekaboo Kidz` `14.41M`, `BBC` `13.77M`, `Insider Science` `7.61M`, `SciShow` `1.20M`) | `"how do venus flytraps work"`, `"carnivorous plants"`, `"why do some plants eat insects"` (`autocomplete = yes`); ranking videos: `BBC` `O7eQKSf0LmY` (`13,770,762` views) & `Insider Science` `YPzp-p-na88` (`7,610,046` views) | **`9.50 / 10` (`95 / 100`)** | **`GO` (in `next_hos`; claims UNVERIFIED)** |

---

## 2. Detailed Verification Against the 4-Item `J2811` Checklist & 10 Rule-E Gates

### 2.1 File & Raw-JSON Evidence Verification (`J2811` Checklist #1) — `PASS (with 2 Raw-JSON Collisions Caught & Fixed)`
- Inspected all files in `02_Video-Projects/105_Ellis-Darwin-BurdonSanderson-Venus-Flytrap-Carnivorous-Plants/` on HOS PR `#581`: `TOPIC.md`, `status.json`, `production-status.md`, `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, `11_Upload-Package/evidence_2026-11-14_neighbours.json`, `11_Upload-Package/evidence_2026-11-14_public_search.json`, `01_Script/episode_script_draft_v01.md`, and `README.md`.
- **Reviewer Catch #1 (Title Collisions in Raw `evidence_2026-11-14_public_search.json`):**
  - Because `public_search.py` prints only the top 5 results per query to stdout while writing 8 results per query to the JSON file, `J2809` reported `0` collisions on all 5 titles. Inspecting all 8 search results per query in `evidence_2026-11-14_public_search.json` uncovered two collisions at results #6–#7:
    1. **Bare Title B (`The Plant That Counts to Five Before It Eats`, `44 chars`):** Result #7 (`id: "ay4_XzfjXm8"`, channel `"The Know-It-Owl"`, `997 views`, `2 mo ago`, `0:31`) is titled verbatim `"The Plant That Counts to Five Before It Eats"`.
    2. **Bare Short `S01` (`How Does a Venus Flytrap Count to Five?`, `39 chars`):** Result #6 (`id: "BL4G1n7g6VI"`, channel `"BearlyBelievable"`, `1,004 views`, `3 mo ago`, `0:21`) is titled `"How does a Venus flytrap count to five? 🪴"`, and result #4 (`id: "x7nd0M1g8DY"`, channel `"edushorts"`, `131 views`) is titled `"How Do Venus Flytraps Count to Five?"`.
  - **Fix Applied in HOS PR `#583`:** Marked both bare strings as **Rejected (Collision)** under `studio/RULES.md` Never list (*"never a title that copies a live video"*), ran `public_search.py` to verify disambiguated replacements across all 8 search hits (`0` collisions), and updated `evidence_2026-11-14_public_search.json`, `TOPIC.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, `TOPIC_OPPORTUNITY_SCORE.md`, `TOPIC_GO_NO_GO_SHEET.md`, and `production-status.md`:
    - **Disambiguated Title B:** `The Leaf That Counts to Five Before It Digests` (`46 chars`, `0` collisions) / `How Do Venus Flytraps Work? (1873 Electric Leaf)` (`48 chars`, `0` collisions, Rule 26 phrase-first).
    - **Disambiguated Short `S01`:** `How Does a Venus Flytrap Count to Five? (Two-Touch Test)` (`56 chars`, `0` collisions).
    - **Also Added `≤50`-Char Rule 15 Variant of Title A:** `How Do Venus Flytraps Work? (Counting to Five)` (`46 chars`, `0` collisions) alongside `59`-char `How Do Venus Flytraps Work? (The Plant That Counts to Five)`.
- **Reviewer Catch #2 (`PRE_BUILD_VIDIQ_AUDIT.md` Completion & Autocomplete Accuracy):**
  - On HOS PR `#581`, `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` ended at `§3b` (`96` lines) without `§4` (*Outlier / competitive patterns*), `§5` (*Incorporate into the build*), `§6` (*Retention plan*), or `§7` (*Sign-off*), and slightly paraphrased two autocomplete strings in `§2`. Completed `§4–§7` and aligned `§2` verbatim with `evidence_2026-11-14_public_search.json` in HOS PR `#583`.

### 2.2 Neighbour Gate & Search Demand (`J2811` Checklist #2) — `PASS`
- **Neighbour Gate (`evidence_2026-11-14_neighbours.json`):** `gate = "PASS"`, `bigCount = 6` education videos `≥ 1,000,000` views (need `3`), `hasTed = true`:
  1. `TED-Ed` (`Hja0SLs2kus`): *The amazing ways plants defend themselves - Valentin Hammoudi* — **`4,447,004` views**
  2. `TED` (`pvBlSFVmoaw`): *Electrical experiments with plants that count and communicate | Greg Gage* — **`3,302,069` views** (direct Venus flytrap electrical action-potential and counting demonstration)
  3. `TED-Ed` (`ee7muQ_qKU0`): *The wild world of carnivorous plants - Kenny Coogan* — **`2,362,056` views** (direct carnivorous-plants lesson)
  4. `TED-Ed` (`fSaHVHTqDY0`): *These animals are also plants … wait, what? - Luka Seamus Wright* — **`1,742,029` views**
  5. `Amoeba Sisters` (`DGpPHrLF-5M`): *(OLD VIDEO) Plant Structure and Adaptations* — **`1,289,643` views**
  6. `Amoeba Sisters` (`A_DF246uVlU`): *Plants: Diversity, Structure, & Adaptations* — **`1,182,864` views**
- **Signed-Out YouTube Autocomplete & Ranking Videos (`LEARNINGS.md` Rule 26):**
  - `"how do venus flytraps work"` (`autocomplete = yes`), `"carnivorous plants"` (`autocomplete = yes`), `"why do some plants eat insects"` (`autocomplete = yes`).
  - Ranking videos for `"how do venus flytraps work"`: `BBC` `O7eQKSf0LmY` (**`13,770,762` views**) and `Insider Science` `YPzp-p-na88` (**`7,610,046` views**), plus `Peekaboo Kidz` `Rj4FiwB1FWE` (`2,333,002` views), `Learn Bright` `5MnZWamBUCE` (`1,966,853` views), `Colossal Cranium` `JPCr4U1VL30` (`1,352,980` views), `Real Science` `CAUOhG_c4Go` (`1,271,863` views), and `SciShow` `PxQj0xjObVE` (*Darwin's Darlings: Meat-Eating Plants*, `1,202,692` views).

### 2.3 Non-Duplication & Visual Proof-First Hook (`J2811` Checklist #2) — `PASS`
- **Zero Overlap:** Checked across `02_Video-Projects/000–104` (including `006` Trees/Photosynthesis, `012` Mendel's Pea Plants, `013` Darwin & Wallace Evolution, and open PRs `102` Ozone Hole, `103` Why Is the Sky Blue, `104` Speed of Light), `00_Brand/Channel-Setup/ideas/011–097` (including `073` Transpiration, `081` Phototropism/Auxin, `091` Wood Wide Web), `VIDEO_BACKLOG.json`, and `jobs/WIP.json` (`active` and `next_hos`). None covers Venus flytraps, carnivorous plants, Ellis vs Linnaeus (`1768–1770`), Darwin's `1875` *Insectivorous Plants* bog-nitrogen feeding tests, Burdon-Sanderson's `1873` plant action potential, or Hedrich's `2016` five-touch counter.
- **Proof-First `0:05–0:15` Apparatus Fit (`Rule 10` & `Rule 30` `HOS-2026-11-E2`):** An open Venus flytrap leaf wired to Burdon-Sanderson's `1873` brass mirror galvanometer as two touches on its sensory hairs fire a visible needle deflection and snap the jaws shut gives a concrete, silent-readable physical proof for `0:05–0:15`.

### 2.4 Explicit Unverified Claims Guard & Rule G WIP Capacity (`J2811` Checklist #3–#4) — `PASS`
- All historical and scientific claims — including John Ellis's `1768–1770` letter to Carl Linnaeus and Linnaeus's reply, Charles Darwin's `1875` *Insectivorous Plants* feeding experiments, John Scott Burdon-Sanderson's `1873` Venus flytrap electrical action-potential galvanometer measurements, and Rainer Hedrich / Böhm et al.'s `2016` five-touch counting mechanism — remain **explicitly marked UNVERIFIED** and **not cleared for narration or Short opens** across `TOPIC.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, `TOPIC_OPPORTUNITY_SCORE.md`, `TOPIC_GO_NO_GO_SHEET.md`, and `production-status.md`.
- `01_Script/episode_script_draft_v01.md` remains the untouched blank template, and `status.json` keeps all stages `todo`.
- Active HOS WIP remains at `4/4` (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). `HOS:105` waits in `jobs/WIP.json` `next_hos` (OWB PR `#916`) until an active HOS WIP slot opens, at which point `SOURCES.md` primary quotes and the `facts` lane must pass before any script lock, VO, or picture generation.
