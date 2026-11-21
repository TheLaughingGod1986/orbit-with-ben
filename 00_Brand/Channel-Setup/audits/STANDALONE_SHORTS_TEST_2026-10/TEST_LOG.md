# Standalone Shorts test measurement log

J0216 · Codex · 13 October 2026. Chief authorisation: J0164; approved S1–S8 v01 and MANIFEST locked slots.
Final four-week readout & compilation readout: J3326 · MacBook slot 2 (`macbook-2`) · 21 November 2026 (read-only analytics pass, £0, nothing changed in Studio).

## Measurement window

Four weeks: **24 October–20 November 2026 (UK)**. Readout from **21 November 2026**. Compare views, day-1 Shorts-feed share (`≥50%` = FED), stayed-to-watch %, retention (APV and AVD), and subscribers gained with Orbit Shorts cut from longs and Orbit longs over the same dates. Retention under about 50 views is inconclusive (`REPORT.md` treats `<100` Studio views as too few to judge for stayed/APV verdicts). All metrics are read-only from `05_Analytics/owb/snapshots/2026-11-20.json` (`takenAt: 2026-11-20T06:40:10Z`; YouTube Analytics v2 API settled through `2026-11-18`), `05_Analytics/owb/studio_ctr.json` (`readAt: 2026-11-21T07:06:16Z`, lifetime Studio metrics covering through 20 Nov), and `05_Analytics/owb/launch/*.json` (6-hour checks for 18–20 Nov Shorts). Never edit generated analytics by hand.

## Final aired cohort (verified against `UPLOADS.json` and `2026-11-20.json`)

Five of the eight standalone Shorts were re-cut and swapped before air; all five superseded v01 uploads (`oyRcrFTYyDY`, `XKlq0TK1OVA`, `RLSJm59OSzI`, `gmzaCfJF1gA`, `kKN8Ale42sE`) remain `private` with `publishAt: null` and `0` views. In particular, **`UPLOADS.json` and `2026-11-20.json` confirm live S6 is `ffYKoNVPoqg`** (superseding `RLSJm59OSzI`) and **live S8 is `9q_OvQ1Rd8Y`** (`swapJob: J2882`, superseding `kKN8Ale42sE`).

| Short | Live YouTube id | Aired (UTC) | Duration (YT / master) | Cover & Buffer | Superseded v01 id (Private, 0 views) |
|---|---|---|---|---|---|
| S1 · Why Does a Day on Mercury Last Two of Its Years? (`s1_mercury` v01) | `vlkj8RQKmH8` | `2026-10-24T10:30:22Z` | 21 s / 20.44 s | Studio cover · Buffer IG/FB/Threads posted | — |
| S2 · Why Are the Winds on Neptune Faster Than Sound? (`s2_neptune` v07a) | `1OCNzhkiBuc` | `2026-10-27T11:30:11Z` | 21 s / 20.60 s | API cover (`2,000 KM/H / WINDS`) · not in `BUFFER_POSTS.json` | `oyRcrFTYyDY` |
| S3 · Why Do Astronauts See 16 Sunrises a Day? (`s3_iss` v04) | `VfDm3E2bUgU` | `2026-10-31T11:30:36Z` | 19 s / 18.90 s | API cover (`DAWN EACH / 90 MINUTES`) · Buffer IG/FB/Threads posted | `XKlq0TK1OVA` |
| S4 · Why Does Uranus Have 21-Year Winters? (`s4_uranus` v01) | `ZpEA8stoSPA` | `2026-11-03T11:30:13Z` | 22 s / 21.17 s | Studio cover · Buffer IG/FB/Threads posted | — |
| S5 · What Are Shooting Stars Really Made Of? (`s5_shooting_stars` v01) | `T9fVlG3CCzU` | `2026-11-07T11:30:04Z` | 21 s / 20.00 s | Studio cover · Buffer IG/FB/Threads posted | — |
| S6 · What Would Standing on Saturn's Moon Titan Feel Like? (`s6_titan` v11) | `ffYKoNVPoqg` | `2026-11-10T11:30:32Z` | 19 s | Studio cover · Buffer IG/FB/Threads posted | `RLSJm59OSzI` |
| S7 · Why Does Pluto's Giant Ice Heart Have Zero Craters? (`s7_pluto_heart` v02) | `z5V6gIXXYs8` | `2026-11-13T11:30:37Z` (swapped from 14 Nov, J2715) | 18 s / 17.60 s | API + Studio cover (`FROZEN / NITROGEN`) · Buffer IG/FB/Threads posted | `gmzaCfJF1gA` |
| S8 · How Far From Earth Is Voyager 1 Right Now? (`s8_voyager1` v02) | `9q_OvQ1Rd8Y` | `2026-11-17T11:30:26Z` (swapped, J2882) | 17 s | Studio cover · Buffer IG/FB/Threads posted (`6af96707…` / `6af96708…` / `6af96709…`) | `kKN8Ale42sE` |

