# 029 Shorts plan v01 (Gemini covering on `gemini-4-argon-high`, 25 Oct 2026, `J0928`)

Three weekday Shorts (plus one Reserve Short) lifted from the locked 029 long. All use the long's own locked voice and score bed plus the house SFX kit (`06_Sound-Effects/kit_v01`): no new VO, no mints, **£0 spend**.

- **Long:** `vP1BbqZ_dnM`, `"Is Betelgeuse About to Explode?"` (uploaded Private in `J0922`; goes public **Sun 6 Dec 2026 18:00Z**).
- **Master:** `/Volumes/data/mac-mini-archive/youtube-staging/029/029_Betelgeuse_full_rough_v03b.mp4` (`542.23 s`, sha256 `54e04d3bfcb42bcf9066a0613254f10c978435b148d158468711e25908060c93`).
- **VO & Score stems:** `02_Voiceover/betelgeuse_vo_v01.wav` + `05_Music/betelgeuse_score_bed_v01.mp3` + `06_Sound-Effects/kit_v01/`.
- **Timings:** master seconds from `07_Edit-Project/full_rough_v03b_pack/betelgeuse_words_list.json` (`s00–s107`) and `cuts_v03b.json`.
- **Schedule slots:** Mon 7 Dec 2026 11:30Z is held by 028 Short `X768qs8sNQs` in `00_Brand/Channel-Setup/social/UPLOADS.json`, so 029's first three free weekday slots after the long goes public on Sun 6 Dec 18:00Z are **Wed 9 Dec**, **Fri 11 Dec**, and **Mon 14 Dec 2026 at 11:30Z** (with **Wed 16 Dec 2026 11:30Z** or the Fri 11 Dec non-Test-A slot for the Reserve Short).

Every Short applies `05_Analytics/LEARNINGS.md` rules 1–3, 6 and 7, plus the 60% stayed-to-watch (`PR #266`) and 70% average viewed (`PR #267`) rules. **Fri 11 Dec** is the rotated Test A opening-Short weekday (`05_Analytics/tests/SHORTS_TESTS.md`: `025` Wed → `026` Fri → `027` Mon → `028` Wed → `029` **Fri**); if Chief ends Test A at `028`, the Reserve Short (`reserve_die_young`, `23.34 s`) takes the Fri 11 Dec slot directly.

