# J1093 QA Verification (for J1090 v07) — 28 October 2026

- **Worker:** `gemini` (`Gemini 4 Argon (High)` via existing subscription `agy` CLI route)
- **Follow-up of:** `J1090` (`ref: c370f1058`, branch `codex/J1090`)
- **Task keys:** `OWB:025`
- **Role / Authority:** Specialist QA worker handoff for elected-Chief review. Not an elected-Chief final PASS. `J1090` and `J1084` remain held pending Chief acceptance; `J1059` remains held for Ben's watch (deadline 11 Nov 10:30 London); scheduled `TtgHNLXfDSs` (`v02`, 11 Nov 11:30 UTC) is untouched. Zero credit spend, TTS, speech rewrite, upload, swap, scheduling, privacy change, or NAS deletion.

---

## 1. Direct Audio Capability Check & Full Audition

### Capability & Ingestion Method
- **Route:** Existing subscription `agy` multimodal `read_file` tool (`Gemini 4 Argon (High)`).
- **Capability:** **SUPPORTED.** Native binary `audio/wav`, `audio/mpeg`, and `video/mp4` (audio stream + video frames) were ingested directly into model perception without paid API calls, external ASR substitution, or unperceived local playback.

### Media Ingested & Verified SHA256 Hashes
| File | MIME | Bytes | SHA256 |
|---|---|---:|---|
| `wed11_opening_testA_v07.mp4` | `video/mp4` | `25,238,529` | `e9f848d99db9f8e73eb70aee635ee3dcd9d4a50bdda906a54a74c10e83d12e83` |
| `wed11_opening_testA_v07_PHONE.mp4` | `video/mp4` | `9,022,873` | `ce9d0befcdef2493fba49230b0ae9ae9e4cc4c5423de5b59ae4c1f8572eb4857` |
| `stem_vo.wav` (`v06` & `v07` identical) | `audio/wav` | `4,998,188` | `c2d824f06a070bd9edad46d4e0cb7d4879716e4a0a14111b0d9f7817be33a171` |
| `mix.wav` (`v07` mixed master WAV) | `audio/wav` | `4,998,222` | `3de3a8920540cb0235bb6aaf55182660afbc2af5bb6d06662e150e230ad1e297` |
| `long.wav` (locked 025 long VO source) | `audio/wav` | `93,461,838` | `a81c6088a04c7c4d862c63aa352aa6abbacc8eb13de3d06fb77321139ae4f871` |
| `opp.wav` (locked Mon 09 Short VO source) | `audio/wav` | `4,785,294` | `1087432444a60c9a505e28e8e3f5608f3cd2e91f5397d5831708b4cd37b6686f` |

### Explicit Resolution: Source `"for more"` vs Whisper `"from more"`
- **Source provenance:** Segment `00` (`0.000s–5.220s` in `stem_vo.wav` and `wed11_opening_testA_v07.mp4`) is a single contiguous, unedited slice (`0.08s–5.30s`) from the locked long voiceover (`long.wav`), gain-matched (`~0.95x`) with **zero internal splice**.
- **Word timestamps in `02_Voiceover/words.json` (`long.wav`) vs rendered master (`v07`):**
  - `kept`: `3.10s–3.26s` (source) / `2.94s–3.10s` (master)
  - `going`: `3.30s–3.62s` (source) / `3.10s–3.42s` (master)
  - `for`: `3.68s–3.76s` (source, 80 ms weak form) / `3.42s–3.64s` (master)
  - `more`: `3.80s–3.92s` (source) / `3.64s–3.84s` (master)
  - `than`: `3.96s–4.14s` (source) / `3.84s–3.94s` (master)
  - `14`: `4.20s–4.70s` (source) / `3.94s–4.44s` (master; mark at `4.12s`)
  - `years`: `4.80s–5.24s` (source) / `4.44s–5.16s` (master; reveal ends at `5.16s`)
- **Audible finding:** Direct side-by-side listening to `long.wav` (`0.00s–6.00s` and `2.80s–5.30s`), `stem_vo.wav`, and `wed11_opening_testA_v07.mp4` confirms that Ben speaks the natural British unstressed weak-form preposition **"for"** (`/fə/`) linking directly from *"going"* (`/ˈɡəʊɪŋ/`) into the bilabial nasal onset `/m/` of *"more"* (`/fə mɔː/`). Because the rapid (~80 ms) schwa `/ə/` coarticulates immediately into `/m/`, the acoustic transition `/fə m/` resembles `/frəm m/`, causing `faster-whisper` to tokenize `"from more"`. Audibly in sentence context, the line is identical to the locked long opening, free of any splice, clip, or stumble, and reads naturally as *"A robot built to last ninety days on Mars kept going for more than fourteen years."*

