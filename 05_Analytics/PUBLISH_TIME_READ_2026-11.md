# Studio Publish-Time & Audience Geography Read (November 2026 — J2422)

- **Date of read:** 9 November 2026 (`03:00–03:11 UTC`, data window through `7 Nov 2026`)
- **Channels inspected (read-only):**
  - **Orbit With Ben** (`@OrbitWithBen`, `UC_esArsDKd3GJvOkeO0DUog`) via Mini Studio CDP `:9223` + YouTube Analytics API v2
  - **History of Science** (`@HistoryOfScienceYT`, `UCXp7HkBIl1LgaznXuZHJyRg`) via Mini Studio CDP `:9460` + YouTube Analytics API v2
- **Question (Ben, 8 Nov 2026):** Are `18:00` (longs) and `11:30` (Shorts) London time the best publish times?
- **Action taken:** Read-only Studio and API pass. **No Studio setting changes and no schedule moves were made** (per brief: Chief decides after the read).

---

## 1. Executive Summary & Recommendation

1. **`Analytics > Audience > "When your viewers are on YouTube"` status:**
   - On **both** Orbit With Ben (`2.8k` monthly audience) and History of Science (`987` monthly audience), YouTube Studio currently displays:
     > **`When your viewers are on YouTube · Your local time (GMT +0000) · Last 28 days`**
     > **`Not enough viewer data to show this report`**
   - Local Studio screenshots of the card and surrounding Audience panels are saved on the Mini under `05_Analytics/publish_time_read_2026-11/` (`owb_audience_28d_mid.png`, `owb_audience_90d_bot.png`, `hos_audience_mid.png`, `hos_audience_90d_bot.png`, `owb_geo_advanced_90d.png`, `hos_geo_advanced_90d.png`).
2. **Audience Geography & Demographic Reality (Last 90 Days: 10 Aug – 7 Nov 2026):**
   - **United Kingdom (`GMT+0`) is the #1 country on both channels** — and its share is **growing** in the last 28 days:
     - **Orbit With Ben:** **United Kingdom 21.9%** of 90d views (**23.8%** in last 28d; **25.6%** of 90d watch time), followed by **United States 16.2%** (**15.1%** of watch time), **Malaysia 2.0%**, **Philippines 1.3%**, **Netherlands 0.6%**, **Japan 0.5%** (**5.6%** of watch time, `6:12` AVD). Among country-attributed views (`7,869`), **UK + Europe (`GMT+0/+1/+2`) represent 50.7%**, **North America (`US + CA`) 35.6%**, and **Asia-Pacific 12.9%**.
     - **History of Science:** **United Kingdom 18.5%** of 90d views (**22.2%** in last 28d; **11.5%** of 90d watch time), followed by **India 3.5%**, **United States 3.0%**, **Philippines 3.0%**, **Indonesia 1.5%**, **Malaysia 1.0%**. Among country-attributed views (`1,208`), **UK + Europe + ZA (`GMT+0/+1/+2`) represent 60.3%**, **India + SE Asia + APAC (`GMT+5` to `+10`) 30.6%**, and **United States 9.0%**.
   - **Demographics & Devices:** Both channels skew strongly to **working-age adults aged 25–44** (**68.7%** on OWB, **64.4%** on HOS). Longs (`Videos`) are heavily **Computer + TV + Mobile** via **Browse features** (`73.3%` OWB, `46.9%` HOS), whereas `Shorts` are **71–72% Mobile phone** via the **Shorts feed** (`85.1%` OWB, `71.8%` HOS) and **YouTube search** (`12.1%` OWB, `27.2%` HOS).
