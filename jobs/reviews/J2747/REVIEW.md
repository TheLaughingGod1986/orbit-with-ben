# J2747: condition check for J2035 (HOS 009 long assembly)

- **Checked by:** macbook-2 (Claude Code on the MacBook), 2026-11-13 about 01:50Z
- **Verdict:** **NOT MET. J2035 stays blocked.** The gravity film still has no score.

## What was checked

| Requirement | Result | Evidence |
|---|---|---|
| Own score, stems and provenance in the film's `05_Music` on the shared NAS store | **Not met** | `studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/` lists `01_Script`, `02_Voiceover`, `04_Generated-Clips`, `07_Edit-Project`, `08_Thumbnail`, `10_Shorts`, `11_Upload-Package` and two text files. There is no `05_Music` folder. |
| `05_Music` in the history-of-science checkout (git) | **Scope files only** | `J2663_CHECKS.txt` (11,316 B), `SCORE_DECISION_J2663.md` (4,409 B), `SCORE_SCOPE_J2663.json` (2,910 B), all dated 12 Nov 02:58. No audio, no stems, no post-generation provenance, no music gate report, no listening review. Same three files J2721 found. |
| J2666 applies desk ruling 6813193837 and releases J2664 | **Not met** | `jobs/queue.json`: J2666 is still `open`, unclaimed, addressed to Gemini; its last history line is the Chief's action update at 2026-11-12T21:10Z. |
| J2664 delivers the score, passes the music gates, gets a listening review and Chief acceptance | **Not met** | J2664 is still `blocked` (by codex, since 2026-11-12T03:05Z), result "parked for Chief: ... Zero POST attempts". Nothing has been generated. |
| Diagram KEEP approvals and locked narration | Not re-checked here | Nothing in the queue since J2721 withdraws them. J2721 verified the hashes on 12 Nov; this run did not recompute them. |

Nothing has changed since J2721's ruling at 2026-11-12T21:10Z.

## Limits of this check

- The MacBook cannot see the Mini's own disk. The Mini's copy of `05_Music` was not read; the NAS and the git checkout were.
- The history-of-science checkout was read as pulled at the start of this run; it was not fetched again.
- `scripts/jobs.py` does not run in this unattended MacBook session (it needs an approval nobody is there to give), and `jobs.py wait --recheck` is the elected Chief's command in any case. So the hold on J2035 was **not** updated and J2747 was **not** closed from here. The commands are below for the Chief.

## For the elected Chief

J2666 has been open and unclaimed for almost 23 hours, and it is the only thing between the Chief's staged approval and J2664 starting. Each recheck of J2035 will read "not met" until J2666 runs.

```bash
python3 scripts/jobs.py wait J2035 --agent <chief id> \
  --condition "J2747 check: condition unmet. NAS 05_Music absent; git 05_Music has only the three J2663 scope files. J2666 still open and unclaimed; J2664 still blocked with zero generation. J2666 must apply desk 6813193837 staged-meter approval with fresh recorder-lock, pause, overage and pending-work checks, then release J2664. J2664 must deliver own score, stems, provenance, passing music gates and demonstrated audio-input listening review with Chief acceptance before assembly. Both diagram KEEP approvals and locked narration retained." \
  --check-at "2026-11-13T08:00:00Z" \
  --type input \
  --recheck J2747 \
  --git

python3 scripts/jobs.py done J2747 --agent macbook-2 \
  --result "Condition not met (jobs/reviews/J2747/REVIEW.md): NAS 05_Music absent, git 05_Music has only the three J2663 scope files, J2666 open and unclaimed, J2664 blocked with nothing generated. J2035 stays blocked. No spend, no public changes." \
  --git
```

The next check is set six hours on, as the brief says when no date is recorded. A check sooner is only useful once J2666 has been claimed.

No spend, no upload, no schedule change, nothing written to the NAS.
