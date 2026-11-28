# J3012 — remote-worker proposals

20 November 2026. Continued PR 1011 from `1017357423`, retaining step 3 of 4.

The installed Cursor CLI help states that `--worker-dir` is repeatable and its first value is assignment
identity. Personal workers can have concurrent sessions. These observations resolve the local option semantics;
they do not establish remote instructions or drain status.

Added a preparation-only helper that verifies the inspected wrapper SHA-256, preserves credential setup and
all existing identity/access arguments, appends the engine root, and binds the four independent repository
roots. Unknown argument shapes, changed source bytes, relative/multiline roots and duplicate engine access
are rejected. Shell path values are quoted. Outputs are exclusively created, mode 0600, outside Git.

Both installed wrappers from REMOTE_WORKERS_2026-11-20.md were staged privately at
`/private/tmp/j3012-remote-proposals-0953`. Both passed `bash -n`; both installed source hashes remained
unchanged. No wrapper ran and no service, remote prompt, credential or launchd definition changed.

Validation: 31 tests passed (six proposal boundary tests, twelve service inventory tests, thirteen
network/address safety tests). The proposal tests check identity/root ordering, unchanged local setup,
changed-source rejection, unsupported flags, literal shell metacharacters, malformed roots and duplicate
engine access. No media or film stage was touched.

Remaining: drain and controlled-task proof for the remote workers; actual MacBook installed/loaded inventory;
HOS exporter guard propagation; approved deployed board Contents probe; final export; preceding-day notice;
live relay/board/tick acceptance. Earlier automatic-review deployment rejection remains unresolved; it was
not retried. No live move or spend. Keep the overall job open at 3/4.
