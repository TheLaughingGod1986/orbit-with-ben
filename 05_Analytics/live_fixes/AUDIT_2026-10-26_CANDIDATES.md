# Audit rules — live re-cut candidates (Orbit Auditor, 26 Oct 2026)

Rules: AGENTS.md → *Audit rules (Orbit Auditor, 26 Oct 2026)*. **Candidates only.** Nothing here is re-cut, swapped or
re-uploaded by the rules change. Any fix is its own job with Chief's OK, and the Never list holds (no file swap on an
existing id; a weak Short is a result, not a re-upload). Anything Ben OK'd and scheduled before 26 Oct ships as is
(*Keeper score* rule 7, PR #287).

Source: the Orbit Auditor's 26 Oct audit (notes and frames on the box at `/workspace/audit26/f`), re-measured with
`00_Brand/Channel-Setup/tools/plate_check.py` on the public 720p (longs) and 360p (Shorts) downloads on 26 Oct.

## Long films

| Video | Repeated plates (rule 1) | End hold vs opening (rule 2) | Burned-in SUBSCRIBE (rule 3) |
|---|---|---|---|
| Sun `h8HGfyShEHI` *Is the Sun Getting Brighter?* | grey-disk plate in 8 beats (21, 50, 120, 224, 343, 404, 462, 493 s); 23 more plates in 2–3 beats each, e.g. the opening limb plate at 5.5 and 153.5 s, the Earth disk at 377.5 and 436.5 s | SSIM 0.987 (497.5 s vs 4.5 s): FAIL | OCR at 239–241 s (~4:00): FAIL |
| Venus `VBaYRPp85Sw` *What Happened to Venus?* | one plate at 229.5, 399.5 and 475.5 s; another at 55.5 and 164.5 s | SSIM 0.999 (505.5 s vs 0.5 s): FAIL | lower-right cue, OCR at 215–217 s (~3:35): FAIL |

The Sun thumbnail test runs to Sun 1 Nov (`05_Analytics/tests/THUMB_LEDGER.json`); don't touch the Sun long before it ends.

## Shorts (12–24 Oct)

The audit found no last card on these: the ending is only spoken, with no long title and no long id on screen (rule 7).
`plate_check.py short` measures (captions = share of 1 s samples with OCR text; Orbit = visor heuristic, eyeball it):

| Short | Runtime | Captions | Orbit | Notes |
|---|---|---|---|---|
| `Cka7_TVVOUQ` Saturn's Rings Are Already Falling (12 Oct) | 23.96 s | 47%: WARN | big at 1.5–4.0 s: WARN | Orbit as hero early (audit: big by 2.5 s) |
| `buaOI3QGm7U` Could a Robot Survive Falling Into Jupiter? (14 Oct) | 25.46 s | 100% | in 60% of samples: WARN | |
| `1NeQFVnzO2Q` Why No Black Dwarf Exists Yet (16 Oct) | 26.92 s | 41%: WARN | — | captions don't run the whole way |
| `23KZK7OjsEE` Jupiter Has No Ground (17 Oct) | 22.46 s | 100% | — | |
| `y-SPHQ0-VjQ` Why Is the Sun Getting Brighter as It Runs Out of Fuel? (19 Oct) | 26.36 s | 100% | 52%: WARN (likely the orange Sun, check by eye) | long title on screen at the end, no long id |
| `lbW2iQ9YvqA` Saturn's Rings Are on a Clock (20 Oct) | 23.66 s | 95% | — | |
| `n_4XskX0yZk` Could a Robot Survive Touching the Sun? (21 Oct) | 24.22 s | 80% | — | |
| `82Ao0v5XiQI` Are Saturn's Rings Younger Than Saturn? (22 Oct) | 25.02 s | 81% | — | |
| `2e-giqFmfy8` Why Didn't Earth Freeze Under a Dimmer Young Sun? (23 Oct) | 23.22 s | 100% | — | long title on screen at the end, no long id |
| `vlkj8RQKmH8` Why Does a Day on Mercury Last Two of Its Years? (24 Oct) | 20.48 s | 100% | — | under 22 s, but a J0216 test Short (exempt until 20 Nov) |
