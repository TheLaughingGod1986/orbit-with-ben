# Production Status — `054_Are-We-Living-Inside-A-Simulation-What-Physics-Actually-Says`

| Field | Value |
|-------|-------|
| Slug | `054_Are-We-Living-Inside-A-Simulation-What-Physics-Actually-Says` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-19_J0681.md` (scored 30/30 studio rubric, #1 of 5; direct hand-off from `053`) |
| Topic lock | **Pending Chief decision** (`J0681` / `J0689` parked for Chief: lock `054` *Are We Living Inside a Simulation? What Physics Actually Says* or pick another candidate from `IDEAS_2026-10-19_J0681.md`) |
| Script draft | `01_Script/simulation_hypothesis_script_master_v01.md` (`v01` revised 20 Oct 2026 in `J0689` from `v00`; `1,258` spoken words / `1,299` reviewer words, ~`8.7 min`; notes in `01_Script/SCRIPT_NOTES_v01.md`) |
| Script review | **PASS — 95.8 / 100** (`1,299` reviewer words, ~`8.7 min`, 5 chapters, 8/8 structure gates, 0 warnings; parked for Chief topic lock & script review in `J0689`) |
| Sources | `01_Script/SOURCES.md` — 16 claim rows verified verbatim across 14 primary URLs (*Philosophical Quarterly* `simulation-argument.com/simulation.html`, NIST 2022 CODATA `plkl` & `plkt`, Beane/Davoudi/Savage `arXiv:1210.1847` / *EPJA* 2014, Fermilab Holometer Release Dec. 3, 2015 & Chou et al. `arXiv:1512.01216` / *PRL* 2016, Ringel & Kovrizhin `arXiv:1704.03880` / *Science Advances* Sept. 2017 & Oxford/AAAS Oct. 3, 2017 release + HTTP-200 Wayback snapshot, Seth Lloyd `arXiv:quant-ph/9908043` / *Nature* 2000, and LOC Name Authority `n2001093242`, `n80038130`, `n50002729`, `n2005037741`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` 16 rows pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all 9 script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| Spend | `0` credits (no ElevenLabs, Vertex, or Flow calls) |

---

## 1. Script Review (`npm run review:script` on `v01`, `J0689`)

```text
> content-ops@0.1.0 review:script
> tsx scripts/review-script.ts --file ../02_Video-Projects/054_Are-We-Living-Inside-A-Simulation-What-Physics-Actually-Says/01_Script/simulation_hypothesis_script_master_v01.md

# simulation_hypothesis_script_master_v01.md

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

Words: 1299 · Est. min: 8.7 · Chapters: 5

## Cold open excerpt

> Why Do Physicists Say We Are Not Living Inside a Simulation? Look inside Fermilab's Holometer tunnel in Illinois in December 2015, where twin lasers searched for a hidden signal testing whether space — from a lab on Earth to a spacecraft in orbit — is made of digital pixels. Coul

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

---

## 2. Episode Gate (`npm run gate:episode` on `v01`, `J0689`)

`prebuild_vidiq` is intentionally left unsigned pending Chief's topic lock (`J0681` / `J0689` rule: *"No topic lock without Chief"*); all 9 remaining episode checks pass.

```text
> content-ops@0.1.0 gate:episode
> tsx scripts/gate-episode.ts --project ../02_Video-Projects/054_Are-We-Living-Inside-A-Simulation-What-Physics-Actually-Says --script ../02_Video-Projects/054_Are-We-Living-Inside-A-Simulation-What-Physics-Actually-Says/01_Script/simulation_hypothesis_script_master_v01.md

# Episode gate — 054_Are-We-Living-Inside-A-Simulation-What-Physics-Actually-Says

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/054_Are-We-Living-Inside-A-Simulation-What-Physics-Actually-Says |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/simulation_hypothesis_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 50% (19 words): "Orbit's already planning the next trip: what spaceflight does to the human body. Subscribe if you want to come." |
| visual_must | OK | [VISUAL MUST] count 6 (need ≥4). |
| teach | OK | [TEACH] count 6 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 5 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```

---

## 3. Teach on Screen, Polish Pass & Per-Chapter Teaching Gate Counts (`v01`)

```text
Spoken words (excl title/brackets): 1258
DATA:             : 6
SCALE:            : 6
WHO:              : 11
WHEN:             : 6
FACT:             : 4
NUMBER OBJECT     : 6
[ORBIT ACTS:      : 2
[SUBSCRIBE BEAT]  : 1
[CHAPTER CARD:    : 5
[TEACH:           : 6
```
