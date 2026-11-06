# J2281 — Condition Verification for J0862 (HOS 009 + 010 Shorts VO)

- **Job:** `J2281` (`Verify condition for J0862`, `recheck_of: J0862`)
- **Agent:** `gemini` (`gemini-argon`, worker lane; `audio_input` capability demonstrated and recorded via `chief_relay.py capabilities`)
- **Date:** 2026-11-06T15:04Z
- **Verdict:** **HOLD / CONDITION UNMET** — `J2279` (`J0862 v04: audition repeated-phrase word-gate failure and scope repair`) remains `open` (`for: gemini`) and `vo_check_py312.sh` still exits `1` (`FAIL`) on `hos_009_short_B_v04.{mp3,wav}` on HOS PR #423 (`cb18632d`). Direct audio audition and ASR segment analysis completed in this verification pass and recorded below for `J2279` and the elected Chief (`codex`).

---

## 1. Condition & Queue State Checked

1. **Parent Job `J0862` (`HOS 009 + 010: Shorts voiceover (2 Shorts each) from the v02 Shorts scripts, vo_check, park for Chief`):**
   - Status: `blocked` by `codex` at `2026-11-06T12:14Z` (`step 2 of 3`).
   - Hold condition:
     > `J2279 must directly audition v04 and reused v03 body and resolve word-gate repeated phrase near19.74s. Session inspected actual tools: no demonstrated audio_input; MP3 and WAV vo_check both FAIL. PR423 cb18632d preserves evidence. No generation or gate override authorized.`
2. **Follow-up Job `J2279` (`J0862 v04: audition repeated-phrase word-gate failure and scope repair`):**
   - Status: `open` (`by: ""`, `for: "gemini"`, `model: "gemini-argon"`, `required_capabilities: ["audio_input"]`).
   - Because `J2279` has not yet been claimed or completed, the repair/gate resolution on HOS PR #423 (`cb18632da4462cc49ae5535b9675b7fd61cc49f5`) is not yet applied, and `J0862` cannot be reopened yet.

---

## 2. Direct Audio Audition (`audio_input`) & SHA-256 Verification

In this session, `gemini` directly perceived the audio streams via `read_file` (`audio/mpeg` and `audio/wav`) and verified all file hashes on disk in `/Users/benjaminoats/YouTube/History Of Science`:

| File | SHA-256 | Duration | Direct Audio Audition Result |
|---|---|---|---|
| `009/10_Shorts/vo_v02/hos_009_short_B_v04.wav` | `e271771b423605690451df8179261da2611f8e51cff653c1496441f0e17205c9` | `24.480 s` | **Clean.** No repeated word or phrase anywhere in the file. |
| `009/10_Shorts/vo_v02/hos_009_short_B_v04.mp3` | `b19373132236f970d3657938403b1ae63d15f65014c1c79899e6f4e473fea6f4` | `24.480 s` | **Clean.** Matches WAV; no repeated phrase at `19.74 s` or `24.14 s`. |
| `009/10_Shorts/vo_v02/hos_009_short_B_open_v04.wav` | `1c1a69aa2342cac31dc1a5a8f405ffcb7fed153e4a55210e2d3434227b6fd859` | `6.580 s` | **Clean.** 2-sentence opening pickup (`"In one minute, the Moon falls five metres. An apple falls that far in one second."`). |
| `009/10_Shorts/vo_v02/hos_009_short_B_open_v04.mp3` | `46f740fed774a36a1853b908989c9c20812bf92a1c09b4c8f5ee3b270eeaa26b` | `6.580 s` | **Clean.** S01 ends at `2.660 s` (`2.820 s` after measured silence trim `<= 2.850 s`). |
| `009/10_Shorts/vo_v02/hos_009_short_B_v03.mp3` | `ea0babb393cb68036ef0ed29e1acd5c200bfb57c3dc74f6af29eba4eebb7b10f` | `23.680 s` | **Clean body `[6.020:23.680]`.** `"One pull for apples and moons."` spoken once at the end. |
| `009/10_Shorts/vo_v02/hos_009_short_A_v02.mp3` | `c2fd407d3aafbe57030b29b213ed128ee4887b785272a2192b4c0809796a1ce6` | `25.320 s` | Retained `KEEP` take untouched. |
| `010/10_Shorts/vo_v02/hos_010_short_A_v02.mp3` | `68d88b5b5883f2376bcec29c26d77efea7634d5c7705693f41202ca587b927fb` | `23.289 s` | Retained `KEEP` take (J1004 Option A1) untouched. |
| `010/10_Shorts/vo_v02/hos_010_short_C_v02.mp3` | `20432ecd645b28e9fdc051578a284cb2845bd09f3040170b192089b256055b87` | `23.560 s` | Retained `KEEP` take untouched. |

