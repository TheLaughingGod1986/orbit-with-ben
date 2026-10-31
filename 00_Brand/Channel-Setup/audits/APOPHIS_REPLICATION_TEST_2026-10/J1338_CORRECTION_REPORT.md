# J1338 — AR2 native-detail correction

Codex, 31 October 2026. GBP0 worker delivery for separate elected-Chief picture acceptance. J1324/J1321 stay held. No UAT or publishing.

AR2 v10 replaces only frames 443–551, 14.766667–18.400 s, with sunlit real station exterior from the accepted NASA Crew-2 source, 540–543.2 s. Full 1280×720 native field is reduced to 1080×608, with coherent same-source defocused fill and a smooth push (maximum effective scale below 1×). Modules, structural members and hardware retain native detail; there is no sharpening, added grain, destructive key or unrelated plate. The original late 468 s footage remained soft even without its crop; the 549 s alternative was overexposed. Full-size previews were inspected before the first render, and the v10 motion revision was inspected again.

All other intervals are decoded directly from v08, including opening, forward loop, approved 109 m original DATA composite, South Pacific map, title and clocks. Final encoding introduces normal compression differences; compressed video identity is not claimed. Captions use the prior unchanged caption functions and locked word timestamps. Audio is stream-copied: AAC payload SHA256 d5e713d14db48a282d198087536efd10fb0ba9bcfe8669f0627f240a60b6768b matches v08 exactly. Duration 19.400 s, 582 frames. Protected AR1 v01, AR3 v09 and prior AR2 v05/v08 hashes freshly match preserved_masters.json.

Durable master: `/Volumes/data/mac-mini-archive/jobs/J1338/masters/owb_apophis_ar2_v10.mp4`
SHA256: `b8dd0285ca162d1109923395d44dff1712f7bc97f61932bbadb6b3017aab841d`
61,821,085 bytes. Local and NAS readback matched.

Unmodified picture_qa, polish, loop/finish_scan and SFX gates all exit 0. Loop difference 0.7443; opening median step 0.6208; head matches [0,0,0,0,0]. The only low-detail WARN is the preserved loop at 18.9 s; exact full-size frame supplied. Late 16.58 s has no WARN. V09 trial is preserved locally and on NAS: picture/polish/SFX passed but loop failed a 3-frame freeze at 15.93 s. V10 changes only the late push to avoid that freeze, with no noise added to mask it. Raw trial and final outputs remain in evidence.

Inspected full-size late preview, exact loop WARN and all 39 tiles of the complete 0.5 s sheet. Review images are off git at `/Volumes/data/mac-mini-archive/jobs/J1338/review_v10/`, with verified hashes and paths in review_images.json. The preview named frame0_preview is diagnostic only; actual frame0.jpg is extracted from the delivered master.

Disk preflight 8.6 GiB free; authorized nas_offload found no eligible old scratch. No protected scratch removed and no NAS overwrites/deletes. Detached sessions J1338-render (v09) and J1338-v10 completed; logs and .done receipts are in `/Users/benjaminoats/_desk/logs/`. Gates did not change. PR365 stays unchanged and unmerged.

Next: elected Chief accepts or requests changes after inspecting this delivery, including the retained loop WARN. This worker delivery does not clear J1324/J1321. No Ben action or spend.
