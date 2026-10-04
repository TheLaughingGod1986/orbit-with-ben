# Orbit Content Ops (local CLIs)

Command-line tools for **Orbit With Ben**. There is no web app and no database: the hosted ops app (Vercel project `orbit-content-ops`, Neon Postgres) was retired on 27 Sep 2026 and lives in `_archive/07_Content-Ops/`.

## Setup (once)

```bash
cd 07_Content-Ops
cp .env.example .env      # fill in locally; never commit or print values
npm install
npm run youtube:auth      # sign in as Orbit With Ben; saves YOUTUBE_REFRESH_TOKEN into .env
```

## Commands

| Command | Purpose |
|---------|---------|
| `npm run review:script -- --file <script.md>` | Script reviewer (long scripts need 90+) |
| `npm run gate:episode -- --project <…>` | Episode gate (blocks VO/picture until PASS) |
| `npm run youtube:package -- --package <…/11_Upload-Package> --video <mp4> [--dry-run]` | Upload to YouTube, then mirror to Buffer (`--no-buffer` to skip) |
| `npx tsx --env-file=.env scripts/retitle-videos.ts --file <fixes.json> --dry-run` | Title-only changes |
| `npx tsx --env-file=.env scripts/update-pinned-comment.ts --dry-run` | Weekly pinned-comment refresh |
| `npm run buffer:mirror -- --video <id> --long <longId> --media <mp4>` | Mirror an upload made another way to Buffer |
| `npm run buffer:check` | Keep Buffer in step with Studio, and mirror scheduled uploads not in Buffer yet (the Mac runs it daily: `launchd/dev.orbit.buffer-check.plist`) |
| `npx tsx scripts/buffer-mirror.ts register --video <id> --media <mp4> --long <longId>` | Tell the daily check which file a hand-made upload came from |
| `npm run diagnose:youtube -- --file <metrics.json>` / `npm run brief:next` | Growth diagnostics and next-episode brief |
| `npm test` / `npm run typecheck` / `npm run lint` | Checks |

Rules for all of it: `AGENTS.md` and `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` (§9 upload, §12 Buffer).

### Mini writer lock

YouTube uploads, listing/comment/disclosure writers and every Buffer CLI command
acquire the shared `youtube-buffer` lock, including direct `npx tsx` calls and the
daily shell wrapper. The atomic mkdir lock lives at
`~/_desk/locks/youtube-buffer.lock/`; `DESK_LOCK_ROOT` overrides the root for tests.
It covers the entire command, including an upload's Buffer mirror and local
records. Dry runs also take the lock.

A held lock stops with exit **75**. Wait for the owner to finish; inspect with
`bash scripts/desk-lock.sh held-by youtube-buffer`. Acquisition never reclaims
locks automatically. After verifying the holder is dead, use
`bash scripts/desk-lock.sh release youtube-buffer`. Missing owner metadata is
held too, since another process may still be writing it.
