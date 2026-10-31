# J1306 VO report — Apophis-mould Shorts AR1–AR3

31 Oct 2026. Ben Orbit Narrator, `eleven_v3`, speed 1.04. Orders: `6c7d0f83b`, J1279 (Chief h37 script PASS). AR4 was not recorded.

Audio (wav/mp3) stays out of git. Each stem has a `TAKE.json`, a `*_words.json`, and `stt/<stem>/`.

## What was spoken

v01 is the locked `>` lines in `SCRIPTS_AND_PACKAGING_v02.md` §4–§6, with only the year tokens respelled the house way named in the job:

- `2024 YR4` → `twenty twenty-four Y R four`
- `2032` → `twenty thirty-two`
- `2031` → `twenty thirty-one` (same year pattern; the job listed the other four)
- `2027` → `twenty twenty-seven`
- `2026's` → `twenty twenty-six's`

No other v01 word was changed. The exact strings are `ar1_spoken_v01.txt`, `ar2_spoken_v01.txt`, `ar3_spoken_v01.txt`. The locked lines with digits are `ar*_locked_v01.txt`.

## Money

Subscription before: 101,577 of 121,114 characters left. Extension cap 0 (`can_extend_character_limit` false), so this could not bill overage. Sent 1,048 characters (322+269+329 for the three shorts, plus 16+56+56 for the three C7 line retakes). Counter after: 101,072 left (used 19,537 → 20,042, a lag of about 500 against the 1,048 sent). J0862's HOS 009/010 Shorts are 1,280 spoken characters (2,560 with one retake each) and were not touched.

## Scribe

Every full-short `vo_check` is REVIEW. The mismatches are Scribe writing digits and US spelling (`meters`, `story`, `vaporizes`, `kilometers`) for words that were sent in the house spelling. There is no substituted word. The line retakes were not used for that: a second take would scribe the same way. `apophis_ar1_c7_look_vo_v01` is an exact PASS.

## Length and answer

Planned cut = wav duration + 1.0 s loop tail. The bar is 17.0–20.0 s. C8: the answer line starts by about 13.5 s, and the look-up line is last.

| Stem | Wav s | Planned cut | LUFS | First word | Surprise | Answer | Answer % of cut | Last word end |
|---|---:|---:|---:|---|---|---|---:|---:|
| AR1 v01 | 24.40 | 25.40 | −21.3 | Asteroid 0.10 | skim 3.60 | It will miss 17.52 | 69% | knowing 24.34 |
| AR1 after C7 trim 1 only | 24.07 | 25.07 | — | (ending only) | — | unchanged | — | — |
| AR1 v02 (C7 trims 1 then 2) | 23.00 | 24.00 | −21.2 | Asteroid 0.10 | skim 3.60 | It will miss 16.46 | 69% | knowing 22.92 |
| AR2 v01 | 18.40 | 19.40 | −19.7 | NASA 0.12 | crash 0.92 | A deorbit craft 10.98 | 57% | because 18.32 |
| AR3 v01 | 26.88 | 27.88 | −21.5 | The 0.08 | turns 2.58 | peaking 19.84 | 71% | as 26.72 |
| AR3 v02 (C7 trim 3) | 26.16 | 27.16 | −21.4 | The 0.08 | turns 2.54 | peaking 19.12 | 70% | as 26.00 |

AR2 v01 is inside 17–20 s, its answer starts at 10.98 s, and `Look up…` is the last line.

AR1 and AR3 stay over 20 s after the C7 trims, in order. Trim 1 (`Look up knowing…`) saved 0.33 s. Trim 2 (`Sixty metres wide…`) saved another 1.07 s. Trim 3 (`Its shadow spans…`) saved 0.72 s. The answer lines stay past 13.5 s (16.46 s and 19.12 s). The look-up line is last on both. No other word change is authorized.

The overrun is the spelled year readings (about a second each) plus 0.6–1.1 s gaps between the locked sentences. Those gaps are why `skim` lands at 3.60 s and `turns` at 2.54 s.

## Files

v01 (locked words):

- `apophis_ar1_vo_v01` wav `cb317004899baae02b119bca3c2041f1f2312ff7b8e2fbf9d8c4ffb3bc511b7b`
- `apophis_ar2_vo_v01` wav `d0d0e4c4e55f616bc73f361e2b508bb4f62b4e94fc0398e66b275917ff5f6283`
- `apophis_ar3_vo_v01` wav `a2b10e3316cfa0b6a55b32887e7ff1345b3474eed434a8a3b801d98cc397e922`

v02 (C7 splices; v01 left as recorded):

- `apophis_ar1_vo_v02` wav `9154050eee7ae6a9245897368dff3282f0bd68f3dc5f28169cedf2e1d9ed28d6`
- `apophis_ar3_vo_v02` wav `03d0e06380a3237257058b8d4a84a31e760af048ef1dc616a0031ea738e1ea2a`

C7 line retakes: `apophis_ar1_c7_look_vo_v01`, `apophis_ar1_c7_sixty_vo_v01`, `apophis_ar3_c7_shadow_vo_v01`.

No picture, no upload, no schedule.
