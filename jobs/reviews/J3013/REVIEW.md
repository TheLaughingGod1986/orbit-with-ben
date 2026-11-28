# J3013 — Exoplanets script record correction

Codex covering, acting Chief, 18 November 2026.

Verdict: **FIX the workflow record; no script or media approval.**

The reported orphan-doing was caused by another channel’s job writing to Orbit’s film 003. Before that write, the script stage had no entry. Restore that exact absence rather than inventing a script PASS, review submission, or production task.

Evidence:
- `0e52d64724^:02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/status.json` has only the existing thumbs stage, no script stage and no claims.
- `0e52d64724` (J2997 claim) introduces the script stage and a claim naming the WW2 pilot, not Exoplanets.
- J2997 is explicitly `film: WW2:003`, `repo: owb`, `stage: script`; its script, claims check and result concern the B-29 documentary. Those results cannot approve the Exoplanets script.
- `b3ed58d6a3` (J2997 completion) leaves script in review. The orphan-doing report was generated during that foreign job’s claim.
- J2998 subsequently writes the picture stage in `ad280b2667` / `07452a6b40`. Existing J3019 owns that separate correction; this change preserves it.
- `jobs.on_board` selects by repo and film presence; `board_claim` passes the foreign qualified film to `studio.film_dir`. J3060 (after J3013) will address identity validation and regression tests.

Action: remove only the contaminated script stage and this repair’s temporary script claim. Preserve the thumbnail approval, picture record, next action and every other field. No new production is commissioned. The historical production-status prose is not approval evidence and is unchanged. No media input is needed for this provenance correction.

Verification: compare the resulting record against the current pre-repair record, removing only script; confirm it matches the pre-J2997 script absence; regenerate the board; check the patch for whitespace errors. Chief authority was checked before the correction.

Checks: PASS — exact JSON comparison against pre-repair record, allowing only script removal and temporary claim removal; PASS — pre-J2997 script absence restored; PASS — board regeneration and git diff --check.
