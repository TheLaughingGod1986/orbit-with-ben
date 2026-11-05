# J1834 — real ISS acquisition candidate

3 November 2026. Codex covering. GBP0. **Acquisition evidence delivered; pending elected-Chief moving-picture and creative review. J1471 input hold is NOT satisfied.** No master edit or full Shorts ship PASS.

Read J1833, h37 C4, J1317, J1321 metadata, PR380 diagnostics at d0b04b5e0, current J1471/J1356 holds. No earlier J1834 acquisition existed. Both repos pulled; required board/thread/inbox read. Disk about 8 GB free; prescribed NAS offload found no old eligible scratch. New retained data about 186 MB, below 2 GB. Only ONE source asset acquired. No additional asset was selected from the two saved search result lists. Existing 351–374 s cache untouched.

## Candidate

NASA Crew-2 reel, exact ID/official URLs/metadata/usage receipt in DELIVERY.json. Official metadata describes the 8 November 2021 Endeavour departure/fly-around; NASA JSC collection, no third-party copyright designation found in the captured asset metadata. General NASA usage terms captured locally; no NASA endorsement implied. Metadata AVAIL:Owner is an internal upload owner, not asserted here as a copyright attribution. Candidate is source T=545 s, preroll [544,545), opening [545,547.4). Native source cache is 540–600 s, 1280x720 at 60000/1001 fps; input seek and stream-copy preserve native encoded video. No speed change. See ffprobe receipts and exact commands.

Sharp foreground: crop 460x460 at x450/y180; scale to1080x1080 (2.347826x); place y420; alpha feathers top/bottom over48 output pixels. Moving fill: native720x720 centre crop x280/y0, scale1.5x to1080square, reflected edge extension to1920height, boxblur30:3. Full recipe in feather_metrics.json/feather_probe.py. No artificial motion, added noise, generated media, text or audio. Distinct moving preview and 3.4s preroll/open preview are in persistent cache; hashes in DELIVERY.json. The source is NOT a finished Short.

## Measurements

Unchanged gate_shorts_open.py frame0_diff_0_1_5s called on actual1080x1920 previews. Full-plate T542/544/551/554/557: 0.69/0.71/0.24/0.25/0.21. Tight square crop T542/543/544:1.25/1.38/1.47. Feathered T544:1.47; T545:**1.54**, threshold1.50. Ten previews total. Earlier full-plate T544 fails picture/polish for a horizontal seam; retained as rejected diagnostic, never waived.

Final raw output:

```
WARN   0:01 row ISS_candidate Crew2_545: sharpness: upscaled 2.35x, may look soft
picture QA PASS: 0 of 1 cuts fail, 1 to look at
ISS_candidate     1.2s Crew2_545                    ok
polish gate PASS: 0 of 1 rows failed, 0 to look at
```

No WARN overridden. These source-preview checks do not cover captions, VO, score, SFX, loop composite or full Shorts opening gates.

## Actual inspection and unresolved review

Viewed native544 full-size still, exact portrait frame0 full size, 270x480 phone frame0, all ten quarter-second sheet tiles, and adjacent preroll/open seam stills at preview0.967/1.001. Exact quarter-second JPEGs plus last decoded frame2.383 are retained; 2.4 is the exclusive end. No shot transition is visible in these samples. **No actual moving playback or audio audition performed in this run.** Decode/measurement/stills are not claimed as moving review.

The tighter crop shows station hardware over Earth but loses the familiar whole-station silhouette; Dragon is partly cropped at the feather boundary and the fill is very soft. Recognition, framing coherence and softness therefore remain material creative concerns despite automated PASS. Elected Chief must actually view feather_candidate_T545.mp4, phone_T545.mp4 and preroll_and_open_T545.mp4, examine the sharpness WARN and provenance, then approve or reject the exact hash/interval/recipe. Do not use the1.54 metric as creative acceptance. If rejected, this finite investigation does not establish that all NASA footage is unsuitable.

J1471 remains sole correction worker after J1468; J1356 owns full moving/audio review, pace WARN and final-watch readiness. Original masters/manifests, accepted remaining picture, repaired score, h40 words/clocks/durations, AR2v10/AR3v09 exclusion, failed gates and Ben/date/credit holds remain. No spend, upload, schedule, retitle, privacy, Buffer or Ben-watch release.
