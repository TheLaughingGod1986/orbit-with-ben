# J3012: isolated analytics gate and bounded auxiliary phase

20 November 2026. Continues PR 1011 from 56d1bc6cbe; existing progress remains 3/4.

The required callback now runs bounded dispatch and registry-selected gates. The gate adapter loads each
channel's own settings, reads source media, writes library JSON and frames only into that channel's record
worktree, and keeps frame links relative. Source-relative VO lookups still work. Retired engines, mismatched
owners and symlink destinations refuse. No shared gate implementation or core lock was modified.

The split now retains the channel-owned profile in the channel tree as well as its temporary engine copy.
Without that correction, a clean channel layout could not supply the profile even though today's untouched
source checkout could. Legacy shared callers still need the engine compatibility copy.

Verification:
- 59 analytics tests pass, including 13 new tests across the adapter, auxiliary phase and collection sequence.
- Tests exercise real gate modules with synthetic frame operations, plus an actual bounded child subprocess
  generating an empty upcoming report. Source records stay untouched; new library entries contain relative
  frame links and the channel-specific profile controls the check.
- Collection integration confirms gate timeout is reported while reporting and publication still run;
  dispatch uses the shared queue, gate media uses the source, records use the detached channel worktree.
- Split and channel-ratchet tests pass; no ceiling raised. Additional split/security results are recorded below.

Limits: no live gate, account call, dispatch or service change. No claim of full timer acceptance: next wire
the shell entrypoint/plist and bounded cache readability fallback, then test collectors, gate, record commits
and retries with fake APIs and local Git remotes. Board credential access, writer inventory and refreshed
private rehearsal remain. Seven daily clean records, previous-day notice and live acceptance still gate the
move. No money spent and no Ben action needed for this preparation.

Final local split verification at source 134b6f878c, 20 November 03:08 UTC: all eight groups zero, left 0,
tests run, exit 0. Layout: 2,355 studio files, 12,857 Orbit files, 60 History of Science files, one Field Order
History file and one generated file. This is the baseline split identity, not refreshed future-identity remote
rehearsal or live acceptance. Official daily history was not modified. The changed-file address/credential
scan found zero; 42 split, channel-ratchet and private-network tests passed. Local result and log remain at
Mini scratch J3012-0300-split.json and J3012-0300-split.log.