### Full Audition of Opening, Segments, and All 9 Joins (`0.000s–26.033s`)
1. **Seg 00 (`0.000s–5.220s`, `long.wav 0.08–5.30s`):** *"A robot built to last ninety days on Mars kept going for more than fourteen years."*
   - Clean VO onset at `0.04s`; *"Mars"* at `2.22s`; surprise number *"fourteen"* at `4.12s` and *"years"* finishing cleanly at `5.16s` (accepted `5.16s` reveal preserved).
2. **Join `00 -> 01` (`5.220s–5.288s`, `0.08s` room-tone gap, `12 ms` xfade, `long.wav -> opp.wav 7.12–10.44s`):**
   - `...fourteen years. | Dust should have choked its solar panels within months.`
   - Seamless loudness and vocal timbre match between gain-matched `long.wav` and `opp.wav`; natural sentence breath; zero click, pop, or room-tone jump.
3. **Join `01 -> 02` (`8.596s–8.644s`, `0.06s` room-tone gap, `12 ms` xfade, `opp.wav 7.12–10.44s -> opp.wav 11.74–14.48s`):**
   - `...within months. | Martian wind kept sweeping them clean.`
   - Clean excision of *"Instead,"*; *"Martian"* enters cleanly at `8.74s` and *"wind"* at `9.224s` through *"clean"* ending at `11.304s` (accepted `9.224s–11.304s` wind window preserved, landing after the `9.0s` title banner onset).
4. **Join `02 -> 03` (`11.372s–11.600s`, `0.24s` room-tone gap, `12 ms` xfade, `opp.wav -> long.wav 263.68–265.70s`):**
   - `...sweeping them clean. | The team called them cleaning events.`
   - Smooth transition back to gain-matched `long.wav`; *"events"* lands at `13.02s`; no audible seam.
5. **Join `03 -> 04` (`13.608s–13.756s`, `0.16s` room-tone gap, `12 ms` xfade, `long.wav 263.68–265.70s -> long.wav 266.04–269.42s`):**
   - `...cleaning events. | Each one gave the rover back its power, and it kept driving.`
   - Natural inter-sentence cadence; *"driving"* completes cleanly at `17.056s`.
6. **Join `04 -> 05` (`17.124s–17.332s`, `0.22s` room-tone gap, `12 ms` xfade, `long.wav 266.04–269.42s -> long.wav 269.96–271.74s`):**
   - `...kept driving. | Ninety days became years.`
   - Clean pause; *"Ninety"* at `17.372s`; *"years"* finishes cleanly before `19.100s` with zero bleed from the following word in `long.wav`.
7. **Joins `05 -> 06 -> 07 -> 08 -> 09` (`19.100s–24.924s`, `long.wav -> opp.wav 14.82–15.16s, 15.46–16.64s, 16.96–19.40s, 19.70–21.30s`):**
   - `...became years. | Then, | in 2018, | a storm wrapped the whole planet | and the sky went dark.`
   - Smooth handoff from `long.wav` to `opp.wav` on *"Then, in 2018"* (`20.024s`, past 70% payoff mark `18.22s`). The tightened intra-sentence micro-gaps (`0.04s`, `0.04s`, `0.06s` with `12 ms` xfades) sound completely natural with no clipped plosives or fricatives. Final word *"dark"* ends cleanly at `24.896s`, followed by `1.136s` of score bed and loop tail to `26.033s`.
8. **Score Bed & SFX Mix in Master (`wed11_opening_testA_v07.mp4` & `PHONE.mp4`):**
   - Continuous music bed (`mars-robot_score_bed_v02_full.mp3` from `80.0s`) and restrained SFX (`whoosh_soft` at `2.50s` first cut, `rumble_low` at `20.00s` storm beat) sit cleanly under the voiceover (`-14.4 LUFS` integrated, `-2.0 dBTP` true peak) without masking speech.

---

## 2. Visual QA: Final-Shot Motion, Transitions, Warnings & Caption/Title Safety

