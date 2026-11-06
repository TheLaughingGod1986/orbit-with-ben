# J2157 — completed take, verification FIX (6 Nov 2026)

Codex recovered the existing detached run, exit marker 0. No second take or new TTS spend. Original script and audio remain untouched. Script v02: 1,291 words / 8,001 characters, 7 audio sections (open + 6 chapters). Ben Orbit Narrator, eleven_v3, locked house settings.

## Evidence

- Audio stays at `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/02_Voiceover/pluto_frozen_heart_vo_v01.wav`.
- WAV SHA256 `86483fb4919c3fd097a84d3c0d43f52a89521f87b2ff6f1976dea1506d2c8618`; MP3 SHA256 `b7fdd348819c9e2dd98a01fc8ca272f1a135c6ff033302ad98022d8eb7bcaf85`.
- Decode complete: 614.680 s (10:14.68), mean -23.0 dB, integrated -19.9 LUFS, true peak -3.7 dBFS. Level checks PASS. Actual runtime exceeds the script estimate; shot timing must use actual word timestamps.
- Scribe raw agreement 84.49%, 69 mismatch runs: automated REVIEW retained unchanged. Most rows are numbers rendered as digits, UK/US spelling, or spoken date formatting. Negative signs and fraction slash exist in raw transcript; tokenisation stripped them. Do not mistake those for omitted spoken numbers.
- Residual lexical differences include script “looked back” versus Scribe “looks back” (end of Where Water Is Bedrock), and “Real Worlds series” versus “Real World series” (closing handoff). These are unresolved transcript discrepancies, not proof of a speech error. They need targeted verification before word-for-word approval.
- `TAIL_METRICS.json` records last 50/100/250 ms RMS for each original part. Several chapter ends lack a sustained silence below -45 dBFS in the final second. That is insufficient to certify an unclipped decay; preserve original parts and verify boundaries against final-word timestamps, repair only on evidence. No claim of listening or hearing tail quality.
- Earlier take logged 8,001 characters; subscription counter advanced only 3,291 immediately after generation. Preserve the full spend ledger rather than trusting that lagging delta. Live reading this session: used 27,674 / limit 121,114 / remaining 93,440. No top-up/overage.

## Decision and next action

FIX / no VO lock and no shot-list release yet. Continue J2157 with targeted Scribe checks of the two lexical discrepancies and measurable chapter-boundary checks, under the ElevenLabs lock with live credit guards if another transcription is needed. Reuse this take; do not regenerate the whole narration. Any proven wrong word requires a separately authorised sentence pickup from the unchanged locked script. On clean evidence the Chief may rule under STUDIO_PLAYBOOK §review (4 Nov): tools establish technical checks; Ben’s final UAT supplies listening. Do not hold solely for absent audio perception and do not claim an unheard take was listened to.

A NAS offload check was run because free space is below 8 GB: no eligible scratch older than 48 h; nothing moved or deleted. This small verification used existing audio. Broader production remains outside this job.

## Targeted Scribe recheck

Two bounded excerpts were transcribed under desk-lock elevenlabs in this session. Both reproduce the same lexical discrepancies: ch05 at source +65 s returns “What if New Horizons looks back?”; ch06 at +55 s returns “Real World series”. Raw JSON and word timestamps are retained in `targeted/`. This is additional ASR evidence, not a listening claim. Treat the word-for-word check as FIX pending exact-script sentence pickups, rather than silently accepting or rewriting the script. No new TTS was generated.
