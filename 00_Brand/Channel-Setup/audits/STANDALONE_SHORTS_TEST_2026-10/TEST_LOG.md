# Standalone Shorts test measurement log

J0216 · Codex · 13 October 2026. Chief authorisation: J0164; approved S1–S8 v01 and MANIFEST locked slots.

## Measurement window

Four weeks: 24 October–20 November 2026 (UK). Readout from 21 November. Compare views, retention (APV and AVD), and subscribers gained with Orbit Shorts cut from longs and Orbit longs over the same dates. Record day-1 Shorts-feed share (fed at ≥50%) separately; retention under about 50 views is inconclusive. Use channel analytics snapshots; never edit generated analytics by hand. No results yet: every test Short is private and scheduled.

## Scheduled cohort

| Short | YouTube id | PublishAt (UTC) | Cover | Buffer |
|---|---|---|---|---|
| Why Does a Day on Mercury Last Two of Its Years? (`s1_mercury`) | vlkj8RQKmH8 | 2026-10-24T10:30:22.000Z (Live) | Set in Studio | IG/FB/Threads scheduled |
| Why Are the Winds on Neptune Faster Than Sound? (`s2_neptune` v07a) | 1OCNzhkiBuc | 2026-10-27T11:30:00Z | Set via API (2,000 KM/H / WINDS) | deferred. v01 `oyRcrFTYyDY` is private and unscheduled |
| Why Do Astronauts See 16 Sunrises a Day? (`s3_iss` v04) | VfDm3E2bUgU | 2026-10-31T11:30:00Z | Set via API (DAWN EACH / 90 MINUTES) | deferred. v01 `XKlq0TK1OVA` is private and unscheduled |
| This Planet Has 21-Year Winters | ZpEA8stoSPA | 2026-11-03T11:30:00.000Z | Set in Studio | IG/FB/Threads scheduled |
| Shooting Stars Aren't Stars | T9fVlG3CCzU | 2026-11-07T11:30:00.000Z | Set in Studio | IG/FB/Threads scheduled |
| Standing on Titan Feels Like Diving 15 Metres Down | RLSJm59OSzI | 2026-11-10T11:30:00.000Z | Set in Studio | IG/FB/Threads scheduled |
| Pluto's Heart Has No Craters | gmzaCfJF1gA | 2026-11-14T11:30:00.000Z | Set in Studio | IG/FB/Threads scheduled |
| Voyager 1 Is About to Be One Light-Day Away | kKN8Ale42sE | 2026-11-17T11:30:00.000Z | Set in Studio | Blocked: 10/10 free-plan slots |

## Next check

Voyager `kKN8Ale42sE`: retry Buffer mirrors after a scheduled post clears capacity. Keep the exact YouTube time (17 November 11:30 UTC). Do not upgrade, change dates, or re-upload. Registry has `standalone` and `standaloneTest` true. Daily Buffer check can retry once the records are on main.

## Scheduled compilation film (J0168 / J0276)

Four-week compilation measurement window: 21 October–18 November 2026 (UK), readout from 19 November 2026. Compare views, retention (APV and AVD), and subscribers gained against Orbit Shorts (cut from longs) and regular Orbit longs over the same four weeks.

| Film | YouTube id | PublishAt (UTC) | Duration | Master SHA-256 | Cover |
|---|---|---|---|---|---|
| How Long Will Anything in Space Last? (`owb_compilation_v05.mp4`) | `m09jUdwC5hk` | `2026-10-21T17:00:00Z` (Wed 21 Oct 18:00 London) | 47:37.8 (2857.77 s) | `ee7850d24601a58f48d8bb4ebac827815c7dc237c4986fceae2271229664e729` | Set via API (`THE LAST LIGHT`) |

## Readout

| Cohort | Views | APV | AVD | Subscribers gained |
|---|---|---|---|---|
| Standalone Shorts (S1 `vlkj8RQKmH8`, ~9.5 h read) | 837 Studio / 813 public (282 engaged, 5 likes, 1.4 h watch time; 95.6% Shorts feed = **FED**) | **73.4%** on 20.44 s (`PASS` vs 70% target; 32.2% stayed = `MISS` vs 60% target) | **0:15** (15 s on 20.44 s) | 0 |
| Compilation film (`m09jUdwC5hk`) | 3 | 1.3% | 0:35 (35 s on 2857.77 s) | 0 |
| Shorts cut from longs (`2e-giqFmfy8` + `82Ao0v5XiQI` + `n_4XskX0yZk`) | 59 (`2e-giqFmfy8`) / 90 (`82Ao0v5XiQI`) / 881 (`n_4XskX0yZk`) | 62.1% / 53.3% / 62.3% Studio | 0:14 / 0:13 / 0:15 | +1 (`n_4XskX0yZk`) |
| Longs | pending | pending | pending | pending |

## Per-Short readouts (J0919)