### What Is Actually Heard in `hos_009_short_B_v04.{mp3,wav}`
- `0.00–2.66 s`: *"In one minute, the Moon falls five metres."* (hook `2.820 s <= 2.850 s`, clean cadence)
- `3.54–6.32 s`: *"An apple falls that far in one second."* (`0.400 s` clean silence splice at `6.420–6.820 s`)
- `6.84–8.34 s`: *"Isaac Newton worked out why."* (reused `v03.wav[6.020:23.680]` body starts cleanly)
- `9.36–13.12 s`: *"The Moon is sixty times further from the Earth's centre than we are,"*
- `13.36–18.72 s`: *"so the pull on it is sixty times sixty weaker — three thousand six hundred times."*
- `19.40–20.70 s`: *"And the numbers matched."*
- `21.32–24.14 s`: *"One pull for apples and moons."*
- `24.14–24.48 s`: Quiet post-speech tail (`0.34 s`) — **zero spoken words**.

---

## 3. Exact Diagnosis of the `vo_check.py` Failure (`~0:19.74` Insert)

Inspection of `.venv_vo_check_py312/bin/python` (`faster-whisper small.en`) on `hos_009_short_B_v04.wav` and `hos_009_short_B_v04.mp3` proves two compounding ASR/tool bugs:

1. **Trailing-Silence Prompt-Repeat Hallucination in `Seg 8 [24.14 -> 24.32]`:**
   - With `word_timestamps=False`, `faster-whisper small.en` produces **8 segments** (`Seg 0` to `Seg 7 [21.36 -> 24.44]`) matching the 59-word script with **0 diffs**.
   - With `word_timestamps=True`, DTW word alignment pulls `Seg 7`'s end timestamp back from `24.44 s` to `24.14 s` (`' One pull for apples and moons.'`, `no_speech_prob = 0.001`, `avg_logprob = -0.205` WAV / `-0.203` MP3, word probabilities `0.763–0.993`).
   - Because `last_speech_timestamp = 24.14 s < 24.48 s`, `faster-whisper` runs a second seek window on the remaining `0.34 s` of silence (`[24.14 -> 24.48 s]`) conditioned on the previous text prompt, emitting a hallucinated **`Seg 8 [24.14 -> 24.32]`**:
     - Text: `' One pull for apples and moons.'` (exact duplicate of `Seg 7` squeezed into `0.18 s` = `2,000 wpm`)
     - `no_speech_prob = 0.986` (WAV) / `0.988` (MP3) (**98.6–98.8% no-speech probability**)
     - `avg_logprob = -0.987` (WAV) / `-0.966` (MP3) (bypasses `faster-whisper`'s default `no_speech_threshold = 0.6` only because `faster-whisper` requires *both* `no_speech_prob > 0.6` *and* `avg_logprob < -1.0`)
     - Word timestamps/probabilities in `Seg 8`:
       - `'One'`: `24.14–24.14 s` (`0.00 s`), `prob = 0.0006` (WAV) / `0.001` (MP3)
       - `'pull'`: `24.14–24.14 s` (`0.00 s`), `prob = 0.0000`
       - `'for'`: `24.14–24.16 s` (`0.02 s`), `prob = 0.0192`
       - `'apples'`: `24.16–24.26 s` (`0.10 s`), `prob = 0.0000`
       - `'and'`: `24.26–24.26 s` (`0.00 s`), `prob = 0.1578` (WAV) / `0.153` (MP3)
       - `'moons.'`: `24.26–24.32 s` (`0.06 s`), `prob = 0.0000`
2. **Timestamp Mis-Indexing (`24.14 s` reported as `0:19.74`) in `vo_check.py`:**
   - `vo_check.py` strips 9 cardinal number tokens (`one`, `five`, `one`, `60`, `60`, `3`, `600`, `one`, `one`) in `norm()` before running `difflib.SequenceMatcher(None, script_words, heard)`.
   - It then indexes `words[min(b1, len(words) - 1)][0]` using `b1 = 48` (an index into the 53-word normalized `heard` list) on the un-normalized `words` list (`len = 62`), landing on `words[48]` (`'the'` at `19.74 s` in *"And the numbers matched"*) instead of the actual inserted words at `24.14 s`.

---

## 4. Next Steps

1. **Elected Chief (`codex`):**
   - `scripts/jobs.py` restricts `jobs.py wait J0862 --recheck J2281` to the elected Chief (`Only the elected Chief may record a condition check`).
   - Run:
     ```bash
     python3 scripts/jobs.py wait J0862 --agent codex --type capability --requires audio_input --condition "J2279 (open for gemini) must apply the bounded vo_check.py trailing no-speech hallucination filter + norm timestamp alignment and rerun vo_check_py312.sh PASS on HOS PR #423 (direct audio audition in J2281 confirmed hos_009_short_B_v04.{mp3,wav} is clean with 0 spoken repeats; Seg 8 [24.14->24.32] has no_speech_prob=0.986/0.988)" --check-at 2026-11-06T21:05:00Z --recheck J2281 --git
     ```
   - Then mark `J2281` done.
2. **Audio Review/Repair Job `J2279` (`gemini`):**
   - Claim `J2279` next and apply the bounded `vo_check.py` fix (skipping trailing `no_speech_prob > 0.85` low-probability/duplicate hallucination segments + preserving `(timestamp, norm_word)` pairs so `word_diffs` timestamps never shift across cardinal numbers) with unit tests in `test_vo_check_words.py`, rerun `vo_check_py312.sh` and `check_all.sh` on HOS PR #423 (`009` and `010`), and reopen `J0862`.
