# J3707 Chief Ruling — Condition Verified; Reopen J3125 to Unschedule `sY0PSQFxjp8`

- **Acting Chief:** `gemini` (elected acting Chief on Mac mini under 24 Nov 2026 chain `claude -> codex -> gemini -> grok`; verified via `chief_relay.py status` at `2026-11-25T12:26Z` before all protected actions: `claude` out of usage until `12:50:00Z`, `codex` down until `12:35:24Z`).
- **Verification job:** `J3707` (*Verify condition for J3125*, parked by `macbook` because that slot could not reach HOS Studio).
- **Parent job:** `J3125` (*HOS Vaccine test: 24 Nov feed gate and conditional 29 Nov readout*, `repo: hos`, `kind: studio`).
- **Ruling:** **CONDITION SATISFIED — REOPEN `J3125` AND CLOSE `J3707` AS `done`.**
- **Gate outcome:** **0 of 3 named controls reached 50% first-24-hour Shorts-feed share** (`Bks_JLId1ew` = **`8 / 23 = 34.8%`**; `Sq_lV89VMUs` and `fgsR8yAHr5s` permanently unavailable, not zero, with no post-hoc replacement substitution). Per standing HOS Chief rulings `7004764743`, `7005625193`, `J3188`, and Codex's `J3527` Chief ruling, the `28 Nov` Variolation test (`sY0PSQFxjp8`) is **NOT CLEARED**. `J3125` is reopened to execute the existing authorized unschedule of `sY0PSQFxjp8` by **Thu 26 Nov 2026 18:00 UTC**.
- **Scope & spend:** Read-only verification and Chief ruling only. Zero YouTube, Studio, Buffer, schedule, privacy, film-approval, or Ben-hold changes performed in `J3707`. Spend: **£0.00**. No public video played.

---

## 1. Exact Matching-Window Evidence (`2026-11-25T12:22Z–12:25Z`)

Read via HOS YouTube Studio (CDP `9460`, single `studio.youtube.com` tab reused via `scripts/cdp_tabs.py:reuse_page`), **Advanced mode** with `dimension=TRAFFIC_SOURCE_TYPE` and `time_period=since_publish,time_period_unit_nth_days,1` (**`First 24 hours`**, 0–24 hours axis), cross-checked against live YouTube Data API v3 & YouTube Analytics API v2 (`UCXp7HkBIl1LgaznXuZHJyRg`):

### A. Named `J3125` / `J3188` Cohort & Plants Reference

| Video ID | Role / Air Time (UTC) | Live Privacy (API `12:22Z`) | Matching Window Read (Studio Advanced Mode `First 24 hours`, `12:25Z`) | First-24h Feed Share | Gate Result |
|---|---|---|---|---|---|
| `Bks_JLId1ew` | **Named 21 Nov control** (006 v03 *How Do Plants Make Oxygen?*, `2026-11-21T11:30:11Z`) | `public`, `78` views (`79` Studio) | **`21–22 Nov 2026` (`First 24 hours`, `21 Nov 11:30 – 22 Nov 11:30`):** **Total `23` views** (`0:17` AVD, `131` impr, `1.5%` CTR) = **`YouTube search: 15`** (`65.2%`, `0:13` AVD) + **`Shorts feed: 8`** (`34.8%`, `0:29` AVD); no other rows (`15 + 8 = 23`). | **`8 / 23 = 34.8%`** | **NOT FED (< 50%)** |
| `Sq_lV89VMUs` | Named 20 Nov original (005 v04 Cuff) | `private`, `publishAt: null`, `0` views | Contained before airing (`J3188`). Permanently unavailable (not zero). | Unavailable | Unavailable |
| `fgsR8yAHr5s` | Named 22 Nov original (005 v04 Heart) | `private`, `publishAt: null`, `0` views | Contained before airing (`J3188`). Permanently unavailable (not zero). | Unavailable | Unavailable |
| `ChbsigHD5_o` | 18 Nov Plants 48 h reference (`2026-11-18T11:30:28Z`) | `public`, `5` views | Accepted from `J3226` (`20 Nov 11:59Z`, 48 h 29 m since-published): **`3` views** (`Direct/unknown 66.7%` [2], `YouTube search 33.3%` [1], `0` Shorts-feed views; `Shorts feed impressions` / `Stayed to watch` / `Audience retention` `Not enough data`; zero feed impressions NOT inferred). | `0 / 3` (`0%`, feed impr unavailable) | Accepted (`J3226`) |

*Separate context on `Bks_JLId1ew` (not used as the First-24h gate metric):* Studio `Since published` (`21 Nov 11:30 – 25 Nov 12:24`): `79` views (`YouTube search 82.3%`, `Shorts feed 17.7%`, `Direct or unknown 0.0%`). Live YTA API daily rows: `2026-11-21` `YT_SEARCH 15, SHORTS 8` (`23`); `2026-11-22` `YT_SEARCH 24, SHORTS 5, NO_LINK_OTHER 0` (`29`).

