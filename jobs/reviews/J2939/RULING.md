# Chief Review & Ruling: J2939 (`OWB: learn from our data, add two new films to the backlog`)

- **Date:** 2026-11-16T11:15Z
- **Reviewer:** Gemini (`gemini`, elected acting Chief; `claude` out of usage until `2026-11-16T12:50:00Z`, `chief` marked down until `2026-11-16T14:51:38Z`, `codex` marked down until `2026-11-17T23:22:00Z`)
- **Job:** `J2939` (`backlog: owb-ideas`, `kind: script`, `repo: owb`)
- **Verdict:** **SEND BACK / REOPEN & REROUTE TO MINI GEMINI ARGON (`needs: "mini"`, `mini_only: true`, `for: "gemini"`, `model: "gemini-argon"`)** — task deliverables are **NOT** complete yet (`0` files/branches written by `macbook`); **NO** to spending `vidIQ` search credits (`5` credits/call) on neighbour passes.

---

## 1. Evidence Reviewed

1. **Worker releases and block (`macbook`, studio thread `#954` comments `#6913174770`, `#6913219307`, `#6913248604`, `2026-11-16T09:54Z–09:59Z`):**
   - `J2939` (`backlog: owb-ideas`) was added by `refill.py` at `2026-11-16T09:53Z` with `needs: "any"` and `kind: "script"` (6 hours after `J2929` under `refill.py`'s `FALLBACK_MIN_H = 6.0` never-empty rule).
   - `macbook` (Slot 1 on the MacBook Pro) claimed `J2939` three times (`09:54Z`, `09:56Z`, `09:58Z`) before `chief_relay.py` on the Mini could reroute it, waking the MacBook's unattended Claude Code lane (`claude`).
   - On the unattended MacBook Claude Code lane, `CLAUDE_ALLOWED_TOOLS` refuses `WebSearch`, `WebFetch`, and `public_search.py` / `neighbours.py`, making the blocking neighbour pass (`studio/RULES.md` Lesson 1 & "Topic pick — neighbour pass": `>=3` education/space videos with `~1M+` views) and `LEARNINGS.md` Rule 26 search phrase verification impossible without inventing view counts.
   - Nothing was written: `0` files, `0` branches, `0` PRs, `0` `WIP.json` updates, `0` Rule-E review jobs, and `£0` / `0` credits spent.
   - `macbook` parked `J2939` for the Chief to choose between: (1) rerouting `J2939` to a lane with web access (`gemini` or `codex`) and keeping it off the MacBook Claude Code lane, or (2) ruling in writing that `vidIQ` connector search credits (`5` credits/call) may be spent for neighbour passes with a per-job cap.
2. **Ruling on `vidIQ` search credits vs free repo tools:**
   - **Ruling: NO to spending `vidIQ` search credits (`5` credits/call) on neighbour passes.** The `owb-ideas` brief (`jobs/backlog.json` line 100) and `AGENTS.md` require `£0` / `0` credits ("Spend nothing: existing subscriptions and free tools only, no paid API"). The repo's `00_Brand/Channel-Setup/tools/public_search.py` and `neighbours.py` tools (using the signed-out YouTube suggest API and `yt-dlp`) plus Gemini `agy`'s built-in web search provide deterministic autocomplete and `>=1M`-view neighbour verification at `0` credits and `£0.00` (as demonstrated in `J2912` for `OWB:070`/`071` and `J2929` for `OWB:072`/`073`).
3. **Current OWB numbering and open topic PRs (`2026-11-16T11:15Z`):**
   - On `main`: `02_Video-Projects/001`–`064` (`064` *Every Planet Explained in 10 Minutes*), `068` (*How Long Is a Day on Mercury?*, GO `92/100` in `J2911`), `069` (*Landing on a Comet Rosetta 67P*, GO `94/100` in `J2911`), `070` (*Every Mars Rover Explained in 10 Minutes*, GO `95/100` in `J2920`), `071` (*Why Did NASA Crash Cassini Into Saturn?*, GO `96/100` in `J2920`), `072` (*Every Dwarf Planet Explained in 10 Minutes*, GO `95/100` in `J2931`), `073` (*How the Soviets Landed on Venus*, GO `96/100` in `J2931`), `J01`, and `_sleep_video_01` (`SLEEP01`).
   - Open PRs `#849`, `#850`, and `#853` (`J2703` / `J2707` / `J2710`) hold `064` (Shooting Stars) and `065` (Space Station Fall to Earth).
   - Open PRs `#901` and `#902` (`J2778` / `J2781`) hold `066` (*Why Do We Only See One Side of the Moon?*) and `067` (*What Would Happen If You Fell Into Neptune?*).
   - Therefore, the next free OWB film numbers for `J2939` are **`OWB:074` and `OWB:075`**.
4. **Alignment with Ben's 14 Nov 2026 Long-Video Plan (`studio/plan.json` & `J2864`):**
   - Under `studio/plan.json` (`longs-2026-11`, agreed by Ben on 14 Nov 2026), new single-question long videos (`"What happens if..."` / `"Why..."`) after the `034` Pluto film (`2026-12-13`) are paused from being locked, scripted, or built until one of the new long-format tests (`J01` Journey film on `8 Dec`, `SLEEP01` Sleep film on `12 Dec`, or `064` Every Planet Explained in 10 Minutes) has its 14-day result.
   - Backlog topic briefs (`TOPIC.md`, `£0` spend) remain in `jobs/WIP.json` `next` (unlocked under Rule G) and must include both the search-led working title (`<=70` chars, Rule 26) + Rule 15 (`<=50` chars) title and how each topic works as or recasts into a multi-body / number-in-title complete-tour format per `studio/plan.json` (subordinate to `studio/plan.json` readout).

---

## 2. Ruling & Required Follow-Up Recorded on `J2939`

1. **Reopen and reroute `J2939` in place to Mini Gemini Argon (`needs: "mini"`, `mini_only: true`, `for: "gemini"`, `model: "gemini-argon"`):**
   - Keeping `J2939` as the live `backlog: "owb-ideas"` job prevents `refill.py` from spawning duplicate `owb-ideas` jobs while `J2939` is completed.
   - Setting `needs: "mini"` and `mini_only: true` (`macbook_portable == False`) keeps `J2939` on the Mini where free YouTube search (`public_search.py` / `neighbours.py`) and `jobs.py` work unattended, preventing another loop back to the restricted MacBook Claude Code lane.
2. **Deliverables required from the Mini `gemini` worker to close `J2939`:**
   - **Data pass:** Read `05_Analytics/owb/channel_daily.json`, today's refreshed `05_Analytics/owb/studio_ctr.json` (`17` OWB longs + `86` OWB Shorts from `J2932` `e44482bdc0`), `05_Analytics/owb/REPORT.md`, the newest `05_Analytics/owb/snapshots/` (`2026-11-16.json`), `05_Analytics/weekly_audit/OWB_2026-11-14.md`, `05_Analytics/LEARNINGS.md` (rules 1–33), and `studio/plan.json`. Rank all public OWB longs and Shorts by views/day since publish, CTR, average % viewed, and Shorts stayed-to-watch, and write down the 3 best and 3 worst with exact numbers and shared patterns.
   - **Two new non-overlapping backlog topics (`OWB:074` and `OWB:075`):**
     - Do not repeat any topic in `02_Video-Projects/` (`001`–`064`, `068`–`073`, `J01`, `SLEEP01`), open PRs `#849`/`#853` (`064` Shooting Stars, `065` Space Station) or `#901`/`#902` (`066` Moon Far Side, `067` Fall Into Neptune), `00_Brand/Channel-Setup/ideas/`, `00_Brand/Channel-Setup/VIDEO_BACKLOG.json`, or `jobs/WIP.json`.
     - Create `02_Video-Projects/074_<Slug>/` and `02_Video-Projects/075_<Slug>/` from `02_Video-Projects/_template_NNN_Episode-Slug/` with `TOPIC.md`, `status.json` (all stages `todo`), `README.md`, `production-status.md`, `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`, `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`, `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`, and saved `public_search.py` / `neighbours.py` evidence (`>=3` education/space videos with `~1M+` views per topic; `£0` spend, `0` `vidIQ` credits), and mirror both folders to `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/` with SHA-256 verification.
     - In each `TOPIC.md`, include: (a) Rule 26 search-led working title (`<=70` chars) + Rule 15 (`<=50` chars) title plus its multi-body / number-in-title complete-tour format/recast per `studio/plan.json`, (b) one-line hook, (c) data justification citing past OWB winners and `LEARNINGS.md` rules, (d) blocking neighbour pass (`>=3` `1M+` education/space videos with video IDs, channels, and view counts), and (e) two `22–27 s` (`55–65` word) Short angles (`OWB-2026-11-E1` opening, mid-Short stat overlay matching spoken VO word-for-word, payoff withheld until `>=70%` runtime).
     - Append `OWB:074` and `OWB:075` to `jobs/WIP.json` `next` (Rule G waiting line only; unlocked while `studio/plan.json` pauses new single-question long builds after `034` Pluto on 13 Dec).
     - Queue one `kind: review` Rule-E topic go/no-go job (`--after J2939`) covering `OWB:074` and `OWB:075`, then close `J2939` with `jobs.py done J2939` naming both topics, the data line behind each, and the Rule-E review job ID.
   - **Guards:** `£0` / `0` credits spent; no `vidIQ` search credits; no script lock, VO, or picture generation; no Studio or publish change; nothing for Ben.
