# Sound Design (SFX) Plan v01 — 034 Why Pluto's Frozen Heart Has Zero Craters (Pluto)

- **Episode:** `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters`
- **VO Master:** `02_Voiceover/pluto_frozen_heart_vo_v03.wav` (`616.160 s`, `-19.9 LUFS` integrated, `-23.0 dB` mean, `-3.7 dBTP` true peak; SHA-256 `2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685`)
- **Target Delivery Runtime:** `634.16 s` (`10.57` minutes)
- **House SFX Kit (`£0` zero-spend synthesis):**
  ```bash
  python3 scripts/sfx_kit.py make --out-dir 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/06_Sound-Effects/kit_v01
  ```
  Synthesises `rumble_low.wav`, `whoosh_soft.wav`, and `tick_label.wav` locally with zero sample licensing and zero credit spend.
- **Level Gate (`Polish Pass` §1, `AGENTS.md`):**
  ```bash
  python3 scripts/sfx_kit.py level \
    --vo 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/02_Voiceover/pluto_frozen_heart_vo_v03.wav \
    --sfx 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/06_Sound-Effects/pluto_sfx_stem_v01.wav \
    --bed 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/05_Music/pluto_score_bed_v01.mp3 \
    --minutes 10.57
  ```
  - Integrated SFX stem loudness `≥ 12 LU` below VO integrated loudness (`-19.9 LUFS` → SFX stem integrated `≤ -31.9 LUFS`);
  - During active speech, SFX and music bed each sit `≥ 10 LU` below VO;
  - During VO pauses (`0.70 s` inter-chapter gaps), SFX stay `≥ 6 LU` below VO integrated loudness (`≤ -25.9 LUFS`);
  - Never use Veo or source-clip audio (`-an` on all video plates);
  - Restraint lock: at most `1` tick per `0.5 s`, no whoosh on plain cuts, no cartoon whooshes or comedy stings.

---

## 1. Low Rumble Placements (`rumble_low.wav`, `2.2–3.5 s`, `-14 LU` under VO)

| # | Row | Timestamp (s) | Visual / Narrative Beat |
|---:|---|---:|---|
| 1 | `R01` | `4.40–7.80` | Explicit script `v03` line 9 cue: zooming across the smooth, crater-free polygons of Sputnik Planitia bordered by dark cratered highlands (`PIA19937`). |
| 2 | `R05` | `39.80–43.20` | Sweeping over `260 km` highland impact craters into the churning solid-nitrogen convection cells of Sputnik Planitia (`PIA20726`). |
| 3 | `R31` | `261.50–265.00` | Atlas V 551 rocket liftoff carrying the `478 kg` New Horizons probe from Cape Canaveral at `58,536 km/h` (`ksc_011906_nh_launchchange`). |
| 4 | `R37` | `320.20–323.70` | Jupiter gravity assist (`+14,000 km/h`) and Io's giant Tvashtar volcanic plume eruption (`File:Jupiter&Io.jpg`). |
| 5 | `R42` | `368.50–371.80` | Midpoint twist (`"Wrong."` at `368.52 s`) as Pluto's `1,000 km` nitrogen heart reveals active planetary-scale convection. |
| 6 | `R47` | `418.20–421.60` | Towering `2 to 3 km` water-ice mountains and `600 km` tectonic troughs bordering Sputnik Planitia (`PIA19954` / `PIA20473`). |
| 7 | `R56` | `509.50–513.00` | Subsurface cutaway (`−226 to −240 °C`, `~13 microbars`) as basal liquid nitrogen rises through northern cracks (`code_graphic_034_r56_basal_melting_cutaway.mp4`). |
| 8 | `R67` | `607.50–611.00` | Active nitrogen geysers erupting on Triton's `−235 °C` frozen crust in the Real Worlds series bridge (`PIA01536`). |

---

## 2. Soft Whoosh Placements (`whoosh_soft.wav`, `0.6–0.9 s`, `-14 LU` under VO)

