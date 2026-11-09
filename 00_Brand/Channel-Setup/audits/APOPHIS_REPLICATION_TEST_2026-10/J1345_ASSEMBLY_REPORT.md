# J1345 — AR3 duration and totality correction

Codex worker delivery, 31 October 2026. Elected-Chief picture review required; J1321 remains held, including its recorded 2026-10-31T12:48:21Z verification time. No UAT, upload or scheduling approval. GBP0; no generation or credit spend.

AR3 v05 moves the unchanged duration graphic at 11.56–14.60 s onto the existing Gerst Earth/cloud footage (actual source 49.00–52.04 s). The approved path interval stays at source 40.00–44.52 s. At 14.60–17.055 s the approved NASA/Aubrey Gemignani totality photograph replaces the previous NOAA view. The disc and corona are free of graphic bars and labels; the existing title stays above the subject, captions below, with the 2017 archive credit. Script, title timing, duration, graphics assets and AAC audio are preserved. No prior master or manifest was overwritten.

AR1 v01, approved AR2 v06 and superseded AR3 v03 hashes freshly verified; exact protected paths/hashes are in J1345_evidence/DELIVERY.json. AAC stream hash matches AR3 v03 exactly. All 37 exact half-second tiles, full-size duration and totality samples were inspected. Chief must decide the retained totality low-detail WARN; no automated gate was modified or bypassed. This is worker evidence, not final picture acceptance.

Persistent master: `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1345_v05/ar3/owb_apophis_ar3_v05.mp4`

SHA-256: `3a2fc5b53e2cfafe4d55422f4f8ae7894ffdb81a727bf47f605e01070a58f13d`

AAC SHA-256: `7650c710d7f515bac41f8d2a333e1c4a79f60fa226ee1197930c04869b26ac51`

Duration 18.055 s; -14.7 LUFS; -1.4 dBTP.

Raw unchanged checks:
```text
WARN   0:16 row ar3_05_NHQ201708210100_s5 NHQ201708210100: low detail: edge density 0.035 < film p5 0.0402
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> /private/tmp/J1345-render-v05/ar3/qa/picture/PICTURE_QA.md, /private/tmp/J1345-render-v05/ar3/qa/picture/picture_qa_review.jpg
ar3_00_NOAA_sat_eclipse_2024_notext_s0     1.2s NOAA_sat_eclipse_2024_notext ok
ar3_01_GSFC_20171208_Archive_e002130_s1     4.3s GSFC_20171208_Archive_e00213 ok
ar3_02_GSFC_20171208_Archive_e002130_s2     6.6s GSFC_20171208_Archive_e00213 ok
ar3_03_Gerst_Earth_timelapses_2017_s3     9.3s Gerst_Earth_timelapses_2017  ok
ar3_04_Gerst_Earth_timelapses_2017_s4    13.1s Gerst_Earth_timelapses_2017  ok
ar3_05_NHQ201708210100_s5    15.8s NHQ201708210100              WARN low detail: edge density 0.035 < film p5 0.0402
ar3_06_NOAA_sat_eclipse_2024_notext_loop    17.6s NOAA_sat_eclipse_2024_notext ok
polish gate PASS: 0 of 7 rows failed, 1 to look at -> /private/tmp/J1345-render-v05/ar3/qa/polish_gate.json
SFX level PASS: VO -20.9 LUFS, SFX -37.9 LUFS, 4 hits
Loop PASS: loop_diff_masked 1.30 open_step 0.86 head [0, 0, 0, 0, 0]
```

Review images (persistent, off git):

- `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1345_v05/ar3/review_frames/contact_0.5s.jpg` — SHA-256 `7ee047b65f70f24410c9d9132c4250ffbe3f6851acc3faed8ce08799484de140`
- `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1345_v05/ar3/review_frames/duration_13.1.png` — SHA-256 `b7bab019557ece294e5012153249219875a6b1af52ddd4548a53105eec55f058`
- `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1345_v05/ar3/review_frames/frame0.png` — SHA-256 `e592742dab065bf5383415bb460cb70c815e169c71a0bfcc39e2a7fe5ebf0c55`
- `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/assembly_j1345_v05/ar3/review_frames/totality_15.2.png` — SHA-256 `21fcd17bfb8abce80d9107478ffac496e51c448229689d0486b5a6ca9b26d6dc`

The failed v04 is preserved under /private/tmp/J1345-render-v04; its raw failure reports are committed in J1345_evidence/v04_failed. Its extended panel shot triggered a gutter and duplicate source-offset check. V05 uses inspected Earth/cloud imagery and records correct in-points. Renders completed in detached tmux; logs and zero-exit receipts are ~/_desk/logs/J1345-render-v05.log and .done. Evidence collection ran in the same tmux environment. The Mini started with 5.1 GB free; authorised nas_offload.py --apply found no eligible old scratch. No NAS files were deleted or overwritten. Persistent master is in the audit delivery directory, not scratch.

Based on PR370 at 7d4f04a17 and Chief ruling c70206699 (PR371). This PR carries the prerequisite PR370 commits if those remain unmerged. Chief should review this AR3 v05 only for this correction; AR1 and AR2 are unchanged. Next: Chief reviews frame 0, all half-second tiles, duration/full-totality samples and low-detail WARN, then resolves J1345/J1321. Nothing needed from Ben.
