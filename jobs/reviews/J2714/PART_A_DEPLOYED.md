Codex covering — J2714 Part A deployed, 12 Nov 2026.

New board: https://studio-kanban.pages.dev

Deployed PR #858 head 4c9e273669dc09413b3cbc2ea900c3490c5dbe80 by direct upload to the free Pages project studio-kanban. No Git integration, card, payment, new key or Vercel export. Set only the four locally held R2 settings and WATCH_LINK_SECRET; BOARD_DATA_REPO and BOARD_OPEN_TAPS=0 come from the checked-in configuration.

Verified production: /, /tracker, /ai and /version.json return 200; /board and /classic land on the home page; version has no-store. /api/data?f=ref and the referenced board data return 200 (about 2 MB). A newly signed Play link returns 302, then R2 returns 206 for a 1 MB Range request. ffprobe identifies H.264 720x1280 and AAC in those bytes. A Play link read from the newly published board data also returns 302. This is transport/codec evidence, not a claim to have watched or heard the cut.

The Mini's every-minute publisher now has a persistent BOARD_SITE_URL override in its LaunchAgent, and the launchd environment has the same override. Reloaded the agent; publish log records board-data 5f9f4664 at 20:38:31Z, and the served board data contains 85 Cloudflare watch-link occurrences. Stopped the redundant legacy two-minute shell publisher loop, which retained the old environment; the minute LaunchAgent remains active. Existing running agents may retain their old environment until restarted; the next-run PR merge/default-setting switch remains necessary.

Ticks and phone linking DO NOT work yet. An unauthenticated tick returns 401 with the plain message that the phone is not linked, without a false saved response. Reading checks returns 500 with BOARD_GH_TOKEN isn't set. The old 75 checks remain in the publisher's retained state. Do not treat a tap as saved or attempt phone linking yet.

Validation: adapter parity test passes for five routes, watch 302, cookie renewal/readback and POST body; 15 Python address/watch-link tests pass (with PYTHONPATH=scripts). Initial Python URL probes were blocked 403; direct curl from the Mini verified production successfully.

Part B remains held under the explicit brief: BOARD_GH_TOKEN, BOARD_KEY and WATCH_UPLOAD_KEY can be recovered only after Ben's explicit approval is recorded. No such approval is at the top of the job. No export was retried. Next run: read the approval, transfer only those three settings if authorized, redeploy if needed, verify pairing and a reversible test tick, review/merge PR #858 and switch the tracked address/docs. Redirect the old Vercel site when available. Read Function requests and CPU-limit errors after 24 hours; no first-day total is claimed today.

Ben can open the new address now to read the board and use Play. Phone linking and adding a fully working approval app to the home screen follow Part B.

Thread read to #6835208289.
