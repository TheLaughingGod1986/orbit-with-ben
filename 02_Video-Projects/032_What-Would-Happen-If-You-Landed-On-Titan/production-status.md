# Production status — 032 What Would Happen If You Landed on Titan?

| Field | Value |
|-------|-------|
| Slug | `032_What-Would-Happen-If-You-Landed-On-Titan` |
| Gate | not run (topic not locked; parked for Chief in J0294) |
| Script review | PASS 92.4 / 100 (`titan_landing_script_master_v00.md`, 6 chapters, J0294) |
| VO | locked `titan_landing_vo_v02b` (Chief h31, J1294, 31 Oct 2026). `v02a` is an unlocked failed-spec attempt |
| CG | pending (Vertex Veo / Omni Orbit-only) |
| Runtime target | 7–9 min |
| Shorts | 3 a week (Mon · Wed · Fri; standalone Short `RLSJm59OSzI` already scheduled for 10 Nov 2026) |

## VO lock (Chief h31, J1294, 31 Oct 2026)

Locked stem `02_Voiceover/titan_landing_vo_v02b`. Built from the v02 parts only. ch00 fades out with `afade=t=out:st=50.30:d=0.18:curve=qsin`. ch02 fades out with `afade=t=out:st=107.66:d=0.02:curve=qsin`. No re-take, no ElevenLabs, no new STT.

| Check | Result |
|-------|--------|
| Duration | 582.440 s, 27,957,120 frames, pcm_s16le, 48 kHz stereo |
| Loudness | I −20.0 LUFS, LRA 4.8 LU, true peak −3.4 dBFS |
| ch00 tail | last 10 ms RMS −51.76 dBFS, last sample 0/0 |
| ch02 tail | last 10 ms RMS −62.53 dBFS, last sample 0/0 |
| Null vs v02 | max abs diff 0 outside 50.300–50.480 s and 245.140–245.160 s |
| wav sha256 | `55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5` (matches Chief sim) |
| mp3 sha256 | `944378a9c7caec4368217a481d35160cfb5621ed4de7dbe4a7787d813a6abff8` (libmp3lame 128k, same settings as v02) |
| Word timings | copied from `stt/titan_landing_vo_v02/` to `stt/titan_landing_vo_v02b/` |

`titan_landing_vo_v02a` stays unlocked. It is the failed 20 ms ch00 spec from J1289 (wav `56482edfe32ab6015033779d319ae3827f94c52ea5b89dcddc6d45127ccf0c35`, mp3 `a457adae2b5b23f20c4348fde76e0ac95332d649f98659307f863ac9b099f4fe`). v01, v02 and v02a were not modified.

## Blockers

- [ ] Chief topic lock + neighbour pass (≥3 education/space videos ≈1M+ views) + Pre-build vidIQ signed
- [x] Script v00 ≥ 90 (`review:script` PASS 92.4/100 on `titan_landing_script_master_v00.md`)
- [ ] Gemini `facts` quote check on `01_Script/SOURCES.md` + `CLAUDE_QUOTE_CHECK_v01.md`
- [ ] Stills locked before Veo/Omni spend

## `npm run review:script` (J0294, 15 Oct 2026)

```
# titan_landing_script_master_v00.md

**Decision:** PASS · **Score:** 92.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.2 |
| escalation | 8.8 |
| retentionPotential | 9 |
| searchPotential | 8.7 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.2 |

Words: 1621 · Est. min: 10.8 · Chapters: 6
Pass threshold: 90
```
