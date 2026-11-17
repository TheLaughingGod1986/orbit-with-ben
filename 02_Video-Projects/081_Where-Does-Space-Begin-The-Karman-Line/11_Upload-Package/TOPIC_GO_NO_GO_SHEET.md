# Topic Go/No-Go Sheet & Opportunity Score — `OWB:081`

- **Film:** `OWB:081` (`02_Video-Projects/081_Where-Does-Space-Begin-The-Karman-Line`)
- **Source Brief Job:** `J2974` (`macbook`, `2026-11-17`) · **Rule-E Review Job:** `J2978` (`gemini`, `2026-11-17`, [`jobs/reviews/J2978/REVIEW.md`](../../../jobs/reviews/J2978/REVIEW.md))
- **Status:** **GO (`96 / 100` in `J2978`; pre-cleared in `jobs/WIP.json` `next` with all 6 fixes applied, waiting on `studio/plan.json` format-test readout & Rule G slot)**
- **Primary Search-Led Title (`Rule 26`, `57 chars`):** `Where Does Space Begin? (The 100 km Kármán Line Explained)`
- **Autocomplete + Geocorona Twist Variant (`Rule 26`, `67 chars`):** `Where Does Space Begin? (And Why Earth's Air Reaches Past the Moon)`
- **Compact Search Question Variant (`Rule 15`, `41 chars`):** `Where Does Space Begin? (100 km vs 80 km)`
- **Contingency Complete-Tour Title (`studio/plan.json`, `56 chars`):** `Every Layer of Earth's Atmosphere Explained in 10 Minutes`
- **Evidence Files:** [`evidence_2026-11-17_public_search.json`](./evidence_2026-11-17_public_search.json), [`evidence_2026-11-17_neighbours.json`](./evidence_2026-11-17_neighbours.json), [`PRE_BUILD_VIDIQ_AUDIT.md`](./PRE_BUILD_VIDIQ_AUDIT.md), [`../TOPIC.md`](../TOPIC.md)

## Rule-E Gate Checklist (`J2974` / `J2978`)

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| **1. Data-First Ranking** | Ranks all `17` public OWB longs + `87` Shorts (`2026-11-17.json` & `studio_ctr.json`) | **PASS** | `TOPIC.md` §1.1 |
| **2. Non-Overlap** | Zero overlap with `02_Video-Projects/`, PRs `#849/#853/#901/#902`, `ideas/`, `WIP.json` | **PASS** | `0` existing films or idea briefs cover the `100-km` Kármán line vs `80.47-km` US boundary (`von Kármán 1957`, `McDowell 2018`), Earth's 5 atmospheric layers (`Troposphere` to `Exosphere`), or the `630,000-km` hydrogen `Geocorona` (`Baliukin et al. 2019`); distinct from `027` (`Earth Stopped Spinning`), `031` (`Magnetic Field Flips`), and `064` (`Shooting Stars`) |
| **3. Neighbour Gate (`≥3` at `1M+`)** | `≥3` education/space videos `≥1M` views in saved evidence; subject words only | **PASS** | `13` strictly on-topic `≥1M` videos in the main table (`1.02M–14.09M`), combining all `9` strictly on-topic `≥1M` education videos in `neighbours.json` (`Kurzgesagt` `14.09M`, Tier-1 `TED` Chris Hadfield `10.19M`, `CrashCourse` `2.82M`, `1.77M`, `1.10M`, Tier-1 `TED-Ed` `2.80M`, `1.79M`, `1.38M`, `1.38M`, with tangential/off-topic rows marked `onTopic: false`, `bigOnTopicCount: 9`) with `4` on-topic `≥1M` videos in `public_search.json` (`Seeker` `6.92M`, `Peekaboo Kidz` `3.86M`, `StarTalk` `1.76M`, `KINETIC SCHOOL` `1.02M`) |
| **4. Rule 26 Search + `studio/plan.json` Alignment** | Autocomplete phrase + ranking check + `studio/plan.json` contingency recast | **PASS** | `#1` exact autocomplete matches across all 3 core queries (`where does space begin`, `karman line explained`, `layers of the atmosphere`; `6.92M` & `485.5k` Seeker, `3.86M` Peekaboo Kidz, `1.76M` StarTalk, `1.02M` KINETIC SCHOOL, `478.1k` Astrum); includes `studio/plan.json` complete-tour contingency recast `Every Layer of Earth's Atmosphere Explained in 10 Minutes` |
| **5. Two `22–27 s` Short Angles (`E1` + Rule 6 Payoff Withholding)** | `24 s` (`60w` & `60w`), `t=0.0s` hook, `≤1.5s` surprise, `<1.2s` loop tail, `≥70%` payoff withholding, `0` collisions | **PASS** | `S01` *Why Does Space Officially Begin 100 Kilometres Above Earth?* (`59 chars`, `8-word` Sentence 1, `THE INTERNATIONAL KÁRMÁN LINE` mid-overlay matching VO, answer starts at `Above` = word `45/60 = 75.0% ≥ 70%` [`46/61 = 75.4%` hyphen-split]) & `S02` *How Far Into Space Does Earth's Atmosphere Actually Reach?* (`58 chars`, `8-word` Sentence 1, `FOUR HUNDRED KILOMETRES HIGH` mid-overlay matching VO, answer starts at `SOHO` = word `45/60 = 75.0% ≥ 70%` [`48/63 = 76.2%` hyphen-split]) |
