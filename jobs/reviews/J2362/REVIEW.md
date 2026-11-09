# J2362 — Chief re-review of J2361 corrected 034 shot plan: FIX

7 November 2026, ~14:15 London. Grok Bot as elected Chief (`chief_relay.py status`: Chief = Grok Bot, J2362 top duty). Reviewed PR #626 at `d89fa79b30477b07d21e868f876cd52056b83fd6` (J2361 repair on top of J2353 `50fa44c23e`). Plan review only, not a rendered film.

**Decision: FIX. Do not merge PR #626 at this head, do not mark 034 shots done, do not release harvest/graphics/assembly.** A bounded zero-spend repair job and a dependent Chief re-review are queued. Nothing needs Ben. Spend £0. v03 VO, J2352 VO PASS and the J2360 Short 2 plan are untouched.

## What J2361 cleared (verified independently)

- **clip_check:** `74 rows — PASS` against accepted v03 `stt_raw.json`, `--vo-end 616.16` (CSV sha256 `e1013170…`).
- **J2359 #1/#2 (reconstructions/annotated plates):** PIA21863, PIA21864, the DEM flyover webm, PIA20589, PIA19708, PIA19857, PIA19947 and the other banned IDs no longer appear in any row. Spot check: PIA19944 orig re-downloaded, sha256 matches `SOURCE_EVIDENCE_v01.json` (`ae1a9f1e…`) and the orig is a clean LORRI frame (the NASA caption's blue arrows are not in the orig). All 64 assets carry URL, rights URL and sha256.
- **J2359 #3 (reuse):** no asset ID appears in more than two rows, counting CODE backgrounds/cutouts. Canonical dedup recorded.
- **J2359 #4 (card timing):** six explicit `source=CARD` rows; each onset is exactly 0.60 s after the previous word end; 0.40 s xfade recorded. (See remaining defect 1: duration.)
- **J2359 #5 (music):** 2.5 s full-level hold after the last word, nonzero bed through the 18 s end hold, 10.0 s fade 624.16–634.16, 2.0 s picture fade 632.16–634.16, in both MUSIC_BRIEF and R74. NOT list now names real earlier films 013–033. PASS.
- **J2359 #6 (counts/labels):** 13 CODE, 0 adjacent CODE; 3 WHO; 4 FACT; DATA/SCALE present; on-screen teaching labels <=4 words (only credit lines and the WHO sub-line are longer, which is fine). Frame 0 PIA20291 is distinct from Short `gmzaCfJF1gA` frame 0 PIA19952.

## Remaining defects (blocking)

1. **Chapter cards are on screen for 0.26–0.80 s.** R08 65.76–66.04 (0.28 s), R20 0.26 s, R33 0.28 s, R45 0.30 s, R54 0.30 s, R64 0.80 s. Five of six are shorter than their own 0.40 s crossfade, so a viewer can't read them. The v03 VO only has ~0.9 s between chapter sentences, so a 0.6 s breath leaves almost nothing. House precedent (021 v03d–v03i) holds cards 1.5–4.5 s. The onset is now correct; the hold is missing. clip_check only checks the breath, so its PASS doesn't cover this.
2. **Real moving imagery between graphics is still missing in 6 of 12 CODE→CODE gaps** (AGENTS.md: "never two code graphics back to back anywhere in the film, with real moving imagery between them"; J2359 #6: still pushes do not count). Gaps with only animated stills (or cards): R15→R17 (R16), R17→R24 (R18–R23), R38→R43 (R39–R42), R43→R48 (R44–R47), R52→R56 (R53–R55), R56→R61 (R57–R60). J2361's claim that it "placed real moving imagery between all 13 CODE rows" contradicts its own row notes, which say "animated still" for every row in these gaps. **Conditional:** R48→R52 relies only on R50 = `New Horizons Extreme Close-Up Of Pluto Surface` ogv. Confirm whether it is real motion or a NASA pan across a still LORRI mosaic. If it is a pan, that gap fails too.
3. **Evidence claims to correct (non-blocking alone, fix with 1–2):** "15 WHEN" counts one `13 JULY 2015` label as #1 & #2, so there are 14 distinct; restate it. The "<=1.58x" upscale summary contradicts SOURCE_EVIDENCE (PIA21965 1.95x). Correct it to the true max (all still <=2.35x). The lifted-navy "measured" luma has no committed frame/script, so either commit the measurement artifact or label it a target for the polish gate.

## Orbit / R28→R30 and R52→R57 ruling (decided)

- **The £0 archive/overlay route is accepted** for R30 (PIA19968 Charon + 153-HOUR clock + FACT #2) and R57 (PIA20198 → PIA19842 + 2–3 KM label). No OMNI price/spend approval; no generation.
- **I'm granting an explicit Orbit-beat exception for the 034 long: zero Orbit beats.** The playbook (§ "Longs: 1–2 beats") normally wants Orbit. We can't do it at £0 without a separately scoped, guarded spend job, and "the world does the science" holds here. The repair must remove the `[ORBIT ACTS #1/#2]` tags and the "optional `omni_034_r30…`/`omni_034_r57…`" references from CSV/MD so no worker reads them as a mint request; retype them as plain archive rows. If anyone wants Orbit back, it has to come in a new scoped spend job with the live-balance, unposted-spend and £5 Vertex margin checks.
- R30 holds 13.48 s on one still (PIA19968, three crops). Add one second distinct real source inside R30, or a native clip, so the row isn't 13.5 s of a single image.

## Handoff

Repair job and dependent Chief re-review queued (see the jobs log). J2319/J2320 holds and all picture/polish/music/SFX/perceptual gates stay in force. No merge, no render, no upload, no schedule change. CHECKS.json has the row-level evidence.
