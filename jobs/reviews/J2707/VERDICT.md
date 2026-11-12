# J2707: rule-E topic verdict for OWB 064 and 065

- Reviewer: macbook (Claude Code on the MacBook), 12 Nov 2026
- Evidence reviewed: PR #853 (branch `gemini/J2710`, commit `e23049fde7`), stacked on PR #850 (`a12f996f9`) and PR #849 (`7e168910d`)
- Spend: nothing

## Verdict

| Film | Verdict | Where it sits |
|---|---|---|
| OWB:064 Where Do Shooting Stars Come From? | **GO** | Stays in `jobs/WIP.json` `next` (rule G). No script job queued until an Orbit place frees up. |
| OWB:065 How Will the Space Station Fall to Earth? | **GO, with five facts to re-source before script lock** | Stays in `jobs/WIP.json` `next`, behind 064. |

Neither GO is a script lock, a production approval or a WIP promotion.

## What this review could and could not check

The MacBook run still has no web access (WebSearch and WebFetch were refused again on this run). So:

- **Not re-checked by me:** the YouTube view counts, the autocomplete results, the title-collision searches, and the NASA, NOAA and GAO quotes. They are J2710's readings from the Mini, taken on 12 Nov 2026, and I am relying on them as recorded.
- **Checked by me:** that the evidence files are complete and agree with each other, the repo overlap, the local analytics numbers quoted, the rule-E rubric, STUDIO_PLAYBOOK section 2, and whether the corrections the Chief asked for in the J2710 brief were made.

## Rule E rubric

### 1. No near-duplicate of a live or scheduled video

- **064: pass.** No long in `02_Video-Projects/` covers meteors or meteor showers (the nearest are 048 Ceres, 049 Bennu, 051 DART, all asteroid missions). The live Short `T9fVlG3CCzU` (What Are Shooting Stars Really Made Of?) is the Short-first lead-in, not a duplicate.
- **065: pass.** No long covers the ISS deorbit. The Short AR2 `xdurJQcoiGM` (Where Will the International Space Station Crash?) is scheduled for 25 Nov. The long's own two Shorts must stay different from it; J2710's two proposed angles do.

### 2. Audience evidence

- **064: pass.** `05_Analytics/owb/REPORT.md` confirms the Short: 1,284 views, 256.8 a day, 49.8% stayed (a WATCH read, not a pass). J2710 records "where do shooting stars come from" as the first YouTube suggestion and two videos ranking for it (2.55M and 1.10M views).
- **065: pass.** REPORT.md confirms the 16 Sunrises Short at 1,090 views, 90.8 a day. The working title's phrase returned no suggestions; "what will happen to the iss" did, with two ranking videos (2.76M and 1.65M).

### 3. Sourced facts

No script exists yet, so this applies at script lock. Both TOPIC.md files now carry an 11-row fact table with quotes and URLs. The 064 universal claim ("every shooting star is a sand-sized grain of comet dust") is struck through and replaced (TOPIC.md lines 78-81 and row F64.1). The 065 table separates the 2030/2031 plan from a guaranteed date (F65.6) and the South Pacific disposal area from the Point Nemo coordinate (F65.8), as the Chief asked.

## Neighbour pass (playbook section 2, step 2)

Both pass the three-video floor, but the "8 neighbours" headline in each file is more generous than the subject match supports.

- **064:** five of the eight are on the subject (shooting stars or meteors): 2.55M, 1.77M, 1.76M, 1.10M, 1.01M. Three of those five are children's channels, so the proven demand leans young. The other three are about comets or asteroids in general.
- **065:** two of the eight are on the subject (the end of the ISS): 2.76M and 1.65M. The next on-subject video is at 883K, just under the line. The other six are about the ISS in general (12.8M, 8.6M, 1.6M), re-entry (4.1M) or Point Nemo (1.57M, 1.12M). I count it a pass because the playbook asks for the same subject at about 1M, and the ISS is the subject; it is a thinner pass than 064.

The 94/100 and 92/100 scores are the evidence worker's own and played no part in this verdict.

## Carry into the script stage

**064**
- Open with the corrected line, never the universal one. The Geminids come from asteroid 3200 Phaethon.

**065: re-source these five before script lock (I could not confirm them from here)**
1. The GAO report number `GAO-26-107805` and its date, and the statement that NASA decides in 2027 whether to launch the deorbit vehicle in 2029.
2. The 57 m/s figure for the final burn.
3. Mir's mass: the table says 143 tons; the unit (US tons or tonnes) must be stated on screen and in the voiceover.
4. The station's mass: the table gives both 419,725 kg and "more than 430,000 kg". Pick one, with its source.
5. The alternative title "The Space Station Was Built to Last 15 Years": the 15-year design life needs its own source before the title is used.

**065 title:** the rule-26 phrase is "What Will Happen to the ISS?", not the working title. `status.json` still carries the working title; the title is decided at packaging.

## Left as is

- `status.json` topic state is still `todo` in both folders. I did not change it on this branch because PR #853 edits the same files; it should be set when the stack merges.
- Merge order for the Chief: #849, then #850 (this branch), then #853.
