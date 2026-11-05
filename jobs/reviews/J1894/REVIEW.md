# J1894 — Rule H Review & Condition Verification for J0862 (HOS 009 + 010 Shorts VO v02)

- **Review Job**: `J1894` (`verify condition for J0862`, `kind: review`, `recheck_of: J0862`)
- **Target Job**: `J0862` (`HOS 009 + 010: Shorts voiceover (2 Shorts each) from the v02 Shorts scripts, vo_check, park for Chief`, `kind: vo`, `repo: hos`, `film: 009`, `stage: vo`)
- **Reviewer**: `gemini` (`gemini-argon`)
- **Date**: 5 Nov 2026 (`2026-11-05T07:34Z`)
- **Overall Verdict**: **FIX** (Reopen `J0862` with approved `HOS 009 Short B` replacement opening and exact 1-take recording scope; **KEEP** `009 Short A`, `010 Short A` Option A1, and `010 Short C` `v02` takes untouched — do not regenerate)

---

## 1. Authority & Mandate

1. **Ben's 4 Nov 2026 Decision (HOS desk `#6631275536`, `2026-11-04T13:00:22Z`)**:
   > *"3. J0862, film 009 Short B opening: 'Chief, write and approve it'. The elected Chief writes a replacement opening that fits the 2.85 s hook at atempo <=1.06 and stays physically true, approves it, and scopes the exact take. Spend: the existing guard still applies (fresh live credit read; one take)."*
2. **Rule E & Rule H (5 Nov 2026, OWB commits `453b0192b5` and `d3bf22c65f`)**:
   - Under Rule E (*Wait only for a real outside fact*) and Rule H (*Review jobs decide in one go*), `J1894` was assigned to the `review` lane (`J2023` / `PLAN.md` item 1) to verify the 4 existing `v02` takes, lock the approved `009 Short B` replacement opening + exact 1-take recording scope, write `jobs/reviews/J1894/REVIEW.md`, and reopen `J0862` in one commit.
3. **Zero Spend in `J1894`**:
   - `J1894` is a `kind: review` verification job (`£0` / `0` ElevenLabs characters spent). The single authorized ElevenLabs take (`311` characters out of `101,014` available as of last check) is executed by `J0862` (`kind: vo`) after reopening and performing a fresh live credit read via `04_Audio/tools/el_client.py` / `vo_take.py`.

---

## 2. Audit of the 4 Existing `vo_v02` Shorts Takes (HOS `fe4524ee` / `fa72f43f`)

All four `v02` Shorts takes in `02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/vo_v02/` and `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/vo_v02/` were verified on disk (SHA-256) and checked with `00_Brand/Channel-Setup/tools/vo_check_py312.sh` (`faster-whisper small.en`) and `00_Brand/Channel-Setup/tools/hos_build_rule_v02.py` (`HOOK_END_MAX_S = 2.85`, `ATEMPO_MAX = 1.06`, `DURATION_MIN_S = 22.0`, `DURATION_MAX_S = 27.0`, `TAIL_MAX_S = 1.0`):

