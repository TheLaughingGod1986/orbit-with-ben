# J0154 — Chief-requested source correction, 14 Oct 2026

Codex covering. Advisory handover only; Chief holds the overlay decision.

Chief's 12 Oct follow-up requested a SOURCES row backing "24 hours" (or removal of the number), gate reruns and parking. Added row 22 (MUST QUOTE) to `01_Script/SOURCES.md`, checked directly against NASA GSFC's Earth Fact Sheet, Orbital parameters. It lists `Length of day (hrs)              24.0000`. This supports the nominal mean solar day; it does not claim invariant physical rotation. Rows 14 and 18 retain the slowdown and millisecond-variation qualifications. No spoken line changed.

The existing v01h builder and manifest omit a "24 hours" overlay; the old handover explicitly says it was omitted for lack of a source. This correction supplies the requested source without adding an optional extra label or rerendering the already-reviewed cut. Chapter 5 already has the date timeline and number labels recorded in `overlays_v01h.json`. Chief's permission for labels beside row 33's clock is retained from the job brief.

Master: `/private/tmp/027_EarthSpin_rough_v01h.mp4`.
SHA-256 checked against original `SHA256.txt`: `4bded8774cc790d808079f1de0ba12c4d8a34ed6b40b701f102593ced698ff2c`.
Picture and audio unchanged. Existing before/after sheet: `../overlay_stills_v01h.jpg`.

Fresh full-video gates use `/opt/homebrew/bin/python3` with the existing v01h cut list, all `pool_v01*.json` files and existing v01g reviewed-ok records; no review exemptions were added. Default Python first failed because NumPy was absent; the installed production Python rerun completed. Gate reports and logs are in this directory. These are automated check results, not a Codex final OK.

Next: Chief reviews the new source and gate reports, then makes the overlay decision. Full-film music remains outside this source-only task (the original handover records the bed hold); this is not film delivery approval.

Shared OWB and HOS pulls remain blocked by existing local-file conflicts, preserved. Work used a clean sparse origin/main worktree. Disk had about 150 MiB free; no large render was started. No spend or YouTube state change.

Automated results: picture QA PASS, 0 failed / 40 warnings / 88 cuts; polish gate PASS, 0 failed / 6 warnings / 88 cuts. Both exited 0.
