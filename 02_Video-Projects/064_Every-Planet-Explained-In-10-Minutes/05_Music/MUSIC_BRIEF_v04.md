# Music Brief v04 — `OWB:064` Every Planet Explained in 10 Minutes (Mercury to Neptune)

- **Episode:** `064_Every-Planet-Explained-In-10-Minutes` (`OWB:064`)
- **Script Master:** `01_Script/every_planet_explained_script_master_v04.md` (SHA-256 `556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8`, `1,296` spoken words / `1,341` whitespace tokens / `8,471` spoken characters)
- **Target Music Runtime:** Full locked VO duration + `18.0 s` end-screen hold (`~606.28 s` estimated; final duration must follow measured locked VO), holding at full bed level `2.5 s` past the final spoken word and fading over the last `3.0 s`
- **Target Output Stem (in `J3022`/`J3023`):** `05_Music/every_planet_score_bed_v01.mp3` + `05_Music/every_planet_score_bed_v04_plan.json`
- **Gate:** `python3 scripts/music_gate.py 02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes --bed 05_Music/every_planet_score_bed_v01.mp3 --video <cut.mp4>`

---

## 1. Resolution of Concept-Sheet Music Conflict (`J3020` Requirement)

- **Conflict in `TOPIC_GO_NO_GO_SHEET.md` §5.1:** The concept sheet table mentioned *"shelf music bed"*, which would violate `studio/RULES.md` Lesson 7 (*"every film has its own score bed, at a pace that fits it ... it doesn't sound like another film's bed, even trimmed or re-encoded"*) and fail `scripts/music_gate.py`'s `reused` check (`similarity >= 0.80` against `02_Video-Projects/*/05_Music/*`).
- **Resolution (£0 cash, 0 Flow/Vertex credits):** `OWB:064` **never reuses** any shelf music bed from `020`–`034`. Instead, just like `032` (`_build_titan_score_bed_v01.py`), `033` (`_build_033_score_bed_v01.py`), and `034` (`_build_pluto_score_bed_v01.py`), `OWB:064` uses its own dedicated, film-specific chapter-shaped score bed (`05_Music/every_planet_score_bed_v01.mp3` + `every_planet_score_bed_v04_plan.json`) synthesised in Python/NumPy (`_build_064_score_bed_v01.py`) at **£0.00 spend** (or generated as a fresh single bed if Chief specifically authorises ElevenLabs music credit). It alternates `awe` and `explain` textures across the 8 planetary chapters with `2.5 s` crossfades at chapter cards, zero gaps `> 6.0 s`, `≥ 10 LU` below VO during speech (`sfx_kit.py level`), and verified `similarity < 0.50` against every other film's `05_Music` stem.

---

## 2. Exact Music Prompt (`Pace:` and `NOT:` Mandatory Lines)

```text
Grand outward solar-system voyage score for Every Planet Explained in 10 Minutes (Mercury to Neptune), alternating between sunlit inner-planet curiosity ("explain": warm felt-piano ostinato, crisp pizzicato strings, and gentle marimba-synth pulse for orbital resonances, core cutaways, and spacecraft probes) and deep outer-system wonder ("awe": wide harmonic string pads, glassy celesta overtones, resonant brass swells, and deep sub-bass planetary horizon drones). Smooth 2.5-second crossfades at each planet transition from 0.4 AU Mercury out to 30 AU Neptune, lifting at the Jupiter "no solid surface" midpoint twist and resolving into a weightless Kuiper-belt horizon hold.
Pace: 68-76 BPM, calm measured pulse matched to British narration, shifting cleanly between explain and awe chapters without heavy percussion.
NOT: Do not sound like 020/023/024/025 shared Jupiter ambient track, 021/022 solar brass drones, 026 Proxima Centauri deep-space pulse, 027 Earth spin clockwork strings, 028 Gliese 710 tension drone, 029 Betelgeuse orchestral doom brass, 031 Earth magnetic-flip sub-bass pulse, 032 Titan sub-aquatic methane sonar, 033 Uranus bowed vibraphone/glass harmonica solo bed, or 034 Pluto frozen-heart celesta bed. No vocals, no lyrics, no drums, no trap beats, no trailer booms, no comedy stings.
```

