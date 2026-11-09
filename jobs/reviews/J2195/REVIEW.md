# Rule H Review — `J2195` (Review of `J0862`: HOS `009` + `010` Shorts Voiceover `v02` / `009 Short B` `v03`)

- **Review Job:** `J2195` (`kind: review`, `review_of: J0862`, `repo: hos`, `film: 009`, `stage: vo`)
- **Reviewed Job:** `J0862` (`HOS 009 + 010: Shorts voiceover (2 Shorts each) from the v02 Shorts scripts, vo_check, park for Chief`)
- **Prior Review:** `J1894` (`jobs/reviews/J1894/REVIEW.md`, commit `eaed0b97f8`)
- **Reviewer:** `gemini` (`--agent gemini`, demonstrated `audio_input` capability via `read_file` on `hos_009_short_B_v03.mp3`)
- **Date:** 2026-11-06 UTC
- **Verdict:** **FIX**

---

## 1. Executive Verdict

**Verdict: FIX** — Reopen `J0862` with a **single scoped 2-sentence opening pickup (`82` characters, `16` words)** for **`009 Short B` (`hos_009_short_B_open_v04`)**, concatenated onto the already-verified clean 43-word body of **`hos_009_short_B_v03.wav[6.020:23.680]` (`17.660 s`)** to produce **`hos_009_short_B_v04.{wav,mp3}`** (`59` orthographical / `60` spoken words, `~22.80 s` VO, `~23.80 s` total with `1.00 s` loop tail, `S01` hook sentence end `~2.26 s <= 2.850 s` at `1.00x`).

1. **Three of the four Shorts VO deliverables in `J0862` are verified `PASS` and locked (`KEEP` — do not regenerate or re-spend):**
   - **`009 Short A` (`hos_009_short_A_v02`)**: `vo_check_py312.sh` **PASS** (`24.32 s` VO, `-23.2 dB` mean, `-4.1 dB` peak, `146 wpm`, `0` word mismatches), `S01` hook ends at **`2.800 s <= 2.850 s`** at `1.00x`, total duration **`25.32 s`** (in `[22.00, 27.00] s`).
   - **`010 Short A` (`hos_010_short_A_v02`)**: `vo_check_py312.sh` **PASS** (`22.72 s` VO, `-22.6 dB` mean, `-4.3 dB` peak, `158 wpm`, `0` word mismatches), `S01` hook ends at **`2.849 s <= 2.850 s`** under the approved `J1004` / HOS PR `#366` **Option A1** (`-0.260 s` word-preserving onset/pause trim + `atempo = 1.06x` on `S01`, `0` words changed, `£0` extra spend), total duration **`23.289 s`** (in `[22.00, 27.00] s`).
   - **`010 Short C` (`hos_010_short_C_v02`)**: `vo_check_py312.sh` **PASS** (`22.56 s` VO, `-23.6 dB` mean, `-4.6 dB` peak, `154 wpm`, `0` word mismatches), `S01` hook ends at **`1.780 s <= 2.850 s`** at `1.00x`, total duration **`23.56 s`** (in `[22.00, 27.00] s`).
