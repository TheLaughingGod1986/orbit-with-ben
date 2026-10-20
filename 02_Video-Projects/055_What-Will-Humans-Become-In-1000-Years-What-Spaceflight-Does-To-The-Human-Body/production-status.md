# Production Status — `055_What-Will-Humans-Become-In-1000-Years-What-Spaceflight-Does-To-The-Human-Body`

| Field | Value |
|-------|-------|
| Slug | `055_What-Will-Humans-Become-In-1000-Years-What-Spaceflight-Does-To-The-Human-Body` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-20_J0696.md` (scored 30/30 studio rubric, #1 of 5; direct hand-off from `054`) |
| Topic lock | **Pending Chief decision** (`J0696` parked for Chief: lock `055` *What Will Humans Become in 1,000 Years? What Spaceflight Does to the Human Body* or pick another candidate from `IDEAS_2026-10-20_J0696.md`) |
| Script draft | `01_Script/human_spaceflight_evolution_script_master_v00.md` (`v00` drafted 20 Oct 2026 in `J0696`; `1,318` spoken words / `1,342` reviewer words, ~`8.9 min`; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 95.6 / 100** (`1,342` reviewer words, ~`8.9 min`, 5 chapters, 8/8 structure gates, 0 warnings; parked for Chief topic lock & script review in `J0696`) |
| Sources | `01_Script/SOURCES.md` — 15 claim rows verified verbatim across 14 primary URLs (NASA Twins Study Science Release, FAQs & Gene Expression Release, Garrett-Bakelman et al. *Science* 2019 `PMID 30975860` & `PMID 32375154`, Leigh Gabel et al. *Scientific Reports* 2022 `PMID 35773442`, Neginhal & George `PMID 42729855`, Cary Zeitlin & Donald Hassler et al. *Science* 2013 `PMID 23723233` & `PMID 27662785` and *Science* 2014 `PMID 24324275`, NASA/GSFC Mars Fact Sheet, Xin Yi & Rasmus Nielsen et al. *Science* 2010 `PMID 20595611`, and LOC Name Authorities `n2014021948`, `no2011061555`, `n78095637`, `n50004587`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` 15 rows pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all 9 script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| Spend | `0` credits (no ElevenLabs, Vertex, or Flow calls) |

---

## 1. Script Review (`npm run review:script` on `v00`, `J0696`)

```text
> content-ops@0.1.0 review:script
> tsx scripts/review-script.ts --file ../02_Video-Projects/055_What-Will-Humans-Become-In-1000-Years-What-Spaceflight-Does-To-The-Human-Body/01_Script/human_spaceflight_evolution_script_master_v00.md

# human_spaceflight_evolution_script_master_v00.md

**Decision:** PASS · **Score:** 95.6 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1342 · Est. min: 8.9 · Chapters: 5

## Cold open excerpt

> Why Does Spaceflight Rewrite the Human Body, and What Will Humans Become in 1,000 Years? Look inside the International Space Station between March 2015 and March 2016, where astronaut Scott Kelly spent 340 days in orbit while his identical twin brother Mark Kelly stayed on Earth.

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```

---

## 2. Episode Gate (`npm run gate:episode` on `v00`, `J0696`)

`prebuild_vidiq` is intentionally left unsigned pending Chief's topic lock (`J0696` rule: *"No topic lock without Chief"*); all 9 remaining episode checks pass.

```text
> content-ops@0.1.0 gate:episode
> tsx scripts/gate-episode.ts --project ../02_Video-Projects/055_What-Will-Humans-Become-In-1000-Years-What-Spaceflight-Does-To-The-Human-Body --script ../02_Video-Projects/055_What-Will-Humans-Become-In-1000-Years-What-Spaceflight-Does-To-The-Human-Body/01_Script/human_spaceflight_evolution_script_master_v00.md

# Episode gate — 055_What-Will-Humans-Become-In-1000-Years-What-Spaceflight-Does-To-The-Human-Body

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/055_What-Will-Humans-Become-In-1000-Years-What-Spaceflight-Does-To-The-Human-Body |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/human_spaceflight_evolution_script_master_v00.md |
| script_review | OK | Script reviewer PASS 95.6/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 49% (19 words): "There's more to come after this, starting with how autonomous probes explore space. Subscribe so you don't miss it." |
| visual_must | OK | [VISUAL MUST] count 6 (need ≥4). |
| teach | OK | [TEACH] count 6 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 5 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.6/100** · PASS
```

---

## 3. Teach on Screen, Polish Pass & Per-Chapter Teaching Gate Counts (`v00`)

```text
Spoken words (excl title/brackets): 1318
DATA:             : 6
SCALE:            : 6
WHO:              : 10
WHEN:             : 6
FACT:             : 4
NUMBER OBJECT     : 6
[ORBIT ACTS:      : 2
[SUBSCRIBE BEAT]  : 1
[CHAPTER CARD:    : 5
[TEACH:           : 6
```
