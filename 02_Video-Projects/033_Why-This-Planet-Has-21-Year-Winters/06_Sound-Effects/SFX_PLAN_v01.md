# Sound Design (SFX) Plan v01 — 033 Why This Planet Has 21-Year Winters (Uranus)

- **Episode:** `033_Why-This-Planet-Has-21-Year-Winters`
- **VO Master:** `02_Voiceover/uranus_vo_v01.wav` (`611.40 s`, `-15.6 LUFS` integrated)
- **Target Runtime:** `629.40 s` (`10.49` minutes)
- **House SFX Kit (`£0` zero-spend synthesis):**
  ```bash
  python3 scripts/sfx_kit.py make --out-dir 02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/06_Sound-Effects/kit_v01
  ```
  Generates `rumble_low.wav`, `whoosh_soft.wav`, and `tick_label.wav` with zero sample licensing and zero credit spend.
- **Level Gate (`Polish Pass` §1, `AGENTS.md`):**
  ```bash
  python3 scripts/sfx_kit.py level \
    --vo 02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/02_Voiceover/uranus_vo_v01.wav \
    --sfx 02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/06_Sound-Effects/uranus_sfx_stem_v01.wav \
    --bed 02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/05_Music/uranus_score_bed_v01.mp3 \
    --minutes 10.49
  ```
  - Integrated SFX stem loudness `≥ 12 LU` below VO integrated loudness (`≤ -27.6 LUFS`);
  - During active speech, SFX and music bed each sit `≥ 10 LU` below VO;
  - During VO pauses (`0.70 s` inter-chapter gaps), SFX stay `≥ 6 LU` below VO integrated loudness;
  - Never use Veo or clip audio (`-an` on all video plates);
  - At most `1` tick per `0.5 s`, no whoosh on plain cuts, no comedy stings.

---

## 1. Low Rumble Placements (`rumble_low.wav`, `2.0–3.5 s`, `-14 LU` under VO)

| # | Row | Timestamp (s) | Visual / Narrative Beat |
|---:|---|---:|---|
| 1 | `R02` | `4.80–7.60` | Distant Sun sinks below Uranus's turquoise horizon into a 21-year polar winter night. |
| 2 | `R28` | `234.00–237.50` | Ancient cataclysmic collision with an Earth-sized protoplanet knocking Uranus onto its side. |
| 3 | `R41` | `368.00–371.50` | December 2007 equinox awakening as convective storms erupt across the planet. |
| 4 | `R43` | `382.50–386.00` | Supersonic wind speeds reaching `900 km/h` (`560 mph`). |
| 5 | `R52` | `468.50–472.00` | Deep cutaway into the `≥ 80%` hot dense fluid mantle (`H₂O · CH₄ · NH₃`) and `4,982 °C` (`9,000 °F`) core. |
| 6 | `R55` | `500.50–504.00` | Extreme atmospheric pressures and temperatures crushing a descending metal spacecraft. |
| 7 | `R61` | `553.00–556.50` | Miranda's giant tectonic fault canyons (`12×` as deep as Earth's Grand Canyon). |

---

## 2. Soft Whoosh Placements (`whoosh_soft.wav`, `0.6–0.9 s`, `-14 LU` under VO)

| # | Row | Timestamp (s) | Camera / Scale Transition Beat |
|---:|---|---:|---|
| 1 | `R05` | `18.00` | Split-screen scale transition from Earth's `23.44°` tilt to Uranus's `97.77°` sideways tilt. |
| 2 | `R17` | `133.50` | Photon pulse racing `2.9 billion km` (`19 AU`) from the Sun to Uranus in `2 hours 40 minutes`. |
| 3 | `R32` | `266.20` | Voyager 2 arriving at Uranus on 24 January 1986 after `> 3 billion km`. |
| 4 | `R46` | `408.50` | Reveal of the `58.6°` (`≈ 60°`) tilted, `1/3`-radius-offset magnetic field and corkscrew tail. |
| 5 | `R51` | `459.50` | Camera dive into Uranus's blue-green methane cloud tops (`NO SOLID SURFACE`). |
| 6 | `R62` | `561.00` | Low-gravity `10-minute` rock fall over the rim of Miranda's Verona Rupes fault cliff. |
| 7 | `R66` | `600.50` | Next-episode bridge flying with New Horizons beyond Uranus to Pluto's nitrogen-ice heart. |

---

## 3. Subtle Label/Data Ticks (`tick_label.wav`, `-16 LU` under VO, `≥ 0.5 s` Spacing)

| # | Row | Timestamp (s) | Synced Overlay / Card / Chart Lock |
|---:|---|---:|---|
| 1 | `R03` | `8.60` | `DATA` #1a counter start: `21 EARTH YEARS` |
| 2 | `R05` | `18.30` | Hook `NUMBER OBJECT` protractor lock: `97.77°` |
| 3 | `R08` | `39.00` | Hook thermometer lock: `−224.2 °C` |
| 4 | `R10` | `58.20` | `WHEN` #1 timeline marker: `13 MARCH 1781` |
| 5 | `R10` | `61.00` | `WHO` #1 card slide-in: `William Herschel (1738–1822)` |
| 6 | `R11` | `70.20` | `FACT` #1 card fade-in: `FIRST TELESCOPE PLANET` |
| 7 | `R12` | `81.50` | `WHEN` #2 timeline marker: `1783` |
| 8 | `R12` | `89.50` | `WHO` #2 card slide-in: `Johann Elert Bode (1747–1826)` |
| 9 | `R14` | `108.00` | Ch 1 `NUMBER OBJECT` caliper lock: `51,118 KM · 4× EARTH` |
| 10 | `R17` | `133.60` | `DATA` #2b timer lock: `2 H 40 MIN SUNLIGHT` |
| 11 | `R19` | `155.20` | `WHEN` #3 timeline marker: `10 MARCH 1977` |
| 12 | `R21` | `183.70` | Ch 2 `NUMBER OBJECT` badge: `13 FAINT RINGS` |
| 13 | `R23` | `193.30` | `WHEN` #4 timeline marker: `22 DECEMBER 2005` |
| 14 | `R25` | `212.80` | `FACT` #2 card fade-in: `28 LITERARY MOONS` |
| 15 | `R32` | `266.20` | `WHEN` #6 timeline marker: `24 JANUARY 1986` |
| 16 | `R33` | `284.80` | `FACT` #3 card fade-in: `SIX HOURS AT URANUS` |
| 17 | `R35` | `304.40` | Ch 3 `NUMBER OBJECT` bar lock: `2.3% METHANE GAS` |
| 18 | `R36` | `316.20` | `DATA` #4b stamp: `MINIMUM: 49 KELVIN` |
| 19 | `R40` | `362.00` | `WHEN` #7 timeline marker: `DECEMBER 2007` |
| 20 | `R46` | `413.10` | `DATA` #5b dipole tilt lock: `≈ 60° MAGNETIC TILT` |
| 21 | `R51` | `459.70` | `FACT` #4 card fade-in: `NO SOLID SURFACE` |
| 22 | `R57` | `514.70` | `WHEN` #8 timeline marker: `16 FEBRUARY 1948` |
| 23 | `R58` | `521.10` | `WHO` #3 card slide-in: `Gerard Kuiper (1905–1973)` |
| 24 | `R63` | `570.80` | `WHEN` #9 timeline marker: `19 APRIL 2022 · 2023–2032` |
| 25 | `R64` | `583.50` | `WHEN` #10 timeline marker: `OCTOBER 2024` |
