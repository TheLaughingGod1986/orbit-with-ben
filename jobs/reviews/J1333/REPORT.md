# J1333 — OWB029 watch-link correction

Codex, 31 October 2026. GBP0. Operational correction complete; code PR #368 remains open.

## Identity and approval

J0991 RULING.md and J0961 brief supply each full PHONE hash. J0961 history records Wednesday v04 approval at 2026-10-28 11:13:22Z and Claude release at 11:16Z; Friday/Monday preserve Ben v03 approvals 6411249334 / 6411258896 with unchanged picture and J0991 audio repair acceptance. No approval has been added or inferred from version order.

Fresh hashes of all six main-checkout top-level/nested PHONE files match those exact hashes (`sources.json`). CloudDocs source reading initially returned errno 11 (dataless file); uploads deliberately read the verified main-checkout copies instead. No CloudDocs file was rewritten. Both relative CloudDocs aliases and absolute main-checkout aliases explicitly map to each cut's own ID, twelve exact mappings in both local and PR registers.

## Correction and verification

Uploaded only the three existing hash-verified PHONE files under distinct per-cut/version IDs. Preserved old owb-029-v04 and every old R2 object. Republished through scripts/board_publish.py --force. Published board-data has four affected links: Wednesday approved card and tracker, Monday film card and tracker. Each uses the intended distinct ID (`published_cards.json`); Friday has no current v04 board card, so both registered Friday aliases were tested directly through signed Play.

`signed_play_readbacks.json`: **PASS 6/6**, actual signed /api/watch redirects read through to filename, complete byte length and SHA-256, without saving the streams. Wednesday eeb6196d5d474954eabbf8d87bbde041c97047948687af40eb544d83f8516d4d differs from Monday 04947ca92e610b6bc6adb49f1ed5cc598a1e6e3607e6e29925b3b4a32496db22. Python urllib encountered HTTP 403 on playback; Node fetch successfully read all six signed streams. No signed URL, key or random storage object key is retained in evidence.

`board_check.py --no-post`: **PASS**, ok true, expected 1, problems [], site 200. `python3 -m unittest discover -s scripts -p test_watch_links.py`: **12 tests PASS**, including distinct same-version cuts through both auto-upload routes, intentional nested aliases and bounded IDs.

## Code PR and remaining limitation

PR #368 fixes the demonstrated generation collision: film and approval-card auto-upload IDs now include a digest of the exact basename, preserving same-cut nested aliases and distinguishing same-film/version cuts. Existing registered IDs are preserved unless explicitly corrected. Neither modified script is a studio-core locked file.

CI: one check passes; full script suite runs 554 tests with one failure, `test_kanban_page.VenusApproved.test_023_note_is_off_bens_box_and_shipping`, an obsolete Venus status-note assertion. The same failure reproduces in the unchanged shared main checkout (75 kanban tests, one failure). Watch tests all pass in CI. PR left open; no failed-check override or unrelated test edit. Next elected-Chief action: resolve that baseline check and merge the focused PR; live aliases are already repaired through the local register.

J1322/J1100 holds, approvals, all media, all NAS files, uploaded records and YouTube/Buffer state remain unchanged. Disk stays below 20 GiB; authorized NAS offloader found no eligible old scratch. No film PASS, generation, new watch request or public distribution.
