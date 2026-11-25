# Music Brief v05 — `OWB:064` Every Planet Explained in 10 Minutes (Mercury to Neptune)

- **Episode:** `064_Every-Planet-Explained-In-10-Minutes` (`OWB:064`)
- **Script Master (locked):** `01_Script/every_planet_explained_script_master_v04.md` (SHA-256 `556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8`)
- **Locked VO (`J3021` PASS):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/every_planet_explained_vo_v01.wav` (`683.86 s`, SHA-256 `4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa`)
- **Measured Music Runtime:** **`701.86 s`** (`683.86 s` locked VO + `18.00 s` end-screen hold), holding full bed past the final spoken word (`683.08 s`) and fading cleanly over the last `3.0 s` (`698.86–701.86 s`).
- **Delivered £0 Score Stem (`studio-live`):** `05_Music/every_planet_score_bed_v01.mp3` (+ `.wav`), plan `05_Music/every_planet_score_bed_v05_plan.json` (and `every_planet_score_bed_v01_plan.json` beside the bed on `studio-live`), builder `05_Music/_build_064_score_bed_v01.py`.
- **Gate:** `python3 scripts/music_gate.py <film-dir> --bed <bed.mp3>` (verified PASS in `05_Music/music_gate_v01.json`, £0.00 spend, 0 credits).

---

## 1. Resolution of Concept-Sheet Shelf-Music Conflict

- `TOPIC_GO_NO_GO_SHEET.md` §5.1 informally mentioned a *"shelf music bed"*, which violates `studio/RULES.md` Lesson 7 and fails `music_gate.py`'s `reused` check (`similarity >= 0.80`).
- `OWB:064` **reuses zero shelf music**. It uses its own newly synthesised, chapter-shaped `701.86 s` score bed (`every_planet_score_bed_v01.mp3`, `£0.00` spend, `0` credits) with `2.5 s` crossfades aligned to the exact locked VO chapter boundaries (`J3021`), alternating `explain` and `awe` textures, zero gaps `> 6 s`, and verified `music_gate.py` PASS (`similarity < 0.80` against all other OWB beds).

---

## 2. Exact Music Prompt (`Pace:` and `NOT:` Mandatory Lines)

```text
Grand outward solar-system voyage score for Every Planet Explained in 10 Minutes (Mercury to Neptune), alternating between sunlit inner-planet curiosity ("explain": warm felt-piano ostinato, crisp pizzicato strings, and gentle marimba-synth pulse for orbital resonances, core cutaways, and spacecraft probes) and deep outer-system wonder ("awe": wide harmonic string pads, glassy celesta overtones, resonant brass swells, and deep sub-bass planetary horizon drones). Smooth 2.5-second crossfades at each planet transition from 0.4 AU Mercury out to 30 AU Neptune, lifting at the Jupiter "no solid surface" midpoint twist and resolving into a weightless Kuiper-belt horizon hold.
Pace: 68-76 BPM, calm measured pulse matched to British narration, shifting cleanly between explain and awe chapters without heavy percussion.
NOT: Do not sound like 020/023/024/025 shared Jupiter ambient track, 021/022 solar brass drones, 026 Proxima Centauri deep-space pulse, 027 Earth spin clockwork strings, 028 Gliese 710 tension drone, 029 Betelgeuse orchestral doom brass, 031 Earth magnetic-flip sub-bass pulse, 032 Titan sub-aquatic methane sonar, 033 Uranus bowed vibraphone/glass harmonica solo bed, or 034 Pluto frozen-heart celesta bed. No vocals, no lyrics, no drums, no trap beats, no trailer booms, no comedy stings.
```

---

## 3. Exact Locked-VO Chapter Mood & Crossfade Map (`2.5 s` Crossfades)

| # | Planet / Section | Exact Window (s) | Mood | Key Palette | Narrative Role |
|---:|---|---|---|----|---|
| 1 | **Mercury** (Cold Open) | `0.00–81.71` | **`explain`** | D Dorian | Sunlit inner-planet pulse (`72.3 BPM`) under 430 °C / −180 °C contrast, Colombo 3:2 resonance, 85% metallic core, and Prokofiev crater ice. |
| 2 | **Venus** (*The Backwards Furnace*) | `81.71–158.25` | **`awe`** | A Mixolydian | Dense warm amber swells for 464 °C / 92-bar greenhouse, retrograde spin, Pioneer Venus 100× deuterium, and Venera 13's 127-minute survival. |
| 3 | **Earth** (*The Shielded Ocean World*) + Subscribe | `158.25–251.59` | **`explain`** | F# Phrygian-Maj | Forward rhythmic pulse for 1,670 km/h spin, 43 km bulge, 3,000 km outer core, 183 reversals, Gauss (1830s), ESA (2020), and subscribe beat. |
| 4 | **Mars** (*The Frozen Robot Desert*) | `251.59–324.69` | **`awe`** | C Lydian | Sparse dusty acoustic fifths for crustal magnetism, 6.36 mbar atmosphere, Olympus Mons (21.3 km above datum), Opportunity, and Ingenuity. |
| 5 | **Jupiter** (*The Ocean of Metallic Hydrogen*) | `324.69–407.23` | **`explain`** | G Min9 | Deep majestic pulse lifting at the midpoint twist (*"Case closed? Wrong — there is no solid surface"*) and Galileo's 58-minute data return. |
| 6 | **Saturn** (*Disappearing Rings and the Hexagon Storm*) | `407.23–496.81` | **`awe`** | E Maj7#11 | Shimmering bell harmonics for 687 kg/m³ density, 282,000 km radial rings, 2017 Cassini dives, and 30,000 km north-pole hexagon. |
| 7 | **Uranus** (*Knocked Sideways Into 21-Year Winters*) | `496.81–584.79` | **`explain`** | B Min11 | Crystalline arpeggio for Herschel (1781), 97.77° sideways tilt, 21-year winter, −224.2 °C minimum, and ≥80% hot dense fluid interior. |
| 8 | **Neptune** (*Supersonic Winds at the Edge*) + `18 s` Hold | `584.79–701.86` | **`awe`** | D Add9 | Sweeping wind-pad motion for Le Verrier/Galle (1846), >2,000 km/h methane winds, Triton >8 km geysers, and New Horizons Pluto end-screen hold. |

Preserves `MUSIC_BRIEF_v01.md`, `v03.md`, `v04.md` untouched as history. No hearing claimed; fit is judged by Ben's final UAT watch.
