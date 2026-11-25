# J3527 — Condition Verification for J3125 (HOS Vaccine Test: 24 Nov Feed Gate)

- **Reviewer:** `gemini` (specialist worker on Mac mini; fallback from `claude` out of usage until `2026-11-24T12:50:00Z`)
- **Elected Chief at check (`chief_relay.py status` at `2026-11-24T12:25Z`):** `codex` (`claude` returning `12:50:00Z`). Per `scripts/jobs.py` (`set_wait` / condition verification), only the Elected Chief records a condition verification (`reopen` or `wait --recheck`) and merges PRs. **This verification is parked for Elected Chief; zero YouTube, Studio, Buffer, schedule, or spend mutations were performed (`£0.00`).**
- **Parent job:** `J3125` (*HOS Vaccine test: 24 Nov feed gate and conditional 29 Nov readout*, `kind: studio`, `repo: hos`, `due: 2026-11-24T12:00:00Z`)
- **Waiting condition verified:** *"The 20-22 November comparison Shorts have aired and their day-1 traffic sources are available for the standing 24 November gate; Plants first-48-hour data must also be read."*
- **Observed (UTC):**
  - Live YouTube Data API v3 & YouTube Analytics API v2 (`UCXp7HkBIl1LgaznXuZHJyRg`): `2026-11-24T12:18Z`
  - Live HOS YouTube Studio (`hub_reach`, CDP `9460`, single `studio.youtube.com` tab reused via `scripts/cdp_tabs.py:reuse_page`): `2026-11-24T12:20Z`–`2026-11-24T12:22Z`
  - Daily snapshot: `05_Analytics/hos/snapshots/2026-11-24.json` (`takenAt: 2026-11-24T06:40:32.612Z`, `analytics.through: 2026-11-22`)
- **Recommendation to Elected Chief:** **CONDITION SATISFIED — merge this evidence PR, REOPEN `J3125` now, and close `J3527` as `done`** (with an explicit cohort ruling needed in `J3125` before the Thu 26 Nov 18:00 UTC deadline for `sY0PSQFxjp8`). See §4 for the alternative 25 Nov 12:00 UTC wait option if Elected Chief requires settled YTA `2026-11-22` daily rows before ruling.

---

## 1. Verification of Every Clause in `J3125`'s Waiting Condition

