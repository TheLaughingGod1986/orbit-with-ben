# J1321 worker delivery — AR2 v05 / AR3 v09

31 October 2026 · codex · GBP0. Parked for elected-Chief picture review. The cohort remains held from UAT, upload and scheduling. No worker final OK, PASS or merge.

## Corrections

- AR1 v01 and original AR2/AR3 v02 masters remain byte-identical to the Chief review hashes (`j1321_evidence/preserved_masters.json`). Prior manifests and ASSEMBLY_REPORT.md are untouched.
- AR2 opening and forward loop preroll now show actual ISS footage from the NASA Crew-2 return highlights. Native 1280×720 frames retain their original RGB and are resized to 1080×608 (0.844×), feathered over the existing Earth plates. Later station footage is a separately verified angle. No final luma key, invented geometry, Discovery, Bahamas or KSC press footage.
- The approved 109 m / football-field graphic and its composite are preserved. The flat station drawing remains only beneath that approved DATA graphic, never in the non-DATA opening, late shot or loop. All 86 approved graphic-frame hashes are recorded.
- AR3’s approved path and duration graphics keep their original VO timing and now sit over moving Earth-facing footage. Path/bar background: Gerst source 40.0–47.56 s, cropped below the horizon at 540×960→1080×1920 (2.0×). Date background: a separate Earth-only crop at source 100.0–103.8 s (1.333×).
- The unobscured 2017 corona is shown at 6.20–7.04 s immediately before the path; both `2017` and `NASA/Aubrey Gemignani` are present. NOAA opening/loop crop and its logo exclusion are unchanged.
- Exact compressed AAC audio matches v02 for each Short, verified separately. No VO, script, title, facts, music or duration changes.

## Final masters and raw gates

### AR2
- Durable master: `/Volumes/data/mac-mini-archive/jobs/J1321/masters/owb_apophis_ar2_v05.mp4`
- SHA-256: `78176f3830a462cefdef2788884dc763534d0ccf70e3d0fc9bb06954ab6a2778`
- Duration: 19.4 s; loudness -14.3 LUFS; true peak -1.4 dBTP.
- Unmodified picture_qa exit 0, polish exit 0, SFX exit 0; loop: loop_diff_masked 3.64 open_step 3.47 head [0, 0, 0, 0, 0].
- Raw reports: `j1321_evidence/ar2_PICTURE_QA.md`, `ar2_polish_gate.json`, `ar2_loop_stdout.txt`, `ar2_sfx_level.txt`.
- Exact audio identity: `j1321_evidence/ar2_audio_identity.json`.

### AR3
- Durable master: `/Volumes/data/mac-mini-archive/jobs/J1321/masters/owb_apophis_ar3_v09.mp4`
- SHA-256: `0aee8edb88969b417d66aa71c4b3a074c7cc0ee1ea04773110aec56997f35b5a`
- Duration: 18.055 s; loudness -14.7 LUFS; true peak -1.4 dBTP.
- Unmodified picture_qa exit 0, polish exit 0, SFX exit 0; loop: loop_diff_masked 1.30 open_step 0.86 head [0, 0, 0, 0, 0].
- Raw reports: `j1321_evidence/ar3_PICTURE_QA.md`, `ar3_polish_gate.json`, `ar3_loop_stdout.txt`, `ar3_sfx_level.txt`.
- Exact audio identity: `j1321_evidence/ar3_audio_identity.json`.

## Source and review evidence

NASA source identity, native size, exact URL, verified visible in-points, full-source hash and NAS backup path are in `j1321_evidence/source_provenance.json` and the saved API metadata. Source: https://images.nasa.gov/details/jsc2021m000259_SpaceX_Crew-2_Flight_Day_3_Highlights . Full ISS is visibly verified at 447.2 s and 468 s; Dragon shots are excluded.

`ar2_v05_frame0.jpg` and `ar3_v09_frame0.jpg` are 1080×1920, q85. Their 0.5-second sheets use four columns, 252×448 tiles and q80 JPEG. Each sheet is below 1.5 MB. Chief must inspect all tiles plus the low-detail WARNs at full size. Earlier failed trials and their raw outputs remain under `j1321_evidence/trials/`; none is substituted for a final gate.

## Reproduce and handoff

Clean job worktree: `/private/tmp/owb-J1321`, branch `worker/J1321-picture-fixes`. New assembler: `assemble_j1321.py` (derived from the preserved original assembler, refuses AR1 and existing output masters). New evidence exporter: `export_j1321.py`. Gates themselves are unmodified; no reviewed-ok overrides or disabled jitter checks. Temporal offsets now name real footage positions; still sources carry no invented offsets.

Final render receipt: `/Users/benjaminoats/_desk/logs/J1321-ar3-v09.done`; log has the same stem. Scratch: `/private/tmp/J1321-render/`. Both masters and full NASA source are on the NAS and SHA-256 verified. Disk preflight was 11 GiB; authorised nas_offload found no eligible 48-hour-old scratch. No NAS file was deleted or overwritten.

Next: elected Chief reviews the corrected station, map, adjacent corona, native frame-0s and all 0.5-second tiles. Cohort stays held. Nothing required from Ben.
