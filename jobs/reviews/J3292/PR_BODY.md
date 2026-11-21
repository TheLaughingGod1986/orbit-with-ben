## Change

Urgent video pulls previously reached the studio thread and board watch cards without a prominent warning. The board publisher now detects recorded schedule changes within 24 hours and pending watch deadlines within 12 hours across channels, reserves one initial alert plus one halfway reminder, and stops resolved watch alerts. Every Studio page displays a red warning linked to the watch card or Review.

The thread fallback uses file-based posts. Optional free ntfy delivery reads its secret URL only from the publisher environment. No phone setup or deployment was performed. Claude has been asked to relay the one-line proposal to Ben before setup: https://github.com/TheLaughingGod1986/orbit-with-ben/issues/954#issuecomment-7063129917 .

## Validation

- 8 urgent-alert tests, including trigger/reminder limits, completion, restart deduplication, restored schedules, dry-run behavior, delivery file handling and banners in all three built pages.
- 42 board publisher tests and 4 board site tests passed.
- Email ratchet (8) and private-network checks (5) passed; JavaScript syntax and diff checks passed.

## Release and limits

Chief review/merge and site publication are still required. Monitoring uses recorded tracker state, with a first-run baseline and the existing full-board rebuild interval (at least every two minutes). Missing state is unknown. Delivery reservations bound attempts across ambiguous network failures; they do not guarantee exactly-once phone delivery. Phone delivery requires the Claude chat handoff, one subscription step and a subsequent phone read-back.

Queue progress is included on this branch: jobs.py --git refuses worker branches and pushes directly to main, conflicting with the explicit instruction never to push to main.
