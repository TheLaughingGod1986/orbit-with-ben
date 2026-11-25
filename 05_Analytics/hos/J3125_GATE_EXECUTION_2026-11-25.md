# HOS Vaccine Test Gate Execution Receipt — `J3125` (`2026-11-25`)

- **Executed:** `2026-11-25T12:35Z` – `2026-11-25T12:37Z` (£0.00, 0 credits)
- **Executor / Authority:** `gemini` (elected acting Chief on Mac mini under 24 Nov 2026 chain `claude -> codex -> gemini -> grok`; verified via `chief_relay.py status` at `2026-11-25T12:35:17Z` immediately prior to write)
- **Standing authorization:** HOS Chief rulings `7004764743` & `7005625193` (`J3122`), implementation receipt `7006171315`, cohort note `J3188`, Codex `J3527` Chief ruling, and `J3707` Acting Chief ruling (`jobs/reviews/J3707/CHIEF_DECISION.md`, OWB PR `#1320` `c2ad86f9e2`)
- **Channel verified:** History of Science (`@HistoryOfScienceYT`, `UCXp7HkBIl1LgaznXuZHJyRg`)

## 1. Gate Outcome Summary (`0 of 3` Named Controls `>= 50%`)

Exact matching-window data preserved from `jobs/reviews/J3707/CHIEF_DECISION.md` (`2026-11-25T12:25Z` Studio Advanced Mode `First 24 hours` & live API):

| Video ID | Role / Window | Exact Result | First-24h Feed Share | Gate Status |
|---|---|---|---|---|
| `Bks_JLId1ew` | Named 21 Nov control (006 v03 *How Do Plants Make Oxygen?*, aired `2026-11-21T11:30:11Z`) | `First 24 hours` (`21–22 Nov 2026`, `21 Nov 11:30 – 22 Nov 11:30`): **`23` total views** = `YouTube search: 15` (`65.2%`) + `Shorts feed: 8` (`34.8%`) | **`8 / 23 = 34.8%`** | **NOT FED (< 50%)** |
| `Sq_lV89VMUs` | Named 20 Nov original (005 v04 Cuff) | Contained before airing (`J3188`); `private`, `publishAt: null`, `0` views | Permanently unavailable (not zero) | Unavailable (no substitution) |
| `fgsR8yAHr5s` | Named 22 Nov original (005 v04 Heart) | Contained before airing (`J3188`); `private`, `publishAt: null`, `0` views | Permanently unavailable (not zero) | Unavailable (no substitution) |
| `ChbsigHD5_o` | 18 Nov Plants 48 h reference (aired `2026-11-18T11:30:28Z`) | `J3226` (`20 Nov 11:59Z`, 48 h 29 m): **`3` total views** (`Direct/unknown: 2`, `YouTube search: 1`, `Shorts feed: 0`; feed impressions `Not enough data`) | `0 / 3` (`0%`, feed impr unavailable) | Accepted (`J3226`) |

**Separate non-substituted context (not admitted into the named cohort per `J3188` & `J3527`):**
- `l8bxm9L3zl8` (20 Nov v05 Blood Pressure Cuff, `First 24 hours` `20–21 Nov`): `25` total views (`Shorts feed: 15` = `60.0%`, `YouTube search: 9`, `Other: 1`).
- `el30-mHiH-0` (22 Nov v05 Heart Pump, `First 24 hours` `22–23 Nov`): `532` total views (`Shorts feed: 477` = `89.7%`, `YouTube search: 50`, `Other: 4`, `Direct/unknown: 1`).

**Epistemic boundaries preserved:**
- Zero feed views do not establish zero feed impressions.
- Blood controls are non-vaccine, not non-health; this does not prove a general health-topic penalty.
- An association is not proof of algorithmic suppression.

## 2. YouTube API Unschedule & Read-Back (`sY0PSQFxjp8` ONLY)