*(Historical note: the earlier "Next check" entry for `kKN8Ale42sE` Buffer capacity was resolved when `J2882` swapped S8 to `9q_OvQ1Rd8Y` and posted its IG/FB/Threads Buffer mirrors on 17 Nov.)*

## Scheduled compilation film (J0168 / J0276)

Four-week compilation measurement window: **21 October–18 November 2026 (UK)**, readout due from **19 November 2026**. Compare views, retention (APV and AVD), and subscribers gained against Orbit Shorts and regular Orbit longs over the same four weeks.

| Film | YouTube id | Aired (UTC) | Duration | Master SHA-256 | Cover |
|---|---|---|---|---|---|
| How Long Will Anything in Space Last? (`owb_compilation_v05.mp4`) | `m09jUdwC5hk` | `2026-10-21T17:00:22Z` (Wed 21 Oct 18:00 London) | 47:37.8 (2857.77 s; YT 2858 s) | `ee7850d24601a58f48d8bb4ebac827815c7dc237c4986fceae2271229664e729` | Set via API (`THE LAST LIGHT`) |

---

## Final Four-Week Readout (J3326 · 21 November 2026)

### Executive summary

1. **Standalone Shorts (S1–S8) matched—but did not beat—cut-from-long Shorts on reach, trailed on subscriber conversion, and missed the 60% stayed-to-watch bar (`0/8`):**
   - **Reach parity:** S1–S8 averaged **`622.5` Studio views/Short** (median `489.0`, total `4,980`), virtually tied with **standard cut-from-long Shorts** (`n = 8`, excluding Test A and the 55 s length test: mean **`608.9`**, median **`542.5`**, total `4,871`) and ahead of all cut-from-long Shorts combined (`n = 10`: mean `504.1`, median `499.5`, total `5,041`).
   - **Feed rate:** S1–S8 were **7/8 FED (`87.5%`**, median `93.9%` day-1 Shorts feed; only S6 Titan `ffYKoNVPoqg` missed at `36.6%`), vs **7/7 FED (`100%`**, median `95.2%`) for settled standard cut-from-long Shorts (`8/9`, `88.9%` across all settled cut-from-long Shorts including the 55 s length test).
   - **Stayed-to-watch:** S1–S8 posted **`37.8%`** view-weighted (`37.2%` mean / `35.9%` median; `0/8` PASS `≥60%`, `2/8` WATCH `45–60%`), slightly below cut-from-long Shorts (**`39.2%`** view-weighted across all 10; `39.7%` mean / `37.8%` median on `≥50`-view cuts; `38.9%` view-weighted on standard cuts).
   - **APV / AVD:** S1–S8 posted higher view-weighted APV (**`96.7%`** vs `86.8%` all cut-from-long / `87.5%` standard cut-from-long; mean `105.9%` vs `82.8%` / `87.0%`), largely because S1–S8 were shorter (`17–22 s`) and S4 Uranus (`ZpEA8stoSPA`) logged an extreme **`306.8%`** (`67 s` AVD) rewatch outlier. Excluding S4, the other 7 standalone Shorts averaged `77.2%` APV, and on **median APV** standard cut-from-long Shorts (`78.2%`) slightly edged out S1–S8 (`75.7%`).
   - **Subscribers gained:** Cut-from-long Shorts generated **`+5` subscribers** (`0.99` subs/1k Studio views; `1.03`/1k on standard cuts) vs **`+2` subscribers** from S1–S8 (`0.40` subs/1k views, both from S4 Uranus) on almost identical total view volume (~5,000 each).
   - **Verdict on standalone format:** Do **not** replace cut-from-long Shorts with standalone Shorts as the default. Cut-from-long Shorts match standalone reach, convert `2.5×` more subscribers per 1,000 views, reuse long-film VO/picture research, and directly reinforce parent-long clusters. Use standalone/dated Shorts selectively as **low-cost topic tests (Rule 37 step 7)** and timely dated events built to the **16–19 s** tight loop format (the two tightest late-window cuts—S7 `18 s` at `98.7%` APV and S8 `17 s` at `104.3%` APV—hit ~100% APV cleanly).
