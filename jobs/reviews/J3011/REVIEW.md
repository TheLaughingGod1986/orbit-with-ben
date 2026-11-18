# J3011 — Every-planet format test: lock and build handoff

Codex, elected acting Chief, 17 November 2026. Ben's “Lock it.” is recorded by Claude in J3011 (18:44Z). Reviewed and merged owner-authored PR #1004 against main, with successful Rules CI; retained its lock/date/plan implementation and updated the remaining stale film brief.

## Decision and scope

Reserved **Wednesday 16 December 2026, 18:00 London** for OWB:064. No other film date changes. Ben's lock and the existing J2875 topic PASS authorise the format-test build. Added OWB:064 to active production: 8/9 total, 4/5 Orbit, 4/4 HOS. Paused single-question backlog remains untouched.

The four packages from go/no-go section 6 are now dependent queue jobs:

| Job | Package | Deadline (London) | Depends on |
|---|---|---|---|
| J3020 | Script, sources, Gemini check and reviewer script lock | 23 Nov 18:00 | J3011 |
| J3021 | Narration and verification | 25 Nov 18:00 | J3020 |
| J3022 | Shelf picture, fresh code graphics, three thumbnails and packaging review | 4 Dec 18:00 | J3021 |
| J3023 | Master edit, QA and playable Ben watch card | 11 Dec 18:00 | J3022 |

All jobs carry film 064 and their script/vo/picture/edit stages. Dates are deadlines, not delayed starts. The first job waits on this handoff being complete. Packages may delegate the independent specialist checks but cannot finish before their checks and locks; narration does not unlock on a facts-only completion. The final package owns the Ben watch card and subsequent approved-delivery handoff, plus linked companion-Short work under the standing rules.

Budget: £0 cash, zero Flow/Vertex credits; about 8,000 narration characters from the existing subscription, checked against live balance/ledger at spend time. No upload, scheduling or public metadata action in these build jobs. A reserved internal air date is not a YouTube publishAt change. Shelf assets must satisfy current gates; reused source graphics require fresh per-row renders, and a shelf music suggestion does not waive the film-specific music gate.

Plan card: **Next: Journey film, Tue 8 Dec**; its needs-you line is empty. Every-planet step: **Wed 16 Dec at 18:00**, linked to the four build jobs. The film brief no longer asks Ben to lock it.

Actual session input: shell/text and still-image tools only; no demonstrated audio or moving-video perception. This is a planning/queue job and makes no media-review claim. Nothing needs Ben now; his next action is watching the finished cut.

## Validation

- `python3 scripts/notes_push.py --check`: `notes check: ok` (includes the tests that read the film briefs).
- `test_plan_board.py`: 6 tests OK; `test_email_ratchet.py`: 8 tests OK; `test_no_private_network.py`: 5 tests OK.
- Queue read-back: all four jobs exist, correct film/stage/kind, dependency chain J3011 → J3020 → J3021 → J3022 → J3023, deadlines through 11 Dec 18:00Z.
- Rendered plan data: `needs` is empty, planets `needsYou` false, date `Wed 16 Dec, 18:00`.
- WIP counts within total/channel limits; no other film air date changed; `git diff --check` clean.
