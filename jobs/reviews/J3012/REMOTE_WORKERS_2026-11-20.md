# J3012 — remaining Mini remote-worker boundaries

20 November 2026. Continued PR 1011 from `0db7e2aa43183ad1d5198a277c2e491b435e7841`.
Preserved the existing 3/4 plan. This is readiness evidence, not migration acceptance.

Read the four installed launchd definitions and their explicitly referenced wrappers without executing them.
No environment values or complete local wrapper contents are included here.

| Service | Observed loaded state | Actual behavior |
| --- | --- | --- |
| `com.cursor.mac-mini-worker` | running | Long-lived remote Cursor worker; permits OWB plus one unrelated project. No task prompt in wrapper. |
| `com.cursor.mac-mini-hos-worker` | running | Long-lived remote Cursor worker; permits HOS only. No task prompt in wrapper. |
| `com.cursor.mac-mini-repo-workers` | not loaded | Supervisor for seven unrelated project workers; none targets a studio/channel checkout. |
| `com.hos.local-wan-ltx-queue-reminder` | loaded, not running | Creates a local handoff directory and appends two reminder lines; no queue, network, model or generation command. |

Wrapper SHA-256, in the same order:

- `1bdf371abec02898d4c12c87647b26f52204effe4497f08b123927c1d9703cf7`
- `4d6fe65045459b40b37c4f32fd41e0300a5c21f5dddfc521b5fa814edd105037`
- `84bd4ca5a7acbb84cd2b62b68067627e858446d2a2a15365864722736164920d`
- `577aaf9850e48675f79c634e2e4d084da9d7666e5b6f6bb320750d791fc015d4`

All four pass `bash -n` (exit 0). Loaded states came from the existing sanitized inventory helper, not a raw
launchctl environment dump. No process arguments or credential values were logged. These observations do not
establish whether remote tasks are active or whether remote instructions reference the old engine.

Chief disposition: retain the unrelated supervisor and reminder unchanged. The two studio-capable remote
workers need a drained cutover and reviewed proposal preserving channel access and identity while adding the
new engine access/environment. A blanket old-root replacement is wrong: OWB remains a channel. The runbook
now gives explicit preparation, resumption and rollback requirements. No live change was made.

Remaining: actual MacBook installed/loaded inventory; reviewed remote-worker proposals and session drain;
safe HOS exporter guard propagation; final export; preceding-day notice; live relay/board/tick/worker proof.
The prior board runtime-probe deployment rejection remains unresolved and was not retried. No new approval
was inferred. The seven-day split result and prior rehearsal are retained, not rerun unnecessarily.
