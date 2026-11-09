# 032 Titan — First-30-Seconds Re-Cut Plan (`J2435`, Follow-On to `J2428` / PR #665)

- **Episode:** `032_What-Would-Happen-If-You-Landed-On-Titan` (*What Would Happen If You Landed on Titan?*)
- **Current Master Inspected:** `09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v01.mp4` (`585.44 s`, `30 fps` CFR, assembled by `07_Edit-Project/_assemble_032_full_master_v01.py`, cut manifest `07_Edit-Project/full_master_v01_pack/cuts_v01.json`)
- **Locked Script & VO:** `01_Script/titan_landing_script_master_v02.md` + `02_Voiceover/titan_landing_vo_v02b.wav` (`02_Voiceover/stt/titan_landing_vo_v02b/stt_raw.json`)
- **Spend:** `£0.00` (uses locked `titan_landing_vo_v02b.wav` and existing `J2089`/`J2378`-approved harvest plates and `composites_v01` graphics on `studio-live` NAS)

---

## 1. Audit of Current Opening (`0:00–0:45` in `v01`) Against `AGENTS.md` First-30s Rule

| Rule Check (`AGENTS.md` Picture QA → *The first 30 seconds of a long*) | Current `v01` Status (`0:00–0:45`) | Verdict | Required Change for `v02` |
|---|---|---|---|
| **1. Frame 0 = single most striking real image of subject, already moving; no Orbit, title, logo or fade before 0:30** | Frame 0 (`R01` cut 1, `0.00–3.10 s`) shows real Cassini natural-colour image `PIA20016.jpg` (orange Titan in front of Saturn's rings) with no Orbit, title, logo, or fade. **However**, `render_still_cut()` in `_assemble_032_full_master_v01.py` loops a static PNG (`-loop 1 -i png_path`), so Frame 0 has **zero motion**. | **FAIL (static still at Frame 0)** | Upgrade `render_still_cut()` to apply the `polish_gate`-verified symmetric sub-pixel PIL `Image.Transform.EXTENT(..., BICUBIC)` zoom (`z = 1.000 -> 1.045`) across every still cut so Frame 0 (`PIA20016.jpg`) is visibly moving from frame 0. |
| **2. First line states the stakes/mystery in the title's own words and ends before `0:08`** | Sentence 1 (`0.16–5.24 s`): *"If you stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"* Ends at **`5.24 s < 8.00 s`**. | **PASS (`5.24 s`)** | Keep Sentence 1 intact (`0.16–5.24 s`). |
| **3. No agenda/meta-promise, no restated hook, no side question in `0:00–0:30`; every sentence adds a new fact, number or image** |- Sentence 1 (`0.16–5.24 s`): Title survival question.<br>- Sentence 2 (`6.38–9.36 s`): *"Your body would not explode, and your blood would not boil."* (Immediate physical answer).<br>- Sentence 3 (`10.06–22.50 s`): *"In fact, while spacecraft in orbit around Saturn fly through a vacuum, Titan wraps itself in an orange nitrogen sky that presses on you about one and a half times harder than the air in your room right now."* (New fact + `1.47 bar / 1.5x Earth` number).<br>- Sentence 4 (`23.34–25.22 s`): *"That pressure would not hurt you at all."*<br>- Sentence 5 (`26.30–31.58 s`): *"What would kill you is the cold and the fact that there is almost no oxygen to breathe."* (`-179 °C · No oxygen`).<br>- Zero agenda/meta-promise lines; preview questions (`R05–R06`) begin after `0:30` at `32.76 s`. | **PASS** | Keep locked VO words intact (or optionally trim the `4.64 s` vacuum clause `10.06–14.70 s` — see §2). |
| **4. Concrete payoff hint (a number, a date, a picture of the answer) by `0:20`** | Spoken payoff number (`"about one and a half times harder"`, `18.96–20.70 s`) straddles `0:20`, and `code_graphic_032_r03_pressure_v01.mp4` (`1.47 BAR · 1.5× EARTH'S AIR`) only cuts in at `19.33 s` (`0.67 s` before `0:20`). | **BORDERLINE (`19.33–20.70 s`)** | Move `code_graphic_032_r03_pressure_v01.mp4` (`1.47 BAR · 1.5× EARTH'S AIR`) earlier to **`16.53–20.13 s`** (and/or tighten `0.80 s` of inter-sentence pause in `5.24–10.06 s`) so both the visual `1.47 bar` payoff gauge and spoken `"one and a half times"` land cleanly before `0:20`. |
| **5. Picture change at least every `4 s` (`<= 4.00 s`) in `0:00–0:30`; no chapter card, starfield breath or music sting before `0:45`** | Chapter 1 (`R07`, *1655 · Christiaan Huygens*) starts at **`50.85 s > 45.00 s`** with no chapter card before `0:45` (**PASS**). **However**, 3 cuts in `0:00–0:30` exceed `4.00 s`:<br>- `R03` Cut 1 (`PIA22766.jpg`, `9.733–14.533 s`) = **`4.80 s > 4.00 s` (FAIL)**<br>- `R03` Cut 2 (`PIA21902.tif`, `14.533–19.333 s`) = **`4.80 s > 4.00 s` (FAIL)**<br>- `R04` Cut 1 (`PIA08167.jpg`, `22.933–28.567 s`) = **`5.63 s > 4.00 s` (FAIL)**<br>*(Also in `32.17–50.85 s`, `R05` Cut 1 is `4.67 s` and `R06` Cut 1 is `10.40 s`.)* | **FAIL (`4.80 s`, `4.80 s`, `5.63 s` cuts in `0:00–0:30`)** | Re-cut `R03` (`13.20 s` -> 4 cuts of `2.80–3.60 s`) and `R04` (`9.23 s` -> 3 cuts of `2.80–3.60 s`) so **every cut in `0:00–0:32.17` is `2.80–3.60 s <= 4.00 s`** (and split `R05`/`R06` so no cut in `0:00–0:50.85` exceeds `3.80 s`). |

---

## 2. Locked VO Transcript & Timing (`0:00–0:50.85`, `titan_landing_vo_v02b.wav`)

### Primary Route (Zero-Shift Locked VO — Recommended)
Keeps `titan_landing_vo_v02b.wav` bit-for-bit untouched (`0.00 s` shift to `R01–R52` and `06_Sound-Effects` cues), since Sentence 1 already finishes at **`5.24 s < 8.00 s`**, `"about one and a half times"` begins at **`18.96 s < 20.00 s`**, and moving `r03_pressure` to `16.53–20.13 s` puts the `1.47 BAR · 1.5× EARTH'S AIR` payoff graphic on screen **`3.47 s` before `0:20`**:

| Row | Time Span (`s`) | Spoken VO (`titan_landing_vo_v02b.wav` exact STT word span) | Rule Role |
|---|---|---|---|
| **R01** | `0.00–6.20` | *"If you stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"* (`0.16–5.24 s`) | **Hook question in title's words; ends at `5.24 s < 8.00 s`** |
| **R02** | `6.20–9.73` | *"Your body would not explode, and your blood would not boil."* (`6.38–9.36 s`) | **Immediate physical answer #1 (survival check)** |
| **R03** | `9.73–22.93` | *"In fact, while spacecraft in orbit around Saturn fly through a vacuum, Titan wraps itself in an orange nitrogen sky that presses on you about one and a half times harder than the air in your room right now."* (`10.06–22.50 s`; `"about one and a half times"` at `18.96–20.24 s`) | **Concrete numerical payoff (`1.47 bar / 1.5× Earth's air` on screen `16.53–20.13 s`, `< 0:20`)** |
| **R04** | `22.93–32.17` | *"That pressure would not hurt you at all. What would kill you is the cold and the fact that there is almost no oxygen to breathe."* (`23.34–31.58 s`) | **Lethal mechanism (`-179 °C` & `~0% O₂`) completing the first 30 s** |
| **R05** | `32.17–40.43` | *"So why are the pebbles under your boots made of frozen water? Why does its rain fall in slow motion?"* (`32.76–38.90 s`) | Post-`0:30` bridge questions (`3 cuts <= 3.60 s`) |
| **R06** | `40.43–50.85` | *"And why is this freezing moon one of the best places in the solar system to look for the building blocks of life?"* (`39.44–50.44 s`) | Bridge into Ch 1 (`R07` starts at `50.85 s > 45.00 s`) |

*(Optional Pause-Tightening Variant: If desired, trimming `0.60 s` from the inter-sentence pause `5.24–6.38 s` and `0.25 s` from `9.36–10.06 s` — and restoring `+0.85 s` into the `31.58–32.76 s` pause before `R05` — shifts `"one and a half times harder"` to `18.11–19.85 s` while keeping `R05–R52` at their exact locked timestamps.)*

---

## 3. Cut-by-Cut Re-Cut Plan (`0:00–0:50.85`, `R01–R06`)

Every cut in `0:00–0:32.17` (`R01–R04`) is **`2.80–3.60 s`** (`<= 4.00 s` hard cap), and `R05–R06` (`32.17–50.85 s`) are also split to **`<= 3.60 s`** so the entire `0:00–0:50.85` opening moves briskly with zero long holds:

| Cut # | Row | Timeline (`s`) | Dur (`s`) | Frames (`30 fps`) | Kind & Asset | Visual / Motion / Overlay Spec |
|---:|---|---|---:|---:|---|---|
| **1** | `R01` | `0.000–3.100` | `3.100` | `93` | `STILL`: `PIA20016.jpg` (`use_idx=1`) | **Frame 0 lock:** Cassini natural-colour view of orange Titan in front of Saturn's rings, **already moving at frame 0** via smooth sub-pixel BICUBIC zoom (`z = 1.000 -> 1.045`). No Orbit, title, or fade. |
| **2** | `R01` | `3.100–6.200` | `3.100` | `93` | `STILL`: `PIA08167.jpg` (`use_idx=1`) | Cassini golden-orange atmospheric limb of Titan, smooth BICUBIC push (`z = 1.000 -> 1.045`). |
| **3** | `R02` | `6.200–9.733` | `3.533` | `106` | `COMP`: `r02_survive_check` (`code_graphic_032_r02_survive_check_v01.mp4`) | Animated survival check card over moving Titan plate (`NO EXPLOSION · BLOOD DOES NOT BOIL`). |
| **4** | `R03` | `9.733–13.133` | `3.400` | `102` | `STILL`: `PIA22766.jpg` (`use_idx=1`) | Cassini wide view of Saturn & rings in hard vacuum (`3.40 s <= 4.00 s`, was `4.80 s`), smooth BICUBIC push. |
| **5** | `R03` | `13.133–16.533` | `3.400` | `102` | `STILL`: `PIA21902.tif` (`use_idx=1`) | Cassini close-up of Titan's dense orange nitrogen haze layer (`3.40 s <= 4.00 s`, was `4.80 s`), smooth BICUBIC push. |
| **6** | `R03` | `16.533–20.133` | `3.600` | `108` | `COMP`: `r03_pressure` (`code_graphic_032_r03_pressure_v01.mp4`) | **Payoff before `0:20`:** Animated `1.47 BAR · 1.5× EARTH'S AIR` pressure gauge (`16.53–20.13 s`) as VO says *"that presses on you about one and a half times harder"*. |
| **7** | `R03` | `20.133–22.933` | `2.800` | `84` | `STILL`: `PIA21889.jpg` (`use_idx=1`, or `PIA08167` wide / `PIA14909`) | Real Cassini crescent/haze plate of Titan (`2.80 s <= 4.00 s`) separating `r03_pressure` from `R04` (`"than the air in your room right now."`). |
| **8** | `R04` | `22.933–25.767` | `2.833` | `85` | `STILL`: `PIA08167.jpg` (`use_idx=2`) | Reframed 88% crop on Titan's golden nitrogen atmosphere (`2.83 s <= 4.00 s`, was `5.63 s`) — *"That pressure would not hurt you at all."* |
| **9** | `R04` | `25.767–28.567` | `2.800` | `84` | `STILL`: `PIA21889.jpg` (`use_idx=2`, or `PIA20016` tight crop) | Reframed 88% crop on Titan's cold backlit upper haze (`2.80 s <= 4.00 s`) — *"What would kill you is the cold"* |
| **10** | `R04` | `28.567–32.167` | `3.600` | `108` | `COMP`: `r04_cold` (`code_graphic_032_r04_cold_v01.mp4`) | Animated `-179 °C · NO OXYGEN TO BREATHE` card (`3.60 s <= 4.00 s`) — *"and the fact that there is almost no oxygen to breathe."* |
| **11** | `R05` | `32.167–35.467` | `3.300` | `99` | `STILL`: `PIA07231.jpg` (`use_idx=1`) | Huygens surface water-ice pebbles (`3.30 s <= 4.00 s`, was `4.67 s`). |
| **12** | `R05` | `35.467–39.067` | `3.600` | `108` | `COMP`: `r05_rain_preview` (`code_graphic_032_r05_rain_preview_v01.mp4`) | Slow-motion methane rain preview graphic (`3.60 s`). |
| **13** | `R05` | `39.067–40.433` | `1.367` | `41` | `STILL`: `NASA_Dragonfly_BannerFactSheet_2024` (`use_idx=1`) | Dragonfly rotorcraft over Titan dunes (`1.37 s`, or balance `R05` as `2.60 s + 3.60 s + 2.07 s = 8.27 s`). |
| **14–16** | `R06` | `40.433–50.850` | `3.47 / 3.47 / 3.47` | `104 / 104 / 104` | `STILL`: `PIA14922.jpg` (`u1`), `PIA21440.jpg` (`u1`), `PIA21440.jpg` (`u2`) | Split `10.42 s` `R06` into 3 cuts (`~3.47 s` each) over real Cassini Titan globe & surface plates before Ch 1 (`R07` at `50.85 s`). |

---

## 4. Exact Assembler Changes (`07_Edit-Project/_assemble_032_full_master_v01.py` -> `v02`)

1. **In `STILL_FILES` and `ROW_CUT_SPECS` (`rows 1..6`):**
   - Add harvested reserve plate `PIA21889` (`"PIA21889.jpg", "NASA/JPL-Caltech/Space Science Institute", "Titan in Natural Color and Haze (Cassini)"`) and `PIA21440` (`"PIA21440.jpg", "NASA/JPL-Caltech/Space Science Institute", "Titan Surface and Atmosphere Mosaic (Cassini)"`) from `03_Reference-Material/harvest_J2089_v01/` (verified present on NAS in `HARVEST_POOL_v01.json`, `0` prior appearances so `<= 2` appearances rule is 100% preserved).
   - Replace `ROW_CUT_SPECS[1..6]` with:
     ```python
     1: [
         ("STILL", "PIA20016", 1, 3.10, None),
         ("STILL", "PIA08167", 1, None, None),
     ],
     2: [
         ("COMP", "r02_survive_check", 3.55),
     ],
     3: [
         ("STILL", "PIA22766", 1, 3.40, None),
         ("STILL", "PIA21902", 1, 3.40, None),
         ("COMP", "r03_pressure", 3.60),
         ("STILL", "PIA21889", 1, None, None),
     ],
     4: [
         ("STILL", "PIA08167", 2, 2.83, None),
         ("STILL", "PIA21889", 2, None, None),
         ("COMP", "r04_cold", 3.60),
     ],
     5: [
         ("STILL", "PIA07231", 1, 2.60, None),
         ("COMP", "r05_rain_preview", 3.60),
         ("STILL", "NASA_Dragonfly_BannerFactSheet_2024", 1, None, None),
     ],
     6: [
         ("STILL", "PIA14922", 1, 3.47, None),
         ("STILL", "PIA21440", 1, 3.47, None),
         ("STILL", "PIA21440", 2, None, None),
     ],
     ```
2. **In `render_still_cut(cut, dest)`:**
   - Replace static `-loop 1` PNG encoding with the smooth symmetric sub-pixel `Image.Transform.EXTENT(..., Image.Resampling.BICUBIC)` zoom (`z = 1.000 + 0.045 * (f_i / max(1, n - 1))`) piped to `ffmpeg`, so Frame 0 (`PIA20016.jpg`) and all still cuts move continuously and pass `polish_gate.py`.
3. **In `TICKS` (`SFX` tick list):**
   - Shift the `R03` pressure-card tick from `19.40` to `16.60` to match the new `16.53 s` in-point of `r03_pressure`.
4. **Output & Gates:**
   - Render `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` and run `clip_check.py`, `picture_qa.py`, `polish_gate.py`, `music_gate.py`, and `sfx_kit.py level`.

---

## 5. Assessment of Uploaded & Scheduled Films (`026`, `027`, `031`) Before Air

Per `J2435` brief: *For 026 Nearest Star, 027 Earth Stopped Spinning, 031 Magnetic Field Flips (uploaded, scheduled): say which could take a re-cut opening as a new version swapped before air without moving the slot, and what it would change; do not touch YouTube.*

All three (`026`, `027`, `031`) are currently `privacyStatus: "private"` with future `publishAt` schedules and `0` public views. Under the `AGENTS.md` Never list (*never swap a file on an existing YouTube ID; never re-render over an uploaded file*), each can take a re-cut opening before air by rendering a new `_v0N` master, uploading it as a fresh private video scheduled for the **exact same `publishAt` slot**, setting the old video ID to private with no schedule (`retired: true` in `UPLOADS.json`), and updating `UPLOADS.json` + linked Shorts' `long` IDs:

| Film | Current YouTube ID & Scheduled Slot | Lead Time (from 9 Nov 2026) | Can Take Re-Cut Opening Before Air Without Moving Slot? | Current First-30s Rule Violations | What a New Version (`_v0N`) Would Change |
|---|---|---|---|---|---|
| **026 Nearest Star** (*The Nearest Star Is One You Can't See (And It Has a Planet)*) | `c5AdqQsnnys` · **Sun 15 Nov 2026 18:00 UTC** (`026_NearestStar_v06_cfr18.mp4`) | **6 days** | **YES (High impact, £0, no Test A Short affected)** | 1. **Rule 3 FAIL (`20.88–33.10 s`):** Explicit 12.2 s agenda line (*"In this film I will show you which star it is, how anyone measured a distance that large, what that gap looks like if you shrink the whole thing down to fit on Earth, and how long it would take to get there."*).<br>2. **Rule 5 FAIL (`0:33` chapter & `> 4 s` cuts):** Chapter 1 starts at `0:33` (`< 0:45`); Row 1 cut 2 is `4.27 s` (`3.73–8.00 s`), Row 2 cut 1 is `5.53 s` (`8.00–13.53 s`), and Row 4 cuts are `4.47 s`, `4.17 s`, `4.40 s`. | 1. **VO (`-12.66 s` whole-sentence trim, £0):** Cut the `20.88–33.54 s` agenda sentence (`Row 4`) from the locked VO+bed or re-lay VO+bed. Row 5 (*"The nearest star to the Sun is called Proxima Centauri. It is a red dwarf..."*, `33.54–49.64 s`) moves up to **`20.88–36.98 s`** so every sentence in `0:00–0:30` adds a concrete fact.<br>2. **Picture (`<= 4.0 s` cuts):** Split Row 1 (`4.00 s + 4.00 s`), split Row 2 (`5.53 s` -> `2.80 s + 2.73 s`), keep Row 3 (`3.73 s + 2.83 s`), and split promoted Row 5 (`20.10–36.98 s`) into 5 cuts `<= 3.60 s`.<br>3. **Chapters & Swap:** Drop the `0:33` chapter marker so the first chapter break after `0:00` is *Measuring the Gap* at `1:49` (`> 0:45`); shift chapter timestamps & captions by `-12.66 s`; export `026_NearestStar_v07_cfr18.mp4`; upload to `2026-11-15T18:00:00Z`; retire `c5AdqQsnnys`; update `long` ID on `HZGTovJu_TQ` (16 Nov), `cwU_0WWeNZ4` (18 Nov), and `aAUgIGEuPwQ` (20 Nov). |
| **027 Earth Stopped Spinning** (*Earth Is Losing Its Spin (And the Moon Is Taking It)*) | `6bbbvfCx6zY` · **Sun 22 Nov 2026 18:00 UTC** (`027_EarthSpin_rough_v01m.mp4`) | **13 days** | **YES (High impact, £0, `0.00 s` shift after `0:23.14`)** | 1. **Rule 2 FAIL (`17.36–20.02 s`):** Title question (*"So what would happen if Earth stopped spinning? Not slowly. All at once."*) is held back until `17.36–23.14 s` instead of ending before `0:08`.<br>2. **Rule 5 FAIL (`0:23` chapter card & `> 4 s` cuts):** `PACKAGE_MANIFEST.json` has a chapter card/marker at **`0:23`** (`< 0:45`), and 6 of 7 cuts in `0:00–0:32` exceed `4.0 s` (`4.80 s`, `4.50 s`, `4.03 s`, `6.20 s`, `5.03 s`, `4.07 s`). | 1. **VO (`0:00–0:23.14` whole-sentence reorder, £0, `0.00 s` downstream shift):** Move *"So what would happen if Earth stopped spinning? Not slowly. All at once."* (`17.36–23.14 s`, `5.78 s`) to **`0:00.16–0:05.94`** (ends `< 0:08` ✅), followed at **`0:06.50–0:22.90`** by *"Right now, you are moving. If you are in Britain, the ground under you is carrying you east at about a thousand kilometres an hour [`1,040 km/h` payoff by `0:15 < 0:20` ✅]. At the equator it is faster than a jet airliner. And you feel nothing at all."* From `0:23.26` (*"Now imagine the impossible..."*) onward, timestamps remain 100% unchanged.<br>2. **Picture & Chapters:** Re-cut `0.00–32.00 s` from 7 cuts into **9 cuts of `2.90–3.80 s <= 4.0 s`** and remove the `0:23` chapter card/marker so the first chapter break after `0:00` is at `1:33` (`> 0:45`).<br>3. **Swap:** Export `027_EarthSpin_v02.mp4`, upload to `2026-11-22T18:00:00Z`, retire `6bbbvfCx6zY`, and update `Dm4xsF1Ateg` (23 Nov) `long` ID. |
| **031 Magnetic Field Flips** (*What Happens When Earth's Magnetic Field Flips?*) | `G5uMANXHtNU` · **Wed 2 Dec 2026 18:00 UTC** (`031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4`) | **23 days** | **YES (23 days lead time; picture-only or VO+picture)** | 1. **Rule 5 FAIL (`> 4 s` cuts in `0:00–0:30`):** 4 cuts exceed `4.00 s`: `R01` cut 1 (`4.60 s`), `R01` cut 2 (`4.44 s`), `R02` cut 2 (`5.20 s`), and `R04` cut 1 (`4.96 s`). Also `Chapters` lists Ch 1 at `0:36` (`< 0:45`, though `R05` on screen is an in-scene lower-third stamp, not a starfield card).<br>2. **Rule 2 / Rule 3 note:** Sentence 1 (`0.14–8.34 s`, *"Right now, the invisible magnetic shield around our planet is weakening, and the north magnetic pole is racing across the Arctic towards Siberia."*) ends at `8.34 s` (`0.34 s` past `0:08`), and the survival question comes in Sentence 3 (`12.54–17.08 s`) with `"No. We will survive."` at `18.12–20.08 s`; `R04` (`23.80–35.32 s`) asks 3 preview questions starting before `0:30`. | 1. **Picture re-cut (`0.00 s` VO shift, £0):** Split `R01` (`9.04 s` -> 3 cuts of `3.00 s, 2.60 s, 3.44 s`), split `R02` (`9.08 s` -> 3 cuts of `3.12 s, 3.00 s, 2.96 s`), and split `R04` cut 1 (`4.96 s` -> 2 cuts of `2.48 s + 2.48 s`) so every cut in `0:00–0:36.16` is `2.48–3.68 s <= 4.00 s`.<br>2. **Optional VO trim (`£0`):** Tighten `0.45 s` of pause in `R01` so Sentence 1 ends at `7.89 s < 8.00 s` (or trim `0.14–4.28 s` *"Right now... is weakening, and"* so *"Earth's north magnetic pole is racing across the Arctic towards Siberia — when north and south swap places, will life on Earth survive?"* ends by `0:08`), and optionally trim `R04`'s 3 preview questions (`23.80–36.16 s`, `-12.36 s`) so `1905, Central France` starts at `23.80 s`.<br>3. **Swap:** Export `031_..._master_v03.mp4`, upload to `2026-12-02T18:00:00Z`, retire `G5uMANXHtNU`, and update `UPLOADS.json` + scheduled Test A Short `C8lPx5N2DwM` (5 Dec). |
