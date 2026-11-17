# J2798 — reduce the board's minute polling traffic

Implementation and bounded Chrome fixture measurements complete. Acting Chief review accepts the change for rollout; production deployment and live traffic validation follow the merge.

An open tab currently fetches the full board whenever the publisher commit changes. A static/live split still
resends the large job queue when one job changes. This change instead publishes a bounded history of structural
edits (twelve revisions, at most 16,000 UTF-8 bytes). The complete board remains available for first load,
missed history, large changes and older tabs. The browser applies edits to an untouched transport copy before
handing a fresh copy to the existing UI. Existing version.json refresh remains in place.

The API still passes file bodies through without JSON parsing. Content ETags replace commit/length ETags, and
weak/list If-None-Match validators work. The tracker revalidates its branch file, so a new board commit with the
same tracker content returns 304. Existing authentication, ticks, open-tap setting and R2 are unchanged.
No new service, package, billing setting or credit spend.

Validation completed:
- 37 publisher/build tests passed.
- 23 data API tests ran: 19 passed, 4 browser tests skipped by the existing Node dependency probe.
- The same existing real-browser auth harness was then run explicitly using Python Playwright's Node driver
  and installed Chrome: private signed-in, private signed-out, public; all behaved correctly, zero direct
  browser GitHub requests. Raw results are in the local log named below.
- 5 new publisher/browser parity tests passed, including job removal/insertion/reordering, randomized lists,
  bounded ten-minute history and oversized-history fallback.
- New JS client tests passed: edit chain, UI mutation isolation, missed-window full fetch, 401, unsafe paths.
- Existing Studio JS regression suite passed; 4 board-site tests, 8 email checks and 5 private-network checks passed.
- Site build and git diff --check passed.

Pending evidence (do not substitute the 16 KB file cap for measured browser totals):
- Live ten-minute baseline: tmux J2798-before-pages; local logs J2798-before.log / .done / .json.
- Twenty-minute real Chrome fixture measurement (ten idle minutes, then ten with one film change): tmux
  J2798-updates-measure; local logs J2798-after.log / .done / .json.
- Both run on the Mini; logs and helper script are under the local desk logs directory. The fixture uses
  the real API and a frozen local board snapshot, never changes a live film, and records phone-profile first
  render and CDP encoded transfer bytes for / and /tracker.
- The custom board domain failed DNS resolution in Chrome; the live baseline uses the existing Pages address.
- A first baseline attempt failed because bundled Chromium is absent; installed Chrome is used instead.

Next run: inspect both .done exit codes and logs; if missing, do not start a duplicate. Record actual numbers,
check cards/counts and <20 KB/min idle budget, review and resolve any failures, then update this result and
merge the single PR through the normal checks. Re-check elected Chief before protected decisions. Pull main,
roll out the publisher (including updates.json), build and deploy the Pages site using the existing documented
free-plan command, then verify live /, /tracker, /ai, version.json, auth and headers. Production measurements
are still needed if fixture results cannot establish the requested acceptance evidence.

Required disk offload ran before implementation; no scratch was old enough, so it moved nothing. Worktree and
build are on the working SSD. The Mini system disk remains low; no NAS files were deleted.

## Resumed review, 14 November

Both detached captures exited 0. Ten-minute transferred bytes (CDP encodedDataLength, initial load excluded):

| Page | Live baseline | Local Chrome fixture, idle | Local Chrome fixture, one film change |
| --- | ---: | ---: | ---: |
| / | 1,751,721 | 17,615 | 27,647 |
| /tracker | 141,613 | 7,100 | 8,822 |

Phone-profile first render was 514/440 ms on the live baseline and 129/153 ms on the local fixture. These are different network conditions, so they establish working phone rendering, not a measured speed improvement. The fixture uses the actual publisher diff and actual API handler but a local HTTP server, without compression; it changes only a fixture film. No live production film was altered.

Re-ran 37 publisher tests, 5 parity tests, 19 API tests (4 existing browser checks skipped by dependency probe), JS transport and full Studio app regressions: PASS. Site build and diff whitespace check: PASS. Existing explicit Chrome auth capture remains the browser authentication evidence. Current main merged cleanly into the branch.

Chief review: KEEP. The bounded edit-history design meets the small-update objective while avoiding retransmission of the whole live queue, which a simple static/live split would still cause. The full snapshot and version-based reload preserve older clients. The function hashes raw bytes once per held copy and does not parse the board payload. Production validation must confirm live API status, content ETags/304 and ten-minute transfer totals; rollout will be reported separately on the studio thread.

## Production acceptance failure and correction

The first production rollout did not meet acceptance: the live board carries 312 per-film production timestamps. Updating those repeated fields made a normal edit payload 31,257 bytes, over the history cap, so history was discarded and clients fell back to a full snapshot. The small local fixture missed this. J2798 remains incomplete until a new production capture passes.

A correction groups consecutive identical updates to the same field across list entries, preserving exact indices and operation ordering. On the captured live delta this reduces 31,257 bytes to 3,373 bytes. A new 312-film regression verifies history stays within budget and reconstructs the full snapshot exactly; an additional splice-order test verifies compaction does not reorder edits. Seven parity/publisher tests and the JS client suite pass. Older clients safely fall back to the full snapshot for the new operation, then receive the usual version reload. No film data is omitted or made stale.


