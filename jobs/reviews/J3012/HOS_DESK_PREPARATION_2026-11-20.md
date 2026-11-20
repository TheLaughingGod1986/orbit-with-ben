# J3012 — channel-local HOS desk launcher

20 November 2026. Continued PR 1011 from `1aacfcf98aba8f17f27225eb8c8d56c418eeecba`.
Existing job plan remains 3/4; this is preparation, not live cutover acceptance.

The installed HOS desk definition and its directly referenced local worker wrapper were inspected.
The watcher runs from HOS, polls every 120 seconds with execution enabled, and the wrapper launches Cursor
in that channel. It has no STUDIO_REPO binding today. Its existing local state, election and dispatch paths
must survive the move. The startup inbox probe reported delivery already running; no lock was removed,
no second dispatch started and no inbox work substituted for J3012.

The service renderer now supports this channel-local watcher without relocating it into the engine.
It preserves the exact reviewed poll/run tail, sets the separate engine environment and HOS working
root, and retains worker/state configuration. Unexpected argument shapes, invalid intervals and absent
channel tools fail. Offline tests cover both delivery-only and executing watchers, unchanged source data,
literal paths and refusal boundaries; preparation never executes the desk or its command template.

A proposal was generated from the actual installed plist into a fresh local 0600 file. `plutil -lint`
returned 0; source bytes, polling policy and channel working directory remained unchanged.
Installed source SHA-256: `712df6ad03f37c4f3ecf456d9a23ba7d1a1c305602600fadc79bbeb64a9bb0f0`.
Proposal SHA-256: `712b9f33fc46c30a59fab8d66a89f42f83028219d791a27c7b89392388f6a457`.
The proposal targets the isolated job worktree, not a production engine: do not install it.
No plist contents, environment values or wrapper text are committed.

Validation: 13 service-renderer tests, 12 inventory tests and 14 engine-guard tests pass.
Actual loaded-state equivalence, drained children, inherited engine selection and both MacBook slots
remain cutover checks. The existing HOS role/election behavior was not changed or approved afresh.

Next: approved deployed board Contents probe; actual MacBook inventory; drained HOS exporter guard
propagation and remaining worker wrappers; final refreshed export; preceding-day notice and live
relay/board/tick/both-worker acceptance. The previous automatic approval rejection of the probe deployment
remains unresolved and was not retried. No live service, marker, deployment, film, credential or spend changed.
