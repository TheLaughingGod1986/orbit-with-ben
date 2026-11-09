# J1321 — AR2 and AR3 picture corrections

31 October 2026 · Codex · GBP0. Assembly delivery for elected-Chief review. **Cohort held from UAT/upload/scheduling. No picture approval is claimed here.**

## Changes

- AR1 v01 and both old v02 masters retain their recorded SHA-256 values (verified by deliver_j1321.py). No scripts, VO, facts, titles, graphics assets, timing, score or upload manifests changed.
- AR2 v06 replaces the non-DATA station drawing with real NASA Crew-2 fly-around imagery at the opening, final spoken interval and loop return. The approved 109 m DATA sequence and its underlying drawing remain exactly as before. A sharp 1080×608 view (0.844× native scale) sits over a feathered, blurred moving fill, avoiding excessive upscaling.
- AR3 v03 puts the approved path sequence over moving Gerst Earth footage at 7.04–11.56 s. It no longer crosses an eclipse disc or corona. The adjacent 2017 eclipse sequence retains its date and NASA/Aubrey Gemignani attribution; after the duration graphic clears, the eclipse is unobscured. The existing NOAA crop remains unchanged.
- AAC stream hashes match the corresponding old masters exactly. All original audio, including its existing music state, is preserved. No fresh audio or credit spend.

## Source identity and visible in-points

- NASA asset: `jsc2021m000259_SpaceX_Crew-2_Flight_Day_3_Highlights`. NASA metadata describes the 8 November 2021 Endeavour return and fly-around. Metadata is preserved in `J1321_evidence/NASA_SOURCE.json`.
- Collection: https://images-assets.nasa.gov/video/jsc2021m000259_SpaceX_Crew-2_Flight_Day_3_Highlights/collection.json
- Acquired `~orig.mp4` (1280×720), source interval 351–374 s, into the local cache. Viewed source frames at 356, 360 and 372 s: real station modules and truss over Earth, no Discovery lettering, Bahamas image or KSC Q&A.
- Actual full-reel source in-points: opening **357 s**, final station shot **368 s**, loop preroll **356 s**. The two spoken footage stretches start 11 s apart. Cut metadata records these actual offsets; the loop retains the existing separately identified preroll convention. Other pre-existing cuts retain inherited metadata.
- Cached segment: `/Users/benjaminoats/_desk/cache/J1321/crew2_351_374.mp4` · SHA-256 `593da478539edb1ea5c6038268704f31abeca4493393dbe9ffab159151490579`.
- AR3 path background: existing verified pool `iss/Gerst_Earth_timelapses_2017.webm`, source 40.00–44.52 s; actual in-point recorded in cuts.json. Frame at 10 s inspected full-size.

## Delivery and unchanged gates

| Cut | Duration | Picture / polish / SFX | Loop |
|---|---:|---|---|
| AR2 | 19.4 s | PASS / PASS / PASS | loop_diff_masked 0.85 open_step 0.53 head [1, 1, 1, 1, 1] |

Master: `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1321_delivery_v02/ar2/owb_apophis_ar2_v06.mp4`
SHA-256: `6d517aad6c61a0f12d67b4f2f7990f94ea165e17e01055b56873e89415bf8e67`
AAC SHA-256 (identical to v02): `d5e713d14db48a282d198087536efd10fb0ba9bcfe8669f0627f240a60b6768b`
Mix: -14.3 LUFS; -1.4 dBTP.

Review image: `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1321_delivery_v02/ar2/review_frames/ar2_v06_frame0.jpg` (193517 bytes), SHA-256 `0cfcfd21ea56383aa20a25a24b91e99bf65e0d9a49fbf41d0f625d32578e2167`.
Review image: `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1321_delivery_v02/ar2/review_frames/ar2_v06_contact_0.5s.jpg` (830502 bytes), SHA-256 `9f01c073a115102702f979df2529dff08cc82626d1bf618acb914077b658cf00`.

Raw unchanged gate output:
```text
WARN   0:19 row ar2_06_Crew2_flyaround_loop Crew2_flyaround_loop_preroll: low detail: edge density 0.024 < film p5 0.0283
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> /private/tmp/J1321-render-v06/ar2/qa/picture/PICTURE_QA.md, /private/tmp/J1321-render-v06/ar2/qa/picture/picture_qa_review.jpg
ar2_00_Crew2_flyaround_s0     1.2s Crew2_flyaround              ok
ar2_01_GSFC_20171208_Archive_e002130_s1     3.8s GSFC_20171208_Archive_e00213 ok
ar2_02_GSFC_20171208_Archive_e002130_s2     6.7s GSFC_20171208_Archive_e00213 ok
ar2_03_GSFC_20171208_Archive_e002130_s3     9.6s GSFC_20171208_Archive_e00213 ok
ar2_04_Gerst_Earth_timelapses_2017_s4    12.9s Gerst_Earth_timelapses_2017  ok
ar2_05_Crew2_flyaround_s5    16.6s Crew2_flyaround              ok
ar2_06_Crew2_flyaround_loop    18.9s Crew2_flyaround_loop_preroll WARN low detail: edge density 0.024 < film p5 0.0283
polish gate PASS: 0 of 7 rows failed, 1 to look at -> /private/tmp/J1321-render-v06/ar2/qa/polish_gate.json
SFX level PASS: VO -19.7 LUFS, SFX -38.1 LUFS, 4 hits
```

