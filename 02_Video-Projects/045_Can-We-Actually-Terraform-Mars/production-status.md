# Production status — 045 Can We Actually Terraform Mars, and Why Does Even a Robot Need Help?

| Field | Value |
|-------|-------|
| Slug | `045_Can-We-Actually-Terraform-Mars` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-18_J0545.md` (scored 19/30, #1 of 5; backlog id `017`) |
| Topic lock | **Pending Chief decision** (`J0545` parked for Chief: lock 045 Can We Actually Terraform Mars or pick #2 Enceladus Geysers / #3 Great Red Spot Shrinking / #4 Simulation Physics / #5 Ceres Salt Domes; confirm Short-first waiver) |
| Script draft | `01_Script/can_we_terraform_mars_script_master_v01.md` (v01 drafted 18 Oct 2026 in J0553, revised from v00 in J0545; 1,223 spoken words / 1,297 reviewer words, ~8.6 min; notes in `01_Script/SCRIPT_NOTES_v01.md`) |
| Script review | **PASS — 95.3 / 100** (1,223 spoken words / 1,297 reviewer words, ~8.6 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief script review in `J0553`) |
| Sources | `01_Script/SOURCES.md` — 13 rows updated to v01 and pre-checked with verbatim quotes (`NASA Mars Facts & Overview`, `NSSDCA Mars Fact Sheet`, `NASA Viking 1 & Mars Pathfinder`, `NASA MAVEN Solar Wind Release 2015`, `Hassler et al. 2014 Science / NASA NTRS 20240009831 & UNSCEAR 2008`, `NASA 2018 Terraforming Study / Jakosky & Edwards Nature Astronomy`, `NASA JPL MOXIE Completion Release 2023`, `NASA Enceladus`, `LOC Name Authority Records n79054677 / n79064998 / n79138780 / nb2017004412 / no2011091172`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA Curiosity `PIA17944`, Viking 1 & Mars Pathfinder `PIA00656`, MRO polar caps `PIA00409`, MAVEN ion-stripping, Perseverance MOXIE `PIA23886`, ESCAPADE + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,223 spoken words / 1,297 reviewer words, ~8.6 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`can_we_terraform_mars_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **5** (every named person in spoken narration at first mention: Thomas A. Mutch 1931–1980, Carl Sagan 1934–1996, Sojourner Truth 1799–1883, John Grunsfeld born 1958, Pam Melroy born 1961; verified in LOC Name Authority Records `n79054677`, `n79064998`, `n79138780`, `nb2017004412`, `no2011091172` and NASA Viking 1)
- `WHEN:` **7** (Hook: `4.5 billion years ago, 1976, 1997, 2015, 2018, 2023, 2027`; Ch 1: `July 20, 1976, January 1982, July 4, 1997, 13 minutes, 24.6 hours, 687 Earth days`; Ch 2: `4 billion years ago, 3.5 billion years ago, two weeks, November 5, 2015`; Ch 3: `20 years, July 2018`; Ch 4: `10 million years`; Ch 5: `2019, May 27, 2021, 10 hours, August 7, 2023`; Ch 6: `November 13, 2025, September 2027`)
- `FACT:` **4** (`Only inhabited by robots`, `Hundred grams per second`, `One point two percent`, `One hundred twenty-two grams`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"If this is your kind of question, subscribe. Next week is why Saturn's moon Enceladus shoots geysers into space."` (Line 3 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `040`–`044`; 19 words at 49%).
- **First 30 seconds rule (`OWB_2026-10-18.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~152 spoken words, ~1:00), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0553, 18 Oct 2026)

```text
# can_we_terraform_mars_script_master_v01.md

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

> Can We Actually Terraform Mars, and Why Does Even a Robot Need Help? Orbiting one hundred and forty-two million miles from the Sun, as you cross the rusty horizon of a cold, dry desert where atmospheric pressure is around zero point six percent of Earth's, can we actually terrafo

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0553, 18 Oct 2026)

```text
# Episode gate — 045_Can-We-Actually-Terraform-Mars

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/045_Can-We-Actually-Terraform-Mars |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/can_we_terraform_mars_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.3/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 49% (19 words): "If this is your kind of question, subscribe. Next week is why Saturn's moon Enceladus shoots geysers into space." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.3/100** · PASS
```