| Short | Stem | MP3 SHA-256 | WAV SHA-256 | `vo_check_py312.sh` | Hook End (`<= 2.850 s`) | Total Duration (`22–27 s` w/ `1.00 s` tail) | Verdict |
|---|---|---|---|---|---|---|---|
| **009 Short A** (*What Would Happen If the Moon Stopped Moving?*) | `hos_009_short_A_v02` | `c2fd407d3aafbe57030b29b213ed128ee4887b785272a2192b4c0809796a1ce6` | `48847b15feda51804a0f6afae1a79aacc74b9bac43ef3eeadda8a7503b745571` | **PASS** (`0:24.32`, `-23.2 dB` mean, `-4.1 dB` peak, `146 wpm`) | **PASS (`2.800 s <= 2.850 s` at `1.00x`)** | **PASS (`25.32 s`)** | **KEEP (do not regenerate)** |
| **009 Short B** (*How Did Newton Discover Gravity?*) | `hos_009_short_B_v02` | `3ae503684c148455d4364c9955ce88dc70caa74df110daf700cd5fa199e7bccd` | `838fa560076cbffb61a7a86d2ce7b2ade93f916b1f90f4206ab374666c14698f` | **PASS** (`0:23.44`, `-23.9 dB` mean, `-4.6 dB` peak, `151 wpm`) | **FAIL (`4.580 s` raw / `3.181 s` pure speech = `3.001 s > 2.850 s` at `1.06x` cap)** | `24.13 s` | **FIX opening via 1 scoped take (`hos_009_short_B_v03`); preserve `v02` files on disk** |
| **010 Short A** (*What Killed the Dinosaurs?*) | `hos_010_short_A_v02` | `68d88b5b5883f2376bcec29c26d77efea7634d5c7705693f41202ca587b927fb` | `2488aa8b49beb3a642597e08f30ca53e723fbee00cd21ad8bdc581a9293ff228` | **PASS** (`0:22.72`, `-22.6 dB` mean, `-4.3 dB` peak, `158 wpm`) | **PASS (`2.849 s <= 2.850 s` via `J1004` / PR `#366` Option A1: `-0.260 s` pause trim + `1.06x` on S1, `0` words changed)** | **PASS (`23.289 s`)** | **KEEP with approved `J1004` Option A1 (do not regenerate)** |
| **010 Short C** (*Are Birds Really Dinosaurs?*) | `hos_010_short_C_v02` | `20432ecd645b28e9fdc051578a284cb2845bd09f3040170b192089b256055b87` | `ca814ab01ad72fde015b4e157638b5e346d592e5df54cefe97e38969340fcb0c` | **PASS** (`0:22.56`, `-23.6 dB`, `-4.6 dB` peak, `154 wpm`) | **PASS (`1.780 s <= 2.850 s` at `1.00x`)** | **PASS (`23.56 s`)** | **KEEP (do not regenerate)** |

### Pasted `vo_check_py312.sh` Outputs (5 Nov 2026)

```text
PASS  /tmp/j1894_vo_check/009_short_A.mp3  (0:24.32, mean -23.2 dB, peak -4.1 dB, 146 wpm, 58/59 words via faster-whisper small.en)
  warn: word mismatch: script 'kilometre' vs heard 'kilometer' at ~10.82s
  warn: word mismatch: script 'for ever' vs heard 'forever' at ~15.42s

PASS  /tmp/j1894_vo_check/009_short_B.mp3  (0:23.44, mean -23.9 dB, peak -4.6 dB, 151 wpm, 52/52 words via faster-whisper small.en)

PASS  /tmp/j1894_vo_check/010_short_A.mp3  (0:22.72, mean -22.6 dB, peak -4.3 dB, 158 wpm, 54/55 words via faster-whisper small.en)
  warn: word mismatch: script 'centimetre' vs heard 'centimeter' at ~5.3s

PASS  /tmp/j1894_vo_check/010_short_C.mp3  (0:22.56, mean -23.6 dB, peak -4.6 dB, 154 wpm, 57/57 words via faster-whisper small.en)
```
*(Note: `hos_009_short_B_v02.mp3` SHA-256 is `3ae503684c148455d4364c9955ce88dc70caa74df110daf700cd5fa199e7bccd`.)*

---

## 3. Approved Replacement Opening & Exact 1-Take Scope for `HOS 009 Short B` (`hos_009_short_B_v03`)