### Complete Final-Shot Motion & Transitions (`s06 -> s07 -> s_loop`, `21.40s–26.033s`)
- **Inspected via `read_file`:** Full `wed11_opening_testA_v07.mp4` video stream, isolated segment clips `/private/tmp/j1090_wed11_v07/s07.mp4` (`21.814s–25.032s`) and `/private/tmp/j1090_wed11_v07/s_loop.mp4` (`25.032s–26.033s`), a 28-tile 6 fps contact sheet spanning `21.40s–26.03s`, and full-size 1080×1920 frames at `21.80s`, `21.85s`, `21.90s`, `22.50s`, `23.40s`, `24.80s`, `25.00s`, `25.05s`, and `26.00s`.
- **Findings:**
  - **`s06 -> s07` transition (`21.814s`):** Clean hard cut from the M2020 descent aerial view (`s06`) to the Gale Crater panorama (`s07`, `JPL-20200303-MSLf-0001.mp4` from source `9.0s`, `crop=608:1080:200:0`, upscale `1.78x`).
  - **Full `s07` motion (`21.814s–25.032s`, 97 frames):** Continuous, smooth rightward pan across neutral Martian bedrock, dark sand flats, and distant Gale Crater rim mountains. **Zero MSL Curiosity deck/hardware, zero black wedge/corner, and zero source text appear anywhere across the entire shot.**
  - **`s07 -> s_loop` transition (`25.032s`) and tail (`25.032s–26.033s`):** Clean cut after *"went dark"* (`24.896s`) to the 1.00s caption-free loop tail (`end_card_loop_JPL-20200303-MSLf-0001.mp4` at source `72.0s`), matching `s00` (`frame 0`) for a seamless Short loop (`loop_diff_masked = 10.17`).

### Full-Size Review of All Three Picture QA Warnings (`7.3s`, `13.8s`, `20.2s`)
- **`0:07.3` (`s02`, `5.719s–8.938s`, `JPL-20210222-M2020f-0001.mp4 @ 96.0s`, `2.18x` upscale, also `polish_gate` low-detail WARN):** Full-size `1080×1920` inspection confirms authentic NASA M2020 descent aerial footage over fine Martian sand ripples and a curved ridge. The low luma standard deviation (`16.41 < 18.0`) and edge density (`0.0113 < 0.0119`) reflect genuine monochrome dusty Martian terrain under *"Dust should have choked its solar panels within months"*, with smooth downward/diagonal aerial motion and no compression artifacts.
- **`0:13.8` (`s04`, `12.157s–15.376s`, `JPL-20210222-M2020f-0001.mp4 @ 124.0s`, `2.18x` upscale):** Full-size `1080×1920` inspection shows clear aeolian sand ripples and cratered terrain during descent under *"The team called them cleaning events / Each one gave"*. Upscale (`2.18x`) is within the `≤2.35x` house limit and reads cleanly on phone and desktop.
- **`0:20.2` (`s06`, `18.595s–21.814s`, `JPL-20210222-M2020f-0001.mp4 @ 154.0s`, `2.18x` upscale):** Full-size `1080×1920` inspection shows higher-relief rocky outcrops and wind-swept dunes at lower altitude during descent under *"Then in 2018 / a storm wrapped"*. Crisp motion, no banding or blockiness.

### Full-Runtime Contact Sheet & Caption/Title Safety
- **Full-runtime sheet (`wed11_opening_testA_v07_2fps.jpg`, 9×6 grid = 54 frames covering `0.0s–26.03s`) & `wed11_opening_testA_v07_open_sheet.jpg`:**
  - **Frame 0 & `0.0s–2.0s` hook:** `14` (yellow `#FFD400`) / `YEARS` (white) with 8 px black stroke at `y = 5%` (`96 px`), centred, high-contrast over moving neutral Martian bedrock (`s00`), zero Orbit on screen.
  - **Mid-Short long-title overlay (`9.0s–14.0s`):** Two-line title `Could a Robot / Survive on Mars?` (white Arial Black, 5 px black stroke, `y = 8%`) sits cleanly in the upper band across `s03` and `s04` and never overlaps the bottom captions.
  - **Bottom captions (`0.04s–25.03s`, 25 cards):** Placed at `y = 78%` (`1497 px`), max width `72%` (`777 px`), 6 px black stroke. Every card is fully legible, within horizontal/vertical safe margins, and clears at `25.032s` for the clean `1.00s` loop tail.
  - **Preserved versions & timings:** Accepted `5.16s` reveal (`years_end`), `9.224s–11.304s` wind window, and all prior exports (`v01`–`v07`) remain intact.

