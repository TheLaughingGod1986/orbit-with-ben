# 027 rough bed lock (J0265, 15 Oct 2026)

Chief ruling (a), #99, 11:30Z. This file is the lock. It is not a PASS of the picture.

| | |
|---|---|
| Bed | `05_Music/earth-spin_score_take2_straight_v01j.wav` |
| Plan | `earth-spin_score_take2_straight_v01j_plan.json` |
| Waiver | `music_gate_v01j_chief_waiver.json` (reused only, this filename only) |
| Cut | `OWB UAT/027_EarthSpin_rough_v01j.mp4` |
| sha256 | `1eebce5b235cfe31f03b5284fc1c347547096d943f3262514f3d12088f2b666d` |
| Length | 446.3 s |
| SFX | PASS (`06_Sound-Effects`, house kit, no spend) |
| Spend | none further until the 30 Oct ElevenLabs reset |

`music_gate.py` reads the waiver and moves that reused line to `waived`. Own, brief, gap and length still fail the run. Pace stays a warning (measured 54.5 BPM on the ducked stem; the full-level fit reads 80, inside 76–88).

Confirming run, 15 Oct: `music_gate_v01j_locked.json` is PASS. `--others` was only the short Mars stem (the known 0.831). The full compare stays in `music_gate_take2_straight_v01j.json`.

Picture on v01j is v01i with this bed and the SFX stem. v01k is that same cut with fine film grain (`noise=alls=4:allf=t`, audio copied). `polish_gate` PASS, 0 of 88 rows failed. It is `OWB UAT/027_EarthSpin_rough_v01k.mp4`, sha256 `4f41806919ef569220c15cd293718c83a900b8be13c508a6479b047980c01ec9`. v01j stays the locked listen copy. Corner credits are the next polish. They are not on v01j or v01k. The NAS share still hangs, so the iCloud UAT files are the masters of record.