| Clause | Status | Verified Evidence |
|---|---|---|
| **24 Nov 12:00 UTC gate clock** | **MET** | Verified `2026-11-24T12:18Z`–`12:22Z` (past `2026-11-24T12:00:00Z`). |
| **Plants (`ChbsigHD5_o`, 18 Nov) first-48-hour data read** | **MET** | Already read & verified at `2026-11-20T11:59Z` (48 h 29 m elapsed) in `J3226`/`J3063` (`05_Analytics/hos/launch/ChbsigHD5_o.json`, `jobs/reviews/J3226/REVIEW.md`): **`3` views** (`Direct/unknown 66.7%` = 2, `YouTube search 33.3%` = 1, `0` Shorts-feed views; `Shorts feed impressions` / `Stayed to watch` / `Audience retention` `Not enough data`; zero feed impressions NOT inferred). Confirmed in settled YTA API (`2026-11-18..2026-11-21`): `2026-11-19` `NO_LINK_OTHER: 2`, `YT_SEARCH: 1` (`3` first-48h views, `0` `SHORTS`); `2026-11-21` `YT_SEARCH: 2` (`5` lifetime views, `0` `SHORTS`). |
| **Named 20 & 22 Nov controls (`Sq_lV89VMUs`, `fgsR8yAHr5s`)** | **PERMANENTLY UNAVAILABLE (`J3188`)** | Live Data API (`12:18Z`) confirms both remain `Private`, `publishAt: null`, `madeForKids: false`, `0` views (YTA `[]`). Per `J3188` cohort note on `J3125` (`2026-11-20T02:54Z`): both were contained before airing; their day-1 Shorts-feed numbers are permanently unavailable (not zero); do not silently substitute another video ID; the 24 Nov date gate and `sY0PSQFxjp8` schedule stay unchanged. |
| **Named 21 Nov control (`Bks_JLId1ew`) aired & day-1 traffic available** | **MET (with explicit YTA `2026-11-22` lag note)** | Live Data API (`12:18Z`): `public`, `publishedAt: 2026-11-21T11:30:11Z` (~72 h 50 m elapsed), `67` views (`68` in Studio at `12:20Z`). Studio `hub_reach` (`12:20Z`): `First 24 hours` (`21 Nov 11:30 – 22 Nov 11:30`) = **`23` views** (`9` unique viewers); `Since published` (`21 Nov 11:30 – 24 Nov 12:20`) = **`68` views** (`YouTube search 79.4%`, **`Shorts feed 20.6%`**, `Direct or unknown 0.0%`). Live YTA API (`12:18Z`) & `2026-11-24.json` (`06:40Z`): `2026-11-21` = **`YT_SEARCH: 15`, `SHORTS: 8`** (**`23` views = `34.8%` Shorts feed**, matching Studio's exact 23-view First 24 hours total; reported as `35%` in `05_Analytics/hos/REPORT.md`). **Explicit lag note:** YTA API channel daily rows currently end at `2026-11-21` (`[["2026-11-18",68],["2026-11-19",30],["2026-11-20",45],["2026-11-21",42]]`), so `2026-11-22` (the remaining ~3.5 UTC hours after Pacific midnight `08:00Z`) is not yet settled in YTA API. |
| **Original gates, Chief rulings & live schedules valid** | **MET** | Standing HOS Chief rulings `7004764743`, `7005625193`, receipt `7006171315`, merged OWB PR `#1039` (`6ed2896e`, `LEARNINGS.md` row 36), `J3126` (`done`, HOS PR `#665`), and `J3188` (`done`) all remain intact. Live Data API (`12:18Z`) confirms: `sY0PSQFxjp8` `Private`, `publishAt: 2026-11-28T11:30:00Z`, `madeForKids: false`, `0` views; `jkUZpyO71lU` `Private`, `publishAt: null`, `madeForKids: false`, `0` views; `wkyGOKepjeQ` `Private`, `publishAt: null`, `madeForKids: false`, `0` views. |

---

## 2. Exact Readback Table (Named Cohort + Non-Substituted Context)

### A. Named `J3125` / `J3188` Cohort & Plants Reference

| Video ID | Slot / Role | Live Privacy & Publish Time (API `12:18Z`) | Live Views (API / Studio) | First-24h / 48h Window Data | YTA API `day x trafficSource` (`12:18Z`, ends `2026-11-21`) | Studio `Since published` Traffic (`12:20Z`) |
|---|---|---|---|---|---|---|
| `Sq_lV89VMUs` | 20 Nov original (005 v04 Cuff) | `private`, `publishAt: null` (contained `J3188`) | `0` / — | Permanently unavailable (not zero; never aired) | `[]` | — |
| `Bks_JLId1ew` | **21 Nov control** (006 v03 Plants Oxygen) | `public`, `2026-11-21T11:30:11Z` | `67` / `68` | Studio `First 24 hours` (`21 Nov 11:30 – 22 Nov 11:30`): **`23` views** (`9` unique) | `2026-11-21`: `YT_SEARCH 15`, `SHORTS 8` (`23` views; **`34.8%` feed**); `2026-11-22` not yet in YTA | `YouTube search 79.4%`, **`Shorts feed 20.6%`**, `Direct/unknown 0.0%` |
| `fgsR8yAHr5s` | 22 Nov original (005 v04 Heart) | `private`, `publishAt: null` (contained `J3188`) | `0` / — | Permanently unavailable (not zero; never aired) | `[]` | — |
| `ChbsigHD5_o` | 18 Nov Plants reference (006 v02 Plants Air) | `public`, `2026-11-18T11:30:28Z` | `5` / — | `J3226` 48 h 29 m (`20 Nov 11:59Z`): `3` views (`Direct/unknown 66.7%` [2], `YouTube search 33.3%` [1], `0` feed; feed impr `Not enough data`) | `2026-11-19`: `NO_LINK_OTHER 2`, `YT_SEARCH 1`; `2026-11-21`: `YT_SEARCH 2` (`0` `SHORTS`) | — (see `J3226`) |

### B. Separate Non-Substituted Context: Ben-Approved v05 Replacements (`J3216`)

*Per `J3188`, these IDs are **NOT** substituted for `Sq_lV89VMUs` / `fgsR8yAHr5s` without an explicit Elected Chief ruling. They are reported separately because they actually aired in the 20 Nov & 22 Nov slots and directly inform whether HOS's Shorts feed is working channel-wide. Note per `J3125`: Blood controls are non-vaccine, not non-health; this cannot prove a general health-topic penalty.*

| Video ID | Slot / Film | Live Privacy & Publish Time (API `12:18Z`) | Live Views (API / Studio) | Studio `First 24 hours` (`12:20Z`) | YTA API `day x trafficSource` (`12:18Z`) | Studio `Since published` Traffic (`12:20Z`) |
|---|---|---|---|---|---|---|
| `l8bxm9L3zl8` | Fri 20 Nov `11:30Z` (005 s06 v05 Cuff; `J3216`, Ben OK `HOS-J3187.1`) | `public`, `2026-11-20T11:30:00Z` | `29` / `29` | **`25` views** (`9` unique) | `2026-11-20`: `SHORTS 15`, `YT_SEARCH 9`, `YT_OTHER_PAGE 1` (`60.0%` feed); `2026-11-21`: `YT_SEARCH 2` → 2-day `day1` = **`15 / 27 = 55.6%` feed** (complete) | **`Shorts feed 51.7%`**, `YouTube search 41.4%`, `Browse features 3.4%` |
| `el30-mHiH-0` | Sun 22 Nov `11:30Z` (005 s07 v05 Heart; `J3216`, Ben OK `HOS-J3187.2`) | `public`, `2026-11-22T11:30:33Z` | `541` / `543` | **`532` views** (earlier `J3383` 6 h read: `475 / 515 = 92.2%` feed) | `[]` (`2026-11-22..23` not yet settled in YTA) | **`Shorts feed 88.0%`**, `YouTube search 10.9%`, `Other YouTube features 0.7%` |

---

## 3. Additional State Relevant to `J3125` Execution

1. **Buffer state for `sY0PSQFxjp8` (`social/hos/BUFFER_POSTS.json`):** Because Sat 28 Nov `11:30Z` entered the 7-day Buffer mirror window, `BUFFER_POSTS.json` now contains scheduled Buffer posts recorded `2026-11-22T07:05Z` (`dueAt: 2026-11-28T11:30:00.000Z`, including Instagram post `6b02943702479690922e8c8e`, Facebook, etc.). If Elected Chief rules to unschedule `sY0PSQFxjp8` by Thu 26 Nov 18:00 UTC, `J3125` **must cancel those Buffer posts** and update `social/hos/UPLOADS.json`, `BUFFER_POSTS.json`, and HOS `library.json` in the same job.
2. **`008` Lightning / Franklin readiness for the Sun 29 Nov gap (`History Of Science/02_Video-Projects/008_Lightning-Franklin/status.json`):**
   - `008` Long (`hos_008_master_v05`) passed Ben's watch (`16 Nov`) and is packaged (`J3500`, awaiting Chief PR merge + Mini private upload/schedule for Thu 26 Nov 18:00 London). It is **NOT yet public**.
   - `008` Shorts A (`v04`, Ben OK `12 Nov`) and C (`v07`, Ben OK `18 Nov`) remain ineligible for 29 Nov until `008` Long is actually public on Thu 26 Nov.
3. **Why an Elected Chief cohort call is needed inside `J3125` before Thu 26 Nov 18:00 UTC:**
   - Under `J3188` applied strictly without substitution, the only aired named control (`Bks_JLId1ew`) is below 50% Shorts-feed share (`34.8%` YTA `2026-11-21`; `20.6%` Studio `Since published`), which would trigger unscheduling `sY0PSQFxjp8` by Thu 26 Nov 18:00 UTC.
   - Conversely, both Ben-approved v05 replacements that actually filled the 20 Nov and 22 Nov Blood slots (`l8bxm9L3zl8` `55.6%` settled YTA day-1 / `51.7%` Studio; `el30-mHiH-0` `88.0%` Studio / `92.2%` at 6 h, `532` first-24h views) exceeded 50% Shorts-feed share, indicating HOS Shorts-feed distribution is not shut off channel-wide.
   - Only Elected Chief can decide whether to (a) enforce `J3188` strictly and unschedule `sY0PSQFxjp8`, or (b) explicitly amend `J3188` to recognize `l8bxm9L3zl8`/`el30-mHiH-0` as the non-vaccine comparison controls and keep `sY0PSQFxjp8` scheduled for Sat 28 Nov `11:30:00Z` (queueing its 29 Nov `>11:30Z` 24 h readout).

---

## 4. Next Actions for Elected Chief (`codex` now / `claude` after `12:50Z`)

1. **Recommended path (reopen `J3125` now so the standing 24 Nov gate executes before the 26 Nov 18:00Z deadline):**
   - Merge this PR (`gemini/J3527`).
   - Run:
     ```bash
     python3 scripts/jobs.py reopen J3125 --agent <chief_id> --note "J3527 verified (PR #<num>): 24 Nov 12:00Z reached; ChbsigHD5_o 48h already read (J3226: 3v, 0 feed); Sq_lV89VMUs/fgsR8yAHr5s permanently Private/unscheduled (J3188); Bks_JLId1ew aired 21 Nov 11:30Z (Studio First-24h 23v, Since-published 68v / 20.6% feed; YTA 2026-11-21 8/23 = 34.8% feed, 2026-11-22 not yet in YTA). Separate non-substituted v05 replacements l8bxm9L3zl8 (55.6% YTA day-1) & el30-mHiH-0 (88.0% Studio, 532 First-24h v) surfaced for Chief cohort ruling before Thu 26 Nov 18:00Z." --git
     python3 scripts/jobs.py done J3527 --agent <chief_id> --result "Chief ruling: CONDITION SATISFIED (PR #<num> merged). J3125 reopened for standing 24 Nov gate and Chief cohort ruling before 26 Nov 18:00Z." --git
     ```
2. **Alternative path (only if Elected Chief requires settled YTA `2026-11-22` daily rows before reopening `J3125`):**
   - Merge this PR (`gemini/J3527`), record `jobs.py wait J3125 --agent <chief_id> --type input --recheck J3527 --check-at 2026-11-25T12:00:00Z --condition "YouTube Analytics API 2026-11-22 daily traffic-source rows settled for Bks_JLId1ew (and el30-mHiH-0 context)" --git`, and close `J3527` as `done`.
