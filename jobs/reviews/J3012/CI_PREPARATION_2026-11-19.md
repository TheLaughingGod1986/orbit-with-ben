# J3012 CI preparation — 19 November 2026

Continued existing PR #1011 from `7e773c3c22495beabf177b674c863f6cb2639c7f` in an isolated detached worktree.
No live workflows, services, repository identity, approvals or board deployment changed.

Added a fail-closed staging renderer for the four current workflow files and the matching core hash lock.
The supplied channel pin is mandatory and immutable. The current default channel is read from the registry;
its repository and environment name come from its manifest. Rules and Notes receive that checkout. Rules no
longer expects a tracked studio status page, and the duplicate core PR job recognises the new engine repository.
Existing queue/data exclusions and Content Ops checks are preserved. The renderer installs nothing.

Validation:

- Four renderer tests pass: source unchanged, expected staged adaptations/lock consistency, existing destination
  refused, unpinned/invalid input refused, and changed template refused before any write.
- Combined renderer, channel-ratchet, email-ratchet and private-network suite: 30 tests, exit 0.
- Generated all five files locally; Ruby YAML parser accepted all four workflow files.
- Existing shared-core check: 56 files match. Rule copies check: pass.

Limit: no GitHub Actions execution or complete fresh split with these adapted workflows was performed in this
run. Those checks, exact deployed board credential Contents access, remaining timer installation, old-entrypoint
single-writer protections, refreshed export and live relay/publish/tick acceptance remain. Official daily records
still show five clean days through 18 November. Neither those records nor the day-before notice gate was changed.

Keep J3012 at step 3 of 4. Use the existing PR and rehearsal; do not recreate them on the next wake.
