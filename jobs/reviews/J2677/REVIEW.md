# J2677 + J2683: what the weekly OWB audit (J2366) did not measure

- **J2677 (MacBook, agent `macbook`, 12 Nov 2026):** Measured Frame 0, First cut, Payoff time, and Loop from the cut metas and the 9 Nov first-second audit (`J2429`).
- **J2683 (Mac mini follow-up, agent `gemini`, 12 Nov 2026):** Pulled the remaining three parts on the Mini (`YT_ANALYTICS_REFRESH_TOKEN_OWB` read-only tracker sign-in through `2026-11-10`, cut `_meta.json` + word timestamps on the Mini/NAS, and `yt-dlp` metadata for `@SEA` resolved from `7oR0Pmd-WIk`). Read-only, £0. No Studio, YouTube, schedule or cut change, and nothing here authorises one.

## Verdict: ALL 8 PARTS MEASURED (J2677 + J2683)

| Part | J2677 (MacBook) | J2683 (Mac mini follow-up) |
|---|---|---|
| Shorts retention curves, biggest-drop second | Not measured on MacBook. | **Measured (9 of 10 Shorts settled in YTA through `2026-11-10`; `ffYKoNVPoqg` aired `10 Nov 11:30Z` at the YTA settlement cutoff with 48 views and has 0 curve points yet).** Every one of the 9 measured Shorts has its steepest ~1 s (5-bucket) drop in **`4.0–5.9 s` (`0.16–0.31` of runtime, `−13.73 pp` to `−40.00 pp`)**, mapped below against the exact shot and spoken word at that second. |
| Search terms (28d) | Not measured on MacBook. | **Measured (`2026-10-14` to `2026-11-10`).** Total 28d `YT_SEARCH` views across OWB = **`596` views (`6.3%` of `9,458` 28d views): `572` (`96.0%`) on Shorts and `24` (`4.0%`) on Longs.** Full channel, Short, and Long query tables below. |
| Frame 0 | Measured where available on MacBook (5 of 10). | **Measured for all 10 Shorts** from the cut `_meta.json` files on the Mini/NAS. |
| First cut | Measured (9 of 10). | **Measured for all 10 Shorts** (`VfDm3E2bUgU` first cut = `2.40 s`). |
| Payoff time | Measured where meta recorded it (6 of 10). | **Measured for all 10 Shorts** from word timestamps (`1OCNzhkiBuc` `"over two thousand kilometers an hour"` at `6.21–8.35 s` / distance payoff at `13.51–18.29 s`; `iyvWYFP_ETA` `"In 2009, Spirit got stuck..."` at `14.72 s`, `57.7%` in). |
| Loop | Measured (8 of 10). | **Measured for all 10 Shorts** (`VfDm3E2bUgU` forward pre-roll `18.14–18.90 s`, `1.14 s` silent tail; `iyvWYFP_ETA` spoken CTA `19.74–23.00 s` + `2.50 s` hold + `1.0 s` fade to black). |
| SEA (`@SEA`, `UCG9ShGbASoiwHwFcLcAh9EA`) | Not read on MacBook. | **Measured via `yt-dlp` from `7oR0Pmd-WIk` (*Higgs Boson: The God Particle*).** Last 30 days (`13 Oct – 12 Nov 2026`): **1 public long** (`-nIsOi-tVKM` *The Real Largest Star*, `2026-10-25`, `30:14`, **`342,328` views**), **3 short members-only companion videos** (`3:25–4:18`), and **0 Shorts**. |

## Sources

- **Views, stayed-to-watch and average viewed:** J2366's table (`05_Analytics/weekly_audit/OWB_2026-11-12.md`, Studio lifetime read 11 Nov) plus YouTube Analytics API (`YT_ANALYTICS_REFRESH_TOKEN_OWB`, settled through `2026-11-10`).
- **Retention curves & search terms:** YouTube Analytics API `audienceWatchRatio` / `relativeRetentionPerformance` by `elapsedVideoTimeRatio` (100 points, `2026-01-01` to `2026-11-10`) and `insightTrafficSourceDetail` (`insightTrafficSourceType==YT_SEARCH`, `maxResults=25`, `sort=-views`, 28d window `2026-10-14` to `2026-11-10`), cross-checked with `05_Analytics/owb/snapshots/2026-11-12.json`.
- **Edit facts:** each aired cut's own `_meta.json` and word-timestamp JSON on the Mini / `/Volumes/data/studio-live` / `/Volumes/data/mac-mini-archive`, plus `00_Brand/Channel-Setup/audits/SHORTS_FIRST_SECOND_AUDIT_2026-11-09.md` (`J2429`).
- **SEA:** `yt-dlp --dump-json` on `https://www.youtube.com/watch?v=7oR0Pmd-WIk` (`channel_id: UCG9ShGbASoiwHwFcLcAh9EA`, `@SEA`), then `yt-dlp --flat-playlist --dump-json` on `/videos` and `/shorts` plus full per-video metadata for the newest uploads.

---

## 1. The ten Shorts: edit facts + retention curves + biggest-drop second

