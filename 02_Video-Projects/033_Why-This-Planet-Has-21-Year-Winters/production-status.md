# Production status — 033 Why Knocked-Sideways Uranus Has 21-Year Winters

**Current ruling, 4 November 2026 (J2148, Rule-E review by `gemini`): GO — topic and script (`uranus_21_year_winter_script_master_v02.md`) LOCKED; VO job queued.** Supersedes the earlier Chief topic jobs (`J1896`, `J1969`, `J1970`) under `AGENTS.md` Rule E (WIP raised to 8, Ben 4 Nov 2026). Full review: `jobs/reviews/J2148/REVIEW.md`.

| Field | Value |
|-------|-------|
| Slug | `033_Why-This-Planet-Has-21-Year-Winters` |
| Working title (Rule 15, 47 chars) | `Why Knocked-Sideways Uranus Has 21-Year Winters` |
| Rule-18 real-imagery variants | `What Voyager 2 Saw in Just 6 Hours at Uranus` (44 chars) · `The Only Spacecraft Photos Ever Taken at Uranus` (47 chars) |
| Series (Rule 20) | `Real Worlds` |
| Rule-19 real-frame thumb (Concept A) | NASA/ESA/CSA JWST NIRCam real frame `PIA25770` (`STScI-01GWQ3`, 2023 sideways Uranus + vertical rings) or NASA/JPL Voyager 2 real frame `PIA18182` (24 Jan 1986), graded, hook `21-YEAR WINTER` |
| Gate | `npm run gate:episode` **PASS** (VO / Gemini Veo allowed) |
| Script review | `npm run review:script` **PASS 95.2 / 100** on locked `uranus_21_year_winter_script_master_v02.md` (1,290 spoken words / 1,347 reviewer words, ~9.0 min, 6 chapters; subscribe beat line 6 at 43%) |
| Sources | 15 / 15 MUST QUOTE rows **VERIFIED** live in `01_Script/SOURCES.md` + `01_Script/CLAUDE_QUOTE_CHECK_v01.md` |
| VO | **DONE** (`J2155` / `J2164` KEEP, `02_Voiceover/uranus_vo_v01.wav`, SHA-256 `3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460`, `611.40 s` / `10:11.4`, `-23.3 dB` mean, `-20.22 LUFS`, `-3.77 dBTP`; review: `jobs/reviews/J2164/REVIEW.md`) |
| Shot list | Open (`J2165`, cleared to start after `J2164` explicit VO acceptance) |
| CG | pending (Vertex Veo / Omni Orbit-only, after VO + shot list) |
| Runtime target | `10:11.4` (`611.40 s` locked VO from `1,290` spoken words) |
| Shorts | Standalone Short `ZpEA8stoSPA` (*Why Does Uranus Have 21-Year Winters?*) public 3 Nov 2026 — **461 views, 6 likes on day 1**; two new Shorts (incl. Test A opening Short) after master |

## Blockers

- [x] Topic lock + neighbour pass (10 education/space videos at 1.24M–7.63M views in `TOPIC_OPPORTUNITY_SCORE.md`) + Pre-build vidIQ signed (`J2148`)
- [x] Script v02 ≥ 90 (`review:script` PASS 95.2/100 on `uranus_21_year_winter_script_master_v02.md`, 1,290 spoken words)
- [x] Direct quote check on `01_Script/SOURCES.md` + `CLAUDE_QUOTE_CHECK_v01.md` (15/15 PASS)
- [x] VO take (`vo_take.py` from `uranus_21_year_winter_script_master_v02.md` — `uranus_vo_v01.wav`, `611.40 s`, accepted in `J2164` / `jobs/reviews/J2164/REVIEW.md`)
- [ ] Timed shot list + music brief (`J2165`)
- [ ] Stills locked before Veo/Omni spend

## `npm run review:script` & `npm run gate:episode` (J2148, 4 Nov 2026)

```
# uranus_21_year_winter_script_master_v02.md

**Decision:** PASS · **Score:** 95.2 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.1 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1347 · Est. min: 9 · Chapters: 6

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.2/100 — proceed to VO after production checklist.

Pass threshold: 90

# Episode gate — 033_Why-This-Planet-Has-21-Year-Winters

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /tmp/J2148-wt/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/uranus_21_year_winter_script_master_v02.md |
| script_review | OK | Script reviewer PASS 95.2/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 43% (17 words): "If you've enjoyed the ride so far, subscribing is the best way to help Orbit keep going." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.2/100** · PASS
```
