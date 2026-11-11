# J2452 — narration build checkpoint, 11 November 2026

Worker: macbook. **Compilation incomplete; release for the next run.** No finished video, UAT card, upload, generation, spend, NAS change or detached process. The latest Chief ruling is accepted: 13 films, Moon first / Andromeda last; 005 and 006 excluded, 032 excluded, runtime floor lifted. The older RESUME note's scope question is resolved.

## Built and measured

Nine reusable narration chapters are on the MacBook's local disk, **75:03.45 total**:

| Film | Duration (s) | Measured LUFS | Measured dBTP |
|---|---:|---:|---:|
| 027 | 438.05 | -20.20 | -6.20 |
| 025 | 462.50 | -20.20 | -6.20 |
| 031 | 543.59 | -20.21 | -6.20 |
| 020 | 572.70 | -20.32 | -9.19 |
| 028 | 452.71 | -20.20 | -6.20 |
| 029 | 494.30 | -20.21 | -6.20 |
| 024 | 463.35 | -20.21 | -6.19 |
| 026 | 471.40 | -20.21 | -6.19 |
| 019 | 604.85 | -20.34 | -9.19 |

Paths and hashes are in `narration_v01/*.json` beside this note. Local outputs are `/Users/ben/_desk/J2452-sleep-scratch/narration_v01/chapter_<film>_narration_v01.wav`, except corrected 019/028/026 in the matching `narration_<film>_v02/` directories and 027 at `/Users/ben/_desk/J2452-sleep-scratch/chapter_03_v01/chapter_03_027_narration_v01.wav`. These are stereo 48 kHz, 24-bit PCM narration intermediates, **without the continuous bed**. Preserve them; no need to re-encode or re-normalize them to resume picture work. Final mixed loudness still needs measuring.

The initial 019/028/026 outputs were shorter than their requested cut timelines because the source narration ended before the picture tail. These are explicitly superseded in `rejected_narration_tails_v01.json`; preserve but do not use them. The corrected builder pads the source to master duration before trimming, and checks saved duration against the timeline.

The warmth/compression chain is followed by two-pass loudness normalization. Each output was fully decoded for loudness/peak measurement. `NARRATION_CHECKS.json` records a second read-back of all nine saved hashes and durations, with every duration matching the cut timeline within 1 ms. `input_i`, `input_tp` and `input_lra` in each report's `levels` describe the actual saved output; `output_*` describe the analysis filter's hypothetical second normalization, not another saved file. This distinction matters when reading the reports.

`corrected_audio_cuts_v01.json` records both planned and used numbers, adjacent master-ASR words, and complete retained transcripts for these nine chapters. No used boundary intersects a master-ASR word; every kept slice ends after sentence punctuation. Retained transcripts contain no subscribe keyword, next-week line, “In this film”, “Stay with me”, or the house subscribe sentence. This is tool/transcript evidence, not a claim of hearing the stems. The remaining four chapters and the assembled master have not passed CTA checks.

## Alignment and identity evidence

`alignment_v02/inputs_v01.json` is a runnable manifest of the 13 approved films with actual readable NAS paths. It replaces the stale copied Mini manifest with null masters and Mini-only paths. All four real Moon narration WAVs are included; AppleDouble sidecars are excluded.

`alignment_v02/*_alignment.json` contains 4-second waveform matches every 20 seconds, decoded mono at 4 kHz. Most raw narration matches at zero offset; 031 needs a **5 ms delay**, Andromeda a **3.005 s delay**. The four Moon parts have separate offsets. Strong matches establish the source/time relationship; sparse samples do not establish every splice or authorize interpolating across a change of source. Moon decoding emitted non-monotonic timestamp warnings, so **do not treat its sample-count clock as a final PTS-accurate laid timeline**: reconstruct it from its part/join records and verify its boundaries next run. Low correlations in silent tail windows are retained as evidence, not treated as matches.

`alignment_v02/master_hashes_v01.json` records current full-file SHA-256 hashes for all 13 masters. All nine masters with an upload hash in the copied input register match it. Four have no upload hash there (013, 021, 020, 019): their current hashes are recorded, not represented as fresh YouTube identity proof. 021's current hash also equals J2548's copied hash. No YouTube access was made.

Use **alignment_v02 only**. Local `alignment_v01` is an unsuccessful diagnostic attempt: silent source windows caused numerical false correlation peaks; it is not build evidence. The v02 script masks silent candidates and all saved normalized correlations were checked to lie within [-1, 1].

## Corrections that matter for picture work

- 027 subscribe removal is **164.45–169.90**, in pauses around the complete two-sentence ask, rather than clipping “We” and “you”.
- 024 resumes **219.45**, before the whole word “Now” at 219.89, rather than at 220.00 inside that word.
- 031's proposed 23.50 cut is between clauses of the same sentence. Keep through the South Atlantic question at 27.66, cut at **27.90**, resume at **36.16** after the two subsequent agenda questions. The subscribe cut is **220.30–225.95**.
- 020's actual opening is “The cloud deck is already around you”, not the plan-described Galileo opening. The planned 22–32 cut would leave “Cloud, then darker cloud” without the rest of its sentence. Keep the substantive opening narration from **0.00** and cover the hook picture separately. End at **572.70**, after the complete question ending at 572.34 and before “Or” at 573.30, as Chief instructed.
- Preserve entire opening words on 024/025/026/028/029/031; pictures still need their hook captions covered. Start 019 at **2.30**, before “A” at 2.74. Remove its whole character sentence **342.10–347.75**.
- The actual 027 narration is the Earth-stopping thought experiment, not the plan's rewritten description about leap seconds/coral. Follow the real film when choosing cover imagery; do not invent that description as its content.
- Plan duration totals are also inconsistent with some of its numeric slices. Recompute the full runtime from the actual final timeline, rather than carrying forward 107.7 minutes as a measured result.

## Next run: concrete work remaining

1. Finish narration assembly and sentence cuts for **013, 021, 022 and 023**. Source files and sparse clock matches are already in the manifest. 013 requires four-part join reconstruction; 021 has a laid narration file. Existing source word files/build timelines can support these cuts, but have not been mapped/approved here.
2. Build the full picture recipe on actual master time: cover hook captions, Orbit beats, bright diagrams and chapter cards as required by the plan; resolve missing plates using the brief's approved alternatives / official sources with provenance. No cover plate was downloaded this run. Apply the measured audio cuts, not the old plan blindly.
3. Render chapters separately on local _desk scratch. Add the one continuous soft house bed, transition breathing room, dissolves and the sleep darkening curve in the edit, with matching encode settings so chapters can be joined without another video encode. Do not call the nonexistent picture_qa sleep-darken flag or waive failures.
4. Run final loudness/peak/silence/CTA/join picture gates, create the ~12-minute reel, copy the master/reel to NAS and verify hashes. Existing thumbnail Option A remains at the NAS path in the earlier resume note. Only then send the finished cut to Ben's watch; no upload.

Reproduce the inventory/alignment with `_desk/J2141-venv/bin/python jobs/reviews/J2452/align_inputs.py --out <new local directory>` (numpy is already in that venv). Build one of the eight general narration chapters with `python3 jobs/reviews/J2452/build_narration.py --film 020 --alignment jobs/reviews/J2452/alignment_v02/020_alignment.json --out <new local directory>`. The dedicated `build_027_narration.py` reproduces the first 027 checkpoint. Both builders refuse to overwrite an existing output. Existing saved stems are the resume point, not a reason to repeat the builds.
