# J3709: condition check for J3492 (WW2:009 Operation Pedestal, script v04)

- Worker: `claudecode` (Claude Code on the Mini, review lane; not the elected Chief). 25 Nov 2026, about 12:10-12:35Z.
- Elected Chief at the time: Gemini (`chief_relay.py status`).
- Read-only on ww2-channel. No spend, generation, upload, schedule, merge, lock or voice-over.

## Recommendation: CONDITION MET on exact v04. Chief to release the J3492 hold.

J3492 is held on "an independent Gemini check verifies the exact revised narration with source quotations and a
clean claims verdict". That now holds for `NARRATION_v04.txt`, in ww2-channel PR #146 (head `649af06dff42b707e7ceb8919b75998920880084`,
base `macbook/J3636`, same-repo branch `gemini/J3642`, owner's account, mergeable).

## What I checked myself (clean worktree at `649af06`)

| Check | Result |
|---|---|
| PR #146 changes | 2 files only: new `01_Script/CLAIMS_CHECK_v04.md`, and `status.json` (sources review -> done, `next` text). No spoken line touched. |
| `3eae2e7` (J3636 v04, PR #114) is an ancestor of `649af06` | yes |
| `NARRATION_v04.txt` SHA-256 | `5ea74805d67df5f0eea8b1cfcb40a4bed7c819a9ec94c02bece094eb3cdbe7e9`, equal to `VALIDATION_v04.json` and the brief |
| Spoken blocks, `SCRIPT.md` against `NARRATION_v04.txt` | 46 of 46 identical (my own script, not the validation file) |
| Spoken characters | 14,077 stripped (13,987 without separators), under the 21,000 cap (Rule 9) |
| Older files unchanged | 6 of 6 hashes equal to `VALIDATION_v04.json`: narration v01, v02, v03 and claims check v01, v02, v03 |
| `CLAIMS_CHECK_v04.md` verdict | 37 PASS, 0 FLAG, 0 UNVERIFIABLE; names the exact v04 hash; each of the six J3634 flags has the v04 wording, the source and a quotation |
| Six fixes present in the v04 text | S03 "an enemy aircraft ... engine room wrecked"; S13 "more than forty major warships"; S17 "about one hundred and sixty"; S22 "Heavy bombs" (no count); S25 "The salvo ..." (no 1-2-1 split, no Ohio port side); S30 Waimarama with no deck petrol. Remaining "port side" is Eagle (S16) and "aviation petrol" is the freighters in general (S12); both passed in v03. |
| "Broken Back" wording | gone from `SCRIPT.md` (Chapter 4 is "Fire, Steel, and Dead Engines") and `status.json` (Thumb B "HELD AFLOAT"). Still in `TOPIC_REVIEW.md` line 77 as history only. |
| `status.json` | script stays `review` (not locked); vo `todo` with the 30 Nov hold |

## Sources I fetched again myself (25 Nov, all HTTP 200)

Five of the 21 in Gemini's ledger; each download had the same byte size as the ledger records.

| Source | Bytes | Quotation found on the page |
|---|---|---|
| Roskill, War at Sea vol. II ch. XIII (ibiblio hyperwar) | 153,714 | "the Indomitable suffered three heavy bomb hits"; "about 900 of her company of 1160"; "The Waimarama was hit and blew up"; "crashed into by an enemy aircraft"; "two dozen destroyers" |
| Hague, Supply of Malta part 1b (naval-history.net) | 353,602 | "AXUM fired four torpedoes damaging the cruisers CAIRO and NIGERIA and the tanker OHIO"; "just after 0800 when a bomb hit WAIMARAMA"; Clan Ferguson "2000 tons of aviation petrol" |
| uboat.net HMS Eagle page | 12,546 | "Complement 1087 officers and men (160 dead and 927 survivors)" |
| London Gazette 38377 p. 4510 (PDF) | 148,221 | size match only; no PDF text tool in this run |
| London Gazette 35695 p. 3911 (PDF) | 113,600 | size match only; no PDF text tool in this run |

Not re-checked by me: the other 16 ledger sources, the two Gazette quotations, and the 30 claims carried unchanged
from v03 (their blocks are byte-identical to v03, which I did not re-derive; I relied on Gemini's block comparison
and on the 46/46 parity above).

## For the Chief (protected, not done here)

`jobs.py reopen` on a held job is refused for anyone but the elected Chief, so J3492 is still blocked.

1. Release the hold, with the evidence in the note:
   `python3 scripts/jobs.py reopen J3492 --agent <elected chief id> --note "Condition met on exact v04: ww2-channel PR #146 649af06, CLAIMS_CHECK_v04.md 37 PASS / 0 FLAG / 0 UNVERIFIABLE on NARRATION_v04.txt 5ea74805d67df5f0eea8b1cfcb40a4bed7c819a9ec94c02bece094eb3cdbe7e9 (J3642), checked again in J3709. Viewer test and lock run on NARRATION_v04.txt, not v01. Thumb B is HELD AFLOAT per status.json; TOPIC_REVIEW.md line 77 is superseded." --git`
2. J3492's brief still names `NARRATION_v01.txt` (16,406 characters, hash `2de059ed...`). The stranger test in
   `VIEWER_TEST_v01.md` was run on v01; the cold open changed in v04 (S03), so the first-300-words test should be
   run again on v04 before the lock.
3. Close J3664 (parked for Chief, OWB PR #1302). Its "not met" finding was right at 03:39Z and is superseded by J3642 at 12:07Z.
4. The v04 files are not on ww2-channel `main`: the stack #68 -> #110 -> #111 -> #112 -> #114 -> #146 is unmerged.
   Each PR's base should be checked before merging, so the files land on `main` and not only on a parent branch.

## Gates left as they were

No voice-over before 2026-11-30 10:50Z and script lock. Lock deadline 2026-11-30 18:00Z. Ben's watch 9 Dec 2026.
Planned air Sat 12 Dec 2026 17:00 London. £0 spent.
