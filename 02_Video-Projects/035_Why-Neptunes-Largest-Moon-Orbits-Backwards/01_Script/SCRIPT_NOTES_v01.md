# 035 Why Neptune's Largest Moon Orbits Backwards — script v01 notes (J0395)

Drafted by Gemini (`gemini-argon`, stand-in worker) for J0395, 16 Oct 2026. **Draft only.** Revised from `triton_backwards_moon_script_master_v00.md` (scaffolded in J0387 as #1 in `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-16_J0387.md`, 25/30, directly answering the closing hand-off at line 110 of `034` `pluto_frozen_heart_script_master_v01.md`), because `030`, `031` and `032` have locked scripts (`030` v02 locked in J0227/J0222; `031` v03 locked in J0340; `032` v01 locked in J0301), `033` Uranus `v01` is already drafted and parked for Chief's script review in J0363 (`56e8c332`), `034` Pluto `v01` is already drafted and parked for Chief's script review in J0378 (`aae28e71`), and `035` only had a `v00` draft from the ideas pass (`J0387`). The topic isn't locked (Chief locks it after the neighbour pass), and the script isn't locked (Chief's script review, then the Gemini `facts` pass and `CLAUDE_QUOTE_CHECK_v01.md` before any VO). No spend.

## Result

- `npm run review:script`: **PASS 95.8 / 100** (10/10 hook, 9.5/10 curiosity, 9.5/10 storytelling, 10/10 scientificAccuracy, 9.6/10 emotion, 10/10 escalation, 9.0/10 retentionPotential, 9.1/10 searchPotential, 9.5/10 visualOpportunities, 9.6/10 narrationFlow; 8/8 structure gates).
- Spoken words: **1,218 words** (1,271 reviewer words, ~8.5 min), 6 chapters — inside the 1,200–1,300 spoken-word / 7–9 min lock.
- Subscribe beat at 47% of spoken words (11 words: *"New space mysteries every Sunday. Subscribe and they'll come to you."*).
- Markers: **DATA 7 · SCALE 7 (SCALE count ≥ DATA count) · WHO 4 · WHEN 6 · FACT 4 · NUMBER OBJECT 7**.
- First concrete answer (*"Triton circles Neptune backwards in a retrograde orbit — and at minus two hundred and thirty-five degrees Celsius, Voyager 2 discovered active geysers spewing icy material more than eight kilometres high"*) lands in the opening seconds; stakes and main question before 0:45; first chapter card (`[CHAPTER CARD: The Brewer Who Found a World]`) held until after 0:30 (`OWB_2026-10-16.md` item 2); no agenda line (Lesson 7).

## Number object per chapter (per-chapter teaching gate)

| Chapter | Number object | People and dates |
|---|---|---|
| Hook | Retrograde orbit and geyser height bar showing Triton (2,700 km diameter, 22% smaller than Earth's Moon, circling opposite to Neptune's 16-hour spin at 30 AU) erupting geysers >8 km (5 miles) high at −235 °C (−391 °F) | WHEN 25 August 1989 (timeline starts) |
| 1 The Brewer Who Found a World | Diameter scale comparing Neptune (49,528 km, 4× wider than Earth — baseball vs nickel) with Earth + 4.5-billion-km (30 AU, 4-hour light-travel, 1/900 sunlight) distance bar and 165-year orbital calendar (1846–2011, seasons >40 years) | WHO Urbain Le Verrier (1811–1877), Johann Gottfried Galle (1812–1910), William Lassell (1799–1880); WHEN 23 September 1846, 10 October 1846, 2011 added to timeline; FACT Financed by a brewery |
| 2 The Moon Going the Wrong Way | Orbital comparison contrasting Triton's retrograde 5.88-day synchronous orbit at 354,760 km (157° inclination, opposite to Neptune's 16-hour spin) with Nereid's 360-Earth-day eccentric orbit at 5.51 million km + Triton's 2,050 kg/m³ (2× water) density bar | WHO Gerard Kuiper (1905–1973); WHEN 1949, millions of years ago added to timeline; FACT Captured from Kuiper Belt |
| 3 Twelve Years to the Blue Giant | Voyager 2 Grand Tour trajectory bar (722 kg, 12 years, 7 billion km, 4,800 km Neptune cloud-top flyby) + wind-speed gauge comparing Neptune (>2,000 km/h / 1,200 mph) with Jupiter (3× slower) and Earth's 400 km/h (250 mph) top winds (9× slower) | WHEN 20 August 1977, 1979, 1981, 24 January 1986, 14 February 1986, 25 August 1989 added to timeline; FACT Winds 9× stronger than Earth's |
| 4 The Coldest Geysers in the Solar System | Surface temperature and reflectivity bar (38 K / −235 °C / −391 °F, 70% sunlight reflected) + geyser plume scale (>8 km / 5 miles high, >160 km / 100 miles long across ~50 south polar plumes at 900 m/pixel resolution) | — (midpoint twist *"Wrong."* opens chapter at ~60% runtime) |
| 5 Ice Lava and the Cantaloupe World | Cryovolcanic basin and interior cutaway gauge spanning 500 km (300 miles) across (nitrogen-ice crust, water-ice mantle, rock-and-metal core) comparing Triton's nitrogen-dominated atmosphere with Earth and Titan | WHEN since 1989 added to timeline; FACT Only 4 active volcanic worlds |
| 6 Farewell to the Ice Giants | Voyager 2 outbound interstellar bar from the 4.86-million-km (3-million-mile) crescent farewell shot (48° below ecliptic) into interstellar space at 15.4 km/s (9.6 miles/s, 19,390 years per light-year) | WHEN 28 August 1989, November 1998, 10 December 2018 completing timeline |

