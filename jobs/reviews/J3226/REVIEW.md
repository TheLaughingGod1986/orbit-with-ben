# J3226 — Condition Check & 48 h Studio Readback for J3063: *How Do Plants Clean the Air?* (`ChbsigHD5_o`)

- **Run:** `gemini` (elected acting Chief on Mac mini; `chief_relay.py status` verified `Chief: Gemini` — Claude down until `2026-11-20T12:50:00Z`, Grok Bot down until `2026-11-20T17:33:46Z`, Codex down until `2026-11-20T12:08:03Z`)
- **Channel:** History of Science (`@HistoryOfScienceYT`, `UCXp7HkBIl1LgaznXuZHJyRg`) — verified directly on Mini HOS CDP `9222` using `scripts/cdp_tabs.py:reuse_page(ctx, "studio.youtube.com")` (single `studio.youtube.com` tab reused across all pages; zero extra Studio tabs opened; Orbit channel ID absent)
- **Video:** `ChbsigHD5_o` (*How Do Plants Clean the Air?*), HOS `006` (*The Willow Tree That Was Made of Air*, `VbPubYd6Fbs`) Short B `v02`, `0:25`
- **Went live:** `2026-11-18T11:30:00Z` (Wed 18 Nov 11:30 London)
- **Actual observation window:** `2026-11-20T11:59:15Z`–`2026-11-20T11:59:55Z` UTC
  - Channel dashboard: `11:59:15Z`–`11:59:22Z`
  - `ChbsigHD5_o` Overview (`Since published`): `11:59:22Z`–`11:59:28Z`
  - `ChbsigHD5_o` Reach (`Since published`): `11:59:28Z`–`11:59:35Z`
  - `ChbsigHD5_o` Engagement (`Since published`): `11:59:35Z`–`11:59:42Z`
  - `xgx2lYHhYZM` Overview & Reach (`Since published`, 17 Nov comparison): `11:59:42Z`–`11:59:55Z`
- **Actual elapsed age:** **48 h 29 m** since `2026-11-18T11:30Z` (recorded at `--hours 48 --read-at 2026-11-20T11:59Z`)
- **Mode:** Strictly read-only (`£0` spend; zero YouTube/Studio/listing/schedule/privacy/Buffer edits)

---

## 1. Studio Analytics Readback for `ChbsigHD5_o` (`Since published`, `18 Nov 2026, 11:30` – `20 Nov 2026, 11:59`)

