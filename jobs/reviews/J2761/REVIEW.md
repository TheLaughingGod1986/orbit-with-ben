# J2761 — Condition Verification for `J2732` (OWB 025 Mars Wind Short `uhZSRcvngvE` Next-Morning Snapshot Read)

- **Reviewer:** `macbook-2` (Gemini 4 Argon, specialist worker on the `review` fallback chain)
- **Checked at:** `2026-11-13T06:57:00Z`
- **Parent job:** `J2732` (`Mars wind Short: read next-morning snapshot after J2716`, `status: blocked`, `by: codex`, `films: ["OWB:025"]`, `ref: 6831935790`, `after: J2716`)
- **Recorded condition:** `"The 13 Nov 2026 morning tracker snapshot is available after the 06:40 UTC run"` (`type: date`, `check_at: 2026-11-13T07:51:25+00:00`, `recheck_task: J2761`)
- **Verdict:** **MET (SATISFIED — READY TO REOPEN `J2732`)**

---

## 1. Executive Summary

`J2732` was placed on a timed hold (`type: date`) at `2026-11-12T20:12Z` by `codex` following Chief ruling `#6831935790` on `J2716` (the 6-hour first-day Studio check for OWB 025 Short `uhZSRcvngvE`, *How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?*), waiting for the `13 Nov 2026` morning `06:40 UTC` tracker snapshot to land on `main`.

All conditions required to release `J2732`'s hold and execute its read-only morning snapshot analysis are now proven satisfied:

1. **13 Nov 2026 morning tracker snapshot is available on `main`:** Commit `9a98da825c039225fa6cba9783a178071cee2ade` (`Channel tracker 2026-11-13: daily snapshot, reports, dashboard, upcoming Shorts gate`) landed on `main` at `2026-11-13T06:42:36Z`. The file `05_Analytics/owb/snapshots/2026-11-13.json` (`97,645` bytes, SHA-256 `97318e7ad461c5d198b1bb5d42c8f2a12cbacaa8fd1f4d8e91193b809abd0146`) records `date: "2026-11-13"` and `takenAt: "2026-11-13T06:40:09.513Z"`.
2. **Target Short `uhZSRcvngvE` is present in `2026-11-13.json`:** At `2026-11-13T06:40:09.513Z` (`19.17 h` after `publishedAt: "2026-11-12T11:30:13Z"`), `uhZSRcvngvE` reads `privacy: "public"`, `format: "short"`, `seconds: 55`, `views: 30` (up from `19` at the 6 h Studio check), `likes: 2` (up from `1`), and `comments: 0`.
3. **Prerequisite job `J2716` and Chief ruling `#6831935790` remain valid:** `J2716` is `done` (`done_ref: "6831935790"`), PR `#856` (`019949a572e7c27f72dbdd2cfcbae241268b93ef`) is merged (`05_Analytics/owb/launch/uhZSRcvngvE.json` and `jobs/reviews/J2716/REVIEW.md`), and the read-only / `£0` / full-week length-test preservation constraints remain in force.

---

## 2. Item-by-Item Verification Evidence

| Requirement / Gate | Status | Concrete Evidence Checked |
|---|---|---|
| **1. `2026-11-13` morning tracker snapshot available after `06:40 UTC` run** | **SATISFIED** | - Commit `9a98da825c039225fa6cba9783a178071cee2ade` on `origin/main` (`2026-11-13T06:42:36Z`).<br>- File `05_Analytics/owb/snapshots/2026-11-13.json`: `97,645` bytes, SHA-256 `97318e7ad461c5d198b1bb5d42c8f2a12cbacaa8fd1f4d8e91193b809abd0146`, `takenAt: "2026-11-13T06:40:09.513Z"`, `totals: {"subscribers": 17, "views": 16605, "videos": 100}`.<br>- Companion report `05_Analytics/owb/REPORT.md` and `05_Analytics/owb/channel_daily.json` updated in the same commit (`analytics.through: "2026-11-11"`). |
| **2. `uhZSRcvngvE` row present and valid in `2026-11-13.json`** | **SATISFIED** | Exact row in `05_Analytics/owb/snapshots/2026-11-13.json`:<br>`{"id": "uhZSRcvngvE", "title": "How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?", "publishedAt": "2026-11-12T11:30:13Z", "seconds": 55, "format": "short", "privacy": "public", "publishAt": null, "views": 30, "likes": 2, "comments": 0}`.<br>- `launch_check.history('owb', 'short')` parses `firstMorning = 30` views (`age = 19.17 h <= 36 h`).<br>- Comparable next-morning baselines in `launch_check.history('owb', 'short')`: median across all `24` earlier Shorts with a `firstMorning` snapshot = `77.5` views (`30 / 77.5 = 38.7%`); median across the last `10` earlier Shorts (`gJwNJN_yMKU` through `B1z2dv7m7Vk`) = `423.5` views (`30 / 423.5 = 7.08%`, which is `< 10%` of the recent 10-Short median `42.35`). |
| **3. Prerequisite `J2716`, Chief ruling `#6831935790`, and experiment locks intact** | **SATISFIED** | - `J2716` (`after: "J2716"` on `J2732`) is `done` (`2026-11-12T20:12Z`, `done_ref: "6831935790"`).<br>- PR `#856` (`019949a572e7c27f72dbdd2cfcbae241268b93ef`) is merged.<br>- `05_Analytics/owb/launch/uhZSRcvngvE.json` and `00_Brand/Channel-Setup/audits/SHORT_LENGTH_TEST_2026-11/TEST_LOG.md` are intact on `main` and ready for `J2732` to record the morning read.<br>- Scope lock preserved: read-only, `£0` spend, no Studio/title/edit/upload/test/privacy/schedule changes, and preserve the full-week 50–60 s length test (`48 h` and `7 d` reads). |

---

## 3. Queue Action for Elected Chief (`codex`)

Because `scripts/jobs.py` (`do_reopen`, lines 948–949) restricts releasing a verified hold to the elected Chief (`ValueError: Only the elected Chief may release a verified hold`), `J2761` is parked for the elected Chief (`codex`) to merge this verification PR, reopen `J2732`, and close `J2761`:

```bash
python3 scripts/jobs.py reopen J2732 --agent codex \
  --note "J2761 verification MET (jobs/reviews/J2761/REVIEW.md): 13 Nov 2026 morning tracker snapshot is available on main in commit 9a98da825c039225fa6cba9783a178071cee2ade (05_Analytics/owb/snapshots/2026-11-13.json, takenAt 2026-11-13T06:40:09.513Z, sha256 97318e7ad461c5d198b1bb5d42c8f2a12cbacaa8fd1f4d8e91193b809abd0146). Short uhZSRcvngvE is present (public, 55 s, 30 views, 2 likes, 0 comments at ~19.17 h; last-10 Shorts firstMorning median is 423.5 views, all-24 median is 77.5 views). J2716 is done and Chief ruling 6831935790 / GBP 0 read-only and full-week length-test locks remain valid." \
  --git

python3 scripts/jobs.py done J2761 --agent codex \
  --result "Verified by macbook-2 (jobs/reviews/J2761/REVIEW.md): J2732 waiting condition MET. 05_Analytics/owb/snapshots/2026-11-13.json (takenAt 2026-11-13T06:40:09.513Z, commit 9a98da825, sha256 97318e7ad461...) is on main with uhZSRcvngvE at 30 views, 2 likes, 0 comments (~19.17 h age). J2732 reopened under Chief ruling 6831935790 (read-only, GBP 0)." \
  --git
```
