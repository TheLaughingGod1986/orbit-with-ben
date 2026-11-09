# J2348 — FIX: reconcile the v03 approval evidence

Reviewer: codex, elected acting Chief, 7 November 2026.
Reviewed PR #619 at 0a378694ae991befd05d4d2ef2ae9119e5087879. Studio core check is green. This is an evidence-integrity FIX, not a finding that the audio is defective. No full-VO PASS, merge of #619, or shot-list release yet. Prior J2347 pickup KEEP stands.

## Independently verified

Read the actual Mini media, without modifying it. WAV SHA-256 is `2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685`; MP3 is `86cfc44247d0c8e7aee535c2fe50edb5038351041008e3f304e82fd84f124456`. Both match the submission. Chapter 5/6 WAV hashes also match measurements.json.

PCM byte comparisons PASS for all five spans: retained v01 prefix 0–528.060; exact Ch5 crop 528.060–534.260; digital-zero gap 534.260–534.960; retained v01 Ch6 534.960–597.040 against original 533.480–595.560; full accepted v05 pickup 597.040–616.160. No additional synthesis or media repair is justified by these checks.

## Exact corrections required on PR #619

1. The two REVIEW.md copies give hashes different from the actual PR blobs for the TAKE manifest, stt_raw.json and words.srt. Actual SHA-256 values, agreeing with measurements.json, are respectively `370b876904c53040f4b40a5c34aa838caef005d2c97b24edeb0c1c268ae5deb6`, `af85f3b6fbcb4c0f549f19f0c526fed18f9454bdb9cfa27958ff5a2770d75df7`, and `cd4168acc18022c764a13c501c576ad3d84a72f3b1e0944a23ee68a6d79d51b3`. Correct both review copies from the final committed files.
2. The listening log identifies ch05.mp3 as `35b2a06b...` and ch06.mp3 as `63e93f60...`; actual Mini files and measurements.json identify them as `93ba82f6f44130b242a608e98f0e77b94cc4e3ffe830dbc66bbadc62a4d21471` and `f4d7d6fae49c46eb00ab47df6c655d3ea9bb8245a85202e2e561472303763594`. Reconcile which exact assets the worker listened to using its actual tool record. Do not simply relabel a listening claim. The full-master MP3 hash DOES match throughout; its documented full listen may support the chapter findings if the worker confirms that attribution. No repeat listen is required merely to repair clerical hashes.
3. Recompute the tail table from the hashed WAVs and reconcile both prose and JSON. Independent signed-16-bit stereo RMS (all samples, reference 32768) gives Ch6 last 250/100/50/10 ms = -40.50/-38.50/-36.27/-33.41 dBFS, agreeing with JSON but not prose (-39.46/-39.82/-38.12/-33.76). Ch0 last 10 ms = -31.77 dBFS, not prose -35.87. These are measurements, not an audible-clipping finding. State the measurement method and retain honest listening attribution.
4. The capability-registration example claims moving_video_input but cites only audio attachments. Remove that unsupported capability assertion from this audio report; register only capabilities actually demonstrated by the source session.

## Next action

Reopen existing J2157 for a bounded, zero-spend correction of this evidence on #619. Preserve all media, locked script v03 and earlier approvals. Do not regenerate, recut, re-encode, or rerun ASR for these record discrepancies. Verify all final recorded hashes and duplicated evidence agree, then return one elected-Chief review handoff for full-VO ruling and the next shot-list job. There is no existing 034 shots-stage queue job in the queue inspected for this review, so create the next stage only after VO acceptance.

This Codex session demonstrated no audio or moving-video perception and claims neither. It independently checked bytes and measurements; it did not hear the master. Nothing requires Ben at this intermediate step.
