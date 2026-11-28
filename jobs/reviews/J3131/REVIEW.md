# J3131: condition check for J3063 (24-hour Studio readback, `ChbsigHD5_o`)

**Verdict: NOT VERIFIED. Keep J3063 blocked. Next read: 20 Nov 2026 11:35Z (the Chief's recorded 48 h date).**

Run: macbook-2 (Claude Code on the MacBook), 19 Nov 2026, about 11:50Z to 12:00Z. Read-only. No spend. Nothing on YouTube was opened or changed.

## Why it could not be verified

The condition is a fresh Studio reading on the MacBook's History of Science browser (CDP 9222). This run could not take one:

- The check of the browser port from this lane was refused by the unattended allowlist ("requires approval"), so the Studio window was never reached. Whether the browser itself is up was not established.
- AGENTS.md (MacBook lane) says Studio jobs on the MacBook run on Gemini, then Cursor, then Codex, "never on the MacBook's Claude Code, whose unattended allowlist cannot reach the browser". This job was handed to that lane anyway.
- `jobs.py` (show, progress, wait, done) is also refused here, so the queue commands below are unrun.

No 24-hour Studio figure exists in the repo: `05_Analytics/hos/launch/ChbsigHD5_o.json` still holds only the 12 h reading (18 Nov 23:56Z).

## Evidence that could be read (records only, not a Studio reading)

Daily tracker snapshot `05_Analytics/hos/snapshots/2026-11-19.json` (commit `2ccb7519f`, committed 19 Nov 06:43Z, about 19 h 13 m after the 11:30Z publish):

| Video | Published | Privacy | Views | Likes | Comments |
|---|---|---|---|---|---|
| `ChbsigHD5_o` *How Do Plants Clean the Air?* | 18 Nov 11:30Z | public | 0 | 0 | 0 |
| `xgx2lYHhYZM` *Why Is It Called a Vaccine?* | 17 Nov 11:30Z | public | 2 | 0 | 0 |

So at about 19 h the Short still had 0 views by the public count, the same as the 12 h reading (0 views, usual 20, rank 9 of 10). That is consistent with BEHIND persisting, but it is not the reading the Chief asked for: it gives no rank, no usual figure, no feed views or shown, no stayed and no average viewed. Feed exposure is still unknown. The 17 Nov Short is unchanged at 2 views.

Nothing was written to the launch record: the snapshot is not a Studio "Since published" reading and the brief says to record only what Studio shows.

## What is still to do

1. Take the Studio reading on CDP 9222 with `reuse_page`, from a lane that can reach the browser (Gemini, Cursor or Codex on the MacBook, or the Mini): Since published views, rank, usual, feed views and shown, stayed, average viewed, likes, with the actual time and elapsed age. No video changes.
2. Route the next recheck of J3063 away from the MacBook's Claude Code (for example `--for codex` or `--for gemini`), or it will end the same way.

## Queue commands this run could not execute

```bash
python3 scripts/jobs.py wait J3063 --agent macbook-2 --condition "24-hour Studio readback for ChbsigHD5_o not taken: the MacBook Claude Code lane cannot reach CDP 9222. Public count was still 0 views at 19 Nov 06:43Z (daily snapshot). Needs a Studio reading from a lane that can drive the browser" --check-at "2026-11-20 11:35" --type input --recheck J3131 --git
python3 scripts/jobs.py done J3131 --agent macbook-2 --result "NOT VERIFIED: this lane cannot reach the Studio browser (CDP 9222), so no 24 h reading. Records only: 0 views at 19 Nov 06:43Z snapshot (about 19 h), same as 12 h. J3063 stays blocked; next read 20 Nov 11:35Z by a lane that can drive Studio. jobs/reviews/J3131/REVIEW.md" --git
```
