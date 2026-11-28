# J3012 continuation: analytics record roots, 19 November 2026

The existing four-step plan remains at 3/4. This extends PR 1011; it does not activate migration.

## Change

- Added a read-only resolver shared by snapshot and report commands. The resident layout preserves its current paths. With no home channel, it calls the existing Python registry loader and requires a real matching channel checkout and staged analytics/snapshots directories. Missing histories, mismatched channel identities and destinations inside the engine fail closed.
- Snapshot collection resolves its destination before the token exchange or API call. Existing per-channel collection failure handling remains.
- Report generation reads snapshots, daily rows, catalog recovery and CTR sidecars from each channel's own directory and writes its report there. The combined dashboard remains in the engine. Existing explicit-root test callers and no-snapshot behavior remain supported; the existing separate Field Order report path remains unchanged.
- Both direct analytics entrypoints check the engine retirement guard before running. The new resolver itself does no network requests and creates no files.

## Checks actually run

From the isolated PR worktree on the Mini:

- `npm run typecheck`: exit 0.
- `npm run lint`: exit 0.
- `npm test`: eight desk-lock/Node pretests and **222 application tests**, all passing.
- New tests execute the actual Python registry loader against isolated sibling channel fixtures for all three channels, verify resident paths, missing-history refusal and mismatched-manifest refusal.
- A report integration test verifies separate channel report destinations and CTR reads, with the combined dashboard in the engine and no channel record directory created there.

No live API collection, channel record write, timer execution, service install, deployment, credential change or spend occurred. These checks do not prove the full detached timer or live acceptance.

## Next concrete work

Adapt the analytics timer's worktree creation, environment overrides and per-repository Git staging/commits. Its code must run from the studio worktree while registry checkout overrides name isolated channel record worktrees. Stage each existing history before invoking the new resolver; do not interpret an absent history as an empty channel. Keep the upcoming-Shorts gate's upload/library paths in Orbit and field-order queue writes in the studio. Test failures/retries/commit isolation with fake APIs and Git remotes before installing it.

Also outstanding: remaining writer inventory, deployed board token Contents access, refreshed private rehearsal, seven consecutive official daily zero results and preceding-day notice, then live relay/publish/tick and both-worker acceptance. The official 19 November result is still `left: 2`; this PR's local tests do not reset that record or establish a move date.
