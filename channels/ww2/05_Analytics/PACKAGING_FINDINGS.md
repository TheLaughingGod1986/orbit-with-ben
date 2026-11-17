# WW2 Packaging Findings (`J3005` — Fair Whole-Channel Sample)

- **Sample:** **`1,020` long videos (`> 8 min`)** from the last up-to-100 uploads across **`14` WW2 / military-history channels** (`4` 2026 breakout channels: *WW2 Dossier*, *WW2 Combat Files*, *Military Studio*, *INKTROOPS*; plus `10` established `100k–2M` channels: *The Operations Room*, *The Tank Museum*, *War Stories*, *Dark Docs*, *World War Two*, *Imperial War Museums*, *Military History Visualized*, *Real Time History*, *Drachinifel*, *Historigraph*). Baseline median outlier score = **`1.000x`** (`25.5%` reach `>=2.0x`; `16.5%` reach `>=3.0x` against their own channel's similar-age median). Read-only API quota used: **`69` units** (£0). Refresh monthly (`00_Brand/PLAYBOOK.md` §7).

## What to Do (Backed by Cross-Channel Evidence)
1. **Frame around a concrete problem, question, or the opposing side's recorded reaction:** Titles naming the other side's reaction (`shocked`, `baffled`, `feared`, `captured`, `couldn't believe`) rank **#1** at **`1.51x` median** (`n=51`, `49.0%` hit `>=2x`, `39.2%` `>=3x`; holds on both breakout `1.51x` and established `1.60x` — use real war-diary/interrogation reactions, never synthetic slop). Questions (`?`) rank **#2** at **`1.27x` median** (`n=58` across 12 channels, `34.5%` `>=2x`; `2.08x` on breakout channels), and **`How` / `Why` openers** rank **#3** at **`1.12x` median** vs `0.98x` without (`n=220` across 13 channels, `30.4%` `>=2x`; **`1.25x`** on breakout channels).
2. **Name the nationality/belligerent and keep titles `<= 70` characters:** Nationality framing lifts median performance to **`1.04x`** vs `0.97x` without (`n=520`, 14 channels; `28.8%` `>=2x`). Keep titles `51–70` chars (`n=395`, `1.00x` median, highest `>=2x` share among length bands at **`27.9%`**) or `<= 50` chars (`n=327`, `1.00x` overall, **`1.83x`** on breakout channels).
3. **Grade thumbnails bright and keep cover text to `1–3` words in white + signal yellow:** Visually **bright thumbnails** rank **#1** among all visual tags at **`1.19x` median** (`n=113` across 11 channels, `29.2%` `>=2x`; `1.05x` breakout, `1.22x` established). **White + yellow text (`1.15x`, `n=25`)**, **yellow-only (`1.04x`, `n=62`)**, and **`1–3` words (`1.01x`, `n=352`, `29.3%` `>=2x`)** beat both cluttered `5+` word slabs (`21.9%` `>=2x`) and `0`-word textless thumbnails (`0.88x` median).
4. **Prefer colourised or bright high-contrast archive photography over AI slop:** On breakout channels, **colourised real archive photos** reach **`1.96x` median** (`1.00x` across all `n=240`, 12 channels), whereas AI/3D illustrations (`n=418`) offer **no median advantage (`1.00x` overall, `0.92x` on established channels)** while adding YouTube policy/trust risk.

## What to Avoid
- **Series labels, pipes (`|`), episode numbers, and `'Full Documentary'`:** Worst established tag at **`0.77x` median** (`n=81`, `17.3%` `>=2x`; loses in both cohorts: `0.84x` breakout, `0.76x` established).
- **Generic `'secret / mystery / untold / forgotten'` buzzwords:** **`0.90x` median** (`n=38` across 8 channels, `1.66x` mean) — vague mystery words underperform specific operational problems.
- **Calendar years (`1941`, `1944`) in the title:** **`0.96x` median** (`n=162`, 13 channels) and cuts the `>=2x` outlier rate nearly in half (**`14.8%`** vs `25.5%` baseline; `0.80x` on breakout channels).
- **Thumbnail maps (`0.98x` median, only `16.3%` `>=2x`, `n=147`), `0` cover words (`0.88x` median, `n=181`), white-on-red alarm banners (`0.91x` median, `0.69x` established, `n=78`), low-contrast ungraded B&W (`0.92x`–`0.93x` median), and `> 90`-char titles (`0.95x`, `18.8%` `>=2x`).** Keep code-drawn maps inside the film, not squashed onto the thumbnail.

## Which Findings Rest on Too Few Videos (or Cohort Concentration) — Plus vidIQ Study Check
- **Too few videos (`n < 25`):** `has_money_figure` (**`n=4`**, `0.70x` — too small to judge `$3 Billion`-style hooks; test live on Pilot 3), `has_until_or_then_turn` (**`n=23`**, `0.81x` — vidIQ's `10.2x` on `n=18` does **not** hold here), `text_colour_red_only` (**`n=2`**, `0.70x`), and `text_colour_white_and_yellow` (**`n=25`**, `1.15x` — right on the sample threshold).
- **Cohort skews & vidIQ audit:** From the 17 Nov vidIQ outlier-feed study, **other-side reaction (`1.51x`)**, **questions (`1.27x`)**, **avoiding series/`Full Documentary` (`0.77x`)**, and **bright over dark/flat grading (`1.19x`)** **HOLD**; **`How`/`Why` openers improve from neutral to `+14%` (`1.12x`, `1.25x` breakout)**; while **superlatives (`1.00x` median, `n=110`; `most/only/first` `0.90x` median / `12.55x` mean)** and **non-year hard numbers (`1.00x` median, `n=393`)** flatten at the median because channels use them routinely (high tail variance, not automatic lift). VidIQ's small top-20 reads for **no text (`0.88x`, `n=181`, `0` breakout videos)** and **plain B&W (`0.92x`, `n=115`)** **REVERSE** once tested across all `1,020` uploads.

## Ranked Title & Thumbnail Tags (`N = 1,020` Long Videos)
| Category | Tag | `n` (Ch) | Median Outlier | Without | `>=2x` Share | Breakout / Estab. Med | Note |
|---|---|---:|---:|---:|---:|---|---|
| title | `has_other_side_reaction` | 51 (5) | **1.511x** | 1.000x | 49.0% | 1.51x / 1.60x |  |
| title | `question_mark` | 58 (12) | **1.267x** | 1.000x | 34.5% | 2.08x / 1.25x |  |
| title | `how_why_opener` | 220 (13) | **1.118x** | 0.980x | 30.4% | 1.25x / 1.03x |  |
| title | `has_nationality_framing` | 520 (14) | **1.044x** | 0.968x | 28.8% | 1.00x / 1.08x |  |
| title | `what_when_opener` | 70 (10) | **1.000x** | 1.000x | 34.3% | 0.99x / 1.05x |  |
| title | `length_51_to_70_chars` | 395 (13) | **1.000x** | 1.000x | 27.9% | 1.00x / 1.00x |  |
| title | `has_superlative_any` | 110 (13) | **1.000x** | 1.000x | 25.4% | 0.94x / 1.00x |  |
| title | `length_le_50_chars` | 327 (14) | **1.000x** | 1.000x | 24.2% | 1.82x / 1.00x |  |
| title | `has_named_machine_or_operation` | 357 (14) | **1.000x** | 1.000x | 23.2% | 0.93x / 1.05x |  |
| title | `has_hard_number_non_year` | 393 (14) | **1.000x** | 1.000x | 22.9% | 0.97x / 1.01x |  |
| title | `has_any_number` | 509 (14) | **1.000x** | 1.000x | 22.0% | 0.99x / 1.00x |  |
| title | `length_71_to_90_chars` | 250 (11) | **0.994x** | 1.000x | 24.8% | 0.97x / 1.01x |  |
| title | `has_year` | 162 (13) | **0.962x** | 1.000x | 14.8% | 0.80x / 0.97x |  |
| title | `length_gt_90_chars` | 48 (5) | **0.954x** | 1.000x | 18.8% | 0.95x / 1.04x |  |
| title | `has_superlative_most_only_first` | 50 (10) | **0.900x** | 1.000x | 26.0% | 1.00x / 0.88x |  |
| title | `has_mystery_or_secret_word` | 38 (8) | **0.895x** | 1.000x | 23.7% | 0.92x / 0.90x |  |
| title | `has_until_or_then_turn` | 23 (6) | **0.812x** | 1.000x | 13.0% | 0.81x / 1.20x | LOW SAMPLE (n=23 (<25 videos)) |
| title | `has_series_or_full_documentary` | 81 (7) | **0.774x** | 1.000x | 17.3% | 0.84x / 0.76x |  |
| title | `has_money_figure` | 4 (3) | **0.700x** | 1.000x | 0.0% | 0.86x / 0.57x | LOW SAMPLE (n=4 (<25 videos)) |
| thumbnail | `brightness_bright` | 113 (11) | **1.188x** | 0.998x | 29.2% | 1.05x / 1.22x |  |
| thumbnail | `text_colour_white_and_yellow` | 25 (8) | **1.150x** | 1.000x | 32.0% | 0.68x / 1.49x |  |
| thumbnail | `text_colour_yellow_only` | 62 (7) | **1.039x** | 1.000x | 22.6% | 1.11x / 1.04x |  |
| thumbnail | `modern_photo` | 65 (7) | **1.036x** | 1.000x | 32.3% | — / 1.04x | 0 breakout vids |
| thumbnail | `words_1_to_3` | 352 (14) | **1.012x** | 1.000x | 29.3% | 1.00x / 1.07x |  |
| thumbnail | `text_colour_white_only` | 611 (14) | **1.009x** | 0.955x | 25.4% | 1.00x / 1.02x |  |
| thumbnail | `colour_mode_colourised` | 387 (12) | **1.000x** | 1.000x | 27.7% | 1.00x / 1.00x |  |
| thumbnail | `brightness_dark` | 229 (13) | **1.000x** | 1.000x | 26.6% | 1.00x / 1.01x |  |
| thumbnail | `has_face` | 482 (13) | **1.000x** | 1.000x | 26.1% | 1.00x / 1.00x |  |
| thumbnail | `has_machine` | 745 (14) | **1.000x** | 1.000x | 24.8% | 1.00x / 1.00x |  |
| thumbnail | `real_archive_photo` | 398 (12) | **1.000x** | 1.000x | 24.6% | 1.00x / 1.00x |  |
| thumbnail | `colour_mode_full_colour` | 466 (14) | **1.000x** | 0.992x | 24.5% | 1.00x / 1.00x |  |
| thumbnail | `no_arrows_or_circles` | 767 (14) | **1.000x** | 0.968x | 24.2% | 1.00x / 1.00x |  |
| thumbnail | `real_archive_photo_colourised` | 240 (12) | **1.000x** | 1.000x | 22.9% | 1.96x / 1.00x |  |
| thumbnail | `words_5_plus` | 292 (12) | **1.000x** | 1.000x | 21.9% | 0.95x / 1.00x |  |
| thumbnail | `tactical_map_graphic_only` | 139 (7) | **1.000x** | 1.000x | 21.6% | 0.73x / 1.00x |  |
| thumbnail | `ai_or_3d_illustration` | 418 (14) | **0.999x** | 1.000x | 26.6% | 1.00x / 0.92x |  |
| thumbnail | `has_machine_no_face` | 474 (14) | **0.993x** | 1.000x | 23.8% | 0.99x / 0.99x |  |
| thumbnail | `words_4` | 195 (14) | **0.987x** | 1.000x | 21.0% | 0.99x / 0.99x |  |
| thumbnail | `has_map` | 147 (10) | **0.980x** | 1.000x | 16.3% | 0.94x / 0.98x |  |
| thumbnail | `brightness_medium` | 678 (14) | **0.977x** | 1.063x | 24.5% | 0.99x / 0.97x |  |
| thumbnail | `has_arrows_or_circles` | 253 (12) | **0.968x** | 1.000x | 29.2% | 1.00x / 0.90x |  |
| thumbnail | `colour_mode_bw` | 167 (8) | **0.930x** | 1.000x | 23.4% | 0.96x / 0.87x |  |
| thumbnail | `real_archive_photo_bw` | 115 (8) | **0.923x** | 1.000x | 25.2% | 1.14x / 0.86x |  |
| thumbnail | `text_colour_white_and_red` | 78 (8) | **0.909x** | 1.000x | 28.2% | 0.98x / 0.69x |  |
| thumbnail | `words_0_no_text` | 181 (7) | **0.883x** | 1.000x | 28.7% | — / 0.88x | 0 breakout vids |
| thumbnail | `text_colour_red_only` | 2 (2) | **0.701x** | 1.000x | 0.0% | — / 0.70x | LOW SAMPLE (n=2 (<25 videos); concentrated in 2 channel(s)) |

## Top 30 Biggest Outliers (`views / similarAgeMedianViews`)
| # | Multiple | Views (vs Med) | Views/d | Channel | Title | Packaging (`image/colour, words textCol, flags`) |
|---:|---:|---:|---:|---|---|---|
| 1 | **1552.3x** | 1,024,507 (660) | 8,606 | Military Studio | USA Unleashes Second Atomic Weapon Against Japan: The Fatal Calculation Nagasaki Paid For (`dRfk6VdxoY4`) | `archive_photo/bw`, 5w `white`, medium, arr,face,map |
| 2 | **456.8x** | 214,222 (469) | 1,927 | WW2 Combat Files | The "Mistake" That Made The M1 Garand The Most Feared Rifle In The Pacific (`RscgsEte2A8`) | `ai_or_3d/colourised`, 2w `white_red`, medium, arr,face,mach |
| 3 | **340.9x** | 10,198,639 (29,913) | 114,545 | War Stories | Afghanistan Uncensored: Rare Footage From The Battle For Marjah (`xGlIQ_IH5-s`) | `archive_photo/colour`, 0w `none`, bright, mach |
| 4 | **235.8x** | 111,998 (475) | 981 | WW2 Combat Files | Why German Snipers Were Baffled By A U.S. Trick That Made Them Reveal Themselves (`P9KB2uq5fbQ`) | `ai_or_3d/colourised`, 2w `white_red`, medium, arr,face,mach |
| 5 | **219.7x** | 103,055 (469) | 919 | WW2 Combat Files | Why German Riflemen Couldn't Explain How U.S. Units Found Them Via Camo That Worked Against British (`Vq9XbLLmbMY`) | `ai_or_3d/colourised`, 3w `white_red`, dark, arr,face |
| 6 | **163.7x** | 167,641 (1,024) | 6,407 | WW2 Combat Files | Pratt & Whitney Built a 28-Cylinder Monster Engine — Mechanics Nicknamed It the 'Corncob' (`-oF-GBiARus`) | `ai_or_3d/colour`, 1w `yellow`, medium, face,mach |
| 7 | **74.4x** | 1,578,433 (21,222) | 9,608 | War Stories | Uncensored Color Footage Of The D-Day Invasion (`lwrp_4ui3jY`) | `archive_photo/colourised`, 0w `none`, medium, face |
| 8 | **69.5x** | 1,943,720 (27,970) | 18,005 | War Stories | Operation Barbarossa: Uncensored Reality Of The Eastern Front (`qcg8KTPtHGE`) | `archive_photo/colourised`, 0w `none`, bright, mach |
| 9 | **67.1x** | 31,184 (465) | 296 | WW2 Combat Files | When British Officers Witnessed American Training, They Couldn't Believe It (`UA2wknngRKE`) | `ai_or_3d/colour`, 2w `white_red`, medium, face |
| 10 | **65.6x** | 30,634 (467) | 278 | WW2 Combat Files | Why German Snipers Were Baffled By U.S. Soldiers Never Using The Same Path Twice (`AYwipYAqxg8`) | `ai_or_3d/colourised`, 1w `white_red`, medium, arr,face,mach |
| 11 | **57.5x** | 107,316 (1,868) | 9,911 | INKTROOPS | Japan Sent 1 Million Soldiers to China… And Never Won \| 5 Fatal Mistakes (`jntDqMp1OWk`) | `ai_or_3d/colour`, 3w `white`, medium, mach |
| 12 | **55.7x** | 75,758 (1,360) | 6,794 | WW2 Combat Files | Crews Called It 'Old Shakey' — The Flying Warehouse Held Together by Four 28-Cylinder Engines (`TlJ7aQlNWRE`) | `ai_or_3d/colour`, 2w `white`, medium, face,mach |
| 13 | **50.2x** | 33,150 (660) | 281 | Military Studio | 10,000 Soviet Guns Unleashed in Fulda Gap. 70% NATO Losses in 24 Hours — The Escalation Trap (`8PH1nOCqW5k`) | `ai_or_3d/colourised`, 7w `white`, dark, face,mach |
| 14 | **49.2x** | 100,438 (2,041) | 772 | WW2 Dossier | What Happened When Germans Opened American Engine for First Time (`TQuEtvT3McQ`) | `ai_or_3d/colourised`, 2w `white`, dark, arr,face,mach |
| 15 | **32.9x** | 136,317 (4,149) | 4,988 | INKTROOPS | His Army Was 21 Miles From England… So Why Did Hitler Never Invade? \| 5 Fatal Mistakes (`jEX6hL7HKGk`) | `ai_or_3d/colour`, 3w `white`, medium, mach |
| 16 | **31.0x** | 182,361 (5,882) | 4,952 | INKTROOPS | 30 KM From Moscow… Then Everything Went Wrong \| Operation Barbarossa (`zOpf5LEidXQ`) | `ai_or_3d/colour`, 3w `white`, medium, mach |
| 17 | **30.8x** | 45,111 (1,465) | 4,836 | INKTROOPS | Hitler Lost More Men in Tunisia Than at Stalingrad… Why? \| 5 Fatal Mistakes (`PLhC2lzA5vQ`) | `ai_or_3d/colour`, 3w `white`, bright, mach |
| 18 | **29.0x** | 533,684 (18,421) | 2,695 | War Stories | 2 Hours Of Rare Colorized Footage From WW2 (`S0ENnZZ8zGk`) | `archive_photo/colourised`, 0w `none`, medium, face |
| 19 | **27.8x** | 12,947 (465) | 131 | WW2 Combat Files | Why German SS Troops Feared Facing America's 101st Airborne Division (`k8hIVYqKt7A`) | `ai_or_3d/colourised`, 2w `white_red`, medium, arr,face,mach |
| 20 | **27.7x** | 2,737,281 (98,790) | 161,066 | War Stories | 100 Days In Hell: Uncensored Footage From The Battle Of Normandy (`vZDDYYZVwf8`) | `archive_photo/colourised`, 0w `none`, dark, face |
| 21 | **27.0x** | 496,623 (18,421) | 2,669 | War Stories | Why Did Hitler’s Best Tanks Fail At The Battle Of The Bulge? (`ie9e1T4Ze3E`) | `archive_photo/colourised`, 0w `none`, medium, mach |
| 22 | **24.6x** | 11,269 (459) | 116 | WW2 Combat Files | Why German Marksmen Couldn't Outshoot the Average American Rifleman (`cHZZ6vkQu8E`) | `ai_or_3d/colourised`, 4w `white_red`, medium, arr,face,mach |
| 23 | **23.4x** | 49,105 (2,095) | 358 | WW2 Dossier | What Captured Americans Had That German Officers Said No Army Would Issue (`r77wHS2OxfE`) | `ai_or_3d/colourised`, 3w `white`, medium, arr,face,map |
| 24 | **23.0x** | 92,654 (4,036) | 4,794 | INKTROOPS | Why Hitler Lost the Battle of Britain: The 5 Fatal Mistakes (`-1ouBXZjS9A`) | `ai_or_3d/colour`, 6w `white`, medium, mach |
| 25 | **22.6x** | 109,866 (4,871) | 661 | WW2 Dossier | What Stunned German Tankers Inside Captured American Shermans (`xearT_fQlfE`) | `ai_or_3d/colour`, 2w `white`, medium, arr,face |
| 26 | **22.1x** | 102,253 (4,622) | 623 | WW2 Dossier | What Haunted German Prisoners About the Way Americans Honored Their Fallen (`WhhDUcKV2Q0`) | `archive_photo/bw`, 2w `other`, medium, arr |
| 27 | **20.9x** | 9,701 (465) | 96 | WW2 Combat Files | The One Tactic U.S. Marines Used to Solve Japan's Sniper Problem—One No One Else Could (`O6N6V3VF0Xs`) | `ai_or_3d/colourised`, 2w `white_red`, medium, arr,face,mach |
| 28 | **19.4x** | 25,421 (1,310) | 487 | WW2 Dossier | What German Mechanics Found When They Cut Open American Tires (`tiRYWBKOr6k`) | `ai_or_3d/colourised`, 2w `white`, bright, arr,face,mach |
| 29 | **19.4x** | 29,929 (1,544) | 1,851 | WW2 Dossier | What Captured American M1 Garands Revealed to Germans Who Fired Them (`wWj-0m7ritA`) | `ai_or_3d/colourised`, 1w `white`, bright, arr,face,mach |
| 30 | **19.0x** | 11,905 (627) | 94 | Military Studio | How the Crude Soviet T-34 Shattered Germany's Panzer Legend in 1941 (`y61kDgrsHTY`) | `archive_photo/bw`, 4w `white`, medium, mach |
