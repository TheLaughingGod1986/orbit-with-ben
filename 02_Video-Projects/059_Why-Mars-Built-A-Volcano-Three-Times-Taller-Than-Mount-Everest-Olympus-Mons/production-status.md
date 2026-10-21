# Production Status — `059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons`

| Field | Value |
|-------|-------|
| Slug | `059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-21_J0757.md` (scored 30/30 studio rubric, #1 of 5; direct hand-off from `058`) |
| Topic lock | **Pending Chief decision** (`J0757` parked for Chief: lock `059` *Why Mars Built a Volcano Three Times Taller Than Mount Everest — Olympus Mons* or pick another candidate from `IDEAS_2026-10-21_J0757.md`) |
| Script draft | `01_Script/olympus_mons_script_master_v00.md` (`v00` drafted 21 Oct 2026 in `J0757`, synced to `01_Script/episode_script_draft_v01.md`; `1,349` spoken words / `1,369` reviewer words, ~`9.1 min`; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 95.8 / 100** (`1,369` reviewer words, ~`9.1 min`, 5 chapters, 8/8 structure gates, 0 warnings; parked for Chief topic lock & script review in `J0757`) |
| Sources | `01_Script/SOURCES.md` — 16 claim rows verified verbatim across primary URLs (NASA Science Mars Facts `science.nasa.gov/mars/facts/`, NASA NSSDC Mars Fact Sheet `marsfact.html`, NASA Photojournal / Image Library `PIA00300` / `PIA25476` / `PIA26219` / `PIA24993` / `PIA22181` / `PIA15443` / `PIA09569`, Sjogren *Science* 1979 `PMID 17811123`, Smith & Zuber et al. *Science* 1999 `PMID 10348732` & `PMID 10506567`, Zuber, Solomon & Phillips et al. *Science* 2000 `PMID 10710301` & 2001 `PMID 11283367`, Neukum & Head et al. *Nature* 2004 `PMID 15616551` & 2005 `PMID 15772652`, and LOC Name Authorities `n85804243` for Giovanni Virginio Schiaparelli `1835–1910`, `n79082203` for Patrick Moore `1923–2012`, `no2007033781` for William L. Sjogren, `nb2012003006` for David E. Smith `born 1937`, `n91103960` for Maria T. Zuber `born 1958`, `nr93014292` for Sean C. Solomon `born 1945`, `n85352655` for Roger J. Phillips `1940–2020`, `n85125781` for Gerhard Neukum `1944–2014`, and `n84047812` for James W. Head `born 1941`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` 16 rows pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all 9 script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| Spend | `0` credits (no ElevenLabs, Vertex, or Flow calls) |

---

## 1. Script Review (`npm run review:script` on `v00`, `J0757`)

```text
> content-ops@0.1.0 review:script
> tsx scripts/review-script.ts --file ../02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/01_Script/olympus_mons_script_master_v00.md

# olympus_mons_script_master_v00.md

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

Words: 1369 · Est. min: 9.1 · Chapters: 5

## Cold open excerpt

> Why Did Mars Build a Volcano Three Times Taller Than Mount Everest? Look down from Mars orbit past the dusty horizon of our neighbor, where one shield volcano — Olympus Mons — rises so high into the thin red sky that its summit survives above planet-wide dust storms. Why did a wo

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

---

## 2. Episode Gate (`npm run gate:episode` on `v00`, `J0757`)

`prebuild_vidiq` is intentionally left unsigned pending Chief's topic lock (`J0757` rule: *"No topic lock without Chief"*); all 9 remaining episode checks pass.

```text
> content-ops@0.1.0 gate:episode
> tsx scripts/gate-episode.ts --project ../02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons --script ../02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/01_Script/olympus_mons_script_master_v00.md

# Episode gate — 059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/olympus_mons_script_master_v00.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 35% (18 words): "If you want the next one, why Hyperion looks like a sponge, subscribing is how you'll see it." |
| visual_must | OK | [VISUAL MUST] count 6 (need ≥4). |
| teach | OK | [TEACH] count 6 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 5 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```

---

## 3. Teach on Screen, Polish Pass & Per-Chapter Teaching Gate Counts (`v00`)

```text
Spoken words (excl title/brackets): 1349
DATA:             : 6
SCALE:            : 6
WHO:              : 9
WHEN:             : 6
FACT:             : 4
NUMBER OBJECT     : 6
[ORBIT ACTS:      : 2
[SUBSCRIBE BEAT]  : 1
[CHAPTER CARD:    : 5
[TEACH:           : 6
```
