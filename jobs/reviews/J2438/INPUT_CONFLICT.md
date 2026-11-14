# J2438 — opening plan conflicts with locked inputs

Codex covering J2438, 12 November 2026. Advisory FIX; no final approval claimed.

FIRST30_PLAN.md cannot be executed literally without interrupting speech. No render was started and no master, VO, Short, YouTube or Buffer state was changed.

## Exact insertion conflicts

The plan requests +1.00 s silence at raw 38.68, +0.90 s at 48.80 and +0.90 s at 56.20. The locked stt_raw.json places these inside words:

- 38.68 s: 'mystery.', 38.28–38.82 s.
- 48.80 s: 'city-sized', 48.74–49.54 s.
- 56.20 s: 'one-fifth', 55.56–56.24 s.

## Row and content conflicts

Actual shot_list_v01.csv rows R01–R07 have durations 9.15, 10.44, 10.62, 9.09, 14.70, 6.55, 5.21 seconds. The plan instead describes later rows as 10.00, 7.48, 8.98 seconds. Both reach R08 at 65.76 seconds, but the proposed internal boundaries do not follow the locked words.

The actual third sentence begins “On 13th and 14th July 2015” at 20.14 s and discusses the flyby, distance and temperature through 38.82 s. The plan substitutes a highlands/history sentence that is absent from this VO. The plan’s R04 plain-ice images would therefore accompany the actual distance/temperature narration, and its 38.68 s breath would split “mystery.”

The initial 2.00–4.80 s trim does match transcript pauses, and the hook/payoff end times become 5.90 and 16.24 seconds. These transcript checks do not establish how the audio splice sounds.

## Required next action

Chief/reviewer should correct FIRST30_PLAN.md using the locked v03 transcript and actual CSV: choose verified inter-sentence gaps for the 2.80 s restoration, retain the actual spoken content and matching picture, and define frame-rounded R01–R07 boundaries that rejoin R08 at 65.76 s. Then reopen J2438 for the v02 assembler, detached render, Short re-export and automated gates. No new voice take or spend is necessary merely to correct this plan.

Audio and moving-video perception were not demonstrated in this session. No listening or motion QA is claimed. Blocking cause here is the written plan/input conflict, not an input-capability hold.

Evidence: NAS 02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_raw.json; repository 07_Edit-Project/shot_list_v01.csv and FIRST30_PLAN.md. Thread read to #6811167124.
