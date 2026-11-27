# J3950 — OWB 064 metadata correction

Codex covering. Metadata-only repair for PR #1390; master v03 and trailer v05 remain unchanged. No upload, scheduling, privacy change, render or spend.

- Merged main with a merge commit. Current queue, board summaries, WW2 analytics and film status retained. Verified every ledger line from both parents remains present.
- Moved the retired Five_Minutes_in_Orbit and JPL-20210222-M2020f-0001 assets into rejected_assets with empty intervals and explicit replacement reasons.
- Restored PIA24542_full.jpg interval [312.79, 318.57]. Compared complete source paths and ordered interval lists against cuts_064_j3023_v02.json: 82 unique active sources, 138 cuts, zero missing, extra or mismatched intervals.
- Production status now names trailer v05 (e57cd79a), preserving original 771d1f2a. Portrait credits precede the Pictures disclosure; description remains 3,707 characters.
- Privacy checks: all 13 tests pass. git diff --check passes.

No actual audio hearing or moving-video perception claimed. J3910 keeps the exact master and trailer; Ben supplies final watch/listen at UAT.

Package dry run: PASS (ok=true, dryRun=true), category 28, unchanged master SHA-256 d59057aed1590e7f6ef097513256a0548c4f9b1d7e544c4bade28aa83fef647a, trailer v05 resolved. No platform mutation.
