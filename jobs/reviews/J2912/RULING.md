# Chief Review & Ruling: J2912 (`OWB: learn from our data, add two new films to the backlog`)

- **Date:** 2026-11-16T00:14Z
- **Reviewer:** Gemini (`gemini`, elected acting Chief; `claude` out of usage until `2026-11-16T07:50:00Z`, `chief` marked down until `2026-11-16T02:20:07Z`, `codex` marked down until `2026-11-17T23:22:00Z`)
- **Job:** `J2912` (`backlog: owb-ideas`, `kind: script`, `repo: owb`)
- **Verdict:** **SEND BACK / REOPEN & REROUTE TO MINI GEMINI ARGON (`needs: "mini"`, `mini_only: true`, `for: "gemini"`, `model: "gemini-argon"`)** — task deliverables are **NOT** complete yet (`0` files/branches written by `macbook`).

---

## 1. Evidence Reviewed

1. **Worker releases and block (`macbook`, `#6900937572`, `#6900978827`, `#6900999475`, `2026-11-15T20:32Z–20:38Z`):**
   - `macbook` (unattended Claude Code on the MacBook) claimed `J2912` twice because `J2912` was queued by `refill` with `needs: "any"` and no `mini_only` guard.
   - The unattended MacBook Claude Code lane refuses `WebSearch` and lacks `public_search.py` / `neighbours.py` and `git worktree add`, making the blocking neighbour pass (`studio/RULES.md` Lesson 1 & "Topic pick — neighbour pass": `>=3` education/space videos with `~1M+` views) and `LEARNINGS.md` Rule 26 search phrase verification impossible without inventing view counts.
   - Nothing was written: no data ranking file, no topic briefs (`02_Video-Projects/NNN_Slug/TOPIC.md`), no `jobs/WIP.json` `next` entries, no Rule-E review job, no branch or PR, and £0 / 0 credits spent.
   - `macbook` left reusable hand-back notes in `#6900978827` and `J2912` history (`2026-11-15T20:36Z`): next free OWB film numbers are **`070` and `071`**, and two non-overlapping candidates from the 15 Nov OWB data read (`2026-11-15.json` snapshot + `studio_ctr.json`) are *(a) Every Mars Rover Explained in 10 Minutes* (six-rover complete tour in `studio/plan.json`'s number-in-title format, backed by OWB's `#1` Shorts subject `RT-ec4_GcOk` `1,120` views in `20 h`, `iyvWYFP_ETA` `1,074` views, `B1z2dv7m7Vk` `52.69%` stayed, `025` long `4.84%` CTR) and *(b) Why Did NASA Crash Cassini Into Saturn?* + its spacecraft grand-finale / outer-planet missions tour recast (backed by real spacecraft footage winner `RT-ec4_GcOk` and Saturn `#2` long `55AEQwvs36g` `218` views).
2. **Current OWB numbering and open topic PRs:**
   - On `main`: `02_Video-Projects/001`–`064`, `068` (*How Long Is a Day on Mercury?*, GO `92/100` in `J2911` `1cd80884df`), `069` (*Landing on a Comet Rosetta 67P*, GO `94/100` in `J2911` `1cd80884df`), `J01`, and `_sleep_video_01` (`SLEEP01`).
   - Open PRs `#849`, `#850`, and `#853` (`J2703` / `J2707` / `J2710`) hold `064` (Shooting Stars) and `065` (Space Station Fall to Earth).
   - Open PRs `#901` and `#902` (`J2778` / `J2781`) hold `066` (*Why Do We Only See One Side of the Moon?*) and `067` (*What Would Happen If You Fell Into Neptune?*).
   - Therefore, the next free OWB film numbers for `J2912` are **`OWB:070` and `OWB:071`**.
3. **Alignment with Ben's 14 Nov 2026 Long-Video Plan (`studio/plan.json` & `J2864`):**
   - Under `studio/plan.json` (`longs-2026-11`, agreed by Ben on 14 Nov 2026), new single-question long videos (`"What happens if..."` / `"Why..."`) after the `034` Pluto film (`2026-12-13`) are paused from being locked, scripted, or built until one of the new long-format tests (`J01` Journey film on `8 Dec`, `SLEEP01` Sleep film on `12 Dec`, or `064` Every Planet Explained in 10 Minutes) has its 14-day result.
   - Backlog topic briefs (`TOPIC.md`, £0 spend) remain in `jobs/WIP.json` `next` (unlocked under Rule G) and must include both the search-led working title (`<=70` chars, Rule 26) + Rule 15 (`<=50` chars) title and how each topic works as or recasts into a multi-body / number-in-title complete-tour format per `studio/plan.json` (subordinate to `studio/plan.json` readout).

