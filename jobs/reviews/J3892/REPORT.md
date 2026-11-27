# J3892 preparation result

27 November 2026 — `macbook-2`.

Implemented `scripts/macbook_cutover.py` in an isolated clean worktree. It provides read-only private preparation, one detached bounded supervisor and a separately activated transaction. The existing queue is the terminal-job/claim authority; the existing studio thread supplies the immutable, fresh, trusted exact-commit activation. No parallel queue or production status tracker was introduced.

The helper retains private originals and file metadata, verifies expected source/installed/loaded/proposal hashes, refuses owner PID reuse or surviving groups/agents/claims/held locks, and repeats checks before replacing only the worker service. Both staged engine mains are preserved under backup refs before the exact production commit is selected. Partial failure leaves evidence and pauses; it never resumes a stale queue automatically. The README gives the concrete invocation, activation, cancellation and retry sequence, including the elected-Chief attestation boundary.

Validation: **34 focused tests passed** with all real process/Git/service dispatch forbidden or mocked; **13 privacy checks passed**; diff check clean. The private receipt and fixture transaction originals are retained under `~/_desk/state/j3892-dry-run/20261127T121029Z/`. `DRY_RUN.json` records their exact receipt/source hashes and zero real children/live changes. Earlier receipts are retained as historical iterations; only the final receipt matches this code.

Self-review specifically caught and corrected the large authoritative queue boundary: the queue is larger than GitHub's inline contents response, so the adapter uses the raw authenticated contents representation. Focused coverage also verifies loaded arguments/environment exactly, command deadlines, safe branch preservation, private one-shot detached launch, nonterminal/claim/PID/group/lock refusals, changed source/proposal/activation, cancellation/deadline races and failure after replacement starts. The full legacy suite and completed inventories/probe were not repeated.

No live pause, bootout, install, restart, engine marker, staged/production Git operation or rehearsal queue execution occurred. No supervisor was started. No film, account, spend, remote-login, production/default branch or existing service was changed. Only mocked fixture files were changed during dry run. This is preparation evidence, not live cutover acceptance or an independent Chief approval.

Next: elected Chief reviews the PR; after merge and global prerequisites, a separately authorized coordination child prepares/launches this reviewed helper, completes and exits. Chief then records the exact fresh production commit/queue activation. J3012 remains **3/4** until the coordinated acceptance work succeeds. Nothing here authorizes a live switch.
