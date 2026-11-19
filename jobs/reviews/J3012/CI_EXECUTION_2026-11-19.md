# J3012: executing the future-layout CI checks, 19 November

Status: **FIX / migration not ready**. This is preparation evidence, not live cutover approval.
Continued existing PR #1011, preserving step 3 of 4. Integrated current main into its existing head
`fad6ad762ffc24c57517be510806b1eac4d9b161`; test input source is merge commit `ece534f343`.
The one merge conflict retained the registry-aware MacBook clone test rather than reintroducing an Orbit-only assertion.

## Actual execution

Fresh isolated split under the Mini scratch root, `J3012-ci-layout-1911`. The initial structural scan used
`--no-tests`: all eight counts were zero, but its printed PASS is **not** evidence of tests passing.
Inventory: 2,264 studio files, 12,759 Orbit files, 58 HOS files, one WW2-routed file, one generated status page.
The registry then used the private studio identity, no home channel, independent sibling channel roots, and the
prepared four CI workflows plus staged hash lock. No live service, workflow or credential was installed.

| Check | Observed result |
| --- | --- |
| Shared core | `core OK (56 shared files)` |
| Rules copies | `rules OK` |
| Notes | `notes check: ok` |
| Weekly audit unit tests | Exit 0 |
| Rules workflow's eight partitioned test groups | 1,488 tests; 3 failures, 5 errors, 7 skips; exit 1 |
| Content Ops install | First attempt blocked by the local npm cache permissions; retry with a job-local cache passed |
| Content Ops typecheck and lint | Both exit 0 |
| Content Ops desk-lock pretest | Six tests pass |
| Content Ops tests | 214 pass, one fails: the real Buffer channel-file integration test |

This executes the workflow test commands locally on macOS with Node 22 and Python 3.14, not an Ubuntu/Python 3.12
GitHub Actions run. The workflow partition script is unchanged except for its log paths (job-private scratch logs
instead of shared `/tmp/tests_*`). Ubuntu package installation and hosted checkout/cache actions were not executed.
No secrets were supplied to the checks. Raw logs remain local in `J3012-ci-layout-1911/ci-logs/`; they are not
published because they include extensive fixture and machine-path output.

## Findings resolved in this continuation

1. `studio_split.build` did not create `channels/owb/channel.json` when Orbit stopped being resident. The loader
   could use a local checkout but had no cache when that checkout was absent; the cache consistency test failed.
   The builder now copies the former resident's manifest into its independent cache. A regression test proves
   the cached file and channel file are independent of the source. The source checkout is never mutated.
   This adds one generated manifest beyond the ROUTES inventory; preserve it in the final export inventory.
2. `test_studio_ci_prepare` ran the pre-cutover renderer on its already-adapted workflow inputs and required the
   old resident manifest. Its tests now use an explicit pre-cutover source fixture, so the same tests run before
   and after migration. Actual generated workflows were separately exercised above; fixture tests alone are not
   called integration proof.
3. The local harness initially named the WW2 sibling `ww2-channel`, but the split actually created `ww2` from the
   channel manifest. Corrected that local harness path. No production registry change was needed.
4. Two upcoming-gate tests classified temporary paths under `/Volumes/MiniWork` as inaccessible volume paths.
   All 12 tests in that module pass with a local `/private/tmp` test temporary directory. No media gate was changed.

After applying the two code/test fixes and the corrected sibling environment, the affected future-layout suites
(`test_studio_ci_prepare`, `test_studio_split`, `test_channels`, `test_macbook_worker`) ran **178 tests, exit 0**.
Source-layout renderer (4) and split (19) tests also pass. Channel ratchet (13), address guard (8), private-network
guard (5), core lock, rules copy and diff-whitespace checks pass. The full 1,488-test suite was not rerun; it must
not be described as passing.

## Remaining blockers and next work

- **Buffer runtime content root:** `buffer-deps.ts` derives `REPO_ROOT` from the engine package location;
  `profileFiles(profile, REPO_ROOT)` then looks for channel-owned `social/BUFFER_CHANNELS.json` in studio.
  Those records correctly remain in Orbit (including the historical HOS social register). The failing
  `buffer-hos.test.ts` integration test exposes a real runtime migration defect, not a reason to copy the social
  ledgers into two repositories. Separate engine/credential paths from the content/record root, cover the
  register, ledger, plan, project scan and relative package/media paths, and make the Content Ops workflow check
  out the required pinned channel records. Preserve existing organisation guards and zero side effects in tests.
- **WW2 browser-port assumption:** `test_jobs.MacBookTakesTextJobs.test_each_channels_nas_folder_and_studio_port_come_from_its_settings`
  fails because the current WW2 manifest has no Studio port and no `prelaunch` marker. The exact test also fails
  in the source layout, independently of migration. Resolve whether that channel requires a browser before
  changing the configuration or assertion; never invent a signed-in port or waive the check.
- Continue the earlier runbook's deployed board-token Contents probe, old-entrypoint single-writer protection,
  remaining timer migration and refreshed private rehearsal export. The remote rehearsal remains historical.
- Five official zero days are recorded through 18 November. This run did not change daily history or send a
  migration notice. Seven consecutive days and prior-day notice still gate cutover. Final relay/publish/tick
  acceptance has not happened. J3012 remains unfinished and must be released with these next steps.
