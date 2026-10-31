# J1324 — AR2 v08 correction delivery

Codex, 31 October 2026, GBP0. Worker delivery for elected-Chief picture acceptance. J1321 remains held. No UAT, upload or scheduling.

Changed intervals: 0.000–2.400 and 14.766667–19.400 s (late 14.766667–18.400; forward loop 18.400–19.400). Native ISS picture now uses its own defocused fill, a global exposure curve and a continuous camera push. No unrelated Earth, drawn geometry or luma key. Late footage is cropped around the station with maximum sharp-view upscale about 1.45×. Accepted NASA source: opening 447.2–449.6, late 468–471.2, loop 446.2–447.2 s. Full-size previews inspected before rendering.

The approved 109 m DATA original composite, South Pacific map and all other picture intervals are decoded directly from v05 with their original clocks. Final picture is re-encoded with house fine temporal grain; unchanged input frames are hashed in render_receipt.json, not claimed as compressed-video identical. Script, captions, titles, facts, audio and 19.400 s duration retain their wording/timing. Exact AAC payload equality is verified in audio_identity.json. AR1 v01, AR3 v09 and AR2 v05 full hashes freshly match in preserved_masters.json.

Durable master: /Volumes/data/mac-mini-archive/jobs/J1324/masters/owb_apophis_ar2_v08.mp4
SHA256: e74c66788c68dd968bcfed7688c9def47c0a17a6d88355ae11112cf15c6375a7
Bytes: 82150770. Local and NAS readback matched.

Unmodified picture_qa, polish_gate, loop/finish_scan and SFX all exit 0. Raw reports, native frame0.jpg, late_16s.jpg and full contact_0.5s.jpg are in j1324_evidence. Loop difference 0.7244; opening step 0.6631; head matches [0,0,0,0,0]. One late-shot low-detail WARN at 16.6 s remains for Chief visual acceptance. No override or suppressed failure.

V06 failed same-stretch reuse and opening freeze. V07 passed picture/polish/SFX but failed freeze. Both trials and separate NAS masters remain. V08's continuous camera push plus house grain passes the unchanged checker.

Required nas_offload found no eligible scratch; 5.2 GiB free initially. No protected scratch was removed. Sparse worktree /private/tmp/J1324-wt, branch codex/J1324; scratch /private/tmp/J1324-render. Detached render and gates completed exit 0: /Users/benjaminoats/_desk/logs/J1324-v08.done, J1324-v08-render.log, J1324-v08-gates.log. No duplicate process.

Next: elected Chief inspects the full-size late WARN and all tiles before picture acceptance. This delivery does not approve a film stage or reopen J1321. No Ben action, spend or publishing.

Review images are durable at /Volumes/data/mac-mini-archive/jobs/J1324/review_v08/; review_images.json records freshly matched SHA256 hashes. Images stay off git.