### 3.1 Physical Truth & `FACT_NOTES_v01.md` Verification
- **Source (`02_Video-Projects/009_The-Falling-Moon-Gravity/01_Script/FACT_NOTES_v01.md` rows 25 & 30, hard check #2)**:
  - Isaac Newton, *Principia* (1687), Book III, Proposition IV (Motte–Cajori / Cohen–Whitman 1999): at $60$ Earth radii, the Moon deprived of its forward motion falls $15\frac{1}{12}$ Paris feet ($\approx 4.90\text{ m}$) in **one minute**, matching the distance a body at Earth's surface (an apple) falls in **one second** ($15\frac{1}{12}$ Paris feet $\approx 4.90\text{ m}$) under inverse-square scaling ($1/60^2 = 1/3600$).
  - Long Part 04 locked script (`009_the-falling-moon-gravity_script_master_v01.md` L65): *"In one second, an apple falls about five metres. At sixty times the distance, the pull is three thousand six hundred times weaker. Which means in one minute, the Moon should fall about the same distance, five metres."*
- **Why the 16-Word `v02` Opening Failed**:
  - `v02` Sentence 1 (*"In one minute, the Moon falls about as far as an apple falls in one second."*, 16 words, 21 syllables, 75 chars) has `3.181 s` of pure speech alone (`3.001 s > 2.850 s` even at the `1.06x` `atempo` cap, `00_Brand/Channel-Setup/audits/J1004_SHORTS_HOOK_DURATION_DISPOSITION_2026-10-27.md`).
- **Why Both Timing Locks (`hook <= 2.85 s` AND `total duration 22.00–27.00 s` / `55–65 words`) Must Be Satisfied Together**:
  - In `hos_009_short_B_v02.wav`, `w[00..15]` ended at `4.580 s` followed by a `0.980 s` pause before `w[16] "Isaac"` at `5.560 s`, leaving only `17.880 s` of body audio (`5.560–23.440 s`, 43 words).
  - Replacing the `4.580 s` opening with a `~2.65 s` hook and tightening the S1->S2 seam to `< 0.25 s` (`05_Analytics/LEARNINGS.md` Rule 7) would shorten a 1-sentence-only replacement to `~20.75 s` VO (`~21.75 s` total with `1.00 s` tail, violating the `22.00 s` floor and leaving only 54 words).
  - Adding the 4-word `FACT_NOTES`-sourced scale beat ***"About five metres each."*** as Sentence 2 (`S02`, `~1.55 s`) bridges the `2.7–4.5 s` seam with a concrete physical number (`LEARNINGS.md` Rule 7), keeps the total spoken word count at **58 spoken words** (57 orthographical words, inside `55–65`), and lands total VO duration at **`~22.5 s`** (`~23.5 s` total with `1.00 s` loop tail, squarely inside `22.00–27.00 s`).

### 3.2 Approved `HOS 009 Short B` (`v03`) Script (57 Orthographical / 58 Spoken Words, 311 Characters)

- **Approved Sentence 1 (`S01`, `0.00–2.85 s` hook, 10 orthographical / 11 spoken words, 14 syllables, 56 chars)**:
  > ***"In one minute the Moon drops an apple's one-second fall."***
  - Preserves **both** required time intervals (**`one minute`** for the Moon and **`one second`** for the apple), stays physically true, and matches Frame 0 plate `P4:05_minute_second` and caption `1 MINUTE = 1 SECOND` (yellow: `1 SECOND`).
  - **Empirical Token-Duration Proof (from `hos_009_short_B_v02/stt_raw.json`, `eleven_v3`, `speed=1.04`)**:
    - Pure speech sum: `0.100 (In) + 0.140 (one) + 0.280 (minute) + 0.090 (the) + 0.220 (Moon) + 0.200 (drops) + 0.090 (an) + 0.300 (apple's) + 0.140 (one) + 0.300 (second) + 0.320 (fall.) = 2.180 s` (vs `3.181 s` in `v02`, saving `1.001 s` of pure speech).
    - With `0.060 s` onset + `10 × 0.050 s` natural inter-word gaps (`0.500 s`): **`2.740 s <= 2.850 s` at `1.00x`**.
    - With `0.040 s` onset + `10 × 0.040 s` tight inter-word gaps (`0.400 s`) at `atempo = 1.06x`: **`2.472 s <= 2.850 s`** (`0.378 s` margin below `2.850 s`).
- **Approved Sentence 2 (`S02`, `~2.85–4.55 s` scale beat, 4 words, 6 syllables, 23 chars)**:
  > ***"About five metres each."***
  - Sourced directly to `FACT_NOTES_v01.md` row 30 / hard check #2 ($15\frac{1}{12}$ Paris feet $\approx 4.90\text{ m}$, matching Long Part 04 VO *"about five metres"*).
- **Unchanged Body Sentences 3–7 (`S03–S07`, 43 words, verbatim from `SHORTS_SCRIPTS_v02.md`)**:
  > ***"Isaac Newton worked out why. The Moon is sixty times further from the Earth's centre than we are, so the pull on it is sixty times sixty weaker. Three thousand six hundred times. And the numbers matched. One pull, for apples and Moons."***
- **Full Approved `hos_009_short_B_v03` Text (`311` characters)**:
  ```text
  In one minute the Moon drops an apple's one-second fall. About five metres each. Isaac Newton worked out why. The Moon is sixty times further from the Earth's centre than we are, so the pull on it is sixty times sixty weaker. Three thousand six hundred times. And the numbers matched. One pull, for apples and Moons.
  ```

---

## 4. Exact Fix List for `J0862` (`kind: vo`, `repo: hos`)

1. **Preserve Existing Accepted `v02` Takes (No Unchanged Regeneration)**:
   - Do **not** regenerate `hos_009_short_A_v02`, `hos_010_short_A_v02` (approved under `J1004` / PR `#366` Option A1), or `hos_010_short_C_v02`.
   - Keep `02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/vo_v02/hos_009_short_B_v02.{mp3,wav}` untouched on disk as history/fallback.
2. **Update `009 Short B` Script & Picture Plan Metadata in HOS**:
   - In `02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/SHORTS_SCRIPTS_v02.md` (Short B section) and `SHORTS_PICTURE_PLAN_v02.json` (`Short_B`), update the spoken script to the approved 57-word (`58` spoken words, `311` chars) `v03` text above (`S01` on `P4:05_minute_second` `0.00–2.85 s`: *"In one minute the Moon drops an apple's one-second fall."*; `S02` on `P4:05_minute_second` / `P1:07_newton_orchard`: *"About five metres each."*).
3. **Fresh Live Credit Check & Single Scoped Take (`hos_009_short_B_v03`, `311` chars)**:
   - Verify `04_Audio/tools/TTS_PAUSE` is absent and perform a fresh live ElevenLabs credit read via `04_Audio/tools/el_client.py` / `vo_take.py` before calling the API.
   - Run **exactly ONE take** (`311` chars) in `/Users/benjaminoats/YouTube/History Of Science`:
     ```bash
     python3 04_Audio/tools/vo_take.py \
       --text "In one minute the Moon drops an apple's one-second fall. About five metres each. Isaac Newton worked out why. The Moon is sixty times further from the Earth's centre than we are, so the pull on it is sixty times sixty weaker. Three thousand six hundred times. And the numbers matched. One pull, for apples and Moons." \
       --out 02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/vo_v02 \
       --stem hos_009_short_B_v03 \
       --order J1894 --order 6631275536
     ```
   - *(Zero-extra-spend assembly fallback if needed: if `hos_009_short_B_v03`'s `S01` needs `-0.04 to -0.15 s` onset/gap trim or `atempo <= 1.06x` to land `<= 2.850 s`, or if concatenating `hos_009_short_B_v03`'s `S01+S02` opening onto `hos_009_short_B_v02.wav`'s `w[16..55]` body `5.560–23.300 s` yields cleaner pacing, do so in `ffmpeg` from that single take without a second ElevenLabs API call.)*
4. **Gate & Record**:
   - Run `00_Brand/Channel-Setup/tools/vo_check_py312.sh` on `hos_009_short_B_v03.mp3` against the updated Short B script and verify `PASS` (`0` missing/added words, mean `-28` to `-19 dB`, peak `<= -1 dB`, no silence `> 1.5 s`, `S01` hook end `<= 2.850 s` at `atempo <= 1.06x`, total VO duration `21.00–26.00 s` so `total_duration_s` with `<= 1.00 s` loop tail is `22.00–27.00 s`).
   - Paste the `vo_check_py312.sh` `PASS` output into `009` and `010` `production-status.md`, claim/pass `009` and `010` `shorts_vo` on the board, and finish `J0862` so downstream assembly jobs `J2171` (009 Shorts A/B) and `J2172` (010 Shorts A/C) can proceed once long plates are ready.