| # | Row | Timestamp (s) | Camera / Scale Transition Beat |
|---:|---|---:|---|
| 1 | `R03` | `20.14` | New Horizons approach sequence diving within `12,500 km` of Pluto on 13–14 July 2015 (`File:The Pluto System As Seen By New Horizons Spacecraft.webm`). |
| 2 | `R14` | `109.70` | Scale transition comparing Pluto (`2,377 km`, `1/5` Earth, `2/3` Moon) against the continental United States (`code_graphic_034_r14_pluto_diameter_scale.mp4`). |
| 3 | `R16` | `135.94` | Photon pulse racing `5.9 billion km` (`39 AU`) from the Sun to Pluto across `5.5 hours` (`code_graphic_034_r16_sunlight_distance_bar.mp4`). |
| 4 | `R22` | `192.90` | Scale transition into the Pluto-Charon double-planet caliper (`1,214 km`, `19,640 km` orbit — `20×` closer than Earth's Moon). |
| 5 | `R38` | `331.90` | New Horizons `11:49 UT` closest-approach flyover across Pluto on 14 July 2015 (`File:Pluto-FlyoverAnimation-20150918.webm`). |
| 6 | `R50` | `451.96` | Low-altitude glide over jagged `2–3 km` water-ice mountains dusted with reddish methane frost (`PIA20732` / `PIA19947`). |
| 7 | `R59` | `535.06` | Looking back from `200,000 km` at Pluto's receding crescent and glowing blue atmospheric haze (`PIA21590`). |
| 8 | `R61` | `550.08` | High-speed approach within `3,500 km` of double-lobed Arrokoth (`6.4 billion km` from Earth, `File:New Horizons Approach to Arrokoth.ogv`). |

---

## 3. Subtle Label/Data Ticks (`tick_label.wav`, `-16 LU` under VO, `≥ 0.5 s` Spacing)

| # | Row | Timestamp (s) | Synced Overlay / Card / Chart Lock |
|---:|---|---:|---|
| 1 | `R02` | `9.70` | Hook `NUMBER OBJECT` caliper lock: `1,000 KM WIDE · 0 CRATERS` |
| 2 | `R02` | `14.50` | `SCALE` #1 comparison badge: `> TEXAS + OKLAHOMA` |
| 3 | `R03` | `20.30` | `WHEN` #1 & #2 timeline drop: `13 JULY 2015 · 14 JULY 2015` |
| 4 | `R08` | `66.15` | `WHEN` #3 timeline drop: `18 FEBRUARY 1930` |
| 5 | `R09` | `69.40` | `WHO` #1 card slide-in: `Clyde Tombaugh (1906–1997)` |
| 6 | `R10` | `82.85` | `WHEN` #4 timeline drop: `14 MARCH 1930` |
| 7 | `R10` | `86.65` | `WHO` #2 card slide-in: `Venetia Burney (1919–2009)` |
| 8 | `R10` | `91.25` | `FACT` #1 card fade-in: `NAMED AT AGE ELEVEN` |
| 9 | `R14` | `109.90` | Ch 1 `NUMBER OBJECT` caliper lock: `2,377 KM DIAMETER (1/5 EARTH)` |
| 10 | `R16` | `136.10` | `DATA` #2b bar lock: `5.9B KM · 39 AU · 5.5 HRS` (`1/900 SUN`) |
| 11 | `R19` | `159.55` | `WHEN` #5 timeline drop: `JUNE 1978` |
| 12 | `R22` | `193.10` | `DATA` #3a caliper lock: `CHARON: 1,214 KM (~1/2 PLUTO)` |
| 13 | `R25` | `213.55` | Ch 2 `NUMBER OBJECT` distance badge: `20× CLOSER THAN OUR MOON` |
| 14 | `R27` | `225.80` | `DATA` #3b tidal lock dial: `153 HOURS (6.4 EARTH DAYS)` |
| 15 | `R28` | `241.85` | `FACT` #2 card fade-in: `CHARON NEVER SETS` |
| 16 | `R31` | `261.55` | `WHEN` #6 timeline drop: `19 JANUARY 2006` |
| 17 | `R32` | `271.10` | Ch 3 `NUMBER OBJECT` speedometer lock: `58,536 KM/H LAUNCH` |
| 18 | `R33` | `281.85` | `WHEN` #7 timeline drop: `2006` (`4.5B YEARS AGO` at `291.55 s`) |
| 19 | `R35` | `304.70` | `DATA` #4b orbit ellipse lock: `248-YEAR ORBIT (30–49.3 AU)` |
| 20 | `R36` | `314.45` | `WHEN` #9 (`1979–1999`) + `FACT` #3 (`CLOSER THAN NEPTUNE` at `316.35 s`) |
| 21 | `R37` | `320.25` | `WHEN` #10 timeline drop: `28 FEBRUARY 2007 (+14,000 KM/H)` |
| 22 | `R38` | `332.05` | `WHEN` #11 timeline drop: `14 JULY 2015 (11:49 UT)` |
| 23 | `R40` | `349.25` | `WHEN` #12 (`25 OCTOBER 2016`) + `DATA` #4c (`6.25 GB / 15 MO AT 1–2 KBPS`) |
| 24 | `R44` | `387.35` | Ch 4 `NUMBER OBJECT` bar lock: `1,000 KM · LARGEST GLACIER` |
| 25 | `R48` | `427.35` | `DATA` #5b elevation & gravity lock: `2–3 KM PEAKS · 6% GRAVITY` |
| 26 | `R51` | `461.55` | Ch 5 `NUMBER OBJECT` thermometer lock: `−226 TO −240 °C` (`FACT` #4 `WATER-ICE BEDROCK` at `469.55 s`) |
| 27 | `R53` | `484.25` | `WHEN` #13 (`5 AUGUST 2026`) + `WHO` #3 (`Alan Stern (born 1957)` at `488.25 s`) |
| 28 | `R56` | `509.65` | `DATA` #6b cutaway lock: `~13 MICROBARS · BASAL LIQUID N₂` |
| 29 | `R61` | `550.25` | `WHEN` #14 timeline drop: `1 JANUARY 2019 (ARROKOTH 6.4B KM)` |
| 30 | `R63` | `567.85` | `WHEN` #15 (`1 OCTOBER 2024`) + Ch 6 `NUMBER OBJECT` (`60 AU · 2× PLUTO DISTANCE`) |