2. **Compilation film (`m09jUdwC5hk`, window 21 Oct–18 Nov 2026): FAIL on discovery (`6` views, `94` impressions, `0.0%` CTR, `0` subs).**
   - Public and Studio views stalled at **`6`** by 1 Nov (`0` new views across 1–20 Nov). Retention (`33.8%` APV, `965 s` / `16:05` AVD, `48` watch minutes) is **inconclusive** (`n = 6 < 50`), though it confirms high watch-minutes per click (`8.0` min/view vs `0.38` min/view across the four 8–9 min longs) when a viewer actually opens a 48-minute film.
   - Confirms `studio/plan.json` (`longs-2026-11`): abstract-titled compilations do not get browse/search impressions on an 18-sub channel. Do not repeat unsearched compilation packaging; December's Journey (`ileYnHpLLCU`, 8 Dec) and Sleep (`13q4_EoLEN4`, 12 Dec) tests already switch to search-researched packaging with explicit 14-day keep/drop gates (`≥500` / `<230` views).
3. **Chief decision recommendation on S1–S8 Related videos:** Unlinked control ended 20 Nov. Recommend **staged, exact-match linking**—set Related now on active S8 `9q_OvQ1Rd8Y` → `c5AdqQsnnys` (and optionally interim `NbW5G1BpPY0` on active S7 `z5V6gIXXYs8`, or hold S7 for 034 Pluto on 13 Dec), bundle exact-match links for S6 → `T3cBBss1F60` (25 Nov), S4 → `oASsmqZfWU4` (9 Dec), and S7 → 034 Pluto (13 Dec) into those longs' launch passes, and skip dedicated Studio trips for plateaued S1/S2/S3/S5 (`+0` views/day; full table below).

### Cohort comparison summary (24 Oct–20 Nov 2026, plus 21 Oct–18 Nov compilation window)

*Sources: Studio views, Stayed %, APV, AVD from `studio_ctr.json` (read `2026-11-21T07:06Z`); day-1 Shorts-feed share, watch minutes, and subscribers gained from `snapshots/2026-11-20.json` (Analytics API settled through `2026-11-18`).*

| Cohort | n | Views total (mean / med) | Day-1 Feed ≥50% (mean / med) | Studio Stayed % mean / med (v-wtd) | Studio APV % mean / med (v-wtd) | Studio AVD mean / med (v-wtd) | Watch min (YTA) | Subs gained (YTA) |
|---|---:|---|---|---|---:|---:|---:|---:|
| **J0216 Standalone Shorts (S1–S8)** | 8 | **4,980** (`622.5` / `489.0`) | **7/8** (`85.6%` / `93.9%`) | `37.2%` / `35.9%` (`37.8%`) | `105.9%` / `75.7%` (`96.7%`) | `20.6 s` / `15.0 s` (`19.0 s`) | 627 | **+2** (`0.40`/1k) |
| **Cut-from-long Shorts — ALL** *(incl. Test A & 55 s len test)* | 10 | **5,041** (`504.1` / `499.5`) | **8/9**† (`84.4%` / `93.3%`) | `43.1%` / `37.8%` (`39.2%`) *(≥50v n=8: `39.7%` / `37.8%`)* | `82.8%` / `74.3%` (`86.8%`) *(≥50v: `85.1%`)* | `21.3 s` / `17.5 s` (`21.0 s`) | 787 | **+5** (`0.99`/1k) |
| **Cut-from-long Shorts — Standard only** *(excl. Test A & 55 s)* | 8 | **4,871** (`608.9` / `542.5`) | **7/7**† (`95.1%` / `95.2%`) | `41.9%` / `34.8%` (`38.9%`) *(≥50v n=6: `36.9%` / `34.8%`)* | `87.0%` / `78.2%` (`87.5%`) *(≥50v: `91.5%`)* | `20.2 s` / `16.0 s` (`20.9 s`) | 760 | **+5** (`1.03`/1k) |
| **Other non-J0216 standalone/dated Shorts** *(24 Oct–19 Nov)*‡ | 2 | **507** (`253.5` / `253.5`) | **1/1**† (`86.9%`) | `33.6%` / `33.6%` (`34.6%`) | `139.8%` / `139.8%` (`213.8%`) | `26.0 s` / `26.0 s` (`40.1 s`) | 119 | **0** |
| **Regular Longs (24 Oct–20 Nov)** | 4 | **267** (`66.8` / `18.0`) | n/a | n/a (CTR `1.9%–4.4%`, 1,597 imp) | `13.8%` / `13.8%` (`23.7%`) | `68.8 s` / `68.0 s` (`120.7 s`) | 101 | **0** |
| **Compilation Film (`m09jUdwC5hk`, 21 Oct–18 Nov)** | 1 | **6** (`6.0`) | n/a | n/a (`0.0%` CTR, 94 imp) | `33.8%` *(inconclusive, n=6)* | `965 s` (16:05) | 48 | **0** |
| *Context: All Shorts (21 Oct–18 Nov, comp window)* | 22 | **11,549** (`525.0` / `480.5`) | **19/21** (`85.3%` / `93.9%`) | `38.4%` / `35.0%` (`37.6%`) | `94.4%` / `74.0%` (`94.4%`) | `21.0 s` / `16.0 s` (`20.4 s`) | 1,636 | **+8** (`0.69`/1k) |

