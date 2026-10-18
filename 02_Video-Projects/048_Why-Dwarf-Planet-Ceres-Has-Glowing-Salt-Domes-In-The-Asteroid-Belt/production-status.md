# Production status — 048 Why Does Dwarf Planet Ceres Have Glowing Salt Domes in the Asteroid Belt?

| Field | Value |
|-------|-------|
| Slug | `048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-18_J0590.md` (scored 17/30, #1 of 5; direct hand-off from `047`) |
| Topic lock | **Pending Chief decision** (`J0590` parked for Chief: lock 048 Why Dwarf Planet Ceres Has Glowing Salt Domes in the Asteroid Belt or pick #2 Asteroid Bennu Sample Return / #3 Simulation Physics / #4 Self-Replicating AI Probes / #5 Humans in 1,000 Years; confirm Short-first waiver) |
| Script draft | `01_Script/ceres_salt_domes_script_master_v01.md` (v01 revised 18 Oct 2026 in J0598 from v00 in J0590; 1,239 spoken words / 1,297 reviewer words, ~8.6 min; notes in `01_Script/SCRIPT_NOTES_v01.md`) |
| Script review | **PASS — 95.3 / 100** (1,239 spoken words / 1,297 reviewer words, ~8.6 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief script review in `J0598`) |
| Sources | `01_Script/SOURCES.md` — 7 rows pre-checked with verbatim quotes (`NASA Science Ceres Facts`, `NASA Dawn Ceres Science & Highlights`, `NASA JPL Mystery Solved Brine Reservoir Release Aug 10, 2020 / Nature Astronomy, Nature Geoscience & Nature Communications`, `NASA Ceres Habitability Release Aug 20, 2025 / Courville et al. Science Advances`, `NASA Science 101955 Bennu Facts`, `LOC Name Authority Records n87803467 / n81114174 / n79083314`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA Dawn Occator Crater & Cerealia/Vinalia Faculae `PIA20350` / `PIA22660`, full-globe Ceres `PIA21906` / `PIA21079`, Ahuna Mons `PIA20348` / `PIA20915`, Ernutet Crater organics + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,239 spoken words / 1,297 reviewer words, ~8.6 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`ceres_salt_domes_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **3** (every named person in spoken narration at first mention: Giuseppe Piazzi 1746–1826, Edwin Hubble 1889–1953, William Herschel 1738–1822; verified in LOC Name Authority Records `n87803467`, `n81114174`, `n79083314`)
- `WHEN:` **7** (Hook: `22 minutes, 9 hours, 2015, hundreds of years, 2 billion years`; Ch 1: `1801, 2006, 4.5 billion years ago, 4 billion years ago, 1,682 Earth days, 4.6 Earth years, 9 hours`; Ch 2: `2003, 2004, 2012, 2013, 6 years, 2011, 2015`; Ch 3: `2017, October 2018, August 10, 2020, 20 million years ago, 2 million years old, hundreds of years`; Ch 4: `20 million years ago, a few million years`; Ch 5: `4.5-billion-year lifetime`; Ch 6: `October 2018, August 20, 2025, 0.5 billion to 2 billion years after formation, 2.5 billion to 4 billion years ago, October 20, 2020, September 24, 2023`)
- `FACT:` **4** (`One-thirteenth the radius`, `Three hundred bright features`, `Twenty-five miles deep`, `Three miles high`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"Orbit's already planning the next trip: why NASA sampled asteroid Bennu. Subscribe if you want to come."` (Line 5 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `044`–`047`; 17 words at 44%).
- **First 30 seconds rule (`OWB_2026-10-18.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~168 spoken words, ~1:07), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0598, 18 Oct 2026)

```text
# ceres_salt_domes_script_master_v01.md

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

Words: 1297 · Est. min: 8.6 · Chapters: 6

## Cold open excerpt

> Why Does Dwarf Planet Ceres Have Glowing Salt Domes in the Asteroid Belt? Orbiting two hundred and fifty-seven million miles from the Sun where sunlight takes twenty-two minutes to arrive and the largest object in the asteroid belt between Mars and Jupiter spins once every nine h

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0598, 18 Oct 2026)

```text
# Episode gate — 048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/ceres_salt_domes_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.3/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 44% (17 words): "Orbit's already planning the next trip: why NASA sampled asteroid Bennu. Subscribe if you want to come." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.3/100** · PASS
```