### B. Separate Non-Substituted Context (Ben-Approved v05 Replacements — NOT Admitted into Named Cohort)

Per `J3188` and Codex's `J3527` Chief ruling (*no replacement IDs admitted into the named cohort; do not change the cohort after observing outcomes*), these exact `First 24 hours` Advanced Mode reads (`2026-11-25T12:25Z`) are logged strictly as separate channel context and **do not substitute** for `Sq_lV89VMUs` / `fgsR8yAHr5s`:

- `l8bxm9L3zl8` (*How Does a Blood Pressure Cuff Work?*, 20 Nov `11:30:00Z`, `public`, `31` API views): `First 24 hours` (`20–21 Nov 2026`) = **`25` total views** (`Shorts feed: 15` [`60.0%`], `YouTube search: 9` [`36.0%`], `Other YouTube features: 1` [`4.0%`]).
- `el30-mHiH-0` (*How Does the Heart Pump Blood?*, 22 Nov `11:30:33Z`, `public`, `547` API views): `First 24 hours` (`22–23 Nov 2026`) = **`532` total views** (`Shorts feed: 477` [`89.7%`], `YouTube search: 50` [`9.4%`], `Other YouTube features: 4` [`0.8%`], `Direct or unknown: 1` [`0.2%`]).

*Note per `J3125`:* Blood controls are non-vaccine, not non-health; zero feed views do not establish zero feed impressions; no general health-topic penalty is proved here.

---

## 2. Live Vaccine Schedule & `008` Slot State (`2026-11-25T12:22Z`)

- `sY0PSQFxjp8` (*What Is Variolation?*): `private`, `publishAt: 2026-11-28T11:30:00Z`, `madeForKids: false`, `0` views; 3 scheduled Buffer posts in `00_Brand/Channel-Setup/social/hos/BUFFER_POSTS.json` (`instagram: 6b02943702479690922e8c8e`, `facebook: 6b029438d5eabfb8cc8c2cf2`, `tiktok: 6b029439d864a01105a3cbc9`); HOS `library.json` status `scheduled`.
- `jkUZpyO71lU` (*How Was Smallpox Eradicated?*): `private`, `publishAt: null`, `madeForKids: false`, `0` views; HOS `library.json` status `retired`.
- `wkyGOKepjeQ` (*What Is Variolation?* duplicate): `private`, `publishAt: null`, `madeForKids: false`, `0` views.
- `008` Lightning / Franklin (`History Of Science/02_Video-Projects/008_Lightning-Franklin/status.json`): Long `YqCWYlv_LCY` Private scheduled Thu 26 Nov 18:00 UK (not yet public); Short A `__UtUYdEUwg` Private scheduled Fri 27 Nov 11:30 UK; Short C `4sYTV_rQcqs` already Private scheduled Sun 29 Nov 11:30 UK (`J3500`, post-publish Related link check queued in `J3649`). `J3125` does not alter `008` slots.

---

## 3. Concrete Follow-Up Directed on Reopened `J3125`

1. **Reopen `J3125`** (now `open` for Mini `studio` execution, deadline **Thu 26 Nov 2026 18:00 UTC**).
2. **Recheck current Chief authority** before executing any YouTube/Buffer write.
3. **Execute existing standing authorization (`7004764743`, `7005625193`, `J3125`, `J3527`):**
   - Clear `publishAt` on **`sY0PSQFxjp8` ONLY**, leaving it **Private** (never delete, never modify any public video, never touch `jkUZpyO71lU` or `wkyGOKepjeQ` except confirming they remain Private with `publishAt: null`).
   - Cancel the 3 scheduled Buffer posts for `sY0PSQFxjp8` (`6b02943702479690922e8c8e`, `6b029438d5eabfb8cc8c2cf2`, `6b029439d864a01105a3cbc9`).
   - Update `00_Brand/Channel-Setup/social/hos/UPLOADS.json`, `00_Brand/Channel-Setup/social/hos/BUFFER_POSTS.json`, HOS `00_Brand/Channel-Setup/audits/shorts_open_library/library.json` (`sY0PSQFxjp8` -> `retired`), and `05_Analytics/LEARNINGS.md` **row 36** (not row 35) in the same job.
   - Record live API read-back (`privacyStatus: private`, `publishAt: null`, `madeForKids: false`), a cropped Studio receipt showing Private and no schedule date (no account name or email visible), applicable checks, and HOS desk + OWB studio thread reports.
4. **PR #1253:** Remains unmerged/superseded by Codex's `J3527` HOLD ruling and this `J3707` matching-window ruling.
