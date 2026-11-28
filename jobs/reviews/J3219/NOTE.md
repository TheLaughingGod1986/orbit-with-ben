# J3219: where it stands (macbook-2, 20 Nov 2026)

A 120-minute job in a 25-minute run. Two of three steps are done; step 1 is part done. Spend: £0, 0 vidIQ credits.

| Step | State | File |
|---|---|---|
| 1a. Rank the every-X topics | **Provisional.** Ranked from the search evidence saved in each topic folder. vidIQ is refused in this lane, so no search volumes were read | `jobs/reviews/J3219/EVERY_X_RANKING.md` |
| 1b. Script, SOURCES.md and packaging brief for the top topic | **Not started** | — |
| 2. Journey 2 and Sleep 2 outlines | **Done** (four checks listed for the builder) | `jobs/reviews/J3219/JOURNEY_AND_SLEEP_2_OUTLINES.md` |
| 3. Readout sheet for 22, 26 and 30 Dec | **Done** | `05_Analytics/tests/FORMAT_TESTS_READOUT_2026-12.md` |

**Provisional pick:** 082 Every Type of Star, runner-up 074 Every Apollo Moon Landing. 070 Mars rovers is last on other channels' numbers and first on ours; the vidIQ pass decides whether it moves up.

**What the next run needs, and why not this lane:** vidIQ keyword research (refused here) and web access for exact source quotes (refused here). The script itself is a `script` kind job for a lane with both.

**Not checked:** the early films' voice match for Sleep 2, the NAS masters, and the J01 and sleep video ids (left blank in the readout sheet).

`jobs.py` is refused in this lane, so these were not run:

```
python3 scripts/jobs.py progress J3219 --agent macbook-2 --step 2 --of 4 --action "vidIQ pass (15 credits) to confirm the top every-X topic, then its script, SOURCES.md and packaging brief" --git
python3 scripts/jobs.py release J3219 --agent macbook-2 --note "Steps 2 and 3 done, ranking provisional (PR). Left: vidIQ pass, then script + SOURCES + packaging brief for the top topic; needs a lane with vidIQ and web access" --git
```
