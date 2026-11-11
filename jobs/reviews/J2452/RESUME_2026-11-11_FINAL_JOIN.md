# J2452 — final join checkpoint, 11 November

Worker macbook. All thirteen saved chapters remain intact. Progress stays **13/15**; this is not a finished film or a UAT delivery. PR #789 remains open.

## New local artifacts

Scratch is `~/_desk/J2452-sleep-scratch/final_join_v01`. `TIMELINE.json` records the exact saved chapter files and hashes in running order: 013, 021, 027, 025, 023, 031, 020, 022, 028, 029, 024, 026, 019. Every local chapter was read completely and matched its NAS delivery record before assembly.

The final clock is **6,502.333333 seconds (108:22.333), 195,070 frames**: chapter pictures, twelve four-second breaths and a twenty-second closing fade. Earth starts at 967.2 seconds, preserving its already checked darkening ramp. Chapter interiors are stream-copied. No source-film reconstruction or new generation.

`sleep_picture_candidate_v03.mp4` has the expected container frame count and duration. SHA-256 is `0d668ba21348eb76fd8c65c26ac4d15f4a372d754a368f335d2af856d82800fe`. **It is rejected as a final candidate**, because join 2 fails. Its complete decode has not passed. The full decode of earlier rejected v02 was deliberately stopped, and its partial log must not be called a PASS.

`sleep_mix_pre_master_v01.wav` aligns each checked clean chapter narration to the final picture clock, adds the four-second breaths, the existing continuous filtered house bed, two-decibel join swells and final fade. Full independent EBU R128 measurement: **−20.6 LUFS, −5.6 dBTP, 2.9 LU LRA**. Full silence scan at −60 dB found no silence exceeding three seconds. **Raw mix peak FAILS** the −6 dBTP ceiling. The first loudnorm attempt timed out at 300 seconds and produced no normalized output; it is not a pass. `limit_join_audio.py` creates and independently measures a separate oversampled, latency-compensated limited PCM candidate; saved-file read-back **PASS for PCM only**: -20.1 LUFS, -6.5 dBTP, 2.9 LU LRA, no silence over three seconds, duration 6502.333333 seconds. `FINAL_AUDIO_PCM_READBACK_V02.json` records its SHA-256 and processing recipe. Do not rerender this PCM file; final encoded AAC must still be measured independently.

## Repair before any final master

Normal unmodified picture QA passes eleven standalone breath clips. **Saturn → Earth fails near-black** at the outgoing Saturn endpoint, including the v03 repair attempt. The new transition cannot inherit the source film's exception: this is a new edit. No failure was waived. The worker also inspected the four failing stills: a backlit ringed Saturn fades into Earth; this is a still-image inspection, not a playback claim.

The first attempted breaths replayed three seconds of neighboring motion; rejected in favor of endpoint holds with a two-second dissolve. Endpoint v02 uses the actual end frame. For Saturn the v03 attempt uses the frame four seconds before its end, which still fails (mean about 21.5). Three nearby donor candidates at two, four and eight seconds before the end were measured; all have mean below 28. Do not repeat that unchanged search. The existing full Saturn pixel report already records a clean neighboring frame at chapter second 505 (mean 57.07); seconds 507 onward contain the dark stretch. Any repair must consider the last chapter seconds as well as the breath and inspect both boundaries. Use the Chief's own-neighbor fallback, preserve every narration sample and the chapter clock, retain old candidates, and run normal new-edit gates. Do not brighten the whole compilation, change gate thresholds, or call the inherited dark endpoint a pass.

Standalone gates are in `join_qa_v03_01` through `join_qa_v03_12`; the summary is `JOIN_GATES_V03.json`. The public evidence snapshot is `FINAL_JOIN_CHECKPOINT_V01.json`. The successful eleven clips can be reused. `join_public_chapters.py --phase picture` currently reproduces the **failed** v03 choice, not an approved repair; change to a new version before rebuilding. Do not re-encode the thirteen complete chapter pictures.

## Still owed

Repair Saturn's exit/breath and check all join neighborhoods in the assembled picture, including source-side boundaries; full final decode; saved AAC loudness/true-peak/silence and duration read-back; whole-film CTA/script audit; final master and approximately twelve-minute reel; additive NAS copies with complete destination SHA-256 read-back; Ben's watch card. Do not set awaits/UAT until these are complete. The watch card must retain the version-one scope: public charts/labels stay, dissolves only on compilation edits. Earliest air date 12 December. Thumbnail Option A already exists as recorded by the previous input audit.

No media was written to git or delivered as a finished master this run. No Studio operation, upload, login, spend, NAS deletion or source replacement. Python compilation and thirteen privacy tests passed. Thread messages were read through #6809039209; persisting the home-directory read marker was sandbox-restricted.

All processes launched in this run exited; the rejected v02 decode was explicitly interrupted. No encode or scan remains running. Resume at the Saturn exit repair, retaining the passed PCM audio candidate and the other eleven breath clips.
