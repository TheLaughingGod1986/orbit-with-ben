# Music Brief v01 — 032 What Would Happen If You Landed on Titan?

- **Episode:** `032_What-Would-Happen-If-You-Landed-On-Titan` (`Real Worlds` series: Saturn's Moon Titan)
- **VO Master:** `02_Voiceover/titan_landing_vo_v02b.wav` (`582.440 s`, `-20.0 LUFS` integrated, `4.8 LU` LRA, `-3.4 dBFS` true peak; SHA-256 `55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5`, locked under Chief h31 / J1294)
- **Word Timings:** `02_Voiceover/stt/titan_landing_vo_v02b/stt_raw.json` (last spoken word ends at `582.380 s`)
- **Target Score Runtime:** `585.44 s` (`582.44 s` VO master + `3.00 s` post-word hold, with `2.50 s` full-level hold `582.38–584.88 s` and `10.00 s` smooth tail fade over `575.44–585.44 s`; `_build_titan_score_bed_v01.py` also accepts `--duration` if chapter-card holds extend the timeline)
- **Target Output Stem:** `05_Music/titan_score_bed_v01.mp3` + `05_Music/titan_score_bed_v01_plan.json`
- **Spend:** £0.00 (chapter-shaped stereo synthesis)
- **Gate:** `python3 scripts/music_gate.py 02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan --bed /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/05_Music/titan_score_bed_v01.mp3`

---

## 1. Prompt (`Pace:` and `NOT:` Mandatory Lines)

```text
Golden-haze hydrocarbon world documentary score for Saturn's moon Titan, Huygens, Kraken Mare, and Dragonfly, alternating between dense amber atmospheric wonder ("awe": warm C-minor / E-flat Lydian brass-pad swells, resonant low cello pedal, and shimmering high bell-flute harmonics) and crisp planetary-physics discovery ("explain": F-Dorian muted mallet arpeggios, warm upright piano intervals, and gentle sub-bass pulse). Subtle harmonic lift at Chapter 5 ("Would It Explode?" at 389.76 s) and Chapter 6 ("Wings for Titan" at 474.94 s), holding full after the final word at 582.38 s before a smooth fade.
Pace: 68-78 BPM, calm measured pulse matched to British narration, changing texture across chapter cards without heavy percussion.
NOT: Do not sound like 013 Moon Leaving quiet lunar pads, 020 Jupiter gas-giant swell, 021 Saturn Rings golden ring-plane pads, 022 Sun Brighter warm solar drone, 023/024/025 shared ambient track (023 Venus lost-twin underscore, 024 Light Speed forward relativistic pulse, 025 Mars Robot cold dusty red plains), 026 Nearest Star deep-space night-sky pad, 027 Earth Stopped Spinning rotational pulse, 028 Star Coming Toward Us (Gliese 710) interstellar ambient, 029 Betelgeuse D-minor supergiant ambient, 030 Apophis asteroid flyby tension, 031 Earth Magnetic Field core dynamo pulse, 033 21-Year Winters (Uranus) bowed vibraphone and glass harmonica, or 034 Pluto Frozen Heart F#-minor bowed glass marimba and concert harp. No drums, no trailer booms, no synthwave beats, no vocals.
```

---

## 2. Chapter Mood & Crossfade Map (`2.5 s` Crossfades Across Chapter Boundaries)

| Chapter | Rows | VO Span (s) | Mood | Tempo | Musical Texture & Narrative Arc |
|---|---|---:|---|---:|---|
| **Ch 0 (`Open`)** | `R01–R06` | `0.16–50.44` | **`awe`** | `70.6 BPM` | Deep C-minor / E-flat Lydian amber haze drone and bell-flute overtones as Cassini peers through Titan's golden nitrogen-methane sky (`1.47 bar`, `−179 °C`). |
| **Ch 1 (*A Moon With a Sky*)** | `R07–R14` | `51.26–136.68` | **`explain`** | `70.6 BPM` | `2.5 s` crossfade at `50.85 s`: warm F-Dorian mallet arpeggios and upright piano intervals for Huygens (1655), Kuiper's 1944 methane spectrum, and Voyager 1's 1980 orange haze flyby. |
| **Ch 2 (*The Huygens Landing*)** | `R15–R24` | `137.56–245.10` | **`awe`** | `70.6 BPM` | `2.5 s` crossfade at `137.12 s`: suspended low cello pedal and crystalline harmonic swells for the 14 January 2005 Huygens descent (`147 min`), branching river channels, and rounded water-ice pebbles at `−179 °C`. |
| **Ch 3 (*Standing on Titan*)** | `R25–R30` | `246.00–324.44` | **`explain`** | `70.6 BPM` | `2.5 s` crossfade at `245.55 s`: measured rhythmic mallet figures for `95% N₂ / 5% CH₄`, `4×` air density, `1/7` gravity, and slow-motion `9.5 mm` methane raindrops falling at `1.6 m/s`. |
| **Ch 4 (*Seas of Natural Gas*)** | `R31–R36` | `325.32–388.92` | **`awe`** | `70.6 BPM` | `2.5 s` crossfade at `324.88 s`: deep sub-bass hydrocarbon sea swell and wide stereo strings for Kraken Mare (`400,000 km²`), Ligeia Mare (`160 m` deep), and the subsurface water-ammonia ocean (`55–80 km` crust). |
| **Ch 5 (*Would It Explode?*)** | `R37–R44` | `389.76–474.10` | **`explain`** | `70.6 BPM` | `2.5 s` crossfade at `389.34 s`: focused harmonic curiosity under the combustion twist (`21% O₂` on Earth vs `0% O₂` on Titan — why a match or rocket engine cannot ignite Titan's sky). |
| **Ch 6 (*Wings for Titan*) + Hold** | `R45–R52` | `474.94–582.38` | **`awe`** | `70.6 BPM` | `2.5 s` crossfade at `474.52 s`: buoyant E-flat Lydian lift for Dragonfly (`28×` easier flight, `8 rotors`, `July 2028` launch, `Late 2034` Selk Crater arrival) and the Uranus `21-year winter` hand-off (`567.66–585.44 s`). |
