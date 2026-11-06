# J2246 / J2288 Specialist Voice Review — HOS 013 Darwin & Wallace Shorts VO (`hos_013_short_A_v02`, `hos_013_short_B_v02`)

- **Review Job:** `J2288` (`HOS 013 Darwin & Wallace: review Shorts VO A and B`, `review_of: J2246`)
- **Reviewed Job:** `J2246` (`HOS 013 Darwin & Wallace: Shorts voiceover (2 v02 Shorts), vo_check, park for Chief`)
- **Film / Stage:** `HOS:013` (`013_Darwin-Wallace-Evolution`) · `vo`
- **Evidence Ref:** HOS PR [#444](https://github.com/TheLaughingGod1986/history-of-science/pull/444) (`e1800ec64c53955e83766c72985501d53ad9406a`, stacked on PR [#432](https://github.com/TheLaughingGod1986/history-of-science/pull/432) `b2ed853`)
- **Reviewer:** `gemini` (`Gemini 4 Argon (High)`, specialist worker lane; direct `audio_input` demonstrated via multimodal `read_file` on both `.wav` and `.mp3` takes and recorded in `chief_relay.py capabilities`)
- **Date:** `2026-11-06T19:25Z`
- **Spend:** **£0.00 / 0 ElevenLabs credits**
- **Verdict:** **KEEP** (`0` sentence pickups, `0` re-recordings; both `hos_013_short_A_v02.wav` and `hos_013_short_B_v02.wav` are clean, natural British narrations ready for the elected Chief `Codex` to record the formal VO lock on `J2246` / HOS PR #444).

> **Role boundary:** `gemini` is a specialist worker, not the elected Chief (`Codex`). This review supplies the complete direct-listening (`audio_input`) and sample-level acoustic verification requested by the acting Chief in `55f0b3c357`; it does **not** declare a VO lock on its own. The locked long `hos_013_vo_v03a` remains untouched.

---

## 1. File Integrity & Demonstrated `audio_input` Verification

Both WAV (`audio/wav`) and MP3 (`audio/mpeg`) files were verified byte-for-byte between the durable Mini media folder (`/Users/benjaminoats/_desk/media/HOS/013_Darwin-Wallace-Evolution/10_Shorts/vo_v02/`) and the worker worktree (`/Users/benjaminoats/_desk/worktrees/J2246-013-shorts-vo/02_Video-Projects/013_Darwin-Wallace-Evolution/10_Shorts/vo_v02/`), and both complete takes were directly auditioned via multimodal `read_file` (`part_0` audio attachments):

| Take | Title | WAV SHA-256 | MP3 SHA-256 | Duration | Loudness / Peak | WPM | `vo_check.py` | Direct Ear Audition (`audio_input`) |
|---|---|---|---|---:|---|---:|---|---|
| `hos_013_short_A_v02` | *How Did Darwin Discover Evolution?* | `9f80fa1c22951b5f7d25b2365fa5d62a58e848898262e6d5365bb2e68047bef8` | `ba46ffaa29dab5ef3dfcc3af7f66c31f3550f90dadcc4e7ed305f643d8c384e1` | `26.64 s` (`1,278,720` frames @ `48 kHz`) | `-20.3 LUFS` / mean `-23.7 dB` / peak `-3.9 dB` | `140` | **PASS** (`0` fails, `0` word diffs, `1` pace warn) | **KEEP (`0` pickups).** Clear British delivery by Ben Orbit Narrator (`eleven_v3`, speed `1.04`); crisp pronunciation of *"Galápagos"*, *"eighteen thirty-five"*, *"John Gould"* (`/ɡuːld/`), *"finches"*, and *"I think."* |
| `hos_013_short_B_v02` | *What Is Survival of the Fittest?* | `6745bd813bd390bdf5091460bd9b5425eca568e4dbb3cf37f2c0a53f70ad47c0` | `9e1eaa2fb9ae2719dd378895820ed7599d8c8532d94f5f39475edf00635c6631` | `26.00 s` (`1,248,000` frames @ `48 kHz`) | `-20.6 LUFS` / mean `-24.0 dB` / peak `-4.0 dB` | `143` | **PASS** (`0` fails, `1` homophone warn at `0:11.42`, `1` pace warn) | **KEEP (`0` pickups).** Clean British narration throughout; *"Alfred Russel Wallace"* (`11.58–12.84 s`) is pronounced naturally (`/ˈælfrɪd ˈrʌsəl ˈwɒlɪs/`) with zero stumble or defect. |

---

## 2. Timestamped Direct-Audition Findings (`audio_input`) & Sample-Level Acoustic Checks

### Short A — `hos_013_short_A_v02.wav` (*How Did Darwin Discover Evolution?*, `60` spoken words, `356` chars)

- **`0.12–2.70 s`:** *"How did Charles Darwin discover evolution?"* — Clean rising-falling British interrogative cadence right from frame 0; UK pronunciation of *"evolution"* (`/ˌiːvəˈluːʃən/` with long initial `/iː/`).
- **`3.46–4.94 s`:** *"Not on a Galápagos beach."* — Follows a natural `0.76 s` hook beat (`2.70–3.46 s`); crisp pronunciation of *"Galápagos"* (`3.92–4.44 s`, `/ɡəˈlæpəɡəs/`) and clean final affricate on *"beach."* (`4.56–4.94 s`).
- **`5.68–13.80 s`:** *"In eighteen thirty-five, he thought the birds there were blackbirds and wrens, and mostly forgot to label which island each came from."* — *"eighteen thirty-five"* (`5.76–6.94 s`) is spoken clearly in full words (Scribe's `"1835"` is digit normalization only); natural `0.44 s` clause breath (`10.22–10.66 s`) after *"wrens,"*; clear articulation across all words.
- **`14.76–20.38 s`:** *"Only back in London did John Gould show him they were all finches, with different beaks."* — Payoff lands at `14.76 s` (clear of the `9.0–14.0 s` on-screen long-title window); *"John Gould"* (`16.40–17.02 s`) is pronounced accurately as `/dʒɒn ɡuːld/`; *"finches"* (`18.30–18.96 s`) and *"beaks."* (`19.88–20.38 s`) are crisp and unclipped.
- **`21.28–26.20 s`:** *"Months later, Darwin drew a branching tree, and wrote: I think."* — Thoughtful `0.66 s` pause (`24.86–25.52 s`) before *"I think."*; *"I"* (`25.52–25.68 s`) and *"think."* (`25.74–26.20 s`) land cleanly.
  - **Ending & tail waveform (`25.74–26.64 s`):** The vowel/nasal of *"think"* runs `25.74–25.99 s` (`-21.7` to `-40.7 dBFS`), the velar closure is `26.00–26.08 s` (`-50.7` to `-72.2 dBFS`), and the full `/k/` release burst lands at `26.09–26.20 s` (peak `-23.5 dBFS` at `26.09–26.10 s`, decaying to `-79.1 dBFS` digital floor by `26.24 s`).
  - **Assembly note (`26.24–26.64 s`):** `26.24–26.62 s` (`380 ms`) is pure `-75` to `-87 dBFS` silence, followed by a `20 ms` `eleven_v3` buffer-end tick at `26.62–26.64 s` (`-31.8 dBFS` RMS / `-22.1 dBFS` peak). During Short A assembly, fade or trim the VO stem at `26.24–26.40 s` (`afade=t=out:st=26.20:d=0.05`) and hold the final video export to **`26.50–26.80 s`** (giving `0.30–0.60 s` of picture/music breath after the `/k/` release at `26.20 s` while staying strictly inside the `22.0–27.0 s` Short gate and removing the `26.62 s` buffer tick).

### Short B — `hos_013_short_B_v02.wav` (*What Is Survival of the Fittest?*, `61` spoken words, `339` chars)

- **`0.12–2.50 s`:** *"What is survival of the fittest?"* — Clean, engaging British question delivery from frame 0.
- **`3.26–6.04 s`:** *"Charles Darwin didn't even coin the famous phrase."* — Natural `0.76 s` pause after the hook question (`2.50–3.26 s`), clear stress on *"didn't even coin"*.
- **`6.66–10.74 s`:** *"The writer Herbert Spencer came up with it in eighteen sixty-four,"* — *"Herbert Spencer"* (`7.24–8.22 s`) and *"eighteen sixty-four"* (`9.58–10.74 s`) are spoken clearly in full words (Scribe's `"1864"` is digit normalization only).
- **`11.32–16.60 s` (Specific `11.42 s` check):** *"and Alfred Russel Wallace persuaded Darwin to add it to his book years later."*
  - Word-level timings: *"and"* (`11.32–11.42 s`), *"Alfred"* (`11.58–11.90 s`), *"Russel"* (`12.00–12.32 s`), *"Wallace"* (`12.42–12.84 s`), *"persuaded"* (`12.92–13.34 s`), *"Darwin"* (`13.46–13.90 s`).
  - **Direct `audio_input` verdict on `0:11.42`:** Listening directly to the WAV and MP3 confirms *"Alfred Russel Wallace"* is spoken smoothly and naturally as `/ˈælfrɪd ˈrʌsəl ˈwɒlɪs/` with zero stumble, click, or phonetic flaw. The `vo_check.py` (`faster-whisper small.en`) sounds-alike warning (`script 'russel' / heard 'russell'`) is purely an orthographic difference between Wallace's historical single-`l` middle name (`Russel`) and Whisper's standard double-`l` spelling (`Russell`), which are exact English homophones (`/ˈrʌsəl/`). **No pickup is required.**
- **`17.62–20.54 s`:** *"And fittest never meant the strongest animal."* — Payoff lands at `17.62 s` (well past `15.0 s` and clear of the `9.0–14.0 s` on-screen long-title window); clean emphasis on *"fittest"* (`17.88–18.44 s`) and *"strongest animal"* (`19.60–20.54 s`).
- **`21.12–25.95 s`:** *"It means the one that fits its world best, like a key in a lock."* — Clean `0.46 s` pause (`23.78–24.24 s`) after *"best,"*, followed by *"like a key in a lock."* (`24.24–25.95 s`).
  - **Ending & tail waveform (`25.58–26.00 s`):** On *"lock"*, the vowel peaks at `25.61–25.64 s` (`-17.2 dBFS` RMS / `-9.6 dBFS` peak), the velar closure sits at `25.75–25.87 s` (`-41.0` to `-68.8 dBFS`), and the unclipped `/k/` release burst lands cleanly at `25.88–25.94 s` (`-41.0 dBFS` RMS / `-30.2 dBFS` peak), decaying to `-47.6` to `-56.0 dBFS` through `26.00 s`.
  - **Assembly note:** Apply `afade=t=out:st=25.95:d=0.05` on the VO stem and add a `0.40–0.60 s` picture/music tail for a **`26.40–26.60 s`** Short B export (well inside `22.0–27.0 s`).

---

## 3. Summary & Next Step for Elected Chief (`Codex`)

- **Ruling (`J2288`):** **KEEP** both `hos_013_short_A_v02.wav` (`9f80fa1c…`) and `hos_013_short_B_v02.wav` (`6745bd81…`) with **`0` pickups** and **£0 / 0 credit spend**.
- **Next step:** Elected Chief (`Codex`) can now record the formal VO lock on `J2246` / HOS PR #444 (stacked on PR #432) and close verification `J2294`.

---

## Prior Acting-Chief Review Record (`55f0b3c357`, 6 November 2026)

Reviewer: codex, elected acting Chief; authority checked before ruling.

### Ruling: FIX — incomplete listening evidence; retain both takes

This is not a rejection of the recordings and not a VO lock. J2246 stays held. No regeneration, script change, picture spend or publishing is authorised by this review. The locked long hos_013_vo_v03a is untouched.

Reviewed original brief, result and complete history; HOS PR #444 at e1800ec64c53955e83766c72985501d53ad9406a, stacked on open script/package PR #432; J2240 and existing follow-up J2288. Do not merge the stacked package as a voice approval.
