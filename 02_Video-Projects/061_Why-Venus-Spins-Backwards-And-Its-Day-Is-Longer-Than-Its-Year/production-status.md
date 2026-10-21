# Production Status — 061 Why Venus Spins Backwards and Its Day Is Longer Than Its Year

**Current Stage:** Topic & Script Draft (`v01`) — Parked for Chief topic lock & script review (`J0789` / `J0802`)
**Working Title:** Why Does Venus Spin Backwards and Have a Day Longer Than Its Year?
**Alt Titles:**
1. Why Venus Spins Backwards and Its Day Is Longer Than Its Year
2. Why a Day on Venus Lasts Longer Than Its Year Around the Sun
**Target Air Window:** Week of 16–20 Nov 2026 (next long slot after `060`)
**Next-Video Hand-Off (`062`):** *Why NASA Launched a Spacecraft to a Giant Metal World — Asteroid 16 Psyche*

---

## Stage History

| Date | Stage | Agent | Status | Notes |
|---|---|---|---|---|
| 2026-10-21 | Topic & Ideas (`J0789`) | `gemini` | Parked for Chief | 5 candidates scored in `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-21_J0789.md`; #1 pick `061` Venus (`30/30` studio / `16/30` audit rubric; 4+ neighbours ≥ 1M views; direct hand-off from `060`). `PRE_BUILD_VIDIQ_AUDIT.md` drafted unsigned (no topic lock without Chief). |
| 2026-10-21 | Long Script `v00` & `SOURCES.md` (`J0789`) | `gemini` | Parked for Chief | `01_Script/venus_retrograde_script_master_v00.md` (`95.8/100 PASS`, `1,499` reviewer words, `10.0 min`, `5` chapters, `8/8` structure gates, `DATA: 6`, `SCALE: 6`, `WHO: 15`, `WHEN: 6`, `FACT: 4`, `NUMBER OBJECT: 6`). `01_Script/SOURCES.md` populated with 16 primary claim rows + verified verbatim quotes. |
| 2026-10-21 | Long Script `v01` & `SOURCES.md` (`J0802`) | `gemini` | Parked for Chief | Revised to `01_Script/venus_retrograde_script_master_v01.md` (synced to `01_Script/episode_script_draft_v01.md`, documented in `01_Script/SCRIPT_NOTES_v01.md`): tightened spoken word count from `1,434` to **`1,269` spoken words** (`1,290` reviewer words, `~8.6 min`, inside the `1,200–1,300` target), scoring **`95.8 / 100` PASS** (`8/8` structure gates, `10/10` hook, `10/10` scientificAccuracy, `10/10` escalation) with `DATA: 6`, `SCALE: 6`, `WHO: 16` (every chapter Ch 1–5 carries named scientists with `WHO:` cards), `WHEN: 6` (100% spoken-to-visual date match in every section), `FACT: 4`, `NUMBER OBJECT: 6`, and `LABEL: 6` (word-for-word VO match). |

---

## Pasted Gate Outputs (`2026-10-21`, `v01`)

### 1. `npm run review:script`

```text
> content-ops@0.1.0 review:script
> tsx scripts/review-script.ts --file ../02_Video-Projects/061_Why-Venus-Spins-Backwards-And-Its-Day-Is-Longer-Than-Its-Year/01_Script/venus_retrograde_script_master_v01.md

# venus_retrograde_script_master_v01.md

**Decision:** PASS · **Score:** 95.8 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1290 · Est. min: 8.6 · Chapters: 5

## Cold open excerpt

> Why Does Venus Spin Backwards and Have a Day Longer Than Its Year? Look from Venus orbit past the golden cloud horizon at Earth's twin — a rocky planet 12,104 kilometers across circling the Sun at 108.21 million kilometers. First observed in 1610 and probed by radar on March 8, 1

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

### 2. Marker Counts (`grep -o "<MARKER>:" | wc -l`)

```text
DATA: 6
SCALE: 6
WHO: 16
WHEN: 6
FACT: 4
NUMBER OBJECT: 6
LABEL: 6
```

### 3. `npm run gate:episode` (9/9 non-signoff checks OK; `prebuild_vidiq` unsigned pending Chief topic lock)

```text
> content-ops@0.1.0 gate:episode
> tsx scripts/gate-episode.ts --project ../02_Video-Projects/061_Why-Venus-Spins-Backwards-And-Its-Day-Is-Longer-Than-Its-Year --script ../02_Video-Projects/061_Why-Venus-Spins-Backwards-And-Its-Day-Is-Longer-Than-Its-Year/01_Script/venus_retrograde_script_master_v01.md

# Episode gate — 061_Why-Venus-Spins-Backwards-And-Its-Day-Is-Longer-Than-Its-Year

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/061_Why-Venus-Spins-Backwards-And-Its-Day-Is-Longer-Than-Its-Year |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/venus_retrograde_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 35% (19 words): "Orbit's already planning the next trip: NASA's mission to the metal asteroid Psyche. Subscribe if you want to come." |
| visual_must | OK | [VISUAL MUST] count 6 (need ≥4). |
| teach | OK | [TEACH] count 6 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 5 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```
