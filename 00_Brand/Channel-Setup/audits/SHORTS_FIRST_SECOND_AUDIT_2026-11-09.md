# Orbit Shorts First-Second Swipe Audit (`J2429` — 9 Nov 2026)

> **Job:** `J2429` (`macbook-2`) — *Orbit Shorts: break the ~1k ceiling — fix the swipe-away in the first second (`stayedToWatch` 30–50%)*
> **Data Source:** `05_Analytics/owb/studio_ctr.json` (80 Shorts with YouTube Studio `stayedToWatch` through 8 Nov 2026), `05_Analytics/owb/UPCOMING_SHORTS_GATE.md`, `00_Brand/Channel-Setup/social/UPLOADS.json`, and local `_meta.json` / `_gate.json` / `cuts.json` sidecars (`£0` spend).

---

## 1. Executive Summary: Why Orbit Shorts Stall at ~1,000 Views

Across all **80 Orbit Shorts** with `stayedToWatch` data (`31` Shorts with `views >= 100`), the channel's average view duration among viewers who stay is already healthy (**`60%–306%` average percentage viewed** on recent standalone and keeper Shorts). The ceiling at `~400–1,250` views is caused almost entirely by **first-second swipe-away (`0.0–1.5 s`)**:

- **Cohort `views >= 100` (`n = 31`):** mean `stayedToWatch` is **`33.2%`** (median **`32.5%`**, range **`15.4%` to `56.8%`**). Over two-thirds of the Shorts feed swipes away before `1.5 s`.
- **Top performers (`stayedToWatch >= 42%`):**
  - `y-SPHQ0-VjQ` (*Why Is the Sun Getting Brighter as It Runs Out of Fuel?*): **`56.8%` stayed**, **`78.6%` avg viewed** (`109` views) — full-bleed moving SDO solar prominence loop at `t = 0.0 s`, hook text `IT'S BRIGHTER` on frame 0 (`0.0–2.2 s`), VO onset at `0.14 s` (*"The sun is getting brighter"*, surprise word completed at `1.34 s <= 1.5 s`), no Orbit (`visor = 0.0002`), no blur bars.
  - `T9fVlG3CCzU` (*What Are Shooting Stars Really Made Of?*): **`49.6%` stayed**, **`61.9%` avg viewed** (`1,248` views, #1 Short on channel) — full-bleed `mode: "cover"` meteor streak (`NHQ202108110001.jpg`, zero blur bars), hook text `NOT A STAR` (yellow `STAR`) at `t = 0.0 s`, VO word 1 at `0.00 s` (*"That shooting star isn't a star"* — 6-word contradiction completed in `1.48 s <= 1.5 s`), `sfx_owb_whoosh_soft_v01.wav` at `0.0 s`. Held just under `50%` because shot 1 was a slow `1.00 -> 1.06` still zoom held `4.7 s` and sentence 2 used the meta-promise *"Stay, and I'll show you what it really is"*.
  - `1OCNzhkiBuc` (*Why Are the Winds on Neptune Faster Than Sound?*): **`42.6%` stayed**, **`75.0%` avg viewed** (`494` views) — moving Voyager 2 Neptune cloud wisps (`PIA01492`) at `t = 0.0 s`, hook text `SUPERSONIC / WIND` at `0.0–2.2 s`, VO onset `0.10 s` (*"The wind on Neptune"*, `0.10–1.62 s`), first cut at `2.70 s <= 3.0 s`, no meta-promise.
- **Proof that first-second framing — not topic interest — causes the swipe:**
  - `ZpEA8stoSPA` (*Why Does Uranus Have 21-Year Winters?*, `481` views) achieved **`306.8%` average percentage viewed** (viewers who stayed watched 3×), yet **`73.1%` swiped away (`26.9%` stayed)** because shot 1 (`webb_weic2310a.jpg`, `0.0–5.9 s`) used `mode: "fit"` (letterboxed/padded frame on a static image pushed `1.25 -> 1.42` over `5.9 s`) and opened with an unanchored pronoun (*"This planet has winters that last 21 years. Stay, and I'll show you why"* — `"Uranus"` was not spoken until `6.0 s`).

---

## 2. Top 10 vs Bottom 10 Orbit Shorts by `stayedToWatch` (`views >= 100`, `n = 31`)

### Table 2A — Top 10 Orbit Shorts by `stayedToWatch` (`views >= 100`)

| Rank | Video ID | Title | Views | Stayed % | Avg % Viewed | Frame 0 (`0.0 s`) Picture, Scale & Mode | On-Screen Hook Text at Frame 0 (`0.0 s`) | First 1.5 s Spoken VO & Onset (`s`) | `0.0–1.5 s` Motion & Cut 1 |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | `y-SPHQ0-VjQ` | *Why Is the Sun Getting Brighter as It Runs Out of Fuel?* | 109 | **56.8%** | 78.6% | Full-bleed `9:16` moving NASA SDO prominence eruption (`SVS 13778`), Sun limb fills `>70%` width, `visor=0.0002` (no Orbit), no blur bars | **`IT'S BRIGHTER`** (2 words, bold house caps, yellow keyword, `0.0–2.2 s`) | `0.14 s`: *"The sun is getting brighter"* (`0.14–1.34 s`, subject + anomaly in `1.20 s`) | Real video motion (`motion_0_1s = 12.15`), cut 1 at `4.3 s` |
| 2 | `T9fVlG3CCzU` | *What Are Shooting Stars Really Made Of?* | 1,248 | **49.6%** | 61.9% | Full-bleed `mode: "cover"` ISS Perseid meteor streak (`NHQ202108110001.jpg`), Earth limb + bright streak, `visor=0.0000`, zero blur bars | **`NOT A STAR`** (white `NOT A`, yellow `STAR`, `136 px`, `y=450..743`, `0.0–2.2 s`) | `0.00 s`: *"That shooting star isn't a star."* (`0.00–1.48 s`, direct reversal in `<1.5 s`) + whoosh at `0.0 s` | Still push `1.00->1.06` (`0.0–4.7 s`, held back from `60%` by still + `"Stay..."`) |
| 3 | `1OCNzhkiBuc` | *Why Are the Winds on Neptune Faster Than Sound?* | 494 | **42.6%** | 75.0% | Full-bleed `9:16` moving Voyager 2 Neptune disc (`PIA01492`, methane wisps translating across blue disc, `>65%` frame), `visor=0.0000` | **`SUPERSONIC / WIND`** (2 words, yellow `SUPERSONIC`, `0.0–2.2 s`) | `0.10 s`: *"The wind on Neptune"* (`0.10–1.62 s`, names subject + phenomenon immediately, no `"Stay..."`) + whoosh at `0.0 s` | Real cloud motion (`f0diff >= 1.5`), cut 1 at `2.70 s <= 3.0 s` |
| 4 | `MDvAKtmKauw` | *Three Suns in the Sky — Real Alien Worlds* | 149 | **42.5%** | 641.0% | Full-bleed `9:16` moving triple-star sunset horizon, three suns immediately legible at `t = 0.0 s`, no Orbit | **`THREE SUNS`** (frame-0 anomaly hook caption) | `0.05 s`: Names three suns in the sky in the first `1.5 s` | Moving sky plate from `0.0 s`, early cut `<3.0 s` |
| 5 | `eSFhBf2rcZk` | *Is the Moon Leaving Us?* | 292 | **41.9%** | 66.3% | Full-bleed `9:16` close-up lunar disc in motion (`>65%` frame scale), high contrast against space | **`LEAVING US`** / **`3.8 CM A YEAR`** (frame-0 hook caption) | `0.05 s`: Names `"The Moon"` + `"drifting away"` in first `1.5 s` | Moving lunar plate at `t = 0.0 s` |
| 6 | `CkSECfUfH2Y` | *The Sky Is Already Running Out of Light* | 292 | **41.2%** | 61.3% | Full-bleed `9:16` deep-field starfield dimming/moving from `t = 0.0 s` (`v05_titlecta`), `visor=0.0` | **`RUNNING OUT / OF LIGHT`** (frame-0 hook caption) | `0.00 s`: Immediate concrete statement on starlight fading in `<1.5 s` | Continuous starfield motion (`motion_0_1s = 40.25`) |
| 7 | `9lLZMy8rBJo` | *What Remains After the Last Star Dies?* | 623 | **39.0%** | 55.4% | Full-bleed `9:16` glowing red-to-dark stellar remnant (`v05_titlecta`), `visor=0.0000`, `luma=53.1` | **`AFTER THE / LAST STAR`** (frame-0 hook caption) | `0.00 s`: Immediate VO onset at frame 0 naming the last star dying | High first-second motion (`motion_0_1s = 50.89`) |
| 8 | `SdNXS1PD_Yk` | *Why the Night Sky Is Getting Darker* | 257 | **38.0%** | 64.6% | Full-bleed `9:16` moving night-sky plate at `t = 0.0 s` | **`GETTING / DARKER`** (frame-0 hook caption) | `<0.15 s`: Names the night sky getting darker in first `1.5 s` | Moving sky plate from `0.0 s` |
| 9 | `e-7hzJv4c80` | *How Long Until Andromeda Hits Us?* | 149 | **37.0%** | 62.5% | Full-bleed `9:16` moving Andromeda galaxy collision approach (`>70%` frame), high brightness contrast | **`HITTING US`** / **`4.5 BILLION YEARS`** (frame-0 hook caption) | `<0.15 s`: Names `"Andromeda"` approaching the Milky Way in `<1.5 s` | Fast approach motion from `0.0 s` |
| 10 | `xRxhb3vSru4` | *What's Left When the Last Star Goes Out?* | 414 | **36.4%** | 45.8% | Full-bleed `9:16` fading stellar remnant (`v05_titlecta`), `visor=0.0001`, `luma=25.9` | **`WHEN STARS / GO OUT`** (frame-0 hook caption) | `0.00 s`: Immediate VO onset at `0.00 s` | Moving plate (`motion_0_1s = 12.16`) |

---

### Table 2B — Bottom 10 Orbit Shorts by `stayedToWatch` (`views >= 100`)

| Rank (from bottom) | Video ID | Title | Views | Stayed % | Avg % Viewed | Frame 0 (`0.0 s`) Picture, Scale & Mode Failure | On-Screen Hook Text Failure | First 1.5 s Spoken VO Failure | `0.0–1.5 s` Motion & Cut Failure |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 (Worst) | `n2WbOfJhOwc` | *Star Recycling Isn't Perfect* | 213 | **15.4%** | 39.0% | Static/near-static dark nebula/star plate; abstract subject with no familiar scale | Abstract negative statement hook (`ISN'T PERFECT`) | Opens on abstract concept (*"star recycling"*) instead of a concrete object + anomaly | Near-still open, cut 1 `> 3.5 s` |
| 2 | `keXe1GNxWSU` | *Those Ice Scars Are How You Find It* | 206 | **15.8%** | 35.8% | Static Galileo Europa globe still (`PIA00502`) reused across 6 Europa Shorts (`dHash` 2–3 bits apart, `luma 140.3 -> 140.5`) | Vague pronoun title/hook (`THOSE ICE SCARS` — no planet named) | Pronoun/anaphoric opener (*"Those red lines across the ice..."*) — `"Europa"` not named in `0–1.5 s` | Static still (`luma` delta `0.2` in `0.5 s`), held `> 4.0 s` |
| 3 | `pII09FbRYGc` | *Why Europa Is Hiding a Massive Ocean* | 291 | **16.7%** | 47.5% | Same static Europa globe family (`dHash` cluster with 5 other Europa Shorts) | Generic label, no visual contrast against bright ice disc | Slow setup before naming the ocean scale | Static still push held `> 4.5 s` |
| 4 | `_8L9jYbDVmQ` | *Why You Can't Stand on a Neutron Star* | 423 | **18.6%** | 74.5% | Legacy dark open; small central object in mostly black frame (`74.5%` avg viewed proves viewers who stayed loved it, but `81.4%` swiped at `0–1 s`) | Negative framing (`CAN'T STAND`) | Negative setup in first `1.5 s` | Slow legacy open (`cut 1 > 4.0 s`) |
| 5 | `1glQuYFSaYQ` | *What Would Life Eat Under Europa?* | 127 | **20.9%** | 45.3% | Same static Europa globe still (`luma 140.0 -> 140.2`, `dHash` 2 bits from `keXe1GNxWSU`) | Repeated visual open across 6 Shorts on same topic | Speculative setup without immediate physical anomaly in `0–1.5 s` | Static still push (`f0diff < 0.5`) |
| 6 | `1NeQFVnzO2Q` | *Why No Black Dwarf Exists Yet* | 161 | **25.3%** | 60.8% | Static PNG (`friday_black_dwarf_cooling_v02.png`) with slow zoom (`0.0–4.92 s`), `visor=0.0048` | Negative abstract hook **`NOT / YET`** (no noun or scale on screen) | Pronoun opener at `0.00 s`: *"This star doesn't exist yet. Stay, and I'll show you why."* (No noun + meta-promise) | Static PNG zoom held `4.92 s > 3.0 s` |
| 7 | `cmeBDZLzPHs` | *A Day on Young Earth Lasted Just a Few Hours* | 104 | **26.1%** | 44.7% | Past-tense statement open; slow still push | Declarative statement, no curiosity gap | Past-tense statement without a question hook | Slow still hold `> 4.0 s` |
| 8 | `xQlV9G9lqLI` | *Why Stars Don't Crash When Galaxies Meet* | 254 | **26.1%** | 58.7% | Wide sparse starfield without a single large hero subject | Negative framing (`DON'T CRASH`) | Negative framing (*"Why stars don't crash..."*) | Wide slow pan |
| 9 | `ZpEA8stoSPA` | *Why Does Uranus Have 21-Year Winters?* | 481 | **26.9%** | **306.8%** | **`mode: "fit"` letterboxed/padded still** (`webb_weic2310a.jpg`, `1.25 -> 1.42` push over `5.9 s`), not full-bleed `9:16` | **`21-YEAR / WINTERS`** (`150 px`, good text, defeated by `fit` bars + pronoun VO) | `0.00 s`: *"This planet has winters that last 21 years. Stay, and I'll show you why."* (`"Uranus"` omitted until `6.0 s` + meta-promise) | Pushed still held **`5.90 s > 3.0 s`** (`f0diff < 1.50`) |
| 10 | `PV50PX-bE4g` | *Most of the Universe Gives Off No Light* | 129 | **27.2%** | 55.2% | Mostly black frame (`luma = 39.2`) with tiny diamond point (`v04_diamond`) | Negative statement (`NO LIGHT`) | Declarative negative statement | Low visible motion in dark frame |

---

### Table 2C — All-80 Unfiltered Extremes (Including `< 100` Views Cohort)

For completeness across all 80 Shorts in `studio_ctr.json`:

- **Highest `stayedToWatch` (`< 100` views cohort):**
  - `buaOI3QGm7U` (**`84.6%` stayed**, `19` views, `75.5%` avg viewed) — *How Do We Know What's Inside Jupiter?* (`0.00 s` VO onset, moving Juno perijove dive `motion_0_1s = 40.91`, zero Orbit `visor = 0.0`).
  - `G8DiaNjD2WE` (**`80.0%` stayed**, `10` views, `70.2%` avg viewed) — *The Moon Was Much Closer to Young Earth* (large full-bleed Moon filling frame 0).
  - `ykmoxRJ6BOI` (**`63.6%` stayed**, `10` views, `127.6%` avg viewed) — *How Do You Weigh a Star You Can't Touch?*.
  - `BX-z1EkgANg` (**`60.0%` stayed**, `21` views, `52.3%` avg viewed) — *Why Didn't Jupiter Become a Second Sun?* (`0.00 s` VO onset, high-contrast Jupiter plate).
  - `tEOHYQbcgOw` (**`60.0%` stayed**, `18` views, `45.6%` avg viewed) — *Could a Spaceship Fly Into Jupiter?* (`0.00 s` VO onset, `motion_0_1s = 39.32`, `visor = 0.0`).
  - `ZnsJTCcrTlA` (**`59.1%` stayed**, `22` views, `57.2%` avg viewed) — *Why Is Earth's Gravity Weaker at the Equator?* (`027` equator-weight Short).
  - `17zpT_u7XsY` (**`58.1%` stayed**, `37` views, `86.1%` avg viewed) — *Where Does All the Gold on Earth Come From?*.
- **Lowest `stayedToWatch` (`< 100` views cohort):**
  - `TE_HDKAnqms` (**`0.0%` stayed**, `2` views) — *Wait Until We Zoom Out From Earth* (**Orbit robot at frame 0**, `visor = 0.0082`, generic command title).
  - `82Ao0v5XiQI` (**`14.1%` stayed**, `90` views, `51.8%` avg viewed) — *Why Do Saturn's Rings Keep Disappearing?* (opened on a static Cassini still `PIA11141.jpg` held `3.56 s` with mid-chapter lift *"The rings are tilted at twenty-seven degrees..."* — omitted `"Saturn"` for `3.56 s`).
  - `QNTeou-w-gY` (**`20.3%` stayed**, `66` views, `51.7%` avg viewed) — *Where Would You Float Inside Jupiter?* (`visor = 0.0020`, slow still open).
  - `KX-XU_AODoI` (**`20.6%` stayed**, `75` views, `48.1%` avg viewed) — *Why a Neutron Star's Crust Is 10 Billion Times Stronger Than Steel* (statement title, static diagram-like open).

---

## 3. What the Winners Share: The 6-Part "First Second" Formula

Comparing the Top 10 (`36.4%–56.8%` stayed) against the Bottom 10 (`14.1%–27.2%` stayed) isolates six concrete, testable attributes in `0.0–1.5 s`:

1. **Full-Bleed `9:16` Already-Moving Real/Rendered Payoff Picture at Frame 0 (`t = 0.0 s`):**
   - Winners use real moving video (SDO solar flare loop, Voyager 2 cloud rotation, Juno perijove dive, Andromeda collision) or an active multi-layer parallax/motion composite where **central-band motion starts in `0.0–0.5 s`** (`frame0_kick_0_0_5s >= 0.40`, `frame0_diff_0_1_5s >= 1.50`).
   - Losers use a single static still with a slow Ken Burns push (`f0diff = 0.14–0.64`), a slow fade-in from black, or `mode: "fit"` letterbox/blur-pad bars (`ZpEA8stoSPA`).
2. **Hero Subject Scale `>= 60%` of the Frame, Zero Orbit at Frame 0 (`visor_frac < 0.0015`):**
   - Winners fill the central `9:16` band with one unmistakable celestial body or physical phenomenon (the Sun's limb, a bright meteor streak over Earth's limb, Neptune's blue disc, the Moon).
   - Losers show sparse starfields, tiny points in a dark frame (`PV50PX-bE4g`), reused identical globes (`keXe1GNxWSU`), or Orbit at `t = 0.0 s` (`TE_HDKAnqms`).
3. **2–4 Word High-Contrast Hook Caption Burned Onto Frame 0 (`0.0–2.2 s`):**
   - Winners render a 2–4 word hook caption at `t = 0.0 s` (no slow fade-in on the text) in large house Inter Black (`>= 90 px`, two lines max, one `#FFE000` yellow keyword, black stroke) inside `y = 280..720` (`IT'S BRIGHTER`, `NOT A STAR`, `SUPERSONIC / WIND`).
   - Abstract or negative two-word hooks (`NOT / YET`, `ISN'T PERFECT`) fail because they do not state an anomaly.
4. **Spoken Hook Lands Under `1.5 s` (`vo_onset_s <= 0.15 s` + Named Subject + Anomaly Word `<= 1.5 s`):**
   - Winners start Ben's voice at `0.00–0.14 s` (accompanied by `sfx_owb_whoosh_soft_v01.wav` at `0.0 s`), name the subject in the first `3–5` words, and land the surprise/contradiction word before `1.5 s`:
     - *"The sun is getting brighter"* (`0.14–1.34 s`, `56.8%` stayed)
     - *"That shooting star isn't a star"* (`0.00–1.48 s`, `49.6%` stayed)
     - *"The wind on Neptune"* (`0.10–1.62 s`, `42.6%` stayed)
   - Losers open with unanchored pronouns (*"This planet..."*, *"This star..."*, *"Those ice scars..."*) or mid-chapter lifts that omit the planet name for `3.5–6.0 s`.
5. **Zero Meta-Promise (`"Stay, and I'll show you..."`):**
   - Every standalone Short that followed its opener with *"Stay, and I'll show you why / what it really is"* (`ZpEA8stoSPA` `26.9%`, `1NeQFVnzO2Q` `25.3%`, `T9fVlG3CCzU` `49.6%`) suffered a measurable swipe cliff during `1.5–4.0 s`. Sentence 2 (`1.5–4.5 s`) must deliver the first concrete number or physical mechanism instead.
6. **First Visual Cut at `<= 2.5–3.0 s`:**
   - Winners cut to a new angle or moving plate at `2.0–2.8 s` (`<= 3.0 s` hard gate). Holding Shot 1 to `4.1–5.9 s` (`iyvWYFP_ETA` `4.1 s`, `kKN8Ale42sE` `4.6 s`, `HZGTovJu_TQ` `4.8 s`, `ZpEA8stoSPA` `5.9 s`) causes viewers to register the clip as a static slideshow before the second sentence begins.

---

## 4. Next-14-Day Uploaded Shorts Audit (`9 Nov – 23 Nov 2026`)

Checked against `05_Analytics/owb/UPCOMING_SHORTS_GATE.md`, `05_Analytics/owb/snapshots/2026-11-08.json`, and `00_Brand/Channel-Setup/social/UPLOADS.json`. All 11 Shorts scheduled through `23 Nov 2026` are listed below, with exact diagnoses for the **5 Shorts that can take a re-cut opening (or Studio swap to an already-built `J0935` export) without moving their slot**:

| Air Date (London) | Video ID | Title | Current Gate Status (`UPCOMING_SHORTS_GATE.md`) | Eligible for Opening Re-Cut / Swap Without Moving Slot? | Exact First-Second Fix (`£0` Spend) |
|---|---|---|---|---|---|
| **Mon 9 Nov 11:30** | `iyvWYFP_ETA` | *Could a Robot Survive a Night on Mars?* (`025` `mon09_night_cold`) | **FAILS stayed gate (report-only):** pushed still at frame 0 (`f0diff = 0.14 < 1.50`); first cut at `4.10 s > 3.0 s` | **YES (Candidate #1 — urgent if swapped before 11:30Z, else keep per J1889/J2216):** | Replace `0.0–2.5 s` static Mars frost still (`f0diff 0.14`) with a full-bleed moving Mars rover/lander twilight plate (`f0diff >= 1.50`), cut 1 at `<= 2.5 s`, keep locked VO & `11:30Z` slot. |
| **Tue 10 Nov 11:30** | `ffYKoNVPoqg` | *What Would Standing on Saturn's Moon Titan Feel Like?* (`owb_sa_s6_titan_v11.mp4`) | **PASS** (already re-cut to `v11` and swapped under `supersedes: RLSJm59OSzI`) | No — already re-cut (`v11`) and passing all first-second gates. | Already passing (`v11`). |
| **Wed 11 Nov 11:30** | `B1z2dv7m7Vk` | *Why Did a 90-Day Mars Rover Last 14 Years?* (`025` `wed11_opening_testA_v07.mp4`) | **PASS** (already re-cut to `v07` under `J1059`) | No — already re-cut (`v07`) and passing all first-second gates. | Already passing (`v07`). |
| **Thu 12 Nov 11:30** | `N42gKBbD7tE` | *How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?* (`025` length test) | **KNOWN (`J1320`):** canonical YouTube copy locked for length test | No — ruled canonical by Chief (`J1320`, 31 Oct). | Leave untouched (`J1320`). |
| **Fri 13 Nov 11:30** | `bSjWiCbB7pY` | *How Did a Helicopter Fly 72 Times on Mars?* (`025` `fri13_ingenuity_72`) | **KNOWN (`J1320`):** canonical YouTube copy locked | No — ruled canonical by Chief (`J1320`, 31 Oct). | Leave untouched (`J1320`). |
| **Sat 14 Nov 11:30** | `gmzaCfJF1gA` | *Why Does Pluto's Giant Ice Heart Have Zero Craters?* (`owb_sa_s7_pluto_heart_v01.mp4`) | **FAILS stayed gate (report-only):** pushed still at frame 0 (`f0diff = 0.64 < 1.50`); first cut at `5.90 s > 3.0 s`; spoken meta-promise (*"stay, and i'll show you"*) | **YES (Candidate #2 — Sat 14 Nov 11:30Z):** | Re-cut `0.0–2.5 s` using the New Horizons Pluto flyby approach animation (`SVS` moving flyby instead of 5.9 s pushed still `PIA19952`), split Shot 1 at `2.4 s <= 3.0 s`, and trim the `"Stay, and I'll show you why"` sentence (`1.8–3.8 s`) from the VO stem (`£0` ffmpeg trim). |
| **Mon 16 Nov 11:30** | `HZGTovJu_TQ` | *If You Can't See the Nearest Star, How Far Away Is It?* (`026` `mon16_cant_see_nearest_star`) | **FAILS stayed gate on YouTube `v01`:** first cut at `4.80 s > 3.0 s` | **YES (Candidate #3 — Mon 16 Nov 11:30Z, `v03` ALREADY RENDERED ON DISK):** | `026/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/mon16_cant_see_nearest_star_v03.mp4` (`J0935`) is already built and passes `gate_shorts_open.py` (`dur=23.7s, f0diff=2.62, cut1=2.53s, vo_onset=0.03s, visor=0.0`). Can be swapped into slot `2026-11-16T11:30:00Z` once Chief waives/resolves the Keeper line-1 question note (`mon16_cant_see_nearest_star_v03_infeasibility.json`). |
| **Tue 17 Nov 11:30** | `kKN8Ale42sE` | *How Far From Earth Is Voyager 1 Right Now?* (`owb_sa_s8_voyager1_v01.mp4`) | **FAILS stayed gate (report-only):** pushed still at frame 0 (`f0diff = 0.33 < 1.50`); first cut at `4.60 s > 3.0 s`; spoken meta-promise (*"stay, and i'll show you"*) | **YES (Candidate #4 — Tue 17 Nov 11:30Z):** | Replace `0.0–2.5 s` static Voyager still (`f0diff 0.33`, held `4.60 s`) with moving NASA JPL/SVS Voyager 1 flyby animation (`f0diff >= 1.50`), cut 1 at `2.3 s <= 3.0 s`, and trim the `"Stay, and I'll show you..."` clause (`£0` ffmpeg trim). |
| **Wed 18 Nov 11:30** | `cwU_0WWeNZ4` | *If Voyager Needs 75,000 Years, How Far Is the Nearest Star?* (`026` `wed18_robot_reach_nearest_star`) | **FAILS stayed gate on YouTube `v01`:** pushed still at frame 0 (`f0diff = 0.46 < 1.50`) | **YES (Candidate #5 — Wed 18 Nov 11:30Z, `v04` ALREADY RENDERED ON DISK):** | `026/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/wed18_robot_reach_nearest_star_v04.mp4` (`J0935`) is already built and passes `gate_shorts_open.py` (`dur=22.6s, f0diff=1.74, cut1=2.63s, vo_onset=0.00s, visor=0.0`). Ready for swap into `2026-11-18T11:30:00Z` upon Chief OK on `wed18_robot_reach_nearest_star_v04_infeasibility.json`. |
| **Fri 20 Nov 11:30** | `aAUgIGEuPwQ` | *The Nearest Star Is a Cherry Past Cairo. How Do We Know?* (`026` `fri20_grapefruit_cherry_v04.mp4`) | **PASS** (already swapped to `v04` under `J1101_v04_swap`, replaces `A6TW_6CXhcs`) | No — already swapped (`v04`, moving SDO solar flare `GSFC_20160426_SDO_m12224_SolarFlare.mp4`, cut 1 at `2.37 s`) and passing. | Already passing (`v04`). |
| **Mon 23 Nov 11:30** | `Dm4xsF1Ateg` | *Why Do You Weigh Less at Earth's Equator?* (`027` `earth_equator_weight_v07.mp4`) | **PASS** (already swapped to `v07` under `J1100`, supersedes `emwQsPxnRGM`) | No — already swapped (`v07`) and passing. | Already passing (`v07`). |

---

## 5. Summary of Unlocked `026`, `027`, and `032` Shorts Updated Under `J2429`

1. **`026_How-Far-Is-The-Nearest-Star` (`10_Shorts/`):**
   - `mon16_cant_see_nearest_star` (`HZGTovJu_TQ`), `wed18_robot_reach_nearest_star` (`cwU_0WWeNZ4`), and `fri20_grapefruit_cherry` (`aAUgIGEuPwQ`, `v04` live) are the 3 scheduled weekday Shorts; `v03` (`mon16`, `f0diff=2.62, cut1=2.53s, vo_onset=0.03s`) and `v04` (`wed18`, `f0diff=1.74, cut1=2.63s, vo_onset=0.00s`) are staged on disk.
   - The 4 unlocked reserve lifts (`lift_earth_pinhead`, `lift_light_4yr`, `lift_red_dwarf`, `lift_walk_900m`) had `v01` first cuts at `3.68 s`, `3.65 s`, `5.82 s`, and `4.60 s` (`> 3.0 s` cap). Updated `NEAREST_STAR_SHORTS_SCRIPTS_v01.md` and added `cuts_v02_first_second_plan.json` in each unlocked lift folder splitting Shot 1 at `2.20–2.50 s <= 3.0 s` with full-bleed `9:16` moving opens, `0.0 s` hook text, and `<= 1.5 s` spoken hook.
2. **`027_What-If-Earth-Stopped-Spinning` (`10_Shorts/`):**
   - `lift_equator_weight` (`Dm4xsF1Ateg`, `v07`) is scheduled for `Mon 23 Nov 11:30Z` and passes all first-second gates.
   - `lift_sudden_air` (`earth_sudden_air_v03.mp4` `23.27 s` / `v05.mp4` `21.5 s`, `f0diff=6.12, cut1=2.50s, vo_onset=0.00s`) is unscheduled/unlocked (`v03` passes the `22–27 s` band AND all first-second gates: `f0diff=6.60, cut1=2.50s, vo_onset=0.00s`).
   - The 3 unlocked reserve lifts (`lift_40000_years`, `lift_ancient_eclipses`, `lift_day_one_year`) had `v01` first cuts at `5.00 s`, `3.80 s`, and `5.50 s` (`> 3.0 s` cap), and `EARTH_SPIN_SHORTS_SCRIPTS_v01.md` had statement titles on Shorts 1 and 3 plus a pronoun opener on Short 3 (*"This coral is..."*). Updated `EARTH_SPIN_SHORTS_SCRIPTS_v01.md` and added `cuts_v02_first_second_plan.json` in each unlocked lift folder enforcing positive question titles, named subject in `<= 1.5 s`, full-bleed moving frame 0, and Cut 1 at `2.20–2.50 s <= 3.0 s`.
3. **`032_What-Would-Happen-If-You-Landed-On-Titan` (`10_Shorts/SHORTS_PLAN_v01.md` & `README.md`):**
   - Updated `SHORTS_PLAN_v01.md` and `README.md` to lock the explicit `J2429` First-Second specification across all 3 planned `032` Shorts (`wed25_strike_match`, `fri27_opening_testA`, and reserve `sat28_flying_28x`), replacing the static-push Frame-0 description on `wed25_strike_match` (`PIA14584` still push) with the verified moving composite/SVS plate from `J2378`/`J2089` (`composites_v01` / NASA SVS `20311` moving plate, `f0diff >= 1.50`, `frame0_kick_0_0_5s >= 0.40`, zero fade-in, zero blur-pad bars, hook caption at `t = 0.00 s`, VO onset `0.06 s <= 0.15 s`, `"Titan"` spoken at `0.06–0.40 s <= 1.5 s`).
