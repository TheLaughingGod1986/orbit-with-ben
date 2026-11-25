# J3021 Elected Acting-Chief Ruling: PASS & Exact-Hash Narration Lock — `OWB:064` (`every_planet_explained_vo_v01`)

- **Date / time:** `2026-11-25T14:12Z`
- **Elected acting Chief:** `gemini` (`chief_relay.py status` re-verified `Chief: Gemini` before ruling; `claude` down until `2026-11-25T17:50:00Z`, `codex` down until `2026-11-25T14:49:49Z`)
- **Film / jobs:** `OWB:064` (*Every Planet Explained in 10 Minutes (Mercury to Neptune)*) — Build Package 2 `J3021` (`after: J3020`), releasing Build Package 3 `J3022` (`after: J3021`)
- **Locked script source (`J3711`):** `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/every_planet_explained_script_master_v04.md` (SHA-256 `556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8`)

## Verdict: **PASS — EXACT-HASH NARRATION LOCK GRANTED ON `every_planet_explained_vo_v01`**

`OWB:064` narration take `every_planet_explained_vo_v01` is **LOCKED (PASS)** by the elected acting Chief on tool measurements and `scribe_v2` ASR evidence. Actual human listening remains reserved for Ben's final finished-cut UAT watch under the 4 November 2026 standing rule (`AGENTS.md`); no direct audio hearing is claimed from ASR or waveforms.

| Artefact | Location | Exact SHA-256 |
|---|---|---|
| Master WAV narration stem (`683.86 s`, 48 kHz stereo PCM) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/every_planet_explained_vo_v01.wav` | `4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa` |
| Master MP3 narration stem (`128 kbps`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/every_planet_explained_vo_v01.mp3` | `cdf06f5a69a2d340e6ac2a46137119085a1cb19a99bbd06797257def828a3157` |
| Take manifest (`vo_take.py`) | `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/every_planet_explained_vo_v01_TAKE.json` | Recorded in git + `studio-live` |
| Scribe `scribe_v2` word timestamps (`stt_raw.json`) | `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/stt/every_planet_explained_vo_v01/stt_raw.json` | Recorded in `J3021_VO_CHECKS_v01.json` |
| Captions (`words.srt`) | `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/stt/every_planet_explained_vo_v01/words.srt` | Recorded in `J3021_VO_CHECKS_v01.json` |
| Machine verification bundle & full mismatch review | `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/J3021_VO_CHECKS_v01.json` & `J3021_VO_REVIEW_v01.md` | Recorded in git + `studio-live` |

## Acting-Chief Verification & Ruling Basis

1. **Voice, model, and API compliance (`PASS`):** Recorded in a single clean pass via `04_Audio/tools/vo_take.py` under `desk-lock elevenlabs`, using locked **Ben Orbit Narrator** (`kDch6ACCIpqgQ0NsU9kk`), `eleven_v3`, speed `1.04`, dry-run first (`8` chapters, `8,481` spoken chars, `1,341` whitespace words, `0.7 s` inter-chapter gaps), followed by `scribe_v2` word-level transcription. Zero ElevenLabs website use; zero retakes needed.
2. **Word-for-word Scribe `scribe_v2` audit (`PASS` — ruling on raw `REVIEW` 89.45%):** All **63** raw mismatch runs in `every_planet_explained_vo_v01_TAKE.json` were individually inspected and tabulated in `J3021_VO_REVIEW_v01.md`:
   - `20` UK/US spelling or possessive orthography differences (`kilometres`/`kilometers`, `metres`/`meters`, `per cent`/`percent`, `mars's`/`mars'`).
   - `9` standard British spoken ordinal date readings (`1 March` → `the 1st of March`, `10 June` → `the 10th of June`, `18 January` → `the 18th of January`, `7 December` → `the 7th of December`, `13 March` → `the 13th of March`, `24 January` → `the 24th of January`, `23 September` → `the 23rd of September`, `10 October` → `the 10th of October`, `25 August` → `the 25th of August`), natural for British Ben Orbit Narrator reading `D Month YYYY`.
   - `34` spelled-out numbers/decimals transcribed as digits by Scribe (`forty-one thousand` → `41,000`, `ninety-seven point seven seven` → `97.77`, `minus two hundred and twenty-four point two` → `-224.2`, `eighty per cent` → `80%`, etc.).
   - **True wording discrepancies:** `0` (`100.0%` semantic/spoken match across all `1,374` normalized script tokens).
   - **Repetitions / stutters:** `0` (`1-gram`, `2-gram`, `3-gram` checks clean).
