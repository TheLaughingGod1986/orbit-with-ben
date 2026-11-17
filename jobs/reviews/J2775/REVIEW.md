# J2775 — Rule-E Topic Go/No-Go Review: `HOS:102` (*How Did We Find the Hole in the Ozone Layer?*)

- **Date:** 13 November 2026 (`14:10 UTC`)
- **Job:** `J2775` (*HOS 102 Ozone Hole: rule-E topic go/no-go review*, `--after J2748`, `board: 102 topic`)
- **Reviewer:** `macbook-2` (`Gemini 4 Argon` / `gemini-argon`, Rule-E review lane)
- **Film Reviewed:** **`HOS:102`** — `02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole` (*How Did We Find the Hole in the Ozone Layer?*)
- **Source & Review PRs:**
  - Source proposal PRs from `J2748`: HOS PR **#572** (`macbook/J2748`, `34324bee`), OWB PR **#881** (`macbook/J2748`, `24cea34c`)
  - Rule-E scorecard & Go/No-Go sheet PR from `J2775`: HOS PR **#576** (`macbook/J2775`, `fbebf688`, https://github.com/TheLaughingGod1986/history-of-science/pull/576)
- **Authority & Scope:** `AGENTS.md` Rule E (*"Topic and script calls are reviewer calls, not Chief calls"*), Rule G (*"At most 9 films in production: 5 OWB, 4 HOS"*), HOS `studio/RULES.md` Definition of Done, `STUDIO_PLAYBOOK.md` §2, `05_Analytics/LEARNINGS.md` rules 1–30, and `jobs/reviews/J2748/RULING.md` (`d1e1e26ed0`).
- **Spend / Publishing:** **£0.00 / 0 credits.** No paid APIs, no TTS/video generation, no script lock, no Studio or publish mutations.
- **Verdict:** **`GO (PRE-CLEARED IN BACKLOG next_hos UNDER RULE G — 94.5 / 100 OPPORTUNITY SCORE)`** — `HOS:102` passes the Rule-E topic rubric (non-duplication, `neighbours.py` `PASS` with `7` education videos `≥1M` views + `5` additional `1M–10M+` direct ozone-hole explainers in `public_search.py` + `TED-Ed` `5wVJeq4mLL0` `670k` `#1` GB search hit, Rule 26 autocomplete & ranking evidence, `0` exact-title collisions across Long Titles `A`/`B`/`C` and Shorts `S01`/`S02`, proof-first `0:05–0:15` **Dobson spectrophotometer** apparatus fit, and corrected `12 Nov` / `13 Nov` analytics comparison). All historical and scientific claims remain **explicitly marked UNVERIFIED** and are **NOT cleared for narration or Short opens** until primary quotes in `SOURCES.md` and the `facts` lane (`gemini-agy`) run when `HOS:102` enters an active HOS WIP slot under Rule G. No production work starts from this review.

---

## 1. Executive Summary Matrix

| Film ID & Folder | Working Title A (`≤50` chars, `0` collisions) | Title B (Rule 23 Story + Stakes, `0` collisions) | Title C (Rule 26 Exact Search Phrase First + Stakes, `≤70` chars, `0` collisions) | Verified `≥1M` Neighbours (`2026-11-13`) | Rule 26 Plain Search Phrases & Ranking Videos (`2026-11-13`) | Opportunity Score | Rule-E Verdict (Under Rule G) |
|---|---|---|---|---|---|---|---|
| **`HOS:102`**<br>`102_Molina-Rowland-Farman-Ozone-Hole` | `How Did We Find the Hole in the Ozone Layer?` (**44 chars**) | `The Ozone Hole (Found by an Instrument From the 1950s)` (**54 chars**) | `Hole in the Ozone Layer: How a 1950s Ground Instrument Found It` (**64 chars**) | **`7` in `neighbours.py` (`PASS`, `TED-Ed/TED = yes`) + `5` in `public_search.py`** (`Veritasium` `43.56M`, `Kurzgesagt` `14.08M`, `Vox` `10.16M`, `Cleo Abram` `8.53M`, `Peekaboo Kidz` `4.28M`, `TED-Ed` `2.80M`, `Seeker` `2.49M`, `Astrum Earth` `1.67M`, plus `TED-Ed` `5wVJeq4mLL0` `670k` `#1` GB hit) | `"hole in the ozone layer"` (`yes`), `"ozone layer"` (`yes`), `"ozone hole"` (`yes`) · Ranking: `Vox` `CaLOiGEDPJQ` (`10,161,545` v), `Astrum Earth` `EmaQVbdd6Ko` (`1,673,345` v), `TED-Ed` `5wVJeq4mLL0` (`670,049` v) | **`9.45 / 10`**<br>(**`94.5 / 100`**) | **`GO` in `next_hos`** — Wait for active HOS WIP slot (`4/4` full), then run `SOURCES.md` + `facts` lane before script lock |

---