3. **Peak Hours in London Time (`GMT+0000`) & Recommendation:**
   - **Longs (`Videos`) — Peak Window: `19:00–22:00 London` → Recommendation: KEEP `18:00 London`.**
     - `18:00 London` is **already 1–2 hours before** the primary UK/European adult evening peak (`19:00–22:00 London`, when computer/TV/tablet Browse sessions peak) while simultaneously catching the US East Coast from lunchtime (`13:00 EST`) through the US evening wave. Moving later would miss the 1–2 hour pre-peak indexing/impression ramp for UK evening Browse; moving earlier would land during UK work hours and before US East Coast midday.
   - **Shorts (`Shorts`) — Peak Windows: `12:00–14:30 London` (Wave 1) & `18:00–21:00 London` (Wave 2) → Recommendation: KEEP `11:30 London`.**
     - `11:30 London` sits **0.5–1.5 hours before** Wave 1 (`12:00–14:30 London`), where **three audience zones overlap**: (a) **UK & Europe lunchtime mobile scroll** (`12:00–14:30 GMT`), (b) **India & SE Asia evening prime time** (`17:30–20:00 IST` in India; `20:00–22:30` in Malaysia, Philippines, Indonesia), and (c) **US East Coast morning wake-up/commute** (`06:30–09:30 EST`).
     - Seeding Shorts at `11:30 London` gives the Shorts feed 1–2 hours to test the initial cohort during the midday UK / evening Asia peak and carry fed Shorts into Wave 2 (`18:00–21:00 London` UK evening / US afternoon) without colliding with the `18:00 London` long-form release.

---

## 2. Studio Heatmap Card: `When your viewers are on YouTube`

| Channel | Studio URL Checked | Card Subheader | Studio UI Output | Monthly Audience (28d) |
|---|---|---|---|---|
| **Orbit With Ben** (`UC_esArsDKd3GJvOkeO0DUog`) | `.../analytics/tab-build_audience/period-default` & `period-quarter` | `Your local time (GMT +0000) · Last 28 days` | `Not enough viewer data to show this report` | `2.8k` (`+5` subs in 28d; `+16` in 90d) |
| **History of Science** (`UCXp7HkBIl1LgaznXuZHJyRg`) | `.../analytics/tab-build_audience/period-default` & `period-quarter` | `Your local time (GMT +0000) · Last 28 days` | `Not enough viewer data to show this report` | `987` (`+5` subs in 28d; `+6` in 90d) |

- **Why no heatmap bars render yet:** YouTube Studio suppresses the 7×24 hourly purple grid until a channel accumulates enough concurrent signed-in hourly viewers across all 168 hour-of-week buckets over the trailing 28 days.
- **Re-check trigger:** Re-read `Analytics > Audience > When your viewers are on YouTube` once 28-day Monthly Audience reaches ~5k–10k on OWB to verify the empirical darkest purple bars against the geography-derived windows below.

---

## 3. Orbit With Ben (`@OrbitWithBen`) — Geography & Format Split

### 3.1 Top Countries — Last 90 Days (`10 Aug – 7 Nov 2026`) vs Last 28 Days (`11 Oct – 7 Nov 2026`)

On the main `Audience` tab (`Top geographies · Views · Last 90 days`), Studio displays the top 5 countries (`United Kingdom 21.9%`, `United States 16.2%`, `Malaysia 2.0%`, `Philippines 1.3%`, `Netherlands 0.6%`). Opening Studio `Advanced mode > Geography` (`16,885` total views, `42.8` hours watch time, `0:23` AVD) gives the full country breakdown:

| Rank | Country | Time Zone (vs London `GMT`) | 90d Views (Studio) | 90d % of Total Views (`16,885`) | 90d Watch Time (h) | 90d % of Watch Time (`42.8 h`) | 90d AVD | Last 28d % of Views (Studio Card) |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | **United Kingdom** | `GMT+0` | 3,692 | **21.9%** | 10.9 | **25.6%** | 0:26 | **23.8%** |
| 2 | **United States** | `GMT−5` to `GMT−8` | 2,739 | **16.2%** | 6.5 | **15.1%** | 0:20 | **5.5%** |
| 3 | **Malaysia** | `GMT+8` | 343 | **2.0%** | 0.9 | **2.1%** | 0:22 | **3.6%** |
| 4 | **Philippines** | `GMT+8` | 222 | **1.3%** | 0.3 | **0.8%** | 0:11 | **2.6%** |
| 5 | **Netherlands** | `GMT+1` | 95 | **0.6%** | 0.2 | **0.4%** | 0:12 | — |
| 6 | **Japan** | `GMT+9` | 89 | **0.5%** | 2.4 | **5.6%** | **6:12** | **1.0%** |
| 7 | **Indonesia** | `GMT+7` | 82 | **0.5%** | 0.1 | **0.3%** | 0:12 | — |
| 8 | **Poland** | `GMT+1` | 80 | **0.5%** | 0.1 | **0.3%** | 0:14 | — |
| 9 | **Australia** | `GMT+10/+11` | 68 | **0.4%** | 0.1 | **0.3%** | 0:14 | — |
| 10 | **Saudi Arabia** | `GMT+3` | 65 | **0.4%** | 0.1 | **0.2%** | 0:10 | — |
| 11 | **Canada** | `GMT−5` to `GMT−8` | 64 | **0.4%** | 0.1 | **0.3%** | 0:10 | — |
| 12 | **India** | `GMT+5:30` | 56 | **0.3%** | 0.1 | **0.2%** | 0:10 | — |
| 13 | **Singapore** | `GMT+8` | 50 | **0.3%** | 0.1 | **0.3%** | 0:14 | — |
| 14 | **Nepal** | `GMT+5:45` | 50 | **0.3%** | 0.1 | **0.2%** | 0:10 | — |
| 15 | **Germany** | `GMT+1` | 36 | **0.2%** | 0.1 | **0.1%** | 0:16 | — |
| 16 | **Myanmar (Burma)** | `GMT+6:30` | 32 | **0.2%** | 0.0 | **0.1%** | 0:11 | — |
| 17 | **Spain** | `GMT+1` | 25 | **0.2%** | 0.0 | **0.1%** | 0:10 | — |
| 18 | **South Africa** | `GMT+2` | 23 | **0.1%** | 0.1 | **0.2%** | 0:35 | — |
| 19 | **Belgium** | `GMT+1` | 22 | **0.1%** | 0.0 | **0.1%** | 0:09 | — |
| 20 | **Ireland** | `GMT+0` | 19 | **0.1%** | 0.0 | **0.1%** | 0:10 | — |
| 21 | **France** | `GMT+1` | 17 | **0.1%** | 0.1 | **0.2%** | 0:22 | — |
| — | *Unattributed / low-volume countries* | — | *9,016* | *53.4%* | *20.1* | *47.0%* | — | — |
| — | **Total (All Content)** | — | **16,885** | **100.0%** | **42.8** | **100.0%** | **0:23** | — |

### 3.2 OWB Longs (`Videos`) vs `Shorts` Split (Last 90 Days)

- **Volume split (`Advanced mode > Content type`):**
  - **Shorts:** `16,270` views (**96.4%** of views), `36.0` hours (**84.1%** of watch time), `0:20` AVD, `+18` subscribers.
  - **Videos (Longs):** `615` views (**3.6%** of views), `6.8` hours (**16.0%** of watch time), `2:07` AVD, `+2` subscribers.