*Notes:*
- † `dH_yCRmzkMo` (aired 18 Nov, cut-from-long) and `HXacmpYkXcA` (aired 19 Nov, dated Supermoon) are inside the 48 h Analytics API lag in `2026-11-20.json` (`analytics.through = 2026-11-18`), so their YTA day-1 feed/subs rows are unsettled (6 h Studio launch checks: `dH_yCRmzkMo` `0/5` feed; `HXacmpYkXcA` `18/29` = `62.1%` feed).
- ‡ A third non-J0216 dated Short, `93JL_IK57EM` (*Will Asteroid 2024 YR4 Hit the Moon in 2032?*, 20 s), aired on `2026-11-20T11:30Z`—after the 06:40Z snapshot and before the 21 Nov `studio_ctr.json` table included it. Its 6 h launch check (`launch/93JL_IK57EM.json`) recorded `179` views, `156/179` (`87.2%`) Shorts feed, `43.8%` stayed, `88.6%` APV.
- Channel-wide `channel_daily.json` (settled through `2026-11-17`) recorded `10,712` views, `1,710` watch minutes, `+7` subs gained / `-4` lost (`+3` net) over 24 Oct–17 Nov, and `11,781` views, `1,814` watch minutes, `+8` gained / `-4` lost (`+4` net) over 21 Oct–17 Nov. Older pre-24-Oct regular longs added `+22` combined public views over 24 Oct–20 Nov (led by `55AEQwvs36g` `+11`).

---

### Per-Short Final Table: J0216 Standalone Cohort (S1–S8)

All 8 standalone Shorts cleared `≥100` Studio views (all judgeable). `Studio` columns come from `studio_ctr.json` (`2026-11-21T07:06Z`); `YTA` and `Day-1 Feed` come from `2026-11-20.json` (`through 2026-11-18`); `+1d / +7d` view velocity is public snapshot delta (`19→20 Nov` and `13→20 Nov`).

| Short | Live ID | Aired | Sec | Pub / Studio views | +1d / +7d | Day-1 Shorts feed (FED ≥50%) | Studio Stayed % | Studio APV % (YTA) | Studio AVD (YTA) | Watch min | Subs |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| **S1 Mercury** | `vlkj8RQKmH8` | 24 Oct | 21 s | 851 / 851 | +0 / +0 | **95.3%** (809/849 · FED) | 32.1% (MISS) | **76.1%** (76.1%) | 15 s (15 s) | 126 | 0 |
| **S2 Neptune** | `1OCNzhkiBuc` | 27 Oct | 21 s | 497 / 497 | +0 / +2 | **93.9%** (450/479 · FED) | 42.7% (MISS) | **75.3%** (75.3%) | 15 s (15 s) | 71 | 0 |
| **S3 ISS Sunrises** | `VfDm3E2bUgU` | 31 Oct | 19 s | 1,095 / 1,095 | +0 / +5 | **96.1%** (1,044/1,086 · FED) | 31.7% (MISS) | 67.6% (66.7%) | 12 s (12 s) | 112 | 0 |
| **S4 Uranus** | `ZpEA8stoSPA` | 03 Nov | 22 s | 481 / 481 | +0 / +0 | **93.9%** (450/479 · FED) | 26.9% (MISS) | **306.8%** (306.8% · LOOP) | 67 s (67 s) | 88 | **+2** |
| **S5 Shooting Stars** | `T9fVlG3CCzU` | 07 Nov | 21 s | 1,286 / 1,286 | +0 / +1 | **91.8%** (1,160/1,263 · FED) | **49.8%** (WATCH) | 66.3% (66.2%) | 13 s (13 s) | 157 | 0 |
| **S6 Titan** | `ffYKoNVPoqg` | 10 Nov | 19 s | 110 / 110 | +3 / +16 | 36.6% (26/71 · NOT FED*) | **46.9%** (WATCH) | 52.0% (52.7%) | 9 s (10 s) | 10 | 0 |
| **S7 Pluto Heart** | `z5V6gIXXYs8` | 13 Nov | 18 s | 380 / 380 | +12 / +380 | **83.5%** (284/340 · FED) | 39.6% (MISS) | **98.7%** (100.0% · PASS) | 17 s (17 s) | 41 | 0 |
| **S8 Voyager 1** | `9q_OvQ1Rd8Y` | 17 Nov | 17 s | 281 / 280 | +13 / +281 | **93.9%** (215/229 · FED) | 27.7% (MISS) | **104.3%** (95.2% · LOOP) | 17 s (16 s) | 22 | 0 |
| **S1–S8 Total / Summary** | **8 live** | 24 Oct–17 Nov | 17–22 s | **4,981 / 4,980** | +28 / +685 | **7/8 FED** (mean 85.6%, med 93.9%) | **37.2%** mean (`37.8%` wtd) | **105.9%** mean (`96.7%` wtd, med `75.7%`) | **20.6 s** mean (med `15.0 s`) | **627** | **+2** |