| Short | Length | Stayed | Avg viewed (Studio / YTA) | Frame 0 | First cut | Payoff | Loop | Biggest drop (`audienceWatchRatio`) | On screen & said at the drop second |
|---|---|---|---|---|---|---|---|---|---|
| `T9fVlG3CCzU` Shooting Stars (`1,282` St / `1,270` YTA) | 20.0 s | 49.8% | 66.4% / 66.35% (`0:13` AVD) | Full-frame still (`s5_meteors/NHQ202108110001.jpg`, ISS Perseid streak), slow zoom `1.00→1.06`, hook `NOT A STAR` (`0–2.2 s`) | 4.70 s | `"between a grain of sand and a pea"` (`6.56–8.38 s`, `32.8%` in; overlay `6.5–8.9 s`); `"Swift-Tuttle, or Tempel-Tuttle"` (`14.42–17.00 s`, `72.1%` in) | Crossfade back to opening plate; last word `"Tempel-Tuttle"` at `17.00 s`, then `3.00 s` silent tail (`17.00–20.00 s`); last line does not run into line 1 | **Single step:** `0.20→0.21` (**`4.00–4.20 s`**: `112.42% → 106.29%`, **`−6.13 pp`**) & `0.95→0.96` (**`19.00–19.20 s`**: `29.47% → 23.34%`, **`−6.13 pp`**). **Steepest 1 s (5 buckets):** `0.20→0.25` (**`4.00–5.00 s`**: `112.42% → 94.21%`, **`−18.21 pp`**; `−28.31 pp` across `4.00–6.00 s`) | **At `4.00–5.00 s`:** Shot 1 (`NHQ202108110001.jpg` static zoom still) is still holding (`0.0–4.70 s`) while VO finishes the meta-promise *"Stay, and I'll show you what it really is."* (`2.38–4.32 s`, `"is."` at `4.04–4.32 s` + `0.40 s` pause `4.32–4.72 s`), before cutting at `4.70 s` to a second static zoom still (`NHQ202108110005.jpg`, `4.7–8.9 s`, *"Most are crumbs of comet"* at `4.72 s`). **At `19.00–19.20 s`:** inside the `3.00 s` silent crossfade tail (`17.00–20.00 s`). |
| `VfDm3E2bUgU` 16 Sunrises (`1,090` St & YTA) | 18.9 s | 31.6% | 66.7% / 66.73% (`0:12` AVD) | Moving video (`Sunrise To Sunset Aboard The ISS.ogv t=3.00s` earth-limb crop, rolled ~9°, `1.18x` wedge crop), hook `16 SUNRISES / A DAY` (`0–2.2 s`) | 2.40 s | Title number `"16 sunrises"` in line 1 (`1.66–2.76 s`); `"every 45 minutes"` at `10.11–11.49 s` (`53.5%` in); `"16 sunrises, 16 sunsets"` at `14.12–16.24 s` (`74.7%` in, overlay `14.05–17.45 s`) | Forward pre-roll (`18.14–18.90 s`, `t=2.24s` ending 1 frame before frame 0); last word `"waiting"` at `17.76 s` (`1.14 s` silent tail); *"Up here, morning never keeps you waiting."* | **Single step:** `0.28→0.29` (**`5.29–5.48 s`**: `92.40% → 87.72%`, **`−4.68 pp`**), flanked by `4.91–5.10 s` (`−4.38 pp`) & `5.67–5.86 s` (`−4.38 pp`). **Steepest ~1 s (5 buckets):** `0.24→0.29` (**`4.54–5.48 s`**: `105.56% → 87.72%`, **`−17.84 pp`**; `−27.20 pp` across `4.16–5.86 s`) | **At `4.54–5.48 s`:** Shot 3 (`Sunrise To Sunset Aboard The ISS.ogv t=22.00s` earth-limb crop, `4.00–7.55 s` — third consecutive crop from the same ISS video) while VO says *"The space station circles Earth"* (`"station"` `4.27–4.69 s`, `"circles"` `4.83–5.25 s`, `"Earth"` `5.45–5.75 s` + `0.32 s` pause before `"about every 90 minutes"` at `6.07–7.79 s`). Viewers already heard `"16 sunrises"` in line 1 (`0.10–3.64 s`); from `13.23–18.90 s` the curve holds flat `42.40% → 36.84%`. |
| `hZH0C7fpCk4` Venus 95% (`566` St / `565` YTA) | 19.7 s | 31.6% | 66.2% / 66.36% (`0:13` AVD) | Moving video (`s01` `svs14095_WISPR_Magellan_3rdFlyby.mp4`), hook `95% EARTH'S / WIDTH` | 2.25 s | Title number `"ninety-five percent"` in line 1 (`0.60–1.56 s`); `"second Earth"` at `14.58 s` (`74.0%` in; `"too much sunlight to ever be a second Earth"` `11.86–15.66 s`) | Forward (`1.22 s` silent tail, last word `"sun"` at `18.48 s`); *"…Because it sat closer to the sun. → Venus is ninety-five percent as wide as Earth."* | **Single step:** `0.25→0.26` (**`4.92–5.12 s`**: `105.11% → 99.43%`, **`−5.68 pp`**) & `0.26→0.27` (**`5.12–5.32 s`**: `99.43% → 94.32%`, **`−5.11 pp`**). **Steepest ~1 s (5 buckets):** `0.24→0.29` (**`4.73–5.71 s`**: `107.95% → 88.07%`, **`−19.88 pp`**; `−29.55 pp` across `3.94–5.91 s`) | **At `4.73–5.71 s`:** End of Shot 2 (`s02` `venus_ch3_plateB_steam_lid_v01.mp4`, `2.25–5.51 s`) cutting at `5.51 s` to Shot 3 (`s03` `13887_DAVINCI_PEVAA.mp4`, `5.51–8.77 s`) while VO finishes sentence 1's second clause *"with about four-fifths of its mass."* (`"four-fifths"` `4.16–4.96 s`, `"of"` `5.00–5.06 s`, `"its"` `5.10–5.24 s`, `"mass."` `5.30–5.74 s`). Because sentence 1 (`0.02–3.44 s`) already gave away the title's `95%` answer, viewers exit at `4.9–5.7 s` before `"It formed from the same kind of rock..."` (`5.94–11.82 s`). |
| `_a66uhRDips` Venus melt lead (`519` St & YTA, `+2` subs) | 17.4 s | 32.8% | **91.7% / 91.74%** (`0:16` AVD) | Moving video (`s01` `13887_DAVINCI_PEVAA.mp4` `t=101.0s`), hook `HOT ENOUGH / TO MELT LEAD` | 2.29 s | `"two hours"` at `15.49 s` (`89.0%` in; *"No lander has lasted much more than two hours"* `12.69–16.21 s`) | Forward (`1.19 s` silent tail, last word `"hours"` at `16.21 s`); *"…much more than two hours. → Venus is hot enough to melt lead."* | **Single step:** tied **`−5.00 pp`** at `0.06→0.07` (`1.04–1.22 s`: `153.13% → 148.13%`), `0.23→0.24` (**`4.00–4.18 s`**: `133.75% → 128.75%`), `0.24→0.25` (**`4.18–4.35 s`**: `128.75% → 123.75%`), & `0.28→0.29` (**`4.87–5.05 s`**: `112.50% → 107.50%`). **Steepest ~1 s (5 buckets):** `0.23→0.28` (**`4.00–4.87 s`**: `133.75% → 112.50%`, **`−21.25 pp`**) | **At `4.00–5.05 s`:** Shot 2 (`s02` `svs14095_ParkerVenus.mp4`, `2.29–5.77 s`) while VO says *"The air presses down like the sea nearly a kilometer deep."* (`"sea"` `4.01–4.25 s`, `"nearly"` `4.35–4.55 s`, `"a"` `4.59–4.65 s`, `"kilometer"` `4.69–5.17 s`, `"deep."` `5.25–5.57 s`). Moving video throughout + withholding the lander survival payoff (`15.49 s = 89.0%`) keeps retention `>100%` through `5.39 s` and `63.75%` (`89.38%` rel) at `17.40 s`. |
| `1OCNzhkiBuc` Neptune winds (`494` St & YTA) | 20.6 s | 42.6% | **75.0% / 74.98%** (`0:15` AVD) | Full-frame moving Voyager 2 clouds (`row 1`, `0.0–2.70 s`), hook `SUPERSONIC / WIND` | 2.70 s | `"over two thousand kilometers an hour"` at **`6.21–8.35 s`** (`30.1%–40.5%` in; graphic `6.3–9.8 s`); distance mystery payoff *"thirty times farther from the sun, there's hardly any sunlight to drive it"* at **`13.51–18.29 s`** (`65.6%–88.8%` in) | Forward (`1.15 s` silent tail, last word `"still"` at `19.45 s`); *"And still. → The wind on Neptune is supersonic."* (loop check PASS) | **Single step:** `0.20→0.21` (**`4.12–4.33 s`**: `120.51% → 114.87%`, **`−5.64 pp`**), then `0.23→0.24` (`4.74–4.94 s`: `108.21% → 103.59%`, `−4.62 pp`). **Steepest 1 s (5 buckets):** `0.20→0.25` (**`4.12–5.15 s`**: `120.51% → 101.54%`, **`−18.97 pp`**; `−31.79 pp` across `3.91–6.18 s`) | **At `4.12–5.15 s`:** Shot 2 (`row 2`, `2.70–6.30 s`: `PIA01492` Great Dark Spot whole-disc view with call-out `Voyager 2 Aug 1989`, repeating the same blue Neptune disc as Shot 1) while VO says *"Clouds of frozen methane race past..."* (`"frozen"` `3.81–4.19 s`, `"methane"` `4.29–4.87 s`, `0.34 s` pause `4.87–5.21 s`, `"race"` `5.21–5.41 s`) before the animated `2,000 km/h` wind bar enters at `6.30 s`. |
| `ZpEA8stoSPA` Uranus winters (`481` St & YTA, `+2` subs) | 21.2 s (`21.17 s`) | 26.9% | **306.8% / 306.81%** (`1:07` AVD) | Still in `"fit"` mode (`s4_uranus/webb_weic2310a.jpg`, letterboxed, zoom `1.25→1.42`), hook `21-YEAR / WINTER` (`0–2.2 s`) | 5.90 s | `"Uranus is tipped 97 degrees"` (`5.94–8.16 s`, overlay `6.4–9.0 s`); `"21 Earth years of unbroken dark"` (`11.24–13.94 s`, `53.1%` in); `"84 Earth years"` (`14.48–18.16 s`, `68.4%–85.8%` in) | Crossfade back to opening plate; last word `"season"` at `18.16 s`, then `3.01 s` silent tail (`18.16–21.17 s`) | **Single step:** `0.25→0.26` (**`5.29–5.50 s`**: `353.85% → 347.55%`, **`−6.30 pp`**) & `0.26→0.27` (**`5.50–5.72 s`**: `347.55% → 341.26%`, **`−6.29 pp`**), after `4.23–4.45 s` (`−5.59 pp`). **Steepest ~1 s (5 buckets):** `0.23→0.28` (**`4.87–5.93 s`**: `359.44% → 336.36%`, **`−23.08 pp`**; `−37.76 pp` across `4.23–6.35 s`) | **At `4.87–5.93 s`:** End of Shot 1 (`webb_weic2310a.jpg`, letterboxed still held **`0.0–5.90 s`**) while VO speaks the meta-promise *"Stay, and I'll show you why."* (`"Stay,"` `3.80–4.16 s`, `0.34 s` pause `4.16–4.50 s`, `"and I'll show you why."` `4.50–5.54 s`, `0.40 s` pause `5.54–5.94 s`), right before the `5.90 s` cut to Shot 2 (`PIA00143.jpg`) where `"Uranus"` is finally named at `5.94 s`. |
| `gJwNJN_yMKU` Apophis (`461` St & YTA) | 18.8 s (`18.83 s`) | 34.5% | **231.0% / 231.03%** (`0:43` AVD) | Moving video (`aurora_rock_open.mp4`, asteroid composite over ISS aurora plate `iss023e058455`), hook `CLOSER THAN / SATELLITES` (`0–2.4 s`) | 2.40 s | `"thirty-two thousand kilometres"` at `13.57 s` (`72.1%` in, scale graphic `9.37–15.42 s`); `"Step outside, look up, and watch"` (`15.56–18.08 s`) | Forward (`0.75 s` silent tail, last word `"watch"` at `18.08 s`); *"…Step outside, look up, and watch. → Apophis will fly closer than some of our satellites."* | **Single step:** `0.29→0.30` (**`5.46–5.65 s`**: `259.48% → 254.90%`, **`−4.58 pp`**), after `0.38–0.56 s` (`−3.92 pp`) & `4.90–5.08 s` (`−3.92 pp`). **Steepest ~1 s (5 buckets):** `0.26→0.31` (**`4.90–5.84 s`**: `266.67% → 252.94%`, **`−13.73 pp`** — smallest drop of all 9 Shorts) | **At `4.90–5.84 s`:** End of Shot 2 (`day_rock_wide.mp4`, `2.40–5.91 s`, asteroid over daytime Earth `iss034e048455`) just before cutting at `5.91 s` to Shot 3 (`aurora_rock_date.mp4`, `5.91–9.37 s`, `FRIDAY 13 APRIL 2029`), while VO says *"An asteroid 340 metres wide,"* (`"340"` `4.44–5.46 s`, `"metres"` `5.50–5.80 s`, `"wide,"` `5.90–6.28 s`). |
| `6dcL5rBmHPM` Saturn's rings (`45` St & YTA, `<100`v descriptive) | 22.8 s (`22.83 s`) | 21.7% (`45`v, too few) | 66.7% / 66.69% (`0:15` AVD) | Moving video (`s01` `cassini_rings_close_072.mp4` `t=70.0s`), hook `ONLY 10 M / THICK` | 2.60 s | `"ten metres"` in line 1 (`1.60–2.42 s`) and repeated at `18.74 s` (`82.1%` in: *"Cross that ten metres, and you're in open space again"* `17.90–21.52 s`) | Forward (`1.31 s` silent tail, last word `"again"` at `21.52 s`); *"…open space again. → Saturn's rings are only about ten metres thick."* | **Descriptive (`45`v `<100`):** `0.22→0.23` (**`5.02–5.25 s`**: `120.00% → 100.00%`, **`−20.00 pp`**), flanked by `4.79–5.02 s` (`−10.00 pp`) & `5.25–5.48 s` (`−10.00 pp`; **`−40.00 pp` across `4.79–5.48 s`**) | **At `4.79–5.48 s`:** Shot 2 (`s02` `cassini_rings_160.mp4`, `2.60–5.79 s`) while VO says *"Gravity and the moons that shepherd the edges pack the paths into a place."* (`"shepherd"` `4.64–4.96 s`, `"the"` `4.96–5.20 s`, `"edges"` `5.20–5.60 s`) after sentence 1 (`0.00–2.98 s`) already gave away the title's `"ten metres thick"` number. |
| `iyvWYFP_ETA` Mars night (`1,060` St at 44 h / `1,033` YTA thru 10 Nov, `+1` sub) | **25.5 s** | 38.8% | 62.6% / 63.17% (`0:16` AVD) | Pushed still (`frost/PIA11132.jpg`, Viking 2 surface frost, `0.0–4.10 s`; J2429 frame-0 movement `0.14` vs `1.50` floor), hook `MINUS 100°` (`0–2.2 s`) | 4.10 s | *"In 2009, Spirit got stuck and couldn't catch the winter sun. We never heard from it again."* starting at **`14.72 s` (`57.7%` in**; `"stuck"` at `17.04 s` = `66.8%` in) | Spoken CTA *"The full film, Could a Robot Survive on Mars?"* (`19.74–23.00 s`) over opening frost still (`19.55–25.50 s`) + end card `Js6EQJ8qDi8` (`19.74–25.50 s`), `2.50 s` music hold (`23.00–25.50 s`), `1.0 s` fade to black | **Single step:** `0.19→0.20` (**`4.84–5.10 s`**: `104.59% → 99.03%`, **`−5.56 pp`**) & `0.20→0.21` (**`5.10–5.35 s`**: `99.03% → 94.44%`, **`−4.59 pp`**). **Steepest ~1.3 s (5 buckets):** `0.16→0.21` (**`4.08–5.35 s`**: `113.29% → 94.44%`, **`−18.85 pp`**; `−28.75 pp` across `3.83–6.38 s`). End-card drop `22.95–24.23 s` (`34.54% → 26.33%`, `−8.21 pp`) | **At `4.08–5.35 s`:** At `4.10 s`, Shot 1 (`frost/PIA11132.jpg` static still) cuts to a second static pushed still (`dusk_plain/PIA19400.jpg`, Gale crater sunset, `4.10–6.00 s`) while VO pauses `0.42 s` (`3.84–4.26 s`) and restates the title question *"Could a robot survive one?"* (`4.26–5.70 s` + `0.44 s` pause before *"Batteries hate deep cold"* at `6.14 s`). |
| `ffYKoNVPoqg` Titan v11 (`48` St at 20 h / `0` YTA thru 10 Nov) | 18.0 s | 39.6% | 48.8% St (`0:09` AVD) | Moving video (`01_open_ splash_v11`, First-second gate PASS in J2429), hook `15 METERS / DEEP` | 2.67 s | Line 1: `"15 meters underwater"` (`0.69–1.92 s`); `"thick, freezing air"` / `"walk outside without a pressure suit"` in second half | Forward; last word at `16.13 s` (`1.87 s` tail) | **Not settled in YTA through `2026-11-10`** (`0` curve points; aired `2026-11-10T11:30:00Z` right at the YTA lag cutoff with `48` Studio views) | Curve not yet available in YTA (`<100` views, `0` YTA curve rows as of `2026-11-10`). |