## Third-run production diagnosis

The corrected production capture exited 0 but failed acceptance: / transferred 1,744,298 bytes in ten minutes (174,429.8/min), while /tracker transferred 25,610 (2,561/min). Phone first render was 624/451 ms, with no JavaScript errors. These figures include normal live publishing and are not a frozen-film experiment.

A fresh real Chrome probe showed the cause: /api/data?f=ref and pinned updates/board requests intermittently return 502 with GitHub 403. Branch-file reads still return 200. The commit lookup exhausts the unauthenticated GitHub API budget, triggering public full-snapshot fallback. No token was added or changed.

The correction reads the bounded updates file directly from the branch, avoiding the commit lookup on the board refresh path. The publisher adds the SHA-256 of the exact published snapshot bytes; the browser assigns a revision only when the full response ETag matches that hash. A publication race therefore retries a full snapshot safely rather than applying edits to mismatched data. Existing raw-file caching and authentication remain in place, without parsing files in the Function. The old reference path remains for clients without the update transport.

Regression checks cover the exact published byte hash, branch reads without a commit lookup, and mismatched-snapshot recovery, alongside existing parity, API, publisher and client tests. Final production traffic acceptance remains required after deployment.

## Fourth-run correction: retain history during frequent publishing

The branch-read capture exited 0 but still failed: / used 1,134,292 bytes in ten minutes (113,429.2/min), /tracker 25,691 (2,569.1/min); phone first render 1,052/879 ms. No page errors. Five recurring full board responses account for the failed budget. Local publisher inspection found only two retained revisions: a few publishes between polls can discard the chain.

Compress the edit history on the publisher using deterministic gzip, in a schema-2 base64 JSON envelope capped at 14,000 bytes, retaining up to 120 revisions. Browser DecompressionStream decodes it before the existing exact replay. The function still performs no JSON parsing or compression. Missing browser support or corrupt/missed updates falls back to the full snapshot; older tabs also fall back and receive the normal version reload. Exact snapshots, cards, counts, authentication and approval writes remain unchanged. The smaller wire cap leaves room for heartbeat/version headers within the 20 KB/min goal.

Validation: 9 publisher/browser parity tests (including 30 frequent live-sized publishes), 37 publisher/build tests, 19 API tests passed (4 dependency-probe browser skips), JS client gzip/recovery and Studio regression suites passed; site build and whitespace checks passed. Production acceptance remains pending; no claim of completion. Chief review KEEP for this correction, subject to CI and real-browser rollout measurement.


## Worker follow-up: stale CDN responses, 14 November 08:35 UTC

Acceptance remains unmet. The completed packed production capture exited 0: `/` transferred
1,464,280 bytes in ten minutes (146,428/min), `/tracker` 15,081 (1,508.1/min).
Phone-profile first render: 800 ms and 612 ms respectively. Neither page reported a JavaScript error.
The board downloaded six full snapshots including its initial load; tracker reference reads intermittently
returned 502, although tracker transfer stayed within budget.

The completed packed fixture also exited 0, but its board totals were invalid acceptance evidence:
21,370,656 idle bytes and 21,380,958 one-film-change bytes, versus tracker 7,902/8,020.
The harness serialized snapshots with JavaScript and omitted the publisher's trailing newline, so
its ETag could never match the publisher snapshot hash. The correction uses the exact Python serializer
and raises the child output buffer for the full-sized snapshot.

A fresh instrumented production Chrome session demonstrated a separate failure. The update revision
advanced, then the next response supplied an older revision already seen by that session. Its full-snapshot
fallback returned a newer board than the stale update hash; revision assignment was therefore cleared.
This is consistent with independent CDN stale-while-revalidate responses, rather than a broken edit chain:
the captured histories had no chain breaks and browser gzip decoding succeeded.

Correction for Chief review: include the snapshot publication timestamp in the small update envelope.
When an update predates the browser's current snapshot, retain the current snapshot and retry the usual
minute poll. A newer update still replays normally. Missing timestamps retain the existing fallback, so
older publisher payloads remain compatible. The Function still passes raw bytes without parsing JSON,
and authentication, approval storage, R2 and open taps are untouched.

Validation: 10 publisher/browser parity tests, 37 publisher tests and 19 API tests passed; four existing
API browser-probe tests skipped. JavaScript transport regressions passed, including a stale response
followed by a fresh edit without another snapshot download. Site build and whitespace check passed.
No new deployment, merge, final OK or acceptance PASS was made by this worker.

Two fresh captures run detached: `J2798-live-current` measures the existing deployed version for ten
minutes; `J2798-fixture-exact-v2` measures ten idle plus ten one-film-change minutes using exact publisher
bytes. Their local desk log basenames match the tmux names (with `.log`, `.json`, `.done`); missing done
means still running and must not be duplicated. The first exact-fixture attempt exited before browser
startup because its child output exceeded Node's default buffer; v2 fixes that. Production acceptance
for the timestamp correction requires Chief review/merge/deployment and a new ten-minute measurement.

Required low-disk offload ran; nothing was old enough to move. No NAS content was deleted.

Real Chrome authentication rechecked against the corrected build: private signed-in and public pages
rendered; private signed-out pages requested sign-in. Zero direct browser GitHub requests in all three
scenarios. Correction submitted as PR #924, commit 5dfaf25d3a. Chief review/merge/deployment required.
