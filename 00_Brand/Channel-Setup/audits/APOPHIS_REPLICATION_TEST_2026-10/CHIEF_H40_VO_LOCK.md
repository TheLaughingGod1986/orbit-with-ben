# Chief h40 VO lock for AR1–AR3 (J1306, 31 Oct 2026)

Verdict: **AR2 PASS as recorded. AR1 and AR3 FIX by Chief sentence cuts**, spliced from the takes already recorded. No re-take, no ElevenLabs, £0.
This file is binding on J1308 (assembly) and on listings. Where it disagrees with SCRIPTS_AND_PACKAGING_v02.md or CHIEF_H37_CORRECTIONS.md C7, this file wins. The h37 facts, C1–C6 and the C8 bar are unchanged.

## Why
The C7 trims could not reach the bar. With the years spoken the house way and eleven_v3's 0.5–1.1 s sentence gaps, AR1 v02 ran 23.00 s (cut 24.0 s, answer 16.46 s) and AR3 v02 ran 26.16 s (cut 27.2 s, answer 19.12 s).
Gap-tightening alone saves about 1.5 s, so whole sentences have to go. As Chief I've cut the line that teaches least out loud and is still shown on screen by a PASSed graphic.

## Locked spoken words (v03)
**AR1** `apophis_ar1_vo_v03` (from v02; drops "Sixty metres wide, it matches a fifteen-storey building."):
> Asteroid 2024 YR4 will skim past the Moon on December twenty-second, 2032. Early tracking gave a four percent chance of lunar impact. It will miss, passing twenty-one thousand two hundred kilometres up. Look up knowing…

**AR2** `apophis_ar2_vo_v01` (unchanged, locked as recorded):
> NASA plans to crash the Space Station into the ocean around 2031. It spans a hundred and nine metres, like a football field. Most hardware vaporises. A deorbit craft steers the rest into the empty South Pacific. Look up and watch it cross the sky, because…

**AR3** `apophis_ar3_vo_v03` (from v02; drops "Its shadow spans two hundred and fifty-eight kilometres." and "That nearly triples twenty twenty-six's two-minute eclipse."):
> The 2027 solar eclipse turns midday into night for over six minutes. Totality crosses Spain and North Africa, peaking over Egypt at six minutes twenty-three seconds. Millions can look up as…

All three loops still read grammatically into line 1. The subject is word 1 and the surprise is in sentence 1.

## Takes (sha256 of the WAV; 48 kHz s16 stereo)
| Short | stem | sha256 | VO s | planned cut | answer line | answer % of cut | I LUFS / peak |
|---|---|---|---:|---:|---|---:|---|
| AR1 | apophis_ar1_vo_v03 | de70ed062c017993e22da6dd5f0e77dd9c9de8331ba94be61e4e74e36a52aedb | 18.365 | **19.37** | "It will miss" 12.17 s | 63% | −21.1 / −4.6 dBFS |
| AR2 | apophis_ar2_vo_v01 | d0d0e4c4e55f616bc73f361e2b508bb4f62b4e94fc0398e66b275917ff5f6283 | 18.400 | **19.40** | "A deorbit craft" 10.94 s | 56% | −19.7 / −4.3 dBFS |
| AR3 | apophis_ar3_vo_v03 | 95ab6cf199bea32c4b85516926152d54b333c0730626f89b97858551dd146c2c | 17.055 | **18.06** | "Totality crosses" 6.93 s; "peaking over Egypt" 10.26 s | 57% | −20.9 / −4.8 dBFS |

Build: `02_Voiceover/vo_build_h40/splice_v03.py ar1|ar3` (deterministic, refuses any input that isn't the reviewed v02, never overwrites).
- Cuts are at room-tone points, all below −70 dB.
- Joins get a 10 ms qsin fade.
- AR1 also gets a 160 ms end fade. The API cut the C7 retake "knowing…" off at about −21 dBFS. Cursor's 10 ms fade left the last 20 ms at −32 dB, which is the h23/h31/h32/h39 too-short-fade case again. Now the last 10 ms is −73.6 and the last 20 ms is −49.0.
- The null test against v02 outside the fade windows is max abs 0.
- faster-whisper small.en and base.en hear every word as written in all three.

## Line clock for the edit (VO time, s; envelope at −50 dBFS)
- **AR1 v03:**
  - L1 0.04–7.60
  - "Early tracking…" 8.15–11.63
  - "It will miss…up." 12.17–16.54
  - "Look up knowing…" 17.09–18.37
  - Loop tail to 19.37
- **AR2 v01:**
  - L1 0.07–4.58
  - "It spans…" 5.21–8.07
  - "Most hardware vaporises." 8.68–10.41
  - "A deorbit craft…Pacific." 10.94–14.68
  - "Look up…because…" 15.15–18.39
  - Loop tail to 19.40
- **AR3 v03:**
  - L1 0.07–6.33
  - "Totality crosses Spain and North Africa," 6.93–9.78
  - "peaking over Egypt at six minutes twenty-three seconds." 10.26–13.92
  - "Millions can look up as…" 14.52–16.98
  - Loop tail to 18.06

## Graphics with the cut lines (J1308)
- **AR1:**
  - `ar1_size` (60 M / SCALE: 15-STOREY BUILDING) is **not used**, because it has no spoken line now.
  - Date card `22 DEC 2032` goes on L1, after the 0–2 s hook caption.
  - The C1 odds call-out goes on "Early tracking…".
  - The miss diagram (21,200 KM) goes on "It will miss…".
  - The cover text `15-STOREY / SPACE ROCK` may stay: it's a true, sourced fact on a still.
- **AR3:**
  - The `2 AUG 2027 · 258 KM PATH · LONGEST: 6M23S, EGYPT` card goes on L1. It's a date/place card whose lead item is L1's eclipse.
  - The path map, with countries labelled one at a time Spain→Egypt, goes on "Totality crosses Spain and North Africa," and runs on into "peaking over Egypt" with the GD dot under EGYPT.
  - The DATA bar `2026 ECLIPSE: 2M 18S` vs `2027 EGYPT: 6M 23S` goes on "at six minutes twenty-three seconds". The bar carries the "nearly triples" fact that's no longer spoken.
- **Everything:**
  - One label at a time, kept clear of 0–2 s and the title interval.
  - Cuts are VO + 1.0 s loop tail.
  - Never clip a line.
