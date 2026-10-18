# Production status — 043 Why Is the 330-Million-Light-Year Boötes Void Almost Empty?

| Field | Value |
|-------|-------|
| Slug | `043_Why-The-Bootes-Void-Is-Almost-Empty` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-18_J0514.md` (scored 19/30, #1 of 5) |
| Topic lock | **Pending Chief decision** (`J0514` parked for Chief: lock 043 Boötes Void or pick #2 Ganymede Bigger Than Mercury / #3 Terraform Mars / #4 Enceladus Geysers / #5 Andromeda Collision; confirm Short-first waiver) |
| Script draft | `01_Script/bootes_void_script_master_v01.md` (v01 drafted 18 Oct 2026 in J0522, revised from v00 in J0514; 1,200 spoken words / 1,284 reviewer words, ~8.6 min; notes in `01_Script/SCRIPT_NOTES_v01.md`) |
| Script review | **PASS — 95.3 / 100** (1,200 spoken words / 1,284 reviewer words, ~8.6 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief script review in `J0522`) |
| Sources | `01_Script/SOURCES.md` — 6 rows updated to v01 and pre-checked with verbatim quotes (`NASA Large-Scale Structures`, `NASA Dark Matter`, `NASA Dark Energy`, `NASA GSFC Blueshift Next Stop: Voids`, `NASA Hubble MCG+01-02-015 & Pisces A/B`, `NASA Roman Space Telescope Cosmic Voids`, `NASA Ganymede Facts`, `LOC Name Authority Records n83826725 / n88039663 / n84073001 / n81114174 / n85800131`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA Hubble Ultra Deep Field, MCG+01-02-015, Pisces A & B, Coma Cluster, Chandra/Hubble Bullet Cluster 1E 0657-56, WMAP CMB Cold Spot, Roman Space Telescope + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,200 spoken words / 1,284 reviewer words, ~8.6 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`bootes_void_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **5** (every named person in spoken narration at first mention: Fritz Zwicky 1898–1974, Vera Rubin 1928–2016, Georges Lemaître 1894–1966, Edwin Hubble 1889–1953, Nancy Grace Roman 1925–2018; verified in LOC Name Authority Records `n83826725`, `n88039663`, `n84073001`, `n81114174`, `n85800131`)
- `WHEN:` **7** (Hook: `1920s, 1960s, 1981, 330 million light-years`; Ch 1: `1933, 1970s, 20 million light-years, 300 million light-years, 1.4 billion light-years`; Ch 2: `less than 100 million years ago, 19 million light-years, 30 million light-years, 150 million light-years`; Ch 3: `8 minutes, 1981, 250 to 330 million light-years`; Ch 4: `1920s, 1927, 1929, 1960s`; Ch 5: `1998, 2006, 3.8 billion light-years, 6 to 10 billion light-years`; Ch 6: `1920s, 1933, 1981, 1998, 2006`)
- `FACT:` **4** (`One atom per cubic metre`, `Sixty galaxies instead of 2,000`, `No other galaxies until 1960s`, `Mapping 12,000 full moons`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"If you'd like more questions like this one, subscribing really helps a small channel."` (Line 9 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `039`–`042`; 14 words at 46%).
- **First 30 seconds rule (`OWB_2026-10-18.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~148 spoken words, ~0:59), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0522, 18 Oct 2026)

```text
# bootes_void_script_master_v01.md

**Decision:** PASS · **Score:** 95.3 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1284 · Est. min: 8.6 · Chapters: 6

## Cold open excerpt

> Why Is the 330-Million-Light-Year Boötes Void Almost Empty? High in the sky in the vicinity of the constellation Boötes, as you cross the horizon into a spherical expanse of intergalactic space up to three hundred and thirty million light-years across where two thousand galaxies 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0522, 18 Oct 2026)

```text
# Episode gate — 043_Why-The-Bootes-Void-Is-Almost-Empty

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/043_Why-The-Bootes-Void-Is-Almost-Empty |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/bootes_void_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.3/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 46% (14 words): "If you'd like more questions like this one, subscribing really helps a small channel." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.3/100** · PASS
```
