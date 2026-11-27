# J3021 — OWB 064 Every Planet Explained VO v01: Evidence & Verification Report

Recorded once from the locked `v04` script (`SHA-256 556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8`, locked by acting Chief `gemini` in `jobs/reviews/J3711/CHIEF_RULING.md`) via `04_Audio/tools/vo_take.py` under `desk-lock elevenlabs` using **Ben Orbit Narrator** (`kDch6ACCIpqgQ0NsU9kk`), `eleven_v3`, speed `1.04`, `0.7 s` inter-chapter gaps, plus `scribe_v2` word-level verification. Zero script changes, zero retakes, zero `atempo` distortion.

## Master Files, Hashes & Loudness

- **Master WAV (`studio-live`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/every_planet_explained_vo_v01.wav` (131,301,198 bytes)
  - SHA-256: `4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa`
- **Master MP3 (`studio-live`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/every_planet_explained_vo_v01.mp3` (10,942,892 bytes)
  - SHA-256: `cdf06f5a69a2d340e6ac2a46137119085a1cb19a99bbd06797257def828a3157`
- **Scribe raw timestamps (`stt_raw.json`) SHA-256:** `dca394c34569c8a63cc4085a148f4d5cb39747c9044a814d618f382135b7211f`
- **Captions (`words.srt`) SHA-256:** `dc33d4edd41d5b31ae0a8a2ef51768d143c92c38830d84dd12c7a773d5dff8d3`
- **Duration:** `683.86 s` (`11:23.86`, 1341 whitespace words / 8481 spoken chars, `117.66 wpm`)
- **Integrated loudness:** `-20.21 LUFS` (`vo_take` `-20.2 LUFS`, target `-19` to `-21 LUFS` — **PASS**)
- **True peak / max / mean / LRA:** `-3.64 dBTP` (limit `< -1 dBTP` — **PASS**), max `-3.6 dB`, mean `-23.4 dB`, LRA `4.20 LU`
- **Chapter loudness spread:** `-20.7` to `-19.6 LUFS` (**`1.1 LU` spread**)
- **Repetitions / stutters (1/2/3-gram):** `0` detected

## Opening & Key Beat Timings (Scribe Word Timestamps)

- **Sentence 1 end (`heat?`):** `6.52 s` (`< 8.0 s` — **PASS**)
- **Sentence 2 concrete answer end (`sunlight.`):** `10.98 s` (`< 20.0 s` — **PASS**)
- **Sentence 3 contrast end (`Celsius.`):** `25.04 s` (`< 30.0 s` — **PASS**)
- **Chapter 2 (`Venus`) start:** `82.06 s` (`> 45.0 s`, zero early chapter card — **PASS**)
- **Subscribe beat:** `245.18 s` – `251.2 s` (**`35.9%`** of VO runtime — **PASS**)

## ElevenLabs Credits & Budget Compliance

- **Live subscription before:** `109,171 / 121,114` (`11,943` remaining)
- **Immediate after (+4 s):** `112,902 / 121,114` (`8,212` remaining)
- **Settled live balance:** `113,111 / 121,114` (**`8,003` remaining**; **`3,940` net plan credits billed** across 8 chapters + Scribe; `5,003` above the `3,000` HOS fixes reserve)
- **Overage protection:** `can_extend_character_limit: false`, `allowed_to_extend_character_limit: false`, resets `2026-11-30T10:50:31Z`, cash spent `£0.00`.

## Per-Chapter Breakdown, Boundaries & Hashes

| # | Chapter | Window (s) | Dur (s) | LUFS | First 50 ms RMS | Last 50 ms RMS | First Word (offset) | Last Word (tail) | WAV SHA-256 (first 12) |
|---:|---|---:|---:|---:|---:|---:|---|---|---|
| 00 | open | 0.00–81.36 | 81.36 | -20.3 | -91.26 dB | -32.26 dB | `On` (+0.16s) | `hotter?` (+0.06s) | `9f7df8fc5dfd` |
| 01 | Venus — The Backwards Furnace | 82.06–157.90 | 75.84 | -20.4 | -41.69 dB | -54.98 dB | `At` (+0.14s) | `oceans?` (+0.14s) | `cd2a63e0cb15` |
| 02 | Earth — The Shielded Ocean World | 158.60–251.24 | 92.64 | -19.6 | -78.83 dB | -29.05 dB | `At` (+0.12s) | `you.` (+0.04s) | `153d8fcda809` |
| 03 | Mars — The Frozen Robot Desert | 251.94–324.34 | 72.40 | -20.4 | -65.31 dB | -58.7 dB | `At` (+0.1s) | `belt?` (+0.14s) | `55ad5911a285` |
| 04 | Jupiter — The Ocean of Metallic Hydrogen | 325.04–406.88 | 81.84 | -19.6 | -83.22 dB | -35.35 dB | `Beyond` (+0.08s) | `vanishing?` (+0.04s) | `11a145b80019` |
| 05 | Saturn — Disappearing Rings and the Hexagon Storm | 407.58–496.46 | 88.88 | -20.1 | -45.52 dB | -34.05 dB | `At` (+0.12s) | `sideways?` (+0.04s) | `bb05866f894b` |
| 06 | Uranus — Knocked Sideways Into 21-Year Winters | 497.16–584.44 | 87.28 | -20.7 | -64.04 dB | -28.67 dB | `At` (+0.12s) | `faster?` (+0.04s) | `3cd28aa5a8b3` |
| 07 | Neptune — Supersonic Winds at the Edge | 585.14–683.86 | 98.72 | -20.5 | -34.03 dB | -54.15 dB | `Now,` (+0.08s) | `craters.` (+0.78s) | `85e72ad11a2c` |

## Scribe `scribe_v2` Full Mismatch Audit (All 63 Runs)

- **Raw `vo_take.py` match:** `89.45%` (`REVIEW`, `63` mismatch runs across `1374` script tokens vs `1337` Scribe tokens).
- **True spoken match:** **`100.0%` (`0` wording discrepancies)** — every mismatch is US/UK spelling or possessive (`20`), natural British ordinal date reading (`9`), or spelled-out numbers transcribed as digits (`34`).

| # | Locked script tokens | Scribe tokens | Classification |
|---:|---|---|---|
| 1 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 2 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 3 | `per cent` | `percent` | `uk_us_spelling_or_possessive` |
| 4 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 5 | `per cent` | `percent` | `uk_us_spelling_or_possessive` |
| 6 | `metres` | `meters` | `uk_us_spelling_or_possessive` |
| 7 | `1` | `the 1st of` | `british_ordinal_date_reading` |
| 8 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 9 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 10 | `kilometre` | `kilometer` | `uk_us_spelling_or_possessive` |
| 11 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 12 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 13 | `per cent` | `percent` | `uk_us_spelling_or_possessive` |
| 14 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 15 | `per cent` | `percent` | `uk_us_spelling_or_possessive` |
| 16 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 17 | `mars's` | `mars'` | `uk_us_spelling_or_possessive` |
| 18 | `10` | `the 10th of` | `british_ordinal_date_reading` |
| 19 | `18` | `the 18th of` | `british_ordinal_date_reading` |
| 20 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 21 | `forty one thousand kilometres` | `41 000 kilometers` | `spelled_number_to_digits_or_spelling` |
| 22 | `sixteen thousand five hundred` | `16 500` | `spelled_number_to_digits_or_spelling` |
| 23 | `7` | `the 7th of` | `british_ordinal_date_reading` |
| 24 | `fifty eight` | `58` | `spelled_number_to_digits_or_spelling` |
| 25 | `one point four` | `1 4` | `spelled_number_to_digits_or_spelling` |
| 26 | `kilometres nine point five` | `kilometers 9 5` | `spelled_number_to_digits_or_spelling` |
| 27 | `ten point seven` | `10 7` | `spelled_number_to_digits_or_spelling` |
| 28 | `six hundred and eighty seven` | `687` | `spelled_number_to_digits_or_spelling` |
| 29 | `metre` | `meter` | `uk_us_spelling_or_possessive` |
| 30 | `two hundred and eighty two thousand kilometres` | `282 000 kilometers` | `spelled_number_to_digits_or_spelling` |
| 31 | `ten metres` | `10 meters` | `spelled_number_to_digits_or_spelling` |
| 32 | `four thousand eight hundred` | `4 800` | `spelled_number_to_digits_or_spelling` |
| 33 | `forty five thousand` | `45 000` | `spelled_number_to_digits_or_spelling` |
| 34 | `zero point four one` | `0 41` | `spelled_number_to_digits_or_spelling` |
| 35 | `ten` | `10` | `spelled_number_to_digits_or_spelling` |
| 36 | `one hundred` | `100` | `spelled_number_to_digits_or_spelling` |
| 37 | `thirty thousand kilometres` | `30 000 kilometers` | `spelled_number_to_digits_or_spelling` |
| 38 | `three hundred and twenty two kilometre` | `322 kilometer` | `spelled_number_to_digits_or_spelling` |
| 39 | `two point nine` | `2 9` | `spelled_number_to_digits_or_spelling` |
| 40 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 41 | `nineteen` | `19` | `spelled_number_to_digits_or_spelling` |
| 42 | `13` | `the 13th of` | `british_ordinal_date_reading` |
| 43 | `eighty four` | `84` | `spelled_number_to_digits_or_spelling` |
| 44 | `twenty three point four` | `23 4` | `spelled_number_to_digits_or_spelling` |
| 45 | `ninety seven point seven seven` | `97 77` | `spelled_number_to_digits_or_spelling` |
| 46 | `seventeen` | `17` | `spelled_number_to_digits_or_spelling` |
| 47 | `twenty one` | `21` | `spelled_number_to_digits_or_spelling` |
| 48 | `24` | `the 24th of` | `british_ordinal_date_reading` |
| 49 | `minus two hundred and twenty four point two` | `224 2` | `spelled_number_to_digits_or_spelling` |
| 50 | `sixty` | `60` | `spelled_number_to_digits_or_spelling` |
| 51 | `eighty per cent` | `80` | `spelled_number_to_digits_or_spelling` |
| 52 | `four thousand nine hundred and eighty two` | `4 982` | `spelled_number_to_digits_or_spelling` |
| 53 | `four point five` | `4 5` | `spelled_number_to_digits_or_spelling` |
| 54 | `kilometres thirty` | `kilometers 30` | `spelled_number_to_digits_or_spelling` |
| 55 | `nine hundred` | `900` | `spelled_number_to_digits_or_spelling` |
| 56 | `sixteen` | `16` | `spelled_number_to_digits_or_spelling` |
| 57 | `one hundred and sixty five` | `165` | `spelled_number_to_digits_or_spelling` |
| 58 | `23` | `the 23rd of` | `british_ordinal_date_reading` |
| 59 | `10` | `the 10th of` | `british_ordinal_date_reading` |
| 60 | `25` | `the 25th of` | `british_ordinal_date_reading` |
| 61 | `two thousand kilometres` | `2 000 kilometers` | `spelled_number_to_digits_or_spelling` |
| 62 | `kilometres` | `kilometers` | `uk_us_spelling_or_possessive` |
| 63 | `thousand kilometre` | `1 000 kilometer` | `spelled_number_to_digits_or_spelling` |

## Perception Boundary

All verdicts above rest strictly on machine audio measurements and `scribe_v2` ASR evidence. No direct human or agent audio hearing is claimed. Under Ben's 4 November 2026 standing rule (`AGENTS.md`), Ben's final finished-cut UAT watch is the watch-and-listen check.
