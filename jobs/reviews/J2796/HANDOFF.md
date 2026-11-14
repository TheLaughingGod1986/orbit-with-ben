# J2796 worker handoff

Shared address: `BOARD_SITE_URL`, otherwise `studio/board_site.json`. All production Python clients use `board_site.site_url`; Node reads the same JSON. WATCH_OK admits explicit hand-set links only, while generated links use the configured URL. Tracker/stage-sync requests now identify themselves: the default Python user agent was rejected by Cloudflare (403); with the studio user agent both reach the intended missing-token response.

Deployment: https://0227fc02.studio-kanban.pages.dev (production https://studio-kanban.pages.dev), 14 Nov 2026 around 02:05Z. Both `/` and `/tracker`: 200, `X-Robots-Tag: noindex, nofollow`. The wildcard header is generated from vercel.json; API responses set it in the worker as Pages headers do not cover Functions. No secrets, R2 records, ticks, or open-tap settings changed.

The existing Cloudflare migration PR #858 remains OPEN. Its adapter, build configuration and data streaming adjustment are copied here to preserve the already deployed runtime; use its established shared-address module rather than introducing a competing setting. Chief should merge #858 first, then resolve any overlap here while preserving the live default and noindex additions. This worker did not merge either PR.

## Validation

- Live `board_check.py --no-post`: ok=true, expected=6, problems=[], site=200.
- Tracker and stage-sync URLs: production `/api/checks`, HTTP 500 with `BOARD_GH_TOKEN isn't set` (expected J2714 token hold).
- Watch links: 13 tests pass; stage sync: 10 pass.
- Board suite: 116 run, four skipped, one failure: the new retired-address guard correctly flags ONLY protected AGENTS.md.
- Targeted corrected fixtures: benauth 13 pass; approved 17 pass; uploaded 15 pass; awaits 5 pass. Studio JS regression checks pass.
- Cloudflare route contracts, watch redirect, cookie round-trip and API noindex checks pass.
- Private-network (5) and email-ratchet (8) checks pass.

## Chief actions before completion

1. Apply `AGENTS.patch` (one URL correction) under Chief authority. The worker was explicitly forbidden to edit AGENTS.md. Re-run `python3 -m unittest discover -s scripts -p 'test_board_site.py'`; its guard is intentionally strict and has no protected-file exemption.
2. Current live board data has THREE retired-host mentions, rather than the six in the brief. They are NOT navigation links. Sources: `jobs/queue.json`, J2532 `hold.condition` and its last history entry (`last.what` in board JSON); the same stale hold is projected as `workflow.states.J2532.reason`. The condition still says Vercel billing blocks deployment. J2795 owns J2532's current deployment review; Chief should reconcile its obsolete hold through queue APIs there. Keep the historical reroute record accurate; changing a hostname in that historical sentence would falsify its meaning. No unrelated job was claimed or its history rewritten.
3. Review and merge the PR. J2796 remains incomplete until protected doc and source-state corrections are resolved and merged. No worker final OK/PASS claimed.
