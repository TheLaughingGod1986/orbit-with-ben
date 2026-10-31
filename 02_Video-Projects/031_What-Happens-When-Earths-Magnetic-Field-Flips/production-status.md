# Production status — 031 What Happens When Earth's Magnetic Field Flips?

| Field | Value |
|-------|-------|
| Slug | `031_What-Happens-When-Earths-Magnetic-Field-Flips` |
| Gate | BLOCK on `prebuild_vidiq` sign-off (all script/structure checks OK) |
| Script review | PASS 95.4 / 100 (`magnetic_field_flip_script_master_v01.md`, 1,300 spoken words, 6 chapters, J0259) |
| VO | locked `magnetic_field_flip_vo_v02a` (Chief h32, J1295, 31 Oct 2026). h24's 20 ms / 40 ms fades were too short |
| CG | pending (Vertex Veo / Omni Orbit-only) |
| Runtime target | 7–9 min (~8.8 min est.) |
| Shorts | 3 a week (Mon · Wed · Fri) |

## VO lock (Chief h32, J1295, 31 Oct 2026)

Locked stem `02_Voiceover/magnetic_field_flip_vo_v02a`. Built from the v02 parts only. Each part fades out with `afade=t=out:curve=qsin` ending on its last sample: ch00 `st=35.24:d=0.12`, ch01 `st=88.38:d=0.02`, ch02 `st=100.28:d=0.04`, ch03 `st=92.14:d=0.02`, ch04 `st=73.96:d=0.04`, ch05 `st=86.22:d=0.02`, ch06 `st=87.42:d=0.18`. This replaces the h24 fades (ch00 20 ms, ch06 40 ms), which stopped above −50 dBFS. No re-take, no ElevenLabs, no new STT. The 1905 date/place card spells PONTFAREIN (h24).

| Check | Result |
|-------|--------|
| Duration | 568.280 s, 27,277,440 frames, pcm_s16le, 48 kHz stereo |
| Loudness | I −19.9 LUFS, LRA 4.8 LU, true peak −3.5 dBFS |
| ch00 tail | last 10 ms RMS −56.11 dBFS, last sample 0/0 |
| ch01 tail | last 10 ms RMS −71.55 dBFS, last sample 0/0 |
| ch02 tail | last 10 ms RMS −58.22 dBFS, last sample 0/0 |
| ch03 tail | last 10 ms RMS −71.09 dBFS, last sample 0/0 |
| ch04 tail | last 10 ms RMS −58.07 dBFS, last sample 0/0 |
| ch05 tail | last 10 ms RMS −59.52 dBFS, last sample 0/0 |
| ch06 tail | last 10 ms RMS −57.08 dBFS, last sample 0/0 |
| Null vs v02 | max abs diff 0 outside 35.240–35.360, 124.440–124.460, 225.440–225.480, 318.320–318.340, 393.000–393.040, 479.960–479.980 and 568.100–568.280 s |
| wav sha256 | `3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6` (matches Chief sim) |
| mp3 sha256 | `334085b5f1eb1992a0fd7f31ff46f97b24b0443158551f2cf91476a9d9c31347` (libmp3lame 128k, same settings as v02) |
| Word timings | copied from `stt/magnetic_field_flip_vo_v02/` to `stt/magnetic_field_flip_vo_v02a/` |

v01 and v02 (wav, mp3, parts, stt) were not modified.

## Blockers

- [ ] Pre-build vidIQ signed + neighbour pass (≥3 education/space videos ≈1M+ views) + Chief topic lock
- [x] Script ≥ 90 (`review:script` PASS 95.4/100 on `v01`)
- [ ] Gemini `facts` quote check on `01_Script/SOURCES.md` + `CLAUDE_QUOTE_CHECK_v01.md`
- [ ] Stills locked before Veo/Omni spend

## `npm run review:script` (J0259, 15 Oct 2026)

```
# magnetic_field_flip_script_master_v01.md

**Decision:** PASS · **Score:** 95.4 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1321 · Est. min: 8.8 · Chapters: 6
Pass threshold: 90
```
