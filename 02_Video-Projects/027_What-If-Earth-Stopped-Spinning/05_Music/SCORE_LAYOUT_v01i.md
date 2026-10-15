# 027 Earth Spin: score layout by chapter for v01i (J0265)

Cursor, 15 Oct 2026. No spend. Advisory: Chief decides on take 2 and scores the gates.

**Why.** J0262's QA sweep failed `music_gate` on v01h and v01i. They carried the retired take 1 lift, which scored as reused (0.80–0.82 against 021, 024 and 025), had a 6.1 s near-gap at 7:41 and measured 52 BPM. The fix is take 2 (`BED_BRIEF_take2.md`). It needs ElevenLabs credit, so it waits for Chief's OK or the 30 Oct reset. Everything else is ready now.

## The layout (Polish pass 2: one bed, both moods, changing at the cards)

The cut is v01i, 446.3 s; the last word is at 7:22.8. Cards are taken from `07_Edit-Project/rough_v01i_pack/overlays_v01i.json`. Each crossfade is 3 s, centred on the card.

| Film | Mood | Chapter | Brief asks for | Bed section (brief time) | Crossfade |
|---|---|---|---|---|---|
| 0:00.0–0:23.3 | awe | Open | light and curious | 0:00 | — |
| 0:23.3–1:33.5 | explain | The Sudden Stop | taut rising pulse, peaks and eases | 0:25 | 0:21.8–0:24.8 |
| 1:33.5–2:55.3 | explain | The Speed You Cannot Feel | relaxed and airy | 1:35 | 1:32.0–1:35.0 |
| 2:55.3–4:08.4 | awe | A Slow Stop | spacious and slow | 3:00 | 2:53.8–2:56.8 |
| 4:08.4–5:56.8 | explain | Earth Is Already Slowing | gently ticking, clocks and tides | 4:10 | 4:06.9–4:09.9 |
| 5:56.8–7:26.3 | awe | Keeping Score | warm, grounded, held chord | 6:00 | 5:55.3–5:58.3 |

That gives three awe-to-explain changes at cards (review gate MUSIC). The music holds past the last word (7:22.8) and fades over 7:23.3–7:26.3.

The v01i chapters land within 5 s of the brief's times, so each section is laid near-continuously (skips of 1.5–4.7 s, hidden in the crossfades). The bed needs at least 449.6 s. The brief's 470 s take covers that, and the script checks it.

## When take 2 exists

```bash
cd 02_Video-Projects/027_What-If-Earth-Stopped-Spinning/05_Music
python3 _lay_score_take2_v01i.py --plan
python3 _lay_score_take2_v01i.py --bed <take-2 file> [--sections 0,25,95,180,250,360] [--bed-db -22]
```

- Listen to the take's contour first. If its section changes miss the brief's times, pass the measured bed times with `--sections`. The film side doesn't move.
- The script writes `earth-spin_score_take2_laid_v01i.wav` with a `_plan.json` (the take's own prompt, so `music_gate` sees the Pace and NOT lines). It builds `/private/tmp/027_EarthSpin_rough_v01i_scored.mp4`: v01i's picture copied, with VO, bed and SFX mixed to −14 LUFS / −1 dBTP. Then it runs `music_gate` and `sfx_kit.py level --bed` into `SCORE_GATES_v01i.json`.
- That master goes to the NAS or OWB UAT with its sha256 before any watch (14 Oct master rule).

**Mechanics test (15 Oct).** I ran it once on the retired take 1, then deleted the outputs. The lay, mix and gates all ran in 20 s. `sfx_kit level` with the bed at −22 dB: PASS. `music_gate` FAILed only on take 1's own faults: reused (0.82 against 025's Mars bed) and its hush (a 30 s near-gap from 5:14). Take 2's brief is written to avoid both.

**Pace note for Chief.** The take 1 plan says 70–84 BPM. The take 2 brief says 76–88. `music_gate` reads whichever plan sits next to the laid bed, so take 2 is measured against 76–88.

## SFX (Polish pass 1): ready, PASS

`06_Sound-Effects/_build_sfx_stem_v01i.py` builds the stem from `kit_v01`, the house kit (own synthesis, `sfx_kit_manifest.json`). It has 15 cues, all in `sfx_cues_v01i.json`:

- **8 ticks**, one on every label and timeline date as it appears: 0:06.9, 6:02.0, 6:12.5, 6:16.7, 6:22.6, 6:37.0, 6:42.4, 7:14.5.
- **4 soft whooshes** into time-lapse or orbital fly-throughs: 0:13.3, 1:14.3, 3:45.9, 6:55.1.
- **4 rumbles** under the huge shots: the winds at 0:32.0, the sea surge at 0:44.6, the lava fountain at 6:25.6, and early Earth at 7:11.4.

`sfx_kit.py level`: **PASS**. VO −14.2 LUFS, SFX −32.5 LUFS (18.3 LU under), 15 hits, no speech or pause breach (`sfx_level_v01i.json`). Whooshes 4 dB hotter breached the speech rule at 1:14 and 6:55, so they sit at −10 dB. Whether each hit suits its shot is judged by ear in Chief's review.
