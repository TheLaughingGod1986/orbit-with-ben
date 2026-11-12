# J2714 — Cloudflare migration, implementation ready

Codex covering, 12 Nov 2026. Implementation is on this branch; the live address has deliberately not switched because deployment cannot yet receive all required settings.

Completed:
- One Pages adapter calls the five existing handlers; API sources are inside the executable worker directory, not public static assets.
- nodejs_compat, API-only Function routing, shared host redirect/header generation, and BOARD_OPEN_TAPS=0.
- Python and Node clients read studio/board_site.json (BOARD_SITE_URL overrides it). The setting still points at the current site until production smoke checks pass.
- Large board files pass through without JSON parsing. Reference responses still validate their SHA.
- Wrangler confirms signed in; account details suppressed. No login step needed.
- Local Wrangler compiles all modules. Home, tracker, AI, board/classic redirects, version, invalid data, unauthorized watch, and pairing page respond correctly. Clean URL rewrites must be omitted on Pages, which already serves them; including the Vercel HTML rewrites caused a self-redirect and was fixed.

Blocker:
Locally available: WATCH_LINK_SECRET and all four R2 settings. Missing: BOARD_GH_TOKEN, BOARD_KEY, WATCH_UPLOAD_KEY. Automatic approval review rejected the brief's production Vercel environment export twice, including after its explicit item 7 authorization was cited. No export ran, no secret file was created, no secret was printed. Explicit approval to recover those settings is required before that step can be attempted again. Do not bypass the rejection.

Remaining steps:
1. After approval, recover the missing settings with vercel env pull into a protected temporary file outside all checkouts; pipe only the required values into wrangler pages secret put, then remove the temporary file. Never print values.
2. Create the free Pages project. Wrangler 4.161.0 now delegates Pages creation to Workers by default and failed static-directory detection when invoked at repo root. Its diagnostic directs using pages project create --force for the original Pages product. Do not retry the unchanged command or accept a paid plan.
3. Build with build.py, then run wrangler pages deploy from board_site with the checked-in config; direct upload only, no Git integration.
4. Verify all endpoints in the brief, signed R2 watch 302 and Range response, fresh pairing cookie, authenticated test tick and removal, and no unauthenticated tick. A synthetic test must identify itself and must not claim Ben approved a film.
5. Switch studio/board_site.json only after success, update AGENTS.md/playbook/kanban README and shell comments, merge approved PR, publish and check the minute job uses the new address. Update any existing saved watch links that still name the old host, preserving signatures/query strings.
6. Give Ben the new public address; deliver a fresh pairing link only through the existing private mechanism. He opens it on his phone and adds the new board to his home screen. Confirm his test tap reaches the thread. Phone use is his device step, not an approval of code.
7. Redirect the old Vercel project when it is available; no deletion or billing changes. Read Function request count and CPU errors after 24 h.

Not claimed: production deployment, production route verification, phone pairing, Play perception, address switch, merge, or completion of J2714. No spend or YouTube changes.