---

## 3. Readable SHA256 Verification Across Local, NAS, and iCloud OWB UAT

### Root Cause of Earlier UAT `Errno 11` & Remediation
- Prior to remediation, `ls -la` on `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/025_wed11_opening_testA_v07` showed `total 17624` blocks (~9 MB): only `wed11_opening_testA_v07_PHONE.mp4` was locally resident on disk, while the master and 7 support files had been marked dataless by iCloud Drive (`bird`), causing non-hydrating reads to fail with `[Errno 11] Resource deadlock avoided`.
- Each affected file in `OWB UAT/025_wed11_opening_testA_v07` (plus `sha256_manifest_v07.json`) was unlinked and freshly written (`shutil.copyfile`) from the verified local original in `06_Final-Exports` (preserving all local and NAS originals untouched, zero NAS deletion).
- Post-copy `ls -la` confirms `total 67808` blocks (~34.7 MB fully resident on disk in `OWB UAT/025_wed11_opening_testA_v07`). An independent read-back pass opened and streamed every byte of all 9 manifest entries + `sha256_manifest_v07.json` across all three storage locations.

### Verified Readable Hashes (`27/27` Manifest Entries + `3/3` Manifests Match)
| File | Bytes | SHA256 | Local | NAS (`youtube-staging/025/wed11_opening_testA_v07`) | iCloud (`OWB UAT/025_wed11_opening_testA_v07`) |
|---|---:|---|---|---|---|
| `wed11_opening_testA_v07.mp4` | `25,238,529` | `e9f848d99db9f8e73eb70aee635ee3dcd9d4a50bdda906a54a74c10e83d12e83` | PASS (`49296` blk) | PASS (`49296` blk) | PASS (`49296` blk) |
| `wed11_opening_testA_v07_PHONE.mp4` | `9,022,873` | `ce9d0befcdef2493fba49230b0ae9ae9e4cc4c5423de5b59ae4c1f8572eb4857` | PASS (`17624` blk) | PASS (`17624` blk) | PASS (`17624` blk) |
| `wed11_opening_testA_v07_PHONE.jpg` | `89,731` | `d005b4988151032b1cd8f621583f481298f0ab800f899461fb64868095a513ea` | PASS (`176` blk) | PASS (`176` blk) | PASS (`176` blk) |
| `wed11_opening_testA_v07_2fps.jpg` | `213,382` | `94546c49baa797471121f4fe246b82b58b71d973415ab7eb8fba120370a1d89f` | PASS (`424` blk) | PASS (`424` blk) | PASS (`424` blk) |
| `wed11_opening_testA_v07_open_sheet.jpg` | `65,320` | `6b413a5c69e7b0c9775032e4d8f3cd62827cb317c6a800b756c58f5dee1b0769` | PASS (`128` blk) | PASS (`128` blk) | PASS (`128` blk) |
| `wed11_opening_testA_v07_meta.json` | `2,976` | `11cd6ec405d06468ca0969d203f9c3c23f7297b37b942f5b900a7c8a4b7f8473` | PASS (`8` blk) | PASS (`8` blk) | PASS (`8` blk) |
| `wed11_opening_testA_v07_whisper.json` | `16,251` | `e911e1f6dd0562f6cf99eb1ef1f502dab189e47f7246e06e657fdadb837ef894` | PASS (`32` blk) | PASS (`32` blk) | PASS (`32` blk) |
| `wed11_opening_testA_v07_whisper.txt` | `2,913` | `a72bc354f5927745814d822509761bf70e4fb38f0f6b654a0df9a3006c5294df` | PASS (`8` blk) | PASS (`8` blk) | PASS (`8` blk) |
| `wed11_opening_testA_v07_checks.json` | `51,494` | `882be9f6872628a1697e1b86028f994ee713e980cb44deb54a33c39c1c2280e7` | PASS (`104` blk) | PASS (`104` blk) | PASS (`104` blk) |
| `sha256_manifest_v07.json` | `1,589` | `6e5ef24cb556d02f950f4d8e5f9ebfb3568173276b9f05f061547c7b1e396327` | PASS (`8` blk) | PASS (`8` blk) | PASS (`8` blk) |