### What the 9 measured retention curves show

1. **Every single one of the 9 measured Shorts has its steepest ~1 s (5-bucket) drop in `4.0–5.9 s` (`0.16–0.31` of runtime):**
   - `T9fVlG3CCzU` Shooting Stars: **`4.00–5.00 s` (`−18.21 pp`)** on *"Stay, and I'll show you what it really is"* (`2.38–4.32 s`) + `0.40 s` pause + `4.70 s` still-to-still cut.
   - `ZpEA8stoSPA` Uranus: **`4.87–5.93 s` (`−23.08 pp`)** on *"Stay, and I'll show you why"* (`3.80–5.54 s`) + `0.40 s` pause + `5.90 s` still-to-still cut.
   - `iyvWYFP_ETA` Mars night: **`4.08–5.35 s` (`−18.85 pp`)** on `0.42 s` pause + restating the title question *"Could a robot survive one?"* (`4.26–5.70 s`) over a `4.10 s` still-to-still cut (`PIA11132.jpg` → `PIA19400.jpg`).
   - `hZH0C7fpCk4` Venus 95%: **`4.73–5.71 s` (`−19.88 pp`)** and `6dcL5rBmHPM` Saturn rings: **`4.79–5.48 s` (`−40.00 pp`, 45v)** right after sentence 1 already gave away the title's number (`95%`, `10 metres`), when sentence 2 adds a secondary fact (*"with about four-fifths of its mass"*, *"moons that shepherd the edges"*).
   - `VfDm3E2bUgU` 16 Sunrises: **`4.54–5.48 s` (`−17.84 pp`)** on Shot 3 (third consecutive crop of the same ISS horizon clip) while VO states basic background (*"The space station circles Earth"*) after line 1 already gave away `"16 sunrises"`.
   - `1OCNzhkiBuc` Neptune: **`4.12–5.15 s` (`−18.97 pp`)** on Shot 2 (`2.70–6.30 s`), which repeats the same blue Voyager 2 whole-disc view of Neptune as Shot 1 before the `2,000 km/h` wind bar appears at `6.30 s`.
   - `_a66uhRDips` Venus melt lead (**`91.7%` avg viewed**) and `gJwNJN_yMKU` Apophis (**`231.0%` avg viewed**) have the smallest `4–6 s` damage relative to their opening level (`gJwNJN_yMKU` loses only `−13.73 pp` across `4.90–5.84 s`, `266.67% → 252.94%`; `_a66uhRDips` stays `>100%` through `5.39 s` and finishes at `63.75%`) because neither gives away its final number in line 1 (`"more than two hours"` at `15.49 s = 89%`; `"32,000 km"` at `13.57 s = 72%`) and both escalate immediately in sentence 2 on a distinct moving plate (`svs14095_ParkerVenus.mp4`, `day_rock_wide.mp4`).