*\*S6 Titan (`ffYKoNVPoqg`) received 43 day-1 `YT_SEARCH` views vs 26 `SHORTS` feed views (77 search vs 27 feed in `last28`). S8 (`9q_OvQ1Rd8Y`) had 229 YTA views settled through 18 Nov vs 281 public / 280 Studio views by 21 Nov 07:06Z (3.8 days old).*

### Comparator Table: Non-J0216 Shorts (24 Oct–20 Nov 2026)

| Date | Type | ID | Sec | Title | Pub / Studio views | Day-1 Shorts feed | Studio Stayed % | Studio APV % | Studio AVD | Subs (YTA) |
|---|---|---|---:|---|---:|---|---:|---:|---:|---:|
| 26 Oct | Cut (027) | `OVLv9dxTcpE` | 22 s | What If Earth Stopped Spinning? | 892 / 892 | 98.2% (870/886 · FED) | 30.7% | 75.9% | 16 s | 0 |
| 28 Oct | Dated/SA (030) | `gJwNJN_yMKU` | 19 s | How Close Will Asteroid Apophis Pass Earth on Friday the 13th? | 464 / 464 | 86.9% (391/450 · FED) | 34.8% | 228.9% | 43 s | 0 |
| 29 Oct | Cut (023) | `_a66uhRDips` | 18 s | Why Is Venus Hot Enough to Melt Lead? | 519 / 519 | 95.2% (492/517 · FED) | 32.8% | 91.7% | 16 s | **+2** |
| 30 Oct | Cut (021) | `6dcL5rBmHPM` | 23 s | How Thin Are Saturn's Rings? | 45 / 45 | 93.2% (41/44 · FED) | 21.7% (<50v) | 66.7% | 15 s | 0 |
| 02 Nov | Cut (023) | `hZH0C7fpCk4` | 20 s | How Big Is Venus Compared to Earth? | 566 / 566 | 93.3% (519/556 · FED) | 31.6% | 66.2% | 13 s | 0 |
| 09 Nov | Cut (025) | `iyvWYFP_ETA` | 26 s | Could a Robot Survive a Night on Mars? | 1,074 / 1,074 | 95.8% (1,016/1,061 · FED) | 38.8% | 62.7% | 16 s | **+1** |
| 11 Nov | Cut Test A (025) | `B1z2dv7m7Vk` | 27 s | Why Did a 90-Day Mars Rover Last 14 Years? | 110 / 110 | 51.7% (46/89 · FED) | 52.7% | 72.7% | 19 s | 0 |
| 12 Nov | Cut 55 s test (025) | `uhZSRcvngvE` | 55 s | How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years? | 60 / 60 | 42.6% (23/54 · NOT FED) | 43.2% | 59.0% | 32 s | 0 |
| 14 Nov | Cut (025) | `RT-ec4_GcOk` | 27 s | How Did a Helicopter Fly 72 Times on Mars? | 1,269 / 1,269 | 97.7% (1,204/1,232 · FED) | 50.7% | 100.9% | 27 s | **+2** |
| 16 Nov | Cut (026) | `aEfdxex__Bo` | 27 s | If You Can't See the Nearest Star, How Far Away Is It? | 480 / 480 | 92.0% (423/460 · FED) | 36.8% | 151.7% | 40 s | 0 |
| 18 Nov | Cut (026) | `dH_yCRmzkMo` | 24 s | If Voyager Needs 75,000 Years, How Far Is the Nearest Star? | 24 / 26 | unsettled (6 h: 0/5) | 91.7% (<50v) | 80.6% | 19 s | unsettled |
| 19 Nov | Dated/SA | `HXacmpYkXcA` | 19 s | How Close Will the Supermoon Get on November 24? | 34 / 43 | unsettled (6 h: 18/29 = 62.1%) | 32.4% (<50v) | 50.7% | 9 s | unsettled |
| 20 Nov | Dated/SA (AR1) | `93JL_IK57EM` | 20 s | Will Asteroid 2024 YR4 Hit the Moon in 2032? | *6 h: 179* | *6 h: 87.2% (156/179)* | *6 h: 43.8%* | *6 h: 88.6%* | — | unsettled |

