# 027 script v01: claims for Gemini to check (Claude, 5 Oct 2026)

The script `earth_spin_script_master_v01.md` was drafted before `SOURCES.md` landed.

**Gemini:**
- Merge these rows into `SOURCES.md` under the heading **"Added by Claude for script v01 (5 Oct). Gemini: verify each row and add the exact quote"**, the same way as 026.
- Verify each row, add the exact quote, and flag anything wrong.
- Spoken wording is Claude's call. Gemini flags errors and doesn't rewrite lines.

| # | Spoken claim | Number behind it | Source to check |
|---|---|---|---|
| 1 | In Britain the ground carries you east at about a thousand km/h; the equator is faster than a jet airliner | 465.1 m/s × cos 51.5° ≈ 290 m/s ≈ 1,040 km/h; equator ≈ 1,670 km/h; airliner cruise ≈ 900 km/h | IERS / NASA Earth Fact Sheet (sidereal day 23.934 h, equatorial radius 6,378.137 km) |
| 2 | You weigh about half of one percent less at the equator than at the poles, because of the spin | Normal gravity 9.7803 vs 9.8322 m/s² (≈0.53%). Both the centrifugal term and the bulge come from rotation | WGS 84 normal gravity formula (NGA TR8350.2) |
| 3 | Earth is about 43 km wider across the equator than pole to pole | 2 × (6,378.137 − 6,356.752) ≈ 42.8 km | WGS 84 |
| 4 | Foucault, Paris, 1851, 67 m wire, the swing turns because the floor does | Panthéon, March 1851, 28 kg bob; Paris period ≈ 31.8 h | Musée des Arts et Métiers / Panthéon (CMN) |
| 5 | Earth turns west to east, so the Sun rises in the east | Prograde rotation | NASA |
| 6 | After a sudden stop the equatorial air keeps going at more than 1,500 km/h, faster than sound and several times the strongest gust ever measured | 1,670 km/h vs sound ≈ 1,235 km/h (sea level, 15 °C) vs 408 km/h | WMO Archive of Weather and Climate Extremes (Barrow Island, 10 Apr 1996, Cyclone Olivia) |
| 7 | At the North Pole you would hardly notice | Surface speed → 0 at the pole | Geometry |
| 8 | The energy in Earth's spin equals about forty thousand years of the sunlight reaching Earth | E = ½Iω²: I ≈ 8.04 × 10³⁷ kg m², ω = 7.292 × 10⁻⁵ rad/s → 2.14 × 10²⁹ J. Intercepted sunlight 1,361 W/m² × π(6.371 × 10⁶ m)² ≈ 1.74 × 10¹⁷ W ≈ 5.5 × 10²⁴ J/yr → ≈ 39,000 yr | NASA Earth Fact Sheet (moment of inertia factor 0.3307); total solar irradiance (Kopp & Lean 2011) |
| 9 | A slow stop sends the oceans to two polar oceans, with one band of land around the equator | Esri model of a non-rotating Earth | Witold Fraczek, Esri ArcNews / ArcUser 2014, "Why Earth's Oceans Would Migrate to the Poles if It Stopped Spinning" |
| 10 | With no spin, one day lasts a year: six months light, six months dark | Solar day = orbital period when the sidereal rotation is zero | Geometry |
| 11 | Venus turns once in 243 Earth days, backwards; its day is longer than its year | Sidereal 243.02 d retrograde; year 224.7 d | NASA NSSDCA Venus Fact Sheet. It must match 023 |
| 12 | Tides drag on the seabed and the Moon takes the spin, drifting about four cm a year | 3.82 ± 0.07 cm/yr | Lunar laser ranging (Dickey et al. 1994, Science 265, 482). Matches 013's "3.8 cm" |
| 13 | The Moon is tidally locked, which is why we see one face | Rotation = orbit = 27.32 d | NASA |
| 14 | Babylonian, Chinese and medieval eclipse records only fit if the day grows by nearly two ms a century; otherwise they'd have been seen hundreds or thousands of km away | +1.78 ms/cy (720 BC – AD 2015). ΔT ≈ 5–6 h at 700 BC → ~80° of longitude | Stephenson, Morrison & Hohenkerk 2016, Proc. R. Soc. A 472, 20160404 |
| 15 | Fossil corals about 380 Myr old show about 400 daily lines a year; the day was about 22 h | Middle Devonian ≈ 400 lines; 8,766 h / 400 ≈ 21.9 h | Wells 1963, Nature 197, 948 |
| 16 | Since the late 1960s the second has been set by atomic clocks | Caesium SI second, 13th CGPM 1967/68 | BIPM SI Brochure |
| 17 | Since 1972, 27 leap seconds; the last at the end of 2016 | 31 Dec 2016 | IERS Bulletin C |
| 18 | Core, oceans and melting ice all nudge the spin; in the last few years Earth has run fast, with some days more than 1 ms short | Shortest days 2020–2024 about 1.3–1.66 ms short (for example 5 Jul 2024) | IERS EOP data; Agnew 2024, Nature 628, 333 |
| 19 | Timekeepers plan to stop adding leap seconds by 2035 | CGPM 2022 Resolution 4 | BIPM |
| 20 | The Moon would need tens of billions of years to lock Earth's day to its month; the Sun changes first | ~50 Gyr estimate vs ~5 Gyr Sun main sequence remaining | Murray & Dermott, *Solar System Dynamics*, or a NASA explainer; Sackmann et al. 1993 for the Sun |
| 21 | Earth formed about four and a half billion years ago; the spin is that first push still running down | 4.54 ± 0.05 Gyr | Dalrymple 2001, GSL Special Publication 190 |

**Tone lock:**
- Calm physics, never doom. No disaster footage and no damaged cities.
- Stay off time dilation (024) and stellar distance (026).
- Use Venus and the Moon as one-line callbacks only.
