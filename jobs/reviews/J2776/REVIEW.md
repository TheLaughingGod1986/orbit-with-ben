# J2776 — Rule-E Topic Go/No-Go Review: `HOS:103` (*Why Is the Sky Blue? (And Why It Isn't Violet)*)

- **Date:** 13 November 2026 (`14:10 UTC`)
- **Job:** `J2776` (*HOS 103 Why Is the Sky Blue: rule-E topic go/no-go review*)
- **Dependency Verified:** `--after J2748` (`J2748` completed by `gemini` on the Mini at commit `34324bee` on HOS PR `#572` and `24cea34c0` on OWB PR `#881`)
- **Reviewer:** `macbook` (`Gemini 4 Argon (High)` / `gemini-argon`, Rule-E review lane)
- **Film Reviewed:** **`HOS:103`** — `02_Video-Projects/103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue` (*Why Is the Sky Blue? (And Why It Isn't Violet)*)
- **Deliverable PRs:**
  - **History of Science PR `#577`** (`https://github.com/TheLaughingGod1986/history-of-science/pull/577`, branch `macbook/J2776`, building on `J2748` HOS PR `#572`): adds `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` (`95/100`) and `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`, and updates `TOPIC.md`, `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, `production-status.md`, and `README.md` (`00_Brand/Channel-Setup/tools/check_all.sh` **ALL CHECKS PASS**).
  - **Orbit With Ben PR** (branch `macbook/J2776`, alongside `J2748` OWB PR `#881`): records this `jobs/reviews/J2776/REVIEW.md`.
- **Spend / Production / Studio:** **£0.00 / 0 credits.** No production work, spend, script lock, VO, or Studio change starts from this review job; active HOS WIP capacity (`4/4` under Rule G) and `facts`-lane gates stay unchanged.
- **Rule-E Verdict (Recorded for Chief Review):** **`GO` (`95 / 100` Opportunity Score — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G; Historical & Scientific Claims Explicitly Unverified Until `SOURCES.md` + `facts` Lane)**

---

## 1. Executive Summary & Rule-E Rubric Verdict

| Film ID & Folder | Primary Title A (`Rule 26` + `Rule 15`, `≤50` chars, `0` collisions) | Title B (`Rule 26` + `Rule 23` T&C, `≤70` chars, `0` collisions) | Title C (Story / Apparatus Alt, `≤50` chars, `0` collisions) | Verified `≥1M` Education Neighbours (`2026-11-13`) | Verified Plain Search Phrases & Ranking Videos (`2026-11-13`) | Opportunity Score | Rule-E Verdict (Under Rule G) |
|---|---|---|---|---|---|---:|---|
| **`HOS:103`**<br>`103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue` | `Why Is the Sky Blue? (And Why It Isn't Violet)` (**46 chars**) | `Why Is the Sky Blue? (The Glass Tube That Solved It)` (**52 chars**; or `Why Is the Sky Blue? (Tyndall's 1869 Glass Tube)`, **47 chars**) | `The 1869 Glass Tube That Put Blue Sky in a Bottle` (**49 chars**) | **`8` in `neighbours.py` (`PASS`, `TED-Ed = yes`)**, incl. **`3` direct sky/scattering explainers `≥1M`** (`Veritasium` `1.54M` `ro2MmmdARrs`, `minutephysics` `1.38M` `R5P6O0pDyMU`, `minutephysics` `1.36M` `NafbGOQBlQs`) + `Be Smart` `26.61M`, `Kurzgesagt` `9.99M`, `3Blue1Brown` `1.90M`, `TED-Ed` `1.82M` & `1.28M` | `"why is the sky blue"` (`autocomplete = yes`), `"rayleigh scattering"` (`autocomplete = yes`), `"why are sunsets red"` (`autocomplete = yes`); ranking videos `StarTalk` `UvmWxm3nR6E` (`3.39M`), `Netflix Jr.` `Ldm_9LsKblU` (`1.05M`), `NASA Space Place` `ehUIlhKhzDA` (`938k`) | **95 / 100** (`9.50 / 10`) | **`GO` (Wait in `next_hos` under Rule G; claims unverified until `SOURCES.md` + `facts` lane)** |

---

## 2. Detailed Verification Against `J2748` Ruling (`jobs/reviews/J2748/RULING.md`) & Rule-E Scope

### 2.1 Search Demand (`LEARNINGS.md` Rule 26) & Exact Title Collision Check — `PASS`
- **Saved Tool Evidence:** `02_Video-Projects/103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue/11_Upload-Package/evidence_2026-11-13_public_search.json` (retrieved `2026-11-13` via signed-out YouTube GB `public_search.py`).
- **Plain Search Phrases (`Rule 26a`):**
  - `"why is the sky blue"` → `autocomplete = yes` (`10` suggestions including `"why is the sky blue"`, `"why is the sky blue and sunsets red"`, `"why is the sky blue but space is black"`).
  - `"rayleigh scattering"` → `autocomplete = yes` (`10` suggestions including `"rayleigh scattering"`, `"rayleigh scattering experiment"`, `"rayleigh scattering law"`).
  - `"why are sunsets red"` → `autocomplete = yes`.
  - `"Why Is the Sky Blue? (And Why It Isn't Violet)"` → triggers related YouTube autocomplete `"why is the sky blue and not violet"`.
- **Two Ranking Videos for Plain Search Phrase `"why is the sky blue"` (`Rule 26a`):**
  1. `StarTalk` — *Neil deGrasse Tyson Explains Why The Sky Is Blue* (`https://youtu.be/UvmWxm3nR6E`, **`3,394,689` views**, retrieved `2026-11-13`).
  2. `Netflix Jr.` — *Why is the Sky Blue | Ask the Storybots | Netflix Jr* (`https://youtu.be/Ldm_9LsKblU`, **`1,050,550` views**, retrieved `2026-11-13`), alongside `NASA Space Place` *Why Is the Sky Blue?* (`https://youtu.be/ehUIlhKhzDA`, **`937,900` views`) and `Veritasium` *Why the Sky ISN'T Blue* (`https://youtu.be/ro2MmmdARrs`, **`1,536,981` views`).
- **Exact Title Collisions (`THUMBNAIL_AND_TITLE_RULES.md` §1.7 & `studio/RULES.md` Never List):**
  - **Bare titles rejected:** Bare `"Why Is the Sky Blue?"` (`4+` live collisions: `ehUIlhKhzDA`, `enKeTKon9NI`, `9mnlJdABRns`, `DiF64N8C0fs`), bare `"Why Isn't the Sky Violet?"` (`3` live collisions: `ChkF5oVeX6c`, `XzCi6GthoJk`, `0eK0pDs76Hw`), and bare `"Why Are Sunsets Red?"` (`1` live collision: `fxRzHYhgi4s`) are explicitly rejected.
  - **Disambiguated candidate titles (`0` exact collisions each):**
    - Long Title A: `Why Is the Sky Blue? (And Why It Isn't Violet)` (`46 chars`, **`0` exact collisions**)
    - Long Title B: `Why Is the Sky Blue? (The Glass Tube That Solved It)` (`52 chars`, **`0` exact collisions**)
    - Long Title C: `The 1869 Glass Tube That Put Blue Sky in a Bottle` (`49 chars`, **`0` exact collisions**)
    - Short `S01`: `Why Isn't the Sky Violet? (Rayleigh's Puzzle)` (`45 chars`, **`0` exact collisions**)
    - Short `S02`: `Why Are Sunsets Red? (Tyndall's 1869 Glass Tube)` (`48 chars`, **`0` exact collisions**)

### 2.2 Education Neighbour Pool (`STUDIO_PLAYBOOK.md` §2 Step 4) — `PASS`
- **Saved Tool Evidence:** `02_Video-Projects/103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue/11_Upload-Package/evidence_2026-11-13_neighbours.json` (`gate = PASS`, `bigCount = 8`, `hasTed = true`, `failedQueries = []`).
- **Direct On-Subject Education Videos (`≥1,000,000` views):**
  1. **Veritasium** (`https://youtu.be/ro2MmmdARrs`, **`1,536,981` views**, retrieved `2026-11-13`): *Why the Sky ISN'T Blue*
  2. **minutephysics** (`https://youtu.be/R5P6O0pDyMU`, **`1,382,559` views**, retrieved `2026-11-13`): *Why Isn't The Sky Purple?*
  3. **minutephysics** (`https://youtu.be/NafbGOQBlQs`, **`1,363,672` views**, retrieved `2026-11-13`): *Why is the Sun Yellow and the Sky Blue?*
- **Additional `≥1M`-View Light-Scattering & Optics Education Neighbours in `neighbours.py`:**
  4. **Be Smart** (`https://youtu.be/3g246c6Bv58`, **`26,613,295` views**): *Why Is Blue So Rare In Nature?* (`foundBy: "why the sky isn't blue"`)
  5. **Kurzgesagt – In a Nutshell** (`https://youtu.be/IXxZRZxafEQ`, **`9,990,176` views**): *What Is Light?*
  6. **3Blue1Brown** (`https://youtu.be/aXRTczANuIs`, **`1,900,703` views**): *How wiggling charges give rise to light*
  7. **TED-Ed ★** (`https://youtu.be/J1yIApZtLos`, **`1,816,004` views**): *Is light a particle or a wave? - Colm Kelleher*
  8. **TED-Ed ★** (`https://youtu.be/O0PawPSdk28`, **`1,275,823` views**): *Light waves, visible and invisible - Lucianne Walkowicz*
- **Subject-Only Tags (Zero Channel Names):** `why is the sky blue, why isn't the sky violet, rayleigh scattering, why are sunsets red, john tyndall blue sky experiment, lord rayleigh scattering, light scattering, cyanometer saussure`.

### 2.3 Non-Duplication Check (`02_Video-Projects/`, `ideas/`, `VIDEO_BACKLOG.json`, `jobs/WIP.json`) — `PASS`
- Verified across all existing HOS project folders (`000–013`, `099–102`), all idea folders (`011–095` & `IDEAS_*.md`), `VIDEO_BACKLOG.json`, and `jobs/WIP.json` (`active` & `next_hos`):
  - **Distinct from `HOS:006` (*The Willow Tree That Was Made of Air*):** `006` Part 05 covers **Nicolas-Théodore de Saussure (`1767–1845`)** and his `1804` quantitative plant gas-exchange balance (`Recherches chimiques sur la végétation`). `HOS:103` Act 1 covers his father **Horace-Bénédict de Saussure (`1740–1799`, *unverified*)** and his `c. 1789` Alpine **cyanometer** sky-blueness wheel.
  - **Distinct from `HOS:034` (*Foote, Tyndall & Arrhenius: The Greenhouse Effect*):** `034` covers John Tyndall's `1859` ratio spectrophotometer measuring invisible thermal-infrared absorption by $CO_2$ and water vapour (heat trapping). `HOS:103` covers Tyndall's `1869` visible-light scattering tube (the Tyndall effect / artificial blue sky and red sunset) and Lord Rayleigh's `1871`/`1899` $\lambda^{-4}$ scattering law.
  - **Distinct from `HOS:018` (*Herschel & Ritter: Invisible Light*), `HOS:025` (*Young, Fresnel & Einstein: Double-Slit*), and `HOS:087` (*Soap & Surface Tension*):** None covers atmospheric Rayleigh scattering or why the sky is blue.

### 2.4 Corrected Analytics Comparison & Hypotheses Guard (`J2748` Ruling #2–#3) — `PASS`
- `TOPIC.md` §1 explicitly states snapshot timestamps (`2026-11-12T06:40:28.196Z` and `2026-11-13T06:40:29.166Z`), lifetime Studio read timestamp (`2026-11-12T07:07:54.728116+00:00`), numerator (`video.views`), and elapsed-day formula (`ageDays = max(daysBetween(publishedAt.slice(0, 10), snapshot.date), 1)`).
- Ranks all eligible public longs (`002` `2.9/d` on `12 Nov` / `2.8/d` on `13 Nov`, `004` `1.1/d`, `006` Willow `0.6/d` [`#3`] / `1.3/d` [`#2`] vs bottom settled `003` X-rays `0.1/d`, `001` Germs `0.1/d`, `005` Tied Arm `0.4/d` / `0.3/d`, plus newly public `007` Vaccine `0.0/d` on `13 Nov`) and all `28` public Shorts consistently by `views/day`, with separate rankings by impressions, CTR, avg % viewed, and stayed-to-watch.
- Discloses the exact `PFj6172YU4Q` denominator (`215` views / `4` elapsed days = `53.8/day` on `12 Nov`; `216` views / `5` elapsed days = `43.2/day` on `13 Nov`).
- Explicitly frames title and retention observations as **hypotheses**, noting that `<10`-view long averages cannot establish a winning/losing retention format, `>100%` Short avg viewed is consistent with viewer replay rather than proof of an intentional loop alone, and plain-question titles `003` (`41` impr) and `001` (`44` impr) show that question syntax alone does not guarantee impressions.

### 2.5 Proof-First `0:05–0:15` Apparatus Fit & Two Search-Led Candidate Shorts — `PASS`
- **Proof-First `0:05–0:15` Apparatus (`Rule 10` & `Rule 30` `HOS-2026-11-E2`):** Tyndall's `1869` glass vapour tube on a darkened Royal Institution bench (white lamp beam entering → azure blue scattered light from the side → orange-red sunset beam out the far end) gives a concrete, silent-readable physical apparatus for the `0:05–0:15` window (`PRE_BUILD_VIDIQ_AUDIT.md` §6).
- **Two Collision-Free Search-Led Shorts (`TOPIC.md` §3 — Unverified Concepts Only):**
  1. **`S01`:** *Why Isn't the Sky Violet? (Rayleigh's Puzzle)* (`45 chars`, `0` collisions; pairs with `"why isn't the sky purple"` autocomplete).
  2. **`S02`:** *Why Are Sunsets Red? (Tyndall's 1869 Glass Tube)* (`48 chars`, `0` collisions; triggers `"why are sunsets red"` autocomplete).

### 2.6 Explicit Unverified Claims Guard & Rule G WIP Capacity — `PASS`
- All historical and scientific claims — including Horace-Bénédict de Saussure's cyanometer details, John Tyndall's `1869` vapour-tube reagents, Lord Rayleigh's `1871`/`1899` $\lambda^{-4}$ derivations, and the solar-spectrum / human-cone explanation for why the sky is not violet — remain **explicitly marked unverified** across `TOPIC.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, `TOPIC_OPPORTUNITY_SCORE.md`, `TOPIC_GO_NO_GO_SHEET.md`, and `production-status.md`.
- `01_Script/episode_script_draft_v01.md` remains the untouched blank template.
- Active HOS WIP remains at `4/4` (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). `HOS:103` remains in `jobs/WIP.json` `next_hos` (OWB PR `#881`) until an active HOS WIP slot opens, at which point `SOURCES.md` primary quotes and the `facts` lane must pass before any script lock, VO, or picture generation.