The timeline builds across the film, so it counts as one DATA moment. No two code graphics run back to back; real moving imagery sits between them in every chapter.

## What changed from v00

- Cold open hook tightened to keep the opening question inside the 180-character hook window while naming Triton's backwards orbit in the first line, lifting `review:script` from **95.3 / 100** (`hook` 9.5/10) in `v00` to **95.8 / 100** (`hook` 10/10, `scientificAccuracy` 10/10, `escalation` 10/10, 8/8 structure gates).
- Audited every spoken date and era across all 6 chapters for the *Teach on screen* `WHEN:` gate: added `millions of years ago` to Chapter 2's `WHEN:`, added `1979, 1981` (Jupiter and Saturn Grand Tour flybys) to Chapter 3's `WHEN:`, added `· WHEN: since 1989, added to the timeline` to Chapter 5 (`WHEN:` count 5 → 6), and removed the unspoken `(30 August 2007)` reference from Chapter 6's `[VISUAL MUST]` so every on-screen date matches spoken narration word for word.
- Added the full chapter-by-chapter `Number object per chapter (per-chapter teaching gate)` table above.

## Open items

1. **Chief:** topic lock (`J0387`: lock `035` *Why Neptune's Largest Moon Orbits Backwards* or pick another candidate from `IDEAS_2026-10-16_J0387.md`; decide Short-first waiver vs standalone Short `oyRcrFTYyDY`, airing 27 Oct 2026; neighbour pass ≥3 education/space videos at ≈1M+ views on Neptune / Triton) and script review of `triton_backwards_moon_script_master_v01.md`.
2. **Gemini `facts` pass + `CLAUDE_QUOTE_CHECK_v01.md`:** all 12 rows in `01_Script/SOURCES.md` were pre-checked against live NASA (`science.nasa.gov/neptune/moons/triton/`, `science.nasa.gov/neptune/neptune-facts/`, `science.nasa.gov/neptune/moons/`, `science.nasa.gov/neptune/moons/nereid/`, `science.nasa.gov/mission/voyager/voyager-2/`, `science.nasa.gov/mercury/facts/`), NSSDCA (`neptunefact.html`, `neptuniansatfact.html`), JPL Photojournal (`PIA00317`, `PIA00059`, `PIA01538`, `PIA02215`) and LOC Authority pages on 16 Oct 2026 with verbatim quotes; formal `facts` pass and Claude quote check still run before VO lock.
3. **Archive portraits:** confirm public-domain/CC-licensed portrait files for Urbain Le Verrier (1811–1877), Johann Gottfried Galle (1812–1910), William Lassell (1799–1880) and Gerard Kuiper (1905–1973) before the shot list.
4. **Hand-off line:** Chapter 6 hands off to Mercury's polar ice (*"Why Is There Ice on the Planet Closest to the Sun?"*, #2 in `IDEAS_2026-10-16_J0387.md`, 24/30); adjust if Chief picks a different `036` topic.
