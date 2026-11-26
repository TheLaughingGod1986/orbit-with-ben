# J3798: condition check for J2040 (Codex allow-list for unattended Mini runs)

- **Verifier:** `claudecode` (a specialist worker on the Mac mini, not the Chief). The elected Chief at check time was Gemini (`chief_relay.py status`, 2026-11-26T16:05Z).
- **Checked:** 2026-11-26T15:50Z to 16:05Z
- **Spend:** £0. Nothing in `~/.codex`, PR #490, the NAS, YouTube, Buffer or any schedule was changed.
- **Finding: CONDITION NOT MET.** J2040 stays blocked.

## What I checked

| Requirement | Status | Evidence |
|---|---|---|
| Operator confirms the Mini Codex config | NOT MET | All eight hashes match J3423 exactly. `config.toml` efa1987b…aed (435 B, mtime 4 Nov 12:18). `rules/default.rules` b6d57758…da6 (2,589 B, 4 Nov 12:27). `rules/studio.rules` e3b8c84f…1fa (3,307 B, 6 Nov 15:12). `bin/` holds the same five scripts with the same hashes: studio-buffer-reschedule 6a78c350…, studio-r2-upload fd28bb4e…, studio-scoped-push d701467a…, studio-service-read 6635f535…, studio-youtube-defaults 5e5d238b…. `codex-cli 0.160.0`. |
| Scoped acceptance/refusal evidence from a fresh session | NOT MET | None posted. Unchanged hashes do not prove acceptance. |
| Draft PR #490 resolved | NOT MET | `gh pr view 490`: OPEN, draft, head f521bcd3f1, last updated 2026-11-17T18:35Z. |
| Thread / desk | NOT MET | Studio thread #954 after 7105379476 through 7196742962 (2026-11-26T15:46Z) has no operator confirmation and no acceptance evidence. All [Ben] posts are video OKs. Only the J3423 ruling and J3530 mention J2040; J3530 says J2040 "left alone". HOS desk #694 since 23 Nov has two [Ben] video OKs and nothing on J2040. HOS #180 has no comments. |
| J2517/J2559 done, J2007 cancelled | Unchanged | Per J3423. Do not retry J2007. |

## Parked for the Chief

`jobs.py wait J2040` was refused: "Only the holder or elected Chief may update this hold" (the holder is codex). Command for the Chief:

```
python3 scripts/jobs.py wait J2040 --agent <chief> --type input --recheck J3798 --check-at "2026-11-27T13:00:00Z" \
  --condition "J3798 (jobs/reviews/J3798/REVIEW.md): NOT MET. All eight Mini ~/.codex hashes unchanged from J3423 (codex-cli 0.160.0); PR490 OPEN draft f521bcd3f1 (last update 17 Nov); thread #954 through 7196742962 and HOS #694/#180 contain no operator confirmation or fresh-session scoped acceptance evidence. Authorized operator must confirm Mini configuration and supply that evidence; then resolve draft PR490. Retain approval controls and fallback routing; never retry J2007. Recheck 27 Nov 13:00 UTC." \
  --action "Await operator confirmation and fresh-session acceptance evidence for the Mini Codex permission settings; verify again 27 Nov 13:00 UTC, then resolve draft PR490." --git
```

After that, merge this PR and close J3798.
