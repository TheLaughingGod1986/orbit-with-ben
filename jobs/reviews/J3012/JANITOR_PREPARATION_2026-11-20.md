# J3012: tab janitor cutover preparation

20 November 2026, Codex. Continuation of PR 1011; progress remains 3/4.

The installed Mini tab-janitor definition was read without executing its shell. Its argv exactly matches the
tracked legacy launcher: the Orbit checkout followed by `python3 scripts/cdp_tabs.py tidy`, through a login shell.
It runs every 300 seconds with RunAtLoad enabled. Installed file SHA-256:
`b64d03489a4cb3e00d52fdaf5d5c3db8cdf745ff226ab03e659f8a270340c51e`.
This resolves the earlier static scanner's unknown shell target; it does not prove the loaded definition matches.

That root matters: the janitor reads its own engine's queue to extend tab protection to three hours while a Studio
job is claimed. After the queue moves, leaving the old timer active could consult stale claims and close an active
tab too early. The proposal now launches the staged engine's `cdp_tabs.py tidy` directly with the chosen Python,
retaining schedule, log paths and existing environment. No shell interprets checkout paths.

`tidy`, including dry mode, refuses a retired engine before reading the queue/cache or contacting Chrome.
The imported cache writer also refuses before resolving or creating its destination. Imports are lazy: the
`reuse_page` helper used by channel picture scripts still loads without the registry or retirement module.
The read-only list operation and pure closure planner remain available. The retirement marker is still absent;
this change neither installs a marker nor drains any process.

Validation: 18 tab-helper tests, 11 service-renderer tests and 14 retirement tests pass. Tests cover refusal before
reads or network access, imported cache writes, claimed-job three-hour protection, literal launcher arguments,
schedule/log preservation, exclusive private output files and the existing tab/sign-in/last-tab safeguards.
The tab suite emits pre-existing unclosed-file ResourceWarnings; no test failed. No browser was contacted by tests.

Cutover: propagate reviewed guards into retained engine copies first, drain the old janitor, stage its plist with
`scripts/mini/render_service_plist.py`, inspect and lint it, then install exactly one janitor alongside the new
queue. Preserve prefix and existing first-seen cache; do not close Chrome or reset signed-in profiles. Save the
old definition and loaded state for rollback. An in-flight old invocation still requires draining; the marker is
not a process lock.

Remaining J3012 gates are unchanged: the rejected production probe deployment needs explicit approval, actual
MacBook installed/loaded inventory remains unverified, the HOS worker checkout needs safe guard propagation,
other wrappers require their documented cutover treatment, and the preceding-day notice/live relay/board/tick
acceptance are still outstanding. No services, production deployment, credentials, films or spend changed.