## 2. Verification of `J2748` Ruling Corrections (`jobs/reviews/J2748/RULING.md` `d1e1e26ed0`) & Rule-E Checklist

### 2.1 Non-Duplication Across `02_Video-Projects/`, `ideas/`, `VIDEO_BACKLOG.json`, `PIPELINE.json`, and `WIP.json` (`PASS`)
- Direct audit of `/Users/ben/_desk/worker/slot2/history-of-science` confirms **zero overlap**:
  - `02_Video-Projects/` (`000`–`011`, `013`, `099`–`101`): None covers CFCs, Molina & Rowland, Farman/Halley Bay, or stratospheric ozone depletion.
  - `00_Brand/Channel-Setup/ideas/` (`011`–`095` & `IDEAS_*.md`): Idea `034_Foote-Tyndall-Arrhenius-Greenhouse` covers infrared heat absorption by $CO_2$ and water vapour (1856–1896), a different gas, spectral band, atmospheric mechanism, and cast; `103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue` covers visible Rayleigh scattering (1869–1899).
  - `jobs/WIP.json`: Active HOS capacity is at `4/4` (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`), and `next_hos` holds `["HOS:011", "HOS:012", "HOS:014", "HOS:015", "HOS:018", "HOS:100", "HOS:101"]` on `main` (with `HOS:102` and `HOS:103` proposed on OWB PR `#881`).

### 2.2 Neighbour Gate & Transparent Query-Scope Disclosure (`PASS`)
- Saved in `02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole/11_Upload-Package/evidence_2026-11-13_neighbours.json` and `evidence_2026-11-13_public_search.json` (retrieved `2026-11-13`):
  - **Transparent query-scope disclosure (`TOPIC.md` §2.3.B & `TOPIC_OPPORTUNITY_SCORE.md` §2):** `neighbours.py` filters strictly to its hardcoded `TIER1`/`TIER2` channel lists. On `"ozone layer" "ozone hole"` alone, `neighbours.py` returns `TED-Ed` `5wVJeq4mLL0` (`670,049` views), `FuseSchool` `J0bx2BuxT-I` (`218,515` views), `TED` `08z_xW-szwM` (`197,607` views), `Khan Academy` `E1P79uFLCMc` (`101,249` views), `Natural History Museum` `7QGD-KiqKdE` (`59,486` views), and `Khan Academy` `5CGtESB40Rc` (`23,563` views) because the five `1M–10M+` direct ozone-hole explainers (`Vox` `10.16M`, `Cleo Abram` `8.53M`, `Peekaboo Kidz` `4.28M`, `Seeker` `2.49M`, `Astrum Earth` `1.67M`) sit on science/explainer channels outside `neighbours.py`'s `TIER1`/`TIER2` list, and `Veritasium`'s `43.56M`-view film on Thomas Midgley Jr.'s CFCs (`IV3dnLzthDA`) does not contain `"ozone"` in its title.
  - With `"earth atmosphere"` and `"thomas midgley killed"` included, `neighbours.py` prints **`PASS` (`7` education videos `≥1,000,000` views, `TED-Ed/TED = yes`)**, led by `Veritasium` (`https://youtu.be/IV3dnLzthDA`, `43,564,438` views), `Kurzgesagt` (`https://youtu.be/JGXi_9A__Vc`, `14,084,839` views), `TED-Ed` (`https://youtu.be/dO2xx-aeZ4w`, `2,795,894` views), `TED-Ed` (`https://youtu.be/de1hiS_XjWg`, `1,615,069` views), `TED-Ed` (`https://youtu.be/2njn71TqkjA`, `1,582,917` views), `TED-Ed` (`https://youtu.be/ztWHqUFJRTs`, `1,383,635` views), and `TED-Ed` (`https://youtu.be/fHztd6k5ZXY`, `1,378,649` views), plus `TED-Ed` (`https://youtu.be/5wVJeq4mLL0`, `670,049` views, *Whatever happened to the hole in the ozone layer?*).
  - Combined with `public_search.py`, `HOS:102` has **6 direct `≥1M`-view videos on CFCs and the ozone hole** (`Veritasium` `43.56M`, `Vox` `10.16M`, `Cleo Abram` `8.53M`, `Peekaboo Kidz` `4.28M`, `Seeker` `2.49M`, `Astrum Earth` `1.67M`) plus `TED-Ed` `5wVJeq4mLL0` (`670,049` views, `#1` GB search result for `"hole in the ozone layer"`).

### 2.3 Rule 26 Search Demand & Exact-Title Collision Check (`PASS`)
- `public_search.py` (`2026-11-13`) verifies:
  - Plain search phrases: `"hole in the ozone layer"` (`autocomplete = yes`), `"ozone layer"` (`autocomplete = yes`), `"ozone hole"` (`autocomplete = yes`).
  - Ranking videos: `Vox` `CaLOiGEDPJQ` (`10,161,545` views), `Cleo Abram` `yWgHx0HE8m8` (`8,528,291` views), `Peekaboo Kidz` `ckULkfv3Hb0` (`4,284,034` views), `Seeker` `0ZfBgjUnXIs` (`2,494,747` views), `Astrum Earth` `EmaQVbdd6Ko` (`1,673,345` views), `TED-Ed` `5wVJeq4mLL0` (`670,049` views).
  - Exact title collisions: **`0`** on Long Title A (`How Did We Find the Hole in the Ozone Layer?`, `44 chars`), Title B (`The Ozone Hole (Found by an Instrument From the 1950s)`, `54 chars`), Title C (`Hole in the Ozone Layer: How a 1950s Ground Instrument Found It`, `64 chars`), Short `S01` (`Is the Hole in the Ozone Layer Still There?`, `43 chars`, related autocomplete `"is there still a hole in the ozone layer"`), and Short `S02` (`Why Did a Satellite Miss the Ozone Hole?`, `40 chars`).

### 2.4 Corrected Analytics Comparison & Hypothesis Framing (`PASS`)
- `TOPIC.md` §1.1–§1.3 states exact snapshot timestamps (`2026-11-12T06:40:28.196Z` and `2026-11-13T06:40:29.166Z`), lifetime Studio read timestamp (`2026-11-12T07:07:54.728116+00:00`), numerator (`video.views`), and elapsed-day denominator (`max(daysBetween(publishedAt.slice(0, 10), snapshot.date), 1)`).
- Ranks all eligible public longs (`002` `2.9/d` on `12 Nov` / `2.8/d` on `13 Nov`, `004` `1.1/d`, `006` Willow `0.6/d` [`#3` on `12 Nov`] / `1.3/d` [`#2` on `13 Nov`] -> `005` Tied Arm `0.4/d` / `0.3/d`, `003` X-rays `0.1/d`, `001` Germs `0.1/d`, plus newly public `007` Vaccine `0.0/d` on `13 Nov`) and all `28` public Shorts consistently by `views/day`, keeping lifetime Studio metrics separate from rolling 28d YTA windows and disclosing `PFj6172YU4Q`'s `4`-day (`215 / 4 = 53.8/d`) and `5`-day (`216 / 5 = 43.2/d`) denominators.
- Explicitly frames title/retention patterns as hypotheses, marks `<10`-view long retention curves `UNKNOWN`, notes `003` X-rays and `001` Germs as plain questions that stalled at `41` and `44` impressions, and notes `105.30%` / `112.43%` Short avg viewed as consistent with replay rather than proof of an intentional seamless loop alone.

### 2.5 Proof-First `0:05–0:15` Apparatus Fit, 3-Way Thumbnails, & Unverified Claims Guardrail (`PASS`)
- **Proof-First `0:05–0:15` Apparatus (`Rule 10` & `Rule 30` `HOS-2026-11-E2`):** The ground-based **Dobson spectrophotometer** at Halley Bay and its falling October ozone strip-chart provide a tactile physical apparatus for `0:05–0:15`.
- **3-Way Thumbnails (`Rules 11, 12, 14`):** `Thumb A` (`MISSED BY SPACE` — Halley Bay Dobson spectrophotometer under purple-blue polar sky hole), `Thumb B` (`ONE SPRAY CAN` — Rule 14 bright 1950s kitchen/lab spray can & split ozone shield), and `Thumb C` (`1985 ALARM` — Antarctic globe cavity & plunging strip chart).
- **Unverified Historical & Scientific Claims Guardrail (`J2748` Correction 4):** All historical and scientific claims — especially the remembered NASA Nimbus-7 TOMS satellite data-processing/flagging story, Halley Bay Dobson spectrophotometer readings, Midgley c. 1930 synthesis details, Molina & Rowland 1974 catalytic numbers, and Montreal Protocol recovery dates — remain **explicitly marked UNVERIFIED** and are **NOT cleared for narration or Short opens** until primary quotes in `SOURCES.md` and the `facts` lane (`gemini-agy`) run when `HOS:102` enters an active HOS WIP slot under Rule G.

---

## 3. Deliverables & PR Handoff for Chief

1. **History of Science PR #576 (`macbook/J2775`, head `fbebf688`):** https://github.com/TheLaughingGod1986/history-of-science/pull/576
   - `02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole/11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` (`9.45 / 10` = `94.5 / 100`)
   - `02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole/11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md` (`GO` in `next_hos` under Rule G)
   - `02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole/TOPIC.md`, `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, `production-status.md`, `README.md`, `11_Upload-Package/evidence_2026-11-13_neighbours.json`, `11_Upload-Package/evidence_2026-11-13_public_search.json` (`check_all.sh` `ALL CHECKS PASS`).
2. **Orbit With Ben (`macbook/J2775`):**
   - `jobs/reviews/J2775/REVIEW.md` — This Rule-E topic go/no-go review report.