| Day (11:30Z / London) | Slug / Stem | Title (Rule 1: positive question naming Betelgeuse) | Hook caption, frame 0 (yellow hook word) | Lift (master s / sentences) | Words | Length |
|---|---|---|---|---|---|---|
| **Wed 9 Dec** (`2026-12-09`) | `wed09_great_dimming` / `029_short_wed09_great_dimming_v01` | Why Did Betelgeuse Suddenly Lose Two-Thirds of Its Light? | `LOST 2/3 OF` / **`ITS LIGHT`** | `109.92–119.14` (`s23–24`) + `127.54–129.38` (`s28`) + `130.42–130.98` (`s29`) + `133.54–143.56` (`s31–32`) | `66 w` | **`23.48 s`** (`21.18 s` VO + `0.30 s` tail + `2.00 s` end card) |
| **Fri 11 Dec** (`2026-12-11`, Test A) | `fri11_opening_testA` / `029_short_fri11_opening_testA_v01` | Is Betelgeuse Really About to Explode? | `VISIBLE IN` / **`DAYLIGHT`** | `0.08–36.94` (`s00–s06`, the long's opening, inter-sentence pauses tightened to `0.20 s`) | `102 w` | **`36.08 s`** (`33.78 s` VO + `0.30 s` tail + `2.00 s` end card; `< 38 s` Test A band) |
| **Mon 14 Dec** (`2026-12-14`) | `mon14_half_moon_daylight` / `029_short_mon14_half_moon_daylight_v01` | How Bright Will Betelgeuse Get When It Explodes? | `BRIGHT AS A` / **`HALF MOON`** | `248.06–261.70` (`s61–63`) + `274.12–284.64` (`s66–68`) | `55 w` | **`23.88 s`** (`21.58 s` VO + `0.30 s` tail + `2.00 s` end card) |
| **Reserve** (or **Fri 11 Dec** if Test A ends at `028`) | `reserve_die_young` / `029_short_reserve_die_young_v01` | Why Is Betelgeuse Already Dying at Just 10 Million Years Old? | `10 MILLION` / **`YEARS OLD`** | `67.64–91.92` (`s13–s18`, continuous with `0.20 s` pauses) | `61 w` | **`23.34 s`** (`21.04 s` VO + `0.30 s` tail + `2.00 s` end card) |

---

## Standing Rules Across All 029 Shorts (`LEARNINGS.md` + 60% / 70% Gates)

1. **Positive question title naming Betelgeuse (Rule 1):** Every title is a direct, positive question naming `Betelgeuse` (never a negative statement or pronoun title, and never identical to the long's exact listing title `"Is Betelgeuse About to Explode?"`).
2. **Frame 0 phenomenon in close-up + concrete hook caption + VO onset `≤0.15 s` (Rule 2):**
   - Frame 0 opens on moving picture of the phenomenon/scale filling `≥60%` of the `16:9` centre band (`y=656..1264` on `1080×1920`), with `motion 0-1s >= 10.0` in `gate_shorts_open.py`.
   - **No Orbit at frame 0 (`visor_frac == 0.0000`):** Use `YELLOW = (255, 224, 0, 255)` (hue `52.7° > 42°`) for the yellow hook word, and render 9:16 backgrounds with lifted navy blue (`B >= 50`, so `v = max(R,G,B)/255 >= 0.196 >= 0.18` and `dark_frac == 0.0`, guaranteeing `visor_frac == 0.0000` even next to orange Betelgeuse).
   - **No opening background reused from the last 10 Shorts (`bizlhspnVvY`, `DETI0HV2jlI`, `jJ5LkFGyzLI`, `X768qs8sNQs`, `gmzaCfJF1gA`, `HZGTovJu_TQ`, `kKN8Ale42sE`, `cwU_0WWeNZ4`, `A6TW_6CXhcs`, `emwQsPxnRGM`):** Verified against `00_Brand/Channel-Setup/audits/shorts_open_library/library.json` (`dHash >= 16 bits`, `bg_sim < 0.30`). Avoid uncropped 16:9 dark-navy code plates or wide La Silla/Paranal horizon plates at frame 0 (`X768qs8sNQs` / `HZGTovJu_TQ` / `A6TW_6CXhcs` used wide Southern Milky Way horizon plates; `jJ5LkFGyzLI` used an uncropped navy diagram).
3. **Visual beat every `2.5–4.0 s`, first cut `≤3.0 s`, no shot hold `>6.0 s` (Rule 3):**
   - Cut 1 lands at `2.20–2.90 s` (`≤3.0 s`).
   - Every later visual beat runs `2.1–4.0 s` (never holding a single shot past `4.0 s` on standard Shorts or `4.5 s` on Test A). Where the long holds a plate for `8–13 s`, subdivide into non-overlapping crops or stretches on word pauses.
4. **Bridge the `4–5 s` sentence-1 seam directly into a concrete number or mechanism (Rule 7):**
   - Close inter-sentence pauses to `0.15–0.20 s` (`<0.25 s` breath).
   - Cut out chronological dateline preambles (`s22` `"At the end of 2019, something strange happened"`) and meta-transitions (`s30` `"Telescopes caught the answer"`) so sentence 1 names `Betelgeuse` + the surprise claim and bridges at `2.9–4.4 s` straight into a concrete number (`February 2020`, `about a third`) or mechanism (`a flood of ghostly particles called neutrinos`).
5. **Withhold numeric/story payoff until `≥70%` runtime (`~16–21 s`), never answering at the `9–14 s` banner (Rule 6):**
   - The `9.0–14.0 s` parent-title banner (`Is Betelgeuse About to Explode?`) sits over the mechanism or mystery escalation, never the final answer.
   - The payoff lands at `16.0–21.6 s` (`68%–90%` of runtime).
6. **Single Teach overlay (`AGENTS.md` *Teach on screen*):**
   - Each Short carries one animated house pill overlay (`≤4` words from the VO at that moment, `11–12%` of the `16:9` band height, inside `y=656..1264`, clear of `0–2.2 s` hook caption and `9.0–14.0 s` title banner, duration `2.5–3.3 s` ≤ `4.0 s`).
7. **End card & Related video:**
   - Keep the long's score bed under the entire Short with a `0.30 s` VO tail after the last spoken word, followed by the `2.00 s` house end card inside the `16:9` centre band showing the exact long listing title **`Is Betelgeuse About to Explode?`** and video ID **`vP1BbqZ_dnM`**.
   - Related video in Studio: **`vP1BbqZ_dnM`** (set automatically on upload or in Studio since `vP1BbqZ_dnM` goes public Sun 6 Dec 18:00Z, before all three Shorts air).

---

## 1. Wed 9 Dec 2026 (`2026-12-09`, 11:30Z): Why Did Betelgeuse Suddenly Lose Two-Thirds of Its Light?

- **Slug / Stem:** `wed09_great_dimming` / `029_short_wed09_great_dimming_v01.mp4`
- **Hook caption (frame 0, `0.00–2.20 s`):** `LOST 2/3 OF` (white) / **`ITS LIGHT`** (yellow `#FFE000`)
- **Cover text (`08_Covers/029_short_wed09_great_dimming_v01_cover.jpg`, no Orbit):** `LOST 2/3 OF` / **`ITS LIGHT?`**

**Sentences, in order (`66` words, `0.18 s` tightened breaths between sentences; VO `0.05–21.18 s`):**
- `s23` (master `109.92–114.20`, local `0.05–4.33 s`, `4.28 s`, 13w): *"Betelgeuse, normally one of the brightest stars in the sky, began to fade."*
- `s24` (master `115.00–119.14`, local `4.51–8.65 s`, `4.14 s`, 14w): *"By February 2020, it had dropped to about a third of its usual brightness."*
- `s28` (master `127.54–129.38`, local `8.83–10.67 s`, `1.84 s`, 5w): *"Was Betelgeuse about to explode?"*
- `s29` (master `130.42–130.98`, local `10.85–11.41 s`, `0.56 s`, 3w): *"It was not."*
- `s31` (master `133.54–137.80`, local `11.59–15.85 s`, `4.26 s`, 15w): *"A huge bubble of gas had burst out from the star's surface and drifted away."*
- `s32` (master `138.44–143.56`, local `16.03–21.15 s`, `5.12 s`, 21w): *"As it cooled, it turned into a cloud of dust, and the dust blocked part of the star from our view."*

*(Note: Skips `s22` `"At the end of 2019, something strange happened."` so frame 0 starts immediately on the subject noun `"Betelgeuse"` + surprise claim `"began to fade"`; skips `s25–27` and meta-sentence `s30` `"Telescopes caught the answer."`.)*

**Picture (`23.48 s` total, 8 cuts, max shot `3.42 s` ≤ `4.0 s`, first cut `2.20 s` ≤ `3.0 s`):**

| Local Time (s) | Dur (s) | Source Plate (`07_Edit-Project/`) | Framing & Notes |
|---|---|---|---|
| `0.00–2.20` | `2.20` | `harvest_v01/sphere_jan.jpg` + animated surface prominence glow | Frame 0 close-up of Betelgeuse's resolved orange surface filling the 16:9 band (`1.00 → 1.16` push + corona shimmer, `motion 0-1s >= 12`, lifted navy fill `B >= 50` so `visor_frac = 0.0000`). Hook caption `LOST 2/3 OF` / **`ITS LIGHT`**. |
| `2.20–4.42` | `2.22` | `harvest_v01/sphere_dec.jpg` (`r13_compare` Dec 2019 dimmed half) | Cut 1 at `2.20 s` (`≤3.0 s`) to the dimmed December 2019 VLT/SPHERE image as VO says *"began to fade"*. |
| `4.42–6.55` | `2.13` | `VerticalCodeRenderer` 9:16 light curve (crop A: late 2019 drop) | Bridges the `4.33–4.51 s` sentence-1 seam directly into *"By February 2020..."* |
| `6.55–8.75` | `2.20` | `VerticalCodeRenderer` 9:16 light curve (crop B: `36%` minimum) | Draws the drop to *"about a third of its usual brightness"*. |
| `8.75–11.50` | `2.75` | `harvest_v01/orion_over_paranal.mp4` (tight Orion crop) | `9.0–14.0 s` parent-title banner (`Is Betelgeuse About to Explode?`) opens over *"Was Betelgeuse about to explode? It was not."* |
| `11.50–15.94` | `4.44` (split at `13.72`: `2.22 s` + `2.22 s`) | `harvest_v01/visir_flames.jpg` (wide plume) → `harvest_v01/mass_ejection.jpg` (close ejection) | Two `2.22 s` cuts showing the surface gas bubble bursting outward while the `9–14 s` banner clears at `14.0 s`. |
| `15.94–21.48` | `5.54` (split at `18.70`: `2.76 s` + `2.78 s`) | `harvest_v01/dust_impression.jpg` (crop A: cooling gas → crop B: dust cloud blocking star) | **Payoff (`68%–90%` of runtime, `16.03–21.15 s`):** *"turned into a cloud of dust, and the dust blocked part of the star from our view."* Single Teach overlay **`CLOUD OF DUST`** at `16.40–19.40 s` inside `y=656..1264`. |
| `21.48–23.48` | `2.00` | `harvest_v01/orion_rise_vlt.mp4` + house end card | `0.30 s` VO tail (`21.15–21.48 s`) + `2.00 s` end card: **`Is Betelgeuse About to Explode?`** + **`vP1BbqZ_dnM`**. |

---

## 2. Fri 11 Dec 2026 (`2026-12-11`, 11:30Z, Test A Opening Short): Is Betelgeuse Really About to Explode?

- **Slug / Stem:** `fri11_opening_testA` / `029_short_fri11_opening_testA_v01.mp4`
- **Test A weekday rotation (`05_Analytics/tests/SHORTS_TESTS.md`):** `025` Wed → `026` Fri → `027` Mon → `028` Wed → `029` **Fri** (`2026-12-11`).
- **Hook caption (frame 0, `0.00–2.20 s`):** `VISIBLE IN` (white) / **`DAYLIGHT`** (yellow `#FFE000`)
- **Cover text (`08_Covers/029_short_fri11_opening_testA_v01_cover.jpg`, no Orbit):** `VISIBLE IN` / **`DAYLIGHT?`**

**Sentences (`s00–s06`, the long's own opening `0.08–36.94 s`, cut on sentence end `s06`; inter-sentence pauses tightened to `0.20 s` so VO runs `0.08–33.78 s` and total duration with `0.30 s` tail + `2.00 s` end card is `36.08 s`, inside the `30–38 s` Test A window and well under the `40.0 s` hard gate):**
- `s00` (master `0.08–3.86`, local `0.08–3.86 s`, `3.78 s`, 12w): *"Look at Orion this winter at the orange star on its shoulder."*
- `s01` (master `4.58–5.70`, local `4.06–5.18 s`, `1.12 s`, 4w): *"That star is dying."*
- `s02` (master `6.54–8.48`, local `5.38–7.32 s`, `1.94 s`, 6w): *"So is Betelgeuse about to explode?"*
- `s03` (master `9.02–10.64`, local `7.52–9.14 s`, `1.62 s`, 8w): *"And what would you see if it did?"*
- `s04` (master `11.76–13.34`, local `9.34–10.92 s`, `1.58 s`, 4w): *"It is called Betelgeuse."*
- `s05` (master `13.96–21.40`, local `11.12–18.56 s`, `7.44 s`, 26w): *"One day it will blow itself apart, and for a few weeks it will shine so brightly that you could see it in the daytime sky."*
- `s06` (master `22.58–36.94`, local `18.76–33.78 s`, `15.02 s` tightened to `14.36 s` with `0.20 s` clause breaths, 42w): *"In this film, I will show you what kind of star it is, why it scared astronomers in 2019, how a giant star actually dies, what the night it goes would look like from your garden, and the honest answer to when."*

**Picture (`36.08 s` total, 11 cuts, re-paced from the long's `8–11 s` holds so every visual beat is `2.5–3.9 s` ≤ `4.0 s`, first cut at `2.50 s` ≤ `3.0 s`):**

| Local Time (s) | Dur (s) | Source Plate (`07_Edit-Project/`) | Framing & Notes |
|---|---|---|---|
| `0.00–2.50` | `2.50` | `harvest_v01/orion_rise_vlt.mp4` (crop A: close-up on Orion's shoulder rising) | Verified against `gate_shorts_open.py`: `visor_frac = 0.0000`, `min_dhash_bits = 18`, `max_bg_sim = 0.098` vs last 10 Shorts. Hook caption `VISIBLE IN` / **`DAYLIGHT`**. |
| `2.50–5.28` | `2.78` | `harvest_v01/orion_rise_vlt.mp4` (crop B: tighter push on orange Betelgeuse) | Cut 1 at `2.50 s` (`≤3.0 s`); bridges `s00 → s01` (*"That star is dying."*). |
| `5.28–9.24` | `3.96` | `harvest_v01/orion_over_paranal.mp4` (offset `0.45 s`) | Covers `s02–s03` (*"So is Betelgeuse about to explode? And what would you see if it did?"*). |
| `9.24–12.80` | `3.56` | `harvest_v01/sphere_jan.jpg` (resolved orange supergiant disc) | `9.0–14.0 s` parent-title banner (`Is Betelgeuse About to Explode?`) over `s04` + start of `s05`. |
| `12.80–15.70` | `2.90` | `code_graphics_v01/code_graphic_029_r03_r04_promise_v01.mp4` (stretch 1: supergiant flare) | Covers *"One day it will blow itself apart..."* |
| `15.70–18.66` | `2.96` | `code_graphics_v01/code_graphic_029_r03_r04_promise_v01.mp4` (stretch 2: daytime sky) | Covers *"shine so brightly that you could see it in the daytime sky."* Single Teach overlay **`DAYTIME SKY`** at `15.90–18.45 s` inside `y=656..1264`. |
| `18.66–22.10` | `3.44` | `harvest_v01/alma_orion_set.mp4` | Covers *"In this film, I will show you what kind of star it is..."* |
| `22.10–25.90` | `3.80` | `code_graphics_v01/code_graphic_029_r03_r04_promise_v01.mp4` (stretch 3: 2019 dimming curve) | Covers *"why it scared astronomers in 2019..."* |
| `25.90–29.80` | `3.90` | `code_graphics_v01/code_graphic_029_r03_r04_promise_v01.mp4` (stretch 4: core shells collapse) | Covers *"how a giant star actually dies, what the night it goes would look like..."* |
| `29.80–34.08` | `4.28` | `harvest_v01/lasilla_mw.mp4` (garden/horizon night sky crop) | **Payoff (`83%–94%` of runtime):** *"from your garden, and the honest answer to when."* + `0.30 s` VO tail (`33.78–34.08 s`). |
| `34.08–36.08` | `2.00` | `harvest_v01/orion_rise_vlt.mp4` + house end card | `2.00 s` end card: **`Is Betelgeuse About to Explode?`** + **`vP1BbqZ_dnM`**. |

---

## 3. Mon 14 Dec 2026 (`2026-12-14`, 11:30Z): How Bright Will Betelgeuse Get When It Explodes?

- **Slug / Stem:** `mon14_half_moon_daylight` / `029_short_mon14_half_moon_daylight_v01.mp4`
- **Hook caption (frame 0, `0.00–2.20 s`):** `BRIGHT AS A` (white) / **`HALF MOON`** (yellow `#FFE000`)
- **Cover text (`08_Covers/029_short_mon14_half_moon_daylight_v01_cover.jpg`, no Orbit):** `BRIGHT AS A` / **`HALF MOON?`**

**Sentences, in order (`55` words, `0.20 s` tightened breaths between sentences; VO `0.06–21.58 s`):**
- `s61` (master `248.06–250.96`, local `0.06–2.96 s`, `2.90 s`, 6w): *"So imagine the night Betelgeuse explodes."*
- `s62` (master `251.88–254.38`, local `3.16–5.66 s`, `2.50 s`, 9w): *"The first sign would not be light at all."*
- `s63` (master `255.30–261.70`, local `5.86–12.26 s`, `6.40 s`, 16w): *"It would be a flood of ghostly particles called neutrinos streaming out of the collapsing core."*
- `s66` (master `274.12–275.72`, local `12.46–14.06 s`, `1.60 s`, 4w): *"Then the light arrives."*
- `s67` (master `276.70–282.16`, local `14.26–19.72 s`, `5.46 s`, 13w): *"Within days, Betelgeuse would blaze as bright as the moon at half phase."*
- `s68` (master `282.92–284.64`, local `19.92–21.64 s`, `1.72 s`, 7w): *"You could see it in broad daylight."*

*(Note: Skips `s64–s65` detector detail so the neutrino flood bridges the `9.0–14.0 s` banner directly into `"Then the light arrives"`, withholding the half-Moon / broad-daylight numeric & visual payoff until `14.26–21.64 s` = **`60%–91%` of the `23.94 s` runtime**.)*

**Picture (`23.94 s` total, 8 cuts, max shot `3.80 s` ≤ `4.0 s`, first cut `2.96 s` ≤ `3.0 s`):**

| Local Time (s) | Dur (s) | Source Plate (`07_Edit-Project/`) | Framing & Notes |
|---|---|---|---|
| `0.00–2.96` | `2.96` | `harvest_v01/casa.jpg` + 9:16 supernova shockwave expansion (`1.00 → 1.16` push) | Frame 0 glowing multi-colour supernova shockwave in close-up (`visor_frac = 0.0000`, distinct texture from all last 10 Shorts). Hook caption `BRIGHT AS A` / **`HALF MOON`**. |
| `2.96–5.76` | `2.80` | `VerticalCodeRenderer` 9:16 collapsing core + neutrino wave (`r23_paranal`) | Cut 1 at `2.96 s` (`≤3.0 s`); bridges sentence-1 seam into *"The first sign would not be light at all."* |
| `5.76–9.00` | `3.24` | `harvest_v01/chajnantor_mw.m4v` (offset `3.25 s`) | Covers *"It would be a flood of ghostly particles called neutrinos..."* |
| `9.00–12.36` | `3.36` | `harvest_v01/dscovr_epic.jpg` (Earth from DSCOVR EPIC with neutrino stream) | `9.0–14.0 s` parent-title banner (`Is Betelgeuse About to Explode?`) over *"...streaming out of the collapsing core."* |
| `12.36–16.00` | `3.64` | `code_graphics_v01/code_graphic_029_r25_orion_v01.mp4` (9:16 Orion shoulder flare) | Covers *"Then the light arrives. Within days, Betelgeuse would blaze..."* as the `9–14 s` banner clears. |
| `16.00–19.80` | `3.80` | `harvest_v01/half_moon.jpg` (sharp half-Moon comparison in 9:16) | **Payoff part 1 (`67%–83%` of runtime):** *"...as bright as the moon at half phase."* Single Teach overlay **`HALF MOON BRIGHT`** at `16.30–19.40 s` inside `y=656..1264`. |
| `19.80–21.94` | `2.14` | `code_graphics_v01/code_graphic_029_r27_orion_v01.mp4` (daylight sky flare) | **Payoff part 2 (`83%–92%` of runtime):** *"You could see it in broad daylight."* + `0.30 s` VO tail (`21.64–21.94 s`). (Replaces the long's `r26_orbit_flare` Omni clip so the Short stays on real/diagram astronomy plates.) |
| `21.94–23.94` | `2.00` | `harvest_v01/orion_rise_vlt.mp4` + house end card | `2.00 s` end card: **`Is Betelgeuse About to Explode?`** + **`vP1BbqZ_dnM`**. |

---

## 4. Reserve Short (or Fri 11 Dec if Test A ends at 028): Why Is Betelgeuse Already Dying at Just 10 Million Years Old?

- **Slug / Stem:** `reserve_die_young` / `029_short_reserve_die_young_v01.mp4`
- **Hook caption (frame 0, `0.00–2.20 s`):** `10 MILLION` (white) / **`YEARS OLD`** (yellow `#FFE000`)
- **Cover text (`08_Covers/029_short_reserve_die_young_v01_cover.jpg`, no Orbit):** `DEAD AT` / **`10M YEARS?`**

**Sentences, in order (`61` words, continuous lift `67.64–91.92 s` with `0.20 s` tightened breaths; VO `0.06–21.04 s`):**
- `s13` (master `67.64–72.84`, local `0.06–5.26 s`, `5.20 s`, 18w): *"Betelgeuse is only about ten million years old, and it is already near the end of its life."*
- `s14` (master `73.86–74.80`, local `5.46–6.40 s`, `0.94 s`, 3w): *"Why so fast?"*
- `s15` (master `75.54–76.54`, local `6.60–7.60 s`, `1.00 s`, 4w): *"Because it is heavy."*
- `s16` (master `77.42–83.60`, local `7.80–13.98 s`, `6.18 s`, 15w): *"With somewhere around fifteen to twenty times the sun's mass, it burns its fuel ferociously."*
- `s17` (master `84.30–88.36`, local `14.18–18.24 s`, `4.06 s`, 14w): *"It gives out around a hundred thousand times as much light as the sun."*
- `s18` (master `89.22–91.92`, local `18.44–21.14 s`, `2.70 s`, 7w): *"Big stars live fast and die young."*

**Picture (`23.44 s` total, 7 cuts, max shot `3.96 s` ≤ `4.0 s`, first cut `2.60 s` ≤ `3.0 s`):**

| Local Time (s) | Dur (s) | Source Plate (`07_Edit-Project/`) | Framing & Notes |
|---|---|---|---|
| `0.00–2.60` | `2.60` | `VerticalCodeRenderer` 9:16 Betelgeuse vs Mars/asteroid-belt scale (`r05_scale` on lifted navy `B >= 50`) | Frame 0 animated supergiant outline expanding past Mars's orbit (`visor_frac = 0.0000`). Hook caption `10 MILLION` / **`YEARS OLD`**. |
| `2.60–5.36` | `2.76` | `harvest_v01/sphere_jan.jpg` (close-up resolved orange surface) | Cut 1 at `2.60 s` (`≤3.0 s`) as VO says *"...and it is already near the end of its life."* |
| `5.36–7.70` | `2.34` | `harvest_v01/sdo_hmi_continuum.jpg` (Sun comparison) | Bridges the `5.26 s` seam directly into *"Why so fast? Because it is heavy."* |
| `7.70–10.84` | `3.14` | `harvest_v01/westerlund.jpg` (crop A: massive star cluster wide) | `9.0–14.0 s` parent-title banner (`Is Betelgeuse About to Explode?`) opens over *"With somewhere around fifteen to twenty times the sun's mass..."* |
| `10.84–14.08` | `3.24` | `harvest_v01/westerlund.jpg` (crop B: massive core cluster tight) | Covers *"...it burns its fuel ferociously."* |
| `14.08–18.34` | `4.26` (split at `16.20` or `3.96 s` + `3.10 s` with `tarantula.jpg`) | `harvest_v01/visir_flames.jpg` (`14.08–18.04 s`, `3.96 s`) → `harvest_v01/tarantula.jpg` (`18.04–21.44 s`, `3.40 s`) | **Payoff (`60%–91%` of runtime):** *"It gives out around a hundred thousand times as much light as the sun. Big stars live fast and die young."* Single Teach overlay **`100,000× THE SUN`** at `14.50–17.80 s` inside `y=656..1264`. |
| `21.44–23.44` | `2.00` | `harvest_v01/orion_rise_vlt.mp4` + house end card | `0.30 s` VO tail (`21.14–21.44 s`) + `2.00 s` end card: **`Is Betelgeuse About to Explode?`** + **`vP1BbqZ_dnM`**. |

---

## Checklist Verification Summary (`05_Analytics/LEARNINGS.md` + `J0928`)

| Check | Short 1 (`Wed 9 Dec`) | Short 2 (`Fri 11 Dec`, Test A) | Short 3 (`Mon 14 Dec`) | Reserve (`Fri 11 Dec` alt / `Wed 16 Dec`) |
|---|---|---|---|---|
| **(1) Positive question title naming Betelgeuse** | *Why Did Betelgeuse Suddenly Lose Two-Thirds of Its Light?* (`PASS`) | *Is Betelgeuse Really About to Explode?* (`PASS`) | *How Bright Will Betelgeuse Get When It Explodes?* (`PASS`) | *Why Is Betelgeuse Already Dying at Just 10 Million Years Old?* (`PASS`) |
| **(2) Frame 0 moving phenomenon/scale + concrete caption + yellow hook word + `visor=0` + no reused bg** | `sphere_jan` animated supergiant (`LOST 2/3 OF` / **`ITS LIGHT`**), `Betelgeuse` at `0.05 s` (`PASS`) | `orion_rise_vlt` close shoulder crop (`VISIBLE IN` / **`DAYLIGHT`**), `Orion` at `0.40 s` (`PASS`) | `casa.jpg` expanding shockwave (`BRIGHT AS A` / **`HALF MOON`**), `Betelgeuse` at `1.40 s` (`PASS`) | `r05_scale` 9:16 Mars-orbit scale (`10 MILLION` / **`YEARS OLD`**), `Betelgeuse` at `0.06 s` (`PASS`) |
| **(3) Cut 1 `≤3.0 s`, visual beat every `2.2–4.0 s`, max hold `≤6.0 s`** | Cut 1 `2.20 s`, 8 cuts, max `2.78 s` (`PASS`) | Cut 1 `2.50 s`, 11 cuts, max `4.28 s` (`PASS`) | Cut 1 `2.96 s`, 8 cuts, max `3.80 s` (`PASS`) | Cut 1 `2.60 s`, 7 cuts, max `3.96 s` (`PASS`) |
| **(4) `4–5 s` sentence-1 seam bridged into concrete number/mechanism (`<0.25 s` breath, no meta)** | `4.33–4.51 s` (`0.18 s` breath) into `"By February 2020, it had dropped to about a third..."` (`PASS`) | `3.86–4.06 s` (`0.20 s` breath) into `"That star is dying. So is Betelgeuse about to explode?"` (`PASS`) | `2.96–3.16 s` (`0.20 s` breath) into `"The first sign would not be light at all. It would be a flood of... neutrinos"` (`PASS`) | `5.26–5.46 s` (`0.20 s` breath) into `"Why so fast? Because it is heavy. With somewhere around 15 to 20 times..."` (`PASS`) |
| **(5) Payoff withheld until `≥70%` runtime (`~16–21 s`), never at `9–14 s` banner** | Dust cloud eclipse at `16.03–21.15 s` (`68%–90%` of `23.48 s`) (`PASS`) | Garden sky + when answer at `29.80–33.78 s` (`83%–94%` of `36.08 s`) (`PASS`) | Half-Moon + broad daylight at `16.00–21.64 s` (`67%–90%` of `23.94 s`) (`PASS`) | `100,000×` Sun light + die young at `14.18–21.14 s` (`60%–90%` of `23.44 s`) (`PASS`) |
| **(6) Test A opening Short on rotated weekday (`Fri 11 Dec`)** | — | Included (`s00–s06`, `36.08 s`) on rotated Friday slot (`PASS`) | — | Ready if Test A stops at `028` (`PASS`) |
| **(7) End card shows `'Is Betelgeuse About to Explode?'` + links `vP1BbqZ_dnM`** | `21.48–23.48 s` (`PASS`) | `34.08–36.08 s` (`PASS`) | `21.94–23.94 s` (`PASS`) | `21.44–23.44 s` (`PASS`) |

---

## Next Step (Queued Assembly & Gate Job)

The £0 Mini assembly job builds all three weekday Shorts (plus the Reserve Short if needed) in `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/`, runs `gate_shorts_open.py check --air-date`, `sfx_kit.py level`, `picture_qa.py`, `polish_gate.py`, `thumb_preview.py short --score`, and the caption/title-safe bounding-box audit, builds the no-Orbit covers, copies `<120 MB` phone MP4s + sheets to OWB UAT and NAS staging (`/Volumes/data/mac-mini-archive/youtube-staging/029/shorts_v01/`), commits `10_Shorts/shorts_v01_pack/`, and parks for Chief's visual PASS before any upload.
