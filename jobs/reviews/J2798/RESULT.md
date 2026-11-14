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
