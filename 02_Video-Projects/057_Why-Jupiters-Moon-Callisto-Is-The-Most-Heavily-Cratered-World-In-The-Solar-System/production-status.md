# Production Status — `057_Why-Jupiters-Moon-Callisto-Is-The-Most-Heavily-Cratered-World-In-The-Solar-System`

| Field | Value |
|-------|-------|
| Slug | `057_Why-Jupiters-Moon-Callisto-Is-The-Most-Heavily-Cratered-World-In-The-Solar-System` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-20_J0727.md` (scored 30/30 studio rubric, #1 of 5; direct hand-off from `056`) |
| Topic lock | **Pending Chief decision** (`J0727` parked for Chief: lock `057` *Why Jupiter's Moon Callisto Is the Most Heavily Cratered World in the Solar System* or pick another candidate from `IDEAS_2026-10-20_J0727.md`) |
| Script draft | `01_Script/callisto_cratered_ocean_script_master_v00.md` (`v00` drafted 20 Oct 2026 in `J0727`; `1,303` spoken words / `1,386` reviewer words, ~`9.2 min`; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 95.8 / 100** (`1,386` reviewer words, ~`9.2 min`, 5 chapters, 8/8 structure gates, 0 warnings; parked for Chief topic lock & script review in `J0727`) |
| Sources | `01_Script/SOURCES.md` — 12 claim rows verified verbatim across 11 primary URLs (NASA Callisto Overview & Facts, NASA NSSDCA Galilean Satellite Fact Sheet, NASA Ganymede Facts, NASA Galileo Mission Overview, NASA Photojournal `PIA01400` / `PIA00516` / `PIA00484` / `PIA03456` / `PIA01478`, Anderson & Schubert et al. *Science* 1998 `PMID 9616114`, Khurana & Kivelson et al. *Nature* 1998 `PMID 9796812`, Carlson *Science* 1999 `PMID 9933159`, ESA/NASA JUICE Factsheet, and LOC Name Authorities `n79003254` for Galileo Galilei `1564–1642`, `n81077094` for Pierre-Simon Laplace `1749–1827`, `n83213689` for Margaret Kivelson `born 1928`, and `n79071955` for Robert W. Carlson `born 1941`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` 12 rows pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all 9 script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| Spend | `0` credits (no ElevenLabs, Vertex, or Flow calls) |

---

## 1. Script Review (`npm run review:script` on `v00`, `J0727`)

```text
> content-ops@0.1.0 review:script
> tsx scripts/review-script.ts --file ../02_Video-Projects/057_Why-Jupiters-Moon-Callisto-Is-The-Most-Heavily-Cratered-World-In-The-Solar-System/01_Script/callisto_cratered_ocean_script_master_v00.md

# callisto_cratered_ocean_script_master_v00.md

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

Words: 1386 · Est. min: 9.2 · Chapters: 5

## Cold open excerpt

> Why Is Jupiter's Moon Callisto the Most Heavily Cratered World in the Solar System, and How Does It Hide a Deep Ocean? Look out beyond Jupiter's horizon to the far orbit of its four great moons, 1,883,000 kilometers — or 1,170,000 miles — from the giant planet, where Callisto cir

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

---

## 2. Episode Gate (`npm run gate:episode` on `v00`, `J0727`)

`prebuild_vidiq` is intentionally left unsigned pending Chief's topic lock (`J0727` rule: *"No topic lock without Chief"*); all 9 remaining episode checks pass.

```text
> content-ops@0.1.0 gate:episode
> tsx scripts/gate-episode.ts --project ../02_Video-Projects/057_Why-Jupiters-Moon-Callisto-Is-The-Most-Heavily-Cratered-World-In-The-Solar-System --script ../02_Video-Projects/057_Why-Jupiters-Moon-Callisto-Is-The-Most-Heavily-Cratered-World-In-The-Solar-System/01_Script/callisto_cratered_ocean_script_master_v00.md

# Episode gate — 057_Why-Jupiters-Moon-Callisto-Is-The-Most-Heavily-Cratered-World-In-The-Solar-System

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/057_Why-Jupiters-Moon-Callisto-Is-The-Most-Heavily-Cratered-World-In-The-Solar-System |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/callisto_cratered_ocean_script_master_v00.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 34% (19 words): "Stay for the rest of this one, and subscribe for why magnetars are the most dangerous objects in space." |
| visual_must | OK | [VISUAL MUST] count 6 (need ≥4). |
| teach | OK | [TEACH] count 6 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 5 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```

---

## 3. Teach on Screen, Polish Pass & Per-Chapter Teaching Gate Counts (`v00`)

```text
Spoken words (excl title/brackets): 1303
DATA:             : 6
SCALE:            : 6
WHO:              : 7
WHEN:             : 6
FACT:             : 4
NUMBER OBJECT     : 6
[ORBIT ACTS:      : 2
[SUBSCRIBE BEAT]  : 1
[CHAPTER CARD:    : 5
[TEACH:           : 6
```
