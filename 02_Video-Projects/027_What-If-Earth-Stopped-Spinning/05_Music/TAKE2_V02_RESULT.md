# 027 take 2, v01j (J0265, 15 Oct 2026)

**Locked.** Chief, 15 Oct 2026 11:30Z, ruling (a): accept this bed. Waiver `music_gate_v01j_chief_waiver.json`. The reused FAIL against 025's short Mars stem is waived for this file only. No further ElevenLabs spend on it until the 30 Oct reset.

Listen: `OWB UAT/027_EarthSpin_rough_v01j.mp4` (sha256 `1eebce5b235cfe31f03b5284fc1c347547096d943f3262514f3d12088f2b666d`). Same bytes as `/private/tmp/027_EarthSpin_rough_v01j.mp4`. The NAS copy was not made: the share still hangs on `ls` (J0267). The iCloud UAT file is the master of record.

## What was tried

**(a) Borrowed beds.** 026 nearest-star (520 s) and 021 Saturn (540 s) cannot pass `music_gate` under 027. Each file still lives in the other film's `05_Music`, so a copy scores similarity 1.0 (FAIL at 0.8). See `BORROWED_BEDS_v01i.md`.

**(b) New take, inside the cap.** API-key account had 5,275 credits. One `music_v2` take, 375.04 s (`earth-spin_score_bed_v02.mp3`). Charged 5,156 (375 × 13.75). 119 left. Under Chief's 380 s / 5,200 cap. Logged in `ai_spend` and `04_Audio/elevenlabs_ledger.jsonl`. No second take: another 375 s needs about 5,156.

The 375 s take is time-fit to 452 s with one `atempo` (0.830), not looped (`_fit_score_take2_v02.py`). Chapter times in `BED_PROMPT_v02.txt` are the 375 s clock, so × 452/375 they land on the v01i cards. v01j plays that fit straight, ducked −22 dB, with the house SFX stem. Picture is v01i, copied.

## Gates

| Check | Result |
|---|---|
| SFX level | PASS. VO −14.2 LUFS, SFX −32.5 LUFS, 15 hits |
| Mix | −13.7 LUFS |
| music_gate on the full-level fit | FAIL reused only: `mars-robot_score_bed_v01.mp3` 0.825. Measured 80 BPM, inside Pace 76–88 |
| music_gate on the ducked v01j stem | FAIL reused: same Mars stem, 0.831. WARN pace 54.5 BPM (the tracker on the −22 dB stem; the full-level fit reads 80) |
| locked re-run (`music_gate_v01j_locked.json`) | PASS. The 0.831 reused line is waived. Pace stays a warning. `--others` was only the short Mars stem |

Similarity of the fit against every other score bed: the only one at 0.8 or more is 025's **short** `mars-robot_score_bed_v01.mp3` (0.825). The full Mars beds are 0.435 and 0.429. Next highest are short stems at 0.767 (024 v01b, 026 v01). Saturn is 0.279. The retired earth-spin lift is 0.648.

iCloud placeholders in OWB UAT (Saturn VO listens, `jupiter-music.mp3`, and others) could not be read. Those are WARNs, not the FAIL.

## Where to listen

`OWB UAT/027_EarthSpin_rough_v01j.mp4`

sha256 `1eebce5b235cfe31f03b5284fc1c347547096d943f3262514f3d12088f2b666d` (matches `/private/tmp/027_EarthSpin_rough_v01j.mp4`, 275,563,672 bytes). NAS was left alone: J0267's copy of v01i was still hung on the share.

## Ruling

Chief accepted it (15 Oct 11:30Z). See `BED_LOCK_v01j.md`. 119 credits still cannot buy another bed. Ben's "83% remaining" is still a different account from this API key; nothing here needs him.
