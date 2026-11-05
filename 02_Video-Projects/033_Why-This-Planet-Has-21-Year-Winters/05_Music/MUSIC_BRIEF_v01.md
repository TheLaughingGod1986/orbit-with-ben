# Music Brief v01 — 033 Why This Planet Has 21-Year Winters (Uranus)

- **Episode:** `033_Why-This-Planet-Has-21-Year-Winters`
- **VO Master:** `02_Voiceover/uranus_vo_v01.wav` (`611.40 s`, accepted `KEEP` in `jobs/reviews/J2164/REVIEW.md`)
- **Target Music Runtime:** `629.40 s` (`10:29.40` — full `611.40 s` VO + `18.00 s` end-screen hold; music holds at full bed level `2.5 s` past the last word at `611.324 s` and fades cleanly over `626.40–629.40 s`)
- **Target Output Stem (at assembly stage):** `05_Music/uranus_score_bed_v01.mp3` + `05_Music/uranus_score_bed_v01_plan.json`
- **Generator:** `python3 04_Audio/tools/generate_music_bed.py` (API only; **not run in `J2165`**, £0 spent in this shot-list job)
- **Gate:** `python3 scripts/music_gate.py 02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters --bed 05_Music/uranus_score_bed_v01.mp3 --video <cut.mp4>`

---

## 1. Exact API Prompt (`Pace:` and `NOT:` Mandatory Lines)

```text
Crystalline, weightless space-documentary score for Uranus and its icy moon Miranda, alternating between suspended polar-night wonder ("awe": glassy bowed vibraphone, celesta overtones, airy choir pad, and deep sub-bass horizon drone) and clean, inquisitive orbital mechanics ("explain": soft felt-piano ostinato, delicate pizzicato strings, and warm analog marimba pulse). Subtle lift at the 2007 equinox storm awakening and a slow, floating resolution for the 10-minute low-gravity cliff drop on Miranda.
Pace: 66-76 BPM, calm measured pulse matched to British narration, lifting gently at chapter transitions without heavy percussion.
NOT: Do not sound like 021/022 solar brass drones, 023/024/025 shared ambient track, 026 Venus metallic industrial dread, 027 Mars dusty desert cello, 028 Titan sub-aquatic methane sonar, 029 Betelgeuse orchestral doom brass, 030 Moon clockwork lute, 031 Mercury/Sun searing high-tension distortion, or 032 Saturn cathedral organ and choral rings. No drums, no trailer booms, no synthwave beats, no vocals.
```

---

## 2. Chapter Mood & Crossfade Map (`2.5 s` Crossfades Across `0.70 s` Chapter Breaths)

| Chapter | Audio Span (s) | Mood | Tempo | Texture & Narrative Role |
|---|---|---|---:|---|
| **Ch 0 (`Open`)** | `0.00–57.36` | **`awe`** | `68 BPM` | Glassy bowed vibraphone, high celesta harmonics, and deep contrabass pad as the Sun sinks into a 21-year polar winter night (`97.77°` tilt, `−224.2 °C`). |
| **Ch 1 (*The Star That Moved*)** | `58.06–154.38` | **`explain`** | `72 BPM` | Crisp felt-piano and pizzicato cello pulse for Herschel's 13 March 1781 discovery, Bode's naming, `51,118 km` diameter (`4×` Earth), and `19 AU` (`2 h 40 min` sunlight, `84-year` orbit). |
| **Ch 2 (*The World Knocked Sideways*)** | `155.08–265.24` | **`awe`** | `68 BPM` | Shimmering string harmonics and bell tones as star `SAO 158687` blinks 13 vertical rings into view (`10 March 1977`), 28 literary moons, `17-hour` retrograde day, and the 21-year polar night. |
| **Ch 3 (*Six Hours at the Ice Giant*)** | `265.94–355.94` | **`explain`** | `74 BPM` | Warm analog marimba-synth arpeggio and muted horn pad for Voyager 2's 24 January 1986 six-hour flyby (`81,500 km`), `2.3%` methane blue-green reflection, and the `49 K` (`−224.2 °C`) cold paradox vs Neptune (`> 30 AU`). |
| **Ch 4 (*The Corkscrew Magnet*)** | `356.64–444.00` | **`awe`** | `76 BPM` | Dynamic lift at the `"Wrong."` midpoint twist (`356.76 s`): swirling polychordal synth pads and helical low strings for the December 2007 equinox storms (`900 km/h` / `560 mph`) and `58.6°` (`≈ 60°`) lopsided corkscrew magnetosphere. |
| **Ch 5 (*Why You Can't Land on Ice*)** | `444.70–513.90` | **`explain`** | `70 BPM` | Focused, tense low-register pulse descending into the `≥ 80%` hot dense fluid mantle (`H₂O · CH₄ · NH₃`) and `4,982 °C` (`9,000 °F`) core (`> 5,000 °C` hotter than the clouds). |
| **Ch 6 (*The Ten-Minute Cliff on Miranda*) + Hold** | `514.60–629.40` | **`awe`** | `66 BPM` | Weightless glass-harmonica and wide ambient string choir for Gerard Kuiper's 1948 discovery of Miranda (`≈ 500 km`, `1/7` Moon), canyons `12×` Grand Canyon, the `10-minute` cliff drop, 2022/2024 return plans, and the bridge to Pluto's nitrogen-ice heart (`611.40–629.40 s` hold + `3.0 s` fade). |
