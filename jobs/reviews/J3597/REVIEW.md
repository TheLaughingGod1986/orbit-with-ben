# J3597 — corrected Mulberry autopsy review

24 Nov 2026. Reviewer: codex, elected Chief confirmed by chief_relay.py status. **FIX: keep J3591 held.** Its five completed Gemini media-review steps remain valid and must not be repeated.

## Exact changes reviewed

- OWB replacement #1279: 0299f1920c59a4d5012b3ab2d2400a081df0a815, owner TheLaughingGod1986, base main. Rules check SUCCESS; Studio core check SKIPPED. Already merged at 18:09:16Z as 9fab6082ff108fd923d03d4a9267ea6dd7683eec, before this review claimed at 18:12Z.
- WW2 replacement #102: 1036da1884540ef71b8a50b4dbc57d960ef13284, same owner, base main, no check runs reported. Already merged at 18:09:18Z as fdfb46ab73da8a514ca8feb5726afbc16443ba68.
- Superseded OWB #1273/#1276 and WW2 #101 are closed. This run made no merges.

## Blocking finding: wrong-window views still leak when a snapshot omits the target

In scripts/retention_autopsy.py, video_context sets launch_only when the target is absent from the latest snapshot. It clears Studio metrics when no exact-window launch reading exists, but the views fallback uses `video.get("views") if snaps else None`. Here video is the synthetic launch record, and snaps can contain other videos. A nonempty snapshot list therefore promotes the wrong-age launch views into the requested window and scores them.

Independent probe at exact #1279 head, with a snapshot containing only video `other`, and target `probe` having one launch reading with 123 views:

| Only reading | Requested window | launch_reading | Returned views | Reference RSI |
|---|---|---|---|---|
| 6 h | 48h | None | 123 | 11 |
| 48 h | 7d | None | 123 | 3 |

Expected: requested-window views and RSI unavailable unless an actual target snapshot within the requested bounds supplies them. A labelled non-window proxy may remain separate. The current text can say the reading was not scored while actually scoring its views.

Reproduction: mock `_all_snapshots` to one dated document whose videos list is `[{"id":"other","views":50}]`; mock `lc.load_record` to target wentLive `2026-11-22T17:00Z` and one reading `{hours:6, views:123, impressions:1000, ctr:5, avgPct:20}`; mock `lc._json` to `{}`; call `video_context("ww2","probe","48h")` and `score_metrics`. Repeat hours=48/window=7d. No network or media access is needed.

## Accepted evidence and limits

- All 99 existing tests passed in an isolated worktree at the reviewed head: retention autopsy 11, launch checks 75, email ratchet 8, private-network 5. Existing wrong-window regressions cover empty snapshots, so they miss the above branch.
- Exact 48h and 7d launch paths pass their existing tests.
- Clip extraction now requires source-only acknowledgement and writes a provenance sidecar. It does not silently apply live curves or AVD to the uploaded source. Mapped live interpretation still needs a separate trim receipt.
- Gemini's four 40-second clips and one 48-second opening are preserved. Source/live trim mapping is explicit. This reviewer did not hear audio or perceive moving video.
- Missing Mulberry as a recommendation cause is qualified as a hypothesis. Numeric comparison targets are labelled configured references rather than measured peers. Row 10 remains a proposal, not a rule change.
- Minor wording cleanup: the report's Window 2b heading still says “Engaged-viewer exit”; rename it “Engaged-viewer AVD proxy” to match the explicit evidence limit.

## Exact correction and handoff

1. Guard synthetic launch fallback views by target provenance, not the existence of any channel snapshot. Preserve valid in-window historical target snapshots and exact-window readings.
2. Add regression cases for other-video-only snapshots at 6h/request-48h and 48h/request-7d. Assert metrics.views and its RSI are None; also assert inspect output cannot claim an unscored proxy while scoring it. Retain exact-window success tests.
3. Correct the Window 2b heading only; preserve all original media observations.
4. Run focused tests and publish a new correction PR from main because the replacements have already merged. Existing follow-up J3598 should review the corrected exact head before finishing J3591. No repeat media review, new rules, YouTube changes, spend, or unrelated hold changes.

J3597 is a completed review with a FIX outcome, not approval of J3591. The original hold must name this remaining defect and retain its 25 Nov 05:03Z verification deadline.
