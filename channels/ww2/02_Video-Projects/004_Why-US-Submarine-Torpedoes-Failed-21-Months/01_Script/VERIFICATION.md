# Verification — J3000

18 November 2026, Codex. No narration request sent and no credits spent.

## Narration dry run (existing studio tool)

Command: `python3 04_Audio/tools/vo_take.py --script <film>/01_Script/SCRIPT.md --out <scratch>/j3000-dry-run --stem torpedoes_v01 --order J3000-dry-run-only --dry-run`

Output, relevant lines:

```text
Ben Orbit Narrator / eleven_v3 / speed 1.04: 6 chapter(s), 19513 chars, 3168 words
dry run: nothing spent
```

PASS: six parsed chapters, under 21,000. The ledger’s conservative 19,523 includes ten separator characters between chapters; the narration tool counts the six bodies separately. Chapter markers are instructions, never spoken narration. No audio file was generated or reviewed.

## Structural verification

```text
PASS: 41/41 paragraph source and shot mappings; 10/10 archive records;
six chapters; 19,523/21,000 narration characters; script hash matches.
Planning runtime at 125 wpm: 25.34 minutes; not an audio measurement.
```

The verification compares each ledger row’s opening text with its paragraph, checks exact source/shot coverage, catalogue-ID/URL/rights presence, archive references and script hash. It does not substitute for the written source check or a later visual review.

## Repository checks

- `python3 scripts/test_email_ratchet.py`: 8 tests, OK.
- `python3 scripts/test_no_private_network.py`: 5 tests, OK.
- `python3 scripts/channel_check.py channels/ww2`: “ww2: the studio can drive it.” Existing three-repo-layout TODO: `repo.url` empty. The separate registration/migration PR owns that; no account or repository configuration changed here.
- `git diff --check`: no errors.

## Routing note

The queue still identifies J3000 as repo `owb` with film `WW2:004` while the WW2 migration PR is pending. The automatic board claim and a direct studio claim resolved film 004 to Orbit’s JWST film. The erroneous Codex claim was released back to todo, with an explicit note that no JWST script work occurred. WW2’s own status.json in this PR carries the correct topic/script state. This job changes no routing code or other film content.

## Handoff limits

Text/source review only; the claims check is explicitly a writer self-check. Catalogue evidence is recorded, but no image master has been downloaded, visually passed or hashed. Diagram renders, final narration, finished-film quality review and Ben’s watch are later work. PR completion does not claim film approval.