### S1 Mercury — `vlkj8RQKmH8` (*Why Does a Day on Mercury Last Two of Its Years?*)
- **Published:** `2026-10-24T10:30:22Z` (Sat 24 Oct 11:30 BST). Read at `2026-10-24T20:01Z` (~9.5 h live).
- **Views & Engagement (`studio_ctr.json` + Studio + Data API):**
  - **Studio views:** **837** (+777 vs typical; **#2 Short on OWB** behind `n_4XskX0yZk` at 881) | **Public Data API views:** **813** (5 likes, 0 comments)
  - **Engaged views:** **282** (~876 shown in feed)
  - **Watch time:** **1.4 hours** (+0.4 vs typical)
  - **Stayed to watch vs Swiped away:** **32.2% stayed / 67.8% swiped** → **`MISS`** vs the **60%+** stayed-to-watch target (`<45%` MISS).
  - **Average view duration / Average % viewed:** **0:15 AVD** on `20.44 s` master (**73.4%**; `71.4%` on YouTube's rounded `21 s`) → **`PASS`** vs the **70%+** average-viewed target.
  - **Traffic sources (Studio Reach, since published):** **Shorts feed 95.6%** (**FED**, well above the `>=50%` day-1 feed bar), **YouTube search 2.6%**, **Other YouTube features 1.4%**, **External 0.4%**.
  - **YouTube Analytics v2 API (`YT_ANALYTICS_REFRESH_TOKEN_OWB`):** `0` metric rows and `0` `elapsedVideoTimeRatio` retention rows at ~9.5 h (Analytics API currently settled through `2026-10-22`, ~48 h lag; Studio's lifetime retention card likewise reads *"Not enough information to display audience retention data"* until the 48 h curve settles on ~26 Oct).
- **Cut-by-cut & word-by-word drop analysis (`06_Final-Exports/owb_sa_s1_mercury_v01_meta.json` + `owb_sa_s1_mercury_vo_v01_trim_words.json`):**
  1. **Drop #1 — 0.0–5.5 s initial swipe (`67.8%` swiped away, `32.2%` stayed):**
     - **On screen (`0.0–5.5 s`, Row 1 `s1_mercury/PIA11351.jpg`):** Static grey MESSENGER limb photo `PIA11351.jpg` with the top ~45% black sky, pushed only `1.00 -> 1.04` over `5.5 s`, with top hook caption `ONE DAY, / TWO YEARS` (yellow `DAY,`, `0.0–2.2 s`). No moving video on frame 0, zoom `<=1.10`, and first cut held to `5.5 s` (vs `<=3.0 s` rule).
     - **Said (`0.08–5.16 s`):** `"On"` (`0.08–0.16 s`), `"Mercury,"` (`0.22–0.72 s`), `[0.40 s pause: 0.72–1.12 s]`, `"one day lasts two years."` (`1.12–3.20 s` — surprise words `"two years"` land at `2.44–3.20 s`, past the `1.5 s` bar), `[0.40 s pause: 3.20–3.60 s]`, `"Stay, and I'll show you how."` (`3.60–5.16 s` — meta-promise filler), `[0.40 s pause: 5.16–5.56 s]`.
  2. **Body hold — 5.5–15.1 s (Row 2 `PIA14083.jpg` `5.5–9.7 s` & Row 3 `PIA12266.jpg` `9.7–15.1 s`):**
     - **On screen:** Colorized globe `PIA14083.jpg` (`zoom 1.05 -> 1.15`, `5.5–9.7 s`), then surface still `PIA12266.jpg` (`zoom 1.00 -> 1.10`, `9.7–15.1 s`, `5.4 s` hold `>4.0 s`), mid-video title banner `A Day on Mercury Lasts Two Years` (`9.0–14.0 s`), and fact card `176 / EARTH DAYS` ticking in at `14.05 s` (`14.0–17.2 s`).
     - **Said:** `"Mercury races round the sun every 88 Earth days,"` (`5.56–9.30 s`), `"but it spins so slowly, sunrise to sunrise takes 176."` (`9.70–14.74 s`; `"176"` spoken `13.42–14.74 s`).
  3. **Drop #2 — ~15.0 s average exit (`0:15` Studio AVD, `73.4%` viewed) & 17.44–20.44 s tail:**
     - **On screen & said (`14.74–20.44 s`):** Viewers who stay past the swipe hold through the `"176"` numeric answer (`13.42–14.74 s`, `72.1%` of runtime) and exit around **`~15.0 s`** as Row 3 cuts to Row 4 (`PIA13674.jpg`, `15.1–17.44 s`, `"Two trips round the sun before it's morning again"` `15.14–17.44 s`), followed by a **`3.00 s` silent VO tail (`17.44–20.44 s`, Row 5 `PIA11351.jpg` loop crossfade)** — double the `<=1.5 s` last-word-to-loop ceiling and without a sentence seam looping into line 1.
- **Comparison with S2 Neptune (`oyRcrFTYyDY`, *Why Is the Wind on Neptune Faster Than Sound?*):**
  - S2 Neptune has **not aired yet** (Private, scheduled for `2026-10-27T11:30:00Z`, `0` views). Its v01 cut shares S1 Mercury's structural flaws (`"Stay, and I'll show you why"` meta-promise and static opening hold), and `J0914` is queued to re-cut S2 Neptune v02 locally (moving frame-0 footage, drop `"Stay, and I'll show you"`, first cut `<=3.0 s`, tail `<=1.5 s`) before its Tue 27 Oct 11:30Z slot.
