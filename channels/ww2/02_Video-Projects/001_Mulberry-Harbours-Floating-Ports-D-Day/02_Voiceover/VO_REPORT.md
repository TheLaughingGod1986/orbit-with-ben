# WW2:001 Voiceover Report (`J2992` — `mulberry_harbours_vo_v01`)

- **Film:** `WW2:001` — *How Britain Built Two Harbours in Secret and Floated Them to Normandy* (Launch Plan alt: *How Britain Towed Two Floating Ports Across the Channel for D-Day*)
- **Voice & Model:** `Ben Orbit Narrator` (`eleven_v3`, speed `1.04`, API via `04_Audio/tools/vo_take.py` under `desk-lock elevenlabs`)
- **Spoken Script (`J2991` / PR #996):** `6` chapters, `3,358` spoken words, **`20,431` spoken characters** (`569` below the `21,000`-character pilot ceiling)
- **ElevenLabs Credits Used:**
  - Before take: `43,725 / 121,114` used (`77,389` remaining)
  - Settled after take + Scribe `scribe_v2`: `53,221 / 121,114` used (**`67,893` remaining**; **`9,496` net plan credits billed** at `eleven_v3` 0.5x character rate + Scribe STT; `£0.00` extra spend)
- **Audio Master on Shared Film Store (`studio-live` NAS):**
  - Folder: `ww2/02_Video-Projects/001_Mulberry-Harbours-Floating-Ports-D-Day/02_Voiceover/`
  - `mulberry_harbours_vo_v01.wav` (`48 kHz` 16-bit stereo PCM, **`1,656.700 s` / `27:36.70`**) — SHA-256 `97d7973fc50ab019ccd7cb57f2679ff5fb212d2b2cdc3e10ff1c5f17f4860d9d`
  - `mulberry_harbours_vo_v01.mp3` (`44.1 kHz` `128 kbps`, **`1,656.700 s`**) — SHA-256 `1934c1e9e23841797c9fec5d870883944433db49793013f2ca47598e27304fef`

## Voice Checks

1. **Transcript Match (`scribe_v2` word-level audit across all `3,358` spoken words):**
   - Zero dropped sentences, zero dropped clauses, zero repeated phrases across all 6 chapters (`3,498` Scribe word tokens).
   - Normalized word match (UK/US orthography + cardinal numbers normalized): **`97.56%`** (`3,119 / 3,197` non-numeric words; **`99.88%`** after accounting for `vo_take.py` em-dash joins like `sand—but` -> `sand, but`, compound hyphenation like `pier-heads` / `deepwater`, and British spoken dates like `7 June` -> `the seventh of June`). Raw `vo_take.py` un-normalized string match (`93.46%`) reflects UK/US spelling (`harbours`/`harbors`, `storeys`/`stories`, `mobilised`/`mobilized`), digits vs spoken numbers, and em-dash punctuation joins only.
2. **Boundary / Clipped-Words Check (`48 kHz` 20 ms waveform & Scribe boundary audit):**
   - First spoken word (`"At"`) starts at `0.160 s` (`first_20ms_peak <= 0.0186` across `ch00`–`ch05`); last spoken word (`"them."`) ends at `1,656.608 s` inside `1,656.700 s` (`92 ms` clean decay tail).
   - `0.700 s` digital silence (`gap.wav`) cleanly separates every chapter join. Zero clipped words at any start or end boundary.
3. **Steady Level (`ebur128` + `volumedetect`):**
   - Full concatenated take: **`-19.7 LUFS` integrated**, **`-22.9 dB` mean volume** (inside `-28.0` to `-19.0 dB` target band), **`-3.4 dB` max peak** (below `-1.0 dB` ceiling).
   - Per-chapter loudness (`1.1 LU` total spread across 27.6 minutes):
     - `ch00` (*Cold Open*, `3,611` chars, `308.24 s`): `-20.1 LUFS` / `-23.4 dB` mean / `-3.6 dB` peak
     - `ch01` (*They Must Float Up and Down with the Tide*, `3,628` chars, `278.80 s`): `-19.1 LUFS` / `-22.3 dB` mean / `-3.4 dB` peak
     - `ch02` (*Secret Concrete Giants in the Thames*, `3,020` chars, `248.40 s`): `-19.9 LUFS` / `-23.0 dB` mean / `-3.8 dB` peak
     - `ch03` (*The Four-Knot Armada*, `3,165` chars, `278.80 s`): `-20.2 LUFS` / `-23.4 dB` mean / `-3.9 dB` peak
     - `ch04` (*The Worst June Gale in Forty Years*, `3,343` chars, `249.44 s`): `-20.1 LUFS` / `-23.1 dB` mean / `-3.7 dB` peak
     - `ch05` (*Fuel Under the Sea and the Tonnage Verdict*, `3,664` chars, `289.52 s`): `-19.3 LUFS` / `-22.3 dB` mean / `-3.4 dB` peak