2. **Spoken end-card CTAs and 3 s silent crossfade tails cause a second cliff at the end of the cut:** `T9fVlG3CCzU` drops **`−6.13 pp` in a single bucket at `19.00–19.20 s`** (tied for its biggest single-bucket drop) inside its `3.00 s` silent crossfade tail (`17.00–20.00 s`), and `iyvWYFP_ETA` drops **`−8.21 pp` across `22.95–24.23 s`** during its `5.76 s` spoken CTA + end-card hold (`19.74–25.50 s`). By contrast, `_a66uhRDips` (`1.19 s` forward loop tail, `89.38%` relative retention at end) and `gJwNJN_yMKU` (`0.75 s` forward loop tail, `94.75%` relative retention at end) hold through the seam.

---

## 2. 28-Day YouTube Search Terms (`2026-10-14` to `2026-11-10`)

Across the 28-day window (`05_Analytics/owb/snapshots/2026-11-12.json` + live YTA query), OWB earned **`596` views from YouTube Search (`6.3%` of `9,458` total 28d views)**:
- **Shorts (`YT_SEARCH`):** **`572` views (`96.0%` of channel search views)** across 25 Shorts.
- **Longs (`YT_SEARCH`):** **`24` views (`4.0%` of channel search views)** across 8 Longs (`0` on `028` `rVqgtkBV3jc`).

