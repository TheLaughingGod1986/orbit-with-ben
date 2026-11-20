# J3012 continuation: analytics record worktrees and dispatch

19 November 2026. Existing PR 1011 and four-step plan remain at 3/4. No live cutover.

## Delivered

`scripts/analytics_worktree.py` prepares detached record worktrees from each source repository's `origin/main` and commits only the selected owner's paths. Studio owns the combined dashboard; each channel owns its own analytics directory; Orbit additionally owns the open-gate library JSON. This is a tested library for the pending timer integration, not an installed timer or a standalone command.

It refuses the shared checkout, nested source destinations, worktrees belonging to another repository, attached branches, unfinished Git operations, symlink scope roots, unrelated unstaged/staged files and unrelated pending commits. Every pending commit is inspected, so a foreign add-then-delete cannot disappear inside a clean net diff. Git operations are bounded and failures omit remote diagnostics that might contain credentials. The executing engine's retirement guard is checked before preparation and publication.

Recovery preserves earlier data edits as a local commit before catching up. Conflicting rebases abort and retain that commit. Publishing retries pending commits even when no new file changed; exhausted pushes return a failure and preserve the local commit for the next run. No force push, reset, production checkout edit or remote deletion is used. The future timer must serialize this helper and validate its source checkouts through the registry before calling it; it does not itself supply a lock, select credentials, collect data or publish the board.

Field Order dispatch now reads its snapshot through the same registry-aware channel root as collection/reporting. It refuses an empty snapshot history and obeys the engine retirement guard before dispatch. Its configured shared queue must have the same engine repository identity as the executing code and contain the queue schema and jobs entrypoint. The detached timer must supply the active shared studio checkout, not a channel record worktree, as `FIELD_ORDER_QUEUE_REPO`. Existing channel/freshness checks and job de-duplication remain.

## Verification

- 13 Python integration tests using real temporary local bare Git remotes passed. These exercise independent channel/dashboard destinations; source-checkout edit preservation; recoverable dirty records; failed push followed by a clean-worktree retry; upstream changes; conflict preservation; foreign changes/renames/history refusal; wrong repository; symlink scope; and retired-engine refusal.
- Content Ops: typecheck, lint, eight desk-lock pretests and 227 application tests passed. Five new dispatch tests cover snapshot selection/absence and shared-queue identity/refusal.
- No production analytics, API call, queue dispatch, timer execution, service installation, marker activation, credential change, remote record push or spend occurred during the tests. All Git record pushes in the new integration tests target temporary local remotes.

## Next

Wire the helper into the detached analytics timer: preflight registry identities and staged histories, prepare separate engine/channel record worktrees, supply their checkout environment overrides, keep media and credential roots separate, and serialize the entire run. Preserve partial channel failure and timeouts, and report push failure while retrying earlier commits. Route the Shorts gate's library to Orbit (its current code-relative library path is still unsuitable after the split), and route Field Order jobs to the active shared studio queue. Test the complete timer with fake APIs before preparing/installing its plist.

Remaining migration gates are unchanged: complete writer inventory, deployed board Contents access, refreshed private rehearsal, seven official consecutive clean daily results and preceding-day notice, then live relay/publish/tick and both-worker acceptance. The nonzero official 19 November result still resets the clean-day streak. This continuation neither changes the official record nor promises a move date.
