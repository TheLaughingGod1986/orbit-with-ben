# `J3214` — Rule-E Topic Go/No-Go Review: `HOS:125` (`What Causes the Tides? (Galileo Got It Wrong)`)

| Field | Value |
|---|---|
| **Job ID & Reviewer** | `J3214` · `macbook-2` (`review` lane) |
| **Target Proposal (`J3203`)** | **`HOS:125`** (`02_Video-Projects/125_Galileo-Newton-Laplace-What-Causes-The-Tides`) |
| **Source PRs (`J3203`)** | HOS PR [`#689`](https://github.com/TheLaughingGod1986/history-of-science/pull/689) (`claudecode/J3203`, commit `300c972e`) · OWB PR [`#1059`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1059) (`claudecode/J3203`) |
| **Review Deliverables (`J3214`)** | `jobs/reviews/J3214/REVIEW.md` (this file) · `jobs/reviews/J3214/evidence_2026-11-20_neighbours_125.json` · `jobs/reviews/J3214/evidence_2026-11-20_public_search_125.json` · companion HOS PR [`#692`](https://github.com/TheLaughingGod1986/history-of-science/pull/692) (`macbook/J3214`, commit `ce20e330`, isolated to `02_Video-Projects/125_Galileo-Newton-Laplace-What-Causes-The-Tides/` so it merges cleanly alongside `J3213` HOS PR `#690`; mirrored `17/17` SHA-256-verified files to `/Volumes/data/studio-live/History Of Science/02_Video-Projects/125_Galileo-Newton-Laplace-What-Causes-The-Tides`) |
| **Rule-E Verdict — `HOS:125` (What Causes the Tides?)** | **GO (`95.9 / 100` · `9.59 / 10` Opportunity Score)** — Stays in `jobs/WIP.json` `next_hos` under Rule G (`Title A`: `What Causes the Tides? (Galileo Got It Wrong)`, `45 chars ≤ 50 chars` Rule 15 & Rule 26; `Title B`: `Why Are There Two Tides a Day? Newton's Answer`, `46 chars ≤ 50 chars`; `Title C`: `What Causes the Tides? Why There Are Two a Day`, `46 chars ≤ 50 chars`; disambiguated `Short S01`: `Why Does the Moon Make Two Tides a Day?`, `39 chars`; `Short S02`: `What Did Galileo Get Wrong About the Tides?`, `43 chars`; `0` exact title collisions across all approved titles) |
| **Production & Claim Guard** | **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND.** Active `WIP.json["active"]` has `4 / 4` HOS slots full (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). Every historical fact, name, date, and number in `TOPIC.md` §2 and `PRE_BUILD_VIDIQ_AUDIT.md` is **UNVERIFIED** working memory and requires an exact primary-source quote in `SOURCES.md` verified by the `facts` lane (`gemini-agy`) when an active HOS WIP slot opens. |
| **Spend** | `£0.00` / `0` credits (no Studio or publish change) |

---

## 1. Executive Summary & Rulings on Writer-Flagged Points

`HOS:125` (`02_Video-Projects/125_Galileo-Newton-Laplace-What-Causes-The-Tides`, *What Causes the Tides? (Galileo Got It Wrong)*) queued by `J3203` (HOS PR [`#689`](https://github.com/TheLaughingGod1986/history-of-science/pull/689), OWB PR [`#1059`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1059)) passes all three prongs of the `AGENTS.md` Rule-E rubric and all 10 `STUDIO_PLAYBOOK.md` §2 topic gates with a **`95.9 / 100` (`9.59 / 10` Opportunity Score) GO** verdict, remaining in `jobs/WIP.json` `next_hos` under Rule G.

### 1.1 Ruling on Writer Flag 1: Four of Six `1M+` Neighbours Are Strictly on Tides — `PASS`
- Fresh signed-out YouTube GB `neighbours.py` run (`"what causes the tides"`, `"tides explained"`, `"how do tides work"`, `"why are there two tides a day"`): **`gate = PASS`**, **`bigCount = 6`**, **`hasTed = true`**.
- Auditing all six `≥1,000,000`-view education rows honestly:
  - **4 of 6 are strictly on tides** — independently exceeding the `≥3` education `1M+` threshold on pure tidal videos alone:
    1. **PBS Space Time** [`pwChk4S99i4`](https://youtu.be/pwChk4S99i4) — *What Physics Teachers Get Wrong About Tides!* (`2,133,852` views)
    2. **CrashCourse** [`KlWpFLfLFBI`](https://youtu.be/KlWpFLfLFBI) — *Tides: Crash Course Astronomy #8* (`2,005,260` views)
    3. **minutephysics** [`gftT3wHJGtg`](https://youtu.be/gftT3wHJGtg) — *The Tides* (`1,791,601` views)
    4. **minutephysics** [`mVJEi-PkkaY`](https://youtu.be/mVJEi-PkkaY) — *The Tides explained in ten seconds* (`1,050,894` views)
  - The remaining 2 `≥1M` rows in `neighbours.json` (`TED-Ed` *How tsunamis work* `Wx9vPv-T51I` `9.29M` and `TED-Ed` *How do ocean currents work?* `p4pWafuvdrY` `3.71M`) are broader oceanography and are **excluded** from the on-topic count.
  - **TED-Ed ★ Tier-1 on-topic presence confirmed:** `TED-Ed` [`mpRJhhbKLFc`](https://youtu.be/mpRJhhbKLFc) (*Why are there two tides a day? - Elise Cutts*, **`605,383`** views, `1 yr ago`) sits directly on the topic, alongside `Khan Academy` [`8sSCXJMUhsQ`](https://youtu.be/8sSCXJMUhsQ) (*Tides*, `22,137` views, `4 mo ago`).
  - Fresh `public_search.py` (`10` queries, `80` search results) adds **5 more direct on-tides `≥1M` ranking videos**: `StarTalk` `dBwNadry-TU` (`2,976,760`), `Waterlust` `bPhhYhN0FAc` (`2,501,261`), `AtomicSchool` `3RdkXs8BibE` (`2,061,645`), `BrainStuff` `5ohDG7RqQ9I` (`1,651,953`), and `NOAA SciJinks` `tcGEjzt_4is` (`1,112,100`) — giving **`9` distinct strictly on-topic tide videos above `1M` views**.

### 1.2 Ruling on Writer Flag 2: Overlap With `HOS:009` (Gravity) and Full Catalogue Check — `PASS (Zero Near-Duplicates)`
- Inspected all live/scheduled/active/backlog projects (`000–018`, `099`, `100–119`), open PRs (`120–124`), `VIDEO_BACKLOG.json`, `WIP.json`, and all `00_Brand/Channel-Setup/ideas/` folders (`011–095` plus `IDEAS_2026-10-*.md`). **Zero duplicates.**
- **Direct inspection of `HOS:009` (`02_Video-Projects/009_The-Falling-Moon-Gravity/01_Script/moon_script_master_v01.md`, 162 lines):**
  - `009` is the story of universal gravitation and orbits (Aristotle's two rules → Newton's 1665–1667 Woolsthorpe apple → orbital cannon → 60 Earth radii / 3,600× Moon test → Halley 1684 & *Principia* 1687 → Halley's comet 1758 → ISS free fall).
  - Tides appear in `009` for **half a sentence** in Part 05 (line 118: *"The Moon even pulls back on the Earth, and lifts the oceans into tides."* + line 112 visual plate). `009` never mentions Kepler (`1609`), Galileo (`1616`/`1632`), the Venetian barge, why there are two tides a day, horizontal/tractive tidal forces, Laplace (`1775–1776`), ocean-basin wave resonance, or Sir William Thomson / Kelvin (`1872`) and WWII tide-predicting machines.
  - `HOS:125` starts where `009` stops and forms a natural cluster sequel rather than a duplicate.
- Also confirmed clean separation from `HOS:124` (*Why Is the Ocean Salty?*, ocean salinity geochemistry & Earth's age clock), `HOS:101` (hydrothermal vents / chemosynthesis), and `ideas/031_Archimedes-Galileo-Buoyancy` (buoyancy / floating bodies).

### 1.3 Ruling on Writer Flag 3: Tidal Physics Traps, Fact Sourceability & Audit Fixes Applied — `PASS WITH SCRIPT GUARDRAILS`
All historical and scientific beats in `TOPIC.md` §2 can be sourced to primary literature (remaining explicitly **UNVERIFIED** until `SOURCES.md` records verbatim primary-source quotes and the `facts` lane verifies them):
- **Primary sources mapped for future `SOURCES.md`:** NOAA Ocean Service / Canadian Hydrographic Service (Bay of Fundy tidal range up to `~16 m` at Burntcoat Head, `24 h 50 min` lunar day, diurnal vs semidiurnal coasts, `~46%` solar tidal force share); Johannes Kepler, *Astronomia Nova* (`1609`, Introduction); Galileo Galilei, *Discorso sul flusso e il reflusso del mare* (`1616`) & *Dialogue Concerning the Two Chief World Systems* (`1632`, Fourth Day); Isaac Newton, *Principia* (`1687`, Book I Prop. 66 & Book III Prop. 24, 36, 37); Pierre-Simon Laplace, *Recherches sur plusieurs points du système du monde* (`1775–1776`, *Mémoires de l'Académie Royale des Sciences*); Sir William Thomson (Lord Kelvin), Edward Roberts & Alexander Légé (`1872–1873` tide-predicting machine, Science Museum / NTSLF Bidston Observatory) and Arthur Doodson (`1944` Normandy D-Day "Position Z" tidal predictions).

**Four concrete audit fixes logged for the script & Shorts stage (applied on HOS PR `#692`):**
1. **Disambiguated `Short S01` title collision (Never list compliance):** J3203's Short 1 title *Why Are There Two Tides a Day?* directly collides with live `TED-Ed` video [`mpRJhhbKLFc`](https://youtu.be/mpRJhhbKLFc) (*Why are there two tides a day? - Elise Cutts*, `605k` views; autocomplete even suggests `why are there two tides a day - elise cutts`) and `kXhXFKOL8PQ`. Replaced with **`Why Does the Moon Make Two Tides a Day?`** (`39` chars, **`0` exact collisions**). `Short S02` (*What Did Galileo Get Wrong About the Tides?*, `43` chars) also verified at **`0` exact collisions**. Both Shorts must follow the **19 Nov 2026 Shorts house rules** (`16–19 s`, premium 3D cartoon moving hero at Frame 0, concrete-fact caption line 1, seamless loop).
2. **Fix "Twice a day, everywhere" in `TOPIC.md` §2.1 Open:** Factually incorrect and contradicts the Laplace twist — diurnal coasts (e.g., parts of the Gulf of Mexico and South China Sea) have **one** high and one low tide per lunar day, and mixed coasts have two unequal highs. Script must say *"Twice a day on most coasts"* (never *"everywhere"*).
3. **Physics accuracy guardrail (horizontal tractive force + dynamic waves):** Never teach that the Moon lifts ocean water straight up against Earth's gravity (vertical tidal acceleration is only `~10^-7 g`) or use the flawed "centrifugal force flings water off the far side" shortcut. Explain Newton's equilibrium picture via the **differential horizontal (tractive) force** sliding water sideways toward opposite sides of Earth, then pivot directly to **Laplace's forced ocean-basin waves** (inertia, Coriolis deflection, basin depth, coastlines, and Fundy resonance).
4. **WHO-card year accuracy (`studio/RULES.md`):** William Thomson was knighted in `1866` and created **Baron Kelvin (Lord Kelvin) in `1892`**. In any `1872` scene, his WHO card must label him **Sir William Thomson (1824–1907) — Glasgow physicist** (never "Lord Kelvin" in 1872).

---

## 2. Rule-E Gate-by-Gate Audit Summary (`10 / 10 PASS`)

| # | Gate | Measured Evidence | Status |
|---:|---|---|---|
| 1 | Channel data ranking (`2026-11-20`) | `TOPIC.md` §1 benchmarks top/bottom 3 longs (`002` `1,139` showings, `004` `840` showings vs `005` `17`, `003` `40`) and Shorts (`xzKoHg0E0_U` `52/d`, `-3L6HzJ_d_4` `78.7%` stayed vs `LanTHJckYx8` `4v`) | **PASS** |
| 2 | Signed-out autocomplete (`Rule 26`) | `4/4` core phrases autocomplete `yes` (`what causes the tides`, `how do tides work`, `why are there two tides a day`, `tides explained`) | **PASS** |
| 3 | Ranking videos named (`Rule 26a`) | `5` direct `≥1M` ranking videos in `public_search.py` (`StarTalk` `2.98M`, `Waterlust` `2.50M`, `AtomicSchool` `2.06M`, `BrainStuff` `1.65M`, `NOAA` `1.11M`) | **PASS** |
| 4 | Neighbour gate (`STUDIO_PLAYBOOK` §2.4) | `neighbours.py` **PASS** (`bigCount = 6`, `4` strictly on tides `≥1M`, `hasTed = true`, `TED-Ed` on-topic `605k`) | **PASS** |
| 5 | No near-duplicate (`Rule E` #1) | Zero duplicates across `000–124` and all `ideas/`; `HOS:009` mentions tides in half a sentence only | **PASS** |
| 6 | Title rules & collisions (`Rule 15/26`) | `Title A` (`45c`), `Title B` (`46c`), `Title C` (`46c`), `Short S01` (`39c`, disambiguated), `Short S02` (`43c`) — `0` exact title collisions | **PASS** |
| 7 | HOS lane & proof-first open | `0:00–0:15` Bay of Fundy boats on mud → floating 6 h later (`Discovery. Wonder. Proof.`) | **PASS** |
| 8 | Two search-titled Shorts (`19 Nov` rules) | `S01` (`39c`) & `S02` (`43c`), `16–19 s`, 3D cartoon moving Frame 0, concrete-fact line-1 caption, seamless loop | **PASS** |
| 9 | Sourceability & unverified guard (`Rule E` #3) | All beats mapped to primary literature; physics & WHO-year guardrails logged; all claims explicitly **UNVERIFIED**; script template untouched | **PASS** |
| 10 | WIP cap & spend guard (`Rule G`) | `£0.00` spent; all `12` stages in `status.json` remain `"todo"`; waits in `next_hos` while `4/4` active HOS slots are full | **PASS** |

---

## 3. Five-Dimension Opportunity Score Summary (`9.59 / 10` = `95.9 / 100`)

| Dimension | Weight | Score (1–10) | Weighted | Key Evidence |
|---|---:|---:|---:|---|
| 1. Evergreen search intent | 25% | `9.7` | `2.425` | `4` GB autocomplete phrases + `9` distinct strictly on-tides videos `≥1M` across `neighbours.json` + `public_search.json` + `TED-Ed` ★ `605k` (`1 yr ago`) |
| 2. Competition gap | 20% | `9.4` | `1.880` | Top `1M+` videos are pure physics explainers; none tells the painted-3D `8.5–9 min` historical discovery story (Kepler `1609` → Galileo's `1616/1632` barge mistake → Newton `1687` → Laplace `1775–1776` → Thomson `1872` / D-Day `1944`) |
| 3. Narrative & visual arc | 20% | `9.6` | `1.920` | Proof-first Bay of Fundy harbour open, Venetian barge sloshing, horizontal tractive force + dynamic ocean-basin waves, brass harmonic machine; `4` `DATA + SCALE` moments |
| 4. Brand & guardrail fit | 20% | `9.7` | `1.940` | Classic HOS everyday phenomenon + famous genius proven wrong; all `3` long titles `≤50 chars` (`Rule 15` & `Rule 26`); `0` collisions after Short S01 disambiguation; clean separation from `009`/`124`/`ideas/031` |
| 5. Series / cluster potential | 15% | `9.5` | `1.425` | Anchors the Earth, Moon & Ocean Physics cluster linking `HOS:009` (Gravity), `HOS:124` (Ocean Salinity), `HOS:101` (Deep-Sea Vents), `HOS:103` (Sky Blue), and `HOS:108` (Slippery Ice) |
| **Total Opportunity Score** | **100%** | — | **`9.590 / 10` (`95.9 / 100`)** | **GO (Stays in `jobs/WIP.json` `next_hos` under Rule G)** |

---

## 4. Verification & Checks Run

- `00_Brand/Channel-Setup/tools/neighbours.py` (in HOS): **PASS** (`bigCount = 6`, `4` strictly on tides `≥1M`, `hasTed = true`, `gate = PASS`; saved in HOS PR `#692` and `jobs/reviews/J3214/evidence_2026-11-20_neighbours_125.json`).
- `00_Brand/Channel-Setup/tools/public_search.py` (in HOS): **PASS** (`10` queries, `80` results, `0` empty searches; saved in HOS PR `#692` and `jobs/reviews/J3214/evidence_2026-11-20_public_search_125.json`; `0` exact collisions across all approved long and Short titles).
- `python3 00_Brand/Channel-Setup/tools/status_board.py --check` (in HOS): **PASS** (`34 status files and BOARD.json are in order`).
- `00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/125_Galileo-Newton-Laplace-What-Causes-The-Tides` (in HOS): **all HOS 125 & repo tests PASS** (`durable desk handoffs` 28/28, `email ratchet` 8/8, `no media`, `status board`, `ElevenLabs guard` 11/11, `vo_check` 9/9, `atempo` 9/9, `contract tests` 28/28); the only failure in `package-lint` is the pre-existing `008_Lightning-Franklin` `[schedule.past]` on `main`, unrelated to `125`.
- NAS mirror parity: **`17 / 17` files** verified by SHA-256 (`0` mismatches) against `/Volumes/data/studio-live/History Of Science/02_Video-Projects/125_Galileo-Newton-Laplace-What-Causes-The-Tides`.
