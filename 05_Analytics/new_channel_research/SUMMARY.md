# New-Channel Research — YouTube Data API v3 Verification (`J2987`)

- **Fetched at:** `2026-11-17T17:19:37Z` (read-only YouTube Data API v3; £0 spent)
- **Quota used:** **`3,323` units** (under the `5,000`-unit cap; `quotaError = None`) — `search.list`: `3,200` (`32` calls × 100), `videos.list`: `62` (`62` calls × 1), `playlistItems.list`: `53` (`53` calls × 1), `channels.list`: `8` (`8` calls × 1)
- **Raw records:** `channels_53_raw.json`, `searches_16x2_raw.json`, `run_summary.json`

## Contradictions & Cross-Checks vs vidIQ Figures

1. **Three shortlist channels were created years before May 2025 (`snippet.publishedAt < 2025-05-01`):** **Wheely Explained** (`UCl3ps8skJPWeQeYBfp2J_CQ`, created **`2019-11-07`**, `1,700` subs — an aged 2019 account whose first current upload aired `2026-06-23`), **Stellar** (`UCNSbgDRlAHM55EXMxEKPrmg`, created **`2022-07-21`**, `29,200` subs, `80` videos), and **Dinodust** (`UC_MCKNUrukBBApIg4-stGBg`, created **`2023-07-29`**, `17,100` subs, `222` videos). The other `50/53` channels were created on or after `2025-05-20`.
2. **Shorts-heavy outliers inside the long-form shortlist:** **GLK** (`UCSEaZLka_GS5v9vbepw6Ajg`, `1,620` subs) has only **`10.0%` (`5/50`)** of sampled uploads over 8 minutes (`41/50` are `≤ 60 s` Shorts; median duration `0:25`), and **Frames Of Myth** (`UC9eon0MV-L3JM0Wm8r7nwSg`, `14,400` subs) is **`52.0%` (`26/50`)** over 8 minutes (`23/50` Shorts `≤ 60 s`). By contrast, `46/53` channels have zero `≤ 60 s` Shorts on page 1 (`35/53` are `100.0%` over 8 minutes).
3. **vidIQ subscriber & WW2 benchmark check:** On the vidIQ figures recorded in repo (`J2989`), **WW2 Dossier** (`UChjdsX71krIrJ4WFyZYFvYA`) matches cleanly — created `2026-04-30` (1 day before `2025-05-01` + 1 yr, i.e. April 2026 as cited), **`14,300` subscribers** (`0%` off vidIQ's `14,300`), `3,477,515` views, `132` videos, `98.0%` (`49/50`) over 8 min (`median 49:18`, `0` Shorts `≤ 60 s`) — alongside **Military Studio** (`UCWwCEHGxwFkf2Zf36mlEAug`, created `2026-05-06`, `7,580` subs, `100%` `> 8m`, `median 42:16`) and **WW2 Combat Files** (`UCwxjLJ5vMJ8WVXozeiYyEFg`, created `2026-07-11`, `3,610` subs, `100%` `> 8m`, `median 39:18`). Exact API subscriber counts for all 53 channels are below to flag any >20% drift against Claude's cloud-session vidIQ sheet.

---

## 1. 53 Example Channels (`channels.list` + First-Page Uploads `maxResults=50`)

> Sorted by subscribers descending. `First Upload Seen` carries `*` when `Videos > 50` (`nextPageToken` present on page 1 of the uploads playlist), meaning earlier uploads exist on older pages; `30d Uploads` shows `50+` when all 50 page-1 items were published within the last 30 days (`≥ 2026-10-18T17:19:37Z`). **`⚠️ <2025-05`** marks channels created before `2025-05-01`.

| # | Channel | Channel ID | Created | Country | Subscribers | Total Views | Videos | First Upload Seen (p.1) | Share > 8m | Median Duration | Median Views (p.1) | 30d Uploads |
|---:|---|---|---|:---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | Senior Insight | `UCx77AMr7kgZj5r81bE93-0g` | 2025-11-25 | US | 64,600 | 5,584,028 | 108 | 2026-06-27* | 100.0% (50/50) | 16:51 | 16,731 | 10 |
| 2 | Auto Unlocked | `UC4BQemnwRy3crTK8Z0F6qjw` | 2025-11-10 | US | 38,200 | 10,456,069 | 116 | 2026-07-15* | 100.0% (50/50) | 17:11 | 6,807.5 | 15 |
| 3 | Sleepy Old World | `UCYz9vNXXwBBOvTsmrMh32yg` | 2026-02-10 | US | 36,500 | 2,986,402 | 78 | 2026-06-25* | 98.0% (49/50) | 3:01:01 | 24,941 | 4 |
| 4 | Sleepy History | `UCxsLxGlOErRciZHaz2j_CWA` | 2025-05-20 | US | 35,200 | 2,864,723 | 113 | 2026-06-25* | 100.0% (50/50) | 3:06:48 | 7,474 | 13 |
| 5 | Aviate | `UCBcIafZ9Vt5JUip17Duw5DA` | 2025-06-15 | US | 35,100 | 5,124,783 | 127 | 2026-04-09* | 100.0% (50/50) | 13:14 | 19,251 | 8 |
| 6 | Wild Bird Survival | `UCsYEZah0zh0XCIaOHrkh93Q` | 2026-06-18 | US | 35,100 | 22,440,108 | 53 | 2026-06-25* | 74.0% (37/50) | 9:42 | 141,957 | 2 |
| 7 | Secrets of Everyday Things | `UCTsMCGz8-cxeMnjkT1Q0i6Q` | 2026-02-24 | US | 31,400 | 4,883,766 | 244 | 2026-09-29* | 100.0% (50/50) | 19:53 | 7,788 | 30 |
| 8 | POV Finance | `UCkPZLXcrP3Hc1J-Xd_uN-Mw` | 2026-04-07 | US | 30,600 | 5,735,974 | 186 | 2026-09-17* | 100.0% (50/50) | 27:48 | 36,772 | 18 |
| 9 | Stellar | `UCNSbgDRlAHM55EXMxEKPrmg` | **2022-07-21** ⚠️ | — | 29,200 | 6,869,768 | 80 | 2025-06-12* | 100.0% (50/50) | 1:06:00 | 4,963.5 | 1 |
| 10 | Everything Audi | `UCisOMF5p4QxVGU_QfvcB4Xg` | 2026-02-08 | US | 28,500 | 3,334,475 | 113 | 2026-07-29* | 100.0% (50/50) | 21:03 | 7,364 | 16 |
| 11 | Forgotten Ways to Make Money | `UC9Yv9fwZGNi77S2NDqRDgEQ` | 2026-04-15 | US | 24,100 | 3,067,816 | 105 | 2026-08-07* | 100.0% (50/50) | 24:32 | 2,934 | 14 |
| 12 | Mayday Protocol | `UCHR4lNIyBRn1sz7E3kXRTkQ` | 2025-05-28 | US | 23,300 | 3,498,950 | 74 | 2025-10-23* | 98.0% (49/50) | 21:58 | 3,323.5 | 3 |
| 13 | Exposed Discoveries | `UCkZFwjrahicdn3R2EVtQ_Tw` | 2025-12-09 | US | 22,300 | 6,433,657 | 330 | 2026-08-17* | 100.0% (50/50) | 20:12 | 697.5 | 15 |
| 14 | MythLore Unpacked | `UCJBu8PlYhslPSYpovOGGK5g` | 2025-10-21 | CA | 20,600 | 4,749,029 | 37 | 2025-11-21 | 100.0% (37/37) | 11:09 | 28,959 | 3 |
| 15 | The Lost Handyman | `UCy-xKlpGW5VhnOh1GOydRNw` | 2026-04-13 | US | 20,500 | 1,538,321 | 113 | 2026-08-24* | 100.0% (50/50) | 22:12 | 3,456.5 | 22 |
| 16 | geography | `UCzHIoLdss_1M_Iw6OxRKKEg` | 2026-06-05 | US | 19,700 | 6,170,277 | 91 | 2026-09-07* | 100.0% (50/50) | 19:56 | 16,350 | 18 |
| 17 | Aussie Money Fix | `UCmAqofaR4vnDiGPVEjwD-9A` | 2026-05-20 | AU | 19,300 | 2,502,357 | 77 | 2026-07-09* | 100.0% (50/50) | 9:23 | 12,417.5 | 20 |
| 18 | Vanished Worlds | `UCjWK-CiFx_dxrEWxbkId5Kw` | 2026-05-25 | US | 18,700 | 3,972,924 | 86 | 2026-08-31* | 100.0% (50/50) | 45:16 | 4,153 | 25 |
| 19 | T O P 7 | `UCeVLlFyuuFlgyBiZbuusREQ` | 2026-05-29 | GB | 18,600 | 8,617,472 | 75 | 2026-08-07* | 100.0% (50/50) | 12:00 | 1,728.5 | 15 |
| 20 | Borderline Wonders | `UCzFVTm-B0CdTUyjO-KaykHg` | 2025-05-25 | US | 18,400 | 4,575,691 | 63 | 2025-09-20* | 100.0% (50/50) | 28:30 | 10,266 | 5 |
| 21 | Aging with Wisdom | `UCjHPxCmCmxjmZuMSbC5TEyg` | 2026-07-02 | US | 17,800 | 1,630,631 | 116 | 2026-09-10* | 100.0% (50/50) | 22:21 | 4,425 | 11 |
| 22 | Dinodust | `UC_MCKNUrukBBApIg4-stGBg` | **2023-07-29** ⚠️ | NO | 17,100 | 5,479,980 | 222 | 2026-08-31* | 100.0% (50/50) | 2:42:44 | 8,429 | 23 |
| 23 | Arthur's UK Retirement Guide | `UCvdfd4h3SPdhAlIuU0NeBpw` | 2026-04-08 | GB | 17,000 | 1,141,565 | 214 | 2026-09-29* | 100.0% (50/50) | 21:33 | 2,624.5 | 30 |
| 24 | UrbanXplain | `UCSAG9BNP2SJz1_fiwIm87tg` | 2026-01-10 | US | 16,800 | 2,986,836 | 114 | 2026-07-10* | 96.0% (48/50) | 20:36 | 1,723.5 | 15 |
| 25 | Mido Explained | `UCH0fYAmg-lg8BauZAthSMrg` | 2026-05-12 | US | 15,800 | 8,081,638 | 166 | 2026-09-23* | 100.0% (50/50) | 16:05 | 9,900 | 28 |
| 26 | Frames Of Myth | `UC9eon0MV-L3JM0Wm8r7nwSg` | 2025-09-16 | US | 14,400 | 3,015,240 | 91 | 2025-10-16* | 52.0% (26/50) | 9:39 | 1,506.5 | 1 |
| 27 | WW2 Dossier | `UChjdsX71krIrJ4WFyZYFvYA` | 2026-04-30 | US | 14,300 | 3,477,515 | 132 | 2026-07-23* | 98.0% (49/50) | 49:18 | 1,058 | 14 |
| 28 | Parts That Changed History | `UC0Up62bLk6TDtOzKIlyBw2g` | 2025-06-17 | US | 13,200 | 2,660,385 | 146 | 2026-09-10* | 100.0% (50/50) | 19:56 | 8,385 | 27 |
| 29 | Discovery Shade | `UCPWwAHugmuJu5oAVYW4YCXA` | 2025-08-07 | US | 11,500 | 3,850,556 | 86 | 2026-09-10* | 100.0% (50/50) | 28:25 | 8,753 | 33 |
| 30 | Paradox Atlas | `UCg_zYQXrjAwRQqiMS2Nmkgg` | 2026-03-03 | US | 11,400 | 7,543,699 | 92 | 2026-05-27* | 94.0% (47/50) | 11:30 | 1,318.5 | 8 |
| 31 | Canadian Finance With Nathan | `UCr0-cpaiYc5mkdzFH6-pDZQ` | 2026-04-14 | CA | 10,600 | 2,435,221 | 136 | 2026-08-03* | 100.0% (50/50) | 13:56 | 3,123.5 | 20 |
| 32 | Ebiker | `UCyVI5PMOhkwgX0j_vnC-YqA` | 2026-07-09 | US | 10,100 | 1,548,451 | 77 | 2026-09-03* | 100.0% (50/50) | 26:07 | 2,135 | 16 |
| 33 | Atlas One | `UCFGbFxED1ZssIePFzToxRxA` | 2026-07-17 | NL | 9,290 | 6,433,243 | 43 | 2026-07-22 | 100.0% (43/43) | 20:53 | 16,702 | 11 |
| 34 | Mr K | `UCpZUhO4J_BjUCZ2dCP8kSlw` | 2025-10-18 | US | 8,040 | 3,956,650 | 343 | 2026-09-18* | 94.0% (47/50) | 11:04 | 5,759 | 25 |
| 35 | Military Studio | `UCWwCEHGxwFkf2Zf36mlEAug` | 2026-05-06 | US | 7,580 | 1,134,293 | 89 | 2026-09-04* | 100.0% (50/50) | 42:16 | 419.5 | 12 |
| 36 | Manufacturing line | `UCwTdAkFDrIcMdKUGDkrKDiA` | 2025-09-05 | US | 7,380 | 6,261,893 | 83 | 2026-03-12* | 100.0% (50/50) | 22:44 | 6,080.5 | 7 |
| 37 | The Unseen Earth | `UC3BTP2FmssM9YAt2QIe6u4A` | 2026-08-07 | US | 7,170 | 3,449,021 | 54 | 2026-08-20* | 92.0% (46/50) | 3:02:07 | 14,314.5 | 15 |
| 38 | Collapse Archive | `UC0-n8t2eNsc8oyWcWyzsXjw` | 2025-11-30 | GB | 5,450 | 1,103,129 | 63 | 2026-05-02* | 100.0% (50/50) | 21:07 | 381.5 | 5 |
| 39 | The Ocean Planet | `UCFZ_h_YPm3lRy_Eg4mxqMfA` | 2026-07-13 | US | 5,380 | 2,091,194 | 68 | 2026-08-10* | 96.0% (48/50) | 3:04:32 | 6,707.5 | 14 |
| 40 | Simple Science | `UCyOullfFIu9TAp74qgrZPtA` | 2025-10-16 | US | 3,890 | 509,889 | 121 | 2026-01-31* | 100.0% (50/50) | 1:52:46 | 1,630.5 | 4 |
| 41 | UK Finance With Harry | `UCX6CiGCU5Iefv7obMFnGKUw` | 2026-04-17 | GB | 3,840 | 1,035,800 | 114 | 2026-07-30* | 100.0% (50/50) | 13:22 | 2,875 | 20 |
| 42 | WW2 Combat Files | `UCwxjLJ5vMJ8WVXozeiYyEFg` | 2026-07-11 | US | 3,610 | 896,674 | 105 | 2026-09-07* | 100.0% (50/50) | 39:18 | 736 | 28 |
| 43 | Boring History Story Relaxing | `UCuij7G73h2G1F69VTrBrM7A` | 2025-11-06 | US | 3,230 | 878,609 | 79 | 2026-02-09* | 100.0% (50/50) | 2:42:12 | 2,909 | 0 |
| 44 | Black Box Down | `UCE1PpvTWLx5pJ9pYmMugIBg` | 2026-04-12 | US | 3,170 | 874,609 | 161 | 2026-10-01* | 86.0% (43/50) | 14:08 | 2,403.5 | 29 |
| 45 | Quantara Explains | `UCP9np-UlRHt_OfQFrsfa6qQ` | 2026-06-05 | US | 3,090 | 594,741 | 212 | 2026-10-22* | 100.0% (50/50) | 2:57:46 | 1,300 | 50+ |
| 46 | INKTROOPS | `UCcsQf3nDqM8o3O2BJhOTimQ` | 2026-06-28 | US | 3,060 | 1,657,620 | 98 | 2026-10-24* | 100.0% (50/50) | 9:00 | 1,465 | 50+ |
| 47 | Earth Origins | `UCvFkZTrmpU7IYQmjkyTjzlw` | 2026-09-25 | US | 2,900 | 632,381 | 14 | 2026-10-08 | 92.9% (13/14) | 3:18:12 | 10,605 | 5 |
| 48 | Candlelit History | `UCS72RVL3pmZPUQikWApSf7Q` | 2026-06-25 | US | 2,830 | 439,638 | 41 | 2026-07-14 | 97.6% (40/41) | 2:40:17 | 3,431 | 7 |
| 49 | The Geography Vault | `UCfTHSylhLm_1FM25AF2Tp3w` | 2026-06-29 | US | 1,950 | 999,876 | 38 | 2026-07-13 | 94.7% (36/38) | 15:37 | 873 | 9 |
| 50 | Wheely Explained | `UCl3ps8skJPWeQeYBfp2J_CQ` | **2019-11-07** ⚠️ | US | 1,700 | 625,638 | 20 | 2026-06-23 | 65.0% (13/20) | 9:32 | 5,089.5 | 9 |
| 51 | GLK | `UCSEaZLka_GS5v9vbepw6Ajg` | 2026-09-26 | US | 1,620 | 1,841,111 | 68 | 2026-10-17* | 10.0% (5/50) | 0:25 | 16,693 | 47 |
| 52 | Science Into Sleep | `UCRsDdBx9JqgNVVqH0GBVzeA` | 2026-07-28 | GB | 1,410 | 448,219 | 50 | 2026-08-03 | 100.0% (50/50) | 2:29:45 | 1,323 | 15 |
| 53 | Forge Atlas | `UCLuqiIyjkVvjHvAZJJO0Wbw` | 2026-07-11 | — | 1,100 | 416,228 | 56 | 2026-07-26* | 90.0% (45/50) | 10:42 | 1,221 | 8 |

---

## 2. 16 Search Phrases × GB & US (`search.list` `maxResults=25`, `order=relevance`, Filtered to `> 8 min`)

> Per phrase and region (`GB`, `US`), up to 25 video results were fetched and filtered to videos strictly over 8 minutes (`duration > 480 s`). Shares are over those kept long results (`12m` cutoff `≥ 2025-11-17T17:19:37Z`).

| Phrase | Region | Long Results (> 8m) | Median Views | Channels Created ≥ 2025-05-01 | Channels < 50k Subs | Published Last 12 Months |
|---|:---:|---:|---:|---:|---:|---:|
| `ww2 documentary` | `GB` | 23 / 25 | 2,058,379 | 0.0% (0/23) | 0.0% (0/23) | 26.1% (6/23) |
| `ww2 documentary` | `US` | 24 / 25 | 1,376,295 | 4.2% (1/24) | 8.3% (2/24) | 37.5% (9/24) |
| `world war 2 documentary` | `GB` | 22 / 25 | 2,014,913.5 | 4.5% (1/22) | 4.5% (1/22) | 27.3% (6/22) |
| `world war 2 documentary` | `US` | 23 / 25 | 1,297,492 | 4.3% (1/23) | 4.3% (1/23) | 30.4% (7/23) |
| `military history documentary` | `GB` | 23 / 25 | 1,815,845 | 0.0% (0/23) | 8.7% (2/23) | 30.4% (7/23) |
| `military history documentary` | `US` | 25 / 25 | 1,408,411 | 4.0% (1/25) | 8.0% (2/25) | 32.0% (8/25) |
| `geography explained` | `GB` | 15 / 25 | 1,332,759 | 0.0% (0/15) | 26.7% (4/15) | 13.3% (2/15) |
| `geography explained` | `US` | 17 / 25 | 1,982,641 | 0.0% (0/17) | 5.9% (1/17) | 17.6% (3/17) |
| `geography facts` | `GB` | 22 / 25 | 408,713.5 | 4.5% (1/22) | 50.0% (11/22) | 50.0% (11/22) |
| `geography facts` | `US` | 15 / 25 | 697,234 | 26.7% (4/15) | 40.0% (6/15) | 40.0% (6/15) |
| `true survival stories` | `GB` | 23 / 25 | 420,976 | 26.1% (6/23) | 56.5% (13/23) | 60.9% (14/23) |
| `true survival stories` | `US` | 25 / 25 | 163,245 | 28.0% (7/25) | 64.0% (16/25) | 68.0% (17/25) |
| `natural disaster documentary` | `GB` | 25 / 25 | 422,699 | 0.0% (0/25) | 24.0% (6/25) | 32.0% (8/25) |
| `natural disaster documentary` | `US` | 25 / 25 | 664,352 | 0.0% (0/25) | 24.0% (6/25) | 52.0% (13/25) |
| `plane crash documentary` | `GB` | 25 / 25 | 682,047 | 8.0% (2/25) | 12.0% (3/25) | 48.0% (12/25) |
| `plane crash documentary` | `US` | 24 / 25 | 1,426,074.5 | 0.0% (0/24) | 0.0% (0/24) | 33.3% (8/24) |
| `deep sea documentary` | `GB` | 25 / 25 | 1,296,071 | 16.0% (4/25) | 20.0% (5/25) | 52.0% (13/25) |
| `deep sea documentary` | `US` | 25 / 25 | 2,966,065 | 20.0% (5/25) | 20.0% (5/25) | 44.0% (11/25) |
| `deep sea creatures documentary` | `GB` | 24 / 25 | 1,323,368 | 20.8% (5/24) | 29.2% (7/24) | 62.5% (15/24) |
| `deep sea creatures documentary` | `US` | 24 / 25 | 453,272.5 | 25.0% (6/24) | 41.7% (10/24) | 54.2% (13/24) |
| `how things work` | `GB` | 19 / 25 | 27,081 | 10.5% (2/19) | 47.4% (9/19) | 89.5% (17/19) |
| `how things work` | `US` | 12 / 25 | 5,657,778.5 | 8.3% (1/12) | 8.3% (1/12) | 25.0% (3/12) |
| `science for sleep` | `GB` | 25 / 25 | 120,758 | 80.0% (20/25) | 4.0% (1/25) | 64.0% (16/25) |
| `science for sleep` | `US` | 25 / 25 | 94,297 | 92.0% (23/25) | 4.0% (1/25) | 76.0% (19/25) |
| `history for sleep` | `GB` | 25 / 25 | 216,633 | 76.0% (19/25) | 20.0% (5/25) | 84.0% (21/25) |
| `history for sleep` | `US` | 25 / 25 | 260,570 | 72.0% (18/25) | 24.0% (6/25) | 84.0% (21/25) |
| `dinosaur documentary` | `GB` | 23 / 25 | 884,313 | 4.3% (1/23) | 34.8% (8/23) | 56.5% (13/23) |
| `dinosaur documentary` | `US` | 23 / 25 | 930,181 | 0.0% (0/23) | 34.8% (8/23) | 47.8% (11/23) |
| `ebike explained` | `GB` | 9 / 25 | 98,221 | 0.0% (0/9) | 44.4% (4/9) | 0.0% (0/9) |
| `ebike explained` | `US` | 12 / 25 | 112,626 | 0.0% (0/12) | 58.3% (7/12) | 8.3% (1/12) |
| `best electric bike` | `GB` | 21 / 25 | 192,935 | 0.0% (0/21) | 9.5% (2/21) | 52.4% (11/21) |
| `best electric bike` | `US` | 20 / 25 | 161,383 | 0.0% (0/20) | 5.0% (1/20) | 65.0% (13/20) |
