# OWB:064 Short 2 — Script Draft v03 (`064_short02_venus_vs_uranus_script_v03.md`)

- **Status: DRAFT, NOT LOCKED.** Written by `gemini` (J3916) after the J3914 reviewer FIX (`jobs/reviews/J3914/REVIEW.md`, PR #1394 commit `ca9429fd55`). Supersedes `064_short02_venus_vs_uranus_script_v02.md` (kept unchanged for history; v02 is retired). No VO take, no Flow/Vertex, no spend (£0), no upload, and no schedule change. Lock and any bounded VO authorisation belong to the dependent reviewer and elected Chief.
- **Concept kept:** Option A, Venus vs Uranus. Option B1 is not selected.
- **Duration band (resolved in J3914):** **16.0–19.0 s** (Ben's 19 Nov 2026 rule, `studio/RULES.md` line 189, `gate_shorts_open.py` `DUR_BAND = (16.0, 19.0)`). Variant v02b is the line; v02 (22–27 s) is retired.
- **Listing title (draft, unchanged):** `Why Is Venus 464°C While Uranus Drops to −224°C?`

## What changed from v02b (J3914 FIX — one word only)

1. **Line 2:** Restored NASA's `"true"` qualifier to match the verified C5 quote (`"As an ice giant, Uranus doesn't have a true surface."`):
   - v02b: `Uranus has no surface; that's its coldest air.`
   - v03: `Uranus has no true surface; that's its coldest air.`
2. **Lines 1 and 3:** Unchanged word-for-word from v02b. No other spoken words were added, removed, or altered.

## Narration v03 (16.0–19.0 s target; single active variant)

Why is Venus's surface 464 degrees Celsius, while Uranus's air drops to minus 224?

Uranus has no true surface; that's its coldest air.

On Venus, thick carbon dioxide air traps heat in a runaway greenhouse.

## Text metrics (recomputed from v03 above; estimates, not measurements)

Method (identical to v02): lines joined with a single space for ElevenLabs character count; numbers expanded as Ben speaks them (`464` → `"four hundred and sixty-four"`, `224` → `"two hundred and twenty-four"`). Rates use the v01 calibration from the locked 064 VO: `15.8 / 14.66 / 13.8` expanded chars/s. Fixed allowance: `0.08 s` lead + `2 × 0.18 s` breaths + `0.85 s` loop tail = `1.29 s`. Payoff onset = start of `"traps heat"` (`0.08 s` lead + `2 × 0.18 s` breaths + prefix expanded chars / `14.66`).

| | v02 (retired) | v02b (superseded) | v03 (active) |
|---|---:|---:|---:|
| Raw characters (ElevenLabs input, single-space join) | 284 | 200 | 205 |
| Written words | 49 | 34 | 35 |
| Expanded spoken words | 60 | 40 | 41 |
| Expanded characters | 381 | 248 | 253 |
| Est. total, fast / mid / slow (s) | 25.4 / 27.28 / 28.9 | 16.99 / 18.21 / 19.26 | 17.30 / 18.55 / 19.62 |
| Est. payoff onset at mid (s, % of runtime) | 23.84 (87.4%) | 14.97 (82.2%) | 15.31 (82.5%) |

- With paragraph breaks (`\n\n`) included, raw input length is 207 characters.
- Mid-rate estimate is **18.55 s** (**≤ 19.0 s**, inside the `16.0–19.0 s` band); fast is **17.30 s** (inside band); slow is **19.62 s** (0.62 s above the 19.0 s warn edge, well below the 40.0 s hard fail).
- Payoff onset at mid is **15.31 s (82.5% of runtime)**, meeting the ≥ 70% target.
- No take exists yet; none of these durations has been measured on audio.

## Sources and quote check (completed in J3914)

- Claim and verbatim quote verification is already recorded in `064_short02_QUOTECHECK_v02.md` (commit `ca9429fd55`, J3914): Gemini (`gemini-4-argon-high`) verified C1–C9 verbatim with 0 flags, and `claudecode` directly fetched all three NASA URLs and confirmed every quote holds.
- The single J3914 reviewer flag — C5 (`"As an ice giant, Uranus doesn't have a true surface."`, `https://science.nasa.gov/uranus/facts/`) missing `"true"` in v02b Line 2 — is now resolved in v03 Line 2. Because no other spoken words changed from v02b, per `jobs/reviews/J3914/REVIEW.md` the dependent reviewer can lock v03 without another source run.
- Description/listing note unchanged from `064_short02_QUOTECHECK_v02.md`: the NSSDC Venus fact sheet backs the spoken `464 °C` figure and must be cited when the listing job rewrites the draft manifest after lock. Shot-provenance fixes in `SHORT02_PLAN_AND_SCRIPT_v02.md` §4 (R01/R02/R08 missing paths, R03/R06 Veo CGI re-plan) remain open for assembly and do not block script lock.
