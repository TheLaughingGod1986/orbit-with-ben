# J3386 Condition Verification — J2020 (`Rule 17 test: measure film 025 Shorts -> long (subs per 1,000 views) on 2026-11-22`)

- **Verification Job:** `J3386` (`Verify condition for J2020`, `recheck_of: J2020`, `repo: owb`, `kind: review`, `films: ["OWB:025"]`, `due: 2026-11-22T00:00:00+00:00`)
- **Parent Job:** `J2020` (`Rule 17 test: measure film 025 Shorts -> long (subs per 1,000 views) on 2026-11-22`, `status: blocked`, `repo: owb`, `needs: cloud`, `kind: review`, `hold.type: date`)
- **Reviewer:** `gemini` (Gemini 4 Neon High, **specialist worker** — per `chief_relay.py status` at `2026-11-22T18:04Z` and `18:07Z`, **`Chief: Codex`** (`codex`) is UP and elected Chief while `claude` is out until `2026-11-22T21:50:00Z` and `chief` / Grok Bot is down). No Chief ruling, no hold release, no self-merge.
- **Checked At:** `2026-11-22T18:04Z–18:07Z` (past `2026-11-22T18:00:15Z`, i.e., **14 days + ~6 minutes** after `025` long `Js6EQJ8qDi8` went public)
- **Spend:** `£0` (`0` credits; read-only verification only — zero YouTube/Studio/API/Buffer writes, no upload, schedule, or metadata changes)
- **Verdict (Advisory — Parked for Elected Chief `codex`):** **CONDITION PROVEN SATISFIED — RECOMMEND ELECTED CHIEF (`codex`) REOPEN `J2020` WITH EVIDENCE AND CLOSE `J3386`** (with a transparent data-lag note below regarding `analytics.through: 2026-11-20` in the `06:40Z` snapshot).

---

## 1. Waiting Condition Checked (`J2020["hold"]`, recorded `2026-11-04T11:49Z` by `claude`, commit `205f968626`)

> `Sun 22 Nov 2026 18:00Z reached (14 days after 025 long public)`

---

## 2. Live Public, Input & Receipt Evidence Verified (`2026-11-22T18:04Z–18:07Z`)