---

## 3. Eight-Planet Chapter Mood & Crossfade Map (`2.5 s` Crossfades at Chapter Cards)

| # | Planet / Section | Est. Window (s) | Mood | Target Tempo | Musical Texture & Narrative Role |
|---:|---|---|---|---:|---|
| 1 | **Mercury** (Cold Open) | `0–76.02 s` | **`awe` → `explain`** | `70 BPM` | Stark high-harmonic shimmer over warm contrabass pedal for 430 °C sunlight vs permanently shadowed polar craters and −180 °C night, settling into a clean 3:2 polyrhythmic felt-piano pulse for Colombo's resonance and the 85% iron core. |
| 2 | **Venus** (*The Backwards Furnace*) | `76.02–143.34 s` | **`awe`** | `68 BPM` | Dense, warm low-cello and amber analog pad swells under the 464 °C / 92-bar greenhouse, Pioneer Venus's 100× deuterium enrichment, and Venera 13's 127-minute survival. |
| 3 | **Earth** (*The Shielded Ocean World*) + Subscribe Beat | `143.34–216.47 s` | **`explain`** | `72 BPM` | Clear, forward-moving pizzicato strings and soft Rhodes harmonic pulse for Earth's 1,670 km/h equatorial surface speed, liquid-iron outer core beginning ~3,000 km down, 183 reversals, Gauss's 1830s measurements, and ESA's 2020 weakening report. |
| 4 | **Mars** (*The Frozen Robot Desert*) | `216.47–281.31 s` | **`awe`** | `69 BPM` | Sparse, wide acoustic-harmonic fifths and dusty low strings for Gale Crater, crustal magnetic traces, 6.36 mbar air, Olympus Mons (21.3 km above Martian datum), Opportunity's 90-Martian-day endurance, and Ingenuity's 72 flights. |
| 5 | **Jupiter** (*The Ocean of Metallic Hydrogen*) | `281.31–354.43 s` | **`explain` → `awe`** | `75 BPM` | Deep, majestic low-register pulse lifting at the midpoint twist (*"Case closed? Wrong — there is no solid surface"*) over a 58-minute Galileo data-return timeline; the far-deeper metallic hydrogen region is a separate explanation, never a probe destination. |
| 6 | **Saturn** (*Disappearing Rings and the Hexagon Storm*) | `354.43–437.90 s` | **`awe`** | `70 BPM` | Shimmering bell harmonics and wide choral-pad chords for the 282,000-km radial ring system (~10 m thick), 2017 Cassini dives, and the 30,000-km north-pole hexagon (2012–2016 colour change, possibly seasonal haze). |
| 7 | **Uranus** (*Knocked Sideways Into 21-Year Winters*) | `437.90–511.43 s` | **`explain`** | `71 BPM` | Cool, crystalline marimba-synth arpeggio and suspended sixths for Herschel's 1781 discovery, the 97.77° sideways tilt, 21-year winter, −224.2 °C atmospheric minimum (colder than Neptune in some places), and ≥80% hot dense fluid mass. |
| 8 | **Neptune** (*Supersonic Winds at the Edge*) + `18 s` End Hold | `511.43–606.28 s` | **`awe`** | `74 → 68 BPM` | Urgent, sweeping high-altitude wind-pad motion for Le Verrier & Galle's 1846 mathematical discovery and >2,000 km/h methane jets (roughly 5× Cyclone Olivia's gust), resolving into a calm, expansive Kuiper-belt horizon hold (`18 s` past the final word) for the `034` Pluto hand-off and end screen. |

This v04 brief supersedes v01 and v03 planning stamps only. v01 and v03 are preserved as history. No rendering or credits authorised by this correction job. Chapter timing source: `jobs/reviews/J3544/COUNTS_v04.json`.
