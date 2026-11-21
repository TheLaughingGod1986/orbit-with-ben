# J3012 per-owner analytics monitoring

Continued PR 1011 from 2b2b53d07e. Existing progress remains 3/4; no live move.

The prepared detached monitor now checks the studio dashboard and every registered channel snapshot history
separately, in their owning repositories. It accepts the exact daily collector subject as well as the legacy
dated subject. A report-only commit or another channel's successful update cannot make a channel look fresh.
Resident monitoring retains its four existing checks. Each channel has a distinct alarm/deduplication key.

Missing checkout paths do not fall back to engine history. Failed fetches refuse stale remote-tracking evidence.
Git operations have a 30-second timeout and return no raw diagnostics. Snapshot commits demonstrate activity,
not completeness of every API dimension; inspect the timer's collection result as well during acceptance.

Validation: 53 focused tests pass (monitor, service renderer, retirement guards, timer guard and collector),
plus 26 channel/address/private-network tests. The monitor's 15 tests include real temporary Git history proving
that report-only and unrelated commits do not count, both collector subject formats work, and another owner
remains unavailable. Offline tests cover independent stale-owner alarms, missing checkouts, failed fetches,
timeouts and nonzero Git exits. No network, account calls or installed service changes in these checks.
Whitespace and changed-file credential/address scans are also required before the commit.

Still required: reconcile loaded and installed service settings, propagate reviewed HOS guards after draining
writers, deployed board Contents probe, remaining wrapper/machine inventory and refreshed private rehearsal.
Before activation run the monitor without posting against the actual detached records. Seven official clean
days, preceding-day notice and live relay/board/tick/both-worker acceptance remain mandatory. No marker,
deployment, film change, live monitor post or spend.
