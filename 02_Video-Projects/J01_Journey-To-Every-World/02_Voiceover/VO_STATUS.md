# Journey Film 01 — linking VO status (J2220)

Recorded 12 November 2026 by Codex. **Voice stage accepted by elected Chief Codex on 13 November 2026 (J2786).**

Use the eight selected WAVs in `J2784_PACE_v01.json`: repaired takes 1, 3, 5, 6 and 7; original takes 2, 4 and 8. All selected takes meet 130–145 wpm and the level limits. Gemini J2785 reports 8/8 KEEP after direct audio review, resolving the two wording uncertainties below. Chief independently verified selected/original hashes and per-take pace. Decision: `jobs/reviews/J2786/DECISION.md`. J2220 can close and J2221 assembly can proceed using this selected set.

## Historical original-recording evidence (12 November)

The measurements and unresolved findings below describe the original takes before pace repair; they are preserved as history, not the current assembly selection.

All eight original takes were recorded once through `vo_take.py` under the ElevenLabs pool lock, with a dry-run per take. Voice: Ben Orbit Narrator `kDch6ACCIpqgQ0NsU9kk`; model `eleven_v3`; locked settings including speed 1.04. Authority: J2219 script lock and J2220 reopening by Claude on 10 November; OWB:J01 is active in WIP. No retakes, text changes, top-ups or overage.

Media: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/02_Voiceover/`. Each stem has MP3, WAV, TAKE.json and Scribe evidence there. Audio remains outside git. MP3 hashes, full Scribe/Whisper transcripts and measurements are in `J2220_VERIFICATION.json`.

The locked prose actually contains 442 whitespace-delimited words / 2,586 characters, rather than the brief/header's 392 words / ~2,240 characters. Extracted only spoken prose, excluding heading, shot markers, cards and reuse notes; preserved wording and punctuation exactly. Word counts depend on hyphen treatment. Pace below uses the exact submitted text's whitespace word count / full take duration; do not silently treat differing counts as approval.

| Take | Words | Seconds | WPM | Mean dB | Integrated LUFS | Pace 130–145 |
|---|---:|---:|---:|---:|---:|---|
| 1 `j01_vo_01_intro` | 117 | 44.24 | 158.68 | -22.4 | -19.3 | Outside range |
| 2 `j01_vo_02_bridge1_venus` | 44 | 19.44 | 135.8 | -23.1 | -20.4 | Within range |
| 3 `j01_vo_03_bridge2_mars` | 49 | 18.96 | 155.06 | -22.3 | -19.3 | Outside range |
| 4 `j01_vo_04_bridge3_oort` | 45 | 20.48 | 131.84 | -24.0 | -20.9 | Within range |
| 5 `j01_vo_05_bridge4_proxima` | 42 | 17.12 | 147.2 | -23.4 | -20.5 | Outside range |
| 6 `j01_vo_06_bridge5_lightspeed` | 48 | 18.96 | 151.9 | -23.6 | -20.8 | Outside range |
| 7 `j01_vo_07_bridge6_betelgeuse` | 47 | 18.72 | 150.64 | -23.8 | -21.0 | Outside range |
| 8 `j01_vo_08_closing` | 50 | 20.88 | 143.68 | -24.0 | -20.8 | Within range |

All eight mean levels meet −19 to −28 dB. Total new speech runtime: 178.8 seconds. Five pace exceptions: takes 1, 3, 5, 6 and 7. Their original audio remains unchanged; no timing stretch or silence padding was used to make a check pass.

Scribe's raw tool verdicts: 1 PASS, 2 REVIEW, 3 REVIEW, 4 REVIEW, 5 REVIEW, 6 PASS, 7 PASS, 8 PASS. These are tool outputs, not final acceptance. Number formatting, US/UK spelling and the checker's em-dash token joining account for most mismatch runs. Independent faster-whisper small.en transcripts show no repeated phrase runs or obvious omitted passages. This does not establish that there are zero audible stumbles.

Two wording uncertainties for review: take 1 has `forge` in both ASR transcripts where the locked script says `forged`; take 2 has Whisper `carbon locks safely` versus Scribe `carbon locked safely` and locked script `carbon locked safely`. Do not rewrite the locked script based on ASR. Chief to decide the specific correction route, including whether to authorise a versioned pickup/retake and how to meet pace. Never overwrite these originals.

Whisper used the installed cached small.en model, CPU/int8, beam 5, word timestamps and VAD. The installed PyAV decoder rejected `metadata_errors`; ffmpeg decoded each WAV to 16 kHz float32 PCM for the same Whisper model instead. Volume measurements used ffmpeg volumedetect; integrated LUFS came from the take tool. No claim to have heard audio or perceived moving video. Ben's final watch supplies the listening check after tool failures are resolved.

Credit check: before 32,505 / 121,114 used (88,609 remaining); after 33,698 used (87,416 remaining). Counter delta 1,193 credits; counters can lag. Conservatively recorded all 2,586 submitted characters in both spend ledgers, one row per take. No additional credit calls made for retakes. Plan credits only, £0 additional cost.

Next: Chief review of pace exceptions and wording uncertainties. J2221 assembly stays dependent on J2220; no voice lock or production PASS is claimed. The queue's --films validator rejects OWB:J01 (numeric IDs only); the job's existing film J01/stage vo link is retained.