| AR3 | 18.055 s | PASS / PASS / PASS | loop_diff_masked 1.30 open_step 0.86 head [0, 0, 0, 0, 0] |

Master: `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1321_delivery_v02/ar3/owb_apophis_ar3_v03.mp4`
SHA-256: `caf3f3b0e2290c703d0cb4d33d587580eaaf43e8ef83ec87e258af1727474ea7`
AAC SHA-256 (identical to v02): `7650c710d7f515bac41f8d2a333e1c4a79f60fa226ee1197930c04869b26ac51`
Mix: -14.7 LUFS; -1.4 dBTP.

Review image: `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1321_delivery_v02/ar3/review_frames/ar3_v03_frame0.jpg` (444593 bytes), SHA-256 `791c24fe0a0bfc323230ca4db08c1a3bfdc6ef13a3cbbc217ec6c1fabe8b442c`.
Review image: `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1321_delivery_v02/ar3/review_frames/ar3_v03_contact_0.5s.jpg` (903511 bytes), SHA-256 `33ce76bd5d67f631de153900e35d6aaf8909514e1c2d3bb0ec992b59acf3fc63`.

Raw unchanged gate output:
```text
WARN   0:13 row ar3_04_NHQ201708210116_s4 NHQ201708210116: low detail: edge density 0.0354 < film p5 0.0405
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> /private/tmp/J1321-render-v03/ar3/qa/picture/PICTURE_QA.md, /private/tmp/J1321-render-v03/ar3/qa/picture/picture_qa_review.jpg
ar3_00_NOAA_sat_eclipse_2024_notext_s0     1.2s NOAA_sat_eclipse_2024_notext ok
ar3_01_GSFC_20171208_Archive_e002130_s1     4.3s GSFC_20171208_Archive_e00213 ok
ar3_02_GSFC_20171208_Archive_e002130_s2     6.6s GSFC_20171208_Archive_e00213 ok
ar3_03_Gerst_Earth_timelapses_2017_s3     9.3s Gerst_Earth_timelapses_2017  ok
ar3_04_NHQ201708210116_s4    13.1s NHQ201708210116              WARN low detail: edge density 0.0354 < film p5 0.0405
ar3_05_NOAA_sat_eclipse_2024_notext_s5    15.8s NOAA_sat_eclipse_2024_notext ok
ar3_06_NOAA_sat_eclipse_2024_notext_loop    17.6s NOAA_sat_eclipse_2024_notext ok
polish gate PASS: 0 of 7 rows failed, 1 to look at -> /private/tmp/J1321-render-v03/ar3/qa/polish_gate.json
SFX level PASS: VO -20.9 LUFS, SFX -37.9 LUFS, 4 hits
```

## Verification and handoff

- Viewed both 0.5 s sheets in full and AR2 frame 0, plus AR3 10.0/13.0/14.2 s full-size samples. All 39 AR2 and 37 AR3 tiles exported from exact frame indices (every 15 frames at 30 fps); frame 0 exports are 1080×1920. Media and review JPEGs stay off git; all paths and hashes are in DELIVERY.json.
- WARNs retained for Chief: AR2 loop low detail; AR3 eclipse low detail. No failed check was overridden or changed.
- Superseded AR2 v03 exposed a split seam in the DATA interval after its underlying drawing was removed; it was restored. V05 exposed the footage-fill seam in the loop tail; v06 feathers that boundary. Raw failed reports remain in `J1321_evidence/ar2_v03_superseded` and `ar2_v05_superseded`. V04 was an intermediate before separating the actual footage stretches. All versions remain preserved.
- Detached sessions completed: J1321-render, J1321-ar2-v04, J1321-ar2-v05, J1321-ar2-v06. Final logs and receipts: `~/_desk/logs/J1321-ar2-v06-codex.log` / `.done` and `~/_desk/logs/J1321-render.log` / `.done` (the older pre-existing receipt was preserved as J1321-render-0814.done). No duplicate render remains active.
- Master delivery is under the persistent audit directory, not /private/tmp. Disk preflight ~10 GB; NAS offload found no eligible scratch. No NAS files were changed. Partial export attempt `assembly_j1321_delivery_v01` is preserved; complete checked delivery is `assembly_j1321_delivery_v02`.
- Next: elected Chief inspects these corrected frames, the two WARN frames, and decides cohort picture approval. No Ben action required. No upload, schedule, social or YouTube state changes.