### Comparator Table: Longs & Compilation Film (21 Oct–20 Nov 2026)

| Date | Type | ID | Duration | Title | Views (Pub / Studio) | Impressions / CTR | Studio APV % | Studio AVD | Watch min (YTA) | Subs (YTA) | `SHORTS_CONTENT_LINKS` (28 d) |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **21 Oct** | **Compilation** | **`m09jUdwC5hk`** | **47:38 (2858 s)** | **How Long Will Anything in Space Last?** | **6 / 6** | **94 / 0.0%** | **33.8%** *(n=6)* | **965 s (16:05)** | **48** | **0** | 0 |
| 25 Oct | Regular long (023) | `VBaYRPp85Sw` | 8:34 (514 s) | What Happened to Venus? | 230 / 230 | 1,327 / 2.0% | 25.2% | 129 s | 84 | 0 | 1 |
| 01 Nov | Regular long (024) | `rVqgtkBV3jc` | 8:12 (492 s) | What Happens If You Travel Near Light Speed? | 1 / 1 | 54 / 1.9% | 2.2% | 10 s | 0 | 0 | 0 |
| 08 Nov | Regular long (025) | `Js6EQJ8qDi8` | 8:11 (491 s) | Could a Robot Survive on Mars? (One Lasted 14 Years) | 24 / 24 | 193 / 3.1% | 15.5% | 76 s | 16 | 0 | 0 |
| 15 Nov | Regular long (026) | `c5AdqQsnnys` | 8:15 (495 s) | How Far Is the Nearest Star? (You Can't See It, and It Has a Planet) | 12 / 12 | 23 / 4.4% | 12.2% | 60 s | 1 | 0 | 0 |

#### Compilation trajectory (`m09jUdwC5hk`, 21 Oct–18 Nov window)
- `22 Oct`: 2 views (YTA unsettled) → `24 Oct`: 3 views (`35 s` AVD, `1.25%` APV) → `28 Oct`: 5 public / 4 YTA views (`19 s` AVD, `0.67%` APV) → `01 Nov`: 6 views (`965 s` AVD, `33.77%` APV, `48` watch min) → **`08 / 15 / 18 / 19 / 20 Nov`: flat at 6 views, 48 watch min, 0 subs**.
- Last-28-day traffic sources (4 matched views): `NO_LINK_OTHER` 1, `SUBSCRIBER` 1, `YT_SEARCH` 1, `RELATED_VIDEO` 1.

---

## Chief Decision Recommendation: S1–S8 Related Videos

**Policy context:** `studio/RULES.md` (lesson 5, *Keeper score*) kept S1–S8 unlinked only *"until 20 Nov"*. With the test window closed, the hold is expired. Live public-page verification in `05_Analytics/live_fixes/2026-11-21.md` (`09:00Z`) confirmed `9q_OvQ1Rd8Y` and `z5V6gIXXYs8` currently serve **no** Related pill (`reelCarouselButtonViewModel` absent; note that `05_Analytics/owb/STUDIO_SETTINGS_AUDIT_2026-11-21.md` line 84 erroneously wrote "Related video set" for `9q_OvQ1Rd8Y`).

**Empirical reality check:**
- Only **3 of 8** standalone Shorts are still receiving daily views as of 20 Nov: **S8 `9q_OvQ1Rd8Y`** (`+13/day`), **S7 `z5V6gIXXYs8`** (`+12/day`), and **S6 `ffYKoNVPoqg`** (`+3/day`, `+16/7d` search tail). **S1–S5** all recorded **`+0` views in the last 24 h** and `0–5` views over the last 7 days combined.
- Across all 4 regular longs published in the window (backed by ~5,000 linked cut-from-long Short views), YouTube Analytics logged only **`1` `SHORTS_CONTENT_LINKS` view** total (`VBaYRPp85Sw`: 1; others: 0). Adding Related links to dead-tail Shorts has near-zero immediate return, whereas linking active Shorts and exact-match upcoming longs aligns topic clusters cleanly with zero wasted Studio work.
- **Three of S1–S8 have exact-match longs scheduled/planned within 3 weeks:** S6 Titan → `T3cBBss1F60` (25 Nov), S4 Uranus → `oASsmqZfWU4` (9 Dec), S7 Pluto Heart → 034 Pluto (13 Dec).

### Recommended Chief ruling: Staged exact-match linking (not a 8-video bulk pass today)

| Priority & Timing | Short | Live ID | Recent velocity (+1d / +7d) | Recommended Related target | Rationale |
|---|---|---|---|---|---|
| **1. Set NOW** (active Short, strong live match) | **S8 Voyager 1** | `9q_OvQ1Rd8Y` | `+13 / +281` | **`c5AdqQsnnys`** (026 *How Far Is the Nearest Star?*, public 15 Nov) | Active tail; directly about Voyager 1's interstellar distance (same parent long as 026 Short `dH_yCRmzkMo`). |
| **1b. Set NOW (interim) OR hold for 13 Dec** | **S7 Pluto Heart** | `z5V6gIXXYs8` | `+12 / +380` | Interim **`NbW5G1BpPY0`** (*Europa Ice Ocean*, closest live icy-world long) now → **re-point to 034 Pluto on 13 Dec** *(or hold until 13 Dec for a single Studio touch)* | Active tail (`+12/day`). Lean: set interim `NbW5G1BpPY0` in the same Studio pass as S8, then re-point to exact-match 034 Pluto when it airs on 13 Dec. |
| **2. Set on 25 Nov** (bundle into 032 launch) | **S6 Titan** | `ffYKoNVPoqg` | `+3 / +16` | **`T3cBBss1F60`** (032 *What Would Happen If You Landed on Titan?*, airs Wed 25 Nov 18:00Z) | Exact subject match goes public in 4 days; hold 4 days instead of adding a throwaway interim link. |
| **3. Set on 9 Dec** (bundle into 033 launch) | **S4 Uranus** | `ZpEA8stoSPA` | `+0 / +0` | **`oASsmqZfWU4`** (033 *Why Knocked-Sideways Uranus Has 21-Year Winters*, airs Wed 9 Dec 18:00Z) | Plateaued (`0` views/7d); wait for exact-match 033 Uranus on 9 Dec. |
| **4. Optional / opportunistic only** (plateaued; no dedicated Studio trip) | **S3 ISS** | `VfDm3E2bUgU` | `+0 / +5` | **`6bbbvfCx6zY`** (027 *What If Earth Stopped Spinning?*, airs Sun 22 Nov 18:00Z) | Closest orbital/day-length match once 027 is public; bundle only if already in Studio. |
| **4. Optional / opportunistic only** | **S1 Mercury**, **S2 Neptune** | `vlkj8RQKmH8`, `1OCNzhkiBuc` | `+0 / +0`, `+0 / +2` | **064** *Every Planet Explained in 10 Minutes* (airs Wed 16 Dec) | No dedicated live Mercury/Neptune long (`035`/`036` paused under Rule 34); 064 covers all eight planets. |
| **4. Optional / opportunistic only** | **S5 Shooting Stars** | `T9fVlG3CCzU` | `+0 / +1` | **`VBaYRPp85Sw`** (023 *What Happened to Venus?*, 230 views) or **`ileYnHpLLCU`** (J01 Journey, 8 Dec) | Plateaued; `VBaYRPp85Sw` already holds Related links for standalone asteroid Shorts (`gJwNJN_yMKU`, `93JL_IK57EM`). |

*(Note: when any S1–S8 Related video is set in Studio under a Chief-approved job, update its row in `00_Brand/Channel-Setup/social/UPLOADS.json` with `relatedStatus: "set"`, `relatedVideoId`, and `relatedJob`. Separately, `dH_yCRmzkMo` and `aEfdxex__Bo` still show `relatedStatus: "pending_studio"` in `UPLOADS.json` despite live verification to `c5AdqQsnnys` in `2026-11-21.md`.)*

---

## Historical Early Readout: S1 Mercury (J0919 · 24 Oct 2026, ~9.5 h live)

Preserved from the day-1 diagnostic pass that drove the v02–v11 re-cuts of S2, S3, S6, S7, and S8:

### S1 Mercury — `vlkj8RQKmH8` (*Why Does a Day on Mercury Last Two of Its Years?*)
- **Published:** `2026-10-24T10:30:22Z` (Sat 24 Oct 11:30 BST). Early read at `2026-10-24T20:01Z` (~9.5 h live; final 4-week metrics in the S1–S8 table above: `851` views, `95.3%` day-1 feed, `32.1%` stayed, `76.1%` APV, `15 s` AVD, `0` subs).
- **Early 9.5 h Views & Engagement (`studio_ctr.json` + Studio + Data API):**
  - **Studio views:** **837** (+777 vs typical; **#2 Short on OWB** at the time behind `n_4XskX0yZk` at 881) | **Public Data API views:** **813** (5 likes, 0 comments)
  - **Engaged views:** **282** (~876 shown in feed) · **Watch time:** **1.4 hours** (+0.4 vs typical)
  - **Stayed to watch vs Swiped away:** **32.2% stayed / 67.8% swiped** → **`MISS`** vs the **60%+** stayed-to-watch target (`<45%` MISS).
  - **Average view duration / Average % viewed:** **0:15 AVD** on `20.44 s` master (**73.4%**; `71.4%` on YouTube's rounded `21 s`) → **`PASS`** vs the **70%+** average-viewed target.
  - **Traffic sources (Studio Reach, since published):** **Shorts feed 95.6%** (**FED**, well above `≥50%`), **YouTube search 2.6%**, **Other YouTube features 1.4%**, **External 0.4%**.
- **Cut-by-cut & word-by-word drop analysis (`06_Final-Exports/owb_sa_s1_mercury_v01_meta.json` + `owb_sa_s1_mercury_vo_v01_trim_words.json`):**
  1. **Drop #1 — 0.0–5.5 s initial swipe (`67.8%` swiped away, `32.2%` stayed):**
     - **On screen (`0.0–5.5 s`, Row 1 `s1_mercury/PIA11351.jpg`):** Static grey MESSENGER limb photo `PIA11351.jpg` with the top ~45% black sky, pushed only `1.00 -> 1.04` over `5.5 s`, with top hook caption `ONE DAY, / TWO YEARS` (yellow `DAY,`, `0.0–2.2 s`). No moving video on frame 0, zoom `<=1.10`, and first cut held to `5.5 s` (vs `<=3.0 s` rule).
     - **Said (`0.08–5.16 s`):** `"On"` (`0.08–0.16 s`), `"Mercury,"` (`0.22–0.72 s`), `[0.40 s pause: 0.72–1.12 s]`, `"one day lasts two years."` (`1.12–3.20 s` — surprise words `"two years"` land at `2.44–3.20 s`, past the `1.5 s` bar), `[0.40 s pause: 3.20–3.60 s]`, `"Stay, and I'll show you how."` (`3.60–5.16 s` — meta-promise filler), `[0.40 s pause: 5.16–5.56 s]`.
  2. **Body hold — 5.5–15.1 s (Row 2 `PIA14083.jpg` `5.5–9.7 s` & Row 3 `PIA12266.jpg` `9.7–15.1 s`):**
     - **On screen:** Colorized globe `PIA14083.jpg` (`zoom 1.05 -> 1.15`, `5.5–9.7 s`), then surface still `PIA12266.jpg` (`zoom 1.00 -> 1.10`, `9.7–15.1 s`, `5.4 s` hold `>4.0 s`), mid-video title banner `A Day on Mercury Lasts Two Years` (`9.0–14.0 s`), and fact card `176 / EARTH DAYS` ticking in at `14.05 s` (`14.0–17.2 s`).
     - **Said:** `"Mercury races round the sun every 88 Earth days,"` (`5.56–9.30 s`), `"but it spins so slowly, sunrise to sunrise takes 176."` (`9.70–14.74 s`; `"176"` spoken `13.42–14.74 s`).
  3. **Drop #2 — ~15.0 s average exit (`0:15` Studio AVD, `73.4%` viewed) & 17.44–20.44 s tail:**
     - **On screen & said (`14.74–20.44 s`):** Viewers who stay past the swipe hold through the `"176"` numeric answer (`13.42–14.74 s`, `72.1%` of runtime) and exit around **`~15.0 s`** as Row 3 cuts to Row 4 (`PIA13674.jpg`, `15.1–17.44 s`, `"Two trips round the sun before it's morning again"` `15.14–17.44 s`), followed by a **`3.00 s` silent VO tail (`17.44–20.44 s`, Row 5 `PIA11351.jpg` loop crossfade)** — double the `<=1.5 s` last-word-to-loop ceiling and without a sentence seam looping into line 1.
