# Studio workflow handoff audit — 3 November 2026

## Findings and repairs

1. **Confirmed lost stage → review handoff.** J1294/J1295 completed, but OWB032/031 Voice remained review with no final-review task. J1752/J1753 were added to the actual queue before this patch. Existing dependency reconciliation only sees jobs; it cannot discover a stage that has no job.
2. **Confirmed review loop in completion code.** `jobs.py done` unconditionally released a linked board claim to review, even for a Chief job that had explicitly marked the stage done. Chief stage completion now requires a done/skip/blocked ruling and an evidence reference, and preserves that ruling when releasing the claim. Normal worker outputs still go to review.
3. **Confirmed timestamp incompatibility.** `studio.parse` rejected valid UTC-offset/fractional timestamps accepted by the workflow calculations and emitted by other tools. ISO timestamps now normalize to UTC. Invalid values still fail rather than inventing dates.
4. **HOS seen ≠ completed.** Its separate desk inbox advanced the watermark after delivery even on worker failure. A companion HOS PR persists pending delivery, requires a linked outcome acknowledgement, and serializes state/dispatch. It must be released independently.

## Continuous recovery

`workflow_handoffs.py` reads existing queue + per-film status records. `jobs.py reconcile` queues deduplicated Chief repair jobs for review/doing/blocked stages with neither a live matching job nor an unexpired stage claim. It also finds a focus film with recorded completed work but no next action. The relay checks this every selection pass alongside missing/cancelled/cyclic dependencies and due conditions. It reports malformed status files rather than skipping them silently.

Repair tasks never claim the broken stage, modify milestones, approve media, launch generation or publish. They require an actual ruling or an explicit linked next-action job; closing with the same unresolved gap fails. Cancellation cannot permanently silence an unresolved gap. Their focus priority is preserved without manufacturing deadlines. All backlog stages remain review candidates rather than automatically starting paid work. Completed upload records are excluded. Historical stages on films already released but whose upload status is stale may still be reconciliation candidates; the repair explicitly requires checking release history, not restarting production.

Read-only inventory: `python3 scripts/workflow_handoffs.py` emits JSON and exits 1 when candidates exist. The reviewed main snapshot had 45 unmatched review stages and 6 unmatched blocked stages. This is an inventory of record/queue discrepancies, **not** 51 verified missing approvals: it includes backlog, stage-less jobs and stale historical release records.

## Transition coverage

| Transition | Check / expected owner |
|---|---|
| Topic → script → facts → voice → shots → picture → edit → packaging | Existing film/stage claims and job prerequisites; Chief repair for missing stage owner or stranded focus continuation |
| Worker output → Chief review | Stage-to-queue watchdog, deduplication, active claim expiry, review evidence retained |
| Chief PASS/FIX → next action | Explicit recorded ruling; no review reset; missing focus continuation becomes a planning task |
| Job waiting → condition verification | Existing structured holds, recheck task deduplication and evidence-before-release tests |
| Predecessor completion/cancellation | Existing dependency graph, cycle/missing-parent reconciliation and inherited deadline tests |
| Worker unavailable / Chief succession | Existing routing, usage fallback, Chief-role enforcement, durable inbox and retry tests |
| Ben UAT → changes / approved delivery | Existing explicit Ben records and workflow/queue tests; no inferred approval |
| Upload/swap → schedule → public → social | Existing swap readback guard, tracker lanes and Buffer registration rules; not exercised by making live publishing changes |
| Runner code update / restart | Existing safe-boundary runner-version tests; pending stage recovery on next relay pass |

## Validation and release limits

Python unit/regression tests exercise queue, stage, dependency, hold, dispatch, succession, refresh and approval calculations. New tests cover orphan recovery, duplicate suppression, live/expired claims, HOS number collisions, Chief completion, source preservation, focus continuation, malformed records and timestamps.

A passing test suite does not prove the installed launchd service is current, media has actually been listened to, browser sign-ins are usable, or YouTube/Buffer accepted a write. After review/merge, verify the Mini's installed/loaded runner version, observe reconcile creating/deduplicating repair jobs, watch one real review through its explicit ruling and successor, and inspect the next published board snapshot. Verify HOS inbox delivery/ack separately. Retain the existing money, manual-review and Ben finished-video gates. No claim that all production handoffs are fault-free is made from cloud checks alone.

## Live review execution update

During the audit, the Mini picked up J1752/J1753. Both are now explicit input holds: technical verification is recorded, but the Codex sessions report no audio-input capability and correctly withheld final listening approval. J1752/J1753 must resume with a genuinely listening-capable elected reviewer. An agent name or Chief election alone does not prove media-review capability. The cloud test suite does not resolve this runtime capability limitation; rollout must verify capability-aware handling rather than retrying unchanged text-only sessions.

The runner version fingerprint now includes the new handoff module and studio timestamp/state helpers, so future changes to those loaded modules trigger the existing safe-boundary restart mechanism.

## Overdue legacy dependency hold (J1213)

J1213 is type=dependency with a recorded 30 October check but no structured after ID. `hold_due` previously returned false before consulting check_at. It now honors the expired check even when the predecessor was only named in prose. Regression verifies exactly one Chief verification task is queued, the parent remains blocked, and a future check does not release it. J1218 repair history progressed through J1267 picture lock and J1297 master-v03 delivery; reconciliation must use that later evidence rather than re-run rough-v01 edits or imply Cursor is the only eligible worker.
