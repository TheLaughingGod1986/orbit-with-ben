# J2564: the Mini's daily credit reading tells the truth about failure

Follow-up to J2559. Written 11 Nov 2026 from the cloud; nothing was run on the Mini and nothing was spent.

## What was wrong

The daily credit reading (`scripts/ai_spend_daily.py`, 08:30 on the Mini) reads seven pools. Three are money or
credit: ElevenLabs, Flow and Vertex. Four are a percent of a plan's limit: Cursor, Codex, Claude and Gemini. The
run ended in an error if any one of the seven could not be read. For three days every money figure was read and
the run still ended in an error, over three usage pages. A check that fails every day cannot tell anyone about
the day a money figure really is missing.

## What changed

| | Before | Now |
|---|---|---|
| A money or credit pool cannot be read | exit 1 | exit 1, printed as `FAIL`, with the likely cause |
| A reading cannot be written to the ledger | exit 1 | exit 1, printed as `FAIL` |
| A usage page cannot be read | exit 1 | exit 0, printed as `UNREAD` with the likely cause and when that pool was last recorded, and by which machine |
| Any page reading that fails | one line of error | also the page's address (no query string) and its first 25 lines, with any email address and any payment line removed |
| The run's last line | none | `SUMMARY`: how many were read, which usage pages were not, and whether a spending figure is missing |

Readings that work are still recorded, exactly as before.

`--strict` keeps the old meaning for one caller. The MacBook worker asks for the Codex pool only and marks it
"recorded" when the script exits 0, so it now passes `--strict` and an unread log does not earn the mark.

## A second fault found on the way: the reading could take a picture run's tab

The reading and the picture runs both find the Flow page with `cdp_tabs.reuse_page`, which returns the newest tab
on that site. So at 08:30 the reading would take the tab a run was generating in and load the Flow home page in
it. No credit would be lost (a submitted take stays in the project and the run's own records stop a second
charge), but the run would stop and need sorting out by hand. It has not happened yet only because the runs so far
were in the small hours. Film 010's twelve plates and film 008's retakes run today.

The picture runs hold one lock for a whole batch (`~/_desk/state/flow/shared/writer.lock`). The reading now takes
that lock before it touches the Flow page:

- A run holds it: the reading leaves the tab alone and prints `BUSY flow`. This is not a failure. The run records
  the balance itself before every take.
- Nobody holds it: the reading holds it for the few seconds it needs, so a run cannot start underneath it. A run
  started in those seconds is refused by its own guard and can be started again straight away.
- A machine that has never had a picture run (no such folder): the reading behaves as before.

## The three pages: which kind of failure each is

Worked out from the ledger and the J2559 log table. The Mini itself was not looked at.

| Page | What the records show | Kind | What happens next |
|---|---|---|---|
| Codex | "no `rate_limits` reading in the Codex session logs", every day. The MacBook records this same pool after its own runs (last at 05:12Z on 11 Nov); both machines are one account with one limit. | Does not need the Mini. The board's figure is fresh without it. | The reader looked at only the five newest runs. It now looks at every run in the last three days (up to 60) and says how many lines held a limit field. If the Mini's logs hold a reading, tomorrow's run records it. If not, the line says so and the run still exits 0. |
| Claude | Read correctly until 5 Nov. On 6, 7 and 8 Nov it recorded "weekly 100% used" with a nonsense session line ("resets 0% used"). From 9 Nov, no usage line found at all. The weekly limit resets today at 10:00. | Most likely the page reads differently once the weekly limit is used up, so a fix to the reader. A sign-out is possible but the page was signed in on 8 Nov. | The nonsense session line is fixed here. The rest needs the page's words: the 08:30 log will now hold them. |
| Cursor | Read until 9 Nov, at 99% used. Failed on 10 Nov. Cursor is flagged out of credit until 9 Dec. | Most likely the same: the page reads differently at 100%. | Needs the page's words, as above. |

Both pages stopped being readable at the moment the pool ran out, which is when the figure matters most. That is
worth fixing properly once the words are known.

## Tests

`scripts/test_ai_spend_daily.py`: 33 tests (was 8). New ones cover: the three-day case exits 0 and names the three
pages; each money pool unread exits 1; a failed write exits 1; working readings are still recorded when others
fail; `--strict`; the likely causes; the page excerpt carries no address, no payment line and no query string;
the Flow page is never opened while a run holds the lock, and is held during a reading; Codex readings older than
the five newest logs are found; the bare "Resets" line.

`scripts/test_macbook_worker.py`: 62 tests, one line added (the worker passes `--strict`).
The whole suite, the rules check and the shared-file check pass.

## Not done here

- The Claude and Cursor readers are not fixed for a used-up pool. The pages' words are needed first. A Mini job
  copies the `UNREAD` lines and the `page shows:` lines from `~/Library/Logs/owb-ai-spend.log` after the next run.
- If a page turns out to be a sign-in screen, that is Ben's: the log line will say "it needs Ben's sign-in" and name
  the page.