| Metric | Studio Readback (`2026-11-20T11:59Z`, 48 h 29 m) | Flag Recorded |
|---|---|---|
| **Overview > Views** | **`3`** (`Since published`, `48-hour views: 3`; Dashboard Published videos row also `3`) | `--views 3` |
| **Overview > N more/less than usual** | **`57 less than the usual 60 – 150`** (`aria-label` on Overview & Reach `Views` comparison badge; lower bound `3 + 57 = 60`) | `--typical 60` |
| **Overview > Watch time (hours)** | **`0.0`** (`About the same as the usual 0.0 – 1.0`) | *(context only)* |
| **Overview > Subscribers** | **`0`** | *(context only)* |
| **Overview > Likes** | **`0`** (`Likes • Since published: 0`; Dashboard row `0` comments, `0` likes) | `--likes 0` |
| **Dashboard > Ranking by views (`N of 10`)** | **Not shown** — `ChbsigHD5_o` is no longer the *Latest Short performance* card on the Dashboard (replaced by today's Short *How Does a Blood Pressure Cuff Work?*, 20 Nov 11:30Z, showing `15` views / `5` engaged views in its first 29 minutes) | *(omitted)* |
| **Reach > Traffic sources (`How viewers found this Short`, `Views • Since published` & `48 hours`)** | **`Direct or unknown`: `66.7%` (`2` views)**, **`YouTube search`: `33.3%` (`1` view)**. No `Shorts feed` row is shown (0 of the 3 views are from the Shorts feed). | *(omitted — see note below)* |
| **Reach > Unique viewers** | **`0`** (`17 Nov 2026, 08:00` – `20 Nov 2026, 08:00`) | *(context only)* |
| **Reach / Engagement > Shown in feed (`Shorts feed impressions • Since published`)** | **`Not enough data`** (`How viewers engaged • Shorts feed impressions • Since published`; no `Shown in feed` card on Reach) | *(omitted)* |
| **Engagement > Viewed vs swiped away (`Stayed to watch`)** | **`Not enough data`** (Overview & Engagement `How viewers engaged`) | *(omitted)* |
| **Engagement > Engaged views** | **`2`** (`Since published`) | *(context only)* |
| **Engagement > Average view duration** | **`0:02`** (`0:04 less than the usual 0:07 – 0:28`) | *(context only)* |
| **Engagement > Average percentage viewed / Audience retention** | **`Not enough data`** (`Audience retention isn't ready yet. Processing can take up to two days.`) | *(omitted)* |

> **Important methodological note (no inference of zero feed impressions):**
> `How viewers found this Short` attributes `100.0%` of the 3 views to `Direct or unknown` (`2`) and `YouTube search` (`1`), with no `Shorts feed` traffic row. However, `How viewers engaged` (`Shorts feed impressions • Since published`) explicitly reads `Not enough data`. Per the J3063/J3131 Chief rulings, **zero Shorts-feed impressions is NOT inferred** from 3 total views or 0 Shorts-feed views. In `launch_check.py record`, `--feed-views` is intentionally omitted alongside `--shown`, `--stayed`, and `--avg-pct` because passing `--feed-views 0` without `--stayed` causes `launch_check.shown_in_feed()` to compute `shown = 0`.

Recorded in `05_Analytics/hos/launch/ChbsigHD5_o.json` via:
```bash
python3 scripts/launch_check.py record ChbsigHD5_o --hours 48 --views 3 --typical 60 --likes 0 --by gemini --read-at 2026-11-20T11:59Z
```

---

## 2. Output of `python3 scripts/launch_check.py judge ChbsigHD5_o`

```text
"How Do Plants Clean the Air?" (ChbsigHD5_o) · History of Science · Short · went live Wed 18 Nov 11:30 London
At 48 h: views 3 · shown in feed no figure yet · stayed to watch no figure yet · average viewed no figure yet
Usual for this channel: stayed to watch 29.6%, average viewed 74.0%

Verdict: BEHIND
  - 3 views at 48 h; Studio says the usual for us at this age is 60.
  - By the next morning it had 0 views; the 10 before it had 67 (median).

Do now
  - Studio gave no reach figures at this check, so the step that lost the viewers is not known. Read them again before deciding anything.
```

---

## 3. Corroboration & Context (Daily Snapshot, 17 Nov Short Comparison, Channel Health)

1. **Setup faults:** `0` faults verified in `J3063` (PR `#1028`, commit `8677fcd1e6`) and accepted by the Chief (`jobs/reviews/J3063/CHIEF_DECISION.md`). Daily snapshot `05_Analytics/hos/snapshots/2026-11-20.json` (`takenAt: 2026-11-20T06:40:34.014Z`) confirms `ChbsigHD5_o` remains `public` with `3` views, `0` likes, `0` comments — flat at `3` views across the 5 h 19 m between `06:40Z` and `11:59Z`.
2. **17 Nov Short comparison (`xgx2lYHhYZM`, *Why Is It Called a Vaccine?*, went live `2026-11-17T11:30Z`, read on Mini CDP `9222` at `2026-11-20T11:59:42Z`–`11:59:55Z`, elapsed 72 h 29 m):**
   - `Views`: `4` (`56 less than the usual 60 – 160`), `Watch time`: `0.0 h`, `Likes`: `0`.
   - `How viewers found this Short` (`Views • Since published` & `48 hours`): `YouTube search` `75.0%` (`3`), `Direct or unknown` `25.0%` (`1`); no `Shorts feed` row.
   - `How viewers engaged` (`Since published`, Overview): `100.0% Stayed to watch`, `0.0% Swiped away`; `Audience retention`: `Not enough data`.
   - Daily snapshot (`2026-11-20T06:40:34.014Z`): `public`, `4` views, `0` likes, `0` comments.
3. **Channel distribution check (Dashboard at `2026-11-20T11:59:21Z`):**
   - Today's Short (*How Does a Blood Pressure Cuff Work?*, 20 Nov 11:30Z) already has **`15` views (`5` engaged views)** in its **First 29 minutes**, while recent Shorts `xzKoHg0E0_U` (`212` views, +62 in last 48 h) and `Wvjd8g0CpzE` (`215` views) remain healthy. This confirms there is **no ongoing channel-wide distribution block**.

---

## 4. Verification Verdict

- **Mini HOS CDP `9222` access & 48 h Studio readback:** **VERIFIED.**
- **Outcome:** All available 48 h `Since published` metrics for `ChbsigHD5_o` have been recorded with exact UTC timestamps and elapsed age (`48 h 29 m`). `ChbsigHD5_o` is confirmed **BEHIND** (`3` views vs usual `60 – 150`) with `0` technical/setup faults; `Shorts feed impressions`, `Stayed to watch`, and `Audience retention` remain `Not enough data` at 48.5 h (below Studio's display threshold on 3 views; zero feed impressions is NOT inferred).
- **Resolution:** Because the 48 h first-day window is complete, `0` setup faults exist, a live Short cannot be re-cut, and no listing/visibility/schedule change is warranted, see `jobs/reviews/J3226/CHIEF_DECISION.md` for the Acting Chief ruling closing `J3063` and `J3226` as `done` (KEEP live video unchanged; track longer-term pattern in daily snapshots and weekly analytics audits rather than looping further first-day rechecks).