### 2.1 Top Channel-Wide Disclosed Search Terms (`insightTrafficSourceDetail`, `YT_SEARCH`)

*(Note: YouTube Analytics privacy-thresholds individual search queries with 1–2 views, so disclosed rows represent the top queries above threshold.)*

| Search term | 28d views | Watch time (min) | Matched OWB topic / video |
|---|---:|---:|---|
| `shooting stars` | 8 | 0 | `T9fVlG3CCzU` (*What Are Shooting Stars Really Made Of?*) |
| `sun` | 6 | 1 | `y-SPHQ0-VjQ` (*Why Is the Sun Getting Brighter as It Runs Out of Fuel?*) |
| `13 april 2029` | 4 | 0 | `gJwNJN_yMKU` (*How Close Will Asteroid Apophis Pass Earth on Friday the 13th?*) |
| `apophis asteroid 2029` | 4 | 0 | `gJwNJN_yMKU` (*Apophis*) |
| `black dwarf` | 4 | 0 | `1NeQFVnzO2Q` (*Why No Black Dwarf Exists Yet*) |
| `meet the galaxies` | 4 | 0 | Galaxy Shorts (`CtllH6VOhEI` / `xQlV9G9lqLI`) |
| `shooting star` | 4 | 0 | `T9fVlG3CCzU` (*Shooting Stars*) |
| `star shooting` | 4 | 0 | `T9fVlG3CCzU` (*Shooting Stars*) |
| `stars` | 4 | 0 | `T9fVlG3CCzU` (*Shooting Stars*) |
| `apophis asteroid` | 3 | 0 | `gJwNJN_yMKU` (*Apophis*) |
| `jupiter robot` | 3 | 0 | `buaOI3QGm7U` (*Could a Robot Survive Falling Into Jupiter?*) |
| `earth vs venus` | 2 | 0 | `hZH0C7fpCk4` (*How Big Is Venus Compared to Earth?*) |
| `my plan to land on the sun` | 2 | 0 | `2e-giqFmfy8` (*Why Didn't Earth Freeze Under a Dimmer Young Sun?*) |
| `orange dwarf star` | 2 | 0 | `1NeQFVnzO2Q` (*Why No Black Dwarf Exists Yet*) |
| `parker solar probe sun video` | 2 | 0 | `n_4XskX0yZk` (*Could a Robot Survive Touching the Sun?*) |
| `sun and proxima centauri` | 2 | 0 | `2e-giqFmfy8` (*Dimmer Young Sun*) |
| `the robot on mars` | 2 | 0 | `iyvWYFP_ETA` (*Could a Robot Survive a Night on Mars?*) |

*(Unrelated Shorts-search spillover terms in the channel top 25: `+15 social credit` [3], `caseoh funniest moments` [2], `drums` [2], `flight instructor` [2], `how to solve pyraminx` [2], `marie temara` [2], `math symbols band` [2], `sfs` [2].)*

### 2.2 Top Shorts by 28-Day `YT_SEARCH` Views & Disclosed Queries

| Video ID | Title | 28d `YT_SEARCH` views | 28d Total views | Search share | Disclosed search terms (views) |
|---|---|---:|---:|---:|---|
| `T9fVlG3CCzU` | What Are Shooting Stars Really Made Of? | **83** | 1,270 | 6.5% | `shooting stars` (8), `shooting star` (4), `star shooting` (4), `stars` (4), `constellations` (1), `sh**ting stars` (1), `shooting star gravitia` (1), `shooting stars never fly for me` (1), `shoting star` (1), `shotingstars` (1) |
| `y-SPHQ0-VjQ` | Why Is the Sun Getting Brighter as It Runs Out of Fuel? | **79** | 109 | **72.5%** | `sun` (6), `red giant sun` (1), `solar constant` (1), `sun expanding` (1), `sun live stream` (1) |
| `gJwNJN_yMKU` | How Close Will Asteroid Apophis Pass Earth on Friday the 13th? | **60** | 461 | **13.0%** | `13 april 2029` (4), `apophis asteroid 2029` (4), `apophis asteroid` (3), `2029 asteroid` (1), `april 13 2029` (1), `asteroid apophis` (1) |
| `n_4XskX0yZk` | Could a Robot Survive Touching the Sun? | **40** | 891 | 4.5% | `parker solar probe sun video` (2), `close to sun` (1) |
| `VfDm3E2bUgU` | Why Do Astronauts See 16 Sunrises a Day? | **34** | 1,090 | 3.1% | `sfs` (2) + broad Shorts-search spillover |
| `1NeQFVnzO2Q` | Why No Black Dwarf Exists Yet | **31** | 161 | **19.3%** | `black dwarf` (4), `orange dwarf star` (2), `black dwarf star` (1), `dwarf lab` (1) |
| `vlkj8RQKmH8` | Why Does a Day on Mercury Last Two of Its Years? | **30** | 851 | 3.5% | `mercury` (1), `mercury in telescope` (1) |
| `hZH0C7fpCk4` | How Big Is Venus Compared to Earth? | **30** | 565 | 5.3% | `earth vs venus` (2) |
| `1OCNzhkiBuc` | Why Are the Winds on Neptune Faster Than Sound? | **29** | 494 | 5.9% | `neptune` (1), `neptune winds` (1), `quasi star` (1) |
| `2e-giqFmfy8` | Why Didn't Earth Freeze Under a Dimmer Young Sun? | **29** | 83 | **34.9%** | `my plan to land on the sun` (2), `sun and proxima centauri` (2), `young sun` (1) |
| `ZpEA8stoSPA` | Why Does Uranus Have 21-Year Winters? | **28** | 481 | 5.8% | `uranus sleeping at last` (2), `uranüs` (2), `moons of uranus` (1) |
| `iyvWYFP_ETA` | Could a Robot Survive a Night on Mars? | **24** | 1,033 | 2.3% | `the robot on mars` (2), `robot on mars` (1) |
| `buaOI3QGm7U` | Could a Robot Survive Falling Into Jupiter? | **16** | 19 | **84.2%** | `jupiter robot` (3), `jupiter` (1) |
| `_a66uhRDips` | Why Is Venus Hot Enough to Melt Lead? | **12** | 519 | 2.3% | *(all queries below privacy threshold)* |
| `6dcL5rBmHPM` | How Thin Are Saturn's Rings? | **2** | 45 | 4.4% | *(all queries below privacy threshold)* |

### 2.3 All Longs by 28-Day `YT_SEARCH` Views

| Video ID | Title | 28d `YT_SEARCH` views | 28d Total views | Search share | Disclosed search terms (views) |
|---|---|---:|---:|---:|---|
| `h8HGfyShEHI` | Is the Sun Getting Brighter? | **9** | 9 | 100.0% | `turn up brightness` (1) |
| `VBaYRPp85Sw` | What Happened to Venus? | **4** | 230 | 1.7% | *(0 disclosed terms)* |
| `55AEQwvs36g` | How Long Do Saturn's Rings Have Left? | **4** | 75 | 5.3% | *(0 disclosed terms)* |
| `m09jUdwC5hk` | How Long Will Anything in Space Last? | **2** | 6 | 33.3% | *(0 disclosed terms)* |
| `REXYxuLOBoI` | The Last Star: What Remains When the Universe Goes Dark | **2** | 4 | 50.0% | *(0 disclosed terms)* |
| `Js6EQJ8qDi8` | The Mars Robot Meant to Die in 90 Days (It Lasted 14 Years) | **1** | 7 | 14.3% | *(0 disclosed terms)* |
| `ziKBPJ6FY0U` | Why JWST's Early Galaxies Look Too Big | **1** | 2 | 50.0% | *(0 disclosed terms)* |
| `Mo93x0fxB1Q` | The Fermi Paradox: Where Is Everybody? | **1** | 1 | 100.0% | *(0 disclosed terms)* |
| `rVqgtkBV3jc` | If You Moved at the Speed of Light, What Would Happen to Time? | **0** | 0 | 0.0% | *(0 views)* |

**What the search numbers show:**
- Viewers searching YouTube type **short 2–4 word noun phrases, dates, and spacecraft names** (`shooting stars`, `apophis asteroid 2029`, `13 april 2029`, `black dwarf`, `earth vs venus`, `parker solar probe sun video`, `the robot on mars`, `jupiter robot`), not abstract textbook clauses.
- Even when a Short (`n_4XskX0yZk` *Could a Robot Survive Touching the Sun?*) only names `Parker Solar Probe` in the spoken script and description (not the title), searchers typing `parker solar probe sun video` find it — while `gJwNJN_yMKU` gets **60 search views (`13.0%`)** on `apophis asteroid 2029` + `13 april 2029` (`13 April 2029` is in line 1 of its description and on-screen card).
- Longs got only **24 search views in 28 days** across the entire channel (and `h8HGfyShEHI`'s 9 search views came from unrelated `turn up brightness` queries), confirming `LEARNINGS.md` Rule 26: our Long titles and line-1 descriptions have lacked high-volume concrete noun phrases (`Parker Solar Probe`, `Spirit and Opportunity Mars rover`, `Huygens Titan landing`, `Apophis 2029`).

---

## 3. SEA (`@SEA`, `UCG9ShGbASoiwHwFcLcAh9EA`) — Last 30 Days of Uploads

Resolved from `7oR0Pmd-WIk` (*Higgs Boson: The God Particle*, uploaded `2026-08-23`, `37:15` / `2,235 s`, `561,923` views): the reference channel is **SEA (`@SEA`, channel ID `UCG9ShGbASoiwHwFcLcAh9EA`, `https://www.youtube.com/@SEA`)**.

### 3.1 Uploads in the Last 30 Days (`13 Oct – 12 Nov 2026`) and Recent Context

| Video ID | Title | Upload date | Length | Views | Availability |
|---|---|---|---:|---:|---|
| `tDWT9IZtPk4` | Giant Stars in the Early Universe | *(recent, members tab)* | `4:18` (`258 s`) | hidden | `subscriber_only` (SeaSquad Membership) |
| `bHYG2jjM_XU` | Stephenson 2-18 is NOT The Largest Star | *(recent, members tab)* | `3:25` (`205 s`) | hidden | `subscriber_only` (SeaSquad Membership) |
| `yXLtdakY3gI` | Webb's New Black Hole Star | *(recent, members tab)* | `4:17` (`257 s`) | hidden | `subscriber_only` (SeaSquad Membership) |
| **`-nIsOi-tVKM`** | **The Real Largest Star** | **`2026-10-25`** | **`30:14` (`1,814 s`)** | **`342,328`** | **Public long (only public upload in last 30 days)** |
| `7oR0Pmd-WIk` | Higgs Boson: The God Particle *(prior public long, for reference)* | `2026-08-23` | `37:15` (`2,235 s`) | `561,923` | Public long |
| `B0S93c3-cR0` | You Live in a Supervoid *(prior public long, for reference)* | `2026-07-08` | `46:13` (`2,773 s`) | `946,356` | Public long |
| `_5J1V-INKoc` | The Cold Spot: The Biggest Mystery in Cosmology *(most recent Short)* | `2026-08-13` | `1:31` (`91 s`) | `14,443` | Public Short (**0 Shorts in the last 30 days**) |

**What SEA's last 30 days show:**
- SEA published **1 public long in the last 30 days** (`-nIsOi-tVKM` *The Real Largest Star*, `30:14`, **`342,328` views in 18 days**) and **0 Shorts** (its last Short was 3 months ago on 13 Aug).
- Its public title (*The Real Largest Star*, 4 words / 21 characters) and description hook (*"How big can a star truly get? For years, the record holder has been Stephenson 2-18..."*) challenge a specific named record-holder (`Stephenson 2-18`, `UY Scuti`, `WOH G64`, `quasi-stars` / `black hole stars`), while spinning off 3–4 minute single-object pieces (*Stephenson 2-18 is NOT The Largest Star*, *Webb's New Black Hole Star*) for members.

---

## 4. One Next-Video Change Each (Updated with J2683 Mini Findings — Chief Decides)

1. **Retention curve and biggest-drop second (`4.0–5.9 s` across all 9 measured Shorts):**
   - **Next-video change:** On the next Short built (and in the `OWB-2026-11-E1` check), **never give away the title's final number in sentence 1 (`0–3.5 s`) and never use sentence 2 (`3.5–6.0 s`) to restate the title question or add a secondary footnote on the same visual subject**. Specifically: (a) if the title asks a scale/count question (*How Big / How Thin / How Many*), sentence 1 shows the physical contrast and sentence 2 (`2.5–5.5 s`) escalates the mechanism on a **new visual scale (wide → close or animated graphic, never a repeat of Shot 1's framing as in `1OCNzhkiBuc` Shot 2 or `VfDm3E2bUgU` Shot 3)** while holding the exact number to `≥70%` runtime (like `_a66uhRDips` `91.7%` and `gJwNJN_yMKU` `231.0%`, vs `hZH0C7fpCk4` `66.2%` and `6dcL5rBmHPM` `66.7%` which state `95%` and `10 metres` in sentence 1 and drop `−19.9 pp` / `−40.0 pp` at `4.7–5.7 s`); and (b) eliminate both the `3.8–5.9 s` meta-promise/question-restatement (`T9fVlG3CCzU`, `ZpEA8stoSPA`, `iyvWYFP_ETA`) and the `>1.5 s` silent/CTA outro (`T9fVlG3CCzU` `−6.13 pp` at `19.0–19.2 s`; `iyvWYFP_ETA` `−8.21 pp` at `23.0–24.2 s`).
2. **Search terms (`596` 28d search views: `572` on Shorts, `24` on Longs):**
   - **Next-video change:** On the next Long upload package (`031` / `032` and any Rule 26 retitle) and its companion Shorts, **put the exact named spacecraft/mission or calendar date people search (`Huygens probe Titan`, `Cassini`, `Parker Solar Probe`, `Spirit rover Mars`, `13 April 2029`) in line 1 of the YouTube description and in the Short's on-screen call-out/caption**, even when the title uses plain everyday words (*"a Robot"*, *"Friday the 13th"*). Evidence: `gJwNJN_yMKU` earned **60 search views (`13.0%`)** from `13 april 2029` / `apophis asteroid 2029` (in line 1 of its description) and `n_4XskX0yZk` earned **40 search views** including `parker solar probe sun video` from its description/VO, whereas Longs without concrete searched nouns in title + line 1 earned `0–4` meaningful search views in 28 days.
3. **Frame 0:**
   - **Next-video change:** The next Short built opens on full-frame moving footage of the titled subject, not a zoomed still (`LEARNINGS` rule 24; confirmed across all 10 metas: `_a66uhRDips`, `gJwNJN_yMKU`, and `1OCNzhkiBuc` open on moving video and reach `91.7%`, `231.0%`, and `42.6% stayed / 75.0% viewed`, whereas `ZpEA8stoSPA` `26.9% stayed` and `iyvWYFP_ETA` `38.8% stayed / 62.6% viewed` open on static stills).
4. **First cut:**
   - **Next-video change:** `J2429` recorded `HZGTovJu_TQ` (`026`, scheduled Mon 16 Nov) holding its first shot `4.8 s`. Here all three Shorts holding Shot 1 past `4.0 s` (`T9fVlG3CCzU` `4.70 s`, `ZpEA8stoSPA` `5.90 s`, `iyvWYFP_ETA` `4.10 s`) suffer a `−18.2 pp` to `−23.1 pp` drop across `4.0–5.9 s`. A re-cut of a scheduled Short is the Chief's call and needs Ben's watch.
5. **Payoff time:**
   - **Next-video change:** Record `first_cut_s` and `payoff_number_s` in every standalone Short's `_meta.json` (as the lifted Shorts already do), and check that the title's primary number is not already spoken in sentence 1 (`0–3.5 s`) when a late payoff is recorded (`VfDm3E2bUgU`, `hZH0C7fpCk4`, and `6dcL5rBmHPM` all spoke their title number in line 1 and plateaued at `66.2%–66.7%` avg viewed despite repeating a secondary number at `74%–82%`).
6. **Loop:**
   - **Next-video change:** Replace the `3.0 s` silent crossfade tail (`T9fVlG3CCzU` `17.0–20.0 s`, where `19.0–19.2 s` loses `−6.13 pp`) and the `5.8 s` spoken CTA end card (`iyvWYFP_ETA` `19.74–25.50 s`, losing `−8.21 pp`) with a forward loop and `≤1.2 s` silent tail (`OWB-2026-11-E1`).
7. **SEA (`@SEA` `-nIsOi-tVKM` *The Real Largest Star*, `342,328` views in 18 days):**
   - **Next-video change:** On our next Long (`032` Titan tentpole / next topic go-no-go) and our first monthly journey film (`LEARNINGS` rule 21), **anchor the opening 30 seconds and description line 1 on the specific named record-holder or spacecraft (`Huygens` — the only landing in the outer solar system — or a named extreme object that overturns the textbook answer, as SEA does with `Stephenson 2-18` in *The Real Largest Star*)**, and cut one 20-second Short directly on that named record-breaker rather than a generic planet overview.
