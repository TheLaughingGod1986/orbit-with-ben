# Studio tests: the Monday test loop (Orbit With Ben + History of Science)

Ben, 26 Oct 2026: scoreboard and keeper-score ideas are tested in the real Studio against controls. Winners are written into the studio rules; losers are reverted. Chief runs the loop every Monday at about 09:30 London (routine "Monday Studio test loop"). This file is the log.

## How the loop works

1. **Inputs.** That Monday's *Weekly recommended-views scoreboard (Orbit + HOS)* (~08:47 London; `05_Analytics/owb/recommended_scoreboard_<date>.*`, HOS `02_Video-Projects/_analytics/evidence_<date>_scoreboard/SCOREBOARD.json` in history-of-science) and the *Orbit weekly keeper score* (~08:12 London). Each "suggested change to try" becomes a proposal row below.
2. **Read out** every test whose end date is today or earlier: compare test videos against controls on the named metric, from real YouTube Analytics. Verdict: **winner** (write the rule into the docs workers read, per AGENTS.md > Changing the rules), **loser** (revert the listing to the logged original, verbatim), or **no clear result** (revert; note why).
3. **Start at most 1–2 new tests**, only when worth testing (the metric must be able to move in 14 days at the channel's current volume).
4. Commit this file by PR to `main`.

## Hard rules for every test

- Listing edits only, all reversible: title, description, tags, Shorts Related video. Through the channel's own Content Ops access (`07_Content-Ops/scripts/retitle-videos.ts`, `redescribe-videos.ts`, `update-shorts-listings.ts`). Confirm the channel name before any write.
- Never delete; never change privacy, publishAt or schedule; £0.
- Never use a video that is in another running test: thumbnail Test & Compare (`THUMB_LEDGER.json`), Shorts Tests A/B (`SHORTS_TESTS.md`), the J0216 standalone Shorts test (`00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/TEST_LOG.md`), or anything else live on the board.
- Never touch anything Ben has OK'd that is scheduled and not yet public.
- **Log the original title and description verbatim here before the edit.**
- Baseline numbers come from real YouTube Analytics (API or Studio) with the date range stated. No real baseline, or no safe edit, means the row stays **proposed, not started** with the reason.
- Default length 14 days.

## Test register

| ID | Channel | Hypothesis | Metric | Test videos | Control videos | Baseline (source, range) | Start | End | Status / verdict |
|---|---|---|---|---|---|---|---|---|---|
| — | — | No tests started yet (first run 26 Oct 2026; see proposals) | — | — | — | — | — | — | — |

Original listings (verbatim, before edit) go under *Originals* below, one block per test ID.

## Originals

None yet.

## Week of Mon 26 Oct 2026 (first run)

### Inputs found

- **OWB recommended-views scoreboard:** `05_Analytics/owb/recommended_scoreboard_2026-10-26.{json,txt}` (pulled 08:51 London). Analytics settled through 23 Oct, so the window is 17–23 Oct, not 19–25 Oct. 15 views on 14 longs: search 10, direct 3, browse 1, suggested 1 (6.7%). Prior window 12–18 Oct: 201 views, 189 of them browse (94%), suggested 2 (1%). No long had a view on all 7 days. Note: the two windows overlap on 17–18 Oct, so the "prior" total is not fully independent; the scoreboard script should use 10–16 Oct for the prior week (HOS already does).
- **HOS recommended-views scoreboard:** history-of-science `02_Video-Projects/_analytics/evidence_2026-10-26_scoreboard/SCOREBOARD.json` (08:51 London). Window 17–23 Oct: 19 views; Related video 13 (68.4%), up from 6 of 15 (40%) in 10–16 Oct. `GHZDsiH7L7A` (What's Really Inside an Atom?) took 15 views, 9 from Related video (Science Retold atom videos and others). `AL_-qlWko_g` got 4 from TED-Ed's Mendeleev video (3.69M views; also in the prior week).
- **Orbit keeper score (Mon 19–Sat 24 Oct):** no standalone output file found; its findings were turned straight into rules by PR #286 (Ben's rulings) and #287 (grandfather line), both merged 26 Oct. *Could a Robot Survive Touching the Sun?* 883 views, *Why Does a Day on Mercury Last Two of Its Years?* 849, *Saturn's Rings Are on a Clock* 12. Rules: one question per Short in the title and line 1, no statement/teaser titles, 22 s floor, Related video + description link to the matching long, Sun Shorts held until the `h8HGfyShEHI` thumbnail test ends 1 Nov.
- Neither routine wrote a "suggested change to try" list to disk; the proposals below are taken from the numbers above and from #286.

### Read-outs due

None. No listing test with controls had an end date on or before 26 Oct. Running tests elsewhere (not read out here): thumbnail Test & Compare T001, T004–T007, T009–T012 (Studio estimates T001 ends ~28 Oct, T005–T007 ~29 Oct, T012 1 Nov); Shorts Test A (first readout Wed 18 Nov) and Test B (~10 Dec); J0216 standalone Shorts test (ends 20 Nov).

### Proposals

| ID | Channel | Proposal | Status | Why |
|---|---|---|---|---|
| P-2026-10-26-1 | OWB | Retitle older statement-titled public Shorts as one question (keeper score rule 1), against untouched statement-titled controls; metric 14-day views and search views. | proposed, not started | Volume. Public-view snapshots (Data API, 12 Oct 05:40 → 26 Oct 06:40 UTC): the 53 public OWB Shorts published before 5 Oct gained **10 views in total** over 14 days (max 3 on one Short). Test and control would both read ~0, so no verdict is possible. The rule is already in force for new cuts (#286), which is where it can be measured (the keeper score each week). The Saturn statement Short `6dcL5rBmHPM` (Fri 30 Oct) is OK'd and scheduled, so it's off limits anyway. |
| P-2026-10-26-2 | OWB | Add the description link to the matching long on public Shorts that lack it (keeper score rule: Related video + description link), metric the long's views from Shorts. | proposed, not started | The recent Shorts with real traffic overlap running tests: `n_4XskX0yZk` and `y-SPHQ0-VjQ` promote `h8HGfyShEHI` (thumbnail test T012, to 1 Nov); `vlkj8RQKmH8` is a J0216 test Short (unlinked until 20 Nov). Older Shorts get ~0 new views (above). Revisit on Mon 2 Nov once T012 has ended: Sun Shorts → `h8HGfyShEHI`, with a baseline of its Shorts-sourced views from Analytics. |
| P-2026-10-26-3 | OWB | Lift Suggested-video share on longs (6.7% of 15 views, 17–23 Oct) with listing changes. | proposed, not started | No concrete listing change came from the scoreboard, and 15 views a week across 14 longs is too few for a 14-day test (the 10 public longs published before 5 Oct gained 9 views in total, 12→26 Oct). Re-check when weekly long views are much higher. |
| P-2026-10-26-4 | HOS | Align `GHZDsiH7L7A`'s description/tags with the atom-history videos that suggest it (Related video is 68% of HOS long views). | proposed, not started | 15 views a week on the video. A 14-day test can't separate an edit effect from noise, and there's no comparable control long (the other public HOS longs had 0–4 views in the window; `frP_YrNShsU` and `_C92tIJCk8A` are in thumbnail tests T001/T009). Revisit if its weekly views pass ~100. |

### Rules changed this week

None from this loop (no test ended). The keeper-score rules (#286, #287) were Ben's rulings, not a result from this loop.