| Check | Result | Direct Observed Evidence |
|---|---|---|
| **1. UTC clock vs 14-day elapsed window** | **PASS (ELAPSED)** | - Verified UTC time: `2026-11-22T18:05:05Z` and `2026-11-22T18:06:31Z`.<br>- `Js6EQJ8qDi8` went public at **`2026-11-08T18:00:15Z`** -> 14 full days (`336 h`) elapsed at **`2026-11-22T18:00:15Z`**. |
| **2. Read-only YouTube Data API v3 `videos.list` (`YOUTUBE_REFRESH_TOKEN`, `18:06:31Z`)** | **PASS (ALL 5 LIVE & PUBLIC)** | All 5 `025` videos on `UC_esArsDKd3GJvOkeO0DUog` (`@OrbitWithBen`), `madeForKids = false`, `publishAt = null`:<br>- **Long `Js6EQJ8qDi8`:** `"Could a Robot Survive on Mars? (One Lasted 14 Years)"`, `privacyStatus = "public"`, `publishedAt = "2026-11-08T18:00:15Z"`, `PT8M11S`, `26` views, `0` likes, `1` comment.<br>- **Short 1 `iyvWYFP_ETA`:** `"Could a Robot Survive a Night on Mars?"`, `privacyStatus = "public"`, `publishedAt = "2026-11-09T11:30:10Z"`, `PT26S`, `1,074` views, `10` likes.<br>- **Short 2 `B1z2dv7m7Vk`:** `"Why Did a 90-Day Mars Rover Last 14 Years?"`, `privacyStatus = "public"`, `publishedAt = "2026-11-11T11:30:09Z"`, `PT27S`, `110` views, `1` like.<br>- **Short 3 `uhZSRcvngvE`:** `"How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?"`, `privacyStatus = "public"`, `publishedAt = "2026-11-12T11:30:13Z"`, `PT55S`, `60` views, `2` likes.<br>- **Short 4 `RT-ec4_GcOk`:** `"How Did a Helicopter Fly 72 Times on Mars?"`, `privacyStatus = "public"`, `publishedAt = "2026-11-14T11:30:27Z"`, `PT27S`, `1,270` views, `16` likes. |
| **3. Signed-out oEmbed & watch page (`18:05Z`)** | **PASS (GENUINELY PUBLIC)** | - Public oEmbed returned **`HTTP 200`** with `author_name = "Orbit With Ben"` for all 5 IDs (`Js6EQJ8qDi8`, `iyvWYFP_ETA`, `B1z2dv7m7Vk`, `uhZSRcvngvE`, `RT-ec4_GcOk`).<br>- Signed-out `https://www.youtube.com/watch?v=Js6EQJ8qDi8`: `isPrivate = false`, `isUnlisted = false`, `publishDate = "2026-11-08T10:00:15-08:00"` (`= 2026-11-08T18:00:15Z`), `viewCount = "27"`.<br>- Retired superseded 025 Shorts (`TtgHNLXfDSs`, `N42gKBbD7tE`, `bSjWiCbB7pY`) remain `privacy = "private"`, `publishAt = null`, `views = 0` in `2026-11-22.json`. |
| **4. Daily snapshot & `studio_ctr.json` availability** | **PRESENT (NOTE YTA 2-DAY LAG)** | - `05_Analytics/owb/snapshots/2026-11-22.json` (`sha256: 0fa6924ed39d7c055387db4dd62813ef73acaf399b05db9b873c2714d05b6315`), `takenAt: 2026-11-22T06:40:09.867Z`, `analytics.through: 2026-11-20`. Contains `analytics.lifetime` (`views`, `subs`, `minutes`, `avgViewPct`) and `analytics.sources.last28` for all 5 videos (`Js6EQJ8qDi8`: `24` YTA views, `0` subs, `RELATED_VIDEO: 6`; 4 live Shorts combined: `2,513` YTA views, `3` subs: `iyvWYFP_ETA` `1,074`v/`1` sub, `B1z2dv7m7Vk` `110`v/`0`, `uhZSRcvngvE` `60`v/`0`, `RT-ec4_GcOk` `1,269`v/`2`).<br>- `05_Analytics/owb/studio_ctr.json` (`sha256: 03d3f3903e52fd051ff6b4c6ff65b3cfebd7a7d1fe84bccd9ae29c994f8abbb1`), `readAt: 2026-11-22T07:12:37.886352+00:00`, `period: lifetime`, contains all 5 videos.<br>- **Lag transparency note for Chief:** `2026-11-22.json` reflects the `06:40Z` daily run with YouTube Analytics `analytics.through = 2026-11-20` (standard ~2-day YTA reporting lag; days 0–12 of the long). Reopening `J2020` now satisfies the exact date-hold condition and lets the executor record the readout noting `analytics.through = 2026-11-20` (or Chief may alternatively hold until after `2026-11-25T06:40Z` if strict YTA `through >= 2026-11-22` is preferred). |
| **5. Original gates, Ben approval & Related-video receipts** | **ALL VALID** | - **Ben approval:** `05_Analytics/LEARNINGS.md` (`sha256: b3494f1ac26958cdb76f38c8b229dcdc0ed9275f4284121d0abdf3f4e00881c0`) Rule 17 records **Ben's go, 4 Nov 2026** (`monthly report rec. 3`; baseline `0.7` subs / 1,000 views from October's 5 subs on 6,830 views; pass = at least double = `≥1.4`). Still marked `**test** (Ben, 4 Nov)` with no `025` readout line recorded yet.<br>- **Scope:** `J2020` is **reads only** (writes one readout line under Rule 17 in `05_Analytics/LEARNINGS.md` and posts on the studio thread; zero spend, zero YouTube/Studio writes).<br>- **Related-video receipts (all `done`):** `J0123` (9 Nov 10:52Z, date gate), `J0135` (9 Nov 22:39Z, `N42gKBbD7tE` -> `Js6EQJ8qDi8`), `J2504` (10 Nov 14:03–14:04Z, `iyvWYFP_ETA`, `B1z2dv7m7Vk`, `bSjWiCbB7pY` -> `Js6EQJ8qDi8` — note `iyvWYFP_ETA` was set ~44 h after long go-public / ~26.5 h after the Short aired, so the "<1 h of go-public" protocol was missed on `025`), `J2519` (10 Nov 18:39:09Z readback `jobs/readbacks/J2519/after_studio.json`, `uhZSRcvngvE` -> `Js6EQJ8qDi8`), `J2520` (11 Nov 13:44:17Z readback `jobs/readbacks/J2520/after_studio.json`, `RT-ec4_GcOk` -> `Js6EQJ8qDi8`), and `J0124` (15 Nov 18:36Z, post-launch checklist complete).<br>- **Receipt-ID note for J2020 executor:** `J2020`'s brief says `(check the J0124/J0135/J0861 receipts)`; `J0861` is actually film `026`'s Related job (`c5AdqQsnnys`), while film `025`'s actual Related receipts are `J0124`, `J0135`, `J2504`, `J2519`, and `J2520`. |

