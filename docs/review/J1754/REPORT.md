# J1754 — Mini workflow rollout evidence, 3 November 2026

Codex covering as elected acting Chief. **Code PASS; operational rollout remains held.** This is not a claim of complete autonomy or media approval.

## Reviewed and released

- OWB PR394 exact head `a8d46b2414a60c6418bf22ac3d9c7f080f7c8009`, merged as `b20b198b6ab446b583378dcd0c5e05033fc374c5` at 10:49:30Z. Initial guarded merge at `a94529d` correctly refused after the head changed. Reviewed the added legacy dependency-hold change and audit before approving the new head. Both required CI checks green.
- HOS PR399 exact head `8e7644faef5c12802b1a5d097f0d6ed42219d830`, merged as `ddefc984a15893513e57fdf01528d1e0e8d7cee0` at 10:47:57Z. All applicable CI checks green; desk-reopen conditional job skipped.
- Both shared Mini checkouts pulled the merged code. No media, publishing, schedule, visibility or subscription spend actions.
- Local tests: 582 OWB tests passed with 8 environment/optional skips on the initial reviewed head; after the small head update all 32 targeted workflow tests passed. Six HOS delivery/ack tests passed. Unit-test synthetic failures are fixtures, not production media checks.

## Actual Mini observations

1. Installed OWB runner fingerprint is `ac2d15fae277db48`. Actual parent relay PID88501 still reports loaded `4adecf25a3a40d02`, state working, job J1754. The safe-boundary restart cannot finish while this child job is running. Do not kill the parent or claim it already loaded the new code. Verify its new PID/version after this run exits.
2. Installed HOS code handled real canary comment [6601656621](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6601656621). Two separate CLI inbox processes both redelivered it. Trusted outcome [6601682729](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6601682729), with exact reply_to, was acknowledged. A third poll returned no new messages; state records the outcome and no pending canary. This validates process restart persistence, not the long-running launchd watcher.
3. The actual HOS watcher is PID8834, started 14 October, running default Grok inbox with `--watch 120 --run`. Its wrapper launches Cursor. It has not reloaded the merged code. Do not blindly restart it into historical production delivery; role routing and selective recovery are J1809.
4. Actual `jobs.py reconcile --agent codex --git` queued 51 unique stage-repair tasks J1758–J1808, plus due-condition checks J1756/J1757 for J1199/J1213. Immediate second reconciliation returned no changes. The candidates are bounded Chief decisions, not approvals or authorizations to regenerate media.
5. No real post-release production stage PASS/completion was observed. The explicit ruling-preservation regression passes, but a test is not a real media review. Keep this requirement open until a genuinely eligible reviewer completes an existing stage with evidence and `done` retains the ruling.
6. Queue focus is empty. Do not invent a focus film to satisfy a test. OWB031/032 each have an explicit VO review hold (J1752/J1753), but no live later stage job. After a real VO ruling, the Chief must record the appropriate next owner/action; no picture is authorized by this audit.

## Inventory before recovery

`HOS_DESK_INVENTORY.json` records IDs, recipients, statuses and the original watermarks from 1,403 live desk comments. There are 175 nonterminal literal-recipient messages at/below those watermarks, 31 addressed to chief, 84 to grok beyond its watermark, and 35 with comma-separated recipients. None of these counts proves unresolved work. Newer outcomes, queue jobs and release history must be checked before selectively recovering an ID. No historical watermark reset or bulk replay was performed.

`STAGE_INVENTORY.json` records 51 candidates: 45 review and 6 blocked. Eight candidate stages have possible matching untagged live jobs (heuristic title/film matches; not established ownership). The 06:40 tracker confirms 023/VBaYRPp85Sw is already public; 026/c5AdqQsnnys, 028/F-jImX5h7ws and 029/vP1BbqZ_dnM are already scheduled. Their stale upload/thumbnail stage records must not trigger new production or re-upload. Remaining candidates include backlog records. Reconciliation decisions must verify evidence individually.

## Concrete follow-ups and hold

- **J1809**, HOS assembly lane: repair elected-Chief aliases, comma-separated recipient handling, supported identities, ownership across succession and acknowledgement, then selective legacy reconciliation and safe watcher refresh. `for_agent` currently tests literal recipient equality; Gemini/Claude cannot use the write/ack CLI. Ordinary Cursor must never inherit Chief authority merely because the watcher says Grok.
- **J1810**, elected Chief: demonstrate an actual supported no-cost audio-input path before resuming J1752/J1753. This session exposes no audio-input/listening tool. Installed Codex help offers images; agy help offers text/stream-json and mic-serve, not demonstrated source-file listening. Playback or ASR is not proof a reviewer heard the voice. No source-audio API egress or new spend is authorized. Keep capability limits distinct from missing tasks.
- **J1754 stays on a structured input hold:** after the safe-boundary refresh, verify loaded/installed relay agreement; verify J1809 runtime outcome; establish the real stage-ruling preservation and next-action evidence. Resolve J1810 capability or record its precise remaining limitation. Preserve Ben finished-video UAT. Do not close from CI or unit tests alone.

Disk check found less than 20 GB free. The authorized NAS offloader ran with actual NAS access and found no eligible scratch old enough to move; nothing was deleted from NAS. No Ben approval is requested for these engineering follow-ups.