---

## 2. Ruling & Required Follow-Up Recorded on `J2912`

1. **Reopen and reroute `J2912` in place to Mini Gemini Argon (`needs: "mini"`, `mini_only: true`, `for: "gemini"`, `model: "gemini-argon"`):**
   - Keeping `J2912` as the live `backlog: "owb-ideas"` job prevents `refill.py` from spawning duplicate `owb-ideas` jobs while `J2912` is completed.
   - Setting `needs: "mini"` and `mini_only: true` keeps `J2912` on the Mini where free YouTube search (`public_search.py` / `neighbours.py`) and `jobs.py` work unattended, preventing another loop back to the restricted MacBook Claude lane.
2. **Deliverables required from the Mini `gemini` worker to close `J2912`:**
   - **Data pass:** Read `05_Analytics/owb/channel_daily.json`, `05_Analytics/owb/studio_ctr.json`, `05_Analytics/owb/REPORT.md`, the newest `05_Analytics/owb/snapshots/` (`2026-11-15.json`), `05_Analytics/weekly_audit/OWB_2026-11-14.md`, `05_Analytics/LEARNINGS.md` (rules 1–33), and `studio/plan.json`. Rank all public OWB longs and Shorts by views/day since publish, CTR, average % viewed, and Shorts stayed-to-watch, and write down the 3 best and 3 worst with exact numbers and shared patterns.
   - **Two new non-overlapping backlog topics (`OWB:070` and `OWB:071`):**
     - Do not repeat any topic in `02_Video-Projects/` (`001`–`064`, `068`–`069`, `J01`, `SLEEP01`), open PRs `#849`/`#853` (`064` Shooting Stars, `065` Space Station) or `#901`/`#902` (`066` Moon Far Side, `067` Fall Into Neptune), `00_Brand/Channel-Setup/ideas/`, `00_Brand/Channel-Setup/VIDEO_BACKLOG.json`, or `jobs/WIP.json`. (Worker may verify and use `macbook`'s `#6900978827` candidates — six-rover Mars tour `Every Mars Rover Explained in 10 Minutes` and `Why Did NASA Crash Cassini Into Saturn?` — or select another non-overlapping pair if search/neighbour checks require.)
     - Create `02_Video-Projects/070_<Slug>/` and `02_Video-Projects/071_<Slug>/` from `02_Video-Projects/_template_NNN_Episode-Slug/` with `TOPIC.md`, `status.json` (all stages `todo`), `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`, `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`, and saved `public_search.py` / `neighbours.py` evidence (`>=3` education/space videos with `~1M+` views per topic; £0 spend, no paid vidIQ).
     - In each `TOPIC.md`, include: (a) Rule 26 search-led working title (`<=70` chars) + Rule 15 (`<=50` chars) title plus its multi-body / number-in-title complete-tour format/recast per `studio/plan.json`, (b) one-line hook, (c) data justification citing past OWB winners and `LEARNINGS.md` rules, (d) blocking neighbour pass (`>=3` `1M+` education/space videos with video IDs, channels, and view counts), and (e) two `22–27 s` (`55–65` word) Short angles (`OWB-2026-11-E1` opening).
     - Append `OWB:070` and `OWB:071` to `jobs/WIP.json` `next` (Rule G waiting line only; unlocked while `studio/plan.json` pauses new single-question long builds after `034` Pluto on 13 Dec).
     - Queue one `kind: review` Rule-E topic go/no-go job (`--after J2912`) covering `OWB:070` and `OWB:071`, then close `J2912` with `jobs.py done J2912` naming both topics, the data line behind each, and the Rule-E review job ID.
   - **Guards:** £0 / 0 credits spent; no script lock, VO, or picture generation; no Studio or publish change; nothing for Ben.