2. **Why `009 Short B` (`hos_009_short_B_v03`, HOS PR `#423` commits `74a01241` / `8d51256c`) requires a `v04` opening pickup:**
   - The `J0862` worker followed `J1894`'s authorization (`1` take, `316` exact characters logged in `spend_ledger.jsonl`, `97,352` ElevenLabs credits remaining after the take) and stopped rather than making an unauthorized second take.
   - However, `J1894`'s 57-word `v03` text opened with a 10-word / 14-syllable comparative clause followed by a verbless fragment:
     - `S01`: *"In one minute the Moon drops an apple's one-second fall."*
     - `S02`: *"About five metres each."*
   - In Ben's voice (`eleven_v3`, `speed=1.04`), that 14-syllable `S01` spans **`0.120–3.680 s`** (`3.560 s` speech). Waveform `< -38 dB` RMS analysis shows only `0.270 s` of true trimmable silence before `3.680 s`; even with `-0.270 s` silence trim plus the `J1004` maximum `atempo = 1.06x`, `S01` finishes at **`(3.680 - 0.270) / 1.06 = 3.217 s > 2.850 s`**.
   - In addition, `"drops an apple's"` (`/ps ən æpəlz/`) triggers a homophone transcription collision (`"drops and apples"`) in both ElevenLabs Scribe (`stt_raw.json` words `12` & `14`) and `faster-whisper small.en` (`vo_check.py` warning at `~1.98 s`), and because `"About five metres each."` is a verbless fragment attached to `"fall"`, `eleven_v3` read `"fall,"` with comma prosody and Scribe punctuated it `'fall,'` (so `hos_build_rule_v02.py`'s `hook_sentence_info()` does not see a terminal `.?!` until `"each."` at `5.500 s`).
   - Meanwhile, the **43-word body of `hos_009_short_B_v03.wav`** (`6.020–23.680 s`, `17.660 s`, preceded by a clean `0.520 s` silence at `5.500–6.020 s`: *"Isaac Newton worked out why. The Moon is sixty times further from the Earth's centre than we are, so the pull on it is sixty times sixty weaker. Three thousand six hundred times. And the numbers matched. One pull, for apples and Moons."*) is **already recorded, directly auditioned (`audio_input`), and verified clean (`0` word/homophone mismatches)**.
3. **Why HOS PR `#423` is NOT merged in `J2195`:**
   - HOS PR `#423` modifies `00_Brand/Channel-Setup/kanban/index.html`, `00_Brand/Channel-Setup/PIPELINE.json`, and `STATUS.md` (board/pipeline files outside `02_Video-Projects/`, `jobs/`, `05_Analytics`) and parks an unresolved `Short_B` hook (`3.680 s > 2.850 s`). Under Rule H item 4, `J2195` leaves PR `#423` unmerged and reopens `J0862` with the exact `v04` 2-sentence opening pickup scope.

---

## 2. Deliverable Verification & Acoustic Evidence

### 2.1 File Integrity & `vo_check_py312.sh` Summary (`009` + `010` Shorts VO)

| Short | Stem | MP3 SHA-256 (`vo_v02/`) | WAV SHA-256 (`vo_v02/`) | `vo_check_py312.sh` | Words | Raw `S01` End | Shaped `S01` End (`<= 2.850 s`) | Total w/ `1.00 s` Tail (`22–27 s`) | Disposition |
|---|---|---|---|---|---:|---:|---:|---:|---|
| `009 Short A` | `hos_009_short_A_v02` | `c2fd407d3aafbe57030b29b213ed128ee4887b785272a2192b4c0809796a1ce6` | `48847b15feda51804a0f6afae1a79aacc74b9bac43ef3eeadda8a7503b745571` | **PASS** (`-23.2 dB` mean, `-4.1 dB` peak, `146 wpm`) | `59` | `2.800 s` | **`2.800 s`** (`1.00x`) | **`25.320 s`** | **KEEP** |
| `009 Short B` (`v02`) | `hos_009_short_B_v02` | `3ae503684c148455d4364c9955ce88dc70caa74df110daf700cd5fa199e7bccd` | `838fa560076cbffb61a7a86d2ce7b2ade93f916b1f90f4206ab374666c14698f` | **PASS** (`-23.9 dB` mean, `-4.6 dB` peak, `151 wpm`) | `59` | `4.580 s` | `3.001 s` (**FAIL** `> 2.850 s`) | `24.130 s` | Preserve on disk |
| `009 Short B` (`v03`) | `hos_009_short_B_v03` | `ea0babb393cb68036ef0ed29e1acd5c200bfb57c3dc74f6af29eba4eebb7b10f` | `f67e8bdfd3badeb97d142fa96a1b67eb68a9dfec49c364e3907cd983d9fa3347` | **PASS** (`-23.7 dB` mean, `-3.9 dB` peak, `137 wpm`, `1` homophone warning `"and"` vs `"an"`) | `57` (`58` spoken) | `3.680 s` (`5.500 s` to `.`) | `3.217 s` min (`3.330 s` in PR `#423`, **FAIL** `> 2.850 s`) | `24.680 s` | Preserve on disk; reuse clean body `[6.020:23.680]` |
| `010 Short A` | `hos_010_short_A_v02` | `68d88b5b5883f2376bcec29c26d77efea7634d5c7705693f41202ca587b927fb` | `2488aa8b49beb3a642597e08f30ca53e723fbee00cd21ad8bdc581a9293ff228` | **PASS** (`-22.6 dB` mean, `-4.3 dB` peak, `158 wpm`) | `60` | `3.280 s` | **`2.849 s`** (`J1004` Option A1: `-0.260 s` trim + `1.06x`) | **`23.289 s`** | **KEEP** |
| `010 Short C` | `hos_010_short_C_v02` | `20432ecd645b28e9fdc051578a284cb2845bd09f3040170b192089b256055b87` | `ca814ab01ad72fde015b4e157638b5e346d592e5df54cefe97e38969340fcb0c` | **PASS** (`-23.6 dB` mean, `-4.6 dB` peak, `154 wpm`) | `58` | `1.780 s` | **`1.780 s`** (`1.00x`) | **`23.560 s`** | **KEEP** |

### 2.2 Direct Audio Audition & Waveform Analysis of `hos_009_short_B_v03`

1. **Direct Listening (`audio_input`)**:
   - Auditioned `02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/vo_v02/hos_009_short_B_v03.mp3` directly via `read_file` (`audio/mpeg`).
   - In `0.00–5.50 s`, Ben reads *"In one minute the Moon drops an apple's one-second fall, about five metres each."* as a single linked clause+appositive phrase with a shallow comma pause (`0.48 s`) after *"fall"* and coarticulated `/ps ən æpəlz/` (*"drops an apple's"*), which sounds identical to *"drops and apples"*.
   - After a clean `0.520 s` silence (`5.500–6.020 s`), the 43-word body (`6.020–23.580 s`, `17.560 s` speech / `17.660 s` slice `6.020–23.680 s`: *"Isaac Newton worked out why. The Moon is sixty times further from the Earth's centre than we are, so the pull on it is sixty times sixty weaker. Three thousand six hundred times. And the numbers matched. One pull, for apples and Moons."*) is crisp, unhurried, warm British narration with zero stumbles, clicks, or homophone ambiguities.
2. **Word-Level Scribe & `< -38 dB` Silence Proof (`0.000–6.020 s`)**:
   - Scribe tokens (`stt/hos_009_short_B_v03/stt_raw.json`):
     - `w[0..20]` (`0.120–3.680 s`): `'In'` (`0.12–0.20`), `'one'` (`0.26–0.40`), `'minute,'` (`0.48–0.70`), `'the'` (`0.84–0.94`), `'moon'` (`1.00–1.26`), `'drops'` (`1.34–1.74`), `'and'` (`1.78–1.88`), `'apples'` (`2.02–2.40`), `'one'` (`2.52–2.68`), `'second'` (`2.82–3.20`), `'fall,'` (`3.34–3.68`).
     - `w[22..28]` (`4.160–5.500 s`): `'about'` (`4.16–4.46`), `'five'` (`4.50–4.74`), `'meters'` (`4.78–5.12`), `'each.'` (`5.20–5.50`).
   - True `< -38 dB` silence windows in `0.000–3.680 s` (`hos_009_short_B_v03.wav`):
     - `0.000–0.090 s` (`0.090 s` lead-in)
     - `0.660–0.790 s` (`0.130 s` after `"minute"`, keeping `0.060 s` natural breath = `0.070 s` trimmable)
     - `1.720–1.860 s` (`0.140 s` after `"drops"`, keeping `0.060 s` = `0.080 s` trimmable)
     - `2.530–2.620 s` (`0.090 s` after `"apples"`, keeping `0.060 s` = `0.030 s` trimmable)
   - Maximum word-preserving silence trim in `S01` is `0.090 + 0.070 + 0.080 + 0.030 = 0.270 s`. Even at the `J1004` ceiling `atempo = 1.06x`, `S01` ends at **`(3.680 - 0.270) / 1.06 = 3.217 s > 2.850 s`** (would require `atempo = 1.196x`, violating the `<= 1.06x` lock).
   - Furthermore, long-form Part 4 (`02_Voiceover/hos_009_part04_the_moon_test_v01.wav`) cannot donate an opening audio splice because its wording is *"A falling apple drops that far in a single second."* (`33.54–36.22 s`) and never speaks the words `"In one minute"`.

---

## 3. Locked `v04` Fix for `009 Short B` (`J0862`)

### 3.1 Why Splitting the Opening Comparison into Two Complete 8-Word Sentences Solves Every Gate

Any single English clause that packs all four comparative elements (`In one minute`, `the Moon`, `an apple`, `in one second`) plus a verb (`falls`/`drops`) contains `13–14` syllables and 4 stress peaks, which takes `3.40–3.68 s` in Ben's voice (`> 2.850 s` even at `1.06x`).

Splitting the opening comparison across `S01` (`P4:05_minute_second`) and `S02` (`P1:02_apple_and_moon`) as **two independent 8-word, 10-syllable complete sentences**:

- **`S01` (`P4:05_minute_second`, 8 words, 10 syllables, 43 chars):**
  > `In one minute, the Moon falls five metres.`
- **`S02` (`P1:02_apple_and_moon`, 8 words, 10 syllables, 38 chars):**
  > `An apple falls that far in one second.`

satisfies every `AGENTS.md`, `J1004`, `6426967421`, and `hos_build_rule_v02.py` requirement simultaneously:

1. **`S01` Hook Sentence Ends `<= 2.850 s` at `1.00x`**:
   - Measured word durations from Ben's existing `v02`/`v03` takes:
     `In` (`0.08 s`) + `one` (`0.14 s`) + `minute,` (`0.22 s`) + `the` (`0.10 s`) + `Moon` (`0.26 s`) + `falls` (`0.22 s`) + `five` (`0.24 s`) + `metres.` (`0.42 s`) = **`1.68 s` pure speech**, or **`~2.15–2.30 s` at `1.00x`** with natural inter-word breath (`<= 2.850 s` with `~0.55 s` margin at `1.00x`, and `~2.03–2.17 s` if `atempo <= 1.06x` is ever needed).
2. **True Terminal Period on `S01`**:
   - `S01` is a complete grammatical sentence ending on `"metres."` and followed by a full independent sentence (`"An apple falls that far in one second."`), so `eleven_v3` reads `"metres."` with falling terminal prosody and Scribe punctuates it with `.`, guaranteeing `hos_build_rule_v02.py`'s `hook_sentence_info()` (`wt[-1:] in ".?!"`) detects `hook_end_s <= 2.85 s`.
3. **Zero Homophone Collision**:
   - Eliminates the possessive `"an apple's"` (`/ən æpəlz/` -> `"and apples"`). The exact words `"An apple falls ... in one second."` were already tested in `hos_009_short_B_v02` and passed `faster-whisper small.en` with `0` word or homophone warnings.
4. **Preserves Both Required Time Intervals & `FACT_NOTES` Scale (`6426967421` / `J1004` / `#6631275536`)**:
   - Preserves the exact substrings `"In one minute"` (`S01`) and `"in one second"` (`S02`) across the two opening comparison plates (`P4:05_minute_second` -> `P1:02_apple_and_moon`), plus the `FACT_NOTES_v01.md` row 30 distance `"five metres"` ($15\frac{1}{12}$ Paris feet $\approx 4.90\text{ m}$).
5. **Reuses the Clean 43-Word Body from `hos_009_short_B_v03.wav` (`82`-Char Pickup Only)**:
   - Following the `J2175` / `J2254` pickup-concatenation pattern, `J0862` records **only the 2-sentence opening pickup (`82` characters, `16` words)** and concatenates it with `0.40 s` clean silence before `hos_009_short_B_v03.wav[6.020:23.680]` (`17.660 s`, `43` words):
     - **Full 59-word (`60` spoken words) `hos_009_short_B_v04` transcript** (in the `55–65` word lock):
       > `In one minute, the Moon falls five metres. An apple falls that far in one second. Isaac Newton worked out why. The Moon is sixty times further from the Earth's centre than we are, so the pull on it is sixty times sixty weaker. Three thousand six hundred times. And the numbers matched. One pull, for apples and Moons.`
     - **Expected VO duration:** `~4.74 s` (16-word opening) + `0.40 s` (inter-sentence pause) + `17.66 s` (`v03` body `[6.020:23.680]`) = **`~22.80 s` VO**, and **`~23.80 s` total with the `1.00 s` loop tail** (squarely inside `[22.00, 27.00] s`).
   - Simulated against `hos_build_rule_v02.find_word_cuts(words, n_cuts=8, total_dur=23.80, tail_s=1.0)`: produces **8 body cuts (`S01..S08`)** matching `PLATES_FILMS[("009", "Short_B")]`:
     - `S01` (`P4:05_minute_second`): `0.000 -> 2.260 s` (`dur = 2.260 s <= 2.850 s`, `"In one minute, the Moon falls five metres."`)
     - `S02` (`P1:02_apple_and_moon`): `2.260 -> 4.840 s` (`dur = 2.580 s`, `"An apple falls that far in one second."`)
     - `S03` (`P1:03_woolsthorpe_orchard`): `4.840 -> 7.940 s` (`dur = 3.100 s`, `"Isaac Newton worked out why."`)
     - `S04` (`P2:03_cannonball_paths`): `7.940 -> 11.320 s` (`dur = 3.380 s`, `"The Moon is sixty times further from the Earth's centre"`)
     - `S05` (`P2:05_full_orbit`): `11.320 -> 14.520 s` (`dur = 3.200 s`, `"than we are, so the pull on it is sixty"`)
     - `S06` (`P3:04_inverse_square_diagram`): `14.520 -> 17.280 s` (`dur = 2.760 s`, `"times sixty weaker. Three thousand"`)
     - `S07` (`P4:03_principia_open`): `17.280 -> 19.920 s` (`dur = 2.640 s`, `"six hundred times. And the numbers matched."`)
     - `S08` (`P4:06_earth_moon_wide`): `19.920 -> 22.800 s` (`dur = 2.880 s`, `"One pull, for apples and Moons."`)
     - `loop_tail` (`P4:05_minute_second`): `22.800 -> 23.800 s` (`dur = 1.000 s`)

---

## 4. Exact Fix List for `J0862`

When `J0862` runs, the worker must execute these exact steps:

1. **Do NOT regenerate `009 Short A` (`hos_009_short_A_v02`), `010 Short A` (`hos_010_short_A_v02`), or `010 Short C` (`hos_010_short_C_v02`), and do NOT delete `hos_009_short_B_v02.{mp3,wav}` or `hos_009_short_B_v03.{mp3,wav}`.**
2. **Record 1 scoped 2-sentence opening pickup (`82` characters) for `009 Short B` (`hos_009_short_B_open_v04`)**:
   - Check live ElevenLabs subscription credits first via `04_Audio/tools/el_client.py` (`el_user_info()`) and paste the live credit balance in the report.
   - Run **at most 1 take** (`82` chars) via `04_Audio/tools/vo_take.py`:
     ```bash
     python3 04_Audio/tools/vo_take.py \
       --text "In one minute, the Moon falls five metres. An apple falls that far in one second." \
       --out 02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/vo_v02 \
       --stem hos_009_short_B_open_v04 \
       --order J2195 --order 6631275536
     ```
   - If `S01` (`"In one minute, the Moon falls five metres."`) in `hos_009_short_B_open_v04.wav` exceeds `2.850 s` raw, apply only zero-extra-spend word-preserving lead-in/inter-word silence trim (`>= 0.060 s` natural gaps preserved) and/or `atempo <= 1.06x` on `S01` (`J1004` Option A1). Never take an unapproved second ElevenLabs generation.
3. **Assemble `hos_009_short_B_v04.{wav,mp3}` and `stt/hos_009_short_B_v04/`**:
   - Slice the clean 16-word opening from `hos_009_short_B_open_v04.wav` (through the end of `"second."`), append `0.400 s` clean silence (`48000 Hz`, mono, `pcm_s16le`), and append the clean 43-word body from `hos_009_short_B_v03.wav[6.020:23.680]` (`17.660 s`, `"Isaac Newton worked out why. ... One pull, for apples and Moons."`) to write `02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/vo_v02/hos_009_short_B_v04.wav` (`48000 Hz`, mono, `pcm_s16le`) and `hos_009_short_B_v04.mp3` (`libmp3lame -b:a 192k`).
   - Build the combined word-level timing files (`stt/hos_009_short_B_v04/stt_raw.json` and `stt/hos_009_short_B_v04/words.srt`) by combining the `hos_009_short_B_open_v04` Scribe word timestamps with the offset-shifted `hos_009_short_B_v03` body word timestamps (`w[30..108]`), and write `hos_009_short_B_v04_TAKE.json`.
4. **Run `vo_check_py312.sh` and Hook / Cut Verification**:
   - Update `02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/SHORTS_SCRIPTS_v02.md` `Short B` `[VO]` block to the 59-word `v04` text (`"In one minute, the Moon falls five metres. An apple falls that far in one second. Isaac Newton worked out why. The Moon is sixty times further from the Earth's centre than we are, so the pull on it is sixty times sixty weaker. Three thousand six hundred times. And the numbers matched. One pull, for apples and Moons."`) and record the `v04` stem and SHA-256 hashes.
   - Run `00_Brand/Channel-Setup/tools/vo_check_py312.sh` on all four takes (`hos_009_short_A_v02.mp3`, `hos_009_short_B_v04.mp3`, `hos_010_short_A_v02.mp3`, `hos_010_short_C_v02.mp3`) against their `SHORTS_SCRIPTS_v02.md` files and confirm **PASS** (`0` word/homophone mismatches on `hos_009_short_B_v04.mp3`, mean `-19` to `-28 dB`, peak `<= -1.0 dB`, `135–170 wpm`).
   - Verify `S01` hook sentence end `<= 2.850 s`, total duration `22.00–27.00 s` (including `1.00 s` loop tail), and 8 body cuts (`S01..S08`) via `hos_build_rule_v02.find_word_cuts()`.
   - **Important `check_all.sh` compatibility note**: `00_Brand/Channel-Setup/tools/hos_build_rule_v02.py` line 1651 (`run_negative_checks()` negative check #7) asserts that `02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/SHORTS_PICTURE_PLAN_v02.json` `Short_B` retains its historical `hook_conflict` dict for the negative test suite. Therefore, keep `Short_B["hook_conflict"]` intact in `009/10_Shorts/SHORTS_PICTURE_PLAN_v02.json` and add the verified `hos_009_short_B_v04` metadata, SHA-256, `hook_end_s`, `total_duration_s`, and 8-row `cuts` table under `Short_B["approved_vo_v04"]` (do not edit `hos_build_rule_v02.py`).
5. **Update `production-status.md`, Run `check_all.sh`, and Update HOS PR `#423`**:
   - Paste the `vo_check_py312.sh` PASS outputs, SHA-256 hashes, hook end times (`009 Short A` `2.800 s`, `009 Short B v04` `<= 2.850 s`, `010 Short A` `2.849 s` Option A1, `010 Short C` `1.780 s`), and live ElevenLabs credit ledger entry in `02_Video-Projects/009_The-Falling-Moon-Gravity/production-status.md` and `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/production-status.md`.
   - Run `00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/009_The-Falling-Moon-Gravity` and `00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs` and verify `ALL CHECKS PASS`.
   - Push the updated commit to HOS PR `#423` (`j0862-hos-009-short-b-vo-v03`) — committing **only** `02_Video-Projects/009_The-Falling-Moon-Gravity/...` and `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/...` (plus `04_Audio/tools/spend_ledger.jsonl` if tracked; revert the board/status changes to `00_Brand/Channel-Setup/kanban/index.html`, `00_Brand/Channel-Setup/PIPELINE.json`, and `STATUS.md` on PR `#423` so PR `#423` is a clean records/project PR).
   - Park `J0862` (`jobs.py block J0862 --agent <agent> --reason "parked for Chief: ..." --git`) for Rule H review / Chief sign-off so downstream Shorts assembly jobs (`J2171` for `009`, `J2172` for `010`) can run.
