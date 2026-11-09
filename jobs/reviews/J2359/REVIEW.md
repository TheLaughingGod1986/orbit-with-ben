# J2359 — Chief shot-list review: FIX

7 November 2026. Codex covering as elected acting Chief. Reviewed PR #626 at `50fa44c23eba698dfd9f3c77c1803f0deea0e80e`, not a rendered film. Relay status confirmed Grok and Claude unavailable and Codex elected before this ruling.

**Decision: FIX. Do not merge PR #626 at this head, mark 034 shots done, or release picture/graphics production.** J2361 owns a zero-spend correction of the existing PR; a dependent Chief acceptance job owns the next production decision. This completes the review, not the film stage. Nothing needs Ben. Existing script and full-VO approval J2352 remain intact.

## What passed and what it proves

Reran against the reviewed CSV and accepted reconciled v03 STT:

```text
python3 00_Brand/Channel-Setup/tools/clip_check.py <034>/07_Edit-Project/shot_list_v01.csv --words <034>/02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_raw.json --vo-end 616.16
clip_check: 68 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.
```

Independent count: 1,183 word tokens, 68 rows, 13 CODE rows, no adjacent CODE rows. The document enumerates 15 WHEN markers, 3 WHO and 4 FACT cards. The source table contains 66 entries. These disagree with the dispatch/delivery summaries (46 plates, 14 CODE / 12 WHEN in the brief). Minimum marker counts are present; counts alone do not approve their design or source evidence. `CHECKS.json` records the actual rows and timing calculations.

Standalone Short `gmzaCfJF1gA` uses PIA19952 at frame 0, confirmed by its committed `06_Final-Exports/owb_sa_s7_pluto_heart_v01_meta.json`, `_assemble_standalone_shorts_v01.py` and QA cut list under `audits/STANDALONE_SHORTS_TEST_2026-10`. The proposed long PIA20291 ID differs. This is source-identity evidence, not a rendered opener gate PASS.

## Blocking findings

1. **Sourced reconstructions presented as approved plates.** NASA identifies [PIA21863](https://images-api.nasa.gov/search?nasa_id=PIA21863) (R06 0:54; R43) and [PIA21864](https://images-api.nasa.gov/search?nasa_id=PIA21864) (R28 fallback, 3:55.56) as digital-elevation-model flyovers with relief exaggerated 2–3 times. The plan also explicitly uses a DEM flyover at R38 (5:31.61). These do not meet AGENTS lesson 7's ban on sourced computer reconstructions. Remove or replace; a NASA credit and clean-looking contact sheet do not turn them into real footage. Check all remaining sources and distinguish native motion from pans over stills or renders.
2. **Annotated/noisy plate accepted as clean.** Full-size inspection of [PIA20589](https://images-assets.nasa.gov/image/PIA20589/PIA20589~orig.jpg), planned at R64, shows a central embedded arrow over a very noisy field. The blanket claim of zero embedded annotations is false. Reject this asset and re-audit the pool. Original image hashes and fetched NASA descriptions are in `NASA_EVIDENCE.json`; no media committed.
3. **Reuse accounting omits graphics inputs and duplicate identities.** PIA19948 appears at R16/R58/R68; PIA21590 at R59/R63/R67; PIA19936 at R44/R54/R56. Their three separated appearances contradict the two-appearance claim. `CHECKS.json` lists every ID present in more than two rows, including adjacent cases that need actual cut-level deduplication. PIA20291 and PIA19708 visibly show the same July 13 exposure (same framing/features; different encoding/colour), yet are tallied separately at R01/R42 and R03/R65. Canonicalize underlying images, include backgrounds inside graphics, and count continuous actual appearances, not just source-table rows. Real-body cutouts still need an explicit documented accounting policy rather than silently omitted references.
4. **Chapter-card timing not covered by the cited gate.** The CSV has zero `source=CARD` rows; `clip_check.py` checks card breath only for that source value. The first five chapter rows start 0.43–0.45 s after the preceding spoken word, while their prose says 0.60 s breath. An overlay may start later inside a row, but that exact onset is not recorded. Supply explicit card onset/end/crossfade timings and verify 0.5–0.8 s breath after a complete sentence without altering or clipping the accepted VO. The current PASS cannot certify these unstated onsets.
5. **Music ending conflicts with the playbook.** MUSIC_BRIEF and R68 prescribe a three-second fade at 631.16–634.16, whereas STUDIO_PLAYBOOK §7 and lessons §2 require 2–3 s post-word hold followed by about a ten-second music fade, full-runtime music and final two-second picture fade. Specify one consistent envelope through the 18 s hold and update both plan files. Check the NOT list against actual prior briefs: labels such as 026 Venus, 027 Mars and 028 Titan do not match the current films.
6. **Teaching/production evidence needs correction.** Reconcile 13 CODE, 15 WHEN and 66 source-table entries; preserve the three WHO/four FACT and sourced DATA/SCALE coverage. All overlay renders need distinct row filenames, <=4-word labels, animation and explicit timing. Examples such as `CRATERS UP TO 260 KM` exceed four whitespace-delimited words; shorten without changing VO. Plain #050814 has luma near 8, so calling it lifted navy is not evidence of meeting the near-black gate (mean >=28 or p95 >=50). Require representative composed-frame measurements, real-body/graded plates and proper moving separators before release. Several separators are only still pushes; they cannot establish the required real moving imagery.

## Orbit and spend decision

**No OMNI price/spend approval.** Select the zero-cost archive/overlay route for the repair plan, preserving the spoken v03. R28's current fallback includes rejected PIA21864, so it is not approved for production. J2361 must replace that input and propose a precise compliant R28/R52 plan. The dependent Chief acceptance must explicitly settle any omission of the usual Orbit acting beats before release; no character exception or model change is silently granted. A scoped paid/credit generation request would need the existing live balance, unposted-spend and £5 Vertex margin checks; none was requested or run here.

## Handoff and limits

J2361 repairs PR #626; dependent Chief re-review accepts or returns concrete defects, then queues the approved harvest/graphics workers. J2360 remains the separate Short 2 exact-lift plan. J2319/J2320 holds and all media gates remain in force. No generation, rendering, music API call, publishing or schedule changes occurred; spend £0.

This session inspected the actual tool catalog and recorded no demonstrated audio_input or moving_video_input. I inspected four original stills (PIA20589, PIA11709, PIA20291, PIA19708), read official metadata and checked plan data. I did not listen to VO, view motion or certify all source plates; confirmed blockers are sufficient to return this draft. Existing full-VO PASS is inherited, not repeated.

Both repos pulled successfully after filesystem escalation. NAS offload was attempted because free space was about 5.3 GB; it found no eligible scratch, and nothing was deleted or moved. No large render was started. Thread read to #6706033165.