3. **Loudness, true peak, and chapter consistency (`PASS`):**
   - Integrated loudness: **`-20.21 LUFS`** (within `-19` to `-21 LUFS` target), true peak **`-3.64 dBTP`** (well under `-1.0 dBTP`), mean **`-23.4 dB`**, max **`-3.6 dB`**, LRA **`4.20 LU`**.
   - Per-chapter integrated loudness across all 8 chapters (`ch00`–`ch07`): `-20.7` to `-19.6 LUFS` (**`1.1 LU`** spread — highly consistent).
4. **Chapter boundaries and opening/beat timings (`PASS`):**
   - Every chapter starts on its exact first locked word at `0.08–0.16 s` lead-in (`first_50ms_rms` `-34.03` to `-91.26 dBFS`) and ends on its exact final locked word with `0.04–0.78 s` natural tail (`last_50ms_rms` `-28.67` to `-58.70 dBFS`) ahead of the `0.70 s` inter-chapter silence gap. Zero clipped starts or truncated endings detected.
   - **First-30-second hook & opening lock (`J2428` / `studio/RULES.md`):** Sentence 1 ends at **`6.52 s`** (`< 8.0 s`); Sentence 2 immediate concrete answer (`"The ice hides in polar craters that never see sunlight."`) finishes at **`10.98 s`** (`< 0:20`); Sentence 3 (`-180 °C` contrast) finishes at **`25.04 s`** (`< 0:30`); Chapter 2 (`Venus`) starts at **`82.06 s`** (`> 0:45`).
   - **Mid-film subscribe beat:** `245.18–251.20 s` (**`35.9%`** of VO duration, verbatim locked line).
5. **Measured runtime note (`11:23.86` pure VO vs `~10 min` concept-sheet estimate):** At locked speed `1.04`, the `1,341`-word locked `v04` script reads naturally at `117.7 wpm` (`683.86 s` / `11:23.86`, plus `15–20 s` end hold ≈ `11:40` finished cut). Chief accepts this measured natural runtime with **zero `atempo` speedup** (keeping the natural cadence and respecting all channel audio rules; `J3022`/`J3023` use the exact Scribe word timestamps).
6. **Budget & zero-overage compliance (`PASS`):**
   - Live ElevenLabs subscription before take: `109,171 / 121,114` (`11,943` remaining, `can_extend_character_limit: false`, `allowed_to_extend_character_limit: false`, resets `2026-11-30T10:50:31Z`).
   - Settled live balance after take + Scribe: `113,111 / 121,114` (**`8,003` remaining**; **`3,940` net plan credits billed**, leaving **`5,003` credits above the `3,000` HOS fixes reserve**). `£0.00` cash, `0` Flow/Vertex credits, no top-up or plan change.

## Downstream Handoff (`J3022`)

- `OWB:064` `vo` stage is marked `done` in `status.json`; `J3021` closes and releases `J3022` (`after: J3021`, Build Package 3: shelf picture, per-row Python code graphics, and 3 thumbnails — `£0`, zero Flow/Vertex generation).
- Use the locked `studio-live` narration stem `every_planet_explained_vo_v01.wav` (`SHA-256 4b478fcd...`) and exact Scribe word timestamps in `stt/every_planet_explained_vo_v01/stt_raw.json` / `words.srt`.
- Actual listening verification remains Ben's final finished-cut UAT watch (deadline **Fri 11 Dec 2026 18:00 London** for planned air slot **Wed 16 Dec 2026 18:00 London**).
