# WW2:002 Voiceover Report (`J2995` — `atlantic_black_pit_vo_v01`)

- **Film:** `WW2:002` — *How the Allies Closed the U-Boats' Safest Hunting Ground* (Launch Plan alt: *How Long-Range Bombers Closed the Atlantic Black Pit in May 1943*)
- **Voice & Model:** `Ben Orbit Narrator` (`eleven_v3`, speed `1.04`, API via `04_Audio/tools/vo_take.py` under `desk-lock elevenlabs`)
- **Locked Spoken Script (`J2994` / PR #1009 / `J3031` Chief lock):** `6` chapters reconstructed from `lines_v03.json`, matching `01_Script/NARRATION_v03.txt` byte-for-byte (`SHA-256` `4a46801b1b586558f7ddd8886bff8317f53084d9fc44994874bedfaab039b63a`), `3,268` spoken words, **`19,756` spoken characters** (`19,767` file characters — `1,244` spoken chars below the `21,000`-character pilot ceiling)
- **ElevenLabs Credits Used:**
  - Live reading before take: `53,221 / 121,114` used (`67,893` remaining)
  - Settled reading after take + Scribe `scribe_v2`: `61,912 / 121,114` used (**`59,202` remaining**; **`8,691` net plan credits billed** at `eleven_v3` 0.5x character rate + Scribe STT; `£0.00` extra spend)
- **Audio Master on Shared Film Store (`studio-live` NAS):**
  - Folder: `ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/02_Voiceover/`
  - `atlantic_black_pit_vo_v01.wav` (`48 kHz` 16-bit stereo PCM, **`1,441.020 s` / `24:01.02`**) — SHA-256 `1fc5fa515ebb28d182476cb381ecb2a7ae820bc91f7379a123e75cbb11190ae9`
  - `atlantic_black_pit_vo_v01.mp3` (`44.1 kHz` `128 kbps`, **`1,441.020 s`**) — SHA-256 `182de6826897a42d19ae64e1868ca8a5bac6a41e3190dee37ab05b76d9200525`

## Measured Chapter Timestamps (`0.700 s` digital silence gap between chapters)

| Chapter | Start (`mm:ss`) | Start (`s`) | End (`s`) | Duration (`s`) | Chars | Loudness (`LUFS` / `mean` / `peak`) |
|---|---|---|---|---|---|---|
| `ch00` — `1 | The gap in the sky` | `00:00` | `0.000` | `223.680` | `223.680` | `2,976` | `-20.8 LUFS` / `-24.1 dB` / `-3.7 dB` |
| `ch01` — `2 | What the submarine needed` | `03:44` | `224.380` | `480.780` | `256.400` | `3,387` | `-19.6 LUFS` / `-22.8 dB` / `-3.5 dB` |
| `ch02` — `3 | A bomber becomes a patrol aircraft` | `08:01` | `481.480` | `746.040` | `264.560` | `3,466` | `-21.1 LUFS` / `-24.3 dB` / `-3.8 dB` |
| `ch03` — `4 | The warning that stopped working` | `12:27` | `746.740` | `986.500` | `239.760` | `3,389` | `-20.2 LUFS` / `-23.5 dB` / `-3.8 dB` |
| `ch04` — `5 | The convoy in the fog` | `16:27` | `987.200` | `1258.640` | `271.440` | `3,810` | `-19.8 LUFS` / `-23.0 dB` / `-3.5 dB` |
| `ch05` — `6 | What closing the gap meant` | `20:59` | `1259.340` | `1441.020` | `181.680` | `2,728` | `-19.7 LUFS` / `-23.0 dB` / `-3.7 dB` |

## Voice Checks

1. **Transcript Match (`scribe_v2` + `faster-whisper` cross-check across all `3,268` spoken words):**
   - `vo_take.py` raw `scribe_v2` verdict: **`PASS` (`97.18%` un-normalized word match)** across `3,232` Scribe word tokens (`136.1 wpm` documentary pace).
   - Zero dropped sentences, zero dropped clauses, zero repeated or stumbled words across all 6 chapters.
   - Normalized word match (UK/US orthography, spaced convoy/service initials `H X`->`HX`, `S C`->`SC`, `O N S`->`ONS`, `R A F`->`RAF`, cardinal numbers, and compound hyphenation `aircrew`/`take-off`/`build-up`): **`99.88%` (`3,241 / 3,245` words)**; the only 4 remaining token differences are benign ASR unstressed consonant/auxiliary transcriptions (`belonged [to]`/`belong [to]`, `trained`/`trains`, `surfaced`/`surface`, `had`/`have`).
   - `faster-whisper` (`vo_check.json`) cross-check confirms every sentence; its 6 nominal word diffs are Whisper abbreviation/homophone spellings confirmed clean in `scribe_v2` (`Number` written `No.` x3, `Leigh Light` written `Lee light`, `twenty-fourth of May, Dönitz` written `24 May, Dernitz`, plus `had`/`have`).
2. **Boundary / Clipped-Words Check (`48 kHz` 20 ms waveform & Scribe boundary audit):**
   - First spoken word (`"In"`) starts at `0.100 s` (`first_20ms_peak = 0.00778`; max start peak across `ch00`–`ch05` is `0.00793`).
   - Last spoken word (`"land."`) ends at `1,440.976 s` inside `1,441.020 s` (`44 ms` tail; `end_20ms_peak = 0.07535`, max end peak across `ch00`–`ch05` is `0.07535`).
   - `0.700 s` digital silence (`gap.wav`) cleanly separates every chapter join (`ch00`–`ch05`). Zero clipped words at any start or end boundary.
3. **Steady Level (`ebur128` + `volumedetect`):**
   - Full concatenated take: **`-20.1 LUFS` integrated**, **`-23.4 dB` mean volume** (inside `-28.0` to `-19.0 dB` target band), **`-3.5 dB` max peak** (well below `-1.0 dB` ceiling).
   - Per-chapter loudness stays within a **`1.5 LU` total spread** (`-21.1` to `-19.6 LUFS`) across all 6 chapters (24.0 minutes).