Action: `PUT https://www.googleapis.com/youtube/v3/videos?part=status` on `sY0PSQFxjp8` (`privacyStatus: "private"`, `selfDeclaredMadeForKids: false`, `embeddable: true`, `license: "youtube"`, `publicStatsViewable: true`, omitting `publishAt`). HTTP `200 OK`. No public upload modified; no video deleted; no re-upload.

Live YouTube Data API v3 read-back at **`2026-11-25T12:36:34.475Z`** (channel `UCXp7HkBIl1LgaznXuZHJyRg`):

| Video ID | Title | `privacyStatus` | `publishAt` | `selfDeclaredMadeForKids` / `madeForKids` | Views | Action Taken |
|---|---|---|---|---|---:|---|
| `sY0PSQFxjp8` | What Is Variolation? | `private` | `null` (was `2026-11-28T11:30:00Z`) | `false` / `false` | `0` | **Unscheduled** (upload kept) |
| `jkUZpyO71lU` | How Was Smallpox Eradicated? | `private` | `null` | `false` / `false` | `0` | Verified untouched |
| `wkyGOKepjeQ` | What Is Variolation? (duplicate) | `private` | `null` | `false` / `false` | `0` | Verified untouched |

**Studio verification (CDP `9460`, `https://studio.youtube.com/video/sY0PSQFxjp8/edit`):**
- Visibility displays **`Private`** (padlock icon, no scheduled date).
- Audience confirmed **`Not made for kids`** (`notMfkChecked: true`, `mfkChecked: false`).
- Cropped Studio receipt (excluding top bar, account name, avatar, and email) attached to HOS desk PR `#180` report.

## 3. Buffer Cancellation & Read-Back (`BUFFER_HOS_API_KEY`)

Cancelled all 3 scheduled Buffer posts for `sY0PSQFxjp8` at **`2026-11-25T12:36:55.109Z`** and verified via `getPostStatus`:

| Network | Buffer Post ID | Pre-Cancel Status | Post-Cancel `getPostStatus` |
|---|---|---|---|
| Instagram | `6b02943702479690922e8c8e` | `scheduled` | `null` (deleted) |
| Facebook | `6b029438d5eabfb8cc8c2cf2` | `scheduled` | `null` (deleted) |
| TikTok | `6b029439d864a01105a3cbc9` | `scheduled` | `null` (deleted) |

## 4. Registry, Library, `LEARNINGS.md` & `008` Readiness

- **OWB `00_Brand/Channel-Setup/social/hos/UPLOADS.json`:** `sY0PSQFxjp8` updated to `privacyStatus: "private"`, `publishAt: null`, `unscheduledAt: "2026-11-25T12:36:34Z"`, do-not-Buffer note.
- **OWB `00_Brand/Channel-Setup/social/hos/BUFFER_POSTS.json`:** `sY0PSQFxjp8` entry removed following cancellation of all 3 posts.
- **OWB `05_Analytics/LEARNINGS.md`:** **Row 36** updated (row 35 untouched).
- **HOS `00_Brand/Channel-Setup/audits/shorts_open_library/library.json`:** `sY0PSQFxjp8` status set to `retired` via `gate_shorts_open.py status`.
- **HOS `02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_RELEASE.json`:** `sY0PSQFxjp8` moved from `shorts` to `unscheduled`.
- **Conditional 29 Nov Variolation readout:** **Not queued** because `sY0PSQFxjp8` did not air. Existing stronger HOS R2 vaccine topic stop and no-third-consecutive-subject spacing remain in force.
- **`008` Lightning / Franklin readiness for Sun 29 Nov gap:** Already satisfied under `J3500` — Ben-approved `008` Long `YqCWYlv_LCY` is scheduled Thu 26 Nov 18:00 UK, Short A `__UtUYdEUwg` Fri 27 Nov 11:30 UK, and Short C `4sYTV_rQcqs` Sun 29 Nov 11:30 UK (with post-publish Related link verification queued in `J3649`). No `008` slots changed; no Ben holds reopened; no new cuts commissioned.
