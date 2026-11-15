# Chief Review & Ruling: J2828 (`OWB: learn from our data, add two new films to the backlog`)

- **Date:** 2026-11-15T19:59Z
- **Reviewer:** Gemini (`gemini`, elected acting Chief; `claude` out of usage until `2026-11-15T21:50:00Z`, `chief` marked down until `2026-11-16T02:20:07Z`, `codex` marked down until `2026-11-17T23:22:00Z`)
- **Job:** `J2828` (`backlog: owb-ideas`, `kind: script`)
- **Submitted branch / PR:** `macbook/J2828` (`4d91d199e8c5d47339236014ec74c1a3b6539740`, PR #927, merged as `ecf937a00c` as the worker hand-back record only)
- **Verdict:** **SEND BACK / REOPEN & REROUTE TO MINI GEMINI ARGON (`mini_only: true`)** — task deliverables are **NOT** complete yet.

---

## 1. Evidence Reviewed

1. **Worker submission (`jobs/reviews/J2828/HANDBACK.md` in PR #927):**
   - `macbook-2` (unattended Claude Code on the MacBook) exited cleanly after recording an honest hand-back note.
   - No topics, project folders (`02_Video-Projects/NNN_Slug`), `jobs/WIP.json` `next` entries, or Rule-E review jobs were created because the unattended MacBook Claude lane refuses `WebSearch`, `vidIQ`, and `jobs.py` mutations, making the blocking neighbour pass (`studio/RULES.md` Lesson 1: `>=3` education/space videos with `~1M+` views) impossible from that lane.
2. **Current OWB numbering and open topic PRs:**
   - On `main`: `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes` (`OWB:064`) is already present and passed Rule-E review (`J2863` / `J2866` / `J2875`).
   - Open PRs `#849`, `#850`, and `#853` (`J2703` / `J2707` / `J2710`) hold the earlier `064` (Shooting Stars) and `065` (Space Station Fall to Earth) proposals.
   - Open PRs `#901` and `#902` (`J2778` / `J2781`) hold `066` (`Why Do We Only See One Side of the Moon?`) and `067` (`What Would Happen If You Fell Into Neptune?`).
   - Therefore, the next free OWB film numbers for `J2828` are **`068` and `069`**.
3. **Alignment with Ben's 14 Nov 2026 Long-Video Plan (`studio/plan.json` & `J2864`):**
   - Under `studio/plan.json` (`longs-2026-11`, agreed by Ben on 14 Nov 2026), new single-question long videos (`"What happens if..."` / `"Why..."`) after the `034` Pluto film (`2026-12-13`) are paused from being locked, scripted, or built until one of the new long-format tests (`064` Every Planet Explained in 10 Minutes or `SLEEP01` Sleep Film) has its 14-day result.
   - Backlog topic briefs (`TOPIC.md`, £0 spend) remain in `jobs/WIP.json` `next` (unlocked under Rule G) and should include both the search-led working title (Rule 26) and a concrete recast/multi-body/number-in-title tour option that fits the tested formats in `studio/plan.json`.

---

## 2. Ruling & Required Follow-Up on `J2828`

1. **PR #927 merged (`ecf937a00c`) as hand-back record only:** Preserves `jobs/reviews/J2828/HANDBACK.md` in git history and closes the open PR cleanly. This is **not** a topic PASS.
2. **Reopen and reroute `J2828` in place to Mini Gemini Argon (`needs: "mini"`, `for: "gemini"`, `model: "gemini-argon"`, `mini_only: true`):**
   - Keeping `J2828` as the live `backlog: "owb-ideas"` job prevents `refill.py` from spawning duplicate `owb-ideas` jobs while `J2828` is being completed.
   - Setting `mini_only: true` and `for: "gemini"` (`model: "gemini-argon"`) keeps `J2828` on the Mini where free YouTube search (`public_search.py` / `neighbours.py`) and `jobs.py` work unattended, preventing a fourth loop back to the restricted MacBook Claude lane.
3. **Deliverables required from the Mini `gemini` worker to close `J2828`:**
   - **Data pass:** Read `05_Analytics/owb/channel_daily.json`, `05_Analytics/owb/studio_ctr.json`, `05_Analytics/owb/REPORT.md`, `05_Analytics/owb/snapshots/2026-11-15.json`, `05_Analytics/weekly_audit/OWB_2026-11-14.md`, `05_Analytics/LEARNINGS.md` (rules 1–31), and `studio/plan.json`. Rank all public OWB longs and Shorts by views/day since publish, CTR, average % viewed, and Shorts stayed-to-watch, and write down the 3 best and 3 worst with exact numbers and shared patterns.
   - **Two new non-overlapping backlog topics (`OWB:068` and `OWB:069`):**
     - Do not repeat any topic in `02_Video-Projects/` (`001`–`064`, `J01`, `SLEEP01`), open PRs `#849`/`#853` (`064` Shooting Stars, `065` Space Station) or `#901`/`#902` (`066` Moon Far Side, `067` Fall Into Neptune), `00_Brand/Channel-Setup/ideas/`, or `jobs/WIP.json`.
     - Create `02_Video-Projects/068_<Slug>/` and `02_Video-Projects/069_<Slug>/` from `02_Video-Projects/_template_NNN_Episode-Slug/` with `TOPIC.md` and `status.json` (all stages `todo`).
     - In each `TOPIC.md`, include: (a) a search-led working title (`<=70` chars, Rule 26) plus its multi-body / number-in-title complete-tour recast option per `studio/plan.json`, (b) one-line hook, (c) data justification citing past OWB winners and `LEARNINGS.md` rules, (d) blocking neighbour pass (`>=3` education/space videos with `~1M+` views, with video IDs, channels, view counts, and saved `public_search.py` / `neighbours.py` evidence — £0, no paid vidIQ), and (e) two `22–27 s` Short angles (`55–65` words, Rule 31 / E1 opening).
     - Append `OWB:068` and `OWB:069` to `jobs/WIP.json` `next` (Rule G waiting line only; unlocked while `studio/plan.json` pauses new single-question long builds after `034` Pluto on 13 Dec).
     - Queue one `kind: review` Rule-E topic go/no-go job (`--after J2828`) covering `OWB:068` and `OWB:069`, then close `J2828` with `jobs.py done J2828` naming both topics, the data line behind each, and the Rule-E review job ID.
   - **Guards:** £0 / 0 credits spent; no script lock, VO, or picture generation; no Studio or publish change; nothing for Ben.
