# Urgent video alerts

J3292 adds monitoring to the existing board publisher, under its single-writer lock. It uses every channel in the resolved video tracker and the full queue. The normal full rebuild runs at least every two minutes; there is no new daemon.

- An observed scheduled video that loses its slot, changes video id, or is pulled within 24 hours raises an alert. Going public is not a pull. First run establishes the baseline; a missing card or unreadable YouTube state is unknown, not a cancellation. This monitors recorded studio state, not YouTube directly, so workers must keep the existing records current.
- A remaining watch card with a deadline within 12 hours raises an alert. Ben's applied response removes the ask; a done/cancelled job also stops it. Past-due watches raise one alert without a reminder.
- Each event has at most two reserved delivery attempts: initial and halfway through its remaining time. Schedule alerts with an associated watch use the earlier deadline. A restored original slot or another scheduled replacement clears the schedule warning. Local state survives restarts in the publisher's state directory.
- Red banners appear above every built Studio page (including AI and Tracker), refresh every minute, use the board's existing authentication, and link to Review/the watch card. Text is inserted with textContent.
- The thread receives the same message from a temporary file. Optional phone delivery reads STUDIO_URGENT_NTFY_URL from the publisher environment only. No topic, account or subscription has been set up, no notification has been sent to a phone, and no secret belongs in a tracked file. A URL is never included in logs or board data.

## Phone handoff

Claude must relay the one-line proposal to Ben in chat before setup. The request was posted at https://github.com/TheLaughingGod1986/orbit-with-ben/issues/954#issuecomment-7063129917 . The proposed route is a free ntfy subscription, per https://docs.ntfy.sh/publish/ . Ben subscribes once on his phone; only after that handoff may the operator set the unguessable topic URL in the publisher environment, outside git. Keep the free service: no billing, account changes or paid fallback. The topic is a bearer secret. Verify delivery on the phone after setup; an HTTP response alone is not phone read-back.

## Delivery limits and release

Reservations are persisted before network I/O. An ambiguous timeout/crash is not retried automatically, avoiding duplicate phone alerts; its delivery result is recorded locally and the red banner remains. This provides bounded attempts rather than a false promise of exactly-once network delivery.

Dry runs calculate banners without writing alert state or sending messages. No service has been installed or started by this job. Chief must review/merge the PR and publish the site using the existing release workflow; phone setup and end-to-end phone delivery remain pending the Claude chat handoff. No deployment or production alert claim is made.

Queue progress is included on the worker branch without --git: the current --git implementation explicitly requires main and pushes metadata to main, which the MacBook job instructions forbid.
