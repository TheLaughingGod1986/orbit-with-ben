# Production Status — `059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons`

| Field | Value |
|-------|-------|
| Slug | `059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-21_J0757.md` (scored 30/30 studio rubric, #1 of 5; direct hand-off from `058`) |
| Topic lock | **Pending Chief decision** (`J0757` parked for Chief: lock `059` *Why Mars Built a Volcano Three Times Taller Than Mount Everest — Olympus Mons* or pick another candidate from `IDEAS_2026-10-21_J0757.md`) |
| Script draft | `01_Script/olympus_mons_script_master_v00.md` (`v00` drafted 21 Oct 2026 in `J0757`, synced to `01_Script/episode_script_draft_v01.md`; `1,349` spoken words / `1,369` reviewer words, ~`9.1 min`; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 95.8 / 100** (`1,369` reviewer words, ~`9.1 min`, 5 chapters, 8/8 structure gates, 0 warnings; parked for Chief topic lock & script review in `J0757`) |
| Sources | `01_Script/SOURCES.md` — **FIX / FLAG (`J1956`, 4 Nov 2026)**: formal Gemini `facts` pass (`01_Script/GEMINI_QUOTE_PASS_v01.md` & `jobs/reviews/J1956/GEMINI_SOURCES_VERIFICATION_2026-11-04.md`) audited all 16 rows (`78` subclaims: `50` `PASS`, `25` `FLAG`, `3` `UNVERIFIABLE`) plus all `22` NASA `PIA` assets; pre-audit snapshots preserved at `01_Script/SOURCES_v00_J0757.md` & `01_Script/SOURCES_v01_J0765.md`. Handed off to `J1957` (direct `MUST QUOTE` check) and `J1953` (elected-Chief editorial/lock owner). |
| Gemini facts pass | **Completed (`J1956`, 4 Nov 2026 — `FIX / FLAG` recorded in `01_Script/GEMINI_QUOTE_PASS_v01.md`)**; awaits `J1957` direct `MUST QUOTE` verification and `J1953` editorial revision + delta facts pass before any script lock |
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
