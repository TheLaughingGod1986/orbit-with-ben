2026-10-15 — Codex

# J0246: independent packaging critique — OWB 024 Light Speed

Advisory only; no final OK or release decision. I did not read the other critics. Reviewed the manifest, description v01, master script v02, abc_v03 metadata and all three actual JPEGs, including fresh 168×94 reductions. Also read LIGHT_SPEED_SHORTS_SCRIPTS_v01.md for hook context. No finished cut was watched; timing and delivered overlays remain unverified. Search suitability below is editorial judgement, not measured search demand or a fresh autocomplete check.

## Scores and concrete revisions

| Item | Score | Finding and concrete revision where below 8 |
|---|---:|---|
| Listing title | 7/10 | “What Happens If You Travel Near Light Speed?” is clear, 43 characters and answerable, but the distinguishing subject arrives at the end and the question could describe many generic relativity explainers. **Rewrite: “Why Light-Speed Travel Makes You Age Slower”** (41 characters). It moves the subject forward and states the specific contradiction. “Near” remains explicit in the opening and description; the film never promises reaching c. |
| Thumbnail A | 7/10 | At 168×94, Earth and “7 YEARS GONE?” read; the probe becomes a white speck over a bright streak. Earth dominates but does not explain whose seven years disappeared. The text is clear of the globe and duration corner, but the question does not name its subject under §2.B.1. **Rewrite: “EARTH AGES FASTER”**, yellow FASTER; retain the large Earth and enlarge the craft enough to read as a traveller, away from the bottom-right badge. |
| Thumbnail B | 6/10 | The astronaut reads immediately and the words remain legible. The plate is busy and pale, and the top-right type crowds the suit/equipment silhouette. The picture says spacewalk rather than near-light-speed journey. **Rewrite/layout: “YOUR SLOW CLOCK”**, yellow SLOW, in a clear top strip; move the astronaut below/left and simplify and grade the Earth backdrop. This requires a fresh colour check, not a waiver for the white suit. |
| Thumbnail C | 5/10 | At phone size the dish reads but most of the spindly probe disappears. “ONE-WAY TRIP” suggests a Voyager mission or a journey from which you physically cannot return. The film explicitly includes a return trip; its one-way meaning is time. **Rewrite: “EARTH MOVES ON”**, yellow EARTH, with a large Earth and a clearly readable departing craft. That would require a new composition, not just replacing the words. |
| Title + A | 8/10 | The broad travel question and specific seven-year cost add information rather than repeat wording. Strongest current pair. The unspecified reference clock is the weakness addressed above. |
| Title + B | 8/10 | The question plus personal ageing consequence makes a coherent promise without repeating the title. It gives the answer but leaves the mechanism open. If adopting the proposed title, do not retain “YOU AGE SLOWER”: that new pair would repeat itself. |
| Title + C | 6/10 | No literal repetition, but it changes the promise from consequences of fast travel to an irreversible voyage. **Pair rewrite: proposed title + “EARTH AGES FASTER”** on the revised A composition. Traveller versus home supplies the contrast. |
| Long opening, script | 8/10 | The first two paragraphs give 99%, one year aboard and seven at home before the agenda. That pays off A promptly and makes the question personal. “The danger was never the speed” adds avoidable threat language, and “In this film I will show you” loses momentum; neither requires rewriting locked VO for this advisory. Confirm actual first-30-second delivery in the cut. |
| Shorts hooks, script/packaging | 7/10 | Monday’s running-fast clocks and Friday’s particles reaching you open on useful contradictions. Wednesday answers the robot question before asking it. Frame-zero captions “TIME SLIPS”, “THE LIMIT”, and “THEY LIVE” are vague without the narration. **Concrete caption rewrites:** Monday “GPS CLOCKS RUN FAST”; Wednesday “LIGHT SPEED STAYS UNREACHABLE”; Friday “PARTICLES PASS THROUGH YOU”. These are edit proposals, not new VO; Wednesday’s picture must make the limit visible while keeping Orbit out of frame zero. The long title in the Short end lines also differs from the manifest (“Near the Speed of Light” versus “Near Light Speed”); use the exact final listing title on end cards and the actual long ID for Related. |
| Description first line + chapters | 7/10 | The one-year/seven-year first line earns the click, but the exact subject/search phrase is pushed into sentence two. The opening paragraph gives the payoff, which is appropriate here; the following paragraph inventories nearly every later surprise. **First-line rewrite:** “Near-light-speed travel changes how you age: spend one year aboard at 99% of light speed, and about seven years pass on Earth.” **Chapter rewrite:** replace “3:44 The Twin Paradox Trip” with “3:44 The Trip” to match the script’s actual chapter card. Verify against the final cut before changing timestamps. The source line, credits and honest production disclosure are already present. |

## Objective checks and package mismatch

`thumb_preview.py long <file> --out /private/tmp/j0246-<variant>.jpg --score` returned:

```text
PASS  light_speed_thumb_A_7-years-gone.jpg  saturation=169.6  near_black=27%
FAIL saturation 63 < 100 (target 120+)  light_speed_thumb_B_you-age-slower.jpg  saturation=62.5  near_black=9%
PASS  light_speed_thumb_C_one-way-trip.jpg  saturation=163.8  near_black=21%
```

These are the tool’s colour results, not a Chief PASS. B is below even the 85 pale-subject threshold. At 168×94 all three text treatments remain readable. No hook text sits under the duration badge; A’s tiny traveller/streak is closest to that risk. C has ample badge space but weak subject mass.

The manifest does **not** select abc_v03: `thumbnail` points to `j0143_v02/024_answer_j0143_v02.jpg`, and `thumbnailAbc` lists only that image and `024_tease_j0143_v02.jpg`. The social alt text describes yet another treatment, “YOU: 1 YEAR / EARTH: 7 YEARS”. Therefore this critique cannot approve the upload’s actual selected artwork. Claude/Chief must name the intended set and reconcile the manifest and alt text before applying a decision. The manifest also names rough v03; this review does not establish that it is the final delivery master. No package file was changed.

**Which would you click, and why?** A with the current title: the seven-year cost creates a specific question that the opening answers immediately; B looks like a spacewalk lesson and C like a Voyager retrospective.

**The single change that would most raise CTR:** Test a revised A reading “EARTH AGES FASTER”, with a clearly readable traveller beside Earth, so the thumbnail makes the two-clock consequence understandable at phone size. This is a test hypothesis, not a measured uplift.

Next: Claude synthesises the independent panel; Chief chooses the artwork/title and any follow-up build. No spend, YouTube changes, or protected approval undertaken.