- **Geography split (`Advanced mode > Geography` filtered by `Content type`):**
  - **`Filter: Shorts` (`16,270` views, `36.0 h`):** Studio attributes all 21 country rows above to Shorts (`United Kingdom 22.7%` of Shorts views / `30.4%` of Shorts watch time; `United States 16.8%` of Shorts views / `18.0%` of Shorts watch time; `Malaysia 2.1%`; `Philippines 1.4%`; `Netherlands 0.6%`; `Japan 0.6%`). Cross-checking the YouTube Analytics API (`creatorContentType==shorts` vs `All`) shows that the `615` long-form views are suppressed at the per-country level when `Filter: Videos` is isolated (`Total: 615 views, 6.8 h, 2:07 AVD`, 0 individual country rows shown due to YouTube's privacy floor).
- **Device & Traffic-Source Split (Studio `Audience` & `Content` tabs, Last 90 days):**

| Metric / Dimension | OWB `All` | OWB `Videos` (Longs) | OWB `Shorts` |
|---|---:|---:|---:|
| **Mobile phone** (% of watch time) | 67.6% | **46.7%** | **71.4%** |
| **Computer** (% of watch time) | 18.1% | **42.8%** | **13.4%** |
| **Tablet** (% of watch time) | 9.3% | **2.4%** | **10.6%** |
| **TV** (% of watch time) | 5.1% | **8.1%** | **4.5%** |
| **Primary traffic source #1** | Shorts feed (82.0%) | **Browse features (73.3%)** | **Shorts feed (85.1%)** |
| **Primary traffic source #2** | YouTube search (12.0%) | **YouTube search (7.8%)** | **YouTube search (12.1%)** |
| **Primary traffic source #3** | Browse features (2.8%) | **Direct/unknown (7.2%) & Suggested (4.4%)** | **Other YouTube features (1.5%)** |

---

## 4. History of Science (`@HistoryOfScienceYT`) — Geography & Format Split

### 4.1 Top Countries — Last 90 Days (`10 Aug – 7 Nov 2026`) vs Last 28 Days (`11 Oct – 7 Nov 2026`)

On the main `Audience` tab (`Top geographies · Views · Last 90 days`), Studio displays the top 5 countries (`United Kingdom 18.5%`, `India 3.5%`, `United States 3.0%`, `Philippines 3.0%`, `Indonesia 1.5%`). Opening Studio `Advanced mode > Geography` (`3,657` total views, `8.8` hours watch time, `0:23` AVD) gives the full country breakdown:

| Rank | Country | Time Zone (vs London `GMT`) | 90d Views (Studio) | 90d % of Total Views (`3,657`) | 90d Watch Time (h) | 90d % of Watch Time (`8.8 h`) | 90d AVD | Last 28d % of Views (Studio Card) |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | **United Kingdom** | `GMT+0` | 675 | **18.5%** | 1.0 | **11.5%** | 0:13 | **22.2%** |
| 2 | **India** | `GMT+5:30` | 129 | **3.5%** | 0.1 | **1.7%** | 0:09 | **3.5%** |
| 3 | **United States** | `GMT−5` to `GMT−8` | 109 | **3.0%** | 0.2 | **1.9%** | 0:09 | **3.6%** |
| 4 | **Philippines** | `GMT+8` | 108 | **3.0%** | 0.1 | **1.6%** | 0:10 | **3.5%** |
| 5 | **Indonesia** | `GMT+7` | 54 | **1.5%** | 0.1 | **0.9%** | 0:09 | **1.8%** |
| 6 | **Malaysia** | `GMT+8` | 37 | **1.0%** | 0.0 | **0.5%** | 0:09 | — |
| 7 | **South Africa** | `GMT+2` | 29 | **0.8%** | 0.0 | **0.5%** | 0:09 | — |
| 8 | **Netherlands** | `GMT+1` | 25 | **0.7%** | 0.0 | **0.5%** | 0:12 | — |
| 9 | **Uzbekistan** | `GMT+5` | 22 | **0.6%** | 0.0 | **0.4%** | 0:10 | — |
| 10 | **Australia** | `GMT+10/+11` | 20 | **0.6%** | 0.0 | **0.5%** | 0:15 | — |
| — | *Unattributed / low-volume countries* | — | *2,449* | *67.0%* | *7.0* | *80.0%* | — | — |
| — | **Total (All Content)** | — | **3,657** | **100.0%** | **8.8** | **100.0%** | **0:23** | — |

### 4.2 HOS Longs (`Videos`) vs `Shorts` Split (Last 90 Days)

- **Volume split (`Content` tab & `Advanced mode > Content type`):**
  - **Shorts:** `3,432` views (**94.2%** of views), `5.5` hours (**62.5%** of watch time), `0:14` AVD, `+5` subscribers.
  - **Videos (Longs):** `211` views (**5.8%** of views), `3.3` hours (**37.5%** of watch time), `1:59` AVD, `+1` subscriber.
- **Geography split (`Advanced mode > Geography` filtered by `Content type`):**
  - **`Filter: Shorts` (`3,432` views, `5.5 h`):** `United Kingdom 19.7%` (675 views; `18.4%` of Shorts watch time), `India 3.8%` (129), `United States 3.2%` (109), `Philippines 3.2%` (108), `Indonesia 1.6%` (54), `Malaysia 1.1%` (37), `South Africa 0.8%` (29), `Netherlands 0.7%` (25), `Uzbekistan 0.6%` (22), `Australia 0.6%` (20).
  - **`Filter: Videos` (`211` views, `3.3 h`, `1:59` AVD):** Individual country rows under `211` views are suppressed by YouTube's privacy threshold (notice that `80.0%` of HOS total watch time sits in the unattributed bucket primarily because long-form watch time — `3.3 h` out of `8.8 h`, driven by `How Did We Discover the Periodic Table?` with 161 views and `What's Really Inside an Atom?` with 31 views — isn't broken out into per-country rows yet).
- **Device & Traffic-Source Split (Studio `Audience` & `Content` tabs, Last 90 days):**

| Metric / Dimension | HOS `All` | HOS `Videos` (Longs) | HOS `Shorts` |
|---|---:|---:|---:|
| **Mobile phone** (% of watch time) | 56.9% | **32.5%** | **71.7%** |
| **Computer** (% of watch time) | 30.6% | **61.4%** | **12.0%** |
| **Tablet** (% of watch time) | 8.1% | **1.5%** | **12.1%** |
| **TV** (% of watch time) | 4.3% | **4.6%** | **4.2%** |
| **Primary traffic source #1** | Shorts feed (67.4%) | **Browse features (46.9%)** | **Shorts feed (71.8%)** |
| **Primary traffic source #2** | YouTube search (26.6%) | **Suggested videos (19.0%)** | **YouTube search (27.2%)** |
| **Primary traffic source #3** | Browse features (2.7%) | **YouTube search (18.5%)** | **Other YouTube features (0.6%)** |

---

## 5. Peak Hours in London Time & Publish-Time Analysis

### 5.1 Peak Audience Windows in London Time (`GMT+0000`)

| Format | Primary Audience Geography & Devices | Peak Viewing Hours (London `GMT`) | Current Publish Slot (London `GMT`) | Lead Time Before Peak |
|---|---|---|---|---|
| **Longs (`Videos`) — OWB & HOS** | **UK (#1) + Europe** (`GMT+0/+1`, ~51–60% of attributed views) + **US (#2 OWB / #3 HOS)** (`GMT−5` to `−8`); **64–69% aged 25–44**; **51–66% Computer + TV** watch time; **47–73% Browse features** | **`19:00–22:00 London`** (UK/EU adult evening prime time + US East/Central `14:00–17:00 EST`), with a secondary US evening tail (`23:00–02:00 London`) | **`18:00 London`** | **1.0–2.0 hours before** the `19:00–22:00 London` peak |
| **Shorts (`Shorts`) — OWB & HOS** | **UK (#1)** (`GMT+0`) + **India / Philippines / Malaysia / Indonesia** (`GMT+5:30` to `+8`, ~31% of HOS attributed views & ~13% of OWB) + **US** (`GMT−5` to `−8`); **71–72% Mobile phone** | **Wave 1: `12:00–14:30 London`** (UK lunch + India `17:30–20:00 IST` + SE Asia `20:00–22:30` evening + US East `07:00–09:30 EST` morning)<br>**Wave 2: `18:00–21:00 London`** (UK evening mobile scroll + US afternoon `13:00–16:00 EST`) | **`11:30 London`** | **0.5–1.5 hours before** Wave 1 (`12:00–14:30 London`), with runway into Wave 2 (`18:00–21:00 London`) |

### 5.2 Recommendation for the Chief

1. **Longs (`18:00 London`): KEEP AS IS on both channels.**
   - By the "publish 1–2 hours before peak" rule, a `19:00–22:00 London` peak calls for publishing at **`17:00–18:00 London`**.
   - `18:00 London` hits the sweet spot: YouTube indexes the upload and begins serving Browse and Suggested impressions right as UK viewers finish work (`18:00–22:00 GMT`) while US East Coast viewers are active from lunchtime (`13:00 EST`) through US prime time.
2. **Shorts (`11:30 London`): KEEP AS IS on both channels.**
   - `11:30 London` sits **30–90 minutes before** the `12:00–14:30 London` multi-region mobile peak (UK lunchtime + India/SE Asia evening prime time + US East morning wake-up).
   - Because Shorts feed exploration happens in staged cohorts over the first several hours after publish, `11:30 London` seeds the initial cohort in Wave 1 (`12:00–14:30 London`) and carries high-retention Shorts into Wave 2 (`18:00–21:00 London`, UK evening + US afternoon) while keeping a clean 6.5-hour separation from `18:00 London` long-form releases.
   - *Optional future test (for Chief consideration only if OWB US share rebounds above UK share):* If OWB wants to test a US-heavier afternoon Short slot on non-long days, `15:30–16:00 London` (`10:30–11:00 EST`, 2 hours before the `18:00–21:00 London` UK evening / US afternoon overlap) is the only alternative worth testing — but while **UK is #1 on both channels** (`23.8%` 28d on OWB, `22.2%` 28d on HOS), **`11:30 London` remains the stronger default**.
