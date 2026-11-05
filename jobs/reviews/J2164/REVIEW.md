# J2164 — Rule H Review: OWB 033 Uranus VO (`J2155` / PR #502 `76284eba93`)

- **Date:** 5 November 2026
- **Reviewer:** `gemini` (`gemini-argon`, Rule H review lane)
- **Film / Stage:** `OWB:033` (`02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters`) · `vo`
- **Reviewed Job / Evidence:** `J2155` (*033 Uranus: VO from locked script v02 (J2148 GO)*), commit `76284eba93572df6f4f75cd6c61855e795e6a6b5` (`codex/J2155-uranus-vo`, PR #502, Studio core check `SUCCESS`)
- **Demonstrated Input Capability:** `audio_input` verified via native `audio/mpeg` multimodal reads (`read_file`) on 10 audio slices extracted from `uranus_vo_v01.mp3` and `parts/uranus_vo_v01/ch00..ch06.wav` (`clip_418_offset.mp3`, `clip_571_april.mp3`, `clip_601_worlds.mp3`, `tail_ch00..ch06.mp3`), alongside full Scribe word timestamps and signal measurements. (Ben's final finished-film watch/listen UAT remains the final human sign-off.)
- **Verdict:** **KEEP** — accept `uranus_vo_v01.wav` (`3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460`) / `uranus_vo_v01.mp3` (`f6e35088c5a71876ff1022a97d81e91dced6bf3f967b9eb7acb156bd7e543868`) with zero retakes and zero additional ElevenLabs spend; close `J2155` (`033 vo` -> `done`), land the `J2155` evidence and ledger records on `main`, and explicitly clear `J2165` (*033 Uranus: shot list after explicit VO acceptance*) to start immediately.

---

## 1. Master Audio & Technical Verification (`PASS`)

| Check | Measured Value | Target / Rule | Status |
|---|---|---|---|
| Locked script source | `01_Script/uranus_21_year_winter_script_master_v02.md` (`c01c9f9e78`) | `review:script` `95.2/100`, `gate:episode` `PASS`, `1,290` spoken words | `PASS` |
| Master WAV SHA-256 | `3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460` | Present on disk (`117,388,878` bytes, `48 kHz` stereo PCM) | `PASS` |
| Master MP3 SHA-256 | `f6e35088c5a71876ff1022a97d81e91dced6bf3f967b9eb7acb156bd7e543868` | Present on disk (`9,783,212` bytes, `48 kHz` stereo MP3) | `PASS` |
| Integrated loudness | `-20.22 LUFS` | `~-20 LUFS` pre-mix VO stem target | `PASS` |
| Mean volume | `-23.3 dB` | `-19` to `-28 dB` mean (`STUDIO_PLAYBOOK.md`) | `PASS` |
| True peak | `-3.77 dBTP` | `<= -1.0 dBTP` ceiling | `PASS` |
| Duration & pace | `611.40 s` (`10:11.4`, incl. six `0.70 s` inter-chapter gaps = `4.20 s`) | `1,290` spoken words (`1,308` whitespace tokens) at `1.04x` = `~128.4 wpm` | `PASS` |
| Spend ledger | `7,858` chars logged in `04_Audio/elevenlabs_ledger.jsonl` & `05_Analytics/ai_spend/ledger.jsonl` | Live counter `101,014 -> 97,557`; full `7,858` chars conservatively reserved | `PASS` |

### Runtime Ruling (`611.40 s` / `10:11.4`)
- The locked script (`uranus_21_year_winter_script_master_v02.md`) is strictly inside the `1,200–1,300` spoken-word lock (`1,290` spoken words across open + 6 chapters).
- Per `AGENTS.md` (*"Length comes from the script, not from holding shots"*), the `~9.0 min` figure in the brief is a nominal `~143 wpm` estimate; Ben's natural calm British narration cadence (`eleven_v3`, speed `1.04`) delivers `1,290` words in `607.2 s` of speech + `4.2 s` of chapter pauses (`611.40 s` total). No speed-up, trim, or script cut is warranted.

---

## 2. Scribe Transcript Ruling (`93.39%`, 54 Mismatch Groups -> `PASS`)

### A. 51 of 54 Groups — Pure Orthographic, UK/US Spelling, or Numeral Representation
Every one of these 51 groups is an ASR formatting difference between the UK-spelled, word-expanded script and ElevenLabs Scribe's US-spelled, digit-normalized output:
1. **UK vs US spelling & possessive punctuation (18 groups):** `kilometres`/`kilometers` (#1, #2, #21, #22, #33, #35, #48), `aeroplane`/`airplane` (#7), `grey`/`gray` (#11), `colour`/`color` (#13, #24), `travelling`/`traveling` (#20), `per cent`/`percent` (#25, #26, #27), `centre`/`center` (#39), and `uranus's`/`uranus'` (#28, #36, #41).
2. **Spoken number words vs Scribe digits & ordinals (33 groups):** `nineteen`/`19` (#3, #4, #31), `forty`/`40` (#5), `eighty four`/`84` (#6, #17), `10`/`10th` (#8, `10 March 1977`), `158687`/`one five eight six eight seven` (#9, star catalog designation `SAO 158687` properly read digit-by-digit), `thirteen`/`13` (#10), `22`/`22nd` (#12, `22 March`), `twenty eight`/`28` (#14), `seventeen`/`17` (#15, #40), `twenty four`/`24` (#16), `twenty one`/`21` (#18, #32, #52), `24`/`24th` (#19, `24 January 1986`), `ten`/`10` (#23, #50, #53), `forty nine`/`49` (#29), `thirty`/`30` (#30), `five hundred and sixty`/`560` (#34), `sixty`/`60` (#37), `two hundred and twenty four`/`224` (#42), `eighty per cent`/`80` (#43 — raw Scribe token at `466.504–467.104 s` is `"80%"`, and `vo_take.py` punctuation stripping normalizes `"80%"` to `"80"`), `nine thousand`/`9 000` (#44), `four thousand nine hundred and eighty two`/`4 982` (#45), `five thousand`/`5 000` (#46), `16`/`16th` (#47, `16 February 1948`), and `twelve`/`12` (#49).
3. **All 15 `SOURCES.md` MUST QUOTE numbers verified in the take:** Every sourced value (`21` Earth years, `84` Earth years, `97.77°` vs `23.44°`, `-224.2 °C`, `13 March 1781`, `10 March 1977` / `SAO 158687` / `9` -> `13` rings, `28` moons, `17h 14m` vs `24` hr, `24 Jan 1986` / `81,500 km` / `~6 hr`, `82.5%` H₂ / `15.2%` He / `2.3%` CH₄, `900 km/h` / `560 mph` vs `400 km/h`, `58.6°` tilt / `1/3` radius offset, `80%` mass / `4,982 K` / `9,000 °F`, `20 km` / `12 mi` Verona Rupes / `~10 min`, `19 April 2022` Decadal Survey / `2049` equinox) is spoken accurately with zero stumbles or repetitions.

### B. 3 Unresolved Wording / Date Items — Direct Audio & Phonetic Ruling (`KEEP`, No Pickups Required)

1. **Mismatch #38 (`~418.204 s`): Script `"and offset"` vs Scribe `"an offset"` — `KEEP`**
   - **Line:** *"Voyager Two discovered that Uranus's magnetic field is tilted by fifty-eight point six degrees from its spin axis, and offset from the planet's centre by one third of Uranus's radius."*
   - **Direct audio verification (`416.0–421.0 s`, `clip_418_offset.mp3`):** The narrator speaks weak-form British RP `"and"` (`/ən/`) before the vowel-initial word `"offset"`. In connected British speech, the final alveolar `/d/` of unstressed `"and"` naturally elides before `/ɒ/` (`[ən ˈɒfsɛt]`), which Scribe ASR transcribes as `"an"`. Both forms are grammatically and scientifically identical in context (`"tilted by 58.6° from its spin axis, and/an offset from the planet's centre..."`), and the delivery is completely smooth.

2. **Mismatch #51 (`~570.744 s`): Script `"On 19 April 2022"` vs Scribe `"On 19th of April 2022"` — `KEEP`**
   - **Line:** *"On 19 April 2022, the Planetary Science Decadal Survey named the Uranus Orbiter and Probe the highest-priority flagship mission for the next decade."*
   - **Direct audio verification (`569.0–574.0 s`, `clip_571_april.mp3`):** In standard British English narration, UK written date format `"19 April 2022"` is spoken aloud as `"nineteenth of April twenty twenty-two"` (consistent with #8 `"10 March"` -> `"10th"`, #12 `"22 March"` -> `"22nd"`, #19 `"24 January"` -> `"24th"`, and #47 `"16 February"` -> `"16th"`). This is natural British spoken expansion of a written date, not a text error.

3. **Mismatch #54 (`~601.524 s`): Script `"Real Worlds series"` vs Scribe `"Real World series"` — `KEEP`**
   - **Line:** *"Next in our Real Worlds series, we follow New Horizons beyond Uranus to the icy heart of Pluto."*
   - **Direct audio verification (`599.0–605.0 s`, `clip_601_worlds.mp3`):** Because `"Worlds"` ends with an alveolar sibilant `/z/` and `"series"` immediately begins with an alveolar sibilant `/s/`, the two adjacent sibilants coalesce across the word boundary (`[wɜːldz ˈsɪəriːz]`) into a single continuous sibilant onset into `"series"`, which Scribe tokenizes as singular `"World"`. Spoken delivery is clean and natural.

---

## 3. Section / Chapter Tail Decay Verification (`PASS`)

Verified both from the 100 ms RMS decay envelopes in `J2155_VO_CHECKS_v01.json` and by direct native `audio_input` listening to the final `4.0 s` of all seven section WAVs (`parts/uranus_vo_v01/ch00.wav` .. `ch06.wav`, concatenated with `0.70 s` `gap.wav` silence between sections):

| Section | Chapter | Duration | Final Line Ending | Final 100 ms RMS / Peak | Direct Audio & Envelope Verdict |
|---|---|---:|---|---:|---|
| `ch00` | `open` | `57.36 s` | `"...spacecraft to visit Uranus find there?"` | `-32.01 dBFS` / `-19.66 dBFS` | Clean vowel release on `"there?"` and natural decay (`PASS`) |
| `ch01` | `The Star That Moved` | `96.32 s` | `"...reveal that Uranus was tipped onto its side."` | `-43.93 dBFS` / `-32.12 dBFS` | Full `/d/` release on `"side."` and clean decay (`PASS`) |
| `ch02` | `The World Knocked Sideways` | `110.16 s` | `"...best way to help Orbit keep going."` | `-34.30 dBFS` / `-21.17 dBFS` | Full nasal `/ŋ/` release on `"going."` (`PASS`) |
| `ch03` | `Six Hours at the Ice Giant` | `90.00 s` | `"...frozen world where nothing ever changes?"` | `-45.00 dBFS` / `-31.39 dBFS` | Full final `/z/` sibilant on `"changes?"` (`PASS`) |
| `ch04` | `The Corkscrew Magnet` | `87.36 s` | `"...beneath those clouds to land on the ice below?"` | `-32.09 dBFS` / `-22.80 dBFS` | Clean diphthong decay on `"below?"` (`PASS`) |
| `ch05` | `Why You Can't Land on Ice` | `69.20 s` | `"...solid ice and look up at those vertical rings?"` | `-35.47 dBFS` / `-17.12 dBFS` | Full voiced `/z/` release on `"rings?"` (`PASS`) |
| `ch06` | `The Ten-Minute Cliff on Miranda` | `96.80 s` | `"...nitrogen ice hides without a single crater."` | `-44.11 dBFS` / `-29.58 dBFS` | Complete schwa `/ə/` decay on `"crater."` (`PASS`) |

---

## 4. Handoff & Queue Application (`jobs.with_git`)

1. **`J2155` closed `done` (`033 vo` -> `done`):** `uranus_vo_v01.wav` (`611.40 s`, SHA-256 `3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460`) is accepted as the locked VO master for `OWB:033`. All `J2155` evidence files (`J2155_VO_CHECKS_v01.json`, `J2155_VO_REVIEW_v01.md`, `stt/uranus_vo_v01/stt_raw.json`, `stt/uranus_vo_v01/words.srt`, `uranus_vo_v01_TAKE.json`) and the `7,858`-character ElevenLabs ledger entries (`04_Audio/elevenlabs_ledger.jsonl`, `05_Analytics/ai_spend/ledger.jsonl`) are landed on `main` in this commit (superseding PR #502).
2. **`J2165` explicitly cleared to start:** With `J2155` closed `done` and `uranus_vo_v01` (`611.40 s`) explicitly accepted by `J2164`, `J2165` (*033 Uranus: shot list after explicit VO acceptance*, `after: J2155`) is now unblocked and ready for immediate claim.
3. **`J2164` closed `done`:** Verdict `KEEP` recorded in `--result`.
