# Production Status — `058_What-Is-The-Most-Dangerous-Place-In-The-Universe-Inside-A-Magnetar-And-Quasar-Jet`

| Field | Value |
|-------|-------|
| Slug | `058_What-Is-The-Most-Dangerous-Place-In-The-Universe-Inside-A-Magnetar-And-Quasar-Jet` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-20_J0742.md` (scored 30/30 studio rubric, #1 of 5; backlog `011`; direct hand-off from `057`) |
| Topic lock | **Pending Chief decision** (`J0742` parked for Chief: lock `058` *What Is the Most Dangerous Place in the Universe? Inside a Magnetar and Quasar Jet* or pick another candidate from `IDEAS_2026-10-20_J0742.md`) |
| Script draft | `01_Script/magnetar_quasar_jet_script_master_v00.md` (`v00` drafted 20 Oct 2026 in `J0742`, synced to `01_Script/episode_script_draft_v01.md`; `1,351` spoken words / `1,424` reviewer words, ~`9.5 min`; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 95.8 / 100** (`1,424` reviewer words, ~`9.5 min`, 5 chapters, 8/8 structure gates, 0 warnings; parked for Chief topic lock & script review in `J0742`) |
| Sources | `01_Script/SOURCES.md` — 15 claim rows verified verbatim across primary URLs (NASA Black Hole Anatomy, NASA Photojournal / Image Library `PIA26274` / `PIA10711` / `PIA23863` / `PIA21085` / `PIA23122` / `PIA08617` / `PIA16114` / `7995525` / `27744663791_o`, Wachter & Kouveliotou et al. *Nature* 2008 `PMID 18509437`, Hurley & Duncan et al. *Nature* 2005 `PMID 15858565`, Palmer, Gehrels & Kouveliotou et al. *Nature* 2005 `PMID 15858567`, Gaensler & Kouveliotou et al. *Nature* 2005 `PMID 15858566`, Abbott et al. *Phys. Rev. Lett.* 2017 `PMID 29099225` & 2018 `PMID 30387654`, Hallinan & Kasliwal et al. *Science* 2017 `PMID 29038372` & `PMID 29038373`, Wu et al. *Nature* 2015 `PMID 25719667`, Bañados et al. *Nature* 2018 `PMID 29211709`, and LOC Name Authorities `n2002089927` for Robert C. Duncan `born 1942`, `no97025267` for Chryssa Kouveliotou `born 1953`, `n82219087` for Kevin Hurley, `no2008167446` for David M. Palmer `born 1962`, `n88118918` for Neil Gehrels `1952–2017`, `no2003008763` for Bryan M. Gaensler `born 1973`, `no2004050360` for Heber Doust Curtis `1872–1942`, and `no2011097247` for Maarten Schmidt `1929–2022`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` 15 rows pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all 9 script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| Spend | `0` credits (no ElevenLabs, Vertex, or Flow calls) |

---

## 1. Script Review (`npm run review:script` on `v00`, `J0742`)

```text
> content-ops@0.1.0 review:script
> tsx scripts/review-script.ts --file ../02_Video-Projects/058_What-Is-The-Most-Dangerous-Place-In-The-Universe-Inside-A-Magnetar-And-Quasar-Jet/01_Script/magnetar_quasar_jet_script_master_v00.md

# magnetar_quasar_jet_script_master_v00.md

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

Words: 1424 · Est. min: 9.5 · Chapters: 5

## Cold open excerpt

> Why Are Magnetars and Quasar Jets the Most Dangerous Places in the Universe? Look out beyond the far orbit and icy horizon of Jupiter's moon Callisto into the deep cosmos, where the crushed cores of dead stars and feeding supermassive black holes create danger that can strip atom

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

---

## 2. Episode Gate (`npm run gate:episode` on `v00`, `J0742`)

`prebuild_vidiq` is intentionally left unsigned pending Chief's topic lock (`J0742` rule: *"No topic lock without Chief"*); all 9 remaining episode checks pass.

```text
> content-ops@0.1.0 gate:episode
> tsx scripts/gate-episode.ts --project ../02_Video-Projects/058_What-Is-The-Most-Dangerous-Place-In-The-Universe-Inside-A-Magnetar-And-Quasar-Jet --script ../02_Video-Projects/058_What-Is-The-Most-Dangerous-Place-In-The-Universe-Inside-A-Magnetar-And-Quasar-Jet/01_Script/magnetar_quasar_jet_script_master_v00.md

# Episode gate — 058_What-Is-The-Most-Dangerous-Place-In-The-Universe-Inside-A-Magnetar-And-Quasar-Jet

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/058_What-Is-The-Most-Dangerous-Place-In-The-Universe-Inside-A-Magnetar-And-Quasar-Jet |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/magnetar_quasar_jet_script_master_v00.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 34% (18 words): "Every Sunday Orbit goes somewhere new. Subscribe and you'll be there for why Mars built a giant volcano." |
| visual_must | OK | [VISUAL MUST] count 6 (need ≥4). |
| teach | OK | [TEACH] count 6 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 5 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```

---

## 3. Teach on Screen, Polish Pass & Per-Chapter Teaching Gate Counts (`v00`)

```text
Spoken words (excl title/brackets): 1351
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
