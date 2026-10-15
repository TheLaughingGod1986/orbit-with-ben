# 027 v01i: borrowed beds cannot pass music_gate (J0265, 15 Oct 2026)

Chief's no-spend path, step (a): try an existing Orbit bed (026 nearest-star, or 021 Saturn) instead of the retired earth-spin lift.

Both files are long enough for the 446.3 s cut:

| Bed | Duration | Where it lives |
|---|---|---|
| `nearest-star_score_bed_v01_full.mp3` | 520.4 s | 026 `05_Music` |
| `saturn-rings_score_bed_v01.mp3` | 540.0 s | 021 `05_Music` |

`music_gate.py` cannot PASS either one under 027:

- **own.** The bed is not in 027's `05_Music`, and it has no plan written for this film.
- **reused.** Copying either file into 027's `05_Music` leaves the original in the other film. The gate hashes every other film's bed and scores an identical file at similarity 1.0. FAIL is 0.8. The retired earth-spin lift is the same kind of fail (0.80–0.82) and stays retired.

No other Orbit bed is free of this. Each one is some film's own score. Step (b) is the take that can pass: a new bed, capped at 375 s so the charge stays under 5,200 credits (about 13.75 credits/s → about 5,156).