---

## 3. Authority Boundary & Ready-to-Run Chief Actions (`codex`)

`gemini` is a specialist worker on this run; `chief_relay.py status` reports **`Chief: Codex`** (`codex`). Releasing a verified hold (`jobs.py reopen J2020`), recording an alternate wait (`jobs.py wait --recheck J3386`), merging this verification PR, and closing `J3386` are protected Chief actions. `J3386` is therefore parked for elected Chief `codex`.

```bash
# Run as elected Chief (codex, or active elected Chief from `chief_relay.py status`):

# 1. Merge this verification PR (jobs/reviews/J3386/REVIEW.md), then reopen J2020 with evidence:
python3 scripts/jobs.py reopen J2020 --agent codex \
  --note "Condition verified SATISFIED via J3386 (jobs/reviews/J3386/REVIEW.md): Sun 22 Nov 2026 18:00Z reached and 14 days elapsed since 025 long Js6EQJ8qDi8 went public at 2026-11-08T18:00:15Z (verified live Public via Data API videos.list at 18:06:31Z, signed-out watch page, and oEmbed HTTP 200 alongside all 4 live 025 Shorts iyvWYFP_ETA, B1z2dv7m7Vk, uhZSRcvngvE, RT-ec4_GcOk). 2026-11-22 snapshot (takenAt 06:40Z, analytics.through 2026-11-20), studio_ctr.json (readAt 07:12Z), Ben's 4 Nov Rule 17 approval, and Related receipts (J0124/J0135/J2504/J2519/J2520; note J0861 is 026) are all present and valid. Executor should note analytics.through=2026-11-20 in the Rule 17 readout." \
  --git

# 2. Close J3386 as elected Chief:
python3 scripts/jobs.py reopen J3386 --agent codex \
  --note "Elected Chief closing completed J3386 condition verification after merging review PR and reopening J2020" \
  --git
python3 scripts/jobs.py next --agent codex --can mini,cloud,any --id J3386 --git
python3 scripts/jobs.py done J3386 --agent codex \
  --result "Chief accepted J3386 CONDITION SATISFIED verification (jobs/reviews/J3386/REVIEW.md): 025 long Js6EQJ8qDi8 live Public since 2026-11-08T18:00:15Z (>14d elapsed at 2026-11-22T18:06:31Z) with all 4 live Shorts Public, 2026-11-22 snapshot + studio_ctr.json + Ben 4 Nov Rule 17 approval and Related receipts verified. Reopened J2020 with evidence." \
  --git
```
