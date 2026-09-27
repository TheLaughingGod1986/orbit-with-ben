# Archive

Superseded material, moved here on 25 Sep 2026 when the repo was cleaned up. **None of it is in force.** The docs in force are listed in `AGENTS.md`.

Files keep their original paths under `_archive/` (for example `_archive/00_Brand/Channel-Setup/ORBIT_HOUSE_AND_UAT_BIBLE.md`), so `git log --follow` still shows their history.

| What | Replaced by |
|---|---|
| `cursor-rules/` (26 old `.mdc` rules, renamed `.md` so Cursor never loads them) | `.cursor/rules/` (6 rules) + `AGENTS.md` |
| House/UAT bible, Omni long-form playbook, long-form story/VO gate, Moon Leaving v04 lock, Growth System v2, retention lock, publishing/cadence/schedule docs, release checklist, package template, Shorts funnel doc | `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` |
| `00_Brand/CHANNEL_BUILD_SYSTEM.md` | `AGENTS.md` |
| Week plan of 23 Sep | `FAMILIAR_DANGER_STRATEGY.md` (the week-one scripts moved into their project folders) |
| One-off Studio/CDP scripts (`scripts/`, `Channel-Setup/_*.py`), result JSONs, old audits and their fix scripts | Nothing. They were single-use. Current audits stay in `Channel-Setup/audits/`. |
| `02_Video-Projects/007_Neutron-Star/` (empty scaffold) | `02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/` |
| Old `README.md` | `README.md` + `AGENTS.md` |
| `00_Brand/Channel-Setup/{Meta,Threads,TikTok,social}/` (Mac LaunchAgents, Chrome/CDP posting scripts, posted ledgers, TikTok pause file), archived 27 Sep 2026 | The Buffer mirror: `STUDIO_PLAYBOOK.md` §12, `07_Content-Ops/scripts/buffer-mirror.ts`, `00_Brand/Channel-Setup/social/BUFFER_*.json`. The Shorts caption library moved to `00_Brand/Channel-Setup/tools/onscreen_captions.py`. |
| `07_Content-Ops/docs/{META,TIKTOK,X}_CONNECTION_SETUP.md`, `THREADS_PUBLISHING_ASSESSMENT.md` | Buffer |
| `07_Content-Ops/` web app, retired 27 Sep 2026 (Vercel project orbit-content-ops): `src/app`, middleware, publishing worker, Prisma schema and migrations (Neon database), platform adapters, OAuth, affiliate `/go/` redirect and tracking, the daily Vercel Buffer cron, their tests, docs and DB scripts | The local CLIs in `07_Content-Ops/` (no database). YouTube login in `.env` via `npm run youtube:auth`. Buffer record in `social/BUFFER_POSTS.json`. Daily Buffer check via LaunchAgent `dev.orbit.buffer-check`. Affiliate links paused (`STUDIO_PLAYBOOK.md` §11). `07_Content-Ops/vercel.json` tells Vercel to skip every build until the project is disconnected. |

To bring something back, `git mv` it out of `_archive/` and add it to the docs in force in `AGENTS.md`.
