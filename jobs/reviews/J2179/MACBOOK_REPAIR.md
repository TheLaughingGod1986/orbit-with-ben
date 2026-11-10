# J2179 MacBook repair for J2182

5 November 2026, agent macbook. Addresses both J2180 P1 findings on PR512.

Every opt-in body source now requires readable regular-file bytes before its content hash can identify reuse. Missing files, broken links, directories and read failures produce protected terminal-loop failures. No unverified pathname masquerades as a content identity. Explicit footage rows require finite nonnegative offsets. Opt-in mixed footage runs continue per-row reuse checks even with incomplete metadata; valid neighboring rows still detect within-run replay. Legacy opt-out behavior and legitimate stills remain supported.

Regression evidence: MACBOOK_TESTS.txt retains 12 terminal-loop and 12 legacy tests passing. Added absent/broken-link/directory/read-error, missing/null/nonfinite/negative/boolean/string offsets, adjacent valid replay, legitimate still and unchanged opt-out cases. Synthetic body files have real distinct bytes. Completed J2169 fixtures now pass through content-identity source_checks and retain exactly B S04/S05 and C S05 failures. py_compile, sync_rules --check, core_sync check (56 shared files) and git diff --check pass. No changed file is studio-core. Playbook/Cursor clarifications remain proposed pending elected-Chief review J2182. No production media generated, spend, NAS, YouTube or Buffer writes. J2169 remains blocked.

## Queue helper incident

Started macbook/J2179 from existing PR512 head be2c980ff. The required jobs.py progress --git invokes studio.git_transaction, which pulls/rebases onto main and pushes HEAD:main. It replayed the previous unmerged implementation as 03e570eec and CI dependency change as 1708dd233, then queue progress c983b2cb5 onto main. This was not an intentional merge or approval. No repair code was committed when that happened. Do not interpret presence on main as Chief acceptance. Repairs are submitted on macbook/J2179; PR512 and J2182 must be reconciled by elected Chief. No force-push or rollback was attempted. Subsequent queue updates run on main with no implementation commits pending.

Thread read through #6649295295; ordinary read retrieved messages but could not persist ~/.owb_thread_state due sandbox restriction.
